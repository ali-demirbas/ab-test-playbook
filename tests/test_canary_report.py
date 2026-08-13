#!/usr/bin/env python3
"""canary_report.py için unit testler. Bağımlısız (unittest).

Bu aracın tek işi aratıldığında GERÇEKTEN eşleşecek ifadeler üretmek. Üretilen
ifade sayfada o sırayla geçmiyorsa arama boş döner ve bu "kopya yok" sanılır —
aracın sessizce yanlış güven vermesi, hiç çalışmamasından kötüdür. Testlerin
çoğu o hataya karşı.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from canary_report import clean, phrases, distinctive, score  # noqa: E402
from collections import Counter  # noqa: E402


class TestSentenceBoundaries(unittest.TestCase):
    def test_phrase_never_spans_two_sentences(self):
        text = "Birinci cümle burada biter. İkinci cümle burada başlar."
        for p in phrases(text, size=4):
            self.assertFalse("biter İkinci" in p, "cümle sınırı aşıldı: %s" % p)

    def test_phrases_come_from_within_one_sentence(self):
        text = "Kupon alanı katlanınca sepet terk oranı düşer mi acaba."
        got = list(phrases(text, size=5))
        self.assertTrue(got)
        self.assertIn("Kupon alanı katlanınca sepet terk", got)

    def test_short_sentence_yields_nothing(self):
        self.assertEqual(list(phrases("Kısa cümle.", size=7)), [])


class TestMarkdownCleaning(unittest.TestCase):
    def test_code_fence_removed(self):
        self.assertNotIn("gizli", clean("Metin\n```\ngizli kod\n```\ndevam"))

    def test_inline_code_removed(self):
        self.assertNotIn("add_to_cart", clean("Olay `add_to_cart` izleniyor"))

    def test_link_text_kept_url_dropped(self):
        out = clean("Bkz [metodoloji](https://example.com/x) dosyası")
        self.assertIn("metodoloji", out)
        self.assertNotIn("example.com", out)

    def test_bold_markers_do_not_weld_sentences(self):
        # Vurgu işaretleri satır başı markup'ından ÖNCE temizlenmezse iki cümle
        # tek ifadeye kaynıyor ve o ifade hiçbir sayfada bulunmuyor.
        out = clean("**Birinci kural.** **İkinci kural.**")
        self.assertNotIn("*", out)
        for p in phrases(out, size=3):
            self.assertFalse("kural İkinci" in p, "cümleler kaynadı: %s" % p)

    def test_html_tags_removed(self):
        self.assertNotIn("div", clean('<div class="x">içerik</div>'))


class TestDistinctiveness(unittest.TestCase):
    def test_function_word_soup_is_rejected(self):
        self.assertFalse(distinctive("this is a thing that we have for the"))

    def test_too_short_is_rejected(self):
        self.assertFalse(distinctive("kupon alanı katlandı"))

    def test_needs_an_anchor_word_or_number(self):
        # Hepsi kısa ve sıradan kelime: aratınca her yerde eşleşir.
        self.assertFalse(distinctive("bir iki üç dört beş altı yedi"))

    def test_domain_phrase_is_accepted(self):
        self.assertTrue(distinctive("Harita işaretlerini listedeki sırayla eşleşmeyecek şekilde numaralandırmayın"))

    def test_number_counts_as_an_anchor(self):
        self.assertTrue(distinctive("sepet terk oranı 890 puan altına düştü"))

    def test_stray_long_token_is_rejected(self):
        self.assertFalse(distinctive("bak buraya aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa uzun kelime var"))


class TestScoring(unittest.TestCase):
    def test_rarer_words_score_higher(self):
        counts = Counter({"sık": 100, "nadir": 1, "kelime": 50})
        common = score("sık sık sık kelime kelime", counts)
        rare = score("nadir nadir nadir kelime kelime", counts)
        self.assertGreater(rare, common)

    def test_deterministic(self):
        counts = Counter({"a": 3, "b": 2})
        self.assertEqual(score("a b a b a", counts), score("a b a b a", counts))


if __name__ == "__main__":
    unittest.main()
