# Design notes — why the binding rules look the way they do

`CLAUDE.md` keeps only the enforceable instruction for each rule, because it is loaded into context on every run. The reasoning behind the less obvious rules lives here.

## Rule 1 — why a record replaced the three boxes

Every proposal used to regenerate the three boxes, the card printed them, and the chat summarized them again. Most of that text restated the archive block it came from or repeated the same KPI in a second wording, and writing it was the largest output cost of a turn, while the decision a reader makes (is this worth a test slot, what decides it, what must not break) rests on about ten facts. The record keeps exactly those ten, each with a rule a validator can check. The boxes aren't lost: the archive keeps them as knowledge, and any proposal gets them back as the detailed view when the user asks.

## Rule 5 — why the playbook stopped doing statistics

Earlier versions computed significance, sample size and guardrail margins from numbers pasted into the chat. Those numbers were a summary of what the testing tool had already counted: the playbook couldn't see how users were assigned, what was logged or who was excluded, so a precise-looking verdict could rest on a broken input. The statistics also pulled the rest of the workflow toward them (traffic questions, pre-registration blocks, numeric margins few users could fill). The playbook's value is before launch, choosing the variable, the primary, the guardrails and the gates and catching what would invalidate the test, so it now stops there and the testing tool reports the outcome.

## Rule 9 — cards, not chat text, and never padding

- **Why a script builds the card.** Retyping the ~180 lines of fixed CSS by hand on every card was the biggest time cost of a turn. A title containing `<`, `>` or `&` silently breaking the card can only be prevented in code; writing it into a rule isn't enough. A "manual fallback" that bypasses `build_card.py` would also bypass correct escaping order, comment stripping, and the drift and injection checks — the reasons the mechanism exists.
- **Why the card shows only the comparison.** The card used to carry a text column beside the mockups: the problem, a summary box with the mechanism and the variable, a KPI box, a warnings box, then a footer of source, evidence and priority tags, a brand note and a mockup disclaimer. Every line of it was already in the record, and the producer wrote much of it a third time in chat, so each card cost output tokens to restate what the JSON held. It also took more than half the card's width, leaving two small phone frames that were hard to compare. The card's job is the visual comparison: the question, A and B large and top-aligned, the change ringed and named. The record holds the rest, and the few lines a user needs (a stronger alternative, a representative mockup) go to chat once.
- **Why at most three, and no lower bound.** A lower bound of two pushed the generator to add a weak second candidate just to reach the count, and five full scenarios per turn buried the best ones under reading and output nobody acted on. A weak test costs the user a traffic slot; one strong test is a better turn than one strong plus one filler.
- **Why the >3 offer.** The top three by priority are produced and the count of the rest is stated with an offer to continue, so a strong candidate is deferred, never silently dropped.
- **Why chat carries only a title and a tag line.** The record lives in the JSON; writing it again in chat doubled the output without adding a fact. Detail the user asks for is the exception, since the card no longer shows it.
- **Why an explicit ask overrides the filter.** The strong-candidate bar exists to stop the playbook padding its own output. Applied to a test the user asked for, the same bar became a silent refusal, or a review loop that never passed. An asked test is the user's call: it is produced, and one chat line states its weakness and names the stronger alternative, so the choice stays informed. Rule 6 is not overridden by an ask.

## Rule 11 — two cases in a regulated flow

"Don't suggest without verifying the market's rule" blocked every test inside an insurance, pension or credit flow, including ones that touch no regulated display at all. The rule now separates the two: a variant that changes a regulated display itself (legal text, a mandatory disclosure, consent wording, a price, rate, cost or return figure, data-purpose copy) is held; a variant that only sits inside such a flow is produced with compliance sign-off as a pre-start gate, written where it can't be lost (a `regulation` warning in the record and the `Pre-start gates` line of the setup notes; a Never-do item in the detailed view).

## Rule 13 — the problem question holds the turn

