# Methodology — The Framework Every Scenario Must Fit

Every scenario in this playbook (from the archive or newly generated) is written in the same framework. This file is binding: `ab-test-design` applies these rules when producing a new scenario, `ab-test-audit` applies them when auditing an existing plan.

## The three-box framework

Every scenario is made of three blocks, all three mandatory, each with exactly 5 items (`validate_scenarios.py` requires this):

1. **Test edilmesi gerekenler ("What to test")** — which questions the hypothesis has to answer. Each item is in `Label: question?` form (e.g. `Position: in the header, or inside the menu?`). At least one item asks a device/segment breakdown.
2. **Takip edilecek ana KPI'lar ("Primary KPIs to track")** — the measurement set. Rules below. (The apostrophe in the box name is curly — U+2019; the validator doesn't recognize a straight-apostrophe version of the heading.)
3. **Yapılmaması gerekenler ("Never do")** — the mistakes that invalidate the test or harm the user. At least one item protects variable isolation, in the form "don't change X and Y together in the same test."

## KPI rules

- The metric in first position is the **primary metric** — it alone decides the test's winner. Reading five metrics as equally weighted is an invitation to p-hacking.
- The list carries at least one **guardrail**: something that could degrade while conversion rises. Typical guardrails: gross margin, return rate, page speed (LCP), support tickets, abandonment rate, RPV. Guardrail items are written in "must not drop / must not rise / must not increase" form. A win with no guardrail is a deferred loss: a cost you didn't measure in the test doesn't get canceled, it just gets carried into next quarter's return rate or support load.
- The metric has to be something the tool can actually measure. "Trust perception" isn't a KPI; its proxy is written instead.
- **An intermediate-step metric can hide whether completion actually happened.** A change can easily boost a step in the middle of the funnel (add-to-cart, starting checkout, opening the form, choosing express checkout), and this looks like a win at first glance — but if the user who clears that step more easily then gets stuck at the next one, the total order count doesn't change, or even drops. The risk is especially high for variants that speed up, skip, or foreground a step: the user gets thrown at the outcome of a decision they haven't actually made yet, and bounces back. This is why the primary metric is always the real outcome at the end of the funnel (completed order, submitted form); the intermediate-step metric is tracked second, as a diagnostic. If the two move in opposite directions, that's the finding.
- **Conversion rate can hide revenue.** In price, installment, discount, or bundle tests, plain "Conversion Rate (CR)" isn't enough as the primary metric — lowering price almost always raises CR but can drop revenue. In these scenarios the primary metric should be revenue-based: Revenue Per Visitor (RPV), or Average Order Value (AOV) × CR. The price scenarios in `knowledge/scenarios/product-detail.md` and `cart-checkout.md` already apply this distinction; the same rule holds when a new price/bundle scenario is produced.

## The hypothesis has three parts

A one-sentence hypothesis ("making X into Y increases Z") isn't enough — it has to answer three separate questions:

1. **Theory:** Why are we proposing this change? What observation, data, or user feedback produced this hypothesis?
2. **Basis:** What concrete evidence supports this theory? (A metric, a user comment, a behavioral pattern.) If there's no evidence, it's marked "intuition," and the confidence level is kept low accordingly. The basis is labeled with one of four levels and shown in the output:
   - **The user's own data** — a signal measured on this exact product/page (the strongest).
   - **Archive precedent** — a pattern already tested in a similar context.
   - **Industry observation** — common practice, but with no product-specific verification.
   - **Intuition** — none of the above; a suggestion can still be given, but it's stated as low-confidence.
3. **What we'd learn:** What do we learn if the test wins, what do we learn if it loses? If neither outcome produces information, the test is already weakly designed.

`ab-test-design` carries these three implicitly in every scenario's description paragraph; if the user explicitly wants them, all three are written out separately. The one-sentence fill-in template:

> "Based on [observation/data], we think that making [change] will produce [expected outcome] for [target audience]. We'll see this in [metric]."

