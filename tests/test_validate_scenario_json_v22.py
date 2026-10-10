#!/usr/bin/env python3
"""validate_scenario_json.py v2.2 denetimleri için unit testler. Bağımlılıksız.

Kapsam: uyarı kanalı ve --strict, yeni hata denetimleri (ölçütsüz kontrol
guardrail'i, birincilin adını taşıyan guardrail, ön kayıtta eksik guardrail,
trafik bilinmezken sayı, üçüncü kol, metin olmayan kart alanları) ve uyarılar
(payda, gecikmeli pencere, tümleyen guardrail, sayı/gören, düzenlemeye tabi akış).
"""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import validate_scenario_json as vsj  # noqa: E402

REPO_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EXAMPLE = os.path.join(REPO_ROOT, "examples", "scenario.json")
SCHEMA = vsj.load_schema()


def base():
    return {
        "id": "cart-checkout-coupon-field-01",
        "title": "Açık kupon alanı sepet terkini artırır mı?",
        "source": "generated",
        "variable": "Kupon alanının görünürlüğü",
        "hypothesis": {"change": "Kupon alanı bağlantı arkasına alınır.",
                       "mechanism": "Açık kutu kod aramaya yönlendirdiği için terk artıyor."},
        "variants": [{"id": "A", "description": "Açık kutu", "is_current": True},
                     {"id": "B", "description": "Bağlantı arkasında"}],
        "kpis": [
            {"name": "Ziyaretçi Başına Gelir (RPV)", "role": "primary", "question": "Artıyor mu?"},
            {"name": "Sipariş Tamamlama Oranı (sepete ulaşan kullanıcı başına)", "role": "secondary", "question": "Değişiyor mu?"},
            {"name": "Kupon Kullanım Oranı (sipariş başına)", "role": "guardrail", "question": "Çökmemeli."},
        ],
        "test_items": ["Kaçak kapanıyor mu?", "Segment farkı var mı?", "Metin etkiliyor mu?"],
        "dont_items": ["Alanı kaldırmayın.", "Hatayı gizlemeyin.", "Aynı testte metni değiştirmeyin."],
        "evidence": {"level": "sector"},
    }


def prereg(**over):
    pre = {
        "hypothesis": "Kupon alanını gizlemek RPV'yi artırır.",
        "variable": "Kupon alanının görünürlüğü",
        "primary_kpi": {"name": "Ziyaretçi Başına Gelir (RPV)", "direction": "increase"},
        "guardrails": [{"name": "Kupon Kullanım Oranı (sipariş başına)", "direction": "must_not_decrease",
                        "margin_relative": 0.05}],
        "mde": None, "alpha": 0.05, "power": 0.8, "alternative": "two-sided",
        "allocation": {"A": 0.5, "B": 0.5},
        "planned_n_per_arm": None, "duration_days": None,
        "decision_rule": "RPV anlamlı artar ve guardrail marj içinde kalırsa yayına al.",
    }
    pre.update(over)
    return pre


def card(**over):
    c = {"difference": "add",
         "variant_a": '<div class="r-h">Sepet</div>',
         "variant_b": '<div class="r-h">Sepet</div><div class="hl" data-note="yeni"><div class="r-link">Kodum var</div></div>'}
    c.update(over)
    return c


def errs(sc, lang="en"):
    return vsj.validate(sc, SCHEMA, lang)


def warns(sc, lang="en"):
    return vsj.lint(sc, SCHEMA, lang)


def has(items, fragment):
    return any(fragment in x for x in items)


class TestBaseline(unittest.TestCase):
    def test_base_is_clean(self):
        self.assertEqual(errs(base()), [])
        self.assertEqual(warns(base()), [])

    def test_base_with_prereg_and_card_is_clean(self):
        sc = base()
        sc["preregistration"] = prereg()
        sc["card"] = card()
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])

    def test_scenario_without_card_is_valid(self):
        self.assertNotIn("card", base())
        self.assertEqual(errs(base()), [])

    def test_shipped_example_has_no_errors_and_no_warnings(self):
        with open(EXAMPLE, encoding="utf-8") as fh:
            sc = json.load(fh)
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])


