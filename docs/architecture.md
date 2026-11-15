# Architecture

How a scenario travels from a request to a delivered card, and which part of the
system is responsible for what. The short version: **judgement is in the skills
and agents, enforcement is in code.** Anything that can be checked
deterministically is checked by a script, because a rule written in prose is a
rule that holds only as long as it is remembered.

## The pipeline

```
user asks (page / URL / screenshot / question / test plan)
        │
        ▼
  ab-test (router) ──► results, sample size, duration, significance:
        │              one out-of-scope line + an offer to audit the plan (rule 5)
        │
        ├── suggest ──┐
        ├── design ───┤   (design also writes short setup notes in chat)
        ├── card ─────┤   (a scenario you bring passes the same gates)
        │             ▼
        │   scripts/new_record.py: a skeleton record, ⟦hints⟧ to fill
        │             │
        │             ▼
        │   scripts/validate_scenario_json.py
        │   record checks; any error refuses · --chat prints the
        │   chat lines the records fix
        │             │
        │             ├── fast mode: build_card.py --quick → quick
        │             │   draft, never final; "finish" resumes below
        │             ▼
        │   agents/scenario-critic (Sonnet, one round)
        │   PASS → stamp from build_card.py --critic-stamp
        │   [fixable] → applied by the main session, stamp stays valid
        │   [blocking] → rework, re-validate, re-review · RET → dropped
        │             │
        │             ▼
        │   scripts/build_card.py --draft
        │   needs the critic stamp; diff, ring, numeric, legal-text,
        │   accessibility and personal-data checks; escaping + drift check
        │   → draft card ("not reviewed", no fingerprint) + manifest
        │             │
        │             ▼
        │   scripts/render_check.mjs (needs Node + Playwright)
        │   size, clipping, blank screen, ring overlaps, text size,
        │   contrast; 0 VERIFIED · 1 VISUAL_CHECK_FAILED (fix, rebuild)
        │   · 3 VISUAL_CHECK_UNAVAILABLE (nothing measured)
        │             │
        │             ▼
        │   agents/mockup-reviewer (Sonnet)
        │   draft + manifest + render_check output, one run for all cards
        │   PASS → runs build_card.py --stamp <draft>; its JSON goes
        │   into review.mockup_reviewer
        │   FIX → mockup fix, new draft, review again
        │   UNVERIFIED (no render) → no stamp; the draft is given only
        │   as a preview labelled UNVERIFIED, never final
        │   (a change to a record field goes back to the critic)
        │             │
        │             ▼
        │   scripts/build_card.py (final)
        │   both stamps must match, or nothing is written;
        │   --share (1200 × 630) and --overview on request
        │             │
        │             ▼
        │   single-file HTML card(s), the only thing delivered:
        │   title + A/B mockups + ring and label, nothing else
        │
        └── audit ───► severity table, decision, fixed plan, card offer
                       (your own plan: the review is the work, no critic;
                       a yes to the offer goes to design)
```

`suggest` and `design` produce compact scenario records (`knowledge/methodology.md`
→ The scenario record), at most three strong ones per turn by default; chat shows
each as its title, a tag line with the score, the `Neden:`, `Doğru olmalı:` and
`Önce yokla:` lines (printed from the record by `validate_scenario_json.py
--chat`) and the card file, never the record again. The card
shows only the comparison (the title, the two mockups, the ring and its label);
the record stays in the JSON. The three boxes are written only when the user
asks for a scenario's detail: the producing skill fills `detail`, the critic
reviews it again and the chat gives it; the card doesn't change. The archive keeps its
three-box format, in Turkish with an English title and body per block, and is
read by `grep` on the head lines (title, variable, tags, English title) plus the
shortlisted blocks in the user's language (`read_section.py --lang`), never a
whole stage file.

Every card goes through both gates: a record without a critic stamp gets no
draft, and a draft without a mockup stamp gets no final card. The critic runs
once: its `[fixable]` findings are exact text in a fixed list of small-fix
fields, which the critic stamp leaves out, so the main session applies them
without a second call; only a `[blocking]` finding (anything the stamp covers)
calls it again. Fast mode, when the user asks for it, stops after the validator
with quick drafts that say so on the card and in chat; "finish" runs both
reviews on the same records. `ab-test-audit`
skips the critic because there the review *is* the requested
work and findings are reported directly rather than silently fixed (CLAUDE.md
rule 17). A request to analyze results or compute a sample size, duration or
significance reaches no branch: the playbook proposes, designs, audits and
visualizes, and the user's testing tool reports the outcome (rule 5).
Any file a branch reads from the user (a plan, `.abtest-history.md`) passes
`scripts/validate_input.py` first (rule 18).

## Who checks what