Weak example: "Changing the button color might increase clicks." (No basis, outcome isn't measurable with any clarity.)
Strong example: "We know from heatmaps that mobile users notice the CTA late; if we enlarge the button and raise contrast, click rate among new visitors will increase by at least 15%. We'll see this in the page-view-to-signup conversion rate."

If the change is too subtle to make a difference in the metric (e.g. a 2px border-width change), don't build a hypothesis; "is this change distinct enough to be noticed?" is the first filter of every scenario design.

**Which objection are we resolving?** If a user isn't completing a step, there's usually an unnamed objection underneath it. Five patterns repeat:

| Objection | The user's question | Typical counter |
|---|---|---|
| Trust | "Why should I believe this?" | A named reference, concrete evidence, a security signal |
| Price | "Is this worth it?" | Value comparison, installments, an ROI display |
| Fit | "Does this suit my situation?" | A similar-user example, segment-based content |
| Timing | "Why now?" | Real (not made-up) urgency, opportunity cost |
| Effort | "How hard will this be?" | "Set up in 5 minutes," a step-by-step walkthrough |

Naming which objection is being targeted in one word when building the hypothesis makes it clearer why the test will (or won't) work. If there's evidence (support tickets, cancellation reasons, a survey answer), which objection it maps to is stated; if not, it's marked as an assumption. The objection-closing message can also be built implicitly — instead of naming the objection directly ("worried you're being lazy?"), moving straight to the solution ("we handle this for you") usually works better; saying the objection out loud can reinforce it.

**Statistical significance ≠ practical significance.** `p < 0.05` alone doesn't mean "ship it." A statistically significant 0.1% lift might not be worth the implementation/maintenance cost. Two separate questions are asked when interpreting a result: (1) Is it statistically real? (2) Does its absolute size cover the engineering/design/operations cost of making the change permanent? The second question isn't a number, it's a decision — `ab-test-results` asks it as part of the "shippable" decision.

## The idea-generation lens

Ideas aren't produced by looking at the page and writing down whatever comes to mind. Four filters are applied, in order.

**1. Opportunity scan.** The five objection lenses above (Trust, Price, Fit, Timing, Effort) are used for the opportunity scan: for each objection, is there a genuine gap or user obstacle on this page? If it's already answered, that lens is skipped. **Not every lens has to produce an idea**; forcing one out of an irrelevant lens produces a suggestion unrelated to the page (e.g. "let's add an expert opinion" at the checkout step). The scan also makes visible what should exist but doesn't, in addition to what's already on screen (see Variable isolation → the addition axis).

**2. The mechanism gate.** Every candidate has to give a concrete answer to "why would this change alter user behavior?" "More eye-catching," "looks more modern," "cleaner" aren't answers; those candidates aren't suggested. The mechanism has to rest on **an observable user obstacle on the page**, not a generic psychology claim:

- Not a mechanism: "Social proof increases trust."
- A mechanism: "On this page the user can't see any evidence to judge the product's quality; moving a verifiable user review to the decision point reduces this uncertainty."

The mechanism goes in the hypothesis's **Theory** part; no new output field is opened for it. It has two limits:

- **The gate only applies to candidates the playbook produces on its own.** If the user explicitly wants a test (e.g. "let's make the button red"), the test isn't refused: it's built, but its mechanism is explicitly stated as weak, and a stronger-mechanism alternative is placed next to it. The only thing that's refused is a dark pattern (rule 6).
- **Mechanism and basis are different axes.** Basis is the question "does this problem genuinely exist" (evidence level, rule 10); mechanism is the question "if it does, why does this change fix it." A strong mechanism can coexist with `Evidence: intuition`, and this candidate isn't eliminated — only its confidence level is marked low.

**3. Mechanism-duplication check.** Ideas resting on the same behavioral mechanism in the same page area aren't presented as separate suggestions just because they're worded differently; they're merged, or the strongest one is picked. "Add social proof," "make reviews visible," "highlight popular products" aren't three ideas, they're three phrasings of the same mechanism.

**4. Impact ranking — not a ban, an order.** If more than one candidate passes the gate, they're prioritized in this order:

1. The offer itself, removing a step from the flow, adding missing information at the decision point, information architecture and decision structure.
2. Hierarchy and visual weight, copy that answers an objection, a trust signal at the friction point.
3. Color, corner radius, font, generic CTA wording, micro-spacing.

A third-tier candidate with a strong mechanism is still suggested; this isn't a ban, it's a tie-break criterion under equal conditions. The ranking is a heuristic priority, not a measured outcome. The user's test memory (rule 16) overrides this ranking **only for the same component or the same mechanism**: a CTA-color test having won in the past doesn't mean every cosmetic candidate now jumps ahead of structural ones.

These four filters don't replace prioritization, they run before it: the lens answers "is this idea worth suggesting at all," ICE answers "which of the remaining ones goes first." Impact ranking doesn't override ICE: candidates that pass the gate are ranked with ICE; the tier only kicks in for candidate selection and when ICE scores are tied.

## Variable isolation

- A test changes **exactly one variable**. If there's a second difference in Variant B — price, product, rating count, a badge — the test is contaminated (a confound) and the result can't be interpreted. Two differences on the same screen are two separate tests; bundling them into one report doesn't make them one test.
- Variant A is always the control (the current state), Variant B is the test. Don't swap the roles.
- **A test isn't only about changing what already exists.** A page has three kinds of opportunity: changing an existing element, removing an existing element, and **adding an element that doesn't exist**. The third is usually the highest-impact and the least obvious, because whatever's on screen is always what "seems to be there." When evaluating a page, this question is also asked separately: what question is the user asking at this step, and is the answer on screen? Missing information or a missing action can be the subject of a variant.
- **If the user shared their page, A is that page.** Redesigning the control, simplifying it, or making it "representative" invalidates the test — what you're measuring is no longer your suggestion's effect, it's the difference between two separate designs. Whatever's on screen is A; the only thing to be produced is B.
- **Moving to multi-step in a form flow isn't the default fix.** Adding a step opens a new abandonment point at every step; in practice, consolidating onto a single page that fits the screen often works better (grouping related fields, dropping unnecessary fields, reducing vertical spacing). A multi-step form is only suggested when the fields genuinely don't fit one screen or naturally belong to separate phases — and when it is suggested, it's stated as an assumption. **Field count comes before step count:** when testing a form, a field-reduction/unnecessary-field-removal scenario is suggested before a single-page-vs-multi-step scenario — large-scale independent research on checkout usability shows again and again that how many fields you make someone fill in shapes the experience more than how many steps you split the flow into.
- The same product, price, and content are used in both variants; only the tested element differs.

## Statistical hygiene

- Don't declare a winner the first time a result looks significant. There are two separate reasons for this, and they shouldn't be conflated:
  - **Statistical (peeking risk):** Repeatedly checking a test while results are still coming in, and stopping the moment it first looks significant (peeking), pushes the false-positive rate well above the nominal threshold (5%) — even in an A/A test comparing two identical experiences, if it's checked more than once during the run, there's a high chance it will look temporarily "significant" at some point. Fix: don't decide before the pre-determined sample/duration target is reached, look at the result only at the planned point. This is a statistical necessity, but it doesn't mean "never look" — sequential-testing methods can make early looks valid by computing a decision boundary in advance for each planned interim look at the start of the test. `analyze_results.py` doesn't compute this kind of boundary; that's exactly why the rule is binding. Unprepared, repeated raw significance checks (without a sequential boundary) are invalid in every case.
  - **External validity (business-cycle coverage):** The at-least-two-full-weeks rule isn't a statistical-power requirement — it's an experiment-hygiene rule for covering days of the week (weekday/weekend behavior difference), payday effects, and operational cycles. Even if the sample target is reached in 3 days, the test stays open for at least two weeks.
- **Regression to the mean:** In a test's first days, one variant can appear far ahead, then reverse by the third week. The first week's "winner" isn't declared; the wait continues until the curve flattens.
- **Novelty effect:** A change that looks new draws extra attention in the first days purely because it's new; this excess fades over time. The lift of a test that ran briefly and was then closed is most likely a novelty effect, not a lasting behavior change. `ab-test-audit` flags this as a separate finding (see `skills/ab-test-audit/SKILL.md` → audit checklist, novelty-effect item).
- Don't make a campaign, price, algorithm, or design change during the test — it contaminates the data. If a technical bug (a script error, a measurement gap, a wrong segment assignment) is noticed during the test, fix it and restart the test from zero — this is the most common cause of SRM, don't continue with dirty data.
- **The same user shouldn't be in more than one test at the same time.** If two tests touch the same page or flow (e.g. one tests the price card, the other tests the checkout button), the variations mix and it becomes impossible to tell which test produced which result. Tests are either sequenced, or the user pool is fully separated (mutually exclusive traffic). The "Exclusions" field in the setup spec exists for exactly this.
- **Selective attrition check.** If the measurement/data-loss rate is asymmetric between control and variant (e.g. a variant can't collect data from some users for a technical reason — a slow-connection user is more likely to "vanish" from a heavy visual variant), the result is invalid. This differs from SRM: SRM catches a sampling-ratio deviation, selective attrition catches equal sampling with unequal data loss across the two arms. `ab-test-audit` asks about this as a separate check.
- **Exception — early stopping for a guardrail:** the "don't look early" rule is for the primary metric. If a guardrail metric (margin, error rate, support tickets) meaningfully degrades during the test, it's correct to stop the test before the sample fills — here the decision rests on "is there harm," not "who won," a different threshold.
- When switching to a new test tool or when traffic segmentation changes, run an **A/A test** first: two groups see the identical experience; a significant difference means the problem is in the measurement infrastructure, not the product.
  - What to check in an A/A: is the 50/50 split genuinely random, is the p-value distribution uniform, is the sample balanced, is the false-positive rate above what's expected at 5% significance.
  - Don't declare the tool trustworthy from a single A/A; repeat it a few times.
  - **A lighter alternative:** setting up a separate A/A test costs time. Splitting the control in two and running a three-arm test alongside the real variant (A₁ / A₂ / B) does the same verification — if A₁ and A₂ come out significantly different, the tool/segmentation is suspect, with no need to set up a separate test.
- If traffic is **known** to be low (the user said so, or it's obvious from the page's nature, e.g. a return form), move to the alternatives in the Fit table instead of suggesting a classic A/B. Don't ask a question at the front door to learn traffic (rule 5): producing a scenario doesn't depend on traffic, only duration and sample-size math does.

## Interpreting results — overall no-difference doesn't mean segment no-difference

An overall non-significant difference between A and B doesn't mean the test has "no winner." If B wins in one segment (mobile, new users, a specific traffic source) while A wins in another (desktop, returning users), the two can cancel out in total and produce a false "no difference" appearance. When the overall result is reported as "no difference," `ab-test-audit` doesn't close the audit without also asking about at least two basic breakdowns (device, new/returning) — if the per-segment sample isn't sufficient, it writes that as a finding rather than making up a guess.

**Pitfall — don't let a segment sweep turn into p-hacking:** this check exists to understand the result, not to slice the data until a winning subgroup turns up. Segments are only looked at when the overall result is inconclusive/no-difference; if the overall result is already clear, a "maybe it does better in this segment" sweep isn't suggested. ~250-350 conversions is a rough warning threshold indicating the segment sample is "probably too small" — it isn't a substitute for a formal power calculation; real sufficiency per segment is computed from that segment's own baseline rate and target MDE via `analyze_results.py samplesize`. A segment difference below the threshold isn't treated as reliable; it's flagged as a finding that "needs verifying."

**A "no difference" result can have two different causes:** either traffic/duration fell short (low statistical power), or the change wasn't distinct enough to affect the user's behavior. `ab-test-audit` separates the two when reporting a "no difference" finding — was the sample target reached, and if so, was the change itself weak.

**The three lenses of segmentation:** device/user type isn't the only breakdown. A meaningful segment comes from three sources:
- **By source:** the channel traffic arrives from (organic search, social, email, paid). A user from one channel may respond differently to the change.
- **By behavior:** usage frequency or depth (first-time vs. frequent visitor, browses few pages vs. many).
- **By outcome:** what they bought, how much they spent in cart, which plan they signed up for.
One segment can win while another loses; at least one of these three lenses is always asked about on a "no difference" or borderline result.

## Prioritization (ICE)

When suggesting multiple scenarios, rank them with ICE: Impact × Confidence × Ease. A low-effort test on a high-traffic page comes before an ambitious test on a low-traffic page.

The scale is fixed so the same input produces the same ranking (each dimension 1-10, total = the product of the three scores):

| Dimension | 1-3 | 4-7 | 8-10 |
|---|---|---|---|
| Impact | Cosmetic difference, indirect effect on the primary KPI | Plausible effect on the primary KPI | Direct effect at an expensive point in the funnel |
| Confidence | Intuition / industry observation | Archive precedent or an indirect observation in your own data (heatmap, session recording, survey) | A direct signal in your own product, or a repeated past test in your own product |
| Ease | New flow / backend work | Medium-scale front-end work | Copy/style/ordering-level change |

Tie-break order: higher traffic on the target page → simpler to measure (a single clear event) → lower guardrail risk comes first. If traffic is unknown, the first tie-breaker is skipped — it isn't asked per rule 5, and isn't guessed per rule 10; ranking is done with the remaining two criteria. The basis for a confidence score is written in one sentence ("Confidence 8: a similar test on the same page won last quarter"); an unsupported high confidence score isn't given.

**Local-maximum risk:** Stacking only small, single-variable improvements (button color, line spacing, item order) plateaus past a certain point — the small gains run out, and a larger win needs the page itself redesigned. If several small tests in a row come back "no difference" or "negligible" for a product/page, `ab-test-suggest` suggests a bolder/more structural variant in its next suggestion (e.g. restructuring the whole flow, not just one field) and states why. A concrete escape tactic: widen the variable from a single small element to the entire page/flow (a radical-redesign test); once a meaningful winner is found, return to micro-optimization.

**Qualitative feedback is added to quantitative KPIs.** Looking only at numbers can be misleading — user comments explain *why* a KPI changed. Adding a short survey link at the bottom of the test page is a cheap extra signal; it isn't mandatory but is especially recommended on "no difference" or borderline results. Single-question surveys give the highest response rate — example questions: "What's stopping you from completing [action] today?" (to those who didn't complete it), "What almost stopped you from buying?" (to those who did buy, asked right after purchase gives the most honest answer). Support-ticket and cancellation-reason records carry the same signal for free — look for phrases like "but," "worried," "not sure."

## When the archive goes stale — knowing when not to trust it

These scenarios aren't timeless. A scenario's validity drops in these cases; if `ab-test-suggest` notices one of them, it warns when suggesting the scenario, or doesn't suggest it at all:

- **A platform rule changed:** Consent flows, notification policies, browser cookie/tracking restrictions, app-store rules. Measurement or implementation may no longer be possible.
- **Regulation changed:** Discount and reference-price display, data collection, subscription cancellation, accessibility requirements.
- **The pattern became standard:** Something that was once differentiating (guest checkout, mobile responsiveness, search suggestions) is now a baseline expectation, and the test's question turns from "should we add this" into "how should we do it."
- **The technology changed:** If page speed, interface conventions, or device usage have shifted the ground the scenario assumed.
- **It ran dry in your own data:** If the same pattern gave you "no difference" repeatedly in your own product, being in the archive doesn't make it valid for you (see local-maximum risk).

The archive isn't a promise, it's a precedent: a scenario being here doesn't mean it will win in your product, only that it was found worth asking in a similar context before.

When a scenario is invalidated by one of these reasons, it isn't quietly deleted from the archive: what changed and what's suggested instead is written underneath the scenario itself, so the reasoning stays attached to it. The "Market note" lines under a scenario serve the same purpose — the dependency becomes visible, and the user can decide whether it applies in their own context.

## Where this discipline comes from

Most of the discipline here comes from this archive's own field practice. Some of it is widely accepted, repeatedly verified findings in experiment methodology — when a user asks "how do I defend this to my team," these can be described as established practice, but not attributed to any single institution or publication:

- **Peeking and repeated checking raising the false-positive rate** — a standard finding in online controlled experiments; sequential-testing methods exist specifically to solve this problem.
- **Verifying measurement infrastructure with an A/A test** — a classic part of experimentation-platform reliability checks.
- **Sample ratio mismatch (SRM)** — one of the most commonly reported data-quality bugs in large-scale experimentation systems; if there's a deviation, the result isn't read.
- **Novelty effect and regression to the mean** — two known reasons experiment results fade over time.
- **Conversion rate hiding revenue** — this is where the reasoning for using a revenue-based metric (RPV) in price and discount experiments comes from.
- **The normal approximation breaking down for rare events** — a foundational assumption of the two-proportion comparison (see the expected-count check inside `scripts/analyze_results.py`).
- **Selective attrition and cross-test contamination** — common practice across large-scale experimentation infrastructure and open-source A/B testing tools; this playbook lists them as separate items in the statistical-hygiene section.
- **Checkout/form usability** — a recurring finding of independent, long-running usability research; the field-count-before-step-count finding comes from here.

When a user asks for the reason behind a rule, "that's just the rule" isn't a sufficient answer — the reason is explained in one sentence. Choices specific to this playbook with no counterpart in the literature (the three-box format, the ICE scale, archive curation) are stated as such; they aren't presented as external authority. No rule is defended by citing a specific company, product, or publication — the basis itself (statistical reasoning, repeated observation) is enough.

## Market context — language and market aren't the same thing

The user's language being Turkish doesn't mean their target market is Turkey; asking in English doesn't mean their market is the US. This archive grew out of Turkish e-commerce practice, and most of its scenarios are universal (buttons, visuals, ordering, search, forms) — but some are directly market-dependent, and break when carried to a different market.

**Market-dependent behavior classes:**
- **Payment culture:** Credit-card installments are central to the purchase decision in Turkey, MENA, and Latin America; the US and Northern Europe don't have this mechanism, and the "buy now, pay later" (BNPL) equivalent there has a different target audience and trust perception. Installment-scenario results don't transfer between these markets.
- **Source of trust signal:** Which logo signals trust is market-dependent — in one market a bank/card verification mark is familiar, in another the payment provider's or an independent security seal is the stronger signal.
- **Shipping and returns expectations:** In markets where free, no-questions-asked returns are the standard, an "easy returns" callout isn't differentiating, it's table stakes; in markets with weak return culture it's a strong trust signal. The psychological weight of a free-shipping threshold also shifts with shipping cost as a share of cart size.
- **Price perception:** The charm-pricing effect (ending in 9) isn't a universal law, it's a cultural habit; in some markets specific digits carry separate associations.
- **Support-channel expectations:** Sales support via a messaging app or phone can increase trust in some markets, and weaken the perception of professionalism in others.
- **Enterprise purchasing:** Markets where price transparency is expected behave differently from markets where a quote/negotiation culture dominates.

**Regulation is a separate constraint from market.** Discount and reference-price display, cookie/consent flows, data collection, and subscription cancellation are legally bound in some regions — there, the question "which variant sells more" can only be asked among the variants that are actually permitted. Verify the target market's rule before setting up the test; the playbook doesn't know this and doesn't guess it.

**Application:** When a market-dependent scenario is suggested, this dependency is stated in the output (the "Market note" lines under the scenarios). If the user's target market is unknown and a market-dependent scenario is being suggested, which market they're working for is asked first.

## Where this playbook works well, and where it doesn't

A classic 50/50 A/B test isn't the right tool for every business model. Fit is evaluated before producing a suggestion, and if it's low, that's stated plainly.

| Fit | Context |
|---|---|
| High | B2C e-commerce, consumer mobile apps, self-serve SaaS — thousands of weekly sessions, a fast, repeated conversion event |
| Medium | Marketplaces (may have supply/demand side effects), subscriptions, B2B lead forms — testable, but sample size and delayed conversion need care |
| Low | Low-traffic enterprise sales pages, long sales cycles (months), heavily regulated flows (insurance/finance/health offer and contract steps), businesses dominated by physical-store effects |

**What's suggested when fit is low (don't leave a dead end):**
- **Qualitative methods:** A 5-8-person usability test, session-recording review, an exit survey — useful for problem detection even on a small sample; it answers "what's wrong," not "which variant won."
- **Before/after measurement (quasi-experiment):** If random splitting isn't possible, compare the before and after periods while noting seasonality/campaign effects — the causal claim is weak, and that's stated explicitly.
- **A cruder but bigger change:** If there isn't enough traffic to measure a small difference, test a structural change large enough to be measurable (a small MDE demands a huge sample).
- **Move it upstream:** Run the test on a higher-traffic step of the funnel that carries the same problem, not on the low-traffic sub-page.
- **In regulated flows:** If one of the variants changes legal text, mandatory disclosure, or price transparency, it isn't tested; legal/compliance approval is obtained first.

## Scope: single-variable A/B, not multivariate (MVT)

This playbook only produces and audits **single-variable A/B tests** — multivariate testing (MVT), where several elements (headline + image + button color) are tested together in different combinations, is out of scope. Reason: MVT needs very high traffic for a meaningful result, and as the number of combinations grows, telling which element drove the effect gets harder — our whole framework (single variable, three boxes, confound audit) is built around this. Determine fit by computing it, not from a fixed traffic number: in MVT the sample is split separately across each **combination**, so the total traffic needed is roughly the number of combinations × the requirement of a single A/B test. Compute the traffic needed per combination with `analyze_results.py samplesize` using your own baseline rate and MDE; if the resulting number doesn't fit your actual traffic, don't attempt MVT. If the user wants to test multiple elements at once, `ab-test-design` splits this into separate single-variable tests (methodology.md → Variable isolation) and, if MVT is genuinely needed (very high traffic + a question about interaction between elements), states plainly that this is out of the playbook's scope.

## Ethical and legal boundaries

- Showing a price that was never actually charged as the "old price" is a legal risk (reference-price regulation).
- Highlighting the monthly installment amount while hiding the total amount is a transparency violation.
- Don't suggest a variant that produces a dark pattern: an unclosable modal, a hidden cancellation condition, false stock information.

**Ranking evidence/trust signals.** If a variant aims to increase trust (a reference, a badge, a statistic, a case example), they aren't all equally weighted — evidence with context and a real number is stronger than a generic one (e.g. a named reference with a concrete result is more persuasive than a plain logo strip). A concrete number looks more credible than a rounded one, and it usually is more real too ("2,487 users" instead of "2,500 users," when the real figure is available). Evidence is placed at the point of most hesitation (e.g. next to the payment form) — not buried in an FAQ. Rule 6 already applies: a certification you don't hold, a made-up statistic, or a fake reference isn't suggested; this item only describes how to rank real evidence.

**Manipulative-variant check.** When there's doubt about whether a variant is a dark pattern, 5 questions are asked in order: (1) Does it put a deliberately unequal burden between the options presented to the user (asymmetric)? (2) Is its effect hidden from the user (covert)? (3) Does it create a false belief — through an exaggerated claim, missing information, or misleading wording (deceptive)? (4) Does it delay or hide necessary information (hides information)? (5) Does it narrow the user's set of choices (restrictive)? If two or more come back "yes," the variant isn't suggested without revision. Independent research shows a significant share of countdown timers and "low stock" messages rest on scheduled/random generation rather than real data — see CLAUDE.md rule 6.
