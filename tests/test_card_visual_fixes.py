#!/usr/bin/env python3
"""Regression tests for the card's visual fixes. Stdlib only; the browser
classes run when Playwright is found (like tests/test_render_check.py).

1 One pill row: the title box is two lines tall on every card and the frames
  are top-aligned under the pills, whatever their height.
2 Automatic scale: the builder estimates the layout and picks the frame's
  scale; phone_scale / web_scale are optional.
3 Ring label: 14px, its room is the template's, the builder picks its place.
4 An edit rings the changed part, not its container.
5 Ribbons: a visible conditional pill, a calm draft pill.
6 The final build writes the card's PNG when it can.
"""
import contextlib
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

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
SCRIPT = os.path.join(REPO_ROOT, "scripts", "render_check.mjs")
BUILD = os.path.join(REPO_ROOT, "scripts", "build_card.py")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
STYLE = re.sub(r"/\*.*?\*/", "", re.search(r"<style>(.*?)</style>", TEMPLATE, re.S).group(1), flags=re.S)
NODE = shutil.which("node")


def rule(selector):
    m = re.search(r"(?:^|\})\s*%s\{([^}]*)\}" % re.escape(selector), STYLE)
    assert m, "no CSS rule %s" % selector
    return m.group(1)


def built(sc):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            return bc.final_html(TEMPLATE, sc)[0]
        except SystemExit:
            raise AssertionError("the builder refused:\n" + err.getvalue())


def refusal(sc):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            bc.final_html(TEMPLATE, sc)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected a refusal")


def spec(screen, change, device="phone-web", title="Does a clearer headline lift sign-ups?", **card):
    c = {"screen": screen, "change": change, "device": device, "url": "shop.example/page"}
    c.update(card)
    return {"title": title, "lang": "en", "difference": ss.OP_DIFFERENCE[change["op"]], "variable": "Headline copy",
            "card": c}


FORM = [{"h": "Create your account", "id": "head"}, {"sub": "It takes a minute."},
        {"field": "Full name", "label": "Full name", "id": "name"},
        {"field": "you@example.com", "label": "Email", "id": "mail"}, {"help": "We never share it.", "id": "help"}]
HEADLINE = {"op": "edit", "target": "head", "set": {"h": "Start in one minute"}, "label": "New headline"}
SHORT = [{"h": "Create your account", "id": "head"}, {"sub": "It takes a minute."},
         {"field": "you@example.com", "label": "Email"}, {"cta": "Continue"}]
LONG = FORM + [{"field": "Company", "label": "Company"}, {"field": "Team size", "label": "Team size", "select": True},
               {"field": "Country", "label": "Country", "select": True},
               {"help": "You can change these later in your settings."}]
PLANS = [{"h": "Simple pricing"}, {"row": [
    {"plan": {"name": "Starter", "price": "$12", "per": "/mo", "cta": "Get started", "cta_style": "outline",
              "features": ["3 projects"]}},
    {"plan": {"name": "Team", "price": "$29", "per": "/mo", "cta": "Get started", "features": ["Unlimited projects"]},
     "id": "team"}]}]


def attr(html, name):
    return re.search(r'<div class="card"[^>]* %s="([^"]*)"' % name, html).group(1)


def labels(html):
    return re.findall(r'<div class="variant" data-label="([^"]*)">', html)


