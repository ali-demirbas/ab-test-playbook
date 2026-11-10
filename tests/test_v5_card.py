#!/usr/bin/env python3
"""Contract 5 regression tests for the card builder. Stdlib only (unittest).

1. card.difference never overrides the record's difference: a card that would
   draw another difference than the one the critic reviewed is refused.
2. A move can be drawn: below the fold (a .r-fold marker in both arms) and
   to a later step (that step below a .r-divider in both arms), the element
   ringed at its old place in A and its new place in B. Contract 7: the old
   in-flow grey "sticky bar" is no longer read as a pinned state (refused).
3. A record with a critical assumption builds a CONDITIONAL card: an inline
   ribbon and <meta name="abtest-status" content="conditional"> in the final
   bytes; its draft is those bytes plus the draft ribbon and metas. A record
   without one builds byte for byte as before.
4. render_check.mjs measures the status ribbons and judges them (inside the
   card, off the title and the stage, off each other).
5. A consent box ("okudum", "aydınlatma", "ileti", "I have read", …) that A
   leaves unticked is never ticked in B (rule 6).
6. A consent box that A shows and B removes is a rule-6 refusal, not a
   rule-11 hold; a reworded consent box stays a rule-11 hold.
7. An added modal can be drawn: an .r-overlay whose only content is the ring
   around .r-modal is part of that ring region (nothing else is loosened), and
   render_check reports content clipped at the top of the screen and doesn't
   count the dimmed screen under the overlay as covered by the modal's ring.
"""
import contextlib
import copy
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import build_card as bc  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
SCHEMA_PATH = os.path.join(REPO_ROOT, "templates", "scenario.schema.json")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
SAMPLES = os.path.join(REPO_ROOT, "examples", "samples")
RENDER_CHECK = os.path.join(REPO_ROOT, "scripts", "render_check.mjs")
NODE = shutil.which("node")

with open(TEMPLATE_PATH, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()
with open(SCHEMA_PATH, encoding="utf-8") as _fh:
    SCHEMA_HAS_ASSUMPTIONS = "assumptions" in json.load(_fh).get("properties", {})

SHIPPED = (
    (EXAMPLE, "scenario-card.html"),
    (os.path.join(SAMPLES, "app-home.json"), "sample-app-home.html"),
    (os.path.join(SAMPLES, "desktop-product.json"), "sample-desktop-product.html"),
    (os.path.join(SAMPLES, "saas-form.json"), "sample-saas-form.html"),
)

CRITICAL = {"type": "critical", "text": "Yıllık fiyatın sayfada aylık karşılığıyla birlikte gösterildiği varsayıldı.",
            "question": "Yıllık fiyat kartta nasıl görünüyor?"}
VISUAL = {"type": "visual", "text": "Ürün adları temsilîdir."}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def example():
    sc = load(EXAMPLE)
    sc.pop("review", None)
    return sc


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


def run_main(scenario, *extra):
    """build_card.main() in a temp dir → (exit code, stdout, stderr, written text or None)."""
    with tempfile.TemporaryDirectory() as tmp:
        src, dst = os.path.join(tmp, "s.json"), os.path.join(tmp, "abtest-card-x.html")
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
        text = None
        if os.path.exists(dst):
            with open(dst, encoding="utf-8") as fh:
                text = fh.read()
        return code, out.getvalue(), err.getvalue(), text


def critic_stamp(sc):
    return {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}


def card_record(variant_a, variant_b, difference="move", device="phone-web", card_difference=None, **card):
    """A minimal record as build() reads it (no validator): title, lang, difference and the card."""
    c = {"variant_a": variant_a, "variant_b": variant_b, "device": device, "url": "https://www.ornekmagaza.com/sepet"}
    if card_difference is not None:
        c["difference"] = card_difference
    c.update(card)
    return {"title": "Ödeme butonunu sabitlemek siparişi artırır mı?", "lang": "tr", "difference": difference,
            "card": c}


# ------------------------------------------------------- 1. no difference override

class TestNoDifferenceOverride(unittest.TestCase):
    """Kartın farkı kaydın farkıdır: kart başka bir fark çizemez."""

    def test_card_difference_unlike_the_record_is_refused(self):
        # Reproduced before the fix: the shipped move sample with card.difference "change" built a draft.
        sc = load(os.path.join(SAMPLES, "desktop-product.json"))
        sc.pop("review", None)
        sc["card"]["difference"] = "change"
        msg = die_text(bc.build, TEMPLATE, sc)
        self.assertIn("card.difference 'change' differs from the record's difference 'move'", msg)
        self.assertIn("misrepresent", msg)
        # The move guidance: ring the element in both arms, old place in A, new place in B.
        self.assertIn("both arms", msg)
        msg_tr = die_text(bc.build, TEMPLATE, sc, lang="tr")
        self.assertIn("card.difference 'change', kaydın difference değeri 'move' ile aynı değil", msg_tr)
        self.assertIn("iki kolda", msg_tr)

    def test_a_move_drawn_as_remove_is_refused(self):
        # The audit's "phone asked after the quote": the record says move, the card drew a removal.
        field = '<div class="r-label">Cep telefonu</div><div class="r-field empty">05XX XXX XX XX</div>'
        a = '<div class="r-h">Teklif</div><div class="hl" data-note="Telefon alanı">%s</div>' % field
        b = '<div class="r-h">Teklif</div>'
        sc = card_record(a, b, difference="move", card_difference="remove")
        msg = die_text(bc.build, TEMPLATE, sc)
        self.assertIn("card.difference 'remove' differs from the record's difference 'move'", msg)

    def test_a_move_drawn_as_add_is_refused(self):
        # The audit's "pinned checkout button": the record says move, the card drew an added button.
        a = '<div class="r-h">Sepetim</div>'
        b = '<div class="r-h">Sepetim</div><div class="hl" data-note="Sabit buton"><div class="r-cta">Öde</div></div>'
        msg = die_text(bc.build, TEMPLATE, card_record(a, b, difference="move", card_difference="add"))
        self.assertIn("card.difference 'add' differs from the record's difference 'move'", msg)

    def test_the_same_difference_in_another_spelling_builds(self):
        cta = '<div class="hl" data-note="Taşındı"><div class="r-cta">Ödemeye geç</div></div>'
        a, b = cta + '<div class="r-h">Sepetim</div>', '<div class="r-h">Sepetim</div>' + cta
        html, _, manifest = builds(card_record(a, b, difference="move", card_difference="taşı"))
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])

    def test_a_card_difference_without_a_record_difference_still_sets_the_ring_rule(self):
        sc = card_record('<div class="r-h">Sepet</div>',
                         '<div class="r-h">Sepet</div><div class="hl" data-note="Yeni"><div class="r-sub">x</div></div>',
                         card_difference="add")
        del sc["difference"]
        builds(sc)
        sc["card"]["difference"] = "remove"  # the card's own type is the rule: B carries a ring, so remove fails
        self.assertIn("difference 'remove'", die_text(bc.build, TEMPLATE, sc))

    def test_difference_problems_reports_without_dying(self):
        self.assertEqual(bc.difference_problems({"difference": "move", "card": {"difference": "taşı"}}), [])
        self.assertEqual(bc.difference_problems({"difference": "move", "card": {}}), [])
        self.assertEqual(bc.difference_problems({"card": {"difference": "add"}}), [])
        self.assertEqual(bc.difference_problems({"difference": "move"}), [])
        # An unknown spelling is the schema's to report, not this check's.
        self.assertEqual(bc.difference_problems({"difference": "move", "card": {"difference": "shift"}}), [])
        self.assertEqual(bc.difference_problems({"difference": 3, "card": {"difference": "add"}}), [])
        problems = bc.difference_problems({"difference": "add", "card": {"difference": "change"}}, "en")
        self.assertEqual(len(problems), 1)
        self.assertIn("ring the new element in Variant B only", problems[0])
        problems = bc.difference_problems({"difference": "remove", "card": {"difference": "change"}}, "tr")
        self.assertIn("halka yalnızca A'daki öğede", problems[0])

    def test_every_shipped_record_agrees_with_its_card(self):
        for path, _ in SHIPPED:
            with self.subTest(os.path.basename(path)):
                sc = load(path)
                self.assertEqual(bc.difference_problems(sc), [])
                bc.final_html(TEMPLATE, sc)

    def test_main_refuses_it_and_writes_nothing(self):
        # The critic stamp still matches (the record fingerprint leaves the card out): the gate is the builder's.
        sc = load(os.path.join(SAMPLES, "desktop-product.json"))
        sc["card"]["difference"] = "change"
        sc["review"] = {"scenario_critic": critic_stamp(sc)}
        code, _, err, written = run_main(sc, "--draft")
        self.assertEqual(code, 1, err)
        self.assertIsNone(written)
        self.assertIn("card.difference 'change' differs from the record's difference 'move'", err)
        self.assertIn("nothing was written", err)


