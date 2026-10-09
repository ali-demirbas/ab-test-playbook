#!/usr/bin/env python3
"""validate_scenario_json.py için unit testler. Bağımlısız (unittest).

Şemanın var olma sebebi, CLAUDE.md'nin iki bağlayıcı kuralını yapısal olarak
zorlamak: tek birincil KPI (kural 2) ve en az bir guardrail (kural 3). Bu
testler asıl olarak o iki kuralın sessizce gevşemesine karşı korumadır; geri
kalanlar doğrulayıcının kendi alt kümesinin (required, enum, oneOf,
additionalProperties, dependentRequired) çalıştığını gösterir.
"""
import contextlib
import copy
import io
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from validate_scenario_json import validate as _validate, validate_prereg_only, main, DEFAULT_SCHEMA  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(DEFAULT_SCHEMA, encoding="utf-8") as _fh:
    SCHEMA = json.load(_fh)


def validate(scenario, schema, lang="en"):
    """The assertions below match English message fragments; Turkish (the
    default) is covered separately in TestMessages."""
    return _validate(scenario, schema, lang)


def base_scenario():
    return {
        "id": "cart-checkout-coupon-field-01",
        "title": "Açık kupon alanı sepet terkini artırır mı?",
        "source": "archive",
        "variable": "Kupon alanının görünürlüğü",
        "hypothesis": {
            "change": "Kupon alanı bağlantı arkasına alınır.",
            "mechanism": "Açık kutu kodu olmayan kullanıcıyı kod aramaya yönlendirdiği için terk artıyor.",
        },
        "variants": [
            {"id": "A", "description": "Açık kutu", "is_current": True},
            {"id": "B", "description": "Bağlantı arkasında"},
        ],
        "kpis": [
            {"name": "RPV", "role": "primary"},
            {"name": "Sipariş tamamlama", "role": "secondary"},
            {"name": "Kupon kullanımı", "role": "guardrail"},
        ],
        "test_items": ["Kaçak?", "Segment?", "Metin?"],
        "dont_items": ["Bir", "İki", "Üç"],
        "evidence": {"level": "archive"},
    }


def errors_for(**changes):
    sc = base_scenario()
    sc.update(changes)
    return validate(sc, SCHEMA)


class TestBindingRules(unittest.TestCase):
    """Şemanın asıl işi: kural 2 ve kural 3."""

    def test_valid_scenario_passes(self):
        self.assertEqual(validate(base_scenario(), SCHEMA), [])

    def test_two_primary_kpis_is_rejected(self):
        errs = errors_for(kpis=[
            {"name": "RPV", "role": "primary"},
            {"name": "CR", "role": "primary"},
            {"name": "İade", "role": "guardrail"},
        ])
        self.assertTrue(any("rule 2" in e for e in errs), errs)

    def test_no_primary_kpi_is_rejected(self):
        errs = errors_for(kpis=[
            {"name": "CR", "role": "secondary"},
            {"name": "AOV", "role": "secondary"},
            {"name": "İade", "role": "guardrail"},
        ])
        self.assertTrue(any("rule 2" in e for e in errs), errs)

    def test_primary_must_come_first(self):
        errs = errors_for(kpis=[
            {"name": "CR", "role": "secondary"},
            {"name": "RPV", "role": "primary"},
            {"name": "İade", "role": "guardrail"},
        ])
        self.assertTrue(any("first KPI" in e and "rule 2" in e for e in errs), errs)

    def test_missing_guardrail_is_rejected(self):
        errs = errors_for(kpis=[
            {"name": "RPV", "role": "primary"},
            {"name": "CR", "role": "secondary"},
            {"name": "AOV", "role": "secondary"},
        ])
        self.assertTrue(any("rule 3" in e for e in errs), errs)

    def test_five_equally_weighted_metrics_is_rejected(self):
        # Kural 2'nin yasakladığı tam senaryo: beş metrik, hiçbiri işaretli değil.
        errs = errors_for(kpis=[{"name": "M%d" % i, "role": "secondary"} for i in range(5)])
        self.assertTrue(any("rule 2" in e for e in errs), errs)
        self.assertTrue(any("rule 3" in e for e in errs), errs)


