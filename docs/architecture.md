# Architecture

How a scenario travels from a request to a delivered card, and which part of the
system is responsible for what. The short version: **judgement is in the skills
and agents, enforcement is in code.** Anything that can be checked
deterministically is checked by a script, because a rule written in prose is a
rule that holds only as long as it is remembered.

## The pipeline

```
user asks (page / URL / screenshot / question / numbers)
        │
        ▼
  ab-test (router)
        │
        ├── suggest ──┐
        ├── design ───┤   (design also emits the setup spec and a
        │             │    pre-registration block, schema-validated)
        │             ▼
        │   agents/scenario-critic
        │   methodology review, adversarial
        │   FIX → fix and re-run · RET → not produced
        │             │
        ├── card ─────┤   (a scenario you bring, rendered directly)
        │             ▼
        │   scripts/build_card.py
        │   deterministic render + escaping + drift self-check
        │             │
        │             ▼
        │   agents/mockup-reviewer
        │   one-difference check, one run for all of a turn's cards
        │             │
        │             ▼
        │   single-file HTML card(s)
        │
        ├── audit ───► findings by severity + "can this run as-is?"
        │              (your own plan: the review is the work, no critic)
        │
        └── results ─► scripts/analyze_results.py
                       SRM first → significance (directional verdict) / continuous /
                       guardrail non-inferiority / interaction / revenue / bayes / samplesize
                       → decision + next step + history row (written on confirm)
```

Only scenario-producing branches go through the critic and the card builder.
`ab-test-audit` skips the critic because there the review *is* the requested
work and findings are reported directly rather than silently fixed (CLAUDE.md
rule 17). `ab-test-results` produces no scenario at all: it runs the stats
engine, reads the result against the pre-registration when one is supplied
(direction, alpha, guardrail margins, lagging windows, pass/fail checks), states
a decision from its decision table, and offers a test-memory row.
Any file a branch reads from the user (a plan, an export,
`.abtest-history.md`) passes `scripts/validate_input.py` first (rule 18).

## Where each concern lives

| Concern | Lives in | Why there |
|---|---|---|
| Binding rules (one variable, one primary KPI, guardrail, no dark patterns) | `CLAUDE.md` | Applies to every skill; a skill cannot opt out of it |
| Method and statistics reasoning | `knowledge/methodology.md` | Referenced by skills rather than restated in each one |
| Visual language of a card | `knowledge/mockup-style.md` | Same reason — one definition, many consumers |
| Curated scenarios | `knowledge/scenarios/` | Content, not logic. Adding a scenario is a content change |
| Per-task instructions | `skills/ab-test-*/SKILL.md` | The task-specific part, kept thin because the rules live above |
| Adversarial review | `agents/` | Separate context: the producer systematically misses its own single-variable violation |
| Text escaping, template fill, drift check | `scripts/build_card.py` | Deterministic — a model rewriting ~180 lines of CSS per card is both the slowest step and the drift risk |
| Statistics | `scripts/analyze_results.py` | Same reason: arithmetic is not a judgement call |
| Structural rules on a test definition | `templates/scenario.schema.json` + `scripts/validate_scenario_json.py` | Rules 2 and 3 become shape, not prose: a scenario with two primary KPIs fails validation |
| Pre-registration (decisions fixed before launch) | optional `preregistration` object in the same schema | Every measured guardrail has a non-inferiority margin; pass/fail guardrails (`type: check`) carry a criterion; a lagging guardrail carries `read_after_days`; allocation must sum to 1; the pre-registered variable, primary KPI and guardrail names must be the scenario's own; optional `trigger` and `pre_start_gates` record the denominator event and what must be closed before traffic. `ab-test-design` validates the block inside the scenario JSON with `validate_scenario_json.py <scenario.json>` (`--prereg-only` only when no scenario JSON exists; `--strict` turns warnings into errors) |
| Untrusted input (pasted files, history, exports) | `scripts/validate_input.py` | Instruction-shaped lines and script payloads are reported with line numbers and quoted back, never followed |
| Rationale behind the binding rules | [`design-notes.md`](design-notes.md) | Kept out of `CLAUDE.md` so the always-loaded rules stay short |
| Archive format | `scripts/validate_scenarios.py` | Guards the 221 shipped scenarios against silent format rot |
| KPI vocabulary | `knowledge/kpi-glossary.md` | 99 canonical KPI names, each with its definition and denominator; the archive uses them and the validator reads the table |
| Cross-file consistency | `scripts/validate.sh` | Frontmatter, links, plugin-root paths, rule citations, the scenario and rule counts the docs quote, description length, bundle freshness: the seams no single validator sees |

## Why two review agents rather than one

They fail differently. `scenario-critic` reads the *argument*: is there a
mechanism, is the primary KPI sensitive to the change, is the evidence level
honest. `mockup-reviewer` reads the *picture*: do the two variants differ in
exactly one thing. A single reviewer asked to do both reliably does the first
and skims the second, because the second is a tedious line-by-line diff and the
first is interesting. Splitting them is not redundancy — it is putting the
boring check somewhere it cannot be skipped.

## What code deliberately does not decide

The schema can tell that `variable` is a non-empty string. It cannot tell that
`"button colour and label"` names two variables. The validator can count KPI
roles; it cannot tell whether the primary KPI will actually move when the change
ships. Those stay with the critic, and the critic's instructions say so — the
split is deliberate, not a gap waiting to be closed.

## Adding to the system

- **A new scenario** → `knowledge/scenarios/<stage>.md`, then `bash scripts/validate.sh`: it runs the archive validator and fails until every doc that quotes the scenario total states the new number. A **new scenario file** also needs a line in the stage-to-file map of `skills/ab-test-suggest/SKILL.md`; without one nothing routes to it.
- **A new rule that applies everywhere** → `CLAUDE.md`, numbered. If it can be checked mechanically, add the check to a script in the same change; a rule with no enforcement path degrades into a suggestion.
- **A new skill** → `skills/ab-test-<name>/SKILL.md` with the `metadata` block (`version`, `category`, `updated`). Keep it thin: reference `CLAUDE.md` and `knowledge/` instead of restating them.
- **A change to the card's look** → `templates/scenario-card.html`. `build_card.py` self-verifies against the template, so a structural edit will surface immediately as a drift error rather than as a quietly malformed card.
