---
name: ab-test-design
description: Design a NEW single-variable A/B test for the user's specific page, feature or funnel step, as a compact scenario record. Use when the user shares a page, screenshot, URL, wireframe or feature description and asks "design an experiment for this", "design a test for this page", "how should I test this", "set up an A/B test for this", "create a test plan", "write a hypothesis for this", "what variant should I try", "bunun için test tasarla", "bu akışta ne test edilir", "hipotez kur", "buna nasıl test kurarım". Also splits a multivariate request into single-variable tests. Produces at most three strong scenarios (problem, mechanism, the one variable, Variant A/B, primary KPI, guardrail, priority) with an HTML card each, plus short tool-agnostic setup notes. When a page, URL or screenshot is shared, use this skill; when none is shared and the user wants ideas, use ab-test-suggest instead. To check a plan you already wrote, see ab-test-audit.
metadata:
  version: 3.2.0
  category: generate
  updated: 2026-11-10
---

# ab-test-design: New Scenario Design

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` is binding; rule numbers below point there. Variant A is the user's current page (rule 15). Records, cards and the review pipeline follow `ab-test-card` (The record, Delivery pipeline).

## Reading budget

- **Archive:** one or two stage files under `${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/` (home-landing, search-filtering, category-listing, product-detail, cart-checkout, thank-you, dashboard, forms-signup, pricing, mobile-app, saas-b2b, finance-pension, ui-elements); a form's own design uses `forms-signup`, a finance, insurance or pension flow `finance-pension`. Titles first, then only the shortlisted blocks:

  ```bash
  grep -nE '^## |Değişken:' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
  awk -v s=<title line> 'NR>=s { if (NR>s && (/^---$/ || /^## /)) exit; print }' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
  ```

  Before calling a candidate `generated`, one title-only grep across all stage files: `grep -n '^## .*<element keyword>' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/*.md`.
- **KPI names:** `grep -niE '<metric>|<synonym>' ${CLAUDE_PLUGIN_ROOT}/knowledge/kpi-glossary.md`; never the whole glossary.
- **Methodology:** only the section a decision needs, never at the start of a turn:

  ```bash
  awk -v h='## <section title>' 'index($0,h)==1{p=1;print;next} p&&/^## /{exit} p' ${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md
  ```

  | Decision | Section |
  |---|---|
  | A candidate in a legally bound area (rule 11) | `Regulated flows` |
  | B adds a tap target or moving element, or changes focus or contrast | `Accessibility checks` |
  | A sensitive field (rule 14) | `Sensitive fields` |
  | Doubt whether a variant manipulates (rule 6) | `Ethical and legal boundaries` |
  | Payment, shipping and returns, price display, trust signals | `Market context` |
  | A price, discount, installment or bundle candidate; a KPI or guardrail choice | `KPI rules`, `Guardrails` |
  | The change only matters at a trigger (a zero-result search, the payment step), or the element sits in an accordion, modal, tab or below the fold | `KPI denominator` |
| The user gave a baseline rate and visitors | `Traffic feasibility` |
  | A number or prior result in a record | `Claims and evidence` |
  | A fact the proposal needs is unverified | `Conditional proposals` |
  | A form flow, a defect in A, personal figures on screen | `Variable isolation` |
  | Two scenarios on one screen | `Concurrent tests` |
  | The mechanism gate or a priority tie | `The idea-generation lens`, `Prioritization` |
  | The user asks for the setup | `Test hygiene` |
  | The user asks why this test | `The hypothesis has three parts` |

## Flow

1. **Problem first (rule 13; `ab-test` → Front door).** Skipped when the router already asked, the message states the problem or the user named the test (its assumed problem goes in `problem`). A screenshot with an obvious problem area: design for that area now and ask the question after the scenarios. Otherwise ask the one problem question and produce nothing else. A stated solution ("make the button bigger") gets the same question; if it doesn't fit the problem, say so and design one that does. An unanswered question counts as (d), with `evidence.level: intuition`. A drop point the screens don't locate (slides, then a signup wall) gets no second question: design for the most likely step, name it in `problem`, and add one assumption line. **Traffic (rule 5)** is never asked; when the user gave a baseline conversion rate and eligible visitors, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/feasibility.py --rate <rate> --visitors <n> --per <day|week|month> --lang <lang>` once for the page (`--arms`, `--weeks` only as the user named them), never an estimate of your own. "Not testable": no card; one line saying so with the alternatives (a bolder single change on the main path, a higher-traffic page with the same problem, qualitative research such as user tests or surveys), then stop. "Bold changes only": only a bold B on the main path passes the gate.
2. **History before any candidate (rule 16).** Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_input.py` on `.abtest-history.md` / `.abtest-backlog.md` when they exist and on any file the user hands over (rule 18). A variable already tested here gets one line with the recorded outcome, and you decide without asking: a retry reason → design it with the reason; otherwise the next step building on it (a recorded win sets `evidence.level: user_data`).
3. **Read the page as elements,** once for the whole turn, into a screen inventory every record reuses (never re-read per scenario): top to bottom, visible elements only, verbatim copy (personal values left out), field order, background colours and where a different background region starts and ends, separator lines and borders, button text, colour and position, spacing between sections, and the screen's real top and bottom edge (what is cut off or hidden under a floating widget is unknown, never guessed). Candidates on three axes: **change** an element's form, copy, position or weight; **remove** one that blocks; **add** what the user needs here and the page lacks (check it isn't collapsed or on a later step; if the screenshot can't tell, deliver with the assumption and ask the absent-element question in rule 19's order). Then scan the six objections (Trust, Price, Fit, Timing, Effort, Clarity); an answered or irrelevant lens is skipped. **A defect** (a typo, a broken or inverted state, a truncated label) gets one fix line (rule 15), never a card.
4. **Archive check.** **Adapted** only when both halves of the block's `Değişken: … · Fark: …` line match (same element and property, same difference type); otherwise **generated**, never "archive pattern". Never bend a block to fit; "from archive" isn't available (the page replaces A).
5. **Gate and rank.**
   - **Mechanism gate:** an obstacle observable on this page ("the delivery date appears only after payment"), not a generic claim; a strong mechanism on `intuition` stays, its low confidence stated. B must be distinct enough to move behaviour. One mechanism, one proposal; its objection goes in `objection`.
   - **Priority and cap** (rule 9): the four `priority.inputs` set from the inventory and the evidence, honestly (`main_path` from where the element sits on this screen; `effort` high for a native-app element or navigation target, an unknown release need assumed and said); the tier is their band. At most three strong: explicit asks first, in the order asked, then the playbook's own by priority, problem-acting first; more → top three plus the offer. An explicit ask counts toward the three and is always produced; dropped screens asked for again get one "ranked below the bar" line; a screen with no strong candidate gets one line saying why.
   - **Gates:** regulation (rule 11: (a) held with one line naming the rule to verify, (b) produced with its warning); the strongest regulated ideas often need a real figure or a sign-off: hold or make them conditional, never invent the figure, and say when only lower-impact tests remain runnable. Accessibility (rule 3), market (rule 11), sensitive field (rule 14: one intermediate method, `mechanism` says why that one; removal only after the user confirms, `feasibility` warning until then), protections and dark patterns (rule 6: at most one line for a protection on the page).
   - **Unverified critical fact** (a real price display, a field's legal purpose or later need, the real names of steps B writes): a critical assumption (rule 10), medium at most, not a drop and not an invented fact.
   - **Form flow:** consider one page before steps; field count before step count. **Multivariate (rule 4):** one record per element, one sentence why; if the user insists on one test, the bundle is the `variable`, its chat line "Daha güçlü alternatif: sonuç tek bir değişkene bağlanamaz; <X> ve <Y> ayrı testler olarak koşulmalı." ("Stronger alternative: the result can't be attributed to a specific variable; run <X> and <Y> as separate tests."), and both reviewers are told it is user-insisted.
6. **Write each record once** (`ab-test-card` → The record): `source` is `adapted` or `generated`; A is the user's current page verbatim (as shown or described), `is_current: true`; `device` matches the screenshot; `exposure` names the trigger (KPI denominator → Exposure point), required when the element is shown conditionally and the source of the setup notes' exposure line. **One screen, written once:** from the inventory write `card.screen` once as a node list (kinds per `mockup-style.md` → Screen spec; the page's own colours as node overrides, drawn identically in both arms by construction; the page's real spacing with `mb`/`gap` only where it matters, as in a tight form; `"line": false` on the header when the page draws none), paste the same list into every record on that screen, and give each record its one `card.change` targeting the tested element's `id` (a different screen or stage gets its own list). A is never tidied, re-spaced or improved. Once the draft exists (after the critic's stamp, Delivery pipeline step 4), compare the compiled A with the screenshot by looking at the draft PNG, not by reading markup: a background region drawn white, a separator the page doesn't have, an order or spacing not on screen is fixed in the list, not left for the mockup reviewer (`card` is outside the critic's fingerprint, so this needs no new scenario review). **Plan the ring label's room** in the same pass: a label needs about 31px clear above or below its ring; on a tight page give it room by placing it (`label_pos`) or with a crop or `phone_scale` applied identically to both arms that keeps the test's context, never by removing a field from the middle of A. Fidelity is for the structure, order, key copy, the flow and the tested element; a logo, a decorative icon or a few pixels are represented reasonably, the same in both arms. A colour under the contrast floor stays as it is in A (an icon drawn as a glyph takes `role="img"`: 3:1); when the element is identical in both arms and outside the ring, list it in `card.inherited_contrast` (exact text, colour as measured) and report it in chat as the page's own accessibility defect, never as a pass. A defect on the tested element itself, or a new or worse one in B, still fails the card. **Order:** the validator (Delivery pipeline step 1, without `--strict`: a standing warning goes to the critic with its reason), then the critic and its stamp, then the draft and `render_check.mjs`, then four looks at the draft PNG before the mockup reviewer: (1) the ring label has its ~31px of room and covers no neighbour; (2) the drawn part fits the frame (no clipping, no blank screen under the last element); (3) nothing outside the page (emulator or browser chrome, the dark surround of a screenshot) is drawn as page content; (4) A's elements are in the screen's order. That B differs from A only in the tested element is guaranteed by the builder.
7. **Cross-scenario pass.** Records on one screen, flow or decision get the sequencing line (one after the other in priority order, or separate traffic); two on one mechanism merge.
8. **Deliver** through `ab-test-card` → Delivery pipeline. The critic gets, in one call: the record files, the page context (the screenshot path, or a top-to-bottom element inventory with verbatim copy, personal values left out), the history rows, the explicit asks (and whether a bundle is user-insisted), the whole planned chat (each scenario block with its "Stronger alternative:" line, every line after the list, the setup notes included) and the reasons for standing validator warnings. Apply each FIX everywhere the fact appears in one pass. Mockup-reviewer gets the same page context. Colors come from the screenshot into `card.brand`, silently; `card.mockup_basis` is `shared_page` (screenshot or URL) or `described`.

## Output

In this order, nothing else:

1. The history line and the fix line, when they apply.
2. Per scenario, exactly:

   ```
   **<n>. <title>**
   Öncelik: <Yüksek/Orta/Düşük> · Kaynak: <arşivden uyarlandı / bu sayfa için üretildi> · Kanıt: <kendi verin / arşiv örüntüsü / sektör gözlemi / sezgi>
   Neden: <the mechanism in plain words, one sentence, at most 140 characters>
   `abtest-card-<slug>.html`
   ```

   English: `Priority: … · Source: <adapted from archive / generated for this page> · Evidence: …`, `Why: …`, the file. `Neden:` restates `mechanism`, no number or claim (rule 10). Under a weak explicit ask, after `Neden:`: "Daha güçlü alternatif: <the better test>; <why this one is weak>."
3. After the list, one line each, only when it applies: `Koşullu (<n>): <every critical assumption as a fact to verify, by scenario number, separated by semicolons>` (rule 10; the turn's one question, unless a higher kind is open, asks the most critical); the sequencing line; the primary differs from a metric the user named, one short clause, no general rule ("Yeni abonelik değeri burada daha uygun: varsayılan dönem ödenen tutarı değiştiriyor."); a held candidate and what it waits for; an open assumption (the drop point, an element assumed absent); screens ranked below the bar; a screen with no strong candidate; described mockups in one short line ("Kartlar anlatımından çizildi; ayrıntılar temsilî."); personal values left out ("Alanlardaki kişisel bilgileri karta taşımadım."); a representative address-bar domain; the history reminder when no `.abtest-history.md` exists and the user mentions past tests or the variable may already have been tested.
4. The setup notes (below); their last line carries the pre-start gates ("Başlamadan önce: 1 için B’nin metnine uyum onayı; 2 için erişilebilirlik kontrolü.").
5. The two `feasibility.py` lines exactly as printed, only when the user gave the numbers.
6. The stakeholder brief for scenario 1 (`${CLAUDE_PLUGIN_ROOT}/templates/stakeholder-brief.md`); a file only when asked.
7. At most one question, one sentence (rule 19). No line about colors or the brand (rule 12), no review or elimination text.

**Setup notes, after every designed test,** once, short, with only what the records don't carry. Their last line is the pre-start line, never written a second time:

```
Hedef kitle: <who is included and excluded; on a native app both arms limited to versions that contain the variant>
Maruz kalma (tetikleyici): <the record's `exposure`: who counts as exposed, the moment the tested element is on screen, logged identically in both arms; for an accordion, modal, tab or below-the-fold element, when it is actually shown, and why (counting every visitor dilutes the effect)>
Dışlamalar ve eşzamanlı testler: <employees, bots, other tests on this screen; a sibling of this turn, by name, sequential or mutually exclusive>
Başlamadan önce: <the gates in a few words, or "yok">
```

English labels: "Target audience:", "Exposure (trigger):", "Exclusions and concurrent tests:", "Pre-start gates:". A value that differs between scenarios is prefixed with the scenario number; an unknown is "needs to come from the user"; no split, sample size, duration or winner criterion (rule 5); the user's tool vocabulary only when they named one.

## Detail on request

"detay", "neden bu", "üç kutuyu göster", "explain scenario 2", "full version":

1. Fill `detail` for that record only: for `adapted`, start from the block (re-read by its title line) fitted to this page; for `generated`, write it. 3 to 6 items per box: `test_items` are `{label, text}` questions about this variable, one a device or segment breakdown (another variable's item labelled "Sonraki test:" / "Next test:"); `kpis` lead with the primary, carry the record's guardrail and state every denominator; `dont_items` carry a variable-isolation item, plus the sibling and compliance items when they apply.
2. Validate and send it to scenario-critic again; the card stays as it is.
3. In chat: the three boxes as three short lists, then a short paragraph along `The hypothesis has three parts`: the theory (problem, and why the mechanism can work on this page), the basis (evidence and level), why this KPI and guardrail, what would invalidate the test, what a win and a loss would teach.

Why a candidate was left out, and what the critic found, are given the same way, only when asked.

## Never do

- Build on an element that isn't on the page as if it were, or redesign A (rule 15).
- Write an unmeasurable KPI ("trust increases", a rate among assistive-technology users).
- Put a sample size, duration, split or winner criterion anywhere, ask for traffic, or estimate feasibility without the script (rule 5).
- Leave out the setup notes, repeat the record beyond the four lines, or show elimination reasons and review reports unasked (rule 9).
- Read a whole archive file, the whole glossary, or a methodology section no decision needs.
