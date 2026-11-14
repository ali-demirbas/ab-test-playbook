#!/usr/bin/env python3
"""validate_scenario_json.py aşama 3 kalite kapıları için unit testler. Bağımlılıksız.

Her yeni hata için bir olumsuz (kötü kayıt reddedilir, mesajıyla) ve bir olumlu
(düzeltilmiş kayıt geçer) test var. Kapsam, sözleşmenin "Regression tests"
listesinin kayıt tarafı: erişilebilirlik ölçütleri (5), kupon/gelir guardrail'i
(6), tümleyen guardrail ve "gören" paydası (7), arşiv kaynağı ve fazla iddia
(8), eksik invariants (9), aciliyet sinyali ve düzenleme uyarısı (10); ayrıca
kayıt parmak izi ve --fingerprint, kanıt notu, başlık/KPI ailesi uyarısı.
"""
import contextlib
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import validate_scenario_json as vsj  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
SCHEMA = vsj.load_schema()

ARCHIVE_TITLE = "Açık kupon kodu alanı sepet terkini artırır mı?"
ARCHIVE_VARIABLE = "Kupon kodu alanının görünürlüğü"  # Fark: değiştir
A11Y_TEXT = ("Bağlantı klavyeyle erişilebilir, ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt ve "
             "kontrastı en az 4.5:1 olmalı.")
REGULATION_TEXT = "B’nin metni için uyum onayı alınmadan teste trafik açılmaz."
SOURCED_REGULATION_TEXT = "Stok sayısı gerçek envanterden gelir; uyum onayı alınmadan teste trafik açılmaz."
INVARIANTS = ["Geçerli bir kod iki kolda da aynı adımla uygulanır.",
              "İndirim iki kolda da toplam tutara aynı hesapla yansır.",
              "Geçersiz ya da süresi dolmuş bir kod iki kolda da aynı hata mesajını alır."]


def coupon():
    """The corrected coupon record of the stage-3 contract, without its card."""
    return {
        "id": "cart-checkout-coupon-field-01",
        "title": "Kupon alanını “İndirim kodum var” bağlantısının arkasına almak sepetten çıkışı azaltır mı?",
        "problem": "Sepette açık duran kupon kutusu, kodu olmayan kullanıcıyı “indirim arayayım” diye siteden çıkarabilir.",
        "mechanism": "Kupon alanı bağlantının arkasına alınınca kodu olmayan kullanıcıya eksik bir indirim hatırlatılmaz.",
        "variable": ARCHIVE_VARIABLE,
        "variants": [{"id": "A", "description": "Kupon alanı sepette açık kutu olarak duruyor"},
                     {"id": "B", "description": "Kupon alanı “İndirim kodum var” bağlantısının arkasında"}],
        "difference": "change",
        "primary_kpi": {"name": "Sipariş Tamamlama Oranı",
                        "denominator": "Sepet sayfasına ulaşan ziyaretçi (iki kolda aynı tetik)", "direction": "increase"},
        "guardrail": {"name": "Kupon Kullanım Oranı", "kind": "metric", "denominator": "Tamamlanan sipariş",
                      "direction": "must_not_decrease"},
        "invariants": list(INVARIANTS),
        "warnings": [{"type": "accessibility", "text": A11Y_TEXT}],
        "source": "adapted",
        "adapted_from": ARCHIVE_TITLE,
        "evidence": {"level": "archive", "note": "Arşivde derlenmiş bir test fikrine dayanıyor, bir test sonucu değil."},
        "priority": {"tier": "medium", "rationale": "Sepetten çıkışı hedefliyor, kanıt arşiv örüntüsü ve iş küçük.",
                     "inputs": {"evidence": "archive_or_research", "main_path": True, "noticeable": True, "effort": "low"}},
        "lang": "tr",
    }


def plain(**changes):
    """A record whose change touches nothing interactive, functional or regulated: a headline's length."""
    sc = {
        "id": "product-detail-title-length-01",
        "title": "Kısa ürün başlığı sepete eklemeyi artırır mı?",
        "problem": "Uzun ürün başlığı ürünün ne olduğunu ilk bakışta saklıyor.",
        "mechanism": "Kısa başlık ürünü ilk bakışta tanıttığı için kullanıcı karara daha çabuk geçer.",
        "variable": "Ürün başlığının uzunluğu",
        "variants": [{"id": "A", "description": "Uzun başlık"}, {"id": "B", "description": "Kısa başlık"}],
        "difference": "change",
        "primary_kpi": {"name": "Sepete Ekleme Oranı", "denominator": "Ürün sayfasına ulaşan ziyaretçi",
                        "direction": "increase"},
        "guardrail": {"name": "İade Oranı (30 gün)", "kind": "metric", "denominator": "Tamamlanan sipariş",
                      "direction": "must_not_increase"},
        "source": "generated",
        "source_note": "Arşivde bu sayfanın başlık uzunluğuna uyan bir senaryo yok.",
        "evidence": {"level": "intuition"},
        "priority": {"tier": "medium", "rationale": "Ürün sayfasında karar anını hedefliyor, kanıt sezgi, iş yalnızca metin.",
                     "inputs": {"evidence": "intuition", "main_path": True, "noticeable": True, "effort": "low"}},
    }
    sc.update(changes)
    return sc


# Score inputs that land in the medium band for each evidence level (methodology.md → Prioritization).
MEDIUM_INPUTS = {
    "user_data": {"evidence": "user_data", "main_path": False, "noticeable": False, "effort": "low"},
    "sector": {"evidence": "archive_or_research", "main_path": True, "noticeable": True, "effort": "low"},
    "archive": {"evidence": "archive_or_research", "main_path": True, "noticeable": True, "effort": "low"},
    "intuition": {"evidence": "intuition", "main_path": True, "noticeable": True, "effort": "low"},
}


def with_evidence(sc, evidence):
    """The record with another evidence level and the medium-band inputs that go with it."""
    sc["evidence"] = evidence
    sc["priority"]["inputs"] = dict(MEDIUM_INPUTS[evidence["level"]])
    return sc


def with_b(sc, description):
    sc["variants"][1]["description"] = description
    return sc


def errs(sc, lang="en"):
    return vsj.validate(sc, SCHEMA, lang)


def warns(sc, lang="en"):
    return vsj.lint(sc, SCHEMA, lang)


def has(items, fragment):
    return any(fragment in x for x in items)


class TestBaselines(unittest.TestCase):
    def test_corrected_coupon_record_is_clean(self):
        self.assertEqual(errs(coupon()), [])
        self.assertEqual(warns(coupon()), [])

    def test_plain_record_is_clean(self):
        self.assertEqual(errs(plain()), [])
        self.assertEqual(warns(plain()), [])

    def test_shipped_example_is_clean(self):
        with open(EXAMPLE, encoding="utf-8") as fh:
            sc = json.load(fh)
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])


