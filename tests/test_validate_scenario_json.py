#!/usr/bin/env python3
"""validate_scenario_json.py için unit testler. Bağımlısız (unittest).

Şemanın var olma sebebi, CLAUDE.md'nin iki bağlayıcı kuralını yapısal olarak
zorlamak: tek birincil KPI (kural 2) ve en az bir guardrail (kural 3). Bu
testler asıl olarak o iki kuralın sessizce gevşemesine karşı korumadır; geri
kalanlar doğrulayıcının kendi alt kümesinin (required, enum, oneOf,
additionalProperties, dependentRequired) çalıştığını gösterir.
"""
import copy
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from validate_scenario_json import validate, DEFAULT_SCHEMA  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(DEFAULT_SCHEMA, encoding="utf-8") as _fh:
    SCHEMA = json.load(_fh)


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
            {"name": "Kupon kullanımı", "role": "guardrail"},
        ],
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
            {"name": "İade", "role": "guardrail"},
        ])
        self.assertTrue(any("rule 2" in e for e in errs), errs)

    def test_missing_guardrail_is_rejected(self):
        errs = errors_for(kpis=[
            {"name": "RPV", "role": "primary"},
            {"name": "CR", "role": "secondary"},
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
        self.assertEqual(errors_for(test_items=["düz madde"]), [])

    def test_labelled_item_is_accepted(self):
        self.assertEqual(errors_for(test_items=[{"label": "Konum", "text": "soru?"}]), [])

    def test_item_missing_text_is_rejected(self):
        errs = errors_for(test_items=[{"label": "Konum"}])
        self.assertTrue(any("oneOf" in e for e in errs), errs)


class TestSample(unittest.TestCase):
    def test_duration_without_traffic_flag_is_rejected(self):
        # Kural 5: trafik bilinmeden süre vaadi verilmez.
        errs = errors_for(sample={"estimated_days": 14})
        self.assertTrue(any("requires" in e for e in errs), errs)

    def test_duration_with_traffic_flag_is_accepted(self):
        self.assertEqual(errors_for(sample={"traffic_known": True, "estimated_days": 14}), [])


class TestExampleFile(unittest.TestCase):
    def test_shipped_example_validates(self):
        if not os.path.isfile(EXAMPLE):
            self.skipTest("examples/scenario.json bulunamadı")
        with open(EXAMPLE, encoding="utf-8") as fh:
            self.assertEqual(validate(json.load(fh), SCHEMA), [])


if __name__ == "__main__":
    unittest.main()
