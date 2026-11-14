#!/usr/bin/env python3
"""Package each skill as a ZIP for upload on claude.ai (Settings > Skills).

A claude.ai skill is one folder in one ZIP: the archive's top level must be
`<skill-name>/`, with `<skill-name>/SKILL.md` inside it, and the folder name
must match the `name` field. Uploading only SKILL.md would ship the same
broken thing as `npx skills add`: every skill reads its binding rules
(CLAUDE.md), the scenario archive, templates and scripts through
`${CLAUDE_PLUGIN_ROOT}`, a Claude Code plugin variable that means nothing on
claude.ai. So each ZIP here is self-contained:

  1. The shared runtime (CLAUDE.md, knowledge/, templates/, agents/, the
     scripts the text actually runs plus the sibling modules they import,
     and every other file referenced through `${CLAUDE_PLUGIN_ROOT}/...`) is
     copied next to SKILL.md, keeping its layout, so the scripts' own
     root-relative lookups (scripts/ -> ../knowledge/) still work.
  2. `${CLAUDE_PLUGIN_ROOT}` becomes `${SKILL_DIR}` in every bundled text
     file, and SKILL.md gets one line after its front matter saying what
     `${SKILL_DIR}` is. Shell commands in the text keep working once the
     variable is set; nothing is guessed from the working directory.
  3. claude.ai documents a 200-character description limit (the Agent Skills
     spec allows 1,024, which ours use). SHORT_DESCRIPTIONS holds a reviewed
     short description per skill; nothing is truncated automatically. Each
     entry records a hash of the source description it was written from, so
     a changed source description is reported as needing a new review.

The ZIPs are release attachments, never committed. Stdlib only, Python 3.9+.

Usage:
  build_skill_zips.py --out DIR            # one <skill>.zip per skill
  build_skill_zips.py --out DIR --skill ab-test-design
  build_skill_zips.py --out DIR --strict   # a stale short description fails
"""
import argparse
import hashlib
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")

# claude.ai upload limits. The description limit is documented in the
# custom-skills help article; 30 MB uncompressed is the documented limit of
# the skills API and is used here as a local safety bound.
MAX_DESCRIPTION = 200
MAX_NAME = 64
MAX_UNCOMPRESSED = 30 * 1024 * 1024

# Always bundled: the skills cite these as a set (rule numbers, the archive,
# the template + schema pair, the reviewer checklists), not file by file.
SHARED = ("CLAUDE.md", "knowledge", "templates", "agents")

# skill -> (short description, sha256 of the source description it was
# reviewed against). Regenerate the hash with --print-hashes after a review.
SHORT_DESCRIPTIONS = {
    "ab-test": (
        "A/B test router for A/B test, split test, experiment or CRO requests: "
        "routes to suggest, design, audit or card. Results and sample-size "
        "questions get a short out-of-scope answer.",
        "2e7c90369ebbef7d94128b4e72649b48b38d5d393314a35de4d9578251713bb5",
    ),
    "ab-test-suggest": (
        "Suggests up to three ranked A/B test ideas for a page type or journey "
        "stage from a 221-scenario archive, when no page of the user's own is "
        "shared. Each idea becomes an HTML card.",
        "7426c7fc33c48cb4a6dff66cf2cb05f7338822f9c9f444035996deab0cb1da24",
    ),
    "ab-test-design": (
        "Designs a new single-variable A/B test for the user's own page, "
        "screenshot, URL or flow description: hypothesis, one variable, primary "
        "KPI, guardrail, priority and an HTML card.",
        "f7eda3bbc2c1e523ab92e6c6d8f83ba8482befa89d630d46ca74f54053f41024",
    ),
    "ab-test-audit": (
        "Audits an A/B test plan, brief or variant pair before launch: "
        "confounds, multi-variable changes, proxy KPIs, missing guardrails, "
        "dark patterns and regulated-flow gates.",
        "432ac9a519d351f00c6cb4ec33a079eea06d0a80bad40eda5787f5374603e94d",
    ),
    "ab-test-card": (
        "Renders an A/B test scenario record as a 16:9 HTML card with Variant A "
        "and B mockups side by side and the changed element ringed. Runs after "
        "ab-test-suggest and ab-test-design.",
        "6f6c9d336f924de0180df5cf0b6ac22f87602e6e50aa877f36ceac5f795a247f",
    ),
}

