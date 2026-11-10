# Examples

Sample scenarios carried end to end: from the question a user asks, through the
compact scenario record, to the rendered card, plus what the chat side actually
looks like while that happens.

| File | What it is |
|---|---|
| `scenario.json` | **The canonical example: one compact scenario record.** It validates against [`templates/scenario.schema.json`](../templates/scenario.schema.json) and the card builder renders it. Field by field: `title` is the question the test answers (does moving the coupon field behind an “İndirim kodum var” link increase orders?); `problem` names the obstacle on the cart page (an open coupon box sends shoppers without a code off to look for one); `mechanism` is the one sentence on why B changes that; `variable` is the coupon field's visibility; `variants` holds A (the open box) and B (the field behind the link), with `difference: "change"`. `source` is `adapted`, with `adapted_from` naming the archive scenario (“Açık kupon kodu alanı sepet terkini artırır mı?”), whose `Değişken` and `Fark` the record keeps. `primary_kpi` is “Dönüşüm Oranı (CR)” over visitors assigned when they reach the cart page (the same trigger in both arms), direction increase: the change sits before checkout, so it affects reaching checkout and a checkout-based completion rate would hide that. Revenue is deliberately not the primary: hiding a coupon field can raise revenue by making code holders pay full price, and that harm must never read as a win (`knowledge/methodology.md` → KPI rules). `guardrail` is that harm: “Kuponlu Sipariş Oranı” per assigned visitor, must not decrease (a per-order coupon rate would fall mechanically when B adds orders without codes). `invariants` lists the three functions that work identically in both arms: the apply step for a valid code, the discount calculation and totals, and the message for an invalid or expired code. `warnings` holds one `accessibility` item for the new link with its criteria: keyboard reachable, a screen-reader name “İndirim kodum var”, it opens the field and moves focus there, a touch target of at least 44×44 pt, text contrast of at least 4.5:1. `evidence` is `archive` (shown as “Arşiv örüntüsü”), with the note that it rests on an archive pattern and wasn't tested on this page. `priority` holds the tier (medium) and a one-sentence rationale weighing impact, evidence and ease without claiming the idea worked anywhere (the chat tag line prints the tier only). `review` holds the two PASS stamps, each with the fingerprint of what was reviewed (Reproducing the card, below). Optional context (`stage`, `lang`, `device`, `market`, `objection`) sits alongside; A variable tested before would be stated in chat from the user's `.abtest-history.md`; the record carries no history field. `detail` is optional and absent here: it holds the three boxes (`test_items`, `kpis`, `dont_items`, 3 to 6 items each; exactly five is the archive's rule and applies to `knowledge/scenarios/` only) and is filled only when the user asks for the detailed view. None of these fields is printed on the card: the card shows only the title, the two mockups, the ring and its label ([`mockup-style.md`](../knowledge/mockup-style.md) → The card), and `detail`, when present, is given in chat. Its `card` object is the visual layer: the two mockup bodies, the difference type (`change`), the device frame (`phone-web`), the address-bar domain and the mockup basis (`representative`, metadata for the mockup reviewer, never printed). On a native app screen (`phone`), `card.bottom_nav` lists the real tab labels and `card.bottom_nav_active` marks the active one. |
| The other sample records | Each a real scenario on a different screen type (a desktop product page, a native app screen with its tab bar, a form or SaaS page), built through the same pipeline as `scenario.json`: validator, scenario-critic, draft, mockup-reviewer, final. |
| [`../docs/demo/`](../docs/demo/) | The sample cards: each record's final card and its PNG. One of them is served as the zero-install demo. |
| [`audit-example.md`](audit-example.md) | A flawed test plan audited against the checklist: isolation, denominators, guardrails, segments named in advance, and the one line a plan's statistical claims get. |

## Reproducing the card

A card is built in two passes, and the final one only builds when both reviews
have stamped the record ([`knowledge/methodology.md`](../knowledge/methodology.md) → Quality gates).

