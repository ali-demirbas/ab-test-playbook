# Fast mode

Rule 17's exception, only when the user asks for it (`ab-test` → routing table); the core is `knowledge/mockup-style.md`. The producing skill writes the same records and the same chat; the pipeline is shorter:

1. Delivery pipeline step 1 (`ab-test-card`), every record in one call.
2. No critic, render_check or mockup reviewer. One quick draft per record: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_card.py --quick --template ${CLAUDE_PLUGIN_ROOT}/templates/scenario-card.html --scenario <record.json> --out abtest-card-<slug>.draft.html`. It needs no stamp and writes no manifest; the card checks still run; its ribbon says "Hızlı taslak · incelenmedi" / "Quick draft · not reviewed"; `--stamp` refuses it and it never becomes final.
3. Deliver with the skill's Output, the `.draft.html` files as the file names, plus one line after the list, a statement, not the turn's question: TR "Hızlı taslak: kartlar ve kayıtlar henüz incelenmedi. “Tamamla” dersen iki incelemeyi yapıp nihai kartları hazırlarım." EN "Quick drafts: the cards and records are not reviewed yet. Say “finish” and I will run both reviews and build the final cards." Nothing calls a quick draft final, checked or reviewed.

**Finish** ("tamamla", "finish"): the same records from step 2 of the Delivery pipeline (one critic round over all of them, drafts, render_check, the mockup reviewer, final or conditional builds); each reviewed draft replaces its quick draft at the same path. The chat gives the usual Output for the reviewed cards; a record the critic changed in substance or dropped gets one line.

**The quick draft** (`--quick`, fast mode only, CLAUDE.md rule 17): the draft without any review stamp, its ribbon "Hızlı taslak · incelenmedi" / "Quick draft · not reviewed" and `<meta name="abtest-status" content="quick-draft">`; the card checks still run, no manifest is written, `--stamp` refuses it and it never becomes final. "Tamamla" / "finish" replaces it with a reviewed draft at the same path.
