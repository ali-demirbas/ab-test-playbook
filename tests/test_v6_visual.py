#!/usr/bin/env python3
"""Contract 7 (visual accuracy) regression tests for the card builder. Stdlib only.

S1 fold split (.r-fold → first view + continuation sheet), pinned bar
   (.r-sticky), card.mobile_toolbar, the pinned-word heuristic.
S2 stages (.r-stage-break + card.stage_captions).
S3 soft ring (.hl-soft), listed as "linked".
S4 neutral identical pills. S5 lighter conditional ribbon. S6 phone_scale 1.4.
Every new rule has a negative and a positive test.
"""
import contextlib
import copy
import io
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import build_card as bc  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
SCHEMA_PATH = os.path.join(REPO_ROOT, "templates", "scenario.schema.json")
with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
STYLE = re.search(r"<style>(.*?)</style>", TEMPLATE, re.S).group(1)
CLASSES = bc.component_classes(TEMPLATE)


def die_text(fn, *args, **kw):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            fn(*args, **kw)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected the builder to refuse; it built instead")


def builds(sc):
    warnings, manifest = [], {}
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            html = bc.final_html(TEMPLATE, sc)[0]
            bc.build(TEMPLATE, sc, warnings=warnings, manifest=manifest)
        except SystemExit:
            raise AssertionError("expected a card, the builder refused:\n" + err.getvalue())
    return html, warnings, manifest


def record(a, b, difference="move", device="phone-web", variable="Ödeme butonunun konumu", **card):
    c = {"variant_a": a, "variant_b": b, "device": device, "url": "magaza.example/sepet"}
    c.update(card)
    return {"title": "Ödeme butonunun yeri ödemeye geçişi artırır mı?", "lang": "tr", "difference": difference,
            "variable": variable, "card": c}


def errors_of(a, b, difference="move", **kw):
    return bc.card_problems(difference, a, b, card_lang="tr", classes=CLASSES, **kw)[0]


def has(errors, text):
    return any(text in e for e in errors)


ITEMS = ('<div class="r-h">Sepetim</div>'
         '<div class="r-line total"><span>Toplam</span><span>1.498 TL</span></div>')
FOLD = '<div class="r-fold"></div>'
BELOW = '<div class="r-info" style="margin-bottom:18px">Siparişin yarın kargoda.</div>'
CTA = '<div class="r-cta">Ödemeye geç</div>'
RING_A = '<div class="hl" data-note="Sayfanın sonunda">%s</div>' % CTA
RING_B = '<div class="hl" data-note="Ekranın altında sabit">%s</div>' % CTA
BAR_B = '<div class="r-sticky">%s</div>' % RING_B
STICKY_A = ITEMS + FOLD + BELOW + RING_A
STICKY_B = ITEMS + BAR_B + FOLD + BELOW


# ------------------------------------------------------------------ S1 fold

