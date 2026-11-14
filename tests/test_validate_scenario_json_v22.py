#!/usr/bin/env python3
"""validate_scenario_json.py denetimleri için unit testler. Bağımlılıksız.

Kapsam: uyarı kanalı ve --strict; kaydın hata denetimleri (source_note,
adapted_from, guardrail türleri, birincilin adını taşıyan guardrail, birincil
ve metrik guardrail paydasının bir kitle olması, tümleyen guardrail,
düzenlemeye tabi akışta 'regulation' uyarısı, varyant kimlikleri, metin
olmayan kart alanları); uyarılar (başlık, tek cümle, uzunluk, zayıf kanıtla
kesin dil, tırnak) ve detay görünümünün KPI satırlarına taşınan sezgiler
(payda, sayı/gören, tümleyen). Aşama 3'ün yeni kapıları test_validate_scenario_json_v3.py'de.
"""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import validate_scenario_json as vsj  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
SCHEMA = vsj.load_schema()


A11Y = {"type": "accessibility",
        "text": "Bağlantı klavyeyle erişilebilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt ve "
                "kontrastı en az 4.5:1 olmalı."}


def base():
    # Stage 3: the link needs its accessibility warning, the coupon its invariants, sector evidence its note.
    return {
        "id": "cart-checkout-coupon-field-01",
        "title": "Açık kupon alanı sepet terkini artırır mı?",
        "problem": "Açık kupon kutusu kodu olmayan kullanıcıyı kod aramak için sepetten çıkarıyor.",
        "mechanism": "Bağlantı arkasındaki alan eksik indirimi hatırlatmadığı için kod arama nedeni kalkar.",
        "variable": "Kupon kodu alanının görünürlüğü",
        "variants": [{"id": "A", "description": "Açık kutu", "is_current": True},
                     {"id": "B", "description": "Bağlantı arkasında"}],
        "difference": "change",
        "primary_kpi": {"name": "Sipariş Tamamlama Oranı", "denominator": "Sepet sayfasına ulaşan ziyaretçi",
                        "direction": "increase"},
        "guardrail": {"name": "Kupon Kullanım Oranı", "kind": "metric", "denominator": "Tamamlanan sipariş",
                      "direction": "must_not_decrease"},
        "invariants": ["Geçerli bir kod iki kolda da aynı adımla uygulanır.",
                       "Geçersiz bir kod iki kolda da aynı hata mesajını alır."],
        "warnings": [dict(A11Y)],
        "source": "generated",
        "source_note": "Arşivde bu sayfanın kupon bağlantısına uyan bir senaryo yok.",
        "evidence": {"level": "sector", "note": "Sepet sayfalarında sık görülen bir kaçak; bu sayfada ölçülmedi."},
        "priority": {"tier": "medium", "rationale": "Ödeme öncesi kaçağı hedefliyor, kanıt sektör gözlemi, iş küçük.",
                     "inputs": {"evidence": "archive_or_research", "main_path": True, "noticeable": True, "effort": "low"}},
    }


def with_detail(sc=None):
    sc = sc or base()
    sc["detail"] = {
        "test_items": ["Kaçak kapanıyor mu?", "Segment farkı var mı?", "Metin etkiliyor mu?"],
        "kpis": [
            {"name": "Ziyaretçi Başına Gelir (RPV)", "role": "primary", "question": "Artıyor mu?"},
            {"name": "Sipariş Tamamlama Oranı (sepete ulaşan kullanıcı başına)", "role": "secondary",
             "question": "Değişiyor mu?"},
            {"name": "Kupon Kullanım Oranı (sipariş başına)", "role": "guardrail", "question": "Çökmemeli."},
        ],
        "dont_items": ["Alanı kaldırmayın.", "Hatayı gizlemeyin.", "Aynı testte metni değiştirmeyin."],
    }
    return sc


def card(**over):
    c = {"difference": "change",  # the record's own: card.difference never overrides it (contract 5)
         "variant_a": '<div class="r-h">Sepet</div>',
         "variant_b": '<div class="r-h">Sepet</div><div class="hl" data-note="Yeni"><div class="r-link">Kodum var</div></div>'}
    c.update(over)
    return c


def errs(sc, lang="en"):
    return vsj.validate(sc, SCHEMA, lang)


def warns(sc, lang="en"):
    return vsj.lint(sc, SCHEMA, lang)


def has(items, fragment):
    return any(fragment in x for x in items)


class TestBaseline(unittest.TestCase):
    def test_base_is_clean(self):
        self.assertEqual(errs(base()), [])
        self.assertEqual(warns(base()), [])

    def test_base_with_card_is_clean(self):
        sc = base()
        sc["card"] = card()
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])

    def test_detail_on_request_is_clean(self):
        sc = with_detail()
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])

    def test_scenario_without_card_is_valid(self):
        self.assertNotIn("card", base())
        self.assertEqual(errs(base()), [])

    def test_shipped_example_has_no_errors_and_no_warnings(self):
        with open(EXAMPLE, encoding="utf-8") as fh:
            sc = json.load(fh)
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])