# --------------------------------------------------------------- fingerprint

class TestFingerprint(unittest.TestCase):
    def test_is_the_contract_formula(self):
        rec = coupon()
        body = json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.assertEqual(vsj.record_fingerprint(rec), hashlib.sha256(body).hexdigest())
        self.assertRegex(vsj.record_fingerprint(rec), r"^[0-9a-f]{64}$")

    def test_stable_across_key_order(self):
        def reverse(value):
            if isinstance(value, dict):
                return {k: reverse(value[k]) for k in reversed(list(value))}
            if isinstance(value, list):
                return [reverse(v) for v in value]
            return value
        rec = coupon()
        flipped = reverse(rec)
        self.assertNotEqual(list(flipped), list(rec))
        self.assertEqual(vsj.record_fingerprint(flipped), vsj.record_fingerprint(rec))

    def test_changes_when_content_changes(self):
        base = vsj.record_fingerprint(coupon())
        edits = (lambda sc: sc.__setitem__("title", sc["title"].replace("azaltır", "düşürür")),
                 lambda sc: sc["invariants"].append("Kod alanı iki kolda da aynı karakter sınırını taşır."),
                 lambda sc: sc["primary_kpi"].__setitem__("denominator", "Teste atanan ziyaretçi"),
                 lambda sc: sc["variants"].reverse())
        for edit in edits:
            sc = coupon()
            edit(sc)
            self.assertNotEqual(vsj.record_fingerprint(sc), base)

    def test_ignores_review_and_card(self):
        base = vsj.record_fingerprint(coupon())
        sc = coupon()
        sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": base}}
        sc["card"] = {"difference": "change", "variant_a": '<div class="r-h">A</div>', "variant_b": '<div class="r-h">B</div>'}
        self.assertEqual(vsj.record_fingerprint(sc), base)
        sc["card"]["variant_b"] = '<div class="r-h">B2</div>'
        self.assertEqual(vsj.record_fingerprint(sc), base)
        self.assertIn("review", sc)  # the record itself is left untouched

    def run_cli(self, doc, *flags, raw=None):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.json")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(raw if raw is not None else json.dumps(doc, ensure_ascii=False))
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = vsj.main(list(flags) + ["--fingerprint", path])
            return code, out.getvalue(), err.getvalue()

    def test_cli_prints_only_the_hex(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = vsj.main(["--fingerprint", EXAMPLE])
        self.assertEqual(code, 0)
        with open(EXAMPLE, encoding="utf-8") as fh:
            self.assertEqual(out.getvalue(), vsj.record_fingerprint(json.load(fh)) + "\n")

    def test_cli_refuses_a_record_with_errors(self):
        sc = coupon()
        del sc["invariants"]
        code, out, err = self.run_cli(sc, "--lang", "en")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("no fingerprint printed, fix the record first", err)
        self.assertIn("invariants: the change touches a functional element", err)
        code, out, err = self.run_cli(sc)
        self.assertIn("parmak izi yazılmadı", err)

    def test_cli_strict_counts_warnings(self):
        sc = coupon()
        sc["title"] = sc["title"].rstrip("?")
        code, out, err = self.run_cli(sc, "--lang", "en")
        self.assertEqual(code, 0, err)
        self.assertEqual(out, vsj.record_fingerprint(sc) + "\n")
        self.assertIn("does not end with '?'", err)  # the warning still reaches the reader, on stderr
        code, out, err = self.run_cli(sc, "--lang", "en", "--strict")
        self.assertEqual(code, 1)
        self.assertEqual(out, "")

    def test_cli_invalid_json(self):
        code, out, err = self.run_cli(None, "--lang", "en", raw="{not json")
        self.assertEqual((code, out), (1, ""))
        self.assertIn("INVALID JSON", err)

    def test_cli_takes_exactly_one_file(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            vsj.main(["--fingerprint", EXAMPLE, EXAMPLE])
        self.assertEqual(caught.exception.code, 2)


# ------------------------------------------------------------ schema fields

class TestNewSchemaFields(unittest.TestCase):
    STAMP = {"verdict": "PASS", "fingerprint": "a" * 64}

    def test_invariants_shape(self):
        for n in (1, 5):
            self.assertEqual(errs(coupon() | {"invariants": INVARIANTS[:1] * n}), [], n)
        self.assertTrue(has(errs(coupon() | {"invariants": []}), "invariants: has 0 item(s), minimum is 1"))
        self.assertTrue(has(errs(coupon() | {"invariants": INVARIANTS * 2}), "invariants: has 6 item(s), maximum is 5"))
        self.assertTrue(has(errs(coupon() | {"invariants": [3]}), "invariants[0]: expected type string"))
        self.assertTrue(has(errs(coupon() | {"invariants": [""]}), "invariants[0]: shorter than minLength 1"))

    def test_numeric_change_shape(self):
        # Fix round 2: numeric_change also says where the figure comes from (tests/test_v5_validator.py).
        self.assertEqual(errs(plain(numeric_change="Fiyat testinde B, kullanıcının verdiği yeni fiyatı gösterir.")), [])
        self.assertTrue(has(errs(plain(numeric_change="")), "numeric_change: shorter than minLength 1"))
        self.assertTrue(has(errs(plain(numeric_change=5)), "numeric_change: expected type string"))

    def test_review_stamps(self):
        self.assertEqual(errs(plain(review={"scenario_critic": self.STAMP})), [])
        self.assertEqual(errs(plain(review={"scenario_critic": self.STAMP, "mockup_reviewer": self.STAMP})), [])

    def test_only_pass_is_stamped(self):
        for verdict in ("FIX", "RET", "pass"):
            e = errs(plain(review={"scenario_critic": dict(self.STAMP, verdict=verdict)}))
            self.assertTrue(has(e, "review.scenario_critic.verdict: %r is not one of ['PASS']" % verdict), e)

    def test_fingerprint_is_64_lowercase_hex(self):
        for bad in ("A" * 64, "a" * 63, "a" * 65, "g" * 64, ""):
            e = errs(plain(review={"mockup_reviewer": dict(self.STAMP, fingerprint=bad)}))
            self.assertTrue(has(e, "review.mockup_reviewer.fingerprint:"), (bad, e))

    def test_stamp_fields_are_closed(self):
        e = errs(plain(review={"scenario_critic": {"verdict": "PASS"}}))
        self.assertTrue(has(e, "review.scenario_critic: missing required field 'fingerprint'"), e)
        e = errs(plain(review={"scenario_critic": dict(self.STAMP, note="ok")}))
        self.assertTrue(has(e, "review.scenario_critic: unknown field 'note'"), e)
        e = errs(plain(review={"copy_reviewer": self.STAMP}))
        self.assertTrue(has(e, "review: unknown field 'copy_reviewer'"), e)


# ----------------------------------------------- 5. accessibility (record side)

class TestAccessibility(unittest.TestCase):
    def link_record(self, warning=None):
        sc = with_b(plain(), "Başlığın altında “Tüm özellikler” bağlantısı")
        sc["invariants"] = ["Başlık iki kolda da aynı ürünü adlandırır."]
        if warning is not None:
            sc["warnings"] = [{"type": "accessibility", "text": warning}]
        return sc

    def test_b_adds_a_link_without_an_accessibility_warning(self):
        e = errs(self.link_record())
        self.assertTrue(has(e, "warnings: the change touches an interactive element ('bağlantısı'); add a warning of "
                               "type 'accessibility' that states its pass/fail criteria: touch target (at least "
                               "44×44 pt / 48×48 dp), text contrast (at least 4.5:1), keyboard access, a name screen readers "
                               "announce (rule 3)"), e)
        self.assertTrue(has(errs(self.link_record(), "tr"), "'accessibility' türünde bir uyarı ekleyin"))

    def test_another_warning_type_does_not_count(self):
        sc = self.link_record()
        sc["warnings"] = [{"type": "feasibility", "text": A11Y_TEXT}]
        self.assertTrue(has(errs(sc), "add a warning of type 'accessibility'"), errs(sc))

    def test_complete_criteria_pass(self):
        self.assertEqual(errs(self.link_record(A11Y_TEXT)), [])

    def test_missing_keyboard_is_named(self):
        e = errs(self.link_record("Bağlantı ekran okuyucuda adıyla okunur, dokunma alanı en az 44×44 pt ve kontrastı en "
                                  "az 4.5:1 olmalı."))
        self.assertIn("warnings: the accessibility warning does not state: keyboard access (for 'bağlantısı'); write "
                      "each as a pass/fail criterion (rule 3)", e)
        tr = errs(self.link_record("Bağlantı ekran okuyucuda okunur, 44×44 pt ve 4.5:1 olmalı."), "tr")
        self.assertTrue(has(tr, "erişilebilirlik uyarısında şu ölçüt(ler) yok: klavyeyle erişim"), tr)

    def test_every_base_criterion_is_required(self):
        parts = {"touch target": "dokunma alanı en az 44×44 pt", "text contrast": "kontrastı en az 4.5:1",
                 "keyboard access": "klavyeyle erişilebilir", "a name screen readers announce": "ekran okuyucuda okunur"}
        for label in parts:
            text = "Bağlantı " + ", ".join(v for k, v in parts.items() if k != label) + " olmalı."
            e = errs(self.link_record(text))
            self.assertTrue(has(e, "does not state: " + label), (label, e))

    def test_thresholds_count(self):
        # Fix round 2: a bare "dokunma alanı" / "contrast" no longer states the criterion; the figures do
        # (bare words and lower figures: tests/test_v5_validator.py → TestAccessibilityThresholds).
        for text in ("The link has a 44×44 pt touch area, 4,5:1 contrast, works by keyboard and has a screen-reader name.",
                     "Bağlantı 48×48 dp, kontrast 4.5:1, klavye ve ekran okuyucu ile kullanılabilir olmalı."):
            self.assertEqual(errs(self.link_record(text)), [], text)

    def test_modal_needs_focus_and_closing(self):
        sc = with_b(plain(), "Sepete ekleyince açılır pencere çıkar")
        sc["invariants"] = ["Ürün iki kolda da sepete aynı adımla eklenir."]
        sc["exposure"] = "Sepete ekle dokunuşunda, iki kolda aynı noktada kaydedilir."
        sc["warnings"] = [{"type": "accessibility", "text": A11Y_TEXT}]
        e = errs(sc)
        self.assertTrue(has(e, "does not state: taking focus when it opens, a visible close control, closing with Esc"), e)
        # A visible close control alone isn't enough: rule 3 asks for the control AND Esc.
        sc["warnings"][0]["text"] = A11Y_TEXT[:-1] + ", açılınca odağı alır ve görünür kapat düğmesiyle kapanır."
        self.assertTrue(has(errs(sc), "closing with Esc"), errs(sc))
        sc["warnings"][0]["text"] = A11Y_TEXT[:-1] + ", açılınca odağı alır ve görünür bir düğme ile Esc tuşuyla kapanır."
        self.assertEqual(errs(sc), [])

    def test_a_bottom_sheet_or_dialog_is_a_modal(self):
        for words in ("bir alt sayfa", "bir diyalog", "a bottom sheet"):
            sc = with_b(plain(), "Başlığın altında %s açılır" % words)
            sc["invariants"] = ["Başlık iki kolda da aynı ürünü adlandırır."]
            sc["warnings"] = [{"type": "accessibility", "text": A11Y_TEXT}]
            self.assertTrue(has(errs(sc), "closing with Esc"), (words, errs(sc)))

    def test_overlay_and_popup_are_modals(self):
        for words in ("bir overlay", "bir pop-up", "bir modal"):
            sc = with_b(plain(), "Başlığın üstünde %s açılır" % words)
            sc["invariants"] = ["Başlık iki kolda da aynı ürünü adlandırır."]
            sc["warnings"] = [{"type": "accessibility", "text": A11Y_TEXT}]
            self.assertTrue(has(errs(sc), "taking focus when it opens"), (words, errs(sc)))

    def test_auto_advancing_carousel_needs_pause(self):
        sc = with_b(plain(), "Ürün görselleri otomatik dönen bir karuselde")
        sc["invariants"] = ["Görseller iki kolda da aynı sırayla gösterilir."]
        sc["warnings"] = [{"type": "accessibility", "text": A11Y_TEXT}]
        self.assertTrue(has(errs(sc), "does not state: a way to pause it"), errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "durdurulabilmesi"), errs(sc, "tr"))
        sc["warnings"][0]["text"] = A11Y_TEXT[:-1] + " ve karusel durdurulabilmeli."
        self.assertEqual(errs(sc), [])

    def test_a_carousel_the_user_moves_needs_no_pause(self):
        sc = with_b(plain(), "Ürün görselleri kaydırılan bir karuselde")
        sc["invariants"] = ["Görseller iki kolda da aynı sırayla gösterilir."]
        sc["warnings"] = [{"type": "accessibility", "text": A11Y_TEXT}]
        self.assertEqual(errs(sc), [])

    def test_attention_is_not_keyboard_focus(self):
        self.assertEqual(errs(plain(mechanism="Kısa başlıkta kullanıcı fiyata odaklanır.")), [])
        self.assertEqual(errs(plain(mechanism="Users focus on the price when the title is short.")), [])

    def test_keywords_match_at_word_starts_only(self):
        # "tab" is not "tablonun", "alan" is not "Kalan".
        self.assertEqual(errs(with_b(plain(), "Kalan tutar tablonun altında")), [])

    def test_only_the_change_is_read(self):
        # The problem may name the page's link; it is the change that has to be accessible.
        self.assertEqual(errs(plain(problem="Uzun başlık, altındaki bağlantıyı ekranın dışına itiyor.")), [])


# ------------------------------------------------------------- 9. invariants

class TestInvariants(unittest.TestCase):
    def test_functional_change_without_invariants(self):
        sc = plain(variable="Sepet özetinin konumu", difference="move",
                   variants=[{"id": "A", "description": "Özet altta"}, {"id": "B", "description": "Özet üstte"}])
        e = errs(sc)
        self.assertIn("invariants: the change touches a functional element ('Sepet'); list the functions that must "
                      "work identically in both arms (1-5 sentences), e.g. \"A valid code applies in the same step in "
                      "both arms.\" (rule 4)", e)
        self.assertTrue(has(errs(sc, "tr"), "invariants: değişiklik işlevsel bir öğeye dokunuyor ('Sepet')"))
        sc["invariants"] = ["Sepet tutarı iki kolda da aynı hesaplanır."]
        self.assertEqual(errs(sc), [])

    def test_every_functional_keyword_is_read(self):
        for word in vsj.FUNCTIONAL_TR + vsj.FUNCTIONAL_EN:
            sc = plain(mechanism="B’de %s adımı sadeleşir." % word)
            self.assertTrue(has(errs(sc), "invariants: the change touches a functional element"), (word, errs(sc)))

    def test_an_interactive_change_needs_them_too(self):
        sc = with_b(plain(), "Başlığın yanında bir buton")
        sc["warnings"] = [{"type": "accessibility", "text": A11Y_TEXT}]
        self.assertTrue(has(errs(sc), "invariants: the change touches a functional element ('buton')"), errs(sc))
        sc["invariants"] = ["Başlık iki kolda da aynı ürünü adlandırır."]
        self.assertEqual(errs(sc), [])

    def test_a_copy_change_needs_none(self):
        self.assertNotIn("invariants", plain())
        self.assertEqual(errs(plain()), [])

    def test_the_corrected_coupon_record_carries_three(self):
        sc = coupon()
        self.assertEqual(len(sc["invariants"]), 3)
        del sc["invariants"]
        self.assertTrue(has(errs(sc), "invariants:"), errs(sc))


# ------------------------------------------------ 6. revenue and a user benefit

class TestRevenueBenefitGuardrail(unittest.TestCase):
    RPV = {"name": "Ziyaretçi Başına Gelir (RPV)", "denominator": "Teste atanan ziyaretçi", "direction": "increase"}
    RETURNS = {"name": "İade Oranı (30 gün)", "kind": "metric", "denominator": "Tamamlanan sipariş",
               "direction": "must_not_increase"}

    def test_coupon_change_with_revenue_primary_and_no_coupon_guardrail(self):
        sc = coupon()
        sc.update(primary_kpi=dict(self.RPV), guardrail=dict(self.RETURNS))
        e = errs(sc)
        self.assertIn("guardrail: the primary KPI is a revenue metric ('Ziyaretçi Başına Gelir (RPV)') and the change "
                      "touches a user benefit ('Kupon'); the guardrail must watch that benefit (e.g. \"Coupon-Order "
                      "Visitor Rate\" must not drop), or the lost benefit reads as a revenue win (rule 3)", e)
        self.assertTrue(has(errs(sc, "tr"), "guardrail o faydayı ölçmeli"), errs(sc, "tr"))

    def test_a_coupon_guardrail_answers_it(self):
        sc = coupon()
        sc["primary_kpi"] = dict(self.RPV)
        self.assertFalse(has(errs(sc), "user benefit"), errs(sc))
        self.assertEqual(errs(sc), [])

    def test_the_corrected_record_decides_on_completion(self):
        # Revenue isn't the primary: hiding the field could raise revenue by making code holders pay full price.
        sc = coupon()
        sc["guardrail"] = dict(self.RETURNS)
        self.assertFalse(has(errs(sc), "user benefit"), errs(sc))

    def test_benefit_families_are_matched_not_words(self):
        # A shown discount or campaign is at risk only when B hides, removes or shrinks it.
        sc = plain(variable="Kampanya rozetinin görünürlüğü", primary_kpi=dict(self.RPV),
                   invariants=["Fiyat iki kolda aynıdır."])
        sc = with_b(sc, "“Sepette indirim” rozeti kaldırılır")
        self.assertTrue(has(errs(sc), "touches a user benefit ('Kampanya')"), errs(sc))
        sc["guardrail"] = {"name": "Kupon Kullanım Oranı", "kind": "metric", "denominator": "Tamamlanan sipariş",
                           "direction": "must_not_decrease"}
        self.assertEqual(errs(sc), [])

    def test_a_discount_shown_more_is_not_a_lost_benefit(self):
        # The page's own label “Yıllık (%20 indirim)” made the default: B shows the discount more, hides nothing.
        sc = plain(variable="Fiyat anahtarının varsayılanı", primary_kpi=dict(self.RPV),
                   mechanism="Yıllık (%20 indirim) seçeneği varsayılan olunca kullanıcı indirimi ilk bakışta görür.",
                   invariants=["Fiyatlar ve indirim oranı iki kolda aynıdır."],
                   numeric_change="B'de yıllık fiyat varsayılan olduğu için aylık karşılık gösterilir.")
        sc = with_b(sc, "Anahtar varsayılan olarak Yıllık (%20 indirim) konumunda")
        self.assertFalse(has(errs(sc), "user benefit"), errs(sc))
        sc = with_b(sc, "Yıllık (%20 indirim) seçeneği bir bağlantının arkasına alınır")
        self.assertTrue(has(errs(sc), "user benefit"), errs(sc))

    def test_every_benefit_family(self):
        for word, guardrail in (("ücretsiz kargo", "Ücretsiz Kargo Kullanım Oranı"), ("iade", "İade Talep Oranı"),
                                ("iptal", "İptal Oranı"), ("free shipping", "Free Shipping Usage Rate"),
                                ("refund", "Refund Request Rate"), ("cancel", "Cancellation Rate"),
                                ("voucher", "Coupon Usage Rate")):
            sc = plain(mechanism="B’de %s koşulu bir bağlantının arkasına alındığı için kullanıcı karar verir." % word,
                       primary_kpi=dict(self.RPV),
                       guardrail={"name": "Destek Talebi Oranı", "kind": "metric", "denominator": "Tamamlanan sipariş",
                                  "direction": "must_not_increase"})
            self.assertTrue(has(errs(sc), "touches a user benefit"), (word, errs(sc)))
            sc["guardrail"] = {"name": guardrail, "kind": "metric", "denominator": "Tamamlanan sipariş",
                               "direction": "must_not_increase"}
            self.assertFalse(has(errs(sc), "user benefit"), (word, errs(sc)))

    def test_a_benefit_shown_more_needs_no_benefit_guardrail(self):
        # A free-shipping progress bar promotes the benefit; only a code field is at risk whatever B does.
        for word in ("ücretsiz kargo", "iade", "iptal", "free shipping", "refund", "cancel"):
            sc = plain(mechanism="B’de %s koşulu görünür olduğu için kullanıcı karar verir." % word,
                       primary_kpi=dict(self.RPV),
                       guardrail={"name": "Destek Talebi Oranı", "kind": "metric", "denominator": "Tamamlanan sipariş",
                                  "direction": "must_not_increase"})
            self.assertFalse(has(errs(sc), "user benefit"), (word, errs(sc)))
        sc = plain(mechanism="B’de voucher koşulu görünür olduğu için kullanıcı karar verir.", primary_kpi=dict(self.RPV))
        self.assertTrue(has(errs(sc), "user benefit"), errs(sc))

    def test_an_unchanged_button_named_in_a_is_not_the_change(self):
        sc = plain()
        sc["variants"][0]["description"] = "Uzun başlık; altında Sepete ekle butonu"
        self.assertEqual(errs(sc), [])

    def test_win_chance_and_uplift_wording_is_refused(self):
        for text in ("Kazanma olasılığı %70.", "Dönüşüm %12 artar.", "Sipariş yüzde 12 daha fazla olur.",
                     "Olasılığı %70 olan bir kazanç.", "A 12% increase in orders.", "A high chance of winning."):
            sc = plain(problem="Uzun ürün başlığı ürünü saklıyor. " + text)
            self.assertTrue(has(errs(sc), "claims a result"), (text, errs(sc)))
        sc = plain(mechanism="Yıllık (%20 indirim) seçeneği görünür olduğu için kullanıcı indirimi fark eder.")
        self.assertFalse(has(errs(sc), "claims a result"), errs(sc))

    def test_a_check_guardrail_counts_by_its_criterion(self):
        sc = coupon()
        sc["primary_kpi"] = dict(self.RPV)
        sc["guardrail"] = {"name": "Fayda Kontrolü", "kind": "check",
                           "criterion": "Geçmeli: kupon kodu iki kolda da aynı adımla uygulanır."}
        self.assertEqual(errs(sc), [])

    def test_every_revenue_family(self):
        for name in ("Ziyaretçi Başına Gelir (RPV)", "Ortalama Sepet Tutarı (AOV)", "Sipariş Tutarı", "Brüt Marj",
                     "Revenue per Visitor", "Gross Margin", "Gelir"):
            sc = coupon()
            sc.update(primary_kpi=dict(self.RPV, name=name), guardrail=dict(self.RETURNS))
            self.assertTrue(has(errs(sc), "touches a user benefit"), (name, errs(sc)))


# --------------------------------------- 7. complement and population denominators

class TestDenominatorsAndComplement(unittest.TestCase):
    def test_complement_guardrail_is_refused(self):
        sc = coupon()
        sc["guardrail"] = {"name": "Sepet Terk Oranı", "kind": "metric",
                           "denominator": "Sepet sayfasına ulaşan ziyaretçi (iki kolda aynı tetik)",
                           "direction": "must_not_increase"}
        self.assertTrue(has(errs(sc), "guardrail: guardrail 'Sepet Terk Oranı' looks like the complement"), errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "tümleyeni gibi görünüyor"), errs(sc, "tr"))
        self.assertEqual(errs(coupon()), [])

    def test_saw_it_denominator_is_refused(self):
        sc = coupon()
        sc["primary_kpi"]["denominator"] = "“İndirim kodum var” bağlantısını gören ziyaretçi"
        self.assertTrue(has(errs(sc), "is a \"users who saw it\" population"), errs(sc))

    def test_b_only_denominator_is_refused(self):
        for den in ("Yalnızca B’de bağlantıya dokunan ziyaretçi", "Sadece B kolundaki ziyaretçi", "Visitors in B only"):
            sc = coupon()
            sc["primary_kpi"]["denominator"] = den
            self.assertIn("primary_kpi.denominator: %r is a population that exists only in B; the denominator is the "
                          "same in both arms (methodology → KPI denominator)" % den, errs(sc))
        sc = coupon()
        sc["guardrail"]["denominator"] = "Yalnız B’de tamamlanan sipariş"
        self.assertTrue(has(errs(sc), "guardrail.denominator:"), errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "yalnızca B’de var olan bir kitle"), errs(sc, "tr"))

    def test_a_population_both_arms_have_passes(self):
        for den in ("Sepet sayfasına ulaşan ziyaretçi", "Teste atanan ziyaretçi (atama sepet sayfasına ulaşınca)",
                    "Bütçe sayfasına ulaşan ziyaretçi"):
            sc = coupon()
            sc["primary_kpi"]["denominator"] = den
            self.assertEqual(errs(sc), [], den)


