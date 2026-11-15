#!/usr/bin/env python3
"""validate_scenario_json.py, 3.4: the regulated-flow reading (item 35), refusal messages that carry the
corrected value (item 8) and the mechanical checks moved over from scenario-critic (item 7). Stdlib only.
"""
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import validate_scenario_json as vsj  # noqa: E402
from test_validate_scenario_json_v3 import plain, with_b, errs, warns, has  # noqa: E402

REGULATION = {"type": "regulation", "text": "B’nin metni için uyum onayı alınmadan teste trafik açılmaz."}


def grocery(**changes):
    """A grocery cart record: the words a checkout uses for confirming an order, nothing legally bound."""
    sc = plain(stage="cart-checkout", title="Sepet özetini onay ekranından önce göstermek siparişi artırır mı?",
               problem="Market sepetinde sipariş özeti yalnızca onay ekranında görünüyor.",
               mechanism="Özet onay ekranından önce görününce kullanıcı Siparişi onayla adımına tutarı bilerek gelir.")
    sc.update(changes)
    return sc


class TestRegulatedFlowReading(unittest.TestCase):
    """Item 35: "onay" counts only in its consent sense; a confirmation screen is no regulated flow."""

    def test_order_confirmation_words_are_not_regulated(self):
        for text in ("Market sepetinde onay ekranı tutarı gösteriyor.", "Siparişi onayla butonu altta duruyor.",
                     "Sipariş onayı e-postası gecikiyor.", "Onay kutusu formun sonunda duruyor.",
                     "The order confirmation screen shows the total."):
            sc = grocery(problem=text)
            self.assertFalse(has(errs(sc), "regulated flow"), (text, errs(sc)))
        self.assertEqual(errs(grocery()), [])

    def test_consent_sense_is_still_regulated(self):
        for text, word in (("Kayıt formundaki pazarlama onayı kutusu uzun.", "pazarlama onayı"),
                           ("Ticari ileti onayı metni kısalıyor.", "ileti onayı"),
                           ("Açık rıza metni adımın sonunda duruyor.", "rıza"),
                           ("KVKK onayı alanın altında duruyor.", "KVKK"),
                           ("Onay metni iki satıra iniyor.", "Onay metni"),
                           ("The consent box sits under the field.", "consent")):
            sc = grocery(problem=text)
            self.assertTrue(has(errs(sc), "regulated flow (%s" % word), (text, errs(sc)))
            sc["warnings"] = [REGULATION]
            self.assertFalse(has(errs(sc), "regulated flow"), (text, errs(sc)))

    def test_subscription_cancellation_and_data_purpose_copy_are_regulated(self):
        for text in ("Abonelik iptali ekranında dondurma seçeneği yok.", "Aboneliği iptal eden kullanıcı geri dönemiyor.",
                     "Users who cancel their subscription see no pause option.",
                     "B adds “No spam, unsubscribe anytime” under the email field.",
                     "Kişisel veri kullanımını anlatan satır butonun altında.", "Gizlilik notu butonun altında.",
                     "A privacy note sits below the button."):
            sc = with_b(plain(), text)
            self.assertTrue(has(errs(sc), "regulated flow"), (text, errs(sc)))

    def test_order_cancellation_is_not_a_subscription(self):
        sc = with_b(plain(), "Sipariş iptal bağlantısı özetin altında")
        sc["warnings"] = [{"type": "accessibility", "text": ("Bağlantı klavyeyle erişilebilir, ekran okuyucuda adıyla "
                                                             "okunur, dokunma alanı en az 44×44 pt ve kontrastı en az "
                                                             "4.5:1 olmalı.")}]
        sc["invariants"] = ["Bağlantı iki kolda da aynı iptal adımını açar."]
        self.assertFalse(has(errs(sc), "regulated flow"), errs(sc))



def example_of(message):
    """The JSON object a refusal prints after "örnek:" / "example:"."""
    m = re.search(r"(?:Düzeltilmiş örnek|Corrected example|Örnek|Example): [^{]*(\{.*?\})(?: \(|$)", message)
    return json.loads(m.group(1)) if m else None


