#!/usr/bin/env python3
"""v2.2 kart denetimleri için unit testler. Bağımlılıksız (unittest).

Kapsam: mockup gövdesi için izin listesi (allowlist) temizleyicisi, yerleştirici
yeniden tarama hatası, "JavaScript" başlığı, marka rengi, sekme çubuğu ve etkin
sekme, halka kuralları (boşluk, etiket, renk uyarısı), şema doğrulamasının
üretimden önce çalışması ve uyarı kanalı.
"""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import build_card as bc  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402
from build_card import build, self_verify, hl_count  # noqa: E402

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


def detailed():
    """The shipped example with the detailed view the user can ask for."""
    sc = example()
    sc["detail"] = {
        "test_items": [{"label": "Kaçak", "text": "Kupon alanını bağlantı arkasına almak terk oranını düşürüyor mu?"},
                       {"label": "Segment", "text": "Yeni ve dönen kullanıcıda kupon arama davranışı farklı mı?"},
                       {"label": "Kampanya", "text": "Kampanya dönemlerinde etki tersine dönüyor mu?"}],
        "kpis": [{"name": "Ziyaretçi Başına Gelir (RPV)", "role": "primary", "question": "Toplam gelir artıyor mu?"},
                 {"name": "Sipariş Tamamlama Oranı", "role": "secondary", "question": "Kaçak kapanıyor mu?"},
                 {"name": "Kupon Kullanım Oranı", "role": "guardrail", "question": "Kullanım çökmemeli."}],
        "dont_items": ["Kupon alanını tamamen kaldırmayın.", "Geçersiz kod hatasını belirsiz bırakmayın.",
                       "Aynı testte hem konumu hem metni değiştirmeyin."],
    }
    return sc


def with_b(extra):
    sc = example()
    sc["card"]["variant_b"] += "\n" + extra
    return sc


def with_both(extra):
    """The same element added to both mockups: no difference between the arms."""
    sc = example()
    sc["card"]["variant_a"] += "\n" + extra
    sc["card"]["variant_b"] += "\n" + extra
    return sc


A11Y_FULL = {"type": "accessibility",
             "text": "Yeni öğe klavyeyle erişilebilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt "
                     "ve metin kontrastı en az 4.5:1 olur."}


def stamped(sc, mockup=True):
    """The record with the reviewers' PASS stamps, computed the way the gates compute them."""
    sc = copy.deepcopy(sc)
    sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}}
    if mockup:
        sc["review"]["mockup_reviewer"] = {"verdict": "PASS", "fingerprint": bc.mockup_stamp(TEMPLATE, sc)}
    return sc


RECORD_KEYS = ("title", "lang", "device", "difference", "variable", "variants", "warnings", "numeric_change")


def flat(**over):
    """A minimal record as build() reads it. Record fields (title, device,
    warnings …) go to the top level, everything else into `card`."""
    rec = {
        "title": "Kupon alanı katlanınca dönüşüm artar mı?",
        "difference": "change",
        "card": {
            "variant_a": '<div class="r-h">Sepet</div>',
            "variant_b": '<div class="hl" data-note="Yeni"><div class="r-h">Sepetim</div></div>',
        },
    }
    for key, value in over.items():
        (rec if key in RECORD_KEYS else rec["card"])[key] = value
    return rec


def die_text(fn, *args, **kw):
    """Run fn, expect SystemExit, return what it wrote to stderr."""
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            fn(*args, **kw)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected the builder to refuse; it built instead")


def run_main(scenario, *extra):
    """build_card.main() on a temp file → (exit code, stdout, stderr, built text or None)."""
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "s.json")
        dst = os.path.join(tmp, "card.html")
        with open(src, "w", encoding="utf-8") as fh:
            json.dump(scenario, fh, ensure_ascii=False)
        out, err = io.StringIO(), io.StringIO()
        code = 0
        msg_lang = bc._MSG_LANG  # main() sets it from --lang; later tests must not inherit it
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = bc.main(["--template", TEMPLATE_PATH, "--scenario", src, "--out", dst] + list(extra))
            except SystemExit as exc:
                code = exc.code
            finally:
                bc._MSG_LANG = msg_lang
        built = None
        if os.path.isfile(dst):
            with open(dst, encoding="utf-8") as fh:
                built = fh.read()
        return code, out.getvalue(), err.getvalue(), built