# ------------------------------------------------ 8. archive source and claims

class TestArchiveSource(unittest.TestCase):
    def test_archive_is_read_as_titles_and_variable_lines(self):
        archive = vsj.load_archive()
        self.assertEqual(archive[ARCHIVE_TITLE], (ARCHIVE_VARIABLE, "değiştir"))
        titles = 0
        for name in os.listdir(vsj.ARCHIVE_DIR):
            if name.endswith(".md"):
                with open(os.path.join(vsj.ARCHIVE_DIR, name), encoding="utf-8") as fh:
                    titles += sum(line.startswith("## ") for line in fh)
        self.assertEqual(len(archive), titles)
        self.assertTrue(all(fark in ("değiştir", "ekle", "taşı", "kaldır") for _, fark in archive.values()))

    def test_adapted_from_must_be_an_archive_title(self):
        sc = coupon()
        sc["adapted_from"] = "Açık kupon alanı sepet terkini artırır mı?"
        e = errs(sc)
        self.assertIn("adapted_from: 'Açık kupon alanı sepet terkini artırır mı?' is not an archive scenario title; "
                      "copy it exactly from a \"## …\" line in knowledge/scenarios/*.md (closest: %r) (rule 8)"
                      % ARCHIVE_TITLE, e)
        self.assertTrue(has(errs(sc, "tr"), "arşivde bir senaryo başlığı değil"), errs(sc, "tr"))
        sc["adapted_from"] = "Kupon kutusu görünürlüğü"
        self.assertTrue(has(errs(sc), "is not an archive scenario title"), errs(sc))

    def test_title_matches_after_whitespace_only(self):
        sc = coupon()
        sc["adapted_from"] = "  Açık  kupon kodu alanı\nsepet terkini artırır mı? "
        self.assertEqual(errs(sc), [])
        sc["adapted_from"] = ARCHIVE_TITLE.lower()
        self.assertTrue(has(errs(sc), "is not an archive scenario title"), errs(sc))

    def test_archive_source_keeps_the_archive_fark(self):
        sc = coupon()
        sc.update(source="archive", difference="add")
        self.assertIn("difference: a record with source 'archive' keeps the archive's Fark: 'change' (Fark: "
                      "değiştir), got 'add' (rule 8)", errs(sc))
        del sc["difference"]
        self.assertTrue(has(errs(sc), "keeps the archive's Fark: 'change' (Fark: değiştir), got none"), errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "fark arşivdeki Fark ile aynıdır"), errs(sc, "tr"))
        sc["difference"] = "change"
        self.assertEqual(errs(sc), [])

    def test_adapted_source_keeps_the_archive_fark_too(self):
        sc = coupon()
        sc["difference"] = "remove"
        self.assertTrue(has(errs(sc), "source 'adapted' keeps the archive's Fark: 'change'"), errs(sc))
        self.assertEqual(errs(coupon()), [])

    def test_archive_source_keeps_the_archive_variable(self):
        sc = coupon()
        sc.update(source="archive", variable="Kupon alanının görünürlüğü")
        self.assertIn("variable: a record with source 'archive' keeps the archive's Değişken: %r, got "
                      "'Kupon alanının görünürlüğü'; a different variable makes it 'adapted' or 'generated' (rule 8)"
                      % ARCHIVE_VARIABLE, errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "değişken arşivdeki Değişken ile aynıdır"), errs(sc, "tr"))
        for same in (ARCHIVE_VARIABLE, " kupon  KODU alanının görünürlüğü", "KUPON KODU ALANININ GÖRÜNÜRLÜĞÜ"):
            sc["variable"] = same
            self.assertEqual(errs(sc), [], same)

    def test_adapted_source_may_fit_the_variable(self):
        sc = coupon()
        sc["variable"] = "İndirim kodu alanının görünürlüğü"
        self.assertEqual(errs(sc), [])

    def test_english_record_variable_is_left_to_the_critic(self):
        sc = coupon()
        sc.update(source="archive", lang="en", variable="Coupon code field visibility")
        self.assertFalse(has(errs(sc), "variable:"), errs(sc))
        sc["difference"] = "add"
        self.assertTrue(has(errs(sc), "keeps the archive's Fark"), errs(sc))

    def test_missing_archive_cannot_verify_the_source(self):
        with tempfile.TemporaryDirectory() as empty, mock.patch.object(vsj, "ARCHIVE_DIR", empty):
            for source in ("archive", "adapted"):
                sc = coupon()
                sc["source"] = source
                self.assertIn("adapted_from: the archive was not found (%s); a '%s' source cannot be verified (rule 8)"
                              % (empty, source), errs(sc))
            self.assertTrue(has(errs(coupon(), "tr"), "kaynağı doğrulanamaz"))
            self.assertEqual(errs(plain()), [])  # a generated record names no archive

    def test_intuition_is_never_high(self):
        sc = plain()
        sc["priority"]["tier"] = "high"
        self.assertIn("priority.tier: an 'intuition' record cannot be priority 'high'; an idea resting on intuition is "
                      "'medium' at most (rules 9, 10)", errs(sc))
        self.assertTrue(has(errs(sc, "tr"), "kanıt 'intuition' iken öncelik 'high' olamaz"), errs(sc, "tr"))
        sc["priority"]["tier"] = "medium"
        self.assertEqual(errs(sc), [])
        # An archive pattern alone never scores high (1+1+1+2 = 5/7); the user's own data can.
        sc = coupon()
        sc["priority"]["tier"] = "high"
        self.assertTrue(has(errs(sc), "doesn't match the inputs' score: 1+1+1+2 = 5/7"), errs(sc))
        sc["evidence"] = {"level": "user_data", "note": "GA4 raporuna göre sepette kupon kutusunda çıkış yoğun."}
        sc["priority"]["inputs"]["evidence"] = "user_data"
        self.assertEqual(errs(sc), [])


