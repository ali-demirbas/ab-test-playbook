#!/usr/bin/env python3
"""Aşama 3 kalite kapıları için regresyon testleri. Bağımlılıksız (unittest).

Her bulgu için bir olumsuz (kötü girdi reddedilir, mesajıyla) ve bir olumlu
(düzeltilmiş girdi geçer) test. Sözleşmenin "Regression tests" maddeleri:
1 (halka dışında fiyat), 2 (halka içinde fiyat ve numeric_change), 3 (halka
içinde ikinci değişiklik: manifest + mockup damgası), 4 (eskiden uyarı olan
hatalar), 5 kart tarafı (etkileşimli öğe ve erişilebilirlik ölçütleri),
10 kart tarafı (yasal metin, önceden işaretli onay, SMS doğrulaması), 11
(kişisel veri) ve 12 (damga kapıları, yazılmayan dosya). Damgalar burada
programla üretilir: eleştirmen damgası record_fingerprint ile, mockup damgası
build_card.mockup_stamp ile.
"""
import contextlib
import copy
import hashlib
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

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")

with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()

A11Y_LINK = ("Yeni bağlantı klavyeyle erişilebilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt "
             "ve metin kontrastı en az 4.5:1 olur.")
A11Y_MODAL = A11Y_LINK + " Açılınca odağı alır, görünür bir düğmeyle ve Esc ile kapanır."
HEAD = '<div class="r-h">Sepetim</div>'
TOTAL = '<div class="r-line total"><span>Toplam</span><span>890 TL</span></div>'


def example():
    """The shipped coupon record WITHOUT its review stamps: the gate tests stamp
    it themselves (stamped()) or exercise the unstamped path."""
    with open(EXAMPLE, encoding="utf-8") as fh:
        sc = json.load(fh)
    sc.pop("review", None)
    return sc


def shipped_example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


def record(variant_a, variant_b, difference="change", **over):
    """The shipped record with its card's two mockups replaced."""
    sc = example()
    sc["card"]["variant_a"], sc["card"]["variant_b"] = variant_a, variant_b
    # Contract 5: card.difference never overrides the record's, so both say the same.
    sc["card"]["difference"] = sc["difference"] = difference
    sc.update(over)
    return sc


def ring(inner, note="Yeni"):
    return '<div class="hl" data-note="%s">%s</div>' % (note, inner)


def die_text(fn, *args, **kw):
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            fn(*args, **kw)
        except SystemExit:
            return err.getvalue()
    raise AssertionError("expected the builder to refuse; it built instead")


def builds(sc, **kw):
    """build() succeeds; returns (html, warnings, manifest)."""
    warnings, manifest = [], {}
    err = io.StringIO()
    with contextlib.redirect_stderr(err):
        try:
            html = bc.build(TEMPLATE, sc, warnings=warnings, manifest=manifest, **kw)
        except SystemExit:
            raise AssertionError("expected a card, the builder refused:\n" + err.getvalue())
    return html, warnings, manifest


def critic_stamp(sc):
    return {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}


def stamped(sc, critic=True, mockup=True):
    sc = copy.deepcopy(sc)
    sc["review"] = {}
    if critic:
        sc["review"]["scenario_critic"] = critic_stamp(sc)
    if mockup:
        sc["review"]["mockup_reviewer"] = {"verdict": "PASS", "fingerprint": bc.mockup_stamp(TEMPLATE, sc)}
    return sc


class Run:
    """build_card.main() in a temporary directory."""

    def __init__(self, scenario, *extra, out_name="abtest-card-kupon.html", existing=None):
        self.tmp = tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.src = os.path.join(d, "s.json")
        self.out = os.path.join(d, out_name)
        self.manifest = self.out + ".manifest.json"
        with open(self.src, "w", encoding="utf-8") as fh:
            json.dump(scenario, fh, ensure_ascii=False)
        if existing is not None:
            with open(self.out, "w", encoding="utf-8") as fh:
                fh.write(existing)
        out, err = io.StringIO(), io.StringIO()
        msg_lang = bc._MSG_LANG
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                self.code = bc.main(["--template", TEMPLATE_PATH, "--scenario", self.src, "--out", self.out]
                                    + list(extra))
            except SystemExit as exc:
                self.code = exc.code
            finally:
                bc._MSG_LANG = msg_lang
        self.stdout, self.stderr = out.getvalue(), err.getvalue()

    def read(self, path=None):
        path = path or self.out
        if not os.path.exists(path):
            return None
        with open(path, "rb") as fh:
            return fh.read()

    def close(self):
        self.tmp.cleanup()


class RunCase(unittest.TestCase):
    def run_main(self, scenario, *extra, **kw):
        r = Run(scenario, *extra, **kw)
        self.addCleanup(r.close)
        return r

    def assertRefused(self, r, *fragments):
        self.assertEqual(r.code, 1, r.stderr)
        self.assertIn("REFUSED at the", r.stderr)
        for fragment in fragments:
            self.assertIn(fragment, r.stderr)


# ------------------------------------------------------------ 1 and 2: numbers

