#!/usr/bin/env python3
"""validate_scenario_json.py için unit testler. Bağımlısız (unittest).

Şemanın var olma sebebi, CLAUDE.md'nin bağlayıcı kurallarını yapısal olarak
zorlamak: her önerinin on alanlı bir senaryo kaydı olması (kural 1), tek
birincil KPI (kural 2) ve bir guardrail (kural 3). Bu testler asıl olarak o
kuralların sessizce gevşemesine karşı korumadır; geri kalanlar doğrulayıcının
kendi alt kümesinin (required, enum, oneOf, additionalProperties), isteğe
bağlı detay görünümünün ve öncelik alanının (kademe + gerekçe, puan yok)
çalıştığını gösterir.
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from validate_scenario_json import validate as _validate, DEFAULT_SCHEMA  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(DEFAULT_SCHEMA, encoding="utf-8") as _fh:
    SCHEMA = json.load(_fh)


def validate(scenario, schema, lang="en"):
    """The assertions below match English message fragments; Turkish (the
    default) is covered separately in TestMessages."""
    return _validate(scenario, schema, lang)


ARCHIVE_TITLE = "Açık kupon kodu alanı sepet terkini artırır mı?"  # Değişken: Kupon kodu alanının görünürlüğü · Fark: değiştir
SOURCE_NOTE = "Arşivde bu sayfanın taksit satırına uyan bir senaryo yok; en yakını kupon alanını değiştirir."


def base_scenario():
    """The corrected coupon record (CONTRACT stage 3): every gate it meets is a gate the old one failed."""
    return {
        "id": "cart-checkout-coupon-field-01",
        "title": "Kupon alanını “İndirim kodum var” bağlantısının arkasına almak sepetten çıkışı azaltır mı?",
        "problem": "Açık kupon kutusu kodu olmayan kullanıcıyı kod aramak için sepetten çıkarıyor.",
        "mechanism": "Bağlantı arkasındaki alan eksik indirimi hatırlatmadığı için kod arama nedeni kalkar.",
        "variable": "Kupon kodu alanının görünürlüğü",
        "variants": [
            {"id": "A", "description": "Açık kutu", "is_current": True},
            {"id": "B", "description": "Bağlantı arkasında"},
        ],
        "difference": "change",
        "primary_kpi": {"name": "Sipariş Tamamlama Oranı", "denominator": "Sepet sayfasına ulaşan ziyaretçi",
                        "direction": "increase"},
        "guardrail": {"name": "Kupon Kullanım Oranı", "kind": "metric", "denominator": "Tamamlanan sipariş",
                      "direction": "must_not_decrease"},
        "invariants": ["Geçerli bir kod iki kolda da aynı adımla uygulanır.",
                       "İndirim iki kolda da toplam tutara aynı hesapla yansır.",
                       "Geçersiz bir kod iki kolda da aynı hata mesajını alır."],
        "warnings": [{"type": "accessibility",
                      "text": "Bağlantı klavyeyle erişilebilir, ekran okuyucuda adıyla okunur, dokunma alanı en az "
                              "44×44 pt ve kontrastı en az 4.5:1 olmalı."}],
        "source": "adapted",
        "adapted_from": ARCHIVE_TITLE,
        "evidence": {"level": "archive"},
        "priority": {"tier": "medium", "rationale": "Sepetteki kaçağı hedefliyor, kanıt arşiv örüntüsü ve iş küçük.",
                     "inputs": {"evidence": "archive_or_research", "main_path": True, "noticeable": True, "effort": "low"}},
    }


def generated(**changes):
    """The base record produced for the page, so the archive's Fark doesn't pin its difference."""
    return dict(base_scenario(), source="generated", source_note=SOURCE_NOTE, **changes)


def detail(**over):
    d = {
        "test_items": ["Kaçak?", "Segment?", "Metin?"],
        "kpis": [
            {"name": "RPV", "role": "primary"},
            {"name": "Sipariş tamamlama", "role": "secondary"},
            {"name": "Kupon kullanımı", "role": "guardrail", "question": "Çökmemeli."},
        ],
        "dont_items": ["Bir", "İki", "Üç"],
    }
    d.update(over)
    return d


def errors_for(**changes):
    sc = base_scenario()
    sc.update(changes)
    return validate(sc, SCHEMA)


class TestBindingRules(unittest.TestCase):
    """Şemanın asıl işi: kural 1, 2 ve 3, kaydın kendisinde yapısal."""

    def test_valid_scenario_passes(self):
        self.assertEqual(validate(base_scenario(), SCHEMA), [])

    def test_the_ten_fields_are_required(self):
        for key in ("id", "title", "problem", "mechanism", "variable", "variants", "primary_kpi", "guardrail",
                    "source", "evidence", "priority"):
            sc = base_scenario()
            del sc[key]
            errs = validate(sc, SCHEMA)
            self.assertTrue(any("missing required field %r" % key in e for e in errs), (key, errs))

    def test_primary_kpi_is_one_object_not_a_list(self):
        # Kural 2 yapısal: birincil KPI bir nesnedir, eşit ağırlıklı bir liste değil.
        errs = errors_for(primary_kpi=[{"name": "RPV"}, {"name": "CR"}])
        self.assertTrue(any("primary_kpi: expected type object" in e for e in errs), errs)

    def test_primary_kpi_needs_name_denominator_and_direction(self):
        for key in ("name", "denominator", "direction"):
            sc = base_scenario()
            del sc["primary_kpi"][key]
            errs = validate(sc, SCHEMA)
            self.assertTrue(any("primary_kpi: missing required field %r" % key in e for e in errs), (key, errs))
        errs = errors_for(primary_kpi=dict(base_scenario()["primary_kpi"], direction="unknown"))
        self.assertTrue(any(e.startswith("primary_kpi.direction:") for e in errs), errs)

    def test_guardrail_is_required_and_takes_one_shape(self):
        # Kural 3: guardrail ya bir metrik ya bir kontrol; ikisinin karışımı değil.
        errs = errors_for(guardrail={"name": "İade Oranı"})
        self.assertTrue(any(e.startswith("guardrail:") for e in errs), errs)
        check = {"name": "Erişilebilirlik Kontrolü (yayın öncesi, geçti/kaldı)", "kind": "check",
                 "criterion": "Geçmeli: B’nin klavye ve ekran okuyucu incelemesinde kritik sorun yok."}
        self.assertEqual(errors_for(guardrail=check), [])


class TestDetail(unittest.TestCase):
    """Detay görünümü yalnızca istendiğinde vardır; varsa eski kutu kuralları geçerli."""

    def test_detail_is_optional(self):
        self.assertNotIn("detail", base_scenario())
        self.assertEqual(validate(base_scenario(), SCHEMA), [])

    def test_detail_on_request_passes(self):
        self.assertEqual(errors_for(detail=detail()), [])

    def test_two_primary_kpis_is_rejected(self):
        errs = errors_for(detail=detail(kpis=[
            {"name": "RPV", "role": "primary"},
            {"name": "CR", "role": "primary"},
            {"name": "İade", "role": "guardrail"},
        ]))
        self.assertTrue(any("detail.kpis" in e and "rule 2" in e for e in errs), errs)

    def test_no_primary_kpi_is_rejected(self):
        errs = errors_for(detail=detail(kpis=[
            {"name": "CR", "role": "secondary"},
            {"name": "AOV", "role": "secondary"},
            {"name": "İade", "role": "guardrail"},
        ]))
        self.assertTrue(any("rule 2" in e for e in errs), errs)

    def test_primary_must_come_first(self):
        errs = errors_for(detail=detail(kpis=[
            {"name": "CR", "role": "secondary"},
            {"name": "RPV", "role": "primary"},
            {"name": "İade", "role": "guardrail"},
        ]))
        self.assertTrue(any("first KPI" in e and "rule 2" in e for e in errs), errs)

    def test_missing_guardrail_is_rejected(self):
        errs = errors_for(detail=detail(kpis=[
            {"name": "RPV", "role": "primary"},
            {"name": "CR", "role": "secondary"},
            {"name": "AOV", "role": "secondary"},
        ]))
        self.assertTrue(any("rule 3" in e for e in errs), errs)

    def test_five_equally_weighted_metrics_is_rejected(self):
        # Kural 2'nin yasakladığı tam senaryo: beş metrik, hiçbiri işaretli değil.
        errs = errors_for(detail=detail(kpis=[{"name": "M%d" % i, "role": "secondary"} for i in range(5)]))
        self.assertTrue(any("rule 2" in e for e in errs), errs)
        self.assertTrue(any("rule 3" in e for e in errs), errs)

    def test_plain_string_item_is_accepted(self):
        self.assertEqual(errors_for(detail=detail(test_items=["düz madde", "iki", "üç"])), [])

    def test_labelled_item_is_accepted(self):
        self.assertEqual(errors_for(detail=detail(test_items=[{"label": "Konum", "text": "soru?"}, "iki", "üç"])), [])

    def test_item_missing_text_is_rejected(self):
        errs = errors_for(detail=detail(test_items=[{"label": "Konum"}, "iki", "üç"]))
        self.assertTrue(any("oneOf" in e for e in errs), errs)

    def test_each_box_needs_three_items(self):
        for key in ("test_items", "dont_items"):
            errs = errors_for(detail=detail(**{key: ["bir", "iki"]}))
            self.assertTrue(any("detail.%s" % key in e and "minimum is 3" in e for e in errs), (key, errs))
        errs = errors_for(detail=detail(kpis=[{"name": "RPV", "role": "primary"}, {"name": "İade", "role": "guardrail"}]))
        self.assertTrue(any("detail.kpis" in e and "minimum is 3" in e for e in errs), errs)

    def test_detail_needs_all_three_boxes(self):
        d = detail()
        del d["dont_items"]
        errs = errors_for(detail=d)
        self.assertTrue(any("detail: missing required field 'dont_items'" in e for e in errs), errs)


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

    def test_difference_enum(self):
        # A generated record: an adapted one keeps the archive's Fark (TestArchive in the v3 tests).
        for diff in ("change", "add", "move", "remove"):
            self.assertEqual(validate(generated(difference=diff), SCHEMA), [], diff)
        self.assertTrue(any(e.startswith("difference:") for e in validate(generated(difference="swap"), SCHEMA)))


class TestStructure(unittest.TestCase):
    def test_missing_mechanism_is_rejected(self):
        # Mekanizmasız bir öneri tahmindir; şema bunu şekil düzeyinde yakalar.
        sc = base_scenario()
        del sc["mechanism"]
        self.assertTrue(any("mechanism" in e for e in validate(sc, SCHEMA)))

    def test_unknown_field_is_rejected(self):
        errs = errors_for(sonuc="kazandı")
        self.assertTrue(any("unknown field" in e for e in errs), errs)

    def test_top_level_fields_are_the_contract_list(self):
        # v3 kaydı: on bilgi alanı + bağlam + isteğe bağlı detay ve kart katmanı.
        self.assertEqual(sorted(SCHEMA["properties"]), sorted([
            "id", "title", "problem", "mechanism", "variable", "variants", "difference", "primary_kpi", "guardrail",
            "source", "adapted_from", "source_note", "evidence", "priority", "warnings", "invariants",
            "numeric_change", "exposure", "assumptions", "review", "lang", "stage", "device", "market", "objection", "detail",
            "card"]))
        self.assertIs(SCHEMA["additionalProperties"], False)

    def test_removed_fields_are_unknown(self):
        for key, value in (("history", {"tested_before": False}),
                           ("ice", {"tier": "medium", "impact": 6, "confidence": 5, "ease": 8}),
                           ("sample", {"traffic_known": False}),
                           ("rationale", "Neden test edilmeli."),
                           ("hypothesis", {"change": "x", "mechanism": "y"}),
                           ("test_items", ["a", "b", "c"]),
                           ("kpis", [{"name": "RPV", "role": "primary"}]),
                           ("dont_items", ["a", "b", "c"])):
            errs = errors_for(**{key: value})
            self.assertTrue(any("unknown field %r" % key in e for e in errs), (key, errs))

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


class TestWarningsField(unittest.TestCase):
    TEXT = "B’nin metni için uyum onayı alınmadan teste trafik açılmaz."

    def test_typed_warnings_are_accepted(self):
        # Next to the base record's accessibility warning, which its link requires.
        for kind in ("accessibility", "regulation", "feasibility", "privacy", "market"):
            warnings = base_scenario()["warnings"] + [{"type": kind, "text": self.TEXT}]
            self.assertEqual(errors_for(warnings=warnings), [], kind)

    def test_at_most_three(self):
        errs = errors_for(warnings=[{"type": "regulation", "text": self.TEXT}] * 4)
        self.assertTrue(any("warnings: has 4 item(s), maximum is 3" in e for e in errs), errs)

    def test_omitted_rather_than_empty(self):
        errs = errors_for(warnings=[])
        self.assertTrue(any("warnings: has 0 item(s), minimum is 1" in e for e in errs), errs)

    def test_unknown_type_and_missing_text(self):
        errs = errors_for(warnings=[{"type": "legal", "text": self.TEXT}])
        self.assertTrue(any(e.startswith("warnings[0].type:") for e in errs), errs)
        errs = errors_for(warnings=[{"type": "regulation"}])
        self.assertTrue(any("missing required field 'text'" in e for e in errs), errs)


class TestSourceAndPriority(unittest.TestCase):
    def test_adapted_and_archive_name_their_original(self):
        for source in ("adapted", "archive"):
            sc = base_scenario()
            sc["source"] = source
            del sc["adapted_from"]
            errs = validate(sc, SCHEMA)
            self.assertTrue(any(e.startswith("adapted_from:") and "rule 8" in e for e in errs), (source, errs))
        # The title is a real archive title (a made-up one is refused, see the v3 tests).
        for source in ("adapted", "archive"):
            self.assertEqual(errors_for(source=source, adapted_from=ARCHIVE_TITLE), [], source)

    def test_generated_carries_a_source_note(self):
        sc = base_scenario()
        sc["source"] = "generated"
        del sc["adapted_from"]
        errs = validate(sc, SCHEMA)
        self.assertTrue(any(e.startswith("source_note:") and "rule 8" in e for e in errs), errs)
        sc["source_note"] = SOURCE_NOTE
        self.assertEqual(validate(sc, SCHEMA), [])
        sc["source_note"] = "   "
        self.assertTrue(any(e.startswith("source_note:") for e in validate(sc, SCHEMA)))

    def test_archive_scenario_is_not_downgraded_to_intuition(self):
        errs = errors_for(evidence={"level": "intuition"})
        self.assertTrue(any("rule 8" in e for e in errs), errs)
        self.assertEqual(errors_for(source="generated", source_note="Arşivde uyan senaryo yok.",
                                    evidence={"level": "intuition"},
                                    priority={"tier": "medium", "rationale": self.RATIONALE, "inputs": {
                                        "evidence": "intuition", "main_path": True, "noticeable": True,
                                        "effort": "low"}}), [])

    RATIONALE = "Sepetteki kaçağı hedefliyor, kanıt arşiv örüntüsü ve yalnızca alanın görünümü değişiyor."

    def test_priority_is_required(self):
        sc = base_scenario()
        del sc["priority"]
        self.assertTrue(any("missing required field 'priority'" in e for e in validate(sc, SCHEMA)))

    INPUTS = {"evidence": "archive_or_research", "main_path": True, "noticeable": True, "effort": "low"}

    def test_priority_tier_enum(self):
        user_data = {"level": "user_data", "note": "GA4 raporuna göre sepette kupon kutusunda çıkış yoğun."}
        for tier, evidence, inputs in (
                ("high", user_data, dict(self.INPUTS, evidence="user_data")),
                ("medium", {"level": "archive"}, self.INPUTS),
                ("low", {"level": "archive"}, dict(self.INPUTS, main_path=False, noticeable=False, effort="high"))):
            self.assertEqual(errors_for(evidence=evidence, priority={"tier": tier, "rationale": self.RATIONALE,
                                                                     "inputs": inputs}), [], tier)
        for tier in ("orta", "Medium", "very-high", 3):
            errs = errors_for(priority={"tier": tier, "rationale": self.RATIONALE, "inputs": self.INPUTS})
            self.assertTrue(any(e.startswith("priority.tier:") for e in errs), (tier, errs))

    def test_priority_rationale_is_required_and_not_empty(self):
        errs = errors_for(priority={"tier": "medium"})
        self.assertTrue(any("missing required field 'rationale'" in e for e in errs), errs)
        errs = errors_for(priority={"tier": "medium", "rationale": ""})
        self.assertTrue(any(e.startswith("priority.rationale:") and "minLength" in e for e in errs), errs)
        errs = errors_for(priority={"rationale": self.RATIONALE})
        self.assertTrue(any("missing required field 'tier'" in e for e in errs), errs)

    def test_priority_carries_no_numeric_scores(self):
        errs = errors_for(priority={"tier": "medium", "rationale": self.RATIONALE, "impact": 6})
        self.assertTrue(any("unknown field 'impact'" in e for e in errs), errs)
        errs = errors_for(priority="medium")
        self.assertTrue(any("priority: expected type object" in e for e in errs), errs)

    def test_lang_enum(self):
        self.assertEqual(errors_for(lang="en"), [])
        self.assertTrue(errors_for(lang="de"))


def base_card(**over):
    card = {
        "difference": "add",
        "variant_a": '<div class="r-h">Sepet</div>',
        "variant_b": '<div class="hl" data-note="Yeni"><div class="r-h">Sepet</div></div>',
    }
    card.update(over)
    return card


def errors_for_card(card):
    """The card on a generated record that states the same difference: card.difference only repeats it."""
    diff = card.get("difference")
    diff = {"ekle": "add", "değiştir": "change", "taşı": "move", "kaldır": "remove"}.get(diff, diff)
    return validate(generated(difference=diff, card=card), SCHEMA)


class TestCard(unittest.TestCase):
    """build_card'ın ihtiyacı olan her alan şemada tanımlı; halka kuralı ortak."""

    def test_full_card_is_accepted(self):
        card = base_card(device="phone-web", url="magaza.example/sepet", bottom_nav=[],
                         brand={"primary": "#c9392b", "on_primary": "#fff", "name": "Örnek"},
                         mockup_basis="shared_page", note_pos="below")
        self.assertEqual(errors_for_card(card), [])

    def test_removed_card_text_fields_are_refused(self):
        # The card shows the title and the two mockups only: the brand note,
        # footer notes and shift notes are gone from the card and the schema.
        for field, value in (("brand_note", "Renkleri ekrandan aldım."), ("footer_notes", ["Not"]),
                             ("shift_note_a", "A"), ("shift_note_b", "İçerik yukarı kaydı")):
            with self.subTest(field):
                errs = errors_for(card=base_card(**{field: value}))
                self.assertIn("card: unknown field '%s'" % field, errs)

    def test_difference_is_required(self):
        # Kartta da kayıtta da yoksa halka yerleşimi denetlenemez.
        card = base_card()
        del card["difference"]
        sc = base_scenario()
        del sc["difference"]
        sc["card"] = card
        errs = validate(sc, SCHEMA)
        self.assertTrue(any(e.startswith("card.difference: neither the card nor the record") for e in errs), errs)

    def test_card_falls_back_to_the_record_difference(self):
        card = base_card()
        del card["difference"]
        self.assertNotIn("difference", SCHEMA["properties"]["card"]["required"])
        # Generated records: an adapted one keeps the archive's Fark whatever the card draws.
        self.assertEqual(validate(generated(difference="add", card=card), SCHEMA), [])
        # The record's difference sets the ring placement: 'remove' wants the ring in A.
        errs = validate(generated(difference="remove", card=card), SCHEMA)
        self.assertTrue(any("difference 'remove'" in e for e in errs), errs)
        # card.difference never overrides it (contract 5): a different one is refused.
        errs = validate(generated(difference="remove", card=base_card()), SCHEMA)
        self.assertTrue(any("differs from the record's difference 'remove'" in e for e in errs), errs)

    def test_turkish_difference_is_accepted(self):
        self.assertEqual(errors_for_card(base_card(difference="ekle")), [])

    def test_ring_placement_is_checked(self):
        errs = errors_for_card(base_card(variant_a=base_card()["variant_b"]))
        self.assertTrue(any("card: difference 'add'" in e for e in errs), errs)

    def test_remove_rings_a_and_leaves_b_empty(self):
        # The ring in A carries the label; no note under B is needed (or accepted).
        card = base_card(difference="remove", variant_a=base_card()["variant_b"],
                         variant_b='<div class="r-h">Sepet</div>')
        self.assertEqual(errors_for_card(card), [])
        card["variant_b"] = card["variant_a"]
        self.assertTrue(any("difference 'remove'" in e for e in errors_for_card(card)))

    def test_both_device_is_gone(self):
        self.assertTrue(errors_for(device="both"))
        self.assertEqual(errors_for(device="phone-web"), [])

    def test_brand_colour_pattern(self):
        self.assertTrue(errors_for(card=base_card(brand={"primary": "red}</style>"})))


