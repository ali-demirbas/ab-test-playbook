#!/usr/bin/env python3
"""validate_scenario_json.py, 3.0.0 final pass (contract 5): claims, KPI meaning, assumptions. Stdlib only.

1. Result and impact claims: a number tied to an outcome or chance word, in every free-text field of the
   record, is an error unless the evidence carries it (the user's own data with its source; a forecast or a
   chance also says who reported it; a sector figure is quoted with its source); "similar tests" phrasing needs
   the user's own data; the archive is never proof. Page figures (discounts, thresholds) and observed baseline
   rates are not claims. --strict adds a "reviewer must judge" warning for borderline wording.
2. KPI meaning: a conditional-population name against an assigned denominator (and the reverse), a canonical
   glossary name over a denominator of another family, normalized revenue under the realized RPV name.
3. The glossary rows the record checks rely on.
4. `assumptions`: shape, a critical item carries its question, priority high never rests on one.
5. Fix round 2 (the negative-input test's misses): a step-transition primary against that step's abandonment
   is a complement; "shown / viewed / exposed" populations are "saw it" populations; the accessibility warning
   states the figures (a target of 44×44 pt / 48×48 dp, contrast of 4.5:1; a lower figure is named); numeric_change
   says where its figure comes from; the billing-period guardrail row of the glossary.
"""
import contextlib
import copy
import glob
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import validate_scenario_json as vsj  # noqa: E402
import validate_scenarios  # noqa: E402
from test_validate_scenario_json_v3 import coupon, plain  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(HERE, ".."))
SCHEMA = vsj.load_schema()
SHIPPED = [os.path.join(REPO_ROOT, "examples", "scenario.json")] + sorted(
    glob.glob(os.path.join(REPO_ROOT, "examples", "samples", "*.json")))
CLAIM = "claims a result"
BORDERLINE = "reviewer must judge"
NAMED_NOTE = "Kullanıcının paylaştığı GA4 huni raporu (Eylül 2026, mobil web)."


def errs(sc, lang="en"):
    return vsj.validate(sc, SCHEMA, lang)


def warns(sc, lang="en"):
    return vsj.lint(sc, SCHEMA, lang)


def has(items, fragment):
    return any(fragment in x for x in items)


def claims(sc, lang="en"):
    return [e for e in errs(sc, lang) if CLAIM in e or "bir sonuç iddiası" in e]


def put(sc, field, text):
    """Write `text` into one free-text field of the record."""
    if field == "variants[1].description":
        sc["variants"][1]["description"] = text
    elif field == "priority.rationale":
        sc["priority"]["rationale"] = text
    elif field == "evidence.note":
        sc["evidence"]["note"] = text
    elif field == "warnings[1].text":
        sc["warnings"].append({"type": "market", "text": text})
    elif field == "invariants[3]":
        sc["invariants"].append(text)
    elif field == "assumptions[0].text":
        sc["assumptions"] = [{"type": "visual", "text": text}]
    else:
        sc[field] = text
    return sc


REFUSED_TR = ("Dönüşüm %12 artar.", "Kazanma olasılığı %70.", "Beklenen artış yüzde 12.",
              "Bu değişiklik geliri %20 yükseltir.", "Benzer testlerde dönüşüm %12 arttı.", "2 kat daha fazla sipariş.",
              "Sepet terki %8 düşer.", "B’nin kazanma ihtimali %60.", "Sipariş yüzde 12 daha fazla olur.")
REFUSED_EN = ("Conversion rises 12%.", "Similar tests lifted conversion by 12%.", "Expected uplift is 12 percent.",
              "This change raises revenue by 20%.", "Win probability is 70%.", "It doubles signups.",
              "A 12% increase in orders.", "Orders grow 3x.", "B has a 70% chance to beat A.")
FIELDS = ("title", "problem", "mechanism", "variable", "variants[1].description", "priority.rationale",
          "evidence.note", "source_note", "warnings[1].text", "invariants[3]", "numeric_change",
          "assumptions[0].text")


