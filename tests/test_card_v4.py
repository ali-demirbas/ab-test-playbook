#!/usr/bin/env python3
"""Kartın 4. aşama sözleşmesi için testler. Bağımlılıksız (unittest).

Kart karşılaştırmanın kendisidir: kaydın başlığı, iki mockup, halka ve etiketi,
iki hap. Metin sütunu, açıklama, kutular, alt bilgi, etiketler ve notlar ne
kartta ne şablonda ne oluşturucuda var; kaydın KPI, guardrail, kanıt, öncelik,
uyarı, değişmez ve detay metni karta hiç yazılmaz. Taslak şeridi yerleşimi
değiştirmez. Eski düz kart girdisi artık kurulmaz. Ölçüler render_check.mjs'de
tarayıcıda denetlenir; burada şablonun onları mümkün kılan kuralları sabitlenir.
"""
import contextlib
import copy
import io
import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import build_card as bc  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
STYLE = re.search(r"<style>(.*?)</style>", TEMPLATE, re.S).group(1)


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        sc = json.load(fh)
    sc.pop("review", None)
    return sc


def css_rule(selector):
    m = re.search(r"(?m)^\s*" + re.escape(selector) + r"\{([^}]*)\}", STYLE)
    return m.group(1) if m else None


def die_text(fn, *args, **kw):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            fn(*args, **kw)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected the builder to refuse; it built instead")


def run_main(scenario, *extra):
    """build_card.main() on a temp file → (exit code, stdout, stderr, written text or None)."""
    with tempfile.TemporaryDirectory() as tmp:
        src, dst = os.path.join(tmp, "s.json"), os.path.join(tmp, "card.html")
        with open(src, "w", encoding="utf-8") as fh:
            json.dump(scenario, fh, ensure_ascii=False)
        out, err = io.StringIO(), io.StringIO()
        msg_lang = bc._MSG_LANG
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = bc.main(["--template", TEMPLATE_PATH, "--scenario", src, "--out", dst] + list(extra))
            except SystemExit as exc:
                code = exc.code
            finally:
                bc._MSG_LANG = msg_lang
        written = None
        if os.path.isfile(dst):
            with open(dst, encoding="utf-8") as fh:
                written = fh.read()
        return code, out.getvalue(), err.getvalue(), written


# Markup and selectors of the removed text column, boxes, footer, tags and notes.
REMOVED_MARKUP = ('class="copy"', 'class="left"', 'class="mockups"', 'class="desc"', 'class="box', "<header>",
                  "<footer", "card-foot", 'class="tags"', "foot-note", "shift-note", 'class="role', "<ul>", "<li>")
REMOVED_SELECTORS = (".copy", ".desc", ".box", ".card-foot", ".tags", ".shift-note", ".role", ".mockups", ".left")
REMOVED_PLACEHOLDERS = ("{{DESC}}", "{{H_TEST}}", "{{H_KPI}}", "{{H_DONT}}", "{{TEST_ITEMS}}", "{{KPI_ITEMS}}",
                        "{{DONT_ITEMS}}", "{{FOOTER}}", "{{SHIFT_NOTE_A}}", "{{SHIFT_NOTE_B}}")


