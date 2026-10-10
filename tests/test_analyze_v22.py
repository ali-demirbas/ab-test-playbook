#!/usr/bin/env python3
"""analyze_results.py v2.2 düzeltmeleri için testler. Her sınıf sessizce yanlış karara yol açan bir
denetim bulgusuna karşılık gelir; beklenen değerler elle hesaplanmıştır (formül yorumda).
"""
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SCRIPT = os.path.join(ROOT, "scripts", "analyze_results.py")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import analyze_results as ar


def setUpModule():
    ar.set_lang("en")


def tearDownModule():
    ar.set_lang("en")


def run_cli(*args):
    out = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)
    return out.returncode, out.stdout, out.stderr


def write(d, name, text, encoding="utf-8"):
    p = os.path.join(d, name)
    with open(p, "w", encoding=encoding) as f:
        f.write(text)
    return p


SIG = ("significance", "--control-visitors", "10000", "--control-conversions", "600",
       "--variant-visitors", "10000", "--variant-conversions", "500")


class TestEffectDirection(unittest.TestCase):
    """Bulgu H1: anlamlı biçimde KÖTÜ bir varyant 'significant' koduyla 'Ship it' satırına yürüyordu."""

    def test_significant_loser_is_never_a_win(self):
        # %6 → %5: z = −3.10, p = 0.00192. Anlamlı ama zararlı yönde.
        r = ar.significance(10000, 600, 10000, 500)
        self.assertTrue(r["is_significant"])
        self.assertEqual(r["effect_direction"], "variant_lower")
        self.assertEqual(r["expected_direction"], "increase")
        self.assertEqual(r["decision_code"], "significant_degradation")
        self.assertIn("degradation", r["decision"])
        self.assertTrue(any("ship" in w.lower() for w in r["warnings"]))

    def test_significant_winner(self):
        r = ar.significance(5000, 250, 5000, 340)
        self.assertEqual(r["effect_direction"], "variant_higher")
        self.assertEqual(r["decision_code"], "significant_improvement")
        self.assertIn("improvement", r["decision"])

    def test_expected_direction_decrease_flips_the_verdict(self):
        # Aşağı iyi olan bir birincil metrik (ör. terk oranı): düşüş iyileşme, artış kötüleşmedir.
        down = ar.significance(10000, 600, 10000, 500, expected_direction="decrease")
        up = ar.significance(10000, 500, 10000, 600, expected_direction="decrease")
        self.assertEqual(down["decision_code"], "significant_improvement")
        self.assertEqual(up["decision_code"], "significant_degradation")
        with self.assertRaises(ValueError):
            ar.significance(10000, 600, 10000, 500, expected_direction="sideways")

    def test_one_sided_test_still_reports_harm(self):
        # --alternative greater ile aynı veri: p = 0.99904 → eskiden 'not_significant', not yok.
        r = ar.significance(10000, 600, 10000, 500, alternative="greater")
        self.assertFalse(r["is_significant"])
        self.assertTrue(r["opposite_direction_significant"])
        self.assertAlmostEqual(r["p_value_opposite_direction"], 0.00096, places=4)
        self.assertEqual(r["decision_code"], "significant_degradation")
        self.assertTrue(r["warnings"])

    def test_one_sided_alternative_sets_or_checks_the_direction(self):
        r = ar.significance(10000, 600, 10000, 500, alternative="less")
        self.assertEqual(r["expected_direction"], "decrease")
        self.assertEqual(r["decision_code"], "significant_improvement")
        with self.assertRaises(ValueError) as cm:
            ar.significance(10000, 600, 10000, 500, alternative="greater", expected_direction="decrease")
        self.assertIn("--alternative", str(cm.exception))

    def test_not_significant_and_interim_carry_direction(self):
        r = ar.significance(5000, 250, 5000, 260)
        self.assertEqual(r["decision_code"], "not_significant")
        self.assertEqual(r["effect_direction"], "variant_higher")
        self.assertFalse(r["opposite_direction_significant"])
        self.assertEqual(ar.significance(1000, 50, 1000, 50)["effect_direction"], "none")
        i = ar.significance(5000, 300, 5000, 240, planned_n=8000)
        self.assertEqual(i["decision_code"], "interim_no_decision")
        self.assertEqual(i["effect_direction"], "variant_lower")

    def test_multi_arm_loser(self):
        m = ar.significance_multi(10000, 600, [(10000, 500), (10000, 610)])
        self.assertEqual(m["comparisons"][0]["decision_code"], "significant_degradation")
        self.assertEqual(m["comparisons"][1]["decision_code"], "not_significant")
        self.assertTrue(m["any_significant_degradation"])
        self.assertFalse(m["any_significant_improvement"])

    def test_continuous_loser(self):
        # 50 → 45, sd 20, n 2000: t = −5 / sqrt(400/2000·2) = −7.906
        r = ar.continuous(control_stats=(2000, 50.0, 20.0), variant_stats=(2000, 45.0, 20.0))
        self.assertTrue(r["is_significant"])
        self.assertEqual(r["effect_direction"], "variant_lower")
        self.assertEqual(r["decision_code"], "significant_degradation")
        ok = ar.continuous(control_stats=(2000, 50.0, 20.0), variant_stats=(2000, 45.0, 20.0),
                           expected_direction="decrease")
        self.assertEqual(ok["decision_code"], "significant_improvement")

    def test_cli_flag_and_text(self):
        rc, out, _ = run_cli(*SIG, "--expected-direction", "decrease")
        self.assertEqual(rc, 0, out)
        self.assertEqual(json.loads(out)["decision_code"], "significant_improvement")
        rc, out, _ = run_cli(*SIG, "--format", "text")
        self.assertIn("significant degradation", out)
        rc, out, _ = run_cli(*SIG, "--format", "text", "--lang", "tr")
        self.assertIn("anlamlı kötüleşme", out)


