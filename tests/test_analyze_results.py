#!/usr/bin/env python3
"""analyze_results.py için unit testler. Bağımlılıksız (unittest).

Koşum: python3 tests/test_analyze_results.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import analyze_results as ar


class TestSignificance(unittest.TestCase):
    def test_known_values_not_significant(self):
        # evals/04-results.md Girdi A: p ~0.077, anlamlı değil
        r = ar.significance(5000, 250, 5000, 290)
        self.assertFalse(r["is_significant"])
        self.assertTrue(0.06 < r["p_value"] < 0.09)
        self.assertAlmostEqual(r["control_rate"], 0.05, places=4)
        self.assertAlmostEqual(r["variant_rate"], 0.058, places=4)
        self.assertAlmostEqual(r["relative_lift_pct"], 16.0, places=1)

    def test_known_values_significant(self):
        r = ar.significance(5000, 250, 5000, 340)
        self.assertTrue(r["is_significant"])
        self.assertLess(r["p_value"], 0.05)

    def test_equal_rates(self):
        r = ar.significance(1000, 50, 1000, 50)
        self.assertEqual(r["z_score"], 0.0)
        self.assertAlmostEqual(r["p_value"], 1.0, places=4)
        self.assertFalse(r["is_significant"])

    def test_zero_conversions_both(self):
        r = ar.significance(1000, 0, 1000, 0)
        self.assertFalse(r["is_significant"])
        self.assertIsNone(r["relative_lift_pct"])
        self.assertTrue(r["low_sample_warning"])

    def test_ci_contains_diff(self):
        r = ar.significance(5000, 250, 5000, 290)
        lo, hi = r["confidence_interval_diff"]
        self.assertLess(lo, hi)
        self.assertTrue(lo <= r["absolute_diff"] <= hi)

    def test_rare_event_invalidates_normal_approx(self):
        # 100.000 ziyaretçide 3 vs 8 dönüşüm: örneklem "büyük" ama beklenen dönüşüm sayısı çok küçük
        r = ar.significance(100000, 3, 100000, 8)
        self.assertFalse(r["normal_approx_valid"])
        self.assertLess(r["min_expected_count"], 10)
        self.assertIn("Nadir olay", r["note"])

    def test_normal_approx_valid_on_healthy_data(self):
        r = ar.significance(5000, 250, 5000, 290)
        self.assertTrue(r["normal_approx_valid"])
        self.assertGreaterEqual(r["min_expected_count"], 10)

    def test_small_sample_but_valid_approx(self):
        # 500 ziyaretçi / ~%40 dönüşüm: dönüşüm sayısı 250'nin altında ama yaklaşım geçerli
        r = ar.significance(500, 200, 500, 220)
        self.assertTrue(r["low_sample_warning"])
        self.assertTrue(r["normal_approx_valid"])

    def test_zero_conversions_flags_rare_event(self):
        r = ar.significance(1000, 0, 1000, 0)
        self.assertFalse(r["normal_approx_valid"])

    def test_low_sample_warning(self):
        r = ar.significance(500, 20, 500, 30)
        self.assertTrue(r["low_sample_warning"])
        self.assertIsNotNone(r["note"])

    def test_zero_visitors_raises(self):
        with self.assertRaises(ValueError):
            ar.significance(0, 5, 100, 10)
        with self.assertRaises(ValueError):
            ar.significance(100, 5, 0, 10)

    def test_conversions_exceed_visitors_raises(self):
        with self.assertRaises(ValueError):
            ar.significance(100, 120, 100, 10)

    def test_negative_conversions_raises(self):
        with self.assertRaises(ValueError):
            ar.significance(100, -1, 100, 10)

    def test_invalid_confidence_raises(self):
        with self.assertRaises(ValueError):
            ar.significance(100, 5, 100, 10, confidence=1.0)
        with self.assertRaises(ValueError):
            ar.significance(100, 5, 100, 10, confidence=0.0)


class TestSampleSize(unittest.TestCase):
    def test_known_values(self):
        # evals/04-results.md Girdi B: %5 baz, %20 göreli lift → varyant başına ~8100-8250
        r = ar.sample_size(0.05, 0.20)
        self.assertTrue(8000 < r["required_n_per_variant"] < 8400)
        self.assertEqual(r["required_n_total"], r["required_n_per_variant"] * 2)
        self.assertAlmostEqual(r["target_rate"], 0.06, places=4)

    def test_bigger_mde_needs_less_sample(self):
        small = ar.sample_size(0.05, 0.10)["required_n_per_variant"]
        big = ar.sample_size(0.05, 0.50)["required_n_per_variant"]
        self.assertLess(big, small)

    def test_zero_mde_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(0.05, 0.0)

    def test_negative_mde_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(0.05, -0.2)

    def test_baseline_zero_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(0.0, 0.2)

    def test_baseline_one_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(1.0, 0.2)

    def test_target_rate_over_one_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(0.6, 0.8)  # 0.6 × 1.8 = 1.08

    def test_invalid_power_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(0.05, 0.2, power=0.0)
        with self.assertRaises(ValueError):
            ar.sample_size(0.05, 0.2, power=1.0)

    def test_invalid_confidence_raises(self):
        with self.assertRaises(ValueError):
            ar.sample_size(0.05, 0.2, confidence=1.5)


class TestRevenue(unittest.TestCase):
    def test_cr_up_but_revenue_down_is_flagged(self):
        # Fiyat indirimi: CR +%12 ama AOV -%15 → RPV düşüyor
        r = ar.revenue(10000, 500, 1000, 10000, 560, 850)
        self.assertGreater(r["cr_change_pct"], 0)
        self.assertLess(r["rpv_change_pct"], 0)
        self.assertIn("RPV olmalı", r["warning"])

    def test_cr_down_but_revenue_up_is_flagged(self):
        r = ar.revenue(10000, 500, 1000, 10000, 450, 1300)
        self.assertLess(r["cr_change_pct"], 0)
        self.assertGreater(r["rpv_change_pct"], 0)
        self.assertIn("elemeyin", r["warning"])

    def test_no_warning_when_both_move_together(self):
        r = ar.revenue(10000, 500, 1000, 10000, 560, 1000)
        self.assertIsNone(r["warning"])

    def test_rpv_math(self):
        r = ar.revenue(1000, 100, 50, 1000, 100, 50)
        self.assertAlmostEqual(r["control"]["rpv"], 5.0, places=4)
        self.assertAlmostEqual(r["variant"]["rpv"], 5.0, places=4)

    def test_margin_applied(self):
        r = ar.revenue(1000, 100, 100, 1000, 100, 100, margin_rate=0.4)
        self.assertAlmostEqual(r["profit_per_visitor"]["control"], 4.0, places=4)

    def test_no_margin_returns_none(self):
        r = ar.revenue(1000, 100, 100, 1000, 100, 100)
        self.assertIsNone(r["profit_per_visitor"])

    def test_invalid_inputs_raise(self):
        with self.assertRaises(ValueError):
            ar.revenue(0, 5, 100, 100, 10, 100)
        with self.assertRaises(ValueError):
            ar.revenue(100, 120, 100, 100, 10, 100)
        with self.assertRaises(ValueError):
            ar.revenue(100, 10, -5, 100, 10, 100)
        with self.assertRaises(ValueError):
            ar.revenue(100, 10, 100, 100, 10, 100, margin_rate=1.5)

    def test_zero_conversions_does_not_crash(self):
        r = ar.revenue(1000, 0, 100, 1000, 5, 100)
        self.assertEqual(r["control"]["rpv"], 0.0)
        self.assertIsNone(r["cr_change_pct"])


class TestNormFunctions(unittest.TestCase):
    def test_norm_cdf_symmetry(self):
        self.assertAlmostEqual(ar.norm_cdf(0), 0.5, places=6)
        self.assertAlmostEqual(ar.norm_cdf(1.96), 0.975, places=3)

    def test_norm_ppf_roundtrip(self):
        for p in (0.01, 0.05, 0.5, 0.8, 0.95, 0.975, 0.99):
            self.assertAlmostEqual(ar.norm_cdf(ar.norm_ppf(p)), p, places=4)

    def test_norm_ppf_bounds_raise(self):
        with self.assertRaises(ValueError):
            ar.norm_ppf(0)
        with self.assertRaises(ValueError):
            ar.norm_ppf(1)


class TestFormatText(unittest.TestCase):
    def test_significance_text(self):
        r = ar.significance(5000, 250, 5000, 290)
        out = ar.format_text("significance", r)
        self.assertIn("yüzde puan", out)
        self.assertIn("anlamlı değil", out)

    def test_samplesize_text(self):
        r = ar.sample_size(0.05, 0.20)
        out = ar.format_text("samplesize", r)
        self.assertIn("varyant başına", out)


class TestNumericAnchors(unittest.TestCase):
    """Formül varyantlarını (pooled/unpooled) ayırt edecek sayısal çapalar.
    Referans değerler bağımsız hesapla (scipy) doğrulanmıştır."""

    def test_z_score_exact(self):
        r = ar.significance(5000, 250, 5000, 290)
        self.assertAlmostEqual(r["z_score"], 1.7698, places=3)

    def test_ci_endpoints_exact(self):
        r = ar.significance(5000, 250, 5000, 290)
        self.assertAlmostEqual(r["confidence_interval_diff"][0], -0.00086, places=4)
        self.assertAlmostEqual(r["confidence_interval_diff"][1], 0.01686, places=4)

    def test_large_z_p_not_zero(self):
        """Regresyon: büyük z'de p tam 0.0 basılmamalı (erfc + yuvarlama koruması)."""
        r = ar.significance(1000000, 50000, 1000000, 60000)
        self.assertGreater(r["p_value"], 0.0)
        self.assertLess(r["p_value"], 1e-100)


