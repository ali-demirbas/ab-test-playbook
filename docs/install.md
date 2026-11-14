# Install, update and troubleshooting

**Language:** [English](install.md) · [Türkçe](install.tr.md)

The short version is in the [README](../README.md): two commands in Claude Code, plus one optional command for the visual check. This page holds everything else: the other ways to install, how the visual check works, updating, and what to do when something looks off.

A/B Test Builder is the display name. The plugin installs as `ab-test-playbook`.

## Requirements

| What | Needed for | Check it with |
|---|---|---|
| Claude Code | Everything | `claude --version` |
| Python 3.9 or newer | Everything (standard library only, nothing to `pip install`) | `python3 --version` |
| Node.js 18 or newer, Playwright and Chromium | Only the final visual check of a card. Without it you still get every card, as a preview that has not been visually checked | `node --version` |

**Requirements:** Claude Code, and `python3` 3.9 or newer on your PATH. The scripts use the Python standard library only; there is nothing to `pip install`. A final card also needs the visual check (`scripts/render_check.mjs`), which runs on Node and Playwright with Chromium (see Visual check below). Without it you get only an unverified preview, never a final card.

## Claude Code (recommended)

```
/plugin marketplace add ali-demirbas/ab-test-playbook
/plugin install ab-test-playbook@ab-test-playbook
```

A/B Test Builder is the display name; the plugin installs as `ab-test-playbook`, and every command uses that name.

Or clone and add as a local plugin:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git
claude --plugin-dir ./ab-test-playbook
```

## Other ways to install

**Skills only, limited.** The skills CLI can copy the five skill instructions on their own:

```bash
npx skills add ali-demirbas/ab-test-playbook --all
```

That route ships each skill's `SKILL.md` and nothing else: no binding rules (`CLAUDE.md`), no scenario archive, no scripts, no review agents. Every skill resolves those through the plugin root, so archive suggestions, scenario validation and card rendering won't work. Use the plugin install above for the full engine.

Using [Gemini CLI](https://github.com/google-gemini/gemini-cli) instead? `.gemini/extensions/ab-test-playbook/` ships the same skills, rules and review agents, generated from the same source files by `scripts/build_gemini.py`:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git
cd ab-test-playbook/.gemini/extensions/ab-test-playbook && gemini extensions link .
```

**Codex.** The repo also carries a Codex plugin manifest (`.codex-plugin/plugin.json`) and marketplace (`.agents/plugins/marketplace.json`):

```bash
codex plugin marketplace add ali-demirbas/ab-test-playbook
```

Then open `/plugins` in a Codex session and install **ab-test-playbook**. Codex installs the five skills with the rules, archive and scripts next to them; the two review agents are Claude Code subagents, and this route is not tested as fully as the Claude Code plugin.

**claude.ai (skill upload).** Each skill can be packaged as a ZIP that carries its own copy of the rules, the scenario archive, the templates and the scripts:

```bash
git clone https://github.com/ali-demirbas/ab-test-playbook.git && cd ab-test-playbook
python3 scripts/build_skill_zips.py --out dist
```

Upload each `dist/<skill>.zip` in Customize > Skills > + > Create skill > Upload a skill, with code execution turned on under Settings > Capabilities. Upload all five, since `ab-test` routes to the other four. claude.ai limits a skill description to 200 characters, so the ZIPs use a shorter, reviewed description; the instructions are unchanged. There is no headless Chromium there, so cards come out as previews labelled UNVERIFIED, as described under Visual check.

## Visual check (needed for a final card)

A card becomes final only after `scripts/render_check.mjs` has rendered it in Chromium and the mockup reviewer has looked at the image. The rest of the playbook stays Python standard library; this part needs Node.js 18 or newer. Install Playwright once, outside the repo:

```bash
npm i --prefix ~/.abtest-visual playwright && npx --prefix ~/.abtest-visual playwright install chromium
```

`render_check.mjs` finds `~/.abtest-visual/node_modules` on its own. On Linux, add `--with-deps` after `install` to get the system libraries too. Set `NODE_PATH` only for a Playwright installed somewhere else, and `CHROMIUM_PATH=/path/to/chrome-headless-shell` only for a browser binary of your own. To test it, go to your clone first:

```bash
cd ab-test-playbook
node scripts/render_check.mjs --strict docs/demo/scenario-card.html
```

The last stderr line names the outcome:

| Exit | Outcome | Meaning |
|---|---|---|
| 0 | `VERIFIED` | Rendered, no error |
| 1 | `VISUAL_CHECK_FAILED` | Rendered, the card has a layout error to fix |
| 2 | usage error | Unknown flag, no card, missing file |
| 3 | `VISUAL_CHECK_UNAVAILABLE` | Playwright or Chromium missing, nothing measured |

With exit 3 the reviewer's verdict is `UNVERIFIED`, so no card becomes final: you get the draft as a preview clearly labelled UNVERIFIED. Once the check is installed, the same draft is checked and finished. `--shot` and `--half` write `card-<name>.png` and `card-<name>-800.png` next to the card. A final build writes `card-<name>.png` next to the card as well (`--no-png` skips it).

## Update

```
/plugin marketplace update ab-test-playbook
/plugin update ab-test-playbook@ab-test-playbook
```

Updates arrive only when the plugin's version number changes. `/plugin` shows the installed version; if it is behind the [CHANGELOG](../CHANGELOG.md), run both commands and restart Claude Code. A local clone updates with `git pull`.

**`claude plugin validate` on an older Claude Code.** Releases that predate plugin relevance suggestions (2.1.117, for example) report `Unrecognized key: "relevance"` for `.claude-plugin/marketplace.json`. It is safe: that key only lets Claude Code suggest the plugin, adding, installing and updating work on those releases, and current releases validate it.

## Troubleshooting

| What you see | What it means | What to do |
|---|---|---|
| A card arrives as a preview labelled UNVERIFIED | The visual check is not installed, so nothing was measured. The scenario and its review are complete; only the last visual check is missing | Run the one-time Playwright command under [Visual check](#visual-check-needed-for-a-final-card). The same draft is then checked and finished |
| `VISUAL_CHECK_UNAVAILABLE` (exit 3) from `render_check.mjs` | Playwright or Chromium is missing or did not start | Same command. On Linux add `--with-deps` after `install` |
| Suggestions, validation or cards do not work after `npx skills add` | That route copies only the skill instructions | Use the plugin install at the top of this page |
| `/plugin update` brings nothing new | Updates arrive only when the version number changes | Run both update commands, then restart Claude Code |
| `Unrecognized key: "relevance"` from `claude plugin validate` | An older Claude Code release | Safe to ignore, see the note under [Update](#update) |
| `python3: command not found`, or a script stops on start | Python 3.9 or newer is not on your PATH | Install a current Python 3 and reopen the terminal |

Still stuck? [Open an issue](https://github.com/ali-demirbas/ab-test-playbook/issues) and include the last line the command printed.
