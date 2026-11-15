#!/usr/bin/env python3
"""3.4 card work. Stdlib only; the browser classes run when Playwright is found.

1 Pills: 16px, in the card's language, "· Mevcut" / "· Current" when A is the user's page.
2 Title: a one-line title sits on the pills (no gap above them).
3 Photo placeholder: a soft gradient and a picture icon.
4 Pinned-bar card: the arm without the bar shows the page going on (.r-peek), not 100px of white.
5 card.theme "dark".
6 Desktop components: logos, price, stars, cols, align (h, sub, cta, link, stack), plan old/note,
  the right-aligned nav, a desktop button at its own width, the fold line on a desktop page.
7 Phone sizes come in steps.
8 --share: a 1200 x 630 variant of the final card. --overview: one page of a turn's cards.
"""
import contextlib
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import build_card as bc  # noqa: E402
import screen_spec as ss  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

REPO = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO, "templates", "scenario-card.html")
BUILD = os.path.join(REPO, "scripts", "build_card.py")
SCRIPT = os.path.join(REPO, "scripts", "render_check.mjs")
with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
STYLE = re.sub(r"/\*.*?\*/", "", re.search(r"<style>(.*?)</style>", TEMPLATE, re.S).group(1), flags=re.S)
NODE = shutil.which("node")


def example():
    with open(os.path.join(REPO, "examples", "scenario.json"), encoding="utf-8") as fh:
        return json.load(fh)


def rule(selector):
    m = re.search(r"(?:^|\})\s*%s\{([^}]*)\}" % re.escape(selector), STYLE)
    assert m, "no CSS rule %s" % selector
    return m.group(1)


def quiet(fn, *args, **kw):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            return fn(*args, **kw)
        except SystemExit:
            raise AssertionError("refused:\n" + err.getvalue())


def refused(fn, *args, **kw):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            fn(*args, **kw)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected a refusal")


def spec(screen, change, device="web", lang="tr", title="Logoları ilk ekrana taşımak demo talebini artırır mı?",
         **card):
    c = {"screen": screen, "change": change, "device": device, "url": "rotaplan.example"}
    c.update(card)
    return {"title": title, "lang": lang, "difference": ss.OP_DIFFERENCE[change["op"]], "variable": "Logo şeridi",
            "card": c}


def built(sc):
    return quiet(bc.final_html, TEMPLATE, sc)[0]


def stamped(sc):
    sc = copy.deepcopy(sc)
    sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}}
    sc["review"]["mockup_reviewer"] = {"verdict": "PASS", "fingerprint": quiet(bc.mockup_stamp, TEMPLATE, sc)}
    return sc


def body(html):
    return html[html.index("<body>"):]


FEATURE = lambda text: {"stack": {"items": [{"img": 90}, {"text": text}], "gap": 8}}  # noqa: E731
LANDING = [
    {"header": {"logo": "Rotaplan", "nav": ["Ürün", "Çözümler", "Fiyatlar", "Giriş yap"]}},
    {"stack": {"align": "center", "items": [{"h": "Saha ekibinizin rotasını dakikalar içinde planlayın", "mb": 6},
                                            {"sub": "Rota planlama yazılımı."}, {"cta": "Demo iste"}]}, "id": "hero"},
    {"fold": True},
    {"h": "Neler yapabilirsiniz?", "align": "center"},
    {"cols": [FEATURE("Rota optimizasyonu"), FEATURE("Canlı araç takibi"), FEATURE("Teslimat kanıtı")]},
    {"logos": ["Nordika", "Pera Lojistik", "Ege Servis", "Mavi Kargo"], "caption": "Ekipler Rotaplan kullanıyor",
     "id": "logolar"},
    {"cta": "Demo iste", "style": "outline", "align": "center"},
]
MOVE_LOGOS = {"op": "move_after", "target": "logolar", "to": "hero", "label_a": "Logolar sayfanın altında",
              "label_b": "Logolar ilk ekranda", "label_pos": "below"}
PRODUCT = [
    {"header": {"logo": "Ketenci", "nav": ["Kadın", "Erkek", "Ev"]}},
    {"row": [{"img": 220}, {"stack": {"items": [
        {"h": "Keten Gömlek", "mb": 4}, {"stars": "4,6", "count": "128 değerlendirme"},
        {"price": "1.290 TL", "old": "1.590 TL", "per": "KDV dahil", "id": "fiyat"},
        {"cta": "Sepete ekle", "id": "cta"}]}}]},
]


