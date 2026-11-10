# Contributing

## Adding a scenario

Follow the three-box format used by the existing files in `knowledge/scenarios/`:

- A `Değişken: … · Fark: …` line under the title: the one variable and the difference type (`değiştir`, `ekle`, `taşı`, `kaldır`).
- **Test edilmesi gerekenler**: exactly 5 items, each `Etiket: soru?`
- **Takip edilecek ana KPI’lar**: exactly 5 items, the first one is the primary metric, at least one is a guardrail that measures an independent harm (never the complement of the primary)
- **Yapılmaması gerekenler**: exactly 5 items, at least one protects variable isolation (`Aynı testte … değiştirmeyin`)

New archive scenarios still use this three-box format. A scenario the playbook produces for a user is a compact scenario record instead (`knowledge/methodology.md` → The scenario record); its three boxes, 3 to 6 items each, exist only in the detail view the user asks for, so "exactly 5" applies to the archive files alone.

The full rules (box format, the scenario record, evidence labeling, market-context notes) are in [`knowledge/methodology.md`](knowledge/methodology.md) and [`CLAUDE.md`](CLAUDE.md).

Then run the repo checks before opening a PR (see [Before you open a PR](#before-you-open-a-pr)). The scenario validator inside them enforces five items per box, a guardrail in the KPI list, a device/segment question, and typographic rules (curly apostrophe in box headers, no straight quotes). It also prints the new scenario total: every place the docs state that number (both READMEs, `docs/llms.txt`, `docs/index.html`, `docs/architecture.md`, the plugin manifests) has to be updated in the same change, and `validate.sh` fails until it is. A new scenario file also needs a line in the stage map of `skills/ab-test-suggest/SKILL.md`; without it the file is never reached.

New archive scenarios keep exactly this format; the quality gates (`knowledge/methodology.md` → Quality gates: invariants, review stamps, the draft and final card) apply to the records and cards the playbook produces, not to `knowledge/scenarios/`.

## Changing a skill

- Skill instructions live in `skills/*/SKILL.md`. Keep the `metadata` block current: bump `version` on a behavior change, update `updated` (YYYY-MM-DD) on any substantive revision.
- Skills that render output (`ab-test-card`) must keep following `knowledge/mockup-style.md` for what a card shows and how it looks: the title, the two mockups, the ring and its label, nothing else. Don't invent new markup ad hoc, and don't put record content back on the card.
- Skills that produce scenarios write the record, not the three boxes, and read the archive through `grep` plus the shortlisted blocks, never a whole stage file; keep both when editing them.
- The scope is fixed by `CLAUDE.md` rule 5: the playbook proposes, designs, audits and visualizes tests. A change that adds result analysis or sample-size, duration or significance math doesn't belong here.
- `CLAUDE.md`'s 19 rules are binding across every skill; a change that would violate one of them needs the rule updated first, not worked around. Adding a rule changes the rule count the docs quote, which `validate.sh` checks too.
- Skill instructions address every shipped file as `${CLAUDE_PLUGIN_ROOT}/knowledge/...`, `${CLAUDE_PLUGIN_ROOT}/scripts/...` or `${CLAUDE_PLUGIN_ROOT}/templates/...`. A bare `knowledge/...` path resolves against the user's project at runtime and silently finds nothing; `validate.sh` rejects it.
- Keep each skill's `description` at or under 1024 characters; it is the only text the router sees before picking a skill.

## Changing a check

A new or changed check in a validator, the card builder or `render_check.mjs` comes with two tests: a negative one (the bad input is refused, and the test asserts the message names the reason) and a positive one (the corrected input passes). A check the gates rely on is an error, not a warning that lets delivery continue. A keyword list stays a named constant with word-boundary matching and is documented as a heuristic.

## Before you open a PR

Requires `python3` 3.9 or newer; nothing to install, the scripts are standard-library only.

```bash
# 1. Unit tests (validators, card builder, layout check)
python3 -m unittest discover -s tests      # or: python3 -m pytest tests -q

# 2. Regenerate the derived bundles after editing CLAUDE.md, skills/, agents/,
#    knowledge/, templates/, scripts/, README.md, FAQ.md or docs/architecture.md
python3 scripts/build_gemini.py && python3 scripts/build_llms_full.py

# 3. Repo consistency: scenario archive, frontmatter, links, plugin-root paths,
#    rule citations, stated counts, and that the bundles above are current
bash scripts/validate.sh
```

All three run in CI (`.github/workflows/validate.yml`) on every PR; the unit tests run on Python 3.9 and 3.13. A red `validate.sh` section 16 or 17 almost always means step 2 was skipped.

## Language

Scenario content is Turkish, the archive's native language and the language its patterns were collected in. Code, skill instructions, and repo docs are English. Don't translate scenario content into English; the skills already answer in whatever language the user writes in.
