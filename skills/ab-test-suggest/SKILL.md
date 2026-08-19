---
name: ab-test-suggest
description: Suggest proven A/B test scenarios for a given page or journey stage, ranked by ICE. Use when the user asks "what should I test", "what should I A/B test on my checkout / cart / product page / pricing page / homepage", "give me A/B test ideas", "experiment ideas", "split test ideas", "CRO ideas", "which tests should I run first", "what tests are worth running", "test öner", "hangi testleri yapmalıyım", "checkout için hangi testler", "anasayfam için test fikirleri", "ne test edeyim". Picks matching scenarios from the curated archive in knowledge/scenarios/ (e-commerce, mobile app, SaaS/B2B, search and filtering, forms, pricing) and delivers each as an HTML card via ab-test-card. For a test designed specifically for a page or screenshot you share, see ab-test-design. To review a plan you already have, see ab-test-audit.
metadata:
  version: 0.1.0
  category: recommend
  updated: 2026-08-17
---

# ab-test-suggest — Archive Test Suggestions

> **Language:** Output always matches the language you write in (CLAUDE.md rule 7).

`${CLAUDE_PLUGIN_ROOT}/CLAUDE.md` rules are binding.

## Flow

1. Take the context from the router (sector, page). **Traffic, test tool and setup info are not asked** (CLAUDE.md rules 5 and 13): they aren't required to produce a scenario, and aren't put in front of the output as "missing." They're only requested when the user asks about duration, sample size or significance. If sector or page is still unclear, pick the closest stage and state the assumption in one sentence — don't ask a question and stall the flow.
   - **Read the test memory (CLAUDE.md rule 16).** Check whether `.abtest-history.md` exists in the user's working directory. If it does, read it and pull the records for the target page. If not, don't narrate that a search happened, just continue silently; at the end of the output, suggest once: "If you keep test history as `.abtest-history.md`, I can filter suggestions against past results."