class TestPills(unittest.TestCase):
    def test_sixteen_pixels_one_neutral_style(self):
        pill = rule(".pill")
        for decl in ("font-size:16px", "font-weight:700", "padding:8px 18px"):
            self.assertIn(decl, pill)
        self.assertIn("background:#ffffff;border:1px solid #d1d5db;color:#111827", rule(".pill-a,.pill-b"))

    def test_turkish_card_turkish_pills(self):
        html = body(built(example()))
        self.assertIn('<span class="pill pill-a">Varyant A</span>', html)
        self.assertIn('<span class="pill pill-b">Varyant B</span>', html)
        self.assertNotIn("Variant", html)

    def test_english_card_english_pills(self):
        html = body(built(spec(LANDING, MOVE_LOGOS, lang="en", title="Do logos above the fold lift demos?")))
        self.assertIn('<span class="pill pill-a">Variant A</span>', html)
        self.assertIn('<span class="pill pill-b">Variant B</span>', html)

    def test_current_page_suffix_only_on_a(self):
        sc = example()
        sc["variants"][0]["is_current"] = True
        html = body(built(sc))
        self.assertIn('<span class="pill pill-a">Varyant A · Mevcut</span>', html)
        self.assertIn('<span class="pill pill-b">Varyant B</span>', html)
        en = spec(LANDING, MOVE_LOGOS, lang="en", title="Do logos above the fold lift demos?")
        en["variants"] = [{"id": "A", "description": "Logos at the end", "is_current": True},
                          {"id": "B", "description": "Logos on the first screen"}]
        self.assertIn('<span class="pill pill-a">Variant A · Current</span>', body(built(en)))

    def test_the_pill_height_is_the_budget(self):
        self.assertEqual(bc.PILL_H, 34)
        self.assertEqual(bc.FRAME_BUDGET, bc.STAGE_H - bc.PILL_H - 10)


class TestTitleAndPlaceholder(unittest.TestCase):
    def test_a_one_line_title_sits_on_the_pills(self):
        title = rule(".title")
        self.assertIn("min-height:75px", title)  # the pills still start at one y on every card
        self.assertIn("justify-content:flex-end", title)

    def test_photo_placeholder_has_a_gradient_and_an_icon(self):
        self.assertIn("linear-gradient", rule(".ph.img"))
        self.assertIn("clip-path:polygon", rule(".ph.img::before"))
        self.assertIn("border-radius:50%", rule(".ph.img::after"))
        self.assertIn("linear-gradient", rule(".r-thumb,.ph.img.r-thumb"))


HEAD = ('<div class="r-h">Ödeme</div><div class="r-item"><div class="ph img r-thumb"></div><div class="r-item-body">'
        '<div class="r-name">Seramik Demlik</div><div class="r-meta">1 adet</div></div><div class="r-price">640 TL</div>'
        '</div><div class="r-label">Teslimat</div>')
STICKY_A = (HEAD + '<div class="r-radio on">Standart kargo</div><div class="r-fold"></div>'
            '<div class="r-line"><span>Ara toplam</span><span>640 TL</span></div>'
            '<div class="hl" data-note="Sayfanın sonunda"><div class="r-cta">Siparişi tamamla</div></div>')
STICKY_B = (HEAD + '<div class="r-radio on">Standart kargo</div>'
            '<div class="r-sticky"><div class="hl" data-note="Ekranın altında sabit"><div class="r-cta">Siparişi '
            'tamamla</div></div></div><div class="r-fold"></div>'
            '<div class="r-line"><span>Ara toplam</span><span>640 TL</span></div>')


def sticky_record():
    return {"title": "Düğmeyi ekranın altına sabitlemek siparişi artırır mı?", "lang": "tr", "difference": "move",
            "variable": "Düğmenin konumu",
            "variants": [{"id": "A", "description": "Düğme sayfanın sonunda"},
                         {"id": "B", "description": "Aynı düğme ekranın altında sabit"}],
            "card": {"device": "phone-web", "url": "ocak.example/odeme", "variant_a": STICKY_A,
                     "variant_b": STICKY_B}}