class TestFold(unittest.TestCase):
    def test_fold_splits_into_first_view_and_continuation(self):
        a = ITEMS + FOLD + BELOW + RING_A
        b = ITEMS + RING_A.replace("Sayfanın sonunda", "Toplamın altında") + FOLD + BELOW
        html, _, manifest = builds(record(a, b))
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])
        self.assertNotIn("r-fold", html.split("</style>")[1])
        self.assertEqual(html.count('<div class="below"><div class="below-cap">Kaydırınca görünen kısım</div>'
                                    '<div class="below-screen">'), 2)
        # The continuation follows the phone in the same column; the first view stays in the screen.
        first, cont = html.split('<div class="below">', 1)
        self.assertIn('<div class="r-h">Sepetim</div>', first)
        self.assertIn("Siparişin yarın kargoda.", cont)
        self.assertNotIn("Siparişin yarın kargoda.", first)

    def test_english_caption(self):
        sc = record(ITEMS + FOLD + BELOW, ITEMS + FOLD + BELOW.replace("yarın", "yarın"), difference="change")
        sc["card"]["variant_b"] = ITEMS + FOLD + '<div class="hl" data-note="New">%s</div>' % BELOW
        sc["lang"] = "en"
        html = builds(sc)[0]
        self.assertEqual(html.count('<div class="below-cap">Below the first screen</div>'), 2)

    def test_no_fold_builds_without_a_continuation(self):
        html = builds(record(ITEMS + RING_A, RING_A + ITEMS))[0]
        self.assertNotIn('<div class="below">', html)
        self.assertNotIn("has-sticky", html.split("</style>")[1])

    def test_fold_in_one_arm_only_is_refused(self):
        self.assertTrue(has(errors_of(ITEMS + FOLD + BELOW + RING_A, ITEMS + RING_A + BELOW),
                            "only Variant A has a .r-fold"))

    def test_fold_must_be_bare_and_spelled_exactly(self):
        for fold in ('<div class="r-fold" style="margin:4px"></div>', '<div class="r-fold x"></div>',
                     '<div class="r-fold" ></div>', '<div class="r-fold">x</div>'):
            with self.subTest(fold=fold):
                errs = errors_of(ITEMS + fold + BELOW + RING_A, ITEMS + RING_A + fold + BELOW)
                self.assertTrue(has(errs, "write the kıvrım exactly as") or has(errs, "write the fold exactly as"),
                                errs)

    def test_fold_must_be_top_level(self):
        nested = '<div>%s</div>' % FOLD
        self.assertTrue(has(errors_of(ITEMS + nested + BELOW + RING_A, ITEMS + RING_A + nested + BELOW),
                            ".r-fold must be a direct child of the screen"))

    def test_one_fold_per_screen(self):
        self.assertTrue(has(errors_of(ITEMS + FOLD + BELOW + FOLD + RING_A, ITEMS + RING_A + FOLD + BELOW + FOLD),
                            "2 .r-fold in one screen"))

    def test_both_sides_of_the_fold_show_content(self):
        self.assertTrue(has(errors_of(FOLD + ITEMS + RING_A, FOLD + RING_A + ITEMS), "nothing before the .r-fold"))
        self.assertTrue(has(errors_of(ITEMS + RING_A + FOLD, RING_A + ITEMS + FOLD), "nothing after the .r-fold"))

    def test_fold_on_web_is_refused(self):
        msg = die_text(bc.build, TEMPLATE, record(STICKY_A, STICKY_B, device="web"))
        self.assertIn("only valid with device phone or phone-web", msg)


# ------------------------------------------------------------------ S1 pinned bar

class TestStickyBar(unittest.TestCase):
    def test_a_pinned_move_builds_as_one_moved_ring(self):
        self.assertEqual(errors_of(STICKY_A, STICKY_B), [])
        html, warnings, manifest = builds(record(STICKY_A, STICKY_B))
        self.assertEqual(warnings, [])
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])
        self.assertEqual(manifest["changes"], [])  # the bar is the pinned state's drawing, not a change
        # Both arms keep the bar's room at the bottom of the first view, so A and B align.
        self.assertEqual(html.count('<div class="screen has-sticky">'), 2)
        self.assertIn(BAR_B, html)

    def test_the_bar_css(self):
        rule = re.search(r"\.r-sticky\{([^}]*)\}", STYLE).group(1)
        for decl in ("position:absolute", "left:0", "right:0", "bottom:0", "padding:10px 20px",
                     "background:var(--surface)", "border-top:1px solid var(--line)",
                     "box-shadow:0 -2px 8px rgba(17,24,39,.06)"):
            self.assertIn(decl, rule)
        self.assertIn("position:relative", re.search(r"\n  \.screen\{([^}]*)\}", STYLE).group(1))
        self.assertIn("padding-bottom:", re.search(r"\.screen\.has-sticky\{([^}]*)\}", STYLE).group(1))

    def test_changed_content_in_the_bar_is_refused(self):
        b = ITEMS + BAR_B.replace("Ödemeye geç", "Hemen öde") + FOLD + BELOW
        self.assertTrue(has(errors_of(STICKY_A, b), "the ringed element's content differs"))

    def test_bar_without_fold_or_after_it_is_refused(self):
        self.assertTrue(has(errors_of(ITEMS + BELOW + RING_A, ITEMS + BAR_B + BELOW), "the screen needs a .r-fold"))
        self.assertTrue(has(errors_of(STICKY_A, ITEMS + FOLD + BELOW + BAR_B), "the bar comes before it"))

    def test_bar_with_its_own_style_or_class_is_refused(self):
        for bar in ('<div class="r-sticky" style="padding:4px">%s</div>', '<div class="r-sticky r-card">%s</div>'):
            with self.subTest(bar=bar):
                b = ITEMS + bar % RING_B + FOLD + BELOW
                self.assertTrue(has(errors_of(STICKY_A, b), '.r-sticky takes class="r-sticky" only'))

    def test_bar_holds_exactly_one_element(self):
        for inner in (RING_B + '<div class="r-sub">Güvenli ödeme</div>', "Toplam" + RING_B, ""):
            with self.subTest(inner=inner):
                b = ITEMS + '<div class="r-sticky">%s</div>' % inner + FOLD + BELOW
                self.assertTrue(has(errors_of(STICKY_A, b), ".r-sticky holds exactly one element"))

    def test_bar_with_extra_content_is_not_a_ring_wrapper(self):
        b = ITEMS + '<div class="r-sticky">%s<div class="r-sub">Güvenli ödeme</div></div>' % RING_B + FOLD + BELOW
        self.assertTrue(has(errors_of(STICKY_A, b), "A and B differ outside any ring"))

    def test_bar_must_be_top_level(self):
        b = ITEMS + '<div>%s</div>' % BAR_B + FOLD + BELOW
        self.assertTrue(has(errors_of(STICKY_A, b), ".r-sticky must be a direct child of the screen"))

    def test_bar_in_both_arms_around_an_unchanged_element_passes(self):
        bar = '<div class="r-sticky">%s</div>' % CTA
        a = ITEMS + '<div class="r-h">Kupon</div>' + bar + FOLD + BELOW
        b = ITEMS + '<div class="hl" data-note="Kupon başlığı"><div class="r-h">Kupon kodu</div></div>' + bar + FOLD + BELOW
        self.assertEqual(errors_of(a, b, difference="change"), [])
        self.assertEqual(builds(record(a, b, difference="change", variable="Kupon başlığı"))[0]
                         .count('<div class="screen has-sticky">'), 2)


