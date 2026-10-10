#!/usr/bin/env python3
"""validate_scenarios.py için unit testler. Bağımlılıksız (unittest).

Bu testler doğrulayıcının bilinen kör noktalarına karşı regresyon korumasıdır:
dosya başındaki senaryonun yutulması, sıfır senaryolu dosyanın temiz sayılması,
mükerrer kutu başlığı, sahte guardrail kalıbı ve doldurma maddeleri; ayrıca
Değişken satırı, guardrail gibi yazılmış birincil KPI, payda uyarıları, genel
hijyen kalıpları, arşiv genelinde tekrar eden madde, senaryo atıfları, neredeyse
aynı senaryolar ve KPI sözlüğü.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from validate_scenarios import (  # noqa: E402
    parse_scenarios, check_scenario, check_warnings, box_items, parse_variable_line,
    extract_cross_refs, find_unresolved_cross_refs, normalize_title,
    find_duplicate_never_do, find_near_duplicates, parse_glossary, glossary_status,
    MAX_VARIABLE_CHARS,
)

DEFAULT_VARIABLE = "Değişken: Buton rengi · Fark: değiştir"


def make_scenario(title="Geçerli bir senaryo başlığı mı?",
                  tests=None, kpis=None, donts=None, variable_line=DEFAULT_VARIABLE,
                  intro="Açıklama paragrafı burada yeterince uzun duruyor."):
    tests = tests or [
        "- Konum: Öğenin konumu dönüşümü değiştiriyor mu?",
        "- Metin: Hangi ifade daha çok tıklanıyor peki?",
        "- Boyut: Daha büyük olması fark yaratıyor mu acaba?",
        "- Sıra: Sıralama değişince davranış değişiyor mu?",
        "- Cihaz: Mobilde ve masaüstünde aynı sonuç mu çıkıyor?",
    ]
    kpis = kpis or [
        "- Dönüşüm Oranı: Değişiklik satın almayı artırıyor mu burada?",
        "- Tıklama Oranı: Butona tıklama oranı yükseliyor mu acaba?",
        "- Sepet Tutarı: Ortalama sepet tutarı düşmemeli bu testte.",
        "- Sayfa Süresi: Sayfada geçirilen süre uzuyor mu dersin?",
        "- Hata Oranı: Yanlış tıklama oranı belirgin şekilde artmamalı.",
    ]
    donts = donts or [
        "- Aynı testte iki değişkeni birlikte değiştirmeyin sakın.",
        "- Yeni rengi marka paletinin dışından seçip kontrastı düşürmeyin.",
        "- Tek segmentte ölçüp tüm kullanıcılara genellemeyin bunu.",
        "- Guardrail metriklerini görmezden gelip karar vermeyin asla.",
        "- Renk değişirken buton metnini de yeniden yazmayın lütfen.",
    ]
    head = f"## {title}\n\n"
    if variable_line:
        head += variable_line + "\n\n"
    return (head + intro + "\n\n"
            "**Test edilmesi gerekenler**\n" + "\n".join(tests) + "\n\n"
            "**Takip edilecek ana KPI’lar**\n" + "\n".join(kpis) + "\n\n"
            "**Yapılmaması gerekenler**\n" + "\n".join(donts) + "\n")


def first(text):
    return parse_scenarios(text)[0]


class TestParseScenarios(unittest.TestCase):
    def test_file_starting_with_heading_keeps_first_scenario(self):
        """Regresyon: '\\n## ' split'i dosya başındaki senaryoyu yutuyordu."""
        text = make_scenario("İlk senaryo yutulmuyor mu?") + "\n" + make_scenario("İkinci senaryo mu?")
        self.assertEqual(len(parse_scenarios(text)), 2)

    def test_no_heading_yields_zero(self):
        self.assertEqual(parse_scenarios("### Yanlış seviye\n\ngövde\n"), [])

    def test_trailing_item_without_newline_counts(self):
        """Regresyon: dosya sonunda newline yoksa son madde sayılmıyordu."""
        text = make_scenario().rstrip("\n")
        title, body = first(text)
        self.assertEqual(len(box_items(body, "Yapılmaması gerekenler")), 5)


