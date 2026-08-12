# Examples

One scenario, carried end to end: from the question a user asks, through the
scenario definition, to the rendered card — plus what the chat side actually
looks like while that happens.

| File | What it is |
|---|---|
| `scenario.json` | The portable test definition, valid against [`templates/scenario.schema.json`](../templates/scenario.schema.json). This is the machine-facing artifact: one variable, two variants, one primary KPI, two guardrails, a stated evidence level. |
| `scenario-card-input.json` | The card-rendering input for the same scenario — the three boxes plus the two mockup bodies. Consumed by `scripts/build_card.py`. |
| [`../docs/demo/scenario-card.html`](../docs/demo/scenario-card.html) | The rendered card, built from that input. Also served as the zero-install demo. |

## Reproducing the card

```bash
python3 scripts/build_card.py \
  --template templates/scenario-card.html \
  --scenario examples/scenario-card-input.json \
  --out /tmp/card.html
```

And validating the test definition:

```bash
python3 scripts/validate_scenario_json.py examples/scenario.json
```

Both run in CI on every push, so a change to the template or the schema that
would break a real card fails the build rather than surfacing later as a
quietly malformed deliverable.

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