Every candidate depends on which problem is being solved, so producing scenarios alongside the question meant producing them for the wrong problem half the time. The question is asked alone and nothing else is produced in that turn. Two limits keep it from becoming a gate: it is skipped when the message already states the problem, and it is never asked twice (no option picked means "no specific problem").

## Rule 12 — brand source never blocks

Asking "brand guide or neutral?" before the first card stalled the whole turn on a cosmetic choice and could collide with rule 13's problem question, producing two blocking questions. The neutral palette is a safe default and a rebrand is cheap once a guide arrives, so the playbook proceeds. It no longer says where the colors came from: a note under every card repeated the same offer on each one and pulled attention from the comparison. A guide sent later still replaces the colors.

## Rule 16 — memory read and write

The history file records outcomes the user's own testing tool reported. The playbook reads it automatically and never writes it: it has no result of its own to record, and re-interpreting someone else's outcome would bring back the statistics rule 5 removed. The backlog is different: it holds the playbook's own suggestions, so `ab-test-suggest` may append rows, but only after the user confirms. Both files are the user's data (a public repo should `.gitignore` them).

## Rule 17 — two separate reviewers

The producing side systematically misses its own single-variable violation and the second difference in its own mockup; a separate pair of eyes is the fix. The mockup reviewer checks rendering only; if a fix would change the scenario's content, that content has not been through the methodology review, so it goes back to scenario-critic.

**Why review stamps.** The builder can't see a review: it sees files, and a review happens in a conversation. Before the gates, nothing stopped a card from being delivered with the review skipped, or edited after it passed. A stamp turns the review into something the builder can check: on PASS each reviewer records the fingerprint of exactly what it reviewed (the record for the critic, the final card's bytes for the mockup reviewer), and the final build recomputes both and refuses on a mismatch. The critic's stamp is required before the draft, so the mockup reviewer only ever looks at a card built from an approved record.

**Why errors, not warnings.** A warning that let delivery continue was read, at best, by the producer that had made the mistake; a price that differed between A and B outside the ring was reported and the card was built anyway. A check the gates rely on now refuses with its reason.

**The limit.** A stamp proves the built content is the content that was reviewed, not that a review took place or was careful, and anyone who can edit the record can write one. It stops the skipped-by-accident and the stale review; the honest review itself rests on this rule. The same goes for what the reviewers judge: invariants and accessibility criteria are declared and checked against the record and the mockup, never run against the real product.

## Rule 19 — one question per turn

Rules 6, 11, 13 and 14, the mockup's need for a real figure, a detail the screenshot doesn't show and the two offers each justify a question on their own. Asked together they turn a deliverable into a questionnaire. A fixed priority order makes the choice deterministic. There are nine kinds, highest first:

1. Rule 13's problem question.
2. A regulation sign-off a scenario depends on (rule 11).
3. Rule 6's signal-verification question (is the countdown, stock count or viewer count real).
4. Rule 11's market question.
5. A real or shareable figure a scenario's mockup needs.
6. Whether an element the scenario would add is really absent from the page, or a detail the screenshot doesn't show.
7. Rule 14's field-feasibility question.
8. The >3-candidates offer.
9. The backlog offer.

The order follows cost of being wrong: the first four can make a scenario unusable or unlawful, the middle ones only change a detail of one card, the last two are conveniences.

- **One question, never two in a sentence.** Merging several same-kind questions into one long sentence still read as a questionnaire. The turn asks only the most critical question; every other open fact is listed once in the "Koşullu" line, so nothing is hidden and the user answers one thing at a time.
- **Only the problem question holds the turn.** For every other kind the turn still delivers whatever can be produced without the answer, with the open assumptions stated once: the critical ones together in the single “Koşullu (n):” line (each a fact to verify, the turn's one question asking the most critical), a visual one only when the user could read the mockup as their own page. The problem question is the exception because nothing can be produced without its answer (see rule 13 above).
