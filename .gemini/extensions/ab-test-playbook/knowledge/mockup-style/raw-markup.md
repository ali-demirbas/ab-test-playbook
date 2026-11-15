# Raw markup

Read only when a card uses raw `card.variant_a` / `card.variant_b` markup, for what the node list can't express (the core: `knowledge/mockup-style.md`). The mockup reviewer also uses it for the ring markup it checks.

## The raw form

`card.variant_a` / `card.variant_b` hold the mockup bodies as HTML from the template's `.r-*` components at their rendered size (`templates/scenario-card.html`; its developer comment has a markup example for every `.r-*` component): `variant_a` byte for byte the same across a shared screen, each `variant_b` that A with its one change. Never alongside `card.screen` / `card.change`: the build refuses both forms at once. Real copy, prices, labels and layout, no filler; components at component scale, no invented markup, inline colors or `zoom`/`transform`; `.ph` only for a photo. Text fields of the record are plain text, never pre-escaped (the script escapes them), but `<`, `>` and `&` in user text placed inside `variant_a` / `variant_b` are escaped by hand.

**Allowlist (rule 18):** only the template's component tags (`div span p b strong i em u s small sup sub br hr ul ol li`) and `class`, `style`, `data-note`, `data-pos`, `title`, `role`, `aria-*`, double-quoted; no comments, links, images, scripts, event handlers, `url(`, a CSS import rule or `position:fixed`. A build warning (`build_card: warning: …`) is read, not ignored. No "hidden / removed" placeholder where a removed element was.

## Component scale

Phone base 15px, web base 16px (desktop text stays readable when the card is shown at half size); headings 19-22px / 600; meta and help text 13-14px; nothing below 12px as rendered. CTA 15px / 600 and fields at least 44px tall on phone.

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
| Steps / progress | `.r-steps` (`.done`, `.on`), `.r-progress`; a numbered-circle stepper: `special-cases.md` |
| Checkbox / radio | `.r-check`, `.r-radio` (`.on`) |
| Info or helper line | `.r-info`, `.r-help` |
| Chips | `.r-chips` with `.r-chip` (`.on`) |
| Popup / overlay | `.r-overlay` with `.r-modal` (covers the screen) |
| Promo strip in the brand color | `.r-banner` |
| Search with suggestions | `.r-search` + `.r-suggest` |
| Photo background | `.ph.hero` |
| Product row, price lines, badges, stars, divider | `.r-item`/`.r-thumb`/`.r-name`/`.r-meta`/`.r-price`, `.r-line` (`.total`), `.r-old`/`.r-now`/`.r-per`, `.r-badge` (`.warn`, `.brand`), `.r-stars`, `.r-divider` |
| Desktop pieces | `.r-logos` (`.r-logos-cap`, `.r-logos-row`), `.r-amount` with `.r-big`, `.r-rating`, `.r-cols` (`.c3`, `.c4`), `.r-plan-note` |

What the node list compiles to, beyond the core's table: `header` → `.r-header` with `.r-logo` / `.r-nav` / `.r-tel` and icons as `role="img"`; `logos` a grey wordmark strip (`.r-logos`); `price` `.r-amount` with the old price struck through; `stars` `.r-rating`, rounded half up, the value as written; `cols` `.r-cols`, equal top-aligned columns; `field` `.r-field` (`.empty`, `.select`); an aligned `link` at its own width, the ring too; `plan` `.r-plan`, `old` struck through before the price, `note` a line under it; `img` `.ph.img`; a centred `stack` keeps each child at its own width; an accordion `edit` with `title` rewords the header. On `web` a button that is a direct child of the page takes its own width (at least 168px), and a header that ends with its nav sets it right.

## Ring and label in markup

