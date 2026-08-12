# Example output

`abtest-card-kupon-alani.html` is a real, unmodified render of an archived scenario ([`knowledge/scenarios/cart-checkout.md`](../knowledge/scenarios/cart-checkout.md) → "Açık kupon kodu alanı sepet terkini artırır mı?") through [`templates/scenario-card.html`](../templates/scenario-card.html) — this is what `abtest card` (and, automatically, every `abtest suggest`/`abtest design` run, per `CLAUDE.md` kural 9) writes to your working directory. Open it directly in a browser; it's a single self-contained file, no build step.

## What the chat side looks like for the same scenario

Per kural 9, the three boxes only live in the card above — the chat only carries this:

> **Açık kupon kodu alanı sepet terkini artırır mı?**
> Kanıt: arşiv emsali — kupon kutusunun görünürlüğü bu bağlamda daha önce test edilmiş bir desen.
> → `abtest-card-kupon-alani.html`

That's the whole exchange. No duplicate three-box text, no "should I generate the card?" round-trip — the file is already on disk by the time this line appears.