class TestSampleSizeValidity(unittest.TestCase):
    def test_huge_mde_flags_invalid_approx(self):
        """Regresyon: dev MDE'de script uyarısız 12 kişilik plan veriyordu."""
        r = ar.sample_size(0.05, 10.0)
        self.assertFalse(r["normal_approx_valid"])
        self.assertIsNotNone(r["note"])

    def test_normal_mde_is_valid(self):
        r = ar.sample_size(0.05, 0.20)
        self.assertTrue(r["normal_approx_valid"])
        self.assertIsNone(r["note"])


class TestSRM(unittest.TestCase):
    def test_no_srm_at_expected_split(self):
        r = ar.srm(5012, 4988)
        self.assertFalse(r["srm_detected"])
        self.assertGreater(r["p_value"], 0.001)

    def test_srm_detected_at_clear_imbalance(self):
        r = ar.srm(5800, 4200)
        self.assertTrue(r["srm_detected"])

    def test_srm_p_value_not_zero_at_extreme_chi2(self):
        """Regresyon: significance()'daki aynı yuvarlama/underflow hatası burada da vardı."""
        r = ar.srm(5800, 4200)
        self.assertGreater(r["p_value"], 0.0)

    def test_custom_expected_split(self):
        r = ar.srm(9000, 1000, expected_split=0.9)
        self.assertFalse(r["srm_detected"])

    def test_small_sample_flags_invalid_approx(self):
        r = ar.srm(3, 2)
        self.assertFalse(r["normal_approx_valid"])
        self.assertIsNotNone(r["note"])

    def test_zero_total_rejected(self):
        with self.assertRaises(ValueError):
            ar.srm(0, 0)

    def test_negative_visitors_rejected(self):
        with self.assertRaises(ValueError):
            ar.srm(-5, 100)

    def test_invalid_expected_split_rejected(self):
        with self.assertRaises(ValueError):
            ar.srm(100, 100, expected_split=1.5)

    def test_srm_text_format(self):
        r = ar.srm(5800, 4200)
        out = ar.format_text("srm", r)
        self.assertIn("SRM TESPİT EDİLDİ", out)


