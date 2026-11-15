#!/usr/bin/env python3
"""3.4: the scenario-critic stamp covers what the review decided, and fast mode.

CLAUDE.md rule 17: one critic round; the main session applies the [fixable]
findings and the stamp stays valid as long as only the small-fix fields
changed (build_card.critic_core). Warnings, invariants and exposure are
add-only: the stamp records the safeguards the critic saw and a fix that
removes or weakens one voids it (build_card.critic_safeguards). A change to
the test itself (variable, variants, KPI or guardrail choice, ...) still voids
it. Fast mode (--quick)
builds an unreviewed preview that can never be stamped or finalized.
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

REPO_ROOT = os.path.join(HERE, "..")
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "scenario-card.html")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")


def example():
    with open(EXAMPLE, encoding="utf-8") as fh:
        sc = json.load(fh)
    sc.pop("review", None)
    return sc


def critic(sc):
    """The stamp scenario-critic writes on PASS: what --critic-stamp prints."""
    return bc.critic_stamp(sc)


def problems_after(base, change):
    """critic_problems() of `base` stamped by the critic, then changed by `change`."""
    sc = copy.deepcopy(base)
    change(sc)
    review = sc.get("review") if isinstance(sc.get("review"), dict) else {}
    sc["review"] = dict(review, scenario_critic=critic(base))
    return bc.critic_problems(sc)


# Small fixes the main session may apply after the critic's one round.
SMALL_FIXES = {
    "title": lambda sc: sc.update(title=sc["title"].replace("artırır mı", "yükseltir mi")),
    "problem": lambda sc: sc.update(problem=sc["problem"].replace("çıkarabilir", "uzaklaştırabilir")),
    "mechanism": lambda sc: sc.update(mechanism=sc["mechanism"] + " "),
    "primary_kpi.denominator": lambda sc: sc["primary_kpi"].update(
        denominator="Teste atanan ziyaretçi (sepet sayfasına ulaşınca atanır, tetik iki kolda aynı)"),
    "guardrail.denominator": lambda sc: sc["guardrail"].update(denominator="Teste atanan ziyaretçi (iki kolda)"),
    "evidence.note": lambda sc: sc["evidence"].update(note=sc["evidence"]["note"] + " Sayfanın verisi yok."),
    "priority.rationale": lambda sc: sc["priority"].update(rationale=sc["priority"]["rationale"] + " "),
    "objection": lambda sc: sc.update(objection="Çaba"),
    "exposure": lambda sc: sc.update(exposure="Sepet sayfasına ulaşan kullanıcılar; tetikleyici iki kolda aynı noktada "
                                              "kaydedilir."),
    "warnings (one added)": lambda sc: sc["warnings"].append(
        {"type": "market", "text": "Kupon kullanım alışkanlığı pazara göre değişir; sonuç başka pazara taşınmaz."}),
    "warnings (text completed)": lambda sc: sc["warnings"][0].update(text=sc["warnings"][0]["text"] + " "),
    "invariants (one added)": lambda sc: sc["invariants"].append("Kupon alanı iki kolda da aynı karakter sınırını alır."),
    "source_note": lambda sc: sc.update(source_note="Kullanıcının tarif ettiği sepet."),
    "an assumption's wording": lambda sc: sc["assumptions"][0].update(
        text="Kupon kodu kampanya bağlantısıyla dağıtılıyor olabilir.", question="Kodlar nasıl dağıtılıyor?"),
    "must_be_true": lambda sc: sc.update(must_be_true={"belief": "Kodsuz kullanıcı açık kutuyu görünce kod aramaya çıkıyor.",
                                                       "probe": "Sepetten çıkıp dönen oturumların kayıtlarına bakın."}),
    "card": lambda sc: sc["card"].update(note_pos="below"),
    "review": lambda sc: sc.update(review={"mockup_reviewer": {"verdict": "PASS", "fingerprint": "a" * 64}}),
}

# Changes that need a re-call: the test itself.
TEST_CHANGES = {
    "variable": lambda sc: sc.update(variable="Kupon kodu alanının yeri"),
    "difference": lambda sc: sc.update(difference="move"),
    "variants[B].description": lambda sc: sc["variants"][1].update(description="Kupon alanı sayfanın sonunda"),
    "variants[A].is_current": lambda sc: sc["variants"][0].update(is_current=True),
    "primary_kpi.name": lambda sc: sc["primary_kpi"].update(name="Dönüşüm Oranı (CR)"),
    "primary_kpi.direction": lambda sc: sc["primary_kpi"].update(direction="decrease"),
    "guardrail.name": lambda sc: sc["guardrail"].update(name="Sayfa Hızı (LCP)"),
    "guardrail.kind": lambda sc: sc["guardrail"].update(kind="check", criterion="Kupon iki kolda uygulanır."),
    "guardrail.direction": lambda sc: sc["guardrail"].update(direction="must_not_increase"),
    "source": lambda sc: sc.update(source="generated"),
    "adapted_from": lambda sc: sc.update(adapted_from="Başka bir başlık?"),
    "evidence.level": lambda sc: sc["evidence"].update(level="intuition"),
    "priority.tier": lambda sc: sc["priority"].update(tier="high"),
    "priority.inputs": lambda sc: sc["priority"]["inputs"].update(effort="high"),
    "numeric_change": lambda sc: sc.update(numeric_change="Fiyat testi."),
    "market": lambda sc: sc.update(market="DE"),
    "device": lambda sc: sc.update(device="phone"),
    "stage": lambda sc: sc.update(stage="product-detail"),
    "lang": lambda sc: sc.update(lang="en"),
    "id": lambda sc: sc.update(id="cart-checkout-coupon-field-02"),
    "detail": lambda sc: sc.update(detail={"test_items": []}),
    "a critical assumption added": lambda sc: sc["assumptions"].append(
        {"type": "critical", "text": "Kampanya kodu dağıtılıyor.", "question": "Kod nasıl dağıtılıyor?"}),
    "an assumption removed": lambda sc: sc.update(assumptions=[]),
    "an assumption's type": lambda sc: sc["assumptions"][0].update(type="critical"),
    "a field the list doesn't know": lambda sc: sc.update(extra="x"),
}


def with_assumption(sc):
    sc = copy.deepcopy(sc)
    sc["assumptions"] = [{"type": "visual", "text": "Ürün adları temsilî."}]
    return sc


class TestCriticCore(unittest.TestCase):
    def test_small_fixes_keep_the_critic_stamp(self):
        base = with_assumption(example())
        for name, fix in SMALL_FIXES.items():
            with self.subTest(fix=name):
                sc = copy.deepcopy(base)
                fix(sc)
                self.assertNotEqual(json.dumps(sc, sort_keys=True), json.dumps(base, sort_keys=True))
                self.assertEqual(problems_after(base, fix), [])

    def test_a_change_to_the_test_voids_it(self):
        base = with_assumption(example())
        fp = bc.critic_fingerprint(base)
        for name, change in TEST_CHANGES.items():
            with self.subTest(change=name):
                sc = copy.deepcopy(base)
                change(sc)
                self.assertNotEqual(bc.critic_fingerprint(sc, bc.critic_safeguards(base)), fp)
                problems = problems_after(base, change)
                self.assertEqual(len(problems), 1)
                self.assertIn("outside the small-fix fields", problems[0])

    def test_it_is_never_the_whole_record_fingerprint(self):
        sc = example()
        self.assertRegex(bc.critic_fingerprint(sc), r"^[0-9a-f]{64}$")
        self.assertNotEqual(bc.critic_fingerprint(sc), vsj.record_fingerprint(sc))

    def test_key_order_does_not_matter(self):
        sc = example()
        flipped = dict(reversed(list(sc.items())))
        self.assertEqual(bc.critic_fingerprint(flipped), bc.critic_fingerprint(sc))

    def test_both_lists_are_disjoint_from_the_schema_fields_they_cover(self):
        # Every small-fix field is a real record field; review and card stay outside both stamps.
        with open(os.path.join(REPO_ROOT, "templates", "scenario.schema.json"), encoding="utf-8") as fh:
            fields = set(json.load(fh)["properties"])
        for name in bc.CRITIC_SMALL_FIX + tuple(bc.CRITIC_SMALL_FIX_IN) + tuple(bc.CRITIC_SMALL_FIX_ITEMS):
            self.assertIn(name, fields)
        for name in ("variable", "variants", "difference", "primary_kpi", "guardrail", "source", "evidence",
                     "priority", "assumptions"):
            self.assertIn(name, bc.critic_core(example()) if name != "assumptions" else
                          bc.critic_core(with_assumption(example())))


def guarded():
    """The example with safeguards the validator doesn't require: two more warnings and exposure."""
    sc = example()
    sc["warnings"].append({"type": "market", "text": "Kupon alışkanlığı pazara göre değişir; sonuç başka pazara "
                                                     "taşınmaz."})
    sc["warnings"].append({"type": "privacy", "text": "Kişiye özel bir kupon kodu kayıtlara ve analitiğe yazılmaz."})
    sc["exposure"] = "Sepet sayfasına ulaşan kullanıcılar; tetikleyici iki kolda aynı noktada kaydedilir."
    return sc


