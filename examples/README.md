# Examples

One scenario, carried end to end: from the question a user asks, through the
scenario definition, to the rendered card — plus what the chat side actually
looks like while that happens.

| File | What it is |
|---|---|
| `scenario.json` | **The canonical example: one JSON per scenario.** It validates against [`templates/scenario.schema.json`](../templates/scenario.schema.json) and the card builder renders it directly. One variable, two variants, one primary KPI listed first, two guardrails, a stated evidence level, the footer tags (source, objection, ICE tier), and the optional `preregistration` block — the decisions fixed before launch (primary KPI and direction, guardrail margins, alpha, power, alternative, allocation, planned sample, decision rule, pre-declared segments), shaped to map onto the experiment-configuration fields common testing platforms ask for. Its `card` object is the visual layer: the two mockup bodies, the difference type (`change`), the device frame (`phone-web`), the address-bar domain and the mockup basis (`representative`, so the footer says it's a representative example). |
| `scenario-card-input.json` | The legacy flat card input (`desc`, `kpi_items`, `variant_a`, … at the top level), kept so older inputs keep building. New cards use `scenario.json`'s shape. |
| [`../docs/demo/scenario-card.html`](../docs/demo/scenario-card.html) | A rendered card, served as the zero-install demo. |
| [`results-walkthrough.md`](results-walkthrough.md) | A finished test read end to end with real script output: SRM check, significance, continuous metric with CUPED, guardrail margin, decision and the history row. |
| [`audit-example.md`](audit-example.md) | A flawed test plan audited against the checklist, including a segment interaction check. |

## Reproducing the card

```bash
python3 scripts/build_card.py \
  --template templates/scenario-card.html \
  --scenario examples/scenario.json \
  --out /tmp/card.html
```

And validating the same file:

```bash
python3 scripts/validate_scenario_json.py examples/scenario.json            # Turkish messages
python3 scripts/validate_scenario_json.py --lang en examples/scenario.json  # English messages
```

`ab-test-design` validates its bare pre-registration block on its own with
`--prereg-only` (a file holding just `{"preregistration": {...}}`).

To see the card the way a reader does, render it in headless Chromium (needs a
local Playwright install; not part of the unit suite):

```bash
NODE_PATH=/path/to/node_modules node scripts/render_check.mjs --shot /tmp/card.html
```

It prints the card size and text-column width, and flags horizontal overflow,
mockup content clipped by the frame and ring labels covering text.

Validation and the card build run in CI on every push, so a change to the
template or the schema that would break a real card fails the build rather than
surfacing later as a quietly malformed deliverable.

## What the chat side looks like

The card holds the full content of the three boxes. Chat deliberately does not
repeat it (CLAUDE.md rule 9) — a scenario costs four lines in the conversation,
not forty:

> **Açık kupon kodu alanı sepet terkini artırır mı?**
> Kaynak: arşivden · Kanıt: arşiv emsali (bu sayfanın kendi verisiyle doğrulanmadı)
> Mekanizma: açık kutu, kodu olmayan kullanıcıya eksik bir şey olduğunu hatırlatıp kod aramaya gönderiyor; bağlantı arkasındaki alan bunu yapmıyor.
> `abtest-card-kupon-alani.html`

Everything else — what to test, which KPI decides, what would invalidate the
test — is in the card. That split is the reason the workflow stays usable when a
turn produces four or five scenarios at once: chat stays scannable, and the
detail lives where it can be read side by side with the mockups.

## What is deliberately not here

A finished visual deck. The archive is methodology and text content; the cards
are generated per scenario against whatever brand you are working in, so a
shipped deck would be a picture of someone else's brand rather than a template
you can use. The demo card uses the neutral palette from
[`knowledge/mockup-style.md`](../knowledge/mockup-style.md) for exactly this
reason.