# ------------------------------------------------------- 2. drawing a move

FOLD = '<div class="r-fold"></div>'
ITEMS = ('<div class="r-h">Sepetim (2 ürün)</div>'
         '<div class="r-item"><div class="r-thumb"></div><div class="r-item-body"><div class="r-name">Kablosuz Kulaklık'
         '</div><div class="r-meta">1 adet</div></div><div class="r-price">1.299 TL</div></div>'
         '<div class="r-item"><div class="r-thumb"></div><div class="r-item-body"><div class="r-name">Şarj Kablosu'
         '</div><div class="r-meta">1 adet</div></div><div class="r-price">199 TL</div></div>'
         '<div class="r-line total" style="margin-bottom:14px"><span>Toplam</span><span>1.498 TL</span></div>')
BELOW = '<div class="r-info" style="margin-bottom:14px">Siparişin yarın kargoda.</div>'
PAY = '<div class="hl" data-note="Ödeme butonu"><div class="r-cta">Ödemeye geç</div></div>'
FOLD_A = ITEMS + FOLD + BELOW + PAY       # reached by scrolling: under the fold, after the page
FOLD_B = ITEMS + PAY + FOLD + BELOW       # pinned to the bottom of the first view

PHONE = '<div class="hl" data-note="Telefon alanı"><div class="r-label">Cep telefonu</div>' \
        '<div class="r-field empty">05XX XXX XX XX</div></div>'
STEP1 = ('<div class="r-h">Aracınızın bilgileri</div>'
         '<div style="margin-bottom:14px"><div class="r-label">Plaka</div><div class="r-field empty">Örn. 34 ABC 123'
         '</div></div>')
STEP1_CTA = '<div class="r-cta">Teklif al</div>'
STEP2 = ('<div class="r-divider"></div><div class="r-h">Teklifiniz hazır</div>'
         '<div class="r-card" style="margin-bottom:14px"><div class="r-line"><span>Yıllık prim</span><b>••• TL</b>'
         '</div></div>')
STEP2_CTA = '<div class="r-cta">Devam et</div>'
STEP_A = STEP1 + PHONE + STEP1_CTA + STEP2 + STEP2_CTA   # asked on the first step
STEP_B = STEP1 + STEP1_CTA + STEP2 + PHONE + STEP2_CTA   # asked after the quote, on the next step


