#!/usr/bin/env python3
"""build_card.py için unit testler. Bağımlılıksız (unittest).

Bu testler kart üretiminin sessizce bozulduğu noktalara karşı regresyon
korumasıdır: kaçırılmamış başlık yüzünden bozulan markup, şablondaki geliştirici
yorumunun da doldurulması, mockup markup'ının yanlışlıkla kaçırılması ve sabit
iskeletin (çerçeveler dahil) sürüklenmesi.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from build_card import build, self_verify, fixed_lines  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REAL_TEMPLATE = os.path.join(REPO_ROOT, "templates", "scenario-card.html")

# Gerçek şablonun küçük bir taklidi: aynı yerleştiricileri ve aynı yapıyı taşır,
# ama testleri 200 satır CSS'e bağlamaz.
FAKE_TEMPLATE = """<!doctype html>
<html>
<head><title>{{TITLE}}</title></head>
<body>
<div class="card">
  <!-- Web senaryosunda bu iskeleti kullan:
       <div class="browser-screen">{{VARIANT_A_SCREEN}}</div> -->
  <h1 class="title">{{TITLE}}</h1>
  <div class="stage">
    <div class="variant">
      <span class="pill pill-a">Variant A</span>
      <div class="phone">
        <div class="statusbar"><span>12:41</span></div>
        <div class="screen">
          {{VARIANT_A_SCREEN}}
        </div>
        <div class="bottomnav"><span>Anasayfa</span></div>
      </div>
    </div>
    <div class="variant">
      <span class="pill pill-b">Variant B</span>
      <div class="phone">
        <div class="statusbar"><span>12:41</span></div>
        <div class="screen">
          {{VARIANT_B_SCREEN}}
        </div>
        <div class="bottomnav"><span>Anasayfa</span></div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""


def make_scenario(title="Kupon alanı katlanınca dönüşüm artar mı?", device="phone", **card):
    """A minimal scenario record as build() reads it: the title, the device and the card."""
    base = {
        "variant_a": '<div class="r-h">Sipariş özeti</div>',
        # B differs inside a ring: two identical arms are refused (they render the same).
        "variant_b": '<div class="r-h hl" data-note="Yeni başlık">Siparişiniz</div>',
    }
    base.update(card)
    return {"title": title, "device": device, "card": base}



# A refusal writes its reason to stderr before it exits; the tests that expect one would print it on every
# run. The test runner keeps its own stream, so only the builder's messages are silenced.
_STDERR = None


def setUpModule():
    global _STDERR
    import io
    _STDERR, sys.stderr = sys.stderr, io.StringIO()


def tearDownModule():
    sys.stderr = _STDERR

class TestEscaping(unittest.TestCase):
    """Metin alanları markup'a doğrudan gömülüyor: kaçırılmazsa kart bozulur."""

    def test_title_with_angle_brackets_does_not_leak_markup(self):
        out = build(FAKE_TEMPLATE, make_scenario(title="CTA < 3 kelime olmalı mı?"))
        self.assertIn("CTA &lt; 3 kelime olmalı mı?", out)
        self.assertNotIn("CTA < 3 kelime", out)

    def test_ampersand_in_title_is_escaped(self):
        out = build(FAKE_TEMPLATE, make_scenario(title="Kargo & iade metni dönüşümü artırır mı?"))
        self.assertIn("Kargo &amp; iade metni", out)

    def test_injected_tag_in_the_title_renders_as_text(self):
        out = build(FAKE_TEMPLATE, make_scenario(title="<script>alert(1)</script>"))
        self.assertNotIn("<script>", out)
        self.assertEqual(out.count("&lt;script&gt;alert(1)&lt;/script&gt;"), 2)  # <title> and the h1


class TestScreenMarkup(unittest.TestCase):
    """Mockup bölgesi üretkendir: ham markup olarak geçmeli, kaçırılmamalı."""

    def test_variant_markup_is_inserted_raw(self):
        markup = '<div class="hl" data-note="Kupon alanı"><div class="r-field"></div></div>'
        out = build(FAKE_TEMPLATE, make_scenario(variant_a=markup))
        self.assertIn(markup, out)
        self.assertNotIn("&lt;div class=&quot;hl&quot;", out)