class TestClaimsRefused(unittest.TestCase):
    def test_turkish_claims_in_the_problem(self):
        for text in REFUSED_TR:
            sc = put(coupon(), "problem", text)
            self.assertTrue(claims(sc), (text, errs(sc)))
            self.assertTrue(claims(sc, "tr"), text)

    def test_english_claims_in_the_problem(self):
        for text in REFUSED_EN:
            sc = put(coupon(), "problem", text)
            sc["lang"] = "en"
            self.assertTrue(claims(sc), (text, errs(sc)))

    def test_every_free_text_field_is_read(self):
        for field in FIELDS:
            for text in ("Dönüşüm %12 artar.", "Win probability is 70%.", "Benzer testlerde dönüşüm arttı."):
                sc = put(coupon(), field, text)
                self.assertTrue(any(e.startswith(field + ":") and CLAIM in e for e in errs(sc)),
                                (field, text, errs(sc)))

    def test_claims_are_errors_in_normal_mode_not_warnings(self):
        sc = put(coupon(), "warnings[1].text", "Beklenen artış yüzde 12.")
        self.assertTrue(claims(sc))
        self.assertFalse(has(warns(sc), CLAIM))

    def test_similar_tests_phrasing_is_refused_without_a_number(self):
        for text in ("Benzer testlerde dönüşüm arttı.", "Başka şirketlerde bu değişiklik siparişi artırdı.",
                     "Similar tests saw more orders.", "Other companies saw a lift from this change."):
            sc = put(coupon(), "mechanism", text)
            self.assertTrue(claims(sc), (text, errs(sc)))

    def test_archive_presence_is_never_proof(self):
        for text in ("Bu fikir arşivde kazanmış bir test.", "It is an archive winner.",
                     "Arşivde işe yaradığı için öncelikli."):
            for evidence in ({"level": "archive", "note": "Arşiv örüntüsü."},
                             {"level": "user_data", "note": NAMED_NOTE}):
                sc = put(coupon(), "priority.rationale", text)
                sc["evidence"] = dict(evidence)
                if evidence["level"] == "user_data":
                    sc["source"], sc["source_note"] = "generated", "Arşivde bu sayfaya uyan bir blok yok."
                    del sc["adapted_from"]
                self.assertTrue(has(errs(sc), "priority.rationale:"), (text, evidence, errs(sc)))

    def test_intuition_and_sector_without_a_quoted_source(self):
        for evidence in ({"level": "intuition"}, {"level": "sector", "note": "Mobil e-ticarette yaygın bir kalıp."}):
            sc = put(plain(evidence=evidence), "mechanism", "Kısa başlık dönüşümü %12 artırır.")
            self.assertTrue(claims(sc), (evidence, errs(sc)))

    def test_a_forecast_or_chance_needs_its_reporter_even_with_user_data(self):
        for text in ("Kazanma olasılığı %70.", "Beklenen artış yüzde 12.", "Win probability is 70%."):
            sc = plain(evidence={"level": "user_data", "note": NAMED_NOTE}, problem=text)
            self.assertTrue(claims(sc), (text, errs(sc)))

    def test_turkish_message(self):
        sc = put(coupon(), "problem", "Dönüşüm %12 artar.")
        self.assertTrue(has(errs(sc, "tr"), "problem: '%12 artar' bir sonuç iddiası"), errs(sc, "tr"))


class TestClaimsAllowed(unittest.TestCase):
    def test_page_discounts_and_thresholds(self):
        for text in ("Yıllık (%20 indirim) seçeneği kartta görünüyor.", "%10 indirim kodu sepette duruyor.",
                     "500 TL üzeri ücretsiz kargo bilgisi özetin altında.", "1.500 TL eşik sepette yazmıyor.",
                     "%20’lik yıllık indirim yalnızca anahtarın etiketinde duruyor.", "“%20 indirim kazan” bandı.",
                     "Annual plan (20% off) is shown on the card.", "Fiyatı %10 artırılan plan kartı.",
                     "Metin %200 büyütüldüğünde kesilmez.", "Kontrast en az 4.5:1, dokunma alanı 44×44 pt.",
                     "Katkı payını %10 artıran müşteri aynı onay adımından geçer.",
                     "Kullanıcıların %20’den fazlası mobilden geliyor."):
            for field in ("problem", "variants[1].description", "invariants[3]", "numeric_change"):
                sc = put(coupon(), field, text)
                self.assertEqual(claims(sc), [], (field, text))

    def test_an_observed_baseline_rate_is_a_fact(self):
        for evidence in ({"level": "user_data", "note": NAMED_NOTE}, {"level": "archive", "note": "Arşiv örüntüsü."}):
            sc = coupon()
            sc["evidence"] = dict(evidence)
            if evidence["level"] == "user_data":
                sc["source"], sc["source_note"] = "generated", "Arşivde bu sayfaya uyan bir blok yok."
                del sc["adapted_from"]
            for text in ("Formu açanların %58'i bu adımda çıkıyor.", "İndirenlerin yalnızca %31’i hesap oluşturuyor.",
                         "58% of visitors who open the form drop off at this step.",
                         "Mobil %38 ile masaüstü %52 arasındaki fark kaybın yerini gösteriyor."):
                sc["problem"] = text
                self.assertEqual(claims(sc), [], (evidence, text))
                self.assertFalse(has(warns(sc), BORDERLINE), (evidence, text, warns(sc)))

    def test_a_hypothesis_without_a_number(self):
        for text in ("B’nin siparişi artıracağı bir hipotez.", "Kısa form kaydı artırabilir.",
                     "B may increase orders; that is the hypothesis."):
            sc = put(coupon(), "mechanism", text)
            self.assertEqual(claims(sc), [], text)
            self.assertFalse(has(warns(sc), BORDERLINE), text)

    def test_the_users_own_figure_with_its_source(self):
        sc = plain(evidence={"level": "user_data", "note": NAMED_NOTE},
                   problem="Geçen çeyrekte mobil dönüşüm %12 arttı ama form adımında kayıp sürüyor.")
        self.assertEqual(claims(sc), [])
        sc = plain(evidence={"level": "user_data", "note": NAMED_NOTE},
                   mechanism="Benzer testlerde dönüşüm %12 arttı.")
        self.assertEqual(claims(sc), [])

    def test_a_reported_chance_or_forecast_with_user_data(self):
        for text in ("Test aracının raporuna göre kazanma olasılığı %70.", "GA4’e göre beklenen artış yüzde 12.",
                     "According to the team’s Optimizely report, win probability is 70%."):
            sc = plain(evidence={"level": "user_data", "note": NAMED_NOTE}, problem=text)
            self.assertEqual(claims(sc), [], (text, errs(sc)))

    def test_a_sector_result_quoted_with_its_source(self):
        note = "2025 ödeme adımı kullanılabilirlik araştırması (checkout usability research)."
        tr_source, en_source = "Ödeme kullanılabilirliği araştırmasına göre ", "Checkout usability research reports that "
        for text in (tr_source + "zorunlu hesap açma ödeme terkini %24 artırır.",
                     en_source + "forced account creation raises checkout abandonment by 24%."):
            sc = plain(evidence={"level": "sector", "note": note}, problem=text)
            self.assertEqual(claims(sc), [], (text, errs(sc)))
            sc["evidence"] = {"level": "sector", "note": "Yaygın bir kalıp."}
            sc["problem"] = text.replace(tr_source, "").replace(en_source, "")
            sc["problem"] = sc["problem"][:1].upper() + sc["problem"][1:]
            self.assertTrue(claims(sc), text)

    def test_the_detail_view_and_the_card_are_not_read(self):
        sc = coupon()
        sc["detail"] = {"test_items": ["Dönüşüm %12 artar mı?", "Mobilde fark var mı?", "Kampanyada fark var mı?"],
                        "kpis": [{"name": "Dönüşüm Oranı (CR)", "role": "primary"},
                                 {"name": "Kuponlu Sipariş Oranı", "role": "guardrail", "question": "Düşmemeli."},
                                 {"name": "Sepet Terk Oranı", "role": "secondary"}],
                        "dont_items": ["Kodu kaldırmayın.", "Mesajı değiştirmeyin.", "Metni değiştirmeyin."]}
        self.assertEqual(claims(sc), [])

    def test_shipped_records_have_no_claim(self):
        for path in SHIPPED:
            with open(path, encoding="utf-8") as fh:
                sc = json.load(fh)
            sc.pop("review", None)
            self.assertEqual(errs(sc), [], path)
            self.assertEqual(warns(sc), [], path)


