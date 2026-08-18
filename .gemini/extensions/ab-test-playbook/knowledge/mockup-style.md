# Visual Language — Scenario Card and Mockup Rules

`ab-test-card` and `templates/scenario-card.html` follow this spec. Source: the archive's visual deck (an internal design reference kept outside the repo — no visual files are added to the repo).

## Neutral palette

Without a brand guide (rule 12c), the card is produced with these colors: the three boxes' identity colors are teal `#08616b`, amber `#6b3804`, navy `#17086b` (header strips); the primary CTA inside the mockup is the template's default orange (`#ff6a00`); the changed-element ring is red (`#e62d37`). This palette is deliberately brand-neutral.

## Card layout

- A horizontal card, two regions: **the mockup pair on the left**, **the text column on the right**.
- The mockup pair: `Variant A` (control) on the left, `Variant B` (test) on the right. Both carry a green pill label above them (`Variant A` / `Variant B`).
- The right column: a question-form title at the top (bold, ~2 lines), a 2-3 sentence description below it, the three boxes below that.

## The three boxes' style

Each box: a colored gradient header strip + a white body card.

| Box | Header strip | Header text color |
|---|---|---|
| Test edilmesi gerekenler ("What to test") | Cyan/turquoise gradient | Dark teal `#08616b` |
| Takip edilecek ana KPI'lar ("Primary KPIs to track") | Yellow/amber gradient | Dark brown `#6b3804` |
| Yapılmaması gerekenler ("Never do") | Purple/lilac gradient | Dark navy `#17086b` |

- Header: bold, ~20px equivalent.
- Body: a bulleted list, each item's `Label:` part **bold**, the rest normal; text color black at ~60% opacity.
- Boxes carry a light shadow, rounded corners (radius ~17), a soft/dashed-edge feel.

## Realism level

The mockup is produced **fully realistic**: text, prices, labels, and layout are all real. Gray placeholder boxes stand in only for **a photo** (a product image, an avatar); never used in place of text. Filler phrases like "Heading," "Lorem ipsum," "Text field" aren't accepted.

**What "realistic" means: the user's own page, not a made-up one.** This distinction is the card's single most critical rule.

- **If the user shared a page (screenshot, URL, or flow):** the mockup is a redraw of that page. Product name, price, button copy, field labels, section order, menu items — whatever's on screen is what gets written. Variant A is exactly the on-screen state (CLAUDE.md rule 15): it isn't redesigned, simplified, made "better," or completed. Variant B differs from A in exactly one element. Building an e-commerce page from your own head and fitting the test onto it isn't realism, it's fabrication, and it's a rule-15 violation.
- **If a detail can't be read from the screenshot** (cut-off text, a hidden section), don't make it up: either leave that part out of the mockup entirely, or ask the user. Filling the gap with plausible-looking content misrepresents the user's page.
- **If there's no shared page in the picture** (a generic scenario from the archive, `ab-test-suggest` output): a representative example is built, but this is made clear on the card — the example content isn't presented as if it were a real customer's page.

Reasoning: the card is most often shown to whoever will run or approve the test; what's being tested can only be discussed properly when the screen is presented exactly as it really looks. A half-realistic mockup shifts the discussion from the test itself to the mockup's shortcomings.

There's a known cost to this, and whoever presents the card should know it: **a design that looks finished suppresses the viewer's structural objection.** People tend to comment at the color and wording level on a screen that looks complete, rather than saying "this flow is built wrong." This risk isn't addressed by simplifying the mockup, but by two things:

- The changed element is marked with a ring, and the ring's label states what changed; so attention goes to the tested variable, not a cosmetic detail.
- The card's text column (the three boxes) is always presented together with the mockup; what gets discussed is the questions there, not the mockup itself.

The `.r-*` components inside `templates/scenario-card.html` (a product row, a form field, a price line, a CTA, a badge, stars) are ready to produce this level; markup isn't invented from scratch on every card.

## Mockup rules

- **Only the tested element** differs between the two variants. Product name, price, rating, badge — all of it stays exactly the same.
- The tested difference is highlighted with a **red rounded-corner outline** (thickness ~3px, radius ~12, a slight glow). The outline is drawn only around the changed element, it doesn't cover the whole screen.
- **The outline carries a label.** A short label above the ring states what changed (`.hl[data-note]`, e.g. "coupon field collapsed," "delivery date added"). An unlabeled ring forces the reader to compare the two screens and find the difference themselves; the card's job is to state that difference. The label doesn't exceed two or three words.
- If a new element is being added (present in B, absent in A), the outline is drawn on the new element in B; no outline is placed on A.
- **If an element is being removed (present in A, absent in B), the outline is drawn on the element in A, and that area is genuinely left empty in B.** A dashed placeholder saying "this element isn't shown" or "removed" isn't put there — a placeholder both reads like a permanent rule and misrepresents the variant: in the real B, that area doesn't exist, and the content below it shifts up naturally. This shift is preserved in the mockup, because it's often part of the test's benefit (the real content moves higher on the screen). To make the shift noticeable, a one-line note is dropped **below** the mockup (`.shift-note`, e.g. "coupon field removed, the content below shifted up"); this note isn't written inside the screen itself.
- Mobile mockup: inside a phone frame, with a status bar (clock + battery) and bottom navigation (Home/Discover/Favorites/Cart/Profile).
- Web/desktop mockup: inside a browser frame — three dots and an address bar in the top bar (the template's `.browser`/`.browser-bar`/`.browser-url`), a white body. The status bar and bottom nav belong only to the mobile frame, they aren't used on a web card.
- Copy language and currency follow the user's page (rules 7 and 15): an English/USD page isn't translated into Turkish/TRY. If there's no shared page (a representative example), Turkish and TRY are assumed by default. Amounts are always identical between the two variants.

## Typography

- Primary font: Inter (headings Bold/Semi Bold, body Regular).
- Full support for Turkish characters is required; character drops like "Baslık," "İndrim" aren't accepted.
- Quotes are curly ("…" and '), straight quotes aren't used.