class TestClaims(unittest.TestCase):
    def test_archive_presented_as_tested_and_won(self):
        for path in ("mechanism", "problem", "title"):
            sc = coupon()
            sc[path] = "Bu senaryo test edildi ve kazandı, alan bağlantının arkasına alınınca çıkış azalır?"
            e = errs(sc)
            self.assertIn("%s: 'test edildi' claims a result; without 'user_data' evidence a scenario is never presented "
                          "as tested, proven or a win, and no chance of winning or uplift percentage is written "
                          "(rules 8, 10)" % path, e)
        self.assertTrue(has(errs(sc, "tr"), "'test edildi' bir sonuç iddiası"), errs(sc, "tr"))

    def test_the_evidence_note_and_rationale_are_read(self):
        sc = coupon()
        sc["evidence"]["note"] = "Arşivde kanıtlanmış bir örüntü."
        sc["priority"]["rationale"] = "Arşivde kazandığı için öncelikli, iş küçük."
        e = errs(sc)
        self.assertTrue(has(e, "evidence.note: 'kanıtlanmış' claims a result"), e)
        self.assertTrue(has(e, "priority.rationale: 'kazandığı' claims a result"), e)

    def test_every_overclaim_word(self):
        for phrase in ("kanıtlanmış", "kanıtlandı", "test edilmiş", "test edildi", "kazanmış", "kazandı",
                       "işe yaradığı biliniyor", "proven", "tested", "known to work", "won"):
            sc = coupon()
            sc["mechanism"] = "Alan bağlantının arkasında (%s) olduğunda çıkış azalır." % phrase
            self.assertTrue(has(errs(sc), "mechanism: %r claims a result" % phrase), (phrase, errs(sc)))

    def test_uplift_and_probability_claims(self):
        for phrase in ("%10 artış", "%80 ihtimalle", "yüzde 15 artış", "%12’lik artış", "10% lift", "20% more",
                       "likely to win", "büyük ihtimalle kazanır"):
            sc = coupon()
            sc["priority"]["rationale"] = "Sepetten çıkışı hedefliyor, %s bekleniyor, iş küçük." % phrase
            self.assertTrue(has(errs(sc), "priority.rationale:") and has(errs(sc), "claims a result"),
                            (phrase, errs(sc)))

    def test_users_own_data_may_report_its_result(self):
        sc = with_evidence(coupon(), {"level": "user_data",
                                      "note": "Geçen ay bu sayfada test edildi ve kazandı, %12 artış görüldü."})
        self.assertEqual(errs(sc), [])

    def test_a_guarantee_is_never_written(self):
        for text in ("Bu değişiklik siparişi garanti eder.", "Kazanç garantidir.", "The uplift is guaranteed.",
                     "This change guarantees more orders."):
            for level in ("user_data", "archive"):
                sc = coupon()
                sc["evidence"] = {"level": level, "note": "Kendi verimiz."}
                sc["mechanism"] = text
                e = errs(sc)
                self.assertTrue(has(e, "mechanism:") and has(e, "is never written, whatever the evidence; no test "
                                                                "result can be guaranteed (rule 10)"), (text, level, e))
        self.assertTrue(has(errs(sc, "tr"), "hiçbir kanıtla yazılmaz"), errs(sc, "tr"))

    def test_negations_and_warranties_are_not_claims(self):
        for text in ("Bu sayfada test edilmedi.", "Etkisi kanıtlanmadı.", "Etkisi kanıtlanmış değil.",
                     "It was not tested on this page.", "It has never been tested here.", "Users won’t search for a code.",
                     "Kısa form kullanıcıya zaman kazandırır.", "Results are not guaranteed.",
                     "İade garantisi ve garantili teslimat bilgisi görünür."):
            sc = coupon()
            sc["evidence"]["note"] = text
            self.assertEqual(errs(sc), [], text)

    def test_the_corrected_note_is_honest(self):
        self.assertEqual(coupon()["evidence"]["note"], "Arşivde derlenmiş bir test fikrine dayanıyor, bir test sonucu değil.")
        self.assertEqual(errs(coupon()), [])