class TestBorderlineInStrictMode(unittest.TestCase):
    def test_unlinked_number_and_outcome_word(self):
        sc = put(coupon(), "problem", "Formu açanların %58'i bu adımda çıkıyor ve B bu kaybı belki azaltabilir.")
        self.assertEqual(claims(sc), [])
        self.assertTrue(has(warns(sc), "problem:") and has(warns(sc), BORDERLINE), warns(sc))

    def test_vague_magnitudes(self):
        for text in ("B çok daha fazla sipariş getirir.", "Bu değişiklik ciddi artış sağlar.",
                     "B brings much more revenue.", "A dramatic lift in signups."):
            sc = put(coupon(), "mechanism", text)
            self.assertEqual(claims(sc), [], text)
            self.assertTrue(has(warns(sc), BORDERLINE), (text, warns(sc)))
        self.assertTrue(has(warns(sc, "tr"), BORDERLINE), warns(sc, "tr"))

    def test_strict_cli_turns_it_into_an_error(self):
        sc = put(coupon(), "mechanism", "Bu değişiklik ciddi artış sağlar.")
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(sc, fh, ensure_ascii=False)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(vsj.main([path]), 0)
                self.assertEqual(vsj.main(["--strict", path]), 1)


# ------------------------------------------------------------- 2. KPI meaning

def guardrail(name, denominator, direction="must_not_decrease"):
    return {"name": name, "kind": "metric", "denominator": denominator, "direction": direction}


INSURANCE = guardrail("Teklif → Sözleşme Dönüşüm Oranı (30 gün, atanan ziyaretçi başına)",
                      "Kasko teklif formunu açıp teste atanan ziyaretçi")
MISMATCH = "name and denominator measure different things"
GLOSSARY_MEANING = "glossary"


class TestKpiNameAgainstDenominator(unittest.TestCase):
    def test_the_insurance_guardrail_is_refused(self):
        e = errs(plain(guardrail=dict(INSURANCE)))
        self.assertTrue(has(e, "guardrail:") and has(e, "Teklif alan"), e)

    def test_conditional_name_with_an_assigned_denominator(self):
        for name, den in (("Sipariş Başına İade Talebi Oranı", "Teste atanan ziyaretçi"),
                          ("Sepet → Sipariş Geçiş Oranı", "Teste atanan ziyaretçi"),
                          ("Kayıt yapanlar arasında aktivasyon", "Teste atanan kullanıcı"),
                          ("Refund rate per order", "Assigned visitors"),
                          ("Activation among new signups", "Visitors assigned to the test")):
            e = errs(plain(guardrail=guardrail(name, den, "must_not_increase")))
            self.assertTrue(has(e, MISMATCH), (name, e))
        self.assertTrue(has(errs(plain(guardrail=guardrail("Sipariş Başına İade Talebi Oranı",
                                                                  "Teste atanan ziyaretçi")), "tr"),
                            "ad ve payda farklı şeyleri ölçüyor"))

    def test_assigned_name_with_a_conditional_denominator(self):
        for name, den in (("İade Talebi Oranı (atanan ziyaretçi başına)", "Tamamlanan sipariş"),
                          ("Refund requests (per assigned visitor)", "Completed orders"),
                          ("Nitelik Oranı (atanan ziyaretçi başına)", "Gelen talep")):
            e = errs(plain(guardrail=guardrail(name, den, "must_not_increase")))
            self.assertTrue(has(e, MISMATCH), (name, e))

    def test_consistent_pairs_pass(self):
        for name, den in (("Sipariş Başına İade Talebi Oranı", "Tamamlanan sipariş"),
                          ("İade Talebi Oranı (atanan ziyaretçi başına)", "Teste atanan ziyaretçi"),
                          ("Liste → Ürün Tıklama Oranı", "Liste sayfasına atanan ziyaretçi"),
                          ("Sözleşme Oranı (30 gün)", "Kasko teklif formunu açıp teste atanan ziyaretçi"),
                          ("Teklif → Sözleşme Dönüşüm Oranı", "Teklif alan ziyaretçi")):
            e = errs(plain(guardrail=guardrail(name, den)))
            self.assertFalse(has(e, MISMATCH) or has(e, GLOSSARY_MEANING), (name, e))


