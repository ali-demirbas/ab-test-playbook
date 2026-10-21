# A/B Testing FAQ

Answers drawn from this repo's own methodology (`knowledge/methodology.md`, `CLAUDE.md`) — not external citations. Where a rule is this playbook's own convention rather than an industry standard, that's said explicitly.

## What does this playbook do, and what doesn't it do?

This playbook proposes, designs, audits and visualizes A/B tests. It doesn't analyze results or compute sample size, duration, significance or a winner; use your testing tool's own reporting for that. Ask it for a number of that kind and it says so in one line and offers to audit your test plan instead. The reason is in the methodology: reading a result correctly depends on how your testing tool assigns users, logs events and computes its statistics, none of which the playbook can see, so a number recomputed from a pasted summary can look precise and still be wrong.

## What should I A/B test first?

Rank candidates by priority, not gut feeling. Each candidate gets a tier (high, medium or low) with a one-sentence reason that weighs, in words, impact (where in the funnel the change acts and what decision it touches), confidence (the evidence behind it) and ease (a copy or ordering change versus a new flow or backend work). There is no numeric score: the reason is what makes the tier checkable. Where a page already gives you real signal (your own data, or a test your history file records as won on a similar page), that carries more confidence than intuition — say so out loud rather than presenting every idea with equal certainty. Ties go to the change at the more important funnel point, then the simpler build, then the lower guardrail risk.

## What's a primary metric, and why only one?

The first metric in your KPI list is the one outcome the test is built to move, named before it starts. Treating five metrics as equally important invites p-hacking — you can always find one that moved. Make it the closest point that is still a business outcome (a completed order, a submitted form), not a click on the way there; a click or step metric stands in only when the outcome event isn't tracked, and then the outcome stays in the list as a guardrail.

## What are guardrail metrics?

Metrics that must not get worse while your primary metric improves — margin, refund rate, page speed, support tickets, abandonment at a later step than the primary. No test ships without at least one. A guardrail measures an independent harm: it is never the complement of the primary (completion and abandonment of the same step are one number written twice). It is written as "must not drop" or "must not rise" with its denominator, and carries no numeric tolerance or reading schedule. A lagging guardrail (returns, cancellations) names its follow-up window inside the metric's name, e.g. "return rate (30 days)". Accessibility is the usual pass/fail case: if the variant adds a touch target or a moving element, or changes focus order or contrast, the plan carries an accessibility check (keyboard and screen-reader review, target size, contrast) with a stated pass criterion, run on the variant before the test takes traffic — a conversion win that breaks the flow for screen-reader users isn't a win. It is a check, not a metric: analytics can't identify assistive-technology users.

## My traffic is low. Can I still run an A/B test?

Sometimes, but not with a subtle change on a quiet page. The playbook doesn't ask for your traffic or compute what it can detect; when a page is known to be low-traffic it says, in words, that it is hard to test and offers ways around it: a bolder, more structural change instead of a small one, moving the test upstream to a busier step of the funnel that carries the same problem, qualitative methods (a short usability test, session recordings, an exit survey) that find what's wrong without a split, or a before/after comparison with its weaker causal claim stated. Whether a given test can conclude on your traffic is a question for your testing tool.

## Can I test several changes at once?

Not in one variant. Every variant pair changes exactly one thing; a second difference is a confound, and the result can't be attributed to either change. Several ideas on one screen become separate single-variable tests, run one after another or with mutually exclusive traffic, never overlapping on the same users. A multivariate test (every combination as its own arm) is outside this playbook's scope. If you insist on changing several things in one variant, the bundle becomes the test's one variable and the output says plainly that the result can't be attributed to any single change.

## What does a proposal look like, and how do I get more detail?

A short structured record of ten pieces: the question-form title, the user problem it targets, a one-sentence mechanism, the single variable, the exact A/B difference, the primary KPI with its denominator, the most important guardrail, the source and evidence level, a priority with its reason, and a warning only when something critical applies. It lives in the scenario JSON. The card shows only the comparison: the question-form title, Variant A and B side by side, the changed element ringed and named in a few words. Chat shows each proposal as its title, one tag line (priority, source, evidence) and the card file. A turn returns at most three strong proposals by default and offers the rest. Ask for detail on one ("explain 2") and it gets the three boxes (what to test, which KPIs to track, what not to do) and a prose explanation, in chat. The archive scenarios themselves keep the three-box format; a new proposal doesn't regenerate it unless you ask.

## Does "archive pattern" mean the idea was tested?

No. The archive is a curated library of test ideas, each found worth asking in a similar context; it isn't a log of tests that won. A proposal resting on it is labelled "archive pattern" ("arşiv örüntüsü") and is never presented as tested, proven or a known win. The validator refuses that wording, and any chance of winning or expected uplift percentage, unless the evidence is your own data; "guaranteed" is refused always.

## How does a card get past review?

