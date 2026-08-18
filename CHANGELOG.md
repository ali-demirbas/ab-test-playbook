# Changelog

All notable changes to this project are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## Unreleased

### Fixed
- **Security:** `scripts/build_card.py`'s `self_verify` only ever refused a card containing a literal `<script` — `onerror=`, `javascript:`/`vbscript:` URIs, `<iframe>`/`<object>`/`<embed>`, and `data:text/html` URIs all passed through unchecked, contradicting `CLAUDE.md` rule 18's own claim about what gets blocked. Extended the deny-list to cover all of these at the code level, with regression tests for each (including a false-positive test — the event-handler pattern needs a `\b` boundary or it matches inside ordinary words like "content="). Still a deny-list, not a full allowlist HTML sanitizer — noted honestly in the code comment, since an allowlist would need an actual HTML-parsing dependency this repo's stdlib-only convention doesn't have.
- **Methodology:** per-segment result reporting (`ab-test-results`, `ab-test-audit`) now explicitly warns against the "significant in one segment, not in another" fallacy — that's not itself evidence the true effect differs by segment (that needs a formal interaction test, which `analyze_results.py` doesn't compute); segment breakdowns are now framed as exploratory/hypothesis-generating, not a declared per-segment winner.
- **Methodology:** the two-week duration rule's rationale was getting cited inconsistently — `ab-test-results` was explaining a short-but-significant result as "regression-to-the-mean risk" when the rule's actual, documented basis (`methodology.md` → external validity) is business-cycle/temporal coverage. The decision table now names three distinct problems (underpowered-but-complete, mid-test peeking, insufficient temporal coverage) instead of one blended "wait and see."
- **Methodology:** softened the A₁/A₂/B three-arm claim from "does the same verification" as a dedicated A/A test to "provides an embedded A/A diagnostic" — a three-way split affects the primary comparison's power and isn't operationally identical.
- **Methodology:** `CLAUDE.md` rule 9 said manual copy-edit is a fallback "when the script can't be used" while `ab-test-card/SKILL.md` said the opposite for a script error ("don't fall back to building the card by hand") — the two contradicted each other. Removed the fallback allowance from `CLAUDE.md`; a script error means diagnose-and-rerun, not hand-building around every guarantee the script enforces.
- **Methodology:** the ICE score's numeric product (e.g. 336 vs. 392) can read as more precise than it is. `methodology.md` now states explicitly that it's an ordinal heuristic, not a measured expected-value model, and recommends a coarse High/Medium/Low tier when scores are close instead of quoting the product as a tiebreaker.
- **Methodology:** the local-maximum escape tactic (widen a small variable to a whole-page redesign) is a bundled-treatment test, not a rule-4 single-variable test in disguise — it answers "is the new experience better," not "which change did it." Named the distinction (diagnostic experiment vs. radical-redesign experiment) so the two aren't conflated.
- **Audit:** added a checklist item for randomization-unit/analysis-unit mismatch (randomized by user, analyzed by session, breaking the independence assumption the z-test relies on) — a common, easy-to-miss confound that wasn't explicitly checked before.

All nine findings above came from an external methodological review of the translated engine — verified against the actual source files before applying (four were confirmed and fixed as described, five were refinements/precision fixes rather than corrections of something wrong).

### Added
- "Why a playbook instead of ad-hoc testing" — a Without/With comparison table in both READMEs, and a closing line on the License section. Loosely modeled on affaan-m/ECC's "Why Choose ECC?" table and sign-off, scaled to what's actually true here — no personal-background blurb yet (parked, not skipped by oversight).

### Changed
- `CLAUDE.md` (all 18 rules), `knowledge/methodology.md` and `knowledge/mockup-style.md` translated to English. These are the files that actually demonstrate the engine's rigor (statistical hygiene, the mechanism gate, adversarial review) to a reader evaluating the repo, and until now they were unreadable to anyone who doesn't read Turkish. The three-box header names ("Test edilmesi gerekenler" etc.) are kept as-is where they're the literal output-template strings, not translated prose — same treatment as `CR`/`AOV` staying English in Turkish output (rule 7). `knowledge/scenarios/` (the 179-scenario archive itself) stays Turkish, deliberately — see the README's "Language" section for why.