class TestCorrectedValues(unittest.TestCase):
    """Item 8: a refusal the logs show sent the model into the source now prints the value to write."""

    def test_glossary_family_prints_the_glossary_pair_and_it_passes(self):
        for lang, den, want in (
                ("tr", "Kayıt sayfasıyla başlayan oturum, teste atanan",
                 {"name": "Hemen Çıkma Oranı", "denominator": "Sayfayla başlayan oturum"}),
                ("en", "Sessions starting on the signup page, assigned to the test",
                 {"name": "Bounce Rate", "denominator": "Sessions starting on the page"})):
            sc = plain(lang=lang)
            sc["guardrail"] = {"name": want["name"], "kind": "metric", "denominator": den,
                               "direction": "must_not_increase"}
            line = next(e for e in errs(sc, lang) if e.startswith("guardrail:"))
            self.assertEqual(example_of(line), want, line)
            self.assertIn("atanan” sözü" if lang == "tr" else 'The word "assigned"', line)
            sc["guardrail"]["denominator"] = want["denominator"]
            self.assertFalse(has(errs(sc, lang), "guardrail:"), errs(sc, lang))

    def test_conditional_kpi_name_prints_the_per_assigned_pair(self):
        sc = plain()
        sc["primary_kpi"] = {"name": "Teklif → Sözleşme", "denominator": "Teste atanan ziyaretçi",
                             "direction": "increase"}
        line = next(e for e in errs(sc, "tr") if e.startswith("primary_kpi:"))
        self.assertEqual(example_of(line), {"name": "Sözleşme Oranı (30 gün)", "denominator": "Teste atanan ziyaretçi"})

    def link(self, warning=None, b="Başlığın altında “Tüm özellikler” bağlantısı"):
        sc = with_b(plain(), b)
        sc["invariants"] = ["Bağlantı iki kolda da aynı sayfayı açar."]
        if warning:
            sc["warnings"] = [{"type": "accessibility", "text": warning}]
        return sc

    def test_missing_accessibility_warning_prints_a_text_that_passes(self):
        for b in ("Başlığın altında “Tüm özellikler” bağlantısı", "Sepete ekleyince alt sayfa açılır",
                  "Ürün görselleri otomatik dönen bir karuselde", "A dialog opens under the title"):
            for lang in ("tr", "en"):
                sc = self.link(b=b)
                sc["exposure"] = "Ürün sayfasını açan kullanıcı; tetikleyici iki kolda aynı noktada kaydedilir."
                line = next(e for e in errs(sc, lang) if "'accessibility'" in e)
                warning = example_of(line)
                self.assertEqual(warning["type"], "accessibility", line)
                sc["warnings"] = [warning]
                self.assertEqual([e for e in errs(sc, lang) if e.startswith("warnings:")], [], (b, lang))
                self.assertFalse(has(warns(sc, lang), "characters"), (b, lang, warns(sc, lang)))

    def test_every_criterion_phrase_is_read_as_stated_and_fits_a_warning(self):
        every = list(vsj.A11Y_BASE) + list(vsj.A11Y_MODAL) + list(vsj.A11Y_AUTO_ADVANCE)
        for lang in ("tr", "en"):
            text = vsj.a11y_example(every, lang)
            self.assertLessEqual(len(text), vsj.MAX_TEXT, text)
            for c in every:
                self.assertTrue(c[2].search(text), (lang, c[1]))
                if isinstance(c[2], vsj.FigureCriterion):
                    self.assertIsNone(c[2].below(text), (lang, c[1]))

    def test_missing_criteria_name_the_word_that_asks_for_them(self):
        sc = self.link("Çip klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 48×48 dp ve "
                       "kontrastı en az 4.5:1 olur.", b="Beden çipine dokununca alt sayfa açılır")
        sc["exposure"] = "Ürün sayfasını açan kullanıcı; tetikleyici iki kolda aynı noktada kaydedilir."
        lines = [e for e in errs(sc, "tr") if "ölçüt(ler) yok" in e]
        self.assertEqual(len(lines), 1, lines)
        self.assertIn("('alt sayfa' için)", lines[0])
        self.assertIn("ör. “açılınca odağı alma, görünür bir kapat düğmesi ve Esc ile kapanma”", lines[0])
        sc["warnings"][0]["text"] = sc["warnings"][0]["text"][:-1] + "; açılınca odağı alır, görünür bir kapat " \
                                                                   "düğmesi ve Esc ile kapanır."
        self.assertFalse(has(errs(sc, "tr"), "ölçüt(ler) yok"), errs(sc, "tr"))

    def test_low_touch_target_prints_the_size_to_write(self):
        for stated, fix in (("44×44 dp", "48×48 dp"), ("40×40 pt", "44×44 pt"), ("32 px", "44×44 px")):
            text = ("Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az %s ve kontrastı "
                    "en az 4.5:1 olur." % stated)
            line = next(e for e in errs(self.link(text), "tr") if "eşiğin altında" in e)
            self.assertIn("yerine “%s” yazın" % fix, line)
            self.assertEqual(errs(self.link(text.replace(stated, fix)), "tr"), [], fix)
        text = ("Bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt ve kontrastı "
                "en az 3:1 olur.")
        line = next(e for e in errs(self.link(text), "en") if "below the threshold" in e)
        self.assertIn('write "4.5:1" instead of', line)

    def test_invariants_example_fits_the_element(self):
        for word, want in (("kupon", "Geçerli bir kod"), ("arama", "Aynı arama"), ("sepet", "Sepet tutarı"),
                           ("form", "Alanın doğrulaması"), ("alt sayfa", "Pencere iki kolda"),
                           ("bağlantı", "Öğeye dokunmak")):
            line = next(e for e in errs(with_b(plain(), "B’de %s yeni yerinde" % word), "tr")
                        if e.startswith("invariants:"))
            self.assertIn("“%s" % want, line)
        line = next(e for e in errs(with_b(plain(), "A search box above the list"), "en") if e.startswith("invariants:"))
        self.assertIn('"invariants": ["The same query returns the same results in both arms."]', line)



