#!/usr/bin/env python3
"""Regression tests for the second audit's builder and render_check findings.

Each finding has a test that fails on the code before the fix: C1/C2 (hiding,
clipping or displacing CSS, and a ring around nothing or around content that
sticks out), M1 (a block inside a span inside a <p>), M2 (the diff on what
renders), M3/M4 (a soft ring listed as linked, and next to the ring), M5 (two
independent rings), M6 (A and B rendering the same), M7 (--out), M8 (the
mockup-reviewer stamp), and the minor items (named colours, an overlay with
its own style, duplicate JSON keys, huge integers, trailing newlines in hex,
per-file render failures, the clipping advice, the Playwright fallback).
Stdlib only; the Chromium cases run when Playwright is found (NODE_PATH or
~/.abtest-visual/node_modules) and are skipped with a reason otherwise.
"""
import contextlib
import copy
import io
import json
import os
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

REPO_ROOT = os.path.abspath(os.path.join(HERE, ".."))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
SCRIPT = os.path.join(REPO_ROOT, "scripts", "render_check.mjs")
NODE = shutil.which("node")
with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
CLASSES = bc.component_classes(TEMPLATE)

HEAD = '<div class="r-h">Sepetim</div>'
LINE = '<div class="r-sub">Kargo yarın</div>'


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        sc = json.load(fh)
    sc.pop("review", None)
    return sc


def ring(inner, note="Yeni"):
    return '<div class="hl" data-note="%s">%s</div>' % (note, inner)


def errors_of(a, b, difference="change", **kw):
    return bc.card_problems(difference, a, b, lang="en", classes=CLASSES, card_lang="tr", **kw)[0]


def report(a, b, difference="change", **over):
    view = {"variant_a": a, "variant_b": b, "difference": difference, "variable": None, "lang": "tr",
            "device": "phone", "warnings": [], "kpi_names": []}
    view.update(over)
    return bc.mockup_report(view, lang="en", classes=CLASSES)


def has(errors, fragment):
    return any(fragment in e for e in errors)


def quiet(fn, *args, **kw):
    """Call fn with stderr captured; returns (result or None, SystemExit code or None, stderr)."""
    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        try:
            return fn(*args, **kw), None, err.getvalue()
        except SystemExit as exc:
            return None, exc.code, err.getvalue()


def critic(sc):
    sc = copy.deepcopy(sc)
    sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}}
    return sc


def main_run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = bc.main(argv)
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


# ------------------------------------------------------------------ C1 / C2: inline style


# A refusal writes its reason to stderr before it exits; the tests that expect one would print it on every
# run. The test runner keeps its own stream, so only the builder's messages are silenced.
_STDERR = None


def setUpModule():
    global _STDERR
    import io
    _STDERR, sys.stderr = sys.stderr, io.StringIO()


def tearDownModule():
    sys.stderr = _STDERR