class TestNoStatisticsInTheRecord(unittest.TestCase):
    """Rule 5: statistics are out of scope, so no record field states one (stage-5 audit escape)."""

    def test_statistics_language_in_any_record_field_is_refused(self):
        cases = (
            (dict(priority={"tier": "medium", "rationale": "ICE puanı 7 (6×5×8), iş küçük."}), "priority.rationale"),
            (dict(evidence={"level": "intuition", "note": "p değeri 0,03 çıkarsa yayına alınır."}), "evidence.note"),
            (dict(warnings=[{"type": "feasibility", "text": "Örneklem büyüklüğü kol başına 12 bin olmalı."}]),
             "warnings[0].text"),
            (dict(mechanism="MDE %5 ile kısa başlık karar anını hızlandırır."), "mechanism"),
            (dict(invariants=["Önce bir A/A testiyle araç doğrulanır."]), "invariants[0]"),
            (dict(problem="Uzun başlık istatistiksel olarak anlamlı bir kayıp yaratıyor."), "problem"),
        )
        for change, path in cases:
            sc = plain(**change)
            self.assertTrue(has(errs(sc), "%s: " % path) and has(errs(sc), "statistics language"), (path, errs(sc)))
            self.assertTrue(has(errs(sc, "tr"), "istatistik dili"), path)

    def test_plain_words_and_the_detail_view_pass(self):
        sc = plain(mechanism="Kısa başlık ürünü ilk bakışta tanıttığı için kullanıcı karara daha çabuk geçer.")
        self.assertEqual(errs(sc), [])
        sc = coupon()
        sc["detail"] = {
            "test_items": [{"label": "Kaçak", "text": "Bağlantı sepetten çıkışı anlamlı azaltıyor mu?"},
                           {"label": "Segment", "text": "Mobil ve masaüstünde etki farklı mı?"},
                           {"label": "Kampanya", "text": "Kampanya döneminde etki tersine dönüyor mu?"}],
            "kpis": [{"name": "Dönüşüm Oranı (CR)", "role": "primary", "question": "Sipariş anlamlı artıyor mu?"},
                     {"name": "Kupon Kullanım Oranı", "role": "guardrail", "question": "Kullanım çökmemeli."},
                     {"name": "Sepet Terk Oranı", "role": "secondary", "question": "Terk azalıyor mu?"}],
            "dont_items": ["Kupon alanını tamamen kaldırmayın.", "Hata mesajını değiştirmeyin.",
                           "Aynı testte metni değiştirmeyin."]}
        self.assertFalse(has(errs(sc), "statistics language"), errs(sc))


