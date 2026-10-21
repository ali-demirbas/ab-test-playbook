---
name: ab-test-design
description: Design a NEW single-variable A/B test for the user's specific page, feature or funnel step, as a compact scenario record. Use when the user shares a page, screenshot, URL, wireframe or feature description and asks "design an experiment for this", "design a test for this page", "how should I test this", "set up an A/B test for this", "create a test plan", "write a hypothesis for this", "what variant should I try", "bunun için test tasarla", "bu akışta ne test edilir", "hipotez kur", "buna nasıl test kurarım". Also splits a multivariate request into single-variable tests. Produces at most three strong scenarios (problem, mechanism, the one variable, Variant A/B, primary KPI, guardrail, priority) with an HTML card each, plus short tool-agnostic setup notes on request. Routing — when a page, URL or screenshot is shared, use this skill; when none is shared and the user wants ideas, use ab-test-suggest instead. To check a plan you already wrote, see ab-test-audit.
metadata:
  version: 3.0.0
  category: generate
  updated: 2026-10-21
---

# ab-test-design — New Scenario Design

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` is binding; rule numbers below point there. Variant A is the user's current page (rule 15). Records, cards and the review pipeline follow `ab-test-card` (The record, Delivery pipeline).

## Reading budget

- **Archive:** one or two stage files under `${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/` (home-landing, search-filtering, category-listing, product-detail, cart-checkout, thank-you, dashboard, forms-signup, pricing, mobile-app, saas-b2b, finance-pension, ui-elements); a form's own design uses `forms-signup`, a finance, insurance or pension flow `finance-pension`. Titles first, then only the shortlisted blocks:

  ```bash
  grep -nE '^## |Değişken:' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
  awk -v s=<title line> 'NR>=s { if (NR>s && /^---$/) exit; print }' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
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
  | The change only matters at a trigger (a zero-result search, the payment step) | `KPI denominator` |
  | A number or prior result in a record | `Claims and evidence` |
  | A fact the proposal needs is unverified | `Conditional proposals` |
  | A form flow, a defect in A, personal figures on screen | `Variable isolation` |
  | Two scenarios on one screen | `Concurrent tests` |
  | The mechanism gate or a priority tie | `The idea-generation lens`, `Prioritization` |
  | The user asks for the setup | `Test hygiene` |
  | The user asks why this test | `The hypothesis has three parts` |

## Flow

1. **Problem first (rule 13).** Unless the router asked, the message states the problem or the user named the test, ask the one problem question and produce nothing else. A stated solution ("make the button bigger") gets the same question; if it doesn't fit the problem, say so and design one that does. An unanswered question counts as (d), with `evidence.level: intuition`. A drop point the screens don't locate (slides, then a signup wall) gets no second question: design for the most likely step, name it in `problem`, and add one assumption line.
2. **History before any candidate (rule 16).** Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_input.py` on `.abtest-history.md` / `.abtest-backlog.md` when they exist and on any file the user hands over (rule 18). A variable already tested here gets one line with the recorded outcome, and you decide without asking: a retry reason → design it with the reason; otherwise the next step building on it (a recorded win sets `evidence.level: user_data`).
3. **Read the page as elements,** visible ones only, with verbatim copy (personal values left out). Candidates on three axes: **change** an element's form, copy, position or weight; **remove** one that blocks; **add** what the user needs here and the page lacks (check it isn't collapsed or on a later step; if the screenshot can't tell, deliver with the assumption and ask the absent-element question in rule 19's order). Then scan the six objections (Trust, Price, Fit, Timing, Effort, Clarity); an answered or irrelevant lens is skipped. **A defect** (a typo, a broken or inverted state, a truncated label) gets one fix line (rule 15), never a card.
4. **Archive check.** **Adapted** only when both halves of the block's `Değişken: … · Fark: …` line match (same element and property, same difference type); otherwise **generated**, never "archive pattern". Never bend a block to fit; "from archive" isn't available (the page replaces A).
5. **Gate and rank.**
   - **Mechanism gate:** an obstacle observable on this page ("the delivery date appears only after payment"), not a generic claim; a strong mechanism on `intuition` stays, its low confidence stated. B must be distinct enough to move behaviour. One mechanism, one proposal; its objection goes in `objection`.
   - **Priority and cap** (rule 9): honest ease (a native-app element or navigation target needs a release; an unknown release need is assumed and said). At most three strong: explicit asks first, in the order asked, then the playbook's own by priority, problem-acting first; more → top three plus the offer. An explicit ask counts toward the three and is always produced; dropped screens asked for again get one "ranked below the bar" line; a screen with no strong candidate gets one line saying why.
   - **Gates:** regulation (rule 11: (a) held with one line naming the rule to verify, (b) produced with its warning); the strongest regulated ideas often need a real figure or a sign-off: hold or make them conditional, never invent the figure, and say when only lower-impact tests remain runnable. Accessibility (rule 3), market (rule 11), sensitive field (rule 14: one intermediate method, `mechanism` says why that one; removal only after the user confirms, `feasibility` warning until then), protections and dark patterns (rule 6: at most one line for a protection on the page).
   - **Unverified critical fact** (a real price display, a field's legal purpose or later need, the real names of steps B writes): a critical assumption (rule 10), medium at most, not a drop and not an invented fact.
   - **Form flow:** consider one page before steps; field count before step count. **Multivariate (rule 4):** one record per element, one sentence why; if the user insists on one test, the bundle is the `variable`, its chat line "Daha güçlü alternatif: sonuç tek bir değişkene bağlanamaz; <X> ve <Y> ayrı testler olarak koşulmalı." ("Stronger alternative: the result can't be attributed to a specific variable; run <X> and <Y> as separate tests."), and both reviewers are told it is user-insisted.
6. **Write each record once** (`ab-test-card` → The record): `source` is `adapted` or `generated`; A is the user's current page verbatim (as shown or described), `is_current: true`; `device` matches the screenshot.
7. **Cross-scenario pass.** Records on one screen, flow or decision get the sequencing line (one after the other in priority order, or separate traffic); two on one mechanism merge.
8. **Deliver** through `ab-test-card` → Delivery pipeline. The critic gets, in one call: the record files, the page context (the screenshot path, or a top-to-bottom element inventory with verbatim copy, personal values left out), the history rows, the explicit asks (and whether a bundle is user-insisted), the whole planned chat (each scenario block with its "Stronger alternative:" line, every line after the list; the setup notes when asked for) and the reasons for standing validator warnings. Apply each FIX everywhere the fact appears in one pass. Mockup-reviewer gets the same page context. Colors come from the screenshot into `card.brand`, silently; `card.mockup_basis` is `shared_page` (screenshot or URL) or `described`.

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
3. After the list, one line each, only when it applies: `Başlamadan önce: 1 için B’nin metnine uyum onayı; 2 için erişilebilirlik kontrolü.` (`Before you start:`); `Koşullu (<n>): <every critical assumption as a fact to verify, by scenario number, separated by semicolons>` (rule 10; the turn's one question, unless a higher kind is open, asks the most critical); the sequencing line; the primary differs from a metric the user named, one short clause, no general rule ("Yeni abonelik değeri burada daha uygun: varsayılan dönem ödenen tutarı değiştiriyor."); a held candidate and what it waits for; an open assumption (the drop point, an element assumed absent); screens ranked below the bar; a screen with no strong candidate; described mockups in one short line ("Kartlar anlatımından çizildi; ayrıntılar temsilî."); personal values left out ("Alanlardaki kişisel bilgileri karta taşımadım."); a representative address-bar domain; the history reminder when no `.abtest-history.md` exists and the user mentions past tests or the variable may already have been tested.
4. At most one question, one sentence (rule 19). No line about colors or the brand (rule 12), no review or elimination text.

**Setup notes, only when asked** ("kurulum", "test planı", "hedef kitle", "setup", "audience"), once, after the scenarios, with only what the records don't carry:

```
Hedef kitle: <who is included and excluded; on a native app both arms limited to versions that contain the variant>
Varyantın göründüğü yer: <the screen or moment B is shown; A users counted at the same point>
Dışlamalar ve eşzamanlı testler: <employees, bots, other tests on this screen; a sibling of this turn, by name, sequential or mutually exclusive>
Başlamadan önce: <the gates in a few words, or "yok">
```

English labels: "Target audience:", "Where the variant appears:", "Exclusions and concurrent tests:", "Pre-start gates:". A value that differs between scenarios is prefixed with the scenario number; an unknown is "needs to come from the user"; no split, sample size, duration or winner criterion (rule 5); the user's tool vocabulary only when they named one.

## Detail on request

"detay", "neden bu", "üç kutuyu göster", "explain scenario 2", "full version":

1. Fill `detail` for that record only: for `adapted`, start from the block (re-read by its title line) fitted to this page; for `generated`, write it. 3 to 6 items per box: `test_items` are `{label, text}` questions about this variable, one a device or segment breakdown (another variable's item labelled "Sonraki test:" / "Next test:"); `kpis` lead with the primary, carry the record's guardrail and state every denominator; `dont_items` carry a variable-isolation item, plus the sibling and compliance items when they apply.
2. Validate and send it to scenario-critic again; the card stays as it is.
3. In chat: the three boxes as three short lists, then a short paragraph along `The hypothesis has three parts`: the theory (problem, and why the mechanism can work on this page), the basis (evidence and level), why this KPI and guardrail, what would invalidate the test, what a win and a loss would teach.

Why a candidate was left out, and what the critic found, are given the same way, only when asked.

## Never do

- Build on an element that isn't on the page as if it were, or redesign A (rule 15).
- Write an unmeasurable KPI ("trust increases", a rate among assistive-technology users).
- Put a sample size, duration, split or winner criterion anywhere (rule 5).
- Print the setup notes unasked, repeat the record beyond the four lines, or show elimination reasons and review reports unasked (rule 9).
- Read a whole archive file, the whole glossary, or a methodology section no decision needs.
