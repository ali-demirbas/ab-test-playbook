#!/usr/bin/env python3
"""validate_scenario_json.py, 3.4: the regulated-flow reading (item 35), refusal messages that carry the
corrected value (item 8) and the mechanical checks moved over from scenario-critic (item 7). Stdlib only.
"""
import json
import os
import re
import sys
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


if __name__ == "__main__":
    unittest.main()