class TestGuardrailDirectionRequired(unittest.TestCase):
    """Bulgu H2: yön verilmeyince must_not_decrease varsayılıyor, artan iade oranı 'clean' çıkıyordu."""

    def test_missing_direction_is_an_error(self):
        with self.assertRaises(ValueError) as cm:
            ar.significance(20000, 800, 20000, 1000, ni_margin=0.02)
        self.assertIn("--guardrail-direction", str(cm.exception))
        self.assertIn("must_not_increase", str(cm.exception))
        with self.assertRaises(ValueError):
            ar.continuous(control_stats=(200, 2000.0, 400.0), variant_stats=(200, 2100.0, 400.0), ni_margin=0.02)
        with self.assertRaises(ValueError):
            ar.significance_multi(20000, 800, [(20000, 1000), (20000, 900)], ni_margin=0.02)

    def test_guardrail_run_never_calls_a_rising_harm_an_improvement(self):
        # İade oranı %4 → %5, yön must_not_increase: yukarı kötüdür; karar kodu 'iyileşme' olamaz.
        r = ar.significance(20000, 800, 20000, 1000, ni_margin=0.02, guardrail_direction="must_not_increase")
        self.assertEqual(r["expected_direction"], "decrease")
        self.assertEqual(r["decision_code"], "significant_degradation")
        self.assertEqual(r["guardrail_status"], "degraded")
        c = ar.continuous(control_stats=(2000, 2000.0, 400.0), variant_stats=(2000, 2100.0, 400.0),
                          ni_margin=0.02, guardrail_direction="must_not_increase")
        self.assertEqual(c["decision_code"], "significant_degradation")

    def test_cli_missing_direction(self):
        args = ("significance", "--control-visitors", "20000", "--control-conversions", "800",
                "--variant-visitors", "20000", "--variant-conversions", "1000", "--ni-margin", "0.02")
        rc, out, _ = run_cli(*args)
        self.assertEqual(rc, 1)
        self.assertIn("--guardrail-direction", json.loads(out)["error"])
        rc, out, _ = run_cli(*args, "--guardrail-direction", "must_not_increase")
        self.assertEqual(rc, 0, out)
        self.assertEqual(json.loads(out)["non_inferiority"]["status"], "degraded")


class TestHolmOnUnroundedP(unittest.TestCase):
    """Bulgu R1: Holm 5 haneye yuvarlanmış p ile ve kayan noktalı alfa ile çalışıyordu."""

    def test_rounding_edge_is_not_significant(self):
        # Ham p = 0.02500056 → Holm 2·p = 0.0500011 > 0.05. Yuvarlanmış 0.025·2 = 0.05 < 0.050000000000000044 idi.
        m = ar.significance_multi(4500, 273, [(4500, 326), (4500, 273)])
        c = m["comparisons"][0]
        self.assertEqual(c["p_value"], 0.025)
        self.assertFalse(c["is_significant"])
        self.assertEqual(c["decision_code"], "not_significant")
        self.assertFalse(m["any_significant"])

    def test_alpha_is_exact(self):
        self.assertEqual(ar._alpha(0.95), 0.05)
        self.assertEqual(ar._alpha(0.9), 0.1)

    def test_step_down_unchanged(self):
        m = ar.significance_multi(10000, 500, [(10000, 570), (10000, 560), (10000, 510)])
        # Ham p 0.0278324 → 3p = 0.083497 → 0.0835 (yuvarlanmış p ile 3 × 0.02783 = 0.08349 basılıyordu).
        self.assertEqual([c["p_value_adjusted"] for c in m["comparisons"]], [0.0835, 0.11652, 0.74676])
        self.assertEqual([c["p_value_raw"] for c in m["comparisons"]], [0.02783, 0.05826, 0.74676])
        self.assertEqual([c["is_significant_raw"] for c in m["comparisons"]], [True, False, False])