class TestGlossaryMeaning(unittest.TestCase):
    def test_canonical_name_over_another_family(self):
        cases = (("Sepete Ekleme Oranı", "Tamamlanan sipariş"),               # assigned → order
                 ("Kupon Kullanım Oranı", "Teste atanan ziyaretçi"),          # order → assigned
                 ("Sipariş Tamamlama Oranı", "Teste atanan ziyaretçi"),       # reached checkout → assigned
                 ("Poliçeleşme Oranı", "Teste atanan ziyaretçi"),             # a synonym of the per-quote rate
                 ("Kayıt Oranı (7 gün)", "Tamamlanan sipariş"),               # the window is stripped
                 ("Talep Başına Nitelik Oranı", "Teste atanan ziyaretçi"))    # request → assigned
        for name, den in cases:
            e = errs(plain(guardrail=guardrail(name, den)))
            self.assertTrue(has(e, "guardrail:") and has(e, GLOSSARY_MEANING), (name, den, e))
        self.assertTrue(has(errs(plain(guardrail=guardrail("Sepete Ekleme Oranı", "Tamamlanan sipariş")), "tr"),
                            "sözlük"))

    def test_a_trigger_metric_over_all_assigned_visitors_gets_a_hint(self):
        sc = plain(guardrail=guardrail("Sipariş Tamamlama Oranı", "Teste atanan ziyaretçi"))
        self.assertTrue(has(errs(sc), "If assignment happens at that trigger"), errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "Atama o tetikte yapılıyorsa"), errs(sc, "tr"))

    def test_the_primary_is_read_too(self):
        sc = plain(primary_kpi={"name": "Sepete Ekleme Oranı", "denominator": "Tamamlanan sipariş",
                                "direction": "increase"})
        self.assertTrue(has(errs(sc), "primary_kpi:"), errs(sc))

    def test_same_family_passes(self):
        cases = (("Sepete Ekleme Oranı", "Ürün sayfasına ulaşan ziyaretçi"),  # a trigger narrows an assignment
                 ("Kupon Kullanım Oranı", "Tamamlanan sipariş"),
                 ("Sipariş Tamamlama Oranı", "Sepet sayfasına ulaşan ziyaretçi (iki kolda aynı tetik)"),
                 ("Kayıt Oranı (7 gün)", "“Hesap oluştur” ekranına ulaşan, teste atanmış kullanıcılar"),
                 ("İade Oranı (30 gün)", "Tamamlanan sipariş"),
                 ("Kuponlu Sipariş Oranı", "Teste atanan mobil ziyaretçi (atama sepet sayfasına ulaşınca)"),
                 ("Artırımı Geri Alma Oranı (90 gün)", "Katkı payını artıran müşteri"))  # not in the glossary
        for name, den in cases:
            e = errs(plain(guardrail=guardrail(name, den)))
            self.assertFalse(has(e, GLOSSARY_MEANING) or has(e, MISMATCH), (name, den, e))

    def test_normalized_revenue_is_not_rpv(self):
        sc = plain(primary_kpi={"name": "Ziyaretçi Başına Gelir (RPV)",
                                "denominator": "Fiyatlar sayfasına atanan ziyaretçi; yıllık tahsilat aylığa çevrilerek "
                                               "sayılır", "direction": "increase"})
        e = errs(sc)
        self.assertTrue(has(e, "primary_kpi:") and has(e, "Yeni Abonelik Değeri"), e)
        sc["primary_kpi"] = {"name": "Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)",
                             "denominator": "Fiyatlar sayfasına atanan ziyaretçi", "direction": "increase"}
        self.assertFalse(has(errs(sc), "Yeni Abonelik Değeri"), errs(sc))

    def test_shipped_records_keep_their_meaning(self):
        for path in SHIPPED:
            with open(path, encoding="utf-8") as fh:
                sc = json.load(fh)
            e = [x for x in errs(sc) if MISMATCH in x or GLOSSARY_MEANING in x]
            self.assertEqual(e, [], path)


class TestGlossaryRows(unittest.TestCase):
    def setUp(self):
        self.glossary = validate_scenarios.load_glossary()
        self.rows = vsj.glossary_rows()

    def test_new_rows_are_canonical(self):
        for name in ("Sözleşme Oranı (30 gün)", "Teklif → Sözleşme Dönüşüm Oranı",
                     "Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)",
                     "Tahsilat (gözlem penceresi, atanan ziyaretçi başına)"):
            self.assertIn(name, self.glossary)

    def test_denominator_families(self):
        fam = {name: vsj.families(row["payda"]) for name, row in self.rows.items()}
        self.assertEqual(fam["Sözleşme Oranı (30 gün)"], {"assigned"})
        self.assertEqual(fam["Teklif → Sözleşme Dönüşüm Oranı"], {"quote"})
        self.assertEqual(fam["Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)"], {"assigned"})
        self.assertEqual(fam["Tahsilat (gözlem penceresi, atanan ziyaretçi başına)"], {"assigned"})
        self.assertEqual(fam["Kuponlu Sipariş Veren Ziyaretçi Oranı"], {"assigned"})
        self.assertEqual(vsj.glossary_canonical("Kuponlu Sipariş Oranı"), "Kuponlu Sipariş Veren Ziyaretçi Oranı")
        self.assertEqual(fam["Kupon Kullanım Oranı"], {"order"})

    def test_coupon_row_says_when_code_holders_can_be_watched(self):
        row = self.rows["Kuponlu Sipariş Veren Ziyaretçi Oranı"]["definition"]
        self.assertIn("atamadan önce", row)


