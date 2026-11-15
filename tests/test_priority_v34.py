#!/usr/bin/env python3
"""Priority score, 3.4 (item 47): the impact input, bands out of 9, a native release that no longer zeroes the
effort, and the tag line that shows the score ("Öncelik: Yüksek (7/9)"). Stdlib only."""
import copy
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import validate_scenario_json as vsj  # noqa: E402
from test_validate_scenario_json_v3 import SCHEMA, coupon, plain  # noqa: E402

ROOT = os.path.join(HERE, "..")
USER_DATA = {"level": "user_data", "note": "GA4 raporuna göre sepette kupon kutusunda çıkış yoğun."}
CRITICAL = {"type": "critical", "text": "Kupon kodunun ödeme adımında da girilebildiği varsayılıyor.",
            "question": "Kod ödeme adımında da girilebiliyor mu?"}


def errs(sc, lang="en"):
    return vsj.validate(sc, SCHEMA, lang)


def has(items, fragment):
    return any(fragment in item for item in items)


def scored(sc, tier, **inputs):
    sc = copy.deepcopy(sc)
    sc["priority"]["tier"] = tier
    sc["priority"]["inputs"] = dict(sc["priority"]["inputs"], **inputs)
    return sc


class TestBands(unittest.TestCase):
    def test_a_strong_main_path_change_on_an_archive_pattern_is_high(self):
        sc = scored(coupon(), "high", impact="structural")  # 1+2+1+1+2 = 7
        self.assertEqual(errs(sc), [])
        self.assertTrue(has(errs(scored(sc, "medium")), "= 7/9, which is 'high'"))

    def test_the_same_archive_change_one_step_weaker_is_medium(self):
        for weaker in ({"effort": "medium"}, {"impact": "persuasive"}, {"noticeable": False}, {"main_path": False}):
            self.assertEqual(errs(scored(coupon(), "medium", **dict({"impact": "structural"}, **weaker))), [], weaker)

    def test_intuition_alone_stays_medium_at_best(self):
        sc = scored(plain(), "medium", impact="structural")  # 0+2+1+1+2 = 6
        self.assertEqual(errs(sc), [])
        e = errs(scored(sc, "high"))
        self.assertTrue(has(e, "an 'intuition' record cannot be priority 'high'"), e)
        self.assertTrue(has(e, "= 6/9, which is 'medium'"), e)

    def test_cosmetic_and_structural_changes_no_longer_tie(self):
        # R3: "küsuratı üst simge yaz" and "yıllık dönemi varsayılan aç" both scored 5/7, both medium.
        cents = vsj.priority_score(dict(coupon()["priority"]["inputs"], impact="cosmetic"))
        annual = vsj.priority_score(dict(coupon()["priority"]["inputs"], impact="structural"))
        self.assertEqual((cents[0], vsj.score_tier(cents[0])), (5, "medium"))
        self.assertEqual((annual[0], vsj.score_tier(annual[0])), (7, "high"))

    def test_a_weak_idea_is_low(self):
        self.assertEqual(errs(scored(coupon(), "low", impact="cosmetic", main_path=False, noticeable=False)), [])

    def test_impact_is_required_and_its_hint_names_the_values(self):
        sc = coupon()
        del sc["priority"]["inputs"]["impact"]
        e = [x for x in errs(sc) if "'impact'" in x]
        self.assertEqual(len(e), 1, errs(sc))
        for part in ("added in 3.4.0", "structural", "persuasive", "cosmetic"):
            self.assertIn(part, e[0])
        sc["priority"]["inputs"]["impact"] = "big"
        self.assertTrue(has(errs(sc), "priority.inputs.impact"), errs(sc))


class TestNativeRelease(unittest.TestCase):
    def native(self, effort, rationale):
        sc = scored(coupon(), "medium", effort=effort)
        sc["device"] = "phone"
        sc["priority"]["rationale"] = rationale
        return sc

    def test_a_release_alone_is_medium_effort(self):
        rationale = "Sepetteki kaçağı hedefliyor, kanıt arşiv örüntüsü ve değişiklik bir uygulama sürümü istiyor."
        self.assertEqual(errs(self.native("medium", rationale)), [])  # 1+1+1+1+1 = 5
        self.assertEqual(vsj.lint(self.native("medium", rationale), SCHEMA, "en"), [])
        sc = scored(self.native("high", rationale), "medium")
        self.assertEqual(errs(sc), [])  # 4/9 is still medium: the warning, not the band, carries it
        w = vsj.lint(sc, SCHEMA, "tr")
        self.assertTrue(has(w, "yerel uygulama sürümü tek başına \"effort\": \"medium\""), w)

    def test_backend_work_stays_high(self):
        rationale = "Kanıt arşiv örüntüsü; değişiklik bir uygulama sürümü ve arka uç işi istiyor."
        self.assertEqual(vsj.lint(scored(self.native("high", rationale), "medium"), SCHEMA, "tr"), [])

    def test_the_native_sample_is_medium_effort(self):
        with open(os.path.join(ROOT, "examples", "samples", "app-home.json"), encoding="utf-8") as fh:
            sample = json.load(fh)
        self.assertEqual(sample["device"], "phone")
        self.assertEqual(sample["priority"]["inputs"]["effort"], "medium")
        self.assertEqual(errs(sample), [])


class TestTagLine(unittest.TestCase):
    def test_the_tag_carries_tier_and_score(self):
        self.assertEqual(vsj.priority_tag(coupon(), "tr"), "Öncelik: Orta (6/9)")
        self.assertEqual(vsj.priority_tag(scored(coupon(), "high", impact="structural"), "en"), "Priority: High (7/9)")
        self.assertEqual(vsj.priority_tag(scored(coupon(), "low", impact="cosmetic", main_path=False,
                                                 noticeable=False), "tr"), "Öncelik: Düşük (3/9)")

    def test_a_critical_assumption_shows_the_hold(self):
        sc = scored(coupon(), "medium", evidence="user_data")
        sc["evidence"] = dict(USER_DATA)
        sc["assumptions"] = [CRITICAL]
        self.assertEqual(errs(sc), [])
        self.assertEqual(vsj.priority_tag(sc, "tr"), "Öncelik: Orta (8/9, koşullu)")
        self.assertEqual(vsj.priority_tag(sc, "en"), "Priority: Medium (8/9, conditional)")

    def test_inputs_that_do_not_score_have_no_tag(self):
        sc = coupon()
        del sc["priority"]["inputs"]["impact"]
        self.assertIsNone(vsj.priority_tag(sc))


class TestShippedRecords(unittest.TestCase):
    def test_every_shipped_record_scores_and_its_tier_is_the_band(self):
        paths = [os.path.join(ROOT, "examples", "scenario.json"), os.path.join(ROOT, "docs", "demo",
                                                                               "scenario-card-en.json")]
        paths += [os.path.join(ROOT, "examples", "samples", f) for f in sorted(os.listdir(
            os.path.join(ROOT, "examples", "samples"))) if f.endswith(".json")]
        for path in paths:
            with open(path, encoding="utf-8") as fh:
                sc = json.load(fh)
            score = vsj.priority_score(sc["priority"]["inputs"])
            self.assertIsNotNone(score, path)
            self.assertEqual(sc["priority"]["tier"], vsj.score_tier(score[0], vsj.critical_open(sc)), path)


if __name__ == "__main__":
    unittest.main()