class TestClaimPatterns(unittest.TestCase):
    """Item 7: the claim shapes the critic kept refusing in evidence notes."""

    def note(self, text, level="archive", **over):
        sc = plain(evidence={"level": level, "note": text}, **over)
        if level == "archive":
            sc = plain(source="adapted", adapted_from="Açık kupon kodu alanı sepet terkini artırır mı?",
                       evidence={"level": level, "note": text})
            sc.pop("source_note")
            sc["priority"]["inputs"]["evidence"] = "archive_or_research"
        return sc

    def test_a_habitual_win_is_a_result_claim(self):
        for text in ("Arşiv örüntüsü: mobil uzun ürün sayfalarında sticky CTA yaygın kazanan bir uygulama.",
                     "Archive pattern: this commonly wins on pricing pages.",
                     "Arşivde genellikle kazanır diye geçen bir fikir.", "A known winner on checkout pages."):
            self.assertTrue(has(errs(self.note(text)), "claims a result"), (text, errs(self.note(text))))

    def test_a_result_stated_as_fact_in_the_note_is_refused(self):
        for text, word in (("Kargo-iade bloğunu fiyatın yakınına taşımak iade kaygısını azaltarak dönüşümü "
                            "iyileştiriyor.", "iyileştiriyor"),
                           ("Kargo bilgisini öne almak siparişi artırır.", "artırır"),
                           ("Bu örüntü dönüşümü artırdı.", "artırdı"),
                           ("Moving delivery info up lifts conversion on product pages.", "lifts")):
            for level in ("archive", "intuition"):
                e = errs(self.note(text, level))
                self.assertTrue(has(e, "'%s' states a result as fact" % word), (text, level, e))

    def test_a_hypothesis_or_a_sourced_study_passes(self):
        for text in ("Arşivde derlenmiş bir fikir: B’nin dönüşümü artırabileceği düşünülüyor, test sonucu değil.",
                     "Arşivde derlenmiş bir test fikrine dayanıyor, bir test sonucu değil.",
                     "A curated archive idea: B may lift conversion; not a test result.",
                     "Teslimat tarihini erken göstermenin kaygıyı azalttığı varsayılıyor."):
            self.assertFalse(has(errs(self.note(text)), "as fact"), (text, errs(self.note(text))))
        sc = self.note("Baymard raporuna göre kargo bilgisini öne almak siparişi artırır.", "sector")
        self.assertFalse(has(errs(sc), "as fact"), errs(sc))
        sc = self.note("Kargo bilgisini öne almak siparişi artırır.", "sector")
        self.assertTrue(has(errs(sc), "as fact"), errs(sc))

    def test_the_users_own_data_states_what_it_observed(self):
        sc = with_b(plain(evidence={"level": "user_data", "note": "GA4 raporuna göre ödeme adımında dönüşüm "
                                                                  "geçen ay düştü."}), "Kısa başlık")
        sc["priority"]["inputs"]["evidence"] = "user_data"
        sc["priority"]["tier"] = "high"
        self.assertFalse(has(errs(sc), "as fact"), errs(sc))


