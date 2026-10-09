#!/usr/bin/env python3
"""analyze_results.py v2 özellikleri için testler: Fisher exact, Newcombe CI, göreli lift CI,
A/B/n + Holm, tek yönlü test, ratio/arms, k kollu SRM, peeking, MDE, continuous (Welch,
bootstrap, CUPED), Bayes, esnek tam sayı ayrıştırma ve CLI.

Referans değerler yayımlanmış tablolardan veya elle hesaptan alınmıştır (yorumlarda belirtildi).
"""
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "analyze_results.py")
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import analyze_results as ar


def setUpModule():
    # Bu dosyadaki testler Türkçe mesaj metinlerini doğrular; CLI varsayılanı İngilizcedir (--lang en).
    ar.set_lang("tr")


def tearDownModule():
    ar.set_lang("en")


def run_cli(*args):
    out = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)
    return out.returncode, out.stdout, out.stderr


class TestDistributions(unittest.TestCase):
    def test_t_table_critical_values(self):
        # Standart t tablosu: t_{0.975}(10)=2.228139, t_{0.975}(1)=12.7062, t_{0.975}(5)=2.570582
        self.assertAlmostEqual(ar.t_sf_two_sided(2.228139, 10), 0.05, places=6)
        self.assertAlmostEqual(ar.t_sf_two_sided(12.7062, 1), 0.05, places=5)
        self.assertAlmostEqual(ar.t_ppf(0.975, 5), 2.570582, places=5)

    def test_t_df1_is_cauchy(self):
        # df=1 → Cauchy: P(|T|>t) = 1 - 2*atan(t)/pi
        for t in (0.5, 1.0, 3.0):
            self.assertAlmostEqual(ar.t_sf_two_sided(t, 1), 1 - 2 * math.atan(t) / math.pi, places=9)

    def test_chi2_table_values(self):
        # df=2: sf(x)=exp(-x/2) tam formül; df=3 tablo: 7.814728 → 0.05
        self.assertAlmostEqual(ar.chi2_sf(4.0, 2), math.exp(-2), places=10)
        self.assertAlmostEqual(ar.chi2_sf(7.814728, 3), 0.05, places=6)
        self.assertAlmostEqual(ar.chi2_sf(3.841459, 1), 0.05, places=6)
        self.assertAlmostEqual(ar.chi2_sf(30.0, 10), 0.000857, places=5)


class TestFisherExact(unittest.TestCase):
    def test_lady_tasting_tea_table(self):
        # Klasik tablo [[1,9],[11,3]]: iki yönlü p=0.002759, tek yönlü 0.001380
        # Kontrol 1/10 (dönüşüm/ziyaretçi), varyant 11/14
        self.assertAlmostEqual(ar.fisher_exact(10, 1, 14, 11), 0.0027595, places=6)
        self.assertAlmostEqual(ar.fisher_exact(10, 1, 14, 11, "greater"), 0.0013797, places=6)
        self.assertAlmostEqual(ar.fisher_exact(10, 1, 14, 11, "less"), 1.0, places=3)

    def test_hand_computed_zero_vs_five(self):
        # 1000/0 vs 1000/5: P(tüm 5 dönüşüm tek kolda) = C(1000,5)/C(2000,5); iki yönlü = 2x
        one = math.comb(1000, 5) / math.comb(2000, 5)
        self.assertAlmostEqual(ar.fisher_exact(1000, 0, 1000, 5), 2 * one, places=10)

    def test_audit_regression_rare_event_not_significant(self):
        # Denetim bulgusu: z-testi p=0.025 diyordu; exact p≈0.062 → anlamlı değil
        r = ar.significance(1000, 0, 1000, 5)
        self.assertEqual(r["method"], "fisher-exact")
        self.assertFalse(r["is_significant"])
        self.assertAlmostEqual(r["p_value"], 0.0622, places=3)
        self.assertLess(r["p_value_z_test"], 0.05)
        self.assertIn("Nadir olay", r["note"])

    def test_healthy_data_uses_z(self):
        self.assertEqual(ar.significance(5000, 250, 5000, 290)["method"], "z-test")


