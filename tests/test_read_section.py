"""scripts/read_section.py: the one reader the skills use instead of awk and sed."""
import io
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import read_section  # noqa: E402

DOC = """# Title

Intro line.

## First part

Body one.

```bash
# a comment, not a heading
## neither is this
```

### A child

Child body.

## Second part (with a note)

Body two.

---

## Third

Body three.
"""


def run(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = read_section.main(args)
    return code, out.getvalue(), err.getvalue()


class TestReadSection(unittest.TestCase):
    def setUp(self):
        fh = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        fh.write(DOC)
        fh.close()
        self.path = fh.name
        self.addCleanup(os.unlink, self.path)

    def test_a_section_runs_to_the_next_heading_of_its_level(self):
        code, out, _ = run([self.path, "First part"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("## First part\n"))
        self.assertIn("### A child", out)
        self.assertIn("## neither is this", out)  # fenced lines stay in the section
        self.assertNotIn("Second part", out)
        self.assertTrue(out.endswith("Child body.\n"))

    def test_the_heading_matches_without_hashes_case_and_by_prefix(self):
        for query in ("## Second part (with a note)", "second part", "SECOND", "with a note"):
            code, out, _ = run([self.path, query])
            self.assertEqual(code, 0, query)
            self.assertTrue(out.startswith("## Second part (with a note)\n"), query)
            self.assertEqual(out, "## Second part (with a note)\n\nBody two.\n", query)

    def test_an_exact_title_wins_over_an_earlier_partial_match(self):
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write("\n## Third and more\n\nx\n\n## More\n\ny\n")
        _, out, _ = run([self.path, "more"])
        self.assertTrue(out.startswith("## More\n"))

    def test_several_headings_in_one_call(self):
        code, out, _ = run([self.path, "Third", "A child"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "## Third\n\nBody three.\n\n### A child\n\nChild body.\n")

    def test_a_block_by_line_number_stops_at_the_separator(self):
        line = DOC.split("\n").index("## Second part (with a note)") + 1
        code, out, _ = run([self.path, "--line", str(line)])
        self.assertEqual(code, 0)
        self.assertEqual(out, "## Second part (with a note)\n\nBody two.\n")

    def test_until_prints_everything_above_the_heading(self):
        code, out, _ = run([self.path, "--until", "Second part"])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("# Title\n"))
        self.assertTrue(out.endswith("Child body.\n"))

    def test_list_gives_line_numbers_and_skips_fenced_lines(self):
        code, out, _ = run([self.path, "--list"])
        self.assertEqual(code, 0)
        self.assertEqual(out.split("\n")[:3], ["1:# Title", "5:## First part", "14:### A child"])
        self.assertNotIn("a comment", out)

    def test_a_missing_heading_fails_and_names_the_headings(self):
        code, out, err = run([self.path, "No such part"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("not found", err)
        self.assertIn("## First part", err)

    def test_a_line_out_of_range_and_a_missing_file_fail(self):
        self.assertEqual(run([self.path, "--line", "999"])[0], 1)
        self.assertEqual(run([self.path + ".none", "Third"])[0], 1)

    def test_no_selector_is_a_usage_error(self):
        self.assertEqual(run([self.path])[0], 2)


class TestRealFiles(unittest.TestCase):
    def test_every_methodology_section_a_skill_names_exists(self):
        path = os.path.join(ROOT, "knowledge", "methodology.md")
        for title in ("KPI rules", "Accessibility checks", "Prioritization", "Regulated flows", "Sensitive fields"):
            code, out, _ = run([path, title])
            self.assertEqual(code, 0, title)
            self.assertTrue(out.startswith("## " + title), title)
            self.assertEqual(len(re.findall(r"(?m)^## ", out)), 1, title)

    def test_mockup_style_core_and_on_demand_sections(self):
        path = os.path.join(ROOT, "knowledge", "mockup-style.md")
        code, core, _ = run([path, "--until", "On demand"])
        self.assertEqual(code, 0)
        self.assertIn("## Screen spec", core)
        self.assertNotIn("\n# On demand", core)
        self.assertNotIn("## Components", core)
        for title in ("Components", "Special cases", "Brand", "Card layout", "Draft and final card", "render_check"):
            code, out, _ = run([path, title])
            self.assertEqual(code, 0, title)
            self.assertEqual(len(re.findall(r"(?m)^##? ", out)), 1, title)

    def test_every_archive_block_is_read_alone(self):
        folder = os.path.join(ROOT, "knowledge", "scenarios")
        for name in sorted(os.listdir(folder)):
            if not re.match(r"^[a-z0-9-]+\.md$", name):
                continue  # stage files only; FORMAT.md documents the format and holds no block
            path = os.path.join(folder, name)
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().split("\n")
            starts = [i + 1 for i, l in enumerate(lines) if l.startswith("## ")]
            code, out, _ = run([path, "--line"] + [str(n) for n in starts[:2]])
            self.assertEqual(code, 0, name)
            self.assertEqual(len(re.findall(r"(?m)^## ", out)), len(starts[:2]), name)
            self.assertNotIn("\n---\n", out, name)

    def test_no_instruction_tells_the_model_to_run_awk_or_sed(self):
        paths = [os.path.join(ROOT, "CLAUDE.md")]
        for top in ("skills", "agents", "knowledge"):
            for base, _, files in os.walk(os.path.join(ROOT, top)):
                paths.extend(os.path.join(base, f) for f in files if f.endswith(".md"))
        for path in paths:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            self.assertIsNone(re.search(r"(?<![A-Za-z])(awk|sed) +(-|')", text), path)

    def test_the_skill_zips_carry_the_helper(self):
        import build_skill_zips
        for skill in ("ab-test-design", "ab-test-suggest", "ab-test-card", "ab-test-audit"):
            with open(os.path.join(ROOT, "skills", skill, "SKILL.md"), encoding="utf-8") as fh:
                files = build_skill_zips.runtime_files([fh.read()])
            self.assertIn("scripts/read_section.py", files, skill)


if __name__ == "__main__":
    unittest.main()
