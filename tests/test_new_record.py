#!/usr/bin/env python3
"""new_record.py (item 5): the skeleton the validator accepts once its ⟦hints⟧ are replaced, for every device and
difference type, and the validator's refusal of a hint left in place. Stdlib only."""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import new_record as nr  # noqa: E402
import validate_scenario_json as vsj  # noqa: E402

SCHEMA = vsj.load_schema()
ARCHIVE_TITLE = "Açık kupon kodu alanı sepet terkini artırır mı?"  # Fark: değiştir


def args(*extra, **kw):
    argv = ["--device", kw.get("device", "phone-web"), "--difference", kw.get("difference", "change"),
            "--page", kw.get("page", "cart-checkout"), "--kpi", kw.get("kpi", "Dönüşüm Oranı (CR)"),
            "--lang", kw.get("lang", "tr"), "--element", kw.get("element", "cta")]
    return nr.parse_args(argv + list(extra))


def strings(node, path=""):
    return dict(vsj._all_strings(node, path))


def run(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = nr.main(argv)
    return code, out.getvalue(), err.getvalue()


class TestEveryCombination(unittest.TestCase):
    def test_every_device_and_difference_validates_once_the_hints_are_replaced(self):
        for lang in ("tr", "en"):
            for device in nr.DEVICES:
                for difference in nr.DIFFERENCES:
                    for element in nr.ELEMENTS:
                        a = args(device=device, difference=difference, element=element, lang=lang)
                        with self.subTest(lang=lang, device=device, difference=difference, element=element):
                            skeleton, problems = nr.self_check(a)
                            self.assertEqual(problems, [])
                            errors = vsj.validate(skeleton, SCHEMA, lang)
                            self.assertTrue(errors)
                            self.assertEqual([e for e in errors if "placeholder" not in e and "yer tutucu" not in e],
                                             [])
                            filled = nr.build(a, sample=True)
                            self.assertEqual(vsj.validate(filled, SCHEMA, lang), [])
                            self.assertEqual(vsj.lint(filled, SCHEMA, lang), [])  # --strict too

    def test_the_hints_are_the_only_thing_to_write(self):
        # Filling the skeleton changes exactly the strings that carry a hint: everything else is final.
        for device in nr.DEVICES:
            for difference in nr.DIFFERENCES:
                a = args("--hidden", device=device, difference=difference, element="accordion")
                skeleton, filled = strings(nr.build(a)), strings(nr.build(a, sample=True))
                hinted = {p for p, _ in vsj.placeholder_paths(nr.build(a))}
                changed = {p for p in skeleton if skeleton[p] != filled.get(p)}
                self.assertEqual(changed, hinted, (device, difference))
                self.assertEqual(set(skeleton), set(filled))


class TestWhatTheSkeletonWrites(unittest.TestCase):
    def test_interactive_elements_carry_the_accessibility_warning_and_an_invariant(self):
        for element in nr.INTERACTIVE:
            rec = nr.build(args(element=element))
            warning = rec["warnings"][0]
            self.assertEqual(warning["type"], "accessibility")
            for c in vsj.A11Y_BASE:
                self.assertTrue(c[2].search(warning["text"]), (element, c[1]))
            self.assertEqual(len(rec["invariants"]), 1)
        for element in ("text", "help", "badge", "banner"):
            rec = nr.build(args(element=element))
            self.assertNotIn("warnings", rec)
            self.assertNotIn("invariants", rec)

    def test_exposure_for_a_conditionally_shown_element(self):
        for element, extra in (("accordion", ()), ("tabs", ()), ("cta", ("--hidden",))):
            rec = nr.build(args(*extra, element=element))
            self.assertTrue(vsj.BOTH_ARMS_RE.search(rec["exposure"]), element)
        self.assertNotIn("exposure", nr.build(args()))
        hidden = nr.build(args("--hidden", device="phone"))
        self.assertIn({"fold": True}, hidden["card"]["screen"])
        self.assertNotIn({"fold": True}, nr.build(args("--hidden", device="web"))["card"]["screen"])

    def test_the_glossary_denominator_in_the_records_language(self):
        rec = nr.build(args(kpi="Sipariş Tamamlama Oranı"))
        self.assertEqual(rec["primary_kpi"]["denominator"], "Checkout’a ulaşan ziyaretçi (iki kolda aynı tetikleyici)")
        rec = nr.build(args(kpi="Checkout Completion Rate", lang="en"))
        self.assertEqual(rec["primary_kpi"], {"name": "Checkout Completion Rate", "direction": "increase",
                                              "denominator": "Visitors who reached checkout (same trigger in both "
                                                             "arms)"})
        rec = nr.build(args(kpi="Bounce Rate"))  # a Turkish record gets the Turkish name
        self.assertEqual(rec["primary_kpi"]["name"], "Hemen Çıkma Oranı")
        self.assertEqual(rec["primary_kpi"]["direction"], "decrease")
        rec = nr.build(args(kpi="Adım Tamamlama Oranı", lang="en"))  # no fixed English wording: a hint
        self.assertTrue(vsj.PLACEHOLDER_RE.search(rec["primary_kpi"]["denominator"]))
        rec = nr.build(args("--guardrail", "İade Oranı (30 gün)"))
        self.assertEqual(rec["guardrail"], {"name": "İade Oranı (30 gün)", "kind": "metric", "denominator": "Sipariş",
                                            "direction": "must_not_increase"})

    def test_priority_inputs_and_tier(self):
        rec = nr.build(args(device="phone"))
        self.assertEqual(rec["priority"]["inputs"], {"evidence": "intuition", "impact": "persuasive",
                                                     "main_path": True, "noticeable": True, "effort": "medium"})
        self.assertEqual(rec["priority"]["tier"], "medium")
        rec = nr.build(args("--adapted-from", ARCHIVE_TITLE, "--impact", "structural"))
        self.assertEqual((rec["source"], rec["evidence"]["level"], rec["priority"]["tier"]),
                         ("adapted", "archive", "high"))  # 1+2+1+1+2
        rec = nr.build(args("--off-path", "--subtle", "--impact", "cosmetic", "--effort", "high"))
        self.assertEqual(rec["priority"]["tier"], "low")
        rec = nr.build(args("--evidence", "behaviour_data"))
        self.assertEqual((rec["evidence"]["level"], rec["priority"]["inputs"]["evidence"]), ("user_data",
                                                                                            "behaviour_data"))

    def test_one_change_op_per_difference(self):
        ops = {"change": "edit", "add": "insert_after", "move": "move_after", "remove": "remove"}
        for difference, op in ops.items():
            self.assertEqual(nr.build(args(difference=difference))["card"]["change"]["op"], op)
        self.assertNotIn("url", nr.build(args(device="phone"))["card"])
        self.assertEqual(nr.build(args(device="web"))["card"]["url"], "site.example/cart-checkout")


class TestPlaceholdersAreRefused(unittest.TestCase):
    def test_every_hint_is_an_error_and_no_fingerprint_is_printed(self):
        rec = nr.build(args())
        errors = vsj.validate(rec, SCHEMA, "en")
        hinted = vsj.placeholder_paths(rec)
        self.assertEqual(len([e for e in errors if "placeholder not replaced" in e]), len(hinted))
        self.assertTrue(any(e.startswith("title: placeholder not replaced") for e in errors), errors)
        self.assertTrue(any(e.startswith("card.screen[0].h:") for e in errors), errors)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "r.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(rec, fh, ensure_ascii=False)
            err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(err):
                code = vsj.main(["--fingerprint", path])
            self.assertEqual((code, out.getvalue()), (1, ""))
            self.assertIn("yer tutucu değiştirilmemiş", err.getvalue())

    def test_a_lone_bracket_is_refused_too(self):
        rec = nr.build(args(), sample=True)
        rec["problem"] = rec["problem"] + " ⟧"
        self.assertTrue(any("problem: placeholder not replaced" in e for e in vsj.validate(rec, SCHEMA, "en")))


class TestCli(unittest.TestCase):
    def test_prints_json_and_says_how_many_hints(self):
        code, out, err = run(["--device", "web", "--difference", "add", "--page", "pricing", "--kpi",
                              "Dönüşüm Oranı (CR)"])
        self.assertEqual(code, 0, err)
        rec = json.loads(out)
        self.assertEqual(rec["id"], "pricing-cta-add-01")
        self.assertIn("%d ⟦…⟧ ipucu var" % len(vsj.placeholder_paths(rec)), err)

    def test_out_writes_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "r.json")
            code, out, err = run(["--device", "phone", "--difference", "remove", "--page", "home", "--kpi",
                                  "Conversion Rate (CR)", "--lang", "en", "--out", path, "--id", "home-banner-01",
                                  "--element", "banner"])
            self.assertEqual((code, out), (0, ""), err)
            with open(path, encoding="utf-8") as fh:
                self.assertEqual(json.load(fh)["id"], "home-banner-01")
            self.assertIn("hints; replace each", err)

    def test_usage_errors(self):
        base = ["--device", "web", "--difference", "change", "--page", "cart"]
        for extra, want in ((["--kpi", "Foo Rate"], "not a knowledge/kpi-glossary.md name"),
                            (["--kpi", "Ortalama Sepet Tutarı (AOV)"], "a primary is counted per assigned visitor"),
                            (["--kpi", "Dönüşüm Oranı (CR)", "--evidence", "archive"], "needs --adapted-from"),
                            (["--kpi", "Dönüşüm Oranı (CR)", "--adapted-from", "Yok böyle bir başlık mı?"],
                             "not an archive scenario title"),
                            (["--kpi", "Dönüşüm Oranı (CR)", "--difference", "add", "--adapted-from", ARCHIVE_TITLE],
                             "pass --difference change")):
            code, out, err = run(base + extra)
            self.assertEqual((code, out), (2, ""), extra)
            self.assertIn(want, err, extra)


if __name__ == "__main__":
    unittest.main()