PLUGIN_ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}"
SKILL_DIR_VAR = "${SKILL_DIR}"
TEXT_EXT = (".md", ".py", ".mjs", ".js", ".json", ".html", ".txt", ".sh")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./*-]+)")
SCRIPT_REF_RE = re.compile(r"\bscripts/([A-Za-z0-9_-]+\.(?:py|mjs))\b")
IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+([A-Za-z0-9_]+)", re.M)


class BuildError(Exception):
    pass


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def split_front_matter(text):
    if not text.startswith("---\n"):
        raise BuildError("no front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise BuildError("unterminated front matter")
    return text[4:end], text[end + 5:]


def field(fm, key):
    """A top-level scalar from front matter, unquoted. The skills keep
    `name` and `description` on one line (check_frontmatter.py enforces
    that they parse), so a line match is enough here."""
    m = re.search(r"^%s:[ \t]*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        raise BuildError("front matter has no '%s'" % key)
    val = m.group(1).strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        val = val[1:-1]
    return val


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def yaml_quote(text):
    return '"%s"' % text.replace("\\", "\\\\").replace('"', '\\"')


def skill_names():
    return sorted(
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
    )


def list_files(rel):
    """Repo-relative file paths under `rel` (a file or a directory),
    skipping caches and OS litter."""
    path = os.path.join(ROOT, rel)
    if os.path.isfile(path):
        return [rel]
    out = []
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = sorted(d for d in dirnames if d != "__pycache__" and not d.startswith("."))
        for fn in sorted(filenames):
            if fn.startswith(".") or fn.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/"))
    return out


def runtime_files(texts):
    """Every repo file the bundle needs: SHARED, each file referenced via
    ${CLAUDE_PLUGIN_ROOT}/..., and each script the text names, closed over
    the sibling modules those scripts import."""
    files = set()
    for rel in SHARED:
        if os.path.exists(os.path.join(ROOT, rel)):
            files.update(list_files(rel))

    pending = list(texts)
    seen_scripts = set()
    while pending:
        text = pending.pop()
        for m in REF_RE.finditer(text):
            ref = m.group(1).rstrip(".")
            if "*" in ref or "<" in ref:
                ref = ref.split("*", 1)[0].rsplit("/", 1)[0]
            if ref and os.path.exists(os.path.join(ROOT, ref)):
                for f in list_files(ref.rstrip("/")):
                    files.add(f)
        for m in SCRIPT_REF_RE.finditer(text):
            name = m.group(1)
            if name in seen_scripts or not os.path.isfile(os.path.join(ROOT, "scripts", name)):
                continue
            seen_scripts.add(name)
            rel = "scripts/" + name
            files.add(rel)
            if name.endswith(".py"):
                src = read(os.path.join(ROOT, rel))
                for mod in IMPORT_RE.findall(src):
                    sib = mod + ".py"
                    if os.path.isfile(os.path.join(ROOT, "scripts", sib)):
                        pending.append("scripts/" + sib)
    return sorted(files)


def rewrite(text):
    return text.replace(PLUGIN_ROOT_VAR, SKILL_DIR_VAR)


def skill_md(name, text, strict, warnings):
    fm, body = split_front_matter(text)
    if field(fm, "name") != name:
        raise BuildError("%s: name '%s' != folder" % (name, field(fm, "name")))
    if name not in SHORT_DESCRIPTIONS:
        raise BuildError("%s: no reviewed short description in SHORT_DESCRIPTIONS" % name)
    short, reviewed_hash = SHORT_DESCRIPTIONS[name]
    if len(short) > MAX_DESCRIPTION:
        raise BuildError("%s: short description is %d characters (max %d)"
                         % (name, len(short), MAX_DESCRIPTION))
    if any(c in short for c in "<>"):
        raise BuildError("%s: short description contains '<' or '>'" % name)
    if sha256(field(fm, "description")) != reviewed_hash:
        msg = ("%s: the source description changed since its short description "
               "was reviewed; review it, then update the hash (--print-hashes)" % name)
        if strict:
            raise BuildError(msg)
        warnings.append(msg)
    fm = re.sub(r"^description:.*$", lambda _m: "description: " + yaml_quote(short),
                fm, count=1, flags=re.M)
    preamble = (
        "> Packaged for claude.ai. `%s` below is this skill's own folder, the one "
        "holding this SKILL.md, `CLAUDE.md`, `knowledge/`, `templates/`, "
        "`scripts/` and `agents/`. Before the first shell command, set it: "
        "`SKILL_DIR=<absolute path of that folder>`.\n\n" % SKILL_DIR_VAR
    )
    return "---\n%s\n---\n%s%s" % (fm, preamble, rewrite(body))


def build_zip(name, out_dir, strict=False, warnings=None):
    """Write <out_dir>/<name>.zip and return (path, member list)."""
    if warnings is None:
        warnings = []
    if not NAME_RE.match(name) or len(name) > MAX_NAME:
        raise BuildError("%s: not a valid skill name" % name)
    if "anthropic" in name or "claude" in name:
        raise BuildError("%s: skill names may not contain reserved words" % name)
    src = read(os.path.join(SKILLS_DIR, name, "SKILL.md"))
    shared_texts = [src]
    for rel in SHARED:
        for f in list_files(rel) if os.path.exists(os.path.join(ROOT, rel)) else []:
            if f.endswith(".md"):
                shared_texts.append(read(os.path.join(ROOT, f)))
    files = runtime_files(shared_texts)

    entries = [(name + "/SKILL.md", skill_md(name, src, strict, warnings).encode("utf-8"))]
    for rel in files:
        path = os.path.join(ROOT, rel)
        if rel.endswith(TEXT_EXT):
            data = rewrite(read(path)).encode("utf-8")
        else:
            with open(path, "rb") as fh:
                data = fh.read()
        entries.append((name + "/" + rel, data))

    total = sum(len(d) for _, d in entries)
    if total > MAX_UNCOMPRESSED:
        raise BuildError("%s: %d bytes uncompressed (max %d)" % (name, total, MAX_UNCOMPRESSED))

    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, name + ".zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for arc, data in entries:
            # Fixed timestamp: the same commit gives the same archive bytes.
            info = zipfile.ZipInfo(arc, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
    return out, [arc for arc, _ in entries]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", help="output directory for the ZIPs")
    ap.add_argument("--skill", action="append", help="build only this skill (repeatable)")
    ap.add_argument("--strict", action="store_true",
                    help="fail when a source description changed since its review")
    ap.add_argument("--print-hashes", action="store_true",
                    help="print each skill's source description hash and exit")
    args = ap.parse_args(argv)

    names = skill_names()
    if args.print_hashes:
        for n in names:
            fm, _ = split_front_matter(read(os.path.join(SKILLS_DIR, n, "SKILL.md")))
            print("%s %s" % (n, sha256(field(fm, "description"))))
        return 0
    if not args.out:
        ap.error("--out is required")
    selected = args.skill or names
    unknown = sorted(set(selected) - set(names))
    if unknown:
        ap.error("unknown skill(s): %s" % ", ".join(unknown))

    warnings = []
    try:
        for n in selected:
            path, members = build_zip(n, args.out, args.strict, warnings)
            print("%s  (%d files, %d bytes)" % (path, len(members), os.path.getsize(path)))
    except BuildError as e:
        sys.stderr.write("build_skill_zips: %s\n" % e)
        return 1
    for w in warnings:
        sys.stderr.write("warning: %s\n" % w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