class TestPriceOutsideTheRing(unittest.TestCase):
    """Madde 1: halkanın dışındaki fiyat farkı reddedilir (eskiden uyarıydı)."""

    def test_price_outside_the_ring_is_refused(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            '<div class="r-line total"><span>Toplam</span><span>890 TL</span></div>',
            '<div class="r-line total"><span>Toplam</span><span>790 TL</span></div>')
        msg = die_text(bc.build, TEMPLATE, sc)
        self.assertIn("A and B differ outside any ring", msg)
        self.assertIn("numbers differ between A and B (only in A: 890; only in B: 790)", msg)

    def test_numeric_change_does_not_excuse_a_difference_outside_the_ring(self):
        sc = example()
        sc["numeric_change"] = "Fiyat testi."
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("<span>890 TL</span></div>\n          <div class=\"r-cta\">",
                                                                  "<span>790 TL</span></div>\n          <div class=\"r-cta\">")
        msg = die_text(bc.build, TEMPLATE, sc)
        self.assertIn("outside any ring", msg)
        self.assertNotIn("numbers differ", msg)

    def test_same_prices_build(self):
        builds(example())


class TestPriceInsideTheRing(unittest.TestCase):
    """Madde 2: halkanın içindeki fiyat farkı numeric_change olmadan reddedilir, onunla geçer ve manifestte görünür."""

    A = HEAD + ring('<div class="r-price">1.299,90 TL</div>', "Fiyat")
    B = HEAD + ring('<div class="r-price">1.099,90 TL</div>', "Fiyat")

    def test_refused_without_numeric_change(self):
        msg = die_text(bc.build, TEMPLATE, record(self.A, self.B))
        self.assertIn("numbers differ between A and B (only in A: 1.299,90; only in B: 1.099,90)", msg)
        self.assertIn("`numeric_change`", msg)

    def test_passes_with_numeric_change_and_the_manifest_lists_it(self):
        _, _, manifest = builds(record(self.A, self.B, numeric_change="Fiyat testi: B indirimli fiyatı gösterir."))
        numbers = [c for c in manifest["changes"] if c["kind"] == "number"]
        self.assertEqual(numbers, [{"ring": 1, "label": "Fiyat", "kind": "number", "change": "changed",
                                    "element": "div.r-price", "a": "1.299,90", "b": "1.099,90"}])

    def test_blank_numeric_change_is_no_reason(self):
        self.assertIn("numbers differ", die_text(bc.build, TEMPLATE, record(self.A, self.B, numeric_change="  ")))

    def test_a_number_only_b_shows_is_a_difference(self):
        b = HEAD + ring('<div class="r-sub">500 TL üzeri ücretsiz kargo</div>', "Kargo eşiği")
        msg = die_text(bc.build, TEMPLATE, record(HEAD, b, difference="add"))
        self.assertIn("only in A: -; only in B: 500", msg)


class TestNumberTokens(unittest.TestCase):
    def test_formats_are_one_token_each(self):
        cases = {
            "1.299 TL": ["1.299"], "1,299.00": ["1,299.00"], "₺1.299,90": ["1.299,90"], "%20 indirim": ["%20"],
            "20% off": ["20%"], "4,5 puan": ["4,5"], "4.5★": ["4.5"], "(3)": ["3"], "1.2345": ["1.2345"],
            "Beden M · 1 adet": ["1"], "0850 000 00 00": ["0850", "000", "00", "00"], "A4 kâğıt": [],
            "% 15": ["%15"], "12 345": ["12", "345"],
        }
        for text, tokens in cases.items():
            with self.subTest(text):
                self.assertEqual(bc.number_tokens(text), tokens)

    def test_same_numbers_in_another_order_are_not_a_difference(self):
        a = HEAD + '<div class="r-line"><span>Ara toplam</span><span>890 TL</span></div>' + ring('<div class="r-sub">Kargo 0 TL</div>')
        b = HEAD + '<div class="r-line"><span>Ara toplam</span><span>890 TL</span></div>' + ring('<div class="r-sub">0 TL kargo</div>')
        _, _, manifest = builds(record(a, b))
        self.assertEqual([c for c in manifest["changes"] if c["kind"] == "number"], [])


# ---------------------------------------- 3: a second change inside the ring

class TestSecondChangeInsideTheRing(RunCase):
    """Madde 3: kod halka içindeki ikinci değişikliği kanıtlayamaz; manifest listeler, final mockup damgası ister."""

    def scenario(self):
        sc = example()
        sc["card"]["variant_a"] = sc["card"]["variant_a"].replace(
            '<div class="r-field empty">Kodu buraya girin</div>',
            '<div class="r-field empty">Kodu buraya girin</div>\n            <div class="r-cta sm outline">Uygula</div>')
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            '<div class="r-link hl" data-note="Kupon bağlantıda" style="align-self:flex-start;line-height:44px">İndirim kodum var</div>',
            '<div class="hl" data-note="Kupon bağlantıda"><div class="r-link">İndirim kodum var</div>'
            '\n            <div class="r-cta sm outline">Kodu kullan</div></div>')
        return sc

    def test_manifest_lists_the_extra_change(self):
        _, _, manifest = builds(self.scenario())
        texts = [(c["element"], c["change"], c["a"], c["b"]) for c in manifest["changes"] if c["kind"] == "text"]
        self.assertIn(("div.r-cta", "changed", "Uygula", "Kodu kullan"), texts)
        self.assertIn(("div.r-link", "added", None, "İndirim kodum var"), texts)
        self.assertTrue(all(c["label"] == "Kupon bağlantıda / Kupon alanı açık" for c in manifest["changes"]))

    def test_draft_writes_the_manifest_with_the_extra_change(self):
        sc = self.scenario()
        sc["review"] = {"scenario_critic": critic_stamp(sc)}
        r = self.run_main(sc, "--draft", out_name="abtest-card-kupon.draft.html")
        self.assertEqual(r.code, 0, r.stderr)
        doc = json.loads(r.read(r.manifest).decode("utf-8"))
        self.assertIn({"ring": 1, "label": "Kupon bağlantıda / Kupon alanı açık", "kind": "text", "change": "changed",
                       "element": "div.r-cta", "a": "Uygula", "b": "Kodu kullan"}, doc["changes"])

    def test_final_without_a_mockup_stamp_is_refused(self):
        r = self.run_main(stamped(self.scenario(), mockup=False))
        self.assertRefused(r, "review stamps", "missing review stamp: review.mockup_reviewer")
        self.assertIsNone(r.read())

    def test_final_with_a_stamp_for_the_earlier_card_is_refused(self):
        reviewed = stamped(example())  # the mockup reviewer passed the card without the extra button
        sc = self.scenario()
        sc["review"] = copy.deepcopy(reviewed["review"])
        r = self.run_main(sc)
        self.assertRefused(r, "review.mockup_reviewer.fingerprint", "doesn't match the card this build would write")
        self.assertIsNone(r.read())

    def test_final_with_matching_stamps_is_written(self):
        r = self.run_main(stamped(self.scenario()))
        self.assertEqual(r.code, 0, r.stderr)
        self.assertIsNotNone(r.read())


