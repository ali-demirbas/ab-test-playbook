#!/usr/bin/env bash
# Repo consistency validation for ab-test-playbook.
#
# The content validators (validate_scenarios.py, validate_scenario_json.py) each
# check one file format well. Nothing checked the seams BETWEEN files: a skill
# whose frontmatter drifted, a markdown link to a renamed doc, or a
# ${CLAUDE_PLUGIN_ROOT}/knowledge/... reference pointing at a file that no longer
# exists. That last class is the dangerous one — it fails only mid-run, inside a
# skill, as a file the model quietly could not read. This script is the single
# entry point that runs both the content validators and those cross-file checks.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
# `|| exit` is load-bearing: this runs under `set -uo pipefail` without `-e`, so
# a failed cd would let every check below run against whatever directory the
# caller happened to be in — reporting a clean pass on a tree it never looked at.
cd "$ROOT" || exit 1
FAIL=0

err() { echo "FAIL: $1"; FAIL=1; }
ok()  { echo "  ok: $1"; }

# Count what a glob actually expanded to. A glob loop rather than `ls | wc -l`:
# a filename containing a space or newline skews a line count.
count_files() {
  local n=0 f
  for f in "$@"; do
    [ -e "$f" ] || continue
    n=$((n + 1))
  done
  printf '%s' "$n"
}

echo "== 1. Skills: frontmatter with name + description + metadata =="
# Parseability comes first. Everything below reads front matter with grep, which
# finds `description:` just as happily in a block no YAML parser can load — and
# the installers that matter (Claude Code, `npx skills add`) do parse it. This
# caught a real one: an unquoted `visual style: a Variant …` made the whole
# ab-test-card skill invisible to `npx skills add`, silently, while every other
# check here passed.
python3 scripts/check_frontmatter.py skills/*/SKILL.md agents/*.md || FAIL=1

# `updated` is deliberately not checked against git: a skill's prose can be
# edited without its behavior changing, so the date is a curated claim about the
# last substantive revision, not a mirror of the last commit touching the file.
SKILL_META_KEYS="version category updated"
for f in skills/*/SKILL.md; do
  head -1 "$f" | grep -q '^---$' || { err "$f: no frontmatter"; continue; }
  fm=$(awk '/^---$/{c++; next} c==1{print} c==2{exit}' "$f")
  echo "$fm" | grep -q '^name:' || err "$f: missing name"
  echo "$fm" | grep -q '^description:' || err "$f: missing description"
  dir=$(basename "$(dirname "$f")")
  nm=$(echo "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -1)
  [ "$nm" = "$dir" ] || err "$f: name '$nm' != directory '$dir'"
  if echo "$fm" | grep -q '^metadata:'; then
    for k in $SKILL_META_KEYS; do
      echo "$fm" | grep -q "^  $k:" || err "$f: metadata missing key '$k'"
    done
    upd=$(echo "$fm" | sed -n 's/^  updated:[[:space:]]*//p' | head -1)
    echo "$upd" | grep -Eq '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' \
      || err "$f: metadata.updated '$upd' is not YYYY-MM-DD"
    ver=$(echo "$fm" | sed -n 's/^  version:[[:space:]]*//p' | head -1)
    echo "$ver" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' \
      || err "$f: metadata.version '$ver' is not semver"
    # A closed set: an open category field drifts into one-off labels, which is
    # the same as having none at all.
    cat=$(echo "$fm" | sed -n 's/^  category:[[:space:]]*//p' | head -1)
    case "$cat" in
      router|recommend|generate|audit|analyze|render) ;;
      *) err "$f: invalid metadata.category '$cat'" ;;
    esac
  else
    err "$f: missing metadata block"
  fi
done
ok "$(count_files skills/*/SKILL.md) skills checked"