class TestIntervals(unittest.TestCase):
    def test_newcombe_1998_reference(self):
        # Newcombe (1998) tablo II: 56/70 vs 48/80 → fark CI (0.0524, 0.3339)
        lo, hi = ar.newcombe_diff_ci(48, 80, 56, 70)
        self.assertAlmostEqual(lo, 0.0524, places=4)
        self.assertAlmostEqual(hi, 0.3339, places=4)

    def test_wilson_reference(self):
        # Wilson 95%: 81/263 → (0.2553, 0.3662) (Newcombe 1998 tek oran örneği)
        lo, hi = ar.wilson_interval(81, 263)
        self.assertAlmostEqual(lo, 0.2553, places=4)
        self.assertAlmostEqual(hi, 0.3662, places=4)

    def test_ci_not_degenerate_at_zero(self):
        r = ar.significance(1000, 0, 1000, 0)
        lo, hi = r["confidence_interval_diff"]
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0)
        self.assertEqual(r["confidence_interval_diff_wald"], [0.0, 0.0])

    def test_relative_lift_ci_hand(self):
        # Katz log-oran: se = sqrt((1-p1)/x1 + (1-p2)/x2)
        r = ar.significance(5000, 250, 5000, 290)
        se = math.sqrt(0.95 / 250 + 0.942 / 290)
        lr = math.log(0.058 / 0.05)
        z = 1.959963985
        lo, hi = r["confidence_interval_relative_lift_pct"]
        self.assertAlmostEqual(lo, (math.exp(lr - z * se) - 1) * 100, places=1)
        self.assertAlmostEqual(hi, (math.exp(lr + z * se) - 1) * 100, places=1)

    def test_relative_lift_ci_none_when_control_zero(self):
        self.assertIsNone(ar.significance(1000, 0, 1000, 5)["confidence_interval_relative_lift_pct"])


class TestAlternativeAndPower(unittest.TestCase):
    def test_one_sided_halves_p(self):
        two = ar.significance(5000, 250, 5000, 290)
        g = ar.significance(5000, 250, 5000, 290, alternative="greater")
        l = ar.significance(5000, 250, 5000, 290, alternative="less")
        self.assertAlmostEqual(g["p_value"], two["p_value"] / 2, places=4)
        self.assertAlmostEqual(g["p_value"] + l["p_value"], 1.0, places=4)
        self.assertTrue(g["is_significant"])

    def test_mde_at_current_n_hand(self):
        r = ar.significance(5000, 250, 5000, 290)
        exp = (1.959964 + 0.841621) * math.sqrt(0.05 * 0.95 * 2 / 5000) / 0.05 * 100
        self.assertAlmostEqual(r["mde_at_current_n_pct"], exp, places=1)

    def test_peeking_guard(self):
        r = ar.significance(5000, 250, 5000, 330, planned_n=8000)
        self.assertTrue(r["peeking_risk"])
        self.assertIn("nihai karar", r["decision"])
        self.assertTrue(any("peeking" in w for w in r["warnings"]))
        r2 = ar.significance(5000, 250, 5000, 330, planned_n=5000)
        self.assertFalse(r2["peeking_risk"])
        self.assertEqual(r2["decision"], "anlamlı")

    def test_single_prioritized_note(self):
        r = ar.significance(1000, 0, 1000, 5)
        self.assertTrue(r["low_sample_warning"])
        self.assertEqual(len(r["warnings"]), 1)  # nadir olay, 250 notunu kapsıyor
        r = ar.significance(2000, 100, 2000, 120)
        self.assertEqual(len(r["warnings"]), 1)
        self.assertIn("250", r["note"])


class TestMultiArm(unittest.TestCase):
    def test_holm_hand(self):
        # p = [0.01, 0.04, 0.03] → sıralı 0.01*3=0.03, 0.03*2=0.06, max(0.06, 0.04)=0.06
        self.assertEqual([round(x, 10) for x in ar.holm_adjust([0.01, 0.04, 0.03])], [0.03, 0.06, 0.06])

    def test_multi_comparisons(self):
        m = ar.significance_multi(5000, 250, [(5000, 290), (5000, 270), (5000, 330)])
        self.assertEqual(m["n_comparisons"], 3)
        raw = [c["p_value_raw"] for c in m["comparisons"]]
        adj = [c["p_value_adjusted"] for c in m["comparisons"]]
        self.assertTrue(all(a >= r for a, r in zip(adj, raw)))
        self.assertTrue(m["comparisons"][2]["is_significant"])
        self.assertFalse(m["comparisons"][0]["is_significant"])
        self.assertEqual([c["arm"] for c in m["comparisons"]], ["B", "C", "D"])


