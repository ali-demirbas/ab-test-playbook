# Changelog

All notable changes to this project are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## Unreleased

### Added
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

### Changed
- README positioning broadened from "A/B test engine for Claude Code" to a practical A/B testing/CRO playbook description, with more of the actual coverage (ICE prioritization, guardrails, statistical significance) stated up front.

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
