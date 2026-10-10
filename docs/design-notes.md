# Design notes — why the binding rules look the way they do

`CLAUDE.md` keeps only the enforceable instruction for each rule, because it is loaded into context on every run. The reasoning behind the less obvious rules lives here.

## Rule 9 — cards, not chat text, and never padding

- **Why a script builds the card.** Retyping the ~180 lines of fixed CSS by hand on every card was the biggest time cost of a turn. A title containing `<`, `>` or `&` silently breaking the card can only be prevented in code; writing it into a rule isn't enough. A "manual fallback" that bypasses `build_card.py` would also bypass correct escaping order, comment stripping, and the drift and injection checks — the reasons the mechanism exists.
- **Why 1-5, not 2-5.** A lower bound of two pushed the generator to add a weak second candidate just to reach the count. A weak test costs the user a traffic slot; one strong test is a better turn than one strong plus one filler.
- **Why the >5 offer.** Producing ten cards in one turn buries the best ones. The top five by ICE are produced; the rest are offered.
- **Why an explicit ask overrides the filter.** The strong-candidate bar exists to stop the playbook padding its own output. Applied to a test the user asked for, the same bar became a silent refusal, or a review loop that never passed. An asked test is the user's call: it is produced, its weakness is stated, and the card names the stronger alternative so the choice stays informed. Rule 6 is not overridden by an ask.

## Rule 11 — two cases in a regulated flow

"Don't suggest without verifying the market's rule" blocked every test inside an insurance, pension or credit flow, including ones that touch no regulated display at all. The rule now separates the two: a variant that changes a regulated display itself (legal text, a mandatory disclosure, consent wording, a price, rate, cost or return figure, data-purpose copy) is held; a variant that only sits inside such a flow is produced with compliance sign-off as a pre-start gate, written where it can't be lost (the setup spec, the first sentence of the decision rule, a Never-do item).

## Rule 13 — the problem question holds the turn

Every candidate depends on which problem is being solved, so producing scenarios alongside the question meant producing them for the wrong problem half the time. The question is asked alone and nothing else is produced in that turn. Two limits keep it from becoming a gate: it is skipped when the message already states the problem, and it is never asked twice (no option picked means "no specific problem").

## Rule 12 — brand source never blocks

Asking "brand guide or neutral?" before the first card stalled the whole turn on a cosmetic choice and could collide with rule 13's problem question, producing two blocking questions. The neutral palette is a safe default and a rebrand is cheap once a guide arrives, so the playbook proceeds and offers.

## Rule 16 — memory read and write

Earlier wording said the playbook "never keeps or fills" the history file, while `ab-test-results` offered to append a row. The consistent rule: reading is automatic, writing happens only on explicit user confirmation, and the file stays the user's data (a public repo should `.gitignore` it).

## Rule 17 — two separate reviewers

The producing side systematically misses its own single-variable violation and the second difference in its own mockup; a separate pair of eyes is the fix. The mockup reviewer checks rendering only; if a fix would change the scenario's content, that content has not been through the methodology review, so it goes back to scenario-critic.

## Rule 19 — one question per turn

Rules 6, 11, 13 and 14, the mockup's need for a real figure, the traffic question and the two offers each justify a question on their own. Asked together they turn a deliverable into a questionnaire. A fixed priority order makes the choice deterministic. There are ten kinds, highest first:

1. Rule 13's problem question.
2. A regulation sign-off a scenario depends on (rule 11).
3. Rule 6's signal-verification question (is the countdown, stock count or viewer count real).
4. Rule 11's market question.
5. A real or shareable figure a scenario's mockup needs.
6. Whether an element the scenario would add is really absent from the page, or a detail the screenshot doesn't show.
7. Rule 14's field-feasibility question.
8. The traffic question, only when the user asked about duration or sample size (rule 5).
9. The >5-candidates offer.
10. The backlog offer.

The order follows cost of being wrong: the first four can make a scenario unusable or unlawful, the middle ones only change a detail of one card, the last two are conveniences.

- **Same kind, one question.** Three scenarios that each need to know whether an element is already on the screen used to mean three turns. Questions of the same kind merge into one that lists every item, and that counts as one. Different kinds never merge, because a merged question of mixed kinds is the questionnaire again.
- **Only the problem question holds the turn.** For every other kind the turn still delivers whatever can be produced without the answer, with each open assumption stated in one line. The problem question is the exception because nothing can be produced without its answer (see rule 13 above).
- **`ab-test-results` has its own order** (counts, pre-registration, duration, MDE target, guardrail margin and direction, check and window confirmations, order value, segments, the history-row offer last), under the same one-question limit.
