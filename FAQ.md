# A/B Testing FAQ

Answers drawn from this repo's own methodology (`knowledge/methodology.md`, `CLAUDE.md`) — not external citations. Where a rule is this playbook's own convention rather than an industry standard, that's said explicitly.

## What should I A/B test first?

Rank candidates with ICE (Impact × Confidence × Ease), not gut feeling. A low-effort test on a high-traffic page beats an ambitious test on a low-traffic one. Where a page already gives you real signal (your own data, or a pattern that already won on a similar page), that carries more confidence than intuition — say so out loud rather than presenting every idea with equal certainty.

## What's a primary metric, and why only one?

The first metric in your KPI list is the one that decides the winner. Treating five metrics as equally important invites p-hacking — you can always find one that moved. Pick one primary metric before the test starts.

## What are guardrail metrics?

Metrics that must not get worse while your primary metric improves — margin, refund rate, page speed, support tickets, abandonment at a later step than the primary. No test ships without at least one. A guardrail measures an independent harm: it is never the complement of the primary (completion and abandonment of the same step are one number written twice). Every measured guardrail has a tolerated-degradation margin; pass/fail guardrails carry a criterion instead. Accessibility is the usual pass/fail case: if the variant adds a touch target or a moving element, or changes focus order or contrast, the plan carries an accessibility check (keyboard and screen-reader review, target size, contrast) that is run on the variant before the test takes traffic — a conversion win that breaks the flow for screen-reader users isn't a win. It is a check, not a metric: analytics can't identify assistive-technology users. A lagging guardrail (returns, cancellations) also declares the window after which it is read, and the ship decision waits for it.

## How many visitors do I need for an A/B test?

This isn't a rule-of-thumb number — it's computed from your actual baseline conversion rate and the minimum effect size you care about detecting (`analyze_results.py samplesize`). Without your real traffic, no duration or sample-size promise is made; asking for a guess and presenting it as a fact is exactly the failure mode this playbook avoids.

## My traffic is low. Can I still run an A/B test?

Often yes, but not with a subtle change read on a distant metric. Three levers, in the order to reach for them: (1) **a bigger minimum detectable effect**: test a bolder change, because the sample you need shrinks roughly with the square of the effect you are trying to detect; (2) **a metric closer to the change**: a step-level conversion moves more, and more often, than end-of-funnel revenue; (3) **variance reduction (CUPED)**: if the same users were measured before the test, their pre-period value explains part of the noise and shrinks the confidence interval without biasing the effect (`analyze_results.py continuous` with a pre-period column). Running longer helps too, but past a couple of months seasonality and returning-user effects start to muddy the comparison. If none of that gets the required sample within reach, the playbook says so and points to qualitative methods or a before/after comparison instead of a split that can't conclude.

## Can I get a Bayesian answer ("probability B beats A")?

Yes: `analyze_results.py bayes` reports the probability that the variant beats control and the expected loss of choosing it. It answers the question stakeholders usually ask more directly than a p-value. It is a second lens, not a loophole: checked continuously and stopped when it looks good, a Bayesian readout has the same optional-stopping problem, and the pre-registered decision rule still decides.

## How do I analyze a test with more than one variant (A/B/n)?

Pass every variant to `analyze_results.py significance`; each one is compared with control and a Holm correction is applied, so only adjusted results count as significant. Plan for it up front: each extra arm splits your traffic further, so size the test with `samplesize --arms`. Each arm must still differ from control in exactly one thing. A test that changes several elements at once in combinations (multivariate) is split into separate single-variable tests instead.

## What is a pre-registration block, and why fix decisions before launch?

A small JSON object `ab-test-design` emits next to the setup spec: the hypothesis, the one variable, the primary metric and its direction, each measured guardrail with its tolerated-degradation margin (a pass/fail guardrail carries a criterion, a lagging one its `read_after_days` window), alpha, power, one- or two-sided test, allocation, planned sample per arm, decision rule and the segments you will look at. Writing these down before the data exists is what keeps the analysis honest: the direction can't be chosen after seeing which way the result went, the planned sample feeds the early-look guard (`--planned-n`), and only the segments named here are read as more than exploratory. It is validated inside the scenario's own JSON (`validate_scenario_json.py <scenario.json>`) before it is shown, and `ab-test-results` reads the result back against it field by field: the declared direction decides which sign is a win, the declared alpha sets the confidence level, and a lagging guardrail makes the verdict provisional until its window closes.

## The variant won on mobile but not on desktop. Is that a real segment difference?

Not by itself. Two separate significance tests, one per segment, answer two separate questions; one coming back significant and the other not is exactly what chance produces even when the true effect is identical. A real claim that the effect differs by segment needs a formal interaction test, or a single segment declared as the decision segment before launch. Picking the best of several pre-named segments after the fact is the same multiple-comparisons problem in a different shape. Without that, report the segment split as a hypothesis for a follow-up test, not as "B won on mobile."

## What is sample ratio mismatch (SRM), and why does it matter?