# ------------------------------------------------------------- 3. card difference (builder's request)

ADD_CARD = {"variant_a": '<div class="r-h">Sepet</div>',
            "variant_b": '<div class="r-h">Sepet</div><div class="hl" data-note="Yeni"><div class="r-h">Not</div></div>'}


class TestCardDifference(unittest.TestCase):
    def test_a_card_difference_that_differs_from_the_record_is_refused(self):
        sc = plain(difference="add", card=dict(ADD_CARD, difference="change"))
        e = errs(sc)
        self.assertTrue(has(e, "card: card.difference 'change' differs from the record's difference 'add'"), e)
        self.assertTrue(has(errs(sc, "tr"), "card:"), errs(sc, "tr"))

    def test_a_card_difference_may_repeat_the_record_in_any_spelling(self):
        for spelling in ("add", "ekle"):
            self.assertEqual(errs(plain(difference="add", card=dict(ADD_CARD, difference=spelling))), [], spelling)
        self.assertEqual(errs(plain(difference="add", card=dict(ADD_CARD))), [])

    def test_ring_placement_follows_the_record(self):
        self.assertEqual(vsj.card_difference({"difference": "move"}, {"difference": "change"}), "move")
        self.assertEqual(vsj.card_difference({}, {"difference": "kaldır"}), "remove")

    def test_schema_says_it_never_overrides(self):
        text = SCHEMA["properties"]["card"]["properties"]["difference"]["description"]
        self.assertIn("never overrides", text)
        self.assertNotIn("override", SCHEMA["properties"]["difference"]["description"].replace("never overrides", ""))


# ------------------------------------------------------------- 4. assumptions

CRITICAL = {"type": "critical", "text": "Sayfanın yıllık görünümünde fiyatların aylık karşılığı gösteriliyor.",
            "question": "Yıllık fiyat kartta nasıl görünüyor?"}
VISUAL = {"type": "visual", "text": "Ürün adları ve görseller temsilî."}


class TestAssumptions(unittest.TestCase):
    def test_valid_assumptions_pass(self):
        for items in ([CRITICAL], [VISUAL], [CRITICAL, VISUAL, dict(VISUAL, text="Logo temsilî.")]):
            sc = plain(assumptions=copy.deepcopy(items))
            self.assertEqual(errs(sc), [], items)
            self.assertEqual(warns(sc), [], items)

    def test_shape(self):
        bad = ([CRITICAL] * 4, [dict(VISUAL, type="minor")], [dict(VISUAL, extra="x")], [{"type": "visual"}],
               [dict(VISUAL, text="")], [dict(CRITICAL, question="")], [])
        for items in bad:
            self.assertTrue(errs(plain(assumptions=copy.deepcopy(items))), items)

    def test_text_is_one_short_sentence(self):
        sc = plain(assumptions=[dict(VISUAL, text="x" * 201)])
        self.assertTrue(has(errs(sc), "assumptions[0].text:"), errs(sc))
        sc = plain(assumptions=[dict(VISUAL, text="x" * 200)])
        self.assertEqual(errs(sc), [])

    def test_a_critical_assumption_carries_its_question(self):
        item = dict(CRITICAL)
        del item["question"]
        e = errs(plain(assumptions=[item]))
        self.assertTrue(has(e, "assumptions[0].question:"), e)
        self.assertTrue(has(errs(plain(assumptions=[item]), "tr"), "assumptions[0].question:"))
        self.assertEqual(errs(plain(assumptions=[dict(VISUAL)])), [])

    def test_high_priority_never_rests_on_a_critical_assumption(self):
        sc = coupon()
        sc["priority"]["tier"] = "high"
        sc["assumptions"] = [dict(CRITICAL)]
        e = errs(sc)
        self.assertTrue(has(e, "priority.tier:") and has(e, "medium at most"), e)
        self.assertTrue(has(errs(sc, "tr"), "priority.tier:"))
        sc["assumptions"] = [dict(VISUAL)]
        self.assertEqual(errs(sc), [])
        sc["priority"]["tier"] = "medium"
        sc["assumptions"] = [dict(CRITICAL)]
        self.assertEqual(errs(sc), [])

    def test_assumptions_are_part_of_the_fingerprint(self):
        sc = plain()
        before = vsj.record_fingerprint(sc)
        sc["assumptions"] = [dict(VISUAL)]
        self.assertNotEqual(vsj.record_fingerprint(sc), before)

    def test_a_claim_inside_an_assumption_is_read(self):
        sc = plain(assumptions=[dict(CRITICAL, text="B dönüşümü %12 artırır.")])
        self.assertTrue(has(errs(sc), "assumptions[0].text:"), errs(sc))


# ------------------------------------------------------------- 5. fix round 2 (negative-input test)
#
# Each class reproduces one MISS of the negative test (v5/N-negative/results.md) with the case's own wording.

COMPLEMENT = "looks like the complement of the primary"
SAW = "is a \"users who saw it\" population"
CART_TRIGGER = "Teste atanan ziyaretçi (atama sepet sayfasına ulaşınca, iki kolda aynı tetik)"