class TestSourceErrors(unittest.TestCase):
    def test_generated_without_source_note(self):
        sc = base()
        del sc["source_note"]
        self.assertTrue(has(errs(sc), "source_note: a 'generated' record says why no archive scenario fits"), errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "source_note: kaynak 'generated' ise"), errs(sc, "tr"))

    def test_archive_and_adapted_without_adapted_from(self):
        for source in ("archive", "adapted"):
            sc = base()
            sc["source"] = source
            sc["evidence"] = {"level": "archive"}
            e = errs(sc)
            self.assertTrue(has(e, "adapted_from: a record with source '%s'" % source), (source, e))
            self.assertFalse(has(e, "source_note"), (source, e))
            sc["adapted_from"] = "Açık kupon kodu alanı sepet terkini artırır mı?"
            self.assertEqual(errs(sc), [], source)


class TestGuardrailShape(unittest.TestCase):
    """guardrail.kind bir etiket: hangi dalın eksiği varsa o söylenir."""

    def test_metric_needs_denominator_and_direction(self):
        for key in ("denominator", "direction"):
            sc = base()
            del sc["guardrail"][key]
            e = errs(sc)
            self.assertIn("guardrail: missing required field %r" % key, e)
            self.assertFalse(has(e, "oneOf"), e)

    def test_metric_direction_enum(self):
        sc = base()
        sc["guardrail"]["direction"] = "decrease"
        self.assertTrue(has(errs(sc), "guardrail.direction: 'decrease' is not one of"), errs(sc))

    def test_check_needs_criterion(self):
        sc = base()
        sc["guardrail"] = {"name": "Erişilebilirlik Kontrolü (yayın öncesi, geçti/kaldı)", "kind": "check"}
        self.assertIn("guardrail: missing required field 'criterion'", errs(sc))
        sc["guardrail"]["criterion"] = "Geçmeli: B’nin klavye ve ekran okuyucu incelemesinde kritik sorun yok."
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])

    def test_fields_of_the_other_kind_are_refused(self):
        sc = base()
        sc["guardrail"] = {"name": "Erişilebilirlik Kontrolü", "kind": "check", "criterion": "Geçmeli: sorun yok.",
                           "direction": "must_not_decrease"}
        self.assertIn("guardrail: unknown field 'direction'", errs(sc))

    def test_unknown_kind_names_the_options(self):
        sc = base()
        sc["guardrail"]["kind"] = "metrik"
        self.assertIn("guardrail.kind: 'metrik' is not one of ['metric', 'check']", errs(sc))

    def test_missing_kind(self):
        sc = base()
        del sc["guardrail"]["kind"]
        self.assertTrue(has(errs(sc), "guardrail: 0/2 oneOf branches matched"), errs(sc))
        self.assertTrue(has(errs(sc), "missing required field 'kind'"), errs(sc))

    def test_tagged_union_reading_is_generic(self):
        branches = SCHEMA["properties"]["guardrail"]["oneOf"]
        self.assertIs(vsj.tagged_branch({"kind": "check"}, branches)[0], branches[1])
        self.assertEqual(vsj.tagged_branch({"kind": "x"}, branches), (None, ("kind", ["metric", "check"])))
        self.assertEqual(vsj.tagged_branch({"name": "x"}, branches), (None, None))
        box = SCHEMA["$defs"]["boxItem"]["oneOf"]  # untagged: the generic reading stays
        self.assertEqual(vsj.tagged_branch({"label": "x", "text": "y"}, box), (None, None))


class TestKpiErrors(unittest.TestCase):
    def test_guardrail_with_the_primary_name(self):
        sc = base()
        sc["guardrail"]["name"] = "sipariş  tamamlama oranı"
        self.assertTrue(has(errs(sc), "guardrail.name: 'sipariş  tamamlama oranı' is the primary KPI’s name"),
                        errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "kural 3"), errs(sc, "tr"))

    def test_primary_denominator_that_is_a_count(self):
        for den in ("Sipariş Sayısı", "sipariş adedi", "Number of orders"):
            sc = base()
            sc["primary_kpi"]["denominator"] = den
            self.assertTrue(has(errs(sc), "primary_kpi.denominator: %r is a count" % den), (den, errs(sc)))

    def test_primary_denominator_of_users_who_saw_it(self):
        for den in ("Bağlantıyı gören kullanıcı", "Bannerı görüp sepete dönen kullanıcı",
                    "Users who saw the link", "Users who have seen the banner"):
            sc = base()
            sc["primary_kpi"]["denominator"] = den
            self.assertTrue(has(errs(sc), "primary_kpi.denominator: %r is a \"users who saw it\" population" % den),
                            (den, errs(sc)))

    def test_saw_in_the_primary_name_is_an_error_too(self):
        sc = base()
        sc["primary_kpi"]["name"] = "Bağlantıyı Gören Kullanıcı Başına Sipariş Oranı"
        self.assertTrue(has(errs(sc), "primary_kpi.name:"), errs(sc))

    def test_population_denominators_pass(self):
        for den in ("Teste atanan ziyaretçi (atama sepete ulaşınca)", "Sepete ulaşan kullanıcı (iki kolda aynı tetikleyici)",
                    "Visitors assigned on reaching the cart"):
            sc = base()
            sc["primary_kpi"]["denominator"] = den
            self.assertEqual(errs(sc), [], den)

    def test_count_or_saw_on_a_metric_guardrail_is_an_error(self):
        # Stage 3: a guardrail compared over a population only one arm has is as broken as such a primary.
        sc = base()
        sc["guardrail"]["denominator"] = "Butonu gören kullanıcı"
        self.assertTrue(has(errs(sc), "guardrail.denominator: 'Butonu gören kullanıcı'"), errs(sc))
        self.assertFalse(has(warns(sc), "guardrail.denominator"), warns(sc))
        sc["guardrail"]["denominator"] = "Sipariş Sayısı"
        self.assertTrue(has(errs(sc), "guardrail.denominator: 'Sipariş Sayısı' is a count"), errs(sc))