def a11y_text(sc):
    return sc["warnings"][0]["text"]


# Every safeguard kind removed or weakened: each voids the stamp, even where the validator has no rule against it.
SAFEGUARD_REMOVALS = {
    "a warning removed": (lambda sc: sc["warnings"].pop(1), "'market' warnings (1 reviewed, 0 now)"),
    "a warning retyped": (lambda sc: sc["warnings"][2].update(type="market"), "'privacy' warnings (1 reviewed, 0 now)"),
    "the accessibility warning removed": (lambda sc: sc["warnings"].pop(0),
                                          "'accessibility' warnings (1 reviewed, 0 now)"),
    "an accessibility criterion removed": (lambda sc: sc["warnings"][0].update(
        text=a11y_text(sc).replace(", açılınca odağı kupon alanına taşımalı", "")), "taking focus when it opens"),
    "the contrast weakened": (lambda sc: sc["warnings"][0].update(text=a11y_text(sc).replace("4.5:1", "3:1")),
                              "text contrast (at least 4.5:1)"),
    "the touch target weakened": (lambda sc: sc["warnings"][0].update(
        text=a11y_text(sc).replace("44×44 pt", "24×24 pt")), "touch target"),
    "an invariant removed": (lambda sc: sc["invariants"].pop(), "invariants (3 reviewed, 2 now)"),
    "an invariant blanked": (lambda sc: sc["invariants"].__setitem__(0, " "), "invariants (3 reviewed, 2 now)"),
    "the invariants removed": (lambda sc: sc.pop("invariants"), "invariants (3 reviewed, 0 now)"),
    "exposure removed": (lambda sc: sc.pop("exposure"), "the exposure statement"),
    "exposure blanked": (lambda sc: sc.update(exposure="  "), "the exposure statement"),
}
# Fixes that add or reword: the stamp holds.
SAFEGUARD_KEEPS = {
    "a warning reworded": lambda sc: sc["warnings"][1].update(text="Sonuç yalnızca bu pazar için geçerlidir."),
    "the accessibility warning reworded, every criterion kept": lambda sc: sc["warnings"][0].update(
        text="Bağlantı klavyeyle açılabilmeli, ekran okuyucu onu “İndirim kodum var” diye okumalı, açılınca odak "
             "kupon alanına geçmeli; dokunma alanı en az 44×44 pt, metin kontrastı en az 4.5:1."),
    "an accessibility criterion added": lambda sc: sc["warnings"][0].update(
        text=a11y_text(sc) + " Kupon alanı Esc ile kapanır."),
    "warnings reordered": lambda sc: sc["warnings"].reverse(),
    "an invariant reworded": lambda sc: sc["invariants"].__setitem__(0, "Geçerli bir kod iki kolda da aynı "
                                                                        "adımlarla uygulanır."),
    "an invariant added": lambda sc: sc["invariants"].append("Kupon alanı iki kolda da aynı karakter sınırını alır."),
    "invariants reordered": lambda sc: sc["invariants"].reverse(),
    "exposure reworded": lambda sc: sc.update(exposure="Sepet sayfasını açan kullanıcılar, iki kolda aynı tetikle."),
}


