#!/usr/bin/env python3
"""v2.1 kart özellikleri için unit testler. Bağımlılıksız (unittest).

Kapsam: tek JSON (senaryo kaydı), kartın dili, phone-web, web yerleşimi
(yapısal), halka yerleşimi ve fark türü, marka değişkenleri, bileşenler.
Tarayıcıda ölçüm burada yapılmaz (pytest saf Python kalır); onun için
scripts/render_check.mjs.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from build_card import (  # noqa: E402
    build, self_verify, fixed_lines, ring_problems, hl_count, domain_of, brand_css,
)

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


RECORD_KEYS = ("title", "lang", "device", "difference", "variable", "variants", "warnings", "numeric_change")


def flat(**over):
    """A minimal record as build() reads it. Record fields (title, lang, device,
    difference …) go to the top level, everything else into `card`."""
    rec = {
        "title": "Kupon alanı katlanınca dönüşüm artar mı?",
        "card": {
            "variant_a": '<div class="r-h">Sepet</div>',
            "variant_b": '<div class="hl" data-note="Yeni"><div class="r-h">Sepetim</div></div>',
        },
    }
    for key, value in over.items():
        (rec if key in RECORD_KEYS else rec["card"])[key] = value
    return rec


def css_rule(selector):
    """Body of the first CSS rule whose selector list is exactly `selector`."""
    m = re.search(r"(?m)^\s*" + re.escape(selector) + r"\{([^}]*)\}", TEMPLATE)
    return m.group(1) if m else None



# A refusal writes its reason to stderr before it exits; the tests that expect one would print it on every
# run. The test runner keeps its own stream, so only the builder's messages are silenced.
_STDERR = None


def setUpModule():
    global _STDERR
    import io
    _STDERR, sys.stderr = sys.stderr, io.StringIO()


def tearDownModule():
    sys.stderr = _STDERR

class TestOneJson(unittest.TestCase):
    """Senaryo kaydı kartı doğrudan üretir."""

    def test_schema_shape_builds_and_verifies(self):
        sc = example()
        built = build(TEMPLATE, sc)
        self_verify(built, TEMPLATE, "phone-web")
        self.assertIn('<h1 class="title">%s</h1>' % sc["title"], built)
        self.assertIn("<title>%s</title>" % sc["title"], built)

    def test_missing_variant_exits(self):
        sc = example()
        del sc["card"]["variant_b"]
        with self.assertRaises(SystemExit):
            build(TEMPLATE, sc)


class TestLanguage(unittest.TestCase):
    def test_default_is_turkish(self):
        built = build(TEMPLATE, flat())
        self.assertIn('<html lang="tr">', built)

    def test_english_frame(self):
        built = build(TEMPLATE, flat(lang="en"))
        self.assertIn('<html lang="en">', built)
        # Pills stay "Variant A/B" in every language.
        self.assertIn(">Variant A<", built)
        self.assertIn(">Variant B<", built)

    def test_unknown_language_exits(self):
        with self.assertRaises(SystemExit):
            build(TEMPLATE, flat(lang="de"))

    def test_drift_check_still_covers_the_fixed_skeleton(self):
        lines = fixed_lines(TEMPLATE)
        self.assertTrue(any(".pill-a,.pill-b{background:#ffffff;border:1px solid #d1d5db;color:#111827}" in ln for ln in lines))
        self.assertFalse(any("{{" in ln for ln in lines))
        built = build(TEMPLATE, flat(lang="en"))
        self_verify(built, TEMPLATE)  # dil değişimi sürüklenme değildir
        with self.assertRaises(SystemExit):
            self_verify(built.replace(".pill-a,.pill-b{background:#ffffff", ".pill-a,.pill-b{background:#222"), TEMPLATE)


class TestDevices(unittest.TestCase):
    def test_phone_web_has_address_bar_and_no_tab_bar(self):
        built = build(TEMPLATE, flat(device="phone-web", url="https://www.magaza.example/sepet?x=1",
                                     bottom_nav=["Ana Sayfa"]))
        self_verify(built, TEMPLATE, "phone-web")
        self.assertEqual(built.count('class="m-addr"'), 2)
        self.assertEqual(built.count('<span class="lock"></span>'), 2)
        self.assertIn('<span class="m-url">magaza.example</span>', built)
        self.assertNotIn('class="bottomnav"', built)
        self.assertIn('data-device="phone-web"', built)

    def test_phone_web_domain_is_escaped(self):
        built = build(TEMPLATE, flat(device="phone-web", url='x"><b>y'))
        self.assertNotIn('<b>y', built)

    def test_domain_of(self):
        self.assertEqual(domain_of("https://www.site.example/a/b"), "site.example")
        self.assertEqual(domain_of("site.example"), "site.example")
        self.assertEqual(domain_of(""), "")

    def test_native_phone_keeps_tab_bar_only_when_given(self):
        self.assertNotIn('class="bottomnav"', build(TEMPLATE, flat(device="phone")))
        built = build(TEMPLATE, flat(device="phone", bottom_nav=["Ana Sayfa", "Hesabım"]))
        self.assertEqual(built.count('class="bottomnav"'), 2)
        self.assertNotIn('class="m-addr"', built)

    def test_both_is_refused_with_guidance(self):
        with self.assertRaises(SystemExit):
            build(TEMPLATE, flat(device="both"))

    def test_card_device_overrides_scenario_device(self):
        sc = example()
        sc["device"] = "phone"
        sc["card"]["device"] = "web"
        sc["card"].pop("phone_scale", None)  # phone_scale belongs to a phone frame
        built = build(TEMPLATE, sc)
        self.assertEqual(built.count('class="browser-screen"'), 2)


class TestWebLayout(unittest.TestCase):
    """Ölçüm render_check.mjs'de; burada düzeni mümkün kılan kurallar sabitlenir."""

    def test_frames_shrink_to_their_column(self):
        self.assertIn("min-width:0", css_rule(".variant"))
        browser = css_rule(".browser")
        self.assertIn("width:100%", browser)
        self.assertNotIn("width:520px", browser)

    def test_built_web_card_is_marked(self):
        built = build(TEMPLATE, flat(device="web", url="site.example"))
        self.assertIn('data-device="web"', built)
        self_verify(built, TEMPLATE, "web")


