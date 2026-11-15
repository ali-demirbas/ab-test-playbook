#!/usr/bin/env python3
"""Print one part of a markdown file, so a skill never needs awk or sed.

  read_section.py FILE "Heading" ["Heading 2" ...]   one section per heading
  read_section.py FILE --line N [N ...]              the block that starts at line N
  read_section.py FILE --line N [N ...] --lang tr|en an archive block in one language
  read_section.py FILE --until "Heading"             everything above that heading
  read_section.py FILE --list                        the headings, with line numbers

A heading is matched without its leading #, ignoring case: an exact title
first, then a title that starts with the text, then one that contains it.
A section runs to the next heading of the same or a higher level; a block
read by line number also ends at the first `---` separator line (the scenario
archive's block end). A closing `---` is never printed.
Lines inside a code fence are never taken for headings.

--lang reads a bilingual archive block (knowledge/scenarios/FORMAT.md) in one
language: tr stops before its `### EN` line; en prints the title, the head lines
(Değişken, Etiket, EN, EN-Variable) and the English body after `### EN`, or the
whole block when it has no English body yet. Without --lang the block is
printed whole.

Standard library only, Python 3.9. Exit 0 printed, 1 not found, 2 usage.
"""
import argparse
import re
import sys

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t#]*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def headings(lines):
    """[(index, level, title)] for every heading outside a code fence."""
    out = []
    fence = None
    for i, line in enumerate(lines):
        f = FENCE_RE.match(line)
        if f:
            if fence is None:
                fence = f.group(1)
            elif fence == f.group(1):
                fence = None
            continue
        if fence is None:
            m = HEADING_RE.match(line)
            if m:
                out.append((i, len(m.group(1)), m.group(2)))
    return out


def norm(text):
    return " ".join(text.strip().lstrip("#").split()).casefold()


def find(heads, query):
    """The first heading that matches the query best, or None."""
    q = norm(query)
    if not q:
        return None
    tests = (lambda t: t == q, lambda t: t.startswith(q), lambda t: q in t)
    for test in tests:
        for h in heads:
            if test(norm(h[2])):
                return h
    return None


def section_end(lines, heads, start, level, stop_at_rule):
    end = len(lines)
    for i, lvl, _ in heads:
        if i > start and lvl <= level:
            end = i
            break
    if stop_at_rule:
        for i in range(start + 1, end):
            if lines[i].strip() == "---":
                end = i
                break
    return end


def block(lines, heads, start, stop_at_rule):
    level = next((lvl for i, lvl, _ in heads if i == start), 6)
    end = section_end(lines, heads, start, level, stop_at_rule)
    # Trailing blank lines and a closing `---` separator are not part of it.
    while end > start + 1 and lines[end - 1].strip() in ("", "---"):
        end -= 1
    return "\n".join(lines[start:end]) + "\n"


EN_MARKER = "### EN"
HEAD_PREFIXES = ("Değişken:", "Etiket:", "EN:", "EN-Variable:")


def in_language(text, lang):
    """An archive block in one language (FORMAT.md): tr up to `### EN`, en the head plus the English body."""
    lines = text.rstrip("\n").split("\n")
    marker = next((i for i, line in enumerate(lines) if line.strip() == EN_MARKER), None)
    if lang is None or marker is None:
        return text
    if lang == "tr":
        keep = lines[:marker]
    else:
        head = 1
        while head < marker and (not lines[head].strip() or lines[head].startswith(HEAD_PREFIXES)):
            head += 1
        keep = lines[:head] + [""] + lines[marker + 1:]
    while len(keep) > 1 and not keep[-1].strip():
        keep.pop()
    out, blank = [], False
    for line in keep:
        if not line.strip() and blank:
            continue
        blank = not line.strip()
        out.append(line)
    return "\n".join(out) + "\n"


def listing(heads):
    return "".join("%d:%s %s\n" % (i + 1, "#" * lvl, title) for i, lvl, title in heads)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print one part of a markdown file.")
    ap.add_argument("file")
    ap.add_argument("heading", nargs="*", help="section title(s), with or without the leading #")
    ap.add_argument("--list", action="store_true", help="list the headings with their line numbers")
    ap.add_argument("--line", type=int, nargs="+", metavar="N", help="print the block starting at line N")
    ap.add_argument("--until", metavar="HEADING", help="print everything above this heading")
    ap.add_argument("--lang", choices=("tr", "en"),
                    help="with --line: an archive block in one language (tr up to ### EN, en its head and English body)")
    args = ap.parse_args(argv)

    try:
        with open(args.file, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except OSError as exc:
        sys.stderr.write("read_section: cannot read %s: %s\n" % (args.file, exc.strerror or exc))
        return 1
    if lines and lines[-1] == "":
        lines.pop()
    heads = headings(lines)

    if args.list:
        sys.stdout.write(listing(heads))
        return 0

    parts = []
    missing = []
    if args.until:
        h = find(heads, args.until)
        if h is None:
            missing.append(args.until)
        else:
            parts.append("\n".join(lines[:h[0]]).rstrip("\n") + "\n")
    for n in args.line or []:
        if 1 <= n <= len(lines):
            parts.append(in_language(block(lines, heads, n - 1, True), args.lang))
        else:
            missing.append("line %d (the file has %d lines)" % (n, len(lines)))
    for q in args.heading:
        h = find(heads, q)
        if h is None:
            missing.append(q)
        else:
            parts.append(block(lines, heads, h[0], False))
    if not (args.until or args.line or args.heading):
        ap.print_usage(sys.stderr)
        sys.stderr.write("read_section: give a heading, --line N, --until HEADING or --list\n")
        return 2

    sys.stdout.write("\n".join(parts))
    if missing:
        sys.stderr.write("read_section: not found in %s: %s\nHeadings:\n%s"
                         % (args.file, "; ".join(missing), listing(heads)))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