### Added
- `README.tr.md` — full Turkish translation of the README, plus a `Language: English · Türkçe` switcher at the top of both. The archive itself is Turkish-native and most of the current audience reads Turkish; the README was the last English-only surface.
- A `[!NOTE]` in both READMEs naming the one official source (this repo + `npx skills add ali-demirbas/ab-test-playbook`) after noticing an unrelated skills.sh listing using a similarly named skill.
- A `Jump to install ↓` anchor near the top of both READMEs.
- `scripts/build_card.py` + tests: deterministic card rendering from a JSON scenario — fills the template, HTML-escapes text fields, drops the template's developer comment, and self-verifies that no fixed skeleton line drifted. `CLAUDE.md` rule 9 now names it as the mechanism; hand-filling the template is the fallback.
- `agents/scenario-critic` and `agents/mockup-reviewer`: adversarial review before delivery, bound by new rule 17. The critic runs a methodology checklist over every generated scenario; the reviewer compares the two rendered mockups for a second difference — the failure that silently invalidates the test a card illustrates.
- `scripts/validate_input.py` + rule 18: anything pasted in (page text, results tables, `.abtest-history.md`) is scanned for instruction-shaped content and script payloads. Findings are quoted back, never obeyed. The markup case is not theoretical — mockup bodies are raw HTML by design, so a payload that survives into a variant renders in whatever browser opens the card.
- `templates/scenario.schema.json` + `scripts/validate_scenario_json.py`: a tool-agnostic test definition, portable to any experimentation platform.
- `scripts/validate.sh`: single-entry repo validation covering the cross-file seams nothing checked before — skill/agent frontmatter, internal links (markdown and the published HTML), `${CLAUDE_PLUGIN_ROOT}` references, and rule citations against `CLAUDE.md`. Wired into CI alongside a shellcheck job.
- `docs/`: an architecture write-up and a zero-install demo published to GitHub Pages, rendered by the real builder rather than mocked up.
- `examples/`: one scenario carried end to end — schema-valid definition, card input, rendered card, and the matching chat-side output.
- `FAQ.md` — common A/B testing and CRO questions answered from this repo's own methodology.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, this `CHANGELOG.md`.
- `updated` field on every skill's metadata block.
- "Questions this playbook helps answer" and "Scope" sections in the README.
- `.gemini/extensions/ab-test-playbook/` + `scripts/build_gemini.py`: the plugin packaged for Gemini CLI, generated from the same `CLAUDE.md`, skills and agents the Claude Code plugin ships — not a hand-maintained second copy. `${CLAUDE_PLUGIN_ROOT}` is rewritten to Gemini CLI's `${extensionPath}`, and the two review agents' tool names are translated to Gemini CLI's vocabulary (an unmapped tool fails the build rather than shipping a no-op). Wired into `validate.sh` via `--check` so an edited skill or agent with a stale extension fails CI.
- `scripts/validate.sh`: a 13th check that every skill description contains "Use when" and that every sibling skill it names by name still exists — the router depends on descriptions alone to pick a skill, so a renamed or removed sibling would otherwise fail silently, findable only by a user who goes looking for a skill that isn't there.
- A bilingual "Türkçe/English" note under every skill's `# heading`, right where GitHub's file view puts it directly below an English-only frontmatter `description:` block. The skills already answer in whatever language you use (`CLAUDE.md` rule 7) — this makes that visible to a reader who only opens one SKILL.md, rather than something you'd only find by reading `CLAUDE.md` or the README's "Language" section.

### Changed
- README positioning broadened from "A/B test engine for Claude Code" to a practical A/B testing/CRO playbook description, with more of the actual coverage (ICE prioritization, guardrails, statistical significance) stated up front.
- **Breaking: all six skills renamed to a hyphenated form** — `abtest` → `ab-test`, and `abtest-suggest` / `abtest-design` / `abtest-audit` / `abtest-results` / `abtest-card` → `ab-test-suggest` / `ab-test-design` / `ab-test-audit` / `ab-test-results` / `ab-test-card` (directories, `name:` frontmatter, and every cross-reference). The un-hyphenated form didn't match how people actually search for this on skills.sh, where the leading competitor family for the query "abtest" is itself an "ab-test-*"-style, higher-hyphenated pattern. `/abtest suggest` etc. are now `/ab-test suggest` etc. The `.abtest-history.md` test-memory file convention keeps its existing name — it's a local file users create in their own project, not a listed skill.
- **The six `SKILL.md` bodies (headings, instructions, tables) were translated from Turkish to English** — the source skills.sh actually renders per skill, since a browsing visitor was reading an English `description:` block immediately followed by Turkish instructions with no language cue either way. `CLAUDE.md`, `knowledge/`, `agents/` and the 179-scenario archive are untouched (none of them render on skills.sh, and the archive's Turkish content is intentional — see the README's "Language" section). This doesn't change what a user gets back: `CLAUDE.md` rule 7 (output always matches the language you write in) is unchanged, so a Turkish request still gets a Turkish card — only the language the instructions are themselves written in changed.

## 2026-08-11

### Added
- `npx skills add ali-demirbas/ab-test-playbook --all` as an install option ([skills.sh](https://skills.sh)).

## 2026-08-10

### Fixed
- Three scenarios that were about the category-listing badge moved out of `product-detail.md` into `category-listing.md`, where they actually apply.
- Apostrophe/header formatting bug in the `abtest-suggest` output template (straight `'` instead of the curly `'` the validator requires).

### Changed
- Rule 9 (`CLAUDE.md`) reworked: every scenario produced in a run (2-5 of them) now becomes its own HTML card automatically — the three-box content lives only in the card, not duplicated as chat text.
- README rewritten with badges, a Mermaid flow diagram, a real example card (`assets/example-card.png`), and a translated usage table.

### Added
- Initial commit: the archive (179 scenarios across 10 journey-stage files), the five `abtest-*` skills, `analyze_results.py`, `validate_scenarios.py`, and the binding rules in `CLAUDE.md`.
