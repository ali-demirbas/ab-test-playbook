#!/usr/bin/env python3
"""v2.1 kart özellikleri için unit testler. Bağımlılıksız (unittest).

Kapsam: tek JSON (şema biçimi + eski düz biçim), dil sözlüğü, phone-web,
web yerleşimi (yapısal), alt bilgi, kayma notları, halka yerleşimi ve fark
türü, KPI rol rozetleri, marka değişkenleri, bileşenler. Tarayıcıda ölçüm
burada yapılmaz (pytest saf Python kalır); onun için scripts/render_check.mjs.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from build_card import (  # noqa: E402
    build, self_verify, fixed_lines, render_item, ring_problems, hl_count, domain_of, brand_css,
)

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
LEGACY_EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario-card-input.json")

with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


def flat(**over):
    base = {
        "title": "Kupon alanı katlanınca dönüşüm artar mı?",
        "desc": "Açıklama.",
        "test_items": ["a", "b", "c"],
        "kpi_items": [{"label": "RPV", "text": "artıyor mu?", "role": "primary"}],
        "dont_items": ["x", "y", "z"],
        "variant_a": '<div class="r-h">Sepet</div>',
        "variant_b": '<div class="hl" data-note="yeni"><div class="r-h">Sepet</div></div>',
    }
    base.update(over)
    return base


def css_rule(selector):
    """Body of the first CSS rule whose selector list is exactly `selector`."""
    m = re.search(r"(?m)^\s*" + re.escape(selector) + r"\{([^}]*)\}", TEMPLATE)
    return m.group(1) if m else None


class TestOneJson(unittest.TestCase):
    """Şema biçimi kartı doğrudan üretir; eski düz biçim çalışmaya devam eder."""

    def test_schema_shape_builds_and_verifies(self):
        built = build(TEMPLATE, example())
        self_verify(built, TEMPLATE)
        self.assertIn("Açık kupon kodu alanı sepet terkini artırır mı?", built)
        # rationale → açıklama
        self.assertIn("Görünür bir kupon kutusu", built)
        # kpis → KPI kutusu, ad kalın etiket, soru metin
        self.assertIn("<b>Ziyaretçi Başına Gelir (RPV):</b>", built)

    def test_legacy_flat_shape_still_builds(self):
        with open(LEGACY_EXAMPLE, encoding="utf-8") as fh:
            legacy = json.load(fh)
        built = build(TEMPLATE, legacy)
        self_verify(built, TEMPLATE)
        self.assertNotIn('class="bottomnav"', built)

    def test_card_fields_may_sit_at_top_level_in_flat_shape(self):
        built = build(TEMPLATE, flat(difference="add", shift_note_b="Not"))
        self.assertIn('<div class="shift-note">Not</div>', built)

    def test_missing_variant_exits(self):
        sc = example()
        del sc["card"]["variant_b"]
        with self.assertRaises(SystemExit):
            build(TEMPLATE, sc)


class TestLanguage(unittest.TestCase):
    def test_default_is_turkish(self):
        built = build(TEMPLATE, flat())
        self.assertIn('<html lang="tr">', built)
        self.assertIn("<header>Test Edilmesi Gerekenler</header>", built)
        self.assertIn(">Birincil<", built)

    def test_english_frame(self):
        built = build(TEMPLATE, flat(lang="en"))
        self.assertIn('<html lang="en">', built)
        self.assertIn("<header>What to Test</header>", built)
        self.assertIn("<header>Primary KPIs to Track</header>", built)
        self.assertIn("<header>Never Do</header>", built)
        self.assertIn(">Primary<", built)
        self.assertNotIn("Gerekenler", built)
        # Pills stay "Variant A/B" in every language.
        self.assertIn(">Variant A<", built)

    def test_unknown_language_exits(self):
        with self.assertRaises(SystemExit):
            build(TEMPLATE, flat(lang="de"))

    def test_template_has_no_hard_coded_box_headers(self):
        self.assertIn("<header>{{H_TEST}}</header>", TEMPLATE)
        self.assertNotIn("Test Edilmesi Gerekenler", TEMPLATE)

    def test_drift_check_still_covers_the_fixed_skeleton(self):
        lines = fixed_lines(TEMPLATE)
        self.assertTrue(any(".box.kpi  header" in ln for ln in lines))
        self.assertFalse(any("{{" in ln for ln in lines))
        built = build(TEMPLATE, flat(lang="en"))
        self_verify(built, TEMPLATE)  # dil değişimi sürüklenme değildir
        with self.assertRaises(SystemExit):
            self_verify(built.replace(".box.kpi  header", ".box.kpi header"), TEMPLATE)


class TestDevices(unittest.TestCase):
    def test_phone_web_has_address_bar_and_no_tab_bar(self):
        built = build(TEMPLATE, flat(device="phone-web", url="https://www.magaza.example/sepet?x=1",
                                     bottom_nav=["Ana Sayfa"]))
        self_verify(built, TEMPLATE)
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
        built = build(TEMPLATE, sc)
        self.assertEqual(built.count('class="browser-screen"'), 2)


class TestWebLayout(unittest.TestCase):
    """Ölçüm render_check.mjs'de; burada düzeni mümkün kılan kurallar sabitlenir."""

    def test_frames_shrink_to_their_column(self):
        self.assertIn("min-width:0", css_rule(".variant"))
        browser = css_rule(".browser")
        self.assertIn("width:100%", browser)
        self.assertIn("max-width:", browser)
        self.assertNotIn("width:520px", browser)

    def test_web_text_column_is_at_least_520px(self):
        rule = css_rule('.card[data-device="web"] .copy')
        self.assertIsNotNone(rule)
        width = int(re.search(r"flex:0 0 (\d+)px", rule).group(1))
        self.assertGreaterEqual(width, 520)

    def test_web_mockups_take_the_remaining_width(self):
        rule = css_rule('.card[data-device="web"] .left')
        self.assertIn("flex:1 1 auto", rule)

    def test_built_web_card_is_marked(self):
        built = build(TEMPLATE, flat(device="web", url="site.example"))
        self.assertIn('data-device="web"', built)


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
    RINGED = '<div class="hl" data-note="x"><div class="r-h">Sepet</div></div>'

    def build_with(self, difference, a, b, **over):
        return build(TEMPLATE, flat(difference=difference, variant_a=a, variant_b=b, **over))

    def test_add_ring_only_in_b(self):
        self.build_with("add", self.A_PLAIN, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("add", self.RINGED, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("add", self.A_PLAIN, self.A_PLAIN)

    def test_remove_ring_only_in_a_and_needs_shift_note(self):
        built = self.build_with("remove", self.RINGED, self.A_PLAIN, shift_note_b="Alan kaldırıldı, içerik yukarı kaydı")
        self.assertIn('<div class="shift-note">Alan kaldırıldı, içerik yukarı kaydı</div>', built)
        with self.assertRaises(SystemExit):
            self.build_with("remove", self.RINGED, self.A_PLAIN)
        with self.assertRaises(SystemExit):
            self.build_with("remove", self.RINGED, self.RINGED, shift_note_b="Not")

    def test_move_ring_in_both(self):
        self.build_with("move", self.RINGED, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("move", self.A_PLAIN, self.RINGED)

    def test_change_ring_in_b_a_optional(self):
        self.build_with("change", self.A_PLAIN, self.RINGED)
        self.build_with("change", self.RINGED, self.RINGED)
        with self.assertRaises(SystemExit):
            self.build_with("change", self.RINGED, self.A_PLAIN)

    def test_turkish_aliases(self):
        self.build_with("ekle", self.A_PLAIN, self.RINGED)
        self.build_with("Değiştir", self.A_PLAIN, self.RINGED)
        self.build_with("kaldır", self.RINGED, self.A_PLAIN, shift_note_b="Not")
        self.build_with("taşı", self.RINGED, self.RINGED)

    def test_unknown_difference_exits(self):
        with self.assertRaises(SystemExit):
            self.build_with("swap", self.A_PLAIN, self.RINGED)

    def test_no_difference_means_no_enforcement(self):
        build(TEMPLATE, flat(variant_a=self.A_PLAIN, variant_b=self.A_PLAIN))

    def test_problems_are_reported_in_turkish_too(self):
        probs = ring_problems("add", self.RINGED, self.RINGED, lang="tr")
        self.assertTrue(any("ekle" in p for p in probs), probs)


class TestShiftNotes(unittest.TestCase):
    def test_notes_sit_under_the_frame_not_in_the_screen(self):
        built = build(TEMPLATE, flat(shift_note_a="A notu", shift_note_b="B notu"))
        screen_b = built.split('<div class="screen">')[2].split("</div>\n      </div>")[0]
        self.assertNotIn("shift-note", screen_b)
        self.assertIn('<div class="shift-note">A notu</div>', built)

    def test_notes_are_escaped(self):
        built = build(TEMPLATE, flat(shift_note_b="<b>x</b> & y"))
        self.assertIn("&lt;b&gt;x&lt;/b&gt; &amp; y", built)


class TestFooter(unittest.TestCase):
    def footer(self, built):
        m = re.search(r'<footer class="card-foot">(.*?)</footer>', built, re.S)
        return m.group(1) if m else ""

    def test_tags_line(self):
        sc = example()
        sc["source"] = "adapted"
        sc["adapted_from"] = "Kupon kutusu görünürlüğü"
        foot = self.footer(build(TEMPLATE, sc))
        self.assertIn("<b>Kaynak:</b> Arşivden uyarlandı (“Kupon kutusu görünürlüğü”)", foot)
        self.assertIn("<b>Kanıt:</b> Arşiv emsali", foot)
        self.assertIn("<b>İtiraz:</b> Fiyat", foot)
        self.assertIn("<b>ICE:</b> Orta (6×5×8)", foot)

    def test_english_tags(self):
        sc = example()
        sc["lang"] = "en"
        foot = self.footer(build(TEMPLATE, sc))
        self.assertIn("<b>Source:</b> From archive", foot)
        self.assertIn("<b>Evidence:</b> Archive precedent", foot)
        self.assertIn("Representative example", foot)

    def test_brand_note_defaults(self):
        self.assertIn("Nötr palet", self.footer(build(TEMPLATE, flat())))
        branded = self.footer(build(TEMPLATE, flat(brand={"primary": "#c9392b"})))
        self.assertIn("ekran görüntüsünden", branded)
        self.assertNotIn("Nötr palet", branded)
        self.assertNotIn("Nötr palet", self.footer(build(TEMPLATE, flat(brand_note=None))))
        self.assertIn("Kılavuz notu", self.footer(build(TEMPLATE, flat(brand_note="Kılavuz notu"))))

    def test_mockup_basis_disclaimers(self):
        self.assertIn("tarifinden yeniden çizildi", self.footer(build(TEMPLATE, flat(mockup_basis="described"))))
        self.assertIn("Temsilî örnek", self.footer(build(TEMPLATE, flat(mockup_basis="representative"))))
        self.assertNotIn("Temsilî", self.footer(build(TEMPLATE, flat(mockup_basis="shared_page"))))

    def test_basis_follows_is_current_when_absent(self):
        sc = example()
        del sc["card"]["mockup_basis"]
        sc["variants"][0]["is_current"] = True
        self.assertNotIn("Temsilî", self.footer(build(TEMPLATE, sc)))
        sc["variants"][0]["is_current"] = False
        self.assertIn("Temsilî", self.footer(build(TEMPLATE, sc)))

    def test_footer_text_is_escaped(self):
        built = build(TEMPLATE, flat(source="adapted", adapted_from="<i>x</i>", objection="a & b",
                                     footer_notes=["<script>bad()</script>"]))
        self_verify(built, TEMPLATE)
        foot = self.footer(built)
        self.assertIn("&lt;i&gt;x&lt;/i&gt;", foot)
        self.assertIn("a &amp; b", foot)
        self.assertNotIn("<script>", built)

    def test_footer_sits_under_the_mockups_not_in_a_screen(self):
        # Sol sütunda, mockup panelinin altında: metin sütunu uzun olduğunda boş
        # kalan yeri kullanır, kartı uzatmaz.
        built = build(TEMPLATE, flat())
        foot = built.index('<footer class="card-foot">')
        self.assertGreater(foot, built.rindex('<div class="variant">'))
        self.assertLess(foot, built.index('<div class="copy">'))
        self.assertGreater(foot, built.index('<div class="left">'))

    def test_bad_ice_tier_exits(self):
        with self.assertRaises(SystemExit):
            build(TEMPLATE, flat(ice={"tier": "huge"}))


class TestKpiRoles(unittest.TestCase):
    def test_role_pills_from_kpis(self):
        built = build(TEMPLATE, example())
        self.assertIn('<span class="role role-primary">Birincil</span> <b>Ziyaretçi Başına Gelir (RPV):</b>', built)
        self.assertIn('<span class="role role-guardrail">Guardrail</span>', built)
        self.assertIn('<span class="role role-secondary">İkincil</span>', built)

    def test_role_pills_in_english(self):
        out = render_item({"label": "RPV", "text": "q?", "role": "secondary"}, lang="en")
        self.assertIn(">Secondary<", out)

    def test_label_colon_rules(self):
        self.assertEqual(render_item({"label": "Kaçak", "text": "soru?"}), "<li><b>Kaçak:</b> soru?</li>")
        self.assertEqual(render_item({"label": "Kaçak:", "text": "soru?"}), "<li><b>Kaçak:</b> soru?</li>")
        self.assertEqual(render_item({"label": "Neden?", "text": "çünkü"}), "<li><b>Neden?</b> çünkü</li>")

    def test_unknown_role_exits(self):
        with self.assertRaises(SystemExit):
            render_item({"label": "x", "text": "y", "role": "north-star"})


class TestBrand(unittest.TestCase):
    def test_cta_uses_brand_variables(self):
        rule = css_rule(".r-cta")
        self.assertIn("var(--brand)", rule)
        self.assertIn("var(--on-brand)", rule)
        self.assertNotIn("#ff6a00", rule)

    def test_brand_override_is_injected(self):
        built = build(TEMPLATE, flat(brand={"primary": "#c9392b", "on_primary": "#fff", "name": "Örnek"}))
        self_verify(built, TEMPLATE)
        self.assertIn(':root{--brand:#c9392b;--on-brand:#fff;--brand-name:"Örnek"}', built)

    def test_neutral_palette_without_brand(self):
        built = build(TEMPLATE, flat())
        self.assertIn("--brand:#ff6a00", built)
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
