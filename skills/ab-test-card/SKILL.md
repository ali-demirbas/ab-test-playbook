---
name: ab-test-card
description: Render an A/B test scenario as a single-file HTML card in the archive's visual style — a Variant A/B mockup pair with the tested element ringed, plus the three coloured boxes and a footer with source, evidence and brand notes. Use when the user says "make a card for this test", "turn this into a card", "visualise this test", "render this scenario", "make a slide out of this", "show me the two variants side by side", "kart yap", "görselleştir", "slayt formatına çevir", "bunu karta bas". Runs automatically for every scenario produced by ab-test-suggest and ab-test-design (CLAUDE.md rule 9), so it rarely needs to be invoked directly. Output is self-contained HTML with no external assets, built deterministically by scripts/build_card.py from the scenario's own JSON.
metadata:
  version: 2.2.0
  category: render
  updated: 2026-10-10
---

# ab-test-card — Scenario Card Rendering

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

The visual language is defined in `${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md` — read it before producing anything. Template: `${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html` (its developer comment lists every mockup component with a markup example). Schema: `${CLAUDE_PLUGIN_ROOT}/templates/scenario.schema.json`; worked example: `${CLAUDE_PLUGIN_ROOT}/examples/scenario.json`.

This skill runs automatically for EVERY scenario that `ab-test-suggest` or `ab-test-design` produces in a turn (CLAUDE.md rule 9) — the user doesn't need to ask separately. The full content of the three boxes ("What to test" / "Primary KPIs to track" / "Never do") lives only in this card; the same content isn't also written to chat as text — chat keeps only the short header rule 9 defines. 1-5 scenarios in a turn become cards directly; if there are more than 5 strong candidates, the top 5 are produced and the rest offered (rule 9). The same flow runs if the user directly says "make a card."

## Flow

0. **Brand source (never blocks — CLAUDE.md rule 12).**
   - **Don't ask if the user shared a screenshot/page:** take the brand color, logo text and button style straight from the image and put them in `card.brand` (`{"primary": "#c9392b", "on_primary": "#fff", "name": "Brand"}`). The footer then carries the default note "I took the colors from the screenshot; send me the official guide and I'll update it." Don't stop the flow and wait for an answer.
   - **No visual source:** leave `card.brand` out. The neutral palette is used and the footer carries the neutral note offering a rebrand. Don't ask and don't wait. If the user gave a URL and a browser tool is available, visit it and take the colors (rule 12a); otherwise use the neutral palette.
   - **If a guide is given:** use its primary/CTA color, text-on-primary color and brand name in `card.brand`, and set `card.brand_note` to `null` (no rebrand note is needed any more). Write the brand name as text (`.r-logo`); never embed a logo file or link one.
   - A guide sent later replaces the palette for the rest of the session; the rebrand note isn't repeated on later cards.