# ------------------------------------------- 4: warnings that are now errors

class TestFormerWarningsAreErrors(unittest.TestCase):
    """Madde 4: eskiden yalnızca uyarıyla kart üreten iki durum artık reddedilir."""

    def test_difference_outside_the_ring_is_refused(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("Ödemeye geç", "Güvenli ödemeye geç")
        msg = die_text(bc.build, TEMPLATE, sc)
        self.assertIn("A and B differ outside any ring", msg)
        self.assertIn("Güvenli ödemeye geç", msg)

    def test_the_same_change_inside_the_ring_builds(self):
        a = HEAD + '<div class="r-cta">Ödemeye geç</div>'
        b = HEAD + ring('<div class="r-cta">Güvenli ödemeye geç</div>', "Buton metni")
        _, _, manifest = builds(record(a, b))
        self.assertEqual(manifest["changes"][0]["a"], "Ödemeye geç")

    def test_colour_only_in_b_outside_the_ring_is_refused(self):
        sc = example()
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace(
            '<div class="r-cta">', '<div class="r-cta" style="background:#0a7f3f">')
        self.assertIn("inline colour only in Variant B on an element outside the ring: #0a7f3f",
                      die_text(bc.build, TEMPLATE, sc))

    def test_the_same_colour_on_both_sides_builds(self):
        sc = example()
        for key in ("variant_a", "variant_b"):
            sc["card"][key] = sc["card"][key].replace('<div class="r-cta">', '<div class="r-cta" style="background:#0a7f3f">')
        builds(sc)

    def test_outside_messages_exist_in_turkish(self):
        errors, _ = bc.card_problems("change", HEAD + '<div class="r-sub">x</div>',
                                     ring(HEAD) + '<div class="r-sub">y</div>', lang="tr")
        self.assertTrue(any("halkanın dışında da farklı" in e for e in errors), errors)


class TestAlignment(unittest.TestCase):
    """Halka dışı fark denetimi meşru biçimleri yanlışlıkla reddetmez."""

    def test_moved_element_that_trades_places_with_its_neighbour(self):
        moved = ring('<div class="r-cta">Ödemeye geç</div>', "Taşındı")
        errors, _ = bc.card_problems("move", moved + HEAD, HEAD + moved)
        self.assertEqual(errors, [])

    def test_change_ringed_on_both_sides_still_sees_a_neighbour_change(self):
        a = ring('<div class="r-sub">Eski</div>', "Metin") + '<div class="r-sub" style="color:#111">Not</div>'
        b = ring('<div class="r-sub">Yeni</div>', "Metin") + '<div class="r-sub" style="color:#222">Not</div>'
        errors, _ = bc.card_problems("change", a, b)
        self.assertTrue(any("outside any ring" in e for e in errors), errors)

    def test_ring_with_a_new_neighbour_is_refused(self):
        a = HEAD + '<div class="r-field">Kod</div>'
        b = HEAD + ring('<div class="r-link">Kodum var</div>') + '<div class="r-sub">Yeni not</div>'
        errors, _ = bc.card_problems("change", a, b)
        self.assertTrue(any("Yeni not" in e for e in errors), errors)

    def test_deep_ring_inside_an_unchanged_container(self):
        a = '<div class="r-card">%s<div class="r-sub">Eski</div></div>' % HEAD
        b = '<div class="r-card">%s%s</div>' % (HEAD, ring('<div class="r-sub">Yeni</div>'))
        errors, _ = bc.card_problems("change", a, b)
        self.assertEqual(errors, [])


# ---------------------------------------------- 5 (card side): accessibility

class TestAccessibilityGate(unittest.TestCase):
    """Madde 5, kart tarafı: B etkileşimli öğe ekliyorsa erişilebilirlik uyarısı ve öğeye uyan ölçütler gerekir."""

    LINK_A = HEAD + '<div class="r-sub">Kupon kodunuz varsa ödeme adımında girin.</div>'
    LINK_B = HEAD + ring('<div class="r-link">İndirim kodum var</div>', "Bağlantı")

    def test_added_link_without_an_accessibility_warning_is_refused(self):
        msg = die_text(bc.build, TEMPLATE, record(self.LINK_A, self.LINK_B, warnings=[]))
        self.assertIn("B adds an interactive element (r-link 0 → 1) and the record has no accessibility warning", msg)

    def test_another_warning_type_does_not_count(self):
        msg = die_text(bc.build, TEMPLATE, record(self.LINK_A, self.LINK_B,
                                                  warnings=[{"type": "feasibility", "text": A11Y_LINK}]))
        self.assertIn("no accessibility warning", msg)

    def test_incomplete_criteria_are_refused(self):
        text = "Yeni bağlantı ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt ve kontrast en az 4.5:1 olur."
        msg = die_text(bc.build, TEMPLATE, record(self.LINK_A, self.LINK_B,
                                                  warnings=[{"type": "accessibility", "text": text}]))
        self.assertIn("the accessibility warning lacks: keyboard access", msg)

    def test_a_number_like_14_5_is_not_a_contrast_criterion(self):
        text = "Yeni bağlantı klavyeyle erişilir, ekran okuyucuda adıyla okunur, dokunma alanı 44×44 pt, yazı 14.5 px."
        msg = die_text(bc.build, TEMPLATE, record(self.LINK_A, self.LINK_B,
                                                  warnings=[{"type": "accessibility", "text": text}]))
        self.assertIn("lacks: text contrast (at least 4.5:1)", msg)

    def test_the_criteria_are_the_validators(self):
        self.assertEqual(bc.accessibility_criteria(), list(vsj.A11Y_BASE))
        self.assertEqual(bc.accessibility_criteria(dialog=True), list(vsj.A11Y_BASE) + list(vsj.A11Y_MODAL))
        self.assertFalse(hasattr(bc, "A11Y_CRITERIA"))

    def test_complete_criteria_pass(self):
        builds(record(self.LINK_A, self.LINK_B, warnings=[{"type": "accessibility", "text": A11Y_LINK}]))

    def test_a_count_increase_counts(self):
        a = HEAD + '<div class="r-cta">Devam</div>'
        b = HEAD + '<div class="r-cta">Devam</div>' + ring('<div class="r-cta outline">Sonra</div>', "İkinci buton")
        msg = die_text(bc.build, TEMPLATE, record(a, b, difference="add", warnings=[]))
        self.assertIn("r-cta 1 → 2", msg)

    def test_modal_without_focus_and_close_criteria_is_refused(self):
        modal = ring('<div class="r-overlay"><div class="r-modal"><div class="r-h">Kampanya</div>'
                     '<div class="r-cta">Tamam</div></div></div>', "Açılır pencere")
        msg = die_text(bc.build, TEMPLATE, record(HEAD + '<div class="r-cta">Tamam</div>',
                                                  HEAD + '<div class="r-cta">Tamam</div>' + modal, difference="add",
                                                  warnings=[{"type": "accessibility", "text": A11Y_LINK}]))
        self.assertIn("lacks: taking focus when it opens, a visible close control, closing with Esc", msg)

    def test_modal_with_focus_and_close_criteria_passes(self):
        modal = ring('<div class="r-overlay"><div class="r-modal"><div class="r-h">Kampanya</div>'
                     '<div class="r-cta">Tamam</div></div></div>', "Açılır pencere")
        builds(record(HEAD + '<div class="r-cta">Tamam</div>', HEAD + '<div class="r-cta">Tamam</div>' + modal,
                      difference="add", warnings=[{"type": "accessibility", "text": A11Y_MODAL}]))

    def test_no_new_interactive_element_needs_no_warning(self):
        builds(record(HEAD + TOTAL, ring('<div class="r-h">Alışveriş sepetim</div>') + TOTAL, warnings=[]))

# ------------------------------------- 10 (card side): regulation, manipulation

class TestRegulationGate(unittest.TestCase):
    """Madde 10, kart tarafı: yasal metin, önceden işaretli onay ve SMS doğrulaması."""

    LEGAL = '<div class="r-sub">KVKK aydınlatma metnini okudum.</div>'
    CTA = '<div class="r-cta">Devam</div>'

    def test_legal_text_removed_in_b_is_refused(self):
        a = HEAD + ring(self.LEGAL + self.CTA, "Onay bloğu")
        b = HEAD + ring(self.CTA, "Onay bloğu")
        msg = die_text(bc.build, TEMPLATE, record(a, b))
        self.assertIn("rule 11: legal or mandatory text in A is missing or changed in B (“KVKK aydınlatma metnini okudum.”)", msg)

    def test_legal_text_reworded_in_b_is_refused(self):
        a = HEAD + ring('<div class="r-sub">Mesafeli satış sözleşmesini onaylıyorum.</div>', "Metin")
        b = HEAD + ring('<div class="r-sub">Satış koşullarını kabul ediyorum.</div>', "Metin")
        self.assertIn("rule 11", die_text(bc.build, TEMPLATE, record(a, b)))

    def test_legal_text_kept_passes(self):
        a = HEAD + self.LEGAL + '<div class="r-cta">Devam</div>'
        b = HEAD + self.LEGAL + ring('<div class="r-cta">Devam et</div>', "Buton metni")
        builds(record(a, b))

    def test_pre_ticked_consent_in_b_is_refused(self):
        a = HEAD + ring('<div class="r-check">Kampanya iletileri için ticari elektronik ileti onayı veriyorum.</div>', "Onay")
        b = HEAD + ring('<div class="r-check on">Kampanya iletileri için ticari elektronik ileti onayı veriyorum.</div>', "Onay")
        msg = die_text(bc.build, TEMPLATE, record(a, b))
        self.assertIn("rule 6: a consent box that A leaves unticked is ticked in B", msg)

    def test_consent_left_unticked_passes_and_a_ticked_non_consent_box_passes(self):
        consent = '<div class="r-check">Ticari ileti onayı veriyorum.</div>'
        a = HEAD + consent + ring('<div class="r-check">Faturamı e-posta ile gönder</div>', "Seçim")
        b = HEAD + consent + ring('<div class="r-check on">Faturamı e-posta ile gönder</div>', "Seçim")
        builds(record(a, b))

    def test_sms_verification_removed_in_b_is_refused(self):
        a = HEAD + ring('<div class="r-label">SMS kodu</div><div class="r-field empty">6 haneli kod</div>'
                        '<div class="r-cta">Doğrula</div>', "adım")
        b = HEAD + ring('<div class="r-cta">Devam</div>', "Adım")
        msg = die_text(bc.build, TEMPLATE, record(a, b, numeric_change="test"))
        self.assertIn("rule 6: B drops security or verification text that A shows (“SMS kodu”: 1 in A, 0 in B)", msg)
        self.assertIn("(“doğrula”: 1 in A, 0 in B)", msg)

    def test_sms_verification_kept_passes(self):
        step = '<div class="r-label">SMS kodu</div><div class="r-field empty">6 haneli kod</div>'
        a = HEAD + step + '<div class="r-cta">Doğrula</div>'
        b = HEAD + step + ring('<div class="r-cta">Kodu doğrula</div>', "Buton metni")
        builds(record(a, b))

    def test_turkish_messages(self):
        a = HEAD + ring(self.LEGAL, "Metin")
        msg = die_text(bc.build, TEMPLATE, record(a, HEAD + ring('<div class="r-sub">Okudum.</div>', "Metin")), lang="tr")
        self.assertIn("kural 11", msg)


# ---------------------------------------------------- 11: personal data

class TestPersonalDataGate(unittest.TestCase):
    """Madde 11: kişisel veri biçimindeki değerler reddedilir; maskeler ve sıfırlı yer tutucular geçer."""

    def card_with(self, text):
        line = '<div class="r-sub">%s</div>' % text
        return record(HEAD + line, ring('<div class="r-h">Sepetiniz</div>', "Başlık") + line)

    def test_personal_values_are_refused(self):
        cases = {
            "TCKN": "TC kimlik: 12345678950",
            "IBAN": "IBAN: TR33 0006 1005 1978 6457 8413 26",
            "card number": "Kart: 4111 1111 1111 1111",
            "e-mail address": "E-posta: ayse.yilmaz@gmail.com",
            "mobile number": "Cep: 0532 123 45 67",
        }
        for kind, text in cases.items():
            with self.subTest(kind):
                msg = die_text(bc.build, TEMPLATE, self.card_with(text))
                self.assertIn("a value shaped like personal data (%s:" % kind, msg)
                self.assertIn("rule 15", msg)

    def test_the_message_does_not_repeat_the_value(self):
        msg = die_text(bc.build, TEMPLATE, self.card_with("Cep: 0532 123 45 67"))
        self.assertNotIn("123 45", msg)
        self.assertIn("05•••••••67", msg)

    def test_an_iban_is_reported_once_not_also_as_a_card(self):
        msg = die_text(bc.build, TEMPLATE, self.card_with("TR33 0006 1005 1978 6457 8413 26"))
        self.assertIn("(IBAN:", msg)
        self.assertNotIn("(card number:", msg)

    def test_attribute_values_are_read_too(self):
        sc = record(HEAD + '<div class="r-sub" aria-label="0532 123 45 67">Cep</div>',
                    ring(HEAD, "Başlık") + '<div class="r-sub" aria-label="0532 123 45 67">Cep</div>')
        self.assertIn("mobile number", die_text(bc.build, TEMPLATE, sc))

    def test_masks_and_placeholders_pass(self):
        for text in ("Kart: •••• •••• •••• 1234", "Bakiye: ••• TL", "Çağrı merkezi: 0850 000 00 00",
                     "Cep: 0500 000 00 00", "+90 532 000 00 00", "IBAN: TR00 0000 0000 0000 0000 0000 00",
                     "Kart: 0000 0000 0000 0000", "E-posta: ornek@example.com", "a•••@gmail.com",
                     "Kimlik: •••••••••12", "Sipariş no: 1234-5678"):
            with self.subTest(text):
                builds(self.card_with(text))


# ------------------------------------------------------------- 12: gates

# Every shipped record went through the real pipeline (validator, scenario-critic,
# draft, mockup-reviewer, final) and its demo card is the reviewed final, byte for
# byte. No skip: a template or builder change that alters a reviewed card fails
# here until the card is reviewed again and re-stamped.
SHIPPED = (
    (EXAMPLE, os.path.join(REPO_ROOT, "docs", "demo", "scenario-card.html")),
    (os.path.join(REPO_ROOT, "examples", "samples", "desktop-product.json"),
     os.path.join(REPO_ROOT, "docs", "demo", "sample-desktop-product.html")),
    (os.path.join(REPO_ROOT, "examples", "samples", "app-home.json"),
     os.path.join(REPO_ROOT, "docs", "demo", "sample-app-home.html")),
    (os.path.join(REPO_ROOT, "examples", "samples", "saas-form.json"),
     os.path.join(REPO_ROOT, "docs", "demo", "sample-saas-form.html")),
)


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class TestShippedExampleIsReviewed(unittest.TestCase):
    """The repo's example and samples went through the real pipeline: both stamps exist and match."""

    def test_the_critic_stamp_matches_the_shipped_record(self):
        for path, _ in SHIPPED:
            with self.subTest(os.path.basename(path)):
                sc = _load(path)
                self.assertEqual(sc["review"]["scenario_critic"]["verdict"], "PASS")
                self.assertEqual(bc.stamp_problems(sc, "scenario_critic", critic_stamp(sc)["fingerprint"]), [])

    def test_the_mockup_stamp_matches_the_shipped_card(self):
        for path, _ in SHIPPED:
            with self.subTest(os.path.basename(path)):
                sc = _load(path)
                self.assertEqual(sc["review"]["mockup_reviewer"]["verdict"], "PASS")
                self.assertEqual(sc["review"]["mockup_reviewer"]["fingerprint"], bc.mockup_stamp(TEMPLATE, sc))

    def test_the_shipped_demo_card_is_the_reviewed_final(self):
        for path, demo in SHIPPED:
            with self.subTest(os.path.basename(demo)):
                with open(demo, "rb") as fh:
                    data = fh.read()
                self.assertEqual(hashlib.sha256(data).hexdigest(), bc.final_fingerprint(TEMPLATE, _load(path)))
                self.assertNotIn(b"abtest-status", data)


class TestNoMetadataInTheMockup(unittest.TestCase):
    """Rule 9: the old card's text can't come back by being drawn into both mockups (stage-5 audit probe)."""

    def test_kpi_and_evidence_lines_in_both_mockups_are_refused(self):
        for line in ("Birincil KPI: sipariş", "Guardrail: kupon kullanımı", "Kanıt: arşiv örüntüsü", "Öncelik: Orta",
                     "Primary KPI: orders", "Daha güçlü alternatif: sabit buton"):
            extra = '<div class="r-sub">%s</div>' % line
            msg = die_text(bc.build, TEMPLATE, record(HEAD + extra, HEAD + ring('<div class="r-link">Kodum var</div>') + extra))
            self.assertIn("metadata", msg, line)

    def test_the_records_own_kpi_name_in_a_mockup_is_refused(self):
        sc = example()
        name = sc["primary_kpi"]["name"]
        extra = '<div class="r-sub">%s</div>' % name
        msg = die_text(bc.build, TEMPLATE, record(HEAD + extra, HEAD + ring('<div class="r-link">Kodum var</div>') + extra))
        self.assertIn(name, msg)

    def test_the_shipped_mockups_carry_no_metadata(self):
        for path, _ in SHIPPED:
            with self.subTest(os.path.basename(path)):
                sc = _load(path)
                view = bc.normalize(sc)
                errors, _, _ = bc.mockup_report(view, "en", bc.component_classes(TEMPLATE))
                self.assertFalse([e for e in errors if "metadata" in e], errors)


class TestPhoneScale(unittest.TestCase):
    def test_default_is_the_enlarged_frame(self):
        sc = example()
        sc["card"].pop("phone_scale", None)  # the shipped example sets 1.4 (a short screen)
        self.assertIn('data-phone-scale="1.2"', bc.build(TEMPLATE, sc))

    def test_a_tall_screen_can_keep_the_natural_size(self):
        sc = example()
        sc["card"]["phone_scale"] = 1
        self.assertIn('data-phone-scale="1"', bc.build(TEMPLATE, sc))

    def test_other_values_and_web_frames_are_refused(self):
        for value in (0.8, 2, "1", True):
            sc = example()
            sc["card"]["phone_scale"] = value
            self.assertIn("phone_scale", die_text(bc.build, TEMPLATE, sc), value)
        sc = example()
        sc["card"].update(phone_scale=1, device="web")
        self.assertIn("phone frame", die_text(bc.build, TEMPLATE, sc))


class TestIsolatedMode(unittest.TestCase):
    def test_the_builder_runs_under_python_isolated_mode(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "card.html")
            p = subprocess.run([sys.executable, "-I", os.path.join(REPO_ROOT, "scripts", "build_card.py"),
                                "--template", os.path.join(REPO_ROOT, "templates", "scenario-card.html"),
                                "--scenario", EXAMPLE, "--out", out, "--draft"], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertTrue(os.path.exists(out))


class TestWrittenFileMode(unittest.TestCase):
    def test_the_card_gets_ordinary_file_permissions(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "card.html")
            old = os.umask(0o022)
            try:
                bc._write_all([(out, "<p>x</p>")])
            finally:
                os.umask(old)
            self.assertEqual(os.stat(out).st_mode & 0o777, 0o644)


class TestReviewGates(RunCase):
    """Madde 12: damga kapıları, yazılmayan dosya ve "GÜNCELLENMEDİ" uyarısı."""

    def test_final_without_a_critic_stamp_is_refused(self):
        r = self.run_main(stamped(example(), critic=False))
        self.assertRefused(r, "review stamps", "missing review stamp: review.scenario_critic")
        self.assertIsNone(r.read())

    def test_final_without_any_stamp_names_both(self):
        r = self.run_main(example())
        self.assertRefused(r, "missing review stamp: review.scenario_critic", "missing review stamp: review.mockup_reviewer")

    def test_record_edited_after_the_critic_stamp_is_refused(self):
        sc = stamped(example())
        sc["problem"] = sc["problem"].replace("çıkarabilir", "uzaklaştırabilir")
        r = self.run_main(sc)
        self.assertRefused(r, "review.scenario_critic.fingerprint", "the record changed after scenario-critic reviewed it")
        self.assertIsNone(r.read())

    def test_draft_without_a_critic_stamp_is_refused(self):
        r = self.run_main(example(), "--draft")
        self.assertRefused(r, "the draft build was refused", "missing review stamp: review.scenario_critic")
        self.assertIsNone(r.read())
        self.assertIsNone(r.read(r.manifest))

    def test_draft_with_a_stale_critic_stamp_is_refused(self):
        sc = example()
        sc["review"] = {"scenario_critic": critic_stamp(sc)}
        sc["mechanism"] += " "
        self.assertRefused(self.run_main(sc, "--draft"), "doesn't match the record")

    def test_final_with_both_valid_stamps_is_written(self):
        sc = stamped(example())
        r = self.run_main(sc)
        self.assertEqual(r.code, 0, r.stderr)
        data = r.read()
        fp = bc.final_fingerprint(TEMPLATE, sc)
        self.assertEqual(hashlib.sha256(data).hexdigest(), fp)
        self.assertIn("final fingerprint: %s\n" % fp, r.stdout)
        self.assertNotIn(b"abtest-draft", data)
        self.assertNotIn(b"abtest-status", data)

    def test_failure_leaves_an_existing_out_untouched_and_says_so(self):
        r = self.run_main(example(), existing="OLD CARD")
        self.assertRefused(r)
        self.assertEqual(r.read(), b"OLD CARD")
        self.assertIn("%s already exists and was NOT updated." % r.out, r.stderr)

    def test_a_card_gate_failure_also_leaves_the_out_untouched(self):
        sc = stamped(example())
        sc["card"]["variant_b"] = sc["card"]["variant_b"].replace("Ödemeye geç", "Hemen öde")
        r = self.run_main(sc, existing="OLD CARD")
        self.assertRefused(r, "outside any ring")
        self.assertEqual(r.read(), b"OLD CARD")
        self.assertIn("was NOT updated", r.stderr)

    def test_turkish_refusal(self):
        r = self.run_main(example(), "--lang", "tr", existing="ESKİ")
        self.assertEqual(r.code, 1)
        self.assertIn("inceleme damgası eksik: review.scenario_critic", r.stderr)
        self.assertIn("“inceleme damgaları” kapısında REDDEDİLDİ; hiçbir şey yazılmadı.", r.stderr)
        self.assertIn("zaten var ve GÜNCELLENMEDİ.", r.stderr)

    def test_only_pass_is_a_stamp(self):
        sc = stamped(example())
        sc["review"]["mockup_reviewer"]["verdict"] = "FIX"
        self.assertRefused(self.run_main(sc), "review.mockup_reviewer.verdict")  # the schema refuses it first
        # The builder's own check, behind the schema:
        self.assertEqual(bc.stamp_problems(sc, "mockup_reviewer", sc["review"]["mockup_reviewer"]["fingerprint"]),
                         ["review.mockup_reviewer.verdict is 'FIX': only a PASS is ever stamped "
                          "(FIX and RET go back to mockup-reviewer)"])
        good = stamped(example())
        self.assertEqual(bc.stamp_problems(good, "mockup_reviewer", good["review"]["mockup_reviewer"]["fingerprint"]), [])

    def test_a_fingerprint_must_be_sha256_hex(self):
        sc = stamped(example())
        sc["review"]["scenario_critic"]["fingerprint"] = "abc"
        r = self.run_main(sc)
        self.assertEqual(r.code, 1)
        self.assertIn("review.scenario_critic.fingerprint", r.stderr)

    def test_missing_input_file_is_a_usage_error(self):
        out = io.StringIO()
        with contextlib.redirect_stderr(out), self.assertRaises(SystemExit) as cm:
            bc.main(["--template", TEMPLATE_PATH, "--scenario", "/nonexistent.json", "--out", "/nonexistent.html"])
        self.assertEqual(cm.exception.code, 2)


class TestDraft(RunCase):
    """Taslak: nihai kartın aynısı + görünür şerit + iki meta etiketi + manifest."""

    def draft(self, sc=None, *extra):
        sc = sc or example()
        sc = copy.deepcopy(sc)
        sc["review"] = {"scenario_critic": critic_stamp(sc)}
        return sc, self.run_main(sc, "--draft", *extra, out_name="abtest-card-kupon.draft.html")

    def test_draft_is_the_final_card_plus_banner_and_metas(self):
        sc, r = self.draft()
        self.assertEqual(r.code, 0, r.stderr)
        draft = r.read().decode("utf-8")
        final, _, _ = bc.final_html(TEMPLATE, sc)
        self.assertIn('<meta name="abtest-status" content="draft">', draft)
        self.assertNotIn("abtest-final-fingerprint", draft)  # audit M8: the draft carries no fingerprint
        self.assertIn(">TASLAK · incelenmedi</div>", draft)
        self.assertEqual(draft, bc.draft_html(final, "tr"))
        stripped = draft.replace('<meta name="abtest-status" content="draft">\n', "")
        stripped = "\n".join(line for line in stripped.split("\n") if 'id="abtest-draft"' not in line)
        self.assertEqual(stripped, final)

    def test_prints_the_paths_and_the_review_step_but_no_fingerprint(self):
        sc, r = self.draft()
        lines = r.stdout.splitlines()
        self.assertTrue(lines[0].startswith("draft: %s (" % r.out), lines)
        self.assertTrue(lines[1].startswith("manifest: %s (" % r.manifest), lines)
        self.assertTrue(lines[2].startswith("review: mockup-reviewer reviews this draft"), lines)
        self.assertIn("--stamp %s" % r.out, r.stdout)
        for value in (bc.final_fingerprint(TEMPLATE, sc), bc.mockup_stamp(TEMPLATE, sc)):
            self.assertNotIn(value, r.stdout)

    def test_english_banner(self):
        sc = example()
        sc["lang"] = "en"
        sc["objection"] = "Price"  # the record's own language (rule 7)
        _, r = self.draft(sc)
        self.assertIn(">DRAFT · not reviewed</div>".encode("utf-8"), r.read())

    def test_nothing_the_draft_writes_is_a_stamp(self):
        sc, r = self.draft()
        stamp = bc.mockup_stamp(TEMPLATE, sc)
        for path in (r.out, r.manifest):
            text = r.read(path).decode("utf-8")
            self.assertNotIn(stamp, text)
            self.assertNotIn(bc.final_fingerprint(TEMPLATE, sc), text)

    def test_manifest_document(self):
        sc, r = self.draft()
        doc = json.loads(r.read(r.manifest).decode("utf-8"))
        self.assertEqual(doc["format"], "ab-test-playbook/diff-manifest")
        self.assertEqual(doc["version"], 1)
        self.assertEqual(doc["draft"], "abtest-card-kupon.draft.html")
        self.assertEqual(doc["id"], sc["id"])
        self.assertEqual(doc["difference"], "change")
        self.assertEqual(doc["mockup_basis"], "representative")
        self.assertIsNone(doc["numeric_change"])
        self.assertEqual(doc["record_fingerprint"], vsj.record_fingerprint(sc))
        self.assertNotIn("final_fingerprint", doc)
        self.assertEqual(doc["rings"], [{"ring": 1, "label": "Kupon bağlantıda / Kupon alanı açık", "variant": "A+B",
                                         "kind": "changed", "changes": len(doc["changes"])}])
        kinds = {(c["kind"], c["change"], c.get("value")) for c in doc["changes"]}
        self.assertIn(("component", "added", "r-link"), kinds)
        self.assertIn(("component", "removed", "r-field"), kinds)
        self.assertIn(("text", "removed", None), kinds)

    def test_the_stamp_the_reviewer_prints_builds_the_final(self):
        sc, r = self.draft()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = bc.main(["--template", TEMPLATE_PATH, "--scenario", r.src, "--stamp", r.out])
        self.assertEqual(code, 0, err.getvalue())
        stamp = json.loads(out.getvalue())
        self.assertEqual(stamp, {"verdict": "PASS", "fingerprint": bc.mockup_stamp(TEMPLATE, sc)})
        sc["review"]["mockup_reviewer"] = stamp
        final = self.run_main(sc)
        self.assertEqual(final.code, 0, final.stderr)
        self.assertEqual(hashlib.sha256(final.read()).hexdigest(), bc.final_fingerprint(TEMPLATE, sc))

    def test_draft_refusal_says_the_manifest_was_not_updated_either(self):
        sc = example()
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "x.draft.html")
            for path in (out, out + ".manifest.json"):
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("OLD")
            src = os.path.join(d, "s.json")
            with open(src, "w", encoding="utf-8") as fh:
                json.dump(sc, fh, ensure_ascii=False)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                code = bc.main(["--template", TEMPLATE_PATH, "--scenario", src, "--out", out, "--draft"])
            self.assertEqual(code, 1)
            self.assertIn("x.draft.html already exists and was NOT updated", err.getvalue())
            self.assertIn("x.draft.html.manifest.json already exists and was NOT updated", err.getvalue())
            with open(out + ".manifest.json", encoding="utf-8") as fh:
                self.assertEqual(fh.read(), "OLD")


class TestFingerprintIndependence(unittest.TestCase):
    """Nihai kart `review`'dan hiçbir şey çizmez: damga eklemek kartın baytlarını değiştirmez."""

    def test_final_bytes_are_identical_with_and_without_review(self):
        sc = example()
        bare, _, _ = bc.final_html(TEMPLATE, sc)
        with_review, _, _ = bc.final_html(TEMPLATE, stamped(sc))
        self.assertEqual(bare, with_review)
        odd = copy.deepcopy(sc)
        odd["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": "f" * 64}}
        self.assertEqual(bc.final_html(TEMPLATE, odd)[0], bare)

    def test_record_fingerprint_ignores_the_stamps_and_the_card(self):
        sc = example()
        fp = vsj.record_fingerprint(sc)
        self.assertEqual(vsj.record_fingerprint(stamped(sc)), fp)
        sc["card"]["note_pos"] = "below"
        self.assertEqual(vsj.record_fingerprint(sc), fp)
        self.assertNotEqual(bc.final_fingerprint(TEMPLATE, sc), bc.final_fingerprint(TEMPLATE, example()))

    def test_fingerprint_is_of_the_written_bytes(self):
        sc = example()
        html, _, _ = bc.final_html(TEMPLATE, sc)
        self.assertEqual(bc.final_fingerprint(TEMPLATE, sc), hashlib.sha256(html.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    unittest.main()
