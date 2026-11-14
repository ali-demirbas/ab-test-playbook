---
name: ab-test-card
description: Render an A/B test scenario record as a single-file 16:9 HTML card that shows only the comparison (the test's question-form title above a large Variant A/B mockup pair, the changed element ringed and labelled) and nothing else. Use when the user says "make a card for this test", "turn this into a card", "visualise this test", "render this scenario", "make a slide out of this", "show me the two variants side by side", "kart yap", "görselleştir", "slayt formatına çevir", "bunu karta bas". Runs automatically for every scenario produced by ab-test-suggest and ab-test-design (CLAUDE.md rule 9), so it rarely needs to be invoked directly. Output is self-contained HTML with no external assets, built deterministically by scripts/build_card.py from the scenario's own JSON and delivered only after scenario-critic and mockup-reviewer pass.
metadata:
  version: 3.2.0
  category: render
  updated: 2026-11-10
---

# ab-test-card: Scenario Card Rendering

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` is binding. This skill holds what `ab-test-suggest` and `ab-test-design` share: how a record is written, how its card is drawn and the Delivery pipeline. It runs for every scenario they produce (rule 9) and when the user says "make a card". Schema `${CLAUDE_PLUGIN_ROOT}/templates/scenario.schema.json`; worked example `${CLAUDE_PLUGIN_ROOT}/examples/scenario.json`; template `${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html` (its developer comment has a markup example for every `.r-*` component).

## Reading

Every card: the core of `mockup-style.md` (The card, Frames, Ring and label, Realism level, Personal data is never copied, Numbers the mockup needs but must not invent), which is everything above its `# On demand` heading:

```bash
awk '/^# On demand/{exit} 1' ${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md
```

On demand, one section by name: `awk -v h='## <title>' 'index($0,h)==1{p=1;print;next} p&&/^##? /{exit} p' ${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md`

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
               "inputs": {"evidence": "user_data|behaviour_data|archive_or_research|intuition", "main_path": true, "noticeable": true, "effort": "low|medium|high"}},
  "exposure": "<the trigger, logged at the same point in both arms; required for an accordion, modal, tab or below-the-fold element>",
  "objection": "<Güven|Fiyat|Uygunluk|Zamanlama|Çaba|Netlik, or Trust|Price|Fit|Timing|Effort|Clarity>",
  "warnings": [{"type": "regulation|accessibility|market|feasibility|privacy", "text": "<one sentence>"}],
  "invariants": ["<a function that works identically in both arms>"],
  "assumptions": [{"type": "critical", "text": "<one sentence, at most 200 characters>", "question": "<one short question>"}]
}
```

- **Source (rule 8).** `archive`: the block as written, examples localized; `adapted`: the block's variable and difference type kept, fitted to the user's context; either half changed → `generated`, with `source_note` saying why no block fits and how this differs. `adapted_from` is the block's exact title. `is_current: true` only when A is the user's own current page (a screenshot, URL or their own described page), else omitted. `device` picks the frame (default `phone`; a website the user calls "mobile" is `phone-web`, `phone` only for a native app).
- **Primary KPI (rule 2).** The outcome the title names, at the closest point it is still an outcome (a completed order, not a click), with the canonical name and denominator from the glossary grep: assigned users of each arm, or a trigger logged in both arms before the change renders. An archive block's KPIs are starting points: its first KPI and strongest must-not item stay only where they fit the title and the denominator rule (a coupon test keeps RPV primary until the user states another business goal; a per-quote "Teklif → Sözleşme" → "Sözleşme Oranı (30 gün)" per assigned visitor). A window in the name ("Kayıt Oranı (7 gün)") is part of its definition; the denominator names the event it counts from, one both arms share (assignment, first open). A change to what is charged (a price, a discount amount, a bundle) takes a revenue-based primary.
- **Guardrail (rule 3).** A harm that can worsen while the primary improves; a lagging harm carries its window in the name; a legal or product window is named by its definition ("Cayma Oranı (yasal cayma süresi içinde)"), never guessed. A functional protection that matters more is `{"kind": "check", "criterion": "…"}`. When B touches a user benefit (a coupon, a discount, free shipping, refunds), the guardrail watches the benefit: hiding a coupon field can raise revenue because code holders pay full price. Coupon: "Kuponlu Sipariş Veren Ziyaretçi Oranı" per assigned visitor, plus the functional pass criterion in `invariants` (a valid code is entered, applied and discounted, and errors are handled, identically in both arms).
- **Invariants (rule 4).** When B touches a link, field, coupon, payment, search, filter or form: 1 to 5 checkable sentences (the code applies in the same step, totals are calculated the same way, an invalid code gets the same message); otherwise omit. `numeric_change` only when a number differs on purpose (a price test, or an amount computed from the page, such as the sum left to free shipping), saying why.
- **Warnings.** Only when one applies, at most three, one sentence each: `accessibility` with rule 3's criteria for the element ("Before launch B must pass a keyboard and screen-reader review: the new link is keyboard-reachable, announced by its visible text, moves focus to the field it opens, has a 44×44 pt target and 4.5:1 contrast."); `regulation` for rule 11 (b) ("Compliance must approve B's exact copy before the test takes traffic."); `market`, `feasibility`, `privacy` naming the dependency.
- **Assumptions (rule 10).** At most three. `critical` (with `question`) when feasibility, legality or the single variable rests on a fact the user didn't give: write it instead of inventing the fact or dropping a strong idea; the tier is then medium at most and the rationale says what it waits for. `visual` (no question) for representative names, photos and decoration; usually omitted.
- **Evidence and priority (rules 9, 10).** `evidence.note` says what the record rests on and, for `intuition` or `sector`, why it's low-confidence; a source the user named goes in the note. No refused claim anywhere in the record. The tier is the band of the inputs' score (6-7 high, 3-5 medium, 0-2 low; `methodology.md` → Prioritization), the validator recomputes it; `effort` is high for backend work, a native app release or an operational change.

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
| `card.note_pos`, `card.phone_scale`, `card.web_scale`, `card.device` | Labels `above` (default) or `below`; phone screen `1.2` (default), `1` for a tall screen the test needs whole, `1.4` for a short one; a short desktop page `1.2` or `1.4` (default `1`); a frame override of `device`. |
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

Binding for every card (rules 4, 9, 10, 17); `ab-test-suggest` and `ab-test-design` point here. One reviewer call per stage covers all of the turn's records or cards.

1. **Validate.** `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_scenario_json.py <scenario.json>` (Turkish messages by default; pass `--lang en` for an English record). An error stops: fix and rerun. A warning is fixed, or its reason goes to the critic.
2. **Scenario review.** `agents/scenario-critic` gets the record files and what the producing skill lists. PASS returns the fingerprint `validate_scenario_json.py --fingerprint` printed. FIX items come tagged `[blocking]` or `[fixable]`; round 1 lists every fixable gap.
3. **Critic stamp.** `"review": {"scenario_critic": {"verdict": "PASS", "fingerprint": "<hex>"}}`, exactly as returned.
4. **Draft.** With `card` in the record (added now if it wasn't written with it):

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py --draft \
     --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html \
     --scenario scenario.json --out abtest-card-<slug>.draft.html
   ```

   It refuses without a matching critic stamp, compiles `card.screen` + `card.change` into the two arms when the record uses them, runs the card checks, writes the draft and its manifest (`<out>.manifest.json`) and prints their paths with the `--stamp` command the reviewer runs on PASS. The draft carries no fingerprint. A record with a critical assumption builds a koşullu kart (conditional card), never a final one: ribbon "KOŞULLU · doğrulama gerekli" / "CONDITIONAL · needs verification", summary "conditional card (not implementation-ready)". Then `node ${CLAUDE_PLUGIN_ROOT}/scripts/render_check.mjs --strict --shot --half <draft.html>` (README → Visual check) measures it and saves the full- and half-size PNGs. Exit 0 `VERIFIED` → review; 1 `VISUAL_CHECK_FAILED` → fix every error, rebuild, rerun; 2 usage error → fix the command; 3 `VISUAL_CHECK_UNAVAILABLE` → nothing was measured: the reviewer's verdict is `UNVERIFIED`, never PASS, so no card becomes final (step 8). Look at the PNG yourself.
