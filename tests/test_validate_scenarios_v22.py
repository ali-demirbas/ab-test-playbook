#!/usr/bin/env python3
"""validate_scenarios.py v2.2 denetimleri için unit testler. Bağımlılıksız.

Kapsam: tümleyen guardrail uyarısı, değişken yalıtımı maddesi olmayan senaryo,
“Sadece … bakıp … atlamayın” genel hijyen kalıbı, birincil dışındaki KPI
satırlarında sayı/gören uyarısı, başlık + Değişken benzerliği ve dosya argümanı.
"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import validate_scenarios as vs  # noqa: E402
from test_validate_scenarios import make_scenario, make_kpis, first  # noqa: E402


def warn(text, glossary=None):
    title, body = first(text)
    return vs.check_warnings("test.md", title, body, glossary=glossary)


def errors(text):
    title, body = first(text)
    return vs.check_scenario("test.md", title, body)


class TestComplementGuardrail(unittest.TestCase):
    def kpis(self, primary, guardrail):
        return [primary, make_kpis()[1], guardrail] + make_kpis()[3:]

    def test_page_abandonment_against_completion_warns(self):
        k = self.kpis("- Form Tamamlama Oranı: Formu gönderenlerin payı artıyor mu?",
                      "- Sayfa Terk Oranı: Sayfadan ayrılma belirgin şekilde artmamalı.")
        self.assertTrue(any("tümleyeni" in w for w in warn(make_scenario(kpis=k))), warn(make_scenario(kpis=k)))

    def test_generic_abandonment_against_conversion_warns(self):
        k = self.kpis("- Dönüşüm Oranı (CR): Satın alma oranı artıyor mu bu testte?",
                      "- Terk Oranı: Terk belirgin şekilde artmamalı bu testte.")
        self.assertTrue(any("tümleyeni" in w for w in warn(make_scenario(kpis=k))))

    def test_later_step_abandonment_is_a_valid_guardrail(self):
        k = self.kpis("- Kayıt Oranı: Hesap oluşturanların payı artıyor mu burada?",
                      "- Ödeme Adımı Terk Oranı: Ödeme adımında terk artmamalı.")
        self.assertEqual([w for w in warn(make_scenario(kpis=k)) if "tümleyeni" in w], [])

    def test_abandonment_as_a_goal_line_is_not_a_guardrail(self):
        k = self.kpis("- Form Tamamlama Oranı: Formu gönderenlerin payı artıyor mu?",
                      "- Sayfa Terk Oranı: Sayfadan ayrılma azalıyor mu bu testte?")
        self.assertEqual([w for w in warn(make_scenario(kpis=k)) if "tümleyeni" in w], [])

    def test_unrelated_primary_does_not_warn(self):
        k = self.kpis("- Ziyaretçi Başına Gelir (RPV): Gelir artıyor mu bu testte?",
                      "- Sayfa Terk Oranı: Sayfadan ayrılma belirgin şekilde artmamalı.")
        self.assertEqual([w for w in warn(make_scenario(kpis=k)) if "tümleyeni" in w], [])


class TestVariableIsolationItem(unittest.TestCase):
    PLAIN = [
        "- Yeni rengi marka paletinin dışından seçip kontrastı düşürmeyin.",
        "- Tek segmentte ölçüp tüm kullanıcılara genellemeyin bunu.",
        "- Guardrail metriklerini görmezden gelip karar vermeyin asla.",
        "- Butonu ekranın altına iterek görünmez hâle getirmeyin sakın.",
    ]

    def test_scenario_without_isolation_item_warns(self):
        d = self.PLAIN + ["- Kontrastı erişilebilirlik sınırının altına düşürmeyin."]
        self.assertTrue(any("değişken yalıtımı" in w for w in warn(make_scenario(donts=d))))

    def test_isolation_family(self):
        for item in ("- Aynı testte buton metnini de yeniden yazmayın lütfen.",
                     "- Rengi ve metni aynı anda değiştirmeyin bu testte.",
                     "- Renkle birlikte butonun boyutunu ve yerini değiştirmeyin.",
                     "- Bu testte tek değişken renk olmalı, başka bir şey oynamamalı."):
            d = self.PLAIN + [item]
            self.assertEqual([w for w in warn(make_scenario(donts=d)) if "değişken yalıtımı" in w], [], item)

    def test_it_is_a_warning_not_an_error(self):
        d = self.PLAIN + ["- Kontrastı erişilebilirlik sınırının altına düşürmeyin."]
        self.assertEqual(errors(make_scenario(donts=d)), [])


class TestGenericHygienePattern(unittest.TestCase):
    def donts(self, item):
        return ["- Aynı testte iki değişkeni birlikte değiştirmeyin sakın.",
                "- Yeni rengi marka paletinin dışından seçip kontrastı düşürmeyin.",
                "- Tek segmentte ölçüp tüm kullanıcılara genellemeyin bunu.",
                "- Renk değişirken buton metnini de yeniden yazmayın lütfen.", item]

    def test_sadece_bakip_atlamayin_is_forbidden(self):
        for item in ("- Sadece dönüşüm oranına bakıp iade oranını atlamayın.",
                     "- Sadece tıklamaya bakıp sipariş tamamlamayı ve geliri atlamayın.",
                     "- Yalnızca kayıt sayısına bakıp nitelikli fırsat oranını atlamayın."):
            e = errors(make_scenario(donts=self.donts(item)))
            self.assertTrue(any("genel kural" in x for x in e), (item, e))

    def test_variant_specific_atlamayin_is_fine(self):
        for item in ("- Eşiğe ulaşıldığında geri bildirim vermeyi atlamayın.",
                     "- Vurguyu yalnızca renkle yapıp kontrast ve biçim farkını atlamayın."):
            self.assertEqual(errors(make_scenario(donts=self.donts(item))), [], item)


class TestCountAndSawOnEveryLine(unittest.TestCase):
    def test_count_in_secondary_warns(self):
        k = make_kpis()[:4] + ["- Destek Talebi Sayısı: Fiyatla ilgili talep artmamalı bu testte."]
        w = warn(make_scenario(kpis=k))
        self.assertTrue(any("Destek Talebi Sayısı" in x and "Sayısı" in x for x in w), w)
        self.assertFalse(any("birincil KPI" in x for x in w), w)

    def test_count_per_visitor_does_not_warn(self):
        k = make_kpis()[:4] + ["- Ziyaretçi Başına Destek Talebi Sayısı: Talep artmamalı bu testte."]
        self.assertEqual(warn(make_scenario(kpis=k)), [])

    def test_saw_denominator_in_guardrail_label_warns(self):
        k = make_kpis()[:4] + ["- Butonu Gören Kullanıcı Başına İade Oranı: İade belirgin şekilde artmamalı."]
        self.assertTrue(any("gören/görüp" in x for x in warn(make_scenario(kpis=k))))

    def test_saw_in_the_question_text_of_another_line_is_ignored(self):
        k = make_kpis()[:4] + ["- İlk Adım Terk Oranı: Süreci görüp vazgeçme belirgin şekilde artmamalı."]
        self.assertEqual(warn(make_scenario(kpis=k)), [])

    def test_b_only_line_never_warns(self):
        k = make_kpis()[:4] + ["- Yeni Butonu Gören Kullanıcı Sayısı (yalnız B): Tanı amaçlı, artmamalı diye okunmaz ama düşmemeli."]
        self.assertEqual(warn(make_scenario(kpis=k)), [])

    def test_glossary_name_inherits_its_denominator(self):
        k = make_kpis()[:4] + ["- Görülen Ürün Sayısı: Kullanıcının gördüğü ürün sayısı düşmemeli."]
        self.assertTrue(warn(make_scenario(kpis=k)))
        self.assertEqual(warn(make_scenario(kpis=k), glossary={"Görülen Ürün Sayısı": []}), [])

    def test_primary_count_still_warns_with_a_glossary(self):
        k = ["- Nitelikli Fırsat Sayısı (SQL): Satışa uygun talep artıyor mu?"] + make_kpis()[1:]
        w = warn(make_scenario(kpis=k), glossary={"Nitelikli Fırsat Sayısı (SQL)": []})
        self.assertTrue(any("birincil KPI bir sayı" in x for x in w), w)


class TestTitleVariableNearDuplicates(unittest.TestCase):
    def sc(self, name, title, variable):
        return (name,) + first(make_scenario(title, variable_line="Değişken: %s · Fark: değiştir" % variable))

    def test_same_title_and_variable_across_files_warns(self):
        a = self.sc("cart-checkout.md", "Form alan sayısını azaltmak tamamlamayı artırır mı?", "Formdaki alan sayısı")
        b = self.sc("saas-b2b.md", "Form alan sayısını azaltmak talebi artırır mı?", "Formdaki alan sayısı")
        w, infos = vs.find_title_variable_duplicates([a, b])
        self.assertEqual(len(w), 1, w)
        self.assertIn("cart-checkout.md", w[0])
        self.assertIn("saas-b2b.md", w[0])
        self.assertEqual(infos, [])

    def test_different_scenarios_do_not_warn(self):
        a = self.sc("cart-checkout.md", "Kupon alanını gizlemek geliri artırır mı?", "Kupon alanının görünürlüğü")
        b = self.sc("saas-b2b.md", "Demo talep formunda telefon alanı gerekli mi?", "Telefon alanının zorunluluğu")
        self.assertEqual(vs.find_title_variable_duplicates([a, b]), ([], []))

    def test_pair_with_a_fark_reference_is_information(self):
        a = (("cart-checkout.md",) + first(make_scenario(
            "Form alan sayısını azaltmak tamamlamayı artırır mı?",
            variable_line="Değişken: Formdaki alan sayısı · Fark: değiştir",
            intro="Bu senaryonun “Form alan sayısını azaltmak talebi artırır mı?” senaryosundan farkı: adres formu.")))
        b = self.sc("saas-b2b.md", "Form alan sayısını azaltmak talebi artırır mı?", "Formdaki alan sayısı")
        w, infos = vs.find_title_variable_duplicates([a, b])
        self.assertEqual(w, [])
        self.assertEqual(len(infos), 1)


class TestCli(unittest.TestCase):
    def run_main(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = vs.main(list(argv))
        return code, out.getvalue()

    def test_archive_passes_and_prints_the_warning_count(self):
        code, out = self.run_main()
        self.assertEqual(code, 0, out[-1500:])
        self.assertRegex(out, r"Uyarı sayısı: \d+")

    def test_single_file_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = os.path.join(tmp, "mine.md")
            with open(good, "w", encoding="utf-8") as fh:
                fh.write(make_scenario())
            code, out = self.run_main(good)
            self.assertEqual(code, 0, out)
            self.assertIn("mine.md: 1", out)
            self.assertIn("TOPLAM: 1", out)
            bad = os.path.join(tmp, "bad.md")
            with open(bad, "w", encoding="utf-8") as fh:
                fh.write(make_scenario("Soru işareti olmayan başlık"))
            code, out = self.run_main(bad)
            self.assertEqual(code, 1, out)
            self.assertIn("soru işaretiyle bitmiyor", out)

    def test_missing_file_argument(self):
        code, out = self.run_main("/nonexistent/x.md")
        self.assertEqual(code, 1)
        self.assertIn("bulunamadı", out)


if __name__ == "__main__":
    unittest.main()