class TestPinnedHeuristic(unittest.TestCase):
    MSG = "a pinned element is drawn as a bar at the bottom of the first view (.r-sticky with .r-fold)"

    def test_pinned_label_without_bar_is_refused(self):
        b = ITEMS + RING_B + FOLD + BELOW
        self.assertTrue(has(errors_of(STICKY_A, b), self.MSG))
        self.assertIn(self.MSG, die_text(bc.build, TEMPLATE, record(STICKY_A, b)))

    def test_every_pinned_word_in_the_variable_or_b_description(self):
        plain = (ITEMS + FOLD + BELOW + RING_A, ITEMS + RING_A.replace("Sayfanın sonunda", "Toplamın altında")
                 + FOLD + BELOW)
        for word in ("Sabit ödeme butonu", "Butonu sabitlenmiş göstermek", "Yapışkan alt bar", "Sticky CTA",
                     "Pinned checkout button", "Fixed checkout button"):
            with self.subTest(word=word):
                self.assertTrue(has(errors_of(*plain, variable=word), self.MSG))
                self.assertTrue(has(errors_of(*plain, change_text=word), self.MSG))
        sc = record(*plain)
        sc["variants"] = [{"id": "A", "description": "Buton sayfanın sonunda."},
                          {"id": "B", "description": "Buton ekranın altına sabitlenir."}]
        self.assertIn(self.MSG, die_text(bc.build, TEMPLATE, sc))

    def test_word_boundaries_and_other_differences_pass(self):
        plain = (ITEMS + FOLD + BELOW + RING_A, ITEMS + RING_A.replace("Sayfanın sonunda", "Toplamın altında")
                 + FOLD + BELOW)
        for text in ("Unpinned button", "Prefixed label", "Ödeme butonunun konumu", "Stickiness score"):
            with self.subTest(text=text):
                self.assertFalse(has(errors_of(*plain, variable=text), self.MSG))
        # Not a move: the heuristic is silent.
        self.assertFalse(has(errors_of(ITEMS, ITEMS + '<div class="hl" data-note="Sabit kargo">%s</div>' % BELOW,
                                       difference="add"), self.MSG))

    def test_drawn_with_the_bar_passes(self):
        self.assertFalse(has(errors_of(STICKY_A, STICKY_B, variable="Sabit ödeme butonu"), self.MSG))

    def test_unpinning_from_a_bar_in_a_passes(self):
        a = ITEMS + '<div class="r-sticky">%s</div>' % RING_A.replace("Sayfanın sonunda", "Sabit bar") + FOLD + BELOW
        b = ITEMS + FOLD + BELOW + RING_A
        errs = errors_of(a, b, variable="Sabit butonu sayfa sonuna almak")
        self.assertFalse(has(errs, self.MSG), errs)