class TestBoxSize(unittest.TestCase):
    def test_three_to_six_items(self):
        for n in (3, 4, 5, 6):
            sc = base()
            sc["test_items"] = ["Madde %d soruyor mu?" % i for i in range(n)]
            self.assertEqual(errs(sc), [], n)
            self.assertEqual(warns(sc), [], n)

    def test_seven_items_is_an_error(self):
        for box in ("test_items", "dont_items"):
            sc = base()
            sc[box] = ["Madde %d" % i for i in range(7)]
            self.assertTrue(has(errs(sc), "%s: has 7 item(s), maximum is 6" % box), errs(sc))
        sc = base()
        sc["kpis"] += [{"name": "M%d (kullanıcı başına)" % i, "role": "secondary"} for i in range(4)]
        self.assertTrue(has(errs(sc), "kpis: has 7 item(s), maximum is 6"), errs(sc))

    def test_two_items_is_an_error(self):
        sc = base()
        sc["dont_items"] = ["Bir", "İki"]
        self.assertTrue(has(errs(sc), "minimum is 3"))


class TestGuardrailErrors(unittest.TestCase):
    def test_check_guardrail_needs_a_criterion(self):
        sc = base()
        sc["kpis"].append({"name": "Erişilebilirlik Kontrolü", "role": "guardrail", "question": "Geçmeli."})
        sc["preregistration"] = prereg()
        sc["preregistration"]["guardrails"].append({"name": "Erişilebilirlik Kontrolü", "type": "check"})
        self.assertTrue(has(errs(sc), "criterion"), errs(sc))
        sc["preregistration"]["guardrails"][-1]["criterion"] = "Klavye ve ekran okuyucuda kritik bulgu yok"
        self.assertEqual(errs(sc), [])

    def test_guardrail_mixing_margin_and_check_gets_a_real_message(self):
        sc = base()
        sc["preregistration"] = prereg(guardrails=[{"name": "Kupon Kullanım Oranı (sipariş başına)", "type": "check",
                                                    "margin_relative": 0.05}])
        e = errs(sc)
        self.assertTrue(has(e, "either margin-based"), e)
        self.assertFalse(has(e, "oneOf"), e)

    def test_guardrail_with_the_primary_name_in_the_kpi_box(self):
        sc = base()
        sc["kpis"][2] = {"name": "ziyaretçi başına  gelir (RPV)", "role": "guardrail", "question": "Düşmemeli."}
        self.assertTrue(has(errs(sc), "appears twice"), errs(sc))

    def test_prereg_guardrail_is_the_primary(self):
        pre = prereg()
        pre["guardrails"] = [{"name": "Ziyaretçi Başına Gelir (RPV)", "direction": "must_not_decrease",
                              "margin_relative": 0.05}]
        e = vsj.validate_prereg_only({"preregistration": pre}, SCHEMA, "en")
        self.assertTrue(has(e, "is the primary KPI itself"), e)

    def test_prereg_guardrail_defined_twice(self):
        pre = prereg()
        pre["guardrails"].append(dict(pre["guardrails"][0], margin_relative=0.2))
        e = vsj.validate_prereg_only({"preregistration": pre}, SCHEMA, "en")
        self.assertTrue(has(e, "is defined twice"), e)

    def test_prereg_drops_a_scenario_guardrail(self):
        sc = base()
        sc["kpis"].append({"name": "İade Oranı (sipariş başına, 30 gün)", "role": "guardrail", "question": "Artmamalı."})
        sc["preregistration"] = prereg()
        e = errs(sc)
        self.assertTrue(has(e, "is missing from the pre-registration"), e)
        self.assertTrue(has(e, "İade Oranı"), e)

    def test_prereg_names_a_guardrail_outside_the_kpi_box(self):
        sc = base()
        sc["preregistration"] = prereg()
        sc["preregistration"]["guardrails"].append({"name": "Destek Talebi Oranı (kullanıcı başına)",
                                                    "direction": "must_not_increase", "margin_relative": 0.1})
        self.assertTrue(has(errs(sc), "not in the scenario's KPI list"), errs(sc))

    def test_expected_direction_contradicts_prereg(self):
        sc = base()
        sc["hypothesis"]["expected_direction"] = "decrease"
        sc["preregistration"] = prereg()
        self.assertTrue(has(errs(sc), "contradicts hypothesis.expected_direction"), errs(sc))
        sc["hypothesis"]["expected_direction"] = "unknown"
        self.assertEqual(errs(sc), [])