class TestMessages(unittest.TestCase):
    def test_turkish_is_the_default(self):
        sc = base_scenario()
        sc["detail"] = detail(kpis=[{"name": "CR", "role": "secondary"}, {"name": "A", "role": "secondary"},
                                    {"name": "B", "role": "secondary"}])
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
            self.skipTest("examples/scenario.json not found")
        with open(EXAMPLE, encoding="utf-8") as fh:
            self.assertEqual(validate(json.load(fh), SCHEMA), [])

    def test_shipped_example_carries_a_renderable_card(self):
        # Tek JSON: aynı dosya hem doğrulanır hem kartı üretir.
        with open(EXAMPLE, encoding="utf-8") as fh:
            sc = json.load(fh)
        self.assertIn("card", sc)
        for key in ("variant_a", "variant_b", "difference"):
            self.assertIn(key, sc["card"])

    def test_shipped_example_is_the_compact_record(self):
        # Varsayılan öneri: detay yok; yalnızca yeni bağlantının gerektirdiği erişilebilirlik uyarısı var.
        # Kupon örneği arşivden uyarlandı: başlık bu sayfanın sorusu, adapted_from arşivdeki başlık.
        with open(EXAMPLE, encoding="utf-8") as fh:
            sc = json.load(fh)
        self.assertNotIn("detail", sc)
        self.assertEqual([w["type"] for w in sc["warnings"]], ["accessibility"])
        self.assertEqual(sc["source"], "adapted")
        self.assertEqual(sc["adapted_from"], ARCHIVE_TITLE)
        self.assertNotEqual(sc["adapted_from"], sc["title"])
        self.assertEqual(len(sc["invariants"]), 3)
        # Birincil gelir; kuponu gizlemek kod sahibine tam fiyat ödetip geliri artırabileceği için guardrail kupon kullanımını izler.
        self.assertEqual(sc["primary_kpi"]["name"], "Ziyaretçi Başına Gelir (RPV)")
        self.assertIn("atanan", sc["primary_kpi"]["denominator"])
        # Guardrail faydanın kendisini atanan paydayla izler; sipariş paydalı oran B'de mekanik düşerdi.
        self.assertEqual(sc["guardrail"]["name"], "Kuponlu Sipariş Veren Ziyaretçi Oranı")
        self.assertEqual(sc["guardrail"]["denominator"], "Teste atanan ziyaretçi")
        # Geçmiş dosyası yokken "daha önce test edilmedi" iddiası yazılmaz.
        self.assertNotIn("history", sc)


if __name__ == "__main__":
    unittest.main()
