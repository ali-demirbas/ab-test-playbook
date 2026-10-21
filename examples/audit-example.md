# Audit example: a flawed plan, reviewed

What `/ab-test audit` returns for a plan with most of the common faults in it at
once. The plan is fictional. The audit reviews the proposal itself (UX, CRO,
methodology, ethics, privacy, regulation, accessibility and feasibility); it
doesn't read the plan's numbers.

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

## What the audit says

**[Blocking] Two variables in one variant.** B adds the banner *and* rewrites
the hero button. Any difference can't be attributed to either. Fix: keep the
button copy identical in both arms; test the copy separately.

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

**[Serious] Segments aren't named in advance.** "Ship to whichever of mobile,
desktop, new or returning wins" picks the breakdown after the fact. Name the
breakdowns you will look at before launch (device and new vs returning are the
usual pair). Which segment wins, and whether to ship, is decided in your testing
tool, not in this playbook.

**[Serious] The guardrail isn't an independent harm.** Once the primary is
orders per homepage visitor, cart abandonment is a step that primary already
contains: it can't degrade while the primary improves. A free-returns promise
has an obvious cost the primary can't see: returns. Proposal (to confirm):
"Return rate within 30 days of delivery (per order) must not rise", with the
window written into the KPI's name.

**[Serious] No accessibility check.** B adds a tappable banner. It needs a
pass/fail check on B before launch (keyboard and screen-reader reachable, an
accessible name, touch target size, contrast), not a metric.

**[Serious] The banner's claim is market-dependent and has to be true.** "Free
returns for 30 days" must match the store's actual returns policy in the target
market, which the plan doesn't state. Needs verifying before any traffic.

**[Serious] Client-side switch after load.** Users can see A flash before B
(flicker), which both changes the experience and blurs which arm a user saw.
Needs verifying: whether the tag hides the page until assignment, and whether
exposure is logged separately from assignment.

**[Serious] No "never do" list.** The plan doesn't state what would
invalidate it (rule 1). Written up as a finding; the plan is not rewritten into
the three boxes for the user.

**Not checked: the plan's numbers.** The day-5 counts, the "significant" claim,
the 50/50 split and the 7-day duration are outside this playbook's scope: it
proposes, designs, audits and visualizes A/B tests, and doesn't analyze results
or compute sample size, duration, significance or a winner. Read them in your
testing tool's own report.

## Decision

**Can this test run as-is? No.** Two blocking problems (two variables, unequal
denominators) each invalidate the comparison on their own. It can run once the
button copy is equalised, both arms are measured per homepage visitor with
orders as the primary, the guardrail is an independent harm with its follow-up
window in its name, the accessibility check and the returns-policy check are
closed before launch, the flicker question is answered, and the segments to
look at are named in advance.