class TestPinnedBarPeek(unittest.TestCase):
    def test_both_first_views_carry_the_unringed_continuation(self):
        html = body(built(sticky_record()))
        line = '<div class="r-line"><span>Ara toplam</span><span>640 TL</span></div>'
        self.assertEqual(html.count('<div class="r-peek"'), 2)
        # Each arm's own continuation without its ring: A's ends with the button, B's button is in the bar.
        self.assertEqual(html.count('<div class="r-peek" aria-hidden="true">%s<div><div class="r-cta">Siparişi '
                                    'tamamla</div></div></div>' % line), 1)
        self.assertEqual(html.count('<div class="r-peek" aria-hidden="true">%s</div>' % line), 1)
        # The rings are where they were: A's at the end of the continuation, B's in the bar.
        self.assertEqual(html.count('data-note="Sayfanın sonunda"'), 1)
        self.assertEqual(html.count('data-note="Ekranın altında sabit"'), 1)

    def test_the_peek_shows_only_where_there_is_no_bar(self):
        self.assertIn("display:none", rule(".r-peek"))
        self.assertIn("display:none", rule(".screen.has-sticky:has(>.r-sticky)>.r-peek"))
        shown = rule(".screen.has-sticky>.r-peek")
        for decl in ("position:absolute", "bottom:0", "overflow:hidden", "mask-image"):
            self.assertIn(decl, shown)

    def test_a_fold_without_a_bar_has_no_peek(self):
        sc = sticky_record()
        sc["card"]["variant_b"] = STICKY_A.replace("Sayfanın sonunda", "Sonda yeşil").replace(
            'class="r-cta"', 'class="r-cta outline"')
        sc["difference"] = "change"
        self.assertNotIn("r-peek", body(quiet(bc.build, TEMPLATE, sc)))

    def test_unringed_takes_off_rings_and_keeps_the_rest(self):
        self.assertEqual(bc.unringed('<div class="r-card hl" data-note="X" data-pos="below" style="max-width:320px">'
                                     '<div class="hl-soft" data-note="Y"><b>1</b></div></div>'),
                         '<div class="r-card" style="max-width:320px"><div><b>1</b></div></div>')
        self.assertEqual(bc.unringed('<div class="r-h">Hl</div>'), '<div class="r-h">Hl</div>')


class TestDarkTheme(unittest.TestCase):
    def test_default_is_light(self):
        self.assertIn('data-theme="light"', built(example()))

    def test_dark_card(self):
        sc = example()
        sc["card"]["theme"] = "dark"
        html = body(built(sc))
        self.assertIn('data-theme="dark"', html)
        light = body(built(example()))
        # Only the attribute differs: the mockups are the same page.
        self.assertEqual(html.replace('data-theme="dark"', 'data-theme="light"'), light)

    def test_dark_rules_keep_mockups_light(self):
        self.assertIn("background:#0f172a", rule('.card[data-theme="dark"]'))
        self.assertIn("color:#f1f5f9", rule('.card[data-theme="dark"] .title'))
        self.assertIn("color:#cbd5e1", rule('.card[data-theme="dark"] .below-cap,.card[data-theme="dark"] .stage-cap'))
        self.assertNotIn('[data-theme="dark"] .screen', STYLE)

    def test_unknown_theme_is_refused(self):
        sc = example()
        sc["card"]["theme"] = "sepia"
        self.assertIn("card.theme", refused(bc.build, TEMPLATE, sc))


def compiled(screen, change, lang="tr", soft=None):
    a, b, problems = ss.compile(screen, change, lang, soft)
    assert not problems, problems
    return a, b


def problems_of(node, lang="en"):
    out = []
    ss._parse(node, "card.screen[0]", True, lang, out, {})
    return out


