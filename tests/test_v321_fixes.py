#!/usr/bin/env python3
"""3.2.1 fixes: the stakeholder brief passes the rule 5 gate and restates no
record field, the 3.1-record migration hints, the tightened exposure
keywords and the screen spec's accordion node."""
import copy
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, HERE)
import screen_spec as ss  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402
import validate_scenarios as vs  # noqa: E402
from test_validate_scenario_json_v3 import SCHEMA, plain  # noqa: E402

BRIEF = os.path.join(ROOT, "templates", "stakeholder-brief.md")


def brief_blocks():
    """The two fenced blocks of the template (TR, EN), as lists of lines."""
    with open(BRIEF, encoding="utf-8") as fh:
        text = fh.read()
    return [b.strip().splitlines() for b in re.findall(r"```\n(.*?)```", text, re.S)]


class TestBriefPassesTheGate(unittest.TestCase):
    def test_two_blocks_of_heading_why_now_and_three_outcomes(self):
        blocks = brief_blocks()
        self.assertEqual(len(blocks), 2)
        for block in blocks:
            self.assertEqual(len(block), 5, block)

    def test_no_line_trips_the_statistics_or_decision_rule_check(self):
        for block in brief_blocks():
            for line in block:
                with self.subTest(line=line):
                    self.assertIsNone(vsj.statistics_hit(line), line)
                    for pattern, why in vs.BANNED_NEVER_DO:
                        self.assertIsNone(pattern.search(line), (line, why))

    def test_the_outcome_lines_pass_in_a_record_field(self):
        for block in brief_blocks():
            for line in block[2:]:
                sc = plain()
                sc["priority"]["rationale"] = sc["priority"]["rationale"] + " " + line
                with self.subTest(line=line):
                    self.assertFalse([e for e in vsj.validate(sc, SCHEMA, "en") if "statistics" in e], line)

    def test_every_outcome_leaves_the_decision_to_its_owner(self):
        tr, en = brief_blocks()
        for line in tr[2:]:
            self.assertIn("karar sahibinde", line)
        for line in en[2:]:
            self.assertIn("the owner's call", line)

    def test_nothing_the_record_holds_is_restated(self):
        for block in brief_blocks():
            text = "\n".join(block)
            for label in ("Soru:", "Ne değişiyor", "Birincil KPI", "Guardrail", "Question:", "What changes",
                          "Primary KPI", "tolerans", "margin", "ship B", "yayına alınır", "A’ya dönülür",
                          "revert"):
                self.assertNotIn(label, text)

    def test_a_ship_condition_is_still_refused(self):
        for text in ("B önde çıkarsa yayına alınır; karar sahibinde", "If B leads, ship it.",
                     "B kazanırsa yayına alınır", "ship B if ahead"):
            self.assertIsNotNone(vsj.statistics_hit(text), text)

    def test_the_rule_5_wording_agrees(self):
        with open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8") as fh:
            rules = fh.read()
        self.assertIn("leaves the decision to its owner", rules)
        with open(os.path.join(ROOT, "agents", "scenario-critic.md"), encoding="utf-8") as fh:
            critic = fh.read()
        self.assertNotIn("the three outcomes with their actions", critic)
        self.assertIn("leaving the decision to its owner", critic)


def old_record():
    sc = plain()
    del sc["priority"]["inputs"]
    return sc


