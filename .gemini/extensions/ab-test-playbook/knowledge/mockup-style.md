# Visual Language: Scenario Card and Mockup Rules

**This file, the core, is read for every card;** a file in `knowledge/mockup-style/` only when its trigger applies:

| When | File |
|---|---|
| A move below the fold, to a pinned bar or to another step; a soft ring; a stepper, carousel dots, a text button, a modal, a photo hero | `special-cases.md` |
| Raw `card.variant_a` / `card.variant_b` markup (what the node list can't express) | `raw-markup.md` |
| Fast mode, or "tamamla" / "finish" after quick drafts | `fast-mode.md` |
| render_check exit 3 (the UNVERIFIED preview); a share image, an overview, `--check`; a ribbon or build question | `draft-and-final.md` |
| A render_check error or warning; a frame's scale; what the template draws | `render-check.md` |

## The card

One job: compare Variant A and Variant B and see the one change; everything else stays in the record (CLAUDE.md rule 9). The builder draws only the `title` (a question, at most two lines), the pills ("Varyant A · Mevcut" / "Variant A · Current" when `variants[A].is_current`), the two mockups side by side, the ring with its label and a draft or conditional ribbon. **Never on the card:** a problem line, mechanism, variable, KPI, guardrail, source, evidence, objection or priority tags, warnings, invariants, assumptions, `detail`, a footer, a brand, mockup-basis, masking or shift note, the "Stronger alternative:" line; inside the mockups nothing beyond the page's own copy and the ring labels. **Language:** copy and currency follow the user's page (rules 7, 15: an English/USD page isn't translated); with no shared page, the user's language, and a currency only when the market is known (else no prices unless the test needs them); complete Turkish characters and curly quotes. `card.theme: "dark"` darkens the ground, title and pills; the mockups keep the page's colours.

## Frames

`device`: `phone` a native app screen with a status bar, a tab bar only when the real app has one (`card.bottom_nav` with its own labels, `card.bottom_nav_active` the same tab in A and B; an invented tab bar is a realism error); `phone-web` a page in a mobile browser (most shared mobile screenshots, and a website the user calls mobile): an address bar with `card.url`'s domain, never a tab bar, `card.mobile_toolbar: true` adds the browser's bottom toolbar in both arms; `web` a desktop browser filling the column, three dots and the address bar, no status or tab bar, a `fold` drawn as the dashed "İlk ekranın sonu" line. **Height = content height** (no blank screen). Draw the part the test is about (the element, the context to read it, what it shifts); decoration and repeated rows may be left out of A, and then of B, never anything the test, its KPI or a warning is about. The builder picks the frame's scale (`render-check.md`); `card.phone_scale` / `card.web_scale` only override it. A screen that still clips is too long: tighten it or use a fold, never cut away the tested element.

## Ring and label

The builder rings what `card.change` names and soft-rings what `card.soft` names (up to two ids). The op matches `difference`: `insert_*` an add (B only), `remove` a removal (A only, labelled as one, B genuinely empty), `move_*` a move (both arms, each label true for its arm: "Telefon ilk adımda" / "Telefon teklif sonrasında"), `replace` or `edit` a change (`label_a` rings A too). One change on N repeated elements: one ring around the group. Ring the variable itself, never the section around it.

- **Label:** two to four words saying what changed ("Kupon alanı bağlantıda"), Turkish starting with a capital (else refused). It needs about 31px clear on its side: the builder places it where `label_pos` / `card.note_pos` asks and moves it off anything it would cover; on a tight page pick the side, or crop identically in both arms, never remove a field from the middle of A. Too wide for the screen → refused: shorten it.
- **Only the tested element differs:** the builder refuses any difference outside the rings and lists every one inside in the manifest. A number (price, amount, percentage, count, rating) differs only when it is the variable and `numeric_change` explains it. A consequence the variable forces (an annual default shows annual prices) goes in `card.soft`; one it doesn't force is a second variable.
- **Colours are page state:** a page colour (a grey band, a tinted section) is a node override, the same in both arms; an element B adds uses the styles A's screen already has (no new colour, icon or emphasis; the brand colour on text only when colour is the variable). A page text colour under the contrast floor stays and goes in `card.inherited_contrast` (exact text, colour as measured; identical in both arms, outside the rings); an icon glyph takes `role="img"` (3:1).
- **Refused by the builder:** legal, mandatory, verification or security text in A missing in B, or a consent box ticked only in B (rules 6, 11; the words it looks for: `raw-markup.md`); an added interactive element (CTA, link, field, checkbox, radio, chip, tabs, search, overlay, modal) without the record's `accessibility` warning (rule 3).

## Realism level

Real text, prices, labels and layout; an `img` placeholder only for a photo, never for text; no "Heading", "Lorem ipsum". **Realistic means the user's own page, not a made-up one**, the card's most critical rule; `card.mockup_basis` (never printed) records the case: **`shared_page`** (screenshot, URL or flow) a redraw of that page, A exactly the on-screen state (rule 15), never redesigned or "improved", a detail the screenshot doesn't show left out or asked, never made up; **`described`** (only words) realistic assumed copy, market-neutral when the market isn't known (no invented brand, payment method or legal phrase), one chat line says so; **`representative`** (no page) a representative example, said in chat only when the user could take it for their own page. With no user-given URL, `card.url` is a `.example` domain (`magaza.example/sepet`).

**Brand** (rule 12): `card.brand: {"primary": "#c9392b", "on_primary": "#fff", "name": "Brand"}` from a shared screen (or a shared URL, visited when a browser tool is available), taken silently, or an official guide, which replaces it for the session; the name as text, never a logo file; plain color syntax only; without it, the neutral palette. The ring, label and pills never take the brand color.

## Screen spec

`card.screen` is a node list, `card.change` one op naming the tested element; `build_card.py` compiles both arms from them (raw markup instead: `raw-markup.md`; both forms at once are refused). Overrides (`fg`, `bg`, `border`, `radius`, `height` as `#rrggbb`/px) are identical in both arms; siblings get a 16px gap unless a node sets `mb`.

| Node (one key names the kind; optional `id`) | Draws |
|---|---|
| `header` {logo true/"Text", nav [], tel, icons [{icon close/support/menu/search/back, label}], line false} | `.r-header` (`line: false` → no border) |
| `h`, `sub`, `text` (+ align center/left) | `.r-h`, `.r-sub`, plain div |
| `logos` [names] (+ caption) · `price` text (+ old, per) · `stars` "4,4" or 4.6 (+ count) · `cols` [2-4 nodes] | wordmark strip · big price, old one struck through · stars and the value as written · equal columns |
| `field` placeholder (+ label, select, value: never personal data) · `row` [fields] | `.r-label` + `.r-field` · `.r-row` |
| `cta` text (+ style filled/outline/ghost, size sm, align center/left) · `link` (+ align) · `help` · `info` | `.r-cta` · `.r-link` · `.r-help` · `.r-info` |
| `check`/`radio` text (+ on) · `chips`/`tabs` [{label, on}] · `steps` [{label, state}] · `progress` n | `.r-check`/`.r-radio` · `.r-chips`/`.r-tabs` · `.r-steps` · `.r-progress` |
| `line` [label, value] (+ total) · `item` {name, meta, price} · `plan` {name, price, old, per, note, featured, badge, cta, cta_style, features} | `.r-line` · `.r-item` · `.r-plan` |
| `badge` text (+ style warn/brand) · `banner` · `img` height · `divider` · `gap` px | `.r-badge` · `.r-banner` · photo · `.r-divider` · spacer |
| `band` {bg, items [], pad [top, bottom]} · `stack` {items [], gap, align center} | full-bleed region · flex column |
| `accordion` {title, open, items []} | header row with its `+`/`−` sign, the body only when `open` (then with `items`); `edit` {"set": {"open": true}} opens it in B |
| `fold` · `stage` · `sticky` (only with a fold) | `special-cases.md` |

Ops (exactly one, each with its ring `label` and optional `label_pos` above/below): `insert_after` / `insert_before` {target, node} · `replace` {target, node, label_a} · `remove` {target} · `move_after` / `move_before` {target, to, label_a, label_b} · `edit` {target, set {key: value}}: one property of one node, ringed around the part that changed (`"ring": "node"` rings the whole node). Unknown kind, missing target, duplicate id or two changes stop the build. Example, a form on a grey band:

```json
"screen": [{"header": {"logo": true, "line": false}}, {"h": "Sağlık Sigortası"},
  {"band": {"bg": "#f5f5f5", "items": [{"field": "T.C. Kimlik Numaranız", "id": "tckn", "border": "#9a9b9d", "height": 52, "mb": 10}, {"field": "E-Posta", "border": "#9a9b9d", "height": 52}]}}],
"change": {"op": "insert_after", "target": "tckn", "node": {"help": "Teklifinizi hazırlamak için bu bilgiye ihtiyaç duyuyoruz."}, "label": "Gerekçe satırı eklendi", "label_pos": "below"}
```

## Personal data is never copied

Values typed into a screenshot's fields (name, e-mail, phone, ID or tax number, card number, address, licence plate) are the user's input, not page state (rule 15): never in the mockup, the JSON or the chat; the field is drawn empty, with its label and only a placeholder really on the page. A default the page ships ("30-65" in a dropdown) is page state. **Derived figures are personal too** (`knowledge/methodology.md` → Variable isolation): balances, accumulated amounts, allocation percentages, chart slices, return rates, contributions, contract, policy or plan numbers. Keep the structure, drop the values: "••• TL" (the page's currency label), "•••" for numbers and codes, a chart in neutral equal slices without percentages or legend values, masks identical in A and B, no note; `card.brand` never takes a chart's colors. A test about such a figure is held and a sample value asked for (rule 19). The builder refuses TCKN, TR IBAN, grouped card, e-mail and 05xx mobile shapes (masks and all-zero placeholders pass); any other shape is the producer's to drop and the reviewer's to catch.

## Numbers the mockup needs but must not invent

A monthly payment, interest rate, premium, "from X" price or credit cost is a regulated display (rule 11) and personal; a sample figure on a card reads as a real quote. **The test is about the number:** no made-up figure; hold the scenario, say why in one line and ask for the real figure (rule 19), which is then page state in both arms. **The element merely contains one:** draw it without the figure. **Computed from the user's figures** (an annual price from a stated monthly price and discount, the sum left to a stated free-shipping threshold): draw it and say in one chat line how; a missing input is asked for. Shop prices on a shared screenshot are page state, identical in both arms unless the amount is the variable (`numeric_change`). **Unverified is not drawn as settled:** a representative value is named in the critical assumption; no invented explanatory sentence ("Yıllık olarak faturalandırılır"), and no line added to both arms just to show it.