class TestTrafficAndArms(unittest.TestCase):
    def test_numbers_with_traffic_known_false(self):
        sc = base()
        sc["sample"] = {"traffic_known": False, "daily_visitors": 4000, "estimated_days": 14}
        e = errs(sc)
        self.assertTrue(has(e, "sample.daily_visitors: no number while traffic_known is false"), e)
        self.assertTrue(has(e, "sample.estimated_days"), e)

    def test_planned_numbers_with_traffic_known_false(self):
        sc = base()
        sc["sample"] = {"traffic_known": False}
        sc["preregistration"] = prereg(planned_n_per_arm=5000, duration_days=14)
        e = errs(sc)
        self.assertTrue(has(e, "preregistration.planned_n_per_arm"), e)
        self.assertTrue(has(e, "rule 5"), e)

    def test_bare_traffic_flag_warns_about_the_inputs(self):
        doc = {"preregistration": prereg(planned_n_per_arm=5000, duration_days=2), "sample": {"traffic_known": True}}
        self.assertEqual(vsj.validate_prereg_only(doc, SCHEMA, "en"), [])
        w = vsj.lint_prereg_only(doc, "en")
        self.assertTrue(has(w, "cannot be computed without mde and power"), w)
        self.assertTrue(has(w, "without sample.daily_visitors"), w)
        self.assertTrue(has(w, "under two full weeks"), w)

    def test_duration_shorter_than_the_sample_needs(self):
        doc = {"preregistration": prereg(planned_n_per_arm=24000, duration_days=14, mde=0.1),
               "sample": {"traffic_known": True, "daily_visitors": 1000}}
        w = vsj.lint_prereg_only(doc, "en")
        self.assertTrue(has(w, "48 days"), w)

    def test_third_arm_gets_a_real_message(self):
        for doc in ({"preregistration": prereg(allocation={"A": 0.34, "B": 0.33, "C": 0.33})},):
            e = vsj.validate_prereg_only(doc, SCHEMA, "en")
            self.assertTrue(has(e, "allocation keys must match variant ids"), e)
            self.assertFalse(has(e, "unknown field"), e)
        sc = base()
        sc["preregistration"] = prereg(allocation={"A": 0.34, "B": 0.33, "C": 0.33})
        e = errs(sc, "tr")
        self.assertTrue(has(e, "varyant kimlikleriyle"), e)

    def test_variant_ids_must_be_a_then_b(self):
        sc = base()
        sc["variants"][1]["id"] = "A"
        self.assertTrue(has(errs(sc), 'ids must be "A" then "B"'), errs(sc))
        sc = base()
        sc["variants"][1]["is_current"] = True
        self.assertTrue(has(errs(sc), "the current page is always A"), errs(sc))

    def test_alpha_and_power_out_of_convention_warn(self):
        doc = {"preregistration": prereg(alpha=0.2, power=0.05)}
        w = vsj.lint_prereg_only(doc, "en")
        self.assertTrue(has(w, "alpha"), w)
        self.assertTrue(has(w, "power"), w)


