# Contributing

## Adding a scenario

Follow the three-box format used by the existing files in `knowledge/scenarios/`:

- A `Değişken: … · Fark: …` line under the title: the one variable and the difference type (`değiştir`, `ekle`, `taşı`, `kaldır`).
- **Test edilmesi gerekenler**: exactly 5 items, each `Etiket: soru?`
- **Takip edilecek ana KPI’lar**: exactly 5 items, the first one is the primary metric, at least one is a guardrail that measures an independent harm (never the complement of the primary)
- **Yapılmaması gerekenler**: exactly 5 items, at least one protects variable isolation (`Aynı testte … değiştirmeyin`)

"Exactly 5" applies to the archive files. A scenario designed for a user's page carries 3 to 6 items per box.

The full rules (box format, evidence labeling, market-context notes) are in [`knowledge/methodology.md`](knowledge/methodology.md) and [`CLAUDE.md`](CLAUDE.md).

Then run the repo checks before opening a PR (see [Before you open a PR](#before-you-open-a-pr)). The scenario validator inside them enforces five items per box, a guardrail in the KPI list, a device/segment question, and typographic rules (curly apostrophe in box headers, no straight quotes). It also prints the new scenario total: every place the docs state that number (both READMEs, `docs/llms.txt`, `docs/index.html`, `docs/architecture.md`, the plugin manifests) has to be updated in the same change, and `validate.sh` fails until it is. A new scenario file also needs a line in the stage map of `skills/ab-test-suggest/SKILL.md`; without it the file is never reached.

## Changing a skill

- Skill instructions live in `skills/*/SKILL.md`. Keep the `metadata` block current — bump `version` on a behavior change, update `updated` (YYYY-MM-DD) on any substantive revision.
- Skills that render output (`ab-test-card`) must keep following `knowledge/mockup-style.md` for visual conventions — don't invent new markup ad hoc.
- `CLAUDE.md`'s 19 rules are binding across every skill; a change that would violate one of them needs the rule updated first, not worked around. Adding a rule changes the rule count the docs quote, which `validate.sh` checks too.
- Skill instructions address every shipped file as `${CLAUDE_PLUGIN_ROOT}/knowledge/...`, `${CLAUDE_PLUGIN_ROOT}/scripts/...` or `${CLAUDE_PLUGIN_ROOT}/templates/...`. A bare `knowledge/...` path resolves against the user's project at runtime and silently finds nothing; `validate.sh` rejects it.
- Keep each skill's `description` at or under 1024 characters; it is the only text the router sees before picking a skill.

## Before you open a PR

Requires `python3` 3.9 or newer; nothing to install, the scripts are standard-library only.

```bash
# 1. Unit tests (stats engine, validators, card builder)
python3 -m unittest discover -s tests      # or: python3 -m pytest tests -q

# 2. Regenerate the derived bundles after editing CLAUDE.md, skills/, agents/,
#    README.md, FAQ.md, docs/architecture.md or knowledge/methodology.md
python3 scripts/build_gemini.py && python3 scripts/build_llms_full.py

# 3. Repo consistency: scenario archive, frontmatter, links, plugin-root paths,
#    rule citations, stated counts, and that the bundles above are current
bash scripts/validate.sh
```

All three run in CI (`.github/workflows/validate.yml`) on every PR; the unit tests run on Python 3.9 and 3.13. A red `validate.sh` section 16 or 17 almost always means step 2 was skipped.

## Language

Scenario content is Turkish — the archive's native language and where the underlying real-world test data comes from. Code, skill instructions, and repo docs are English. Don't translate scenario content into English; the skills already answer in whatever language the user writes in.