class TestComplementTransition(unittest.TestCase):
    """Item 1 (case e1): a step-transition primary and the abandonment of that step over one population."""

    def kpis(self, primary, guardrail_name, p_den=CART_TRIGGER, g_den=CART_TRIGGER):
        sc = coupon()
        sc["primary_kpi"] = {"name": primary, "denominator": p_den, "direction": "increase"}
        sc["guardrail"] = {"name": guardrail_name, "kind": "metric", "denominator": g_den,
                           "direction": "must_not_increase"}
        return sc

    def test_case_e1_transition_against_cart_abandonment(self):
        e = errs(self.kpis("Sepetten Ödemeye Geçiş Oranı", "Sepet Terk Oranı"))
        self.assertTrue(has(e, "guardrail: guardrail 'Sepet Terk Oranı' " + COMPLEMENT), e)

    def test_transition_and_proceed_wording(self):
        for primary, guard in (("Ödeme Adımına Geçiş Oranı", "Sepet Terk Oranı"),
                               ("Ödeme Adımına Ulaşma Oranı", "Sepet Terk Oranı"),
                               ("Adımlar Arası İlerleme Oranı", "Adım Terk Oranı"),
                               ("Checkout Proceed Rate", "Cart Abandonment Rate"),
                               ("Funnel Progression Rate", "Funnel Abandonment Rate")):
            e = errs(self.kpis(primary, guard))
            self.assertTrue(has(e, COMPLEMENT), (primary, guard, e))

    def test_no_stated_guardrail_denominator_is_the_same_population(self):
        sc = self.kpis("Sepetten Ödemeye Geçiş Oranı", "Sepet Terk Oranı")
        sc["detail"] = {"kpis": [
            {"role": "primary", "name": "Sepetten Ödemeye Geçiş Oranı", "denominator": CART_TRIGGER,
             "question": "B ödemeye geçişi artırıyor mu?"},
            {"role": "guardrail", "name": "Sepet Terk Oranı", "question": "Sepet terki artıyor mu?"}]}
        self.assertTrue(has(errs(sc), "detail.kpis[1]: guardrail 'Sepet Terk Oranı' " + COMPLEMENT), errs(sc))

    def test_a_later_step_is_an_independent_harm(self):
        sc = self.kpis("Sepetten Ödemeye Geçiş Oranı", "Ödeme Adımı Terk Oranı",
                       g_den="Ödeme adımına ulaşan ziyaretçi (iki kolda aynı tetik)")
        self.assertFalse(has(errs(sc), COMPLEMENT), errs(sc))

    def test_turkish_message(self):
        e = errs(self.kpis("Sepetten Ödemeye Geçiş Oranı", "Sepet Terk Oranı"), "tr")
        self.assertTrue(has(e, "tümleyeni"), e)


class TestShownDenominator(unittest.TestCase):
    """Item 2 (case d4): "shown to", "viewed", "exposed" populations are "saw it" populations."""

    def with_den(self, den, field="primary_kpi"):
        sc = coupon()
        sc[field] = dict(sc[field], denominator=den)
        return sc

    def test_case_d4_shown_the_link(self):
        den = "“İndirim kodum var” bağlantısı gösterilen kullanıcı"
        e = errs(self.with_den(den))
        self.assertTrue(has(e, "primary_kpi.denominator: %r %s" % (den, SAW)), e)

    def test_every_shown_viewed_exposed_wording(self):
        for den in ("Yeni bant gösterilen ziyaretçi", "Bannerı görüntüleyen kullanıcı", "Yeni bloğa maruz kalan kullanıcı",
                    "Rozet gösterilen her ziyaretçi", "Users shown the link", "Visitors exposed to the banner",
                    "Exposed users", "Users who were shown the offer", "Visitors viewing the new block"):
            for field in ("primary_kpi", "guardrail"):
                e = errs(self.with_den(den, field))
                self.assertTrue(has(e, field + ".denominator:") and has(e, SAW), (den, field, e))

    def test_in_the_name_too(self):
        sc = coupon()
        sc["primary_kpi"]["name"] = "Bağlantı Gösterilen Kullanıcı Başına Sipariş"
        self.assertTrue(has(errs(sc), "primary_kpi.name:") and has(errs(sc), SAW), errs(sc))

    def test_populations_both_arms_have_still_pass(self):
        for den in ("Sepet sayfasına ulaşan ziyaretçi (iki kolda aynı tetik)", "Sayfa görüntüleme",
                    "Teste atanan ziyaretçi (öğe iki kolda da varsa öğe gösterimi)",
                    "Teste atanan ziyaretçi; pay: teklifi kendisine gösterilen ziyaretçiler"):
            e = errs(self.with_den(den))
            self.assertFalse(has(e, SAW), (den, e))


A11Y_THRESHOLD = "below the threshold"
I2_WARNING = ("Geçmeli: pencere açılınca odak kod alanına geçer, Kapat düğmesi ve Esc ile kapanır, klavyeyle kullanılır, "
              "ekran okuyucu “İndirim kodun var mı?” adıyla okur, dokunma alanı yeterli ve kontrast en az 3:1.")