class TestRelativeFractionConvention(unittest.TestCase):
    """Bulgu R2: --mde 1, %100 lift olarak okunuyor (749 kişi/kol), --mde 2 ise %2 oluyordu."""

    def test_one_or_more_is_rejected(self):
        for bad in (1, 1.5, 2, 10, -3):
            with self.assertRaises(ValueError) as cm:
                ar.sample_size(0.03, bad)
            self.assertIn("fraction", str(cm.exception))
            self.assertIn("%", str(cm.exception))
        with self.assertRaises(ValueError):
            ar.sample_size_mean(50, 100, 10)
        with self.assertRaises(ValueError):
            ar.significance(20000, 2000, 20000, 2000, ni_margin=2, guardrail_direction="must_not_decrease")

    def test_explicit_percent_form(self):
        self.assertEqual(ar.sample_size(0.03, "10%")["required_n_per_variant"],
                         ar.sample_size(0.03, 0.10)["required_n_per_variant"])
        self.assertEqual(ar.sample_size(0.03, "1%")["mde_relative_pct"], 1.0)
        ni = ar.significance(20000, 2000, 20000, 2000, ni_margin="5%",
                             guardrail_direction="must_not_decrease")["non_inferiority"]
        self.assertEqual(ni["margin_relative"], 0.05)
        with self.assertRaises(ValueError):
            ar.sample_size(0.03, "abc")

    def test_cli(self):
        rc, out, _ = run_cli("samplesize", "--baseline-rate", "0.03", "--mde", "1")
        self.assertEqual(rc, 1)
        self.assertIn("0.01", json.loads(out)["error"])
        rc, out, _ = run_cli("samplesize", "--baseline-rate", "0.03", "--mde", "10%")
        self.assertEqual(rc, 0, out)
        self.assertEqual(json.loads(out)["required_n_per_variant"], 53211)

    def test_decrease_is_sized_as_a_decrease(self):
        # Bulgu L7: negatif MDE ve --alternative less artış için boyutlanıyordu.
        down = ar.sample_size(0.05, -0.20)
        self.assertAlmostEqual(down["target_rate"], 0.04)
        self.assertEqual(ar.sample_size(0.05, 0.20, alternative="less")["target_rate"], down["target_rate"])
        self.assertNotEqual(down["required_n_per_variant"], ar.sample_size(0.05, 0.20)["required_n_per_variant"])
        self.assertAlmostEqual(ar.sample_size_mean(50, 100, -0.10)["target_mean"], 45.0)


class TestInteractionScaleDependence(unittest.TestCase):
    """Bulgu R5: effect_differs: true, 'etki farklı demeyin' uyarısıyla birlikte dönüyordu."""

    def test_flag_and_text_agree(self):
        r = ar.interaction(((4000, 200), (4000, 260)), ((6000, 300), (6000, 310)))
        self.assertNotEqual(r["interaction_absolute"]["is_significant"], r["interaction_relative"]["is_significant"])
        self.assertTrue(r["scale_dependent"])
        self.assertFalse(r["effect_differs"])
        self.assertEqual(r["decision_code"], "scale_dependent")
        self.assertNotIn("effect differs between", r["decision"])

    def test_consistent_scales(self):
        r = ar.interaction(((1000, 100), (1000, 150)), ((1000, 100), (1000, 100)))
        self.assertFalse(r["scale_dependent"])
        self.assertTrue(r["effect_differs"])
        self.assertEqual(r["decision_code"], "effect_differs")


