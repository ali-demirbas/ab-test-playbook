#!/usr/bin/env python3
"""Contract 8: the screen spec compiler (scripts/screen_spec.py) and its seams.

Every node kind compiles to its template class; the page-colour overrides land
as inline style identical in both arms; each op places the ring where its
difference type wants it and passes card_problems; Variant A is byte-identical
across records that share a screen list; refusals (both forms, unknown kind,
missing target, two changes, duplicate id) are problems, never fallbacks; and
the health-form spec compiles, passes --strict, builds a draft and, when
Playwright is on NODE_PATH, render_check --strict is VERIFIED. Bağımlılıksız
(unittest), Python 3.9+.
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
REPO_ROOT = os.path.normpath(os.path.join(HERE, ".."))
SCRIPTS = os.path.join(REPO_ROOT, "scripts")
sys.path.insert(0, SCRIPTS)
import build_card as bc  # noqa: E402
import screen_spec as ss  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
CLASSES = bc.component_classes(TEMPLATE)
NODE = shutil.which("node")

# ------------------------------------------------------------ the reference spec (Contract 8)

FIELD = {"fg": "#777879", "border": "#9a9b9d", "radius": 4, "height": 52, "mb": 10}


def field(text, node_id=None):
    node = {"field": text}
    node.update(FIELD)
    if node_id:
        node["id"] = node_id
    return node


SCREEN = [
    {"header": {"logo": True,
                "icons": [{"icon": "support", "label": "Canlı destek", "fg": "#ca3c2c"},
                          {"icon": "close", "label": "Kapat", "fg": "#777879"}],
                "line": False}},
    {"h": "Sağlık Sigortası", "fg": "#1e1f1f"},
    {"band": {"bg": "#f5f5f5", "pad": [20, 40], "items": [
        {"text": "Teklif almak için aşağıdaki bilgileri eksiksiz\ndoldurunuz.", "align": "center",
         "fg": "#000000", "mb": 24},
        field("Adınız", "adiniz"),
        field("Soyadınız"),
        field("T.C. Kimlik Numaranız", "tckn"),
        field("Cep Telefonu"),
        field("E-Posta", "eposta"),
    ]}},
]
CHANGE = {"op": "insert_after", "target": "tckn",
          "node": {"help": "Teklifinizi hazırlamak için bu bilgiye ihtiyaç duyuyoruz.", "fg": "#000000"},
          "label": "Gerekçe satırı eklendi", "label_pos": "below"}
PLACEHOLDERS = ("Adınız", "Soyadınız", "T.C. Kimlik Numaranız", "Cep Telefonu", "E-Posta")

RECORD = {
    "id": "finance-pension-kimlik-gerekce-01",
    "title": "T.C. Kimlik alanının altına neden istendiğini yazmak teklif talebini artırır mı?",
    "lang": "tr", "stage": "finance-pension", "device": "phone-web", "market": "TR",
    "problem": ("Teklif formu, henüz teklif görmemiş ziyaretçiden üçüncü alanda kimlik numarası istiyor ve sayfada "
                "bunun neden gerektiği yazmıyor; “neden şimdi” sorusu yanıtsız kalınca form bu alanda bırakılabilir."),
    "mechanism": ("Alanın hemen altına bilginin teklif için istendiğini söyleyen tek bir satır eklenince ziyaretçi "
                  "numaranın neden istendiğini sormadan alanı doldurabilir ve formu orada bırakma nedeni zayıflar."),
    "variable": "Kimlik numarası alanının altındaki gerekçe satırı",
    "difference": "add",
    "variants": [
        {"id": "A", "description": "Kimlik numarası alanı, altında açıklama satırı olmadan duruyor", "is_current": True},
        {"id": "B", "description": ("Kimlik numarası alanının altında, bilginin teklif için istendiğini söyleyen tek "
                                    "bir satır var")},
    ],
    "primary_kpi": {"name": "Talep Oluşturma Oranı",
                    "denominator": ("Teste atanan ziyaretçi (atama teklif formu sayfasına ulaşınca, iki kolda aynı "
                                    "tetik)"),
                    "direction": "increase"},
    "guardrail": {"name": "Sözleşme Oranı (30 gün)", "kind": "metric", "denominator": "Teste atanan ziyaretçi",
                  "direction": "must_not_decrease"},
    "source": "adapted",
    "adapted_from": "Ön teklif formunda kimlik numarası alanının yanına neden istendiğini yazmak teklif almayı artırır mı?",
    "evidence": {"level": "archive",
                 "note": "Arşivde derlenmiş bir test fikrine dayanıyor, bir test sonucu değil; bu formun verisi yok."},
    "priority": {"tier": "medium",
                 "rationale": ("Formun en hassas alanında bırakmayı hedefliyor ve metin işi olduğu için uygulaması "
                               "kolay, ama gerekçenin metni alanın gerçek amacına ve uyum onayına bağlı olduğundan "
                               "orta.")},
    "objection": "Güven",
    "warnings": [
        {"type": "regulation", "text": ("Gerekçe satırının tam metni uyum ekibince yayımlanan aydınlatma metniyle "
                                        "karşılaştırılıp onaylanmalı; onaydan önce test trafik almaz.")},
        {"type": "accessibility", "text": ("Geçmeli: kimlik numarası alanı klavyeyle erişilebilir kalır ve dokunma "
                                           "alanı en az 44×44 pt olur, satır ekran okuyucuda alanla ilişkilendirilip "
                                           "birlikte okunur, metin kontrastı en az 4.5:1 olur.")},
    ],
    "invariants": ["Kimlik numarası alanı iki kolda aynı doğrulamayı ve aynı hata mesajını kullanır.",
                   "Alanın zorunluluğu ve girilen değerin işlenişi iki kolda aynıdır."],
    "assumptions": [{"type": "critical",
                     "text": ("Satırın metni temsilîdir: kimlik numarasının bu formda gerçekte neden istendiği ve "
                              "aydınlatma metnindeki amaç doğrulanmadı."),
                     "question": "Kimlik numarası bu formda hangi amaçla isteniyor?"}],
    "card": {
        "difference": "add", "url": "saglik.example/teklif", "mockup_basis": "shared_page",
        "brand": {"primary": "#ca3c2c", "on_primary": "#ffffff", "name": "Sigorta"},
        "phone_scale": 1,
        "inherited_contrast": [{"text": t, "color": "#777879"} for t in PLACEHOLDERS],
        "screen": SCREEN,
        "change": CHANGE,
    },
}


def critic_stamp(sc):
    return {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}


def reference_record():
    sc = copy.deepcopy(RECORD)
    sc["review"] = {"scenario_critic": critic_stamp(sc)}
    return sc


# ------------------------------------------------------------ helpers

SIMPLE = [{"h": "Sepetim", "id": "h"}, {"field": "E-posta", "id": "mail"}, {"cta": "Devam", "id": "cta"},
          {"help": "Yardım", "id": "help"}]


def compiled(screen, change, soft=None, lang="en"):
    a, b, problems = ss.compile(screen, change, lang, soft)
    if problems:
        raise AssertionError("expected a clean compile:\n  " + "\n  ".join(problems))
    return a, b


def problems_of(screen, change, soft=None, lang="en"):
    a, b, problems = ss.compile(screen, change, lang, soft)
    if not problems:
        raise AssertionError("expected problems; compiled:\n%s\n%s" % (a, b))
    return problems


def gate(difference, a, b, **kw):
    """card_problems' errors for the compiled pair, with the template's classes."""
    errors, _ = bc.card_problems(difference, a, b, lang="en", classes=CLASSES, card_lang="tr", **kw)
    return errors


def die_text(fn, *args, **kw):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            fn(*args, **kw)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected the builder to refuse; it went on instead")


# ------------------------------------------------------------ node kinds

class TestNodeKinds(unittest.TestCase):
    """Every kind of the contract compiles to its template class (and nothing outside the allowlist)."""

    CASES = [
        ({"header": {"logo": True, "nav": ["Ürünler", "Teklif"], "tel": "0850 222 27 27",
                     "icons": [{"icon": "menu"}, {"icon": "search"}, {"icon": "back"}], "line": False}},
         ['<div class="r-header" style="border-bottom:0">', '<span class="r-logo"></span>',
          '<span class="r-nav"><span>Ürünler</span><span>Teklif</span></span>', '<span class="r-tel">0850 222 27 27</span>',
          'role="img" aria-label="Menu"', 'role="img" aria-label="Search"', 'role="img" aria-label="Back"']),
        ({"header": {"logo": "Dükkan"}}, ['<div class="r-header"><span class="r-logo">Dükkan</span></div>']),
        ({"h": "Başlık"}, ['<div class="r-h">Başlık</div>']),
        ({"sub": "Alt başlık"}, ['<div class="r-sub">Alt başlık</div>']),
        ({"text": "Metin", "align": "center"}, ['<div style="text-align:center">Metin</div>']),
        ({"text": "Metin"}, ['<div>Metin</div>']),
        ({"field": "E-posta"}, ['<div class="r-field empty">E-posta</div>']),
        ({"field": "E-posta", "label": "E-posta adresi", "select": True},
         ['<div class="r-label">E-posta adresi</div><div class="r-field empty select">E-posta</div>']),
        ({"field": "Ad", "value": "••••"}, ['<div class="r-field">••••</div>']),
        ({"row": [{"field": "Ay"}, {"field": "Yıl"}]},
         ['<div class="r-row"><div class="r-field empty">Ay</div><div class="r-field empty">Yıl</div></div>']),
        ({"cta": "Devam"}, ['<div class="r-cta">Devam</div>']),
        ({"cta": "Devam", "style": "filled"}, ['<div class="r-cta">Devam</div>']),
        ({"cta": "Vazgeç", "style": "outline", "size": "sm"}, ['<div class="r-cta outline sm">Vazgeç</div>']),
        ({"cta": "Sil", "style": "ghost"}, ['<div class="r-cta ghost">Sil</div>']),
        ({"link": "Tümünü gör"}, ['<div class="r-link">Tümünü gör</div>']),
        ({"help": "Yardım"}, ['<div class="r-help">Yardım</div>']),
        ({"info": "Bilgi"}, ['<div class="r-info">Bilgi</div>']),
        ({"check": "Kabul ediyorum", "on": False}, ['<div class="r-check">Kabul ediyorum</div>']),
        ({"check": "Kabul ediyorum", "on": True}, ['<div class="r-check on">Kabul ediyorum</div>']),
        ({"radio": "Kredi kartı", "on": True}, ['<div class="r-radio on">Kredi kartı</div>']),
        ({"chips": [{"label": "S", "on": True}, {"label": "M"}]},
         ['<div class="r-chips"><span class="r-chip on">S</span><span class="r-chip">M</span></div>']),
        ({"tabs": [{"label": "Trafik", "on": True}, {"label": "Kasko"}]},
         ['<div class="r-tabs"><span class="on">Trafik</span><span>Kasko</span></div>']),
        ({"steps": [{"label": "Bilgiler", "state": "done"}, {"label": "Teklif", "state": "on"}, {"label": "Ödeme"}]},
         ['<div class="r-steps"><span class="done">Bilgiler</span><span class="on">Teklif</span><span>Ödeme</span></div>']),
        ({"progress": 40}, ['<div class="r-progress"><i style="width:40%"></i></div>']),
        ({"line": ["Ara toplam", "1.230 TL"]}, ['<div class="r-line"><span>Ara toplam</span><span>1.230 TL</span></div>']),
        ({"line": ["Toplam", "1.230 TL"], "total": True}, ['<div class="r-line total">']),
        ({"item": {"name": "Ürün", "meta": "Beden M", "price": "890 TL"}},
         ['<div class="r-item"><div class="ph img r-thumb"></div><div class="r-item-body"><div class="r-name">Ürün</div>'
          '<div class="r-meta">Beden M</div></div><div class="r-price">890 TL</div></div>']),
        ({"plan": {"name": "Pro", "price": "299 TL", "per": "/ay", "featured": True, "badge": "Popüler",
                   "cta": "Seç", "cta_style": "outline", "features": ["Sınırsız", "Destek"]}},
         ['<div class="r-plan featured">', '<span class="r-badge brand">Popüler</span>', '<div class="r-plan-name">Pro</div>',
          '<div class="r-plan-price">299 TL<span class="r-per">/ay</span></div>',
          '<ul class="r-plan-feat"><li>Sınırsız</li><li>Destek</li></ul>', '<div class="r-cta outline">Seç</div>']),
        ({"badge": "Yeni"}, ['<div><span class="r-badge">Yeni</span></div>']),
        ({"badge": "Son 3", "style": "warn"}, ['<span class="r-badge warn">Son 3</span>']),
        ({"badge": "Kampanya", "style": "brand"}, ['<span class="r-badge brand">Kampanya</span>']),
        ({"banner": "Kargo bedava"}, ['<div class="r-banner">Kargo bedava</div>']),
        ({"img": 150}, ['<div class="ph img" style="height:150px"></div>']),
        ({"divider": True}, ['<div class="r-divider"></div>']),
        ({"gap": 24}, ['<div style="height:24px"></div>']),
        ({"band": {"bg": "#f5f5f5", "items": [{"h": "İç"}]}},
         ['<div style="margin:0 -20px;padding:20px;background:#f5f5f5">\n<div class="r-h">İç</div>\n</div>']),
        ({"band": {"items": [{"h": "İç"}], "pad": [12, 30]}}, ['style="margin:0 -20px;padding:12px 20px 30px"']),
        ({"fold": True}, ['<div class="r-fold"></div>']),
        ({"stage": True}, ['<div class="r-stage-break"></div>']),
        ({"sticky": {"cta": "Ödemeye geç"}}, ['<div class="r-sticky"><div class="r-cta">Ödemeye geç</div></div>']),
        ({"stack": {"items": [{"h": "Bir"}, {"sub": "İki"}], "gap": 4}},
         ['<div style="display:flex;flex-direction:column">\n<div class="r-h" style="margin-bottom:4px">Bir</div>\n'
          '<div class="r-sub">İki</div>\n</div>']),
    ]

    def test_every_kind_compiles_to_its_component(self):
        for node, expected in self.CASES:
            screen = [{"text": "Üst", "id": "top"}, node, {"text": "Alt", "id": "bottom"}]
            if "sticky" in node:  # the pinned bar lives before a fold (mockup-style.md)
                screen.insert(2, {"fold": True})
            change = {"op": "edit", "target": "bottom", "set": {"text": "Alt satır"}, "label": "Metin"}
            a, b = compiled(screen, change)
            for fragment in expected:
                self.assertIn(fragment, a, "%r\n%s" % (node, a))
            errors = gate("change", a, b)
            self.assertEqual(errors, [], "%r\n%s" % (node, errors))

    def test_the_whole_catalogue_is_covered(self):
        kinds = set(k for node, _ in self.CASES for k in node if k in ss.KINDS)
        self.assertEqual(kinds, set(ss.KINDS))

    def test_icon_labels_follow_the_card_language(self):
        screen = [{"header": {"icons": [{"icon": "close"}]}, "id": "hd"}, {"h": "X", "id": "h"}]
        change = {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"}
        a_tr, _ = compiled(screen, change, lang="tr")
        a_en, _ = compiled(screen, change, lang="en")
        self.assertIn('aria-label="Kapat"', a_tr)
        self.assertIn('aria-label="Close"', a_en)

    def test_text_newline_is_a_line_break(self):
        a, _ = compiled([{"text": "Bir\nİki", "id": "t"}, {"h": "H", "id": "h"}],
                        {"op": "edit", "target": "h", "set": {"h": "Y"}, "label": "Başlık"})
        self.assertIn("Bir<br>İki", a)

    def test_text_is_escaped(self):
        a, _ = compiled([{"h": "<b>&", "id": "h"}, {"sub": "S", "id": "s"}],
                        {"op": "edit", "target": "s", "set": {"sub": "T"}, "label": "Alt"})
        self.assertIn("&lt;b&gt;&amp;", a)
        self.assertNotIn("<b>", a)


# ------------------------------------------------------------ overrides and rhythm

class TestOverrides(unittest.TestCase):
    def test_overrides_become_inline_style_identical_in_both_arms(self):
        node = {"field": "Ad", "id": "ad", "fg": "#777879", "bg": "#FAFAFA", "border": "#9a9b9d", "radius": 4, "height": 52}
        screen = [node, {"cta": "Devam", "id": "cta"}]
        a, b = compiled(screen, {"op": "edit", "target": "cta", "set": {"style": "outline"}, "label": "Çerçeveli buton"})
        style = 'style="color:#777879;background:#fafafa;border-color:#9a9b9d;border-radius:4px;min-height:52px"'
        self.assertIn(style, a)
        self.assertEqual(a.count(style), b.count(style))
        self.assertEqual(gate("change", a, b), [])

    def test_mb_sets_the_spacing_inside_a_band_and_the_last_child_has_none(self):
        screen = [{"band": {"items": [{"field": "A", "mb": 10, "id": "a"}, {"field": "B", "id": "b"},
                                      {"field": "C", "id": "c"}]}}, {"cta": "Devam", "id": "cta"}]
        a, _ = compiled(screen, {"op": "edit", "target": "cta", "set": {"cta": "İlerle"}, "label": "Buton metni"})
        self.assertIn('style="margin-bottom:10px">A</div>', a)
        self.assertIn('style="margin-bottom:16px">B</div>', a)
        self.assertIn('<div class="r-field empty">C</div>', a)

    def test_mb_at_the_top_level_writes_only_the_difference_to_the_template_gap(self):
        a, _ = compiled([{"h": "H", "mb": 24, "id": "h"}, {"sub": "S", "mb": 16, "id": "s"}, {"cta": "C", "id": "c"}],
                        {"op": "edit", "target": "c", "set": {"cta": "D"}, "label": "Buton metni"})
        self.assertIn('<div class="r-h" style="margin-bottom:8px">H</div>', a)
        self.assertIn('<div class="r-sub">S</div>', a)

    def test_a_band_opening_or_closing_the_screen_bleeds_through_its_padding(self):
        screen = [{"band": {"items": [{"h": "Üst"}]}}, {"h": "Orta", "id": "o"}, {"band": {"items": [{"h": "Alt"}]}}]
        a, _ = compiled(screen, {"op": "edit", "target": "o", "set": {"h": "Orta 2"}, "label": "Başlık"})
        self.assertIn('style="margin:0 -20px;padding:20px;margin-top:-14px">', a)
        self.assertIn('style="margin:0 -20px;padding:20px;margin-bottom:-20px">', a)

    def test_unknown_override_is_refused(self):
        problems = problems_of([{"h": "H", "colour": "#000000", "id": "h"}, {"sub": "S", "id": "s"}],
                               {"op": "edit", "target": "s", "set": {"sub": "T"}, "label": "Alt"})
        self.assertIn('"colour" is not a property of a h node', problems[0])

    def test_bad_colour_is_refused(self):
        problems = problems_of([{"h": "H", "fg": "red", "id": "h"}, {"sub": "S", "id": "s"}],
                               {"op": "edit", "target": "s", "set": {"sub": "T"}, "label": "Alt"})
        self.assertIn('"fg" must be #rrggbb', problems[0])


# ------------------------------------------------------------ the ops

class TestOps(unittest.TestCase):
    """Each op: the ring where its difference type wants it, and card_problems passes for that type."""

    def test_insert_after_rings_the_new_node_in_b_only(self):
        a, b = compiled(SIMPLE, {"op": "insert_after", "target": "mail", "node": {"help": "Fatura için gerekli"},
                                 "label": "Gerekçe satırı"})
        self.assertNotIn("hl", a)
        self.assertIn('<div class="r-field empty">E-posta</div>\n'
                      '<div class="hl" data-note="Gerekçe satırı"><div class="r-help">Fatura için gerekli</div></div>\n'
                      '<div class="r-cta">Devam</div>', b)
        self.assertEqual(gate("add", a, b), [])

    def test_insert_before(self):
        a, b = compiled(SIMPLE, {"op": "insert_before", "target": "mail", "node": {"sub": "Önce"}, "label": "Açıklama"})
        self.assertIn('<div class="hl" data-note="Açıklama"><div class="r-sub">Önce</div></div>\n'
                      '<div class="r-field empty">E-posta</div>', b)
        self.assertEqual(gate("add", a, b), [])

    def test_replace_rings_b_and_a_only_with_label_a(self):
        change = {"op": "replace", "target": "cta", "node": {"cta": "Teklif al"}, "label": "Yeni metin"}
        a, b = compiled(SIMPLE, change)
        self.assertNotIn("hl", a)
        self.assertIn('<div class="hl" data-note="Yeni metin"><div class="r-cta">Teklif al</div></div>', b)
        self.assertEqual(gate("change", a, b), [])
        a2, b2 = compiled(SIMPLE, dict(change, label_a="Eski metin"))
        self.assertIn('<div class="hl" data-note="Eski metin"><div class="r-cta">Devam</div></div>', a2)
        self.assertEqual(b2, b)
        self.assertEqual(gate("change", a2, b2), [])

    def test_remove_rings_a_and_leaves_b_empty(self):
        a, b = compiled(SIMPLE, {"op": "remove", "target": "help", "label": "Alan kaldırıldı"})
        self.assertIn('<div class="hl" data-note="Alan kaldırıldı"><div class="r-help">Yardım</div></div>', a)
        self.assertNotIn("Yardım", b)
        self.assertNotIn("hl", b)
        self.assertEqual(gate("remove", a, b), [])

    def test_move_rings_both_with_the_same_content(self):
        for op in ("move_after", "move_before"):
            a, b = compiled(SIMPLE, {"op": op, "target": "help", "to": "h", "label_a": "Formun altında",
                                     "label_b": "Başlığın yanında"})
            self.assertIn('<div class="hl" data-note="Formun altında"><div class="r-help">Yardım</div></div>', a)
            self.assertIn('<div class="hl" data-note="Başlığın yanında"><div class="r-help">Yardım</div></div>', b)
            lines = b.split("\n")
            idx = lines.index('<div class="hl" data-note="Başlığın yanında"><div class="r-help">Yardım</div></div>')
            self.assertEqual(idx, 1 if op == "move_after" else 0, b)
            self.assertEqual(gate("move", a, b), [], op)

    def test_move_below_the_fold_with_a_fold_target(self):
        screen = [{"h": "Sepetim", "id": "h"}, {"cta": "Ödemeye geç", "id": "cta"}, {"fold": True, "id": "fold"},
                  {"line": ["Toplam", "890 TL"], "id": "total"}]
        a, b = compiled(screen, {"op": "move_after", "target": "cta", "to": "fold", "label_a": "İlk ekranda",
                                 "label_b": "Kaydırınca görünüyor"})
        self.assertIn('<div class="r-fold"></div>', a)
        self.assertLess(b.index('<div class="r-fold"></div>'), b.index("Ödemeye geç"))
        self.assertEqual(gate("move", a, b), [])

    def test_edit_changes_one_property_and_rings_b(self):
        screen = [{"h": "Sepetim", "id": "h"}, {"check": "Kampanya e-postası", "on": False, "id": "chk"},
                  {"cta": "Devam", "id": "cta"}]
        a, b = compiled(screen, {"op": "edit", "target": "cta", "set": {"style": "outline"}, "label": "Çerçeveli buton"})
        self.assertIn('<div class="r-cta">Devam</div>', a)
        self.assertIn('<div class="hl" data-note="Çerçeveli buton"><div class="r-cta outline">Devam</div></div>', b)
        self.assertEqual(gate("change", a, b), [])
        a, b = compiled(screen, {"op": "edit", "target": "cta", "set": {"text": "Teklif al"}, "label": "Buton metni",
                                 "label_a": "Eski metin"})
        self.assertIn('data-note="Eski metin"><div class="r-cta">Devam</div>', a)
        self.assertIn('data-note="Buton metni"><div class="r-cta">Teklif al</div>', b)
        self.assertEqual(gate("change", a, b), [])

    def test_edit_inside_a_dict_valued_kind(self):
        screen = [{"plan": {"name": "Pro", "price": "299 TL"}, "id": "plan"}, {"cta": "Seç", "id": "cta"}]
        a, b = compiled(screen, {"op": "edit", "target": "plan", "set": {"featured": True}, "label": "Öne çıkan plan"})
        self.assertIn('<div class="r-plan">', a)
        self.assertIn('<div class="hl" data-note="Öne çıkan plan"><div class="r-plan featured">', b)
        self.assertEqual(gate("change", a, b), [])

    def test_edit_that_changes_nothing_is_refused(self):
        problems = problems_of(SIMPLE, {"op": "edit", "target": "cta", "set": {"cta": "Devam"}, "label": "Aynı"})
        self.assertIn("B would equal A", problems[0])

    def test_edit_of_an_unknown_property_is_refused(self):
        problems = problems_of(SIMPLE, {"op": "edit", "target": "cta", "set": {"on": True}, "label": "X"})
        self.assertIn('"on" is not something a cta node has', problems[0])

    def test_label_pos_below_adds_room_for_the_label(self):
        a, b = compiled(SIMPLE, {"op": "insert_after", "target": "mail", "node": {"help": "Satır"},
                                 "label": "Gerekçe satırı", "label_pos": "below"})
        self.assertIn('<div class="hl" data-note="Gerekçe satırı" data-pos="below">'
                      '<div class="r-help" style="margin-bottom:20px">Satır</div></div>', b)
        _, b2 = compiled(SIMPLE, {"op": "insert_after", "target": "mail", "node": {"help": "Satır"},
                                  "label": "Gerekçe satırı", "label_pos": "above"})
        self.assertIn('data-pos="above"><div class="r-help" style="margin-top:20px">Satır</div></div>', b2)

    def test_a_target_inside_a_band_or_row(self):
        screen = [{"band": {"items": [{"row": [{"field": "Ay", "id": "ay"}, {"field": "Yıl", "id": "yil"}]}]}}]
        a, b = compiled(screen, {"op": "edit", "target": "yil", "set": {"select": True}, "label": "Açılır liste"})
        self.assertIn('<div class="r-row"><div class="r-field empty">Ay</div><div class="hl" data-note="Açılır liste">'
                      '<div class="r-field empty select">Yıl</div></div></div>', b)
        self.assertEqual(gate("change", a, b), [])

    def test_the_ring_wrapper_carries_no_style_of_its_own(self):
        change = {"op": "insert_after", "target": "mail", "node": {"help": "Satır", "mb": 12, "fg": "#000000"},
                  "label": "Satır", "label_pos": "below"}
        _, b = compiled(SIMPLE, change)
        self.assertIn('<div class="hl" data-note="Satır" data-pos="below"><div class="r-help" style="color:#000000;', b)


# ------------------------------------------------------------ soft rings and sharing

class TestSoftAndSharing(unittest.TestCase):
    def test_soft_wraps_the_named_nodes_in_both_arms(self):
        a, b = compiled(SIMPLE, {"op": "edit", "target": "cta", "set": {"cta": "Satın al"}, "label": "Buton metni"},
                        soft=[{"id": "help", "note": "Yardım metni"}, "h"])
        for arm in (a, b):
            self.assertIn('<div class="hl-soft" data-note="Yardım metni"><div class="r-help">Yardım</div></div>', arm)
            self.assertIn('<div class="hl-soft"><div class="r-h">Sepetim</div></div>', arm)
        self.assertEqual(gate("change", a, b), [])

    def test_soft_limits(self):
        change = {"op": "edit", "target": "cta", "set": {"cta": "Satın al"}, "label": "Buton metni"}
        self.assertIn("up to 2", problems_of(SIMPLE, change, soft=["h", "mail", "help"])[0])
        self.assertIn("change's own target", problems_of(SIMPLE, change, soft=["cta"])[0])
        self.assertIn('no node in card.screen has id "yok"', problems_of(SIMPLE, change, soft=["yok"])[0])

    def test_variant_a_is_byte_identical_across_records_sharing_a_screen(self):
        a1, _ = compiled(SCREEN, CHANGE)
        a2, _ = compiled(SCREEN, {"op": "edit", "target": "eposta", "set": {"field": "E-Posta Adresiniz"},
                                  "label": "Alan adı"})
        a3, _ = compiled(SCREEN, {"op": "remove", "target": "adiniz", "label": "Alan kaldırıldı"})
        self.assertEqual(a1.encode("utf-8"), a2.encode("utf-8"))
        self.assertEqual(a1, a3.replace('<div class="hl" data-note="Alan kaldırıldı">', "").replace(
            "Adınız</div></div>", "Adınız</div>"))

    def test_compile_is_deterministic_and_pure(self):
        screen, change = copy.deepcopy(SCREEN), copy.deepcopy(CHANGE)
        first = ss.compile(screen, change, "tr")
        self.assertEqual(first, ss.compile(screen, change, "tr"))
        self.assertEqual(screen, SCREEN)
        self.assertEqual(change, CHANGE)


# ------------------------------------------------------------ refusals

class TestRefusals(unittest.TestCase):
    def test_unknown_kind(self):
        problems = problems_of([{"headline": "X", "id": "x"}, {"h": "H", "id": "h"}],
                               {"op": "edit", "target": "h", "set": {"h": "I"}, "label": "Başlık"})
        self.assertIn("unknown node kind (headline, id)", problems[0])

    def test_two_kinds_in_one_node(self):
        problems = problems_of([{"h": "X", "sub": "Y"}, {"cta": "C", "id": "c"}],
                               {"op": "edit", "target": "c", "set": {"cta": "D"}, "label": "Buton"})
        self.assertIn("names one kind, this one names 2", problems[0])

    def test_missing_target(self):
        problems = problems_of(SIMPLE, {"op": "insert_after", "target": "yok", "node": {"help": "X"}, "label": "Satır"})
        self.assertIn('no node in card.screen has id "yok"', problems[0])
        problems = problems_of(SIMPLE, {"op": "insert_after", "node": {"help": "X"}, "label": "Satır"})
        self.assertIn("card.change.target is missing", problems[0])
        problems = problems_of(SIMPLE, {"op": "move_after", "target": "help", "to": "yok", "label_a": "A", "label_b": "B"})
        self.assertIn('card.change.to: no node in card.screen has id "yok"', problems[0])

    def test_duplicate_id(self):
        problems = problems_of([{"h": "X", "id": "dup"}, {"sub": "Y", "id": "dup"}],
                               {"op": "edit", "target": "dup", "set": {"sub": "Z"}, "label": "Alt"})
        self.assertIn('id "dup" is already used at card.screen[0]', problems[0])

    def test_two_changes(self):
        for change in ([CHANGE, CHANGE], None, "insert_after"):
            problems = ss.compile(SIMPLE, change, "en")[2]
            self.assertTrue(problems, repr(change))
            self.assertIn("card.change", problems[0])
        problems = problems_of(SIMPLE, {"op": "insert_after", "target": "mail", "node": {"help": "X"}, "label": "Satır",
                                        "to": "h"})
        self.assertIn('"to" is not a field of op insert_after', problems[0])

    def test_unknown_op_and_missing_labels(self):
        self.assertIn("card.change.op must be one of", problems_of(SIMPLE, {"op": "swap", "target": "h"})[0])
        self.assertIn("card.change.label:", problems_of(SIMPLE, {"op": "remove", "target": "h"})[0])
        self.assertIn("card.change.label_b:", problems_of(SIMPLE, {"op": "move_after", "target": "h", "to": "cta",
                                                                   "label_a": "A"})[0])

    def test_top_only_kinds_inside_a_container(self):
        problems = problems_of([{"band": {"items": [{"fold": True}]}}, {"h": "H", "id": "h"}],
                               {"op": "edit", "target": "h", "set": {"h": "I"}, "label": "Başlık"})
        self.assertIn("a fold node sits only at the top level", problems[0])

    def test_nothing_half_drawn_leaves_the_compiler(self):
        a, b, problems = ss.compile(SIMPLE, {"op": "remove", "target": "yok", "label": "X"}, "en")
        self.assertTrue(problems)
        self.assertEqual((a, b), ("", ""))

    def test_turkish_messages_have_no_em_dash(self):
        for en, tr in ss.MSG.values():
            self.assertNotIn("\u2014", tr)
            self.assertNotIn("\u2014", en)

    def test_forms(self):
        self.assertEqual(ss.card_form({"variant_a": "x", "variant_b": "y"}), "raw")
        self.assertEqual(ss.card_form({"screen": [], "change": {}}), "spec")
        self.assertEqual(ss.card_form({"variant_a": "x", "screen": []}), "both")
        self.assertIsNone(ss.card_form({"difference": "add"}))
        self.assertIn("both forms", ss.form_problems({"variant_a": "x", "variant_b": "y", "screen": SCREEN})[0])
        self.assertIn("either card.variant_a", ss.form_problems({})[0])
        self.assertIn("card.variant_b is missing", ss.form_problems({"variant_a": "x"})[0])
        self.assertIn("card.change is missing", ss.form_problems({"screen": SCREEN})[0])
        self.assertIn("card.soft belongs", ss.form_problems({"variant_a": "x", "variant_b": "y", "soft": ["a"]})[0])
        self.assertEqual(ss.form_problems({"screen": SCREEN, "change": CHANGE}), [])


# ------------------------------------------------------------ the builder's hook

class TestBuilderHook(unittest.TestCase):
    def test_normalize_compiles_the_screen(self):
        view = bc.normalize(reference_record())
        a, b, _ = ss.compile(SCREEN, CHANGE, "en")
        self.assertEqual((view["variant_a"], view["variant_b"]), (a, b))
        self.assertTrue(view["screen_spec"])
        self.assertEqual(len(view["inherited_contrast"]), 5)

    def test_raw_form_is_untouched(self):
        with open(os.path.join(REPO_ROOT, "examples", "scenario.json"), encoding="utf-8") as fh:
            sc = json.load(fh)
        view = bc.normalize(sc)
        self.assertFalse(view["screen_spec"])
        self.assertEqual(view["variant_a"], sc["card"]["variant_a"])

    def test_both_forms_die(self):
        sc = reference_record()
        sc["card"]["variant_a"] = sc["card"]["variant_b"] = '<div class="r-h">X</div>'
        text = die_text(bc.normalize, sc)
        self.assertIn("both forms are given", text)

    def test_a_spec_problem_dies_with_the_problem(self):
        sc = reference_record()
        sc["card"]["change"] = dict(CHANGE, target="yok")
        text = die_text(bc.normalize, sc)
        self.assertIn("the screen spec was refused", text)
        self.assertIn('no node in card.screen has id "yok"', text)
        text = die_text(bc.normalize, sc, "tr")
        self.assertIn("ekran tanımı reddedildi", text)

    def test_build_passes_every_gate_and_the_manifest_says_so(self):
        warnings, manifest = [], {}
        html = bc.build(TEMPLATE, reference_record(), warnings=warnings, manifest=manifest)
        self.assertIn('data-note="Gerekçe satırı eklendi"', html)
        self.assertEqual(len(manifest["rings"]), 1)
        self.assertEqual(bc.final_fingerprint(TEMPLATE, reference_record()), bc.html_fingerprint(html))

    def test_isolated_python_still_runs_the_builder(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "s.json")
            with open(src, "w", encoding="utf-8") as fh:
                json.dump(reference_record(), fh, ensure_ascii=False)
            out = os.path.join(d, "abtest-card-ref.draft.html")
            p = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "build_card.py"), "--template",
                                TEMPLATE_PATH, "--scenario", src, "--out", out, "--draft"],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            with open(out + ".manifest.json", encoding="utf-8") as fh:
                doc = json.load(fh)
            self.assertTrue(doc["screen_spec"])


# ------------------------------------------------------------ the validator's seam

class TestValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = vsj.load_schema()

    def errors(self, sc):
        return vsj.validate(sc, self.schema, "en")

    def test_the_reference_record_validates_strictly(self):
        sc = reference_record()
        self.assertEqual(self.errors(sc), [])
        self.assertEqual(vsj.lint(sc, self.schema, "en"), [])

    def test_exactly_one_form(self):
        sc = reference_record()
        sc["card"]["variant_a"] = sc["card"]["variant_b"] = '<div class="r-h">X</div>'
        self.assertTrue(any("both forms are given" in e for e in self.errors(sc)), self.errors(sc))
        del sc["card"]["screen"], sc["card"]["change"], sc["card"]["variant_b"]
        self.assertTrue(any("card.variant_b is missing" in e for e in self.errors(sc)), self.errors(sc))
        del sc["card"]["variant_a"]
        self.assertTrue(any("either card.variant_a and card.variant_b" in e for e in self.errors(sc)), self.errors(sc))

    def test_a_spec_problem_is_a_validator_error(self):
        sc = reference_record()
        sc["card"]["change"] = dict(CHANGE, target="yok")
        self.assertTrue(any('no node in card.screen has id "yok"' in e for e in self.errors(sc)), self.errors(sc))

    def test_the_validator_sees_the_compiled_markup(self):
        sc = reference_record()
        sc["difference"] = sc["card"]["difference"] = "remove"  # the spec draws an add
        errs = self.errors(sc)
        self.assertTrue(any("difference 'remove'" in e for e in errs), errs)

    def test_schema_accepts_the_new_fields(self):
        sc = reference_record()
        sc["card"]["soft"] = ["adiniz"]
        self.assertEqual([e for e in self.errors(sc) if "additionalProperties" in e or "not allowed" in e], [])


# ------------------------------------------------------------ end to end

def _playwright_ready():
    if not NODE:
        return False
    p = subprocess.run([NODE, "-e", "require.resolve('playwright')"], capture_output=True)
    return p.returncode == 0


class TestEndToEnd(unittest.TestCase):
    """The health-form spec: --strict, a draft build, and render_check --strict when Playwright is available."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.src = os.path.join(cls.tmp.name, "finance-pension-kimlik-gerekce-01.json")
        with open(cls.src, "w", encoding="utf-8") as fh:
            json.dump(reference_record(), fh, ensure_ascii=False, indent=1)
        cls.draft = os.path.join(cls.tmp.name, "abtest-card-kimlik-gerekce.draft.html")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_1_strict_validation(self):
        p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "validate_scenario_json.py"), "--strict", self.src],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

    def test_2_draft_build(self):
        p = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "build_card.py"), "--template", TEMPLATE_PATH,
                            "--scenario", self.src, "--out", self.draft, "--draft"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("draft:", p.stdout)
        with open(self.draft, encoding="utf-8") as fh:
            html = fh.read()
        for text in PLACEHOLDERS:
            self.assertEqual(html.count(">%s<" % text), 2)
        self.assertEqual(html.count('data-note="Gerekçe satırı eklendi"'), 1)

    @unittest.skipUnless(_playwright_ready(), "Playwright yok (NODE_PATH)")
    def test_3_render_check_strict_is_verified(self):
        if not os.path.exists(self.draft):
            self.test_2_draft_build()
        p = subprocess.run([NODE, os.path.join(SCRIPTS, "render_check.mjs"), "--strict", self.draft],
                           capture_output=True, text=True, timeout=180)
        if p.returncode == 3:
            self.skipTest("render_check could not start a browser: " + p.stderr.strip()[:200])
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("render_check: VERIFIED", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