5. **Mockup review.** `agents/mockup-reviewer` gets every draft with its manifest, its record, the render_check output and PNG (or a line that it couldn't run) and, for a shared page, the screenshot path or an element inventory (personal values left out). It judges what the drawing means (variable shown, labels true, ring tight, neutral A/B, nothing unverified as fact), not only what render_check measures. On PASS the reviewer runs `build_card.py --template … --scenario <record> --stamp <draft.html>` (it writes nothing and refuses a draft or manifest the record no longer builds) and returns the JSON line it prints.
6. **Mockup stamp.** The JSON line the reviewer returned, `{"verdict": "PASS", "fingerprint": "<hex>"}`, into `review.mockup_reviewer`, exactly as printed.
7. **Final or conditional build.** The same command without `--draft`, `--out abtest-card-<slug>.html` in the user's working directory. It writes only when both stamps match; on refusal nothing is written and an existing file stays. It prints the final card's fingerprint; `build_card.py --template … --scenario <record> --check <card.html>` later confirms that a delivered file is byte for byte that reviewed card.
8. **Deliver** only that card, a conditional one named "koşullu kart" in chat, never final. Drafts and manifests are working files, never delivered or linked, with one exception (rule 9): when the visual check was unavailable (exit 3, verdict `UNVERIFIED`), give the draft as a preview labelled UNVERIFIED in chat, never called final (its ribbon says "TASLAK · incelenmedi" / "DRAFT · not reviewed"), with one line: the visual check couldn't run here (README → Visual check), and once it's installed the same draft is checked and finished from step 4. The final build still refuses without a mockup PASS stamp (code); that no PASS is given without a render is a review rule (process).

**Loops.** Critic FIX → fix the record, back to step 1 with the previous report; `[fixable]` items the critic fully specifies may be applied as given, then reviewed; a fix that needs a fact the user didn't give becomes a critical assumption instead. Mockup FIX `route: render` → fix only the mockup or `card.*`, rebuild the draft, resend; `route: scenario-critic` → back to step 1 (any record change, typographic included, voids the critic stamp). At most two re-reviews per reviewer; `RET`, or still FIX → not delivered, one sentence to the user. **Confirmed assumption:** remove it from `assumptions`, back to step 1; the new final card carries no ribbon.

**Never** write a stamp without a PASS or with a fingerprint not printed by the scripts, edit a draft into a final, or work around a refusal: it names the failed gate or field; fix the input.

## Never do

- Put any record text but the title on the card (no description, boxes, tags, notes, footer), or render a card for a record the validator refuses (rule 9).
- Render a dark-pattern scenario, even on "make the card" (rule 6).
- Escape text fields by hand (`&lt;` shows up as `&amp;lt;`); but escape `<`, `>`, `&` yourself in user text placed inside `variant_a` / `variant_b`.
- Use markup outside the allowlist: only the template's component tags (`div span p b strong i em u s small sup sub br hr ul ol li`) and `class`, `style`, `data-note`, `data-pos`, `title`, `role`, `aria-*`, double-quoted; no comments, links, images, scripts, event handlers, `url(`, `@import` or `position:fixed` (rule 18). A build warning (`build_card: warning: …`) is read, not ignored.
- Put a second difference in the mockups, or a "hidden / removed" placeholder where a removed element was.
- Draw a tab bar on a page that isn't a native app screen, or copy personal data from a screenshot (rule 15).
- Color elements with inline `style` instead of `card.brand`, add an external font or CDN link, pull a logo from a URL, or ask about or note the brand (rule 12).
- Render in a language other than the user's (rule 7); a Turkish card sets `lang: "tr"` and uses curly quotes.
