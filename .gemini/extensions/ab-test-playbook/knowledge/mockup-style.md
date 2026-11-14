# Visual Language: Scenario Card and Mockup Rules

**Core, read for every card:** The card · Frames · Ring and label · Realism level · Screen spec · Personal data is never copied · Numbers the mockup needs but must not invent (all above "# On demand": `awk '/^# On demand/{exit} 1' ${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md`).
**On demand, when the card needs it:** Components (`.r-*` markup) · Special cases (steppers, fold and sticky bar, stages, soft ring, carousels and dots, text buttons, modals, photo backgrounds) · Brand · Card layout · Draft and final card · render_check (`awk -v h='## <title>' 'index($0,h)==1{p=1;print;next} p&&/^##? /{exit} p' ${CLAUDE_PLUGIN_ROOT}/knowledge/mockup-style.md`).
`ab-test-card`, the card template, `build_card.py` and `render_check.mjs` follow this spec.

## The card

One job: let a reader compare Variant A and Variant B and see the one change. Everything else lives in the scenario record (CLAUDE.md rule 9).

- **On the card:** the record's `title` (a question) at the top, at most two lines, nothing under it; the "Variant A" / "Variant B" pills (in every language); the two mockups side by side, frames top-aligned and the same width; the ring around the changed element and its short label. A draft adds its ribbon; a record with a critical assumption builds a conditional card with the "KOŞULLU · doğrulama gerekli" / "CONDITIONAL · needs verification" ribbon (Draft and final card).
- **Never on the card:** a description or problem line, mechanism, variable, KPI, guardrail, source, evidence, objection or priority tags, warnings, invariants, assumptions, `detail`, a footer, a brand, mockup-basis, masking or shift note, the "Stronger alternative:" line; inside the mockups, no explanatory text beyond the page's own copy and the ring labels.
- **Layout:** 1600 × 900, fixed; the template sets the title, pills, columns, background and the system font stack (no font file, so the card opens offline).
- **Neutral palette** (no shared screen, no guide; rule 12): text `#111827`, secondary `#374151`, muted `#6b7280`, borders `#e5e7eb` / `#d1d5db`, surfaces `#ffffff` / `#f9fafb`, link `#2563eb`, success `#15803d`, warning `#b45309`; `--brand` `#1f2937` on `--on-brand` `#ffffff`. A page's or guide's colors: Brand.
- **Language:** copy and currency follow the user's page (rules 7, 15; an English/USD page isn't translated into Turkish/TRY). With no shared page: the user's language, and a currency only when the market is known (otherwise no prices unless the test needs them). Complete Turkish characters ("Baslık" isn't accepted) and curly quotes.

## Frames

Components are drawn at their sizes and never scaled on their own (no `zoom`, `transform` or smaller text to make content fit); only the phone frame as a whole carries `zoom: 1.2` (420px drawn 504px wide). A phone-web frame holds about 500px of content under its bars (native a little more) before render_check reports it clipped. For a tall screen the test needs whole, tighten the drawing first (a label and its field in one block, `.r-steps` for a step indicator), then set `card.phone_scale: 1` (about 120px more); never cut away an element the test or its regulation warning is about. A short screen (a single phone filling under 62% of the stage) takes `card.phone_scale: 1.4` when it still fits; render_check names the scale. Stage phones (Special cases) are never rescaled. A short desktop page (`device: web`, a cart summary or a pricing row) that leaves most of the stage empty takes `card.web_scale: 1.2` or `1.4`, which zooms the whole browser frame; check the PNG that nothing wraps awkwardly.

| `device` | Frame |
|---|---|
| `phone` | A native app screen, 420px wide, with a status bar. A bottom tab bar only if the real app has one: `card.bottom_nav` with its own labels, `card.bottom_nav_active` (label or 0-based index) the same tab in A and B. An invented tab bar is a realism error. |
| `phone-web` | A page in a mobile browser (landing, form, checkout, most shared mobile screenshots): the phone frame plus an address bar with the domain from `card.url`; `card.mobile_toolbar: true` adds the browser's bottom toolbar, identical in both arms (chrome, never diffed). Never a tab bar. |
| `web` | A desktop browser frame filling the column (about 728px): three dots and the address bar (`card.url`). No status or tab bar. |

