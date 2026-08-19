# Architecture

How a scenario travels from a request to a delivered card, and which part of the
system is responsible for what. The short version: **judgement is in the skills
and agents, enforcement is in code.** Anything that can be checked
deterministically is checked by a script, because a rule written in prose is a
rule that holds only as long as it is remembered.

## The pipeline

```
user asks (page / URL / screenshot / question)
        │
        ▼
  ab-test (router)  ─────────────────────────────────┐
        │                                            │
        ├── suggest ──┐                              │
        ├── design ───┤                              │
        ├── audit ────┤ (user's own plan — no critic) │
        └── results ──┘                              │
                      │                              │
                      ▼                              │
        agents/scenario-critic  ◄────────────────────┘
        methodology review, adversarial
        FIX → fix and re-run · RET → not produced
                      │
                      ▼
        scripts/build_card.py
        deterministic render + escaping + drift self-check
                      │
                      ▼
        agents/mockup-reviewer
        one-difference check on the two mockups
                      │
                      ▼
              single-file HTML card
```

`ab-test-audit` is the one branch that skips the critic: there, review *is* the
requested work and findings are reported directly rather than silently fixed
(CLAUDE.md rule 17).

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
| Archive format | `scripts/validate_scenarios.py` | Guards the 211 shipped scenarios against silent format rot |

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

- **A new scenario** → `knowledge/scenarios/<stage>.md`, then `python3 scripts/validate_scenarios.py`.
- **A new rule that applies everywhere** → `CLAUDE.md`, numbered. If it can be checked mechanically, add the check to a script in the same change; a rule with no enforcement path degrades into a suggestion.
- **A new skill** → `skills/ab-test-<name>/SKILL.md` with the `metadata` block (`version`, `category`, `updated`). Keep it thin: reference `CLAUDE.md` and `knowledge/` instead of restating them.
- **A change to the card's look** → `templates/scenario-card.html`. `build_card.py` self-verifies against the template, so a structural edit will surface immediately as a drift error rather than as a quietly malformed card.
