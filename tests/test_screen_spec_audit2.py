#!/usr/bin/env python3
"""Second-audit regressions for the screen spec compiler (scripts/screen_spec.py).

A change B draws exactly like A is refused (an identical replace, a move to
where the node already is, a hex colour differing only in case); a spacing
edit under MIN_PX_CHANGE px is refused; a remove or move that empties a
container is refused; a fold cannot move into a band; card.change.linked
edits soft-ringed nodes in B only (the annual-default toggle and its prices);
a back icon leads the header; Turkish messages carry no English phrases; a
quote in a label stays inside its attribute; a short hex colour is refused.
Dependency-free (unittest), Python 3.9+.
"""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
sys.path.insert(0, HERE)
import screen_spec as ss  # noqa: E402
from test_screen_spec import SIMPLE, compiled, gate, problems_of  # noqa: E402


class TestNoOpChanges(unittest.TestCase):
    def test_an_identical_replace_is_refused(self):
        p = problems_of(SIMPLE, {"op": "replace", "target": "cta", "node": {"cta": "Devam", "id": "cta"},
                                 "label": "Aynı buton"})
        self.assertIn("B draws exactly what A draws", p[0])
        self.assertIn("replacement node is the same", p[0])

    def test_a_move_to_where_the_node_already_is_is_refused(self):
        for op, to in (("move_before", "cta"), ("move_after", "h")):
            with self.subTest(op=op):
                p = problems_of(SIMPLE, {"op": op, "target": "mail", "to": to, "label_a": "Eski", "label_b": "Yeni"})
                self.assertIn("lands where it already is", p[0])

    def test_a_hex_case_only_edit_is_refused(self):
        screen = [{"cta": "Devam", "id": "cta", "fg": "#AABBCC"}]
        p = problems_of(screen, {"op": "edit", "target": "cta", "set": {"fg": "#aabbcc"}, "label": "Renk"})
        self.assertIn("differing only in case", p[0])

    def test_a_real_move_still_compiles(self):
        a, b = compiled(SIMPLE, {"op": "move_after", "target": "mail", "to": "cta", "label_a": "Eski", "label_b": "Yeni"})
        self.assertNotEqual(a, b)
        self.assertEqual(gate("move", a, b), [])

    def test_turkish_no_difference_message(self):
        p = problems_of(SIMPLE, {"op": "replace", "target": "cta", "node": {"cta": "Devam", "id": "cta"},
                                 "label": "Aynı"}, lang="tr")
        self.assertIn("birebir aynı", p[0])


class TestSubPerceptualEdits(unittest.TestCase):
    def test_a_one_px_margin_edit_is_refused(self):
        p = problems_of(SIMPLE, {"op": "edit", "target": "cta", "set": {"mb": 17}, "label": "Boşluk"})
        self.assertIn("1px difference", p[0])

    def test_a_small_height_edit_is_refused(self):
        screen = [{"cta": "Devam", "id": "cta", "height": 48}]
        p = problems_of(screen, {"op": "edit", "target": "cta", "set": {"height": 52}, "label": "Yükseklik"})
        self.assertIn("4px difference", p[0])

    def test_a_visible_margin_edit_compiles(self):
        a, b = compiled(SIMPLE, {"op": "edit", "target": "mail", "set": {"mb": 40}, "label": "Boşluk"})
        self.assertIn("margin-bottom:24px", b)


class TestContainers(unittest.TestCase):
    ROW = [{"row": [{"field": "Ay", "id": "ay"}]}, {"cta": "Devam", "id": "cta"}]

    def test_removing_a_rows_only_child_is_refused(self):
        p = problems_of(self.ROW, {"op": "remove", "target": "ay", "label": "Alan kaldırıldı"})
        self.assertIn("leaves the row at card.screen[0] empty in B", p[0])

    def test_moving_a_rows_only_child_out_is_refused(self):
        p = problems_of(self.ROW, {"op": "move_after", "target": "ay", "to": "cta", "label_a": "Eski", "label_b": "Yeni"})
        self.assertIn("empty", p[0])

    def test_a_fold_cannot_move_into_a_band(self):
        screen = [{"h": "Başlık"}, {"fold": True, "id": "fold"},
                  {"band": {"items": [{"field": "Ad", "id": "ad"}, {"field": "Soyad"}]}}]
        p = problems_of(screen, {"op": "move_after", "target": "fold", "to": "ad", "label_a": "Eski", "label_b": "Yeni"})
        self.assertIn("cannot move into a band", p[0])


class TestContainerEdits(unittest.TestCase):
    BAND = [{"band": {"bg": "#f5f5f5", "items": [{"field": "Ad"}, {"field": "Soyad"}, {"field": "Telefon"},
                                                 {"field": "E-posta"}]}, "id": "band"}]

    def test_a_colour_edit_on_a_container_is_refused(self):
        p = problems_of(self.BAND, {"op": "edit", "target": "band", "set": {"fg": "#111111"}, "label": "Renk"})
        self.assertIn("reaches every element inside it", p[0])

    def test_a_content_edit_on_a_container_is_refused(self):
        p = problems_of(self.BAND, {"op": "edit", "target": "band", "set": {"items": []}, "label": "İçerik"})
        self.assertIn('"items" on a band', p[0])

    def test_the_containers_own_background_may_change(self):
        a, b = compiled(self.BAND, {"op": "edit", "target": "band", "set": {"bg": "#ffffff"}, "label": "Zemin"})
        self.assertIn("background:#ffffff", b)


