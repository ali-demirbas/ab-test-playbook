---
name: ab-test
description: A/B test engine router. Use when the user says "abtest", "A/B test", "A/B/n", "split test", "multivariate test", "experiment", "CRO", "improve conversion", "dönüşümü nasıl artırırım", "Hangi varyant daha iyi olur?", "test öner", "hangi testi yapmalıyım", "fiyat testi", "test planımı denetle", "deney tasarla", any /ab-test subcommand or a bare /ab-test (shows a menu), or when a request could match more than one ab-test-* skill, so the router disambiguates instead of guessing. Also for requests that may not be A/B questions (a diagnosis, a measurement setup, a decision already made), a delivered scenario's detail ("detay", "neden bu", "üç kutuyu göster"), and results or sizing questions ("anlamlı mı", "kazandı mı", "kaç ziyaretçi lazım", "is it significant", "sample size"), which get the one-line out-of-scope answer. Routes to ab-test-suggest (archive ideas), ab-test-design (a new test for your page), ab-test-audit (review a plan) and ab-test-card (render a scenario).
metadata:
  version: 3.2.0
  category: router
  updated: 2026-11-10
---

# ab-test: Router

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

The entry point of the ab-test-playbook engine: parse the intent and route. First read `${CLAUDE_PLUGIN_ROOT}/CLAUDE.md`: it is binding, and rule numbers below point there.

## What "page shared" means

Defined once, here; `ab-test-suggest`, `ab-test-design` and the evals use it.

- **A page is shared** when the message carries the user's **own** page, screen or flow as a screenshot, a URL or a concrete description ("my pricing page has three plans, the middle one is highlighted, the button under each says …"). A bare page type ("my checkout") is not one. Shared → `ab-test-design`; not shared (a page type, a sector, a stage, or nothing) → `ab-test-suggest`, which also keeps a direct `/ab-test-suggest` call that shares a page.
- **A screenshot is not a page when it shows something else:** a results dashboard or a table of numbers is a results request (out of scope, below); a plan, brief or variant pair with a correctness question goes to `ab-test-audit`. Neither gets the problem question (rule 13).

## Routing table