class TestFoldMove(unittest.TestCase):
    """Sabit buton / kaydırınca ulaşılan buton: kıvrım çizgisi iki kolda da aynı yerde."""

    def test_the_fold_marker_passes_the_allowlist(self):
        root, problems = bc.parse_markup(FOLD)
        self.assertEqual(problems, [])
        self.assertIsNotNone(root)

    def test_a_fold_move_builds_as_one_moved_ring(self):
        errors, warnings = bc.card_problems("move", FOLD_A, FOLD_B, card_lang="tr",
                                            classes=bc.component_classes(TEMPLATE))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        html, _, manifest = builds(card_record(FOLD_A, FOLD_B))
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])
        self.assertEqual(manifest["changes"], [])
        self.assertNotIn(FOLD, html)  # the marker splits the screen, it is never drawn
        self.assertEqual(html.count('<div class="below">'), 2)

    def test_a_fold_marker_in_a_only_is_refused(self):
        # Draw the marker in both arms: a fold in one arm only is refused, wherever B's ring sits.
        for b in (PAY + ITEMS + BELOW, ITEMS + PAY + BELOW):
            errors, _ = bc.card_problems("move", FOLD_A, b)
            self.assertTrue(any("only Variant A has a .r-fold" in e for e in errors), errors)

    def test_a_fold_marker_inside_the_ring_is_refused(self):
        ringed_with_marker = '<div class="hl" data-note="Ödeme butonu">%s<div class="r-cta">Ödemeye geç</div></div>' % FOLD
        errors, _ = bc.card_problems("move", ITEMS + BELOW + ringed_with_marker, ITEMS + PAY + FOLD + BELOW)
        self.assertTrue(any("the ringed element's content differs" in e for e in errors), errors)
        self.assertTrue(any(".r-fold must be a direct child of the screen" in e for e in errors), errors)


class TestCrossStepMove(unittest.TestCase):
    """Sonraki adıma taşıma: adım bir .r-divider altında, başlığıyla, iki kolda da çizilir."""

    def test_a_cross_step_move_builds_as_one_moved_ring(self):
        errors, warnings = bc.card_problems("move", STEP_A, STEP_B, card_lang="tr",
                                            classes=bc.component_classes(TEMPLATE))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        sc = card_record(STEP_A, STEP_B)
        sc["title"] = "Telefonu teklif gösterildikten sonra sormak teklif talebini artırır mı?"
        _, _, manifest = builds(sc)
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])
        self.assertEqual(manifest["changes"], [])

    def test_the_destination_step_drawn_only_in_b_is_refused(self):
        # The next step's divider and heading are page copy outside the ring: both arms draw them.
        a = STEP1 + PHONE + STEP1_CTA
        b = STEP1 + STEP1_CTA + STEP2 + PHONE + STEP2_CTA
        errors, _ = bc.card_problems("move", a, b)
        self.assertTrue(any("A and B differ outside any ring" in e for e in errors), errors)

    def test_the_destination_step_inside_b_s_ring_is_a_changed_element(self):
        a = STEP1 + PHONE + STEP1_CTA + STEP2_CTA
        b = STEP1 + STEP1_CTA + '<div class="hl" data-note="Telefon alanı">%s%s</div>' % (
            STEP2, PHONE[PHONE.index(">") + 1:-len("</div>")]) + STEP2_CTA
        errors, _ = bc.card_problems("move", a, b)
        self.assertTrue(any("the ringed element's content differs" in e for e in errors), errors)

    def test_labels_describe_each_arm_and_may_differ(self):
        # Contract 6: a move's label says where the element is in THAT arm; only the content must match.
        a = STEP_A.replace("Telefon alanı", "Telefon ilk adımda")
        b = STEP_B.replace("Telefon alanı", "Telefon teklif sonrasında")
        errors, warnings = bc.card_problems("move", a, b, card_lang="tr", classes=bc.component_classes(TEMPLATE))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        _, _, manifest = builds(card_record(a, b))
        self.assertEqual([r["kind"] for r in manifest["rings"]], ["moved"])

    def test_labels_are_still_required(self):
        errors, _ = bc.card_problems("move", STEP_A, STEP_B.replace(' data-note="Telefon alanı"', ""))
        self.assertTrue(any("label" in e for e in errors), errors)


# ------------------------------------------------------- contract 6 → 7: the in-flow grey bar is gone

STICKY_BAR_STYLE = "padding:10px 0 4px;border-top:1px solid #e5e7eb;box-shadow:0 -6px 12px rgba(17,24,39,.08)"
SCROLL_CTA = '<div class="hl" data-note="Kaydırınca görünüyor"><div class="r-cta">Ödemeye geç</div></div>'


def sticky_ring(inner='<div class="r-cta">Ödemeye geç</div>', style=STICKY_BAR_STYLE):
    return '<div class="hl" data-note="Ekranın altında sabit"><div style="%s">%s</div></div>' % (style, inner)


STICKY_A = ITEMS + FOLD + BELOW + SCROLL_CTA
STICKY_B = ITEMS + sticky_ring() + FOLD + BELOW


class TestInFlowStickyBarRefused(unittest.TestCase):
    """Sabit buton artık sayfa akışında gri bar olarak çizilemez: .r-sticky ile ilk ekranın altına çizilir."""

    def test_the_bar_still_passes_the_allowlist(self):
        root, problems = bc.parse_markup(sticky_ring())
        self.assertEqual(problems, [])

    def test_the_in_flow_bar_is_refused_as_a_changed_element(self):
        errors, _ = bc.card_problems("move", STICKY_A, STICKY_B, card_lang="tr",
                                     classes=bc.component_classes(TEMPLATE))
        self.assertTrue(any("the ringed element's content differs" in e for e in errors), errors)
        self.assertIn("refused", die_text(bc.build, TEMPLATE, card_record(STICKY_A, STICKY_B)))

    def test_the_pinned_label_without_r_sticky_is_refused(self):
        errors, _ = bc.card_problems("move", STICKY_A, STICKY_B, card_lang="tr")
        self.assertTrue(any("a pinned element is drawn as a bar at the bottom of the first view" in e
                            for e in errors), errors)

    def test_no_bar_declaration_list_is_left(self):
        self.assertFalse(hasattr(bc, "BAR_DECL_RE"))
        self.assertFalse(hasattr(bc, "_sticky_bar"))

    def test_the_bar_s_colours_are_no_longer_exempt(self):
        _, warnings = bc.card_problems("change", STICKY_A.replace("Kaydırınca görünüyor", "Ödeme"),
                                       ITEMS + FOLD + BELOW + sticky_ring().replace("Ekranın altında sabit", "Ödeme"))
        self.assertTrue(any("inline colour only in Variant B" in w for w in warnings), warnings)