echo "== 2. Agents: frontmatter with name + description + tools =="
# The review agents are spawned BY NAME from the skills (CLAUDE.md kural 17). A
# name that drifts from its filename is a spawn that silently finds nothing.
for f in agents/*.md; do
  [ -e "$f" ] || continue
  head -1 "$f" | grep -q '^---$' || { err "$f: no frontmatter"; continue; }
  fm=$(awk '/^---$/{c++; next} c==1{print} c==2{exit}' "$f")
  base=$(basename "$f" .md)
  nm=$(echo "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -1)
  [ "$nm" = "$base" ] || err "$f: name '$nm' != filename '$base'"
  echo "$fm" | grep -q '^description:' || err "$f: missing description"
  echo "$fm" | grep -q '^tools:' || err "$f: missing tools"
  # An agent nothing spawns is dead weight; a spawn naming a missing agent is
  # worse. Both directions are checked here.
  grep -rqF "agents/$base" skills/ CLAUDE.md \
    || err "$f: no skill or CLAUDE.md rule references agents/$base — dead agent"
done
ok "$(count_files agents/*.md) agents checked"

echo "== 3. Plugin manifests parse =="
for m in .claude-plugin/plugin.json .claude-plugin/marketplace.json; do
  if python3 -c "import json,sys; json.load(open('$m'))" 2>/dev/null; then
    ok "$m parses"
  else
    err "$m is not valid JSON"
  fi
done

echo "== 4. Scenario archive format =="
# if-then-else, not `A && B || C`: with the latter, a failure in the success
# branch would also run the error branch and report a passing archive as broken.
if python3 scripts/validate_scenarios.py >/dev/null 2>&1; then
  ok "scenario archive conforms (validate_scenarios.py)"
else
  err "scenario archive failed validate_scenarios.py — run it directly for detail"
fi

echo "== 5. Scenario JSON against the schema =="
for j in examples/*.json; do
  [ -e "$j" ] || continue
  # scenario-card-input.json is the CARD builder's input shape, not a scenario
  # definition — it is exercised by section 6 instead.
  [ "$(basename "$j")" = "scenario-card-input.json" ] && continue
  if python3 scripts/validate_scenario_json.py "$j" >/dev/null 2>&1; then
    ok "$j conforms to templates/scenario.schema.json"
  else
    err "$j failed validate_scenario_json.py — run it directly for detail"
  fi
done

echo "== 6. Card builder produces a card from the template =="
if python3 scripts/build_card.py \
     --template templates/scenario-card.html \
     --scenario examples/scenario-card-input.json \
     --out /tmp/abtest-validate-card.html >/dev/null 2>&1; then
  ok "build_card.py builds and self-verifies against drift"
  rm -f /tmp/abtest-validate-card.html
else
  err "build_card.py failed — the template and the builder have diverged"
fi

echo "== 7. Internal links (markdown + published HTML) =="
python3 - <<'PY' || FAIL=1
import json, os, re, sys
failed = False
checked = 0

# docs/index.html is the published landing page and links into docs/demo/. It is
# HTML, not markdown, so the markdown link scanner below never sees it — and a
# broken href there ships a 404 on the live site with nothing in the repo able
# to notice. Checked first, on its own terms.
href_re = re.compile(r'(?:href|src)="([^"#?]+)"')
for page in ('docs/index.html',):
    if not os.path.exists(page):
        continue
    base = os.path.dirname(page)
    with open(page, encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            for m in href_re.finditer(line):
                target = m.group(1)
                if target.startswith(('http://', 'https://', 'mailto:', 'data:', '//')):
                    continue
                checked += 1
                if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                    print(f"FAIL: {page}:{lineno} -> {target} (broken)")
                    failed = True
# Any relative target, not just .md/.json. A narrower extension list leaves every
# link to a template's .html, a screenshot's .png, a script's .py, or a bare
# directory unchecked — precisely the targets most likely to be renamed, since
# no reader following prose notices them.
link_re = re.compile(r'\]\(([^)\s]+?)(?:#[^)]*)?\)')
SKIP_PREFIXES = ('http://', 'https://', 'mailto:', 'tel:', '#', '${')

# A link to this repo's own GitHub Pages site is an internal link written the
# long way — skipping it as "external" is how the published site ends up
# shipping a 404 that nothing in the repo can see.
with open('.claude-plugin/plugin.json', encoding='utf-8') as f:
    repo_url = json.load(f)['repository']
owner, repo = repo_url.rstrip('/').split('/')[-2:]
SITE_PREFIX = f"https://{owner}.github.io/{repo}/"

for dirpath, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs
               if d not in ('.git', 'node_modules', 'output', '__pycache__')
               and not os.path.exists(os.path.join(dirpath, d, '.git'))]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                for m in link_re.finditer(line):
                    target = m.group(1)
                    if '<' in target or '{' in target:  # placeholder
                        continue
                    if target.startswith(SITE_PREFIX):
                        # Pages serves docs/ as the site root.
                        rel = target[len(SITE_PREFIX):] or 'index.html'
                        resolved = os.path.normpath(os.path.join('docs', rel))
                        label = f"{target} (published site)"
                    elif target.startswith(SKIP_PREFIXES):
                        continue
                    else:
                        resolved = os.path.normpath(os.path.join(dirpath, target))
                        label = target
                    checked += 1
                    if not os.path.exists(resolved):
                        print(f"FAIL: {path}:{lineno} -> {label} (broken)")
                        failed = True
if failed:
    sys.exit(1)
print(f"  ok: {checked} internal links resolve")
PY

echo "== 8. \${CLAUDE_PLUGIN_ROOT} path references =="
python3 - <<'PY' || FAIL=1
import os, re, sys
# Skills address knowledge files at runtime as ${CLAUDE_PLUGIN_ROOT}/knowledge/…,
# which is a plain string inside backticks, not a markdown link — so section 7
# never sees any of them. A renamed knowledge file leaves these pointing at
# nothing and fails only mid-run, inside a skill, as a file the model quietly
# could not read.
ref_re = re.compile(r'\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)')
failed = False
checked = 0
for dirpath, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs
               if d not in ('.git', 'node_modules', 'output', '__pycache__')
               and not os.path.exists(os.path.join(dirpath, d, '.git'))]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                for m in ref_re.finditer(line):
                    # trailing sentence punctuation is not part of the path
                    target = m.group(1).rstrip('.,;:)`')
                    if '<' in target:  # placeholder like <slug>.html
                        continue
                    checked += 1
                    if not os.path.exists(target):
                        print(f"FAIL: {path}:{lineno} -> ${{CLAUDE_PLUGIN_ROOT}}/{target} (no such path)")
                        failed = True
if failed:
    sys.exit(1)
print(f"  ok: {checked} plugin-root references resolve")
PY

echo "== 9. Rule references point at rules that exist =="
python3 - <<'PY' || FAIL=1
import os, re, sys
# Skills and agents cite the binding rules by number — "kural 17" in the Turkish
# files (CLAUDE.md, knowledge/, agents/), "rule 17" in the English skill bodies.
# CLAUDE.md is the only place those numbers are defined; a citation past the end
# of the list is a rule the reader will look for and not find.
with open('CLAUDE.md', encoding='utf-8') as f:
    rules = re.findall(r'^(\d+)\.\s+\*\*', f.read(), re.M)
highest = max(int(r) for r in rules) if rules else 0
if highest == 0:
    print("FAIL: CLAUDE.md: no numbered rules found")
    sys.exit(1)

cite_re = re.compile(r'\b(?:kural|rule)\s+(\d+)', re.I)
failed = False
checked = 0
for dirpath, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs
               if d not in ('.git', 'node_modules', 'output', '__pycache__')
               and not os.path.exists(os.path.join(dirpath, d, '.git'))]
    for fn in files:
        if not fn.endswith('.md'):
            continue
        path = os.path.join(dirpath, fn)
        with open(path, encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                for m in cite_re.finditer(line):
                    n = int(m.group(1))
                    checked += 1
                    if n < 1 or n > highest:
                        print(f"FAIL: {path}:{lineno} cites '{m.group(0)}' but CLAUDE.md defines 1-{highest}")
                        failed = True
if failed:
    sys.exit(1)
print(f"  ok: {checked} rule citations resolve against CLAUDE.md's 1-{highest}")
PY

echo "== 10. Shipped content carries no instruction-like text =="
# The archive and knowledge files are read back into context on every run. A
# line in them shaped like an instruction would be indistinguishable from one
# the user pasted, so the repo holds its own content to the same rule it holds
# user input to (CLAUDE.md rule 18).
if python3 scripts/validate_input.py knowledge/scenarios/*.md knowledge/*.md >/dev/null 2>&1; then
  ok "no instruction-like or executable-markup lines in shipped knowledge"
else
  err "validate_input.py flagged shipped content — run it directly for the quoted lines"
fi

echo "== 11. Vocabulary agrees across schema, validator and builder =="
# The same closed sets are spelled out in more than one place: the schema's
# enums, validate_scenario_json's rule checks and build_card's constants (the
# devices it can frame, the difference types whose ring placement it enforces,
# the KPI roles it draws pills for, the source/evidence tags and languages its
# footer and dictionary print). Duplicated vocabulary drifts silently — a
# device added to the schema alone would validate and then fail to render; a
# role added to the builder alone would render and never be validated.
python3 - <<'PY' || FAIL=1
import json
import sys

sys.path.insert(0, "scripts")
import build_card as bc  # noqa: E402

schema = json.load(open("templates/scenario.schema.json", encoding="utf-8"))
props = schema["properties"]
card = props["card"]["properties"]
validator = open("scripts/validate_scenario_json.py", encoding="utf-8").read()

failed = False


def same(label, schema_values, builder_values):
    global failed
    a, b = set(schema_values), set(builder_values)
    if a != b:
        print("FAIL: %s differ: schema %s, build_card %s" % (label, sorted(a), sorted(b)))
        failed = True


same("device types (scenario.device)", props["device"]["enum"], bc.DEVICES)
same("device types (card.device)", card["device"]["enum"], bc.DEVICES)
same("KPI roles", props["kpis"]["items"]["properties"]["role"]["enum"], bc.KPI_ROLES)
same("sources", props["source"]["enum"], bc.SOURCES)
same("evidence levels", props["evidence"]["properties"]["level"]["enum"], bc.EVIDENCE_LEVELS)
same("ICE tiers", props["ice"]["properties"]["tier"]["enum"], bc.ICE_TIERS)
same("languages", props["lang"]["enum"], bc.L10N.keys())
same("mockup bases", card["mockup_basis"]["enum"], bc.MOCKUP_BASES)
same("ring label positions", card["note_pos"]["enum"], bc.NOTE_POSITIONS)
# card.difference lists the English types plus their Turkish archive spellings
# (the archive's "Fark:" line); the builder maps each alias to a type.
same("difference types", card["difference"]["enum"], set(bc.DIFFERENCES) | set(bc.DIFFERENCE_TR))
for alias, target in bc.DIFFERENCE_ALIASES.items():
    if target not in bc.DIFFERENCES:
        print("FAIL: build_card maps difference alias %r to unknown type %r" % (alias, target))
        failed = True

# Every language prints every word the card frame needs.
needed = set(bc.L10N["tr"])
for lang, words in bc.L10N.items():
    if set(words) != needed:
        print("FAIL: build_card L10N[%r] keys differ from L10N['tr']: %s" % (lang, sorted(set(words) ^ needed)))
        failed = True
    for group, keys in (("role", bc.KPI_ROLES), ("source", bc.SOURCES),
                        ("evidence", bc.EVIDENCE_LEVELS), ("ice", bc.ICE_TIERS)):
        missing = set(keys) - set(words[group])
        if missing:
            print("FAIL: build_card L10N[%r][%r] has no label for %s" % (lang, group, sorted(missing)))
            failed = True

for role in ("primary", "guardrail"):
    if '"%s"' % role not in validator and "'%s'" % role not in validator:
        print("FAIL: validator does not mention KPI role %r defined in the schema" % role)
        failed = True

if failed:
    sys.exit(1)
print("  ok: devices %s, KPI roles, sources, evidence levels, difference types and languages %s"
      " agree across schema, validator and builder" % (sorted(bc.DEVICES), sorted(bc.L10N)))
PY

echo "== 12. Skill description contract (sibling refs + 'Use when') =="
# The router relies on the description alone to decide whether a skill fires
# (progressive disclosure: the body never loads until picked). Two things can
# silently break that contract: a description that names a sibling skill which
# has since been renamed or removed (a dead pointer nothing else notices — the
# reader just never finds the skill it was told to look at), and a description
# missing the "Use when ..." sentence the routing logic depends on.
python3 - <<'PY' || FAIL=1
import glob
import re
import sys

SKILL_DIR_RE = re.compile(r'^skills/([a-z-]+)/SKILL\.md$')
skill_names = set()
for f in glob.glob("skills/*/SKILL.md"):
    m = SKILL_DIR_RE.match(f)
    if m:
        skill_names.add(m.group(1))