class TestOnlyTheComparison(unittest.TestCase):
    def test_the_built_card_has_no_text_column_box_or_footer_markup(self):
        built = bc.build(TEMPLATE, example())
        body = built[built.index("<body>"):]
        for fragment in REMOVED_MARKUP:
            self.assertNotIn(fragment, body, fragment)
        # What is there: the title, two pills, two frames.
        self.assertEqual(body.count('<h1 class="title">'), 1)
        self.assertEqual(body.count('class="pill pill-a">Variant A</span>'), 1)
        self.assertEqual(body.count('class="pill pill-b">Variant B</span>'), 1)
        self.assertEqual(body.count('<div class="phone">'), 2)

    def test_the_template_carries_none_of_it_either(self):
        for ph in REMOVED_PLACEHOLDERS:
            self.assertNotIn(ph, TEMPLATE)
        for sel in REMOVED_SELECTORS:
            self.assertNotRegex(STYLE, r"(?m)(^|[\s,}])%s[\s{.:,\[]" % re.escape(sel), sel)

    def test_the_builder_has_no_text_column_code_left(self):
        for name in ("L10N", "render_item", "render_list", "render_footer", "record_boxes", "drop_boxes",
                     "shift_note", "priority_label", "is_scenario_shape", "LEGACY_BOXES", "strip_mockup_region"):
            self.assertFalse(hasattr(bc, name), name)

    def test_the_record_text_never_appears_in_the_card(self):
        sc = example()
        sc["detail"] = {
            "test_items": ["Detay maddesi QX-test-1", "Detay maddesi QX-test-2", "Detay maddesi QX-test-3"],
            "kpis": [{"name": "QX-kpi-primary", "role": "primary", "question": "QX-kpi-question?"},
                     {"name": "QX-kpi-guardrail", "role": "guardrail", "question": "QX-kpi-guard?"},
                     {"name": "QX-kpi-second", "role": "secondary", "question": "QX-kpi-q2?"}],
            "dont_items": ["QX-dont-1", "QX-dont-2", "QX-dont-3"],
        }
        sc["warnings"] = sc["warnings"] + [{"type": "regulation", "text": "QX-regulation-warning"}]
        sc["objection"] = "QX-objection"
        sc["source_note"] = "QX-source-note"
        sc["numeric_change"] = "QX-numeric-change"
        built = bc.build(TEMPLATE, sc)
        texts = [sc["problem"], sc["mechanism"], sc["variable"], sc["primary_kpi"]["name"],
                 sc["primary_kpi"]["denominator"], sc["guardrail"]["name"], sc["guardrail"]["denominator"],
                 sc["evidence"]["note"], sc["priority"]["rationale"], sc["adapted_from"], sc["objection"],
                 sc["source_note"], sc["numeric_change"], sc["variants"][0]["description"],
                 sc["variants"][1]["description"]]
        texts += [w["text"] for w in sc["warnings"]] + list(sc["invariants"])
        texts += ["QX-test-1", "QX-kpi-primary", "QX-kpi-question", "QX-dont-1"]
        for text in texts:
            self.assertNotIn(bc.escape(text), built, text)
            self.assertNotIn(text, built, text)
        # Nor the labels that used to frame them.
        for word in ("Kanıt", "Öncelik", "Kaynak", "Birincil", "Guardrail", "Uyarılar", "Mekanizma", "Temsilî",
                     "Nötr palet", "Arşiv örüntüsü", "Orta"):
            self.assertNotIn(word, built, word)

    def test_the_title_is_the_only_record_text_and_it_is_escaped(self):
        sc = example()
        sc["title"] = "“İndirim” < 3 & <b>kalın</b> mı?"
        built = bc.build(TEMPLATE, sc)
        escaped = "“İndirim” &lt; 3 &amp; &lt;b&gt;kalın&lt;/b&gt; mı?"
        self.assertIn("<title>%s</title>" % escaped, built)
        self.assertIn('<h1 class="title">%s</h1>' % escaped, built)
        self.assertNotIn("<b>kalın</b>", built)

    def test_mockup_basis_is_metadata_for_the_reviewer_never_printed(self):
        sc = example()
        self.assertEqual(bc.normalize(sc)["mockup_basis"], "representative")
        built = bc.build(TEMPLATE, sc)
        sc["card"]["mockup_basis"] = "shared_page"
        self.assertEqual(bc.build(TEMPLATE, sc), built)  # the card bytes don't depend on it
        sc["variants"][0]["is_current"] = True
        del sc["card"]["mockup_basis"]
        self.assertEqual(bc.normalize(sc)["mockup_basis"], "shared_page")
        sc["card"]["mockup_basis"] = "photo"
        self.assertIn("mockup_basis must be one of", die_text(bc.normalize, sc))