class TestLinkedDifferences(unittest.TestCase):
    PRICING = [
        {"tabs": [{"label": "Aylık", "on": True}, {"label": "Yıllık"}], "id": "toggle"},
        {"plan": {"name": "Temel", "price": "100 TL", "per": "/ay"}, "id": "p1"},
        {"plan": {"name": "Pro", "price": "200 TL", "per": "/ay"}, "id": "p2"},
    ]
    CHANGE = {"op": "edit", "target": "toggle", "set": {"tabs": [{"label": "Aylık"}, {"label": "Yıllık", "on": True}]},
              "label": "Yıllık varsayılan", "label_a": "Aylık varsayılan",
              "linked": [{"target": "p1", "set": {"price": "80 TL"}}, {"target": "p2", "set": {"price": "160 TL"}}]}

    def test_linked_edits_land_in_b_inside_their_soft_rings(self):
        a, b = compiled(self.PRICING, self.CHANGE, soft=[{"id": "p1", "note": "Yıllık fiyat"}, "p2"])
        self.assertIn("100 TL", a)
        self.assertNotIn("80 TL", a)
        self.assertIn("80 TL", b)
        self.assertIn("160 TL", b)
        self.assertEqual(b.count('class="hl-soft"'), 2)
        self.assertEqual(a.count('class="hl-soft"'), 2)
        self.assertEqual(gate("change", a, b), [])

    def test_a_linked_target_outside_card_soft_is_refused(self):
        p = problems_of(self.PRICING, self.CHANGE, soft=["p1"])
        self.assertIn('"p2" is not in card.soft', p[0])

    def test_an_edit_with_linked_differences_needs_label_a(self):
        change = {k: v for k, v in self.CHANGE.items() if k != "label_a"}
        p = problems_of(self.PRICING, change, soft=["p1", "p2"])
        self.assertIn("needs label_a", p[0])

    def test_linked_works_with_every_op(self):
        screen = self.PRICING + [{"help": "Fiyatlara KDV dahildir.", "id": "kdv"}]
        linked = [{"target": "p1", "set": {"price": "80 TL"}}]
        for difference, change in (
                ("add", {"op": "insert_after", "target": "toggle", "node": {"badge": "2 ay bedava"}, "label": "Rozet"}),
                ("remove", {"op": "remove", "target": "toggle", "label": "Seçici kaldırıldı"}),
                ("move", {"op": "move_before", "target": "kdv", "to": "toggle", "label_a": "Eski", "label_b": "Yeni"}),
                ("change", {"op": "replace", "target": "toggle", "node": {"badge": "Yıllık"}, "label": "Yeni",
                            "label_a": "Eski"})):
            change["linked"] = linked
            with self.subTest(op=change["op"]):
                a, b = compiled(screen, change, soft=["p1"])
                self.assertEqual(gate(difference, a, b), [])

    def test_a_malformed_linked_list_is_refused(self):
        change = dict(self.CHANGE, linked=[{"target": "p1"}])
        p = problems_of(self.PRICING, change, soft=["p1"])
        self.assertIn("card.change.linked must be a list", p[0])


class TestHeaderIcons(unittest.TestCase):
    def test_a_back_icon_leads_and_the_others_trail(self):
        screen = [{"header": {"logo": "Mağaza", "icons": [{"icon": "back"}, {"icon": "search"}]}}, {"h": "Sepet", "id": "h"}]
        a, _ = compiled(screen, {"op": "edit", "target": "h", "set": {"h": "Sepetim"}, "label": "Başlık"}, lang="tr")
        back, logo, search = a.index('aria-label="Geri"'), a.index('class="r-logo"'), a.index('aria-label="Ara"')
        self.assertLess(back, logo)
        self.assertLess(logo, search)
        lead = a[:logo]
        self.assertNotIn("margin-left:auto", lead)


class TestMessagesAndValues(unittest.TestCase):
    def test_turkish_messages_carry_no_english_want_phrase(self):
        cases = [
            ([{"h": "X", "id": "h"}], {"op": "insert_after", "target": "h", "node": {"help": "Y"}}),
            ([{"h": "X", "id": "h"}], {"op": "edit", "target": "h", "set": {}, "label": "Z"}),
            ([{"h": "X", "id": "h"}], {"op": "insert_after", "target": "h", "node": {"help": "Y"}, "label": "Z",
                                       "label_pos": "side"}),
            ([{"progress": 140}], {"op": "remove", "target": "x", "label": "Z"}),
            ([{"img": "tall"}], {"op": "remove", "target": "x", "label": "Z"}),
            ([{"h": "X", "mb": "big"}], {"op": "remove", "target": "x", "label": "Z"}),
        ]
        english = re.compile(r"\b(?:a short label|an object of|an integer|a height in|a px integer|a non-empty|"
                             r"true or false|a list of)\b")
        for screen, change in cases:
            problems = ss.compile(screen, change, "tr")[2]
            self.assertTrue(problems)
            for p in problems:
                with self.subTest(p=p):
                    self.assertIsNone(english.search(p), p)

    def test_a_quote_in_a_label_stays_inside_the_attribute(self):
        _, b = compiled(SIMPLE, {"op": "insert_after", "target": "mail", "node": {"help": "Satır"},
                                 "label": 'Yeni "satır" eklendi'})
        self.assertIn('data-note="Yeni &quot;satır&quot; eklendi"', b)

    def test_a_short_hex_colour_is_refused(self):
        problems = ss.compile([{"cta": "Devam", "fg": "#abc"}], {"op": "remove", "target": "x", "label": "Z"})[2]
        self.assertTrue(any('"fg" must be #rrggbb' in p for p in problems), problems)

    def test_a_hex_colour_with_a_trailing_newline_is_refused(self):
        problems = ss.compile([{"cta": "Devam", "fg": "#aabbcc\n"}], {"op": "remove", "target": "x", "label": "Z"})[2]
        self.assertTrue(any('"fg" must be #rrggbb' in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
