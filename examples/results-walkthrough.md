# Results walkthrough: SRM → significance → revenue guardrail → decision → history row

One finished test read end to end the way `/ab-test results` reads it. Every
number below is real output from `scripts/analyze_results.py`, run on the data
this page tells you how to regenerate. The JSON is trimmed to the fields the
skill reads and reflowed onto fewer lines; no value in it is edited.

The data is **synthetic** (a seeded generator, below), so the story is
illustrative, but the arithmetic is not: rerun the commands and you get the same
numbers.

## The test

- **Page:** cart. **Variable:** an estimated delivery date shown under the order total (A: no date; B: "Arrives Fri, 16 Oct").
- **Pre-registered** (the block `ab-test-design` emits before launch): primary = order completion per cart visitor, two-sided, alpha 0.05, power 0.8, MDE 12% relative; guardrail = revenue per cart visitor (RPV), `must_not_decrease`, margin 3% relative; allocation 50/50.
- **Planned sample**, computed before launch from a 4.5% baseline and ~3,600 eligible cart visitors a day:

```bash
python3 scripts/analyze_results.py samplesize --baseline-rate 0.045 --mde 0.12 --daily-visitors 3600
```

```json
{
  "target_rate": 0.0504,
  "mde_relative_pct": 12.0,
  "required_n_per_variant": 24453,
  "required_n_total": 48906,
  "daily_visitors": 3600,
  "duration_days": 14,
  "duration_weeks": 2
}
```

So `planned_n_per_arm` = 24,453 went into the pre-registration, and the test ran for 14 days.

## Regenerating the data

Four per-user CSVs: in-test revenue for each arm (zero for non-buyers) and the
same users' revenue in the 30 days *before* the test, which CUPED uses as a
covariate. Standard library only; the files come out byte-identical on Python
3.9 and 3.13.

```bash
mkdir -p /tmp/abtest-walk && cd /tmp/abtest-walk
python3 - <<'EOF'
import csv, random
random.seed(11)
def arm(name, n, p_buy, start):
    with open(f"{name}.csv", "w", newline="") as f, open(f"{name}-pre.csv", "w", newline="") as g:
        cur, pre = csv.writer(f), csv.writer(g)
        cur.writerow(["user_id", "revenue"]); pre.writerow(["user_id", "revenue_pre30d"])
        for i in range(start, start + n):
            before = round(random.lognormvariate(4.2, 0.7), 2) if random.random() < 0.18 else 0.0
            buys = random.random() < p_buy * (3.2 if before else 0.52)
            now = round(0.9 * before + random.lognormvariate(3.5, 0.5), 2) if buys else 0.0
            cur.writerow([f"u{i}", now]); pre.writerow([f"u{i}", before])
arm("control", 25130, 0.045, 1)
arm("variant", 24870, 0.050, 900001)
EOF
REPO=/path/to/ab-test-playbook   # wherever you cloned it
```

The files hold 1,134 buyers out of 25,130 control users and 1,206 out of 24,870
variant users. Because they arrive as files, the skill scans them first
(CLAUDE.md rule 18):

```bash
python3 $REPO/scripts/validate_input.py control.csv variant.csv control-pre.csv variant-pre.csv
```

Nothing is flagged, so the data is read as data.

## Step 0: SRM, before anything else

```bash
python3 $REPO/scripts/analyze_results.py srm --control-visitors 25130 --variant-visitors 24870 --expected-split 0.5
```

```json
{
  "observed_shares": [0.5026, 0.4974],
  "expected_shares": [0.5, 0.5],
  "chi2": 1.352,
  "p_value": 0.244929,
  "srm_detected": false
}
```

A 50.3 / 49.7 split on 50,000 users is ordinary noise (p = 0.24). Had
`srm_detected` come back `true`, the walkthrough would end here: the result is
**Invalid**, no significance, lift or segment is read, and the history row says
`invalid`.

## Step 1: significance on the primary metric

```bash
python3 $REPO/scripts/analyze_results.py significance \
  --control-visitors 25130 --control-conversions 1134 \
  --variant-visitors 24870 --variant-conversions 1206 \
  --alternative two-sided --planned-n 24453
```

```json
{
  "control_rate": 0.04513,
  "variant_rate": 0.04849,
  "absolute_diff_pp": 0.337,
  "relative_lift_pct": 7.46,
  "method": "z-test",
  "alternative": "two-sided",
  "p_value": 0.07472,
  "confidence_interval_diff": [-0.00034, 0.00707],
  "confidence_interval_relative_lift_pct": [-0.72, 16.31],
  "is_significant": false,
  "decision": "not significant",
  "planned_n_per_arm": 24453,
  "peeking_risk": false,
  "low_sample_warning": false,
  "mde_at_current_n_pct": 11.53
}
```