class TestHidingStyleIsRefused(unittest.TestCase):
    """Inline CSS that hides, clips, displaces or reorders drawn content is refused anywhere in a mockup."""

    HIDING = ("opacity:0", "opacity:.4", "visibility:hidden", "display:none", "display:contents",
              "overflow:hidden;height:10px", "overflow-y:clip", "clip-path:inset(50%)", "clip:rect(0 0 0 0)",
              "filter:blur(8px)", "-webkit-filter:blur(2px)", "mask-image:linear-gradient(red,red)",
              "text-indent:-9999px", "transform:translateX(-600px)", "transform:scale(0)", "translate:10px",
              "margin-left:-600px", "margin-bottom:-60px", "margin:0 -40px", "position:absolute",
              "position:sticky", "top:-20px", "inset:0", "z-index:5", "order:-1", "flex-direction:column-reverse",
              "white-space:pre", "-webkit-text-fill-color:transparent", "zoom:.2", "letter-spacing:-6px",
              "contain:paint", "mix-blend-mode:difference")

    def test_each_is_refused_outside_the_ring(self):
        for decl in self.HIDING:
            with self.subTest(decl):
                a = '<div class="r-h" style="%s">Sepetim</div>' % decl + LINE
                b = '<div class="r-h" style="%s">Sepetim</div>' % decl + ring(LINE.replace("yarın", "bugün"))
                self.assertTrue(has(errors_of(a, b), "can hide, clip, displace or reorder"), (decl, errors_of(a, b)))

    def test_c1_an_absolute_child_inside_the_ring_is_refused(self):
        cover = '<span style="position:absolute;left:0;top:-80px;width:300px;height:60px;background:#fff"></span>'
        errs = errors_of(HEAD + LINE, HEAD + ring('<div class="r-sub">Kargo bugün</div>' + cover))
        self.assertTrue(has(errs, "“position:absolute”"), errs)
        self.assertTrue(has(errs, "“top:-80px”"), errs)

    def test_a_negative_margin_under_a_ring_is_refused_beyond_an_icon(self):
        errs = errors_of(HEAD + LINE, HEAD + ring('<div class="r-sub" style="margin-bottom:-12px">Kargo bugün</div>'))
        self.assertTrue(has(errs, "inside a ring a negative margin of more than 4px"), errs)

    def test_label_room_on_the_ring_itself_is_non_negative_only(self):
        changed = '<div class="r-sub">Kargo bugün</div>'
        ok = '<div class="hl" data-note="Yeni" style="margin-top:20px">%s</div>' % changed
        self.assertFalse(has(errors_of(HEAD + LINE, HEAD + ok), "must not push content"))
        bad = '<div class="hl" data-note="Yeni" style="margin-bottom:-2px">%s</div>' % changed
        self.assertTrue(has(errors_of(HEAD + LINE, HEAD + bad), "must not push content"))

    def test_what_the_screen_spec_draws_still_passes(self):
        # Rotated icon glyphs, a full-bleed band (-20px / -14px), a tighter rhythm (-12px), relative position.
        ok = ('<div class="r-header"><span role="img" aria-label="Geri" style="display:inline-block;width:11px;'
              'height:11px;border-left:2px solid #111;border-bottom:2px solid #111;transform:rotate(45deg);'
              'margin-left:6px"></span><span style="display:inline-block;width:8px;height:2px;background:#111;'
              'transform:rotate(45deg);margin:13px 0 0 -3px"></span></div>'
              '<div style="margin:0 -20px;padding:20px;margin-top:-14px;background:#f5f5f5;position:relative">'
              '<div class="r-h" style="margin-bottom:-12px;white-space:nowrap">Sepetim</div></div>')
        errs = errors_of(ok + LINE, ok + ring(LINE.replace("yarın", "bugün")))
        self.assertEqual([e for e in errs if "can hide" in e], [], errs)

    def test_the_message_is_turkish_too(self):
        errs = bc.card_problems("change", '<div class="r-h" style="opacity:0">A</div>' + LINE,
                                '<div class="r-h" style="opacity:0">A</div>' + ring(LINE + LINE), lang="tr")[0]
        self.assertTrue(has(errs, "okurun gördüğünü gizleyebilir"), errs)


class TestRingAroundNothing(unittest.TestCase):
    def test_a_ring_around_a_no_break_space_is_refused(self):
        errs = errors_of(HEAD, HEAD + ring('<div class="r-help">&nbsp;</div>', "Gerekçe satırı"), difference="add")
        self.assertTrue(has(errs, "contains nothing visible"), errs)

    def test_a_ring_around_zero_width_characters_is_refused(self):
        errs = errors_of(HEAD, HEAD + ring('<div class="r-sub">​​</div>'), difference="add")
        self.assertTrue(has(errs, "contains nothing visible"), errs)

    def test_a_ring_around_a_drawn_component_is_content(self):
        errs = errors_of(HEAD, HEAD + ring('<div class="r-divider"></div>'), difference="add")
        self.assertFalse(has(errs, "contains nothing visible"), errs)


# ------------------------------------------------------------------ M1, M2