class TestGuardrailInconclusive(unittest.TestCase):
    """Bulgular H4 ve (f): 'inconclusive' kendi durumu; gereken örneklem veya 'marj bu trafik için dar' yazılır."""

    def test_flat_guardrail_reports_sample_needed(self):
        r = ar.significance(20000, 800, 20000, 800, ni_margin=0.02, guardrail_direction="must_not_increase")
        ni = r["non_inferiority"]
        self.assertEqual(ni["status"], "inconclusive")
        self.assertEqual(ni["inconclusive_reason"], "underpowered")
        # n = (z_.95 + z_.80)² · p(1−p)(1 + θ²) / (p·marj)², p = 0.04, θ = 1.02
        want = math.ceil((ar.norm_ppf(0.95) + ar.norm_ppf(0.80)) ** 2 * 0.04 * 0.96 * (1 + 1.02 ** 2)
                         / (0.04 * 0.02) ** 2)
        self.assertEqual(ni["sample_needed"]["n_control"], want)
        self.assertGreater(want, 700000)
        self.assertTrue(ni["sample_needed"]["margin_too_tight_for_current_n"])
        self.assertEqual(r["guardrail_status"], "inconclusive")
        self.assertTrue(any(f"{want:,}" in w for w in r["warnings"]))

    def test_clean_and_degraded_have_no_sample_block(self):
        clean = ar.significance(20000, 2000, 20000, 2000, ni_margin=0.05, guardrail_direction="must_not_decrease")
        self.assertEqual(clean["guardrail_status"], "clean")
        self.assertIsNone(clean["non_inferiority"]["sample_needed"])
        self.assertIsNone(clean["non_inferiority"]["inconclusive_reason"])

    def test_rare_event_is_inconclusive_not_degraded(self):
        # 2/5000 vs 9/5000: en küçük beklenen sayı 5.5 < 10; Wald p 0.022 'degraded' diyordu.
        r = ar.significance(5000, 2, 5000, 9, ni_margin=0.10, guardrail_direction="must_not_increase")
        ni = r["non_inferiority"]
        self.assertEqual(ni["status"], "inconclusive")
        self.assertEqual(ni["inconclusive_reason"], "rare_event")
        self.assertFalse(ni["passed"])

    def test_note_sentences_are_separated(self):
        ni = ar.significance(20000, 2000, 20000, 2000, ni_margin="5%",
                             guardrail_direction="must_not_decrease")["non_inferiority"]
        self.assertNotIn("margin --ni-margin", ni["note"])
        self.assertRegex(ni["note"], r"margin\. ")

    def test_samplesize_guardrail_mode(self):
        r = ar.sample_size(0.04, ni_margin=0.02, guardrail_direction="must_not_increase")
        g = r["guardrail"]
        want = math.ceil((ar.norm_ppf(0.95) + ar.norm_ppf(0.80)) ** 2 * 0.04 * 0.96 * (1 + 1.02 ** 2)
                         / (0.04 * 0.02) ** 2)
        self.assertEqual(g["required_n_control"], want)
        with self.assertRaises(ValueError):
            ar.sample_size(0.04, ni_margin=0.02)
        # Ters yön: 4 haftada günde 10.000 ziyaretçiyle çözülebilen en küçük marj; bulunan marj n'i doldurmalı.
        inv = ar.sample_size(0.04, weeks=4, daily_visitors=10000, ni_margin=0.02,
                             guardrail_direction="must_not_increase")["guardrail"]
        m = inv["margin_resolvable_relative_pct"] / 100
        self.assertGreater(m, 0.02)
        back = ar.sample_size(0.04, ni_margin=m, guardrail_direction="must_not_increase")["guardrail"]
        self.assertAlmostEqual(back["required_n_control"] / 140000, 1.0, places=2)

    def test_cli_samplesize_guardrail(self):
        rc, out, _ = run_cli("samplesize", "--baseline-rate", "0.04", "--ni-margin", "0.02",
                             "--guardrail-direction", "must_not_increase")
        self.assertEqual(rc, 0, out)
        self.assertIn("guardrail", json.loads(out))


