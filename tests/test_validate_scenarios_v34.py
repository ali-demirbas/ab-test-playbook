#!/usr/bin/env python3
"""validate_scenarios.py, 3.4: the archive tag line, the English title line, the
English body shape (knowledge/scenarios/FORMAT.md) and the archive-wide id and
English-title checks."""
import contextlib
import io
import os
import re
import sys
import tempfile
import textwrap
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import validate_scenarios as vs  # noqa: E402
from test_validate_scenarios import make_scenario, first, DEFAULT_TAG  # noqa: E402

ROOT = os.path.join(HERE, "..")
FORMAT_MD = os.path.join(ROOT, "knowledge", "scenarios", "FORMAT.md")


def tag(**over):
    values = dict(id="cc-001", mercek="Netlik", düzey="görsel", sektör="genel", pazar="global",
                  emek="düşük", durum="güncel", tarih="2026-11")
    values.update(over)
    return "Etiket: " + " · ".join(f"{k}={values[k]}" for k in vs.TAG_KEYS)


def meta_errors(text):
    title, body = first(text)
    return vs.check_metadata("t.md", title, body, glossary=vs.load_glossary())[2]


def format_example():
    """The indented example block of FORMAT.md, dedented."""
    with open(FORMAT_MD, encoding="utf-8") as fh:
        text = fh.read()
    part = text.split("### Example", 1)[1]
    lines = [l for l in part.split("\n") if l.startswith("    ") or not l.strip()]
    start = next(i for i, l in enumerate(lines) if l.startswith("    ## "))
    return textwrap.dedent("\n".join(lines[start:])).strip() + "\n"


class TestTagLine(unittest.TestCase):
    def test_valid_line_parses(self):
        tags, errors = vs.parse_tag_line(tag())
        self.assertEqual(errors, [])
        self.assertEqual(tags["düzey"], "görsel")

    def test_every_key_in_order(self):
        line = tag().replace("mercek=Netlik · düzey=görsel", "düzey=görsel · mercek=Netlik")
        self.assertTrue(any("bu sırada" in e for e in vs.parse_tag_line(line)[1]))
        line = tag().replace(" · durum=güncel", "")
        self.assertTrue(vs.parse_tag_line(line)[1])

    def test_values_come_from_the_lists(self):
        for key, bad in (("mercek", "Hız"), ("düzey", "renk"), ("pazar", "AB"), ("emek", "çok"),
                         ("durum", "eski"), ("sektör", "seyahat")):
            with self.subTest(key=key):
                errors = vs.parse_tag_line(tag(**{key: bad}))[1]
                self.assertTrue(any(key in e and bad in e for e in errors), errors)

    def test_id_and_date_shape(self):
        for bad in ("cc-1", "zz-001", "CC-001", "cc_001"):
            with self.subTest(id=bad):
                self.assertTrue(any("id" in e for e in vs.parse_tag_line(tag(id=bad))[1]))
        for bad in ("2026-13", "26-11", "2026/11", "2026-11-15"):
            with self.subTest(tarih=bad):
                self.assertTrue(any("tarih" in e for e in vs.parse_tag_line(tag(tarih=bad))[1]))

    def test_two_sectors_allowed_three_not(self):
        self.assertEqual(vs.parse_tag_line(tag(sektör="saas,b2b"))[1], [])
        self.assertTrue(vs.parse_tag_line(tag(sektör="saas,b2b,finans"))[1])
        self.assertTrue(vs.parse_tag_line(tag(sektör="saas,saas"))[1])

    def test_levels_split_into_element_and_structural(self):
        self.assertEqual(set(vs.ELEMENT_LEVELS) & set(vs.STRUCTURAL_LEVELS), set())
        self.assertEqual(set(vs.ELEMENT_LEVELS) | set(vs.STRUCTURAL_LEVELS), set(vs.TAG_VALUES["düzey"]))

    def test_every_file_has_an_id_prefix(self):
        self.assertEqual(sorted(vs.ID_PREFIXES), sorted(vs.archive_files()))
        self.assertEqual(len(set(vs.ID_PREFIXES.values())), len(vs.ID_PREFIXES))