1. Get the scenario to render: this session's `ab-test-suggest`/`ab-test-design` output, or text the user gives directly. Use the content in the text verbatim; don't rewrite or shorten the items while rendering the card. For text the user brings: set `source` to `generated` and `evidence.level` to what the user stated (`intuition` if nothing was stated), and leave `ice` and `objection` out rather than inventing them. If the three boxes are missing, a box has fewer than three items, there is no guardrail, or no mechanism is stated, don't fill the gap silently: route to `ab-test-design` (which runs scenario-critic) and tell the user in one sentence what was missing.
2. **Write ONE JSON per scenario** — the same file the schema validates, with a `card` object for the visual layer (a designed scenario already has its file from `ab-test-design`, pre-registration included: add `card` to that file). Don't fill the template by hand (CLAUDE.md rule 9 → Mechanism), and don't keep a second "card input" file next to it. Validate it first: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/validate_scenario_json.py scenario.json` (messages in Turkish by default, `--lang en` for English).

   | Field | What goes in it |
   |---|---|
   | `title`, `rationale` | The question-form title and the 2-3 sentence description. **Plain text, never pre-escaped**: the script applies `html.escape`. |
   | `lang` | `tr` or `en`: the user's language. Box headers, role pills, footer labels and `<html lang>` follow it. |
   | `test_items`, `dont_items` | At least three each. A labelled item is `{"label": "Kaçak", "text": "…?"}`; the script bolds the label and adds the colon. Never write `<b>` yourself. |
   | `kpis` | `[{"name", "role", "question"}]`, at least three, the **primary first**, at least one `guardrail`; a pass/fail check (accessibility) is a `guardrail` item whose text is its criterion. Rendered as the KPI box with a role pill per item (Birincil / Guardrail / İkincil). |
   | `source`, `adapted_from` | `archive` / `adapted` / `generated` (rule 8). An adapted scenario names the archive scenario's title in `adapted_from`. |
   | `evidence.level`, `objection`, `ice` | Evidence label (rule 10), the objection the change answers, `{"tier": "medium", "impact": 7, "confidence": 4, "ease": 9}`. All three go into the footer's tags line. |
   | `device` | `phone` = native app screen; `phone-web` = page in a mobile browser (status bar + address bar with lock and domain, no tab bar); `web` = desktop browser. `card.device` overrides it for the frame only. |
   | `card.variant_a` / `card.variant_b` | The mockup bodies, **raw HTML** built from the template's `.r-*` components. The rules below are for these two fields. |
   | `card.difference` | `change` / `add` / `move` / `remove` (the archive's "Fark:" line; `değiştir` / `ekle` / `taşı` / `kaldır` also accepted). The script refuses a card whose rings don't match it (below). |
   | `card.url` | Address bar text (`web`) or the domain shown in the mobile address bar (`phone-web`). If the real URL wasn't visible, say so in `card.footer_notes`. |
   | `card.bottom_nav` | `phone` only: the real app's tab labels. Leave it out for anything that isn't a native app screen; the script then draws no tab bar. Never copy placeholder tabs. |
   | `card.brand`, `card.brand_note` | Step 0. |
   | `card.mockup_basis` | `shared_page` (a redraw of the user's screenshot/URL), `described` (the page was only described in words; footer: "rebuilt from your description"), `representative` (no page; footer: "representative example"). |
   | `card.shift_note_a` / `card.shift_note_b` | One line under each mockup. `shift_note_b` is required for `remove` ("coupon field removed, the content below shifted up"). |
   | `card.note_pos` | `above` (default) or `below`: where ring labels sit. One ring can override with `data-pos="below"`. |
   | `card.footer_notes` | One-line notes about the drawing only: what wasn't visible, what was masked or left out. Never advice, a to-do for the user, or anything about changing Variant A. One exception: the "Stronger alternative: …" line on a weak test the user explicitly asked for (rule 9). |

   The legacy flat shape (`desc`, `kpi_items`, `variant_a`, … at the top level) still builds, but new cards use the schema shape above.
   - **Content is written fully realistic** (`mockup-style.md` → Realism level): real copy, prices, labels and layout; no "Heading," "Lorem ipsum" filler. Use the template's `.r-*` components (header bar, tabs, fields and dropdowns, filled/outlined buttons, product grid, plan card, stepper, checkbox/radio, info line, chips, popup, search with suggestions, dark photo hero `.ph.hero`, badges, price lines) — don't invent markup or inline-style colors from scratch. Gray `.ph` blocks stand in only for a photo, never for text. An element B adds is drawn in the styles the page already uses (existing `.r-*` text styles, the page's own bullet and icon style): no colour, icon or emphasis that A's screen doesn't have, and never the brand colour on bullets or text unless that colour is the tested variable. A styled addition tests content and styling at once.
   - **If the user shared a page, the mockup is a redraw of THAT page, not a made-up one.** Product name, price, button copy, field labels, section order — whatever's on screen is what gets written. Variant A is exactly the on-screen state (rule 15): don't redesign it, simplify it, or fill in gaps. Don't make up a detail that's unreadable in the screenshot: either leave it out of the mockup or ask, in its place in rule 19's order.
   - **Personal data is never copied** (rule 15), typed or displayed. Typed values: draw the field empty, with its label and only a placeholder that's really on the page. Account data on a logged-in screen (holder's name, balance, holdings, allocation, contribution, premium, policy, contract or customer number, plan code) and everything derived from it (percentages, chart slices, bar fills): keep the label and the layout, mask the value ("••• TL", "•••"), draw a chart with equal neutral slices and no percentages, identical in A and B, and add `card.footer_notes`: "Account values are masked." A masked value is not filler.
   - **Don't invent a regulated number** (a monthly payment, rate, premium, "from X" price): `mockup-style.md` → Numbers the mockup needs but must not invent.
   - The tested difference is ringed and **the ring carries a short label saying what changed**: `<div class="hl" data-note="coupon field collapsed">`, two or three words. Ring placement by `card.difference`: **change** → B (A optional); **add** → B only; **move** → both; **remove** → A only, B left genuinely empty, plus `shift_note_b`. One change applied to N repeated elements gets **one ring around the group**. A difference the tested variable directly causes is allowed and labelled (a linked difference), not a second variable. `.hl` is drawn as an outline and takes no space: never give it, or a wrapper around it, a `style` attribute, margin, padding, border or background to make room for the label; move the label with `data-pos="below"` or `card.note_pos`. Everything below the ringed element sits exactly where it sits in the other variant, apart from the shift the change itself causes.
   - Everything except the tested element (and its linked consequences) must be identical between the two variants.
3. Render the card:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py \
     --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html \
     --scenario scenario.json \
     --out abtest-card-<slug>.html
   ```

   The script produces a single self-contained HTML file (inline CSS, no external source) and verifies after writing that the fixed skeleton wasn't disturbed. If it errors, no file is written: fix the input (the message says which field or which ring), don't fall back to building the card by hand. The output is written to the user's working directory. If Node with Playwright is available, `node ${CLAUDE_PLUGIN_ROOT}/scripts/render_check.mjs abtest-card-*.html` measures the rendered cards (overflow, clipped content, ring labels covering text) and `--shot` saves a PNG of each.
