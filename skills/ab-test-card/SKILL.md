---
name: ab-test-card
description: Render an A/B test scenario as a single-file HTML card in the archive's visual style — a Variant A/B mockup pair with the tested element boxed, plus the three coloured boxes. Use when the user says "make a card for this test", "turn this into a card", "visualise this test", "render this scenario", "make a slide out of this", "show me the two variants side by side", "kart yap", "görselleştir", "slayt formatına çevir", "bunu karta bas". Runs automatically for every scenario produced by ab-test-suggest and ab-test-design (CLAUDE.md rule 9), so it rarely needs to be invoked directly. Output is self-contained HTML with no external assets, built deterministically by scripts/build_card.py.
metadata:
  version: 0.1.0
  category: render
  updated: 2026-08-17
---

# ab-test-card — Scenario Card Rendering

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

The visual language is defined in `${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md` — read it before producing anything. Template: `${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html`.

This skill runs automatically for EVERY scenario that `ab-test-suggest` or `ab-test-design` produces in a turn (CLAUDE.md rule 9) — the user doesn't need to ask separately. The full content of the three boxes ("What to test" / "Primary KPIs to track" / "Never do") lives only in this card; the same content isn't also written to chat as text — chat only keeps the title, source tag and a one-sentence summary. 2-5 scenarios in a turn become cards directly; if there are more than 5 strong candidates, they aren't all produced without asking (rule 9). The same flow runs if the user directly says "make a card."

## Flow