class TestParse(unittest.TestCase):
    def test_m1_a_block_inside_a_span_inside_a_p_is_refused(self):
        _, problems = bc.parse_markup('<p><span class="hl" data-note="X"><div>Yeni</div></span></p>')
        self.assertTrue(any("inside <p>" in p for p in problems), problems)

    def test_m2_a_space_between_inline_elements_is_part_of_the_diff(self):
        a = bc.parse_markup('<div class="r-sub"><b>890</b> <span>TL</span></div>')[0]
        b = bc.parse_markup('<div class="r-sub"><b>890</b><span>TL</span></div>')[0]
        self.assertNotEqual(a.key(), b.key())

    def test_m2_formatting_whitespace_between_blocks_is_not(self):
        a = bc.parse_markup('<div class="r-h">Sepetim</div>\n   <div class="r-sub">Kargo</div>')[0]
        b = bc.parse_markup('<div class="r-h">Sepetim</div><div class="r-sub">  Kargo\n</div>')[0]
        self.assertEqual(a.key(), b.key())

    def test_m2_a_no_break_space_is_text(self):
        a = bc.parse_markup('<div class="r-sub">890&nbsp;TL</div>')[0]
        b = bc.parse_markup('<div class="r-sub">890 TL</div>')[0]
        self.assertNotEqual(a.key(), b.key())

    def test_style_spelling_does_not_count_as_a_difference(self):
        a = bc.parse_markup('<div class="r-sub a b" style="color:#AABBCC; margin-top : 4px">X</div>')[0]
        b = bc.parse_markup('<div class="r-sub b a" style="color:#abc;margin-top:4px">X</div>')[0]
        self.assertEqual(a.key(), b.key())


# ------------------------------------------------------------------ M3, M4, M5

TOGGLE_A = '<div class="r-row"><div class="r-chip on">Aylık</div><div class="r-chip">Yıllık</div></div>'
TOGGLE_B = ('<div class="r-row"><div class="hl" data-note="Yıllık varsayılan"><div class="r-chips">'
            '<div class="r-chip">Aylık</div><div class="r-chip on">Yıllık</div></div></div></div>')


class TestSoftRing(unittest.TestCase):
    def test_m3_a_soft_ring_next_to_the_ring_is_its_own_linked_entry(self):
        a = ('<div class="r-chips"><div class="r-chip on">Aylık</div><div class="r-chip">Yıllık</div></div>'
             '<div class="r-plan-price">99</div>')
        b = ('<div class="hl" data-note="Yıllık varsayılan"><div class="r-chips"><div class="r-chip">Aylık</div>'
             '<div class="r-chip on">Yıllık</div></div></div>'
             '<div class="hl-soft" data-note="Yıllık fiyat"><div class="r-plan-price">79</div></div>')
        errors, _, manifest = report(a, b, numeric_change="B shows the annual price the user gave")
        self.assertEqual(errors, [])
        kinds = {r["label"]: r["kind"] for r in manifest["rings"]}
        self.assertEqual(kinds.get("Yıllık fiyat"), "linked", manifest["rings"])
        self.assertNotIn("Yıllık fiyat", [r["label"] for r in manifest["rings"] if r["kind"] != "linked"])

    def test_m4_a_soft_ring_far_from_the_ring_is_refused(self):
        filler = "".join('<div class="r-sub">Satır %d</div>' % i for i in range(6))
        a = HEAD + filler + '<div class="r-sub">Toplam</div>'
        b = ring('<div class="r-h">Sepetiniz</div>') + filler + \
            '<div class="hl-soft" data-note="Toplam"><div class="r-sub">Toplam güncel</div></div>'
        self.assertTrue(has(errors_of(a, b), "is not next to the ring"), errors_of(a, b))

    def test_m4_a_soft_ring_beside_the_ring_passes(self):
        a = HEAD + '<div class="r-sub">Toplam</div>'
        b = ring('<div class="r-h">Sepetiniz</div>') + \
            '<div class="hl-soft" data-note="Toplam"><div class="r-sub">Toplam güncel</div></div>'
        self.assertFalse(has(errors_of(a, b), "is not next to the ring"), errors_of(a, b))

    def test_m5_two_independent_rings_are_refused(self):
        b = ring('<div class="r-h">Sepetiniz</div>', "Bir") + ring('<div class="r-sub">Kargo bugün</div>', "İki")
        self.assertTrue(has(errors_of(HEAD + LINE, b), "2 rings in B"), errors_of(HEAD + LINE, b))

    def test_m5_a_ring_around_the_whole_screen_warns(self):
        body = ('<div class="r-sub">Kargo yarın kapında, iade otuz gün içinde ücretsiz.</div>'
                '<div class="r-sub">Sepette iki ürün var, toplam 890 TL.</div>')
        warnings = bc.card_problems("change", HEAD + body, ring('<div class="r-h">Sepetiniz</div>' + body),
                                    lang="en", classes=CLASSES)[1]
        self.assertTrue(has(warnings, "of the screen's text"), warnings)


# ------------------------------------------------------------------ M6

