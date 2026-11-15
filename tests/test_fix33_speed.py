"""3.3.0 speed fixes: the first-validation checklist in ab-test-card says what
the validator and the screen spec really accept, and two formatting causes of
first-round refusals (quote typography in adapted_from, the both-arms wording
of exposure) no longer refuse a record."""
import copy
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import screen_spec as ss  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

with open(os.path.join(ROOT, "templates", "scenario.schema.json"), encoding="utf-8") as _fh:
    SCHEMA = json.load(_fh)
with open(os.path.join(ROOT, "examples", "scenario.json"), encoding="utf-8") as _fh:
    EXAMPLE = json.load(_fh)
with open(os.path.join(ROOT, "skills", "ab-test-card", "SKILL.md"), encoding="utf-8") as _fh:
    SKILL = _fh.read()
CHECKLIST = SKILL[SKILL.index("### Before the first validation"):SKILL.index("- **Source (rule 8).**")]


def record():
    sc = copy.deepcopy(EXAMPLE)
    sc.pop("review", None)
    return sc


def errs(sc, lang="tr"):
    return vsj.validate(sc, SCHEMA, lang)


def quoted_title():
    """An archive title that carries a curly quote or apostrophe, with its Fark."""
    for title, (_, fark) in sorted(vsj.load_archive().items()):
        if re.search("[‘’“”]", title) and fark:
            return title, vsj.DIFFERENCE_ALIASES.get(fark, fark)
    raise AssertionError("no archive title with typographic quotes")


class TestAdaptedFromTypography(unittest.TestCase):
    def setUp(self):
        self.title, self.difference = quoted_title()

    def adapted(self, title):
        sc = record()
        sc.update(source="adapted", adapted_from=title, difference=self.difference)
        return [e for e in errs(sc) if e.startswith(("adapted_from", "difference"))]

    def test_the_exact_title_passes(self):
        self.assertEqual(self.adapted(self.title), [])

    def test_straight_quotes_match_a_curly_title(self):
        straight = self.title.translate({0x2018: "'", 0x2019: "'", 0x201c: '"', 0x201d: '"'})
        self.assertNotEqual(straight, self.title)
        self.assertEqual(self.adapted(straight), [])

    def test_curly_quotes_match_a_straight_title_and_a_pasted_heading_mark(self):
        self.assertEqual(vsj.quote_fold("## Mobilde 2’li grid"), vsj.quote_fold("Mobilde  2'li grid"))
        self.assertEqual(self.adapted("## " + self.title), [])

    def test_the_archive_fark_is_still_checked_through_a_folded_title(self):
        straight = self.title.translate({0x2018: "'", 0x2019: "'", 0x201c: '"', 0x201d: '"'})
        sc = record()
        other = next(d for d in ("change", "add", "move", "remove") if d != self.difference)
        sc.update(source="adapted", adapted_from=straight, difference=other)
        self.assertTrue(any(e.startswith("difference:") for e in errs(sc)), errs(sc))

    def test_other_words_or_another_case_are_still_refused(self):
        self.assertTrue(self.adapted(self.title.lower()))
        self.assertTrue(self.adapted(self.title.replace(" ", " pek ", 1)))


class TestExposureWording(unittest.TestCase):
    def test_equivalent_both_arms_wordings_pass(self):
        for text in ("tetikleyici iki kolda aynı noktada kaydedilir", "her kolda aynı noktada kaydedilir",
                     "iki varyantta da aynı noktada kaydedilir", "her iki grupta aynı noktada kaydedilir",
                     "logged at the same point in both variants", "logged the same way in each group",
                     "A ve B için aynı noktada kaydedilir"):
            self.assertTrue(vsj.BOTH_ARMS_RE.search(text), text)

    def test_a_sentence_without_the_arms_is_still_refused(self):
        self.assertIsNone(vsj.BOTH_ARMS_RE.search("Kargo akordeonunu açan kullanıcılar"))
        self.assertIsNone(vsj.BOTH_ARMS_RE.search("yalnızca B kolunda kaydedilir"))


