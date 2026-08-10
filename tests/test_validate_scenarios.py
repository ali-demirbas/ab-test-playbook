#!/usr/bin/env python3
"""validate_scenarios.py için unit testler. Bağımlılıksız (unittest).

Bu testler doğrulayıcının bilinen kör noktalarına karşı regresyon korumasıdır:
dosya başındaki senaryonun yutulması, sıfır senaryolu dosyanın temiz sayılması,
mükerrer kutu başlığı, sahte guardrail kalıbı ve doldurma maddeleri.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from validate_scenarios import parse_scenarios, check_scenario, box_items  # noqa: E402


def make_scenario(title="Geçerli bir senaryo başlığı mı?",
                  tests=None, kpis=None, donts=None):
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
        "- Sonuçları örneklem dolmadan yorumlamayın hiçbir zaman.",
        "- Tek segmentte ölçüp tüm kullanıcılara genellemeyin bunu.",
        "- Guardrail metriklerini görmezden gelip karar vermeyin asla.",
        "- Testi hafta ortasında başlatıp erken kapatmayın lütfen.",
    ]
    return (f"## {title}\n\nAçıklama paragrafı burada yeterince uzun duruyor.\n\n"
            "**Test edilmesi gerekenler**\n" + "\n".join(tests) + "\n\n"
            "**Takip edilecek ana KPI’lar**\n" + "\n".join(kpis) + "\n\n"
            "**Yapılmaması gerekenler**\n" + "\n".join(donts) + "\n")


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
        title, body = parse_scenarios(text)[0]
        self.assertEqual(len(box_items(body, "Yapılmaması gerekenler")), 5)


class TestCheckScenario(unittest.TestCase):
    def check(self, text):
        title, body = parse_scenarios(text)[0]
        return check_scenario("test.md", title, body)

    def test_valid_scenario_passes(self):
        self.assertEqual(self.check(make_scenario()), [])

    def test_title_without_question_mark_fails(self):
        errs = self.check(make_scenario(title="Soru işareti yok"))
        self.assertTrue(any("soru işaretiyle bitmiyor" in e for e in errs))

    def test_four_items_fail(self):
        s = make_scenario()
        s = s.replace("- Testi hafta ortasında başlatıp erken kapatmayın lütfen.\n", "")
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
            "- Sonuçları örneklem dolmadan yorumlamayın hiçbir zaman.",
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


if __name__ == "__main__":
    unittest.main()