class TestMigrationHints(unittest.TestCase):
    def test_missing_inputs_names_the_four_keys_and_an_example(self):
        for lang, word in (("en", "Example"), ("tr", "Örnek")):
            e = [x for x in vsj.validate(old_record(), SCHEMA, lang) if "'inputs'" in x]
            self.assertEqual(len(e), 1, e)
            for part in ("evidence", "main_path", "noticeable", "effort", "archive_or_research", "low / medium / high",
                         word, '"inputs": {"evidence"'):
                self.assertIn(part, e[0])

    def test_a_missing_single_input_names_its_values(self):
        sc = plain()
        del sc["priority"]["inputs"]["effort"]
        e = [x for x in vsj.validate(sc, SCHEMA, "en") if "'effort'" in x]
        self.assertTrue(e and "low (copy, style, order)" in e[0], e)

    def test_exposure_messages_carry_an_example(self):
        sc = plain()
        sc["variants"][0]["description"] = "Teslimat bilgisi kapalı bir akordeonun içinde"
        self.assertTrue(any("Example: \"exposure\"" in x for x in vsj.validate(sc, SCHEMA, "en")))
        self.assertTrue(any("Örnek: \"exposure\"" in x for x in vsj.validate(sc, SCHEMA, "tr")))
        sc["exposure"] = "Akordeon başlığı ekrana gelen kullanıcılar sayılır."
        self.assertTrue(any("\"both arms\"" in x for x in vsj.validate(sc, SCHEMA, "en")))


class TestExposureKeywords(unittest.TestCase):
    HITS = ("Shipping info sits in the Details tab", "The fee is in the country dropdown",
            "A dropdown menu holds the sizes", "the drop-down list hides the fee", "tabs on the product page",
            "Detay bir sekmede", "Ücret açılır menüde görünüyor", "Bilgi modalda gösterilir", "A dialog asks first")
    MISSES = ("The size table lists every size", "A stable layout", "On a tablet the price wraps",
              "Press Tab to move focus to the field", "The Tab key reaches the link", "the keyboard tab order",
              "Tab tuşuyla alana geçilir", "A country dropdown above the fold", "a dropdown field for the country",
              "the modality of payment", "The app's tab bar stays", "a dialogue with customers")

    def test_ui_words_match(self):
        for text in self.HITS:
            with self.subTest(text=text):
                self.assertIsNotNone(vsj.conditional_hit(text), text)

    def test_lookalikes_do_not_match(self):
        for text in self.MISSES:
            with self.subTest(text=text):
                self.assertIsNone(vsj.conditional_hit(text), text)

    def test_the_record_check_uses_it(self):
        sc = plain()
        sc["variants"][0]["description"] = "The size table sits under the photo"
        self.assertFalse([e for e in vsj.validate(sc, SCHEMA, "en") if e.startswith("exposure")])
        sc["variants"][0]["description"] = "The returns policy sits in the Details tab"
        self.assertTrue([e for e in vsj.validate(sc, SCHEMA, "en") if e.startswith("exposure")])


SCREEN = [
    {"h": "Kanvas Ayakkabı"},
    {"cta": "Sepete ekle"},
    {"id": "acc", "accordion": {"title": "Kargo ve iade", "items": [{"text": "Ertesi gün kargoda, ücretsiz iade."}]}},
    {"accordion": {"title": "Ürün özellikleri"}},
]
OPEN = {"op": "edit", "target": "acc", "set": {"open": True}, "label": "Açık gelen kargo bilgisi"}