class TestSampleSizeV2(unittest.TestCase):
    def test_ratio_one_matches_legacy(self):
        r = ar.sample_size(0.05, 0.20, ratio=1)
        self.assertEqual(r["required_n_control"], r["required_n_variant"])
        self.assertEqual(r["required_n_per_variant"], 8158)

    def test_ratio_hand(self):
        # n1 = (za*sqrt(pb*qb*(1+1/k)) + zb*sqrt(p1q1 + p2q2/k))^2 / d^2, pb=(p1+k p2)/(1+k)
        k, p1, p2 = 2.0, 0.05, 0.06
        pb = (p1 + k * p2) / (1 + k)
        n1 = (1.959964 * math.sqrt(pb * (1 - pb) * (1 + 1 / k))
              + 0.841621 * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2) / k)) ** 2 / (p2 - p1) ** 2
        r = ar.sample_size(0.05, 0.20, ratio=2)
        self.assertAlmostEqual(r["required_n_control"], math.ceil(n1), delta=1)
        self.assertEqual(r["required_n_variant"], 2 * r["required_n_control"])
        self.assertEqual(r["required_n_total"], r["required_n_control"] + r["required_n_variant"])

    def test_one_sided_needs_less(self):
        self.assertLess(ar.sample_size(0.05, 0.2, alternative="greater")["required_n_per_variant"],
                        ar.sample_size(0.05, 0.2)["required_n_per_variant"])

    def test_arms_bonferroni(self):
        r = ar.sample_size(0.05, 0.2, arms=3)
        self.assertAlmostEqual(r["alpha_per_comparison"], 0.025)
        self.assertGreater(r["required_n_per_variant"], 8158)
        self.assertEqual(r["required_n_total"], 3 * r["required_n_per_variant"])


class TestSRMMulti(unittest.TestCase):
    def test_three_arm_hand(self):
        # beklenen 5000'er: chi2 = (0 + 100^2 + 100^2)/5000 = 4, df=2 → p = e^-2
        r = ar.srm_multi([5000, 5100, 4900])
        self.assertEqual(r["df"], 2)
        self.assertAlmostEqual(r["chi2"], 4.0)
        self.assertAlmostEqual(r["p_value"], math.exp(-2), places=5)

    def test_expected_ratios(self):
        self.assertFalse(ar.srm_multi([2500, 2500, 5000], [1, 1, 2])["srm_detected"])
        self.assertTrue(ar.srm_multi([3333, 3333, 3334], [1, 1, 2])["srm_detected"])

    def test_two_arm_consistent(self):
        a = ar.srm(5800, 4200)
        b = ar.srm_multi([5800, 4200])
        self.assertEqual(a["chi2"], b["chi2"])
        self.assertEqual(a["p_value"], b["p_value"])


class TestContinuous(unittest.TestCase):
    def test_welch_hand(self):
        # Özet istatistik: elle Welch t ve Welch-Satterthwaite sd
        r = ar.continuous(control_stats=(10, 20.0, 4.0), variant_stats=(12, 24.0, 6.0))
        se2 = 16 / 10 + 36 / 12
        t = 4.0 / math.sqrt(se2)
        df = se2 ** 2 / ((16 / 10) ** 2 / 9 + (36 / 12) ** 2 / 11)
        self.assertAlmostEqual(r["t_stat"], t, places=4)
        self.assertAlmostEqual(r["df"], df, places=2)
        self.assertAlmostEqual(r["p_value"], ar.t_sf_two_sided(t, df), places=5)
        # t=1.865, df≈19.3 → p ≈ 0.0774 (t tablosu arası)
        self.assertTrue(0.07 < r["p_value"] < 0.085)

    def test_welch_equal_var_matches_student(self):
        # Eşit n ve varyansta Welch t = Student t, df = 2n-2
        r = ar.continuous(control=[1, 2, 3, 4, 5], variant=[3, 4, 5, 6, 7])
        self.assertAlmostEqual(r["t_stat"], 2 / math.sqrt(2.5 / 5 * 2), places=4)
        self.assertAlmostEqual(r["df"], 8.0, places=4)

    def test_winsorize_caps_outlier(self):
        c = [0.0] * 90 + [10.0] * 9 + [10000.0]
        v = [0.0] * 90 + [12.0] * 10
        r = ar.continuous(control=c, variant=v, winsorize=0.99)
        self.assertGreater(r["winsorize"]["n_capped"], 0)
        self.assertLess(r["control"]["mean"], 50)

    def test_bootstrap_seeded_and_brackets_diff(self):
        c = [0.0] * 80 + [5.0, 10.0, 20.0, 40.0] * 5
        v = [0.0] * 75 + [5.0, 10.0, 20.0, 40.0, 60.0] * 5
        r1 = ar.continuous(control=c, variant=v, bootstrap=500, seed=7)
        r2 = ar.continuous(control=c, variant=v, bootstrap=500, seed=7)
        self.assertEqual(r1["bootstrap"], r2["bootstrap"])
        lo, hi = r1["bootstrap"]["ci_diff"]
        self.assertTrue(lo < r1["absolute_diff"] < hi)

    def test_cuped_reduces_variance(self):
        import random
        rng = random.Random(3)
        cp = [rng.gauss(10, 3) for _ in range(400)]
        vp = [rng.gauss(10, 3) for _ in range(400)]
        c = [x + rng.gauss(0, 1) for x in cp]
        v = [x + 0.3 + rng.gauss(0, 1) for x in vp]
        r = ar.continuous(control=c, variant=v, control_pre=cp, variant_pre=vp)
        cu = r["cuped"]
        self.assertGreater(cu["variance_reduction_pct"], 70)
        self.assertAlmostEqual(cu["theta"], 1.0, delta=0.1)
        self.assertLess(cu["p_value"], r["p_value"])

    def test_cuped_length_mismatch(self):
        with self.assertRaises(ValueError):
            ar.continuous(control=[1, 2, 3], variant=[1, 2, 3], control_pre=[1, 2], variant_pre=[1, 2, 3])

    def test_relative_ci_none_when_mean_zero(self):
        r = ar.continuous(control=[0, 0, 0, 0], variant=[0, 1, 0, 2])
        self.assertIsNone(r["confidence_interval_relative_lift_pct"])