class TestStatusBar(unittest.TestCase):
    def test_battery_glyph_replaces_power_symbol(self):
        built = build(TEMPLATE, flat())
        self.assertNotIn("⏻", built)
        self.assertIn('<span class="batt"></span>', built)
        self.assertIsNotNone(css_rule(".batt"))


class TestHighlight(unittest.TestCase):
    def test_ring_takes_no_layout_space(self):
        rule = css_rule(".hl")
        self.assertIn("outline:", rule)
        self.assertIn("outline-offset:", rule)
        self.assertNotIn("border:", rule)
        self.assertNotIn("padding", rule)
        # No glow and no fill: the ring is the outline alone.
        self.assertNotIn("box-shadow", rule)
        self.assertNotIn("background", rule)

    def test_label_position_options(self):
        self.assertIn('.hl[data-pos="below"]::after', TEMPLATE)
        built = build(TEMPLATE, flat(note_pos="below"))
        self.assertIn('data-note-pos="below"', built)
        self.assertIn('data-note-pos="above"', build(TEMPLATE, flat()))
        with self.assertRaises(SystemExit):
            build(TEMPLATE, flat(note_pos="left"))

    def test_hl_count_reads_class_tokens(self):
        self.assertEqual(hl_count('<div class="hl">x</div><div class="r-hl">y</div>'), 1)
        self.assertEqual(hl_count("<div class='r-item hl'></div><span class=\"hl\"></span>"), 2)
        self.assertEqual(hl_count('<div class="highlight"></div>'), 0)


