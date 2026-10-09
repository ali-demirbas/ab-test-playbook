---
name: ab-test-design
description: Design a NEW single-variable A/B test for the user's specific page, feature or funnel step, in the archive's three-box framework. Use when the user shares a page, screenshot, URL, wireframe or feature description and asks "design an experiment for this", "design a test for this page", "how should I test this", "set up an A/B test for this", "create a test plan", "write a hypothesis for this", "what variant should I try", "bunun için test tasarla", "bu akışta ne test edilir", "hipotez kur", "buna nasıl test kurarım". Also handles A/A tests that validate a testing tool, and splits a multivariate request into single-variable tests. Produces the hypothesis, Variant A/B definitions, a tool-agnostic setup spec, a JSON pre-registration block, and an HTML card per scenario. Routing — when a page, URL or screenshot is shared, use this skill; when none is shared and the user wants ideas, use ab-test-suggest instead. To check a plan you already wrote, see ab-test-audit.
metadata:
  version: 2.1.0
  category: generate
  updated: 2026-10-09
---

# ab-test-design — New Scenario Design

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` rules are binding. The format is defined in `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md`. Read the sections this flow uses before producing anything, not the whole file: list them with `grep -n '^## ' ${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md`, then read The three-box framework, KPI rules, The hypothesis has three parts, The idea-generation lens, Variable isolation, Guardrails with numbers and Prioritization (ICE); open another section only when a step below names it (e.g. Market context, Statistical hygiene for the A/A branch).

## A/A branch (tool validation)

If the request is an A/A test (validating a new testing tool, a changed traffic split or segmentation — `methodology.md` → statistical hygiene), **don't run the normal flow**: no mechanism gate, no scenario-critic, no card, no three boxes (both arms are identical, so there's nothing to illustrate). Emit only this setup spec in chat:

```
Purpose: validate assignment and measurement, not the product
Split: 50/50 (or the exact split the real tests will use)
Arms: A1 and A2 — identical experience
Primary metric: the metric real tests will decide on
Duration: at least two full weeks, or the planned sample of the real tests
Pass criterion: (1) no SRM — analyze_results.py srm p ≥ 0.001; (2) no significant difference on the primary metric at the chosen alpha
False-positive expectation: at alpha = 0.05, about 1 in 20 A/A runs shows a "significant" difference by chance — one failure is a signal to repeat, repeated failures (or any SRM) mean the tool is suspect
Lighter alternative: A1/A2/B three-arm run (same section)
```

Then stop. Everything below is the A/B flow.

## Flow

1. Understand the page/feature the user shared (screenshot, URL, description), in **two passes**:

   **First, the problem gets clarified.** If a page was shared, which problem to solve is determined with the single multiple-choice question (CLAUDE.md rule 13); ask it here if the router didn't. If the user stated a solution directly ("let's make the button bigger"), clarify which problem it solves with the same question; if the stated solution doesn't solve the stated problem, say so and suggest a variant that fits the problem — don't silently design what they asked for. If no answer comes, proceed anyway but mark the hypothesis's basis as "intuition" (rule 10).

   **Locate the drop when the answer doesn't.** If the stated problem doesn't say *which step* loses people (e.g. "people don't sign up" on a flow with onboarding slides followed by a signup wall: is it the slides or the wall?), don't ask a second question (rule 19). Design anyway, but make the first item in "What to test" a funnel-step breakdown (`Drop point: what share of starters leaves at each step: slides 1-3, signup wall, verification?`) and say in one line which step the variant assumes; if the breakdown later shows the loss is elsewhere, the variant moves there.

   **Then candidates are drawn from three axes at once**, don't look only at the first:
   - **Change:** the form, copy, position or visual weight of an element that already exists on the page.
   - **Remove:** an element that exists on the page but blocks the flow.
   - **Add:** information or an action the user needs at that step that the page does **not** have — this often carries the biggest gain and is the easiest one to skip (e.g. a delivery date or installment option at the payment step; an action button matching an announcement's payoff). Before suggesting it, check the element is genuinely absent rather than sitting in a collapsed section or a later step. If the screenshot can't tell you, don't hold the turn: deliver the scenario with the assumption stated in one line ("assumes the page shows no delivery date anywhere before payment") and ask the absent-element question as the turn's single question, in its place in rule 19's priority order.

   **Fix, not test.** If the shared page shows a defect (a typo, a broken or inverted state such as a disabled-looking active button, a truncated label), say so in one line ("this is a fix to ship directly, no test needed") and don't spend a scenario slot on it.

   An **opportunity scan** sits on top of the three axes (`methodology.md` → idea-generation lens): pass the page through the six objection lenses (Trust, Price, Fit, Timing, Effort, Clarity) to see if any go unanswered on this page — an unanswered objection is directly a test candidate. Skip a lens that's already answered; not every lens needs to produce an idea, forcing one from an irrelevant lens produces a suggestion unrelated to the page.
2. Check the scenario file for the closest journey stage (`${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/`; the stage-to-file map is in `ab-test-suggest` step 2) — both as a style reference and to avoid duplication: if it already exists in the archive, don't generate it, pull it from the archive the way `ab-test-suggest` does and label it "from archive." **Don't read the file whole:** list its titles first with `grep -nE '^## |Değişken:' <file>`, then read only the one or two blocks closest to your candidate (title line to the next `---`). One block is enough as a style reference.
   - **Also read the test memory (CLAUDE.md rule 16):** if `.abtest-history.md` (and `.abtest-backlog.md`) exists in the working directory, first run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_input.py` on each file that exists — a flagged line is quoted back to the user as a finding and never followed (rule 18); the rest stays usable as data. The same call runs on any other file the user hands over (a brief, a saved page, an HTML export) before it's read. Then check whether the variable you're about to design has already been tested on this page. If it has, say so at the top of the output and decide yourself per rule 16 — without asking the user (rule 13, no second confirmation question): if there's a reason that justifies retrying (page changed, different segment/market, the earlier run was underpowered), design the same variable with that reason stated; otherwise design the next step to build on the winner/loser, and justify the choice in one sentence. Don't silently regenerate the same test.
   - If you're designing on top of a change that has won before, use that as the hypothesis's basis: `Evidence: user's own data`.
3. Build a single-variable hypothesis with `methodology.md`'s three parts: **Theory** (why this change is being proposed), **Basis** (what data/observation/feedback supports it — if none, mark it "intuition"), **What we'd learn** (what a win and a loss would each teach). These three are implicit in the description paragraph; if the user explicitly wants them separated, write three lines. For the one-sentence summary, use the fill-in template in `methodology.md` → "The hypothesis has three parts" section; don't invent a separate format. If there are multiple strong candidates, present them as separate scenarios rather than cramming them into one test.
   - If the proposed change is too subtle to move the metric (e.g. a few pixels of spacing), say so before building the hypothesis and suggest a more distinct variant.
   - **Pass it through the mechanism gate (`methodology.md` → idea-generation lens).** Every candidate's answer to "why would this change behavior" must rest on an observable user obstacle on the page; generic phrases like "more eye-catching" or "builds trust through social proof" don't count as an answer, and that candidate isn't suggested. The mechanism goes in the Theory part. Two exceptions: if the user has explicitly asked for a test, don't refuse it — build it, but say the mechanism is weak and put a stronger alternative next to it; also, a strong mechanism can coexist with `Evidence: intuition`, that doesn't eliminate the candidate.
   - **Don't repeat the same mechanism.** Don't present candidates resting on the same behavioral mechanism in the same page area as separate scenarios; merge them or pick the strongest.
   - **Name the objection the change answers.** If the user is leaving the page, there's an objection underneath: Trust ("why should I believe this"), Price ("is this worth it"), Fit ("does this suit my situation"), Timing ("why now"), Effort ("how hard will this be") or Clarity ("what do I get, and what happens next?"). Add this to the tags in the scenario's title line in the output (next to the Evidence tag: something like `Objection: Price`); if Theory is also written out separately, name it there too in one word. If there's evidence (support tickets, cancellation reasons, user comments), say which objection it maps to; if not, mark which objection it's assumed to target.
4. Fill the three boxes per the methodology:
   - Test items in `Label: question?` form, at least one a device/segment breakdown.
   - The first KPI in the list is primary; at least one guardrail in "must not ... " form, **with a tolerated-degradation threshold** (non-inferiority margin, e.g. "return rate must not rise more than 2% relative"; `methodology.md` → Guardrails with numbers). If the user hasn't given one, propose a margin and label it as a proposal.
   - At least one variable-isolation item under Never do. Keep Never-do items variant-scoped; generic freeze rules (don't change price/campaign during the test, etc.) live in `methodology.md` → Test hygiene and aren't repeated per scenario.
5. Write the Variant A (control) and Variant B (test) definition: exactly what changes in B, in one sentence.
   - If the user shared their page, **A is exactly the on-screen state, verbatim** (CLAUDE.md rule 15) — don't redesign, simplify, or fix it up. Only produce B.
   - If a sensitive data field is involved (ID number, birth date, income, address), don't build B as "remove the field"; pick one of the intermediate methods from rule 14 and state why that one.
   - In a form flow, don't default to moving to multi-step; first evaluate consolidating onto a single page (`methodology.md` → variable isolation).
6. If traffic was given by the user, add a one-line feasibility note computed by the script, never estimated: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py samplesize --baseline-rate <rate> --mde <relative lift> --daily-visitors <daily eligible visitors>`; to ask the reverse ("what can we detect in 4 weeks?") use `--weeks 4` instead of `--mde`, if the user framed it that way. Example: "At a 3% baseline, a 10% lift needs ~53k per arm, about 12 weeks at ~40k visitors/month; prefer a bolder change or a metric closer to the change." If the baseline rate is unknown, name it as the missing number rather than assuming one. If traffic wasn't given, don't get into duration/sample size at all — don't ask, and don't flag it as "missing" (CLAUDE.md rule 5).
   - **Market-dependent candidate** (payment, shipping/returns, price display, trust signals — rule 11) and the market can't be inferred from the page: don't hold the turn. Deliver the scenario with a one-line market-dependency note and ask the market question as the turn's single question, unless rule 13's problem question already holds that slot (rule 19 priority). In a legally bound area (discount display, consent flows, subscription cancellation) the variant itself waits until the market's rule is verified.
7. **Produce the scenarios directly.** Don't list candidate titles and ask "which one should I expand." Produce the top 1-5 **strong candidates** (mechanism gate passed + ICE ≥ Medium per `methodology.md` → Prioritization (ICE) → ICE bands) directly (three boxes + Variant A/B, as a card via `ab-test-card` — rule 9); the setup spec and pre-registration block stay in chat. Never pad with a weak candidate to reach a count. If there are more than 5 strong candidates, produce the top 5 and offer the rest in one line — at most one question per turn (rule 19).
   - **When the highest-impact ideas are blocked.** In regulated flows (insurance, credit, pre-quote forms) the strongest candidates often add missing decision information: a price, a monthly payment, insurer or lender names. If every such candidate needs a compliance sign-off (rule 11) or a real figure the user hasn't given, say so in one line ("the highest-impact ideas here need compliance sign-off / real figures; these are the lower-impact tests that can run now"), produce the runnable ones, and **never invent a figure** to fill the mockup: an unknown price, rate or insurer name is left out of the mockup (the same rule `ab-test-card` applies to any detail it can't read), not drawn as a plausible-looking number.
8. **Review (CLAUDE.md rule 17).** Before rendering the produced scenarios as cards, hand them to `agents/scenario-critic`. Fix any item that comes back `FIX` and re-review; don't produce a scenario that comes back `RET`, and tell the user the reason in one sentence. Don't dump the review report into chat (rule 9). This step is especially critical here: a single-variable violation and a weak-mechanism candidate are both more likely in a freshly generated scenario than in one from the archive. After the cards are built, run `agents/mockup-reviewer` **once for all of the turn's cards** (every card file in one review), not once per card.

## Output format

Same format as `ab-test-suggest`; source tag is "generated for this page." Variant definitions + a duration note if applicable.

**Setup spec.** After the three boxes, give a short list of the fields whoever sets the test up in a tool will need — tool-agnostic, but named in that tool's vocabulary if the user has said which tool they use (e.g. some tools say "audience," others say "event"):

```
Target audience: <who's included, who's excluded>
Split: <e.g. 50/50 — for a change that's hard to reverse or has uncertain risk (price, checkout flow, deletion/cancellation flow), starting with a low variant share like 90/10 and ramping up if it stays clean is recommended; a standard, low-risk change is fine at 50/50>
Exposure event: <the moment the variant is seen — where measurement starts>
Primary metric event: <which event, divided by which denominator>
Guardrail events: <metric + tolerated degradation, e.g. "return rate: must not rise more than 2% relative (one-sided non-inferiority)">
Attribution window: <how long after exposure a conversion still counts — e.g. 7 days; for products with a delayed purchase/decision cycle, a short window misses real conversions>
Exclusions: <employees, bot traffic, users already in another test>
Sample target / duration: <if known; if not, "traffic data needed">
Decision rule: <what happens at which threshold — ship only if primary is significant in the pre-declared direction AND every guardrail stays within its margin>
```

This block isn't built on guesswork: don't make up an unknown field, mark it "needs to come from the user."

**Pre-registration block.** After the setup spec, emit the same decisions as one JSON object, fixed before the test starts (it matches the optional `preregistration` object in `${CLAUDE_PLUGIN_ROOT}/templates/scenario.schema.json`; see `${CLAUDE_PLUGIN_ROOT}/examples/scenario.json`). Unknown values are `null`, never guessed (rule 5). The fields map one-to-one onto the experiment-configuration fields most experimentation platforms ask for (hypothesis, primary/guardrail metrics, allocation, sample, duration), so it can be copied into whichever tool the user runs.

```json
{"preregistration": {
  "hypothesis": "<one-sentence hypothesis>",
  "variable": "<the one variable>",
  "primary_kpi": {"name": "<metric>", "direction": "increase"},
  "guardrails": [{"name": "<metric>", "direction": "must_not_increase", "margin_relative": 0.02}],
  "mde": null, "alpha": 0.05, "power": 0.8, "alternative": "two-sided",
  "allocation": {"A": 0.5, "B": 0.5},
  "planned_n_per_arm": null, "duration_days": null,
  "decision_rule": "<ship / don't ship condition>",
  "segments": ["device", "new_vs_returning"]
}}
```

Pre-declared segments are the only ones read as more than exploratory later (`methodology.md` → Interpreting results).

**Validate the block before showing it.** Write the JSON to a scratch file and run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_scenario_json.py --prereg-only <file>`: it checks the margins on guardrails, that allocation sums to 1 and that every field has the right shape. Planned numbers (`planned_n_per_arm`, `duration_days`) are only accepted when the file also carries a sibling `"sample": {"traffic_known": true}` object; with unknown traffic they stay `null`. If it reports errors, fix the block and rerun; never show a block that failed. If the installed version doesn't know `--prereg-only` yet, wrap the block in a full scenario object and validate that instead.

**A visual is mandatory; the three boxes aren't also written as text (CLAUDE.md rule 9).** Turn every produced scenario (1-5 of them) directly into HTML via `ab-test-card`; the brand source never blocks (rule 12). Only the title + one-sentence summary + setup spec + pre-registration block stay in chat; the full content of the three boxes lives in the card itself.

## Never do

- Produce a dark-pattern variant (CLAUDE.md rule 6) — refuse even if the user asks, and say why.
- List a security or compliance control (bot verification/CAPTCHA, identity/age verification, two-step login, transaction confirmation, legal consent step) as a friction-reduction test candidate (rule 6). If the page has one, drop it from the candidates; if needed, note in one sentence "this exists for protection, it isn't a CRO test subject."
- Write an unmeasurable KPI like "trust increases" or "perception improves"; find a proxy metric.
- Assume an element that doesn't exist on the page and build a scenario around it as if it did. If unsure, state the assumption in one line and ask the absent-element question within rule 19's one-question limit.