class TestBayes(unittest.TestCase):
    def test_seeded_and_consistent_with_frequentist(self):
        a = ar.bayes(5000, 250, 5000, 290, draws=20000, seed=1)
        b = ar.bayes(5000, 250, 5000, 290, draws=20000, seed=1)
        self.assertEqual(a, b)
        # Düz önselde P(v>c) ≈ 1 - tek yönlü p (≈0.962)
        self.assertAlmostEqual(a["prob_variant_beats_control"], 0.962, delta=0.01)
        self.assertLess(a["expected_loss_choose_variant"], a["expected_loss_choose_control"])
        self.assertIn("Alternatif", a["note"])

    def test_posterior_mean(self):
        r = ar.bayes(100, 10, 100, 10, draws=2000, seed=0)
        self.assertAlmostEqual(r["control_posterior_mean"], 11 / 102, places=6)


class TestParsingAndCLI(unittest.TestCase):
    def test_parse_count(self):
        for s, v in (("1000", 1000), ("1e3", 1000), ("1,000", 1000), ("1_000", 1000), ("2.5e4", 25000)):
            self.assertEqual(ar.parse_count(s), v)
        for bad in ("1.5", "abc", "1,00"):
            with self.assertRaises(Exception):
                ar.parse_count(bad)

    def test_cli_legacy_significance(self):
        rc, out, _ = run_cli("significance", "--control-visitors", "5e3", "--control-conversions", "250",
                             "--variant-visitors", "5,000", "--variant-conversions", "290")
        self.assertEqual(rc, 0)
        r = json.loads(out)
        self.assertEqual(r["method"], "z-test")
        self.assertIn("is_significant", r)

    def test_cli_multi_variant(self):
        rc, out, _ = run_cli("significance", "--control-visitors", "5000", "--control-conversions", "250",
                             "--variant", "5000:290", "--variant", "5000:330", "--format", "text")
        self.assertEqual(rc, 0)
        self.assertIn("Holm", out)

    def test_cli_srm_k_arms(self):
        rc, out, _ = run_cli("srm", "--visitors", "5000,5100,4900")
        self.assertEqual(json.loads(out)["df"], 2)

    def test_cli_continuous_csv(self):
        with tempfile.TemporaryDirectory() as d:
            cp, vp = os.path.join(d, "c.csv"), os.path.join(d, "v.csv")
            with open(cp, "w") as f:
                f.write("revenue\n" + "\n".join(["0", "0", "10", "20", "0", "5"] * 10))
            with open(vp, "w") as f:
                f.write("\n".join(["0", "12", "10", "25", "0", "5"] * 10))
            rc, out, _ = run_cli("continuous", "--control-csv", cp, "--variant-csv", vp,
                                 "--bootstrap", "200", "--seed", "1")
            self.assertEqual(rc, 0, out)
            r = json.loads(out)
            self.assertEqual(r["control"]["n"], 60)
            self.assertIn("bootstrap", r)

    def test_cli_bayes_and_samplesize(self):
        rc, out, _ = run_cli("bayes", "--control-visitors", "1000", "--control-conversions", "50",
                             "--variant-visitors", "1000", "--variant-conversions", "60",
                             "--draws", "5000", "--seed", "2")
        self.assertEqual(rc, 0)
        self.assertIn("prob_variant_beats_control", json.loads(out))
        rc, out, _ = run_cli("samplesize", "--baseline-rate", "0.05", "--mde", "0.2", "--ratio", "2", "--arms", "3")
        r = json.loads(out)
        self.assertEqual(r["required_n_total"], r["required_n_control"] + 2 * r["required_n_variant"])

    def test_cli_error_is_json(self):
        rc, out, _ = run_cli("significance", "--control-visitors", "100", "--control-conversions", "5")
        self.assertEqual(rc, 1)
        self.assertIn("error", json.loads(out))

    def test_revenue_points_to_continuous(self):
        r = ar.revenue(1000, 50, 100, 1000, 55, 95)
        self.assertEqual(r["inference_command"], "continuous")


if __name__ == "__main__":
    unittest.main(verbosity=2)