class TestCardFields(unittest.TestCase):
    def test_non_string_variant_does_not_crash(self):
        sc = base()
        sc["card"] = card(variant_a=123)
        e = errs(sc)
        self.assertTrue(has(e, "card.variant_a: expected type string"), e)

    def test_non_string_card_fields_are_errors(self):
        sc = base()
        sc["card"] = card(shift_note_b=5, url=["x"], footer_notes="tek satır", bottom_nav=[{"label": "Ana Sayfa"}])
        e = errs(sc)
        for path in ("card.shift_note_b", "card.url", "card.footer_notes", "card.bottom_nav[0]"):
            self.assertTrue(has(e, path), (path, e))

    def test_markup_outside_the_allowlist_is_an_error(self):
        sc = base()
        sc["card"] = card(variant_b=card()["variant_b"] + "<img src=x onerror=alert(1)>")
        self.assertTrue(has(errs(sc), "card: variant_b"), errs(sc))

    def test_ring_margin_is_an_error(self):
        sc = base()
        sc["card"] = card(variant_b=card()["variant_b"].replace('class="hl"', 'class="hl" style="margin-bottom:20px"'))
        self.assertTrue(has(errs(sc, "tr"), "içeriği itmemeli"), errs(sc, "tr"))

    def test_unknown_colour_name_is_an_error(self):
        sc = base()
        sc["card"] = card(brand={"primary": "mavi"})
        self.assertTrue(has(errs(sc), "brand.primary"), errs(sc))
        sc["card"] = card(brand={"primary": "rgb(,,/%%)"})
        self.assertTrue(has(errs(sc), "brand.primary"), errs(sc))
        sc["card"] = card(brand={"primary": "navy", "on_primary": "#fff"})
        self.assertEqual(errs(sc), [])

    def test_bottom_nav_active(self):
        sc = base()
        sc["device"] = "phone"
        sc["card"] = card(bottom_nav=["Ana Sayfa", "Ürünlerim"], bottom_nav_active="Ürünlerim")
        self.assertEqual(errs(sc), [])
        sc["card"]["bottom_nav_active"] = 1
        self.assertEqual(errs(sc), [])
        sc["card"]["bottom_nav_active"] = "Profil"
        self.assertTrue(has(errs(sc), "card.bottom_nav_active"), errs(sc))
        sc["card"]["bottom_nav_active"] = 2
        self.assertTrue(has(errs(sc), "card.bottom_nav_active"), errs(sc))
        del sc["card"]["bottom_nav"]
        self.assertEqual(errs(sc), [])  # ignored without bottom_nav

    def test_tab_bar_and_url_follow_the_frame(self):
        sc = base()
        sc["device"] = "phone-web"
        sc["card"] = card(url="magaza.example/sepet", bottom_nav=["Ana Sayfa"])
        self.assertTrue(has(errs(sc), "card.bottom_nav: only valid with device 'phone'"), errs(sc))
        sc["card"] = card()
        self.assertTrue(has(errs(sc), "card.url: device 'phone-web' draws an address bar"), errs(sc))
        sc["device"] = "phone"
        sc["card"] = card(device="web")
        self.assertTrue(has(errs(sc), "card.url"), errs(sc))

    def test_card_warnings_reach_lint(self):
        sc = base()
        sc["card"] = card(variant_b=card()["variant_b"].replace('class="r-link"', 'class="r-link" style="color:#0a7f3f"'))
        w = warns(sc)
        self.assertTrue(has(w, "card: ") and has(w, "#0a7f3f"), w)
        self.assertEqual([x for x in vsj.lint(sc, SCHEMA, "en", include_card=False) if "#0a7f3f" in x], [])

    def test_shared_page_without_is_current_warns(self):
        sc = base()
        del sc["variants"][0]["is_current"]
        sc["card"] = card(mockup_basis="shared_page")
        self.assertTrue(has(warns(sc), "is_current"), warns(sc))

    def test_card_device_differs_from_scenario_device(self):
        sc = base()
        sc["device"] = "web"
        sc["card"] = card(device="phone")
        self.assertTrue(has(warns(sc), "differs from the scenario's device"), warns(sc))