class TestDraftRibbon(unittest.TestCase):
    def setUp(self):
        self.final = bc.final_html(TEMPLATE, example())[0]
        self.fp = bc.html_fingerprint(self.final)
        self.draft = bc.draft_html(self.final, self.fp, "tr")

    def test_the_ribbon_is_the_only_new_line_inside_the_card(self):
        ribbon = [ln for ln in self.draft.splitlines() if 'id="abtest-draft"' in ln]
        self.assertEqual(len(ribbon), 1)
        lines = self.draft.splitlines()
        self.assertTrue(lines[lines.index(ribbon[0]) - 1].startswith('<div class="card"'))
        # Draft minus the ribbon and the two metas is the final card, byte for byte.
        rest = [ln for ln in lines if ln not in ribbon and not ln.startswith('<meta name="abtest-')]
        self.assertEqual("\n".join(rest) + "\n", self.final)

    def test_the_ribbon_takes_no_space(self):
        style = re.search(r'id="abtest-draft" role="status" style="([^"]*)"', self.draft).group(1)
        self.assertIn("position:absolute", style)
        self.assertIn("top:0", style)
        self.assertIn("pointer-events:none", style)
        for prop in ("margin", "position:relative", "position:static", "transform"):
            self.assertNotIn(prop, style)
        # It overlays the card, whose box clips it and doesn't grow with it.
        card = css_rule(".card")
        for decl in ("position:relative", "width:1600px", "height:900px", "overflow:hidden"):
            self.assertIn(decl, card)

    def test_the_ribbon_text(self):
        self.assertIn(">TASLAK · incelenmedi</div>", self.draft)
        self.assertIn(">DRAFT · not reviewed</div>", bc.draft_html(self.final, self.fp, "en"))


class TestLayoutRules(unittest.TestCase):
    """The contract's layout, as CSS: render_check.mjs measures the rendered result."""

    def test_card_title_and_stage(self):
        card = css_rule(".card")
        for decl in ("width:1600px", "height:900px", "padding:40px 48px", "background:#f4f5f7"):
            self.assertIn(decl, card)
        title = css_rule(".title")
        for decl in ("font-size:30px", "line-height:1.25", "font-weight:650", "color:#111827"):
            self.assertIn(decl, title)
        stage = css_rule(".stage")
        self.assertIn("grid-template-columns:repeat(2,minmax(0,1fr))", stage)
        self.assertIn("column-gap:48px", stage)

    def test_system_font_stack_no_web_fonts(self):
        self.assertIn('font-family:-apple-system,"Segoe UI",Inter,Roboto,"Helvetica Neue",Arial,sans-serif', STYLE)
        self.assertNotIn("@font-face", STYLE)
        self.assertNotIn("fonts.googleapis", TEMPLATE)

    def test_pills(self):
        # A and B carry the same neutral pill (no winner colour); only the text differs.
        self.assertIn("background:#ffffff;border:1px solid #d1d5db;color:#111827", css_rule(".pill-a,.pill-b"))
        self.assertNotRegex(STYLE, r"(?m)^\s*\.pill-[ab]\{")  # no separate style for one arm
        pill = css_rule(".pill")
        for decl in ("font-size:14px", "font-weight:600", "border-radius:999px"):
            self.assertIn(decl, pill)

    def test_frames_are_as_tall_as_their_content(self):
        phone, browser = css_rule(".phone"), css_rule(".browser")
        for decl in ("width:420px", "border:1px solid #d1d5db", "border-radius:36px", "--fs:15px", "--tap:44px"):
            self.assertIn(decl, phone)
        self.assertIn("width:100%", browser)
        self.assertIn("--fs:14px", browser)
        for rule in (phone, browser):
            self.assertNotRegex(rule, r"(^|;)\s*height:")
            self.assertNotRegex(rule, r"min-height:(?!0;)")  # min-height:0 only lets it shrink
            self.assertIn("overflow:hidden", rule)  # capped at the stage, clipped (render_check: error)
        self.assertIn("flex-shrink:0", css_rule(".screen>*,.browser-screen>*"))
        self.assertIn("font-size:14px", css_rule(".statusbar"))

    def test_ring_and_label(self):
        self.assertIn("--ring:#e11d48", STYLE)
        ring = css_rule(".hl")
        for decl in ("outline:3px solid var(--ring)", "outline-offset:4px", "border-radius:10px"):
            self.assertIn(decl, ring)
        label = css_rule(".hl[data-note]::after")
        for decl in ("right:-7px", "background:var(--ring)", "color:#ffffff", "font-size:12.5px", "font-weight:600",
                     "border-radius:999px"):
            self.assertIn(decl, label)

    def test_no_text_below_12px(self):
        sizes = [float(v) for v in re.findall(r"font-size:([\d.]+)px", STYLE)]
        sizes += [float(v) for v in re.findall(r"--fs[\w-]*:([\d.]+)px", STYLE)]
        self.assertTrue(sizes)
        self.assertGreaterEqual(min(sizes), 12, sorted(sizes)[:5])
        # The only scaling is a phone frame as a whole (proportions kept) and its continuation sheet at the same
        # scale: card.phone_scale 1 / 1.2 / 1.4; stage phones at .8 with larger size variables. Nothing scales text alone.
        self.assertEqual(re.findall(r"zoom:[^;}]*", re.sub(r"/\*.*?\*/", "", STYLE, flags=re.S)),
                         ["zoom:1.2", "zoom:1", "zoom:1.4", "zoom:1.2", "zoom:1", "zoom:1.4", "zoom:.8"])
        stage = css_rule(".card .stage-col>.phone")
        stage_sizes = [float(v) for v in re.findall(r"--fs[\w-]*:([\d.]+)px", stage)]
        self.assertTrue(stage_sizes)
        self.assertGreaterEqual(min(stage_sizes) * 0.8, 12)  # rendered size inside a stage phone
        self.assertIn("zoom:1.2", css_rule(".phone"))
        self.assertIn("zoom:1", css_rule('.card[data-phone-scale="1"] .phone'))
        self.assertNotRegex(STYLE, r"transform:\s*scale")

    def test_neutral_palette(self):
        for colour in ("#111827", "#374151", "#6b7280", "#e5e7eb", "#d1d5db", "#2563eb", "#15803d", "#b45309"):
            self.assertIn(colour, STYLE)
        self.assertIn("--brand:#1f2937; --on-brand:#ffffff;", STYLE)
        for old in ("#08616b", "#6b3804", "#17086b", "#ff6a00", "#e62d37", "#5cf679"):
            self.assertNotIn(old, TEMPLATE, old)

    def test_the_developer_comment_documents_the_layout_and_the_allowlist(self):
        comment = re.search(r"<!--(.*?)-->", TEMPLATE, re.S).group(1)
        for fragment in ("1600 × 900", "420px", "phone-web", "bottom_nav", "data-pos=\"below\"", "NEFES PAYI",
                         "div span p b strong i em u s small sup sub br hr ul ol li", "aria-*"):
            self.assertIn(fragment, comment)
        for gone in ("shift_note", "footer", "metin sütunu 580px"):
            self.assertNotIn(gone, comment)