class TestDesktopComponents(unittest.TestCase):
    def test_logos(self):
        a, _ = compiled([{"logos": ["Nordika", "Ege"], "id": "l"}, {"h": "X", "id": "h"}],
                        {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn('<div class="r-logos"><div class="r-logos-row"><span>Nordika</span><span>Ege</span></div></div>', a)
        self.assertTrue(problems_of({"logos": []}))
        self.assertTrue(problems_of({"logos": ["", "Ege"]}))
        self.assertTrue(problems_of({"logos": ["A"], "caption": ""}))

    def test_price(self):
        a, _ = compiled([{"price": "$29", "per": "/mo", "id": "p"}, {"h": "X", "id": "h"}],
                        {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn('<div class="r-amount"><span class="r-big">$29</span><span class="r-per">/mo</span></div>', a)
        self.assertTrue(problems_of({"price": 29}))

    def test_stars(self):
        self.assertEqual(ss.stars_value("4,4"), ("4,4", 4.4))
        self.assertEqual(ss.stars_value(4.6, "tr"), ("4,6", 4.6))
        self.assertEqual(ss.stars_value(4.6, "en"), ("4.6", 4.6))
        self.assertEqual(ss.stars_value(5), ("5", 5.0))
        for bad in ("5,5", "4.44.", "dört", True, -1, 6, "45"):
            self.assertIsNone(ss.stars_value(bad), bad)
            self.assertTrue(problems_of({"stars": bad}), bad)
        a, _ = compiled([{"stars": 4.5, "id": "s"}, {"h": "X", "id": "h"}],
                        {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"}, lang="en")
        self.assertIn('aria-label="4.5 out of 5">★★★★★</span><span class="r-meta">4.5</span>', a)  # half up
        a, _ = compiled([{"stars": "3,2", "count": "12", "id": "s"}, {"h": "X", "id": "h"}],
                        {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn('aria-label="5 üzerinden 3,2">★★★☆☆</span><span class="r-meta">3,2 (12)</span>', a)

    def test_cols(self):
        self.assertTrue(problems_of({"cols": [{"text": "Tek"}]}))
        self.assertTrue(problems_of({"cols": [{"text": str(i)} for i in range(5)]}))
        a, _ = compiled([{"cols": [{"text": "A"}, {"text": "B"}], "id": "c"}, {"h": "X", "id": "h"}],
                        {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn('<div class="r-cols"><div>A</div><div>B</div></div>', a)

    def test_removing_a_column_keeps_the_grid(self):
        screen = [{"cols": [{"text": "A", "id": "a"}, {"text": "B"}, {"text": "C"}]}]
        a, b = compiled(screen, {"op": "remove", "target": "a", "label": "Sütun kaldırıldı"})
        self.assertIn('<div class="r-cols c3">', a)
        self.assertIn('<div class="r-cols c3">', b)  # the container is the same in both arms
        errors, _ = bc.card_problems("remove", a, b, lang="en")
        self.assertEqual(errors, [])

    def test_align(self):
        a, b = compiled([{"h": "Başlık", "align": "center", "id": "h"}, {"sub": "Alt", "align": "center"},
                         {"cta": "Demo iste", "align": "center", "id": "c"}, {"link": "Daha fazla", "align": "left"}],
                        {"op": "edit", "target": "c", "set": {"cta": "Ücretsiz dene"}, "label": "Yeni metin"})
        self.assertIn('<div class="r-h" style="text-align:center;margin-bottom:0px">', a.replace(
            'style="text-align:center"', 'style="text-align:center;margin-bottom:0px"', 1))
        self.assertIn('<div class="r-cta" style="align-self:center">Demo iste</div>', a)
        self.assertIn('<div class="r-link" style="align-self:flex-start">Daha fazla</div>', a)
        # Ringed, the button keeps its width: the alignment moves onto the ring.
        self.assertIn('<div class="hl" data-note="Yeni metin" style="align-self:center"><div class="r-cta">Ücretsiz dene'
                      '</div></div>', b)
        errors, _ = bc.card_problems("change", a, b, lang="en")
        self.assertEqual(errors, [])
        self.assertTrue(problems_of({"badge": "Yeni", "align": "center"}))
        self.assertTrue(problems_of({"h": "X", "align": "right"}))

    def test_centred_stack(self):
        a, _ = compiled([{"stack": {"align": "center", "items": [{"h": "Bir"}, {"cta": "İki"}]}, "id": "s"},
                         {"h": "X", "id": "h"}], {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn('style="display:flex;flex-direction:column;align-items:center;text-align:center"', a)
        self.assertTrue(problems_of({"stack": {"items": [{"h": "X"}], "align": "middle"}}))

    def test_plan_old_price_and_note(self):
        plan = {"plan": {"name": "Team", "price": "$29", "old": "$39", "per": "/mo", "note": "Billed yearly",
                         "cta": "Start"}, "id": "team"}
        a, b = compiled([plan], {"op": "edit", "target": "team", "set": {"note": "Billed monthly"},
                                 "label": "New billing line"}, lang="en")
        self.assertIn('<div class="r-plan-price"><span class="r-old">$39</span>$29<span class="r-per">/mo</span></div>'
                      '<div class="r-plan-note">Billed yearly</div>', a)
        self.assertIn('<div class="hl" data-note="New billing line"><div class="r-plan-note">Billed monthly</div></div>', b)
        _, b = compiled([plan], {"op": "edit", "target": "team", "set": {"old": "$49"}, "label": "New old price"},
                        lang="en")
        self.assertIn('<div class="hl" data-note="New old price"><div class="r-plan-price">', b)  # the price part

    def test_template_defines_every_new_class(self):
        classes = bc.component_classes(TEMPLATE)
        for cls in ("r-logos", "r-logos-cap", "r-logos-row", "r-amount", "r-big", "r-rating", "r-cols", "r-plan-note",
                    "r-peek"):
            self.assertIn(cls, classes)

    def test_desktop_nav_is_right_aligned_and_buttons_take_their_width(self):
        self.assertIn("justify-content:flex-end", rule(".browser .r-nav:last-child"))
        self.assertIn("align-self:flex-start", rule(".browser-screen>.r-cta,.browser-screen>.hl:has(>.r-cta:only-child)"))
        self.assertIn("min-width:%dpx" % bc.WEB_CTA_MIN, STYLE)


class TestDesktopFold(unittest.TestCase):
    def test_a_desktop_page_draws_the_fold_where_it_stands(self):
        sc = spec(LANDING, MOVE_LOGOS)
        html = built(sc)
        view = bc.normalize(sc)
        self.assertFalse(bc.layout_of(view)["fold"])
        self.assertEqual(body(html).count('<div class="r-fold"></div>'), 2)  # one line per arm, in the page
        self.assertNotIn('class="below"', body(html))
        self.assertIn("border-top:2px dashed", rule(".browser-screen>.r-fold::before"))
        self.assertIn("İlk ekranın sonu", rule('html[lang="tr"] .browser-screen>.r-fold::after'))
        self.assertIn("End of first screen", rule('html[lang="en"] .browser-screen>.r-fold::after'))
        # B's logos are above the line, A's below it.
        a, b = view["variant_a"], view["variant_b"]
        self.assertLess(a.index("r-fold"), a.index("Nordika"))
        self.assertLess(b.index("Nordika"), b.index("r-fold"))

    def test_a_pinned_bar_stays_a_phone_thing(self):
        screen = [{"h": "X", "id": "h"}, {"sticky": {"cta": "Al"}}, {"fold": True}, {"text": "Alt"}]
        sc = spec(screen, {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn(".r-sticky", refused(bc.build, TEMPLATE, sc))

    def test_the_fold_in_one_arm_is_still_refused(self):
        sc = spec([{"h": "X", "id": "h"}, {"text": "Alt"}],
                  {"op": "insert_after", "target": "h", "node": {"fold": True}, "label": "Çizgi"})
        out = io.StringIO()
        with contextlib.redirect_stderr(out):
            with self.assertRaises(SystemExit):
                bc.build(TEMPLATE, sc)

    def test_the_estimate_counts_the_line(self):
        tree = bc.parse_markup(bc.normalize(spec(LANDING, MOVE_LOGOS))["variant_a"])[0]
        with_line = bc.frame_estimate(tree, "web", {})[0]
        without = bc.frame_estimate(bc.parse_markup(bc.normalize(spec(
            [n for n in LANDING if "fold" not in n], MOVE_LOGOS))["variant_a"])[0], "web", {})[0]
        self.assertAlmostEqual(with_line - without, bc.WEB_FOLD_H + 4 + 16, delta=1)


class TestEstimates(unittest.TestCase):
    def lay(self, markup, device="web"):
        tree = bc.parse_markup(markup)[0]
        lay = bc._Layout(device)
        h, flat = lay.screen(tree.kids, bc.COLUMN_W - 2)
        return {bc._node_text(b.node) if b.node is not None else "": (x, y, b) for b, x, y, _ in flat}

    def test_a_desktop_button_at_the_top_level_takes_its_own_width(self):
        boxes = self.lay('<div class="r-cta">Demo iste</div><div class="r-row"><div class="r-cta">Tam</div></div>')
        self.assertEqual(boxes["Demo iste"][2].w, bc.WEB_CTA_MIN)
        self.assertGreater(boxes["Tam"][2].w, 300)  # a row's button fills its share
        phone = self.lay('<div class="r-cta">Demo iste</div>', "phone")
        self.assertGreater(phone["Demo iste"][2].w, 300)

    def test_a_ring_around_it_is_as_wide_as_the_button(self):
        tree = bc.parse_markup('<div class="hl" data-note="Yeni"><div class="r-cta">Demo iste</div></div>')[0]
        _, flat = bc._Layout("web").screen(tree.kids, bc.COLUMN_W - 2)
        ring = [b for b, _, _, _ in flat if b.node is not None and b.node.is_ring][0]
        self.assertEqual(ring.w, bc.WEB_CTA_MIN)

    def test_a_centred_stack_centres_its_children(self):
        boxes = self.lay('<div style="display:flex;flex-direction:column;align-items:center;text-align:center">'
                         '<div class="r-h">Kısa</div><div class="r-cta">Demo iste</div></div>')
        x, _, box = boxes["Demo iste"]
        inner = bc.COLUMN_W - 2 - 48
        self.assertAlmostEqual(x - 24 + box.w / 2, inner / 2, delta=1)
        self.assertLess(boxes["Kısa"][2].w, 100)

    def test_new_components_have_heights(self):
        a = bc.normalize(spec(LANDING, MOVE_LOGOS))["variant_a"]
        tree = bc.parse_markup(a)[0]
        lay = bc._Layout("web")
        for cls, low, high in (("r-logos-row", 20, 60), ("r-cols", 100, 200), ("r-logos", 40, 90)):
            node = next(n for n in bc._walk(tree) if cls in n.classes)
            h = lay.lay(node, bc.COLUMN_W - 50, (16, 400, 1.45)).h
            self.assertTrue(low <= h <= high, (cls, h))


class TestPhoneSteps(unittest.TestCase):
    def test_a_phone_from_one_up_is_drawn_at_a_step(self):
        form = [{"h": "Create your account", "id": "head"}, {"sub": "It takes a minute."}]
        fields = [{"field": "Field %d" % i, "label": "Label %d" % i} for i in range(9)]
        for n in range(0, 10):
            sc = spec(form + fields[:n] + [{"cta": "Continue"}],
                      {"op": "edit", "target": "head", "set": {"h": "Start now"}, "label": "New headline"},
                      device="phone-web", lang="en", title="Does a clearer headline lift sign-ups?")
            scale = bc.card_layout(bc.normalize(sc))["scale"]
            with self.subTest(fields=n, scale=scale):
                if scale >= 1:
                    self.assertIn(scale, bc.PHONE_STEPS)
                else:
                    self.assertGreaterEqual(scale, bc.AUTO_SCALE_MIN)


def _write(path, text):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class TestShare(unittest.TestCase):
    def test_a_phone_card_puts_the_title_beside_the_frames(self):
        sc = example()
        html = built(sc)
        view = bc.normalize(sc)
        share = bc.share_html(html, view, bc.card_layout(view)["scale"])
        self.assertIn('<meta name="abtest-variant" content="share">', share)
        self.assertIn('<div class="card" data-share="side" ', share)
        self.assertIn("width:1200px;height:630px", share)
        zoom = float(re.search(r'\.card\[data-share="side"\] \.stage\{flex:0 0 auto;zoom:([\d.]+)', share).group(1))
        self.assertTrue(0.5 < zoom < 1.0, zoom)
        # The card's own bytes are all still there: the share adds, it doesn't redraw.
        self.assertIn(body(html).split('<div class="card"', 1)[1].split(">", 1)[1], share)

    def test_a_desktop_card_puts_the_title_on_top(self):
        sc = spec(LANDING, MOVE_LOGOS)
        view = bc.normalize(sc)
        share = bc.share_html(built(sc), view, bc.card_layout(view)["scale"])
        self.assertIn('data-share="top"', share)
        self.assertIn("grid-template-columns:repeat(2,%dpx)" % bc.COLUMN_W, share)

    def test_long_titles_get_a_smaller_size(self):
        short = bc._share_title("Kısa bir soru?", 300, 558)[0]
        long = bc._share_title(" ".join(["uzun"] * 40), 300, 558)[0]
        self.assertGreater(short, long)

    def test_share_path(self):
        self.assertEqual(bc.share_path("/x/abtest-card-kupon.html"), "/x/abtest-card-kupon.share.html")
        self.assertEqual(os.path.basename(bc.png_path(bc.share_path("/x/abtest-card-kupon.html"))),
                         "card-kupon.share.png")

    def run_build(self, args):
        env = dict(os.environ, ABTEST_NO_PNG="1")
        return subprocess.run([sys.executable, BUILD, "--template", TEMPLATE_PATH] + args, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, universal_newlines=True, env=env, timeout=180)

    def test_the_final_build_writes_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = os.path.join(tmp, "kupon.json")
            _write(rec, json.dumps(stamped(example()), ensure_ascii=False))
            out = os.path.join(tmp, "abtest-card-kupon.html")
            p = self.run_build(["--scenario", rec, "--out", out, "--share"])
            self.assertEqual(p.returncode, 0, p.stderr)
            share = bc.share_path(out)
            self.assertTrue(os.path.isfile(share))
            self.assertIn("share: %s" % share, p.stdout)
            with open(out, encoding="utf-8") as fh:
                card = fh.read()
            with open(share, encoding="utf-8") as fh:
                self.assertEqual(fh.read(), bc.share_html(card, bc.normalize(example()),
                                                          bc.card_layout(bc.normalize(example()))["scale"]))

    def test_a_draft_has_no_share(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = os.path.join(tmp, "kupon.json")
            _write(rec, json.dumps(stamped(example()), ensure_ascii=False))
            p = self.run_build(["--scenario", rec, "--out", os.path.join(tmp, "d.html"), "--draft", "--share"])
            self.assertEqual(p.returncode, 2)
            self.assertIn("--share belongs to the final build", p.stderr)

    def test_an_unreviewed_record_writes_no_share(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = os.path.join(tmp, "kupon.json")
            sc = example()
            sc.pop("review", None)
            _write(rec, json.dumps(sc, ensure_ascii=False))
            out = os.path.join(tmp, "abtest-card-kupon.html")
            p = self.run_build(["--scenario", rec, "--out", out, "--share"])
            self.assertEqual(p.returncode, 1)
            self.assertFalse(os.path.exists(bc.share_path(out)))


class TestOverview(unittest.TestCase):
    def cards(self, tmp):
        one = built(example())
        sc = spec(LANDING, MOVE_LOGOS)
        two = built(sc)
        paths = [os.path.join(tmp, "abtest-card-kupon.html"), os.path.join(tmp, "alt klasör", "abtest-card-logo.html")]
        os.makedirs(os.path.dirname(paths[1]))
        _write(paths[0], one)
        _write(paths[1], two)
        return paths

    def test_one_page_with_every_card(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.cards(tmp)
            out = os.path.join(tmp, "ozet.html")
            p = subprocess.run([sys.executable, BUILD, "--overview", out] + paths, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("overview: %s (2 card(s))" % out, p.stdout)
            with open(out, encoding="utf-8") as fh:
                page = fh.read()
            self.assertTrue(page.startswith(bc.PROVENANCE))
            self.assertIn('<html lang="tr">', page)
            self.assertIn("<title>A/B test kartları (2)</title>", page)
            self.assertEqual(page.count("<iframe srcdoc="), 2)
            self.assertIn('href="abtest-card-kupon.html"', page)
            self.assertIn('href="alt%20klas%C3%B6r/abtest-card-logo.html"', page)
            self.assertIn("1. Kupon alanını", page)
            self.assertIn("2. Logoları ilk ekrana", page)
            self.assertNotIn("<script", page.replace("&lt;script", ""))
            self.assertNotRegex(page, r'\ssrc="')  # the thumbnails are the cards themselves, no image file

    def test_drafts_and_foreign_files_are_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.cards(tmp)
            draft = os.path.join(tmp, "taslak.html")
            _write(draft, bc.draft_html(built(example()), "tr"))
            other = os.path.join(tmp, "baska.html")
            _write(other, "<html><body>x</body></html>")
            out = os.path.join(tmp, "ozet.html")
            p = subprocess.run([sys.executable, BUILD, "--overview", out, paths[0], draft, other, "--lang", "tr"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
            self.assertEqual(p.returncode, 1)
            self.assertIn("bir taslak", p.stderr)
            self.assertIn("bu aracın kurduğu bir kart değil", p.stderr)
            self.assertFalse(os.path.exists(out))

    def test_the_conditional_tag_and_the_page_language(self):
        sc = example()
        sc["assumptions"] = [{"type": "critical", "text": "Kupon sistemi bağlantıyla çalışır.",
                              "question": "Kupon alanı bağlantıyla açılabiliyor mu?"}]
        html = built(sc)
        en = built(spec(LANDING, MOVE_LOGOS, lang="en", title="Do logos above the fold lift demos?"))
        with tempfile.TemporaryDirectory() as tmp:
            page = bc.overview_html([(os.path.join(tmp, "a.html"), html), (os.path.join(tmp, "b.html"), en)],
                                    os.path.join(tmp, "o.html"))
        self.assertIn('<html lang="en">', page)  # mixed languages: English labels
        self.assertEqual(page.count('<span class="tag">Conditional · needs verification</span>'), 1)


@unittest.skipUnless(NODE, "node not found")
class TestJudgeShare(unittest.TestCase):
    def judge(self, m):
        js = ("import * as rc from %s; process.stdout.write(JSON.stringify(rc.judgeShare(%s)));"
              % (json.dumps(__import__("pathlib").Path(SCRIPT).as_uri()), json.dumps(m)))
        p = subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)["errors"]

    def test_rules(self):
        ok = {"card": {"w": 1200, "h": 630, "scrollW": 1200, "scrollH": 630, "clientW": 1200, "clientH": 630},
              "page": {"w": 1200, "h": 630}, "stage": {"r": 1150, "b": 600}, "screens": [{"scrollH": 400, "clientH": 400}]}
        self.assertEqual(self.judge(ok), [])
        bad = json.loads(json.dumps(ok))
        bad["card"]["w"] = 1600
        bad["screens"][0]["scrollH"] = 430
        bad["stage"]["b"] = 700
        errs = " | ".join(self.judge(bad))
        self.assertIn("it must be exactly 1200×630px", errs)
        self.assertIn("a screen is cut off (30px", errs)
        self.assertIn("the frames end outside the image", errs)


def _playwright_ready():
    if not NODE:
        return False
    js = "import('%s').then((rc) => process.exit(rc.loadPlaywright() ? 0 : 1))" % \
         __import__("pathlib").Path(SCRIPT).as_uri()
    return subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True).returncode == 0


@unittest.skipUnless(_playwright_ready(), "Playwright not found (NODE_PATH or ~/.abtest-visual/node_modules)")
class TestInChromium(unittest.TestCase):
    """The new components, the peek, the dark theme and the share image pass render_check --strict."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        product = {"title": "Eski fiyatı üstü çizili göstermek sepete eklemeyi artırır mı?", "lang": "tr",
                   "difference": "change", "variable": "Eski fiyat", "numeric_change": "B adds the old price",
                   "card": {"device": "web", "url": "ketenci.example/gomlek", "screen": PRODUCT,
                            "change": {"op": "edit", "target": "fiyat", "set": {"old": "1.690 TL"},
                                       "label": "Eski fiyat değişti"}}}
        dark = example()
        dark["card"]["theme"] = "dark"
        cards = {"landing": spec(LANDING, MOVE_LOGOS), "product": product, "sticky": sticky_record(), "dark": dark}
        cls.paths = []
        for name, sc in cards.items():
            html = built(sc)
            path = os.path.join(cls.tmp.name, "abtest-card-%s.html" % name)
            _write(path, html)
            cls.paths.append(path)
            view = bc.normalize(sc)
            share = os.path.join(cls.tmp.name, "abtest-card-%s.share.html" % name)
            _write(share, bc.share_html(html, view, bc.card_layout(view)["scale"]))
            cls.paths.append(share)
        p = subprocess.run([NODE, SCRIPT, "--json", "--strict", "--shot"] + cls.paths, capture_output=True, text=True,
                           timeout=300)
        if p.returncode == 3:
            raise unittest.SkipTest("render_check could not start a browser: " + p.stderr.strip()[:200])
        cls.result = {os.path.basename(json.loads(l)["file"]): json.loads(l) for l in p.stdout.splitlines()}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_card_and_share_passes_strict(self):
        self.assertEqual(len(self.result), 8)
        for name, res in self.result.items():
            with self.subTest(card=name):
                self.assertEqual(res["errors"] + res.get("warnings", []), [])

    def test_the_share_images_are_1200_by_630(self):
        for name, res in self.result.items():
            if name.endswith(".share.html"):
                self.assertTrue(res.get("share"))
                self.assertEqual([round(x) for x in res["card"]], [1200, 630])
                self.assertTrue(os.path.isfile(res["png"]))


if __name__ == "__main__":
    unittest.main()