class TestDetailBoxes(unittest.TestCase):
    def test_three_to_six_items(self):
        for n in (3, 4, 5, 6):
            sc = with_detail()
            sc["detail"]["test_items"] = ["Madde %d soruyor mu?" % i for i in range(n)]
            self.assertEqual(errs(sc), [], n)
            self.assertEqual(warns(sc), [], n)

    def test_seven_items_is_an_error(self):
        for box in ("test_items", "dont_items"):
            sc = with_detail()
            sc["detail"][box] = ["Madde %d" % i for i in range(7)]
            self.assertTrue(has(errs(sc), "detail.%s: has 7 item(s), maximum is 6" % box), errs(sc))
        sc = with_detail()
        sc["detail"]["kpis"] += [{"name": "M%d (kullanıcı başına)" % i, "role": "secondary"} for i in range(4)]
        self.assertTrue(has(errs(sc), "detail.kpis: has 7 item(s), maximum is 6"), errs(sc))

    def test_two_items_is_an_error(self):
        sc = with_detail()
        sc["detail"]["dont_items"] = ["Bir", "İki"]
        self.assertTrue(has(errs(sc), "minimum is 3"))

    def test_metric_listed_twice(self):
        sc = with_detail()
        sc["detail"]["kpis"][2] = {"name": "ziyaretçi başına  gelir (RPV)", "role": "guardrail", "question": "Düşmemeli."}
        self.assertTrue(has(errs(sc), "detail.kpis[2]: 'ziyaretçi başına  gelir (RPV)' appears twice (detail.kpis[0])"),
                        errs(sc))


class TestVariantErrors(unittest.TestCase):
    def test_variant_ids_must_be_a_then_b(self):
        sc = base()
        sc["variants"][1]["id"] = "A"
        self.assertTrue(has(errs(sc), 'ids must be "A" then "B"'), errs(sc))
        sc = base()
        sc["variants"][1]["is_current"] = True
        self.assertTrue(has(errs(sc), "the current page is always A"), errs(sc))


