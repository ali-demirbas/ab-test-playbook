#!/usr/bin/env python3
"""check_frontmatter.py için unit testler. Bağımlısız (unittest).

Bu kontrolün varlık sebebi gerçek bir kusur: `description` içindeki tırnaksız
bir `style: a Variant` yüzünden abtest-card skill'i `npx skills add` tarafından
sessizce atlanıyordu — repoda duruyor, diğer tüm kontrollerden geçiyor, ama
kurulmuyordu.

Testlerin ağırlığı YANLIŞ POZİTİFTE. Şablon dosyalarında bilerek yazılmış YAML
yorumları, akış dizileri ve blok skalerleri var; bunlara takılan bir kontrol
insanların atlamayı öğrendiği bir kontroldür ve hiç olmamasından kötüdür.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from check_frontmatter import frontmatter, lint, scalar_problems  # noqa: E402


def block(*lines):
    return "\n".join(lines)


class TestTheBugThatShipped(unittest.TestCase):
    def test_unquoted_colon_space_is_caught(self):
        problems = lint(block("name: abtest-card",
                              "description: card in the archive's visual style: a Variant pair"))
        self.assertEqual(len(problems), 1)
        self.assertIn("nested mapping", problems[0][1])

    def test_line_number_points_at_the_offending_line(self):
        problems = lint(block("name: x", "tone: fine", "desc: broken: here"))
        self.assertEqual(problems[0][0], 3)

    def test_quoting_the_value_fixes_it(self):
        self.assertEqual(lint(block('desc: "card in the style: a Variant pair"')), [])

    def test_em_dash_rewrite_fixes_it(self):
        self.assertEqual(lint(block("desc: card in the style — a Variant pair")), [])


class TestUnterminatedQuote(unittest.TestCase):
    def test_value_opening_with_a_quote_must_close_it(self):
        # Gerçek örnek: formality: "siz" always in TR; formal-neutral EN
        # PyYAML bunu yakalar ama CI'da PyYAML yok, o yüzden lint yakalamalı.
        problems = lint(block('formality: "siz" always in TR'))
        self.assertEqual(len(problems), 1)
        self.assertIn("does not close it", problems[0][1])

    def test_quote_in_the_middle_is_fine(self):
        self.assertEqual(lint(block('formality: B2B TR "siz", EN neutral')), [])


class TestNoFalsePositives(unittest.TestCase):
    def test_inline_comment_is_legal_yaml(self):
        # `key: value  # not` YAML'da geçerli ve şablonlarda bilerek kullanılıyor.
        self.assertEqual(lint(block("urgency_allowed: true          # only when true")), [])

    def test_flow_sequence_is_legal(self):
        self.assertEqual(lint(block("default_channels: [email, push, sms]")), [])

    def test_flow_mapping_is_legal(self):
        self.assertEqual(lint(block('limits: {max: 40, unit: chars}')), [])

    def test_url_colon_without_space_is_legal(self):
        self.assertEqual(lint(block("home: https://example.com/x")), [])

    def test_block_scalar_body_is_not_parsed_as_keys(self):
        problems = lint(block("intent: >-",
                              "  Create a map: the whole thing",
                              "  across stages.",
                              "type: component"))
        self.assertEqual(problems, [])

    def test_nested_mapping_keys_are_checked_at_depth(self):
        problems = lint(block("metadata:", "  category: render", "  note: broken: here"))
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0][0], 3)

    def test_one_colon_in_a_sequence_item_is_legal(self):
        # PyYAML'a karşı doğrulandı: `- a: b` tek çiftlik geçerli bir mapping.
        # Bunu hata saymak sıradan liste içeriğinde ateş eder.
        self.assertEqual(lint(block("best_for:", "  - map a journey: end to end")), [])

    def test_two_colons_in_a_sequence_item_are_fatal(self):
        problems = lint(block("best_for:", "  - map a journey: end to end: really"))
        self.assertEqual(len(problems), 1)
        self.assertIn("list item", problems[0][1])

    def test_unclosed_quote_in_a_sequence_item_is_caught(self):
        problems = lint(block("scenarios:", '  - "map a journey'))
        self.assertEqual(len(problems), 1)
        self.assertIn("does not close it", problems[0][1])

    def test_quoted_sequence_item_is_fine(self):
        self.assertEqual(lint(block("scenarios:", '  - "map a journey: end to end"')), [])

    def test_comment_line_is_skipped(self):
        self.assertEqual(lint(block("# a note: with a colon", "name: x")), [])

    def test_empty_value_means_a_block_follows(self):
        self.assertEqual(lint(block("metadata:", "  version: 0.1.0")), [])


class TestFrontmatterExtraction(unittest.TestCase):
    def test_returns_none_without_a_leading_marker(self):
        self.assertIsNone(frontmatter("# Just a heading\n"))

    def test_returns_none_when_the_block_is_never_closed(self):
        self.assertIsNone(frontmatter("---\nname: x\nno closing marker\n"))

    def test_body_is_not_included(self):
        got = frontmatter("---\nname: x\n---\n\n# Body: with a colon\n")
        self.assertIn("name: x", got)
        self.assertNotIn("Body", got)


class TestScalarProblems(unittest.TestCase):
    def test_empty_value_is_clean(self):
        self.assertEqual(scalar_problems("   "), [])

    def test_yaml_indicator_start_is_flagged(self):
        self.assertTrue(scalar_problems("*anchor"))

    def test_dash_start_is_not_an_indicator(self):
        self.assertEqual(scalar_problems("-15% discount cap"), [])


if __name__ == "__main__":
    unittest.main()
