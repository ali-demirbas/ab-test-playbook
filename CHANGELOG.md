# Changelog

All notable changes to this project are documented here. Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## Unreleased

### Added
- `FAQ.md` — common A/B testing and CRO questions answered from this repo's own methodology.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, this `CHANGELOG.md`.
- `updated` field on every skill's metadata block.
- "Questions this playbook helps answer" and "Scope" sections in the README.

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