class TestCardFields(unittest.TestCase):
    def test_non_string_variant_does_not_crash(self):
        sc = base()
        sc["card"] = card(variant_a=123)
        e = errs(sc)
        self.assertTrue(has(e, "card.variant_a: expected type string"), e)

    def test_non_string_card_fields_are_errors(self):
        sc = base()
        sc["card"] = card(note_pos=5, url=["x"], mockup_basis=["shared_page"], bottom_nav=[{"label": "Ana Sayfa"}])
        e = errs(sc)
        for path in ("card.note_pos", "card.url", "card.mockup_basis", "card.bottom_nav[0]"):
            self.assertTrue(has(e, path), (path, e))

    def test_markup_outside_the_allowlist_is_an_error(self):
        sc = base()
        sc["card"] = card(variant_b=card()["variant_b"] + "<img src=x onerror=alert(1)>")
        self.assertTrue(has(errs(sc), "card: variant_b"), errs(sc))

    def test_ring_margin_is_an_error(self):
        sc = base()
        sc["card"] = card(variant_b=card()["variant_b"].replace('class="hl"', 'class="hl" style="margin-left:20px"'))
        self.assertTrue(has(errs(sc, "tr"), "içeriği itmemeli"), errs(sc, "tr"))

    def test_unknown_colour_name_is_an_error(self):
        sc = base()
        sc["card"] = card(brand={"primary": "mavi"})
        self.assertTrue(has(errs(sc), "brand.primary"), errs(sc))
        sc["card"] = card(brand={"primary": "rgb(,,/%%)"})
        self.assertTrue(has(errs(sc), "brand.primary"), errs(sc))
        sc["card"] = card(brand={"primary": "navy", "on_primary": "#fff"})
        self.assertEqual(errs(sc), [])

    def test_bottom_nav_active(self):
        sc = base()
        sc["device"] = "phone"
        sc["card"] = card(bottom_nav=["Ana Sayfa", "Ürünlerim"], bottom_nav_active="Ürünlerim")
        self.assertEqual(errs(sc), [])
        sc["card"]["bottom_nav_active"] = 1
        self.assertEqual(errs(sc), [])
        sc["card"]["bottom_nav_active"] = "Profil"
        self.assertTrue(has(errs(sc), "card.bottom_nav_active"), errs(sc))
        sc["card"]["bottom_nav_active"] = 2
        self.assertTrue(has(errs(sc), "card.bottom_nav_active"), errs(sc))
        del sc["card"]["bottom_nav"]
        self.assertEqual(errs(sc), [])  # ignored without bottom_nav

    def test_tab_bar_and_url_follow_the_frame(self):
        sc = base()
        sc["device"] = "phone-web"
        sc["card"] = card(url="magaza.example/sepet", bottom_nav=["Ana Sayfa"])
        self.assertTrue(has(errs(sc), "card.bottom_nav: only valid with device 'phone'"), errs(sc))
        sc["card"] = card()
        self.assertTrue(has(errs(sc), "card.url: device 'phone-web' draws an address bar"), errs(sc))
        sc["device"] = "phone"
        sc["card"] = card(device="web")
        self.assertTrue(has(errs(sc), "card.url"), errs(sc))

    def test_card_warnings_reach_lint(self):
        sc = base()
        sc["card"] = card(variant_b=card()["variant_b"].replace('class="r-link"', 'class="r-link" style="color:#0a7f3f"'))
        w = warns(sc)
        self.assertTrue(has(w, "card: ") and has(w, "#0a7f3f"), w)
        self.assertEqual([x for x in vsj.lint(sc, SCHEMA, "en", include_card=False) if "#0a7f3f" in x], [])

    def test_shared_page_without_is_current_warns(self):
        sc = base()
        del sc["variants"][0]["is_current"]
        sc["card"] = card(mockup_basis="shared_page")
        self.assertTrue(has(warns(sc), "is_current"), warns(sc))

    def test_card_device_differs_from_scenario_device(self):
        sc = base()
        sc["device"] = "web"
        sc["card"] = card(device="phone")
        self.assertTrue(has(warns(sc), "differs from the scenario's device"), warns(sc))


class TestTitleAndLength(unittest.TestCase):
    def test_title_without_question_mark(self):
        sc = base()
        sc["title"] = "Açık kupon alanı sepet terkini artırır"
        self.assertTrue(has(warns(sc), "title: does not end with '?'"), warns(sc))

    def test_title_over_90_characters(self):
        sc = base()
        sc["title"] = "Kupon alanını sepetin altına, ödeme adımına ve ayrıca ürün sayfasına taşımak sepet terkini artırır mı?"
        self.assertGreater(len(sc["title"]), 90)
        self.assertTrue(has(warns(sc), "title: %d characters; keep the question short (at most 90)" % len(sc["title"])),
                        warns(sc))
        sc["title"] = "x" * 89 + "?"
        self.assertFalse(has(warns(sc), "title:"), warns(sc))

    def test_problem_and_mechanism_are_one_sentence(self):
        for key in ("problem", "mechanism"):
            sc = base()
            sc[key] = "Kutu açık duruyor. Kullanıcı kod aramaya çıkıyor."
            self.assertTrue(has(warns(sc), "%s: 2 sentences; write one" % key), (key, warns(sc)))
            self.assertTrue(has(warns(sc, "tr"), "%s: 2 cümle var; tek cümle olmalı" % key), warns(sc, "tr"))

    def test_sentence_count_reads_stops_not_dots(self):
        self.assertEqual(vsj.sentence_count("Kupon kutusu açık, kullanıcı çıkıyor."), 1)
        self.assertEqual(vsj.sentence_count("Fiyat 1.250 TL ve indirim %2.5 oranında."), 1)
        self.assertEqual(vsj.sentence_count("Kısa alanlar (ör. Ad) doldurulur."), 1)
        self.assertEqual(vsj.sentence_count("Short fields (e.g. Name) are filled."), 1)
        self.assertEqual(vsj.sentence_count("Kutu açık. “İndirim” arıyor! Çıkıyor mu?"), 3)
        self.assertEqual(vsj.sentence_count("Kutu açık… Kullanıcı çıkıyor."), 2)

    def test_long_fields_warn(self):
        long = "Kupon kutusu " + "çok " * 70 + "uzun."
        self.assertGreater(len(long), 240)
        cases = (("problem", lambda sc: sc.__setitem__("problem", long)),
                 ("mechanism", lambda sc: sc.__setitem__("mechanism", long)),
                 ("variants[1].description", lambda sc: sc["variants"][1].__setitem__("description", long)),
                 ("priority.rationale", lambda sc: sc["priority"].__setitem__("rationale", long)),
                 ("warnings[0].text", lambda sc: sc.__setitem__("warnings", [{"type": "feasibility", "text": long}])))
        for path, apply in cases:
            sc = base()
            apply(sc)
            self.assertTrue(has(warns(sc), "%s: %d characters; keep it to 240" % (path, len(long))), (path, warns(sc)))

    def test_240_characters_is_fine(self):
        sc = base()
        sc["problem"] = "K" + "a" * 239
        self.assertFalse(has(warns(sc), "characters"), warns(sc))


