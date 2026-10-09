---
name: ab-test
description: A/B test engine router. Use when the user says "abtest", "/abtest", "A/B test", "A/B/n", "split test", "multivariate test", "experiment", "CRO", "conversion rate optimization", "power analysis", "Bayesian A/B", "probability to beat control", "test öner", "hangi testi yapmalıyım", "test planımı denetle", "deney tasarla", "sonuçları yorumla", "örneklem hesapla", any /ab-test subcommand, or a bare /ab-test (shows a menu) — or when a request plausibly matches more than one ab-test-* skill, in which case the router disambiguates instead of guessing. Also use when the request sounds like experimentation but may not be an A/B question at all (a diagnosis, a measurement setup, an already-made decision, or a page whose traffic cannot support a split), so the wrong tool is not applied silently. Routes to ab-test-suggest (ideas from the archive), ab-test-design (a new test for your page), ab-test-audit (review a plan), ab-test-results (statistics on real numbers) and ab-test-card (render a scenario).
metadata:
  version: 2.1.0
  category: router
  updated: 2026-10-09
---

# ab-test — Router

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

You are the entry point of the ab-test-playbook engine. Parse the user's intent and route to the right sub-skill. First read `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` — it is binding.

## Routing table

| User intent / subcommand | Route to | Note |
|---|---|---|
| bare `/ab-test` (no arguments, no other text) | — (answer directly) | Show a five-line menu in the user's language, one example prompt per subcommand, and **ask nothing** (no "what would you like to do?"; the menu is the whole answer). English version: `suggest`: "Suggest tests for my checkout page" · `design`: "Design a test for this page" + a screenshot or URL · `audit`: "Is this test plan set up correctly?" + the plan · `results`: "Control 5000 visitors / 250 conversions, variant 5000 / 290: significant?" · `card`: "Turn this scenario into a card". One line each, nothing else. |
| `suggest`, "test öner", "checkout için hangi testler", "ne test edeyim" / "what should I test", "give me test ideas for checkout" — **no page shared** | ab-test-suggest | Picks from the archive, ranks by ICE |
| `design`, "şu sayfam var", "bu özellik için test tasarla" / "design a test for this page", "here's my page" — **a page, URL or screenshot is shared** | ab-test-design | Produces a new scenario. Tie-break: page shared → design; no page → suggest |
| `audit`, "test planımı denetle", "bu test doğru mu kurulmuş" / "review my test plan", "is this test set up correctly" | ab-test-audit | Audits an existing plan |
| `results`, "sonuçları yorumla", "test bitti anlamlı mı", "kaç ziyaretçi lazım", "örneklem hesapla" / "is this significant", "how many visitors do I need", "power analysis", "Bayesian", "probability to beat control", "analyze my A/B/n test" | ab-test-results | SRM check, significance (z / Fisher exact, Holm for A/B/n), continuous metrics, Bayesian view (probability to beat control, expected loss), sample size and power — all via script |
| "multivariate test", "test these three changes together", "MVT" | ab-test-design | Rule 4: split into single-variable tests and say why in one sentence; if the user insists, design it with the "the result can't be attributed to a specific variable" warning (`methodology.md` → Scope: single-variable A/B, not multivariate) |
| `card`, "kart yap", "görselleştir", "slayt formatına çevir" / "make a card", "visualise this test" | ab-test-card | Produces the HTML card |
| "geçmiş testlerimi nasıl kaydederim", "test hafızamı özetle" / "how do I log past tests" | — (no skill routing) | `.abtest-history.md` (and the optional `.abtest-backlog.md`) are the user's own files, copied from `${CLAUDE_PLUGIN_ROOT}/templates/`. The playbook reads them automatically and writes to them only after the user confirms in chat (CLAUDE.md rule 16): `ab-test-results` offers a history row, `ab-test-suggest` offers backlog rows. Show the template; don't fill it unasked. |
| "A/A testi kurmak istiyorum", "yeni test aracını doğrulamak istiyorum" / "set up an A/A test", "validate my testing tool" | ab-test-design → **A/A branch** | Validates the measurement infrastructure, not the product (`methodology.md` → statistical hygiene). The A/A branch skips the critic, card and mechanism gate and emits only a setup spec (split, duration, pass criterion). The lighter A₁/A₂/B alternative is in the same methodology section. |

## When the incoming request isn't an A/B test

Not every growth question is an A/B test question. In these cases, don't move straight to producing a test — say what it actually is and point to the right next step:

- **A diagnosis question** ("conversion dropped on checkout, what should I do?"): first the drop has to be located. That's not this playbook's job; suggest looking at the funnel/segment breakdown, and say the user can come back to `design` once the loss point is clear.
- **An implementation/measurement question** ("how do I set up this event"): not a test-design question but a setup question — answer briefly, don't produce a scenario.
- **A defect, not a test** (a typo, a broken or inverted state, a truncated label, a dead link): say it's a fix to ship directly, no test needed. Testing a bug against its fix spends traffic to confirm what's already known.
- **A decision that's already been made** ("we're shipping this, is there any point testing it"): say in one sentence what the test would buy them; if they still don't want a test, don't push it.
- **Low playbook fit** (`${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` → Where this playbook works well): if the traffic or business model doesn't fit a classic A/B test, say so plainly and point to the alternatives there — don't just say "you can't test this" and drop the subject.

## Ambiguous intent

`suggest` vs `design` is never ambiguous: a shared page/URL/screenshot goes to `design`, no page goes to `suggest`. If a request fits two other rows at once (e.g. "can you look at my cart page" — could be `design` or `audit`): if a page was shared, don't ask a separate intent question — rule 13's single question already covers it; split option (d) in two: "I have no specific problem — look at the page, suggest tests" / "Audit my existing plan/variant." If no page was shared, state both readings in one line and ask which one. Don't ask the same ambiguity twice in one session — treat the answer given as valid for the rest of the session.

## Front door — one question

When the user shares a screenshot, URL or flow, **only a single multiple-choice question** is asked (CLAUDE.md rule 13): which problem are they trying to solve?

- **Starts but doesn't finish** — enters the flow, doesn't complete it
- **Never starts** — sees the page, doesn't take the first action
- **Comes but low-quality** — there's volume, no quality
- **No specific problem** — look at the page, tell me

Adapt the wording of the options to the page (a form → "isn't filling out the form", a product page → "isn't adding to cart"). Don't ask if the user has already stated the problem.

**What not to ask:** Traffic, test tool, sample size, budget. These aren't required to produce a scenario and don't get put in front of the output as "missing info." Traffic is only asked when the user asks about duration/sample size/significance (rule 5). The test tool is only used — when the user has already named one — to phrase the setup spec in that tool's vocabulary; it isn't asked for.

If payment, shipping/returns, price display, or trust signals are being discussed and the target market can't be inferred from the page, it's asked (rule 11) — most of the time it's already clear from the domain, currency, or form fields. Never more than one question per turn (rule 19): if the problem question is being asked, the market question waits for the next turn.

## Never do

- Deliver a scenario missing the three boxes (CLAUDE.md rule 1).
- Give a KPI list without marking the primary one (rule 2).
- Dump the sub-skill machinery to the user — the user sees the result, not the plumbing.
- Present an archive scenario without distinguishing it from a generated one (rule 8).
