#!/usr/bin/env python3
"""Build a Gemini CLI extension from the same skills/agents/rules this repo
ships as a Claude Code plugin — so the plugin reaches Gemini CLI users too,
without a second, hand-maintained copy of the content to keep in sync.

This is NOT a blind concatenation of the SKILL.md files (that is what a naive
port would do, and it would silently ship two things that don't work in
Gemini CLI):

  1. Every skill and agent addresses its own knowledge files and CLAUDE.md
     through `${CLAUDE_PLUGIN_ROOT}`, a Claude Code plugin-install variable
     with no meaning outside it. Left as-is, an instruction to read
     `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` would be inert prose in
     Gemini CLI. Rewritten here to `${extensionPath}`, the documented Gemini
     CLI extension-install-path equivalent.
  2. The two review agents (CLAUDE.md rule 17) are Claude Code subagents,
     declared with Claude Code tool names (Read, Grep, Glob, Bash). Gemini CLI
     supports bundled extension subagents too, but under a different tool
     vocabulary (read_file, grep_search, glob, run_shell_command) — an
     unmapped name would silently do nothing rather than fail loudly, so
     TOOL_MAP below is exhaustive on purpose and this script refuses to build
     if an agent uses a tool it doesn't cover.

CLAUDE.md's rule text is inlined in full, not linked — every skill and agent
cites it by rule number ("kural 17"), and Gemini CLI has no plugin-relative
file-loading step equivalent to Claude Code reading it at the top of a skill
run. knowledge/ is NOT inlined: it is the 179-scenario archive, meant to be
read selectively by page/stage, and inlining it would both bloat the context
file past what any session needs and defeat the progressive-disclosure design
the router relies on — skills still address it via the rewritten
`${extensionPath}/knowledge/...` path.

Usage:
  build_gemini.py           # write .gemini/extensions/<plugin>/...
  build_gemini.py --check   # exit 1 if the written files would differ (CI)
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_JSON = os.path.join(ROOT, ".claude-plugin", "plugin.json")
CLAUDE_MD = os.path.join(ROOT, "CLAUDE.md")
SKILLS_DIR = os.path.join(ROOT, "skills")
AGENTS_DIR = os.path.join(ROOT, "agents")
EXT_ROOT = os.path.join(ROOT, ".gemini", "extensions")

# Claude Code tool name -> Gemini CLI subagent tool name (per Gemini CLI's
# subagent frontmatter schema). The only place this mapping lives — a new
# tool added to an agent's frontmatter with no entry here fails the build
# instead of shipping a Gemini subagent with a tool name that resolves to
# nothing.
TOOL_MAP = {
    "Read": "read_file",
    "Write": "write_file",
    "Edit": "replace",
    "Grep": "grep_search",
    "Glob": "glob",
    "Bash": "run_shell_command",
}


def die(msg):
    sys.stderr.write("build_gemini: %s\n" % msg)
    sys.exit(2)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def rewrite_plugin_root(text):
    return text.replace("${CLAUDE_PLUGIN_ROOT}", "${extensionPath}")


def translate_tools_line(match):
    prefix, val = match.group(0).split(":", 1)
    names = [t.strip() for t in val.split(",") if t.strip()]
    mapped = []
    for n in names:
        if n not in TOOL_MAP:
            die("agent tool '%s' has no Gemini CLI mapping in TOOL_MAP — add one" % n)
        mapped.append(TOOL_MAP[n])
    return prefix + ": " + ", ".join(mapped)


def build_agent_file(text):
    """Same frontmatter and body, `tools:` translated, plugin-root rewritten.
    Only the tools line is touched — name/description stay byte-identical to
    the Claude Code agent, so the two never drift apart in meaning."""
    text = rewrite_plugin_root(text)
    return re.sub(r"^tools:.*$", translate_tools_line, text, count=1, flags=re.M)


def build_files():
    plugin = json.loads(read(PLUGIN_JSON))
    name = plugin["name"]
    # plugin.json's description names the Claude Code plugin specifically
    # ("... for Claude Code."); reused verbatim it would misdescribe this
    # extension inside Gemini CLI's own extension listing.
    description = plugin["description"].replace(" for Claude Code.", ".")
    version = plugin.get("version", "0.1.0")
    ext_dir = os.path.join(EXT_ROOT, name)

    files = {}

    files[os.path.join(ext_dir, "gemini-extension.json")] = json.dumps(
        {
            "name": name,
            "version": version,
            "description": description,
            "contextFileName": "GEMINI.md",
        },
        indent=2,
    ) + "\n"

    parts = [
        "# %s\n\n%s\n" % (name, description),
        "You are an expert assistant for %s with the skills below available. "
        "Apply whichever skill matches the user's request; the \"Binding "
        "rules\" section is non-negotiable and applies to every skill's "
        "output — this is the same rule set the Claude Code plugin version "
        "of this tool enforces, generated from the same source file.\n"
        % name,
        "## Binding rules (CLAUDE.md)\n\n" + rewrite_plugin_root(read(CLAUDE_MD)).strip() + "\n",
    ]

    skill_dirs = sorted(
        d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md"))
    )
    parts.append("## Skills\n")
    for d in skill_dirs:
        text = rewrite_plugin_root(read(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        parts.append(text.strip() + "\n")

    agent_files = sorted(f for f in os.listdir(AGENTS_DIR) if f.endswith(".md")) if os.path.isdir(AGENTS_DIR) else []
    if agent_files:
        parts.append(
            "## Review agents\n\n"
            "This extension bundles the adversarial review agents the skills "
            "above reference, under `agents/`. Invoke them the way a skill's "
            "text says to — do not skip a review step just because no tool "
            "call syntax is shown inline.\n"
        )

    files[os.path.join(ext_dir, "GEMINI.md")] = "\n".join(p.rstrip() + "\n" for p in parts).rstrip() + "\n"

    for fn in agent_files:
        text = read(os.path.join(AGENTS_DIR, fn))
        files[os.path.join(ext_dir, "agents", fn)] = build_agent_file(text)

    return files


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="exit 1 if written output would differ")
    args = ap.parse_args(argv)

    files = build_files()

    if args.check:
        stale = []
        for path, content in files.items():
            if not os.path.isfile(path) or read(path) != content:
                stale.append(os.path.relpath(path, ROOT))
        if stale:
            sys.stderr.write(
                "build_gemini --check: stale or missing (%d): %s\n"
                % (len(stale), ", ".join(stale))
            )
            return 1
        print("gemini extension is in sync with its sources (%d files)" % len(files))
        return 0

    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    print("wrote %d files under %s" % (len(files), os.path.relpath(EXT_ROOT, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