# ------------------------------------------------------- 3. conditional card

def conditional(sc=None, *items):
    sc = copy.deepcopy(sc or example())
    sc["assumptions"] = list(items) or [dict(CRITICAL)]
    return sc


class TestConditionalCard(unittest.TestCase):
    """Doğrulanmamış kritik varsayım → KOŞULLU kart; varsayımsız kayıt eskisiyle bayt bayt aynı."""

    def test_a_record_without_critical_assumptions_builds_byte_identical_to_the_demo(self):
        for path, demo in SHIPPED:
            with self.subTest(demo):
                with open(os.path.join(REPO_ROOT, "docs", "demo", demo), encoding="utf-8") as fh:
                    shipped = fh.read()
                sc = load(path)
                self.assertEqual(bc.final_html(TEMPLATE, sc)[0], shipped)
                self.assertEqual(bc.final_html(TEMPLATE, conditional(sc, dict(VISUAL)))[0], shipped)
                self.assertEqual(bc.final_html(TEMPLATE, dict(sc, assumptions=[]))[0], shipped)
                self.assertNotIn("abtest-status", shipped)

    def test_the_conditional_final_carries_the_ribbon_and_the_meta(self):
        plain = bc.final_html(TEMPLATE, example())[0]
        built = bc.final_html(TEMPLATE, conditional(None, dict(VISUAL), dict(CRITICAL)))[0]
        self.assertIn('<meta name="abtest-status" content="conditional">\n</head>', built)
        self.assertIn('<div id="abtest-conditional" role="note"', built)
        self.assertIn(">KOŞULLU · doğrulama gerekli</div>", built)
        self.assertNotIn("—", bc.CONDITIONAL_BANNER["tr"] + bc.CONDITIONAL_BANNER["en"])
        lines = built.splitlines()
        ribbon = [ln for ln in lines if 'id="abtest-conditional"' in ln]
        self.assertEqual(len(ribbon), 1)
        self.assertTrue(lines[lines.index(ribbon[0]) - 1].startswith('<div class="card"'))
        # Nothing else changes: the conditional card minus its meta and ribbon is the plain card.
        rest = [ln for ln in lines if ln not in ribbon and ln != '<meta name="abtest-status" content="conditional">']
        self.assertEqual("\n".join(rest) + "\n", plain)

    def test_english_ribbon(self):
        sc = conditional()
        sc["lang"] = "en"
        self.assertIn(">CONDITIONAL · needs verification</div>", bc.final_html(TEMPLATE, sc)[0])

    def test_the_ribbon_is_distinct_and_takes_no_space(self):
        style = bc.CONDITIONAL_RIBBON_STYLE
        for decl in ("position:absolute", "top:0", "pointer-events:none", "background:#fffbeb", "color:#92400e",
                     "border:1px solid #fcd34d", "12px"):
            self.assertIn(decl, style)
        self.assertNotIn("margin", style)
        self.assertNotIn("right:48px", style)  # the draft ribbon's corner: both show on a conditional draft
        self.assertNotEqual(style, bc.DRAFT_RIBBON_STYLE)

    def test_the_fingerprint_is_of_the_conditional_bytes(self):
        sc = conditional()
        built = bc.final_html(TEMPLATE, sc)[0]
        self.assertEqual(bc.final_fingerprint(TEMPLATE, sc), bc.html_fingerprint(built))
        self.assertNotEqual(bc.final_fingerprint(TEMPLATE, sc), bc.final_fingerprint(TEMPLATE, example()))

    def test_the_draft_of_a_conditional_card(self):
        final = bc.final_html(TEMPLATE, conditional())[0]
        draft = bc.draft_html(final, "tr")
        self.assertIn(">TASLAK · incelenmedi</div>", draft)
        self.assertIn(">KOŞULLU · doğrulama gerekli</div>", draft)
        # The first status meta a reader finds says draft.
        first = draft.index('<meta name="abtest-status"')
        self.assertTrue(draft.startswith('<meta name="abtest-status" content="draft">', first))
        self.assertNotIn("abtest-final-fingerprint", draft)
        stripped = draft.replace('<meta name="abtest-status" content="draft">\n', "")
        stripped = "\n".join(line for line in stripped.split("\n") if 'id="abtest-draft"' not in line)
        self.assertEqual(stripped, final)

    def test_a_malformed_assumptions_field_is_not_a_conditional_card(self):
        # The validator reports the shape; the builder only acts on a well-formed critical item.
        for value in ("critical", {"type": "critical"}, [None, "critical", {"type": "visual"}]):
            with self.subTest(value=value):
                self.assertFalse(bc.is_conditional(dict(example(), assumptions=value)))
        self.assertTrue(bc.is_conditional(dict(example(), assumptions=[{"type": "critical", "text": "x"}])))

    def test_the_summary_says_conditional(self):
        sc = conditional(None, dict(CRITICAL), dict(CRITICAL))
        built = bc.final_html(TEMPLATE, sc)[0]
        line = bc.build_summary(built, bc.normalize(sc))
        self.assertIn("conditional card (not implementation-ready)", line)
        self.assertIn("2 critical assumptions", line)
        plain = bc.final_html(TEMPLATE, example())[0]
        line = bc.build_summary(plain, bc.normalize(example()))
        self.assertNotIn("conditional", line)
        self.assertTrue(line.endswith("difference=change"), line)


