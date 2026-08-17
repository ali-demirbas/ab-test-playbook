---
name: ab-test-results
description: Interpret A/B test results and run the statistics on real numbers. Use when the user pastes visitor and conversion counts per variant, or asks "is this significant", "interpret these results", "did my test win", "which variant won", "calculate statistical significance", "what is the p-value", "confidence interval", "how many visitors do I need", "what sample size do I need", "how long should I run this test", "minimum detectable effect", "is my traffic split off", "sample ratio mismatch", "SRM", "sonuçları yorumla", "test bitti ne çıktı", "anlamlı mı", "kaç ziyaretçi lazım", "örneklem hesapla". Runs a real two-proportion z-test, confidence interval, required sample size, revenue and margin check, and an SRM check through scripts/analyze_results.py — the math is computed, never estimated — then states the decision and what happens next. To check whether the test was set up correctly in the first place, see ab-test-audit.
metadata:
  version: 0.1.0
  category: analyze
  updated: 2026-08-17
---

# ab-test-results — Result Interpretation and Sample-Size Math

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` and `${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` are binding. Calculations are done with `${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py` — significance and the p-value are never computed by hand or estimated, the script is run.

## Two modes

### A) Interpreting results (test finished or still running)

1. Get the control and variant's visitor + conversion counts. Ask if missing; if a rate was given without visitor counts (e.g. "5% in control, 6% in variant"), ask for the absolute numbers too — a confidence interval can't be computed from a rate alone.
2. Run:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py significance \
     --control-visitors <n> --control-conversions <n> \
     --variant-visitors <n> --variant-conversions <n>
   ```
3. Don't show the raw JSON output; interpret it through the `methodology.md` lens:
   - If `normal_approx_valid: false` comes back, **don't interpret anything else**: the z-test doesn't apply to this test (a rare-event case), the p-value and confidence interval aren't reliable. Don't declare a winner/loser; say more data needs to be collected, or a method suited to rare events should be used. This holds even if the sample is large.
   - If `is_significant: false` comes back, **don't just say "lost" on its own**. Check for a `low_sample_warning`, ask how many days/weeks the test has been running. Separate whether the sample fell short or the change is simply weak (methodology.md → "No difference" diagnosis).
   - If `is_significant: true` comes back, confirm the test has run for **at least two full weeks**. If it hasn't, warn: "statistically significant but doesn't meet the duration rule, there's a regression-to-the-mean risk" — don't declare a definitive winner.
   - If the user also gave a guardrail number (returns, margin, error rate), evaluate it separately; if the guardrail has degraded, flag "should be stopped for the guardrail" even if the primary metric is significant (methodology.md → guardrail early-stop exception).
   - If the user also gave a segment breakdown (mobile/desktop, new/returning), run it separately and compare to the overall result; if they didn't give one and the overall result is "no difference," ask for the segment breakdown.
4. The result sentence must be clear: "significant, ship it" / "significant but duration/sample risk, wait" / "not significant, because X" — don't leave it in between. The decision follows this table (if rows conflict, prioritize the one above):

   **First, ask the "is the sample enough" question correctly.** In the table, "Sufficient" is **not** the absence of `low_sample_warning`. That warning looks at a rough floor of 250 conversions, and the script itself says this isn't a formal sufficiency criterion. Real sufficiency is one thing: **the sample target computed for a pre-specified baseline rate and MDE has been reached.** Compute this with the `samplesize` command:

   - If the user set an MDE before the test, use it.
   - If not, ask along with the observed baseline rate: "what size of difference on this page would be worth shipping for you?" Don't say "sufficient" before an answer comes.
   - If the target hasn't been reached, the sample is **insufficient** — even if the conversion count is many times over 250. In this case, don't declare "no difference"; say "this test didn't have the power to detect this size of effect" and state the sample needed.

   | Significant | Sample (vs. MDE target) | Duration | Guardrail | Decision |
   |---|---|---|---|---|
   | — | — | — | Degraded | **Stop** — whatever the primary metric shows |
   | No | Target not reached | — | Clean | **Continue or declare underpowered** — say how far from the target; if it can't be reached, close the test as "inconclusive," don't say "no difference" |
   | No | Target reached | < 2 weeks | Clean | **Wait** — sample is filled but the duration rule isn't; don't declare "no difference" before the business cycle completes |
   | No | Target reached | ≥ 2 weeks | Clean | **No significant difference** — no effect of the targeted size exists; a smaller effect may still be possible, say so |
   | Yes | Target not reached | ≥ 2 weeks | Clean | **Needs confirmation** — came back significant but was underpowered, the effect size may be inflated; flag it as fragile |
   | Yes | Target not reached | < 2 weeks | Clean | **Wait** — neither the power nor the duration condition is met; the highest-risk case for peeking, don't decide |
   | Yes | Target reached | < 2 weeks | Clean | **Wait** — statistically significant but the duration rule isn't met, there's a regression-to-the-mean risk |
   | Yes | Target reached | ≥ 2 weeks | Clean | **Ship it** — a winner can be declared |

   `low_sample_warning` isn't a decision input in this table; it's only a floor that says "no interpretation below this count is reliable." If it's present, there's no need to even look at the target — the sample is definitely insufficient.
5. **Don't stop after the decision — write the continuation too.** A result interpretation isn't complete on its own; give the step that follows the decision:
   - **If it's shippable:** fill in and present the staged-rollout table below; also say when the control variant gets removed and how the test's learning feeds the next hypothesis (methodology.md → local-maximum risk).

     | Stage | Traffic share | Check frequency | Automatic STOP condition | Continue condition |
     |---|---|---|---|---|
     | 1 | 25% | 1 guardrail check/day | Guardrail moves outside its reference range on 2 consecutive checks → full rollback | 2 consecutive clean checks → stage 2 |
     | 2 | 50% | 1 check/day | Same rule | Same rule → stage 3 |
     | 3 | 75% | 1 check/day | Same rule | Same rule → 100% |
     | 4 | 100% | — | — | Full 7-day guardrail observation from here |

     The stage count and traffic shares aren't fixed — extend the per-stage duration on a low-traffic page, add more stages for a higher-risk change (price, checkout flow); adapt the table to context, don't copy-paste it.

     **"Clean check" and "outside reference" aren't left undefined.** Write out all three when filling the table, or it can't be applied:
     - **Reference range:** the normal fluctuation band for each guardrail before the test (e.g. the daily min and max of the last 4 weeks). If this band doesn't exist, staged rollout isn't started — you can't know what "clean" means without knowing what counts as degraded.
     - **Minimum observation:** how many users must have seen the variant at that stage for a check to count as "clean." If daily volume is low, checks happen when that count is reached, not daily; otherwise you're measuring noise every day.
     - **Degradation threshold:** how far outside the reference band counts as STOP. A single day's deviation may be normal variation — that's exactly what the "2 consecutive checks" rule in the table is for — but a single large deviation far outside the band (e.g. the error rate doubling) is rolled back without waiting for a second check.
   - **If no significant difference:** what's the learning? Was the change weak (a bolder variant), or is the problem elsewhere (a different variable on the same page)? Suggest the next test.
   - **If it lost:** write a one-sentence learning about why the existing experience worked better — a losing test is information too, don't close it silently.
   - **If stopped for a guardrail:** the rollback step + a hypothesis for why the guardrail degraded.
6. **Write the record to test memory (CLAUDE.md rule 16).** After the result interpretation and next step are given, produce this test's `.abtest-history.md` row and present it to the user:

   ```
   | <YYYY-MM> | <page/flow> | <the single variable tested> | <won/lost/no difference/inconclusive/stopped/invalid> | <primary metric impact> | <guardrail status> | <generalizable pattern — fill only if it won, otherwise "—"> | <one-sentence note> |
   ```

   - If `.abtest-history.md` exists in the working directory, offer to add the row to the top of the table; add it if the user confirms.
   - If the file doesn't exist, offer to create it from the `${CLAUDE_PLUGIN_ROOT}/templates/abtest-history.md` template — offer once, don't push it.
   - Pick the result value consistent with the decision matrix: if closed before the sample/duration target was reached, it's **inconclusive**, not "lost"; if there was an SRM or measurement error, it's **invalid**; if stopped for a guardrail, it's **stopped**.
   - **Generalizable pattern** is only filled in on a "won" result — write the abstract mechanism behind the test itself (e.g. not "the shipping bar won," but "a progress indicator strengthens spending behavior"). This makes it visible that the same mechanism is worth trying on other pages (`templates/abtest-history.md` → Generalizable pattern column).
   - Don't write it if the user doesn't want to. This file is their data; if they're working in a public repo, remind them to add it to `.gitignore`.
7. **Don't confuse the two percentages:** the script returns both `absolute_diff` (the percentage-point difference) and `relative_lift_pct` (the relative change) — these are different numbers and get misread if conflated (e.g. going from 5% to 6% is described by both "a 1-point increase" and "a 20% relative increase," but saying "a 1% increase" is wrong). Give both separately and labeled in the output: "control 5.0% → variant 6.0% (1.0 percentage point / 20% relative increase)."

### A2) Revenue check for a price/discount/bundle test

If what's being tested is price, discount, installments, a shipping threshold or a bundle, conversion rate alone is misleading (methodology.md → Conversion rate can hide revenue). Ask the user for both arms' average order value too and run:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py revenue \
  --control-visitors <n> --control-conversions <n> --control-aov <amount> \
  --variant-visitors <n> --variant-conversions <n> --variant-aov <amount> \
  [--margin-rate 0.35]
```

- If the `warning` field is filled in, move it to the top of the output: revenue dropping while conversion rises (or vice versa) is this test's real finding.
- If the margin rate is known, also compute gross profit per visitor with `--margin-rate`; in discount tests, revenue may hold while margin has eroded.
- This command isn't a significance test — the order-value distribution is skewed. Present it as a directional signal, and check the conversion rate's significance separately with `significance`. Don't say "RPV is up 5%, significant."

### B) Sample size / duration planning (before the test starts)

1. Get the baseline conversion rate and the target relative lift (if not given, suggest the typical 10-20% range and ask them to narrow it down).
2. Run:
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/analyze_results.py samplesize \
     --baseline-rate <decimal> --mde <decimal>
   ```
3. Once `required_n_per_variant` comes back, compute how many days it'll take given the user's daily/weekly traffic (`required_n_total / daily_traffic`). Even if it comes out under two full weeks, still recommend at least two weeks (the methodology rule — a short duration carries an external-validity risk even if the sample is sufficient).
4. If no traffic was given at all, don't compute duration — just give the required sample and ask for traffic.

## Never do

- Estimate the p-value or significance without running the script.
- Say "significant, ship it" without asking about the test's duration — the duration rule is as binding as the KPI.
- Dump the raw JSON at the user uninterpreted; every number gets translated into a sentence.
- Write to the test-memory file without the user's confirmation; produce the record, offer to add it, leave the decision to them.
- Make up a random number when computing sample size if the user hasn't given an MDE (target lift); ask.