class TestNoOpIsRefused(unittest.TestCase):
    def test_an_identical_ringed_replacement(self):
        errors = report(HEAD + LINE, HEAD + ring(LINE))[0]
        self.assertTrue(has(errors, "A and B render the same"), errors)

    def test_a_hex_case_only_edit(self):
        a = '<div class="r-h" style="color:#AABBCC">Sepetim</div>'
        b = '<div class="r-h hl" data-note="Renk" style="color:#aabbcc">Sepetim</div>'
        self.assertTrue(has(report(a + LINE, b + LINE)[0], "A and B render the same"))

    def test_a_self_move_through_the_screen_spec(self):
        screen = [{"h": "Sepetim", "id": "h"}, {"field": "E-posta", "id": "mail"}, {"cta": "Devam", "id": "cta"}]
        a, b, problems = ss.compile(screen, {"op": "move_before", "target": "mail", "to": "cta",
                                             "label_a": "Eski yer", "label_b": "Yeni yer"}, "tr")
        # The screen spec refuses the no-op itself, before the builder's own A == B check is reached.
        self.assertTrue(has(problems, "birebir aynı"), problems)

    def test_a_real_change_passes(self):
        self.assertFalse(has(report(HEAD + LINE, HEAD + ring(LINE.replace("yarın", "bugün")))[0], "render the same"))


# ------------------------------------------------------------------ minor builder items

class TestMinorBuilder(unittest.TestCase):
    def test_a_named_colour_only_in_b_outside_the_ring_is_refused(self):
        a = '<div class="r-sub" style="color:black">Kargo</div>'
        b = '<div class="r-sub" style="color:red">Kargo</div>'
        errs = errors_of(HEAD + a, ring('<div class="r-h">Sepetiniz</div>') + b)
        self.assertTrue(has(errs, "inline colour only in Variant B on an element outside the ring: red"), errs)

    def test_an_overlay_with_its_own_style_is_not_a_ring(self):
        modal = '<div class="r-modal hl" data-note="Yeni modal"><div class="r-h">Kampanya</div></div>'
        a = HEAD
        b = HEAD + '<div class="r-overlay" style="background:#000">%s</div>' % modal
        self.assertTrue(has(errors_of(a, b, difference="add"), "differ outside any ring"))
        self.assertFalse(has(errors_of(a, HEAD + '<div class="r-overlay">%s</div>' % modal, difference="add"),
                             "differ outside any ring"))

    def test_hex_with_a_trailing_newline_is_refused(self):
        sc = {"review": {"mockup_reviewer": {"verdict": "PASS", "fingerprint": "a" * 64 + "\n"}}}
        self.assertTrue(has(bc.stamp_problems(sc, "mockup_reviewer", "a" * 64), "must be a sha256 hex string"))
        line = '<div class="r-sub">Adınız</div>'
        sc = {"title": "T", "card": {"variant_a": line, "variant_b": line + ring(LINE), "mockup_basis": "shared_page",
                                     "inherited_contrast": [{"text": "Adınız", "color": "#777879"}]}}
        self.assertIsNone(quiet(bc.normalize, sc)[1])
        sc["card"]["inherited_contrast"][0]["color"] = "#777879\n"
        self.assertEqual(quiet(bc.normalize, sc)[1], 2)

    def test_s2_a_three_digit_hex_in_the_screen_spec_is_refused(self):
        _, _, problems = ss.compile([{"h": "Sepetim", "id": "h", "fg": "#abc"}],
                                    {"op": "edit", "target": "h", "set": {"fg": "#112233"}, "label": "Renk"}, "en")
        self.assertTrue(problems, "a 3-digit hex reached the mockup")

    def test_s1_a_quote_in_a_label_stays_inside_the_attribute(self):
        a, b, problems = ss.compile([{"h": "Sepetim", "id": "h"}],
                                    {"op": "replace", "target": "h", "node": {"h": "Sepetiniz"},
                                     "label": 'Yeni "başlık"'}, "tr")
        self.assertEqual(problems, [])
        tree, errs = bc.parse_markup(b)
        self.assertEqual(errs, [])
        self.assertEqual(bc.rings(tree)[0].attrs["data-note"], 'Yeni "başlık"')

    def test_no_em_dash_in_the_card_or_the_template(self):
        html = quiet(bc.final_html, TEMPLATE, example())[0][0]
        self.assertNotIn("\u2014", html)
        self.assertNotIn("\u2014", TEMPLATE)