class TestDenominatorWarnings(unittest.TestCase):
    def kpi(self, name, role="guardrail", **extra):
        sc = base()
        sc["kpis"][2 if role == "guardrail" else 1] = dict({"name": name, "role": role, "question": "Soru?"}, **extra)
        return sc

    def test_rate_without_denominator_warns_on_any_role(self):
        for role in ("guardrail", "secondary"):
            w = warns(self.kpi("Talepten Poliçeye Dönüşüm Oranı", role))
            self.assertTrue(has(w, "is a rate with no stated denominator"), (role, w))

    def test_window_in_parentheses_is_not_a_denominator(self):
        w = warns(self.kpi("Talepten Poliçeye Dönüşüm Oranı (90 gün)"))
        self.assertTrue(has(w, "no stated denominator"), w)

    def test_primary_rate_without_denominator_warns(self):
        sc = base()
        sc["kpis"][0]["name"] = "Talep Oluşturma Oranı"
        self.assertTrue(has(warns(sc), "kpis[0]"), warns(sc))

    def test_stated_denominators_do_not_warn(self):
        for name in ("Dönüşüm Oranı (atanan kullanıcı başına)", "Conversion Rate (per assigned user)",
                     "Sipariş Başına İade Oranı", "Orders per Visitor Rate"):
            self.assertFalse(has(warns(self.kpi(name)), "denominator"), name)
        self.assertFalse(has(warns(self.kpi("Dönüşüm Oranı", denominator="atanan kullanıcı")), "denominator"))

    def test_non_rate_metrics_are_skipped(self):
        for name in ("Akordeonda Kalma Süresi", "LCP", "Ziyaretçi Başına Gelir (RPV)", "Ortalama Sepet Tutarı (AOV)",
                     "Sipariş Tutarı"):
            self.assertFalse(has(warns(self.kpi(name)), "denominator"), name)

    def test_check_type_guardrail_is_skipped(self):
        sc = self.kpi("Erişilebilirlik Kontrolü Geçme Oranı (yayın öncesi, geçti/kaldı)")
        self.assertFalse(has(warns(sc), "denominator"), warns(sc))
        sc = self.kpi("Kontrast Oranı")
        sc["preregistration"] = prereg(guardrails=[{"name": "Kontrast Oranı", "type": "check",
                                                    "criterion": "4.5:1 ve üstü"}])
        self.assertFalse(has(warns(sc), "denominator"), warns(sc))

    def test_b_only_line_is_skipped(self):
        for name in ("Uygunluk Girişine Dokunma Oranı (yalnız B, tanı amaçlı)", "Tooltip Open Rate (B only, diagnostic)",
                     "Yeni Butonu Gören Kullanıcı Sayısı (yalnız B)"):
            w = warns(self.kpi(name, "secondary"))
            self.assertEqual(w, [], (name, w))

    def test_archive_scenario_inherits_glossary_denominators(self):
        sc = self.kpi("Kupon Kullanım Oranı")
        sc["source"] = "archive"
        sc["evidence"] = {"level": "archive"}
        self.assertFalse(has(warns(sc), "denominator"), warns(sc))
        sc["source"] = "generated"
        self.assertTrue(has(warns(sc), "denominator"), warns(sc))

    def test_turkish_message(self):
        w = warns(self.kpi("Talepten Poliçeye Dönüşüm Oranı"), "tr")
        self.assertTrue(has(w, "paydası yazılmamış"), w)


class TestCountAndSaw(unittest.TestCase):
    def test_count_primary_is_an_error(self):
        sc = base()
        sc["kpis"][0]["name"] = "Sipariş Sayısı"
        self.assertTrue(has(errs(sc), "primary KPI 'Sipariş Sayısı' is a count"), errs(sc))

    def test_count_per_visitor_is_fine(self):
        sc = base()
        sc["kpis"][0]["name"] = "Ziyaretçi Başına Sipariş Sayısı"
        self.assertEqual(errs(sc), [])
        self.assertEqual(warns(sc), [])

    def test_saw_denominator_on_primary_is_an_error(self):
        sc = base()
        sc["kpis"][0]["name"] = "Sipariş Oranı (kupon bağlantısını gören kullanıcı başına)"
        self.assertTrue(has(errs(sc), '"users who saw"'), errs(sc))

    def test_count_and_saw_on_other_roles_warn(self):
        sc = base()
        sc["kpis"][1] = {"name": "Hızlı Ödeme Tıklama Sayısı", "role": "secondary", "question": "?"}
        sc["kpis"][2] = {"name": "İade Oranı (butonu gören kullanıcı başına)", "role": "guardrail", "question": "Artmamalı."}
        self.assertEqual(errs(sc), [])
        w = warns(sc)
        self.assertTrue(has(w, "kpis[1]: secondary KPI") and has(w, "is a count"), w)
        self.assertTrue(has(w, "kpis[2]: guardrail KPI") and has(w, "users who saw"), w)

    def test_prereg_only_checks_names_too(self):
        pre = prereg(primary_kpi={"name": "Sipariş Sayısı", "direction": "increase"})
        e = vsj.validate_prereg_only({"preregistration": pre}, SCHEMA, "en")
        self.assertTrue(has(e, "is a count"), e)