**Height = content height**, never a fixed or minimum height, so a phone frame shows no blank screen; content past the stage is clipped and reported. Draw the part of the screen the test is about (the element, the context to read it, what it shifts), not the whole page. What may be left out of A to fit: decoration and repeated rows (a third identical list item, a footer, a header icon nothing refers to); never anything the test, its KPI or a warning is about. What is left out of A is left out of B too. First-screen, sticky, pinned and multi-step tests: Special cases.

### Component scale

Phone base 15px, web base 14px; headings 18-20px / 600; meta and help text 13px; nothing below 12px. CTA 15px / 600 and fields at least 44px tall on phone.

## Ring and label

- **Ring:** `outline: 3px solid #e11d48; outline-offset: 4px; border-radius: 10px;` no glow, no fill; an outline takes no space, so a ringed element sits where its twin sits in the other arm. The `.hl` wrapper has no margin, padding, border, background or `style` of its own (the builder refuses inline margin or padding); a ringed component's own style (`class="r-card hl" style="max-width:320px"`) is identical in A and B.
- **Spacing parity.** A bare `.hl` around several siblings of a gap container (`.screen`, `.browser-screen`, `.r-card`, `.r-modal`, a flex row) removes their gap, and in a `.r-row` it takes the element's flex sizing. Ring one element, or wrap the siblings in the same plain container in both arms (`<div style="display:flex;flex-direction:column;gap:16px">`).
- **Room, nothing covered.** The ring crosses no neighbour; the room comes from the mockup's own spacing, the same in A and B: at least 8px around a ringed element (the outline takes 7px), about 31px free above it when the label sits on top (label 25px plus a 6px gap; a margin-bottom on the element above or a plain outer wrapper, identical in both arms, never inside `.hl`), the label at least 6px clear of anything and never on a line (a header's bottom border, a divider, a tab underline, a field border).
- **Label:** `.hl[data-note]`, two to four words saying what changed ("Kupon alanı bağlantıda"; a Turkish label starts with a capital, or the builder refuses it); a pill outside the ring at its top-right, `data-pos="below"` (one ring) or `card.note_pos: "below"` (the card) moves it below.
- **Where rings go** (the record's `difference`; `card.difference`, when present, equals it; the builder refuses a card that breaks this): **change** (değiştir) the changed element in B, its old state in A optional; **add** (ekle) only B; **move** (taşı) the same element in both arms, old place in A and new place in B, identical copy, size and style, each arm's label true for that arm ("Telefon ilk adımda" / "Telefon teklif sonrasında"), a gap or shift it causes being a linked difference the label names (below the fold, pinned or to another step: Special cases); **remove** (kaldır) the element in A, labelled as a removal ("Kupon alanı kaldırıldı"), B genuinely empty there (no "removed" placeholder; the content below shifts up). One change on N repeated elements gets **one ring around the group**, never N rings.
- **Tight ring.** Ring the variable itself, never the section around it; render_check refuses a `.hl` over 45% of its screen, or wider than 85% and taller than 40%. What the variable forces elsewhere gets a soft ring (Special cases).
- **Only the tested element differs.** The builder diffs A and B: a difference outside the rings refuses the card; every one inside goes into the manifest.
  - **Numbers** (price, amount, percentage, count, rating) are identical unless the number is the variable and `numeric_change` explains it (a price test), still inside a ring.
  - **Linked differences** the variable forces (an annual default shows annual prices; a removed field shortens the form) are drawn and named: the ring on the variable (the toggle), a `.hl-soft` on the consequence (the prices); a change it doesn't force is a second variable.
  - **Inline colors are page state:** a color only B has (a brand-colored bullet) is a second variable unless it is the variable. A colour the page itself has (a grey form band, a tinted section) is drawn with the same inline style in both arms; leaving it out makes A a different page, which is the error. A page text colour under the contrast floor is kept and documented in `card.inherited_contrast` (shared page, identical in both arms, outside the rings); an icon glyph carries `role="img"` and is held to 3:1.
  - **Legal, security and consent displays stay as A shows them.** Legal or mandatory text in A (KVKK, aydınlatma, cayma, faiz, toplam maliyet, yıllık maliyet, sözleşme, terms, privacy, APR) missing in B refuses the card and holds the scenario (rule 11); so does verification or security text (doğrulama, SMS kodu, CAPTCHA, şifre, iki adımlı, verification code, password) missing in B, or a consent box ticked only in B (rule 6).
  - **An added interactive component** (`.r-cta`, `.r-link`, `.r-field`, `.r-check`, `.r-radio`, `.r-chip`, `.r-tabs`, `.r-search`, `.r-overlay`, `.r-modal`, or more of one than A) needs the record's `accessibility` warning with the fitting criteria (44×44 pt / 48×48 dp target, 4.5:1 contrast, keyboard, screen-reader name; a modal also focus and close with a visible control and Esc; an auto-advancing carousel a pause; `knowledge/methodology.md` → Accessibility checks), or the card is refused. A tiny target or low-contrast text drawn in B is a reviewer FIX.

## Realism level

**Fully realistic:** real text, prices, labels and layout; gray `.ph` blocks only for **a photo** (a product image, an avatar), never for text; no "Heading", "Lorem ipsum", "Text field". **Realistic means the user's own page, not a made-up one**, the card's most critical rule; `card.mockup_basis` records the case (for the reviewer, never printed):

- **`shared_page`** (screenshot, URL or flow): a redraw of that page, names, prices, copy, labels and order as on screen. Variant A is exactly the on-screen state (rule 15), never redesigned, simplified or "improved"; B differs in one element. A page from your own head with the test fitted onto it is fabrication. A detail the screenshot doesn't show (cut-off text, a hidden section) is left out or asked, never made up.
- **`described`** (only words): rebuilt from the description with realistic assumed copy, market-neutral where the market isn't known (no invented brand, local payment method or legal phrase); one chat line says so. With no user-given URL, `card.url` is a `.example` domain (`magaza.example/sepet`), also for `representative`; a user-given URL stays.
- **`representative`** (no page, e.g. a generic archive scenario): a representative example; chat says so only when the user could take it for their own page.

A finished-looking design draws comments on color and wording rather than "this flow is built wrong"; the ring with its label and the question-form title keep attention on the tested variable.

## Screen spec

The producer describes the screen, the builder draws it: `card.screen` is a node list, `card.change` one op naming the tested element; `build_card.py` compiles both arms from them, so A and B cannot differ anywhere else. Raw `card.variant_a`/`variant_b` markup stays for what the list can't express; both forms at once are refused. Overrides (`fg`, `bg`, `border`, `radius`, `height` as `#rrggbb`/px) become inline style identical in both arms; siblings get the template's 16px gap unless a node sets `mb`; the page's real spacing is copied with `mb`/`gap` only where it matters.

| Node (one key names the kind; optional `id`) | Draws |
|---|---|
| `header` {logo true/"Text", nav [], tel, icons [{icon close/support/menu/search/back, label}], line false} | `.r-header` (+ `.r-logo`/`.r-nav`/`.r-tel`, icons as `role="img"`; `line: false` → no border) |
| `h`, `sub`, `text` (+ align center/left) | `.r-h`, `.r-sub`, plain div |
| `field` placeholder (+ label, select, value: never personal data) · `row` [fields] | `.r-label` + `.r-field` (`.empty`, `.select`) · `.r-row` |
| `cta` text (+ style filled/outline/ghost, size sm) · `link` · `help` · `info` | `.r-cta` · `.r-link` · `.r-help` · `.r-info` |
| `check`/`radio` text (+ on) · `chips`/`tabs` [{label, on}] · `steps` [{label, state}] · `progress` n | `.r-check`/`.r-radio(.on)` · `.r-chips`/`.r-tabs` · `.r-steps` · `.r-progress` |
| `line` [label, value] (+ total) · `item` {name, meta, price} · `plan` {name, price, per, featured, badge, cta, cta_style, features} | `.r-line(.total)` · `.r-item` · `.r-plan` |
| `badge` text (+ style warn/brand) · `banner` · `img` height · `divider` · `gap` px | `.r-badge` · `.r-banner` · `.ph.img` · `.r-divider` · spacer |
| `band` {bg, items [], pad [top, bottom]} · `stack` {items [], gap} | full-bleed region · plain flex column |
| `accordion` {title, open, items []} | a bordered section: the header row with its state sign (`+` closed, `−` open) and the body only when `open` (an open one needs `items`); `edit` {"set": {"open": true}} opens it in B as one change, the sign following the state, `title` rewords the header |
| `fold` · `stage` · `sticky` node (only with a fold) | `.r-fold` · `.r-stage-break` · `.r-sticky` |

Change ops (exactly one; every op carries the ring `label`, `label_pos` above/below): `insert_after` / `insert_before` {target, node} · `replace` {target, node, label_a optional: rings A too} · `remove` {target}: ring on A, B genuinely empty · `move_after` / `move_before` {target, to, label_a, label_b}: ring in both arms · `edit` {target, set {key: value}}: one property of one node. `card.soft` names up to two ids wrapped in `.hl-soft`. Unknown kind, missing target, duplicate id or two changes stop the build; nothing falls back silently.

Example, a quote form on a grey band, header without a line, test = a help line under the ID field:

```json
"screen": [
  {"header": {"logo": true, "icons": [{"icon": "support", "label": "Destek"}, {"icon": "close", "label": "Kapat"}], "line": false}},
  {"h": "Sağlık Sigortası"},
  {"band": {"bg": "#f5f5f5", "items": [
    {"text": "Teklif almak için aşağıdaki bilgileri eksiksiz doldurunuz.", "align": "center"},
    {"field": "Adınız", "id": "adiniz", "fg": "#777879", "border": "#9a9b9d", "radius": 4, "height": 52, "mb": 10},
    {"field": "Soyadınız", "fg": "#777879", "border": "#9a9b9d", "radius": 4, "height": 52, "mb": 10},
    {"field": "T.C. Kimlik Numaranız", "id": "tckn", "fg": "#777879", "border": "#9a9b9d", "radius": 4, "height": 52, "mb": 10},
    {"field": "Cep Telefonu", "fg": "#777879", "border": "#9a9b9d", "radius": 4, "height": 52, "mb": 10},
    {"field": "E-Posta", "id": "eposta", "fg": "#777879", "border": "#9a9b9d", "radius": 4, "height": 52}
  ]}}
],
"change": {"op": "insert_after", "target": "tckn", "node": {"help": "Teklifinizi hazırlamak için bu bilgiye ihtiyaç duyuyoruz."}, "label": "Gerekçe satırı eklendi", "label_pos": "below"}
```

The five placeholders are below the contrast floor on the page itself: they go in `card.inherited_contrast` as today.

## Personal data is never copied

Values typed into fields in a screenshot (name, e-mail, phone, ID or tax number, card number, address, licence plate) are **the user's input, not page state** (rule 15): never carried into the mockup, the JSON or the chat. The field is drawn **empty**, with its label and only a placeholder really on the page (`<div class="r-label">E-posta</div><div class="r-field empty">E-posta adresiniz</div>`). A default the page itself ships (a dropdown that loads with "30-65") is page state and is kept.

**Derived figures are personal too** (`knowledge/methodology.md` → Variable isolation): balances, accumulated amounts, allocation percentages, chart slices, return rates, contributions, contract or policy numbers, plan codes. Keep the structure, drop the values:

- Amounts masked as "••• TL" (the page's currency label), numbers and plan codes as "•••".
- A chart with neutral equal slices and no percentages or legend values; the real proportions never reproduced, in size or color.
- Masks identical in A and B, with no note; `card.brand` never takes a chart's allocation colors.
- A test about such a figure is held, and a sample value the user may share is asked for (rule 19).

The builder refuses values shaped like personal data (an 11-digit TCKN, a TR IBAN, a 16-digit grouped card number, an e-mail address, a 05xx mobile number); masks (“•••”) and all-zero placeholders (“0850 000 00 00”) pass. Any other shape (a name, an address, a balance) is the producer's to drop and the reviewer's to catch.

## Numbers the mockup needs but must not invent

A monthly payment, interest rate, insurance premium, "from X" price or credit cost is a **regulated display** in most markets (rule 11) and personal; a sample figure on a card reads as a real quote.

- **The test is about the number** (a payment preview, an added "from" price): no made-up figure. Hold the scenario, say why in one line and ask for the real figure the page shows (rule 19); a figure the user supplies for this is page state, drawn as given in both arms.
- **The element merely contains one:** draw it without the figure (the label, the layout, a "Teklifinizi görün" line).
- **Computed from the user's figures** (an annual price from the stated monthly price and discount, the amount left to a stated free-shipping threshold): not invented; draw it and say in one chat line how it was derived; a missing input is asked for.
- Shop prices on a shared screenshot are page state, copied as they are, identical in both arms unless the amount is the variable (`numeric_change`).
- **Unverified is not drawn as settled.** Only verified or derived values appear as page text; a representative one is named in the critical assumption. No invented explanatory sentence (a billing line such as "Yıllık olarak faturalandırılır"), and never a new line added to both arms just to show it.

# On demand

## Components

The `.r-*` components in `templates/scenario-card.html` give this realism without inventing markup (CSS only; the template's developer comment has a markup example for each):

| Need | Component |
|---|---|
| Site/app header with logo text, nav links, phone number | `.r-header` (`.filled` = brand color), `.r-logo`, `.r-nav`, `.r-tel` |
| Tabs | `.r-tabs` with `<span class="on">` |
| Form field, dropdown, two fields side by side | `.r-label` + `.r-field` (`.empty`, `.select`), `.r-row` |
| Buttons | `.r-cta` (filled), `.r-cta.outline`, `.r-cta.ghost` (black outline), `.sm` (small) |
| Product/option grid | `.r-grid` (`.c3` for three columns) with `.r-tile` |
| Pricing plan | `.r-plan` (`.featured`), `.r-plan-name`, `.r-plan-price`, `.r-plan-feat` |
| Steps / progress | `.r-steps` (`.done`, `.on`), `.r-progress`; a numbered-circle stepper: Special cases |
| Checkbox / radio | `.r-check`, `.r-radio` (`.on`) |
| Info or helper line | `.r-info`, `.r-help` |
| Chips | `.r-chips` with `.r-chip` (`.on`) |
| Popup / overlay | `.r-overlay` with `.r-modal` (covers the screen) |
| Promo strip in the brand color | `.r-banner` |
| Search with suggestions | `.r-search` + `.r-suggest` |
| Photo background | `.ph.hero` |
| Product row, price lines, badges, stars, divider | `.r-item`/`.r-thumb`/`.r-name`/`.r-meta`/`.r-price`, `.r-line` (`.total`), `.r-old`/`.r-now`/`.r-per`, `.r-badge` (`.warn`, `.brand`), `.r-stars`, `.r-divider` |

## Special cases

- **Steppers.** Ring the single changed step, not the whole bar (unless the bar is the variable), with the label below (`data-pos="below"`) so it covers neither digits nor neighbours. A numbered-circle stepper has no component: draw each step as a small inline-styled circle with the digit inside and the step label under it, never beside it; circles, digits and labels identical in A and B except the tested step.
- **Fold and sticky bar** (`phone`, `phone-web`). A bare `<div class="r-fold"></div>` splits a screen: before it the first view (in the phone), after it the continuation, drawn under the phone as a plain sheet captioned "Kaydırınca görünen kısım"; one arm with a fold means both. A pinned element is `<div class="r-sticky">` around one ring, before the fold: the template pins it to the bottom edge of the first view (light top border, no dark edge or heavy shadow) and pads the first view in both arms, so nothing is hidden. Pinned versus reached by scrolling is a `move`: A keeps the element at the end of the flow in the continuation, B's bar holds the identical element, each label true for its arm:
  A `…<div class="r-fold"></div>…<div class="hl" data-note="Sayfanın sonunda"><div class="r-cta">Ödemeye geç</div></div>`
  B `…<div class="r-sticky"><div class="hl" data-note="Ekranın altında sabit"><div class="r-cta">Ödemeye geç</div></div></div><div class="r-fold"></div>…`
  A pinned label ("sabit", "sticky") on a ring outside an `.r-sticky` is refused; an in-flow grey bar is not a sticky drawing. No `position` in markup: the template places the bar.
- **Stages** (a flow across screens). `<div class="r-stage-break"></div>` splits a screen into 2 stages (one break at most), drawn as small phones left to right with a neutral "→"; `card.stage_captions` gives one short caption per stage (the same in both arms, count = breaks + 1). A move to another step rings the element in its stage in each arm (`card.stage_captions: ["Bilgiler", "Teklif"]`):
  A `<div class="hl" data-note="Telefon ilk adımda"><div class="r-field empty">Telefon numaranız</div></div>…<div class="r-stage-break"></div><div class="r-h">Teklifiniz hazır</div>…`
  B `…<div class="r-stage-break"></div><div class="r-h">Teklifiniz hazır</div>…<div class="hl" data-note="Telefon teklif sonrasında"><div class="r-field empty">Telefon numaranız</div></div>`
  Both arms have the same breaks; no "sonraki adım" text in the screens, only page copy, captions and ring labels.
- **Soft ring** (a consequence the variable forces). `.hl-soft` is a thin dashed outline with an optional outlined `data-note` pill; only beside a `.hl`, at most two per arm, never counted as the variable's ring. An annual-default test rings the toggle and soft-rings the prices: `<div class="hl-soft" data-note="Yıllık fiyatlar">…</div>`. Differences inside are listed as `linked`; a number still needs `numeric_change`.
- **Carousels and dots.** A dot indicator has no component: small inline-styled circles (`<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#111827"></span>` for the active dot, `#d1d5db` for the others), identical in A and B unless the dots are the variable. An auto-advancing carousel's accessibility warning carries a pause.
- **Text buttons.** A plain text button in an app bar ("Atla", "Vazgeç") is a `.r-sub` or `.r-name` span in the screen's own text color (in a flex row identical in both arms when it needs aligning); `.r-link` is only for links the page draws in its link color. An added text button still needs the record's accessibility warning.
- **Modal over a tab screen.** When B adds a modal (`add`), A shows the full underlying screen (status bar, content, tab bar) and B the same screen with an `.r-overlay` whose only content is one ring around `.r-modal` (`<div class="r-overlay"><div class="r-modal hl" data-note="Kayıt penceresi">…</div></div>`, placed as the last child of B's screen; a bare ring around `.r-modal` also builds but draws the modal at content width), the tab bar still drawn beneath the dimming; the overlay is the ringed modal's wrapper, the dimming a linked difference, and the modal is never cut off at the top of the screen. A test inside an existing modal draws the modal over the same screen in both arms and rings the changed element within it. A modal screen is never paired with a different tab: that is two differences.
- **Photo backgrounds.** A hero with a photograph behind it is `.ph.hero`: a dark gradient block with white text on top (`.r-h`, `.r-sub`, `.r-name` turn white inside it). Never dark text on a pale gray "photo" block, never the photo described in words.

## Brand

The brand color is a CSS variable, never hard-coded: `--brand` (fills `.r-cta`, `.r-header.filled`, the active tab, checked boxes, the progress bar), `--on-brand` (text on that fill) and `--brand-name` (an empty `.r-logo` prints it). `card.brand: {"primary": "#c9392b", "on_primary": "#fff", "name": "Brand"}` sets them once: a shared screen's colors, taken silently, or an official guide's, which replaces them for the rest of the session (both rule 12). No note says where the colors came from. Only plain color syntax (hex, `rgb()`, `hsl()`, a color name), and no inline `style="background:…"` override on individual buttons. The ring, the label and the pills never take the brand color.

## Card layout

What the template draws, for reference (the producer only fills the mockups): card 1600 × 900, padding 40px 48px, background `#f4f5f7`, font stack `-apple-system, "Segoe UI", Inter, Roboto, "Helvetica Neue", Arial, sans-serif`. Title 30px / 1.25 / weight 650, `#111827`. Stage: two equal columns with a 48px gap, each a pill above its frame, frames centred and top-aligned. Pills: A and B identical (white, 1px `#d1d5db` border, `#111827` text, 14px / 600, fully rounded); only the text differs, never a winner color. Phone frame: white screen, 1px `#d1d5db` border, radius 36px, soft shadow, 14px status bar; the active tab drawn in `--brand`. Ring label: a `#e11d48` pill with white text, 12.5px / 600, fully rounded.

## Draft and final card

`build_card.py` writes a card in two passes (`knowledge/methodology.md` → Quality gates); only the final or conditional card is delivered.

- **Draft** (`--draft`): needs the scenario-critic stamp matching the current record. It is the final card plus a ribbon, “TASLAK · incelenmedi” / “DRAFT · not reviewed”, over a corner without changing the layout, and the meta tag `<meta name="abtest-status" content="draft">`; it carries no fingerprint. The build prints the draft and manifest paths and the `--stamp` command. A draft is for the mockup reviewer only: on PASS it runs `build_card.py --template … --scenario <record> --stamp <draft.html>`, which writes nothing, refuses a draft or manifest the record no longer builds, and prints the stamp JSON that goes into `review.mockup_reviewer`.
- **Conditional card** (koşullu kart, never called final): a record with at least one critical assumption builds a conditional card, never a final one, with the “KOŞULLU · doğrulama gerekli” / “CONDITIONAL · needs verification” ribbon (small, light amber, top left, never competing with the title) and `<meta name="abtest-status" content="conditional">`, the build summary saying “conditional card (not implementation-ready)”; its draft shows both ribbons (the draft one top right) and its first `abtest-status` says `draft`, and it still needs both stamps. When the user confirms, the assumption leaves the record, which goes back through the critic, a new draft and the mockup review, and only then is the card final, with no ribbon.
- **Manifest** (`<out>.manifest.json`, written with the draft): every difference between A and B inside the rings, one item each. The reviewer confirms each is the declared variable or a labelled linked difference; any other item is a FIX, even when the code found nothing wrong.
- **Final** (no `--draft`): needs both stamps, the critic's matching the record and the mockup reviewer's matching the card about to be written (its bytes, `card.mockup_basis` and the manifest); no draft ribbon or draft meta tags. A refused build writes nothing: a file already at `--out` stays as it was, and the message says so. The build prints the final card's fingerprint; `--check <card.html>` confirms later that a delivered file is byte for byte that reviewed card.

## render_check

`node scripts/render_check.mjs <card.html>` renders a card in headless Chromium (optional: needs Node and Playwright with Chromium); `--shot` writes `card-<name>.png`, `--strict` makes warnings fail too. Errors: the card isn't exactly 1600 × 900 or something overflows it; the title runs over two lines; frame, stage-phone or continuation content is clipped, or a continuation sheet isn't its screen's width; a phone frame shows more than 24px of blank screen; a ring label overlaps anything outside its ring or sits under 6px from what it faces (the gap is reported), or a ring overlaps text or painted elements outside it; a ring too wide (Tight ring); an `.r-sticky` not touching the bottom of its screen, or a pinned label outside one; pills that differ in anything but text; text below 12px or below 4.5:1 contrast (3:1 for large text); A and B frames not top-aligned or not the same width. Warnings (errors in `--strict`): a short single phone that a larger `phone_scale` would fill; a frame using under 40% of the stage height or (web) under 45% of the column width. It can't judge meaning (a gap lost inside a ring wrapper, a label on a 1px line, a label false for its arm); the mockup reviewer reads its output and checks those.