# The 27 payloads of the audit plus its two controls. Each one is appended to
# variant_b of the shipped example; every one must be refused.
PAYLOADS = [
    ("s00_control_script", "<script>alert(1)</script>"),
    ("s00_control_onerror_quoted", '<img src=x onerror="alert(1)">'),
    ("s01_onerror_unquoted", "<img src=x onerror=alert(1)>"),
    ("s02_svg_onload_unquoted", "<svg onload=alert(1)></svg>"),
    ("s03_details_ontoggle_unquoted", "<details open ontoggle=alert(1)><summary>x</summary></details>"),
    ("s04_onerror_backtick", "<img src=x onerror=alert`1`>"),
    ("s05_entity_javascript_href", '<a href="jav&#x61;script:alert(1)">Kampanyayı gör</a>'),
    ("s06_tab_in_javascript_href", '<a href="java&#9;script:alert(1)">Kampanyayı gör</a>'),
    ("s07_meta_refresh", '<meta http-equiv="refresh" content="0;url=https://example.org/phish">'),
    ("s08_base_href", '<base href="https://example.org/">'),
    ("s09_link_stylesheet", '<link rel="stylesheet" href="https://example.org/x.css">'),
    ("s10_form_action", '<form action="https://example.org/collect"><input name="tckn"><button>Devam</button></form>'),
    ("s11_style_import", "<style>@import url(https://example.org/x.css);</style>"),
    ("s12_style_restyle_card", "<style>.hl{outline:none!important;box-shadow:none!important}.box.dont{display:none}</style>"),
    ("s13_inline_style_url", '<div style="background:url(https://example.org/pixel.gif)">x</div>'),
    ("s14_img_remote", '<img src="https://example.org/pixel.gif" width="1" height="1">'),
    ("s15_data_svg_img", '<img src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27/%3E">'),
    ("s16_iframe_srcdoc", '<iframe srcdoc="<b>x</b>"></iframe>'),
    ("s17_object", '<object data="x"></object>'),
    ("s18_embed", '<embed src="x">'),
    ("s19_data_text_html", '<a href="data:text/html,<b>x</b>">x</a>'),
    ("s20_formaction_button", '<form><button formaction="https://example.org/collect">Devam</button></form>'),
    ("s21_svg_animate_onbegin", "<svg><animate onbegin=alert(1) attributeName=x dur=1s></svg>"),
    ("s22_unclosed_comment", "<!--"),
    ("s23_unclosed_textarea", "<textarea>"),
    ("s24_extra_closing_divs", "</div></div></div>"),
    ("s25_css_expression", '<div style="width:expression(alert(1))">x</div>'),
    ("s26_svg_use_remote", '<svg><use href="https://example.org/sprite.svg#a"/></svg>'),
    ("s27_video_remote", '<video src="https://example.org/a.mp4" autoplay></video>'),
]

# Parser-differential and CSS tricks beyond the audit's list.
EXTRA_PAYLOADS = [
    ("attr_glued_to_quote", '<div class="a"onclick=alert(1)>x</div>'),
    ("slash_separated_handler", "<div/onclick=alert(1)>x</div>"),
    ("unquoted_class", "<div class=hl>x</div>"),
    ("single_quoted_value", "<div class='r-h'>x</div>"),
    ("duplicate_class", '<div class="a" class="hl">x</div>'),
    ("handler_uppercase", '<div ONCLICK="alert(1)">x</div>'),
    ("unclosed_tag_at_end", '<div class="r-h"'),
    ("unclosed_element", '<div class="r-h">x'),
    ("self_closing_div", '<div class="r-h"/>x'),
    ("end_tag_with_attributes", '<div>x</div onclick="alert(1)">'),
    ("cdata", "<![CDATA[x]]>"),
    ("processing_instruction", "<?xml version='1.0'?>"),
    ("doctype", "<!DOCTYPE html>"),
    ("style_backslash_escape", '<div style="background:u\\72l(https://example.org/x)">x</div>'),
    ("style_entity_url", '<div style="background:&#117;rl(https://example.org/x)">x</div>'),
    ("style_at_import", '<div style="@import \'https://example.org/x.css\'">x</div>'),
    ("style_javascript", '<div style="background:javascript:alert(1)">x</div>'),
    ("style_behavior", '<div style="behavior:url(x.htc)">x</div>'),
    ("style_moz_binding", '<div style="-moz-binding:url(x)">x</div>'),
    ("style_position_fixed", '<div style="position:fixed;inset:0">x</div>'),
    ("style_position_fixed_spaced", '<div style="position : FIXED">x</div>'),
    ("style_angle_bracket", '<div style="color:red;&lt;/style&gt;">x</div>'),
    ("style_comment", '<div style="color:red;/*x*/">x</div>'),
    ("href_plain", '<a href="https://example.org">x</a>'),
    ("src_on_allowed_tag", '<div src="https://example.org/x.png">x</div>'),
    ("action_on_allowed_tag", '<div action="https://example.org/">x</div>'),
    ("srcdoc_on_allowed_tag", '<div srcdoc="x">x</div>'),
    ("handler_on_allowed_tag", '<div onmouseover="alert(1)">x</div>'),
    ("math", "<math><mi>x</mi></math>"),
    ("input", '<input value="x">'),
    ("button", "<button>Devam</button>"),
    ("nul_byte", "<div>x\x00</div>"),
    ("block_inside_p", "<p><div>x</div></p>"),
    ("li_without_list", "<div><li>x</li></div>"),
]