class TestCheckScenario(unittest.TestCase):
    def check(self, text):
        title, body = first(text)
        return check_scenario("test.md", title, body)

    def test_valid_scenario_passes(self):
        self.assertEqual(self.check(make_scenario()), [])

    def test_title_without_question_mark_fails(self):
        errs = self.check(make_scenario(title="Soru işareti yok"))
        self.assertTrue(any("soru işaretiyle bitmiyor" in e for e in errs))

    def test_four_items_fail(self):
        s = make_scenario()
        s = s.replace("- Renk değişirken buton metnini de yeniden yazmayın lütfen.\n", "")
        errs = self.check(s)
        self.assertTrue(any("4 madde" in e for e in errs))

    def test_duplicate_items_fail(self):
        dup = ["- Aynı testte iki değişkeni birlikte değiştirmeyin sakın."] * 5
        errs = self.check(make_scenario(donts=dup))
        self.assertTrue(any("tekrar eden madde" in e for e in errs))

    def test_short_filler_item_fails(self):
        donts = [
            "- Genel",
            "- Aynı testte iki değişkeni birlikte değiştirmeyin sakın.",
            "- Yeni rengi marka paletinin dışından seçip kontrastı düşürmeyin.",
            "- Tek segmentte ölçüp tüm kullanıcılara genellemeyin bunu.",
            "- Guardrail metriklerini görmezden gelip karar vermeyin asla.",
        ]
        errs = self.check(make_scenario(donts=donts))
        self.assertTrue(any("doldurma gibi" in e for e in errs))

    def test_positive_goal_is_not_guardrail(self):
        """'…kalmalıdır' hedef cümlesi guardrail sayılmamalı."""
        kpis = [
            "- Dönüşüm Oranı: Değişiklik satın almayı artırıyor mu burada?",
            "- Müşteri Memnuniyeti: Müşteri her zaman memnun kalmalıdır bence.",
            "- Tıklama Oranı: Butona tıklama oranı yükseliyor mu acaba?",
            "- Sepet Tutarı: Ortalama sepet tutarı artıyor mu bu testte?",
            "- Sayfa Süresi: Sayfada geçirilen süre uzuyor mu dersin?",
        ]
        errs = self.check(make_scenario(kpis=kpis))
        self.assertTrue(any("guardrail yok" in e for e in errs))

    def test_test_item_without_question_fails(self):
        tests = [
            "- A: olur",
            "- Metin: Hangi ifade daha çok tıklanıyor peki?",
            "- Boyut: Daha büyük olması fark yaratıyor mu acaba?",
            "- Sıra: Sıralama değişince davranış değişiyor mu?",
            "- Cihaz: Mobilde ve masaüstünde aynı sonuç mu çıkıyor?",
        ]
        errs = self.check(make_scenario(tests=tests))
        self.assertTrue(any("biçiminde değil" in e for e in errs))

    def test_question_with_trailing_options_passes(self):
        """'Soru? (2 / 4 / 6)' biçimi geçerli sayılmalı."""
        tests = [
            "- Sayı: Öneri sayısı kaç olmalı? (2 / 4 / 6)",
            "- Metin: Hangi ifade daha çok tıklanıyor peki?",
            "- Boyut: Daha büyük olması fark yaratıyor mu acaba?",
            "- Sıra: Sıralama değişince davranış değişiyor mu?",
            "- Cihaz: Mobilde ve masaüstünde aynı sonuç mu çıkıyor?",
        ]
        self.assertEqual(self.check(make_scenario(tests=tests)), [])

    def test_sonraki_test_label_is_valid_item(self):
        """'Sonraki test: …?' etiketi geçerli bir test maddesidir."""
        tests = [
            "- Sonraki test: Kazanan renk sabitken konum ayrı testte fark yaratıyor mu?",
            "- Metin: Hangi ifade daha çok tıklanıyor peki?",
            "- Boyut: Daha büyük olması fark yaratıyor mu acaba?",
            "- Sıra: Sıralama değişince davranış değişiyor mu?",
            "- Cihaz: Mobilde ve masaüstünde aynı sonuç mu çıkıyor?",
        ]
        self.assertEqual(self.check(make_scenario(tests=tests)), [])