class TestAccordion(unittest.TestCase):
    def test_closed_draws_plus_and_no_body(self):
        a, _, problems = ss.compile(SCREEN, OPEN, "tr")
        self.assertEqual(problems, [])
        self.assertIn('aria-expanded="false"', a)
        self.assertIn(">+</span>", a)
        self.assertNotIn("Ertesi gün kargoda", a)
        self.assertNotIn(ss.ACC_OPEN_SIGN, a)

    def test_opening_it_is_one_change_and_the_sign_follows(self):
        _, b, problems = ss.compile(SCREEN, OPEN, "tr")
        self.assertEqual(problems, [])
        self.assertIn('aria-expanded="true"', b)
        self.assertIn(">%s</span>" % ss.ACC_OPEN_SIGN, b)
        self.assertIn("Ertesi gün kargoda", b)
        ring = b[b.index('class="hl"'):]
        self.assertLess(ring.index("Kargo ve iade"), ring.index("Ertesi gün kargoda"))
        # the other accordion stays closed and outside the ring
        self.assertEqual(b.count('aria-expanded="false"'), 1)

    def test_an_open_one_needs_items(self):
        _, _, problems = ss.compile([{"accordion": {"title": "Kargo", "open": True}}, {"h": "x"}],
                                    {"op": "remove", "target": "h1", "label": "Başlık kaldırıldı"}, "en")
        self.assertTrue(any("accordion" in p and "items" in p for p in problems), problems)
        bad = copy.deepcopy(SCREEN)
        bad[3] = {"id": "spec", "accordion": {"title": "Ürün özellikleri"}}
        _, _, problems = ss.compile(bad, dict(OPEN, target="spec"), "en")
        self.assertTrue(problems)

    def test_value_shape_is_checked(self):
        for value in ({"open": False}, {"title": ""}, {"title": "x", "open": "yes"}, {"title": "x", "items": []},
                      {"title": "x", "colour": "#ffffff"}):
            _, _, problems = ss.compile([{"accordion": value}, {"h": "y", "id": "y"}],
                                        {"op": "remove", "target": "y", "label": "Başlık kaldırıldı"}, "en")
            self.assertTrue(problems, value)

    def test_only_its_state_title_and_box_are_editable(self):
        _, _, problems = ss.compile(SCREEN, dict(OPEN, set={"fg": "#ff0000"}), "en")
        self.assertTrue(any("reaches every element" in p for p in problems), problems)
        _, b, problems = ss.compile(SCREEN, dict(OPEN, set={"title": "Kargo, iade ve teslimat"}), "en")
        self.assertEqual(problems, [])
        self.assertIn("Kargo, iade ve teslimat", b)

    def test_a_change_inside_a_closed_accordion_is_no_difference(self):
        screen = copy.deepcopy(SCREEN)
        screen[2]["accordion"]["items"][0]["id"] = "body"
        _, _, problems = ss.compile(screen, {"op": "edit", "target": "body", "set": {"text": "Başka metin"},
                                             "label": "Metin değişti"}, "en")
        self.assertTrue(any("B draws exactly what A draws" in p for p in problems), problems)

    def test_removing_the_last_item_of_an_open_one_is_refused(self):
        screen = copy.deepcopy(SCREEN)
        screen[2]["accordion"]["open"] = True
        screen[2]["accordion"]["items"][0]["id"] = "body"
        _, _, problems = ss.compile(screen, {"op": "remove", "target": "body", "label": "Metin kaldırıldı"}, "en")
        self.assertTrue(any("empty" in p for p in problems), problems)

    def test_documented_in_mockup_style(self):
        with open(os.path.join(ROOT, "knowledge", "mockup-style.md"), encoding="utf-8") as fh:
            self.assertIn("`accordion` {title, open, items []}", fh.read())


class TestNames(unittest.TestCase):
    def test_display_name_and_install_slug(self):
        with open(os.path.join(ROOT, "docs", "index.html"), encoding="utf-8") as fh:
            page = fh.read()
        self.assertIn("<title>A/B Test Builder", page)
        self.assertIn('og:title" content="A/B Test Builder', page)
        self.assertIn("<h1>A/B Test Builder</h1>", page)
        with open(os.path.join(ROOT, "docs", "llms.txt"), encoding="utf-8") as fh:
            self.assertTrue(fh.readline().startswith("# A/B Test Builder"))
        for readme in ("README.md", "README.tr.md"):
            with open(os.path.join(ROOT, readme), encoding="utf-8") as fh:
                self.assertIn("`ab-test-playbook`", fh.read())

    def test_version_is_the_same_everywhere(self):
        versions = set()
        for rel in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json",
                    ".gemini/extensions/ab-test-playbook/gemini-extension.json"):
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                versions.add(json.load(fh)["version"])
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8") as fh:
            market = json.load(fh)
        versions.add(market["metadata"]["version"])
        versions.update(p["version"] for p in market["plugins"])
        for name in os.listdir(os.path.join(ROOT, "skills")):
            with open(os.path.join(ROOT, "skills", name, "SKILL.md"), encoding="utf-8") as fh:
                versions.add(re.search(r"^  version: (\S+)$", fh.read(), re.M).group(1))
        self.assertEqual(len(versions), 1, versions)
        with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as fh:
            self.assertIn("## %s - " % versions.pop(), fh.read())


if __name__ == "__main__":
    unittest.main()