class TestRegulation(unittest.TestCase):
    WARNING = {"type": "regulation", "text": "B’nin metni için uyum onayı alınmadan teste trafik açılmaz."}

    # Stage 3: a regulated-looking record without a regulation warning is an error (it was a warning).

    def test_regulated_record_needs_a_regulation_warning(self):
        sc = base()
        sc["title"] = "Poliçe özetini maddelere bölmek talep oranını artırır mı?"
        e = errs(sc)
        self.assertTrue(has(e, "warnings: the record looks like a regulated flow (Poliçe)"), e)
        self.assertTrue(has(e, "add a warning of type 'regulation' (rule 11)"), e)
        self.assertTrue(has(errs(sc, "tr"), "'regulation' türünde bir uyarı ekleyin (kural 11)"), errs(sc, "tr"))
        self.assertFalse(has(warns(sc), "regulated flow"), warns(sc))
        sc["warnings"] = sc["warnings"] + [self.WARNING]
        self.assertEqual(errs(sc), [])

    def test_another_warning_type_does_not_count(self):
        sc = base()
        sc["stage"] = "insurance-quote"
        self.assertEqual([w["type"] for w in sc["warnings"]], ["accessibility"])
        self.assertTrue(has(errs(sc), "regulated flow (insurance)"), errs(sc))

    def test_every_contract_word_is_read(self):
        words = ("insurance", "pension", "credit", "loan", "consent", "KVKK", "sigorta", "emeklilik", "BES", "kredi",
                 "poliçe", "rıza", "onay")
        for word in words:
            sc = base()
            sc["mechanism"] = "Adımda %s metni kısalınca kullanıcı devam eder." % word
            self.assertTrue(has(errs(sc), "regulated flow (%s)" % word), (word, errs(sc)))

    def test_the_fields_that_are_read(self):
        for key in ("stage", "title", "problem", "mechanism"):
            sc = base()
            sc[key] = "Emeklilik planına katılım adımı uzun."
            self.assertTrue(has(errs(sc), "regulated flow"), (key, errs(sc)))
        sc = base()
        sc["variants"][1]["description"] = "KVKK aydınlatma bağlantısı alanın yanında"
        self.assertTrue(has(errs(sc), "regulated flow (KVKK)"), errs(sc))
        sc = base()
        sc["priority"]["rationale"] = "Sigorta teklifinden önceki adımda, kanıt sektör gözlemi."
        self.assertFalse(has(errs(sc), "regulated flow"), errs(sc))

    def test_card_payment_is_not_a_regulated_flow(self):
        sc = base()
        sc["problem"] = "Kredi kartı formu uzun olduğu için ödeme adımı yavaş."
        self.assertEqual(errs(sc), [])
        sc["problem"] = "The credit card form is long."
        self.assertEqual(errs(sc), [])


class TestOverconfidence(unittest.TestCase):
    PHRASES = ("kesin", "kesinlikle", "garanti", "mutlaka artırır", "certainly", "guaranteed", "will definitely")

    def test_weak_evidence_with_certain_wording_warns(self):
        for level in ("intuition", "sector"):
            for phrase in self.PHRASES:
                sc = base()
                sc["evidence"] = {"level": level}
                sc["mechanism"] = "Bağlantı arkasındaki alan %s kaçağı kapatır." % phrase
                self.assertTrue(has(warns(sc), "mechanism: %r is too certain for '%s' evidence" % (phrase, level)),
                                (level, phrase, warns(sc)))

    def test_problem_and_priority_rationale_are_read(self):
        sc = base()
        sc["problem"] = "Açık kutu kesinlikle kaçağa yol açıyor."
        sc["priority"]["rationale"] = "Etkisi garanti, iş küçük."
        w = warns(sc)
        self.assertTrue(has(w, "problem: 'kesinlikle'"), w)
        self.assertTrue(has(w, "priority.rationale: 'garanti'"), w)
        self.assertTrue(has(warns(sc, "tr"), "kanıt 'sector' iken 'kesinlikle' fazla kesin"), warns(sc, "tr"))

    def test_stronger_evidence_is_not_checked(self):
        for level in ("archive", "user_data"):
            sc = base()
            sc["evidence"] = {"level": level}
            sc["mechanism"] = "Bağlantı arkasındaki alan kesinlikle kaçağı kapatır."
            self.assertFalse(has(warns(sc), "too certain"), (level, warns(sc)))

    def test_whole_words_only(self):
        sc = base()
        sc["mechanism"] = "Kesintisiz ödeme akışı ve garantili teslimat bilgisi kullanıcıyı sepette tutar."
        self.assertFalse(has(warns(sc), "too certain"), warns(sc))