class TestAddOnlySafeguards(unittest.TestCase):
    def test_the_stamp_records_what_the_critic_saw(self):
        stamp = critic(guarded())
        self.assertEqual(stamp["safeguards"], {
            "warnings": ["accessibility", "market", "privacy"],
            "accessibility": ["touch_target", "text_contrast", "keyboard", "screen_reader", "focus_on_open"],
            "invariants": 3, "exposure": True})
        self.assertEqual(stamp["fingerprint"], bc.critic_fingerprint(guarded()))

    def test_removing_or_weakening_any_safeguard_voids_the_stamp(self):
        base = guarded()
        for name, (change, named) in SAFEGUARD_REMOVALS.items():
            with self.subTest(change=name):
                problems = problems_after(base, change)
                self.assertEqual(len(problems), 1, problems)
                self.assertIn("A small fix removed or weakened what scenario-critic reviewed", problems[0])
                self.assertIn(named, problems[0])

    def test_adding_or_rewording_keeps_it(self):
        base = guarded()
        for name, change in SAFEGUARD_KEEPS.items():
            with self.subTest(change=name):
                self.assertEqual(problems_after(base, change), [])

    def test_a_removal_the_validator_allows_is_still_refused(self):
        # The point of the floor: these deletions break no validator rule, only the critic's review.
        schema = vsj.load_schema()
        for name in ("a warning removed", "a warning retyped", "an accessibility criterion removed",
                     "an invariant removed", "exposure removed"):
            with self.subTest(change=name):
                sc = guarded()
                SAFEGUARD_REMOVALS[name][0](sc)
                self.assertEqual(vsj.validate(sc, schema, "tr"), [])
                self.assertTrue(problems_after(guarded(), SAFEGUARD_REMOVALS[name][0]))

    def test_a_removal_plus_an_addition_is_still_a_removal(self):
        def swap(sc):
            sc["warnings"].pop(2)  # privacy out
            sc["warnings"].append({"type": "feasibility", "text": "Kupon servisi iki kolda da aynı yanıtı verir."})
            sc["invariants"].append("Kupon alanı iki kolda da aynı karakter sınırını alır.")
        problems = problems_after(guarded(), swap)
        self.assertEqual(len(problems), 1)
        self.assertIn("'privacy' warnings", problems[0])

    def test_every_removal_is_named(self):
        def strip(sc):
            sc["warnings"].pop(1)
            sc["invariants"].pop()
            sc.pop("exposure")
        problem = problems_after(guarded(), strip)[0]
        for named in ("'market' warnings", "invariants (3 reviewed, 2 now)", "the exposure statement"):
            self.assertIn(named, problem)

    def test_turkish_message(self):
        sc = guarded()
        sc["review"] = {"scenario_critic": critic(guarded())}
        sc["warnings"].pop(1)
        sc["invariants"].pop()
        sc["warnings"][0]["text"] = a11y_text(sc).replace(", açılınca odağı kupon alanına taşımalı", "")
        problem = bc.critic_problems(sc, "tr")[0]
        self.assertTrue(problem.startswith("Küçük bir düzeltme scenario-critic'in incelediği bir güvenceyi"))
        for named in ("'market' türünde uyarı (incelenen 1, şimdi 0)", "açılınca odağı alması",
                      "değişmezler (incelenen 3, şimdi 2)"):
            self.assertIn(named, problem)

    def test_the_fingerprint_covers_the_recorded_safeguards(self):
        # Lowering the stamp's own floor to fit a deletion breaks its fingerprint.
        sc = guarded()
        stamp = critic(sc)
        sc["warnings"].pop(1)
        stamp["safeguards"]["warnings"].remove("market")
        sc["review"] = {"scenario_critic": stamp}
        problems = bc.critic_problems(sc)
        self.assertEqual(len(problems), 1)
        self.assertIn("outside the small-fix fields", problems[0])

    def test_a_malformed_floor_is_stale(self):
        for bad in ({"warnings": [], "accessibility": [], "invariants": "3", "exposure": True},
                    {"warnings": [], "accessibility": ["nope"], "invariants": 3, "exposure": True},
                    {"warnings": []}, []):
            with self.subTest(safeguards=bad):
                sc = guarded()
                sc["review"] = {"scenario_critic": dict(critic(sc), safeguards=bad)}
                self.assertIn("outside the small-fix fields", bc.critic_problems(sc)[0])

    def test_a_stamp_without_safeguards_matches_only_the_exact_record(self):
        sc = guarded()
        sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": bc.critic_fingerprint(sc)}}
        problem = bc.critic_problems(sc)[0]
        self.assertIn("this stamp has no safeguards", problem)
        sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}}
        self.assertEqual(bc.critic_problems(sc), [])
        sc["invariants"].append("Kupon alanı iki kolda da aynı karakter sınırını alır.")
        self.assertIn("this stamp has no safeguards", bc.critic_problems(sc)[0])

    def test_the_schema_names_the_same_keys(self):
        with open(os.path.join(REPO_ROOT, "templates", "scenario.schema.json"), encoding="utf-8") as fh:
            schema = json.load(fh)
        floor = schema["$defs"]["criticStamp"]["properties"]["safeguards"]["properties"]
        self.assertEqual(floor["accessibility"]["items"]["enum"], list(bc.A11Y_SAFEGUARD_KEYS))
        self.assertEqual(floor["warnings"]["items"]["enum"],
                         schema["properties"]["warnings"]["items"]["properties"]["type"]["enum"])
        self.assertEqual(schema["properties"]["review"]["properties"]["scenario_critic"],
                         {"$ref": "#/$defs/criticStamp"})

    def test_each_key_names_its_criterion(self):
        labels = {key: c[1] for key, c in bc.a11y_safeguard_criteria()}
        for key, label in (("touch_target", "touch target"), ("text_contrast", "text contrast"),
                           ("keyboard", "keyboard access"), ("screen_reader", "a name screen readers announce"),
                           ("focus_on_open", "taking focus when it opens"), ("close_control", "a visible close"),
                           ("esc_closes", "closing with Esc"), ("pause", "a way to pause it")):
            self.assertTrue(labels[key].startswith(label), (key, labels[key]))

    def test_a_printed_stamp_validates(self):
        sc = guarded()
        sc["review"] = {"scenario_critic": critic(sc)}
        self.assertEqual(vsj.validate(sc, vsj.load_schema(), "en"), [])
        sc["review"]["scenario_critic"]["safeguards"]["extra"] = 1
        self.assertTrue(vsj.validate(sc, vsj.load_schema(), "en"))