- **Ring:** `outline: 3px solid #e11d48; outline-offset: 4px; border-radius: 10px;` no glow, no fill; an outline takes no space, so a ringed element sits where its twin sits in the other arm. The `.hl` wrapper has no margin, padding, border, background or `style` of its own (the builder refuses inline margin or padding); a ringed component's own style (`class="r-card hl" style="max-width:320px"`) is identical in A and B.
- **Spacing parity.** A bare `.hl` around several siblings of a gap container (`.screen`, `.browser-screen`, `.r-card`, `.r-modal`, a flex row) removes their gap, and in a `.r-row` it takes the element's flex sizing. Ring one element, or wrap the siblings in the same plain container in both arms (`<div style="display:flex;flex-direction:column;gap:16px">`).
- **Room, nothing covered.** The ring crosses no neighbour; the room comes from the mockup's own spacing, the same in A and B: at least 8px around a ringed element (the outline takes 7px), about 31px free above it when the label sits on top (label 25px plus a 6px gap; a margin-bottom on the element above or a plain outer wrapper, identical in both arms, never inside `.hl`), the label at least 6px clear of anything and never on a line (a header's bottom border, a divider, a tab underline, a field border).
- **Label:** `.hl[data-note]`, two to four words saying what changed ("Kupon alanı bağlantıda"; a Turkish label starts with a capital, or the builder refuses it); a 14px pill outside the ring. The builder places it: first where the author asked (`data-pos`, `card.note_pos` or the spec's `label_pos`; top right when nothing is said), and when that would cover something or leave the screen, at the ring's left edge or on the other side. The room the label needs (34px outside the ring, on the label's side) comes from the template, so no spacer or margin is written for it. A label wider than the screen fits nowhere and is refused: shorten it.
- **Where rings go** (the record's `difference`; `card.difference`, when present, equals it; the builder refuses a card that breaks this): **change** (değiştir) the changed element in B, its old state in A optional; **add** (ekle) only B; **move** (taşı) the same element in both arms, old place in A and new place in B, identical copy, size and style, each arm's label true for that arm ("Telefon ilk adımda" / "Telefon teklif sonrasında"), a gap or shift it causes being a linked difference the label names (below the fold, pinned or to another step: `special-cases.md`); **remove** (kaldır) the element in A, labelled as a removal ("Kupon alanı kaldırıldı"), B genuinely empty there (no "removed" placeholder; the content below shifts up). One change on N repeated elements gets **one ring around the group**, never N rings.
- **Tight ring.** Ring the variable itself, never the section around it; render_check refuses a `.hl` over 45% of its screen, or wider than 85% and taller than 40%. What the variable forces elsewhere gets a soft ring (`special-cases.md`).
- **Only the tested element differs.** The builder diffs A and B: a difference outside the rings refuses the card; every one inside goes into the manifest.
  - **Numbers** (price, amount, percentage, count, rating) are identical unless the number is the variable and `numeric_change` explains it (a price test), still inside a ring.
  - **Linked differences** the variable forces (an annual default shows annual prices; a removed field shortens the form) are drawn and named: the ring on the variable (the toggle), a `.hl-soft` on the consequence (the prices); a change it doesn't force is a second variable.
  - **Inline colors are page state:** a color only B has (a brand-colored bullet) is a second variable unless it is the variable. A colour the page itself has (a grey form band, a tinted section) is drawn with the same inline style in both arms; leaving it out makes A a different page, which is the error. A page text colour under the contrast floor is kept and documented in `card.inherited_contrast` (shared page, identical in both arms, outside the rings); an icon glyph carries `role="img"` and is held to 3:1.
  - **Legal, security and consent displays stay as A shows them.** Legal or mandatory text in A (KVKK, aydınlatma, cayma, faiz, toplam maliyet, yıllık maliyet, sözleşme, terms, privacy, APR) missing in B refuses the card and holds the scenario (rule 11); so does verification or security text (doğrulama, SMS kodu, CAPTCHA, şifre, iki adımlı, verification code, password) missing in B, or a consent box ticked only in B (rule 6).
  - **An added interactive component** (`.r-cta`, `.r-link`, `.r-field`, `.r-check`, `.r-radio`, `.r-chip`, `.r-tabs`, `.r-search`, `.r-overlay`, `.r-modal`, or more of one than A) needs the record's `accessibility` warning with the fitting criteria (44×44 pt / 48×48 dp target, 4.5:1 contrast, keyboard, screen-reader name; a modal also focus and close with a visible control and Esc; an auto-advancing carousel a pause; `knowledge/methodology.md` → Accessibility checks), or the card is refused. A tiny target or low-contrast text drawn in B is a reviewer FIX.

## Brand variables

The brand color is a CSS variable, never hard-coded: `--brand` (fills `.r-cta`, `.r-header.filled`, the active tab, checked boxes, the progress bar), `--on-brand` (text on that fill) and `--brand-name` (an empty `.r-logo` prints it). `card.brand: {"primary": "#c9392b", "on_primary": "#fff", "name": "Brand"}` sets them once: a shared screen's colors, taken silently, or an official guide's, which replaces them for the rest of the session (both rule 12). No note says where the colors came from. Only plain color syntax (hex, `rgb()`, `hsl()`, a color name), and no inline `style="background:…"` override on individual buttons. The ring, the label and the pills never take the brand color.