class TestAllowlist(unittest.TestCase):
    """Mockup gövdesi ham HTML'dir; buraya yalnızca izinli etiket ve nitelik girer."""

    def test_every_audit_payload_is_refused(self):
        self.assertEqual(len([p for p in PAYLOADS if not p[0].startswith("s00")]), 27)
        for name, payload in PAYLOADS:
            with self.subTest(name):
                die_text(build, TEMPLATE, with_b(payload))

    def test_parser_differential_and_css_payloads_are_refused(self):
        for name, payload in EXTRA_PAYLOADS:
            with self.subTest(name):
                die_text(build, TEMPLATE, with_b(payload))

    def test_message_names_the_tag(self):
        msg = die_text(build, TEMPLATE, with_b('<img src="x.png">'))
        self.assertIn("variant_b", msg)
        self.assertIn("<img>", msg)

    def test_message_names_the_attribute(self):
        msg = die_text(build, TEMPLATE, with_b('<div onclick="alert(1)">x</div>'))
        self.assertIn("onclick", msg)
        self.assertIn("<div>", msg)

    def test_message_names_tag_and_handler_in_a_malformed_tag(self):
        msg = die_text(build, TEMPLATE, with_b("<img src=x onerror=alert(1)>"))
        self.assertIn("<img>", msg)
        self.assertIn("onerror=", msg)
        msg = die_text(build, TEMPLATE, with_b("<div class=hl ONCLICK=alert(1)>x</div>"))
        self.assertIn("onclick=", msg)

    def test_message_names_the_css_construct(self):
        msg = die_text(build, TEMPLATE, with_b('<div style="background:url(x.png)">x</div>'))
        self.assertIn("url(", msg)

    def test_messages_exist_in_turkish(self):
        _, problems = bc.parse_markup('<img src="x">', lang="tr")
        self.assertTrue(any("izin" in p for p in problems), problems)
        _, problems = bc.parse_markup('<img src="x">', lang="en")
        self.assertTrue(any("not allowed" in p for p in problems), problems)

    def test_real_component_markup_passes(self):
        # Every component the template's developer comment documents.
        ring = ('<div class="hl" data-note="Yeni" data-pos="below" style="align-self:flex-start">'
                '<div class="r-cta sm outline" style="display:flex;gap:8px;color:#0b4dc2">Devam</div></div>')
        markup = (
            '<div class="r-header"><span class="r-logo">Marka</span><span class="r-nav"><span>Ürünler</span></span>'
            '<span class="r-tel">0850 000 00 00</span></div>'
            '<div class="r-tabs"><span class="on">Kredi</span><span>Mevduat</span></div>'
            '<div class="r-label">Ad Soyad</div><div class="r-field empty">Adınızı yazın</div>'
            '<div class="r-plan featured"><div class="r-plan-name">Pro</div>'
            '<div class="r-plan-price">499 TL<span class="r-per">/ay</span></div>'
            '<ul class="r-plan-feat"><li>Sınırsız</li></ul></div>'
            '<div class="r-progress"><i style="width:40%"></i></div>'
            '<div class="r-info">Bilgi <b>kalın</b> <strong>güçlü</strong> <em>eğik</em><br>satır</div>'
            '<p class="r-sub">Kargo &amp; iade · 3 &lt; 5</p>'
        )
        # A is the same screen without the added button: the only difference sits in the ring.
        sc = flat(difference="add", variant_a=markup, variant_b=markup + ring, warnings=[A11Y_FULL])
        built = build(TEMPLATE, sc)
        self.assertIn(markup + ring, built)

    def test_literal_less_than_in_text_is_text(self):
        text = '<div class="r-h">3 < 5 ve 5 > 3</div>'
        build(TEMPLATE, flat(variant_a=text, variant_b='<div class="hl" data-note="Yeni">%s</div>' % text.replace("ve", "ile")))

    def test_markup_is_inserted_byte_for_byte(self):
        sc = example()
        built = build(TEMPLATE, sc)
        self.assertIn(sc["card"]["variant_a"], built)
        self.assertIn(sc["card"]["variant_b"], built)

    def test_whitespace_only_lines_inside_a_mockup_survive(self):
        markup = '<div class="r-h">Sepet</div>\n   \n<div class="r-sub">Alt</div>'
        self.assertIn(markup, build(TEMPLATE, flat(variant_a=markup)))

    def test_non_string_variant_is_refused_without_a_traceback(self):
        sc = example()
        sc["card"]["variant_a"] = 123
        msg = die_text(build, TEMPLATE, sc)
        self.assertIn("variant_a", msg)

    def test_ring_class_shape_stays_greppable(self):
        # agents/mockup-reviewer finds rings with this exact expression.
        import re
        built = build(TEMPLATE, example())
        hits = re.findall(r'<[^>]*class="([^"]* )?hl( [^"]*)?"[^>]*>', built)
        self.assertEqual(len(hits), 2)