class TestLaggingWindows(unittest.TestCase):
    def sc(self, name, rule=None, **guard):
        sc = base()
        sc["kpis"][2] = {"name": name, "role": "guardrail", "question": "Artmamalı."}
        g = dict({"name": name, "direction": "must_not_increase", "margin_relative": 0.05}, **guard)
        sc["preregistration"] = prereg(guardrails=[g])
        if rule:
            sc["preregistration"]["decision_rule"] = rule
        return sc

    def test_window_in_name_without_read_after_days(self):
        for name, n in (("İade Oranı (sipariş başına, 90 gün)", 90), ("Return Rate (per order, 30 days)", 30),
                        ("Yenileme Oranı (kullanıcı başına, 2 hafta)", 14)):
            w = warns(self.sc(name))
            self.assertTrue(has(w, "names a %d-day window but has no read_after_days" % n), (name, w))

    def test_lagging_word_without_window(self):
        for name in ("Poliçe İptal Oranı (düzenlenen poliçe başına)", "Churn Rate (per subscriber)",
                     "Hizmeti Durdurma Oranı (katılan kullanıcı başına)", "Cayma Oranı (poliçe başına)"):
            w = warns(self.sc(name))
            self.assertTrue(has(w, "looks like a lagging outcome"), (name, w))

    def test_window_to_be_verified_from_product_terms_is_accepted(self):
        for rule in ("Cayma süresi ürün koşullarından doğrulanıp ön kayda yazılmadan test başlamaz. RPV artarsa yayına al.",
                     "The withdrawal period is verified from product terms before start. Ship if RPV rises."):
            w = warns(self.sc("Cayma Süresi İçinde Poliçe İptal Oranı (düzenlenen poliçe başına)", rule=rule))
            self.assertFalse(has(w, "lagging"), w)
            self.assertFalse(has(w, "read_after_days"), w)

    def test_read_after_days_shorter_than_the_name(self):
        w = warns(self.sc("İade Oranı (sipariş başına, 90 gün)", read_after_days=30,
                          rule="RPV artarsa ve 30 günlük pencere kapandıktan sonra iade marj içindeyse yayına al."))
        self.assertTrue(has(w, "read_after_days 30 is shorter than the 90-day window"), w)

    def test_decision_rule_must_mention_the_window(self):
        sc = self.sc("İade Oranı (sipariş başına, 90 gün)", read_after_days=90)
        self.assertTrue(has(warns(sc), "the rule never mentions that window"), warns(sc))
        for rule in ("RPV artarsa ve son kohortun 90 günlük penceresi kapandıktan sonra iade marj içindeyse yayına al.",
                     "Ship if RPV rises; the refund guardrail is read once its window has closed for the last cohort."):
            sc["preregistration"]["decision_rule"] = rule
            self.assertFalse(has(warns(sc), "never mentions"), rule)

    def test_primary_window(self):
        sc = base()
        sc["kpis"][0]["name"] = "Talep Oluşturma Oranı (ekranı açan kullanıcı başına, ilk açıştan 7 gün)"
        sc["preregistration"] = prereg(primary_kpi={"name": sc["kpis"][0]["name"], "direction": "increase"})
        self.assertTrue(has(warns(sc), "preregistration.primary_kpi"), warns(sc))
        sc["preregistration"]["primary_kpi"]["read_after_days"] = 7
        sc["preregistration"]["decision_rule"] = "Birincil KPI son kohortun 7 günlük penceresi kapandıktan sonra okunur."
        self.assertEqual(errs(sc), [])
        self.assertFalse(has(warns(sc), "preregistration.primary_kpi"), warns(sc))

    def test_prereg_only_mode_runs_the_same_checks(self):
        doc = {"preregistration": self.sc("İade Oranı (sipariş başına, 90 gün)")["preregistration"]}
        self.assertTrue(has(vsj.lint_prereg_only(doc, "en"), "90-day window"))