class Run:
    """build_card.main() in a temporary directory, the record written to s.json."""

    def __init__(self, scenario, *args, out_name="abtest-card-kupon.draft.html", tmp=None):
        self.tmp = tmp or tempfile.TemporaryDirectory()
        d = self.tmp.name
        self.src = os.path.join(d, "s.json")
        self.out = os.path.join(d, out_name)
        with open(self.src, "w", encoding="utf-8") as fh:
            json.dump(scenario, fh, ensure_ascii=False)
        argv = [a.format(src=self.src, out=self.out, template=TEMPLATE_PATH, dir=d) for a in args]
        out, err = io.StringIO(), io.StringIO()
        msg_lang = bc._MSG_LANG
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                self.code = bc.main(argv)
            except SystemExit as exc:
                self.code = exc.code
            finally:
                bc._MSG_LANG = msg_lang
        self.stdout, self.stderr = out.getvalue(), err.getvalue()

    def text(self, path=None):
        path = path or self.out
        if not os.path.exists(path):
            return None
        with open(path, encoding="utf-8") as fh:
            return fh.read()


DRAFT = ("--template", "{template}", "--scenario", "{src}", "--draft", "--out", "{out}")
QUICK = ("--template", "{template}", "--scenario", "{src}", "--quick", "--out", "{out}")