class TestVariableLine(unittest.TestCase):
    def check(self, text):
        title, body = first(text)
        return check_scenario("test.md", title, body)

    def test_parsed(self):
        _, body = first(make_scenario(variable_line="Değişken: Kupon alanının görünürlüğü · Fark: kaldır"))
        var, fark, errs = parse_variable_line(body)
        self.assertEqual((var, fark, errs), ("Kupon alanının görünürlüğü", "kaldır", []))

    def test_all_four_fark_values_pass(self):
        for fark in ("değiştir", "ekle", "taşı", "kaldır"):
            s = make_scenario(variable_line=f"Değişken: Buton rengi · Fark: {fark}")
            self.assertEqual(self.check(s), [], fark)

    def test_missing_line_fails(self):
        errs = self.check(make_scenario(variable_line=None))
        self.assertTrue(any("satırı yok" in e for e in errs))

    def test_unknown_fark_fails(self):
        errs = self.check(make_scenario(variable_line="Değişken: Buton rengi · Fark: değiştirme"))
        self.assertTrue(any("geçersiz" in e for e in errs))

    def test_english_fark_fails(self):
        errs = self.check(make_scenario(variable_line="Değişken: Buton rengi · Fark: change"))
        self.assertTrue(any("geçersiz" in e for e in errs))

    def test_empty_variable_fails(self):
        errs = self.check(make_scenario(variable_line="Değişken:  · Fark: ekle"))
        self.assertTrue(any("Değişken boş" in e for e in errs))

    def test_too_long_variable_fails(self):
        long_var = "Ç" * (MAX_VARIABLE_CHARS + 1)
        errs = self.check(make_scenario(variable_line=f"Değişken: {long_var} · Fark: ekle"))
        self.assertTrue(any("karakter" in e for e in errs))

    def test_exactly_max_length_passes(self):
        var = "Ç" * MAX_VARIABLE_CHARS
        self.assertEqual(self.check(make_scenario(variable_line=f"Değişken: {var} · Fark: ekle")), [])

    def test_missing_separator_fails(self):
        errs = self.check(make_scenario(variable_line="Değişken: Buton rengi - Fark: ekle"))
        self.assertTrue(any("biçiminde değil" in e for e in errs))

    def test_line_below_intro_fails(self):
        s = make_scenario(variable_line=None, intro="Açıklama paragrafı burada.\n\n" + DEFAULT_VARIABLE)
        errs = self.check(s)
        self.assertTrue(any("hemen altında değil" in e for e in errs))

    def test_two_lines_fail(self):
        s = make_scenario(variable_line=DEFAULT_VARIABLE + "\n" + DEFAULT_VARIABLE)
        errs = self.check(s)
        self.assertTrue(any("tam bir tane" in e for e in errs))


class TestWarnings(unittest.TestCase):
    def warn(self, text):
        title, body = first(text)
        return check_warnings("test.md", title, body)

    def test_clean_scenario_has_no_warnings(self):
        self.assertEqual(self.warn(make_scenario()), [])

    def test_ve_in_variable_warns(self):
        s = make_scenario(variable_line="Değişken: Buton rengi ve metni · Fark: değiştir")
        self.assertTrue(any("iki değişken" in w for w in self.warn(s)))

    def test_slash_in_variable_warns(self):
        s = make_scenario(variable_line="Değişken: Renk/boyut · Fark: değiştir")
        self.assertTrue(any("iki değişken" in w for w in self.warn(s)))

    def test_ve_inside_word_does_not_warn(self):
        """'Güvence' içindeki 've' bir bağlaç değildir."""
        s = make_scenario(variable_line="Değişken: Güvence rozetinin varlığı · Fark: ekle")
        self.assertEqual(self.warn(s), [])

    def test_two_variables_is_warning_not_error(self):
        s = make_scenario(variable_line="Değişken: Buton rengi ve metni · Fark: değiştir")
        title, body = first(s)
        self.assertEqual(check_scenario("test.md", title, body), [])

    def test_count_primary_warns(self):
        kpis = ["- Nitelikli Fırsat Sayısı (SQL): Satışa uygun talep artıyor mu?"] + make_kpis()[1:]
        self.assertTrue(any("Sayısı" in w for w in self.warn(make_scenario(kpis=kpis))))

    def test_saw_denominator_primary_warns(self):
        kpis = ["- Kurtarma Oranı: Pop-up görüp oturuma devam eden kullanıcı oranı."] + make_kpis()[1:]
        self.assertTrue(any("gören/görüp" in w for w in self.warn(make_scenario(kpis=kpis))))

    def test_saw_suffix_form_warns(self):
        kpis = ["- Yükseltme Oranı: Modalı görenlerin ödemeye geçme oranı artıyor mu?"] + make_kpis()[1:]
        self.assertTrue(any("gören/görüp" in w for w in self.warn(make_scenario(kpis=kpis))))

    def test_count_in_secondary_kpi_warns_too(self):
        # Payda kuralı her KPI satırı içindir; birincil dışındaki satır da uyarı alır
        # (ayrıntılı durumlar: test_validate_scenarios_v22.py).
        kpis = make_kpis()[:4] + ["- Destek Talebi Sayısı: Fiyatla ilgili talep artmamalı bu testte."]
        warnings = self.warn(make_scenario(kpis=kpis))
        self.assertEqual(len(warnings), 1, warnings)
        self.assertIn("Destek Talebi Sayısı", warnings[0])