class TestVariants(unittest.TestCase):
    def test_three_variants_is_rejected(self):
        errs = errors_for(variants=[
            {"id": "A", "description": "a"},
            {"id": "B", "description": "b"},
            {"id": "A", "description": "c"},
        ])
        self.assertTrue(any("maximum is 2" in e for e in errs), errs)

    def test_single_variant_is_rejected(self):
        errs = errors_for(variants=[{"id": "A", "description": "a"}])
        self.assertTrue(any("minimum is 2" in e for e in errs), errs)

    def test_unknown_variant_id_is_rejected(self):
        errs = errors_for(variants=[
            {"id": "A", "description": "a"},
            {"id": "C", "description": "c"},
        ])
        self.assertTrue(any("not one of" in e for e in errs), errs)


class TestStructure(unittest.TestCase):
    def test_missing_required_field(self):
        sc = base_scenario()
        del sc["hypothesis"]
        errs = validate(sc, SCHEMA)
        self.assertTrue(any("hypothesis" in e and "required" in e for e in errs), errs)

    def test_missing_mechanism_is_rejected(self):
        # Mekanizmasız hipotez tahmindir; şema bunu şekil düzeyinde yakalar.
        errs = errors_for(hypothesis={"change": "Bir şey değişir."})
        self.assertTrue(any("mechanism" in e for e in errs), errs)

    def test_unknown_field_is_rejected(self):
        errs = errors_for(sonuc="kazandı")
        self.assertTrue(any("unknown field" in e for e in errs), errs)

    def test_bad_id_pattern(self):
        errs = errors_for(id="Cart Checkout 01")
        self.assertTrue(any("does not match" in e for e in errs), errs)

    def test_bad_evidence_level(self):
        errs = errors_for(evidence={"level": "hunch"})
        self.assertTrue(any("not one of" in e for e in errs), errs)

    def test_source_must_be_stated(self):
        sc = base_scenario()
        del sc["source"]
        errs = validate(sc, SCHEMA)
        self.assertTrue(any("source" in e for e in errs), errs)


class TestBoxItems(unittest.TestCase):
    def test_plain_string_item_is_accepted(self):
        self.assertEqual(errors_for(test_items=["düz madde", "iki", "üç"]), [])

    def test_labelled_item_is_accepted(self):
        self.assertEqual(errors_for(test_items=[{"label": "Konum", "text": "soru?"}, "iki", "üç"]), [])

    def test_item_missing_text_is_rejected(self):
        errs = errors_for(test_items=[{"label": "Konum"}, "iki", "üç"])
        self.assertTrue(any("oneOf" in e for e in errs), errs)

    def test_each_box_needs_three_items(self):
        # Kural 1: üç kutu eksiksiz; iki maddelik bir kutu eksik kutudur.
        for key in ("test_items", "dont_items"):
            errs = errors_for(**{key: ["bir", "iki"]})
            self.assertTrue(any(key in e and "minimum is 3" in e for e in errs), (key, errs))
        errs = errors_for(kpis=[{"name": "RPV", "role": "primary"}, {"name": "İade", "role": "guardrail"}])
        self.assertTrue(any("kpis" in e and "minimum is 3" in e for e in errs), errs)

    def test_boxes_are_required(self):
        sc = base_scenario()
        del sc["dont_items"]
        self.assertTrue(any("dont_items" in e for e in validate(sc, SCHEMA)))


class TestSample(unittest.TestCase):
    def test_duration_without_traffic_flag_is_rejected(self):
        # Kural 5: trafik bilinmeden süre vaadi verilmez.
        errs = errors_for(sample={"estimated_days": 14})
        self.assertTrue(any("requires" in e for e in errs), errs)

    def test_duration_with_traffic_flag_is_accepted(self):
        self.assertEqual(errors_for(sample={"traffic_known": True, "estimated_days": 14}), [])

    def test_sample_mde_must_be_a_fraction(self):
        self.assertTrue(errors_for(sample={"traffic_known": True, "mde": 5}))