class TestOnePillRow(unittest.TestCase):
    def test_the_title_box_is_two_lines_tall_on_every_card(self):
        title = rule(".title")
        self.assertIn("min-height:75px", title)  # 2 × 30px × 1.25
        self.assertIn("line-height:1.25", title)
        self.assertIn("font-size:30px", title)

    def test_frames_are_top_aligned_under_the_pills(self):
        stage = rule(".stage")
        self.assertIn("align-content:start", stage)
        self.assertNotIn("align-content:center", stage)

    def test_the_builder_budget_matches_the_template(self):
        card = rule(".card")
        pad = re.search(r"padding:(\d+)px (\d+)px (\d+)px", card)
        gap = int(re.search(r"gap:(\d+)px", card).group(1))
        top, side, bottom = (int(x) for x in pad.groups())
        self.assertEqual(bc.STAGE_H, 900 - top - 75 - gap - bottom)
        self.assertEqual(bc.COLUMN_W, (1600 - 2 * side - 48) // 2)
        pill_gap = int(re.search(r"gap:(\d+)px", rule(".variant")).group(1))
        self.assertEqual(bc.FRAME_BUDGET, bc.STAGE_H - 30 - pill_gap)


class TestAutoScale(unittest.TestCase):
    def test_tokens_mirror_the_template(self):
        for device, selector in (("phone", ".phone"), ("web", ".browser")):
            css = rule(selector)
            tok = bc.LAYOUT_TOKENS[device]
            for var, key in (("--fs", "fs"), ("--fs-sm", "sm"), ("--fs-ctl", "ctl"), ("--fs-h", "h"), ("--fs-lg", "lg"),
                             ("--fs-xl", "xl"), ("--tap", "tap"), ("--tap-sm", "tapsm")):
                self.assertIn("%s:%dpx" % (var, tok[key]), css, (device, var))
        self.assertIn("padding:14px 20px 20px", rule(".screen"))
        self.assertIn("padding:20px 24px 24px", rule(".browser-screen"))
        self.assertIn("zoom:%s" % bc.scale_text(bc.DEFAULT_PHONE_SCALE), rule(".phone"))

    def test_desktop_base_text_is_legible_at_half_size(self):
        self.assertGreaterEqual(bc.LAYOUT_TOKENS["web"]["fs"], 16)

    def test_no_scale_field_is_needed(self):
        html = built(spec(FORM, HEADLINE))
        self.assertEqual(attr(html, "data-scale"), "auto")
        self.assertEqual(attr(html, "data-phone-scale"), "1.2")  # the phone's one default size
        self.assertNotIn(".phone,.below{zoom:", html)

    def test_a_long_screen_is_drawn_smaller_so_it_fits(self):
        sc = spec(LONG, HEADLINE)
        html = built(sc)
        scale = float(attr(html, "data-phone-scale"))
        self.assertLess(scale, 1.2)
        self.assertGreaterEqual(scale, bc.AUTO_SCALE_MIN)
        self.assertEqual(html.count(".phone,.below{zoom:%s}" % bc.scale_text(scale)), 1)
        view = bc.normalize(sc)
        tree = bc.parse_markup(view["variant_b"])[0]
        tall = bc.frame_estimate(tree, "phone-web", bc.layout_of(view))[0]
        if scale > bc.AUTO_SCALE_MIN:
            self.assertLessEqual(tall * scale, bc.FILL_HIGH * bc.FRAME_BUDGET)

    def test_a_short_screen_is_enlarged(self):
        html = built(spec(SHORT, HEADLINE))
        self.assertEqual(attr(html, "data-phone-scale"), "1.4")

    def test_a_browser_frame_fills_the_stage(self):
        sc = spec(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Start free trial"}, "label": "New button copy"},
                  device="web")
        html = built(sc)
        m = re.search(r"\.browser\{zoom:([\d.]+)\}", html)
        self.assertTrue(m, "a short desktop page is enlarged")
        z = float(m.group(1))
        self.assertLessEqual(z, bc.AUTO_SCALE_MAX)
        view = bc.normalize(sc)
        tree = bc.parse_markup(view["variant_b"])[0]
        self.assertLessEqual(bc.frame_estimate(tree, "web", bc.layout_of(view), bc.COLUMN_W / z)[0] * z,
                             bc.FILL_TARGET * bc.FRAME_BUDGET)

    def test_an_explicit_scale_still_wins(self):
        html = built(spec(SHORT, HEADLINE, phone_scale=1))
        self.assertEqual(attr(html, "data-scale"), "manual")
        self.assertEqual(attr(html, "data-phone-scale"), "1")
        self.assertIn(".phone,.below{zoom:1}", html)
        web = built(spec(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Try it"}, "label": "New button copy"},
                         device="web", web_scale=1.2))
        self.assertIn(".browser{zoom:1.2}", web)

    def test_the_same_record_builds_the_same_bytes(self):
        self.assertEqual(built(spec(LONG, HEADLINE)), built(spec(LONG, HEADLINE)))

    def test_text_width_grows_with_the_text(self):
        self.assertLess(bc.text_width("ill", 15), bc.text_width("mmm", 15))
        self.assertEqual(bc._wrap_lines("", 100, 15), 0)
        self.assertEqual(bc._wrap_lines("one two", 1000, 15), 1)
        self.assertGreater(bc._wrap_lines("one two three four five six seven eight", 80, 15), 2)


class TestRingLabel(unittest.TestCase):
    def test_label_is_14px_bold(self):
        label = rule(".hl[data-note]::after")
        for decl in ("font-size:14px", "font-weight:700", "background:var(--ring)", "color:#ffffff"):
            self.assertIn(decl, label)
        self.assertEqual(bc.LABEL_PX, 14)

    def test_the_template_opens_the_labels_room_outside_the_ring(self):
        room = "%dpx!important" % bc.LABEL_ROOM
        self.assertIn("margin-top:" + room, rule('.variant:not([data-label~="below"]) .hl[data-note]'))
        self.assertIn("margin-bottom:" + room, rule('.variant[data-label~="below"] .hl[data-note]'))
        # the label (4px off the ring, 22px tall) and the 6px clearance fit in the room at the smallest scale
        self.assertGreaterEqual((bc.LABEL_ROOM - bc.LABEL_OFFSET - bc.LABEL_H) * bc.AUTO_SCALE_MIN, bc.LABEL_CLEAR)

    def test_the_compiler_writes_no_room_of_its_own(self):
        a, b, problems = ss.compile(FORM, dict(HEADLINE, label_pos="below"), "en")
        self.assertEqual(problems, [])
        self.assertIn('<div class="hl" data-note="New headline" data-pos="below"><div class="r-h">', b)

    def test_the_declared_side_is_kept_when_it_is_clear(self):
        self.assertEqual(labels(built(spec(FORM, HEADLINE)))[1], "above end")
        self.assertEqual(labels(built(spec(FORM, dict(HEADLINE, label_pos="below"))))[1], "below end")
        self.assertEqual(labels(built(spec(FORM, HEADLINE, note_pos="below")))[1], "below end")

    def test_a_label_wider_than_its_ring_at_the_left_edge_starts_at_the_ring(self):
        change = {"op": "edit", "target": "name", "set": {"label": "Name"}, "label": "Shorter field label"}
        html = built(spec(FORM, change))
        self.assertEqual(labels(html)[1], "above start")  # at the right edge it would leave the screen
        self.assertIn('.variant[data-label~="start"] .hl[data-note]::after{right:auto;left:-7px}', STYLE)

    def test_a_label_that_fits_nowhere_is_refused(self):
        change = dict(HEADLINE, label="A very long ring label that describes the whole change in a full sentence")
        self.assertIn("fits at no position", refusal(spec(FORM, change)))

    def test_the_pinned_bar_keeps_its_own_label_place(self):
        self.assertIn("margin:0!important", rule(".card .screen .r-sticky .hl[data-note]"))
        cta = '<div class="r-cta">Pay</div>'
        rest = '<div class="r-line total"><span>Total</span><span>$40</span></div>'
        a = ('<div class="r-h">Cart</div><div class="r-fold"></div>%s<div class="hl" data-note="At the end">%s</div>'
             % (rest, cta))
        b = ('<div class="r-h">Cart</div><div class="r-sticky"><div class="hl" data-note="Pinned to the bottom">%s</div>'
             '</div><div class="r-fold"></div>%s' % (cta, rest))
        sc = {"title": "Does pinning the button lift payments?", "lang": "en", "difference": "move",
              "variable": "Button position", "card": {"variant_a": a, "variant_b": b, "device": "phone-web",
                                                       "url": "shop.example/cart"}}
        self.assertEqual(labels(built(sc))[1], "above end")


class TestRingTarget(unittest.TestCase):
    def compiled(self, screen, change):
        a, b, problems = ss.compile(screen, change, "en")
        self.assertEqual(problems, [])
        return a, b

    def test_a_plan_edit_rings_the_button_only(self):
        a, b = self.compiled(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Start free trial"},
                                     "label": "New button copy", "label_a": "Current button copy"})
        self.assertIn('<div class="hl" data-note="New button copy"><div class="r-cta">Start free trial</div></div>', b)
        self.assertIn('<div class="hl" data-note="Current button copy"><div class="r-cta">Get started</div></div>', a)
        self.assertNotIn('<div class="hl" data-note="New button copy"><div class="r-plan', b)

    def test_a_price_edit_rings_the_price_line(self):
        _, b = self.compiled(PLANS, {"op": "edit", "target": "team", "set": {"price": "$25"}, "label": "Lower price"})
        self.assertIn('<div class="hl" data-note="Lower price"><div class="r-plan-price">$25', b)

    def test_a_field_label_edit_rings_the_label(self):
        _, b = self.compiled(FORM, {"op": "edit", "target": "name", "set": {"label": "Name (optional)"},
                                    "label": "Marked optional"})
        self.assertIn('<div class="hl" data-note="Marked optional"><div class="r-label">Name (optional)</div></div>'
                      '<div class="r-field empty">Full name</div>', b)

    def test_the_author_can_ring_the_container_on_purpose(self):
        _, b = self.compiled(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Start free trial"},
                                     "label": "New button copy", "ring": "node"})
        self.assertIn('<div class="hl" data-note="New button copy"><div class="r-plan">', b)
        _, _, problems = ss.compile(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Try"}, "label": "X y",
                                            "ring": "half"}, "en")
        self.assertTrue(problems)

    def test_an_edit_of_several_parts_rings_the_node(self):
        _, b = self.compiled(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Start", "price": "$25"},
                                     "label": "New offer"})
        self.assertIn('<div class="hl" data-note="New offer"><div class="r-plan">', b)

    def test_a_part_one_arm_does_not_draw_rings_the_node(self):
        change = {"op": "edit", "target": "team", "set": {"badge": "Most popular"}, "label": "Badge added",
                  "label_a": "No badge"}
        a, b = self.compiled(PLANS, change)
        self.assertIn('<div class="hl" data-note="No badge"><div class="r-plan">', a)
        self.assertIn('<div class="hl" data-note="Badge added"><div class="r-plan">', b)

    def test_a_short_text_ring_hugs_the_text(self):
        self.assertRegex(STYLE, r"\.hl:has\(>\.r-link:only-child\)[^{]*\{width:fit-content")
        self.assertIn(".hl:has(>.r-label:only-child)", STYLE)

    def test_soft_rings_still_mark_linked_consequences(self):
        screen = PLANS + [{"line": ["Total", "$29"], "total": True, "id": "total"}]
        change = {"op": "edit", "target": "team", "set": {"price": "$25"}, "label": "Lower price",
                  "label_a": "Current price", "linked": [{"target": "total", "set": {"line": ["Total", "$25"]}}]}
        a, b, problems = ss.compile(screen, change, "en", soft=["total"])
        self.assertEqual(problems, [])
        for arm in (a, b):
            self.assertEqual(arm.count('class="hl-soft"'), 1)
            self.assertEqual(arm.count('class="hl"'), 1)


