# ab-test-playbook

A/B test engine for Claude Code. Suggests proven test scenarios by journey stage, designs new ones in a disciplined framework, audits existing test plans for methodological flaws, and renders deck-style scenario cards — text and visual card together by default, no extra ask needed.

Built from an archive of A/B test scenarios used in real e-commerce, mobile app and SaaS growth work — 179 scenarios shipped as text. The visual deck itself is intentionally not included; this repo is the methodology and text content. Every scenario follows the same three-box discipline:

- **Test edilmesi gerekenler** — what questions the experiment must answer
- **Takip edilecek ana KPI’lar** — one primary metric + guardrails that must not degrade
- **Yapılmaması gerekenler** — the mistakes that invalidate the test

## Install

In Claude Code:

```
/plugin marketplace add ali-demirbas/ab-test-playbook
/plugin install ab-test-playbook@ab-test-playbook
```

Or clone and add as a local plugin:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git
claude --plugin-dir ./ab-test-playbook
```

## Usage

| You say | What happens |
|---|---|
| `/abtest suggest` — "checkout için test öner" | Picks matching scenarios from the archive, ranks by ICE, outputs in the three-box format |
| `/abtest design` — "şu sayfam var, test tasarla" (+ screenshot/URL) | Designs a new single-variable scenario for your page in the same framework |
| `/abtest audit` — "bu test doğru kurulmuş mu?" | Audits a plan or variant pair: confounds, missing guardrails, p-hacking risk, unrealistic duration |
| `/abtest results` — "sonuçları yorumla" / "kaç ziyaretçi lazım" | Runs a real two-proportion z-test on your numbers (significance, CI, lift) or calculates required sample size — math via script, never eyeballed — then states the decision and what happens next (staged rollout, guardrail watch, or the follow-up experiment) |
| `/abtest card` — "bunu karta çevir" | Renders the scenario as a single-file HTML card (Variant A/B wireframes + three boxes) |

When you share a page, the router asks exactly one multiple-choice question — which problem you're solving — and nothing else up front; no traffic, tool, or setup questions before it produces a scenario. Sample-size or duration numbers appear only when real traffic data exists — volunteered by you, or asked for when you request them. If you shared a screenshot or page, brand colors are taken straight from it with no question; otherwise it asks once, before the first card, whether to upload a brand guide — say no and it uses a neutral palette. Cards follow the text output automatically: a single designed scenario gets its card immediately; any multi-scenario list gets one right after you pick a scenario.

## What a session looks like

A product-page example, end to end:

**You:** share a screenshot of a product page.

**It asks once:** a single multiple-choice question — which problem you're trying to solve (users start the flow but don't finish / never start / arrive but convert poorly / no specific problem, just look). No traffic, tool, or setup questions up front; those aren't needed to produce a scenario and only get asked if you later ask about sample size or duration.

**It returns** 2-3 full scenarios directly — no "which one should I expand" round-trip — each in the three-box format with the primary KPI marked, guardrails in "must not degrade" form, and an evidence label — `Kanıt: arşiv emsali` when it is a known pattern, `Kanıt: sezgi` when it is a hunch, said out loud rather than dressed up. Variant A is the page exactly as shown, never redesigned.

**Each scenario ships with** the single-variable hypothesis, Variant A/B definitions, and a tool-agnostic setup spec (audience, split, exposure event, guardrail events, attribution window, decision rule) — named in your tool's vocabulary if you mention one — plus the scenario card as a self-contained HTML file (brand colors pulled from your screenshot when you shared one; otherwise a one-time brand-guide question, with a neutral palette as the fallback).

**Test finishes, you paste the numbers** → a real two-proportion z-test runs (never eyeballed), and because this was a price test it also runs the revenue check: conversion up 12% while revenue per visitor drops 4.8% is the finding, not a footnote. Then it states the decision and what happens next — staged rollout with a guardrail watch, or the follow-up experiment if there was no difference.

## What's inside

```
skills/          abtest (router) + suggest / design / audit / results / card
knowledge/       methodology.md · mockup-style.md
                 scenarios/ — curated scenarios by journey stage (TR)
scripts/         analyze_results.py — z-test, sample size, revenue/margin check, sample-ratio-mismatch check (stdlib-only)
                 validate_scenarios.py — format check for the scenario archive
templates/       scenario-card.html · abtest-history.md — test memory template
tests/           test_analyze_results.py — unit tests for the stats engine
evals/           manual acceptance tests for the four core flows (suggest / design / audit / results)
```

Contributing a scenario: follow the three-box format of the existing files, then run the validator — it enforces five items per box, a guardrail in the KPI list, a device/segment question, and typographic rules.

```bash
python3 scripts/validate_scenarios.py
```

## Test memory

Keep a `.abtest-history.md` in your project (copy `templates/abtest-history.md`) and the skills read it before suggesting, designing, or auditing: they will tell you when you have already run this variable on this page and what came of it, stop re-proposing a pattern that already won, and switch to a structural change when the same element keeps returning no difference. After each result, `/abtest results` hands you the row to paste in.

A past loss is information, not a veto — if the page has since changed, or the earlier run was underpowered or invalid, the scenario comes back with the reason stated. The file is yours and stays out of this repo; it is gitignored here.

## Hard rules (CLAUDE.md)

Every output honors these, non-negotiable: one variable per test, one primary KPI, at least one guardrail, no dark patterns, no fake reference prices, no duration estimates without traffic data, and an explicit evidence label on every recommendation — including "this is intuition, treat it as low confidence."

## Language

Scenario content is Turkish (the archive's native language). The skills answer in whatever language you use; metric abbreviations (CR, AOV, LCP, SQL) are kept as-is.

## License

MIT