@unittest.skipUnless(SCHEMA_HAS_ASSUMPTIONS, "the schema has no `assumptions` field yet (agent V adds it)")
class TestConditionalBuildEndToEnd(unittest.TestCase):
    """main(): stamps work exactly as before, on the conditional bytes."""

    def test_draft_then_final(self):
        sc = conditional()
        sc["review"] = {"scenario_critic": critic_stamp(sc)}
        code, out, err, draft = run_main(sc, "--draft")
        self.assertEqual(code, 0, err)
        self.assertIn("conditional card (not implementation-ready)", out)
        self.assertNotIn(bc.final_fingerprint(TEMPLATE, sc), out)  # the draft prints no fingerprint (M8)
        self.assertIn('<meta name="abtest-status" content="draft">', draft)
        code, _, err, _ = run_main(sc)
        self.assertEqual(code, 1)
        self.assertIn("review.mockup_reviewer", err)
        fp = bc.final_fingerprint(TEMPLATE, sc)
        sc["review"]["mockup_reviewer"] = {"verdict": "PASS", "fingerprint": bc.mockup_stamp(TEMPLATE, sc)}
        code, out, err, final = run_main(sc)
        self.assertEqual(code, 0, err)
        self.assertIn("conditional card (not implementation-ready)", out)
        self.assertEqual(bc.html_fingerprint(final), fp)
        self.assertIn('<meta name="abtest-status" content="conditional">', final)
        # The user confirms: the assumption goes, the record changes, both stamps go stale.
        del sc["assumptions"]
        code, _, err, _ = run_main(sc)
        self.assertEqual(code, 1)
        self.assertIn("review.scenario_critic.fingerprint", err)


# ------------------------------------------------------- 4. render_check