class TestChecklist(unittest.TestCase):
    """Every example the checklist gives is one the code accepts."""

    def test_it_sits_before_the_record_rules_and_stays_short(self):
        self.assertLess(SKILL.index("### Before the first validation"), SKILL.index("- **Source (rule 8).**"))
        self.assertGreater(SKILL.index("### Before the first validation"), SKILL.index("## The record"))
        lines = [l for l in CHECKLIST.split("\n") if l.strip()]
        self.assertLessEqual(len(lines), 25)
        self.assertEqual(len(re.findall(r"(?m)^\d+\. \*\*", CHECKLIST)), 10)
        self.assertNotIn("—", CHECKLIST)
        self.assertIn("scripts/validate_scenario_json.py <record.json> [more.json]", CHECKLIST)

    def test_the_kpi_pairs_are_the_glossary_rows(self):
        with open(os.path.join(ROOT, "knowledge", "kpi-glossary.md"), encoding="utf-8") as fh:
            glossary = fh.read()
        self.assertRegex(glossary, r"\| \*\*Dönüşüm Oranı \(CR\)\*\* \|[^|]+\| Teste atanan ziyaretçi \|")
        self.assertRegex(glossary, r"\| \*\*Hemen Çıkma Oranı\*\* \|[^|]+\| Sayfayla başlayan oturum \|")
        self.assertIn('"Hemen Çıkma Oranı"` over `"Sayfayla başlayan oturum"', CHECKLIST)
        sc = record()
        sc["primary_kpi"] = {"name": "Dönüşüm Oranı (CR)", "denominator": "Teste atanan ziyaretçi",
                             "direction": "increase"}
        self.assertEqual([e for e in errs(sc) if e.startswith("primary_kpi")], [])
        sc["primary_kpi"] = {"name": "Hemen Çıkma Oranı", "denominator": "Teste atanan ziyaretçi",
                             "direction": "decrease"}
        self.assertTrue([e for e in errs(sc) if e.startswith("primary_kpi")], "a family mismatch is refused")

    def test_the_accessibility_sentence_states_every_base_criterion(self):
        sentence = re.search(r'"(B yayına girmeden[^"]+)"', CHECKLIST).group(1)
        sc = record()
        sc["warnings"] = [{"type": "accessibility", "text": sentence}]
        self.assertEqual([e for e in errs(sc) if e.startswith("warnings")], [])
        sc["warnings"] = [{"type": "accessibility", "text": "Bağlantı erişilebilir olmalı."}]
        self.assertTrue([e for e in errs(sc) if e.startswith("warnings")])

    def test_the_exposure_and_invariant_examples_pass(self):
        exposure = re.search(r'"exposure": "([^"]+)"', CHECKLIST).group(1)
        self.assertTrue(vsj.BOTH_ARMS_RE.search(exposure))
        sc = record()
        sc["variants"][1]["description"] += " (akordeonun içinde)"
        self.assertTrue([e for e in errs(sc) if e.startswith("exposure")])
        sc["exposure"] = exposure
        self.assertEqual([e for e in errs(sc) if e.startswith("exposure")], [])
        self.assertIn('["Geçerli bir kod iki kolda da aynı adımla uygulanır."]', CHECKLIST)

    def test_the_score_table_is_the_validators(self):
        for name, points in vsj.SCORE_EVIDENCE.items():
            self.assertIn("`%s` %d" % (name, points), CHECKLIST)
        for name, points in vsj.SCORE_EFFORT.items():
            self.assertIn("`%s` %d" % (name, points), CHECKLIST)
        self.assertEqual(vsj.SCORE_BANDS, ((7, "high"), (4, "medium"), (0, "low")))
        self.assertEqual(vsj.EVIDENCE_INPUTS, {"user_data": ("user_data", "behaviour_data"),
                                               "archive": ("archive_or_research",),
                                               "sector": ("archive_or_research",), "intuition": ("intuition",)})

    def test_the_ops_are_the_compilers(self):
        for op in ss.OPS:
            self.assertIn("`%s`" % op, CHECKLIST)

    def test_the_move_and_plan_examples_compile(self):
        move = json.loads(re.search(r'`(\{"op": "move_before"[^`]+)`', CHECKLIST).group(1))
        plan = json.loads(re.search(r'`(\{"plan": [^`]+)`', CHECKLIST).group(1))
        screen = [{"h": "Sepet"}, {"line": ["Ara toplam", "499 TL"], "id": "ozet"},
                  {"field": "Kupon kodu", "id": "kupon"}, dict(plan, id="pro"), {"cta": "Devam et"}]
        card = {"screen": screen, "change": move}
        self.assertEqual(ss.form_problems(card, "en"), [])
        variant_a, variant_b, problems = ss.compile(screen, move, "tr")
        self.assertEqual(problems, [])
        self.assertIn("Kupon altta", variant_a)
        self.assertIn("Kupon üstte", variant_b)
        self.assertLess(variant_b.index("Kupon kodu"), variant_b.index("Ara toplam"))

    def test_the_node_shapes_it_names_are_the_ones_refused(self):
        def problems(node):
            out = []
            ss._parse(node, "card.screen[0]", True, "en", out, {})
            return out
        self.assertEqual(problems({"fold": True}), [])
        self.assertTrue(problems({"fold": "below"}))
        self.assertTrue(problems({"h": "Başlık", "align": "center"}))
        self.assertEqual(problems({"text": "Metin", "align": "center"}), [])
        self.assertTrue(problems({"plan": {"name": "Pro", "price": 499}}))


if __name__ == "__main__":
    unittest.main()
