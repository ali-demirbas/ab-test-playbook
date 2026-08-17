# A/B Testing FAQ

Answers drawn from this repo's own methodology (`knowledge/methodology.md`, `CLAUDE.md`) — not external citations. Where a rule is this playbook's own convention rather than an industry standard, that's said explicitly.

## What should I A/B test first?

Rank candidates with ICE (Impact × Confidence × Ease), not gut feeling. A low-effort test on a high-traffic page beats an ambitious test on a low-traffic one. Where a page already gives you real signal (your own data, or a pattern that already won on a similar page), that carries more confidence than intuition — say so out loud rather than presenting every idea with equal certainty.

## What's a primary metric, and why only one?

The first metric in your KPI list is the one that decides the winner. Treating five metrics as equally important invites p-hacking — you can always find one that moved. Pick one primary metric before the test starts.

## What are guardrail metrics?

Metrics that must not get worse while your primary metric improves — margin, refund rate, page speed, support tickets, abandonment elsewhere in the funnel. No test ships without at least one. If a variant changes something that could affect accessibility (keyboard/screen-reader use, touch target size, contrast, motion), accessibility is a guardrail candidate too — a conversion win that breaks the flow for screen-reader users isn't a win.

## How many visitors do I need for an A/B test?

This isn't a rule-of-thumb number — it's computed from your actual baseline conversion rate and the minimum effect size you care about detecting (`analyze_results.py samplesize`). Without your real traffic, no duration or sample-size promise is made; asking for a guess and presenting it as a fact is exactly the failure mode this playbook avoids.

## What is sample ratio mismatch (SRM), and why does it matter?

When your 50/50 (or other) traffic split comes out meaningfully skewed, something is wrong with the experiment's plumbing — not the product. Reading results from a test with SRM is reading noise. `analyze_results.py` checks for this before any result is interpreted.

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

Field count before step count is the playbook's own applied finding here — cutting unnecessary fields tends to move completion more reliably than splitting one page into several steps; multi-step is suggested only when fields genuinely don't fit one screen or belong to naturally separate phases, and that's flagged as an assumption when it's suggested. Guardrails to watch: margin, coupon usage, support tickets. Run `/ab-test suggest` on a checkout screenshot for the full, ranked scenario set.

## What should I test on a product detail page (PDP)?

Depends on which problem you actually have: users arriving but not converting, users not starting the flow at all, or volume without quality. This playbook asks that one question first, then returns matching scenarios — it doesn't apply a generic PDP checklist regardless of context.

## What should I A/B test in a SaaS pricing or onboarding flow?

The same single-variable discipline applies, with SaaS-relevant guardrails: cancellation requests, support tickets, plan downgrades — not just signup rate. A test that improves signups but spikes churn or downgrades isn't a win; see `/ab-test audit` for catching that before it ships.

## Is this playbook the right tool for every product?

No, and it says so. It fits best for B2C e-commerce, consumer mobile apps, and self-serve SaaS with weekly traffic in the thousands and a fast, repeated conversion event. It fits less well for low-traffic enterprise sales pages, long sales cycles, or heavily regulated flows (insurance/finance/health offer and contract steps) — for those, the playbook points to qualitative methods, before/after comparison, or moving the test up-funnel instead of forcing a classic A/B split where it doesn't belong.