class TestRibbons(unittest.TestCase):
    def test_the_conditional_ribbon_is_a_visible_pill_off_the_edge(self):
        style = bc.CONDITIONAL_RIBBON_STYLE
        size = int(re.search(r"font:\d+ (\d+)px", style).group(1))
        self.assertGreaterEqual(size, 13)
        for decl in ("top:8px", "left:48px", "background:#b45309", "color:#ffffff", "border-radius:999px"):
            self.assertIn(decl, style)
        # white on #b45309
        lum = lambda c: sum(w * ((v / 255 / 12.92) if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4)
                            for w, v in zip((0.2126, 0.7152, 0.0722), c))  # noqa: E731
        self.assertGreaterEqual(1.05 / (lum((0xb4, 0x53, 0x09)) + 0.05), 4.5)

    def test_the_draft_ribbon_is_calm_and_still_marks_a_draft(self):
        self.assertEqual(bc.DRAFT_BANNER, {"tr": "Önizleme · görsel kontrol yapılmadı",
                                           "en": "Preview · not visually checked"})
        style = bc.DRAFT_RIBBON_STYLE
        self.assertNotIn("#b42318", style)  # no alarm red
        self.assertIn("background:#374151", style)
        final = built(spec(FORM, HEADLINE))
        draft = bc.draft_html(final, "en")
        self.assertIn('<meta name="abtest-status" content="draft">', draft)
        self.assertIn('id="abtest-draft"', draft)
        self.assertNotIn('id="abtest-draft"', final)
        self.assertNotEqual(bc.html_fingerprint(draft), bc.html_fingerprint(final))

    def test_no_capitalised_alarm_words(self):
        for text in bc.DRAFT_BANNER.values():
            self.assertNotIn("TASLAK", text)
            self.assertNotIn("DRAFT", text)
            self.assertTrue(text[0].isupper())