class TestHead(unittest.TestCase):
    def test_tagged_block_passes(self):
        self.assertEqual(meta_errors(make_scenario()), [])

    def test_tag_line_required(self):
        self.assertTrue(any("Etiket" in e for e in meta_errors(make_scenario(tag_line=None))))

    def test_en_title_required_and_a_question(self):
        self.assertTrue(any("EN:" in e for e in meta_errors(make_scenario(en_line=None))))
        self.assertTrue(any("soru işareti" in e for e in meta_errors(make_scenario(en_line="EN: A title"))))

    def test_untranslated_en_title_is_caught(self):
        errors = meta_errors(make_scenario(en_line="EN: Buton rengi dönüşümü etkiler mi?"))
        self.assertTrue(any("Türkçe harf" in e for e in errors), errors)

    def test_head_order_is_fixed(self):
        text = make_scenario(tag_line=None, en_line=None).replace(
            "Değişken: Buton rengi · Fark: değiştir", "Değişken: Buton rengi · Fark: değiştir\n\n"
            + DEFAULT_TAG.replace("Etiket", "EN: Is this it?\n\nEtiket"))
        self.assertTrue(meta_errors(text))

    def test_en_variable_is_optional(self):
        text = make_scenario(en_line="EN: Is this a valid scenario title?\n\nEN-Variable: Button color")
        self.assertEqual(meta_errors(text), [])


class TestEnglishBody(unittest.TestCase):
    def test_format_example_is_a_valid_block(self):
        text = format_example()
        title, body = first(text)
        glossary = vs.load_glossary()
        self.assertEqual(vs.check_scenario("FORMAT.md", title, body, glossary=glossary), [])
        tags, en_title, errors = vs.check_metadata("FORMAT.md", title, body, glossary=glossary)
        self.assertEqual(errors, [])
        self.assertIsNotNone(vs.split_en_body(body)[1])

    def test_format_example_matches_its_archive_block(self):
        """The example is cc-010 with an English body; its Turkish part is the archive's."""
        title, body = first(format_example())
        tr_part = vs.split_en_body(body)[0].strip()
        with open(os.path.join(ROOT, "knowledge", "scenarios", "cart-checkout.md"), encoding="utf-8") as fh:
            blocks = dict(vs.parse_scenarios(fh.read()))
        archive = re.sub(r"\n+---\s*$", "", blocks[title].strip())
        self.assertEqual(tr_part.replace("\n\nEN-Variable: Free-shipping threshold amount", ""), archive)

    def test_format_example_cross_reference_resolves(self):
        meta = []
        for name in vs.archive_files():
            with open(os.path.join(vs.SCENARIO_DIR, name), encoding="utf-8") as fh:
                for title, body in vs.parse_scenarios(fh.read()):
                    tags, en_title, _ = vs.check_metadata(name, title, body)
                    meta.append((name, title, tags, en_title))
        en_body = vs.split_en_body(first(format_example())[1])[1]
        self.assertEqual(vs.find_unresolved_en_cross_refs(meta, [("FORMAT.md", en_body)]), [])
        broken = en_body.replace("free-shipping progress bar", "free shipping bar")
        self.assertTrue(vs.find_unresolved_en_cross_refs(meta, [("FORMAT.md", broken)]))

    def body_errors(self, mutate):
        text = mutate(format_example())
        title, body = first(text)
        return vs.check_metadata("t.md", title, body, glossary=vs.load_glossary())[2]

    def test_english_body_needs_en_variable(self):
        errors = self.body_errors(lambda t: t.replace("EN-Variable: Free-shipping threshold amount\n\n", ""))
        self.assertTrue(any("EN-Variable" in e for e in errors), errors)

    def test_parallel_item_counts(self):
        errors = self.body_errors(lambda t: t.replace("- Campaign: Does the urge to reach the threshold grow during a sale?\n", ""))
        self.assertTrue(any("What to test" in e and "4 madde" in e for e in errors), errors)

    def test_english_primary_is_the_glossary_english_name(self):
        errors = self.body_errors(lambda t: t.replace("- Revenue per Visitor (RPV):", "- Visitor Revenue:"))
        self.assertTrue(any("English name" in e for e in errors), errors)

    def test_english_guardrail_and_segment(self):
        errors = self.body_errors(lambda t: t.replace("must not erode", "may erode"))
        self.assertTrue(any("guardrail" in e for e in errors), errors)
        errors = self.body_errors(lambda t: t.replace("- Segment: Do loyal customers and new users",
                                                      "- Loyalty: Do loyal shoppers and first-time buyers"))
        self.assertTrue(any("segment" in e for e in errors), errors)

    def test_notes_are_translated(self):
        errors = self.body_errors(lambda t: t.replace("> **Market note:**", "> **Remark:**"))
        self.assertTrue(any("Market note" in e for e in errors), errors)

    def test_missing_english_box(self):
        errors = self.body_errors(lambda t: t.replace("**What not to do**", "**Avoid**"))
        self.assertTrue(any("What not to do" in e for e in errors), errors)

    def test_turkish_boxes_are_not_read_from_the_english_body(self):
        title, body = first(format_example())
        self.assertEqual(len(vs.box_items(body, vs.TEST_BOX)), 5)
        self.assertEqual(vs.parse_variable_line(body)[2], [])


