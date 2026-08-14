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
# abtest-card skill invisible to `npx skills add`, silently, while every other
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
# Skills and agents cite the binding rules by number ("kural 17"). CLAUDE.md is
# the only place those numbers are defined; a citation past the end of the list
# is a rule the reader will look for and not find.
with open('CLAUDE.md', encoding='utf-8') as f:
    rules = re.findall(r'^(\d+)\.\s+\*\*', f.read(), re.M)
highest = max(int(r) for r in rules) if rules else 0
if highest == 0:
    print("FAIL: CLAUDE.md: no numbered rules found")
    sys.exit(1)

cite_re = re.compile(r'kural\s+(\d+)', re.I)
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
                        print(f"FAIL: {path}:{lineno} cites 'kural {n}' but CLAUDE.md defines 1-{highest}")
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
# The same closed sets are spelled out in more than one place: KPI roles and
# device types live in the schema's enums, in validate_scenario_json's rule
# check, and in build_card's device branch. Duplicated vocabulary drifts
# silently — a role added to the schema alone would validate and then never be
# enforced.
python3 - <<'PY' || FAIL=1
import json
import re
import sys

schema = json.load(open("templates/scenario.schema.json", encoding="utf-8"))
roles = set(schema["properties"]["kpis"]["items"]["properties"]["role"]["enum"])
devices = set(schema["properties"]["device"]["enum"])

builder = open("scripts/build_card.py", encoding="utf-8").read()
validator = open("scripts/validate_scenario_json.py", encoding="utf-8").read()

failed = False

# build_card accepts the card-renderable devices; "both" is a definition-level
# value with no single skeleton, so it is legitimately absent there.
builder_devices = set(re.findall(r'device not in \(([^)]*)\)', builder))
if builder_devices:
    accepted = set(re.findall(r'"([a-z]+)"', builder_devices.pop()))
    unknown = accepted - devices
    if unknown:
        print("FAIL: build_card accepts device(s) the schema does not define: %s" % sorted(unknown))
        failed = True

for role in ("primary", "guardrail"):
    if role not in roles:
        print("FAIL: schema no longer defines KPI role %r, but the validator enforces it" % role)
        failed = True
    if '"%s"' % role not in validator and "'%s'" % role not in validator:
        print("FAIL: validator does not mention KPI role %r defined in the schema" % role)
        failed = True

if failed:
    sys.exit(1)
print("  ok: KPI roles %s and device types %s agree across schema, validator and builder"
      % (sorted(roles), sorted(devices)))
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

    # `abtest-*` is a glob standing for "any abtest skill", not a literal
    # reference — the [a-z]+ requirement (no bare "abtest", no "abtest-*")
    # excludes it and the router's own name without a separate special case.
    for ref in set(re.findall(r'\babtest-[a-z]+\b', desc)) - {own}:
        if ref not in skill_names:
            print(f"FAIL: {f}: description points at '{ref}', no such skill directory")
            failed = True

if failed:
    sys.exit(1)
print(f"  ok: {checked} skill descriptions carry 'Use when' and resolve their sibling references")
PY

echo "== 13. Gemini CLI extension matches its sources =="
# .gemini/extensions/ is generated from CLAUDE.md, skills/ and agents/, not
# hand-maintained — the same reasoning as docs/llms-full.txt below, and the
# same failure mode: a source file edited without regenerating ships an
# out-of-date second copy of the plugin under a different runtime.
if python3 scripts/build_gemini.py --check >/dev/null 2>&1; then
  ok "gemini extension is in sync with CLAUDE.md, skills and agents"
else
  err ".gemini/extensions/ is stale — run: python3 scripts/build_gemini.py"
fi

echo "== 14. Published Markdown bundle matches its sources =="
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