0. **Brand source (once per session).**
   - **Don't ask if the user shared a screenshot/page:** pull the brand color, logo text and button style straight from the image and use them. Add a one-line note under the card: "I took the colors from the screenshot; send me the official guide and I'll update it." Don't stop the flow and wait for an answer.
   - **Ask if there's no visual source:** "Should I prepare the card to your brand guide (logo, color palette), or use a neutral style?" Wait at this step until an answer comes. If the user gave a URL, that also counts as a page share (rule 12a): if a browser tool is available, visit the site and pull the colors from there without asking; if not, fall back to the question above.
   - **If a guide is given:** extract the colors (primary/secondary, CTA color), the logo/brand name and any typography preference; use these instead of the neutral palette in `mockup-style.md`. Instead of embedding the logo as a real file, write the brand name/abbreviation from the guide as text in the header (so the "no external asset links" rule isn't broken).
   - **If not given / the answer is "no":** use the neutral palette (teal/amber/navy) from `mockup-style.md`.
   - The choice is remembered for the rest of the session (CLAUDE.md rule 12), not asked again on later cards — unless the user wants to change it.
1. Get the scenario to render: this session's `ab-test-suggest`/`ab-test-design` output, or text the user gives directly. If the three boxes are missing, complete them first (route to `ab-test-design`). Use the content in the text verbatim; don't rewrite or shorten the items while rendering the card.
2. Write the scenario to a JSON file; don't fill the template by hand (CLAUDE.md rule 9 → Mechanism). Fields:
   - `title`, `desc` and the three boxes' items (`test_items`, `kpi_items`, `dont_items`): **give plain text, don't escape it yourself** — the script applies `html.escape`. An item that wants a bold label is given as `{"label": "Primary KPI", "text": "cart → checkout"}`; don't write `<b>` by hand, it breaks the ordering.
   - `device`: `"phone"` for a mobile context, `"web"` for desktop/web (+ `url` for the address bar). The script handles switching to the browser skeleton; don't copy the skeleton from the comment by hand.
   - `variant_a` / `variant_b`: the mockup markup, as **raw HTML**. The rules below are for these two fields.
   - Mockup area: if the scenario is mobile-context, use the `.phone` skeleton (status bar + bottom nav); if desktop/web-context, use the template's `.browser`/`.browser-bar`/`.browser-url`/`.browser-screen` skeleton (three dots + address bar + white body, no statusbar/bottomnav). If a brand guide was given, the header/CTA color and brand name follow it; if not, the neutral palette.
   - **Content is written fully realistic** (`mockup-style.md` → Realism level): real copy, prices, labels and layout; no "Heading," "Lorem ipsum" filler. Use the template's `.r-*` components (`.r-item` a product row, `.r-field` a form field, `.r-line` a price line, `.r-cta`, `.r-badge`, `.r-stars`) — don't invent markup from scratch. Gray `.ph` blocks stand in only for a photo (product image, avatar), never used in place of text.
   - **If the user shared a page, the mockup is a redraw of THAT page, not a made-up one.** Product name, price, button copy, field labels, section order — whatever's on screen is what gets written. Variant A is exactly the on-screen state (rule 15): don't redesign it, simplify it, or fill in gaps. Don't build a page from your own head and fit the test onto it. Don't make up a detail that's unreadable in the screenshot: either leave it out of the mockup or ask. If there's no shared page (an archive scenario), build a representative example, but don't present it as if it were a real customer's page.
   - The tested difference is highlighted with a red outline, and **the outline carries a short label saying what changed**: `<div class="hl" data-note="coupon field collapsed">`. The label doesn't exceed two or three words. For a removal test, the outline is drawn on the element in A.
   - Everything except the tested element must be identical between the two variants (the mockup-style.md rule).
3. Render the card:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py \
     --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html \
     --scenario scenario.json \
     --out abtest-card-<slug>.html
   ```

   The script produces a single self-contained HTML file (inline CSS, no external source) and verifies after writing that the fixed skeleton wasn't disturbed. If it errors, no file is written: fix the error, don't fall back to building the card by hand.  The output is written to the user's working directory.
4. **Review (CLAUDE.md rule 17).** After the card is produced, run `agents/mockup-reviewer`: it looks for whether there's a second difference between the two mockups beyond the tested element. If it returns `FIX`, fix it and re-render the card. Don't write the review report to chat; only state a constraint the user needs to know, in one sentence, if there is one.
5. Deliver directly to the user (file delivery). If you have a way to view it (a browser tool), open it and verify: text overflow, character rendering, box alignment, whether brand colors were applied correctly.

## Never do

- Render a card for a scenario missing the three boxes.
- Render a card for a scenario containing a dark pattern — even if the user directly says "make the card," CLAUDE.md rule 6 still applies; refuse and say why.
- Put a `<script>` tag or interactive code in the card; the card is static HTML/CSS only.
- **Escape text fields by hand, or hand over pre-escaped text.** `title`, `desc` and the three boxes' items are escaped by the script; if you write `&lt;` into the JSON, `&amp;lt;` shows up on the card. Give plain text. (Why escaping is in code rather than a rule: a manually embedded string like "should the CTA be < 3 words?" or "shipping & returns" silently breaks the card, and a bold label leaking as a literal tag if escaping runs before the label is applied — neither mistake can be left to be remembered case by case.)
- **Embed user text raw inside the `variant_a`/`variant_b` markup.** These two fields pass through as raw HTML — when writing a product name, button copy or a piece of user-shared text into the mockup, escape `<`, `>`, `&` yourself. Escaping is automatic only for the text fields. This isn't the only line of defense: `build_card.py`'s `self_verify` step also refuses to write a card whose built HTML contains a `<script>` tag, an inline event-handler attribute (`onerror=`, `onclick=`, ...), a `javascript:`/`vbscript:` URI, an `<iframe>`/`<object>`/`<embed>`, or a `data:text/html` URI — a deny-list backstop at the code level, not something that depends on this instruction being remembered. It's a deny-list, not a full allowlist sanitizer, so escaping proactively here still matters.
- Put a second difference between the two variants in the mockup.
- Put a placeholder saying "hidden / removed" where a removed element used to be (`mockup-style.md`); in B, don't write that block at all — let the content below it naturally shift up. To make the shift visible, add a one-line note **below** the mockup: `<div class="shift-note">…</div>` — this note doesn't go inside the screen itself.
- Add an external font/CDN link; the card must open offline (system font: falls back to -apple-system/Segoe UI if Inter isn't available).
- Render the card in a different language from the user's (rule 7); curly quotes, full Turkish character support on a Turkish card.
- Ask the brand-guide question and stall the flow when a screenshot exists; take the colors from the image. Also don't silently default to the neutral palette when there's no visual source at all — ask in that case.
- Try to pull the brand logo from an external URL; use only what the user has given (a color code, a brand name).
