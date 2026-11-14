# Stakeholder brief

The last block of a turn that delivered cards (CLAUDE.md rule 9), before the turn's one question: one brief, for scenario 1 only (another on request), in the record's language. Every value comes from the record, the page or the user; nothing is invented. No statistic, threshold or number the user didn't give (rules 5, 10): the outcomes name the testing tool's result in words. Asked for as a file: the same block as `abtest-brief-<slug>.md`, never unasked.

Fill: `Soru` / `Question` is the title; `Neden şimdi` / `Why now` the problem plus the evidence label and what it rests on; `Ne değişiyor` / `What changes` A and B in a few words; the KPI and guardrail with their denominators. A guardrail check is written "<criterion> (yayın öncesi, geçti/kaldı)" / "(before launch, pass/fail)". The margin is the user's figure when they gave one, else the fixed wording below.

```
**Karar özeti: <n>. senaryo**
Soru: <title>
Neden şimdi: <problem>; kanıt: <kendi verin / arşiv örüntüsü / sektör gözlemi / sezgi>, <what it rests on>.
Ne değişiyor: <A> yerine <B>; başka hiçbir şey değişmez.
Birincil KPI: <primary_kpi.name> (<denominator>).
Guardrail: <guardrail.name> <düşmemeli / artmamalı> (<denominator>); tolerans payını test aracında sahibi belirler.
B kazanırsa (test aracının sonucuna göre): B yayına alınır.
B kaybederse: A’ya dönülür, öğrenilen kendi test geçmişine yazılır.
Belirgin fark yoksa: A kalır; aynı soruna daha cesur tek bir değişiklik denenir ya da konu kapatılır.
```

```
**Stakeholder brief: scenario <n>**
Question: <title>
Why now: <problem>; evidence: <your own data / archive pattern / industry observation / intuition>, <what it rests on>.
What changes: <B> instead of <A>; nothing else changes.
Primary KPI: <primary_kpi.name> (<denominator>).
Guardrail: <guardrail.name> must not <drop / rise> (<denominator>); the tolerated margin is the owner's call, set in the testing tool.
If B wins (per the testing tool's result): ship B.
If B loses: revert to A and record the learning in your test history.
If no clear difference: keep A; try a bolder single change on the same problem, or stop.
```
