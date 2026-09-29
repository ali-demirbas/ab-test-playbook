# Design notes — why the binding rules look the way they do

`CLAUDE.md` keeps only the enforceable instruction for each rule, because it is loaded into context on every run. The reasoning behind the less obvious rules lives here.

## Rule 9 — cards, not chat text, and never padding

- **Why a script builds the card.** Retyping the ~180 lines of fixed CSS by hand on every card was the biggest time cost of a turn. A title containing `<`, `>` or `&` silently breaking the card can only be prevented in code; writing it into a rule isn't enough. A "manual fallback" that bypasses `build_card.py` would also bypass correct escaping order, comment stripping, and the drift and injection checks — the reasons the mechanism exists.
- **Why 1-5, not 2-5.** A lower bound of two pushed the generator to add a weak second candidate just to reach the count. A weak test costs the user a traffic slot; one strong test is a better turn than one strong plus one filler.
- **Why the >5 offer.** Producing ten cards in one turn buries the best ones. The top five by ICE are produced; the rest are offered.

## Rule 12 — brand source never blocks

Asking "brand guide or neutral?" before the first card stalled the whole turn on a cosmetic choice and could collide with rule 13's problem question, producing two blocking questions. The neutral palette is a safe default and a rebrand is cheap once a guide arrives, so the playbook proceeds and offers.

## Rule 16 — memory read and write

Earlier wording said the playbook "never keeps or fills" the history file, while `ab-test-results` offered to append a row. The consistent rule: reading is automatic, writing happens only on explicit user confirmation, and the file stays the user's data (a public repo should `.gitignore` it).

## Rule 17 — two separate reviewers

The producing side systematically misses its own single-variable violation and the second difference in its own mockup; a separate pair of eyes is the fix. The mockup reviewer checks rendering only; if a fix would change the scenario's content, that content has not been through the methodology review, so it goes back to scenario-critic.

## Rule 19 — one question per turn

Rules 11, 13 and 14 and the >5 offer each justify a question on their own. Asked together they turn a deliverable into a questionnaire. A fixed priority order makes the choice deterministic, and delivering what can be produced under a stated assumption keeps the turn useful.