def make_kpis():
    return [
        "- Dönüşüm Oranı: Değişiklik satın almayı artırıyor mu burada?",
        "- Tıklama Oranı: Butona tıklama oranı yükseliyor mu acaba?",
        "- Sepet Tutarı: Ortalama sepet tutarı düşmemeli bu testte.",
        "- Sayfa Süresi: Sayfada geçirilen süre uzuyor mu dersin?",
        "- Hata Oranı: Yanlış tıklama oranı belirgin şekilde artmamalı.",
    ]


class TestPrimaryNotGuardrail(unittest.TestCase):
    def check(self, kpis):
        title, body = first(make_scenario(kpis=kpis))
        return check_scenario("test.md", title, body)

    def test_guardrail_phrased_primary_fails(self):
        kpis = ["- Ziyaretçi Başına Gelir (RPV): Kod CR’yi artırsa bile geliri düşürmemeli."] + make_kpis()[1:]
        self.assertTrue(any("birincil KPI guardrail gibi" in e for e in self.check(kpis)))

    def test_directional_primary_passes(self):
        kpis = ["- Ziyaretçi Başına Gelir (RPV): Kod ziyaretçi başına geliri artırıyor mu?"] + make_kpis()[1:]
        self.assertEqual(self.check(kpis), [])


class TestNeverDo(unittest.TestCase):
    def check(self, donts):
        title, body = first(make_scenario(donts=donts))
        return check_scenario("test.md", title, body)

    def base(self):
        return [
            "- Aynı testte iki değişkeni birlikte değiştirmeyin sakın.",
            "- Yeni rengi marka paletinin dışından seçip kontrastı düşürmeyin.",
            "- Tek segmentte ölçüp tüm kullanıcılara genellemeyin bunu.",
            "- Guardrail metriklerini görmezden gelip karar vermeyin asla.",
        ]

    def test_generic_freeze_rule_fails(self):
        errs = self.check(self.base() + ["- Test sırasında rengi, konumu ve boyutu birlikte değiştirmeyin."])
        self.assertTrue(any("genel kural" in e for e in errs))

    def test_generic_test_suresince_fails(self):
        errs = self.check(self.base() + ["- Test süresince gerçek fiyatı değiştirmeyin lütfen."])
        self.assertTrue(any("genel kural" in e for e in errs))

    def test_sik_sik_fails(self):
        errs = self.check(self.base() + ["- Buton metnini testler arasında sık sık değiştirmeyin."])
        self.assertTrue(any("genel kural" in e for e in errs))

    def test_sample_rule_fails(self):
        errs = self.check(self.base() + ["- Sonuçları örneklem dolmadan yorumlamayın hiçbir zaman."])
        self.assertTrue(any("genel kural" in e for e in errs))

    def test_test_sirasinda_mid_sentence_is_variant_scoped(self):
        """Cümle içindeki 'test sırasında' varyanta özgü bir uyarı olabilir."""
        errs = self.check(self.base() + ["- Orta planın içeriğini test sırasında zenginleştirmeyin; tek değişken üçüncü seçenektir."])
        self.assertEqual(errs, [])

    def test_duplicate_across_archive_fails(self):
        a = first(make_scenario("Birinci senaryo mu?"))
        donts = self.base() + ["- Renk değişirken buton metnini de yeniden yazmayın lütfen."]
        b = first(make_scenario("İkinci senaryo mu?", donts=donts))
        problems = find_duplicate_never_do([("a.md",) + a, ("b.md",) + b])
        self.assertTrue(problems)
        self.assertTrue(any("birebir aynı" in p for p in problems))

    def test_unique_across_archive_passes(self):
        a = first(make_scenario("Birinci senaryo mu?"))
        # base() maddeleri make_scenario varsayılanlarıyla aynı; tamamen farklı bir set kullan.
        b_donts = [
            "- Fiyat kartında çizili fiyatı aynı anda büyütmeyin lütfen.",
            "- Rozeti eklerken kart başlığını da kısaltmayın bu testte.",
            "- Rozeti stok verisine dayanmadan göstermeyin hiçbir zaman.",
            "- Rozeti kapatılamaz bir katman olarak eklemeyin kesinlikle.",
            "- Rozet metnini yalnızca mobilde farklı yazmayın bu testte.",
        ]
        b = first(make_scenario("İkinci senaryo mu?", donts=b_donts))
        self.assertEqual(find_duplicate_never_do([("a.md",) + a, ("b.md",) + b]), [])