Code checks what code can check, the reviewers check what code can't, and
delivery needs both. A failed check is an error with its reason, never a
warning that lets delivery continue (`knowledge/methodology.md` → Quality gates
has the full table and what the gates can't guarantee).

| Check | `validate_scenario_json.py` (record) | `build_card.py` (card) | `scenario-critic` (record) | `mockup-reviewer` (card) |
|---|---|---|---|---|
| Single variable | Can't prove it | Refuses any difference outside the rings and any numeric difference without `numeric_change`; lists every change inside the rings in the manifest | Variants differ in exactly the variable | Every manifest item is part of the variable |
| Accessibility | Refuses an interactive change without the criteria (keyword heuristic) | Refuses an added interactive component without the warning | Criteria fit the element | The mockup doesn't contradict them |
| KPI and guardrail | Refuses count, "saw it" and B-only denominators, a complement or same-name guardrail, a revenue primary that could hide user harm | | The guardrail catches the harm | |
| Evidence | Refuses a false `adapted_from`, "tested" or "proven" wording and invented uplift without user data | | Honest label | |
| Functional equivalence | Refuses a missing `invariants` (keyword heuristic) | | The right invariants | |
| Regulation | Refuses a regulated-looking record without a `regulation` warning, unverified urgency | Refuses B dropping legal or security text, or pre-ticking consent | Dark patterns, held displays | |
| Personal data | | Refuses values shaped like personal data | | Masking right |
| Layout and readability | | `render_check.mjs` errors on size, clipping, blank screen, ring overlaps, text size, contrast | | Reads that output; judges size and misleading clipping |
| Gates | `--fingerprint`; `--chat` prints the record-bound chat lines | `--critic-stamp` prints the critic stamp; the draft needs it, the final needs both; `--stamp` prints the mockup stamp, `--check` verifies a delivered card; `--quick` drafts are never stamped | One round; stamps what `--critic-stamp` prints on PASS | Stamps what `build_card.py --stamp` prints on PASS |

## Where each concern lives

| Concern | Lives in | Why there |
|---|---|---|
| Binding rules (one variable, one primary KPI, guardrail, no dark patterns) | `CLAUDE.md` | Applies to every skill; a skill cannot opt out of it |
| Method reasoning (KPI choice, guardrails, isolation, priority) | `knowledge/methodology.md` | Referenced by skills rather than restated in each one |
| What a card shows and how it looks | `knowledge/mockup-style.md` (the core) + `knowledge/mockup-style/` (one file per trigger) | Same reason: one definition, many consumers (the card skill, the template, the builder, render_check, the mockup reviewer); the core is read for every card, a fold, raw markup, fast mode, the UNVERIFIED preview or a render_check finding opens only its own file |
| How a record is written | `templates/record-checklist.md` | The skeleton command, the fields it leaves to the producer and the first-validation list, shared by suggest, design and card so none of them restates it |
| Curated scenarios | `knowledge/scenarios/` | Content, not logic, in the three-box format: Turkish blocks with a tag line, an English title and an English body ([`FORMAT.md`](../knowledge/scenarios/FORMAT.md)). Adding a scenario is a content change |
| Per-task instructions | `skills/ab-test-*/SKILL.md` | The task-specific part, kept thin because the rules live above |
| Adversarial review | `agents/` | Separate context: the producer systematically misses its own single-variable violation |
| Record skeleton | `scripts/new_record.py` | What the validator decides from a few facts (the KPI's denominator, the accessibility criteria, the invariant, the exposure sentence, the priority inputs) is written by code, so a first draft rarely fails validation |
| Record-bound chat lines | `scripts/validate_scenario_json.py --chat` | The tag line with its score, `Neden:`, the must-be-true lines, the conditional and pre-start lines and the brief are printed from the record, so they can't drift from it |
| Delivery gates (review stamps, draft and final card) | `scripts/build_card.py --critic-stamp` + `scripts/build_card.py` | A review the builder can't see is one it can't enforce; a fingerprint of the reviewed content is something it can check ([`design-notes.md`](design-notes.md) → Rule 17) |
| Text escaping, template fill, drift check | `scripts/build_card.py` | Deterministic: a model rewriting ~180 lines of CSS per card is both the slowest step and the drift risk |
| Structural rules on a test definition | `templates/scenario.schema.json` + `scripts/validate_scenario_json.py` | Rules 1-3 become shape, not prose: a record has one `primary_kpi` and one `guardrail`, each with its denominator or criterion, so a second primary can't be written. Only the validator reads the schema: a record starts from `new_record.py`, and a refusal names the field and its fix |
| Detailed view | optional `detail` in the same schema | Written only on request: regenerating three boxes per proposal cost tokens and repeated the record |
| Priority (a tier, its score and a one-sentence reason) | `priority` in the same schema: `tier`, `rationale` and the five `inputs` | The tier is the band of a score out of 9 that the validator recomputes from the recorded inputs, so it can't be chosen; the chat shows the score next to the tier, while the rationale stays in words (`methodology.md` → Prioritization) |
| Untrusted input (pasted files, plans, history) | `scripts/validate_input.py` | Instruction-shaped lines and script payloads are reported with line numbers and quoted back, never followed |
| Rationale behind the binding rules | [`design-notes.md`](design-notes.md) | Kept out of `CLAUDE.md` so the always-loaded rules stay short |
| Archive format | `scripts/validate_scenarios.py` | Guards the 217 shipped scenarios against silent format rot: head lines, tag values and unique ids, the English body's parallel boxes |
| KPI vocabulary | `knowledge/kpi-glossary.md` | Canonical KPI names, each with its definition, denominator and English name; the archive uses them and the validator reads the table |
| Cross-file consistency | `scripts/validate.sh` | Frontmatter, links, plugin-root paths, rule citations, the scenario and rule counts the docs quote, description length, bundle freshness: the seams no single validator sees |

## What each flow reads

Everything a flow reads before it produces anything is billed again on every
model call of the run, so the always-read set is kept small and the rest is read
when its trigger applies. `python3 tests/test_reading_budget.py --table` prints
the bytes; the test holds each flow under a ceiling and checks that every named
section, on-demand file and bundled path still resolves.

| Flow | Read whole, once per session | On demand |
|---|---|---|
| design, suggest | `CLAUDE.md`, the flow's skill, `ab-test-card`, `templates/record-checklist.md`, `knowledge/mockup-style.md` | One `methodology.md` section per decision (the skill's table); one or two archive blocks by line; a glossary grep; a `knowledge/mockup-style/` file by its trigger |
| card | `CLAUDE.md`, `ab-test-card`, the checklist, the mockup core | The same mockup files |
| audit | `CLAUDE.md`, `ab-test-audit` | The methodology section a checklist item names |
| scenario-critic, per round | Its agent file, `CLAUDE.md` | Methodology sections a check needs |
| mockup-reviewer, per round | Its agent file, the mockup core, `CLAUDE.md` | The mockup file a card uses |

The schema and the worked example are never read by a model (the validator and
the skeleton use them); the card template only for a card in raw markup.

## Why two review agents rather than one

They fail differently. `scenario-critic` reads the *argument*: is there a
mechanism, is the primary KPI sensitive to the change, is the evidence level
honest. `mockup-reviewer` reads the *picture*: do the two variants differ in
exactly one thing. A single reviewer asked to do both reliably does the first
and skims the second, because the second is a tedious line-by-line diff and the
first is interesting. Splitting them is not redundancy; it is putting the
boring check somewhere it cannot be skipped. Both run on Sonnet: their
checklists are explicit and the code has already refused what it can, so a
smaller, cheaper model carries them, and their instructions say the bar stays
where it was.

## What code deliberately does not decide

The schema can tell that `variable` is a non-empty string. It cannot tell that
`"button colour and label"` names two variables. The validator can check that a
record has one primary KPI with a denominator; it cannot tell whether that KPI
will actually move when the change ships. The builder can list every change
inside a ring; it cannot tell whether a listed change is the variable or a second
one riding along. Those stay with the critic and the mockup reviewer, and their
instructions say so: the split is deliberate, not a gap waiting to be closed.
What the code does guarantee is that a stale review can't pass: the final
build checks both stamps against what it is about to write. That a review
really took place, and was careful, rests on rule 17, not on code.

## Adding to the system

- **A new scenario** → `knowledge/scenarios/<stage>.md`, then `bash scripts/validate.sh`: it runs the archive validator and fails until every doc that quotes the scenario total states the new number. A **new scenario file** also needs a line in the stage-to-file map of `skills/ab-test-suggest/SKILL.md`; without one nothing routes to it.
- **A new rule that applies everywhere** → `CLAUDE.md`, numbered. If it can be checked mechanically, add the check to a script in the same change; a rule with no enforcement path degrades into a suggestion.
- **A new skill** → `skills/ab-test-<name>/SKILL.md` with the `metadata` block (`version`, `category`, `updated`). Keep it thin: reference `CLAUDE.md` and `knowledge/` instead of restating them.
- **A change to the card's look** → `knowledge/mockup-style.md` (or the on-demand file in `knowledge/mockup-style/` that holds the case) first, then `templates/scenario-card.html` and the matching `render_check.mjs` check. `build_card.py` self-verifies against the template, so a structural edit will surface immediately as a drift error rather than as a quietly malformed card.