class TestObjectionLanguage(unittest.TestCase):
    def test_an_english_objection_in_a_turkish_record_is_refused(self):
        sc = plain(objection="Price")
        self.assertTrue(has(errs(sc), "objection: 'Price' isn't in the record's language (tr); write 'Fiyat'"), errs(sc))
        sc["objection"] = "Fiyat"
        self.assertEqual(errs(sc), [])

    def test_a_turkish_objection_in_an_english_record_is_refused(self):
        sc = plain(objection="Çaba", lang="en")
        self.assertTrue(has(errs(sc), "write 'Effort'"), errs(sc))


class TestEvidenceNote(unittest.TestCase):
    def test_user_data_and_sector_say_what_they_rest_on(self):
        for level in ("user_data", "sector"):
            for evidence in ({"level": level}, {"level": level, "note": "  "}):
                e = errs(with_evidence(plain(), evidence))
                self.assertIn("evidence.note: '%s' evidence says what it rests on (which data, which industry "
                              "observation) (rule 10)" % level, e)
            self.assertTrue(has(errs(with_evidence(plain(), {"level": level}), "tr"), "neye dayandığı yazılır"))
            self.assertEqual(errs(with_evidence(plain(), {"level": level,
                                                          "note": "Benzer ürün sayfalarında sık görülür."})), [])

    def test_archive_and_intuition_need_no_note(self):
        self.assertEqual(errs(plain(evidence={"level": "intuition"})), [])
        sc = coupon()
        del sc["evidence"]["note"]
        self.assertEqual(errs(sc), [])