class TestPng(unittest.TestCase):
    def test_png_path(self):
        self.assertEqual(os.path.basename(bc.png_path("/x/abtest-card-kupon.html")), "card-kupon.png")
        self.assertEqual(os.path.basename(bc.png_path("/x/demo.html")), "card-demo.png")

    def test_without_node_the_build_says_so_in_one_line(self):
        old = os.environ.get("PATH", "")
        os.environ["PATH"] = ""
        try:
            path, line = bc.write_png("/nonexistent/abtest-card-x.html")
        finally:
            os.environ["PATH"] = old
        self.assertIsNone(path)
        self.assertEqual(line.count("\n"), 0)
        self.assertIn("png: not written", line)

    def run_build(self, out, env=None, extra=()):
        full = dict(os.environ)
        full.pop("ABTEST_NO_PNG", None)
        full.update(env or {})
        return subprocess.run([sys.executable, BUILD, "--template", TEMPLATE_PATH, "--scenario", EXAMPLE, "--out", out]
                              + list(extra), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                              env=full, timeout=180)

    def test_a_final_build_without_playwright_still_succeeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "abtest-card-kupon.html")
            p = self.run_build(out, {"PATH": os.path.dirname(sys.executable) + os.pathsep + "/usr/bin:/bin",
                                     "NODE_PATH": "", "HOME": tmp})
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(os.path.isfile(out))
            lines = [ln for ln in p.stdout.splitlines() if ln.startswith("png:")]
            self.assertEqual(len(lines), 1)
            self.assertIn("not written", lines[0])
            self.assertFalse(os.path.exists(bc.png_path(out)))

    def test_no_png_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "abtest-card-kupon.html")
            p = self.run_build(out, extra=["--no-png"])
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertNotIn("png:", p.stdout)