```bash
# 1. Validate the record and print its fingerprint (refuses on any error)
python3 scripts/validate_scenario_json.py --fingerprint examples/scenario.json

# 2. Draft: needs the scenario-critic stamp matching that fingerprint.
#    Writes the card with a "DRAFT · not reviewed" banner and the inside-ring
#    manifest next to it (<out>.manifest.json); the draft has no fingerprint
python3 scripts/build_card.py --draft \
  --template templates/scenario-card.html \
  --scenario examples/scenario.json \
  --out /tmp/card.draft.html

# 3. Mockup stamp (mockup-reviewer only, after its PASS): prints the JSON for
#    review.mockup_reviewer; writes nothing, refuses a stale draft or manifest
python3 scripts/build_card.py \
  --template templates/scenario-card.html \
  --scenario examples/scenario.json \
  --stamp /tmp/card.draft.html

# 4. Final: needs both stamps; otherwise nothing is written. Prints the final
#    card's fingerprint
python3 scripts/build_card.py \
  --template templates/scenario-card.html \
  --scenario examples/scenario.json \
  --out /tmp/card.html

# 5. Later: is a delivered file still byte for byte the reviewed card?
python3 scripts/build_card.py \
  --template templates/scenario-card.html \
  --scenario examples/scenario.json \
  --check /tmp/card.html
```

In a session the stamps are written by the pipeline: scenario-critic's PASS
carries the fingerprint from step 1 into `review.scenario_critic`, and
mockup-reviewer, after its PASS on the draft and its manifest, runs step 3
and the JSON it prints goes into `review.mockup_reviewer`. Edit the record after
that and step 1 prints a different fingerprint, so the final build refuses
until the record is reviewed again; edit only the mockup and the critic's stamp
still holds, but the mockup reviewer's no longer matches the card. A refused
build names the gate that failed and leaves an existing `--out` file as it was.

Validating the same file:

```bash
python3 scripts/validate_scenario_json.py examples/scenario.json            # Turkish messages
python3 scripts/validate_scenario_json.py --lang en examples/scenario.json  # English messages
python3 scripts/validate_scenario_json.py --strict examples/scenario.json   # warnings fail too
```

Anything that decides whether a record may reach a card is an error with its
reason: a revenue primary on this coupon change without the coupon guardrail, a
missing `invariants`, the new link without its accessibility criteria, an
`adapted_from` that isn't an archive title, "tested" or "proven" wording on
archive evidence. Only soft wording problems are warnings (a title without "?",
a second sentence in `problem` or `mechanism`); `--strict` turns them into
failures.

To see the card the way a reader does, render it in headless Chromium (needs a
local Playwright install; not part of the unit suite):

```bash
NODE_PATH=/path/to/node_modules node scripts/render_check.mjs --shot /tmp/card.html
```

It fails on a card that isn't 1600 × 900, a title over two lines, frame
content that is clipped, a blank phone screen, a ring or label covering screen
elements, text below 12px or contrast below 4.5:1, and A and B frames that
aren't top-aligned or the same width; it warns on a frame too small for its
stage (`--strict` makes that fail too). `--shot` writes a PNG.

Validation and the card build run in CI on every push, so a change to the
template or the schema that would break a real card fails the build rather than
surfacing later as a quietly malformed deliverable.

## What the chat side looks like

The record lives in the JSON. Chat deliberately does not repeat it, and neither
does the card (CLAUDE.md rule 9): a scenario costs two lines in the
conversation, not forty:

> **1. Kupon alanını “İndirim kodum var” bağlantısının arkasına almak siparişi artırır mı?**
> Öncelik: Orta · Kaynak: arşivden uyarlandı · Kanıt: arşiv örüntüsü · `abtest-card-kupon-alani.html`

Everything else (the problem, the mechanism, the primary KPI, the guardrail and
the accessibility warning) stays in the JSON; the card named there shows the
question and the two mockups with the change ringed, and it is always the final
build, never the draft. A weak test the user asked for gets one more line, under
its tag line, starting “Daha güçlü alternatif:”. The three boxes come only when
the user asks for them (“1. öneriyi detaylandır”): the producing skill fills
`detail`, has the record reviewed again and gives the boxes and the reasoning in
chat; the card doesn't change. That split is the reason the workflow stays
usable when a turn produces three scenarios at once: chat stays scannable, each
card is a picture of one change, and the detail is a request away.

## What is deliberately not here

A finished visual deck. The archive is methodology and text content; the cards
are generated per scenario against whatever brand you are working in, so a
shipped deck would be a picture of someone else's brand rather than a template
you can use. The coupon demo card uses the neutral palette from
[`knowledge/mockup-style.md`](../knowledge/mockup-style.md) for exactly this
reason.