class TestRingCounting(unittest.TestCase):
    def test_unquoted_class_counts_as_a_ring(self):
        self.assertEqual(hl_count("<div class=hl data-note=Eski>x</div>"), 1)

    def test_data_class_is_not_a_ring(self):
        self.assertEqual(hl_count('<div data-class="hl">x</div>'), 0)

    def test_non_string_markup_counts_zero(self):
        self.assertEqual(hl_count(123), 0)
        self.assertEqual(hl_count(None), 0)

    def test_add_with_a_ring_smuggled_into_a_is_refused(self):
        sc = example()
        sc["card"]["difference"] = sc["difference"] = "add"  # contract 5: the card can't override the record
        sc["card"]["variant_a"] = sc["card"]["variant_a"].replace(
            'class="hl" data-note="Kupon alanı açık"', "class=hl data-note=Eski")
        die_text(build, TEMPLATE, sc)

    def test_data_class_ring_in_b_is_refused(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace('class="r-link hl"', 'class="r-link" data-class="hl"')
        die_text(build, TEMPLATE, sc)


class TestPlaceholders(unittest.TestCase):
    """Doldurulan metin yeniden taranmaz: tek geçişte yerleştirme."""

    def test_title_with_a_screen_token_does_not_paste_the_mockup(self):
        sc = example()
        sc["title"] = "Not: {{VARIANT_B_SCREEN}} mı?"
        built = build(TEMPLATE, sc)
        self.assertIn("Not: {{VARIANT_B_SCREEN}} mı?", built)
        self.assertEqual(built.count('hl" data-note="'), 2)  # one ring per arm (B's ring sits on the link itself)

    def test_title_with_a_template_variable_builds(self):
        sc = example()
        sc["title"] = "Konu satırında {{AD}} ile hitap etmek açılma oranını artırır mı?"
        built = build(TEMPLATE, sc)
        self.assertIn("{{AD}} ile hitap", built)

    def test_mockup_text_with_a_template_variable_builds(self):
        built = build(TEMPLATE, with_both('<div class="r-sub">Merhaba {{FIRST_NAME}}, sepetin seni bekliyor</div>'))
        self.assertIn("Merhaba {{FIRST_NAME}},", built)

    def test_known_placeholder_names_in_text_stay_text(self):
        sc = example()
        sc["title"] = "Başlık {{TITLE}} ve {{LANG}} içeriyor mu?"
        built = build(TEMPLATE, sc)
        self.assertIn('<h1 class="title">Başlık {{TITLE}} ve {{LANG}} içeriyor mu?</h1>', built)

    def test_url_and_tab_labels_are_not_rescanned(self):
        built = build(TEMPLATE, flat(device="web", url="site.example/{{VARIANT_B_SCREEN}}"))
        self.assertIn("site.example/{{VARIANT_B_SCREEN}}", built)
        built = build(TEMPLATE, flat(device="phone", bottom_nav=["{{TITLE}}", "Hesabım"]))
        self.assertIn("<span>{{TITLE}}</span>", built)

    def test_unknown_template_placeholder_is_still_reported(self):
        tpl = TEMPLATE.replace('<h1 class="title">{{TITLE}}</h1>', '<h1 class="title">{{TITLE}}</h1> {{FOOTER_NOTE}}')
        msg = die_text(build, tpl, flat())
        self.assertIn("{{FOOTER_NOTE}}", msg)


class TestOrdinaryTextIsNotRefused(unittest.TestCase):
    def test_title_javascript_builds(self):
        sc = example()
        sc["title"] = "JavaScript: betik yükü azalınca etkileşim süresi kısalır mı?"
        code, _, err, built = run_main(stamped(sc))
        self.assertEqual(code, 0, err)
        self.assertIn('<h1 class="title">JavaScript: betik yükü', built)

    def test_text_mentioning_handlers_builds(self):
        sc = example()
        sc["problem"] = "Sayfada onclick=“...” ile açılan pencere ve javascript: bağlantıları var."
        sc["mechanism"] = "B’de <script> ve <img onerror=x> diye yazılan metin yalnızca metin olarak kalır."
        code, _, err, built = run_main(stamped(sc))
        self.assertEqual(code, 0, err)
        self.assertNotIn("onclick", built)  # the record's text never reaches the card

    def test_mockup_text_is_ordinary_text_too(self):
        text = ('<div class="r-sub">JavaScript: açık · Online = kart · onay = evet</div>'
                '<div class="r-sub">Örnek: &lt;script&gt;alert(1)&lt;/script&gt; ve &lt;a href="javascript:x"&gt;</div>')
        code, _, err, built = run_main(stamped(with_both(text)))
        self.assertEqual(code, 0, err)
        self.assertIn(text, built)

    def test_script_tag_in_built_text_is_still_refused(self):
        built = build(TEMPLATE, flat())
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            self_verify(built + "<script>x</script>", TEMPLATE)

    def test_second_layer_scans_the_raw_variants(self):
        built = build(TEMPLATE, flat())
        for bad in ('<div onclick=alert(1)>', '<a href="jav&#x61;script:alert(1)">', '<a href="java\tscript:x">',
                    "<iframe>", '<a href="data:text/html,x">'):
            with self.subTest(bad):
                with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                    self_verify(built, TEMPLATE, variants=("<div>ok</div>", bad))


class TestBrandColour(unittest.TestCase):
    def test_unknown_colour_name_is_refused(self):
        msg = die_text(build, TEMPLATE, flat(brand={"primary": "mavi", "on_primary": "#fff"}))
        self.assertIn("mavi", msg)
        self.assertIn("brand.primary", msg)

    def test_garbage_functional_colour_is_refused(self):
        die_text(build, TEMPLATE, flat(brand={"primary": "rgb(,,/%%)"}))
        die_text(build, TEMPLATE, flat(brand={"primary": "#fff", "on_primary": "rgba(999999)"}))

    def test_transparent_is_refused(self):
        die_text(build, TEMPLATE, flat(brand={"primary": "transparent"}))

    def test_real_colours_are_accepted(self):
        for value in ("#c9392b", "#FFF", "#0b4dc2cc", "rgb(11, 77, 194)", "rgba(11,77,194,.9)", "rgb(11 77 194 / 50%)",
                      "hsl(210, 80%, 40%)", "hsl(210deg 80% 40%)", "navy", "RebeccaPurple", "DarkSlateGray"):
            with self.subTest(value):
                self.assertIn("--brand:%s" % value, build(TEMPLATE, flat(brand={"primary": value})))

    def test_named_colour_set_is_the_css_list(self):
        self.assertEqual(len(bc.NAMED_COLORS), 148)
        self.assertIn("rebeccapurple", bc.NAMED_COLORS)
        self.assertNotIn("transparent", bc.NAMED_COLORS)

    def test_message_exists_in_turkish(self):
        self.assertIn("renk", bc.color_problem("mavi", "primary", lang="tr"))
        self.assertIsNone(bc.color_problem("#fff", "primary"))


class TestBottomNav(unittest.TestCase):
    NAV = ["Ana Sayfa", "Ürünlerim", "Hesaplamalar"]

    def test_object_item_is_refused(self):
        msg = die_text(build, TEMPLATE, flat(device="phone", bottom_nav=[{"label": "Ana Sayfa", "active": True}, "Ürünlerim"]))
        self.assertIn("bottom_nav", msg)

    def test_non_list_is_refused(self):
        die_text(build, TEMPLATE, flat(device="phone", bottom_nav="Ana Sayfa"))

    def test_active_tab_by_label(self):
        built = build(TEMPLATE, flat(device="phone", bottom_nav=self.NAV, bottom_nav_active="Hesaplamalar"))
        self.assertEqual(built.count('<span class="on">Hesaplamalar</span>'), 2)
        self.assertEqual(built.count('<span>Ana Sayfa</span>'), 2)

    def test_active_tab_by_index(self):
        built = build(TEMPLATE, flat(device="phone", bottom_nav=self.NAV, bottom_nav_active=0))
        self.assertEqual(built.count('<span class="on">Ana Sayfa</span>'), 2)
        self.assertEqual(built.count('class="on"'), 2)

    def test_active_label_match_ignores_case_and_spaces(self):
        built = build(TEMPLATE, flat(device="phone", bottom_nav=self.NAV, bottom_nav_active="  ürünlerim "))
        self.assertEqual(built.count('<span class="on">Ürünlerim</span>'), 2)

    def test_unknown_active_tab_is_refused(self):
        msg = die_text(build, TEMPLATE, flat(device="phone", bottom_nav=self.NAV, bottom_nav_active="Profil"))
        self.assertIn("bottom_nav_active", msg)
        die_text(build, TEMPLATE, flat(device="phone", bottom_nav=self.NAV, bottom_nav_active=3))
        die_text(build, TEMPLATE, flat(device="phone", bottom_nav=self.NAV, bottom_nav_active=True))

    def test_active_is_ignored_without_bottom_nav(self):
        built = build(TEMPLATE, flat(device="phone", bottom_nav_active="Ana Sayfa"))
        self.assertNotIn('class="bottomnav"', built)
        built = build(TEMPLATE, flat(device="web", url="site.example", bottom_nav_active=0))
        self.assertNotIn('class="bottomnav"', built)

    def test_template_styles_the_active_tab(self):
        self.assertTrue(".bottomnav span.on{color:var(--brand);font-weight:700}" in TEMPLATE)

    def test_card_field_in_scenario_shape(self):
        sc = example()
        sc["device"] = "phone"
        del sc["card"]["url"]
        sc["card"]["bottom_nav"] = self.NAV
        sc["card"]["bottom_nav_active"] = "Ürünlerim"
        code, _, err, built = run_main(stamped(sc))
        self.assertEqual(code, 0, err)
        self.assertEqual(built.count('<span class="on">Ürünlerim</span>'), 2)


class TestRingRules(unittest.TestCase):
    def test_ring_with_inline_margin_is_refused(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            'style="align-self:flex-start;line-height:44px"',
            'style="align-self:flex-start;line-height:44px;margin-left:20px"')
        msg = die_text(build, TEMPLATE, sc)
        self.assertIn("margin", msg)
        self.assertIn("must not push content", msg)

    def test_label_room_outside_the_ring_is_allowed(self):
        # A non-negative margin-top / margin-bottom on the ring keeps the label's room outside the ring.
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            'style="align-self:flex-start;line-height:44px"',
            'style="align-self:flex-start;line-height:44px;margin-top:20px;margin-bottom:8px"')
        build(TEMPLATE, sc)

    def test_ring_with_inline_padding_is_refused(self):
        b = '<div class="hl" data-note="Yeni" style="display:flex;padding:6px"><div class="r-h">Sepet</div></div>'
        msg = die_text(build, TEMPLATE, flat(variant_b=b))
        self.assertIn("padding", msg)

    def test_ring_with_layout_neutral_style_is_accepted(self):
        b = ('<div class="hl" data-note="Yeni" style="align-self:flex-start;display:flex;flex-direction:column;gap:8px">'
             '<div class="r-h">Sepet</div></div>')
        build(TEMPLATE, flat(variant_b=b))

    def test_margin_message_in_turkish(self):
        errors, _ = bc.card_problems("change", '<div class="r-h">S</div>',
                                     '<div class="hl" data-note="X" style="margin:4px"><div class="r-h">S</div></div>',
                                     lang="tr")
        self.assertTrue(any("içeriği itmemeli" in e for e in errors), errors)

    def test_ring_without_label_is_refused(self):
        msg = die_text(build, TEMPLATE, flat(variant_b='<div class="hl"><div class="r-h">Sepet</div></div>'))
        self.assertIn("data-note", msg)

    def test_unknown_component_class_is_refused(self):
        msg = die_text(build, TEMPLATE, flat(variant_a='<div class="r-ctaa">Devam</div>'))
        self.assertIn("r-ctaa", msg)

    def test_colour_only_in_b_outside_the_ring_is_refused(self):
        # Stage 3: was a warning and the card was built.
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            '<div class="r-cta">', '<div class="r-cta" style="background:#0a7f3f;border-color:#0a7f3f;color:#fff">')
        msg = die_text(build, TEMPLATE, sc)
        self.assertIn("inline colour only in Variant B on an element outside the ring: #0a7f3f", msg)

    def test_colour_outside_the_ring_is_refused_even_in_a_colour_test(self):
        sc = example()
        sc["variable"] = "Ödeme butonunun rengi"
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            '<div class="r-cta">', '<div class="r-cta" style="background:#0a7f3f">')
        self.assertIn("outside the ring", die_text(build, TEMPLATE, sc))

    def test_colour_only_in_b_inside_the_ring_warns(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            'line-height:44px">', 'line-height:44px;color:#0a7f3f">')
        warnings = []
        build(TEMPLATE, sc, warnings=warnings)
        self.assertTrue(any("only in Variant B, inside the ring" in w and "#0a7f3f" in w for w in warnings), warnings)

    def test_colour_test_does_not_warn_about_colour_inside_the_ring(self):
        sc = example()
        sc["variable"] = "Bağlantının rengi"
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            'line-height:44px">', 'line-height:44px;color:#0a7f3f">')
        warnings = []
        build(TEMPLATE, sc, warnings=warnings)
        self.assertFalse(any("only in Variant B" in w for w in warnings), warnings)

    def test_shared_colours_do_not_warn(self):
        a = '<div class="r-h" style="color:#0B4DC2">Sepet</div>'
        b = '<div class="hl" data-note="Yeni"><div class="r-h" style="color: #0b4dc2">Sepetim</div></div>'
        warnings = []
        build(TEMPLATE, flat(variant_a=a, variant_b=b), warnings=warnings)
        self.assertEqual([w for w in warnings if "only in Variant B" in w], [])

    def test_shipped_example_builds_without_warnings(self):
        warnings = []
        build(TEMPLATE, example(), warnings=warnings)
        self.assertEqual(warnings, [])

    def test_lowercase_turkish_label_is_refused(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("Kupon bağlantıda", "kupon alanı bağlantıda")
        msg = die_text(build, TEMPLATE, sc)
        self.assertIn("lowercase", msg)
        self.assertIn("“kupon alanı bağlantıda”", msg)

    def test_dotted_i_label_is_refused_and_capital_i_passes(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("Kupon bağlantıda", "indirim bağlantıda")
        die_text(build, TEMPLATE, sc)
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("indirim bağlantıda", "İndirim bağlantıda")
        build(TEMPLATE, sc)

    def test_lowercase_label_is_allowed_on_an_english_card(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("Kupon bağlantıda", "coupon behind link")
        errors, _ = bc.card_problems(sc["card"]["difference"], sc["card"]["variant_a"], sc["card"]["variant_b"],
                                     card_lang="en")
        self.assertFalse([e for e in errors if "lowercase" in e], errors)
        errors, _ = bc.card_problems(sc["card"]["difference"], sc["card"]["variant_a"], sc["card"]["variant_b"],
                                     card_lang="tr")
        self.assertTrue([e for e in errors if "lowercase" in e], errors)

    def test_long_label_warns(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            "Kupon bağlantıda", "Kupon alanı artık yalnızca bir bağlantı olarak duruyor")
        warnings = []
        build(TEMPLATE, sc, warnings=warnings)
        self.assertTrue(any("label" in w for w in warnings), warnings)

    def test_several_rings_in_one_variant_are_refused(self):
        # Two independent rings read as two variables (audit M5): refused, not a warning.
        b = ('<div class="hl" data-note="Bir"><div class="r-h">A2</div></div>'
             '<div class="hl" data-note="İki"><div class="r-h">B2</div></div>')
        msg = die_text(build, TEMPLATE, flat(variant_a='<div class="r-h">A</div><div class="r-h">B</div>', variant_b=b))
        self.assertIn("2 rings in B", msg)

    def test_move_with_a_different_element_is_refused(self):
        # Stage 3: a moved element whose content changed was a warning; it is a second variable.
        sc = example()
        sc["card"]["difference"] = sc["difference"] = "move"  # contract 5: the card can't override the record
        msg = die_text(build, TEMPLATE, sc)
        self.assertIn("difference 'move': the ringed element's content differs", msg)

    def test_move_with_the_same_element_builds_and_lists_no_change(self):
        cta = '<div class="hl" data-note="Taşındı"><div class="r-cta">Ödemeye geç</div></div>'
        a = cta + '<div class="r-h">Sepetim</div>'
        b = '<div class="r-h">Sepetim</div>' + cta
        manifest = {}
        build(TEMPLATE, flat(difference="move", variant_a=a, variant_b=b), manifest=manifest)
        self.assertEqual(manifest["changes"], [])
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])

    def test_difference_outside_the_ring_is_refused(self):
        # Stage 3: was a warning and the card was built.
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("Ödemeye geç", "Hemen öde")
        msg = die_text(build, TEMPLATE, sc)
        self.assertIn("A and B differ outside any ring", msg)
        self.assertIn("Hemen öde", msg)


class TestValidationBeforeBuild(unittest.TestCase):
    """main() şemayı çalıştırır; hatalı senaryodan kart çıkmaz."""

    def refused(self, scenario, fragment, *extra):
        # Stage 3: a refusal is exit 1 and names its gate (was exit 2).
        code, _, err, built = run_main(scenario, *extra)
        self.assertEqual(code, 1, err)
        self.assertIsNone(built)
        self.assertIn(fragment, err)
        self.assertIn("REFUSED at the", err)

    def test_shipped_example_builds(self):
        # The record as a final card once both stamps match.
        code, out, err, built = run_main(stamped(example()))
        self.assertEqual(code, 0, err)
        self.assertIn("built", out)

    def test_empty_boxes_are_refused(self):
        sc = detailed()
        sc["detail"] = {"test_items": [], "dont_items": [], "kpis": []}
        self.refused(sc, "detail.test_items")

    def test_old_record_fields_are_refused(self):
        sc = example()
        sc["kpis"] = [{"name": "RPV", "role": "primary"}]
        self.refused(sc, "unknown field 'kpis'")

    def test_four_primaries_are_refused(self):
        sc = detailed()
        sc["detail"]["kpis"] = [dict(k, role="primary") for k in sc["detail"]["kpis"]]
        self.refused(sc, "rule 2")

    def test_missing_difference_is_refused(self):
        sc = example()
        del sc["card"]["difference"]
        del sc["difference"]
        self.refused(sc, "difference")

    def test_card_without_difference_uses_the_record_difference(self):
        sc = example()
        del sc["card"]["difference"]
        code, out, err, built = run_main(stamped(sc))
        self.assertEqual(code, 0, err)
        self.assertIn("difference=change", out)
        sc["difference"] = "add"  # the record's type now sets the ring rule, and A carries a ring
        self.refused(sc, "difference 'add'")

    def test_non_string_items_are_refused(self):
        sc = detailed()
        sc["detail"]["test_items"] = [None, 5, ["x"], {"label": "", "text": ""}]
        self.refused(sc, "detail.test_items[0]")

    def test_scenario_without_card_gets_a_clear_message(self):
        sc = example()
        del sc["card"]
        self.refused(sc, "card")
        code, _, err, _ = run_main(sc)
        self.assertIn("variant_a", err)
        self.assertNotIn("Traceback", err)

    def test_messages_follow_lang(self):
        sc = detailed()
        sc["detail"]["kpis"] = [dict(k, role="primary") for k in sc["detail"]["kpis"]]
        code, _, err, _ = run_main(sc, "--lang", "tr")
        self.assertEqual(code, 1)
        self.assertIn("kural 2", err)
        self.assertIn("kapısında REDDEDİLDİ", err)

    def test_warnings_are_printed_and_do_not_block(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            'line-height:44px">', 'line-height:44px;color:#0a7f3f">')
        code, _, err, built = run_main(stamped(sc))
        self.assertEqual(code, 0, err)
        self.assertIsNotNone(built)
        self.assertIn("build_card: warning:", err)
        self.assertIn("only in Variant B, inside the ring: #0a7f3f", err)
        # A warning is printed once, not once per layer that noticed it.
        self.assertEqual(err.count("only in Variant B"), 1)

    def test_tab_bar_on_a_browser_frame_is_refused(self):
        sc = example()
        sc["card"]["bottom_nav"] = ["Ana Sayfa", "Ürünlerim"]
        self.refused(sc, "bottom_nav")

    def test_browser_frame_without_url_is_refused(self):
        sc = example()
        del sc["card"]["url"]
        self.refused(sc, "card.url")


class TestSkillClaimMatchesCode(unittest.TestCase):
    """Belgelerdeki izin listesi cümlesi koddaki listeyle aynı kalmalı."""

    def test_allowlist_is_small_and_inert(self):
        for tag in ("div", "span", "i", "b", "strong", "em", "ul", "li", "br", "p"):
            self.assertIn(tag, bc.ALLOWED_TAGS)
        for tag in ("script", "style", "iframe", "object", "embed", "svg", "meta", "base", "link", "form",
                    "img", "a", "input", "button", "video", "audio", "textarea", "details", "math"):
            self.assertNotIn(tag, bc.ALLOWED_TAGS)
        for attr in ("class", "style", "data-note", "data-pos"):
            self.assertIn(attr, bc.ALLOWED_ATTRS)
        for attr in ("href", "src", "action", "srcdoc", "formaction", "onclick", "id", "name"):
            self.assertNotIn(attr, bc.ALLOWED_ATTRS)


if __name__ == "__main__":
    unittest.main()