class TestFreshnessNotes(unittest.TestCase):
    NOTE = "> **Güncellik notu (2026-11):** Platform kuralı değişti; yerine şunu test edin."

    def test_dated_note_passes(self):
        self.assertEqual(meta_errors(make_scenario() + "\n" + self.NOTE + "\n"), [])

    def test_note_needs_a_month(self):
        for bad in ("> **Güncellik notu:** Değişti.", "> **Güncellik notu (Kasım 2026):** Değişti."):
            with self.subTest(note=bad):
                self.assertTrue(meta_errors(make_scenario() + "\n" + bad + "\n"))

    def test_archive_uses_the_mechanism(self):
        """Item 39: the stale-ground blocks carry a dated note (autoplay, passkey, source
        personalization, chat window, push permission)."""
        titles = []
        for name in vs.archive_files():
            with open(os.path.join(vs.SCENARIO_DIR, name), encoding="utf-8") as fh:
                titles += [t for t, b in vs.parse_scenarios(fh.read()) if "**Güncellik notu (" in b]
        for needle in ("Otomatik oynayan", "tek kullanımlık kod", "kaynağa göre başlığı", "Sohbet penceresini",
                       "Push izni"):
            with self.subTest(block=needle):
                self.assertTrue(any(needle in t for t in titles), titles)

    def test_out_of_scope_line_for_consent(self):
        with open(FORMAT_MD, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("### Deliberately out of scope", text)
        self.assertIn("Cookie consent", text)


class TestLooserPattern(unittest.TestCase):
    """Item 40: 3 to 6 items, at most one patched-looking follow-up, no rule numbers."""
    TESTS = ["- Metin: Hangi ifade daha çok tıklanıyor peki?",
             "- Boyut: Daha büyük olması fark yaratıyor mu acaba?",
             "- Cihaz: Mobilde ve masaüstünde aynı sonuç mu çıkıyor?"]

    def errors(self, text):
        title, body = first(text)
        return vs.check_scenario("t.md", title, body)

    def test_three_questions_are_enough(self):
        self.assertEqual(self.errors(make_scenario(tests=self.TESTS)), [])

    def test_one_next_test_at_most(self):
        tests = self.TESTS + ["- Sonraki test: Kazanan renk sabitken metin ayrı testte fark yaratıyor mu?",
                              "- Sonraki test: Kazanan renk sabitken boyut ayrı testte fark yaratıyor mu?"]
        self.assertTrue(any("Sonraki test" in e for e in self.errors(make_scenario(tests=tests))))

    def test_position_follow_up_warns(self):
        tests = self.TESTS + ["- Sonraki test: Buton kazanırsa yeri (üst / alt) ayrı bir testte tıklamayı değiştiriyor mu?"]
        title, body = first(make_scenario(tests=tests))
        self.assertTrue(any("kazananın yerini" in w for w in vs.check_warnings("t.md", title, body)))
        tests[-1] = "- Sonraki test: Buton kazanırsa metni (“Al” / “Sepete ekle”) ayrı bir testte tıklamayı değiştiriyor mu?"
        title, body = first(make_scenario(tests=tests))
        self.assertFalse(any("kazananın yerini" in w for w in vs.check_warnings("t.md", title, body)))

    def test_rule_numbers_are_refused(self):
        for text in ("Bu bir aldatma örüntüsüdür (kural 6).", "Bkz. kural 14’teki yöntemler.",
                     "This is a dark pattern (rule 6)."):
            with self.subTest(text=text):
                errs = self.errors(make_scenario(intro="Açıklama paragrafı burada duruyor. " + text))
                self.assertTrue(any("kural numarası" in e for e in errs), errs)
        self.assertEqual(self.errors(make_scenario(intro="Hedef pazarın kuralını doğrulamadan yayınlamayın.")), [])

    def test_archive_has_no_rule_numbers_in_blocks(self):
        for name in vs.archive_files():
            with open(os.path.join(vs.SCENARIO_DIR, name), encoding="utf-8") as fh:
                for title, body in vs.parse_scenarios(fh.read()):
                    with self.subTest(block=title[:40]):
                        self.assertIsNone(vs.RULE_NUMBER.search(body))


class TestConditionedKpis(unittest.TestCase):
    """Item 36: the per-quote quote-to-contract rate is never the primary, and a
    guardrail uses the glossary's per-assigned-visitor equivalent."""
    BASE = ["- Talep Oluşturma Oranı: Formu gönderip teklif isteyenlerin payı artıyor mu bu testte?",
            "- Alan Bazlı Terk Oranı: Formu bırakanların son alanı nerede; tanı metriği olarak izlenir.",
            "- Doğrulama Hatası Oranı: Geçersiz numara girişleri bu testte artmamalı.",
            "- Veri Şikâyeti Oranı: Kişisel veriyle ilgili şikâyetler çoğalmamalı.",
            "- Sayfa Yüklenme Süresi: Form sayfası bu değişiklikle yavaşlamamalı."]

    def errors(self, kpis):
        title, body = first(make_scenario(kpis=kpis))
        return vs.check_scenario("t.md", title, body, glossary=vs.load_glossary())

    def test_per_quote_primary_is_refused(self):
        kpis = ["- Teklif → Sözleşme Dönüşüm Oranı (teklif akışına atanan ziyaretçi başına): Sözleşme artıyor mu?"] \
            + self.BASE[1:]
        self.assertTrue(any("paydası kollar arasında" in e for e in self.errors(kpis)))

    def test_per_quote_guardrail_names_the_equivalent(self):
        kpis = self.BASE[:4] + ["- Teklif → Sözleşme Dönüşüm Oranı (90 gün): Tekliflerin sözleşmeye dönüşen payı düşmemeli."]
        errors = self.errors(kpis)
        self.assertTrue(any("Sözleşme Oranı (30 gün)" in e for e in errors), errors)

    def test_assigned_equivalent_and_diagnostic_pass(self):
        kpis = self.BASE[:4] + [
            "- Sözleşme Oranı (90 gün): Atanan ziyaretçilerden sözleşmeyi tamamlayanların payı düşmemeli.",
            "- Teklif → Sözleşme Dönüşüm Oranı (90 gün): Tanı metriği; kazanan seçmez."]
        self.assertFalse(any("kollar arasında" in e or "koşullu paydalı" in e for e in self.errors(kpis)))

    def test_archive_finance_blocks_are_fixed(self):
        with open(os.path.join(vs.SCENARIO_DIR, "finance-pension.md"), encoding="utf-8") as fh:
            text = fh.read()
        glossary = vs.load_glossary()
        for title, body in vs.parse_scenarios(text):
            kpis = vs.box_items(body, vs.KPI_BOX)
            with self.subTest(block=title[:40]):
                self.assertEqual(vs.conditioned_kpi_problems(kpis, glossary), [])

    def test_parsed_glossary_keeps_its_rows(self):
        glossary = vs.load_glossary()
        self.assertIn("Sözleşme Oranı (30 gün)", glossary.rows)
        self.assertEqual(vs.glossary_row("Sözleşme Oranı (90 gün)", glossary), "Sözleşme Oranı (30 gün)")


class TestArchiveWide(unittest.TestCase):
    def test_duplicate_id_and_en_title(self):
        meta = [("a.md", "A mı?", {"id": "cc-001"}, "Is it A?"),
                ("b.md", "B mi?", {"id": "cc-001"}, "Is it a?")]
        problems = vs.find_metadata_duplicates(meta)
        self.assertTrue(any("id" in p for p in problems))
        self.assertTrue(any("EN başlığı" in p for p in problems))

    def test_next_free_id(self):
        meta = [("x", "t", {"id": "cc-001"}, None), ("x", "t", {"id": "cc-007"}, None),
                ("x", "t", {"id": "pd-030"}, None)]
        self.assertEqual(vs.next_free_id("cart-checkout.md", meta), "cc-008")
        self.assertEqual(vs.next_free_id("thank-you.md", meta), "ty-001")

    def test_format_md_is_not_a_stage_file(self):
        self.assertIn("FORMAT.md", os.listdir(vs.SCENARIO_DIR))
        self.assertNotIn("FORMAT.md", vs.archive_files())


class TestCli(unittest.TestCase):
    def run_main(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = vs.main(list(argv))
        return code, out.getvalue()

    def test_archive_is_fully_tagged(self):
        code, out = self.run_main()
        self.assertEqual(code, 0, out[-1500:])
        m = re.search(r"Etiketler: (\d+)/(\d+) senaryo", out)
        self.assertIsNotNone(m, out[-800:])
        self.assertEqual(m.group(1), m.group(2))

    def test_next_id_option(self):
        code, out = self.run_main("--next-id", "thank-you.md")
        self.assertEqual(code, 0)
        self.assertRegex(out.strip(), r"^ty-\d{3}$")
        self.assertEqual(self.run_main("--next-id", "FORMAT.md")[0], 1)

    def test_file_without_tags_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "x.md")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(make_scenario(tag_line=None))
            code, out = self.run_main(path)
            self.assertEqual(code, 1)
            self.assertIn("Etiket", out)


if __name__ == "__main__":
    unittest.main()
