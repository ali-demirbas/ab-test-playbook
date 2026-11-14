---
name: ab-test-suggest
description: Suggest A/B test scenarios for a page type or journey stage from a curated pattern archive, ranked by priority. Use when the user asks "what should I test", "what should I A/B test on my checkout / product page / pricing page", "give me A/B test ideas", "CRO ideas", "which tests should I run first", "test öner", "hangi testleri yapmalıyım", "anasayfam için test fikirleri", "ne test edeyim". Writes at most three strong scenarios from knowledge/scenarios/ as records, each delivered as an HTML card via ab-test-card. Use it when NO page of the user's own is shared (no screenshot, URL or described flow), or on a direct /ab-test-suggest; a shared page goes to ab-test-design, a plan to review to ab-test-audit.
metadata:
  version: 3.2.0
  category: recommend
  updated: 2026-11-10
---

# ab-test-suggest: Archive Test Suggestions

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` is binding; rule numbers below point there. Records, cards and the review pipeline follow `ab-test-card` (The record, Delivery pipeline). The archive is read as a source; its three boxes are never regenerated unasked.

## Reading budget

- **Archive:** one or two stage files (Stage map). List titles, shortlist by title and `Değişken:` line, read only the shortlisted blocks (title line to the next `---`):

  ```bash
  grep -nE '^## |Değişken:' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
  awk -v s=<title line> 'NR>=s { if (NR>s && (/^---$/ || /^## /)) exit; print }' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
  ```

  Before calling a candidate `generated`, one title-only grep across all stage files for its element (a sticky button lives under product-detail): `grep -n '^## .*<element keyword>' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/*.md`.
- **KPI names:** `grep -niE '<metric>|<synonym>' ${CLAUDE_PLUGIN_ROOT}/knowledge/kpi-glossary.md` (canonical name and denominator); never the whole glossary.
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
  | Payment, shipping and returns, price display, trust signals, enterprise purchasing | `Market context` |
  | A price, discount, installment or bundle candidate; a KPI or guardrail choice | `KPI rules`, `KPI denominator`, `Guardrails` |
  | A number or prior result in a record | `Claims and evidence` |
  | A fact the proposal needs is unverified | `Conditional proposals` |
  | The mechanism gate or a priority tie | `The idea-generation lens`, `Prioritization` |
  | The block's ground may have shifted (platform rule, regulation, now standard) | `When the archive goes stale` |
  | History shows repeated "no difference" on one page | `Local-maximum risk` |

## Stage map

Files under `${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/`; at most two per turn.

| Page or flow | Stage files |
|---|---|
| Homepage, landing, campaign page | `home-landing.md` |
| Search, filters, results; menu and navigation | `search-filtering.md` |
| Category or listing | `category-listing.md` |
| Product detail | `product-detail.md` |
| Cart, coupon, checkout, address | `cart-checkout.md` |
| Order confirmation, thank-you | `thank-you.md` |
| Logged-in, recurring-use home screen | `dashboard.md` |
| Form, signup, login | `forms-signup.md` |
| Pricing page, price display, plan comparison | `pricing.md` |
| App onboarding, permissions, app home | `mobile-app.md` |
| SaaS commercial decisions (plan default, trial length, paywall) | `saas-b2b.md` |
| Finance, insurance, private pension (BES): product text, calculators, call-back and lead requests, offer steps, contract and contribution screens | `finance-pension.md` (every scenario needs compliance sign-off; disclosures, withdrawal, consent and identity steps are never the subject) |
| Buttons, links, icons on any page | `ui-elements.md` (a lower tier: not first while a stronger candidate exists) |
| Multi-product hub ("choose your product") | `category-listing.md` + `finance-pension.md` for finance lines, else `home-landing.md`; primary = completed quote or lead per assigned hub visitor, product clicks a diagnostic |
| Booking-style search form | `search-filtering.md` + `forms-signup.md`; primary = completed booking per assigned visitor, "search started" the guardrail when submissions can drop |
| Pre-quote insurance or credit form | `finance-pension.md` + `forms-signup.md` |
| App checkout / app paywall | `cart-checkout.md` + `mobile-app.md` / `saas-b2b.md` + `mobile-app.md` |
| SaaS web onboarding; account or settings; order tracking; help or blog | `saas-b2b.md` + `forms-signup.md`; `dashboard.md` + `forms-signup.md`; `thank-you.md` + `dashboard.md`; `home-landing.md` + `search-filtering.md` |

A form's own design lives only in `forms-signup.md`. Subscription cancellation is legally bound: the regulation gate comes first. A page type without a row: one line naming the stages it was mapped to.

## Flow

1. **Context, no questions.** Sector, page and stated problem come from the router or the request. A direct `/ab-test-suggest` that describes a page stays here: A is the stated state (rule 15), the mechanism gate uses the page version (an obstacle observable there) and `card.mockup_basis` is `described` (`shared_page` for a screenshot). Traffic, tool and setup are never asked (rules 5, 13); a baseline rate and visitors the user gave go through `feasibility.py` once, as in `ab-test-design` → Flow step 1 ("not testable": no cards, the alternatives line). Unclear sector or page → the closest stage, said in one line.
2. **History first (rule 16).** Look for `.abtest-history.md` and `.abtest-backlog.md`; run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_input.py <the files that exist>` before reading them, and on any file the user hands over (rule 18). Pull the rows for this page; a queued backlog row is surfaced, not re-suggested. No file → the reminder line, only when the user mentions past tests or a variable may already have been tested.
3. **Retrieve** (Reading budget), candidates acting on the stated problem first. With a named loss point, separate a clogged vein (a busy step that converts poorly: improve it) from a missing link (a step the funnel lacks: add it).
4. **Select.**
   - **Mechanism gate, page-type version:** the obstacle typical for this page type ("on a cart page an open coupon field sends code-less shoppers off to hunt for a code"), stated in `problem` as an assumption to check. A generic reason fails.
   - **Fit, never force-fit:** use a block only when its obstacle plausibly exists in the user's context; when none fits but a strong idea does, generate it. Two candidates on one mechanism are one idea: keep the stronger.
   - **History:** state a recorded outcome as the tool reported it. Won → the next step building on it; lost or no difference → retry only with a stated reason, otherwise one line saying it was left out; inconclusive → suggest, noting the run; a pattern that won on the user's product sets `evidence.level: user_data`.
   - **Order and cap** (rule 9): the tier is the band of the four `priority.inputs` (`Prioritization`), set honestly; the user's explicit asks first, in the order asked, always produced, weak or not; then the playbook's own candidates by priority, problem-acting first, ties as in `Prioritization`; at most three strong, never padded; more → the top three and the count for the offer.
   - **Gates:** regulation (rule 11: hold (a), produce (b) with its warning), accessibility (rule 3), market (rule 11), sensitive fields (rule 14), protections and dark patterns (rule 6); a stale block is flagged or left out. An unverified fact the idea needs → a critical assumption (rule 10), not a drop and not an invented fact.
5. **Write each record once** (`ab-test-card` → The record), localized to the user's sector (a clothing example on a fashion site). `source` is `archive`, `adapted` or `generated`; `problem` is the typical obstacle as an assumption; `is_current: true` only for the user's own page kept here in step 1, else omitted.
6. **Deliver** through `ab-test-card` → Delivery pipeline. The critic gets, in one call: the record files, the page context (page type plus the step 4 assumption), the history rows, the explicit asks, the whole planned chat (each scenario block, "Stronger alternative:" lines included, and every line after the list) and the reasons for standing validator warnings. `card.mockup_basis` is `representative` unless step 1 set it; neutral palette unless a screenshot gives colors.
7. **Backlog (rule 16).** Offer once to append the ranked candidates, strong ones beyond the top three included, to `.abtest-backlog.md` (format `${CLAUDE_PLUGIN_ROOT}/templates/abtest-backlog.md`, tier in `Öncelik`); append only after the user confirms, else show the rows. It is rule 19's kind 9.

## Output

Per scenario, exactly:

```
**<n>. <title>**
Öncelik: <Yüksek/Orta/Düşük> · Kaynak: <arşivden / arşivden uyarlandı / bu sayfa için üretildi> · Kanıt: <kendi verin / arşiv örüntüsü / sektör gözlemi / sezgi>
Neden: <the mechanism in plain words, one sentence, at most 140 characters>
`abtest-card-<slug>.html`
```

English: `Priority: <High/Medium/Low> · Source: <from archive / adapted from archive / generated for this page> · Evidence: <your own data / archive pattern / industry observation / intuition>`, then `Why: …` and the file. The `Neden:` line restates `mechanism` and adds no number or claim (rule 10). Under a weak explicit ask, after `Neden:`: "Daha güçlü alternatif: <the better test>; <why this one is weak>." Nothing else per scenario.

After the list, one line each, only when it applies, in this order:

- `Başlamadan önce: 2 için B’nin metnine uyum onayı; 1 ve 2 için erişilebilirlik kontrolü.` (pre-start gates, once for the set)
- `Koşullu (<n>): <every critical assumption, briefly, as a fact to verify, by scenario number, separated by semicolons>` (rule 10; e.g. "Koşullu (2): 1 için yıllık planın kartta görünen fiyatı; 3 için telefonun teklif hesabında gerekip gerekmediği."); the turn's one question, unless a higher kind is open, asks the most critical
- siblings on one screen, flow or decision run one after the other (priority order) or in separate traffic
- the primary differs from a metric the user named: one short clause, no general rule ("RPV burada daha uygun: kupon alanı geliri de etkiler.")
- a held candidate and what it waits for
- a tested variable retried or left out, with its recorded outcome
- representative or described mockups, only when the user could take them for their own page: "Kartlar anlatımından çizildi; ayrıntılar temsilî."
- the user asked for suggestions beyond their own ideas and no other candidate passed the bar: "Bu sayfa için başka güçlü aday bulamadım."
- the history reminder, only when the user mentions past tests or a variable may already have been tested ("Geçmiş test sonuçlarını `.abtest-history.md` olarak tutarsan önerileri onlara göre süzerim.")

Then the two `feasibility.py` lines as printed, only when the user gave the numbers; the stakeholder brief for scenario 1 (`${CLAUDE_PLUGIN_ROOT}/templates/stakeholder-brief.md`; a file only when asked); then at most one question, one sentence (rule 19), e.g. "2 güçlü aday daha var, devam edeyim mi?" No line about colors or the brand (rule 12), no review or elimination text.

## Detail on request

"detay", "neden bu", "üç kutuyu göster", "explain scenario 2", "full version":

1. Fill `detail` for that record only: from the archive block (re-read by its title line), localized, for `archive` and `adapted`; written for `generated`. 3 to 6 items per box: `test_items` are `{label, text}` questions about this variable, one a device or segment breakdown (another variable's item is labelled "Sonraki test:" / "Next test:"); `kpis` lead with the primary, carry the record's guardrail and state every denominator; `dont_items` carry a variable-isolation item, plus the sibling and compliance items when they apply.
2. Validate and send it to scenario-critic again (the fingerprint changed); the card stays as it is.
3. In chat: the three boxes as three short lists, then a short paragraph of reasons, not a restatement: the problem, why the mechanism can work here, what the evidence rests on, why this KPI and guardrail, what would invalidate the test, what a win and a loss would teach.

Why a candidate was left out, and what the critic found, are given the same way, only when asked.

## Never do

- Read a whole archive file, the whole glossary, or a methodology section no decision needs.
- Repeat the record in chat beyond the four lines, or regenerate the three boxes unasked (rule 9).
- Produce more than three without the offer, pad with a weak candidate, or drop a test the user asked for (rule 9).
- Force-fit an archive scenario, or present two proposals on one mechanism.
- Skip the regulation gate or a market or accessibility warning (rules 3, 11).
- List titles and ask "which one should I expand" (rule 13).
