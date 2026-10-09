---
name: Scenario proposal
about: Propose a new A/B test scenario for the archive, in the three-box format
title: "[scenario] "
labels: scenario
---

<!--
Scenarios in knowledge/scenarios/ are written in Turkish; English is fine here
and will be translated when the scenario is added. Use exactly the three boxes
below with five items each (CONTRIBUTING.md). No vendor, brand or study names:
state the mechanism, not who reported it.
-->

**Journey stage / file**
<!-- e.g. cart-checkout.md, product-detail.md, forms-signup.md -->

**Title (as a question)**
<!-- e.g. "Does collapsing the coupon field behind a link reduce cart abandonment?" -->

**The one variable**
<!-- Exactly one thing that differs between A and B. -->

**Mechanism**
<!-- Why would this change behavior? Name the user obstacle it removes and the
objection it answers (Trust / Price / Fit / Timing / Effort). "More eye-catching" is not a mechanism. -->

**Evidence level**
<!-- your own test data / an archive precedent / industry observation / intuition -->

**Test edilmesi gerekenler (What to test)**: 5 items, each `Label: question?`, at least one device or segment question
1.
2.
3.
4.
5.

**Takip edilecek ana KPI’lar (Primary KPIs to track)**: 5 items, the first is the primary metric, at least one guardrail in "must not ..." form with a margin
1. Primary:
2.
3.
4.
5. Guardrail:

**Yapılmaması gerekenler (Never do)**: 5 items, at least one protecting variable isolation
1.
2.
3.
4.
5.

**Market or regulation dependency**
<!-- Does this depend on payment culture, price-display law, consent rules? Which market? "None" is a valid answer. -->

- [ ] The variant is not a dark pattern (no fake scarcity, hidden total, fake reference price, unclosable modal) and does not weaken a security or consent step.