class TestCrossRefs(unittest.TestCase):
    def test_simple_reference_extracted(self):
        text = "Bu “Taksit bilgisi satın almayı etkiliyor mu?” senaryosundan farkı: burada çerçeve değişir."
        self.assertEqual(extract_cross_refs(text), [("Taksit bilgisi satın almayı etkiliyor mu?", 1, True)])

    def test_earlier_quote_on_same_line_not_swallowed(self):
        """Regresyon: aynı satırda önce gelen “aylık 2.000 TL” alıntısı başlığa karışmamalı."""
        text = ("Üründe “aylık 2.000 TL” ifadesi erişilebilir algılanır. “Taksit bilgisi satın almayı "
                "etkiliyor mu?” senaryosundan farkı: burada çerçeve test edilir.")
        refs = extract_cross_refs(text)
        self.assertEqual([r[0] for r in refs], ["Taksit bilgisi satın almayı etkiliyor mu?"])

    def test_nested_quotes_in_title(self):
        text = "“Stokta olmayan ürünü gizlemek mi, “haber ver” demek mi?” senaryosundan farkı: burada liste."
        refs = extract_cross_refs(text)
        self.assertEqual(refs[0][0], "Stokta olmayan ürünü gizlemek mi, “haber ver” demek mi?")

    def test_file_name_between_quote_and_senaryo(self):
        text = "“Pop-up ne zaman gösterilmeli?” (`category-listing.md`) senaryosundan farkı: tetik."
        self.assertEqual(extract_cross_refs(text)[0][0], "Pop-up ne zaman gösterilmeli?")

    def test_plural_reference_extracts_both(self):
        text = "“Birinci başlık mı?” ve “İkinci başlık mı?” (product-detail.md) senaryolarından farkı: rozet."
        self.assertEqual([r[0] for r in extract_cross_refs(text)], ["İkinci başlık mı?", "Birinci başlık mı?"])

    def test_nested_quote_style_normalized(self):
        """‘Satın Al’ ile “Satın Al” aynı başlığa çözülmeli."""
        self.assertEqual(normalize_title("Sticky ‘Satın Al’ butonu dönüşümü artırıyor mu?"),
                         normalize_title("Sticky “Satın Al” butonu dönüşümü artırıyor mu?"))
        text = "“Sticky ‘Satın Al’ butonu dönüşümü artırıyor mu?” senaryosundan farkı: konum."
        self.assertEqual(find_unresolved_cross_refs([("x.md", text)],
                                                    ["Sticky “Satın Al” butonu dönüşümü artırıyor mu?"]), [])

    def test_unresolved_reference_fails(self):
        text = "Bu “Aylık taksit tutarını ana fiyat gibi göstermek” senaryosunun değişkenidir."
        problems = find_unresolved_cross_refs([("x.md", text)],
                                              ["Aylık taksit tutarını ana fiyat gibi göstermek işe yarar mı?"])
        self.assertEqual(len(problems), 1)
        self.assertIn("x.md:1", problems[0])

    def test_quote_not_followed_by_senaryo_ignored(self):
        text = "Butonun “Satın Al” metni sabit kalır; bu senaryo yalnızca rengi değiştirir."
        self.assertEqual(extract_cross_refs(text), [])