class TestQuotes(unittest.TestCase):
    def test_straight_quotes_in_turkish_text(self):
        for path, apply in (("problem", lambda sc: sc.__setitem__("problem", 'Kullanıcı "indirim arayayım" diyor.')),
                            ("mechanism", lambda sc: sc.__setitem__("mechanism", 'B "Kodum var" der.')),
                            ("variants[1].description", lambda sc: sc["variants"][1].__setitem__("description", '"Kodum var"')),
                            ("primary_kpi.name", lambda sc: sc["primary_kpi"].__setitem__("name", '"RPV"')),
                            ("guardrail.denominator", lambda sc: sc["guardrail"].__setitem__("denominator", '"Sipariş"')),
                            ("source_note", lambda sc: sc.__setitem__("source_note", 'Arşivde "kupon" yok.')),
                            ("priority.rationale", lambda sc: sc["priority"].__setitem__("rationale", 'Etkisi "ödeme" adımında.'))):
            sc = base()
            apply(sc)
            self.assertTrue(has(warns(sc), "%s: straight quotes" % path), (path, warns(sc)))
            sc["lang"] = "en"
            self.assertFalse(has(warns(sc), "straight quotes"), (path, warns(sc)))

    def test_detail_items_are_read(self):
        sc = with_detail()
        sc["detail"]["dont_items"][0] = 'Alanı "gizli" yapmayın.'
        self.assertTrue(has(warns(sc), "detail.dont_items[0]: straight quotes"), warns(sc))


class TestComplement(unittest.TestCase):
    def record(self, primary, primary_den, guardrail, guardrail_den):
        sc = base()
        sc["primary_kpi"].update(name=primary, denominator=primary_den)
        sc["guardrail"].update(name=guardrail, denominator=guardrail_den, direction="must_not_increase")
        return sc

    # Stage 3: a complement guardrail is an error (it was a warning), in the record and in the detail view.

    def test_record_complement_is_an_error(self):
        e = errs(self.record("Sipariş Tamamlama Oranı", "Sepete ulaşan kullanıcı",
                             "Sepet Terk Oranı", "sepete  ulaşan kullanıcı"))
        self.assertTrue(has(e, "guardrail: guardrail 'Sepet Terk Oranı' looks like the complement of the primary"), e)
        e = errs(self.record("Checkout Conversion Rate", "Assigned users", "Checkout Abandonment Rate", "Assigned users"))
        self.assertTrue(has(e, "complement"), e)

    def test_record_later_step_abandonment_is_fine(self):
        sc = self.record("Kayıt Tamamlama Oranı", "Forma başlayan kullanıcı",
                         "Ödeme Adımı Terk Oranı", "Ödeme adımına ulaşan kullanıcı")
        self.assertEqual(errs(sc), [])

    def test_a_check_is_never_a_complement(self):
        sc = base()
        sc["primary_kpi"]["name"] = "Sipariş Tamamlama Oranı"
        sc["guardrail"] = {"name": "Sepet Terk Oranı Kontrolü", "kind": "check", "criterion": "Geçmeli: akış bozulmaz."}
        self.assertEqual(errs(sc), [])

    def detail(self, primary, guardrail):
        sc = with_detail()
        sc["detail"]["kpis"][0]["name"] = primary
        sc["detail"]["kpis"][2] = {"name": guardrail, "role": "guardrail", "question": "Artmamalı."}
        return sc

    def test_detail_same_denominator_complement_is_an_error(self):
        e = errs(self.detail("Sipariş Tamamlama Oranı (sepete ulaşan kullanıcı başına)",
                             "Sepet Terk Oranı (sepete ulaşan kullanıcı başına)"))
        self.assertTrue(has(e, "detail.kpis[2]: guardrail 'Sepet Terk Oranı (sepete ulaşan kullanıcı başına)' looks like"),
                        e)

    def test_detail_no_denominator_complement_is_an_error(self):
        e = errs(self.detail("Form Tamamlama Oranı (forma başlayan kullanıcı başına)", "Sayfa Terk Oranı"))
        self.assertTrue(has(e, "complement"), e)

    def test_detail_unrelated_guardrail_is_fine(self):
        sc = self.detail("Sipariş Tamamlama Oranı (sepete ulaşan kullanıcı başına)", "İade Oranı (sipariş başına, 30 gün)")
        self.assertFalse(has(errs(sc) + warns(sc), "complement"), errs(sc) + warns(sc))


