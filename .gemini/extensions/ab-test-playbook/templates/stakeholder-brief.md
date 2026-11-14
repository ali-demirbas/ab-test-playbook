# Stakeholder brief

The last block of a turn that delivered cards (CLAUDE.md rule 9), before the turn's one question: one brief, for scenario 1 only (another on request), in the record's language. It carries only what the record, the card and the tag line don't: why now, and the three possible outcomes with the next steps open to the owner. The title, problem, A and B, KPI and guardrail are already in the record and on the card, and aren't repeated here (rule 9).

Nothing is pre-decided. Each outcome names the testing tool's result in words and leaves the decision with its owner, listing the options; no ship or revert command, no statistic, threshold, margin or number the user didn't give (rules 5, 10). Asked for as a file: the same block as `abtest-brief-<slug>.md`, never unasked.

Fill: `Neden şimdi` / `Why now` is what the evidence rests on, in plain words (from `evidence.note`; the evidence label is already in the tag line). The three outcome lines are fixed wording.

```
**Karar özeti: <n>. senaryo**
Neden şimdi: <what the evidence rests on>.
B önde çıkarsa (test aracının sonucuna göre): karar sahibinde; olası adım B’yi yaymak.
B geride kalırsa: karar sahibinde; olası adım A’da kalıp öğrenileni test geçmişine yazmak.
Belirgin fark yoksa: karar sahibinde; olası adımlar A’da kalmak, aynı soruna daha cesur tek bir değişiklik denemek ya da konuyu kapatmak.
```

```
**Stakeholder brief: scenario <n>**
Why now: <what the evidence rests on>.
If B leads (per the testing tool's result): the owner's call; a possible step is rolling B out.
If B trails: the owner's call; a possible step is keeping A and recording the learning in your test history.
If no clear difference: the owner's call; possible steps are keeping A, trying a bolder single change on the same problem, or closing the topic.
```