class TestDeveloperComment(unittest.TestCase):
    """Şablondaki yorum aynı yerleştiricileri tekrarlıyor; teslim edilen kartta yeri yok."""

    def test_comment_is_stripped(self):
        out = build(FAKE_TEMPLATE, make_scenario())
        self.assertNotIn("Web senaryosunda bu iskeleti kullan", out)
        # Tek istisna: builder'ın kendi eklediği kaynak bildirimi (aşağıda).
        self.assertEqual(out.count("<!--"), 1)

    def test_comment_placeholder_is_not_half_filled(self):
        # Yorum silinmeseydi içindeki {{VARIANT_A_SCREEN}} de dolar ve teslim
        # edilen kartın içine yarı doldurulmuş bir örnek blok sızardı.
        # B'de halkalı başka bir öğe: A ile B'nin farkı halkanın içinde kalır.
        out = build(FAKE_TEMPLATE, make_scenario(variant_a="<b>AAA</b>",
                                                 variant_b='<div class="hl" data-note="Yeni"><b>BBB</b></div>'))
        self.assertEqual(out.count("<b>AAA</b>"), 1)


class TestProvenance(unittest.TestCase):
    """Kart repodan ayrıldıktan sonra kaynağını söyleyen tek şey bu bildirim."""

    def test_notice_is_present(self):
        out = build(FAKE_TEMPLATE, make_scenario())
        self.assertIn("ab-test-playbook", out)
        self.assertIn("github.com/ali-demirbas/ab-test-playbook", out)
        self.assertIn("MIT License", out)

    def test_notice_survives_comment_stripping(self):
        # Şablondaki geliştirici yorumları silinir; bildirim silme İŞLEMİNDEN
        # SONRA eklendiği için hayatta kalır. Sıra bozulursa bu test düşer.
        out = build(FAKE_TEMPLATE, make_scenario())
        self.assertNotIn("Web senaryosunda", out)
        self.assertIn("Generated by ab-test-playbook", out)

    def test_notice_sits_before_the_html_element(self):
        out = build(FAKE_TEMPLATE, make_scenario())
        self.assertLess(out.index("Generated by ab-test-playbook"), out.index("<html"))

    def test_doctype_stays_first(self):
        # Bildirim DOCTYPE'ın önüne geçerse bazı tarayıcılar quirks mode'a düşer.
        out = build(FAKE_TEMPLATE, make_scenario())
        self.assertTrue(out.lstrip().startswith("<!doctype") or out.lstrip().startswith("<!DOCTYPE"))

    def test_notice_is_invisible(self):
        # Görünmez olması bilinçli: müşteri sunumunda yer kaplamaz.
        out = build(FAKE_TEMPLATE, make_scenario())
        body = out.split("<body", 1)[1] if "<body" in out else out
        self.assertNotIn("ab-test-playbook", body)


class TestDeviceSkeleton(unittest.TestCase):
    def test_web_device_converts_both_variants_to_browser(self):
        out = build(FAKE_TEMPLATE, make_scenario(device="web", url="site.com/sepet"))
        self.assertEqual(out.count('class="browser-screen"'), 2)
        self.assertIn("site.com/sepet", out)
        self.assertNotIn('class="statusbar"', out)
        self.assertNotIn('class="bottomnav"', out)

    def test_web_url_is_escaped(self):
        out = build(FAKE_TEMPLATE, make_scenario(device="web", url='a"><b>'))
        self.assertNotIn('<b>', out.split('browser-url')[1][:80])

    def test_unknown_device_exits(self):
        with self.assertRaises(SystemExit):
            build(FAKE_TEMPLATE, make_scenario(device="tablet"))


