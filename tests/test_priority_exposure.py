#!/usr/bin/env python3
"""The evidence-led priority score and the exposure point (methodology.md →
Prioritization, KPI denominator → Exposure point)."""
import copy
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import validate_scenario_json as vsj  # noqa: E402
from test_validate_scenario_json_v3 import SCHEMA, coupon, plain  # noqa: E402

USER_DATA = {"level": "user_data", "note": "GA4 raporuna göre ürün sayfasında teslimat bölümünde çıkış yoğun."}


def errs(sc, lang="en"):
    return vsj.validate(sc, SCHEMA, lang)


def has(items, fragment):
    return any(fragment in item for item in items)


def scored(sc, tier, evidence_level=None, **inputs):
    sc = copy.deepcopy(sc)
    if evidence_level == "user_data":
        sc["evidence"] = dict(USER_DATA)
    elif evidence_level:
        sc["evidence"] = {"level": evidence_level}
    sc["priority"]["tier"] = tier
    sc["priority"]["inputs"] = dict(sc["priority"]["inputs"], **inputs)
    return sc


class TestScore(unittest.TestCase):
    def test_formula(self):
        self.assertEqual(vsj.priority_score({"evidence": "user_data", "main_path": True, "noticeable": True,
                                             "effort": "low"}), (7, "3+1+1+2"))
        self.assertEqual(vsj.priority_score({"evidence": "intuition", "main_path": False, "noticeable": False,
                                             "effort": "high"}), (0, "0+0+0+0"))
        self.assertEqual(vsj.priority_score({"evidence": "behaviour_data", "main_path": True, "noticeable": False,
                                             "effort": "medium"}), (4, "2+1+0+1"))
        self.assertIsNone(vsj.priority_score({"evidence": "user_data"}))
        self.assertIsNone(vsj.priority_score({"evidence": "x", "main_path": 1, "noticeable": True, "effort": "low"}))

    def test_bands(self):
        self.assertEqual([vsj.score_tier(n) for n in range(8)],
                         ["low", "low", "low", "medium", "medium", "medium", "high", "high"])
        self.assertEqual(vsj.score_tier(7, capped=True), "medium")

    def test_intuition_can_never_reach_high(self):
        best = vsj.priority_score({"evidence": "intuition", "main_path": True, "noticeable": True, "effort": "low"})
        self.assertNotEqual(vsj.score_tier(best[0]), "high")


class TestTierMatchesScore(unittest.TestCase):
    def test_matching_tiers_pass(self):
        self.assertEqual(errs(scored(coupon(), "medium")), [])  # archive 1+1+1+2 = 5
        self.assertEqual(errs(scored(coupon(), "low", main_path=False, noticeable=False, effort="high")), [])
        self.assertEqual(errs(scored(coupon(), "high", "user_data", evidence="user_data")), [])

    def test_a_chosen_tier_off_the_score_is_refused(self):
        e = errs(scored(coupon(), "high"))
        self.assertTrue(has(e, "priority.tier: 'high' doesn't match the inputs' score: 1+1+1+2 = 5/7, which is "
                               "'medium'"), e)
        e = errs(scored(coupon(), "medium", main_path=False, noticeable=False, effort="high"))
        self.assertTrue(has(e, "= 1/7, which is 'low'"), e)
        self.assertTrue(has(errs(scored(coupon(), "high"), "tr"), "girdilerin puanıyla uyuşmuyor"))

    def test_inputs_are_required(self):
        sc = coupon()
        del sc["priority"]["inputs"]
        self.assertTrue(has(errs(sc), "missing required field 'inputs'"), errs(sc))
        sc = coupon()
        del sc["priority"]["inputs"]["effort"]
        self.assertTrue(has(errs(sc), "missing required field 'effort'"), errs(sc))
        sc = coupon()
        sc["priority"]["inputs"]["effort"] = "easy"
        self.assertTrue(has(errs(sc), "priority.inputs.effort"), errs(sc))

    def test_a_critical_assumption_caps_the_band_at_medium(self):
        critical = {"type": "critical", "text": "Kupon kodunun ödeme adımında da girilebildiği varsayılıyor.",
                    "question": "Kod ödeme adımında da girilebiliyor mu?"}
        sc = scored(coupon(), "medium", "user_data", evidence="user_data")  # 7/7, capped to medium
        sc["assumptions"] = [critical]
        self.assertEqual(errs(sc), [])
        sc["priority"]["tier"] = "high"
        e = errs(sc)
        self.assertTrue(has(e, "medium at most"), e)
        self.assertFalse(has(e, "doesn't match the inputs' score"), e)  # one message for one fault