Through gates that code and two reviewers share. The validator and the card builder refuse what code can check: a difference outside the ring, a number that changed between A and B without a stated reason, an added button or link without accessibility criteria (touch target, contrast, keyboard, screen reader), a functional change without its invariants, a revenue primary on a coupon or discount change without a guardrail on that benefit, a value shaped like personal data. A layout check, when Node and Playwright are installed, measures the drawn card: clipped content, a blank phone screen, a ring or label covering the screen, text too small or too faint. A methodology critic and a mockup reviewer check what code can't, and each PASS is stamped into the record with a fingerprint of exactly what was reviewed. The builder first writes a draft marked "not reviewed", with a list of every change inside the rings for the mockup reviewer; the final card is written only when both stamps match, so anything edited after its review is refused until it is reviewed again. The limits are stated plainly: a stamp proves the reviewed content is unchanged, not that the review was careful, and the declared invariants and accessibility criteria are checked against the record and the mockup, not tested on your live product.

## What do I get besides the card?

For a designed test, short setup notes written once in chat after the cards: the target audience (who is included and excluded), where the variant appears, exclusions and concurrent tests, and the pre-start gates (compliance sign-off on the variant's exact copy in a regulated flow, an accessibility check of the variant, or "none"). The primary KPI and the guardrail are already in each record and aren't repeated. Anything the playbook doesn't know is written as "needs to come from the user", never guessed. Split ratios, durations and decision rules aren't in them: those belong to your testing tool.

## What are common A/B testing mistakes that invalidate a result?

- Changing more than one variable in the same test (a confound — you can't tell which change caused the effect).
- Measuring the two arms over different denominators: "banner clicks / banner views" has no counterpart in an arm without the banner.
- Reading conversion rate alone on a price or discount test — CR almost always goes up when price goes down, but revenue per visitor can drop. Price/packaging tests need a revenue-based primary metric.
- Calling a revenue rise a win when it came from users losing a benefit: hiding the coupon field can lift revenue because code holders now pay full price. A change that touches a coupon, discount or other user benefit carries a guardrail on that benefit.
- Redesigning "Variant A" when a real page is being tested — if you shared a real page, A is that page exactly as it is; only B changes.
- Running two tests that touch the same page or flow on overlapping traffic, so you can't tell which test produced the result.

## What should I test on an e-commerce checkout or cart page?

Field count before step count is the playbook's own applied finding here — cutting unnecessary fields tends to move completion more reliably than splitting one page into several steps; multi-step is suggested only when fields genuinely don't fit one screen or belong to naturally separate phases, and that's flagged as an assumption when it's suggested. Guardrails to watch: margin, coupon usage, support tickets. Ask `/ab-test suggest` for checkout tests to get the prioritized archive set (no page needed); share a screenshot, a URL or a description of your own checkout and `/ab-test design` builds tests for that page instead.

## What should I test on a product detail page (PDP)?

Depends on which problem you actually have: users arriving but not converting, users not starting the flow at all, or volume without quality. This playbook asks that one question first, then returns matching scenarios — it doesn't apply a generic PDP checklist regardless of context.

## What should I A/B test in a SaaS pricing or onboarding flow?

The same single-variable discipline applies, with SaaS-relevant guardrails: cancellation requests, support tickets, plan downgrades — not just signup rate. A test that improves signups but spikes churn or downgrades isn't a win; see `/ab-test audit` for catching that before it ships.

## Is this playbook the right tool for every product?

No, and it says so. The methodology names three fit tiers. **Suitable:** B2C e-commerce, consumer mobile apps, and self-serve SaaS with plenty of visits and a fast, repeated conversion event. **Conditional:** marketplaces, subscriptions, B2B lead forms and pre-quote forms in regulated sectors — testable, with care for low volume, delayed conversion and regulated copy. **Poor fit:** low-traffic enterprise sales pages, long sales cycles, or heavily regulated offer and contract steps (insurance, finance, health) — for those, the playbook points to qualitative methods, before/after comparison, or moving the test up-funnel instead of forcing a classic A/B split where it doesn't belong.

## Can I test inside an insurance, pension or credit flow?

Yes, within two limits. A mandatory disclosure, a withdrawal notice, a consent step or an identity check is never the test subject. And the playbook separates two cases: a variant that changes a regulated display itself (legal text, consent wording, a price, rate, cost or return figure, the stated purpose of personal data) is held until the target market's rule is verified; a variant that sits inside the flow but leaves those displays untouched (navigation, ordering, explanatory copy that promises nothing) is produced with compliance sign-off as a pre-start gate. The archive has a dedicated file for these flows: product information, calculators, lead requests, pre-quote forms and a logged-in customer's contract and contribution screens. On a logged-in screen, balances, contract numbers and chart slices are masked on the card, never copied. None of this is legal advice.

## What does it do with my past tests?

If you keep a `.abtest-history.md` in your project (from `templates/abtest-history.md`), filled from your testing tool's own results, the skills read it before suggesting, designing or auditing. A variable that already ran on the same page is flagged with the outcome you recorded; a loss isn't a veto when the page has changed, the segment or market differs, or the earlier run was invalid or inconclusive, and the reason is stated. A page where small tests keep coming back "no difference" gets a more structural idea next. The playbook never writes that file and never re-interprets an outcome.