class TestVariantMargin(unittest.TestCase):
    def test_different_margins_applied_per_arm(self):
        r = ar.revenue(1000, 50, 400, 1000, 68, 700, margin_rate=0.40, variant_margin_rate=0.25)
        p = r["profit_per_visitor"]
        self.assertAlmostEqual(p["control"], 20.0 * 0.40, places=4)
        self.assertAlmostEqual(p["variant"], 47.6 * 0.25, places=4)

    def test_text_output_shows_both_margins(self):
        """Regresyon: text çıktı varyant marjını gizleyip tek marj basıyordu."""
        r = ar.revenue(1000, 50, 400, 1000, 68, 700, margin_rate=0.40, variant_margin_rate=0.25)
        out = ar.format_text("revenue", r)
        self.assertIn("%40", out)
        self.assertIn("%25", out)

    def test_zero_margin_accepted(self):
        r = ar.revenue(1000, 50, 100, 1000, 55, 95, margin_rate=0.0)
        self.assertEqual(r["profit_per_visitor"]["control"], 0.0)

    def test_variant_margin_alone_rejected(self):
        with self.assertRaises(ValueError):
            ar.revenue(1000, 50, 100, 1000, 55, 95, variant_margin_rate=0.25)

    def test_same_margin_assumption_noted(self):
        r = ar.revenue(1000, 50, 100, 1000, 55, 95, margin_rate=0.35)
        self.assertIn("assumption", r["profit_per_visitor"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
