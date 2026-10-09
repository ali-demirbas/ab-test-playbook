---
name: Bug report
about: A skill broke a binding rule, a script returned a wrong number, or a card rendered wrong
title: "[bug] "
labels: bug
---

**What happened**
<!-- One or two sentences. Quote the output line that is wrong. -->

**What should have happened**
<!-- If a binding rule was broken, name it (e.g. "rule 19: two questions in one turn"). -->

**How to reproduce**
- Install route: plugin (`/plugin install ab-test-playbook@ab-test-playbook`) / local `--plugin-dir` / skills only (`npx skills add`, limited, see README)
- Plugin version (`.claude-plugin/plugin.json`):
- `python3 --version`:
- The prompt you gave, or the exact command for a script bug, e.g.
  `python3 scripts/analyze_results.py significance --control-visitors 5000 --control-conversions 250 --variant-visitors 5000 --variant-conversions 290`

**Output**
<!-- Paste the script JSON or the chat output. For a card, attach the HTML file or a screenshot. -->

**Before you submit**
- [ ] I removed real customer data, URLs I can't share and personal information from everything pasted above.
- [ ] `bash scripts/validate.sh` and `python3 -m unittest discover -s tests` pass on my checkout (or I said which one fails).