# ------------------------------------------------------------------ CLI: JSON, --out, the stamp

class CliCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def record(self, sc):
        return self.write("s.json", json.dumps(sc, ensure_ascii=False))

    def build(self, *extra, sc=None, out="abtest-card-x.html"):
        src = self.record(sc if sc is not None else critic(example()))
        argv = ["--template", TEMPLATE_PATH, "--scenario", src] + list(extra)
        if out is not None:
            argv += ["--out", os.path.join(self.dir, out)]
        return main_run(argv)


class TestJsonInput(CliCase):
    def test_duplicate_keys_are_refused(self):
        raw = json.dumps(critic(example()), ensure_ascii=False)
        src = self.write("s.json", raw[:-1] + ', "title": "Başka bir başlık?"}')
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", src, "--out",
                                 os.path.join(self.dir, "c.html"), "--draft"])
        self.assertEqual(code, 2)
        self.assertIn("key 'title' appears twice in one object", err)  # the validator's shared reader, in --lang

    def test_a_huge_integer_is_a_message_not_a_traceback(self):
        src = self.write("s.json", '{"title": "T", "n": %s}' % ("9" * 5000))
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", src, "--out",
                                 os.path.join(self.dir, "c.html")])
        self.assertIn(code, (1, 2))  # 2 where Python limits int digits, 1 (schema) where it doesn't
        self.assertNotIn("Traceback", err)


class TestOutPath(CliCase):
    def test_m7_the_template_is_never_overwritten(self):
        src = self.record(critic(example()))
        before = TEMPLATE
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", src, "--out", TEMPLATE_PATH, "--draft"])
        self.assertEqual(code, 1)
        self.assertIn("is the template", err)
        with open(TEMPLATE_PATH, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), before)
        self.assertFalse(os.path.exists(TEMPLATE_PATH + bc.MANIFEST_SUFFIX))

    def test_m7_a_repo_source_directory_is_refused(self):
        src = self.record(critic(example()))
        target = os.path.join(REPO_ROOT, "scripts", "abtest-card-x.html")
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", src, "--out", target, "--draft"])
        self.assertEqual(code, 1)
        self.assertIn("scripts/ directory", err)
        self.assertFalse(os.path.exists(target))

    def test_m7_not_an_html_file_and_the_record_itself(self):
        code, _, err = self.build("--draft", out="card.json")
        self.assertIn("must name an .html card file", err)
        src = self.record(critic(example()))
        html_src = self.write("s.html", open(src, encoding="utf-8").read())
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", html_src, "--out", html_src, "--draft"])
        self.assertIn("is the record", err)

    def test_m7_an_existing_file_that_is_not_a_card_is_left_alone(self):
        self.write("index.html", "<html>mine</html>")
        code, _, err = self.build("--draft", out="index.html")
        self.assertEqual(code, 1)
        self.assertIn("is not a card this tool built", err)
        with open(os.path.join(self.dir, "index.html"), encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "<html>mine</html>")

    def test_m7_rebuilding_over_an_earlier_draft_is_fine(self):
        self.assertEqual(self.build("--draft")[0], 0)
        self.assertEqual(self.build("--draft")[0], 0)