failed = False
checked = 0
for f in sorted(glob.glob("skills/*/SKILL.md")):
    own = SKILL_DIR_RE.match(f).group(1)
    with open(f, encoding="utf-8") as fh:
        text = fh.read()
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    m = re.search(r'^description:\s*(.+)$', fm, re.M)
    desc = m.group(1) if m else ""
    checked += 1

    if "Use when" not in desc:
        print(f"FAIL: {f}: description has no 'Use when ...' sentence")
        failed = True

    # `ab-test-*` is a glob standing for "any ab-test skill", not a literal
    # reference — the [a-z]+ requirement (no bare "ab-test", no "ab-test-*")
    # excludes it and the router's own name without a separate special case.
    for ref in set(re.findall(r'\bab-test-[a-z]+\b', desc)) - {own}:
        if ref not in skill_names:
            print(f"FAIL: {f}: description points at '{ref}', no such skill directory")
            failed = True

if failed:
    sys.exit(1)
print(f"  ok: {checked} skill descriptions carry 'Use when' and resolve their sibling references")
PY

echo "== 13. Stated counts match the archive and CLAUDE.md =="
# The scenario total and the rule count are quoted in prose all over the public
# docs, and nothing tied those numbers to their source: a scenario batch landed
# and docs/llms.txt kept saying 179 for several releases. The source of truth is
# the validator's own TOPLAM line and the highest numbered rule in CLAUDE.md.
# The patterns are deliberately narrow (a number directly before "scenario",
# "senaryo" or "rules", the badge, "archive of N"): per-turn counts such as
# "1-5 scenarios" are excluded by the lookbehind, a phrase like "5 full
# scenarios" never matches, and single-digit numbers are skipped outright (they
# are per-turn counts or "five rules it will not bend", never a total), so a hit
# is always a claim about the total.
python3 - <<'PY' || FAIL=1
import re
import subprocess
import sys