# ------------------------------------------- 10. regulation and urgency (record side)

class TestRegulationAndUrgency(unittest.TestCase):
    def urgent(self, description="Başlığın altında “Son 3 ürün kaldı” uyarısı"):
        return with_b(plain(), description)

    def test_regulated_record_is_refused_without_its_warning(self):
        sc = plain(stage="credit-application", problem="Kredi başvurusunda ürün başlığı uzun.")
        self.assertTrue(has(errs(sc), "the record looks like a regulated flow"), errs(sc))
        self.assertFalse(has(warns(sc), "regulated flow"), warns(sc))
        sc["warnings"] = [{"type": "regulation", "text": REGULATION_TEXT}]
        self.assertEqual(errs(sc), [])

    def test_regulated_word_only_in_the_invariants_is_found(self):
        sc = plain(invariants=["KVKK aydınlatma bağlantısı iki kolda da aynı yerde durur."])
        self.assertTrue(has(errs(sc), "the record looks like a regulated flow (KVKK)"), errs(sc))
        sc["warnings"] = [{"type": "regulation", "text": REGULATION_TEXT}]
        self.assertEqual(errs(sc), [])

    def card(self, line):
        return {"device": "web", "url": "magaza.example",
                "variant_a": '<div class="r-h">Uzun ürün başlığı burada duruyor</div><div class="r-sub">%s</div>' % line,
                "variant_b": '<div class="hl" data-note="Kısa başlık"><div class="r-h">Kısa başlık</div></div>'
                             '<div class="r-sub">%s</div>' % line}

    def test_regulated_text_only_on_the_mockup_is_found(self):
        for line, word in (("KVKK Aydınlatma Metni", "KVKK (card)"), ("Açık rıza metnini okudum", "Açık rıza (card)"),
                           ("Ürün sigortası ekle", "sigorta (card)"), ("I agree to the privacy notice",
                                                                         "privacy notice (card)")):
            sc = plain(card=self.card(line))
            self.assertTrue(has(errs(sc), "the record looks like a regulated flow (%s)" % word), (line, errs(sc)))
            sc["warnings"] = [{"type": "regulation", "text": REGULATION_TEXT}]
            self.assertEqual(errs(sc), [], line)

    def test_generic_mockup_words_are_not_regulated(self):
        for line in ("Siparişi onayla", "Kredi kartına 9 taksit", "Onay kodu e-postanıza gelir"):
            sc = plain(card=self.card(line))
            self.assertFalse(has(errs(sc), "regulated flow"), (line, errs(sc)))

    def test_urgency_in_b_without_a_regulation_warning(self):
        e = errs(self.urgent())
        self.assertIn("warnings: B or the mechanism carries an urgency or scarcity signal ('Son 3 ürün kaldı'); add a "
                      "warning of type 'regulation' that names the real data source behind it (real stock, inventory, "
                      "verified traffic), and don't propose it if it can't be verified (rule 6)", e)
        self.assertTrue(has(errs(self.urgent(), "tr"), "aciliyet veya kıtlık sinyali taşıyor"))

    def test_a_regulation_warning_must_name_the_data_source(self):
        sc = self.urgent()
        sc["warnings"] = [{"type": "regulation", "text": REGULATION_TEXT}]
        self.assertTrue(has(errs(sc), "urgency or scarcity signal"), errs(sc))
        sc["warnings"] = [{"type": "feasibility", "text": SOURCED_REGULATION_TEXT}]
        self.assertTrue(has(errs(sc), "urgency or scarcity signal"), errs(sc))
        sc["warnings"] = [{"type": "regulation", "text": SOURCED_REGULATION_TEXT}]
        self.assertEqual(errs(sc), [])
        sc["warnings"] = [{"type": "regulation", "text": "The count comes from verified inventory; no traffic before sign-off."}]
        self.assertEqual(errs(sc), [])

    def test_urgency_wording_in_b_or_the_mechanism(self):
        for phrase in ("Stok tükeniyor", "Geri sayım sayacı", "12 kişi bakıyor", "Son fırsat", "Sınırlı stok",
                       "Yalnızca 2 adet kaldı", "Only 2 left", "Low stock", "Don’t miss it", "Countdown timer",
                       "Selling fast"):
            self.assertTrue(has(errs(self.urgent("Başlığın altında “%s” notu" % phrase)), "urgency"), phrase)
            sc = plain(mechanism="“%s” notu karar vermeyi hızlandırır." % phrase)
            self.assertTrue(has(errs(sc), "urgency"), (phrase, errs(sc)))

    def test_the_current_page_is_not_the_variant(self):
        sc = plain()
        sc["variants"][0]["description"] = "Başlığın altında “Son 3 ürün kaldı” uyarısı"
        self.assertEqual(errs(sc), [])

    def test_last_step_is_not_scarcity(self):
        self.assertEqual(errs(self.urgent("Kısa başlık son ekranda")), [])