class TestMockupStamp(CliCase):
    def draft(self, sc=None):
        sc = sc or critic(example())
        code, out, err = self.build("--draft", sc=sc, out="abtest-card-x.draft.html")
        self.assertEqual(code, 0, err)
        return sc, out, os.path.join(self.dir, "abtest-card-x.draft.html")

    def stamp(self, draft):
        return main_run(["--template", TEMPLATE_PATH, "--scenario", os.path.join(self.dir, "s.json"), "--stamp", draft])

    def test_m8_the_draft_output_carries_no_valid_stamp(self):
        sc, out, draft = self.draft()
        stamp = bc.mockup_stamp(TEMPLATE, sc)
        for text in (out, open(draft, encoding="utf-8").read(), open(draft + bc.MANIFEST_SUFFIX, encoding="utf-8").read()):
            self.assertNotIn(stamp, text)
        # The audit's forgery: copy what the draft printed into the stamp.
        printed = [w for line in out.splitlines() for w in line.split() if len(w) == 64]
        for value in printed + [bc.final_fingerprint(TEMPLATE, sc)]:
            forged = dict(sc, review=dict(sc["review"], mockup_reviewer={"verdict": "PASS", "fingerprint": value}))
            self.assertEqual(self.build(sc=forged)[0], 1)

    def test_m8_the_reviewer_stamp_builds_the_final_and_check_confirms_the_file(self):
        sc, _, draft = self.draft()
        code, out, err = self.stamp(draft)
        self.assertEqual(code, 0, err)
        sc["review"]["mockup_reviewer"] = json.loads(out)
        code, _, err = self.build(sc=sc, out="abtest-card-x.html")
        self.assertEqual(code, 0, err)
        card = os.path.join(self.dir, "abtest-card-x.html")
        code, out, err = main_run(["--template", TEMPLATE_PATH, "--scenario", os.path.join(self.dir, "s.json"),
                                   "--check", card])
        self.assertEqual(code, 0, err)
        self.assertIn("matches the reviewed card", out)
        with open(card, "a", encoding="utf-8") as fh:
            fh.write("<!-- edited -->")
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", os.path.join(self.dir, "s.json"),
                                 "--check", card])
        self.assertEqual(code, 1)
        self.assertIn("does not match the reviewed card", err)

    def test_m8_a_stale_or_edited_draft_gets_no_stamp(self):
        sc, _, draft = self.draft()
        with open(draft, "a", encoding="utf-8") as fh:
            fh.write(" ")
        code, out, err = self.stamp(draft)
        self.assertEqual(code, 1)
        self.assertIn("the draft is not what this record builds now", err)
        self.assertEqual(out, "")

    def test_m8_mockup_basis_is_part_of_the_stamp(self):
        sc = example()
        other = copy.deepcopy(sc)
        other["card"]["mockup_basis"] = "described"
        self.assertEqual(quiet(bc.final_fingerprint, TEMPLATE, sc)[0], quiet(bc.final_fingerprint, TEMPLATE, other)[0])
        self.assertNotEqual(quiet(bc.mockup_stamp, TEMPLATE, sc)[0], quiet(bc.mockup_stamp, TEMPLATE, other)[0])

    def test_stamp_and_check_write_nothing_and_take_no_out(self):
        sc, _, draft = self.draft()
        code, _, err = main_run(["--template", TEMPLATE_PATH, "--scenario", os.path.join(self.dir, "s.json"),
                                 "--stamp", draft, "--out", os.path.join(self.dir, "y.html")])
        self.assertEqual(code, 2)
        self.assertFalse(os.path.exists(os.path.join(self.dir, "y.html")))


# ------------------------------------------------------------------ render_check

def _playwright_ready():
    if not NODE:
        return False
    js = "import('%s').then((rc) => process.exit(rc.loadPlaywright() ? 0 : 1))" % \
         __import__("pathlib").Path(SCRIPT).as_uri()
    return subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True).returncode == 0


def rc(args, env=None, timeout=180):
    full = dict(os.environ)
    full.update(env or {})
    return subprocess.run([NODE, SCRIPT] + args, capture_output=True, text=True, timeout=timeout, env=full)