class TestEvidenceInput(unittest.TestCase):
    def test_the_input_follows_the_evidence_level(self):
        e = errs(scored(coupon(), "medium", evidence="user_data", noticeable=False, effort="medium"))
        self.assertTrue(has(e, "priority.inputs.evidence: 'user_data' doesn't match evidence.level 'archive'; "
                               "write 'archive_or_research'"), e)
        e = errs(scored(plain(), "medium", evidence="archive_or_research"))
        self.assertTrue(has(e, "write 'intuition'"), e)

    def test_users_own_behaviour_data_is_user_data(self):
        for inp, tier in (("user_data", "high"), ("behaviour_data", "high")):
            self.assertEqual(errs(scored(coupon(), tier, "user_data", evidence=inp)), [], inp)

    def test_sector_research_is_research(self):
        sc = scored(coupon(), "medium", evidence="archive_or_research")
        sc["evidence"] = {"level": "sector", "note": "Sektör raporlarında sık görülen bir gözlem."}
        self.assertEqual(errs(sc), [])


ACCORDION = "Teslimat bilgisi kapalı “Teslimat ve İade” akordeonunun içinde"


def accordion(**over):
    sc = plain()
    sc["problem"] = "Teslimat tarihi yalnız kapalı bir akordeon açılınca görünüyor."
    sc["variants"][0]["description"] = ACCORDION
    sc.update(over)
    return sc


class TestExposure(unittest.TestCase):
    def test_a_conditionally_shown_element_needs_its_trigger(self):
        e = errs(accordion())
        self.assertTrue(has(e, "exposure: the tested element is shown conditionally ('akordeon"), e)
        self.assertTrue(has(errs(accordion(), "tr"), "kimin maruz sayıldığını"))

    def test_the_trigger_names_both_arms(self):
        e = errs(accordion(exposure="Akordeon başlığı ekrana geldiğinde sayılır."))
        self.assertTrue(has(e, "same point in both arms"), e)
        self.assertEqual(errs(accordion(exposure="Akordeon başlığı ekrana geldiğinde, iki kolda aynı noktada "
                                                 "kaydedilir.")), [])

    def test_other_conditional_places(self):
        for text in ("Bilgi ilk ekranın altında duruyor", "Detay bir sekmede", "Shipping sits below the fold",
                     "Details are in a collapsed panel", "A modal shows the fee"):
            sc = plain()
            sc["variants"][0]["description"] = text
            self.assertTrue(has(errs(sc), "exposure:"), text)

    def test_a_plain_change_needs_none(self):
        self.assertEqual(errs(plain()), [])
        sc = plain()
        sc["variants"][0]["description"] = "Uygulamanın alt sekme çubuğu aynı kalır, başlık uzun"
        self.assertFalse(has(errs(sc), "exposure:"), errs(sc))

    def test_exposure_is_statistics_free_text(self):
        e = errs(accordion(exposure="İki kolda akordeon açılınca sayılır; örneklem büyüklüğü 8.000."))
        self.assertTrue(has(e, "exposure:") and has(e, "statistics language"), e)


if __name__ == "__main__":
    unittest.main()
