#!/usr/bin/env python3
"""Concatenate the repo's core documents into docs/llms-full.txt.

Why generated rather than hand-written: a full-text bundle is only useful while
it matches the documents it bundles, and a hand-maintained copy silently rots
the first time README or CLAUDE.md changes. Generating it means `validate.sh`
can diff the committed file against a fresh build and fail the run when they
diverge — the same reasoning as build_card.py self-verifying against drift.

Why this file exists at all: when someone pastes a repo URL into a chat tool,
the assistant fetches HTML and burns most of its budget on markup. A single
Markdown bundle is the cheapest complete answer to "what is this project". The
narrower `docs/llms.txt` is the index; this is the whole thing.

Usage:
  build_llms_full.py                 # write docs/llms-full.txt
  build_llms_full.py --check         # exit 1 if the committed file is stale
"""
import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "docs", "llms-full.txt")

# Order matters: what the project is, then the rules that constrain it, then
# how it is put together, then the questions people actually arrive with.
SOURCES = [
    ("README.md", "Overview"),
    ("CLAUDE.md", "Binding rules"),
    ("docs/architecture.md", "Architecture"),
    ("FAQ.md", "FAQ"),
    ("knowledge/methodology.md", "Methodology"),
]

HEADER = """# ab-test-playbook — full text

> Single-file bundle of this project's core documentation, generated from the
> repository by scripts/build_llms_full.py. An A/B testing and CRO engine for
> Claude Code: scenario suggestion from a 179-scenario archive, single-variable
> test design, methodology audit, real two-proportion z-test math, and a
> self-contained HTML card per scenario.
>
> Source: https://github.com/ali-demirbas/ab-test-playbook (MIT)

"""


def build():
    parts = [HEADER]
    for rel, label in SOURCES:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            sys.stderr.write("build_llms_full: skipping missing %s\n" % rel)
            continue
        with open(path, encoding="utf-8") as fh:
            body = fh.read().strip()
        parts.append("\n\n---\n\n# %s — %s\n\n%s\n" % (label, rel, body))
    return "".join(parts)


def main(argv):
    ap = argparse.ArgumentParser(description="Build docs/llms-full.txt from the core docs.")
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if the committed file is out of date")
    args = ap.parse_args(argv)

    built = build()

    if args.check:
        if not os.path.isfile(OUT):
            print("docs/llms-full.txt is missing — run scripts/build_llms_full.py")
            return 1
        with open(OUT, encoding="utf-8") as fh:
            current = fh.read()
        if current != built:
            print("docs/llms-full.txt is stale — run scripts/build_llms_full.py")
            return 1
        print("  ok: docs/llms-full.txt matches its sources")
        return 0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(built)
    print("wrote %s (%d bytes from %d sources)" % (OUT, len(built.encode("utf-8")), len(SOURCES)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