class TestMobileToolbar(unittest.TestCase):
    def test_toolbar_is_drawn_identically_in_both_arms(self):
        html = builds(record(STICKY_A, STICKY_B, mobile_toolbar=True))[0]
        body = html.split("</style>")[1]
        self.assertEqual(body.count(bc.TOOLBAR_HTML), 2)
        self.assertIn('<div class="m-home"><span></span></div>', bc.TOOLBAR_HTML)
        # Inside the phone, right below the screen.
        self.assertRegex(body, r"</div>\n\s*" + re.escape(bc.TOOLBAR_HTML) + r"\n\s*</div>\n\s*\{?<div class=\"below\">")

    def test_without_the_field_no_toolbar(self):
        self.assertNotIn('class="m-toolbar"', builds(record(STICKY_A, STICKY_B))[0])

    def test_toolbar_on_a_native_phone_or_web_is_refused(self):
        for device in ("phone", "web"):
            with self.subTest(device=device):
                sc = record(ITEMS + RING_A, RING_A + ITEMS, device=device, mobile_toolbar=True)
                self.assertIn("card.mobile_toolbar draws a mobile browser's bottom toolbar",
                              die_text(bc.build, TEMPLATE, sc))

    def test_toolbar_must_be_a_boolean(self):
        sc = record(ITEMS + RING_A, RING_A + ITEMS, mobile_toolbar="yes")
        self.assertIn("card.mobile_toolbar must be true or false", die_text(bc.build, TEMPLATE, sc))

    def test_toolbar_survives_the_drift_check(self):
        sc = record(STICKY_A, STICKY_B, mobile_toolbar=True)
        html = bc.final_html(TEMPLATE, sc)[0]
        layout = bc.layout_of(bc.normalize(sc))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            bc.self_verify(html.replace('<span class="mt-share"></span>', ""), TEMPLATE, "phone-web", layout=layout)


# ------------------------------------------------------------------ S2 stages

BRK = '<div class="r-stage-break"></div>'
FIELD = ('<div class="hl" data-note="Telefon burada"><div><div class="r-label">Cep telefonu</div>'
         '<div class="r-field empty">05XX XXX XX XX</div></div></div>')
S1 = '<div class="r-h" style="margin-bottom:20px">Aracınızın bilgileri</div>'
S2 = '<div class="r-h" style="margin-bottom:20px">Teklifiniz hazır</div>'
STAGE_A = S1 + FIELD + BRK + S2 + CTA
STAGE_B = S1 + BRK + S2 + FIELD.replace("Telefon burada", "Telefon teklifte") + CTA
CAPTIONS = ["Araç bilgileri", "Teklif"]