| User intent / subcommand | Route to | Note |
|---|---|---|
| bare `/ab-test` (no other text) | answer directly | A four-line menu in the user's language, one example prompt per subcommand, nothing asked: `suggest`: "Suggest tests for my checkout page" · `design`: "Design a test for this page" + a screenshot or URL · `audit`: "Is this test plan set up correctly?" + the plan · `card`: "Turn this scenario into a card". |
| `suggest`, "test öner", "ne test edeyim" / "what should I test" with **no page shared** | ab-test-suggest | Archive picks, ranked by priority |
| `design`, "bu sayfa için test tasarla" / "design a test for this page" with **a page shared** | ab-test-design | The verb doesn't decide: "bu ekranlara test öner" with screenshots is `design` |
| "dönüşümü nasıl artırırım" / "improve conversion", "how do I get more signups" | design if a page is shared, else suggest | A test request in other words; a located drop goes through Diagnosis below first |
| "Hangi varyant daha iyi olur?" / "which variant is better?" with two versions shared | ab-test-audit | The pair is reviewed as a test plan; which one wins is what the test answers, never predicted (rule 10). With results attached, the out-of-scope line below |
| "o elediğin ekrana da test yaz" / "give me a test for the one you dropped" | ab-test-design | An explicit ask (rule 9): always produced; weak → its "Daha güçlü alternatif:" line, plus one line that it was ranked below the bar. No new problem question |
| "detay", "neden bu", "üç kutuyu göster", "neden şunu önermedin" / "explain scenario 2", "why did you drop that one" | the skill that produced it | Its Detail on request: `detail` for that one record, re-validated and re-reviewed by scenario-critic (the card stays as it is), the three boxes and the reasons in chat. "Why not that one" gets the reason in prose, no card |
| "kurulum", "hedef kitle", "test planını yaz" / "setup", "audience" about a delivered designed scenario | ab-test-design | Its setup notes again, expanded only where asked; no new card |
| An answer to a "Koşullu" question | the skill that produced it | Confirmed → the assumption is removed and the record goes through the whole pipeline again (a final card without the ribbon); contradicted → the record is rewritten or dropped, said in one line |
| `audit`, "test planımı denetle", "bu test doğru mu kurulmuş" / "is this test set up correctly" with a plan, brief or variant pair | ab-test-audit | |
| "sonuçları yorumla", "anlamlı mı", "kazandı mı", "kaç ziyaretçi lazım", "ne kadar sürmeli", "A/A testi kur", "ön kayıt", "karar kuralı" / "is this significant", "did it win", "sample size", "how long should it run", "set up an A/A test", "pre-registration", "decision rule" | answer directly | One line (rule 5): "This playbook proposes, designs, audits and visualizes A/B tests. It doesn't analyze results or compute sample size, duration, significance or a winner; use your testing tool's own reporting for that." (TR: "Bu playbook A/B test önerir, tasarlar, denetler ve görselleştirir. Sonuç analizi yapmaz; örneklem, süre, anlamlılık veya kazanan hesaplamaz. Bunun için test aracınızın kendi raporunu kullanın.") With a plan in hand, offering to audit it is the turn's one question. No computation, no reading of the numbers |
| The user gives a baseline conversion rate and eligible visitors ("dönüşüm %2,5, günde 1.200 ziyaretçi, test edilebilir mi?") | design if a page is shared, else suggest; alone, answer directly | `${CLAUDE_PLUGIN_ROOT}/scripts/feasibility.py` once, its two lines as printed (rule 5's one exception); "not testable" gets the alternatives instead of a card. A missing number is never asked |
| A plan **and** interim or final numbers | ab-test-audit | The plan is audited; the numbers aren't read, said in one line with the sentence above |
| "fiyat testi", "indirim gösterimini test edelim" / "price test" | design if a page is shared, else suggest | Rule 11's regulation gate first: a changed displayed or reference price is held until the market's rule is verified; a revenue-based primary (`methodology.md` → KPI rules) |
| "şu 8 fikri önceliklendir" / "rank my test ideas" (the user's own list) | answer directly | Each idea through the mechanism gate, then a tier with a one-sentence rationale (`${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` → Prioritization); say which fail and why. Each idea gets the four score inputs and its tier, never ICE or another score. No cards; offering `design` for the top idea is the one question |
| "multivariate test", "MVT", "test these three changes together" | ab-test-design | Rule 4: split, one sentence why; insisted → the bundle with its warning |
| `card`, "kart yap", "görselleştir" / "make a card" | ab-test-card | Through its Delivery pipeline (both reviews) |
| "geçmiş testlerimi nasıl kaydederim" / "how do I log past tests" | answer directly | `.abtest-history.md` is the user's file, kept from their tool (format `${CLAUDE_PLUGIN_ROOT}/templates/abtest-history.md`); the optional `.abtest-backlog.md` follows `${CLAUDE_PLUGIN_ROOT}/templates/abtest-backlog.md` (rule 16). Show the template; don't fill it unasked |

## When the request isn't an A/B test

These checks come before the routing table; a trigger phrase in the same message doesn't override them.

- **Diagnosis** ("checkout dönüşümüm düştü, hangi testi yapmalıyım?"): a drop without a located step is located first, with the funnel or segment breakdown; `design` follows once the loss point is clear.
- **Implementation or measurement** ("how do I set up this event"): answer briefly, no scenario.
- **A defect** (a typo, a broken or inverted state, a dead link): a fix to ship, no test needed.
- **A decision already made**: one sentence on what a test would buy; don't push it.
- **Poor fit** (`${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md` → Where this playbook works well; tiers Suitable / Conditional / Poor fit, not the priority words): a low-volume enterprise page or a months-long cycle is said plainly, with the alternatives there. A Conditional context (a regulated pre-quote form, a subscription) is still tested, with that tier's care.

## Ambiguous intent

`suggest` versus `design` is never ambiguous (above). A request fitting two other rows ("can you look at my cart page": design or audit?): with a page shared, rule 13's question covers it, option (d) split in two ("no specific problem, suggest tests" / "audit my existing plan or variant"); with no page, state both readings in one line and ask which. Never the same ambiguity twice in a session.

## Front door: one question

Rule 13 decides when the problem question is asked; word it for the page (a form → "isn't filling out the form", a product page → "isn't adding to cart"):

- **Starts but doesn't finish** (enters the flow, doesn't complete it)
- **Never starts** (sees the page, doesn't take the first action)
- **Comes but low quality** (volume, no quality)
- **No specific problem** (look at the page, tell me)

Skipped when the message states the problem or names the test. A screenshot with an obvious problem area (an obstacle visible on the page, such as a CTA below the fold or an open coupon field) gets that area's cards in the same turn, the assumed problem in `problem`, and this question after them as the turn's one question (rule 19). Otherwise it holds the turn. Either way it is asked once for several screens and not again in the session; no pick → (d); after the answer, a screen with no strong candidate gets one line. Traffic, test tool and budget are never asked (rule 5); a named tool only shapes the setup notes' vocabulary. A market question (rule 11) waits its turn under rule 19 and is usually answered by the domain, currency or fields.

## Never do

- Deliver anything but a complete record (rule 1), with exactly one primary KPI (rule 2), as a final or conditional card after both reviews (rule 17), never a draft except rule 9's UNVERIFIED preview.
- Regenerate the three boxes unasked, or dump the sub-skill machinery to the user.
- Compute, estimate or interpret a sample size, duration, significance or winner (rule 5).
- Present an archive scenario as generated, or as a tested win (rule 8).