class TestDifference(unittest.TestCase):
    A_PLAIN = '<div class="r-h">Sepet</div>'
    # The ringed element differs from A's: two arms that render the same are refused (audit M6).
    RINGED = '<div class="hl" data-note="X"><div class="r-h">Sepetim</div></div>'
    A_RINGED = '<div class="hl" data-note="Eski"><div class="r-h">Sepet</div></div>'
    # A move: the same ringed element at another place, next to an unchanged neighbour.
    NEXT = '<div class="r-sub">Alt satır</div>'

    def build_with(self, difference, a, b, **over):
        return build(TEMPLATE, flat(difference=difference, variant_a=a, variant_b=b, **over))

    def test_add_ring_only_in_b(self):
        self.build_with("add", self.A_PLAIN, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("add", self.RINGED, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("add", self.A_PLAIN, self.A_PLAIN)

    def test_remove_ring_only_in_a(self):
        # The ring in A is labelled; B is genuinely empty there. No note under the frame.
        self.build_with("remove", self.RINGED, self.A_PLAIN)
        with self.assertRaises(SystemExit):
            self.build_with("remove", self.RINGED, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("remove", self.A_PLAIN, self.A_PLAIN)

    def test_move_ring_in_both(self):
        self.build_with("move", self.RINGED + self.NEXT, self.NEXT + self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("move", self.A_PLAIN + self.NEXT, self.NEXT + self.RINGED)
        with self.assertRaises(SystemExit):  # rings in place: A and B render the same
            self.build_with("move", self.RINGED, self.RINGED)

    def test_change_ring_in_b_a_optional(self):
        self.build_with("change", self.A_PLAIN, self.RINGED)
        self.build_with("change", self.A_RINGED, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("change", self.RINGED, self.A_PLAIN)

    def test_turkish_aliases(self):
        self.build_with("ekle", self.A_PLAIN, self.RINGED)
        self.build_with("Değiştir", self.A_PLAIN, self.RINGED)
        self.build_with("kaldır", self.RINGED, self.A_PLAIN)
        self.build_with("taşı", self.RINGED + self.NEXT, self.NEXT + self.RINGED)

    def test_unknown_difference_exits(self):
        with self.assertRaises(SystemExit):
            self.build_with("swap", self.A_PLAIN, self.RINGED)

    def test_no_difference_means_no_enforcement(self):
        build(TEMPLATE, flat(variant_a=self.A_PLAIN, variant_b=self.RINGED))

    def test_problems_are_reported_in_turkish_too(self):
        probs = ring_problems("add", self.RINGED, self.RINGED, lang="tr")
        self.assertTrue(any("ekle" in p for p in probs), probs)


class TestBrand(unittest.TestCase):
    def test_cta_uses_brand_variables(self):
        rule = css_rule(".r-cta")
        self.assertIn("var(--brand)", rule)
        self.assertIn("var(--on-brand)", rule)
        self.assertNotRegex(rule, r"#[0-9a-fA-F]{3,8}")

    def test_brand_override_is_injected(self):
        built = build(TEMPLATE, flat(brand={"primary": "#c9392b", "on_primary": "#fff", "name": "Örnek"}))
        self_verify(built, TEMPLATE)
        self.assertIn(':root{--brand:#c9392b;--on-brand:#fff;--brand-name:"Örnek"}', built)

    def test_neutral_palette_without_brand(self):
        built = build(TEMPLATE, flat())
        self.assertIn("--brand:#1f2937; --on-brand:#ffffff;", built)
        self.assertNotIn(":root{--brand:", built)

    def test_colour_injection_is_refused(self):
        with self.assertRaises(SystemExit):
            build(TEMPLATE, flat(brand={"primary": "red}</style><script>alert(1)</script>"}))

    def test_brand_name_cannot_close_the_style_block(self):
        css = brand_css({"name": '"</style><script>x</script>'})
        self.assertNotIn("<", css)
        self.assertNotIn('""', css)


class TestComponents(unittest.TestCase):
    REQUIRED = (
        ".r-header", ".r-logo", ".r-nav", ".r-tel", ".r-tabs span", ".r-field.select", ".r-cta.outline",
        ".r-grid", ".r-tile", ".r-plan", ".r-plan-price", ".r-steps", ".r-progress", ".r-check", ".r-radio",
        ".r-info", ".r-chips", ".r-chip", ".r-overlay", ".r-modal", ".r-search", ".r-suggest", ".ph.hero",
        ".r-badge", ".r-old", ".r-now", ".r-per", ".r-banner",
    )

    def test_components_are_defined(self):
        for sel in self.REQUIRED:
            self.assertRegex(TEMPLATE, r"(?m)^\s*[^{}]*" + re.escape(sel) + r"[\s,{:.\[>]", sel)

    def test_components_are_documented_in_the_template_comment(self):
        comment = re.search(r"<!--(.*?)-->", TEMPLATE, re.S).group(1)
        for cls in ("r-header", "r-tabs", "r-grid", "r-plan", "r-steps", "r-check", "r-chips",
                    "r-overlay", "r-search", "ph hero"):
            self.assertIn(cls, comment)

    def test_no_external_assets(self):
        self.assertNotRegex(TEMPLATE, r"(?i)(https?:)?//[a-z0-9.-]+\.[a-z]{2,}/[^\s\"']*\.(css|js|woff2?|ttf|png|jpe?g)")
        self.assertNotIn("@import", TEMPLATE)
        self.assertNotIn("<link", TEMPLATE)


if __name__ == "__main__":
    unittest.main()