def _playwright_ready():
    if not NODE:
        return False
    js = "import('%s').then((rc) => process.exit(rc.loadPlaywright() ? 0 : 1))" % \
         __import__("pathlib").Path(SCRIPT).resolve().as_uri()
    return subprocess.run([NODE, "--input-type=module", "-e", js], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE).returncode == 0


@unittest.skipUnless(_playwright_ready(), "Playwright not found (NODE_PATH or ~/.abtest-visual/node_modules)")
class TestInChromium(unittest.TestCase):
    """What the estimate promises, measured on the real render."""

    CARDS = {
        "short-one-line": lambda: spec(SHORT, HEADLINE),
        "form": lambda: spec(FORM, HEADLINE),
        "long-two-lines": lambda: spec(LONG, dict(HEADLINE, label_pos="below"),
                                       title="Does a headline that names the one minute it takes to open an account "
                                             "lift completed sign-ups on the mobile form?"),
        "field-label": lambda: spec(FORM, {"op": "edit", "target": "name", "set": {"label": "Name"},
                                           "label": "Shorter field label"}),
        "web-plans": lambda: spec(PLANS, {"op": "edit", "target": "team", "set": {"cta": "Start free trial"},
                                          "label": "New button copy", "label_a": "Current button copy"}, device="web"),
        "conditional": lambda: dict(spec(FORM, HEADLINE), assumptions=[
            {"type": "critical", "text": "The headline can be changed without a legal review.",
             "verify": "Ask the legal team."}]),
    }

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.paths, cls.scenarios = {}, {}
        for name, make in cls.CARDS.items():
            sc = make()
            cls.scenarios[name] = sc
            path = os.path.join(cls.tmp.name, "abtest-card-%s.html" % name)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(bc.draft_html(built(sc), "en"))
            cls.paths[name] = path
        p = subprocess.run([NODE, SCRIPT, "--json", "--strict"] + list(cls.paths.values()), stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, universal_newlines=True, timeout=180)
        if p.returncode == 3:
            raise unittest.SkipTest("render_check could not start a browser: " + p.stderr.strip()[:200])
        cls.result = {os.path.basename(json.loads(l)["file"])[len("abtest-card-"):-5]: json.loads(l)
                      for l in p.stdout.splitlines()}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_card_passes_strict_without_a_scale_or_spacing_from_the_author(self):
        for name, res in self.result.items():
            with self.subTest(card=name):
                self.assertEqual(res["errors"] + res["warnings"], [])

    def test_frames_start_at_one_y_on_every_card(self):
        tops = set()
        for name, res in self.result.items():
            for frame in res["frames"]:
                tops.add(round(frame["y"]))
        self.assertEqual(tops, {167})

    def test_the_estimate_is_close_to_the_render_and_never_clips(self):
        for name, res in self.result.items():
            sc = self.scenarios[name]
            view = bc.normalize(sc)
            decided = bc.card_layout(view)
            scale = decided["scale"]
            width = bc.COLUMN_W / scale if view["device"] == "web" else None
            for frame, key, lab in zip(res["frames"], ("variant_a", "variant_b"), decided["labels"]):
                with self.subTest(card=name, arm=frame["name"]):
                    est = bc.frame_estimate(bc.parse_markup(view[key])[0], view["device"], bc.layout_of(view), width,
                                            lab.split()[0])[0] * scale
                    self.assertLessEqual(frame["h"], bc.FRAME_BUDGET + 1)
                    self.assertLess(abs(est - frame["h"]) / frame["h"], 0.08, (est, frame["h"]))

    def test_the_final_build_writes_the_png(self):
        out = os.path.join(self.tmp.name, "abtest-card-kupon.html")
        full = dict(os.environ)
        full.pop("ABTEST_NO_PNG", None)
        p = subprocess.run([sys.executable, BUILD, "--template", TEMPLATE_PATH, "--scenario", EXAMPLE, "--out", out],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=full, timeout=180)
        self.assertEqual(p.returncode, 0, p.stderr)
        png = bc.png_path(out)
        self.assertIn("png: %s" % png, p.stdout)
        with open(png, "rb") as fh:
            self.assertEqual(fh.read(8), b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
