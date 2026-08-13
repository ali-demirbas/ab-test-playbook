#!/usr/bin/env python3
"""build_card.py için unit testler. Bağımlılıksız (unittest).

Bu testler kart üretiminin sessizce bozulduğu noktalara karşı regresyon
korumasıdır: kaçırılmamış metin yüzünden bozulan markup, kaçırmadan ÖNCE
uygulanan bold etiketi, şablondaki geliştirici yorumunun da doldurulması,
mockup markup'ının yanlışlıkla kaçırılması ve sabit iskeletin sürüklenmesi.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from build_card import build, render_item, render_list, self_verify, fixed_lines  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REAL_TEMPLATE = os.path.join(REPO_ROOT, "templates", "scenario-card.html")

# Gerçek şablonun küçük bir taklidi: aynı yerleştiricileri ve aynı yapıyı taşır,
# ama testleri 180 satır CSS'e bağlamaz.
FAKE_TEMPLATE = """<!doctype html>
<html>
<head><title>{{TITLE}}</title></head>
<body>
<div class="card">
  <!-- Web senaryosunda bu iskeleti kullan:
       <div class="browser-screen">{{VARIANT_A_SCREEN}}</div> -->
  <div class="mockups">
    <div class="variant">
      <span class="pill">Variant A</span>
      <div class="phone">
        <div class="statusbar"><span>12:41</span></div>
        <div class="screen">
          {{VARIANT_A_SCREEN}}
        </div>
        <div class="bottomnav"><span>Anasayfa</span></div>
      </div>
    </div>
    <div class="variant">
      <span class="pill">Variant B</span>
      <div class="phone">
        <div class="statusbar"><span>12:41</span></div>
        <div class="screen">
          {{VARIANT_B_SCREEN}}
        </div>
        <div class="bottomnav"><span>Anasayfa</span></div>
      </div>
    </div>
  </div>
  <div class="copy">
    <h1>{{TITLE}}</h1>
    <p class="desc">{{DESC}}</p>
    <div class="box test"><ul>
        {{TEST_ITEMS}}
    </ul></div>
    <div class="box kpi"><ul>
        {{KPI_ITEMS}}
    </ul></div>
    <div class="box dont"><ul>
        {{DONT_ITEMS}}
    </ul></div>
  </div>
</div>
</body>
</html>
"""


def make_scenario(**over):
    base = {
        "title": "Kupon alanı katlanınca dönüşüm artar mı?",
        "desc": "Sepette açık duran kupon alanı indirim arayışını tetikliyor.",
        "device": "phone",
        "test_items": ["Kupon alanının katlanmış hâli"],
        "kpi_items": [{"label": "Birincil KPI", "text": "sepet → ödeme tamamlama"}],
        "dont_items": ["Aynı turda ödeme adımını değiştirme"],
        "variant_a": '<div class="r-h">Sipariş özeti</div>',
        "variant_b": '<div class="r-h">Sipariş özeti</div>',
    }
    base.update(over)
    return base


class TestEscaping(unittest.TestCase):
    """Metin alanları markup'a doğrudan gömülüyor: kaçırılmazsa kart bozulur."""

    def test_title_with_angle_brackets_does_not_leak_markup(self):
        out = build(FAKE_TEMPLATE, make_scenario(title="CTA < 3 kelime olmalı mı?"))
        self.assertIn("CTA &lt; 3 kelime olmalı mı?", out)
        self.assertNotIn("CTA < 3 kelime", out)

    def test_ampersand_in_item_is_escaped(self):
        out = build(FAKE_TEMPLATE, make_scenario(test_items=["kargo & iade metni"]))
        self.assertIn("kargo &amp; iade metni", out)

    def test_injected_tag_in_text_renders_as_text(self):
        out = build(FAKE_TEMPLATE, make_scenario(desc="<script>alert(1)</script>"))
        self.assertNotIn("<script>", out)
        self.assertIn("&lt;script&gt;", out)

    def test_bold_label_is_applied_after_escaping(self):
        # SKILL.md'nin sırası: önce içerik kaçırılır, sonra biçimlendirme eklenir.
        # Ters sırada bir <b> etiketi de kaçırılır ve bold görünmez; ya da daha
        # kötüsü, etiket içeriği tag olarak sızar.
        item = {"label": "<img src=x>", "text": "açıklama"}
        rendered = render_item(item)
        self.assertTrue(rendered.startswith("<li><b>&lt;img src=x&gt;</b>"))
        self.assertNotIn("<img", rendered)


