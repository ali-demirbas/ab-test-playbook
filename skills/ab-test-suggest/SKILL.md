---
name: ab-test-suggest
description: 'Suggest A/B test scenarios for a page type or journey stage from a curated pattern archive, ranked by priority. Use when the user asks "what should I test", "what should I A/B test on my checkout / product page / pricing page", "give me A/B test ideas", "CRO ideas", "which tests should I run first", "test öner", "hangi testleri yapmalıyım", "anasayfam için test fikirleri", "ne test edeyim". Writes at most three strong scenarios from knowledge/scenarios/ as records, each delivered as an HTML card via ab-test-card. Use it when NO page of the user''s own is shared (no screenshot, URL or described flow), or on a direct /ab-test-suggest; a shared page goes to ab-test-design, a plan to review to ab-test-audit.'
metadata:
  version: 3.4.0
  category: recommend
  updated: 2026-11-14
---

# ab-test-suggest: Archive Test Suggestions

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` is binding; rule numbers below point there. Records follow `${CLAUDE_PLUGIN_ROOT}/templates/record-checklist.md`; cards and the review pipeline `ab-test-card` (Reading, Delivery pipeline). The archive is read as a source; its three boxes are never regenerated unasked.

## Reading budget

- **Archive:** one or two stage files (Stage map). List each block's head, shortlist by title, variable and tags, read only the shortlisted blocks, in the user's language (`--lang en`: the block's English body when it has one, else its English title and the Turkish body; `--lang tr` stops before the English body):

  ```bash
  grep -nE '^(## |Değişken:|Etiket:|EN:)' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/read_section.py ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/<stage>.md --line <title line> [<title line> ...] --lang <tr|en>
  ```

  The tags map to record fields as `record-checklist.md` → From an archive block says.

  Before calling a candidate `generated`, one title-only grep across all stage files for its element (a sticky button lives under product-detail): `grep -n '^## .*<element keyword>' ${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/*.md`.
- **KPI names:** `grep -niE '<metric>|<synonym>' ${CLAUDE_PLUGIN_ROOT}/knowledge/kpi-glossary.md` (canonical name and denominator); never the whole glossary.
- **Methodology:** only the section a decision needs, never at the start of a turn:

  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/read_section.py ${CLAUDE_PLUGIN_ROOT}/knowledge/methodology.md "<section title>"
  ```

  | Decision | Section |
  |---|---|
  | A candidate in a legally bound area (rule 11) | `Regulated flows` |
  | B adds a tap target or moving element, or changes focus or contrast | `Accessibility checks` |
  | A sensitive field (rule 14) | `Sensitive fields` |
  | Doubt whether a variant manipulates (rule 6) | `Ethical and legal boundaries` |
  | Payment, shipping and returns, price display, trust signals, enterprise purchasing | `Market context` |
  | A price, discount, installment or bundle candidate; a benefit B touches (coupon, free shipping, refunds); a KPI or guardrail the glossary and `record-checklist.md` don't settle | `KPI rules`, `KPI denominator`, `Guardrails` |
  | A number or prior result in a record | `Claims and evidence` |
  | A fact the proposal needs is unverified | `Conditional proposals` |
  | A mechanism the gate (Flow step 4) doesn't settle, the impact ranking, or a priority tie | `The idea-generation lens`, `Prioritization` |
  | The block's ground may have shifted (platform rule, regulation, now standard) | `When the archive goes stale` |
  | History shows repeated "no difference" on one page | `Local-maximum risk` |

## Stage map

Files under `${CLAUDE_PLUGIN_ROOT}/knowledge/scenarios/`; at most two per turn.

| Page or flow | Stage files |
|---|---|
| Homepage, landing, campaign page; on mobile web also the app download banner, the returning-visitor homepage and the recently viewed strip | `home-landing.md` |
| Search, filters, results; menu and navigation | `search-filtering.md` |
| Category or listing; a mobile-web exit-intent pop-up | `category-listing.md` |
| Product detail | `product-detail.md` |
| Cart, coupon, checkout, address | `cart-checkout.md` |
| Order confirmation, thank-you | `thank-you.md` |
| Logged-in, recurring-use home screen | `dashboard.md` |
| Form, signup, login | `forms-signup.md` |
| Pricing page, price display, plan comparison | `pricing.md` |
| App onboarding, permissions, app home (native app only; a mobile website goes by its page type) | `mobile-app.md` |
| SaaS commercial decisions (plan default, trial length, paywall) | `saas-b2b.md` |
| Finance, insurance, private pension (BES): product text, calculators, call-back and lead requests, offer steps, contract and contribution screens | `finance-pension.md` (every scenario needs compliance sign-off; disclosures, withdrawal, consent and identity steps are never the subject) |
| Buttons, links, icons on any page | `ui-elements.md` (a lower tier: not first while a stronger candidate exists) |
| Multi-product hub ("choose your product") | `category-listing.md` + `finance-pension.md` for finance lines, else `home-landing.md`; primary = completed quote or lead per assigned hub visitor, product clicks a diagnostic |
| Booking-style search form | `search-filtering.md` + `forms-signup.md`; primary = completed booking per assigned visitor, "search started" the guardrail when submissions can drop |
| Pre-quote insurance or credit form | `finance-pension.md` + `forms-signup.md` |
| App checkout / app paywall | `cart-checkout.md` + `mobile-app.md` / `saas-b2b.md` + `mobile-app.md` |
| SaaS web onboarding; account or settings; order tracking; help or blog | `saas-b2b.md` + `forms-signup.md`; `dashboard.md` + `forms-signup.md`; `thank-you.md` + `dashboard.md`; `home-landing.md` + `search-filtering.md` |

A form's own design lives only in `forms-signup.md`. Subscription cancellation is legally bound: the regulation gate comes first. Cookie consent and other consent requests are out of scope on purpose (`FORMAT.md`): never suggested, and a scenario next to a consent step leaves it identical in both arms. A page type without a row: one line naming the stages it was mapped to.

## Flow

1. **Context.** Sector, page and stated problem come from the router or the request. No page shared and the request doesn't say what is sold or how it is sold: the turn's one question (rule 19, kind 4) asks it as a short multiple choice fitted to the page type ("Ne satıyorsun: (a) abonelik, (b) tek seferlik ürün, (c) teklif ya da başvuru, (d) başka?"), after the scenarios, never before them; the answer re-selects for that model in the next turn. Unanswered or outranked by a higher kind, the scenarios still stand, with the generic-picks line under Output. A direct `/ab-test-suggest` that describes a page stays here: A is the stated state (rule 15), the mechanism gate uses the page version (an obstacle observable there) and `card.mockup_basis` is `described` (`shared_page` for a screenshot). Traffic, tool, setup and the brand are never asked (rules 5, 12, 13); a baseline rate and visitors the user gave go through `feasibility.py` once, routed by its verdict as `Traffic feasibility` says ("not testable": no cards, the alternatives line). Unclear sector or page → the closest stage, said in one line.
2. **History first (rule 16).** Look for `.abtest-history.md` and `.abtest-backlog.md`; run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_input.py <the files that exist>` before reading them, and on any file the user hands over (rule 18). Pull the rows for this page; a queued backlog row is surfaced, not re-suggested. No file → the reminder line, only when the user mentions past tests or a variable may already have been tested.
3. **Retrieve** (Reading budget), candidates acting on the stated problem first. With a named loss point, separate a clogged vein (a busy step that converts poorly: improve it) from a missing link (a step the funnel lacks: add it).
4. **Select.**
   - **Mechanism gate, page-type version:** the obstacle typical for this page type ("on a cart page an open coupon field sends code-less shoppers off to hunt for a code"), stated in `problem` as an assumption to check. A generic reason fails.
   - **Fit, never force-fit:** use a block only when its obstacle plausibly exists in the user's context (its `sektör`, and `pazar=TR` only for a Turkish market or with its market note); a `durum=klasik` block only when the user names it; when none fits but a strong idea does, generate it. Two candidates on one mechanism are one idea: keep the stronger.
   - **Diversity:** among the playbook's own picks, at most one per element-level `düzey` (two `metin` blocks are one slot, the stronger kept); structural levels are not capped. Explicit asks are exempt.
   - **History:** state a recorded outcome as the tool reported it. Won → the next step building on it; lost or no difference → retry only with a stated reason, otherwise one line saying it was left out; inconclusive → suggest, noting the run; a pattern that won on the user's product sets `evidence.level: user_data`.
   - **Order and cap** (rule 9): the tier is the band of the five `priority.inputs` (`Prioritization`), set honestly (`effort` from the block's `emek`, `impact` from its level and the impact ranking); the user's explicit asks first, in the order asked, always produced, weak or not; then the playbook's own candidates by priority, problem-acting first, ties as in `Prioritization`; at most three strong, never padded; more → the top three, the strongest left out named in one line, and the count for the offer.
   - **Gates:** regulation (rule 11: hold (a) with its "once X is confirmed, test Y" line, produce (b) with its warning), accessibility (rule 3), market (rule 11), sensitive fields (rule 14), protections and dark patterns (rule 6); a stale block is flagged or left out. An unverified fact the idea needs → a critical assumption (rule 10), not a drop and not an invented fact.
5. **Write each record once,** from the skeleton (`record-checklist.md`), localized to the user's sector (a clothing example on a fashion site). `source` is `archive`, `adapted` or `generated`; `problem` is the typical obstacle as an assumption; `is_current: true` only for the user's own page kept here in step 1, else omitted.
6. **Deliver** through `ab-test-card` → Delivery pipeline (fast mode, rule 17: its Fast mode); each `[fixable]` line is applied as written, no re-call. The critic gets, in one call: the record files, the page context (page type plus the step 4 assumption), the history rows, the explicit asks, the whole planned chat (each scenario block, "Stronger alternative:" lines included, and every line after the list) and the reasons for standing validator warnings. `card.mockup_basis` is `representative` unless step 1 set it; neutral palette unless a screenshot gives colors.
7. **Backlog (rule 16).** Offer once to append the ranked candidates, strong ones beyond the top three included, to `.abtest-backlog.md` (format `${CLAUDE_PLUGIN_ROOT}/templates/abtest-backlog.md`, tier in `Öncelik`); append only after the user confirms, else show the rows. It is rule 19's kind 9.

## Output

Per scenario, exactly the lines `validate_scenario_json.py --chat` printed (`ab-test-card` → Delivery pipeline, step 1: the title, the tag line with the score, `Neden:`, `Doğru olmalı:`, `Önce yokla:`), then the file, `abtest-card-<slug>.html`; nothing else per scenario. You write only what `--chat` can't: a `Neden:` / `Why:` line when its stderr says the mechanism runs over 140 characters (plain words, no number or claim, rule 10) and, under a weak explicit ask, after `Neden:`, "Daha güçlü alternatif: <the better test>; <why this one is weak>." / "Stronger alternative: …". `must_be_true` holds what must hold in the user's context (`record-checklist.md` → Field by field).

After the list, one line each, in this order, each only when it applies except the first:

- the `Başlamadan önce:` line as `--chat` printed it (pre-start gates, once for the set; always, `yok` when none)
- the `Koşullu (<n>):` line as `--chat` printed it (rule 10; every critical assumption by scenario number, as a fact to verify), asked as rule 19 says: the most critical, or with two or more open and no higher kind the line itself as a numbered list ("Koşullu (2), teyit eder misin: 1) 1 için …; 2) 3 için …?")
- siblings on one screen, flow or decision: `Sıra: 1 → 2 → 3, aynı kullanıcılarda üst üste binmeden. 1 kazanırsa sıradaki <next, built on B>; kaybederse <next>.` (EN `Order: 1 → 2 → 3, never on the same users at once. If 1 wins, next <…>; if it loses, next <…>.`)
- the strongest candidate left out of the top three: `Sıralamada kalan güçlü aday: <title>.` / `Also strong, not in the top three: <title>.`
- the primary differs from a metric the user named: one short clause, no general rule ("RPV burada daha uygun: kupon alanı geliri de etkiler.")
- a held candidate as a path: `Bekletilen: <idea>; <X> teyit edilince test: <Y>.` / `Held: <idea>; once <X> is confirmed, test <Y>.`
- a tested variable retried or left out, with its recorded outcome
- no page shared: "Bunlar arşivden genel seçimler; sayfanı ya da ekran görüntünü paylaşırsan sayfana özel üretirim." / "These are generic archive picks; share your page or a screenshot and I will design for it."
- representative or described mockups, only when the user could take them for their own page: "Kartlar anlatımından çizildi; ayrıntılar temsilî."
- the user asked for suggestions beyond their own ideas and no other candidate passed the bar: "Bu sayfa için başka güçlü aday bulamadım."
- the history reminder, only when the user mentions past tests or a variable may already have been tested ("Geçmiş test sonuçlarını `.abtest-history.md` olarak tutarsan önerileri onlara göre süzerim.")

Then the two `feasibility.py` lines as printed, only when the user gave the numbers; the stakeholder brief for scenario 1 only, as `--chat` printed it (why now and the three outcome lines; a file only when asked: `${CLAUDE_PLUGIN_ROOT}/templates/stakeholder-brief.md`, read then), with more scenarios followed by one line: "2 ve 3 için karar özetini istersen yazarım." / "Ask and I will write the brief for 2 and 3."; then at most one question, one sentence (rule 19): step 1's context question when it applies, else e.g. "2 güçlü aday daha var, devam edeyim mi?" No line about colors or the brand (rule 12), no review or elimination text.

## Detail on request

"detay", "neden bu", "üç kutuyu göster", "explain scenario 2", "full version": `methodology.md` → Detail on request, read then (fill `detail` for that one record, validate it, send it to scenario-critic again, the card stays as it is; in chat the three boxes and the reasons). Why a candidate was left out, and what the critic found, are given the same way, only when asked.

## Never do

- Read a whole archive file, the whole glossary, or a methodology section no decision needs.
- Repeat the record in chat beyond its scenario lines, or regenerate the three boxes unasked (rule 9).
- Produce more than three without the offer, pad with a weak candidate, or drop a test the user asked for (rule 9).
- Force-fit an archive scenario, or present two proposals on one mechanism.
- Skip the regulation gate or a market or accessibility warning (rules 3, 11).
- List titles and ask "which one should I expand" (rule 13).