4. **Review (CLAUDE.md rule 17) — one reviewer for the whole turn.** After all of the turn's cards are produced, run `agents/mockup-reviewer` **once**, passing every card, its JSON, the `render_check.mjs` output if it ran, and for a shared page the screenshot's file path or a written element inventory (personal values left out); don't spawn one reviewer per card. It looks for a second difference beyond the tested element, ring placement against the difference type, personal data (typed or displayed), a fake tab bar, labels covering content and the footer tags. If it returns `FIX` for a card, fix only that card's mockup markup or card fields (`card.*`) and re-render it — **never change the three boxes, title or description in this step**, apart from typographic corrections (quotes, characters, escaping). If the fix would require changing the scenario's content (e.g. the tested variable itself was drawn differently from the scenario), send the scenario back through `agents/scenario-critic` first, then re-render. Don't write the review report to chat; only state a constraint the user needs to know, in one sentence, if there is one.
5. **Verify, then deliver.** If you can view the card (a browser tool, or `render_check.mjs --shot` and reading the PNG), look at it before delivery: text overflow, clipped content, a ring label covering text, character rendering, brand colours. Fix and re-render what you find; a change to mockup markup goes through step 4 again, a change to `card.note_pos` or `data-pos` doesn't. Then deliver the file.

## Never do

- Render a card for a scenario missing the three boxes.
- Render a card for a scenario containing a dark pattern — even if the user directly says "make the card," CLAUDE.md rule 6 still applies; refuse and say why.
- Put a `<script>` tag or interactive code in the card; the card is static HTML/CSS only.
- **Escape text fields by hand, or hand over pre-escaped text.** Title, description, the three boxes' items, notes and tags are escaped by the script; if you write `&lt;` into the JSON, `&amp;lt;` shows up on the card. Give plain text. (Why escaping is in code rather than a rule: a manually embedded string like "should the CTA be < 3 words?" or "shipping & returns" silently breaks the card, and a bold label leaking as a literal tag if escaping runs before the label is applied — neither mistake can be left to be remembered case by case.)
- **Embed user text raw inside the `variant_a`/`variant_b` markup.** When writing a product name, button copy or a piece of user-shared text into the mockup, escape `<`, `>`, `&` yourself; escaping is automatic only for the text fields. The two mockup fields go through `build_card.py`'s allowlist: only the template's component tags (`div span p b strong i em u s small sup sub br hr ul ol li`) and the attributes `class`, `style`, `data-note`, `data-pos`, `title`, `role`, `aria-*`, every value double-quoted; no comments, links, images, scripts or event handlers, and no `url(`, `@import` or `position:fixed` in an inline style. A refused card names the tag or attribute; fix the markup, never work around the refusal (rule 18). The builder also validates the scenario first and prints warnings (`build_card: warning: …`): read them, they are usually a real second variable or a missing denominator. `--lang tr` gives Turkish messages; `card.url` is required on `web` and `phone-web`; `card.bottom_nav_active` (label or 0-based index) marks the active tab.
- Put a second difference between the two variants in the mockup.
- Put a placeholder saying "hidden / removed" where a removed element used to be (`mockup-style.md`); in B, don't write that block at all — let the content below it naturally shift up, and say so in `card.shift_note_b` (rendered **below** the mockup, never inside the screen).
- Draw a tab bar on a page that isn't a native app screen, or copy anyone's personal data, typed or displayed, from a screenshot into the mockup.
- Color individual elements with inline `style` overrides instead of `card.brand`.
- Add an external font/CDN link; the card must open offline (system font: falls back to -apple-system/Segoe UI if Inter isn't available).
- Render the card in a different language from the user's (rule 7); set `lang`, use curly quotes and full Turkish character support on a Turkish card.
- Ask a brand-guide question or wait for one; take colors from the screenshot if there is one, otherwise use the neutral palette with the footer's rebrand note.
- Try to pull the brand logo from an external URL; use only what the user has given (a color code, a brand name).