class TestDetailDenominatorWarnings(unittest.TestCase):
    """Detay görünümünün KPI satırlarına taşınan payda sezgileri."""

    def kpi(self, name, role="guardrail", **extra):
        sc = with_detail()
        sc["detail"]["kpis"][2 if role == "guardrail" else 1] = dict({"name": name, "role": role, "question": "Soru?"},
                                                                     **extra)
        return sc

    def test_rate_without_denominator_warns_on_any_role(self):
        for role in ("guardrail", "secondary"):
            w = warns(self.kpi("Talepten Poliçeye Dönüşüm Oranı", role))
            self.assertTrue(has(w, "is a rate with no stated denominator"), (role, w))

    def test_window_in_parentheses_is_not_a_denominator(self):
        w = warns(self.kpi("Talepten Poliçeye Dönüşüm Oranı (90 gün)"))
        self.assertTrue(has(w, "no stated denominator"), w)

    def test_primary_rate_without_denominator_warns(self):
        sc = with_detail()
        sc["detail"]["kpis"][0]["name"] = "Talep Oluşturma Oranı"
        self.assertTrue(has(warns(sc), "detail.kpis[0]"), warns(sc))

    def test_stated_denominators_do_not_warn(self):
        for name in ("Dönüşüm Oranı (atanan kullanıcı başına)", "Conversion Rate (per assigned user)",
                     "Sipariş Başına İade Oranı", "Orders per Visitor Rate"):
            self.assertFalse(has(warns(self.kpi(name)), "denominator"), name)
        self.assertFalse(has(warns(self.kpi("Dönüşüm Oranı", denominator="atanan kullanıcı")), "denominator"))

    def test_non_rate_metrics_are_skipped(self):
        for name in ("Akordeonda Kalma Süresi", "LCP", "Ziyaretçi Başına Gelir (RPV)", "Ortalama Sepet Tutarı (AOV)",
                     "Sipariş Tutarı"):
            self.assertFalse(has(warns(self.kpi(name, "secondary")), "denominator"), name)

    def test_check_type_guardrail_is_skipped(self):
        for name in ("Erişilebilirlik Kontrolü (yayın öncesi, geçti/kaldı)",
                     "Erişilebilirlik Kontrolü Geçme Oranı (yayın öncesi, geçti/kaldı)",
                     "Contrast Check Pass Rate (pre-launch, pass/fail)"):
            sc = self.kpi(name)
            self.assertFalse(has(warns(sc), "denominator"), (name, warns(sc)))

    def test_a_check_is_read_from_its_name(self):
        # Pass/fail kontrolü adıyla tanınır; adı kontrol demeyen bir oran, payda uyarısını alır.
        self.assertTrue(has(warns(self.kpi("Kontrast Oranı")), "denominator"))
        self.assertFalse(has(warns(self.kpi("Kontrast Kontrolü (yayın öncesi, geçti/kaldı)")), "denominator"))

    def test_window_inside_the_name_is_part_of_the_definition(self):
        for name in ("İade Oranı (sipariş başına, 30 gün)", "Return Rate (per order, 30 days)",
                     "Poliçe İptal Oranı (düzenlenen poliçe başına, 90 gün)"):
            sc = self.kpi(name)
            self.assertEqual(errs(sc), [], name)
            self.assertEqual(warns(sc), [], name)

    def test_b_only_line_is_skipped(self):
        for name in ("Uygunluk Girişine Dokunma Oranı (yalnız B, tanı amaçlı)", "Tooltip Open Rate (B only, diagnostic)",
                     "Yeni Butonu Gören Kullanıcı Sayısı (yalnız B)"):
            w = warns(self.kpi(name, "secondary"))
            self.assertEqual(w, [], (name, w))

    def test_archive_scenario_inherits_glossary_denominators(self):
        sc = self.kpi("Kupon Kullanım Oranı")
        sc["source"] = "archive"
        sc["adapted_from"] = "Açık kupon kodu alanı sepet terkini artırır mı?"
        sc["evidence"] = {"level": "archive"}
        self.assertFalse(has(warns(sc), "denominator"), warns(sc))
        sc["source"] = "generated"
        self.assertTrue(has(warns(sc), "denominator"), warns(sc))

    def test_count_primary_is_an_error(self):
        sc = with_detail()
        sc["detail"]["kpis"][0]["name"] = "Sipariş Sayısı"
        self.assertTrue(has(errs(sc), "detail.kpis[0]: primary KPI 'Sipariş Sayısı' is a count"), errs(sc))

    def test_count_per_visitor_is_fine(self):
        sc = with_detail()
        sc["detail"]["kpis"][0]["name"] = "Ziyaretçi Başına Sipariş Sayısı"
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])

    def test_saw_denominator_on_primary_is_an_error(self):
        sc = with_detail()
        sc["detail"]["kpis"][0]["name"] = "Sipariş Oranı (kupon bağlantısını gören kullanıcı başına)"
        self.assertTrue(has(errs(sc), '"users who saw"'), errs(sc))

    def test_count_and_saw_on_other_roles_warn(self):
        sc = with_detail()
        sc["detail"]["kpis"][1] = {"name": "Hızlı Ödeme Tıklama Sayısı", "role": "secondary", "question": "?"}
        sc["detail"]["kpis"][2] = {"name": "İade Oranı (butonu gören kullanıcı başına)", "role": "guardrail",
                                   "question": "Artmamalı."}
        self.assertEqual(errs(sc), [])
        w = warns(sc)
        self.assertTrue(has(w, "detail.kpis[1]: secondary KPI") and has(w, "is a count"), w)
        self.assertTrue(has(w, "detail.kpis[2]: guardrail KPI") and has(w, "users who saw"), w)

    def test_guardrail_without_question(self):
        sc = with_detail()
        del sc["detail"]["kpis"][2]["question"]
        self.assertTrue(has(warns(sc), "detail.kpis[2]: guardrail has no question text"), warns(sc))

    def test_turkish_message(self):
        w = warns(self.kpi("Talepten Poliçeye Dönüşüm Oranı"), "tr")
        self.assertTrue(has(w, "paydası yazılmamış"), w)


