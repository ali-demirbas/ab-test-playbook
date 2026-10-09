# Audit example: a flawed plan, reviewed

What `/ab-test audit` returns for a plan with most of the common faults in it at
once. The plan and its numbers are fictional; the script outputs are real runs
of `scripts/analyze_results.py` on those numbers, trimmed to the fields the
audit cites.

## The plan the user brought

Shared as a file, `plan.md`:

> **Test:** homepage returns banner. **A:** current homepage. **B:** adds a
> "Free returns for 30 days" banner under the hero, and the hero button reads
> "Shop the new season" instead of "Shop now".
> **Primary metric:** banner click-through rate (banner clicks / banner views).
> **Guardrail:** cart abandonment must not get worse.
> **Setup:** 50/50, variant applied in the browser by our tag after the page
> loads. 7 days.
> **Decision:** ship to whichever of mobile, desktop, new or returning users wins.
> **Day 5 so far:** control 18,200 visitors, variant 17,350. Orders: mobile
> 270 / 9,000 vs 309 / 8,600 (significant!), desktop 368 / 9,200 vs 362 / 8,750.

The file is scanned before it is read (CLAUDE.md rule 18):

```bash
python3 scripts/validate_input.py plan.md
```

Nothing instruction-shaped in it, so it is audited as data.

## The numbers the audit runs

**SRM** on the day-5 split:

```bash
python3 scripts/analyze_results.py srm --control-visitors 18200 --variant-visitors 17350
```

```json
{"observed_split": 0.51195, "chi2": 20.3235, "p_value": 7e-06, "srm_detected": true}
```

**The "won on mobile" claim**, checked the way it has to be checked, as an
interaction rather than two separate tests. This is shown to explain the method
problem only; with an SRM, none of these numbers is read as a result.

```bash
python3 scripts/analyze_results.py interaction \
  --seg1 9000:270,8600:309 --seg2 9200:368,8750:362 \
  --seg1-name mobile --seg2-name desktop
```

```json
{
  "segments": [
    {"name": "mobile", "relative_lift_pct": 19.77},
    {"name": "desktop", "relative_lift_pct": 3.43}
  ],
  "interaction_relative": {"ratio_of_rate_ratios": 1.15797, "p_value": 0.18004, "is_significant": false},
  "effect_differs": false,
  "decision": "no evidence the effect differs between segments"
}
```

Separately, mobile alone gives p = 0.027 and desktop alone p = 0.64, which is
exactly the "significant in one, not the other" pattern chance produces.

## What the audit says

**[Blocking] Two variables in one variant.** B adds the banner *and* rewrites
the hero button. Any difference can't be attributed to either. Fix: keep the
button copy identical in both arms; test the copy separately.

**[Blocking] Sample ratio mismatch.** 51.2 / 48.8 on 35,550 visitors is not
noise (chi-square p = 0.000007). Results from this run aren't trustworthy.
Fix: find where variant users are lost (a client-side tag that fails to load,
assignment logged together with exposure), fix it, restart.

**[Blocking] Different denominators.** "Banner clicks / banner views" exists
only in B, since A has no banner, so the two arms are not measured on the same
population. Fix: measure both arms over everyone who reached the homepage.

**[Serious] The primary metric is a mid-funnel proxy.** Banner clicks can rise
while orders stay flat. The change is meant to reduce returns anxiety before
purchase, so the primary is orders (or revenue) per homepage visitor; banner
clicks stay as a diagnostic.

**[Serious] No hypothesis.** The plan never says why a returns banner would
change behavior. Suggested: "Showing free 30-day returns on the homepage
answers the fit objection (what if it doesn't fit?) earlier, so more visitors
start shopping; we'd learn whether returns anxiety blocks first purchases."

**[Serious] Picking the best of four segments.** "Ship to whichever of mobile,
desktop, new or returning wins" is four chances at a false winner. The
interaction run above shows the mobile/desktop gap is not evidence of a real
difference (p = 0.18). Fix: declare one decision segment before launch, or
decide on the overall result and treat segments as exploratory, testing a
segment difference only with `interaction`.

**[Serious] Guardrail without a number.** "Must not get worse" can't be
decided. Proposal (to confirm): cart abandonment must not rise more than 2%
relative, tested one-sided.

**[Serious] Client-side switch after load.** Users can see A flash before B
(flicker), which both changes the experience and blurs which arm a user saw.
Needs verifying: whether the tag hides the page until assignment, and whether
exposure is logged separately from assignment.

**[Improvement] Duration.** Seven days misses weekly cycles; plan at least two
full weeks, sized with `samplesize` once the primary metric is fixed.

**[Improvement] No "never do" list.** The plan doesn't state what would
invalidate it (rule 1). Written up as a finding; the plan is not rewritten into
the three boxes for the user.

## Decision

**Can this test run as-is? No.** Three blocking problems (two variables, SRM,
unequal denominators) each invalidate the result on their own. It can run once
the button copy is equalised, the assignment bug behind the SRM is fixed, both
arms are measured per homepage visitor with orders as the primary, the
guardrail has a margin, and either one segment is pre-declared or segments are
read as exploratory. Restart the count from day 1 after the fix.