def base_prereg():
    return {
        "hypothesis": "Kupon alanını gizlemek RPV'yi artırır.",
        "variable": "Kupon alanının görünürlüğü",
        "primary_kpi": {"name": "RPV", "direction": "increase"},
        "guardrails": [{"name": "Kupon kullanımı", "direction": "must_not_decrease",
                        "margin_relative": 0.05}],
        "mde": None,
        "alpha": 0.05,
        "power": 0.8,
        "alternative": "two-sided",
        "allocation": {"A": 0.5, "B": 0.5},
        "planned_n_per_arm": None,
        "duration_days": None,
        "decision_rule": "RPV anlamlı artar ve guardrail marj içinde kalırsa yayına al.",
        "segments": ["device"],
    }


def prereg_errors(**changes):
    pre = base_prereg()
    pre.update(changes)
    return errors_for(preregistration=pre)


class TestPreregistration(unittest.TestCase):
    def test_valid_block_is_accepted(self):
        self.assertEqual(prereg_errors(), [])

    def test_block_is_optional(self):
        self.assertEqual(errors_for(), [])

    def test_unknown_numbers_may_be_null(self):
        self.assertEqual(prereg_errors(mde=None, planned_n_per_arm=None, duration_days=None), [])

    def test_guardrail_without_margin_is_rejected(self):
        errs = prereg_errors(guardrails=[{"name": "Kupon kullanımı", "direction": "must_not_decrease"}])
        self.assertTrue(any("margin_relative" in e for e in errs), errs)

    def test_empty_guardrails_is_rejected(self):
        self.assertTrue(prereg_errors(guardrails=[]))

    def test_allocation_must_sum_to_one(self):
        errs = prereg_errors(allocation={"A": 0.5, "B": 0.4})
        self.assertTrue(any("sum" in e for e in errs), errs)

    def test_uneven_allocation_summing_to_one_is_accepted(self):
        self.assertEqual(prereg_errors(allocation={"A": 0.9, "B": 0.1}), [])

    def test_bad_alternative_is_rejected(self):
        self.assertTrue(prereg_errors(alternative="one-sided"))

    def test_alpha_out_of_range_is_rejected(self):
        self.assertTrue(prereg_errors(alpha=1.5))

    def test_primary_kpi_must_match_scenario(self):
        errs = prereg_errors(primary_kpi={"name": "CR", "direction": "increase"})
        self.assertTrue(any("primary KPI" in e for e in errs), errs)

    def test_missing_decision_rule_is_rejected(self):
        pre = base_prereg()
        del pre["decision_rule"]
        errs = errors_for(preregistration=pre)
        self.assertTrue(any("decision_rule" in e for e in errs), errs)

    def test_primary_name_match_ignores_case_and_whitespace(self):
        self.assertEqual(prereg_errors(primary_kpi={"name": "  rpv ", "direction": "increase"}), [])

    def test_variable_must_match_scenario(self):
        errs = prereg_errors(variable="Kupon alanının rengi")
        self.assertTrue(any("variable" in e for e in errs), errs)
        self.assertEqual(prereg_errors(variable="kupon  alanının görünürlüğü"), [])

    def test_guardrail_must_exist_in_kpis(self):
        errs = prereg_errors(guardrails=[{"name": "İade oranı", "direction": "must_not_increase",
                                          "margin_relative": 0.05}])
        self.assertTrue(any("not in the scenario's KPI list" in e for e in errs), errs)

    def test_guardrail_must_be_a_guardrail_kpi(self):
        errs = prereg_errors(guardrails=[{"name": "Sipariş tamamlama", "direction": "must_not_decrease",
                                          "margin_relative": 0.05}])
        self.assertTrue(any("expected guardrail" in e for e in errs), errs)

    def test_check_guardrail_needs_no_margin(self):
        pre = base_prereg()
        pre["guardrails"].append({"name": "Kupon kullanımı", "type": "check",
                                  "criterion": "Klavye ve ekran okuyucu kontrolünde kritik bulgu yok"})
        self.assertEqual(errors_for(preregistration=pre), [])

    def test_check_guardrail_cannot_carry_a_margin(self):
        errs = prereg_errors(guardrails=[{"name": "Kupon kullanımı", "type": "check", "margin_relative": 0.05}])
        self.assertTrue(any("oneOf" in e for e in errs), errs)

    def test_lagging_guardrail_read_after_days(self):
        self.assertEqual(prereg_errors(guardrails=[{"name": "Kupon kullanımı", "direction": "must_not_decrease",
                                                    "margin_relative": 0.05, "read_after_days": 30}]), [])
        self.assertTrue(prereg_errors(guardrails=[{"name": "Kupon kullanımı", "direction": "must_not_decrease",
                                                   "margin_relative": 0.05, "read_after_days": 0}]))

    def test_alternative_must_agree_with_direction(self):
        errs = prereg_errors(alternative="less")
        self.assertTrue(any("contradicts" in e for e in errs), errs)
        self.assertEqual(prereg_errors(alternative="greater"), [])
        errs = prereg_errors(primary_kpi={"name": "RPV", "direction": "decrease"}, alternative="greater")
        self.assertTrue(any("contradicts" in e for e in errs), errs)

    def test_mde_must_be_a_fraction(self):
        self.assertTrue(prereg_errors(mde=5))
        self.assertTrue(prereg_errors(mde=0))
        self.assertEqual(prereg_errors(mde=0.05), [])

    def test_alpha_ceiling(self):
        self.assertTrue(prereg_errors(alpha=0.25))
        self.assertEqual(prereg_errors(alpha=0.2), [])
        self.assertTrue(prereg_errors(alpha=0))

    def test_numbers_need_known_traffic(self):
        # Kural 5: trafik bilinmeden örneklem ve süre sayısı yazılmaz.
        errs = prereg_errors(duration_days=14)
        self.assertTrue(any("rule 5" in e for e in errs), errs)
        errs = prereg_errors(planned_n_per_arm=5000)
        self.assertTrue(any("rule 5" in e for e in errs), errs)
        pre = base_prereg()
        pre["duration_days"] = 14
        self.assertEqual(errors_for(preregistration=pre, sample={"traffic_known": True}), [])