class TestBottomNav(unittest.TestCase):
    """The phone tab bar is drawn only when the page really has one."""

    def test_missing_bottom_nav_drops_the_bar(self):
        out = build(FAKE_TEMPLATE, make_scenario())
        self.assertNotIn('class="bottomnav"', out)
        self.assertIn('class="statusbar"', out)

    def test_empty_list_drops_the_bar(self):
        out = build(FAKE_TEMPLATE, make_scenario(bottom_nav=[]))
        self.assertNotIn('class="bottomnav"', out)

    def test_given_labels_are_rendered_in_both_variants(self):
        out = build(FAKE_TEMPLATE, make_scenario(bottom_nav=["Ana Sayfa", "Poliçelerim", "Hesabım"]))
        self.assertEqual(out.count('<span>Poliçelerim</span>'), 2)
        self.assertNotIn("<span>Anasayfa</span>", out)

    def test_labels_are_escaped(self):
        out = build(FAKE_TEMPLATE, make_scenario(bottom_nav=["<b>x</b>"]))
        self.assertIn("&lt;b&gt;x&lt;/b&gt;", out)
        self.assertNotIn("<span><b>x</b></span>", out)

    def test_web_card_ignores_bottom_nav(self):
        out = build(FAKE_TEMPLATE, make_scenario(device="web", bottom_nav=["A"]))
        self.assertNotIn('class="bottomnav"', out)


class TestLeftoverPlaceholders(unittest.TestCase):
    def test_unknown_placeholder_is_reported(self):
        tpl = FAKE_TEMPLATE.replace('<h1 class="title">{{TITLE}}</h1>', '<h1 class="title">{{TITLE}}</h1> {{FOOTER_NOTE}}')
        with self.assertRaises(SystemExit):
            build(tpl, make_scenario())