@unittest.skipUnless(NODE, "node not found")
class TestRenderCheckWithoutBrowser(unittest.TestCase):
    def call(self, fn, *args):
        js = ("import * as rc from %s; process.stdout.write(JSON.stringify(rc[%s](...%s)));"
              % (json.dumps(__import__("pathlib").Path(SCRIPT).as_uri()), json.dumps(fn), json.dumps(list(args))))
        p = subprocess.run([NODE, "--input-type=module", "-e", js], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def test_clipping_advice_never_suggests_the_scale_already_set(self):
        at1 = self.call("fitAdvice", {"phoneScale": 1}, {"kind": "phone-web"})
        self.assertNotIn("set card.phone_scale: 1", at1)
        self.assertIn(".r-fold", at1)
        self.assertIn("set card.phone_scale: 1", self.call("fitAdvice", {"phoneScale": 1.2}, {"kind": "phone"}))
        self.assertNotIn("phone_scale", self.call("fitAdvice", {"phoneScale": None}, {"kind": "web"}))

    def test_hidden_text_and_ring_measurements_become_errors(self):
        from test_render_check import card
        m = card()
        m["variants"][1]["hidden"] = [{"what": "“Sepetim”", "why": "opacity 0 (with its ancestors)"}]
        m["variants"][1]["rings"][0]["content"] = False
        m["variants"][1]["rings"][0]["spill"] = {"px": 80, "what": "a 300×60px span element"}
        errs = " | ".join(self.call("judge", m)["errors"])
        self.assertIn("variant B: text “Sepetim” is not visible: opacity 0", errs)
        self.assertIn("the ring holds nothing visible", errs)
        self.assertIn("a 300×60px span element sticks 80px out of the ring's box", errs)

    def test_the_header_lists_every_exit_status(self):
        with open(SCRIPT, encoding="utf-8") as fh:
            head = fh.read().split("import ", 1)[0]
        for line in ("0  VERIFIED", "1  VISUAL_CHECK_FAILED", "2  usage error", "3  VISUAL_CHECK_UNAVAILABLE"):
            self.assertIn(line, head)
        self.assertNotIn("Exit: 0 = no error", head)

    def test_playwright_is_found_in_the_per_user_folder(self):
        with tempfile.TemporaryDirectory() as home:
            pkg = os.path.join(home, ".abtest-visual", "node_modules", "playwright")
            os.makedirs(pkg)
            with open(os.path.join(pkg, "index.js"), "w", encoding="utf-8") as fh:
                fh.write("module.exports = {chromium: {launch: async () => { throw new Error('stub browser'); }}};\n")
            env = {k: v for k, v in os.environ.items() if k != "NODE_PATH"}
            env["HOME"] = home
            p = subprocess.run([NODE, SCRIPT, os.path.join(HERE, "fixtures", "render_check", "clean.html")],
                               capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertIn("Chromium did not start (stub browser)", p.stderr)


@unittest.skipUnless(_playwright_ready(), "Playwright not found (NODE_PATH or ~/.abtest-visual/node_modules)")
class TestRenderCheckInChromium(unittest.TestCase):
    """Cards the builder refuses, edited after the build: render_check must refuse them on its own."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        final = quiet(bc.final_html, TEMPLATE, example())[0][0]
        target = '>İndirim kodum var</div>'
        assert final.count(target) == 1
        cover = ('<span style="position:absolute;left:0;top:-70px;width:330px;height:60px;'
                 'background:#ffffff"></span>')
        cases = {
            "clean": final,
            "c1-cover": final.replace(target, '>İndirim kodum var%s</div>' % cover),
            "ring-nbsp": final.replace(target, ">&nbsp;</div>"),
            "faded": final.replace('<div class="r-h">Sepetim</div>', '<div class="r-h" style="opacity:0">Sepetim</div>', 1),
            "broken": final.replace("</head>", "<script>document.querySelectorAll = null;</script></head>"),
        }
        cls.paths = {}
        for name, html in cases.items():
            path = os.path.join(cls.tmp.name, "abtest-card-%s.html" % name)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(html)
            cls.paths[name] = path
        p = rc(["--json"] + [cls.paths[n] for n in ("clean", "c1-cover", "ring-nbsp", "faded")])
        if p.returncode == 3:
            raise unittest.SkipTest("render_check could not start a browser: " + p.stderr.strip()[:200])
        cls.result = {os.path.basename(json.loads(l)["file"]): json.loads(l) for l in p.stdout.splitlines()}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def errs(self, name):
        return " | ".join(self.result["abtest-card-%s.html" % name]["errors"])

    def test_the_built_card_passes(self):
        self.assertEqual(self.result["abtest-card-clean.html"]["errors"], [])

    def test_c1_an_absolute_child_of_the_ring_covering_the_screen(self):
        errs = self.errs("c1-cover")
        self.assertIn("is not visible: it is covered by", errs)
        self.assertIn("out of the ring's box", errs)

    def test_c2_a_ring_around_a_no_break_space(self):
        self.assertIn("the ring holds nothing visible", self.errs("ring-nbsp"))

    def test_c2_faded_text_outside_the_ring(self):
        self.assertIn("text “Sepetim” is not visible: opacity 0", self.errs("faded"))

    def test_a_card_that_fails_to_render_after_a_failed_one_keeps_exit_1(self):
        p = rc([self.paths["faded"], self.paths["broken"]])
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        self.assertIn("UNAVAILABLE", p.stdout)
        alone = rc([self.paths["broken"]])
        self.assertEqual(alone.returncode, 3, alone.stdout + alone.stderr)


if __name__ == "__main__":
    unittest.main()