class TestGlossaryNames(unittest.TestCase):
    def test_a_borrowed_abbreviation_is_refused_with_the_names_that_carry_it(self):
        sc = plain(lang="en")
        sc["guardrail"] = {"name": "Subscription Conversion Rate (CR)", "kind": "metric",
                           "denominator": "Visitors assigned to the test", "direction": "must_not_decrease"}
        line = next(e for e in errs(sc) if "abbreviation" in e)
        self.assertIn("'Conversion Rate (CR)' / 'Search Conversion Rate (CR)'", line)
        self.assertNotIn("Dönüşüm", line)
        sc["guardrail"]["name"] = "Subscription Start Rate"
        self.assertFalse(has(errs(sc), "abbreviation"), errs(sc))
        sc["guardrail"]["name"] = "Conversion Rate (CR)"
        self.assertFalse(has(errs(sc), "abbreviation"), errs(sc))

    def test_a_glossary_name_in_the_other_language_warns(self):
        sc = plain()
        sc["guardrail"] = {"name": "Bounce Rate", "kind": "metric", "denominator": "Sayfayla başlayan oturum",
                           "direction": "must_not_increase"}
        self.assertTrue(has(warns(sc, "tr"), "sözlükteki İngilizce adı; kayıt Türkçe yazılır, 'Hemen Çıkma Oranı' "
                                             "yazın"), warns(sc, "tr"))
        sc = plain(lang="en")
        sc["guardrail"] = {"name": "Hemen Çıkma Oranı", "kind": "metric", "denominator": "Sessions starting on the page",
                           "direction": "must_not_increase"}
        self.assertTrue(has(warns(sc), "write 'Bounce Rate'"), warns(sc))
        self.assertTrue(has(warns(sc), "primary_kpi.name: 'Sepete Ekleme Oranı' is the glossary's Turkish name"))
        sc["guardrail"]["name"] = "Bounce Rate"
        self.assertFalse(has(warns(sc), "guardrail.name"), warns(sc))
        self.assertEqual(warns(plain()), [])


class TestMustBeTrue(unittest.TestCase):
    BELIEF = {"belief": "Kullanıcılar teslimat tarihini ödemeden önce görmek istiyor.",
              "probe": "Ödeme adımının oturum kayıtlarında teslimat bilgisine geri dönüşleri sayın."}

    def test_optional_and_valid(self):
        self.assertEqual(errs(plain()), [])
        sc = plain(must_be_true=dict(self.BELIEF))
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])
        self.assertNotEqual(vsj.record_fingerprint(sc), vsj.record_fingerprint(plain()))

    def test_shape_length_and_claims(self):
        self.assertTrue(has(errs(plain(must_be_true={"belief": "x"})), "missing required field 'probe'"))
        self.assertTrue(has(errs(plain(must_be_true=dict(self.BELIEF, extra=1))), "unknown field 'extra'"))
        long = dict(self.BELIEF, belief="Kullanıcılar " + "teslimat tarihini görmek ister " * 6 + "der.")
        self.assertTrue(has(errs(plain(must_be_true=long), "tr"), "en fazla 160 karakterlik"), errs(plain(
            must_be_true=long), "tr"))
        claim = dict(self.BELIEF, belief="B siparişi %12 artırır.")
        self.assertTrue(has(errs(plain(must_be_true=claim)), "must_be_true.belief"), errs(plain(must_be_true=claim)))
        stats = dict(self.BELIEF, probe="Örneklem büyüklüğü 400 olan bir anket yapın.")
        self.assertTrue(has(errs(plain(must_be_true=stats)), "must_be_true.probe"), errs(plain(must_be_true=stats)))
        two = dict(self.BELIEF, probe="Kayıtlara bakın. Sonra beş kullanıcıyla konuşun.")
        self.assertTrue(has(warns(plain(must_be_true=two)), "must_be_true.probe: 2 sentences"))