class TestSrmInsideSignificance(unittest.TestCase):
    """Bulgu R6: 10000/450 vs 9500/480 uyarısız yorumlanıyordu; SRM yalnızca ayrı komutla yakalanıyordu."""

    def test_srm_blocks_the_decision(self):
        r = ar.significance(10000, 450, 9500, 480)
        self.assertTrue(r["srm"]["srm_detected"])
        self.assertEqual(r["decision_code"], "invalid_srm")
        self.assertIn("SRM", r["note"])

    def test_planned_split_and_balanced(self):
        r = ar.significance(10000, 450, 9500, 480, expected_split=10000 / 19500)
        self.assertFalse(r["srm"]["srm_detected"])
        self.assertNotEqual(r["decision_code"], "invalid_srm")
        self.assertFalse(ar.significance(5000, 250, 5000, 290)["srm"]["srm_detected"])

    def test_multi_arm(self):
        m = ar.significance_multi(10000, 450, [(9500, 480), (10000, 470)])
        self.assertTrue(m["srm"]["srm_detected"])
        self.assertTrue(all(c["decision_code"] == "invalid_srm" for c in m["comparisons"]))
        ok = ar.significance_multi(10000, 450, [(5000, 240), (5000, 230)], expected_ratios=[2, 1, 1])
        self.assertFalse(ok["srm"]["srm_detected"])

    def test_cli_expected_split(self):
        rc, out, _ = run_cli("significance", "--control-visitors", "9000", "--control-conversions", "450",
                             "--variant-visitors", "1000", "--variant-conversions", "60", "--expected-split", "0.9")
        self.assertEqual(rc, 0, out)
        self.assertFalse(json.loads(out)["srm"]["srm_detected"])


class TestSrmCommandEdges(unittest.TestCase):
    """Bulgu L4."""

    def test_p_value_is_never_zero(self):
        self.assertGreater(ar.srm(1000000, 10)["p_value"], 0.0)
        self.assertGreater(ar.srm_multi([1000000, 10, 10])["p_value"], 0.0)

    def test_conflicting_flags_and_swapped_split(self):
        rc, out, _ = run_cli("srm", "--visitors", "5000,5100", "--control-visitors", "5000")
        self.assertEqual(rc, 1)
        self.assertIn("--visitors", json.loads(out)["error"])
        r = ar.srm(9000, 1000, expected_split=0.1)
        self.assertTrue(r["srm_detected"])
        self.assertIn("--expected-split", r["note"])


class TestLanguageLeaks(unittest.TestCase):
    """Bulgu L1/L2/L5: --lang tr altında İngilizce kalan çıktılar ve dosya hataları."""

    def test_argparse_errors_are_json_and_translated(self):
        rc, out, _ = run_cli("--lang", "tr", "significance", "--control-visitors", "100")
        self.assertEqual(rc, 2)
        self.assertIn("zorunlu", json.loads(out)["error"])
        rc, out, _ = run_cli("--lang", "tr", "significance", "--control-visitors", "100",
                             "--control-conversions", "5", "--alternative", "sideways")
        self.assertEqual(rc, 2)
        self.assertIn("geçersiz seçim", json.loads(out)["error"])
        rc, out, _ = run_cli("significance", "--control-visitors", "100")
        self.assertEqual(rc, 2)
        self.assertIn("required", json.loads(out)["error"])

    def test_file_errors(self):
        with tempfile.TemporaryDirectory() as d:
            missing = os.path.join(d, "yok.csv")
            rc, out, _ = run_cli("--lang", "tr", "continuous", "--control-csv", missing, "--variant-csv", missing)
            self.assertEqual(rc, 1)
            self.assertIn("bulunamadı", json.loads(out)["error"])
            u16 = write(d, "u16.csv", "revenue\n1\n2\n", encoding="utf-16")
            rc, out, _ = run_cli("continuous", "--control-csv", u16, "--variant-csv", u16)
            err = json.loads(out)["error"]
            self.assertIn("u16.csv", err)
            self.assertIn("UTF-8", err)
            semi = write(d, "semi.csv", "user_id;revenue\nu1;12.5\nu2;3\n")
            rc, out, _ = run_cli("continuous", "--control-csv", semi, "--variant-csv", semi)
            self.assertIn("semicolon", json.loads(out)["error"])

    def test_text_mode_turkish(self):
        rc, out, _ = run_cli("--lang", "tr", "significance",
                             "--control-visitors", "20000", "--control-conversions", "2000",
                             "--variant-visitors", "20000", "--variant-conversions", "2000",
                             "--ni-margin", "0.05", "--guardrail-direction", "must_not_decrease",
                             "--format", "text")
        self.assertEqual(rc, 0, out)
        self.assertIn("temiz", out)
        self.assertNotIn("clean", out)
        self.assertNotIn("must_not_decrease", out)

    def test_turkish_thousands_and_sd(self):
        try:
            ar.set_lang("tr")
            r = ar.significance(5000, 250, 5000, 290, planned_n=8000)
            txt = ar.format_text("samplesize", ar.sample_size_mean(42, 120, 0.05))
        finally:
            ar.set_lang("en")
        self.assertIn("8.000", r["note"])
        self.assertNotIn("8,000", r["note"])
        self.assertIn("ss 120", txt)


if __name__ == "__main__":
    unittest.main(verbosity=2)