class TestSchemaKeywords(unittest.TestCase):
    def test_schema_uses_only_implemented_keywords(self):
        self.assertEqual(vsj.unsupported_keywords(SCHEMA), [])
        broken = copy.deepcopy(SCHEMA)
        broken["properties"]["title"]["maxLength"] = 10
        broken["properties"]["variants"]["uniqueItems"] = True
        self.assertEqual(vsj.unsupported_keywords(broken), ["maxLength", "uniqueItems"])
        # The subset is what the schema uses: keywords no field needs any more are refused, not half-applied.
        broken = copy.deepcopy(SCHEMA)
        broken["properties"]["card"]["dependentRequired"] = {"url": ["device"]}
        broken["properties"]["card"]["properties"]["bottom_nav_active"]["maximum"] = 9
        self.assertEqual(vsj.unsupported_keywords(broken), ["dependentRequired", "maximum"])

    def test_keywords_inside_oneof_branches_are_seen(self):
        broken = copy.deepcopy(SCHEMA)
        broken["properties"]["guardrail"]["oneOf"][0]["if"] = {"required": ["kind"]}
        self.assertEqual(vsj.unsupported_keywords(broken), ["if"])

    def test_unknown_keyword_stops_the_cli(self):
        broken = copy.deepcopy(SCHEMA)
        broken["properties"]["title"]["maxLength"] = 10
        with tempfile.TemporaryDirectory() as tmp:
            sp = os.path.join(tmp, "schema.json")
            with open(sp, "w", encoding="utf-8") as fh:
                json.dump(broken, fh)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(vsj.main(["--schema", sp, EXAMPLE]), 2)
            self.assertIn("maxLength", err.getvalue())


class TestCli(unittest.TestCase):
    def run_cli(self, doc, *flags):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = vsj.main(list(flags) + [path])
            return code, out.getvalue()

    def warned(self):
        sc = base()
        sc["title"] = "Açık kupon alanı sepet terkini artırır"
        return sc

    def test_warnings_print_and_exit_zero(self):
        code, out = self.run_cli(self.warned(), "--lang", "en")
        self.assertEqual(code, 0, out)
        self.assertIn("1 warning(s) (exit code unaffected)", out)
        self.assertIn("does not end with '?'", out)

    def test_strict_turns_warnings_into_errors(self):
        code, out = self.run_cli(self.warned(), "--lang", "en", "--strict")
        self.assertEqual(code, 1, out)
        self.assertIn("does not end with '?'", out)

    def test_strict_with_a_clean_file_is_zero(self):
        code, out = self.run_cli(base(), "--strict")
        self.assertEqual(code, 0, out)

    def test_turkish_default(self):
        code, out = self.run_cli(self.warned())
        self.assertEqual(code, 0)
        self.assertIn("1 uyarı (çıkış kodunu etkilemez)", out)

    def test_errors_exit_one(self):
        sc = base()
        del sc["source_note"]
        code, out = self.run_cli(sc, "--lang", "en")
        self.assertEqual(code, 1, out)
        self.assertIn("source_note", out)

    def test_regulated_flow_without_a_regulation_warning_fails(self):
        # Stage 3: an error, so it fails without --strict too.
        sc = base()
        sc["title"] = "Poliçe özetini maddelere bölmek talep oranını artırır mı?"
        for flags in (("--lang", "en"), ("--lang", "en", "--strict")):
            code, out = self.run_cli(sc, *flags)
            self.assertEqual(code, 1, (flags, out))
            self.assertIn("regulated flow", out)
        sc["warnings"] = sc["warnings"] + [{"type": "regulation",
                                            "text": "B’nin metni için uyum onayı alınmadan teste trafik açılmaz."}]
        code, out = self.run_cli(sc, "--strict")
        self.assertEqual(code, 0, out)

    def test_shipped_example_passes_strict(self):
        with open(EXAMPLE, encoding="utf-8") as fh:
            code, out = self.run_cli(json.load(fh), "--strict")
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