class TestSourceAndIce(unittest.TestCase):
    def test_adapted_source_names_its_original(self):
        errs = errors_for(source="adapted")
        self.assertTrue(any("adapted_from" in e and "rule 8" in e for e in errs), errs)
        self.assertEqual(errors_for(source="adapted", adapted_from="Kupon kutusu görünürlüğü"), [])

    def test_archive_scenario_is_not_downgraded_to_intuition(self):
        errs = errors_for(evidence={"level": "intuition"})
        self.assertTrue(any("rule 8" in e for e in errs), errs)
        self.assertEqual(errors_for(source="generated", evidence={"level": "intuition"}), [])

    def test_ice_tier_matches_scores(self):
        self.assertEqual(errors_for(ice={"tier": "medium", "impact": 7, "confidence": 4, "ease": 9}), [])
        errs = errors_for(ice={"tier": "high", "impact": 7, "confidence": 4, "ease": 9})
        self.assertTrue(any("ice.tier" in e for e in errs), errs)
        self.assertEqual(errors_for(ice={"tier": "low"}), [])

    def test_lang_enum(self):
        self.assertEqual(errors_for(lang="en"), [])
        self.assertTrue(errors_for(lang="de"))


def base_card(**over):
    card = {
        "difference": "add",
        "variant_a": '<div class="r-h">Sepet</div>',
        "variant_b": '<div class="hl" data-note="yeni"><div class="r-h">Sepet</div></div>',
    }
    card.update(over)
    return card