class CaseWithTmp(unittest.TestCase):
    def run_main(self, sc, *args, **kw):
        r = Run(sc, *args, **kw)
        if "tmp" not in kw:
            self.addCleanup(r.tmp.cleanup)
        return r


class TestCriticStampCommand(CaseWithTmp):
    def test_prints_the_stamp_json(self):
        sc = example()
        sc.pop("card")  # the critic reviews before the card exists
        r = self.run_main(sc, "--critic-stamp", "{src}")
        self.assertEqual(r.code, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), critic(sc))

    def test_a_record_with_errors_is_never_stamped(self):
        sc = example()
        del sc["guardrail"]
        r = self.run_main(sc, "--critic-stamp", "{src}")
        self.assertEqual(r.code, 1)
        self.assertEqual(r.stdout, "")
        self.assertIn("no critic stamp", r.stderr)
        self.assertIn("guardrail", r.stderr)

    def test_turkish_messages(self):
        sc = example()
        del sc["guardrail"]
        r = self.run_main(sc, "--critic-stamp", "{src}", "--lang", "tr")
        self.assertIn("eleştirmen damgası yok", r.stderr)

    def test_takes_only_the_record(self):
        for extra in (("--out", "{out}"), ("--draft",), ("--quick",), ("--template", "{template}")):
            with self.subTest(extra=extra):
                self.assertEqual(self.run_main(example(), "--critic-stamp", "{src}", *extra).code, 2)

    def test_other_modes_still_need_template_and_scenario(self):
        self.assertEqual(self.run_main(example(), "--scenario", "{src}", "--draft", "--out", "{out}").code, 2)