class TestNearDuplicates(unittest.TestCase):
    def pair(self, intro_a="Açıklama paragrafı burada yeterince uzun duruyor."):
        a = first(make_scenario("Birinci senaryo mu?", intro=intro_a))
        b = first(make_scenario("İkinci senaryo mu?"))
        return [("a.md",) + a, ("b.md",) + b]

    def test_identical_boxes_without_reference_fail(self):
        errors, infos = find_near_duplicates(self.pair(), threshold=0.5)
        self.assertEqual(len(errors), 1)
        self.assertEqual(infos, [])

    def test_identical_boxes_with_fark_reference_pass(self):
        intro = "Bu senaryonun “İkinci senaryo mu?” senaryosundan farkı: burada yalnızca renk değişir."
        errors, infos = find_near_duplicates(self.pair(intro), threshold=0.5)
        self.assertEqual(errors, [])
        self.assertEqual(len(infos), 1)

    def test_reference_without_fark_does_not_count(self):
        intro = "Bu senaryo “İkinci senaryo mu?” senaryosuyla birlikte okunur."
        errors, _ = find_near_duplicates(self.pair(intro), threshold=0.5)
        self.assertEqual(len(errors), 1)

    def test_dissimilar_boxes_pass(self):
        a = first(make_scenario("Birinci senaryo mu?"))
        b = first(make_scenario(
            "İkinci senaryo mu?",
            tests=[
                "- Zamanlama: Hatırlatma e-postası kaçıncı saatte gidiyor?",
                "- Kanal: Bildirim uygulama içinde mi iletiliyor acaba?",
                "- Sıklık: Haftalık özet okuyucuyu yoruyor mu sonunda?",
                "- Kişiselleştirme: Ad ile hitap açılmayı etkiliyor mu?",
                "- Segment: Yeni abonelerde etki eskilerden farklı mı?",
            ],
            kpis=[
                "- Açılma Oranı: Gönderilen iletilerin açılması yükseliyor mu?",
                "- Abonelikten Ayrılma: Liste terki belirgin biçimde artmamalı.",
                "- Okuma Süresi: İletide geçirilen zaman uzuyor mu gerçekten?",
                "- Şikâyet Oranı: İstenmeyen ileti bildirimi çoğalıyor mu?",
                "- Geri Dönüş: Okur siteye yeniden geliyor mu bu sayede?",
            ],
            donts=[
                "- Gönderim saatini değiştirirken konu satırını yeniden yazmayın.",
                "- Onay vermemiş kişilere ileti göndermeyin kesinlikle hiçbir zaman.",
                "- Tatil haftasında başlatıp normal haftalarla karıştırmayın.",
                "- Açılma artışını tıklamaya bakmadan başarı saymayın lütfen.",
                "- Liste dışı adresleri sonuca dahil edip oranı şişirmeyin.",
            ],
        ))
        errors, infos = find_near_duplicates([("a.md",) + a, ("b.md",) + b], threshold=0.28)
        self.assertEqual((errors, infos), ([], []))


class TestGlossary(unittest.TestCase):
    TEXT = (
        "| Kanonik ad | Tanım | Payda | Eş anlamlılar |\n"
        "|---|---|---|---|\n"
        "| **Dönüşüm Oranı (CR)** | Hedef aksiyonu tamamlayan pay. | Atanan ziyaretçi | Genel Dönüşüm Oranı (CR); Nihai Dönüşüm Oranı (CR) |\n"
        "| **Nitelikli Fırsat Oranı** | Satışa uygun fırsat payı. | Atanan ziyaretçi | Nitelikli Fırsat Sayısı (SQL) |\n"
        "| **Kaydırma Derinliği** | Sayfanın ne kadarının görüldüğü. | Sayfa görüntüleme | - |\n"
    )

    def test_parse(self):
        g = parse_glossary(self.TEXT)
        self.assertEqual(set(g), {"Dönüşüm Oranı (CR)", "Nitelikli Fırsat Oranı", "Kaydırma Derinliği"})
        self.assertEqual(g["Kaydırma Derinliği"], [])
        self.assertIn("Nihai Dönüşüm Oranı (CR)", g["Dönüşüm Oranı (CR)"])

    def test_header_row_ignored(self):
        self.assertNotIn("Kanonik ad", parse_glossary(self.TEXT))

    def test_status(self):
        g = parse_glossary(self.TEXT)
        self.assertEqual(glossary_status("Dönüşüm Oranı (CR)", g), "canonical")
        self.assertEqual(glossary_status("Nitelikli Fırsat Oranı (atanan ziyaretçi başına)", g), "canonical")
        self.assertEqual(glossary_status("Nihai Dönüşüm Oranı (CR)", g), "synonym:Dönüşüm Oranı (CR)")
        self.assertEqual(glossary_status("Kurtarma Oranı", g), "missing")


if __name__ == "__main__":
    unittest.main()