`--alternative` is the pre-registered direction, not one picked after seeing the
data. `peeking_risk: false` because both arms passed the planned 24,453.
`method: z-test` because the counts are large enough for the normal
approximation; with a handful of conversions the script switches to Fisher's
exact test on its own and says so.

## Step 2: the revenue guardrail (continuous, with CUPED)

RPV is a per-user continuous metric with a heavy right tail, so it never goes
through the proportion test. The guardrail is tested one-sided against its 3%
margin; CUPED uses the pre-period column to cut variance.

```bash
python3 $REPO/scripts/analyze_results.py continuous \
  --control-csv control.csv --variant-csv variant.csv \
  --value-column revenue --id-column user_id \
  --control-pre-csv control-pre.csv --variant-pre-csv variant-pre.csv \
  --pre-value-column revenue_pre30d \
  --ni-margin 0.03 --guardrail-direction must_not_decrease
```

```json
{
  "method": "welch-t-test",
  "control": {"n": 25130, "mean": 3.732507, "sd": 21.891004},
  "variant": {"n": 24870, "mean": 3.996621, "sd": 23.161397},
  "relative_lift_pct": 7.08,
  "p_value": 0.19016,
  "non_inferiority": {
    "margin_relative": 0.03,
    "direction": "must_not_decrease",
    "observed_relative_change_pct": 7.08,
    "p_value": 0.02925,
    "status": "clean"
  },
  "cuped": {
    "join": "id",
    "theta": 0.178388,
    "variance_reduction_pct": 11.88,
    "relative_lift_pct": 7.22,
    "p_value": 0.15475,
    "confidence_interval_diff": [-0.101622, 0.640146],
    "is_significant": false
  }
}
```

The guardrail is **clean**: the one-sided test shows RPV did not fall by more
than 3% (p = 0.029). CUPED removed about 12% of the variance; it narrows the
interval but doesn't change the reading. The pre-period column must be measured
before assignment, which is why it comes from the 30 days before launch.

## Optional: the Bayesian view

Asked "how likely is it that B is better?", the skill can add this, labelled as
a second lens:

```bash
python3 $REPO/scripts/analyze_results.py bayes \
  --control-visitors 25130 --control-conversions 1134 \
  --variant-visitors 24870 --variant-conversions 1206 --seed 1
```

```json
{
  "prior": "Beta(1,1)",
  "prob_variant_beats_control": 0.9631,
  "expected_loss_choose_variant": 2.78e-05,
  "credible_interval_relative_lift_pct": [-0.7, 16.35]
}
```

96% sounds decisive, and it is exactly the trap the pre-registration exists for:
the decision rule was fixed as a two-sided test at alpha 0.05 before launch, and
a Bayesian readout doesn't overrule it after the fact.

## Step 3: the decision

The decision table in `skills/ab-test-results/SKILL.md`, row by row:

| Input | Value |
|---|---|
| SRM | none (p = 0.24) |
| Significant | no (p = 0.075) |
| Sample vs. MDE target | reached (25,130 and 24,870 ≥ 24,453) |
| Duration | 14 days, two full weeks |
| Guardrail | clean (RPV non-inferior at 3%) |

→ **No significant difference at the planned 12% effect.** What the chat says:

> Order completion went from 4.51% to 4.85% (+0.34 percentage points, +7.5%
> relative), not significant (p = 0.075). The test reached its planned sample
> and ran two full weeks, so this isn't a peeking or duration problem: it was
> powered to detect a 12% lift, and the observed effect is smaller. The
> interval (-0.7% to +16.3% relative) still allows both no effect and a real
> lift of that size. Revenue per visitor held (guardrail clean).
>
> Next step: if a ~7.5% lift would be worth shipping, a confirmation run needs
> about 61,337 users per arm, about 5 weeks at your traffic
> (`samplesize --mde 0.075`). Otherwise, a bolder version of the same idea
> (date plus a delivery-promise badge at the payment step) is the stronger next
> test.

## Step 4: the history row

Offered for `.abtest-history.md`, written only if the user confirms (CLAUDE.md
rule 16):

```
| 2026-10 | Cart | Estimated delivery date under the order total (none → shown) | no difference | CR 4.51% → 4.85% (+7.5% rel., p = 0.075, n.s.) | RPV clean (non-inferior at 3%) | — | Powered for 12%; a 7.5% effect needs ~61k/arm (5 weeks) |
```

"No difference" here means the target sample and duration were reached and the
pre-registered effect size didn't show; it is not "lost", and rule 16 means it
doesn't veto a stronger variant of the same mechanism later.