class TestAccessibilityThresholds(unittest.TestCase):
    """Item 3 (case i2): contrast states at least 4.5:1, the touch target 44×44 pt / 48×48 dp; a bare word or a
    lower figure no longer counts."""

    def link(self, text):
        sc = coupon()
        sc["warnings"] = [{"type": "accessibility", "text": text}]
        return sc

    def modal(self, text):
        sc = self.link(text)
        sc["variable"] = "Sepetteki kupon penceresi"
        sc["variants"][1]["description"] = "Sepette kupon kodu bir açılır pencereyle sorulur"
        return sc

    def test_case_i2_wording(self):
        e = errs(self.modal(I2_WARNING))
        self.assertTrue(has(e, "text contrast '3:1'") and has(e, A11Y_THRESHOLD), e)
        self.assertTrue(has(e, "does not state: touch target (at least 44×44 pt / 48×48 dp)"), e)
        tr = errs(self.modal(I2_WARNING), "tr")
        self.assertTrue(has(tr, "'3:1'") and has(tr, "eşiğin altında"), tr)

    def test_a_lower_ratio_is_named(self):
        for ratio in ("3:1", "4:1", "4,4:1", "3 : 1"):
            text = "Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt, " \
                   "kontrast en az %s olur." % ratio
            e = errs(self.link(text))
            self.assertTrue(has(e, "text contrast %r" % ratio) and has(e, A11Y_THRESHOLD), (ratio, e))
            self.assertFalse(has(e, "does not state"), (ratio, e))

    def test_a_lower_ratio_next_to_the_right_one_is_still_named(self):
        text = A11Y_THRESHOLDS_OK + " Kontrast 3:1 olur."
        self.assertTrue(has(errs(self.link(text)), "'3:1'"), errs(self.link(text)))

    def test_a_qualified_non_text_ratio_next_to_the_text_one_passes(self):
        for extra in ("büyük metin ve simgelerde 3:1", "odak göstergesi için 3:1", "icons and borders at least 3:1"):
            text = A11Y_THRESHOLDS_OK[:-1] + ", " + extra + "."
            self.assertEqual(errs(self.link(text)), [], extra)

    def test_a_qualified_lower_ratio_alone_does_not_state_text_contrast(self):
        text = "Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt, " \
               "büyük metinde kontrast 3:1 olur."
        self.assertTrue(has(errs(self.link(text)), "does not state: text contrast (at least 4.5:1)"))

    def test_bare_words_no_longer_count(self):
        text = "Bağlantının dokunma alanı yeterli, kontrastı yüksek, klavye ve ekran okuyucu ile kullanılabilir olmalı."
        e = errs(self.link(text))
        self.assertTrue(has(e, "does not state: touch target (at least 44×44 pt / 48×48 dp), text contrast "
                               "(at least 4.5:1)"), e)
        e = errs(self.link("The link's tap target, contrast, keyboard use and screen reader name pass review."))
        self.assertTrue(has(e, "touch target") and has(e, "text contrast"), e)

    def test_a_target_needs_its_unit(self):
        text = "Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44, kontrast 4.5:1."
        self.assertTrue(has(errs(self.link(text)), "does not state: touch target"), errs(self.link(text)))

    def test_a_smaller_target_is_named(self):
        for size in ("32×32 px", "40 pt", "44×44 dp", "48×40 dp"):
            text = "Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı %s, kontrast 4.5:1." % size
            e = errs(self.link(text))
            self.assertTrue(has(e, "touch target %r" % size) and has(e, A11Y_THRESHOLD), (size, e))

    def test_font_icon_and_spacing_sizes_are_not_targets(self):
        text = "Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, yazı 16 px, simge 24 px, kontrast 4.5:1."
        e = errs(self.link(text))
        self.assertTrue(has(e, "does not state: touch target"), e)
        self.assertFalse(has(e, A11Y_THRESHOLD), e)
        ok = A11Y_THRESHOLDS_OK[:-1] + ", hedefler arasında en az 8 px boşluk, yazı 14 px."
        self.assertEqual(errs(self.link(ok)), [])

    def test_accepted_spellings(self):
        for target in ("en az 44×44 pt", "44x44pt", "44 × 44 pt", "48×48 dp", "en az 48 dp", "44 px", "en az 44×44 pt "
                       "(48×48 dp)", "60×60 pt"):
            for contrast in ("4.5:1", "4,5:1", "4.5 : 1", "en az 7:1", "oranı en az 4.5"):
                text = ("Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı %s, kontrastı %s."
                        % (target, contrast))
                self.assertEqual(errs(self.link(text)), [], text)

    def test_the_builder_reads_the_same_criteria(self):
        criteria = {c[1]: c[2] for c in vsj.A11Y_BASE}
        self.assertIsNone(criteria["text contrast (at least 4.5:1)"].search("kontrast en az 3:1"))
        self.assertIsNone(criteria["touch target (at least 44×44 pt / 48×48 dp)"].search("dokunma alanı yeterli"))
        self.assertTrue(criteria["text contrast (at least 4.5:1)"].search("kontrast en az 4.5:1"))
        self.assertTrue(criteria["touch target (at least 44×44 pt / 48×48 dp)"].search("en az 44×44 pt"))

    def test_shipped_records_state_both_thresholds(self):
        for path in SHIPPED:
            with open(path, encoding="utf-8") as fh:
                sc = json.load(fh)
            e = [x for x in errs(sc) if "warnings:" in x]
            self.assertEqual(e, [], path)


A11Y_THRESHOLDS_OK = ("Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt, "
                      "metin kontrastı en az 4.5:1 olur.")
UNSOURCED = "does not say where the figure comes from"
G3_NUMERIC = "B yıllık ödemenin aylık karşılığını gösterir; 960 TL/ay satırı varyantın kendisidir."