class TestComplement(unittest.TestCase):
    def sc(self, primary, guardrail):
        sc = base()
        sc["kpis"][0]["name"] = primary
        sc["kpis"][2] = {"name": guardrail, "role": "guardrail", "question": "Artmamalı."}
        return sc

    def test_same_denominator_complement_warns(self):
        w = warns(self.sc("Sipariş Tamamlama Oranı (sepete ulaşan kullanıcı başına)",
                          "Sepet Terk Oranı (sepete ulaşan kullanıcı başına)"))
        self.assertTrue(has(w, "looks like the complement of the primary"), w)

    def test_no_denominator_complement_warns(self):
        w = warns(self.sc("Form Tamamlama Oranı (forma başlayan kullanıcı başına)", "Sayfa Terk Oranı"))
        self.assertTrue(has(w, "complement"), w)
        w = warns(self.sc("Checkout Conversion Rate (per assigned user)", "Checkout Abandonment Rate (per assigned user)"))
        self.assertTrue(has(w, "complement"), w)

    def test_later_step_abandonment_is_fine(self):
        w = warns(self.sc("Kayıt Tamamlama Oranı (forma başlayan kullanıcı başına)",
                          "Ödeme Adımı Terk Oranı (ödeme adımına ulaşan kullanıcı başına)"))
        self.assertFalse(has(w, "complement"), w)

    def test_unrelated_guardrail_is_fine(self):
        w = warns(self.sc("Sipariş Tamamlama Oranı (sepete ulaşan kullanıcı başına)", "İade Oranı (sipariş başına, 30 gün)"))
        self.assertFalse(has(w, "complement"), w)


class TestOtherWarnings(unittest.TestCase):
    def test_intuition_with_medium_tier_must_say_where_the_tier_comes_from(self):
        sc = base()
        sc["evidence"] = {"level": "intuition", "note": "Bu ekran için ölçülmüş sinyal yok."}
        sc["ice"] = {"tier": "medium", "impact": 6, "confidence": 3, "ease": 7}
        self.assertTrue(has(warns(sc), "evidence.note"), warns(sc))
        sc["evidence"]["note"] = "Ölçülmüş sinyal yok; Medium kademesi kanıttan değil Impact ve Ease’ten geliyor."
        self.assertFalse(has(warns(sc), "evidence.note"), warns(sc))
        sc["evidence"] = {"level": "intuition"}
        sc["ice"] = {"tier": "low"}
        self.assertFalse(has(warns(sc), "evidence.note"), warns(sc))

    def test_native_app_addition_with_high_ease(self):
        sc = base()
        sc["device"] = "phone"
        sc["ice"] = {"tier": "low", "impact": 3, "confidence": 2, "ease": 9}
        sc["card"] = card()
        self.assertTrue(has(warns(sc), "Ease"), warns(sc))
        sc["ice"]["ease"] = 7
        self.assertFalse(has(warns(sc), "Ease"), warns(sc))
        sc["ice"]["ease"] = 9
        sc["device"] = "phone-web"
        sc["card"] = card(url="magaza.example")
        self.assertFalse(has(warns(sc), "Ease"), warns(sc))

    def test_regulated_flow_opens_its_rule_with_a_compliance_gate(self):
        sc = base()
        sc["title"] = "Poliçe özetini maddelere bölmek talep oranını artırır mı?"
        sc["preregistration"] = prereg()
        self.assertTrue(has(warns(sc), "compliance"), warns(sc))
        sc["preregistration"]["decision_rule"] = ("Uyum onayı test başlamadan alınmış olmalı. " +
                                                  sc["preregistration"]["decision_rule"])
        self.assertFalse(has(warns(sc), "compliance"), warns(sc))
        # Gate sentences come first; the compliance gate may be the second of them.
        sc["preregistration"]["decision_rule"] = ("Erişilebilirlik kontrolü geçmiş olmalı. Uyum onayı alınmış olmalı. "
                                                  "RPV artarsa yayına al.")
        self.assertFalse(has(warns(sc), "compliance"), warns(sc))
        sc["preregistration"]["decision_rule"] = "RPV artarsa yayına al. Uyum onayı sonradan alınır."
        self.assertTrue(has(warns(sc), "compliance"), warns(sc))

    def test_card_payment_is_not_a_regulated_flow(self):
        sc = base()
        sc["rationale"] = "Kredi kartı formunu sadeleştirmek ödeme adımını kısaltır."
        sc["preregistration"] = prereg()
        self.assertFalse(has(warns(sc), "compliance"), warns(sc))

    def test_title_and_quotes(self):
        sc = base()
        sc["title"] = "Açık kupon alanı sepet terkini artırır"
        sc["rationale"] = 'Kullanıcı "indirim arayayım" diye çıkıyor.'
        w = warns(sc)
        self.assertTrue(has(w, "title: does not end with '?'"), w)
        self.assertTrue(has(w, "rationale: straight quotes"), w)
        sc["lang"] = "en"
        self.assertFalse(has(warns(sc), "straight quotes"), warns(sc))

    def test_guardrail_without_question(self):
        sc = base()
        del sc["kpis"][2]["question"]
        self.assertTrue(has(warns(sc), "guardrail has no question/threshold text"), warns(sc))