# --------------------------------------------- title and KPI family (warning)

class TestTitleKpiFamily(unittest.TestCase):
    RPV = {"name": "Ziyaretçi Başına Gelir (RPV)", "denominator": "Teste atanan ziyaretçi", "direction": "increase"}

    def test_abandonment_title_with_revenue_primary_warns(self):
        sc = coupon()
        sc["primary_kpi"] = dict(self.RPV)
        self.assertEqual(errs(sc), [])
        self.assertIn("primary_kpi.name: the title asks about 'çıkışı' but the primary KPI 'Ziyaretçi Başına Gelir (RPV)' "
                      "is a revenue metric; a revenue win can hide a lost benefit, measure the outcome the title names "
                      "(heuristic, rule 2)", warns(sc))
        self.assertTrue(has(warns(sc, "tr"), "sezgisel uyarı"), warns(sc, "tr"))
        sc["title"] = "Checkout abandonment drops when the coupon field hides behind a link?"
        self.assertTrue(has(warns(sc), "the title asks about 'abandonment'"), warns(sc))

    def test_revenue_title_with_completion_primary_warns(self):
        sc = coupon()
        sc["title"] = "Kupon alanını bağlantının arkasına almak geliri artırır mı?"
        self.assertIn("primary_kpi.name: the title asks about 'geliri' but the primary KPI 'Sipariş Tamamlama Oranı' is "
                      "a completion or abandonment rate; measure the outcome the title names (heuristic, rule 2)",
                      warns(sc))

    def test_matching_families_do_not_warn(self):
        self.assertEqual(warns(coupon()), [])
        sc = coupon()
        sc.update(title="Kupon alanını bağlantının arkasına almak geliri artırır mı?", primary_kpi=dict(self.RPV))
        self.assertEqual(warns(sc), [])
        self.assertEqual(warns(plain(primary_kpi=dict(self.RPV))), [])

    def test_strict_turns_it_into_a_failure(self):
        sc = coupon()
        sc["primary_kpi"] = dict(self.RPV)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(sc, fh, ensure_ascii=False)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(vsj.main([path]), 0)
                self.assertEqual(vsj.main(["--strict", path]), 1)


class TestKeywordLists(unittest.TestCase):
    """The heuristics are named constants that compile to word-start patterns."""

    def test_turkish_stems_take_suffixes_english_words_a_plural(self):
        self.assertTrue(vsj.INTERACTIVE_RE.search("bağlantısının"))
        self.assertTrue(vsj.INTERACTIVE_RE.search("two tabs"))
        self.assertFalse(vsj.INTERACTIVE_RE.search("a stable table"))
        self.assertFalse(re.search(vsj.FUNCTIONAL_RE, "carton"))

    def test_curly_and_straight_apostrophes(self):
        self.assertTrue(vsj.URGENCY_RE.search("don't miss"))
        self.assertTrue(vsj.URGENCY_RE.search("don’t miss"))


if __name__ == "__main__":
    unittest.main()