class TestScreenMarkup(unittest.TestCase):
    """Mockup bölgesi üretkendir: ham markup olarak geçmeli, kaçırılmamalı."""

    def test_variant_markup_is_inserted_raw(self):
        markup = '<div class="hl" data-note="kupon alanı"><div class="r-field"></div></div>'
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
        out = build(FAKE_TEMPLATE, make_scenario(variant_a="<b>AAA</b>"))
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


class TestLeftoverPlaceholders(unittest.TestCase):
    def test_unknown_placeholder_is_reported(self):
        tpl = FAKE_TEMPLATE.replace("{{DESC}}", "{{DESC}} {{FOOTER_NOTE}}")
        with self.assertRaises(SystemExit):
            build(tpl, make_scenario())


class TestSelfVerify(unittest.TestCase):
    def test_drift_is_detected(self):
        built = build(FAKE_TEMPLATE, make_scenario())
        # Sabit bölgeden bir kutu iskeleti düşerse sürüklenme sayılır.
        drifted = built.replace('<div class="box dont"><ul>', "")
        with self.assertRaises(SystemExit):
            self_verify(drifted, FAKE_TEMPLATE, "phone")

    def test_mockup_region_is_excluded_from_drift(self):
        # Mockup iskeleti device'a göre meşru biçimde değişir (phone -> browser);
        # oradaki bir farkın sürüklenme sayılmaması bilinçli bir karardır.
        built = build(FAKE_TEMPLATE, make_scenario())
        swapped = built.replace('<span class="pill">Variant B</span>', "")
        self_verify(swapped, FAKE_TEMPLATE, "phone")  # yükselmemeli

    def test_clean_build_passes(self):
        built = build(FAKE_TEMPLATE, make_scenario())
        self_verify(built, FAKE_TEMPLATE, "phone")  # yükselmemeli

    def test_script_tag_is_refused(self):
        built = build(FAKE_TEMPLATE, make_scenario())
        with self.assertRaises(SystemExit):
            self_verify(built + "<script>x</script>", FAKE_TEMPLATE, "phone")

    def test_fixed_lines_skips_placeholder_and_comment_lines(self):
        lines = fixed_lines(FAKE_TEMPLATE)
        self.assertFalse(any("{{" in ln for ln in lines))
        self.assertFalse(any("<!--" in ln for ln in lines))


class TestRealTemplate(unittest.TestCase):
    """Gerçek şablonla uçtan uca: yerleştirici adları sürüklenirse burada patlar."""

    def setUp(self):
        if not os.path.isfile(REAL_TEMPLATE):
            self.skipTest("templates/scenario-card.html bulunamadı")
        with open(REAL_TEMPLATE, encoding="utf-8") as fh:
            self.template = fh.read()

    def test_builds_and_self_verifies_phone(self):
        built = build(self.template, make_scenario())
        self_verify(built, self.template, "phone")
        self.assertIn("Kupon alanı katlanınca", built)
        self.assertIn("Test Edilmesi Gerekenler", built)

    def test_builds_and_self_verifies_web(self):
        built = build(self.template, make_scenario(device="web", url="site.com/sepet"))
        self_verify(built, self.template, "web")
        self.assertEqual(built.count('class="browser-screen"'), 2)

    def test_no_placeholder_survives(self):
        built = build(self.template, make_scenario())
        self.assertNotIn("{{", built)


class TestRenderList(unittest.TestCase):
    def test_empty_list_renders_empty(self):
        self.assertEqual(render_list([]), "")

    def test_plain_and_labelled_items_mix(self):
        out = render_list(["düz madde", {"label": "Etiket", "text": "açıklama"}])
        self.assertIn("<li>düz madde</li>", out)
        self.assertIn("<li><b>Etiket</b> açıklama</li>", out)


if __name__ == "__main__":
    unittest.main()
