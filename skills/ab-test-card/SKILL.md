---
name: ab-test-card
description: 'Render an A/B test scenario record as a single-file 16:9 HTML card that shows only the comparison (the test''s question-form title above a large Variant A/B mockup pair, the changed element ringed and labelled) and nothing else. Use when the user says "make a card for this test", "turn this into a card", "visualise this test", "render this scenario", "make a slide out of this", "show me the two variants side by side", "kart yap", "görselleştir", "slayt formatına çevir", "bunu karta bas". Runs automatically for every scenario produced by ab-test-suggest and ab-test-design (CLAUDE.md rule 9), so it rarely needs to be invoked directly. Output is self-contained HTML with no external assets, built deterministically by scripts/build_card.py from the scenario''s own JSON and delivered only after scenario-critic and mockup-reviewer pass.'
metadata:
  version: 3.3.0
  category: render
  updated: 2026-11-14
---

# ab-test-card: Scenario Card Rendering

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` is binding. This skill holds what `ab-test-suggest` and `ab-test-design` share: how a record is written, how its card is drawn and the Delivery pipeline. It runs for every scenario they produce (rule 9) and when the user says "make a card". Schema `${CLAUDE_PLUGIN_ROOT}/templates/scenario.schema.json`; worked example `${CLAUDE_PLUGIN_ROOT}/examples/scenario.json`; template `${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html` (its developer comment has a markup example for every `.r-*` component).

## Reading

Every card: the core of `mockup-style.md` (The card, Frames, Ring and label, Realism level, Personal data is never copied, Numbers the mockup needs but must not invent), which is everything above its `# On demand` heading:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/read_section.py ${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md --until "On demand"
```

On demand, one section by name: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/read_section.py ${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md "<title>"`

| When | Section |
|---|---|
| Markup beyond a header, fields, buttons and text (tabs, chips, plan card, product grid, popup, badges, price lines) | `Components` |
| A stepper, the fold or a pinned bar (`.r-fold`, `.r-sticky`), a move to another step (stages), a consequence to soft-ring (`.hl-soft`), a carousel, a text button, a modal, a photo hero | `Special cases` |
| `card.brand` from a screenshot or a brand guide | `Brand` |
| A ribbon or build question | `Draft and final card` |
| A `render_check.mjs` error or warning to fix | `render_check` |

## The record

One JSON file per scenario, written once by the producing skill; `card` may be written with it (it is outside the critic's fingerprint), but the draft build needs the critic stamp:

```json
{
  "id": "<stage>-<slug>-01", "title": "<short question?>", "lang": "tr", "stage": "<stage>", "device": "phone|phone-web|web",
  "problem": "<one sentence>", "mechanism": "<one sentence resting on the problem>",
  "variable": "<noun phrase>", "difference": "change|add|move|remove",
  "variants": [{"id": "A", "description": "<control>", "is_current": true}, {"id": "B", "description": "<the one change>"}],
  "primary_kpi": {"name": "<canonical name>", "denominator": "<same in both arms>", "direction": "increase|decrease"},
  "guardrail": {"name": "<independent harm>", "kind": "metric", "denominator": "<same in both arms>", "direction": "must_not_increase|must_not_decrease"},
  "source": "archive|adapted|generated", "adapted_from": "<exact archive title>", "source_note": "<generated only>",
  "evidence": {"level": "user_data|archive|sector|intuition", "note": "<what it rests on; why it's low-confidence when it is>"},
  "priority": {"tier": "<the band of the inputs' score>", "rationale": "<one sentence: what the inputs rest on>",
               "inputs": {"evidence": "user_data|behaviour_data|archive_or_research|intuition", "impact": "structural|persuasive|cosmetic", "main_path": true, "noticeable": true, "effort": "low|medium|high"}},
  "exposure": "<the trigger, logged at the same point in both arms; required for an accordion, modal, tab or below-the-fold element>",
  "objection": "<Güven|Fiyat|Uygunluk|Zamanlama|Çaba|Netlik, or Trust|Price|Fit|Timing|Effort|Clarity>",
  "warnings": [{"type": "regulation|accessibility|market|feasibility|privacy", "text": "<one sentence>"}],
  "invariants": ["<a function that works identically in both arms>"],
  "assumptions": [{"type": "critical", "text": "<one sentence, at most 200 characters>", "question": "<one short question>"}]
}
```

### Before the first validation

Nearly every first-validation refusal is one of these. Write each right the first time, then validate every record of the turn in one call: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_scenario_json.py <record.json> [more.json]`.

1. **KPI name and denominator are one family.** The glossary row's Payda is the denominator: `{"name": "Dönüşüm Oranı (CR)", "denominator": "Teste atanan ziyaretçi"}`; a session metric counts sessions (`"Hemen Çıkma Oranı"` over `"Sayfayla başlayan oturum"`). Never a count ("Sayısı"), "gören/görüp" or an audience only B has.
2. **An interactive element needs the accessibility warning.** B adds or changes a link, button, field, checkbox, chip, tab, toggle, accordion, menu, modal or carousel → one `accessibility` warning naming all four criteria with their figures: "B yayına girmeden klavye ve ekran okuyucu kontrolünden geçmeli: yeni bağlantı klavyeyle erişilir, ekran okuyucuda görünen adıyla okunur, dokunma alanı en az 44×44 pt, metin kontrastı en az 4.5:1 olur." A modal or pop-up adds focus on open, a visible close control and Esc; an auto-advancing carousel adds a pause.
3. **A conditionally shown element needs `exposure`.** Accordion, tab, modal, pop-up, dropdown, drawer, tooltip or below the fold → who is exposed, with the words "iki kolda" / "both arms": `"exposure": "Kargo akordeonunun başlığı ekrana gelen kullanıcılar; tetikleyici iki kolda aynı noktada kaydedilir."`
4. **A functional element needs `invariants`.** B touches a coupon, discount, payment, cart, filter, search, login, signup or form → 1 to 5 sentences: `["Geçerli bir kod iki kolda da aynı adımla uygulanır."]`
5. **`adapted_from` is the archive's `## ` title, whole.** Same words and case (straight or curly quotes both match), and `difference` is the block's `Fark:` (değiştir → `change`, ekle → `add`, taşı → `move`, kaldır → `remove`); `archive` also keeps its `Değişken:` as `variable`.
6. **`priority.inputs` has all five, and the tier is the band of their score out of 9.** evidence (`user_data` 3, `behaviour_data` 2, `archive_or_research` 1, `intuition` 0) + impact (`structural` 2, `persuasive` 1, `cosmetic` 0) + `main_path` 1 + `noticeable` 1 + effort (`low` 2, `medium` 1, `high` 0): 7-9 `high`, 4-6 `medium`, 0-3 `low`; `medium` at most with a critical assumption. A native app release alone is `medium` effort; `high` is backend or operational work. `inputs.evidence` follows `evidence.level`: `user_data` → `user_data` or `behaviour_data`; `archive` and `sector` → `archive_or_research`; `intuition` → `intuition`.
7. **`card.change` is one op on an `id` the screen has:** `insert_after`, `insert_before`, `replace`, `remove`, `move_after`, `move_before` or `edit`, each with its ring `label`; a move names both places: `{"op": "move_before", "target": "kupon", "to": "ozet", "label_a": "Kupon altta", "label_b": "Kupon üstte"}`.
8. **Screen nodes keep their shapes.** One kind per node. `{"fold": true}`, `{"stage": true}`, `{"divider": true}` take `true` and nothing else; `align` (`"center"` / `"left"`) only on `text`; a `plan` has `name` and `price` as strings: `{"plan": {"name": "Pro", "price": "499 TL", "per": "/ay", "features": ["Sınırsız proje"], "cta": "Başla"}}`; `sticky` only on a screen with a `fold`, placed before it; colours `#rrggbb`, sizes whole numbers.
9. **Nothing differs outside the ring.** Copy, numbers, order and spacing are the same in both arms; a number that differs on purpose carries `numeric_change`, saying where the figure comes from; a consequence the variable forces goes in `card.soft`.
10. **Plain JSON.** Straight `"` around keys and values (curly quotes only inside the text), no trailing comma, no comment.

- **Source (rule 8).** `archive`: the block as written, examples localized; `adapted`: the block's variable and difference type kept, fitted to the user's context; either half changed → `generated`, with `source_note` saying why no block fits and how this differs. `is_current: true` only when A is the user's own current page (a screenshot, URL or their own described page), else omitted. `device` picks the frame (default `phone`; a website the user calls "mobile" is `phone-web`, `phone` only for a native app).
- **Primary KPI (rule 2).** The outcome the title names, at the closest point it is still an outcome (a completed order, not a click), with the canonical name and denominator from the glossary grep: assigned users of each arm, or a trigger logged in both arms before the change renders. An archive block's KPIs are starting points: its first KPI and strongest must-not item stay only where they fit the title and the denominator rule (a coupon test keeps RPV primary until the user states another business goal; a per-quote "Teklif → Sözleşme" → "Sözleşme Oranı (30 gün)" per assigned visitor). A window in the name ("Kayıt Oranı (7 gün)") is part of its definition; the denominator names the event it counts from, one both arms share (assignment, first open). A change to what is charged (a price, a discount amount, a bundle) takes a revenue-based primary.
- **Guardrail (rule 3).** A harm that can worsen while the primary improves; a lagging harm carries its window in the name; a legal or product window is named by its definition ("Cayma Oranı (yasal cayma süresi içinde)"), never guessed. A functional protection that matters more is `{"kind": "check", "criterion": "…"}`. When B touches a user benefit (a coupon, a discount, free shipping, refunds), the guardrail watches the benefit: hiding a coupon field can raise revenue because code holders pay full price. Coupon: "Kuponlu Sipariş Veren Ziyaretçi Oranı" per assigned visitor, plus the functional pass criterion in `invariants` (a valid code is entered, applied and discounted, and errors are handled, identically in both arms).
- **Invariants (rule 4).** When B touches a link, field, coupon, payment, search, filter or form: 1 to 5 checkable sentences (item 4: same step, same totals, same error message); otherwise omit. `numeric_change` only when a number differs on purpose (a price test, or an amount computed from the page, such as the sum left to free shipping), saying why.
- **Warnings.** Only when one applies, at most three, one sentence each: `accessibility` with rule 3's criteria for the element (item 2); `regulation` for rule 11 (b) ("Compliance must approve B's exact copy before the test takes traffic."); `market`, `feasibility`, `privacy` naming the dependency.
- **Assumptions (rule 10).** At most three. `critical` (with `question`) when feasibility, legality or the single variable rests on a fact the user didn't give: write it instead of inventing the fact or dropping a strong idea; the tier is then medium at most and the rationale says what it waits for. `visual` (no question) for representative names, photos and decoration; usually omitted.
- **Evidence and priority (rules 9, 10).** `evidence.note` says what the record rests on and, for `intuition` or `sector`, why it's low-confidence; a source the user named goes in the note. No refused claim anywhere in the record. The tier is the band of the inputs' score (item 6; `methodology.md` → Prioritization), the validator recomputes it; `impact` is the change's tier in the impact ranking (the offer, a step or missing decision information `structural`; hierarchy, objection copy or a trust signal `persuasive`; colour, radius, font or generic wording `cosmetic`); `effort` is high for backend or operational work, medium for front-end work or a native app release.

## The card object

| Field | What goes in it |
|---|---|
| `card.screen` + `card.change` (+ `card.soft`) | The default way to draw. `screen` describes the page once as a node list (kinds and overrides: `mockup-style.md` → Screen spec); `change` is exactly one op (`insert_after`, `insert_before`, `replace`, `remove`, `move_after`, `move_before`, `edit`) with its target `id` and ring `label`. The builder compiles both arms from them, so A and B cannot differ anywhere else. Records on one shared screen carry the same `screen` list; `soft` names up to two node ids for `.hl-soft`. |
| `card.variant_a` / `card.variant_b` | Raw markup for the special case the node list can't express: the mockup bodies as HTML from the template's `.r-*` components at their rendered size, `variant_a` byte for byte the same across a shared screen, each `variant_b` that A with its one change. Never alongside `screen`/`change`: the build refuses both forms at once. |
| `card.difference` | Normally left out. If set, it must name the record's `difference` (`değiştir` / `ekle` / `taşı` / `kaldır` spell the same four); the build refuses a mismatch. |
| `card.url` | Address bar (`web`) or mobile address bar domain (`phone-web`); required on both. With no user-given URL, a `.example` domain (`magaza.example/sepet`); a user-given URL stays. |
| `card.bottom_nav`, `card.bottom_nav_active` | `phone` (native app) only: the real app's tab labels and the active one (label or 0-based index). Otherwise omitted: no tab bar is drawn. |
| `card.brand` | `{"primary": "#c9392b", "on_primary": "#fff", "name": "Brand"}` from a shared screen (or a shared URL, visited when a browser tool is available) or a guide, silently (rule 12); omitted → neutral palette. Brand name as text, never a logo file. |
| `card.mockup_basis` | Never printed: `shared_page` (a redraw of the screenshot or URL), `described` (rebuilt from words), `representative` (no page). |
| `card.note_pos`, `card.phone_scale`, `card.web_scale`, `card.device` | Where you would like the labels, `above` (default) or `below`; the builder keeps it when the label is clear there. The scale fields are optional: the builder picks the frame's scale from the content (leave them out; `1`, `1.2` or `1.4` overrides). A frame override of `device`. |
| `card.mobile_toolbar`, `card.stage_captions` | `phone-web` only: `true` draws the browser's bottom toolbar, identical in both arms. One short caption per stage when the screens use `.r-stage-break` (count = breaks + 1, same in both arms). |

`device`: `phone` = native app screen; `phone-web` = page in a mobile browser (status bar, address bar, no tab bar); `web` = desktop browser. Text fields are plain text, never pre-escaped (the script escapes them). A record the user brings as text is mapped as given, `source: generated` with a `source_note` saying the user brought it, `evidence.level` as the user stated (`intuition` if nothing), no invented `objection`; a missing required piece routes to `ab-test-design`, one sentence saying what was missing.

## Drawing

- **Realistic, from the page's own parts.** Real copy, prices, labels and layout, no filler; `.r-*` components at component scale, no invented markup, inline colors or `zoom`/`transform`; `.ph` only for a photo. An element B adds uses the styles A's screen already has: no new color, icon or emphasis, never the brand color on text unless color is the variable.
- **The region the test is about,** with enough context to read it; a frame is as tall as its content. Clipped content and a blank phone screen are render_check errors.
- **A shared page is redrawn, not invented** (rule 15): A is exactly the on-screen state; an unreadable detail is left out or asked (rule 19). To fit the frame, decoration and repeated rows may be left out, the same in both arms; never anything the test, its KPI or a warning is about. Personal data and figures follow the core sections read above.
- **Rings by difference type:** `change` → B (A optional); `add` → B only; `move` → both arms, the same element with identical content at its old place in A and its new place in B, each arm's label true for that arm ("Telefon ilk adımda" / "Telefon teklif sonrasında"); `remove` → A only, the label naming the removal, B genuinely empty (no placeholder). One change on N repeated elements → one ring around the group; a linked difference the variable forces is named by the label. A ring label is two to four words, Turkish starting with a capital. `.hl` takes no space: no `style`, margin, padding, border or background on it or a wrapper; move the label with `data-pos="below"` or `card.note_pos`.
- **A move below the fold, to a pinned bar or to another step is still a move,** never remove plus add: both arms carry the same `.r-fold` (B's pinned element in an `.r-sticky` at the bottom of the first view, A's at the end of the continuation) or the same stages (`.r-stage-break`), and the ring sits at the element's old place in A and its new place in B (`Special cases` has the markup). A consequence the variable forces gets `.hl-soft`, not a wider ring. No text beyond page copy, stage captions and ring labels, and no unverified value drawn as settled text.
- Everything outside the rings is identical in both arms; the build refuses any other difference and any numeric one without `numeric_change`.

## Delivery pipeline

Binding for every card (rules 4, 9, 10, 17); `ab-test-suggest` and `ab-test-design` point here. One reviewer call per stage covers all of the turn's records or cards. Every command below runs in the main session, never through a subagent (rule 17), copied as one line.

1. **Validate** every record of the turn in one call: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_scenario_json.py <a.json> <b.json> <c.json>` (Turkish messages by default; `--lang en` for an English record). An error stops: fix and rerun. A warning is fixed, or its reason goes to the critic.
2. **Scenario review, one round.** `agents/scenario-critic` gets every record file and what the producing skill lists. Per record it returns `PASS` with the stamp JSON `build_card.py --critic-stamp` printed, alone or with `[fixable]` lines, or `FIX` (at least one `[blocking]` line) or `RET`.
3. **Critic stamp and fixes.** Write the stamp exactly as returned, `"review": {"scenario_critic": {"verdict": "PASS", "fingerprint": "<hex>"}}`; then apply every `[fixable]` line as written (only rule 17's small-fix fields, so the stamp stays valid) and every `chat:` line, and rerun step 1 on the changed records. No re-call. A `FIX` is reworked and goes back through steps 1 and 2 (Loops).
4. **Draft.** With `card` in the record (added now if it wasn't written with it): `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py --draft --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html --scenario <record.json> --out abtest-card-<slug>.draft.html`. It refuses without a matching critic stamp, compiles `card.screen` + `card.change` into the two arms when the record uses them, runs the card checks, writes the draft and its manifest (`<out>.manifest.json`) and prints their paths with the `--stamp` command the reviewer runs on PASS. The draft carries no fingerprint. A record with a critical assumption builds a koşullu kart (conditional card), never a final one: ribbon "KOŞULLU · doğrulama gerekli" / "CONDITIONAL · needs verification", summary "conditional card (not implementation-ready)". Then `node ${CLAUDE_PLUGIN_ROOT}/scripts/render_check.mjs --strict --shot --half <draft.html>` measures it (Node.js 18 or newer with Playwright and Chromium, installed once outside any project: `npm i --prefix ~/.abtest-visual playwright && npx --prefix ~/.abtest-visual playwright install chromium`; render_check finds it there on its own) and saves the full- and half-size PNGs. Exit 0 `VERIFIED` → review; 1 `VISUAL_CHECK_FAILED` → fix every error, rebuild, rerun; 2 usage error → fix the command; 3 `VISUAL_CHECK_UNAVAILABLE` → nothing was measured: the reviewer's verdict is `UNVERIFIED`, never PASS, so no card becomes final (step 8). Look at the PNG yourself.
5. **Mockup review.** `agents/mockup-reviewer` gets every draft with its manifest, its record, the render_check output and PNG (or a line that it couldn't run) and, for a shared page, the screenshot path or an element inventory (personal values left out). It judges what the drawing means (variable shown, labels true, ring tight, neutral A/B, nothing unverified as fact), not only what render_check measures. On PASS the reviewer runs `build_card.py --template … --scenario <record> --stamp <draft.html>` (it writes nothing and refuses a draft or manifest the record no longer builds) and returns the JSON line it prints.
6. **Mockup stamp.** The JSON line the reviewer returned, `{"verdict": "PASS", "fingerprint": "<hex>"}`, into `review.mockup_reviewer`, exactly as printed.
7. **Final or conditional build** in the user's working directory: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html --scenario <record.json> --out abtest-card-<slug>.html`. It writes only when both stamps match; on refusal nothing is written and an existing file stays. It also writes the card's image, `card-<name>.png`, next to the card and prints its path (`--no-png` skips it; without Node or Playwright it says so in one line and still succeeds). It prints the final card's fingerprint; `build_card.py --template … --scenario <record> --check <card.html>` later confirms that a delivered file is byte for byte that reviewed card.
8. **Deliver** only that card, a conditional one named "koşullu kart" in chat, never final. Drafts and manifests are working files, never delivered or linked, with two exceptions (rule 9): fast mode's quick drafts (below), and when the visual check was unavailable (exit 3, verdict `UNVERIFIED`), give the draft as a preview labelled UNVERIFIED in chat, never called final (its ribbon says "Önizleme · görsel kontrol yapılmadı" / "Preview · not visually checked"). The chat line that goes with it is calm and says three things once per turn, in the user's language, and nothing more: what this is, that it has not been visually checked yet, and the one-time command that gets checked cards from now on. EN: "This is a preview of your card (UNVERIFIED): the test plan is reviewed, but the drawing has not been visually checked yet, because the visual check is not installed on this computer. To get fully checked cards from now on, run this once in a terminal: `npm i --prefix ~/.abtest-visual playwright && npx --prefix ~/.abtest-visual playwright install chromium`. Then tell me and I will check and finish this same card." TR: "Bu, kartınızın bir önizlemesi (UNVERIFIED): test planı incelendi, ama çizim henüz görsel olarak kontrol edilmedi, çünkü görsel kontrol bu bilgisayarda kurulu değil. Bundan sonra tam kontrol edilmiş kart almak için terminalde bir kez şunu çalıştırın: `npm i --prefix ~/.abtest-visual playwright && npx --prefix ~/.abtest-visual playwright install chromium`. Sonra bana haber verin, aynı kartı kontrol edip tamamlayayım." No "error", "failed" or "warning" wording: nothing broke, one check is pending. Where nothing can be installed (no terminal, a hosted chat), leave the command out and say the visual check is not available in this environment. Once it is installed the same draft is checked and finished from step 4. The final build still refuses without a mockup PASS stamp (code); that no PASS is given without a render is a review rule (process).

**Loops.** Critic `FIX` → rework its `[blocking]` lines (a fix needing a fact the user didn't give becomes a critical assumption), back to step 1 and a re-call with the previous report. Mockup FIX `route: render` → fix only the mockup, `card.*` or the title's wording (a small-fix field: the critic stamp stays), rebuild the draft, resend; `route: scenario-critic` → back to step 1. At most two re-calls per reviewer; `RET`, or still FIX → not delivered, one sentence to the user. **Confirmed assumption:** remove it from `assumptions` (a covered change: the critic stamp no longer matches), back to step 1; the new final card carries no ribbon.

**Never** write a stamp without a PASS or with a fingerprint not printed by the scripts, run `--critic-stamp` or `--stamp` yourself, edit a draft into a final, or work around a refusal: it names the failed gate or field; fix the input.

## Fast mode

Rule 17's exception, only when the user asks for it (`ab-test` → routing table). The producing skill writes the same records and the same chat; the pipeline is shorter:

1. Step 1 as above, every record in one call.
2. No critic, render_check or mockup reviewer. One quick draft per record: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py --quick --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html --scenario <record.json> --out abtest-card-<slug>.draft.html`. It needs no stamp and writes no manifest; the card checks still run; its ribbon says "Hızlı taslak · incelenmedi" / "Quick draft · not reviewed"; `--stamp` refuses it and it never becomes final.
3. Deliver with the skill's Output, the `.draft.html` files as the file names, plus one line after the list, a statement, not the turn's question: TR "Hızlı taslak: kartlar ve kayıtlar henüz incelenmedi. “Tamamla” dersen iki incelemeyi yapıp nihai kartları hazırlarım." EN "Quick drafts: the cards and records are not reviewed yet. Say “finish” and I will run both reviews and build the final cards." Nothing calls a quick draft final, checked or reviewed.

**Finish** ("tamamla", "finish"): the same records from step 2 of the Delivery pipeline (one critic round over all of them, drafts, render_check, the mockup reviewer, final or conditional builds); each reviewed draft replaces its quick draft at the same path. The chat gives the usual Output for the reviewed cards; a record the critic changed in substance or dropped gets one line.

## Never do

- Put any record text but the title on the card (no description, boxes, tags, notes, footer), or render a card for a record the validator refuses (rule 9).
- Render a dark-pattern scenario, even on "make the card" (rule 6).
- Escape text fields by hand (`&lt;` shows up as `&amp;lt;`); but escape `<`, `>`, `&` yourself in user text placed inside `variant_a` / `variant_b`.
- Use markup outside the allowlist: only the template's component tags (`div span p b strong i em u s small sup sub br hr ul ol li`) and `class`, `style`, `data-note`, `data-pos`, `title`, `role`, `aria-*`, double-quoted; no comments, links, images, scripts, event handlers, `url(`, `@import` or `position:fixed` (rule 18). A build warning (`build_card: warning: …`) is read, not ignored.
- Put a second difference in the mockups, or a "hidden / removed" placeholder where a removed element was.
- Draw a tab bar on a page that isn't a native app screen, or copy personal data from a screenshot (rule 15).
- Color elements with inline `style` instead of `card.brand`, add an external font or CDN link, pull a logo from a URL, or ask about or note the brand (rule 12).
- Render in a language other than the user's (rule 7); a Turkish card sets `lang: "tr"` and uses curly quotes.
