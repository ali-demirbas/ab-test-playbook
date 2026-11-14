#!/usr/bin/env python3
"""feasibility.py: the rough MDE from the user's own numbers (CLAUDE.md rule 5).

The formula is checked against values computed by hand, the verdict bands at
their edges, and the inputs for clear errors without a traceback.
"""
import io
import math
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "feasibility.py")
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import feasibility as fz  # noqa: E402


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        try:
            code = fz.main(list(args))
        except SystemExit as exc:  # argparse's own usage errors
            code = exc.code
    return code, out.getvalue(), err.getvalue()


class TestFormula(unittest.TestCase):
    def test_hand_computed_values(self):
        # p = 0.025, 1,200 a day, 2 arms, 2 weeks: n = 1200*14/2 = 8400 per arm
        # sqrt(2*0.025*0.975/8400) = 0.00240906; * 2.80158522 = 0.00674920; / 0.025 = 0.269968
        self.assertAlmostEqual(fz.relative_mde(0.025, 1200, 2, 2), 0.269968, places=5)
        # 4 weeks doubles n: the MDE shrinks by sqrt(2)
        self.assertAlmostEqual(fz.relative_mde(0.025, 1200, 2, 4), 0.269968 / math.sqrt(2), places=5)
        # p = 0.10, 10,000 a day, 2 arms, 2 weeks: n = 70,000; sqrt(0.18/70000) = 0.00160357
        # * 2.80158522 = 0.00449254; / 0.10 = 0.0449254
        self.assertAlmostEqual(fz.relative_mde(0.10, 10000, 2, 2), 0.0449254, places=6)

    def test_more_arms_split_the_traffic(self):
        # three arms: n per arm is 2/3 of the two-arm n, so the MDE grows by sqrt(3/2)
        self.assertAlmostEqual(fz.relative_mde(0.025, 1200, 3, 2) / fz.relative_mde(0.025, 1200, 2, 2),
                               math.sqrt(1.5), places=9)

    def test_z_values(self):
        self.assertAlmostEqual(fz.Z_ALPHA + fz.Z_POWER, 2.8015852, places=6)


class TestVerdict(unittest.TestCase):
    def test_band_edges(self):
        self.assertEqual(fz.verdict(0.05), "small_ok")
        self.assertEqual(fz.verdict(0.0501), "small_no")
        self.assertEqual(fz.verdict(0.15), "small_no")
        self.assertEqual(fz.verdict(0.1501), "bold_only")
        self.assertEqual(fz.verdict(0.30), "bold_only")
        self.assertEqual(fz.verdict(0.3001), "not_testable")

    def test_verdict_reads_the_longest_run(self):
        # 2 weeks ~27% and 4 weeks ~19%: both bold-only; 1 week alone is ~38%: not testable
        _, key = fz.report(0.025, 1200, 2, [4, 2], "en")
        self.assertEqual(key, "bold_only")
        _, key = fz.report(0.025, 1200, 2, [1], "en")
        self.assertEqual(key, "not_testable")


class TestOutput(unittest.TestCase):
    def test_turkish_default_two_lines(self):
        code, out, err = run("--rate", "0.025", "--visitors", "1200")
        self.assertEqual(code, 0, err)
        lines = out.strip().split("\n")
        self.assertEqual(len(lines), 2, out)
        self.assertIn("2 haftada yaklaşık %27, 4 haftada yaklaşık %19", lines[0])
        self.assertIn("günde 1.200 uygun ziyaretçi", lines[0])
        self.assertIn("Yalnızca cesur değişiklikler ölçülebilir.", lines[0])
        self.assertTrue(lines[1].startswith("Kaba bir normal yaklaşım"), lines[1])
        self.assertNotIn("—", out)

    def test_english(self):
        code, out, _ = run("--rate", "2.5%", "--visitors", "1,200", "--lang", "en")
        self.assertEqual(code, 0)
        self.assertIn("about 27% in 2 weeks, about 19% in 4 weeks", out)
        self.assertIn("Detectable for bold changes only.", out)
        self.assertIn("not a promise of a result", out)

    def test_period_conversion_is_done_by_the_script(self):
        _, by_month, _ = run("--rate", "0.03", "--visitors", "40000", "--per", "month", "--lang", "en")
        _, by_day, _ = run("--rate", "0.03", "--visitors", str(40000 / 30.0), "--lang", "en")
        self.assertEqual(by_month.split("arms)")[1], by_day.split("arms)")[1])

    def test_custom_weeks_and_arms(self):
        code, out, _ = run("--rate", "0.05", "--visitors", "5000", "--arms", "3", "--weeks", "3", "--lang", "en")
        self.assertEqual(code, 0)
        self.assertIn("3 arms", out)
        self.assertIn("in 3 weeks", out)
        self.assertNotIn("in 2 weeks", out)

    def test_low_traffic_is_not_testable(self):
        _, out, _ = run("--rate", "0.02", "--visitors", "300", "--lang", "en")
        self.assertIn("Not testable at this traffic.", out)


class TestInputs(unittest.TestCase):
    def test_rate_strictly_between_zero_and_one(self):
        for bad in ("0", "1", "1.5", "-0.1", "abc", "nan", "100%", "0%"):
            code, out, err = run("--rate", bad, "--visitors", "1000", "--lang", "en")
            self.assertEqual(code, 2, bad)
            self.assertEqual(out, "")
            self.assertIn("between 0 and 1", err)

    def test_turkish_percent_forms(self):
        for good in ("%2,5", "2,5%", "%2.5", "0,025"):
            code, out, _ = run("--rate", good, "--visitors", "1200", "--lang", "en")
            self.assertEqual(code, 0, good)
            self.assertIn("27%", out, good)

    def test_visitors_positive(self):
        for bad in ("0", "-5", "many", "inf"):
            code, _, err = run("--rate", "0.02", "--visitors", bad, "--lang", "en")
            self.assertEqual(code, 2, bad)
            self.assertIn("positive number", err)

    def test_arms_and_weeks(self):
        self.assertIn("at least 2", run("--rate", "0.02", "--visitors", "100", "--arms", "1", "--lang", "en")[2])
        self.assertIn("weeks must be", run("--rate", "0.02", "--visitors", "100", "--weeks", "0", "--lang", "en")[2])

    def test_turkish_errors_start_with_a_capital(self):
        _, _, err = run("--rate", "2", "--visitors", "100")
        self.assertTrue(err.startswith("Hata:"), err)

    def test_cli_never_prints_a_traceback(self):
        for args in (["--rate", "x", "--visitors", "1"], ["--visitors", "1"], ["--rate", "0.1", "--visitors", "1e999"]):
            proc = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0, args)
            self.assertNotIn("Traceback", proc.stderr, args)


if __name__ == "__main__":
    unittest.main()
