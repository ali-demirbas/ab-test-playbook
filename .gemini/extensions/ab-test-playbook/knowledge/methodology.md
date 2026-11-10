# Methodology: The Framework Every Scenario Must Fit

Every scenario in this playbook fits the same framework. Archive scenarios (`knowledge/scenarios/`) are written in the three-box format; every scenario the playbook produces is a compact scenario record (below). This file is binding: `ab-test-suggest` and `ab-test-design` apply these rules when producing a scenario, `ab-test-audit` applies them when auditing an existing plan. It covers what a test changes, measures and protects; reading a finished test's numbers is the testing tool's job, not this playbook's (CLAUDE.md rule 5).

## The scenario record

*Evidence: archive practice (this playbook's own format).* Every produced scenario is one JSON object validated by `templates/scenario.schema.json`, carrying ten pieces of information (CLAUDE.md rule 1):

| # | Information | Field | Rule |
|---|---|---|---|
| 1 | Question-form title | `title` | Ends with "?"; aim for 90 characters or fewer |
| 2 | The user problem or opportunity | `problem` | One sentence naming the observable obstacle or opportunity on the page |
| 3 | Behavioural mechanism | `mechanism` | Exactly one sentence: why B changes behaviour, resting on `problem`; no generic psychology claim (idea-generation lens → the mechanism gate) |
| 4 | The single variable | `variable` | A short noun phrase |
| 5 | The exact A/B difference | `variants`, `difference` | Exactly two variants, A (`is_current: true` only when it is the user's own current page, shown or described) and B, each with a description; `difference` is `change`, `add`, `move` or `remove` |
| 6 | Primary KPI | `primary_kpi` | `name` (the glossary's canonical name when one exists), `denominator` (who is counted, identical in both arms; never a count, never "users who saw the new element"), `direction` |
| 7 | Most important guardrail or functional protection | `guardrail` | A metric (`denominator`, `must_not_increase` / `must_not_decrease`) or a check (`criterion`); an independent harm, never the primary's complement or its name |
| 8 | Source and evidence | `source`, `adapted_from`, `source_note`, `evidence` | `adapted_from` names the archive scenario for `archive` and `adapted`; a `generated` record says in `source_note` why no archive scenario fits and how this idea differs; `evidence.level` is one of the four basis labels (The hypothesis has three parts) |
| 9 | Priority | `priority` | A tier and a one-sentence rationale (Prioritization) |
| 10 | Critical warning, only when needed | `warnings` | At most three one-sentence items typed `accessibility`, `regulation`, `feasibility`, `privacy` or `market`; omitted when nothing is critical |

Four more fields serve the quality gates (below): `invariants` (one to five functions that must work identically in both arms; required when the record touches an interactive or functional element, Variable isolation → Functional equivalence), `numeric_change` (why a number legitimately differs between A and B, e.g. in a price test), `assumptions` (at most three facts the proposal rests on that the user hasn't confirmed, `critical` with one question or `visual`; Conditional proposals) and `review` (the two reviewers' PASS stamps, written by the pipeline and required by the final card build). The card draws exactly the record's `difference`: `card.difference`, when present, must equal it.

`validate_scenario_json.py` refuses a record that breaks these rules, and everything that decides whether a record may reach a card is an error, never a warning (Quality gates); it warns only on soft wording (a title without "?", a second sentence in `problem` or `mechanism`, a title whose outcome and primary KPI belong to different families, borderline claim wording marked "reviewer must judge"); `--strict` turns warnings into errors. **The three boxes stay the archive's format and the detailed view on request:** a new proposal doesn't regenerate them; when the user asks for detail, the producing skill fills the record's optional `detail` and gives it in chat. The card never shows it: the card is the visual comparison (the title, the two mockups, the ring and its label; `mockup-style.md` → The card), and the record holds everything else.

## Quality gates

*Evidence: archive practice (this playbook's own delivery pipeline).* Code checks what code can check, the two reviewers check what code can't, and a card can't be delivered without both. A failed check is an error with its reason, never a warning that lets delivery continue.

| Check | `validate_scenario_json.py` (record, code) | `build_card.py` (card, code) | `scenario-critic` (record, judgement) | `mockup-reviewer` (card, judgement) |
|---|---|---|---|---|
| Structure | Schema errors | Runs the validator first; any validator error refuses | | |
| Single variable | Can't prove that the variants differ only in the declared variable | Any A/B difference outside the rings and any numeric difference (price, amount, %, count, rating) without `numeric_change` refuses; a `card.difference` other than the record's refuses; ring rules; writes a manifest of every change inside the rings | The variants differ in exactly the variable; `numeric_change` is justified | Every manifest item is part of the variable; anything else is FIX |
| Accessibility | An interactive change (keyword heuristic) without an accessibility warning carrying the required criteria refuses | B adds an interactive component (or more of them) without an accessibility warning refuses | The criteria fit the element | Nothing in the mockup contradicts them (a tiny target, low-contrast text) |
| KPI and guardrail | A count, "saw it" or B-only denominator, a name and denominator that measure different things, a canonical glossary name over another denominator family, a guardrail equal to or the complement of the primary, and a revenue primary on a change that touches a user benefit without a guardrail on that benefit refuse; a title and KPI family mismatch warns | | The primary matches the title's outcome, the denominator is right, the guardrail catches user harm | |
| Evidence and source | `adapted_from` must be an archive title whose `Değişken` and `Fark` the record keeps (archive) or whose `Fark` it keeps (adapted); user data and sector evidence need a note; intuition can't be high priority; in any free-text field, a number tied to an outcome or chance word (an uplift, a win probability) and experiment-result phrasing refuse unless they are the user's data with a named source, "tested", "proven" or "won" without user data refuse, "guaranteed" always does; borderline wording warns "reviewer must judge" (Claims and evidence) | | Honest label; claims judged by class, borderline wording decided (Claims and evidence) | |
| Assumptions | High priority with a critical assumption, and a critical item without its question, refuse | A critical assumption builds a conditional card, never a final one (ribbon and `abtest-status` `conditional`) | Critical and visual classified; an unverified critical fact without its item is a FIX | The conditional ribbon is expected, never a FIX |
| Functional equivalence | `invariants` missing on a record that touches an interactive or functional element (keyword heuristic) refuses | | The invariants are the right ones | |
| Regulation and manipulation | A regulated-looking record without a `regulation` warning, and urgency or scarcity wording in B without a `regulation` warning naming the real data source, refuse | Legal or mandatory text in A missing in B, security or verification text in A missing in B, and a consent box unticked in A but ticked in B refuse | Dark patterns are RET; fake urgency; price and legal display changes held | |
| Personal data | | A value shaped like personal data in a mockup refuses (`mockup-style.md` → Personal data is never copied) | | Fidelity and masking are right |
| Layout and readability | | `render_check.mjs`, when it can run, measures the draft: card size, title lines, clipped or blank frames, a ring or label covering screen elements, text below 12px, contrast below 4.5:1, A/B alignment; an error fails the run | | Reads that output (an error is a FIX) and judges what it can't measure: the mockups large enough to compare, clipping that misleads, nothing on the card but the comparison |
| Gates | `--fingerprint` prints the record fingerprint | The draft needs the critic stamp; the final needs both stamps, each matching | PASS / FIX / RET; on PASS, the record fingerprint | Reviews the draft and its manifest; on PASS, the stamp `build_card.py --stamp <draft>` prints |

**Delivery pipeline.** `validate_scenario_json.py` checks the record; scenario-critic reviews it and, on PASS, its stamp in `review.scenario_critic` carries the fingerprint `validate_scenario_json.py --fingerprint` printed; `build_card.py --draft` refuses a record without a matching critic stamp, and otherwise writes a draft card marked "DRAFT · not reviewed", and a manifest of every change inside the rings (the draft carries no fingerprint); `render_check.mjs` measures the draft and its errors are fixed first; mockup-reviewer reviews the draft, the manifest and the render_check output and, on PASS, runs `build_card.py --stamp <draft>`, which refuses a draft or manifest the record no longer builds, and the JSON it prints goes into `review.mockup_reviewer`; the final build (no `--draft`) writes the card only when both stamps match (a record with a critical assumption builds a conditional card, never a final one), and only that card is delivered; `build_card.py --check <card>` later confirms a delivered file is byte for byte that card. A refused build writes nothing and names the gate that failed.

**Fingerprints.** A fingerprint is a SHA-256 hash: of the record without `review` and `card` for the critic's stamp, of the final card's exact bytes together with `card.mockup_basis` and the manifest for the mockup reviewer's. Anything changed after a review changes its hash, so the stamp no longer matches and the build refuses until the changed part is reviewed again.

### What the gates can't guarantee

- **That the variants differ only in the variable, semantically.** The builder diffs the markup and lists every change inside the rings; whether each listed change belongs to the variable is the mockup reviewer's call and can't be proven from HTML.
- **That the keyword heuristics are right.** Detecting an interactive change, a functional element, a user benefit, over-claiming or urgency from words has false positives (a harmless mention) and false negatives (the same change described in other words); the reviewers cover what the words miss.
- **That the invariants hold in the product.** They are declared and reviewed, not executed against the real product; the team that builds B keeps them true.
- **That B is accessible.** The criteria are declared and checked against the mockup, not tested on the live product; the pre-start gate (Guardrails → Pass/fail guardrails) is the real check on the built B.
- **That the layout was measured.** `render_check.mjs` needs Node and Playwright; without them the mockup reviewer reads the markup instead, which can't measure contrast or overlaps.
- **That a careful review happened.** A stamp proves the reviewed content is unchanged since the review, not how well it was reviewed (CLAUDE.md rule 17).

## The three-box framework

*Evidence: archive practice (this playbook's own format, not an external standard).* The archive writes every scenario in three blocks, each with exactly 5 items (`validate_scenarios.py` requires this). The same three blocks are a produced record's detail view: they exist only when the user asks for it, in `detail`, with 3 to 6 items per box (`kpis` has exactly one primary, listed first, and at least one guardrail):

1. **Test edilmesi gerekenler ("What to test")**: which questions the hypothesis has to answer. Each item is in `Label: question?` form (e.g. `Position: in the header, or inside the menu?`). At least one item asks a device/segment breakdown.
2. **Takip edilecek ana KPI’lar ("Primary KPIs to track")**: the measurement set. Rules below. (The apostrophe in the box name is curly, U+2019; the validator doesn't recognize a straight-apostrophe version of the heading.)
3. **Yapılmaması gerekenler ("Never do")**: the mistakes that invalidate the test or harm the user. At least one item protects variable isolation, in the form "don't change X and Y together in the same test." Items stay scoped to this variant; the generic freeze/hygiene rules live once in **Test hygiene (applies to every scenario)** and aren't repeated per scenario.

## KPI rules

*Evidence: established experimentation practice.*

- The **primary metric** (a record's `primary_kpi`; the first line of a KPI box) is the one outcome the hypothesis predicts will move, named before the test starts. Listing five metrics as equally weighted leaves the test without a question and invites picking whichever one moved afterwards (p-hacking).
- Every record carries a **guardrail** (a KPI box carries at least one): something that could degrade while conversion rises. Typical guardrails: gross margin, return rate, page speed (LCP), support tickets, abandonment at a later step than the primary, RPV, and accessibility as a pass/fail check (keyboard and screen-reader completion, touch target, contrast, motion; CLAUDE.md rule 3 and Guardrails below). Measured guardrail items are written in "must not drop / must not rise / must not increase" form. A win with no guardrail is a deferred loss: a cost you didn't measure in the test doesn't get canceled, it just gets carried into next quarter's return rate or support load.
- **A guardrail measures an independent harm.** It is never the complement of the primary: completion and abandonment of the same step over the same denominator are one metric written twice, so one can't win while the other degrades and the guardrail measures nothing. A valid guardrail is a cost the primary can't see: a downstream step (order after form, activation after signup), a quality signal (return rate, qualified share), a cost (margin, support load, LCP), or a different population the tool can identify (returning users, a device class). An abandonment rate qualifies only at a later step than the one the primary measures.
- The metric has to be something the tool can actually measure. "Trust perception" isn't a KPI; its proxy is written instead.
- **An intermediate-step metric can hide whether completion actually happened.** A change can easily boost a step in the middle of the funnel (add-to-cart, starting checkout, opening the form, choosing express checkout), and this looks like a win at first glance, but if the user who clears that step more easily then gets stuck at the next one, the total order count doesn't change, or even drops. The risk is especially high for variants that speed up, skip, or foreground a step: the user gets thrown at the outcome of a decision they haven't actually made yet, and bounces back. This is why the primary metric is the outcome the change is meant to move, measured at the closest point where it is still a business outcome: the completion of the step's job (completed order, submitted form, finished signup), not a click or a step entry on the way there. A step or proxy metric (add-to-cart, CTA click, checkout start) is primary only when the outcome event isn't tracked; then it's named as a proxy and the outcome stays in the list as a guardrail, so a proxy win that loses orders is still caught. Otherwise the intermediate-step metric is tracked second, as a diagnostic. If the two move in opposite directions, that's the finding.
- **Conversion rate can hide revenue.** In price, installment, discount, or bundle tests, plain "Conversion Rate (CR)" isn't enough as the primary metric: lowering price almost always raises CR but can drop revenue. In these scenarios the primary metric should be revenue-based: Revenue Per Visitor (RPV), or Average Order Value (AOV) × CR. The price scenarios in `knowledge/scenarios/product-detail.md` and `cart-checkout.md` already apply this distinction; the same rule holds when a new price/bundle scenario is produced.
- **A revenue win must not hide user harm.** When the change touches a benefit the user is owed or offered (a coupon or discount code, a campaign or promotion, free shipping, a refund or cancellation path), a revenue primary (RPV, revenue, AOV, order value, margin) can rise because users lost that benefit: hiding the coupon field can raise revenue by making code holders pay full price, and that reads as a win. Such a record carries a guardrail on the benefit itself, over a denominator the change can't dilute (coupon change: "Kuponlu Sipariş Veren Ziyaretçi Oranı" per assigned visitor must not decrease; a per-order coupon rate falls mechanically when B adds orders without codes, so it can flag harm that didn't happen), plus the functional pass criterion in `invariants`. A coupon test takes RPV as primary until the user states the business goal (then the goal's outcome, e.g. orders): the field moves revenue both ways, and the benefit guardrail and invariants protect coupon use. `validate_scenario_json.py` refuses a revenue primary on a benefit-touching record without a guardrail on that benefit (keyword heuristic); scenario-critic checks the guardrail really catches the harm.

## KPI denominator: assigned visitors (KPI paydası: atanan ziyaretçi)

*Evidence: established experimentation practice.* A rate is only comparable between arms when its denominator exists, defined identically, in both arms.

- **The default denominator is the assigned population:** every user (or visitor, session or account, matching the randomization unit) assigned to the test, counted from the assignment event in both arms. "Conversion rate" in a scenario means conversions divided by assigned visitors unless the item says otherwise.
- **Never "users who saw the new element".** If B adds a pop-up, a hint card or a badge, only B has users who saw it; "share of users who saw the pop-up and continued" has no A counterpart, and the users who see it are already a filtered, non-random group. Comparing it with anything in A compares two different populations. Within-B diagnostics (touch rate on an element only B has) are allowed as secondaries but are labelled "B only" and never compared across arms.
- **Every line carries its denominator.** Every KPI line, guardrails included, states its denominator; a triggered denominator names the trigger event and says it is logged at the same point in both arms, before the change is shown. (An archive line written with a canonical glossary name inherits that row's denominator; a produced record writes it out in `primary_kpi.denominator` and, for a metric guardrail, `guardrail.denominator`.)
- **A triggered denominator is the valid narrower option.** When the change only matters at a specific moment (reaching the payment step, a zero-result search, an exit-intent signal, opening an empty dashboard), the denominator can be the users who reached that trigger, provided the same trigger is logged in both arms, at the same point, whether or not the arm then shows anything (counterfactual logging in A: "B would have shown the pop-up here"). The trigger must sit upstream of the change; if the variant itself changes who reaches the trigger, fall back to the assigned population.
- **Never conditioned after assignment.** A metric over a population defined by something users do after assignment (per quote, per order, per request or trial, "among users who…") moves when B changes who does that thing: B can raise quotes per visitor while the per-quote conversion falls, reading a win as a loss or the reverse. It is never the primary and never replaces the main comparison; at most a labelled secondary or diagnostic in the detail view. A denominator is never an event the test changes (a step at or after the change). Insurance example: the guardrail per assigned visitor is "Sözleşme Oranı (30 gün)" (contracts within 30 days over assigned visitors); "Teklif → Sözleşme Dönüşüm Oranı" (per quote) is a quote-denominator diagnostic.
- **Archive KPIs are starting points.** A block's KPI lines are written for its own example; a record keeps one only where it fits the record's title and these rules. A per-quote "Teklif → Sözleşme" line in a block (whatever its parenthesis says) becomes "Sözleşme Oranı (30 gün)" per assigned visitor in a record; the per-quote rate stays a labelled diagnostic in `detail`.
- **Name, denominator and behaviour agree.** A name encoding a conditional population (an arrow such as "Teklif → Sözleşme", "<X> Başına" for a post-assignment event, "per order", "among", "arasında") over assigned visitors, or "(atanan ziyaretçi başına)" / "per assigned visitor" over an order, request or quote population, measures two different things: the validator refuses both.
- **One KPI name, one meaning.** A canonical glossary name fixes its denominator family (assigned visitor or user; order; request or lead; quote; session; a trigger "reached"), the same in every scenario; a trailing window like "(30 gün)" belongs to the name but not to the match. Another denominator needs another name (a one-off metric with its denominator written out); the validator refuses a canonical name over another family.
- **Coupon eligibility.** Code holders generally can't be identified before assignment, so no "code holders" segment is invented: the measurable guardrail is "Kuponlu Sipariş Veren Ziyaretçi Oranı" per assigned visitor (must not decrease), and the record's invariants carry the functional pass criterion (a valid code can be entered, is applied and discounted, and errors are handled identically in both arms). When holders are identifiable before assignment (they arrived through a coupon campaign link, or a logged-in user has an issued code), the same rate can also be watched in that pre-assignment segment.
- **Realized versus normalized revenue (subscriptions).** Cash actually collected in the observation window ("Tahsilat (gözlem penceresi, atanan ziyaretçi başına)"), monthly-normalized new subscription value ("Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)": the sum of new subscriptions' monthly-equivalent price over assigned visitors) and subscription value over a stated window are different metrics. An annual-by-default test can raise cash collected up front while lowering normalized value; neither is presented as the other, and normalized value is never presented as realized RPV.
- **Counts are not primaries.** A count ("Nitelikli Fırsat Sayısı", "Talep Sayısı") is only comparable when the arms are exactly the same size, which a random split never guarantees. The primary is written as a rate per assigned visitor ("Nitelikli Fırsat Oranı (atanan ziyaretçi başına)"); a count can stay as a secondary readout.
- **One metric per line.** "Stay rate / return rate" is two metrics with two denominators; pick the one the mechanism predicts and keep the other as a secondary, if at all.
- **A window in the name is part of the definition.** Returns, cancellations, retention and repeat purchase happen after the test's exposure, so the window is written inside the KPI name ("İade Oranı (30 gün)": returns within 30 days of delivery); the same holds for a primary whose event B can shift in time ("Kayıt Oranı (7 gün)" is not "Kayıt Oranı"). The denominator says from which event the window counts, an event both arms share (assignment, first open, each user's own order), never one B moves. A cause-specific rate ("Beden kaynaklı iade oranı") is preferred over a generic one when the mechanism is specific; its denominator is still orders (or assigned visitors) in each arm, not returns.

The canonical Turkish KPI names, each with its definition, denominator and accepted synonyms, are in `knowledge/kpi-glossary.md`; the archive uses those names, a synonym in a user's plan is read as its canonical metric, and a one-off metric outside the glossary is allowed as long as its denominator is written out. `validate_scenarios.py` refuses a primary KPI that is a count ("Sayısı") or uses a "saw it" denominator ("gören/görüp"), and warns on the same pattern in any other KPI line, on a guardrail that is the complement of the primary and on a scenario with no variable-isolation item; `validate_scenario_json.py` applies the same checks to a produced record, as errors: a count, "saw it" or B-only primary denominator, a guardrail named like the primary and a guardrail that is the primary's complement.

## The hypothesis has three parts

*Evidence: archive practice.* A one-sentence hypothesis ("making X into Y increases Z") isn't enough; it has to answer three separate questions:

1. **Theory:** Why are we proposing this change? What observation, data, or user feedback produced this hypothesis?
2. **Basis:** What concrete evidence supports this theory? (A metric, a user comment, a behavioral pattern.) If there's no evidence, it's marked "intuition," and the confidence level is kept low accordingly. The basis is labeled with one of four levels and shown in the output:
   - **The user's own data**: a signal measured on this exact product/page (the strongest).
   - **Archive pattern** (“Arşiv örüntüsü”): a curated idea from this playbook's archive, found worth asking in a similar context. It is not a test result: the archive doesn't record that it won anywhere, so a record resting on it is never presented as tested, proven or a known win.
   - **Industry observation**: common practice, but with no product-specific verification.
   - **Intuition**: none of the above; a suggestion can still be given, but it's stated as low-confidence.
3. **What we'd learn:** What do we learn if the test wins, what do we learn if it loses? If neither outcome produces information, the test is already weakly designed.

A record carries the first two in compact form (Theory is `problem` plus `mechanism`, Basis is `evidence`); What we'd learn is written out in the detail view or when the user asks. The one-sentence fill-in template:

> "Based on [observation/data], we think that making [change] will produce [expected outcome] for [target audience]. We'll see this in [metric]."

Weak example: "Changing the button color might increase clicks." (No basis, outcome isn't measurable with any clarity.)
Strong example: "We know from heatmaps that mobile users notice the CTA late; if we raise the button's contrast against the page (one variable: its colour), click rate among new visitors will increase by a measurable amount. We'll see this in the page-view-to-signup conversion rate."

If the change is too subtle to make a difference in the metric (e.g. a 2px border-width change), don't build a hypothesis; "is this change distinct enough to be noticed?" is the first filter of every scenario design.

**Which objection are we resolving?** If a user isn't completing a step, there's usually an unnamed objection underneath it. Six patterns repeat (*Evidence: industry observation*):

| Objection | The user's question | Typical counter |
|---|---|---|
| Trust | "Why should I believe this?" | A named reference, concrete evidence, a security signal |
| Price | "Is this worth it?" | Value comparison, installments, an ROI display |
| Fit | "Does this suit my situation?" | A similar-user example, segment-based content |
| Timing | "Why now?" | Real (not made-up) urgency, opportunity cost |
| Effort | "How hard will this be?" | "Set up in 5 minutes," a step-by-step walkthrough |
| Clarity | "What do I get, and what happens next?" | Naming the outcome on the button, previewing the next step or result |

Naming which objection is being targeted in one word when building the hypothesis makes it clearer why the test will (or won't) work. If there's evidence (support tickets, cancellation reasons, a survey answer), which objection it maps to is stated; if not, it's marked as an assumption. The objection-closing message can also be built implicitly: instead of naming the objection directly ("worried you're being lazy?"), moving straight to the solution ("we handle this for you") usually works better; saying the objection out loud can reinforce it (*Evidence: industry observation*).

## Claims and evidence

*Evidence: binding rules 8 and 10.* A record makes no claim about results that it can't source. The rule holds in every free-text field (title, problem, mechanism, variable, variant descriptions, priority rationale, evidence and source notes, warnings, invariants, `numeric_change`).

- **Allowed:** real performance data the user supplied, with its source (`evidence.level: user_data`, `evidence.note` naming the source); a discount percentage or threshold that is on the page; a directional expectation framed as a hypothesis with no number ("B'nin siparişi artıracağı bir hipotez"); a verified prior research result quoted in context with its source and kept attributed ("<source> reports …"; level `user_data` or `sector`, the note naming the source).
- **Refused:** an unsourced chance of winning ("win probability 70%", "büyük ihtimalle kazanır", "likely to win"); a fabricated experiment result ("benzer testlerde %12 arttı", "similar tests lifted conversion 12%", "other companies saw", "arşivde kazanmış"), which is refused even without a number unless it is the user's data with a named source; a predicted uplift presented as an estimate ("beklenen artış yüzde 12", "expected uplift 12 percent", "raises revenue by 20%", "conversion rises 12%"); a vague sector observation stated as proven; archive presence as experimental proof ("tested", "proven", "known to work"); "garanti" / "guaranteed" always.
- **How it is checked:** the validator refuses a number (%, yüzde, percent, x or kat) tied to an outcome or chance word in either order within a short window, and experiment-result phrasing, as errors; borderline wording it can't decide (an outcome word near an unrelated number, "çok daha fazla", "ciddi artış") is flagged "reviewer must judge" (an error under `--strict`). scenario-critic decides those, and the same claim in other words.
- **The unknown is written as unknown.** Whatever the playbook doesn't know (past tests, margin structure, technical constraints, a real figure on the page) is stated as missing; no number, ratio or duration that isn't certain is presented as if it were.

## Conditional proposals

*Evidence: archive practice (this playbook's convention).* A strong idea can rest on a fact the user hasn't given. It isn't dropped and the gap isn't filled with an invented fact: the record carries the fact as an assumption and becomes a conditional proposal.

- **The field.** `assumptions`: at most three items, each `{"type": "critical" | "visual", "text": one sentence of at most 200 characters, "question": one short question}`, the question required for a critical item. **Critical:** the proposal's feasibility, legality or single-variable status depends on it (how a real price is displayed, a field's legal purpose, whether a field is needed at a later step, the real step names the variant writes). **Visual:** representative product names, photos, decorative details.
- **Priority.** A record with an open critical assumption is medium at most; the validator refuses high, and the rationale says what it waits for.
- **The card.** A record with a critical assumption builds a conditional card ("koşullu kart"), never a final one: it carries the "KOŞULLU · doğrulama gerekli" / "CONDITIONAL · needs verification" ribbon and `<meta name="abtest-status" content="conditional">`, the build summary says "conditional card (not implementation-ready)", and chat never calls it final; it still needs both stamps (`mockup-style.md` → Draft and final card).
- **Chat.** One line after the list, "Koşullu (<n>): …" / "Conditional (<n>): …", n being the number of conditional records in the turn, naming every critical assumption briefly as a fact to verify, by scenario number, separated by semicolons ("Koşullu (2): 1 için yıllık planın kartta görünen fiyatı; 3 için telefonun teklif hesabında gerekip gerekmediği."). The turn's one question (rule 19) asks the most critical of them, ranked by its subject: a regulated display is kind 2, a real figure kind 5, an unseen detail or absent element kind 6, a field's need or feasibility kind 7; when a higher kind is open, that one is asked and the line stands without a question. Visual assumptions get no line beyond the existing representative or described line, when it applies.
- **Confirmation.** When the user confirms, the producer removes the assumption; the record changes, so it goes back through scenario-critic, a new draft and the mockup review, and only then is a final card built, with no ribbon. An answer that contradicts the assumption rewrites the record or drops it, said in one line.
- **Review findings.** A fixable finding whose fix needs a fact the user didn't give becomes a critical assumption with its question, never an invented value and never a reason to drop the record (`agents/scenario-critic` → Severity).

## The idea-generation lens

*Evidence: archive practice.* Ideas aren't produced by looking at the page and writing down whatever comes to mind. Four filters are applied, in order.

**1. Opportunity scan.** The six objection lenses above (Trust, Price, Fit, Timing, Effort, Clarity) are used for the opportunity scan: for each objection, is there a genuine gap or user obstacle on this page? If it's already answered, that lens is skipped. **Not every lens has to produce an idea**; forcing one out of an irrelevant lens produces a suggestion unrelated to the page (e.g. "let's add an expert opinion" at the checkout step). The scan also makes visible what should exist but doesn't, in addition to what's already on screen (see Variable isolation → the addition axis).

**2. The mechanism gate.** Every candidate has to give a concrete answer to "why would this change alter user behavior?" "More eye-catching," "looks more modern," "cleaner" aren't answers; those candidates aren't suggested. The mechanism has to rest on **an observable user obstacle on the page**, not a generic psychology claim:

- Not a mechanism: "Social proof increases trust."
- A mechanism: "On this page the user can't see any evidence to judge the product's quality; moving a verifiable user review to the decision point reduces this uncertainty."

The mechanism is the record's `mechanism` field: exactly one sentence, resting on the obstacle `problem` names. The gate has two limits:

- **The gate only applies to candidates the playbook produces on its own.** If the user explicitly wants a test (e.g. "let's make the button red"), the test isn't refused: it's built, but its mechanism is explicitly stated as weak, and a stronger-mechanism alternative is placed next to it. The only thing that's refused is a dark pattern (rule 6).
- **Mechanism and basis are different axes.** Basis is the question "does this problem genuinely exist" (evidence level, rule 10); mechanism is the question "if it does, why does this change fix it." A strong mechanism can coexist with `Evidence: intuition`, and this candidate isn't eliminated; only its confidence level is marked low.

**3. Mechanism-duplication check.** Ideas resting on the same behavioral mechanism in the same page area aren't presented as separate suggestions just because they're worded differently; they're merged, or the strongest one is picked. "Add social proof," "make reviews visible," "highlight popular products" aren't three ideas, they're three phrasings of the same mechanism.

**4. Impact ranking: not a ban, an order.** If more than one candidate passes the gate, they're prioritized in this order:

1. The offer itself, removing a step from the flow, adding missing information at the decision point, information architecture and decision structure.
2. Hierarchy and visual weight, copy that answers an objection, a trust signal at the friction point.
3. Color, corner radius, font, generic CTA wording, micro-spacing.

A third-tier candidate with a strong mechanism is still suggested; this isn't a ban, it's a tie-break criterion under equal conditions. The ranking is a heuristic priority, not a measured outcome. The user's test memory (rule 16) overrides this ranking **only for the same component or the same mechanism**: a CTA-color test having won in the past doesn't mean every cosmetic candidate now jumps ahead of structural ones.

These four filters don't replace prioritization, they run before it: the lens answers "is this idea worth suggesting at all," priority (Prioritization below) answers "which of the remaining ones goes first." The impact tiers above are what the impact part of a priority rationale weighs, and they break a tie between two candidates of the same priority.

## Variable isolation

*Evidence: established experimentation practice.*

- A test changes **exactly one variable**. If there's a second difference in Variant B (price, product, rating count, a badge), the test is contaminated (a confound) and the result can't be interpreted. Two differences on the same screen are two separate tests; bundling them into one report doesn't make them one test.
- **Functional equivalence.** One variable means B changes how one thing is presented, not what the product does. Whatever the change touches but doesn't test works identically in both arms: when B touches an interactive or functional element (a link, a field, a coupon, payment, search, a form), the record lists those functions in `invariants`, one sentence each ("Geçerli bir kod iki kolda da aynı adımla uygulanır ve indirim toplam tutara aynı hesapla yansır."). In the coupon example they are the apply step, the discount calculation and totals, and the message for an invalid or expired code. An arm where one of them behaves differently carries a second variable. The validator requires `invariants` when the record's text names such an element (keyword heuristic); scenario-critic checks they are the right ones.
- Variant A is always the control (the current state), Variant B is the test. Don't swap the roles.
- **A test isn't only about changing what already exists.** A page has three kinds of opportunity: changing an existing element, removing an existing element, and **adding an element that doesn't exist**. The third is usually the highest-impact and the least obvious, because whatever's on screen is always what "seems to be there." When evaluating a page, this question is also asked separately: what question is the user asking at this step, and is the answer on screen? Missing information or a missing action can be the subject of a variant.
- **If the user shared their page, A is that page.** Redesigning the control, simplifying it, or making it "representative" invalidates the test: what you're measuring is no longer your suggestion's effect, it's the difference between two separate designs. Whatever's on screen is A; the only thing to be produced is B.
- **A defect in A isn't a variant.** A defect on the shared page (a typo, a broken label, a dead control) is reported as a fix to ship, not a scenario. It ships either before the test starts, in both arms, with the card's Variant A redrawn from the fixed page, or after the test ends; never in one arm and never while the test is running. A missing mandatory notice is a compliance finding (rule 11), not a test.
- **Derived personal figures are personal data.** Personal data isn't only what the user typed into a field (rule 15). Any figure the page derives from the user's own account is personal too: balances and accumulated amounts, allocation percentages, pie or ring chart slices, return rates, contribution amounts, contract or policy numbers, plan codes. None of it enters the card, the scenario JSON or the chat. The mockup keeps the structure and drops the values (`knowledge/mockup-style.md` → Personal data is never copied), identically in both variants.
- **Moving to multi-step in a form flow isn't the default fix.** Adding a step opens a new abandonment point at every step; in practice, consolidating onto a single page that fits the screen often works better (grouping related fields, dropping unnecessary fields, reducing vertical spacing). A multi-step form is only suggested when the fields genuinely don't fit one screen or naturally belong to separate phases, and when it is suggested, it's stated as an assumption. **Field count comes before step count:** when testing a form, a field-reduction/unnecessary-field-removal scenario is suggested before a single-page-vs-multi-step scenario, because how many fields you make someone fill in tends to shape the experience more than how many steps you split the flow into (*Evidence: industry observation, a recurring one in form usability work; not verified on your product*).
- The same product, price, and content are used in both variants; only the tested element differs. A number that differs between A and B is a second variable unless the number is the variable; then the record says why in `numeric_change` (a price test), and the card builder refuses any numeric difference without it.

## Test hygiene (applies to every scenario)

*Evidence: established experimentation practice.* These rules hold for every test, so a Never-do box (archive or detail view) doesn't repeat them; it stays scoped to its own variant (what not to change alongside *this* variable).

**Pre-start gates.** The test takes no traffic until every gate that applies is closed. They are always written, once: as the one pre-start line after the list ("Başlamadan önce:" / "Before you start:"); `ab-test-design` writes that line only in its setup notes, as their last line under `Pre-start gates` ("none" when nothing applies), never a second time after the list:

1. **Compliance sign-off on B's exact copy** when the variant sits inside a regulated flow (rule 11) without changing a regulated display. A variant that changes regulated copy, a price or rate display, consent wording or a mandatory disclosure is held, not gated (Regulated flows). The condition also travels with the record: a `regulation` item in its `warnings` (one Never-do item in the detail view).
2. **Pass/fail guardrails checked on B** (accessibility, legal copy intact; Guardrails → Pass/fail guardrails).

- **Freeze everything else during the run.** No price, campaign, promotion, algorithm, copy or design change on the tested page or flow while the test runs, including "small" edits like CTA wording or a banner swap. A mid-test change contaminates both arms unequally in time.
- **Don't iterate the variant mid-test.** Editing Variant B after launch starts a new test; restart the count from zero.
- **A bug fix restarts the test.** A script error, measurement gap or wrong assignment found mid-test is fixed and the test restarts with fresh data.
- **Log assignment and outcome as separate events**, and keep exposure identical in timing across arms (no extra redirect or delayed load in one arm only). **Data loss must be equal too:** if one arm fails to record some users for a technical reason (a heavy visual variant that slow connections leave before it logs, a script an older browser can't run), the arms no longer describe the same people; an implementation that could do this is checked before launch.
- **Keep one user in one arm** for the whole run (sticky assignment); don't reshuffle between sessions or devices you can link.
- **Don't stack copy or CTA changes back to back on the same page:** each change moves the baseline the next test starts from.
- **Exclusions are fixed in advance:** employees, bots, users in a conflicting concurrent test (see Concurrent tests below). They go in the setup notes under "Exclusions and concurrent tests".

**Setup notes.** `ab-test-design` writes the setup notes after every designed test, asked for or not, because they are short and the user needs them to run the test: the target audience (who is included and excluded), where the variant appears, exclusions and concurrent tests, and the pre-start gates, once, after the scenarios, carrying only what the records don't hold. The pre-start gates are always written, as the notes' last line ("Başlamadan önce:" / "Before you start:"), the only place design writes them, and siblings on one screen always get the sequencing line. The primary KPI and the guardrail are already in each record and aren't repeated. A field the playbook doesn't know is written "needs to come from the user", never guessed. Split ratios, sample size, duration and decision rules aren't part of them (rule 5).

## Guardrails

*Evidence: established experimentation practice.* Every record carries its most important guardrail or functional protection (CLAUDE.md rule 3): a metric in "must not drop / must not rise" form (`must_not_decrease` / `must_not_increase`) with its denominator, or a pass/fail check with its criterion. It measures an independent harm (KPI rules: never the complement of the primary). The detail view may list more guardrails.

- **A harm to watch, not a threshold.** A guardrail names what must not get worse; it carries no numeric tolerance margin, no "read after N days" and no decision rule. How a finished test is read belongs to the user's testing tool (rule 5).
- **A lagging guardrail names its window in the KPI name.** Returns, cancellations, churn or a payment stop happen after exposure, so the window is part of the definition ("İade Oranı (30 gün)"). A window that is legal or product-specific (a withdrawal period) is taken from the product terms, never guessed. When the only harm is lagging, a leading companion that shows the same harm sooner (payment error rate, support contacts in the first 7 days) is worth adding to the list.

**Pass/fail guardrails.** Some guardrails aren't rates: accessibility (keyboard and screen-reader completion, touch target, contrast, motion), mandatory legal copy intact, security controls untouched. They are written as a check with a criterion instead of a "must not rise" metric and run as pre-start gates (Test hygiene → Pre-start gates). Accessibility's triggers, criteria and wording: Accessibility checks.

## Accessibility checks

*Evidence: binding rule 3; the criteria are widely used accessibility thresholds.*

- **Triggers.** B adds or changes a link, a button or another tap target (a chip, toggle or card), a field, a modal or pop-up, a moving or auto-advancing element, the focus order, contrast, or how an element behaves when used (a link that opens a field).
- **Criteria that fit the element:** a touch target of at least 44×44 pt (48×48 dp), text contrast of at least 4.5:1, reachable and operable by keyboard (on a native app, the platform's equivalents such as an external keyboard or switch control), a name a screen reader announces; a modal or pop-up also takes focus when it opens and closes with a visible control and Esc; an auto-advancing element can be paused; a control that opens something says where focus goes. The record's `accessibility` warning states them as a must-pass check ("Geçmeli: …"), e.g. "Geçmeli: “İndirim kodum var” bağlantısı klavyeyle ulaşılır ve ekran okuyucuda bu adla okunur, açılınca odağı alana taşır, dokunma alanı en az 44×44 pt, metin kontrastı en az 4.5:1."
- **A pre-start gate, never auto-approved.** The check is run on B and closed before the test takes traffic (Test hygiene → Pre-start gates); the warning states it, the team runs it. It is never a metric segmented on assistive-technology users, which most analytics stacks can't identify. "Conversion went up but the flow broke for screen-reader users" doesn't count as a win.
- **Where it lives.** When accessibility is the most important protection it is the record's `guardrail` itself (kind `check`). In the detail view the KPI box carries "Erişilebilirlik Kontrolü (yayın öncesi, geçti/kaldı)" (accessibility check, before launch, pass/fail) with the Guardrail pill and the same criterion.
- **Mechanical checks.** The validator refuses an interactive change without these criteria (keyword heuristic), the builder refuses a B that adds an interactive component without the warning, and scenario-critic checks the criteria fit the element; mockup-reviewer checks the drawing doesn't contradict them.

## Concurrent tests: layering and mutual exclusion

*Evidence: established experimentation practice.* Tests on **different** pages or independent elements can run at the same time on overlapping traffic (**layering**): randomization is independent, so each test's other-test exposure averages out across its arms. Tests that touch the **same** page, flow or decision don't share users: one user is in one test on a screen. They run sequentially or with **mutually exclusive** traffic (disjoint user pools), because their effects can interact (B1 only works when combined with B2), e.g. a price-card test and a checkout-button test on the same funnel. Concurrent tests are recorded in the setup notes under "Exclusions and concurrent tests".

**Several scenarios on one screen in one turn.** When a turn produces more than one scenario for the same screen or flow, the chat states once (in the sequencing line after the list; under "Exclusions and concurrent tests" when the setup notes are written) that they run sequentially (in priority order) or with mutually exclusive traffic, never overlapping on the same users. In the detail view, each of them also carries a mutual-exclusion Never-do item that names the other test ("don't run this at the same time as the CTA-position test on this screen"); it is scoped to the variant, so it isn't a repeated hygiene rule.

## Prioritization

*Evidence: archive practice (the tiers are this playbook's convention).* When several scenarios are suggested, each carries a **priority**: high, medium or low (Yüksek / Orta / Düşük; the chat tag line prints the tier, "Öncelik: Orta" / "Priority: Medium"; the rationale stays in the record's `priority.rationale` and is given in chat when the user asks). The tier comes with a one-sentence rationale that weighs three things in words:

- **Impact:** where in the funnel the change acts and what decision it touches (the impact ranking in the idea-generation lens above). A change at the payment step's decision weighs more than a cosmetic one on a browse page.
- **Confidence:** the evidence label (rule 10). A direct signal in the user's own data is the strongest, an archive pattern comes next, industry observation and intuition are weak. An archive source never means high confidence by itself and is never an experiment result: it is a curated idea, not a test that won.
- **Ease:** a copy, style or ordering change is easy; medium-scale front-end work sits in between; ease is low when the test needs backend work, a new native app release or an operational change (a team, a process, a supplier), and the rationale says so.

Example rationale: "Medium: acts on the payment step's decision (high impact), rests on an archive pattern (moderate confidence), a copy-only change (easy)." There are no numeric scores, no multiplication and no cut-offs: the tier is a judgement the rationale makes visible, not a computed quantity.

- **Strong candidate (rule 9)** = passes the mechanism gate **and** has priority medium or high. A turn produces at most three by default, never two resting on the same mechanism. Order: the user's explicit asks first, in the order asked, then the playbook's own candidates by priority, those acting on the stated problem first.
- **An intuition-only idea is high only when impact and ease are both clearly high,** and its rationale says so: the tier comes from impact and ease, not from evidence.
- **A native-app change that adds a new element or a new navigation target isn't "easy" by default:** it needs a release, a review cycle and usually a new screen state, whatever its size on screen.
- **A record with an open critical assumption is medium at most** (Conditional proposals; the validator refuses high). A strong idea resting on an unverified critical fact stays as a conditional proposal instead of disappearing.
- **Never pad to three:** one strong proposal is a complete turn, and a weak candidate isn't added to reach a count.
- **No numeric score** (ICE or any other), even when the user asks for one: the tiers are given with one line saying the playbook doesn't score numerically.
- **Ties:** the higher-impact funnel point goes first, then the one simpler to implement, then the one with lower guardrail risk.
- **Confidence is never claimed without its basis:** the rationale names what it rests on ("a similar test on the same page won last quarter, per the history file").

## Local-maximum risk

*Evidence: archive practice.* Stacking only small, single-variable improvements (button color, line spacing, item order) plateaus past a certain point: the small gains run out, and a larger win needs the page itself redesigned. When the user's `.abtest-history.md` records several small tests on a product or page coming back "fark yok" / "no difference" (as the user's own tool reported them, rule 16), `ab-test-suggest` suggests a bolder/more structural variant in its next suggestion (e.g. restructuring the whole flow, not just one field) and states why. A concrete escape tactic: widen the variable from a single small element to the entire page/flow (a radical-redesign test); once that bigger question is answered, return to single-variable tests.

**This escape tactic is a different kind of experiment, and it's worth naming that difference rather than blurring it with rule 4.** A **diagnostic experiment** isolates one variable so a win or loss teaches you which specific mechanism moved behavior; this is what rule 4 (one variable) governs, and it's the default. A **radical-redesign experiment** bundles many changes into one new experience on purpose; it can tell you whether the new experience as a whole beats the old one, but it can't tell you which of the bundled changes did the work; that's the price of measuring the total effect. When this escape tactic is used, say explicitly that it's a bundled-treatment test, not a rule-4 single-variable test wearing a bigger variant: the result answers "is the new experience better," not "which part of it worked." A follow-up round of single-variable tests is what answers that second question, once the bundle has won.

## Qualitative feedback alongside the test

*Evidence: industry observation.* Numbers alone can mislead: user comments explain *why* a metric moved. Adding a short survey link at the bottom of the test page is a cheap extra signal; it isn't mandatory, but it's worth suggesting, especially on a page whose earlier tests the history file records as "no difference". Single-question surveys usually get the most responses. Example questions: "What's stopping you from completing [action] today?" (to those who didn't complete it), "What almost stopped you from buying?" (to those who did buy, asked right after purchase gives the most honest answer). Support-ticket and cancellation-reason records carry the same signal for free: look for phrases like "but," "worried," "not sure."

## When the archive goes stale: knowing when not to trust it

*Evidence: archive practice.* These scenarios aren't timeless. A scenario's validity drops in these cases; if `ab-test-suggest` notices one of them, it warns when suggesting the scenario, or doesn't suggest it at all:

- **A platform rule changed:** Consent flows, notification policies, browser cookie/tracking restrictions, app-store rules. Measurement or implementation may no longer be possible.
- **Regulation changed:** Discount and reference-price display, data collection, subscription cancellation, accessibility requirements.
- **The pattern became standard:** Something that was once differentiating (guest checkout, mobile responsiveness, search suggestions) is now a baseline expectation, and the test's question turns from "should we add this" into "how should we do it."
- **The technology changed:** If page speed, interface conventions, or device usage have shifted the ground the scenario assumed.
- **It ran dry in your own data:** If the same pattern gave you "no difference" repeatedly in your own product, being in the archive doesn't make it valid for you (see local-maximum risk).

The archive isn't a promise, it's a pattern library: a scenario being here doesn't mean it was tested or won anywhere, let alone that it will win in your product, only that it was found worth asking in a similar context.

When a scenario is invalidated by one of these reasons, it isn't quietly deleted from the archive: what changed and what's suggested instead is written underneath the scenario itself, so the reasoning stays attached to it. The "Market note" lines under a scenario serve the same purpose: the dependency becomes visible, and the user can decide whether it applies in their own context.

## Where this discipline comes from

*Evidence: this section is the key to the labels above (archive practice, established experimentation practice, industry observation).* Most of the discipline here comes from this archive's own field practice. Some of it is widely accepted in experiment methodology; when a user asks "how do I defend this to my team," these can be described as established practice, but not attributed to any single institution or publication:

- **One variable per test and a primary metric named in advance**: the core of controlled-experiment design: a second difference makes the result unattributable, a metric picked afterwards makes it unfalsifiable.
- **The same denominator in both arms**: a rate compares two arms only when it counts the same population in each.
- **Conversion rate hiding revenue**: this is where the reasoning for using a revenue-based metric (RPV) in price and discount experiments comes from.
- **Cross-test contamination**: common practice across large-scale experimentation infrastructure; this playbook keeps one user in one test per screen (Concurrent tests).
- **Checkout/form usability**: a recurring industry observation in form usability work, not a measured result of this archive; the field-count-before-step-count ordering comes from here and is labelled as such where it's used.

**Why the playbook stops at design.** Reading a result correctly depends on how the testing tool assigns users, logs events and computes its statistics, none of which the playbook can see; a number recomputed from a pasted summary can look precise and still be wrong. So the playbook proposes, designs, audits and visualizes, and the user's testing tool reports the outcome (rule 5).

When a user asks for the reason behind a rule, "that's just the rule" isn't a sufficient answer; the reason is explained in one sentence. Choices specific to this playbook with no counterpart in the literature (the three-box format, the priority tiers, archive curation, the review stamps) are stated as such; they aren't presented as external authority. No rule is defended by citing a specific company, product, or publication: the basis itself (statistical reasoning, repeated observation) is enough.

## Market context: language and market aren't the same thing

*Evidence: industry observation (the behavior classes below are common practice, not verified for your market).* The user's language being Turkish doesn't mean their target market is Turkey; asking in English doesn't mean their market is the US. This archive grew out of Turkish e-commerce practice, and most of its scenarios are universal (buttons, visuals, ordering, search, forms), but some are directly market-dependent, and break when carried to a different market.

**Market-dependent behavior classes** (*Evidence: industry observation*):
- **Payment culture:** Credit-card installments are central to the purchase decision in Turkey, MENA, and Latin America; the US and Northern Europe don't have this mechanism, and the "buy now, pay later" (BNPL) equivalent there has a different target audience and trust perception. Installment-scenario results don't transfer between these markets.
- **Source of trust signal:** Which logo signals trust is market-dependent: in one market a bank/card verification mark is familiar, in another the payment provider's or an independent security seal is the stronger signal.
- **Shipping and returns expectations:** In markets where free, no-questions-asked returns are the standard, an "easy returns" callout isn't differentiating, it's table stakes; in markets with weak return culture it's a strong trust signal. The psychological weight of a free-shipping threshold also shifts with shipping cost as a share of cart size.
- **Price perception:** The charm-pricing effect (ending in 9) isn't a universal law, it's a cultural habit; in some markets specific digits carry separate associations.
- **Support-channel expectations:** Sales support via a messaging app or phone can increase trust in some markets, and weaken the perception of professionalism in others.
- **Enterprise purchasing:** Markets where price transparency is expected behave differently from markets where a quote/negotiation culture dominates.

**Regulation is a separate constraint from market.** Discount and reference-price display, cookie/consent flows, data collection, and subscription cancellation are legally bound in some regions; there, the question "which variant sells more" can only be asked among the variants that are actually permitted. Verify the target market's rule before setting up the test; the playbook doesn't know this and doesn't guess it. In Turkey the discount reference-price rule was amended in 2026 (the reference period is now 10 days); check the current regulation before any discount-display test.

**Application:** When a market-dependent scenario is suggested, this dependency is stated in the output (the "Market note" lines under archive scenarios; a `market` item in the record's `warnings`). If the user's target market is unknown and a market-dependent scenario is being suggested, the market is asked in one sentence (CLAUDE.md rule 19, kind 4); the question doesn't hold the turn, and the scenario is delivered with its `market` warning.

## Where this playbook works well, and where it doesn't

*Evidence: archive practice.* A classic A/B test isn't the right tool for every business model. Fit is evaluated before producing a suggestion, and if it's poor, that's stated plainly. The fit tiers are named differently from the priority tiers (high / medium / low) on purpose: "priority medium or high" (rule 9) never refers to this table.

| Fit | Context |
|---|---|
| Suitable | B2C e-commerce, consumer mobile apps, self-serve SaaS: many visits and a fast, repeated conversion event |
| Conditional | Marketplaces (may have supply/demand side effects), subscriptions, B2B lead forms, pre-quote forms in regulated sectors (insurance, credit: the form and product-selection steps before an offer is made): testable, but low volume, delayed conversion and regulated copy need care |
| Poor fit | Low-traffic enterprise sales pages, long sales cycles (months), heavily regulated flows (insurance/finance/health offer and contract steps), businesses dominated by physical-store effects |

A page known to be low-traffic (the user said so, or it's obvious from the page's nature, e.g. a return form) is noted, in words, as hard to test, and the alternatives below are offered alongside or instead of a classic A/B. Traffic isn't asked for to find this out (rule 5), and no visitor or conversion threshold is quoted.

**What's suggested when the fit is poor (don't leave a dead end):**
- **Qualitative methods:** A 5-8-person usability test, session-recording review, an exit survey: useful for problem detection even on a small sample; it answers "what's wrong," not "which variant won."
- **Before/after measurement (quasi-experiment):** If random splitting isn't possible, compare the before and after periods while noting seasonality/campaign effects; the causal claim is weak, and that's stated explicitly.
- **A bolder change:** a subtle change on a low-traffic page is hard to tell apart from noise; a structural change gives the test a chance of showing something.
- **Move it upstream:** Run the test on a higher-traffic step of the funnel that carries the same problem, not on the low-traffic sub-page.
- **In regulated flows:** a variant that changes legal text, a mandatory disclosure or price transparency isn't tested until the rule is verified; one that changes none of these is produced with compliance sign-off as a pre-start gate, whatever the fit tier (Regulated flows).

## Scope: single-variable A/B, not multivariate (MVT)

*Evidence: archive practice (a scope choice).* This playbook only produces and audits **single-variable A/B tests**. Multivariate testing (MVT), where several elements (headline + image + button color) are tested together in different combinations, is out of scope. Reason: MVT splits visitors across every **combination**, so it needs far more traffic than a single A/B test, and as the number of combinations grows, telling which element drove the effect gets harder, and our whole framework (single variable, the scenario record, confound audit) is built around one variable. If the user wants to test multiple elements at once, `ab-test-design` splits this into separate single-variable tests (Variable isolation) and, if MVT is genuinely needed (a question about interaction between elements), states plainly that this is out of the playbook's scope.

## Regulated flows

*Evidence: binding rule 11; which rule applies is the target market's, verified by the user's compliance team, never guessed.* Legally bound areas: discount display, consent flows, subscription cancellation, credit cost and rate display, insurance or pension offer and contract steps, and any copy that states why personal data is collected or how it is used (it must match the published privacy notice).

- **(a) A variant that changes a regulated display** (legal text, a mandatory disclosure, consent wording, a price, rate, cost or return figure, data-purpose copy that says more than the published notice) is held until the target market's rule is verified.
- **(b) A variant inside such a flow that changes no regulated display** is produced with compliance sign-off on B's exact copy as a pre-start gate. It is carried as the record's `regulation` warning, written in the chat's pre-start line ("Başlamadan önce:" / "Before you start:"; `Pre-start gates` in the setup notes when they are written) and, in the detail view, as one Never-do item; the test takes no traffic before that sign-off.
- **A rule-14 reason or data-assurance line** next to a field that only restates the purpose the published privacy notice already states is not a changed display: it is produced under (b), and compliance checks its exact wording against the notice before traffic.
- **A mandatory notice missing from the page** is reported as a compliance finding, not turned into a test.
- **Mechanical checks:** the validator refuses a regulated-looking record without a `regulation` warning; `build_card.py` refuses a card whose B drops legal or mandatory text that A shows (a changed regulated display, so it is held).

## Sensitive fields

*Evidence: binding rule 14; the intermediate methods are common form practice (industry observation).* If a sensitive field like an ID number, birth date, income or address is causing friction, a variant isn't built as a direct "remove the field": most of these fields aren't technically mandatory, and there are several methods in between. They are evaluated first, and one is tested as the single variable:

- **Make it optional:** the field stays but is no longer required.
- **Give a reason:** why it's asked for is written next to the field ("Your advisor will need this to prepare the offer").
- **Defer it:** the information is collected at a later touchpoint, not this step.
- **Ask for less data:** a year instead of a full date, only as many digits as verification needs instead of the full number.
- **Data-assurance signal:** how the information is protected and not shared is stated next to the field.

Removing the field entirely is suggested only if it's genuinely possible operationally and legally; the playbook doesn't assume it, it asks the user (CLAUDE.md rule 19, kind 7), and the record carries a `feasibility` warning until then. A variant that changes several of them at once isn't built (rule 4). A reason or data-assurance line that only restates the purpose the published privacy notice already states is produced under Regulated flows case (b).

## Ethical and legal boundaries

*Evidence: binding rules 6 and 11; the two ranking and prevalence remarks below are industry observation and are labelled where they appear.*

- Showing a price that was never actually charged as the "old price" is a legal risk (reference-price regulation).
- Highlighting the monthly installment amount while hiding the total amount is a legal risk (price and credit-cost transparency rules); verify the target market's rule.
- Don't suggest a variant that produces a dark pattern: an unclosable modal, a hidden cancellation condition, false stock information.

**Protections aren't test subjects.** Security and compliance controls (bot verification such as CAPTCHA, identity or age verification, two-step login, transaction confirmation, legal consent steps) exist for protection, not conversion; removing or weakening them can't be justified by a conversion metric, so they aren't presented as friction-reduction candidates. Improvement there is separate work with the security or compliance team.

**Urgency, scarcity and social proof are verified first:** (a) does the offer really end when the timer hits zero, or does it restart with the same offer; (b) does the stock count come from real inventory, or is it scheduled or randomly generated; (c) does the viewer count come from real traffic. Unverifiable → not suggested: not only an ethics question but a direct legal risk in some markets (EU, US). The validator refuses urgency or scarcity wording in B without a `regulation` warning naming the real data source.

**Ranking evidence/trust signals.** If a variant aims to increase trust (a reference, a badge, a statistic, a case example), they aren't all equally weighted: evidence with context and a real number is stronger than a generic one (e.g. a named reference with a concrete result is more persuasive than a plain logo strip). A concrete number looks more credible than a rounded one, and it usually is more real too ("2,487 users" instead of "2,500 users," when the real figure is available) (*Evidence: industry observation*). Evidence is placed at the point of most hesitation (e.g. next to the payment form), not buried in an FAQ. Rule 6 already applies: a certification you don't hold, a made-up statistic, or a fake reference isn't suggested; this item only describes how to rank real evidence.

**Manipulative-variant check.** When there's doubt about whether a variant is a dark pattern, 5 questions are asked in order: (1) Does it put a deliberately unequal burden between the options presented to the user (asymmetric)? (2) Is its effect hidden from the user (covert)? (3) Does it create a false belief, through an exaggerated claim, missing information, or misleading wording (deceptive)? (4) Does it delay or hide necessary information (hides information)? (5) Does it narrow the user's set of choices (restrictive)? A single "yes" refuses the variant: it isn't suggested until it is revised so that every answer is "no". Countdown timers and "low stock" messages are often driven by scheduled or random generation rather than real data (*Evidence: industry observation*), which is why rule 6 asks for the signal to be verified before it's suggested (CLAUDE.md rule 6).