class TestCard(unittest.TestCase):
    """build_card'ın ihtiyacı olan her alan şemada tanımlı; halka kuralı ortak."""

    def test_full_card_is_accepted(self):
        card = base_card(device="phone-web", url="magaza.example/sepet", bottom_nav=[],
                         brand={"primary": "#c9392b", "on_primary": "#fff", "name": "Örnek"},
                         brand_note=None, mockup_basis="shared_page", note_pos="below",
                         shift_note_a="A", shift_note_b="B", footer_notes=["Adres temsilîdir."])
        self.assertEqual(errors_for(card=card), [])

    def test_difference_is_required(self):
        card = base_card()
        del card["difference"]
        self.assertTrue(any("difference" in e for e in errors_for(card=card)))

    def test_turkish_difference_is_accepted(self):
        self.assertEqual(errors_for(card=base_card(difference="ekle")), [])

    def test_ring_placement_is_checked(self):
        errs = errors_for(card=base_card(variant_a=base_card()["variant_b"]))
        self.assertTrue(any("difference 'add'" in e for e in errs), errs)

    def test_remove_needs_shift_note(self):
        card = base_card(difference="remove", variant_a=base_card()["variant_b"],
                         variant_b='<div class="r-h">Sepet</div>')
        self.assertTrue(any("shift_note_b" in e for e in errors_for(card=card)))
        card["shift_note_b"] = "Alan kaldırıldı, içerik yukarı kaydı"
        self.assertEqual(errors_for(card=card), [])

    def test_both_device_is_gone(self):
        self.assertTrue(errors_for(device="both"))
        self.assertEqual(errors_for(device="phone-web"), [])

    def test_brand_colour_pattern(self):
        self.assertTrue(errors_for(card=base_card(brand={"primary": "red}</style>"})))


class TestPreregOnly(unittest.TestCase):
    def test_bare_block_is_accepted(self):
        self.assertEqual(validate_prereg_only({"preregistration": base_prereg()}, SCHEMA, "en"), [])

    def test_bare_block_still_checks_internal_rules(self):
        pre = base_prereg()
        pre["allocation"] = {"A": 0.6, "B": 0.6}
        pre["alternative"] = "less"
        pre["duration_days"] = 14
        errs = validate_prereg_only({"preregistration": pre}, SCHEMA, "en")
        self.assertTrue(any("sum" in e for e in errs), errs)
        self.assertTrue(any("contradicts" in e for e in errs), errs)
        self.assertTrue(any("rule 5" in e for e in errs), errs)

    def test_sample_sibling_unlocks_numbers(self):
        pre = base_prereg()
        pre["duration_days"] = 14
        doc = {"preregistration": pre, "sample": {"traffic_known": True}}
        self.assertEqual(validate_prereg_only(doc, SCHEMA, "en"), [])

    def test_wrong_shape_is_reported(self):
        self.assertTrue(validate_prereg_only(base_prereg(), SCHEMA, "en"))
        errs = validate_prereg_only({"preregistration": base_prereg(), "kpis": []}, SCHEMA, "en")
        self.assertTrue(any("unknown field" in e for e in errs), errs)

    def test_cli_mode(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "pre.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"preregistration": base_prereg()}, fh)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(["--prereg-only", path]), 0)
            self.assertIn("ok", out.getvalue())


class TestMessages(unittest.TestCase):
    def test_turkish_is_the_default(self):
        sc = base_scenario()
        sc["kpis"] = [{"name": "CR", "role": "secondary"}, {"name": "A", "role": "secondary"},
                      {"name": "B", "role": "secondary"}]
        errs = _validate(sc, SCHEMA)
        self.assertTrue(any("kural 2" in e for e in errs), errs)
        self.assertTrue(any("kural 3" in e for e in errs), errs)
        self.assertFalse(any("rule 2" in e for e in errs), errs)

    def test_english_on_request(self):
        sc = base_scenario()
        del sc["source"]
        errs = _validate(sc, SCHEMA, "en")
        self.assertTrue(any("missing required field 'source'" in e for e in errs), errs)


class TestExampleFile(unittest.TestCase):
    def test_shipped_example_validates(self):
        if not os.path.isfile(EXAMPLE):
            self.skipTest("examples/scenario.json bulunamadı")
        with open(EXAMPLE, encoding="utf-8") as fh:
            self.assertEqual(validate(json.load(fh), SCHEMA), [])

    def test_shipped_example_carries_a_renderable_card(self):
        # Tek JSON: aynı dosya hem doğrulanır hem kartı üretir.
        with open(EXAMPLE, encoding="utf-8") as fh:
            sc = json.load(fh)
        self.assertIn("card", sc)
        for key in ("variant_a", "variant_b", "difference"):
            self.assertIn(key, sc["card"])


if __name__ == "__main__":
    unittest.main()
