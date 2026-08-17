# Contributing

## Adding a scenario

Follow the three-box format used by the existing files in `knowledge/scenarios/`:

- **Test edilmesi gerekenler** — exactly 5 items, each `Etiket: soru?`
- **Takip edilecek ana KPI'lar** — exactly 5 items, first one is the primary metric, at least one is a guardrail
- **Yapılmaması gerekenler** — exactly 5 items, at least one protects variable isolation

The full rules — box format, evidence labeling, market-context notes — are in [`knowledge/methodology.md`](knowledge/methodology.md) and [`CLAUDE.md`](CLAUDE.md).

Then run the validator before opening a PR:

```bash
python3 scripts/validate_scenarios.py
```

It enforces five items per box, a guardrail in the KPI list, a device/segment question, and typographic rules (curly apostrophe in box headers, no straight quotes).

## Changing a skill

- Skill instructions live in `skills/*/SKILL.md`. Keep the `metadata` block current — bump `version` on a behavior change, update `updated` (YYYY-MM-DD) on any substantive revision.
- Skills that render output (`ab-test-card`) must keep following `knowledge/mockup-style.md` for visual conventions — don't invent new markup ad hoc.
- `CLAUDE.md`'s 16 rules are binding across every skill; a change that would violate one of them needs the rule updated first, not worked around.

## Testing

```bash
python3 -m pytest tests/
python3 scripts/validate_scenarios.py
```

Both run in CI (`.github/workflows/validate.yml`) on every PR.

## Language

Scenario content is Turkish — the archive's native language and where the underlying real-world test data comes from. Code, skill instructions, and repo docs are English. Don't translate scenario content into English; the skills already answer in whatever language the user writes in.