class TestOnlyRecordsBuild(unittest.TestCase):
    """The legacy flat card input is gone: only scenario records build."""

    FLAT = {"title": "Kupon alanı katlanınca dönüşüm artar mı?", "desc": "Açıklama.",
            "test_items": ["a", "b", "c"], "kpi_items": ["x", "y", "z"], "dont_items": ["p", "q", "r"],
            "variant_a": '<div class="r-h">Sepet</div>',
            "variant_b": '<div class="hl" data-note="yeni"><div class="r-h">Sepet</div></div>'}

    def test_build_refuses_a_record_without_card(self):
        self.assertIn("the record has no `card` object", die_text(bc.build, TEMPLATE, copy.deepcopy(self.FLAT)))

    def test_main_refuses_the_flat_shape_as_a_draft_too(self):
        for extra in ((), ("--draft",)):
            code, _, err, written = run_main(self.FLAT, *extra)
            self.assertEqual(code, 1, err)
            self.assertIsNone(written)
            self.assertIn("unknown field 'desc'", err)
            self.assertIn("the record has no `card` object", err)
            self.assertIn("REFUSED at the “record validation” gate", err)

    def test_the_legacy_example_is_gone(self):
        self.assertFalse(os.path.exists(os.path.join(REPO_ROOT, "examples", "scenario-card-input.json")))

    def test_a_stamped_record_still_builds_its_final(self):
        sc = example()
        sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}}
        sc["review"]["mockup_reviewer"] = {"verdict": "PASS", "fingerprint": bc.final_fingerprint(TEMPLATE, sc)}
        code, out, err, written = run_main(sc)
        self.assertEqual(code, 0, err)
        self.assertEqual(bc.html_fingerprint(written), sc["review"]["mockup_reviewer"]["fingerprint"])


if __name__ == "__main__":
    unittest.main()