2. Map the page/flow to a journey stage and read the matching file:
   - Homepage, landing, campaign page → `knowledge/scenarios/home-landing.md`
   - Search, filter, results page → `knowledge/scenarios/search-filtering.md`
   - Menu and in-site navigation → `knowledge/scenarios/search-filtering.md`
   - Category/listing page → `knowledge/scenarios/category-listing.md`
   - Product detail → `knowledge/scenarios/product-detail.md`
   - Cart, coupon, checkout, address → `knowledge/scenarios/cart-checkout.md`
   - Order confirmation / thank-you page (post-purchase, post-signup) → `knowledge/scenarios/thank-you.md`
   - Logged-in, recurring-use home screen (not first-open, not the marketing homepage) → `knowledge/scenarios/dashboard.md`
   - Form, signup, login → `knowledge/scenarios/forms-signup.md`
   - Pricing page, price display, plan comparison → `knowledge/scenarios/pricing.md`
   - App onboarding/permissions/home → `knowledge/scenarios/mobile-app.md`
   - SaaS commercial decisions (plan default, trial length, paywall) → `knowledge/scenarios/saas-b2b.md`
   - Page-independent elements like buttons, links, icons → `knowledge/scenarios/ui-elements.md` (a lower tier: it isn't put first while a stronger candidate from a higher tier exists, but a scenario with a strong mechanism resting on an observable page obstacle is still suggested — `methodology.md` → impact ranking. Don't suggest from this file if traffic is known to be low; don't assume it if unknown.)
   - If multiple stages are requested, read all the relevant files. **On any page with a form, also read `forms-signup.md`**: the checkout address form, a lead form and a signup screen live in the context file, but scenarios about the form's own design (label position, field order, input method) live only there.
   - **Diagnose the funnel.** If the user has said where the loss is happening (rule 13's problem question answers this), first separate two things: a **clogged vein** — a high-traffic, low-conversion step (even a small improvement here affects many users, so it's the priority) and a **missing link** — a step the funnel should have but doesn't at all (e.g. no delivery date shown at all in cart). They carry different priority: for a clogged vein, improve the existing step; for a missing link, add a new element (methodology.md → variable isolation, the "addition" axis).
3. Pick 2-5 scenarios that fit the user's context. Drop any that don't fit, with the reason (e.g. don't suggest a return-rate-primary test on a low-traffic page). If there are more than 5 strong candidates, don't produce them all without asking — step 6's rule applies.
   - **Compare against history.** If a scenario has already tested the same variable on the same page before:
     - **won** → don't suggest it again; instead suggest the next step to build on the winning change.
     - **lost / no difference** → no automatic elimination (rule 16: history isn't a veto). First look for a reason that justifies retrying: has the page changed since that test, is a different segment/market being asked about, has a long time passed, was the earlier run underpowered. If there's a reason, suggest it with the reason: "This lost in March, but the card design changed after that test." If there's no reason, choose not to include it this round and say so in one sentence — don't drop it silently.
     - **inconclusive / invalid** → this isn't a result; suggest the scenario normally and note "tried before but couldn't be measured."
   - If the same page keeps getting "no difference" in a row, stop suggesting small variations; suggest a more structural change and say why (methodology.md → local-maximum risk).
   - A history record also changes a scenario's confidence level: a pattern that won on the user's own product becomes `Evidence: user's own data`.
   - **Reuse the "generalizable pattern" column for other pages too.** If a row has that column filled in (e.g. "a progress indicator strengthens spending behavior") and the page being suggested for fits the same mechanism, suggest it as a separate scenario with the reason stated: "[The same mechanism] won on [page X], it may work here too." Don't assume it automatically — it's still set up as a separate, single-variable test.
4. **Pass it through the lens, then rank with ICE (`methodology.md` → idea-generation lens).** Candidates picked from the archive go through two filters before ICE: (a) **mechanism duplication** — don't present two scenarios in the same page area resting on the same behavioral mechanism as separate suggestions; merge them or pick the stronger one; (b) **impact ranking** — among candidates that pass the gate, offer/flow/decision-moment information or information architecture comes first, then hierarchy and objection-answering copy, then color and generic CTA wording comes last. This isn't a ban: a third-tier candidate with a strong mechanism is still suggested. Test memory only overrides this ranking for the **same component or same mechanism**, not the whole tier.
5. Rank with ICE: Impact × Confidence × Ease. The scoring scale and tie-break order are in `knowledge/methodology.md` → Prioritization (ICE); produce the same ranking for the same input. Write a one-sentence ICE rationale next to each suggestion.
6. **Review (CLAUDE.md rule 17).** Before rendering the selected scenarios as cards, hand them to `agents/scenario-critic`. Fix any item that comes back `FIX` and re-review; don't produce a scenario that comes back `RET`, and tell the user the reason for the drop in one sentence. Don't dump the review report into the chat (rule 9). Archive scenarios are reviewed too — being in the archive doesn't prove it's valid for this page (market dependency, staleness, test memory).
7. If the brand-guide question hasn't been asked this session, ask it first (rule 12). Then turn every scenario that passed review (2-5 of them) directly into HTML via `ab-test-card` (CLAUDE.md rule 9) — the full content of the three boxes lives only in the card, it isn't also written to chat as text.

## Output format

Only a short header per scenario stays in the chat (not the three boxes — those live in the card):

```
## <Title as a question>  (from archive · ICE: High — <one-sentence reason> · Evidence: <user's own data / archive precedent / industry observation / intuition>)
<one-sentence mechanism> → `abtest-card-<slug>.html`
```

If there are more than 5 strong candidates, don't produce them all without asking: say how many there are and ask whether to continue — this is rule 13's one exception (CLAUDE.md rule 9).

At the end of the list, if the confidence of the suggestion set is weak, say so in one sentence — don't present it as strong silently. Sources of weakness: the user shared no data at all, there's no close archive precedent for this context, the sector/page info stayed coarse, traffic is unknown. Example: "These suggestions are based on page type alone; your own funnel data could change the ranking."

## Never do

- Suggest a market-dependent scenario (ones with a "Market note" underneath) without passing that note along; if the user's target market is unknown, ask first (CLAUDE.md rule 11).
- Silently suggest a scenario whose validity has expired: if a platform rule, regulation or standardization shifted the scenario's ground, say so or don't suggest it at all (`knowledge/methodology.md` → Archive staleness).
- Copy archive text without adapting it to the user's context — localize the examples to the sector/product (e.g. a clothing example, not "Wireless Headphones," on a fashion site).
- Produce more than five scenarios without asking; state the count and ask the user (rule 9).
- Write the full content of the three boxes as chat text in addition to the card (rule 9) — only if the user explicitly asks for a text version, write it separately.
- List scenario titles and ask "which one should I expand" (CLAUDE.md rule 13); give the selected ones directly as cards.