class TestStages(unittest.TestCase):
    def test_two_stages_draw_two_phones_per_arm(self):
        html, _, manifest = builds(record(STAGE_A, STAGE_B, stage_captions=CAPTIONS))
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])
        body = html.split("</style>")[1]
        self.assertEqual(body.count('<div class="phone">'), 4)
        self.assertEqual(body.count('<div class="stages">'), 2)
        self.assertEqual(body.count('<span class="stage-arrow" aria-hidden="true">→</span>'), 2)
        self.assertEqual(body.count('<div class="stage-cap">Araç bilgileri</div>'), 2)
        self.assertEqual(body.count('<div class="stage-cap">Teklif</div>'), 2)
        self.assertNotIn("r-stage-break", body)
        # Stage 2 of B holds the moved field.
        b = body.split("Variant B", 1)[1]
        self.assertLess(b.index("Teklifiniz hazır"), b.index("Telefon teklifte"))

    def test_caption_is_escaped(self):
        html = builds(record(STAGE_A, STAGE_B, stage_captions=["Araç <b>", "Teklif"]))[0]
        self.assertIn('<div class="stage-cap">Araç &lt;b&gt;</div>', html)

    def test_stage_phone_css_keeps_text_at_12px(self):
        rule = re.search(r"\.card \.stage-col>\.phone\{([^}]*)\}", STYLE).group(1)
        zoom = float(re.search(r"zoom:([\d.]+)", rule).group(1))
        self.assertTrue(0.78 <= zoom <= 0.85, zoom)
        self.assertLessEqual(2 * 420 * zoom + 2 * 16 + 22, 728)  # two phones, the arrow, 16px gaps
        for var in ("--fs", "--fs-sm", "--fs-ctl"):
            self.assertGreaterEqual(float(re.search(var + r":([\d.]+)px", rule).group(1)) * zoom, 12)

    def test_captions_are_required_and_counted(self):
        self.assertIn("card.stage_captions needs 2 short captions",
                      die_text(bc.build, TEMPLATE, record(STAGE_A, STAGE_B)))
        self.assertIn("has 3 caption(s) for 2 stage(s)",
                      die_text(bc.build, TEMPLATE, record(STAGE_A, STAGE_B, stage_captions=CAPTIONS + ["Ödeme"])))
        self.assertIn("every caption is a short non-empty text",
                      die_text(bc.build, TEMPLATE, record(STAGE_A, STAGE_B, stage_captions=["Araç", " "])))
        self.assertIn("starts with a lowercase letter",
                      die_text(bc.build, TEMPLATE, record(STAGE_A, STAGE_B, stage_captions=["araç", "Teklif"])))

    def test_captions_without_breaks_are_refused(self):
        self.assertIn("no .r-stage-break", die_text(bc.build, TEMPLATE, record(STICKY_A, STICKY_B,
                                                                              stage_captions=CAPTIONS)))

    def test_same_number_of_breaks_in_both_arms(self):
        self.assertTrue(has(errors_of(STAGE_A, S1 + S2 + FIELD + CTA), "Variant A has 1 .r-stage-break, Variant B 0"))

    def test_at_most_two_stages(self):
        a, b = STAGE_A + BRK + S1, STAGE_B + BRK + S1
        self.assertTrue(has(errors_of(a, b), "2 .r-stage-break in one screen; at most 1"))

    def test_empty_stage_fold_mix_and_web(self):
        self.assertTrue(has(errors_of(BRK + STAGE_A.replace(BRK, ""), BRK + STAGE_B.replace(BRK, "")),
                            "stage 1 is empty"))
        self.assertTrue(has(errors_of(STAGE_A + FOLD + BELOW, STAGE_B + FOLD + BELOW), "don't mix"))
        msg = die_text(bc.build, TEMPLATE, record(STAGE_A, STAGE_B, device="web", stage_captions=CAPTIONS))
        self.assertIn(".r-stage-break draws a phone screen", msg)

    def test_drift_check_covers_the_stage_skeleton(self):
        sc = record(STAGE_A, STAGE_B, stage_captions=CAPTIONS)
        html = bc.final_html(TEMPLATE, sc)[0]
        layout = bc.layout_of(bc.normalize(sc))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            bc.self_verify(html.replace('<span class="stage-arrow" aria-hidden="true">→</span>', ""), TEMPLATE,
                           "phone-web", layout=layout)


# ------------------------------------------------------------------ S3 soft ring

RADIOS = ('<div><div class="r-radio%s">Standart kargo</div>'
          '<div class="r-radio%s" style="margin-top:12px">Hızlı kargo</div></div>')
SHIP_A = '<div class="r-h">Teslimat</div>' + RADIOS % (" on", "")
SHIP_B = '<div class="r-h">Teslimat</div><div class="hl" data-note="Hızlı kargo seçili">%s</div>' % (RADIOS % ("", " on"))
SUM = '<div class="r-card"><div class="r-line" style="margin-bottom:18px"><span>Ürünler</span><span>1.498 TL</span></div>%s</div>'
TOT_A = '<div class="r-line total"><span>Toplam</span><span>1.498 TL</span></div>'
TOT_B = ('<div class="hl-soft" data-note="Toplam güncellenir"><div class="r-line total"><span>Toplam</span>'
         '<span>1.547 TL</span></div></div>')
SOFT_A, SOFT_B = SHIP_A + SUM % TOT_A, SHIP_B + SUM % TOT_B
NUMERIC = "Hızlı kargo seçili gelince toplam kargo ücreti kadar artar."


def soft_record(a=SOFT_A, b=SOFT_B, numeric=NUMERIC):
    sc = record(a, b, difference="change", variable="Varsayılan teslimat seçeneği")
    if numeric:
        sc["numeric_change"] = numeric
    return sc