class TestNumericChangeProvenance(unittest.TestCase):
    """Item 4 (case g3): numeric_change silences the builder's numbers gate, so it says where the figure comes
    from (the page, the user, a derivation) or a critical assumption holds the figure open."""

    def test_case_g3_unsourced_figure(self):
        sc = plain(numeric_change=G3_NUMERIC)
        e = errs(sc)
        self.assertTrue(has(e, "numeric_change:") and has(e, UNSOURCED), e)
        self.assertTrue(has(errs(sc, "tr"), "numeric_change:"), errs(sc, "tr"))

    def test_a_source_or_a_derivation_passes(self):
        for text in ("B, sayfadaki yıllık fiyatı (960 TL/ay) varsayılan gösterir.",
                     "960 TL/ay sayfada yıllık sekmesinde yazıyor.",
                     "B, kullanıcının verdiği yıllık fiyatı gösterir.",
                     "Kullanıcının paylaştığı fiyat listesine göre yıllık plan 960 TL/ay.",
                     "B’deki 270 TL, eşikten ara toplamın çıkarılmasıyla hesaplandı.",
                     "Kalan tutar 1.500 − 1.230 = 270 TL.",
                     "Doluluk 1.230 / 1.500 oranından gelir.",
                     "Aylık karşılık 1.200 × 0,8 ile bulunur.",
                     "B shows the annual price from the page (960 TL a month).",
                     "The remaining amount is derived from the subtotal and the threshold.",
                     "The user gave the annual price.", "Computed as 1,500 - 1,230."):
            self.assertFalse(has(errs(plain(numeric_change=text)), UNSOURCED), text)

    def test_a_critical_assumption_about_the_figure_passes(self):
        sc = plain(numeric_change=G3_NUMERIC,
                   assumptions=[{"type": "critical", "text": "Yıllık planın aylık karşılığı 960 TL.",
                                 "question": "Yıllık plan kartta hangi fiyatla görünüyor?"}])
        self.assertFalse(has(errs(sc), UNSOURCED), errs(sc))
        sc["assumptions"] = [{"type": "critical", "text": "Yıllık seçiliyken kartlar aylık karşılığı gösteriyor.",
                              "question": "Yıllık seçiliyken kartta fiyat nasıl yazıyor?"}]
        self.assertFalse(has(errs(sc), UNSOURCED), errs(sc))

    def test_an_assumption_about_something_else_or_a_visual_one_does_not(self):
        for item in ({"type": "critical", "text": "Kimlik alanının yasal amacı doğrulanmadı.",
                      "question": "Kimlik alanı hangi adım için gerekli?"},
                     {"type": "visual", "text": "Yıllık planın aylık karşılığı 960 TL olarak temsilî çizildi."}):
            sc = plain(numeric_change=G3_NUMERIC, assumptions=[item])
            self.assertTrue(has(errs(sc), UNSOURCED), (item, errs(sc)))

    def test_compared_to_an_arm_is_not_a_source(self):
        # "göre" names a source ("GA4’e göre"), but "A’ya göre" / "B’ye göre" only compares the arms.
        for text in ("A’ya göre B’de 960 TL/ay yazar.", "B'ye göre A’da fiyat 960 TL/ay."):
            sc = plain(numeric_change=text)
            self.assertTrue(has(errs(sc), UNSOURCED), (text, errs(sc)))

    def test_shipped_and_run_records_that_state_a_derivation_pass(self):
        for text in ("B’deki 270 TL, sayfadaki 1.230 TL’lik ara toplamın 1.500 TL’lik ücretsiz kargo eşiğinden "
                     "çıkarılmasıyla hesaplanan kalan tutardır; çubuğun %82 doluluğu da aynı orandan (1.230 / 1.500) gelir.",
                     "B açılışta sayfanın Yıllık görünümünü gösterir; karttaki tutarlar verilen aylık fiyatlara %20 "
                     "uygulanarak hesaplandı (960 ve 1.920 TL/ay, yıllık 11.520 ve 23.040 TL); fiyatlar ve indirim "
                     "oranı değişmez."):
            self.assertFalse(has(errs(plain(numeric_change=text)), UNSOURCED), text)


class TestBillingPeriodGuardrailRow(unittest.TestCase):
    """Item 17: the default billing-period change's guardrail is a canonical glossary name, per assigned visitor."""
    NAME = "Dönem Kaynaklı İade veya Şikâyet Talebi Oranı (ilk ödemeden sonra 30 gün)"

    def test_row_is_canonical_and_per_assigned_visitor(self):
        self.assertTrue(self.NAME in validate_scenarios.load_glossary())
        row = vsj.glossary_rows()[self.NAME]
        self.assertEqual(vsj.families(row["payda"]), {"assigned"})
        self.assertIn("dönem", row["definition"])
        self.assertEqual(vsj.glossary_canonical("Dönem Kaynaklı İade veya Şikâyet Talebi Oranı (30 gün)"), self.NAME)

    def test_a_request_or_order_denominator_is_refused(self):
        sc = plain(guardrail=guardrail(self.NAME, "Gelen iade talebi", "must_not_increase"))
        self.assertTrue(has(errs(sc), GLOSSARY_MEANING), errs(sc))
        sc = plain(guardrail=guardrail(self.NAME, "Teste atanan ziyaretçi (abonelik başlatanlar değil)",
                                       "must_not_increase"))
        self.assertFalse(has(errs(sc), GLOSSARY_MEANING) or has(errs(sc), MISMATCH), errs(sc))


if __name__ == "__main__":
    unittest.main()
