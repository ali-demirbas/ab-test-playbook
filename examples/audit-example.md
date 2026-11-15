# Audit example: a flawed plan, reviewed

What `/ab-test audit` returns for a plan with most of the common faults in it at
once. The plan is fictional. The audit reviews the proposal itself (UX, CRO,
methodology, ethics, privacy, regulation, accessibility and feasibility); it
doesn't read the plan's numbers. Turkish version: [`audit-example.tr.md`](audit-example.tr.md).

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
python3 scripts/validate_input.py --lang en plan.md
```

Nothing instruction-shaped in it, so it is audited as data.

## What the audit says

The table comes first, most severe first, each row with the fixed label its
checklist item gives (`[Critical]`, `[Serious]`, `[Moderate]`, `[Note]`;
Turkish `[Kritik]`, `[Ciddi]`, `[Orta]`, `[Not]`). Details follow only for the
critical rows, and the fixed plan closes the audit.

| Severity | Finding | Fix |
|---|---|---|
| [Critical] | B also rewrites the hero button | Keep "Shop now" in both arms; test the copy separately |
| [Critical] | "Banner clicks / banner views" exists only in B | Count both arms over everyone who reached the homepage |
| [Serious] | No hypothesis | The sentence in the fixed plan |
| [Serious] | Banner clicks stand in for orders | Orders per homepage visitor as primary; clicks a diagnostic |
| [Serious] | Cart abandonment sits inside that primary | Guard returns, the harm a free-returns promise can cause |
| [Serious] | The tappable banner has no accessibility check | A pass/fail check on B before traffic |
| [Serious] | The winning segment is picked after the fact | Name the breakdowns before launch |
| [Moderate] | Nothing says what would invalidate the test | The "Held constant" line below |

**Decision: it cannot start as designed; it can start with the fixed plan.**

**B also rewrites the hero button.** A difference could come from either
change, so neither can be credited.
**"Banner clicks / banner views" exists only in B.** A has no banner, so the
arms are measured on different populations.

To verify: free 30-day returns are the store's real policy in the target
market; the tag hides the page until assignment and logs exposure apart from
it; no other test runs on the homepage.

Of the 20 headings checked, clean: Targeting and measurement scope, Exposure
point, Ethics, protections and regulation, Privacy, Setup hygiene, Multivariate
plans, Selective attrition, History.

Not checked: the day-5 counts, the "significant" claim, the 50/50 split and the
7-day duration. This playbook proposes, designs, audits and visualizes A/B
tests. It doesn't analyze results or compute sample size, duration,
significance or a winner; use your testing tool's own reporting for that.
If you share your baseline conversion rate and eligible visitors, I can show a rough detectable range.

**Fixed plan**
- Variable: a "Free returns for 30 days" banner under the hero.
- A: the current homepage, button "Shop now".
- B: the same page plus the banner; the button still reads "Shop now".
- Hypothesis: free 30-day returns shown before shopping answer the fit objection, so more visitors order; we'd learn whether returns anxiety blocks first purchases.
- Primary KPI: Conversion rate (CR), orders per assigned homepage visitor, counted from homepage load in both arms (banner clicks: a B-only diagnostic).
- Guardrail: Return rate (30 days), per order, must not rise.
- Held constant: the hero, the button copy, prices; a second change or an overlapping homepage test invalidates it.
- Before you start: the accessibility check on the banner (keyboard, a screen-reader name, a target of at least 44×44 pt, contrast of at least 4.5:1); the facts above verified; breakdowns: device, new vs returning.

If you like, I'll turn the fixed plan into a card.