class TestSelfVerify(unittest.TestCase):
    def test_drift_is_detected(self):
        built = build(FAKE_TEMPLATE, make_scenario())
        # Sabit iskeletten bir satır düşerse sürüklenme sayılır.
        drifted = built.replace('  <div class="stage">', "  <div>")
        with self.assertRaises(SystemExit):
            self_verify(drifted, FAKE_TEMPLATE, "phone")

    def test_frames_and_pills_are_checked_too(self):
        # Çerçeve iskeleti artık sürüklenme denetiminin dışında değil: fixed_lines
        # şablonu kartın cihaz çerçevesine çevirip öyle karşılaştırır.
        built = build(FAKE_TEMPLATE, make_scenario())
        with self.assertRaises(SystemExit):
            self_verify(built.replace('<span class="pill pill-b">Variant B</span>', ""), FAKE_TEMPLATE, "phone")
        with self.assertRaises(SystemExit):
            self_verify(built.replace('<div class="statusbar">', '<div>'), FAKE_TEMPLATE, "phone")

    def test_the_frame_is_the_one_the_card_was_built_with(self):
        web = build(FAKE_TEMPLATE, make_scenario(device="web", url="site.example"))
        self_verify(web, FAKE_TEMPLATE, "web")  # yükselmemeli
        with self.assertRaises(SystemExit):
            self_verify(web, FAKE_TEMPLATE, "phone")  # the phone skeleton is not in a web card
        nav = build(FAKE_TEMPLATE, make_scenario(bottom_nav=["Ana Sayfa", "Hesabım"]))
        self_verify(nav, FAKE_TEMPLATE, "phone", bottom_nav=True)  # yükselmemeli

    def test_clean_build_passes(self):
        built = build(FAKE_TEMPLATE, make_scenario())
        self_verify(built, FAKE_TEMPLATE, "phone")  # yükselmemeli

    def test_script_tag_is_refused(self):
        built = build(FAKE_TEMPLATE, make_scenario())
        with self.assertRaises(SystemExit):
            self_verify(built + "<script>x</script>", FAKE_TEMPLATE, "phone")

    def test_event_handler_attribute_is_refused(self):
        # The one CLAUDE.md rule 18 names by example: an onerror= payload that
        # survived into a variant, e.g. via a screenshot's product name. The
        # allowlist refuses it in build(), before anything is written.
        with self.assertRaises(SystemExit):
            build(FAKE_TEMPLATE, make_scenario(variant_a='<img src=x onerror="alert(1)">'))

    def test_javascript_uri_is_refused(self):
        with self.assertRaises(SystemExit):
            build(FAKE_TEMPLATE, make_scenario(variant_a='<a href="javascript:alert(1)">go</a>'))

    def test_iframe_is_refused(self):
        with self.assertRaises(SystemExit):
            build(FAKE_TEMPLATE, make_scenario(variant_a='<iframe src="https://evil.example"></iframe>'))

    def test_data_html_uri_is_refused(self):
        with self.assertRaises(SystemExit):
            build(FAKE_TEMPLATE, make_scenario(variant_a='<a href="data:text/html,<script>alert(1)</script>">go</a>'))

    def test_second_layer_still_reads_the_raw_variants(self):
        # Behind the allowlist: self_verify scans the raw variants once more.
        built = build(FAKE_TEMPLATE, make_scenario())
        for bad in ('<img src=x onerror="alert(1)">', '<a href="javascript:alert(1)">go</a>'):
            with self.assertRaises(SystemExit):
                self_verify(built, FAKE_TEMPLATE, "phone", variants=('<div class="r-h">x</div>', bad))

    def test_ordinary_mockup_markup_is_not_a_false_positive(self):
        # Ordinary copy like "based on = ..." or a class named "button-on" is
        # not an event handler.
        a = '<div class="r-h button-on">Fiyat karşılaştırması ekranda mı? Based on = fiyat</div>'
        b = '<div class="hl" data-note="Yeni">%s</div>' % a
        built = build(FAKE_TEMPLATE, make_scenario(variant_a=a, variant_b=b.replace("Based on", "Based upon")))
        self_verify(built, FAKE_TEMPLATE, "phone", variants=(a, b))  # should not raise

    def test_fixed_lines_skips_placeholder_and_comment_lines(self):
        lines = fixed_lines(FAKE_TEMPLATE)
        self.assertFalse(any("{{" in ln for ln in lines))
        self.assertFalse(any("<!--" in ln for ln in lines))

    def test_fixed_lines_follow_the_device_frame(self):
        self.assertIn('        <div class="browser-bar">', fixed_lines(FAKE_TEMPLATE, "web"))
        self.assertNotIn('        <div class="statusbar"><span>12:41</span></div>', fixed_lines(FAKE_TEMPLATE, "web"))
        self.assertIn('        <div class="statusbar"><span>12:41</span></div>', fixed_lines(FAKE_TEMPLATE, "phone-web"))


class TestRealTemplate(unittest.TestCase):
    """Gerçek şablonla uçtan uca: yerleştirici adları sürüklenirse burada patlar."""

    def setUp(self):
        if not os.path.isfile(REAL_TEMPLATE):
            self.skipTest("templates/scenario-card.html not found")
        with open(REAL_TEMPLATE, encoding="utf-8") as fh:
            self.template = fh.read()

    def test_builds_and_self_verifies_phone(self):
        built = build(self.template, make_scenario())
        self_verify(built, self.template, "phone")
        self.assertIn('<h1 class="title">Kupon alanı katlanınca dönüşüm artar mı?</h1>', built)

    def test_builds_and_self_verifies_phone_web(self):
        built = build(self.template, make_scenario(device="phone-web", url="https://www.magaza.example/sepet"))
        self_verify(built, self.template, "phone-web")
        self.assertEqual(built.count('class="m-addr"'), 2)

    def test_builds_and_self_verifies_web(self):
        built = build(self.template, make_scenario(device="web", url="site.com/sepet"))
        self_verify(built, self.template, "web")
        self.assertEqual(built.count('class="browser-screen"'), 2)

    def test_no_placeholder_survives(self):
        built = build(self.template, make_scenario())
        self.assertNotIn("{{", built)


if __name__ == "__main__":
    unittest.main()