def rc_call(fn, *args):
    js = ("import * as rc from %s;\n"
          "let raw = ''; process.stdin.on('data', (d) => (raw += d));\n"
          "process.stdin.on('end', () => process.stdout.write(JSON.stringify(rc[%s](...JSON.parse(raw)))));\n"
          % (json.dumps(pathlib.Path(RENDER_CHECK).resolve().as_uri()), json.dumps(fn)))
    p = subprocess.run([NODE, "--input-type=module", "-e", js], input=json.dumps(list(args)),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise AssertionError(p.stderr)
    return json.loads(p.stdout)


def measured_card(ribbons):
    """A clean card as collect() measures it, with the given status ribbons (no frames: judge stops early)."""
    return {
        "device": "phone-web",
        "card": {"x": 0, "y": 0, "w": 1600, "h": 900, "r": 1600, "b": 900,
                 "scrollW": 1600, "scrollH": 900, "clientW": 1600, "clientH": 900},
        "page": {"w": 1600, "h": 900},
        "title": {"h": 37.5, "lineHeight": 37.5, "text": "Kupon alanı … mı?",
                  "rect": {"x": 48, "y": 40, "w": 900, "h": 37.5, "r": 948, "b": 77.5}},
        "stage": {"x": 48, "y": 105.5, "w": 1504, "h": 754.5, "r": 1552, "b": 860},
        "ribbons": ribbons,
        "variants": [],
    }


def ribbon(rid, x, w, y=0, h=29):
    return {"id": rid, "x": x, "y": y, "w": w, "h": h, "r": x + w, "b": y + h}


@unittest.skipUnless(NODE, "node not found")
class TestRenderCheckRibbons(unittest.TestCase):
    FRAMES = "expected 2 frames (Variant A and B), found 0"

    def errors(self, ribbons):
        result = rc_call("judge", measured_card(ribbons))
        return [e for e in result["errors"] if e != self.FRAMES], result["warnings"]

    def test_ribbons_in_the_top_padding_pass(self):
        conditional_ribbon = ribbon("abtest-conditional", 48, 210)
        draft_ribbon = ribbon("abtest-draft", 1352, 200)
        self.assertEqual(self.errors([conditional_ribbon]), ([], []))
        self.assertEqual(self.errors([conditional_ribbon, draft_ribbon]), ([], []))
        self.assertEqual(self.errors([]), ([], []))

    def test_a_ribbon_over_the_title_is_an_error(self):
        errors, _ = self.errors([ribbon("abtest-conditional", 48, 210, y=30)])
        self.assertTrue(any("#abtest-conditional" in e and "title" in e for e in errors), errors)

    def test_a_ribbon_outside_the_card_is_an_error(self):
        errors, _ = self.errors([ribbon("abtest-conditional", 1500, 210)])
        self.assertTrue(any("#abtest-conditional" in e and "outside the card" in e for e in errors), errors)

    def test_two_ribbons_on_each_other_are_an_error(self):
        errors, _ = self.errors([ribbon("abtest-conditional", 1352, 210), ribbon("abtest-draft", 1352, 200)])
        self.assertTrue(any("covers the ribbon #abtest-draft" in e for e in errors), errors)

    def test_measurements_without_ribbons_still_judge(self):
        m = measured_card([])
        del m["ribbons"]
        del m["title"]["rect"]
        result = rc_call("judge", m)
        self.assertEqual([e for e in result["errors"] if e != self.FRAMES], [])


# ------------------------------------------------------- 5-6. consent boxes (fix round 2)

DEMO_FORM_HEAD = '<div class="r-h">Demo talep edin</div><div class="r-label">İş e-postası</div>' \
                 '<div class="r-field empty">E-posta adresiniz</div>'
DEMO_FORM_CTA = '<div class="r-cta">Demo talep et</div>'


def gate_record(variant_a, variant_b, difference="change", **over):
    """The shipped record (no stamps) with its card's two mockups replaced."""
    sc = example()
    sc["card"]["variant_a"], sc["card"]["variant_b"] = variant_a, variant_b
    sc["card"]["difference"] = sc["difference"] = difference
    sc.update(over)
    return sc


def gate_errors(variant_a, variant_b, difference="change", lang="en", **over):
    errors, _, _ = bc.mockup_report(bc.normalize(gate_record(variant_a, variant_b, difference, **over)), lang,
                                    bc.component_classes(TEMPLATE))
    return errors


def ringed(inner, note="Kutu işaretli"):
    return '<div class="hl" data-note="%s">%s</div>' % (note, inner)


class TestPreTickedConsent(unittest.TestCase):
    """Önceden işaretlenmiş onay: “okudum”, “aydınlatma”, “ileti”, “I have read” kutuları da onay kutusudur."""

    CONSENT = ("KVKK Aydınlatma Metni’ni okudum.", "Aydınlatma metnini okudum ve anladım.",
               "Açık rıza metnini onaylıyorum.", "Ticari elektronik ileti almak istiyorum.",
               "Kullanım koşullarını kabul ediyorum.", "Kampanya duyuruları için onay veriyorum.",
               "I have read the privacy notice.", "I agree to the terms.", "I consent to marketing e-mails.",
               "I read and accept the terms.")
    NOT_CONSENT = ("Faturamı e-posta ile gönder", "İletişim adresimi fatura adresi olarak kullan", "Beni hatırla",
                   "Remember me", "Ready-made gift wrap", "Hediye paketi istiyorum")

    def test_every_consent_wording_ticked_only_in_b_is_refused(self):
        # Reproduced before the fix: the negative test's h2 ("…okudum.") built clean.
        for text in self.CONSENT:
            with self.subTest(text):
                a = DEMO_FORM_HEAD + '<div class="r-check">%s</div>' % text + DEMO_FORM_CTA
                b = DEMO_FORM_HEAD + ringed('<div class="r-check on">%s</div>' % text) + DEMO_FORM_CTA
                errors = gate_errors(a, b)
                self.assertTrue(any("rule 6: a consent box that A leaves unticked is ticked in B" in e
                                    for e in errors), errors)

    def test_the_negative_test_case_is_refused(self):
        a = DEMO_FORM_HEAD + '<div class="r-check">KVKK Aydınlatma Metni’ni okudum.</div>' + DEMO_FORM_CTA
        b = DEMO_FORM_HEAD + ringed('<div class="r-check on">KVKK Aydınlatma Metni’ni okudum.</div>') + DEMO_FORM_CTA
        msg = die_text(bc.build, TEMPLATE, gate_record(a, b))
        self.assertIn("rule 6: a consent box that A leaves unticked is ticked in B (“KVKK Aydınlatma Metni’ni okudum.”)",
                      msg)
        self.assertIn("kural 6: A'da işaretsiz duran onay kutusu B'de işaretli", "\n".join(gate_errors(a, b, lang="tr")))

    def test_a_ticked_box_that_is_not_consent_still_passes(self):
        for text in self.NOT_CONSENT:
            with self.subTest(text):
                a = DEMO_FORM_HEAD + '<div class="r-check">%s</div>' % text + DEMO_FORM_CTA
                b = DEMO_FORM_HEAD + ringed('<div class="r-check on">%s</div>' % text) + DEMO_FORM_CTA
                self.assertEqual(gate_errors(a, b), [])

    def test_the_same_ticked_state_in_both_arms_passes(self):
        # The state is compared: B ticks nothing A doesn't (a pre-ticked A is a defect to fix, rule 15).
        box = '<div class="r-check on">KVKK Aydınlatma Metni’ni okudum.</div>'
        a = DEMO_FORM_HEAD + box + '<div class="r-cta">Demo talep et</div>'
        b = DEMO_FORM_HEAD + box + ringed('<div class="r-cta">Demo iste</div>', "Buton metni")
        self.assertEqual(gate_errors(a, b), [])
        plain = '<div class="r-check">KVKK Aydınlatma Metni’ni okudum.</div>'
        self.assertEqual(gate_errors(DEMO_FORM_HEAD + plain + '<div class="r-cta">Demo talep et</div>',
                                     DEMO_FORM_HEAD + plain + ringed('<div class="r-cta">Demo iste</div>',
                                                                     "Buton metni")), [])


class TestConsentBoxRemoved(unittest.TestCase):
    """Kaldırılan onay kutusu kural 6'dır (test konusu olmaz), kural 11 bekletmesi değil."""

    LEGAL_BOX = '<div class="r-check">KVKK Aydınlatma Metni’ni okudum.</div>'
    NOTICE = '<div class="r-help">Kişisel verileriniz KVKK Aydınlatma Metni kapsamında işlenir.</div>'

    def test_a_removed_legal_consent_box_is_a_rule_6_refusal(self):
        # Reproduced before the fix: the negative test's h1 got "rule 11: … is held until the market's rule is verified".
        a = DEMO_FORM_HEAD + ringed(self.LEGAL_BOX, "Kutu kaldırıldı") + self.NOTICE + DEMO_FORM_CTA
        b = DEMO_FORM_HEAD + self.NOTICE + DEMO_FORM_CTA
        errors = gate_errors(a, b, difference="remove")
        self.assertTrue(any(e.startswith("rule 6: B removes a consent box that A shows (“KVKK Aydınlatma Metni’ni okudum.”)")
                            for e in errors), errors)
        self.assertTrue(any("never a test subject" in e for e in errors), errors)
        self.assertFalse(any(e.startswith("rule 11") for e in errors), errors)
        tr = gate_errors(a, b, difference="remove", lang="tr")
        self.assertTrue(any(e.startswith("kural 6: B, A'nın gösterdiği onay kutusunu kaldırıyor") for e in tr), tr)
        self.assertIn("rule 6: B removes a consent box", die_text(bc.build, TEMPLATE, gate_record(a, b, "remove")))

    def test_a_removed_consent_box_without_legal_words_is_refused_too(self):
        box = '<div class="r-check">Kampanya iletileri için onay veriyorum.</div>'
        errors = gate_errors(DEMO_FORM_HEAD + ringed(box, "Kutu kaldırıldı") + DEMO_FORM_CTA,
                             DEMO_FORM_HEAD + DEMO_FORM_CTA, difference="remove")
        self.assertTrue(any(e.startswith("rule 6: B removes a consent box") for e in errors), errors)

    def test_a_reworded_consent_box_is_still_a_rule_11_hold(self):
        a = DEMO_FORM_HEAD + ringed(self.LEGAL_BOX, "Kutu metni") + DEMO_FORM_CTA
        b = DEMO_FORM_HEAD + ringed('<div class="r-check">Aydınlatma metnini okudum ve anladım.</div>', "Kutu metni") \
            + DEMO_FORM_CTA
        errors = gate_errors(a, b)
        self.assertTrue(any(e.startswith("rule 11: legal or mandatory text in A is missing or changed in B") for e in errors),
                        errors)
        self.assertFalse(any("removes a consent box" in e for e in errors), errors)

    def test_removed_legal_text_that_is_no_checkbox_is_still_a_rule_11_hold(self):
        a = DEMO_FORM_HEAD + ringed(self.NOTICE, "Bilgi metni") + DEMO_FORM_CTA
        errors = gate_errors(a, DEMO_FORM_HEAD + DEMO_FORM_CTA, difference="remove")
        self.assertTrue(any(e.startswith("rule 11") for e in errors), errors)
        self.assertFalse(any("removes a consent box" in e for e in errors), errors)

    def test_a_kept_consent_box_passes(self):
        a = DEMO_FORM_HEAD + self.LEGAL_BOX + '<div class="r-cta">Demo talep et</div>'
        b = DEMO_FORM_HEAD + self.LEGAL_BOX + ringed('<div class="r-cta">Demo iste</div>', "Buton metni")
        self.assertEqual(gate_errors(a, b), [])


# ------------------------------------------------------- 7. drawing an added modal

CART = ('<div class="r-h">Sepetim</div>'
        '<div class="r-item"><div class="ph img r-thumb"></div><div class="r-item-body"><div class="r-name">Kadife Ceket'
        '</div><div class="r-meta">Beden M · 1 adet</div></div><div class="r-price">890 TL</div></div>'
        '<div class="r-link">İndirim kodum var</div>'
        '<div class="r-line"><span>Ara toplam</span><span>890 TL</span></div>'
        '<div class="r-line total"><span>Toplam</span><span>890 TL</span></div>'
        '<div class="r-cta">Ödemeye geç</div>')
MODAL_BODY = ('<div class="r-h">İndirim kodun var mı?</div><div class="r-field empty">Kodu buraya girin</div>'
              '<div class="r-cta">Uygula</div><div class="r-link">Kapat</div>')
MODAL = '<div class="r-overlay"><div class="r-modal hl" data-note="Kupon penceresi">%s</div></div>' % MODAL_BODY
MODAL_WRAPPED = ('<div class="r-overlay"><div class="hl" data-note="Kupon penceresi"><div class="r-modal">%s</div></div>'
                 '</div>' % MODAL_BODY)
A11Y_DIALOG = [{"type": "accessibility",
                "text": "Geçmeli: açılınca odak kod alanına geçer, görünür Kapat düğmesi ve Esc ile kapanır, klavyeyle "
                        "kullanılır, ekran okuyucu “İndirim kodun var mı?” adıyla okur, dokunma alanı en az 44×44 pt, "
                        "metin kontrastı en az 4.5:1."}]
OUTSIDE = "A and B differ outside any ring"


def modal_errors(a, b, difference="add"):
    return bc.card_problems(difference, a, b, card_lang="tr", classes=bc.component_classes(TEMPLATE))[0]


class TestAddedModal(unittest.TestCase):
    """Eklenen pencere: halka .r-modal'da; yalnızca o halkayı taşıyan .r-overlay halka bölgesinin parçasıdır."""

    def test_the_ringed_modal_in_its_overlay_builds_as_one_added_ring(self):
        # Reproduced before the fix: mockup-style's own shape was refused ("differ outside any ring … r-overlay").
        self.assertEqual(modal_errors(CART, CART + MODAL), [])
        html, warnings, manifest = builds(gate_record(CART, CART + MODAL, "add", warnings=A11Y_DIALOG))
        self.assertEqual([(r["kind"], r["label"], r["variant"]) for r in manifest["rings"]],
                         [("added", "Kupon penceresi", "B")])
        added = {c["value"] for c in manifest["changes"] if c["kind"] == "component" and c["change"] == "added"}
        self.assertTrue({"r-overlay", "r-modal", "r-field"} <= added, manifest["changes"])
        self.assertIn(MODAL, html)

    def test_a_wrapper_ring_around_the_modal_in_its_overlay_passes_the_diff(self):
        self.assertEqual(modal_errors(CART, CART + MODAL_WRAPPED), [])

    def test_removing_the_modal_is_the_mirror(self):
        self.assertEqual(modal_errors(CART + MODAL, CART, difference="remove"), [])

    def test_a_modal_changed_inside_an_overlay_in_both_arms_still_builds(self):
        b = MODAL.replace("Uygula", "Kodu kullan")
        a = MODAL.replace(' hl" data-note="Kupon penceresi"', '"')
        self.assertEqual(modal_errors(CART + a, CART + b, difference="change"), [])

    def test_an_unrelated_b_only_element_outside_the_rings_is_still_refused(self):
        banner = '<div class="r-banner">Bugün kargo bedava</div>'
        for b in (banner + CART + MODAL, CART + banner + MODAL, CART + MODAL + banner):
            with self.subTest(b.index(banner)):
                errors = modal_errors(CART, b)
                self.assertTrue(any(OUTSIDE in e and "r-banner" in e for e in errors), errors)

    def test_an_overlay_with_more_than_the_ringed_modal_is_refused(self):
        extra = MODAL[:-len("</div>")] + '<div class="r-sub">Kampanya</div></div>'
        text = MODAL.replace('<div class="r-overlay">', '<div class="r-overlay">Son gün', 1)
        two = MODAL[:-len("</div>")] + MODAL[len('<div class="r-overlay">'):]
        for name, b in (("extra element", extra), ("loose text", text), ("two rings", two)):
            with self.subTest(name):
                self.assertTrue(any(OUTSIDE in e and "r-overlay" in e for e in modal_errors(CART, CART + b)),
                                modal_errors(CART, CART + b))

    def test_an_overlay_whose_ring_is_not_the_modal_is_refused(self):
        cta = '<div class="r-overlay"><div class="r-cta hl" data-note="Kupon butonu">Kupon kullan</div></div>'
        self.assertTrue(any(OUTSIDE in e for e in modal_errors(CART, CART + cta)))
        bare = '<div class="r-overlay"><div class="hl" data-note="Kupon penceresi"><div class="r-sub">x</div>' \
               '</div></div>'
        self.assertTrue(any(OUTSIDE in e for e in modal_errors(CART, CART + bare)))

    def test_an_unringed_modal_with_the_ring_elsewhere_is_refused(self):
        b = CART.replace('<div class="r-link">İndirim kodum var</div>',
                         ringed('<div class="r-link">Kodum var</div>', "Bağlantı metni"))
        b += MODAL.replace(' hl" data-note="Kupon penceresi"', '"')
        self.assertTrue(any(OUTSIDE in e and "r-overlay" in e for e in modal_errors(CART, b, "change")))


# ------------------------------------------------------- 7. render_check: content clipped at the top

def rc_variant(name, **over):
    """One clean phone-web frame as collect() measures it."""
    x, y, w, h = (202 if name == "A" else 978), 282, 420, 447
    v = {"name": name, "column": {"x": x - 154, "y": 200, "w": 728, "h": 755},
         "frame": {"x": x, "y": y, "w": w, "h": h, "r": x + w, "b": y + h, "kind": "phone-web",
                   "innerBottom": y + h - 1, "scrollH": h - 2, "clientH": h - 2},
         "screen": {"x": x + 1, "y": y + 90, "w": w - 2, "h": h - 92, "r": x + w - 1, "b": y + h - 1,
                    "scrollH": h - 92, "clientH": h - 92, "scrollW": w - 2, "clientW": w - 2},
         "widest": None, "topmost": None, "lowest": {"y": y + h - 21, "what": "“Ödemeye geç”"},
         "texts": [], "items": [], "rings": []}
    v.update(over)
    return v


def rc_card(a, b):
    m = measured_card([])
    m["stage"] = {"x": 48, "y": 105.5, "w": 1504, "h": 755, "r": 1552, "b": 860.5}
    m["variants"] = [a, b]
    return m


@unittest.skipUnless(NODE, "node not found")
class TestRenderCheckTopClip(unittest.TestCase):
    """Ekranın üst kenarında kesilen içerik de bir hatadır (yalnızca alt ve yan değil)."""

    def test_content_cut_off_at_the_top_is_an_error(self):
        b = rc_variant("B", topmost={"px": 118.4, "what": "“İndirim kodun var mı?”"})
        errors = rc_call("judge", rc_card(rc_variant("A"), b))["errors"]
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("variant B: screen content is clipped at the top", errors[0])
        self.assertIn("“İndirim kodun var mı?”", errors[0])
        self.assertIn("118px", errors[0])

    def test_nothing_above_the_screen_passes(self):
        for topmost in (None, {"px": 0.6, "what": "“Sepetim”"}):
            with self.subTest(topmost):
                result = rc_call("judge", rc_card(rc_variant("A", topmost=topmost), rc_variant("B")))
                self.assertEqual(result, {"errors": [], "warnings": []})
        legacy = rc_variant("A")
        del legacy["topmost"]
        self.assertEqual(rc_call("judge", rc_card(legacy, rc_variant("B")))["errors"], [])

    def test_collect_measures_the_top_edge(self):
        with open(RENDER_CHECK, encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn("v.topmost", src)
        self.assertIn("clipped at the top", src)


@unittest.skipUnless(NODE, "node not found")
class TestRenderCheckRingOverOverlay(unittest.TestCase):
    """A ring on the modal sits over the dimming: the screen under the overlay isn't covered by it."""

    def frame_b(self, ring_over_overlay):
        x, y = 978, 282
        under = {"what": "“Ödemeye geç”", "rects": [{"x": x + 20, "y": y + 360, "r": x + 400, "b": y + 404}], "skip": [],
                 "dimmed": True}
        modal_text = {"what": "“Uygula”", "rects": [{"x": x + 60, "y": y + 300, "r": x + 360, "b": y + 340}],
                      "skip": [0], "dimmed": False}
        ring = {"note": "Kupon penceresi", "grow": 7, "nested": [], "overOverlay": ring_over_overlay,
                "outline": {"x": x + 34, "y": y + 180, "r": x + 386, "b": y + 420},
                "label": {"rect": {"x": x + 266, "y": y + 152, "r": x + 386, "b": y + 172}, "pos": "above",
                          "px": 12.5, "fg": [255, 255, 255, 1], "bg": [225, 29, 72, 1]}}
        return rc_variant("B", items=[under, modal_text], rings=[ring])

    def test_the_dimmed_screen_under_a_modal_ring_is_not_covered(self):
        result = rc_call("judge", rc_card(rc_variant("A"), self.frame_b(True)))
        self.assertEqual(result["errors"], [])

    def test_a_ring_that_is_not_over_the_overlay_still_covers_it(self):
        errors = rc_call("judge", rc_card(rc_variant("A"), self.frame_b(False)))["errors"]
        self.assertTrue(any("ring covers screen elements" in e and "Ödemeye geç" in e for e in errors), errors)

    def test_collect_marks_the_dimmed_items_and_the_rings_over_the_overlay(self):
        with open(RENDER_CHECK, encoding="utf-8") as fh:
            src = fh.read()
        self.assertIn("overOverlay", src)
        self.assertIn("item.dimmed", src)


if __name__ == "__main__":
    unittest.main()


class TestMarketingOptInIsConsent(unittest.TestCase):
    """Lead fix after B2: an opt-in worded as a wish is a consent box; pre-ticking it is a dark pattern."""

    def test_opt_in_wish_is_a_consent_term(self):
        for text in ("Ürün haberlerini e-postayla almak istiyorum.", "Kampanyaların SMS ile gönderilmesini istiyorum.",
                     "I want to receive product news by e-mail.", "Subscribe me to the newsletter."):
            self.assertTrue(bc.CONSENT_RE.search(bc._fold(text)), text)

    def test_ordinary_wish_is_not(self):
        for text in ("Beni hatırla", "Faturamı e-posta ile gönder", "Ready to order"):
            self.assertFalse(bc.CONSENT_RE.search(bc._fold(text)), text)