def run_chat(records, *flags):
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for i, sc in enumerate(records):
            path = os.path.join(tmp, "r%d.json" % i)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(sc, fh, ensure_ascii=False)
            paths.append(path)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = vsj.main(["--chat"] + list(flags) + paths)
        return code, out.getvalue(), err.getvalue()


class TestChat(unittest.TestCase):
    """Item 7: the chat lines that are a function of the record are printed, not hand-written."""

    def test_one_record(self):
        code, out, err = run_chat([plain()])
        self.assertEqual(code, 0, err)
        lines = out.splitlines()
        self.assertEqual(lines[0], "**1. Kısa ürün başlığı sepete eklemeyi artırır mı?**")
        self.assertEqual(lines[1], "Öncelik: Orta (5/9) · Kaynak: bu sayfa için üretildi · Kanıt: sezgi")
        self.assertEqual(lines[2], "Neden: " + plain()["mechanism"])
        self.assertIn("Başlamadan önce: yok.", lines)
        self.assertNotIn("Koşullu", out)
        with open(vsj.BRIEF_TEMPLATE, encoding="utf-8") as fh:
            template = fh.read()
        self.assertIn("**Karar özeti: 1. senaryo**", lines)
        for line in lines[lines.index("**Karar özeti: 1. senaryo**") + 2:]:
            self.assertIn(line, template)  # the three outcome lines, word for word
        self.assertEqual(err, "")

    def test_gates_conditions_and_labels_follow_the_records(self):
        first = with_b(plain(), "Başlığın altında “Tüm özellikler” bağlantısı")
        first["invariants"] = ["Bağlantı iki kolda da aynı sayfayı açar."]
        first["warnings"] = [{"type": "accessibility", "text": vsj.a11y_example(list(vsj.A11Y_BASE))},
                             REGULATION]
        first["assumptions"] = [{"type": "critical", "text": "Bağlantının açtığı sayfanın hazır olduğu varsayılıyor.",
                                 "question": "Özellikler sayfası hazır mı?"},
                                {"type": "visual", "text": "Ürün adı temsilîdir."}]
        second = plain(evidence={"level": "sector", "note": "Sektör raporlarında sık görülen bir gözlem."})
        second["priority"]["inputs"]["evidence"] = "archive_or_research"
        code, out, err = run_chat([first, second])
        self.assertEqual(code, 0, err)
        self.assertIn("Kanıt: sektör gözlemi", out)
        self.assertIn("Koşullu (1): 1: Bağlantının açtığı sayfanın hazır olduğu varsayılıyor.", out)
        self.assertNotIn("temsilî", out)
        self.assertIn("Başlamadan önce: 1 için B’nin metnine uyum onayı ve erişilebilirlik kontrolü.", out)
        self.assertIn("**2. ", out)
        self.assertEqual(out.count("Karar özeti"), 1)

    def test_english_labels_long_mechanism_and_must_be_true(self):
        sc = plain(lang="en", evidence={"level": "sector", "note": "A common industry observation."},
                   mechanism="A short title names the product at first glance, " * 4 + "so users decide sooner.",
                   must_be_true={"belief": "Users skim titles before reading the price.",
                                 "probe": "Watch ten session recordings of the product page."})
        sc["priority"]["inputs"]["evidence"] = "archive_or_research"
        code, out, err = run_chat([sc])
        self.assertEqual(code, 0, err)
        self.assertIn("Priority: Medium (6/9) · Source: generated for this page · Evidence: industry observation", out)
        self.assertNotIn("Why:", out)
        self.assertIn("the Why line is at most 140", err)
        self.assertIn("Must be true: Users skim titles before reading the price.", out)
        self.assertIn("Probe first: Watch ten session recordings of the product page.", out)
        self.assertIn("Pre-start gates: none.", out)
        self.assertIn("**Stakeholder brief: scenario 1**", out)
        self.assertIn("Why now: A common industry observation.", out)

    def test_an_invalid_record_prints_nothing(self):
        sc = plain()
        sc["priority"]["tier"] = "high"
        code, out, err = run_chat([plain(), sc])
        self.assertEqual((code, out), (1, ""))
        self.assertIn("priority.tier", err)


if __name__ == "__main__":
    unittest.main()