class TestSoftRing(unittest.TestCase):
    def test_a_linked_consequence_builds_and_is_listed_as_linked(self):
        _, warnings, manifest = builds(soft_record())
        self.assertEqual(warnings, [])
        linked = [r for r in manifest["rings"] if r["kind"] == "linked"]
        self.assertEqual([(r["label"], r["variant"]) for r in linked], [("Toplam güncellenir", "B")])
        self.assertIn({"a": "1.498 TL", "b": "1.547 TL"},
                      [{"a": c["a"], "b": c["b"]} for c in manifest["changes"] if c["label"] == "Toplam güncellenir"])

    def test_the_same_change_without_the_soft_ring_is_still_refused(self):
        b = SHIP_B + SUM % TOT_B.replace('<div class="hl-soft" data-note="Toplam güncellenir">', "<div>")
        b = SHIP_B + SUM % '<div class="r-line total"><span>Toplam</span><span>1.547 TL</span></div>'
        self.assertTrue(has(errors_of(SOFT_A, b, difference="change"), "A and B differ outside any ring"))

    def test_numbers_inside_still_need_numeric_change(self):
        self.assertIn("numbers differ between A and B", die_text(bc.build, TEMPLATE, soft_record(numeric=None)))

    def test_soft_ring_alone_is_refused_and_does_not_place_the_ring(self):
        a, b = SUM % TOT_A, SUM % TOT_B
        errs = errors_of(a, b, difference="change")
        self.assertTrue(has(errs, "the card also needs a .hl around the variable itself"), errs)
        self.assertTrue(has(errs, "difference 'change': ring the changed element in Variant B"), errs)

    def test_at_most_two_per_arm(self):
        soft = '<div class="hl-soft" data-note="Bağlı"><div class="r-sub">Not</div></div>'
        a = SOFT_A + '<div class="r-sub">Not</div>' * 2
        b = SOFT_B + soft * 2
        self.assertTrue(has(errors_of(a, b, difference="change"), "3 .hl-soft rings; at most 2 per arm"))
        self.assertFalse(has(errors_of(SOFT_A + '<div class="r-sub">Not</div>', SOFT_B + soft, difference="change"),
                             ".hl-soft rings; at most"))

    def test_never_nested_with_a_ring_nor_both_at_once(self):
        nested = SHIP_B.replace(RADIOS % ("", " on"), '<div class="hl-soft">%s</div>' % (RADIOS % ("", " on")))
        self.assertTrue(has(errors_of(SOFT_A, nested + SUM % TOT_B, difference="change"), "never inside or around"))
        both = SOFT_B.replace('class="hl-soft"', 'class="hl hl-soft"')
        self.assertTrue(has(errors_of(SOFT_A, both, difference="change"), "not both"))

    def test_no_push_and_capitalised_label(self):
        b = SOFT_B.replace('class="hl-soft" data-note="Toplam güncellenir"',
                           'class="hl-soft" style="margin-top:4px" data-note="toplam güncellenir"')
        errs = errors_of(SOFT_A, b, difference="change")
        self.assertTrue(has(errs, "soft ring in B carries inline margin"), errs)
        self.assertTrue(has(errs, "soft ring label in B starts with a lowercase letter"), errs)

    def test_soft_ring_css(self):
        rule = re.search(r"\n  \.hl-soft\{([^}]*)\}", STYLE).group(1)
        for decl in ("outline:2px dashed var(--ring)", "outline-offset:4px"):
            self.assertIn(decl, rule)
        label = re.search(r"\.hl-soft\[data-note\]::after\{([^}]*)\}", STYLE).group(1)
        for decl in ("background:#ffffff", "color:var(--ring)", "border:1px solid var(--ring)", "font-size:12px"):
            self.assertIn(decl, label)


# ------------------------------------------------------------------ S4-S6

class TestPillsRibbonScale(unittest.TestCase):
    def test_pills_are_identical(self):
        self.assertIn(".pill-a,.pill-b{background:#ffffff;border:1px solid #d1d5db;color:#111827}", STYLE)
        self.assertNotRegex(STYLE, r"(?m)^\s*\.pill-[ab]\{")

    def test_conditional_ribbon_is_light(self):
        style = bc.CONDITIONAL_RIBBON_STYLE
        for decl in ("background:#fffbeb", "color:#92400e", "border:1px solid #fcd34d", "font:600 12px/1",
                     "position:absolute", "top:0", "pointer-events:none"):
            self.assertIn(decl, style)
        self.assertNotIn("#b45309", style)

    def test_phone_scale_accepts_1_1_2_and_1_4(self):
        for value, attr in ((1, "1"), (1.2, "1.2"), (1.4, "1.4")):
            with self.subTest(value=value):
                html = builds(record(ITEMS + RING_A, RING_A + ITEMS, phone_scale=value))[0]
                self.assertIn('data-phone-scale="%s"' % attr, html)
        self.assertIn("zoom:1.4", re.search(r'\.card\[data-phone-scale="1\.4"\] \.phone\{([^}]*)\}', STYLE).group(1))
        self.assertIn("zoom:1.4", re.search(r'\.card\[data-phone-scale="1\.4"\] \.below\{([^}]*)\}', STYLE).group(1))

    def test_other_scales_are_refused(self):
        for value in (1.3, 0.8, "1.4"):
            with self.subTest(value=value):
                msg = die_text(bc.build, TEMPLATE, record(ITEMS + RING_A, RING_A + ITEMS, phone_scale=value))
                self.assertIn("card.phone_scale must be 1, 1.2 (default) or 1.4", msg)


