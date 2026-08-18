---
name: ab-test-audit
description: Audit an existing A/B test plan, running experiment or mockup pair for methodological flaws. Use when the user says "review my experiment", "is this test set up correctly", "what is wrong with this test", "check my A/B test", "is my test valid", "did I set this up right", "why did my test fail", "does this test have a confound", "test planımı denetle", "bu test doğru mu kurulmuş", "testimde sorun var mı", or shares variant designs, a test brief or a running experiment asking what is wrong. Checks confounds and multi-variable changes, missing or wrong primary metric, absent guardrails, p-hacking and peeking risk, sample ratio mismatch, selective attrition, novelty effect, unrealistic duration and overlapping concurrent tests. To interpret numbers from a finished test, see ab-test-results.
metadata:
  version: 0.1.0
  category: audit
  updated: 2026-08-17
---

# ab-test-audit — Test Plan Audit

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` and `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` are binding.

## Audit checklist

Audit the shared plan/variants in this order; report every finding with its evidence:

1. **Variable isolation (most critical):** is there any difference between A and B OUTSIDE the tested element? Price, product, rating, badge, copy, ordering — any second difference is a confound. If variant visuals were shared, compare them element by element.
2. **Primary metric:** is it single and clear? If multiple metrics are being read with equal weight, flag it as p-hacking risk.
3. **Guardrail:** is a metric that could degrade while conversion rises (margin, returns, speed, support, abandonment) being watched? If not, suggest one fitting the scenario.
4. **Measurability:** can the metrics actually be measured with the tool in place? Flag unproxied "perception" metrics. Is the variant applied client-side (via JS after the page loads) or server-side? In a client-side implementation, the user can briefly see the control variant before it switches (flicker/FOUC) — this both breaks the experience and makes it ambiguous which variant that user should count toward. If unknown, flag it as an assumption that needs verifying.
5. **Sample size/duration:** is the test duration realistic given the traffic volume? Warn if the plan is shorter than two full weeks. If traffic is unknown, write that as a finding, don't make up an estimate.
6. **Hypothesis-implementation consistency:** does what the title/hypothesis says match what the variants actually change? (If the title says "background color" but the variant changes menu order, that's a mismatch.)
7. **Ethics/legal:** fake reference price, a hidden total, an unclosable modal, misleading stock info — flag any as a blocking finding.
8. **Setup hygiene:** is there a planned campaign/price/algorithm change during the test window? Is an A/A validation needed (new tool / new segmentation)?
9. **Novelty-effect risk:** if the test ran for a short period (under a week) and was or is planned to be closed, flag that it can't be told apart whether the measured lift is a lasting behavior change or temporary interest from the change being "new."
10. **Segment check:** if the result is "no difference overall," don't stop there. Was at least a device (mobile/desktop) and user-type (new/returning) breakdown asked for? If not, write as a finding that the two segments may have canceled each other out into a false "no difference." But don't turn this into slicing data until a winning subgroup turns up — don't suggest a segment sweep if the overall result is already clearly conclusive (p-hacking risk). The reverse case is also a finding: if the plan being audited already claims a per-segment winner ("won on mobile, lost on desktop") from two separately run significance tests, flag that this doesn't by itself establish the effect actually differs by segment — that needs a formal interaction test, and "significant in one, not the other" is exactly what chance alone can produce (methodology.md → a second pitfall).
11. **"No difference" diagnosis:** if the result is "no significant difference," separate the reason: was the sample target not reached (insufficient traffic/duration), or was the target reached but the change wasn't distinct enough to move behavior? The two need different fixes (wait longer / design a bolder variant).
12. **Sample ratio mismatch (SRM):** does the actual traffic split match the planned ratio (e.g. 50/50)? Whether the deviation is meaningful isn't determined by a fixed percentage but by sample size: a 52/48 split in a 200-person test is completely normal, the same ratio in a 200,000-person test is a serious signal. Run with `analyze_results.py srm --control-visitors <N> --variant-visitors <N> --expected-split <e.g. 0.5>` — it tests with a chi-square goodness-of-fit test, which differs from the two-proportion z-test (the two arms' counts aren't independent samples, they're parts of the same total, so the `significance` command doesn't apply to this question). If `srm_detected: true` comes back, it's a randomization or tooling bug; the results aren't trustworthy, flag it as a blocking finding. Common cause: the variant-assignment event got mixed up with the outcome-measurement event (e.g. "shown" and "clicked" logged as one event) — these two events must be logged separately, otherwise the source of the SRM can't be found.
13. **Multiple comparisons / peeking:** what's counted here are **decision metrics**, not every metric being tracked. This playbook asks for one primary metric + up to four secondary/guardrail metrics per test; guardrails are watched for "did it break," not used to pick a winner, so they don't count toward the multiple-comparisons count. A finding is written in these three cases: (a) the win decision is tied to more than one metric ("we'll ship if either CR or AOV goes up"), (b) a winner was hunted for in segments that weren't predefined, (c) the result was checked repeatedly and the test was stopped the moment significance appeared. Note separately if there are three or more variant arms. A high guardrail count alone isn't a finding.
14. **History repeat:** if `.abtest-history.md` exists in the working directory, read it (CLAUDE.md rule 16). Has the audited test run on this page before? If it ran and the result was "lost/no difference," ask what changed since then — if nothing changed, the cost of getting the same result again is itself a finding. If the result was "invalid/inconclusive," rerunning it is correct, say so too. If the same variable keeps returning "no difference," suggest a more structural variant (local-maximum risk).
15. **Experiment contamination:** three questions in order:
    - What identity (user ID, device ID, anonymous cookie) is the variant assignment keyed on — does it stay the same across a login/device switch, or is it re-derived per session (sticky bucketing)?
    - Is the "shown" (exposure) event logged separately from the outcome event (purchase, click) — can the "assigned but never shown" gap be queried?
    - Were the segment/rollout rules (a new segment, a changed rollout percentage) updated during the test — and if so, was the chance of a user drifting into a different variant assessed?
    Flag it as an assumption that needs verifying if unknown.
16. **Selective attrition:** is the measurement/data-loss rate equal between control and variant? If one variant systematically collects less data from some users for a technical reason (a heavy page, a late-loading script, a browser incompatibility), the result is invalid — this differs from SRM (SRM questions the sampling ratio, this questions measurement completeness). If there's no evidence, flag it as "needs checking."
17. **Randomization/analysis unit consistency:** what unit was the variant assignment actually randomized on — user, device, or session/visit — and does that match the unit the primary metric counts? A common, easy-to-miss mismatch: randomized by user (or device), but the reported numerator/denominator counts sessions or page views. When the analysis unit is finer-grained than the randomization unit, the same user's repeated sessions aren't independent observations, which the two-proportion z-test assumes they are — the effective sample size is smaller than the raw count suggests, and the reported significance can be optimistic. If the plan doesn't state both units explicitly, flag it as needing verification rather than assuming they match.

## Output format

- Findings in order of severity: `[Blocking] / [Serious] / [Improvement]` tag, each with one sentence for the problem and one for the fix.
- Flag anything you're not sure of as "needs verifying"; don't present it as certain.
- End with a one-paragraph decision: "Can this test run as-is?" — yes/no + condition.

## Never do

- Write a generic remark ("could be improved"); suggest a concrete change for every finding.
- Invent a problem if none was found; "variable isolation is clean" is itself a finding.