out = subprocess.run([sys.executable, "scripts/validate_scenarios.py"],
                     capture_output=True, text=True).stdout
m = re.search(r"TOPLAM:\s*(\d+)", out)
if not m:
    print("FAIL: could not read the scenario total (TOPLAM) from validate_scenarios.py")
    sys.exit(1)
scenarios = int(m.group(1))

with open("CLAUDE.md", encoding="utf-8") as f:
    rules = max(int(n) for n in re.findall(r"^(\d+)\.\s+\*\*", f.read(), re.M))

FILES = ["README.md", "README.tr.md", "docs/llms.txt", "docs/index.html",
         "docs/architecture.md", "CONTRIBUTING.md",
         ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"]
NUM = r"(?<![\d.,/-])(\d+)"
SCENARIO_RES = [
    re.compile(NUM + r"[- ](?:(?:curated|experiment|shipped|deney) )?(?:scenario|senaryo)", re.I),
    re.compile(r"archive of " + NUM, re.I),
    re.compile(r"scenarios-(\d+)-"),  # the shields badge; NUM's lookbehind would skip it
]
RULE_RES = [re.compile(NUM + r" (?:non-negotiable |binding |bağlayıcı )?(?:rules|kural)\b", re.I)]

failed = False
checked = 0
for path in FILES:
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        continue
    for lineno, line in enumerate(lines, 1):
        for kind, regexes, want in (("scenario", SCENARIO_RES, scenarios),
                                    ("rule", RULE_RES, rules)):
            for rx in regexes:
                for hit in rx.finditer(line):
                    if int(hit.group(1)) < 10:
                        continue
                    checked += 1
                    if int(hit.group(1)) != want:
                        print(f"FAIL: {path}:{lineno} says {hit.group(0)!r}, "
                              f"but the real {kind} count is {want}")
                        failed = True
if failed:
    sys.exit(1)
print(f"  ok: {checked} stated counts match {scenarios} scenarios and {rules} rules")
PY

echo "== 14. Skills and agents address shipped files via \${CLAUDE_PLUGIN_ROOT} =="
# At runtime the working directory is the USER's project, not this repo, so a
# bare `knowledge/scenarios/x.md` in a skill resolves to nothing and the model
# silently reads no archive. Section 8 only sees paths that already carry the
# prefix; this catches the ones that forgot it. Code fences are checked too: in
# a skill, a fenced command is something the model runs from the user's cwd,
# so a relative `scripts/...` there is the same bug. The front matter is skipped
# — the description is routing prose for the picker, never resolved as a path.
python3 - <<'PY' || FAIL=1
import glob
import re
import sys

bare_re = re.compile(r"(?<![\w./{}$-])(?:knowledge|scripts|templates)/")
failed = False
checked = 0
for path in sorted(glob.glob("skills/*/SKILL.md") + glob.glob("agents/*.md")):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    checked += 1
    for lineno in range(start, len(lines)):
        for hit in bare_re.finditer(lines[lineno]):
            print(f"FAIL: {path}:{lineno + 1}: bare '{hit.group(0)}' path — "
                  "prefix it with ${CLAUDE_PLUGIN_ROOT}/")
            failed = True
if failed:
    sys.exit(1)
print(f"  ok: {checked} skill/agent bodies use only ${{CLAUDE_PLUGIN_ROOT}}-prefixed paths")
PY

echo "== 15. Skill descriptions fit the 1024-character limit =="
# The description is the only text the picker sees before a skill loads, and
# installers enforce a 1024-character ceiling on it. A description that grows
# past it is truncated or rejected at install time, usually losing the routing
# hints at its end — "To check ..., see ab-test-audit" — first.
python3 - <<'PY' || FAIL=1
import glob
import re
import sys

LIMIT = 1024
failed = False
longest = 0
for path in sorted(glob.glob("skills/*/SKILL.md")):
    text = open(path, encoding="utf-8").read()
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    m = re.search(r"^description:\s*(.+)$", fm, re.M)
    desc = m.group(1).strip() if m else ""
    if len(desc) >= 2 and desc[0] == desc[-1] and desc[0] in "\"'":
        desc = desc[1:-1]
    longest = max(longest, len(desc))
    if len(desc) > LIMIT:
        print(f"FAIL: {path}: description is {len(desc)} characters (limit {LIMIT})")
        failed = True
if failed:
    sys.exit(1)
print(f"  ok: every skill description is within {LIMIT} characters (longest {longest})")
PY

echo "== 16. Gemini CLI extension matches its sources =="
# .gemini/extensions/ is generated from CLAUDE.md, skills/ and agents/, not
# hand-maintained — the same reasoning as docs/llms-full.txt below, and the
# same failure mode: a source file edited without regenerating ships an
# out-of-date second copy of the plugin under a different runtime.
if python3 scripts/build_gemini.py --check >/dev/null 2>&1; then
  ok "gemini extension is in sync with CLAUDE.md, skills and agents"
else
  err ".gemini/extensions/ is stale — run: python3 scripts/build_gemini.py"
fi

echo "== 17. Published Markdown bundle matches its sources =="
# docs/llms-full.txt is a concatenation of the core docs. Its only value is
# being current, and a stale bundle is worse than none: it answers questions
# with documentation the repo no longer ships.
if python3 scripts/build_llms_full.py --check >/dev/null 2>&1; then
  ok "docs/llms-full.txt is in sync with README, CLAUDE.md, architecture, FAQ and methodology"
else
  err "docs/llms-full.txt is stale — run: python3 scripts/build_llms_full.py"
fi

echo
if [ "$FAIL" = 1 ]; then
  echo "VALIDATION FAILED"; exit 1
else
  echo "ALL CHECKS PASSED"; exit 0
fi