class TestSchemaExtensions(unittest.TestCase):
    def test_trigger_and_pre_start_gates(self):
        sc = base()
        sc["preregistration"] = prereg(trigger="payment_step_viewed, iki kolda aynı noktada loglanır",
                                       pre_start_gates=["Uyum onayı", "Erişilebilirlik kontrolü"])
        self.assertEqual(errs(sc), [])
        sc["preregistration"]["pre_start_gates"] = "Uyum onayı"
        self.assertTrue(has(errs(sc), "preregistration.pre_start_gates"), errs(sc))
        sc["preregistration"]["pre_start_gates"] = []
        sc["preregistration"]["trigger"] = 5
        self.assertTrue(has(errs(sc), "preregistration.trigger"), errs(sc))

    def test_schema_uses_only_implemented_keywords(self):
        self.assertEqual(vsj.unsupported_keywords(SCHEMA), [])
        broken = copy.deepcopy(SCHEMA)
        broken["properties"]["title"]["maxLength"] = 10
        broken["properties"]["variants"]["uniqueItems"] = True
        self.assertEqual(vsj.unsupported_keywords(broken), ["maxLength", "uniqueItems"])

    def test_unknown_keyword_stops_the_cli(self):
        broken = copy.deepcopy(SCHEMA)
        broken["properties"]["title"]["maxLength"] = 10
        with tempfile.TemporaryDirectory() as tmp:
            sp = os.path.join(tmp, "schema.json")
            with open(sp, "w", encoding="utf-8") as fh:
                json.dump(broken, fh)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(vsj.main(["--schema", sp, EXAMPLE]), 2)
            self.assertIn("maxLength", err.getvalue())


class TestCli(unittest.TestCase):
    def run_cli(self, doc, *flags):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh, ensure_ascii=False)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = vsj.main(list(flags) + [path])
            return code, out.getvalue()

    def warned(self):
        sc = base()
        sc["kpis"][2]["name"] = "Kupon Kullanım Oranı"
        return sc

    def test_warnings_print_and_exit_zero(self):
        code, out = self.run_cli(self.warned(), "--lang", "en")
        self.assertEqual(code, 0, out)
        self.assertIn("1 warning(s) (exit code unaffected)", out)
        self.assertIn("no stated denominator", out)

    def test_strict_turns_warnings_into_errors(self):
        code, out = self.run_cli(self.warned(), "--lang", "en", "--strict")
        self.assertEqual(code, 1, out)
        self.assertIn("no stated denominator", out)

    def test_strict_with_a_clean_file_is_zero(self):
        code, out = self.run_cli(base(), "--strict")
        self.assertEqual(code, 0, out)

    def test_turkish_default(self):
        code, out = self.run_cli(self.warned())
        self.assertEqual(code, 0)
        self.assertIn("1 uyarı (çıkış kodunu etkilemez)", out)

    def test_prereg_only_still_works_and_warns(self):
        doc = {"preregistration": prereg(guardrails=[{"name": "İade Oranı (sipariş başına, 90 gün)",
                                                      "direction": "must_not_increase", "margin_relative": 0.05}])}
        code, out = self.run_cli(doc, "--prereg-only", "--lang", "en")
        self.assertEqual(code, 0, out)
        self.assertIn("90-day window", out)
        code, _ = self.run_cli(doc, "--prereg-only", "--strict")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