class TestDraftGateAfterSmallFixes(CaseWithTmp):
    def stamped(self):
        sc = example()
        sc["review"] = {"scenario_critic": critic(sc)}
        return sc

    def test_a_small_fix_keeps_the_draft_buildable(self):
        sc = self.stamped()
        sc["mechanism"] = sc["mechanism"].replace("zayıflar", "azalır")
        sc["warnings"].append({"type": "market", "text": "Kupon alışkanlığı pazara göre değişir; sonuç başka "
                                                         "pazara taşınmaz."})
        sc["primary_kpi"]["denominator"] = "Teste atanan ziyaretçi (sepet sayfasında atanır, iki kolda aynı tetik)"
        r = self.run_main(sc, *DRAFT)
        self.assertEqual(r.code, 0, r.stderr)
        self.assertIn('content="draft"', r.text())

    def test_a_variable_change_still_voids_the_stamp(self):
        sc = self.stamped()
        sc["variable"] = "Kupon kodu alanının yeri"
        r = self.run_main(sc, *DRAFT)
        self.assertEqual(r.code, 1)
        self.assertIn("the record changed after scenario-critic reviewed it, outside the small-fix fields", r.stderr)
        self.assertIsNone(r.text())

    def test_a_variant_change_still_voids_the_stamp(self):
        sc = self.stamped()
        sc["variants"][1]["description"] = "Kupon alanı tamamen kaldırıldı"
        self.assertEqual(self.run_main(sc, *DRAFT).code, 1)

    def test_a_kpi_choice_still_voids_the_stamp(self):
        sc = self.stamped()
        sc["primary_kpi"]["name"] = "Dönüşüm Oranı (CR)"
        sc["primary_kpi"]["denominator"] = "Teste atanan ziyaretçi"
        self.assertEqual(self.run_main(sc, *DRAFT).code, 1)

    def test_a_small_fix_that_breaks_a_rule_is_refused_by_the_validator(self):
        # Small-fix fields are re-validated at every build: removing the required accessibility warning fails.
        sc = self.stamped()
        sc["warnings"] = []
        r = self.run_main(sc, *DRAFT)
        self.assertEqual(r.code, 1)
        self.assertIn("record validation", r.stderr)

    def test_the_whole_record_fingerprint_is_an_exact_match(self):
        sc = example()
        sc["review"] = {"scenario_critic": {"verdict": "PASS", "fingerprint": vsj.record_fingerprint(sc)}}
        self.assertEqual(self.run_main(sc, *DRAFT).code, 0)
        sc["mechanism"] += " "
        self.assertEqual(self.run_main(sc, *DRAFT).code, 1)

    def test_deleting_a_safeguard_the_critic_saw_refuses_the_draft(self):
        sc = guarded()
        sc["review"] = {"scenario_critic": critic(sc)}
        sc["warnings"].pop(1)  # the validator doesn't require the market warning; the critic saw it
        r = self.run_main(sc, *DRAFT)
        self.assertEqual(r.code, 1)
        self.assertIn("review stamps", r.stderr)
        self.assertNotIn("record validation", r.stderr)
        self.assertIn("A small fix removed or weakened what scenario-critic reviewed: 'market' warnings "
                      "(1 reviewed, 0 now)", r.stderr)
        self.assertIsNone(r.text())

    def test_adding_and_rewording_safeguards_keeps_the_draft_buildable(self):
        sc = guarded()
        sc["review"] = {"scenario_critic": critic(sc)}
        sc["warnings"][1]["text"] = "Sonuç yalnızca bu pazar için geçerlidir."
        sc["invariants"].append("Kupon alanı iki kolda da aynı karakter sınırını alır.")
        sc["exposure"] = "Sepet sayfasını açan kullanıcılar, iki kolda aynı tetikle."
        r = self.run_main(sc, *DRAFT)
        self.assertEqual(r.code, 0, r.stderr)

    def test_turkish_stale_message(self):
        sc = self.stamped()
        sc["variable"] = "Kupon kodu alanının yeri"
        r = self.run_main(sc, *DRAFT, "--lang", "tr")
        self.assertIn("küçük düzeltme alanlarının", r.stderr)


