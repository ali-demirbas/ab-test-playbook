#!/usr/bin/env python3
"""render_check.mjs için hafif testler. Bağımlılıksız (unittest).

Ölçüm Playwright ister ve bu paketin bağımlılığı değildir; burada yalnızca
tarayıcı gerektirmeyen davranış sabitlenir: betik sözdizimi, bilinmeyen
seçeneğin reddi ve ölçüm kurallarının kaynakta durması. Node yoksa atlanır.
"""
import os
import shutil
import subprocess
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "render_check.mjs")
NODE = shutil.which("node")

with open(SCRIPT, encoding="utf-8") as _fh:
    SOURCE = _fh.read()


@unittest.skipUnless(NODE, "node bulunamadı")
class TestCli(unittest.TestCase):
    def test_syntax(self):
        self.assertEqual(subprocess.run([NODE, "--check", SCRIPT], capture_output=True).returncode, 0)

    def test_unknown_option_is_refused_before_anything_runs(self):
        p = subprocess.run([NODE, SCRIPT, "--shots", "card.html"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("--shots", p.stderr)

    def test_no_file_is_a_usage_error(self):
        self.assertEqual(subprocess.run([NODE, SCRIPT, "--json"], capture_output=True).returncode, 2)


class TestMeasurementRules(unittest.TestCase):
    """The rules the audit found missing stay in the source."""

    def test_label_is_measured_as_its_border_box(self):
        for prop in ("paddingLeft", "paddingRight", "paddingTop", "paddingBottom"):
            self.assertIn("cs.%s" % prop, SOURCE)
        self.assertIn('cs.boxSizing === "border-box"', SOURCE)

    def test_label_is_compared_with_painted_boxes_not_only_glyphs(self):
        self.assertIn("paintsBox", SOURCE)
        self.assertIn('frame.querySelectorAll("*")', SOURCE)

    def test_shift_is_never_printed_as_n_apx(self):
        self.assertNotIn('?? "n/a"}px', SOURCE)
        self.assertIn("element height", SOURCE)
        self.assertIn("more than the", SOURCE)

    def test_clipping_is_measured_against_the_screen_and_sideways(self):
        self.assertIn("below the screen", SOURCE)
        self.assertIn("scrollWidth", SOURCE)
        self.assertNotIn("below the frame", SOURCE)


if __name__ == "__main__":
    unittest.main()