When your 50/50 (or other) traffic split comes out meaningfully skewed, something is wrong with the experiment's plumbing — not the product. Reading results from a test with SRM is reading noise. The results skill runs `analyze_results.py srm` before anything else, and `significance` repeats the check on the arms it is given: when the split is off, the result is marked `invalid_srm` instead of significant or not.

## Can I peek at results early and stop when they look significant?

No — repeatedly checking a test and stopping the moment it looks significant inflates your false-positive rate well above the nominal 5%, even when there's no real difference (this is a standard, well-established finding in online controlled experiments; sequential-testing methods exist specifically to allow valid early looks by pre-committing to a decision boundary at each check). This repo doesn't implement sequential boundaries, which is exactly why the rule is binding: decide your sample size or duration up front, and look once, at that point. The one exception is a guardrail metric visibly breaking mid-test — that's a "stop for harm" decision, not a "declare a winner" decision, and a different threshold applies.

## Why run a test for at least two full weeks?

Not a statistical-power requirement — a coverage requirement. Weekday/weekend behavior, payday effects, and operational cycles need to be represented in the data. Even if you hit your sample-size target in three days, the test stays open for two weeks.

## What are common A/B testing mistakes that invalidate a result?

- Changing more than one variable in the same test (a confound — you can't tell which change caused the effect).
- Declaring a winner from the first days of data (novelty effect and regression to the mean both distort early results).
- Reading conversion rate alone on a price or discount test — CR almost always goes up when price goes down, but revenue per visitor can drop. Price/packaging tests need a revenue-based primary metric.
- Redesigning "Variant A" when a real page is being tested — if you shared a real page, A is that page exactly as it is; only B changes.
- Running two tests that touch the same page or flow on overlapping traffic, so you can't tell which test produced the result.

## What should I test on an e-commerce checkout or cart page?

Field count before step count is the playbook's own applied finding here — cutting unnecessary fields tends to move completion more reliably than splitting one page into several steps; multi-step is suggested only when fields genuinely don't fit one screen or belong to naturally separate phases, and that's flagged as an assumption when it's suggested. Guardrails to watch: margin, coupon usage, support tickets. Ask `/ab-test suggest` for checkout tests to get the ranked archive set (no page needed); share a screenshot, a URL or a description of your own checkout and `/ab-test design` builds tests for that page instead.

## What should I test on a product detail page (PDP)?

Depends on which problem you actually have: users arriving but not converting, users not starting the flow at all, or volume without quality. This playbook asks that one question first, then returns matching scenarios — it doesn't apply a generic PDP checklist regardless of context.

## What should I A/B test in a SaaS pricing or onboarding flow?

The same single-variable discipline applies, with SaaS-relevant guardrails: cancellation requests, support tickets, plan downgrades — not just signup rate. A test that improves signups but spikes churn or downgrades isn't a win; see `/ab-test audit` for catching that before it ships.

## Is this playbook the right tool for every product?

No, and it says so. The methodology names three fit tiers. **Suitable:** B2C e-commerce, consumer mobile apps, and self-serve SaaS with weekly traffic in the thousands and a fast, repeated conversion event. **Conditional:** marketplaces, subscriptions, B2B lead forms and pre-quote forms in regulated sectors — testable, with care for sample size, delayed conversion and regulated copy. **Poor fit:** low-traffic enterprise sales pages, long sales cycles, or heavily regulated offer and contract steps (insurance, finance, health) — for those, the playbook points to qualitative methods, before/after comparison, or moving the test up-funnel instead of forcing a classic A/B split where it doesn't belong.

## Can I test inside an insurance, pension or credit flow?

Yes, within two limits. A mandatory disclosure, a withdrawal notice, a consent step or an identity check is never the test subject. And the playbook separates two cases: a variant that changes a regulated display itself (legal text, consent wording, a price, rate, cost or return figure, the stated purpose of personal data) is held until the target market's rule is verified; a variant that sits inside the flow but leaves those displays untouched (navigation, ordering, explanatory copy that promises nothing) is produced with compliance sign-off as a pre-start gate. The archive has a dedicated file for these flows: product information, calculators, lead requests, pre-quote forms and a logged-in customer's contract and contribution screens. On a logged-in screen, balances, contract numbers and chart slices are masked on the card, never copied. None of this is legal advice.

## My variant is statistically significant, but it is worse. Is that a result?

Yes: it is a loss, with the same confidence a win would have. The engine reports the direction with the verdict (`significant_improvement` or `significant_degradation`, relative to the direction declared before the test), so "significant" never reads as "ship" on its own. A one-sided test whose data went the other way is reported as harm too, not as "no difference".

## What if a guardrail comes back inconclusive?

Then it is neither clean nor degraded, and it blocks the ship decision until it is resolved. The engine says why: usually the margin is too tight for the traffic (showing that a 4% rate stays inside a 2% relative margin takes about 757,000 users per arm), and it prints the sample that would resolve it. The options are to keep running, or to roll out in stages with that guardrail as the automatic stop condition, as an accepted risk. The margin is never widened after seeing the result; `samplesize --ni-margin` tells you before launch which margin your traffic can resolve.