CHIPS = '<div class="r-chips"><span class="r-chip%s">Aylık</span><span class="r-chip%s">Yıllık</span></div>'


class TestMovedModifierClass(unittest.TestCase):
    """A selection moving between siblings (.on from "Aylık" to "Yıllık") keeps its count but is a change."""

    def test_inside_the_ring_the_manifest_lists_it_on_each_element(self):
        a = '<div class="r-h">Plan</div>' + CHIPS % (" on", "")
        b = '<div class="r-h">Plan</div><div class="hl" data-note="Yıllık varsayılan">%s</div>' % (CHIPS % ("", " on"))
        html, _, manifest = builds(record(a, b, difference="change", variable="Varsayılan dönem"))
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["changed"])
        moved = [(c["change"], c["value"], c["at"]) for c in manifest["changes"] if c["kind"] == "class"]
        self.assertEqual(moved, [("removed", "on", "Aylık"), ("added", "on", "Yıllık")])
        # The manifest only: the card's bytes don't depend on it.
        self.assertEqual(html, bc.final_html(TEMPLATE, record(a, b, difference="change",
                                                               variable="Varsayılan dönem"))[0])

    def test_a_count_change_is_not_listed_twice(self):
        a = '<div class="r-h">Plan</div>' + CHIPS % ("", "")
        b = '<div class="r-h">Plan</div><div class="hl" data-note="Yıllık seçili">%s</div>' % (CHIPS % ("", " on"))
        _, _, manifest = builds(record(a, b, difference="change", variable="Varsayılan dönem"))
        self.assertEqual(len([c for c in manifest["changes"] if c["kind"] == "class"]), 1)

    def test_outside_any_ring_it_is_refused(self):
        ring = '<div class="hl" data-note="Yeni başlık"><div class="r-h">Plan seç</div></div>'
        a = '<div class="r-h">Plan</div>' + CHIPS % (" on", "")
        b = ring + CHIPS % ("", " on")
        self.assertTrue(has(errors_of(a, b, difference="change"), "A and B differ outside any ring"))


class TestSchemaFields(unittest.TestCase):
    def setUp(self):
        with open(SCHEMA_PATH, encoding="utf-8") as fh:
            self.card = json.load(fh)["properties"]["card"]["properties"]

    def test_new_card_fields(self):
        self.assertEqual(self.card["phone_scale"]["enum"], [1.2, 1, 1.4])
        self.assertEqual(self.card["mobile_toolbar"]["type"], "boolean")
        self.assertEqual((self.card["stage_captions"]["minItems"], self.card["stage_captions"]["maxItems"]), (2, 2))
        self.assertIn(".example", self.card["url"]["description"])

    def test_the_validator_accepts_and_refuses_them_by_shape(self):
        with open(os.path.join(REPO_ROOT, "examples", "scenario.json"), encoding="utf-8") as fh:
            sc = json.load(fh)
        schema = vsj.load_schema()
        good = copy.deepcopy(sc)
        good["card"].update(device="phone-web", url="magaza.example", mobile_toolbar=True, phone_scale=1.4)
        self.assertFalse([e for e in vsj.validate(good, schema, "en") if "mobile_toolbar" in e or "phone_scale" in e])
        bad = copy.deepcopy(sc)
        bad["card"].update(mobile_toolbar="yes", stage_captions=["Tek"], phone_scale=1.3)
        errs = " ".join(vsj.validate(bad, schema, "en"))
        for field in ("mobile_toolbar", "stage_captions", "phone_scale"):
            self.assertIn(field, errs)


if __name__ == "__main__":
    unittest.main()