class TestQuickDraft(CaseWithTmp):
    def test_builds_without_any_stamp(self):
        r = self.run_main(example(), *QUICK, "--lang", "tr")
        self.assertEqual(r.code, 0, r.stderr)
        html = r.text()
        self.assertIn('<meta name="abtest-status" content="quick-draft">', html)
        self.assertNotIn('content="draft"', html)
        self.assertIn("Hızlı taslak · incelenmedi", html)
        self.assertIn('id="abtest-draft"', html)  # the same ribbon element render_check knows
        self.assertFalse(os.path.exists(r.out + bc.MANIFEST_SUFFIX))
        self.assertIn("quick draft:", r.stdout)

    def test_english_ribbon(self):
        built, _, _ = bc.final_html(bc_template(), example())
        self.assertIn("Quick draft · not reviewed", bc.draft_html(built, "en", quick=True))

    def test_only_the_ribbon_and_meta_differ_from_the_draft(self):
        built, _, _ = bc.final_html(bc_template(), example())
        quick, draft = bc.draft_html(built, "tr", quick=True), bc.draft_html(built, "tr")
        self.assertEqual(quick.replace("quick-draft", "draft").replace(bc.QUICK_BANNER["tr"], bc.DRAFT_BANNER["tr"]),
                         draft)

    def test_the_validator_and_card_gates_still_run(self):
        sc = example()
        del sc["guardrail"]
        r = self.run_main(sc, *QUICK)
        self.assertEqual(r.code, 1)
        self.assertIn("record validation", r.stderr)

    def test_a_quick_draft_is_never_stamped(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sc = example()
        self.run_main(sc, *QUICK, tmp=tmp)
        sc["review"] = {"scenario_critic": critic(sc)}
        r = self.run_main(sc, "--template", "{template}", "--scenario", "{src}", "--stamp", "{out}", tmp=tmp)
        self.assertEqual(r.code, 1)
        self.assertIn("is a quick draft (fast mode): it is never stamped", r.stderr)
        self.assertEqual(r.stdout, "")

    def test_never_final(self):
        r = self.run_main(example(), "--template", "{template}", "--scenario", "{src}", "--out", "{dir}/x.html")
        self.assertEqual(r.code, 1)
        self.assertIn("missing review stamp: review.scenario_critic", r.stderr)

    def test_finish_replaces_it_with_the_reviewed_draft(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        sc = example()
        first = self.run_main(sc, *QUICK, tmp=tmp)
        self.assertIn("quick-draft", first.text())
        sc["review"] = {"scenario_critic": critic(sc)}
        second = self.run_main(sc, *DRAFT, tmp=tmp)
        self.assertEqual(second.code, 0, second.stderr)
        self.assertIn('content="draft"', second.text())
        self.assertNotIn("quick-draft", second.text())
        self.assertTrue(os.path.exists(second.out + bc.MANIFEST_SUFFIX))

    def test_does_not_combine_with_draft(self):
        self.assertEqual(self.run_main(example(), *QUICK, "--draft").code, 2)


def read(*parts):
    with open(os.path.join(REPO_ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def rule(n):
    return [line for line in read("CLAUDE.md").splitlines() if line.startswith("%d. " % n)][0]


class TestTextContract(unittest.TestCase):
    """The binding text says what the code enforces."""

    def test_rule_17_names_every_small_fix_field(self):
        text = rule(17)
        names = {"title": "title", "problem": "problem", "mechanism": "mechanism", "denominator": "denominators",
                 "note": "evidence note", "rationale": "priority rationale", "source_note": "source note",
                 "objection": "objection", "exposure": "exposure", "warnings": "warnings",
                 "invariants": "invariants", "text": "an assumption's wording", "must_be_true": "must-be-true lines"}
        fields = set(bc.CRITIC_SMALL_FIX) | {f for fs in bc.CRITIC_SMALL_FIX_IN.values() for f in fs} | \
            {f for fs in bc.CRITIC_SMALL_FIX_ITEMS.values() for f in fs}
        for field in fields - {"question"}:
            self.assertIn(names[field], text, field)
        for covered in ("variable", "variants", "primary KPI or guardrail choice", "number or type of assumptions"):
            self.assertIn(covered, text)
        self.assertIn("build_card.py --critic-stamp <record>", text)
        self.assertIn("Scripts run in the main session", text)

    def test_fast_mode_is_documented_where_it_runs(self):
        self.assertIn("**Fast mode**", rule(17))
        self.assertIn("fast mode's quick drafts", rule(9))
        router, card = read("skills", "ab-test", "SKILL.md"), read("skills", "ab-test-card", "SKILL.md")
        for word in ("hızlı", "taslak", "quick", "fast", "draft"):
            self.assertIn('"%s"' % word, router)
        self.assertIn("## Fast mode", card)
        self.assertIn("build_card.py --quick", card)
        self.assertIn(bc.QUICK_BANNER["tr"], card)
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, "evals", "12-fast-mode.md")))

    def test_reviewers_run_on_sonnet(self):
        for name in ("scenario-critic", "mockup-reviewer"):
            head = read("agents", name + ".md").split("\n---", 1)[0]
            self.assertIn("\nmodel: sonnet", head, name)

    def test_the_critic_stamps_with_the_builder(self):
        critic = read("agents", "scenario-critic.md")
        self.assertIn("build_card.py --critic-stamp <record.json>", critic)
        self.assertNotIn("validate_scenario_json.py --fingerprint", critic)

    def test_no_em_dash_in_any_language(self):
        self.assertIn("No em dash in any language", rule(7))


def bc_template():
    with open(TEMPLATE_PATH, encoding="utf-8") as fh:
        return fh.read()


if __name__ == "__main__":
    unittest.main()
