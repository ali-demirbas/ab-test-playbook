#!/usr/bin/env python3
"""Validate scenario JSON files against templates/scenario.schema.json.

Stdlib-only by design (the repo takes no runtime dependencies), so this is a
deliberately small subset of JSON Schema rather than a general implementation:
type, required, enum, const, additionalProperties, minItems/maxItems,
minLength, pattern, minimum/maximum (inclusive and exclusive), oneOf and
dependentRequired. A schema that uses any other keyword stops the tool (exit
2) instead of being half-applied in silence.

On top of the shape, the cross-field rules a schema cannot express are checked
directly, because they are the whole point of having a schema here.

ERRORS (exit 1):

  * KPIs: exactly one with role "primary", and it is the first item (rule 2);
    at least one "guardrail" (rule 3); no metric listed twice; the primary is
    not a count ("Sayısı") and has no "users who saw it" denominator
  * the three boxes carry three to six items each
  * source "adapted" names its archive original in adapted_from (rule 8), and
    an archive/adapted scenario is never labelled "intuition" (rule 8)
  * ice.tier matches the product of its three scores when they are given
  * variants are "A" then "B", and the current page is A (rule 15)
  * card (optional; a scenario is valid without one): the mockup markup passes
    the builder's allowlist, ring placement matches card.difference, a ring has
    a label and no margin/padding, brand colours are real colours, a browser
    frame has its url and no tab bar, bottom_nav_active names a tab (all shared
    with build_card.py)
  * preregistration, when present: its variable, primary KPI and guardrail
    names are the scenario's own (whitespace and case normalised) and every
    guardrail of the KPI box is pre-registered; a guardrail is not the primary
    itself, is defined once, and is either margin-based or a check with a
    criterion; the alternative agrees with the primary direction; allocation
    keys are the variant ids and sum to 1; planned_n_per_arm / duration_days
    are numbers only when sample.traffic_known is true, and sample carries no
    number while traffic_known is false (rule 5)

WARNINGS (printed, exit code unaffected; --strict turns them into errors):

  * a rate with no stated denominator (any role); a count or a "saw it"
    denominator on a secondary or guardrail line. Lines labelled "yalnız B" /
    "B only" and pass/fail checks are skipped
  * a guardrail or primary whose name states a day window, or that is a known
    lagging outcome (returns, cancellation, churn …), with no read_after_days,
    unless the decision rule says the window is to be verified from product
    terms; a read_after_days the decision rule never mentions
  * a guardrail that looks like the complement of the primary
  * evidence "intuition" with ICE medium/high and no word on where the tier
    comes from; a native-app addition scored Ease 8 or more
  * a regulated-looking flow whose decision rule does not open with the
    compliance gate (rule 11)
  * the card's own warnings (a colour only in B, a difference outside the ring …)

What this tool deliberately does NOT check: whether `variable` really names a
single variable, whether the mechanism is causal, whether the primary KPI is
sensitive to the change. Those are judgement calls and belong to
agents/scenario-critic — a schema can only enforce shape, and the warnings
above are heuristics on names, not verdicts.

Usage:
  validate_scenario_json.py <file.json> [more.json ...]
  validate_scenario_json.py --strict <file.json>         # warnings count as errors
  validate_scenario_json.py --prereg-only <file.json>    # a bare {"preregistration": {...}}
  validate_scenario_json.py --lang en <file.json>        # messages in English (default: Turkish)
  validate_scenario_json.py --schema templates/scenario.schema.json <file.json>

The normal path is to validate the pre-registration inside the scenario's own
JSON. --prereg-only is the fallback when no scenario JSON exists: the file holds
exactly what ab-test-design emits, {"preregistration": {...}}, optionally with a
sibling "sample" object; without {"sample": {"traffic_known": true}} next to it,
planned_n_per_arm and duration_days must stay null.

Exit: 0 = all valid, 1 = violations found, 2 = usage error.
"""
import argparse
import json
import math
import os
import re
import sys

DEFAULT_SCHEMA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "templates",
    "scenario.schema.json",
)
DEFAULT_SCHEMA = os.path.normpath(DEFAULT_SCHEMA)

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(DEFAULT_SCHEMA), "scenario-card.html")

try:  # one source of truth for everything about the card: the builder's own rules
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build_card  # noqa: E402
    from build_card import ring_problems, DIFFERENCE_ALIASES  # noqa: E402
except ImportError:  # pragma: no cover - build_card ships next to this file
    build_card = None
    ring_problems = None
    DIFFERENCE_ALIASES = {}

# Keywords walk() applies. A keyword outside this list (and outside the two
# below) would be silently inert, so load_schema() refuses a schema that has one.
IMPLEMENTED_KEYWORDS = frozenset((
    "type", "required", "enum", "const", "additionalProperties", "minItems", "maxItems", "minLength",
    "pattern", "minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "oneOf", "dependentRequired",
    "properties", "items", "$ref",
))
# Written in the schema for other tools; the same rule is enforced by hand in
# check_kpi_roles (exactly one primary, at least one guardrail).
HANDLED_ELSEWHERE = frozenset(("allOf", "contains", "minContains", "maxContains"))
ANNOTATIONS = frozenset(("$schema", "$id", "$defs", "title", "description"))

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}

# Messages: Turkish by default (the playbook's home language), English with
# --lang en. Field paths are identical in both, so a message can be traced to
# the JSON whichever language it is printed in.
MSG = {
    "type": ("{path}: beklenen tür {exp}, gelen {got}", "{path}: expected type {exp}, got {got}"),
    "enum": ("{path}: {val!r} şu değerlerden biri değil: {opts}", "{path}: {val!r} is not one of {opts}"),
    "const": ("{path}: beklenen değer {exp!r}", "{path}: expected {exp!r}"),
    "minLength": ("{path}: en az {n} karakter olmalı", "{path}: shorter than minLength {n}"),
    "pattern": ("{path}: {val!r}, {pat} kalıbına uymuyor", "{path}: {val!r} does not match {pat}"),
    "minimum": ("{path}: en küçük değer {n}", "{path}: below minimum {n}"),
    "maximum": ("{path}: en büyük değer {n}", "{path}: above maximum {n}"),
    "exclusiveMinimum": ("{path}: {n} değerinden büyük olmalı", "{path}: must be greater than {n}"),
    "exclusiveMaximum": ("{path}: {n} değerinden küçük olmalı", "{path}: must be less than {n}"),
    "minItems": ("{path}: {have} öğe var, en az {n} olmalı", "{path}: has {have} item(s), minimum is {n}"),
    "maxItems": ("{path}: {have} öğe var, en fazla {n} olabilir", "{path}: has {have} item(s), maximum is {n}"),
    "required": ("{path}: zorunlu alan eksik: {key!r}", "{path}: missing required field {key!r}"),
    "unknown": ("{path}: tanımsız alan: {key!r}", "{path}: unknown field {key!r}"),
    "dependent": ("{path}: {key!r} alanı {need!r} alanını gerektirir", "{path}: {key!r} requires {need!r}"),
    "oneOf": ("{path}: oneOf dallarından {m}/{n} tanesi eşleşti (tam 1 olmalı)",
              "{path}: {m}/{n} oneOf branches matched (expected exactly 1)"),
    "closest": (" (en yakın dal: {detail})", " (closest branch: {detail})"),
    "primary_count": ("kpis: 'primary' rolünde {n} KPI var, tam 1 olmalı (kural 2)",
                      "kpis: found {n} KPI(s) with role 'primary', expected exactly 1 (rule 2)"),
    "primary_first": ("kpis[0]: ilk KPI birincil olmalı, gelen rol {role!r} (kural 2)",
                      "kpis[0]: the first KPI must be the primary one, got role {role!r} (rule 2)"),
    "no_guardrail": ("kpis: 'guardrail' rolünde KPI yok (kural 3)",
                     "kpis: no KPI with role 'guardrail' (rule 3)"),
    "adapted_from": ("adapted_from: kaynak 'adapted' ise uyarlanan arşiv senaryosunun adı yazılmalı (kural 8)",
                     "adapted_from: a scenario with source 'adapted' must name the archive scenario it adapts (rule 8)"),
    "evidence_downgrade": ("evidence.level: '{src}' kaynaklı bir senaryo 'intuition' olarak etiketlenmez; kanıt arşiv emsalidir (kural 8)",
                           "evidence.level: a '{src}' scenario is not labelled 'intuition'; its evidence is archive precedent (rule 8)"),
    "ice_tier": ("ice.tier: {i}×{c}×{e} = {p}, bu '{want}' bandına düşer, '{got}' yazılmış",
                 "ice.tier: {i}×{c}×{e} = {p} falls in the '{want}' band, not '{got}'"),
    "ring": ("card: {msg}", "card: {msg}"),
    "alloc": ("preregistration.allocation: paylar toplamı {s:g}, 1 olmalı",
              "preregistration.allocation: shares sum to {s:g}, expected 1"),
    "pre_primary": ("preregistration.primary_kpi: {got!r}, senaryonun birincil KPI'ı {want!r} ile aynı değil",
                    "preregistration.primary_kpi: {got!r} differs from the scenario's primary KPI {want!r}"),
    "pre_variable": ("preregistration.variable: {got!r}, senaryonun değişkeni {want!r} ile aynı değil",
                     "preregistration.variable: {got!r} differs from the scenario's variable {want!r}"),
    "pre_guardrail_missing": ("preregistration.guardrails[{i}]: {name!r} senaryonun KPI listesinde yok",
                              "preregistration.guardrails[{i}]: {name!r} is not in the scenario's KPI list"),
    "pre_guardrail_role": ("preregistration.guardrails[{i}]: {name!r} KPI listesinde '{role}' rolünde, guardrail olmalı",
                           "preregistration.guardrails[{i}]: {name!r} has role '{role}' in the KPI list, expected guardrail"),
    "pre_alternative": ("preregistration.alternative: '{alt}', birincil KPI yönü '{dir}' ile çelişiyor",
                        "preregistration.alternative: '{alt}' contradicts the primary KPI direction '{dir}'"),
    "pre_traffic": ("preregistration.{key}: trafik bilinmeden sayı verilmez; null bırakın ya da sample.traffic_known: true ekleyin (kural 5)",
                    "preregistration.{key}: no number without known traffic; leave it null or add sample.traffic_known: true (rule 5)"),
    "prereg_only_shape": ("(kök): beklenen biçim {{\"preregistration\": {{...}}}} (isteğe bağlı \"sample\" ile)",
                          "(root): expected {{\"preregistration\": {{...}}}} (optionally with \"sample\")"),
    "prereg_only_unknown": ("(kök): tanımsız alan: {key!r} (yalnızca preregistration ve sample)",
                            "(root): unknown field {key!r} (only preregistration and sample)"),
    "file_errors": ("{file}: {n} ihlal", "{file}: {n} violation(s)"),
    "file_ok": ("{file}: ok", "{file}: ok"),
    "invalid_json": ("{file}: GEÇERSİZ JSON: {err}", "{file}: INVALID JSON: {err}"),
    "total": ("TOPLAM: {n} ihlal", "TOTAL: {n} violation(s)"),
    "all_ok": ("Tüm senaryolar şemaya uyuyor.", "All scenarios conform to the schema."),
    "root": ("(kök)", "(root)"),
    # ---- v2.2: errors ----------------------------------------------------
    "kpi_dup": ("kpis[{i}]: {name!r} listede iki kez geçiyor (kpis[{j}]); her metrik bir kez ve tek rolle yazılır",
                "kpis[{i}]: {name!r} appears twice (kpis[{j}]); each metric is listed once, with one role"),
    "kpi_count_primary": ("{path}: birincil KPI {name!r} bir sayı (“Sayısı”); kollar farklı büyüklükteyse "
                          "karşılaştırılamaz, atanan ziyaretçi başına orana çevirin",
                          "{path}: primary KPI {name!r} is a count; arms of different size cannot be compared, "
                          "turn it into a rate per assigned visitor"),
    "kpi_saw_primary": ("{path}: birincil KPI {name!r} paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda "
                        "iki kolda karşılaştırılamaz (methodology → KPI denominator)",
                        "{path}: primary KPI {name!r} has a \"users who saw\" denominator; a denominator that exists "
                        "only in B cannot be compared across arms (methodology → KPI denominator)"),
    "variants_ids": ("variants: kimlikler sırasıyla \"A\" ve \"B\" olmalı, gelen {ids}",
                     "variants: ids must be \"A\" then \"B\", got {ids}"),
    "variants_current": ("variants[1].is_current: mevcut sayfa her zaman A'dır (kural 15)",
                         "variants[1].is_current: the current page is always A (rule 15)"),
    "sample_traffic_false": ("sample.{key}: traffic_known false iken sayı verilmez (kural 5)",
                             "sample.{key}: no number while traffic_known is false (rule 5)"),
    "alloc_keys": ("preregistration.allocation: allocation anahtarları varyant kimlikleriyle (A ve B) eşleşmeli, "
                   "gelen {keys}; bu şema iki kollu test tanımlar, üçüncü kol ayrı bir tasarımdır: her karşılaştırma "
                   "için ayrı bir ön kayıt bloğu yazın",
                   "preregistration.allocation: allocation keys must match variant ids (A and B), got {keys}; this "
                   "schema describes a two-arm test, a third arm is a different design: write one pre-registration "
                   "block per comparison"),
    "guardrail_mixed": ("preregistration.guardrails[{i}]: bir guardrail ya marjlıdır (direction + margin_relative) ya "
                        "da kontroldür (type: check + criterion); ikisi birden olmaz",
                        "preregistration.guardrails[{i}]: a guardrail is either margin-based (direction + "
                        "margin_relative) or a check (type: check + criterion), not both"),
    "pre_guardrail_is_primary": ("preregistration.guardrails[{i}]: {name!r} birincil KPI'ın kendisi; guardrail "
                                 "birincilin göremediği bağımsız bir zararı ölçer",
                                 "preregistration.guardrails[{i}]: {name!r} is the primary KPI itself; a guardrail "
                                 "measures an independent harm the primary cannot see"),
    "pre_guardrail_dup": ("preregistration.guardrails[{i}]: {name!r} iki kez tanımlı",
                          "preregistration.guardrails[{i}]: {name!r} is defined twice"),
    "pre_guardrail_dropped": ("preregistration.guardrails: senaryodaki guardrail {name!r} ön kayıtta yok; her "
                              "guardrail marjı ya da kontrol ölçütüyle ön kayda yazılır",
                              "preregistration.guardrails: scenario guardrail {name!r} is missing from the "
                              "pre-registration; every guardrail is pre-registered with its margin or check criterion"),
    "pre_direction": ("preregistration.primary_kpi.direction: '{pre}', hypothesis.expected_direction '{hyp}' ile çelişiyor",
                      "preregistration.primary_kpi.direction: '{pre}' contradicts hypothesis.expected_direction '{hyp}'"),
    "card_line": ("card: {msg}", "card: {msg}"),
    "plain": ("{msg}", "{msg}"),
    # ---- v2.2: warnings --------------------------------------------------
    "kpi_denominator": ("{path}: {name!r} bir oran ama paydası yazılmamış; varsayılan atanan ziyaretçidir, farklıysa "
                        "adına “(… başına)” ekleyin ya da denominator alanını doldurun",
                        "{path}: {name!r} is a rate with no stated denominator; assigned visitors is assumed, "
                        "otherwise add \"(per …)\" to the name or fill the denominator field"),
    "kpi_count": ("{path}: {role} KPI {name!r} bir sayı (“Sayısı”); kollar farklı büyüklükteyse karşılaştırılamaz, "
                  "atanan ziyaretçi başına orana çevirin",
                  "{path}: {role} KPI {name!r} is a count; arms of different size cannot be compared, turn it into "
                  "a rate per assigned visitor"),
    "kpi_saw": ("{path}: {role} KPI {name!r} paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda iki kolda "
                "karşılaştırılamaz",
                "{path}: {role} KPI {name!r} has a \"users who saw\" denominator; a denominator that exists only in B "
                "cannot be compared across arms"),
    "kpi_no_question": ("kpis[{i}]: guardrail için soru/eşik yazılmamış",
                        "kpis[{i}]: guardrail has no question/threshold text"),
    "complement": ("{path}: guardrail {name!r} birincil KPI'ın tümleyeni gibi görünüyor (aynı payda, 1 − birincil); "
                   "biri kazanırken diğeri bozulamaz, bağımsız bir zarar ölçün (sonraki adım, kalite, maliyet)",
                   "{path}: guardrail {name!r} looks like the complement of the primary (same denominator, "
                   "1 − primary); one cannot win while the other degrades, measure an independent harm (a later "
                   "step, quality, cost)"),
    "pre_window_missing": ("{path}: {name!r} {n} günlük bir pencere söylüyor ama read_after_days yok; "
                           "read_after_days: {n} ekleyin",
                           "{path}: {name!r} names a {n}-day window but has no read_after_days; add read_after_days: {n}"),
    "pre_window_short": ("{path}: read_after_days {have}, adındaki {n} günlük pencereden kısa",
                         "{path}: read_after_days {have} is shorter than the {n}-day window in its name"),
    "pre_lagging": ("{path}: {name!r} gecikmeli bir sonuç gibi görünüyor; takip penceresini read_after_days ile yazın "
                    "(pencere ürün koşullarından doğrulanacaksa bunu karar kuralında söyleyin)",
                    "{path}: {name!r} looks like a lagging outcome; declare its follow-up window with read_after_days "
                    "(if the window is still to be verified from product terms, say so in the decision rule)"),
    "rule_window": ("preregistration.decision_rule: {name!r} {n} gün sonra okunuyor ama karar kuralı bu pencereyi "
                    "söylemiyor; son kohortun {n} günlük penceresi kapanmadan yayına alınmayacağını yazın",
                    "preregistration.decision_rule: {name!r} is read after {n} days but the rule never mentions that "
                    "window; state that nothing ships before the last cohort's {n}-day window closes"),
    "pre_n_inputs": ("preregistration.planned_n_per_arm: örneklem mde ve power olmadan hesaplanamaz; ikisini de yazın "
                     "ya da null bırakın",
                     "preregistration.planned_n_per_arm: a sample size cannot be computed without mde and power; set "
                     "both or leave it null"),
    "pre_duration_inputs": ("preregistration.duration_days: süre sample.daily_visitors olmadan hesaplanamaz",
                            "preregistration.duration_days: a duration cannot be computed without sample.daily_visitors"),
    "pre_duration_need": ("preregistration.duration_days: {d} gün, {n}×2 / {v} ≈ {need} günden kısa",
                          "preregistration.duration_days: {d} days is shorter than {n}×2 / {v} ≈ {need} days"),
    "pre_duration_weeks": ("preregistration.duration_days: {d} gün iki tam haftadan kısa (methodology → external validity)",
                           "preregistration.duration_days: {d} days is under two full weeks (methodology → external validity)"),
    "pre_alpha": ("preregistration.alpha: {v:g}, alışılmış 0,1 üst sınırının üstünde; gerekçesini karar kuralına yazın",
                  "preregistration.alpha: {v:g} is above the conventional ceiling of 0.1; justify it in the decision rule"),
    "pre_power": ("preregistration.power: {v:g}, alışılmış 0,8 alt sınırının altında; test gerçek bir etkiyi kaçırabilir",
                  "preregistration.power: {v:g} is below the conventional floor of 0.8; the test can miss a real effect"),
    "ice_source": ("evidence.note: kanıt 'intuition' ama ICE '{tier}'; kademenin nereden geldiğini (Impact, Ease) "
                   "nota yazın",
                   "evidence.note: evidence is 'intuition' but ICE is '{tier}'; say in the note where the tier comes "
                   "from (Impact, Ease)"),
    "ice_ease_native": ("ice.ease: {ease}, ama bu yerel uygulamaya öğe ekleyen bir test (device phone, fark ekle); "
                        "uygulama sürümü ve mağaza onayı gerektiren eklemelerde Ease en çok 7 puanlanır",
                        "ice.ease: {ease}, but this test adds an element to a native app (device phone, difference "
                        "add); an addition that needs an app release and store review scores Ease 7 at most"),
    "regulated_gate": ("preregistration.decision_rule: senaryo düzenlemeye tabi bir akışta görünüyor ({word}); karar "
                       "kuralı uyum onayı kapısıyla başlamalı (kural 11), ör. “Uyum onayı test başlamadan alınmış olmalı.”",
                       "preregistration.decision_rule: the scenario looks like a regulated flow ({word}); the decision "
                       "rule opens with the compliance gate (rule 11), e.g. \"Compliance sign-off is obtained before "
                       "the test starts.\""),
    "title_question": ("title: başlık soru işaretiyle bitmiyor; iddia cümlesi testi önceden yargılar",
                       "title: does not end with '?'; an assertion prejudges the test"),
    "straight_quotes": ("{path}: düz tırnak var; Türkçe metinde kıvrık tırnak kullanın (kural 7)",
                        "{path}: straight quotes; use curly quotes in scenario text (rule 7)"),
    "basis_current": ("card.mockup_basis: 'shared_page' ise variants[0].is_current: true beklenir (kural 15)",
                      "card.mockup_basis: 'shared_page' expects variants[0].is_current: true (rule 15)"),
    "card_device": ("card.device: '{card}', senaryonun device değeri '{scn}' ile farklı",
                    "card.device: '{card}' differs from the scenario's device '{scn}'"),
    "file_warnings": ("{file}: {n} uyarı (çıkış kodunu etkilemez)", "{file}: {n} warning(s) (exit code unaffected)"),
    "file_warnings_strict": ("{file}: {n} uyarı (--strict: ihlal sayılır)",
                             "{file}: {n} warning(s) (--strict: counted as violations)"),
    "total_warnings": ("TOPLAM: {n} uyarı (çıkış kodunu etkilemez; --strict ile ihlal sayılır)",
                       "TOTAL: {n} warning(s) (exit code unaffected; --strict counts them as violations)"),
    "all_ok_strict": ("Tüm senaryolar şemaya uyuyor, uyarı yok.", "All scenarios conform to the schema, no warnings."),
    "bad_schema": ("şema, bu doğrulayıcının uygulamadığı anahtar sözcük(ler) kullanıyor: {kw}",
                   "schema uses keyword(s) this validator does not implement: {kw}"),
}


def msg(_lang, _key, **kw):
    tr, en = MSG[_key]
    return (en if _lang == "en" else tr).format(**kw)


def type_ok(value, expected):
    names = expected if isinstance(expected, list) else [expected]
    for name in names:
        py = TYPES.get(name)
        if py is None:
            continue
        if name in ("number", "integer") and isinstance(value, bool):
            continue  # bool is an int in Python; not a number here
        if isinstance(value, py):
            return True
    return False


def walk(value, schema, path, errors, root, lang="tr"):
    if "$ref" in schema:
        schema = resolve(schema["$ref"], root)
    shown = path or msg(lang, "root")

    if "oneOf" in schema:
        matches = 0
        closest = None
        for sub in schema["oneOf"]:
            trial = []
            walk(value, sub, path, trial, root, lang)
            if not trial:
                matches += 1
            elif closest is None or len(trial) < len(closest):
                closest = trial
        if matches != 1:
            text = msg(lang, "oneOf", path=shown, m=matches, n=len(schema["oneOf"]))
            if matches == 0 and closest:
                # The bare count says nothing actionable; the branch that came
                # closest usually names the one missing or extra field.
                text += msg(lang, "closest", detail="; ".join(closest))
            errors.append(text)
        return

    if "type" in schema and not type_ok(value, schema["type"]):
        errors.append(msg(lang, "type", path=shown, exp=schema["type"], got=type(value).__name__))
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(msg(lang, "enum", path=shown, val=value, opts=schema["enum"]))

    if "const" in schema and value != schema["const"]:
        errors.append(msg(lang, "const", path=shown, exp=schema["const"]))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(msg(lang, "minLength", path=shown, n=schema["minLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(msg(lang, "pattern", path=shown, val=value, pat=schema["pattern"]))

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(msg(lang, "minimum", path=shown, n=schema["minimum"]))
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(msg(lang, "maximum", path=shown, n=schema["maximum"]))
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(msg(lang, "exclusiveMinimum", path=shown, n=schema["exclusiveMinimum"]))
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errors.append(msg(lang, "exclusiveMaximum", path=shown, n=schema["exclusiveMaximum"]))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(msg(lang, "minItems", path=shown, have=len(value), n=schema["minItems"]))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(msg(lang, "maxItems", path=shown, have=len(value), n=schema["maxItems"]))
        if "items" in schema:
            for i, item in enumerate(value):
                walk(item, schema["items"], "%s[%d]" % (path, i), errors, root, lang)

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(msg(lang, "required", path=shown, key=key))
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(msg(lang, "unknown", path=shown, key=key))
        for key, sub in props.items():
            if key in value:
                walk(value[key], sub, "%s.%s" % (path, key) if path else key, errors, root, lang)
        for key, needs in schema.get("dependentRequired", {}).items():
            if key in value:
                for need in needs:
                    if need not in value:
                        errors.append(msg(lang, "dependent", path=shown, key=key, need=need))


def resolve(ref, root):
    if not ref.startswith("#/"):
        return {}
    node = root
    for part in ref[2:].split("/"):
        node = node.get(part, {})
    return node


def unsupported_keywords(schema):
    """Schema keywords walk() would ignore. Empty list = the schema is fully applied."""
    known = IMPLEMENTED_KEYWORDS | HANDLED_ELSEWHERE | ANNOTATIONS
    found = set()

    def visit(node):
        if not isinstance(node, dict):
            return
        found.update(k for k in node if k not in known)
        for key in ("properties", "$defs"):
            for sub in (node.get(key) or {}).values():
                visit(sub)
        for key in ("items", "contains"):
            visit(node.get(key))
        for key in ("oneOf", "allOf"):
            for sub in node.get(key) or []:
                visit(sub)

    visit(schema)
    return sorted(found)


class SchemaError(Exception):
    pass


def load_schema(path=DEFAULT_SCHEMA, lang="en"):
    """Read the schema and refuse one this validator cannot fully apply."""
    with open(path, encoding="utf-8") as fh:
        schema = json.load(fh)
    unknown = unsupported_keywords(schema)
    if unknown:
        raise SchemaError(msg(lang, "bad_schema", kw=", ".join(unknown)))
    return schema


def norm(text):
    """Whitespace- and case-insensitive comparison key for names typed twice."""
    return " ".join(str(text or "").split()).casefold()


# ----------------------------------------------------------- reading KPI names
#
# These are heuristics on names. They feed warnings (and two errors on the
# primary); they never decide whether a metric is right for the test.

PER_RE = re.compile(r"başına|\bper\b", re.IGNORECASE)
RATE_RE = re.compile(r"\boran[ıi]?\b|\boranları\b|\brate\b|\bCR\b|\bCTR\b|%|\byüzde|\bshare\b|\bpay[ıi]\b", re.IGNORECASE)
COUNT_RE = re.compile(r"sayısı|adedi|\bcount\b|\bnumber\s+of\b", re.IGNORECASE)
SAW_RE = re.compile(r"\bgör(?:en|üp|enler|dükten)|\bwho\s+(?:saw|see|viewed)\b|\bsaw\b", re.IGNORECASE)
B_ONLY_RE = re.compile(r"yalnız(?:ca)?\s+B\b|sadece\s+B\b|\bB\s+only\b|\bonly\s+(?:in\s+)?B\b")
CHECK_NAME_RE = re.compile(r"kontrol|denetim|geçti\s*/\s*kaldı|\bcheck\b|pass\s*/\s*fail|\breview\b", re.IGNORECASE)
WINDOW_RE = re.compile(
    r"(\d+)\s*[- ]?(günlük|günde|gün|days?|haftalık|hafta|weeks?|aylık|ay|months?)\b", re.IGNORECASE)
LAGGING_RE = re.compile(
    r"iade|iptal|cayma|durdurma|yenileme|elde\s+tutma|tekrar\s+satın|churn|\breturns?\b|refund|cancel|retention|"
    r"renewal|\brepeat\b", re.IGNORECASE)
# The skill's wording for a statutory or product window the playbook does not
# know: the rule says it is verified before the test starts.
VERIFY_RE = re.compile(r"ürün\s+koşullarından\s+doğrulan|verified\s+from\s+(?:the\s+)?product\s+terms", re.IGNORECASE)
RULE_WINDOW_RE = re.compile(r"pencere|window|kapan", re.IGNORECASE)
COMPLETE_RE = re.compile(r"tamamlama|dönüşüm|kayıt|completion|conversion", re.IGNORECASE)
ABANDON_RE = re.compile(r"terk\s+oran|abandon", re.IGNORECASE)
REGULATED_RE = re.compile(
    r"sigorta|emeklilik|kredi(?!\s+kart)|poliçe|insurance|pension|\bcredit\b(?!\s+card)|consent|KVKK", re.IGNORECASE)
REGULATED_CASED_RE = re.compile(r"\bBES\b")
GATE_RE = re.compile(r"uyum|compliance|hukuk|legal|mevzuat|regulat|sign-?off", re.IGNORECASE)
SHIP_RE = re.compile(r"yayına\s+al|kontrolde\s+kal|\bship|roll\s*out|\blaunch|keep\s+(?:the\s+)?control", re.IGNORECASE)
TIER_SOURCE_RE = re.compile(r"kademe|\btier\b|impact|\bease\b|\betki\b|kolaylık|\bICE\b", re.IGNORECASE)

_GLOSSARY = []  # loaded once, on first use: [glossary dict or None]


def _glossary():
    if not _GLOSSARY:
        try:
            import validate_scenarios
            _GLOSSARY.append(validate_scenarios.load_glossary())
        except Exception:  # the glossary is optional; without it nothing is exempted
            _GLOSSARY.append(None)
    return _GLOSSARY[0]


def _in_glossary(name):
    glossary = _glossary()
    if not glossary:
        return False
    import validate_scenarios
    return validate_scenarios.glossary_status(" ".join(str(name).split()), glossary) != "missing"


def denominator_of(name, field=None):
    """The denominator a KPI line states, normalised, or '' when it states none.

    "… Oranı (sepete ulaşan kullanıcı başına, 30 gün)" → "sepete ulaşan kullanıcı".
    A parenthesis that only gives a window or an abbreviation is not one.
    """
    if isinstance(field, str) and field.strip():
        return norm(field)
    text = str(name or "")
    m = re.search(r"([^(),;]*?)\s+başına", text, re.IGNORECASE)
    if m:
        return norm(m.group(1))
    m = re.search(r"\bper\s+([^(),;]+)", text, re.IGNORECASE)
    if m:
        return norm(m.group(1))
    return ""


def window_days(name):
    """Largest day window a name states ("90 gün", "2 hafta", "30 days"), or None."""
    best = None
    for num, unit in WINDOW_RE.findall(str(name or "")):
        unit = unit.lower()
        days = int(num) * (7 if unit.startswith(("hafta", "week")) else 30 if unit.startswith(("ay", "month")) else 1)
        best = days if best is None else max(best, days)
    return best


def kpi_entries(scenario):
    """The scenario's KPI lines as the name checks read them."""
    kpis = scenario.get("kpis") if isinstance(scenario.get("kpis"), list) else []
    pre = scenario.get("preregistration") if isinstance(scenario.get("preregistration"), dict) else {}
    checks = {norm(g.get("name")) for g in pre.get("guardrails") or []
              if isinstance(g, dict) and g.get("type") == "check"}
    out = []
    for i, k in enumerate(kpis):
        if not isinstance(k, dict) or not isinstance(k.get("name"), str):
            continue
        out.append({"path": "kpis[%d]" % i, "role": k.get("role"), "name": k["name"],
                    "denominator": k.get("denominator"),
                    "is_check": norm(k["name"]) in checks or bool(CHECK_NAME_RE.search(k["name"]))})
    return out


def prereg_entries(pre):
    """The same view over a bare pre-registration block."""
    out = []
    if not isinstance(pre, dict):
        return out
    pkpi = pre.get("primary_kpi")
    if isinstance(pkpi, dict) and isinstance(pkpi.get("name"), str):
        out.append({"path": "preregistration.primary_kpi", "role": "primary", "name": pkpi["name"],
                    "denominator": pkpi.get("denominator"), "is_check": False})
    for i, g in enumerate(pre.get("guardrails") or []):
        if isinstance(g, dict) and isinstance(g.get("name"), str):
            out.append({"path": "preregistration.guardrails[%d]" % i, "role": "guardrail", "name": g["name"],
                        "denominator": g.get("denominator"),
                        "is_check": g.get("type") == "check" or bool(CHECK_NAME_RE.search(g["name"]))})
    return out


def kpi_name_problems(entries, lang="tr", glossary_ok=False):
    """Denominator rules on KPI names. Returns (errors, warnings).

    A count or a "saw it" denominator is an error on the primary (the decision
    metric cannot be compared between arms) and a warning on the other lines.
    A rate with no denominator is a warning on every line: assigned visitors is
    the default when nothing is written. Pass/fail checks and lines labelled
    "yalnız B" / "B only" (a diagnostic that exists in one arm) are skipped.
    `glossary_ok`: an archive scenario's canonical glossary names inherit the
    glossary's denominator; a produced scenario writes it out.
    """
    errors, warnings = [], []
    for e in entries:
        name, path, role = e["name"], e["path"], e["role"]
        if e["is_check"] or B_ONLY_RE.search(name):
            continue
        has_per = bool(PER_RE.search(name)) or bool(isinstance(e.get("denominator"), str) and e["denominator"].strip())
        primary = role == "primary"
        if COUNT_RE.search(name) and not has_per:
            if primary:
                errors.append(msg(lang, "kpi_count_primary", path=path, name=name))
            else:
                warnings.append(msg(lang, "kpi_count", path=path, role=role, name=name))
        if SAW_RE.search(name):
            if primary:
                errors.append(msg(lang, "kpi_saw_primary", path=path, name=name))
            else:
                warnings.append(msg(lang, "kpi_saw", path=path, role=role, name=name))
        if RATE_RE.search(name) and not has_per and not (glossary_ok and _in_glossary(name)):
            warnings.append(msg(lang, "kpi_denominator", path=path, name=name))
    return errors, warnings


def complement_warnings(entries, lang="tr"):
    """A guardrail that is 1 − primary: completion against abandonment of the
    same step over the same (or no stated) denominator."""
    primary = next((e for e in entries if e["role"] == "primary"), None)
    if primary is None or not COMPLETE_RE.search(primary["name"]):
        return []
    out = []
    p_den = denominator_of(primary["name"], primary.get("denominator"))
    for e in entries:
        if e["role"] != "guardrail" or e["is_check"] or not ABANDON_RE.search(e["name"]):
            continue
        g_den = denominator_of(e["name"], e.get("denominator"))
        if p_den and g_den and p_den != g_den:
            continue  # a different population: a later step, which is what a guardrail should be
        out.append(msg(lang, "complement", path=e["path"], name=e["name"]))
    return out


# ------------------------------------------------------------------ the checks

def check_kpi_roles(scenario, errors, lang="tr"):
    """Rules 2 and 3 on the KPI list.

    Checked directly rather than via the generic walker: they are the reason
    this schema exists, and a silent miss here would let a scenario ship with
    five equally-weighted metrics and no guardrail — exactly what rules 2 and 3
    forbid. Rule 2 also fixes the order: the first item IS the primary metric.
    A metric listed twice (a "guardrail" carrying the primary's own name) is
    refused here too: the later duplicate used to win the role lookup.
    """
    kpis = scenario.get("kpis")
    if not isinstance(kpis, list):
        return
    roles = [k.get("role") for k in kpis if isinstance(k, dict)]
    primaries = roles.count("primary")
    if primaries != 1:
        errors.append(msg(lang, "primary_count", n=primaries))
    elif roles and roles[0] != "primary":
        errors.append(msg(lang, "primary_first", role=roles[0]))
    if roles.count("guardrail") < 1:
        errors.append(msg(lang, "no_guardrail"))
    seen = {}
    for i, k in enumerate(kpis):
        if not isinstance(k, dict) or not isinstance(k.get("name"), str):
            continue
        key = norm(k["name"])
        if key in seen:
            errors.append(msg(lang, "kpi_dup", i=i, name=k["name"], j=seen[key]))
        else:
            seen[key] = i
    name_errors, _ = kpi_name_problems(kpi_entries(scenario), lang)
    errors.extend(name_errors)


def check_variants(scenario, errors, lang="tr"):
    variants = scenario.get("variants")
    if not isinstance(variants, list) or len(variants) != 2 or not all(isinstance(v, dict) for v in variants):
        return
    ids = [v.get("id") for v in variants]
    if all(i in ("A", "B") for i in ids) and ids != ["A", "B"]:
        errors.append(msg(lang, "variants_ids", ids=ids))
    if variants[1].get("is_current") is True:
        errors.append(msg(lang, "variants_current"))


def check_source(scenario, errors, lang="tr"):
    source = scenario.get("source")
    if source == "adapted" and not str(scenario.get("adapted_from") or "").strip():
        errors.append(msg(lang, "adapted_from"))
    evidence = scenario.get("evidence")
    level = evidence.get("level") if isinstance(evidence, dict) else None
    if source in ("archive", "adapted") and level == "intuition":
        errors.append(msg(lang, "evidence_downgrade", src=source))


def ice_band(product):
    if product >= 300:
        return "high"
    if product >= 125:
        return "medium"
    return "low"


def check_ice(scenario, errors, lang="tr"):
    ice = scenario.get("ice")
    if not isinstance(ice, dict):
        return
    scores = [ice.get(k) for k in ("impact", "confidence", "ease")]
    if not all(isinstance(s, int) and not isinstance(s, bool) for s in scores):
        return
    product = scores[0] * scores[1] * scores[2]
    want = ice_band(product)
    if ice.get("tier") in ("high", "medium", "low") and ice["tier"] != want:
        errors.append(msg(lang, "ice_tier", i=scores[0], c=scores[1], e=scores[2], p=product,
                          want=want, got=ice["tier"]))


def check_sample(sample, errors, lang="tr"):
    """Rule 5: a number next to traffic_known: false is a promise without traffic."""
    if not isinstance(sample, dict) or sample.get("traffic_known") is not False:
        return
    for key in ("daily_visitors", "estimated_days"):
        if sample.get(key) is not None:
            errors.append(msg(lang, "sample_traffic_false", key=key))


_CLASSES = []  # the default template's component classes, read once


def _template_classes():
    if not _CLASSES:
        names = frozenset()
        if build_card is not None and os.path.isfile(DEFAULT_TEMPLATE):
            with open(DEFAULT_TEMPLATE, encoding="utf-8") as fh:
                names = build_card.component_classes(fh.read())
        _CLASSES.append(names)
    return _CLASSES[0]


def card_difference(card):
    diff = card.get("difference")
    if not isinstance(diff, str):
        return None
    diff = DIFFERENCE_ALIASES.get(diff.lower(), diff.lower())
    return diff if diff in ("change", "add", "move", "remove") else None


def card_device(scenario, card):
    for value in (card.get("device"), scenario.get("device")):
        if isinstance(value, str) and value:
            return value
    return "phone"


def _card_report(scenario, card, lang):
    """(errors, warnings) of the two mockups, from the builder's own function."""
    a, b = card.get("variant_a"), card.get("variant_b")
    diff = card_difference(card)
    # Both must be strings: the walker has already reported the wrong type, and
    # markup rules have nothing to say about a number.
    if build_card is None or not isinstance(a, str) or not isinstance(b, str) or diff is None:
        return [], []
    return build_card.card_problems(diff, a, b, card.get("shift_note_b"), lang=lang,
                                    variable=scenario.get("variable"), classes=_template_classes())


def check_card(scenario, errors, lang="tr"):
    card = scenario.get("card")
    if not isinstance(card, dict) or build_card is None:
        return
    card_errors, _ = _card_report(scenario, card, lang)
    errors.extend(msg(lang, "card_line", msg=p) for p in card_errors)
    brand = card.get("brand")
    if isinstance(brand, dict):
        for key in ("primary", "on_primary"):
            value = brand.get(key)
            if isinstance(value, str) and value:
                problem = build_card.color_problem(value, key, lang)
                # The schema's pattern already speaks for a value that is not colour syntax at all.
                if problem and not any(e.startswith("card.brand.%s:" % key) for e in errors):
                    errors.append(msg(lang, "card_line", msg=problem))
    nav = card.get("bottom_nav")
    url = card.get("url")
    errors.extend(build_card.frame_problems(card_device(scenario, card), url if isinstance(url, str) else None,
                                            nav if isinstance(nav, list) else None,
                                            card.get("bottom_nav_active"), lang))


def check_prereg_block(pre, sample, errors, lang="tr"):
    """Rules internal to the pre-registration block (also run in --prereg-only)."""
    if not isinstance(pre, dict):
        return
    alloc = pre.get("allocation")
    if isinstance(alloc, dict):
        extra = sorted(k for k in alloc if k not in ("A", "B"))
        if extra:
            errors.append(msg(lang, "alloc_keys", keys=sorted(alloc)))
        shares = [v for v in alloc.values()
                  if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if shares and abs(sum(shares) - 1.0) > 1e-6:
            errors.append(msg(lang, "alloc", s=sum(shares)))
    pkpi = pre.get("primary_kpi")
    direction = pkpi.get("direction") if isinstance(pkpi, dict) else None
    alt = pre.get("alternative")
    if (direction == "increase" and alt == "less") or (direction == "decrease" and alt == "greater"):
        errors.append(msg(lang, "pre_alternative", alt=alt, dir=direction))
    traffic_known = isinstance(sample, dict) and sample.get("traffic_known") is True
    for key in ("planned_n_per_arm", "duration_days"):
        if pre.get(key) is not None and not traffic_known:
            errors.append(msg(lang, "pre_traffic", key=key))
    check_sample(sample, errors, lang)

    primary_name = norm(pkpi.get("name")) if isinstance(pkpi, dict) and isinstance(pkpi.get("name"), str) else None
    seen = set()
    for i, g in enumerate(pre.get("guardrails") or []):
        if not isinstance(g, dict):
            continue
        if (g.get("type") == "check" or "criterion" in g) and ("margin_relative" in g or "direction" in g):
            errors.append(msg(lang, "guardrail_mixed", i=i))
        if not isinstance(g.get("name"), str):
            continue
        key = norm(g["name"])
        if primary_name and key == primary_name:
            errors.append(msg(lang, "pre_guardrail_is_primary", i=i, name=g["name"]))
        if key in seen:
            errors.append(msg(lang, "pre_guardrail_dup", i=i, name=g["name"]))
        seen.add(key)


def refine_prereg_errors(pre, errors, lang="tr"):
    """Drop the walker's generic lines where a check above says the same thing
    in words a person can act on ("unknown field 'C'" for a third arm, a bare
    "0/2 oneOf branches matched" for a guardrail that is both margin and check)."""
    if not isinstance(pre, dict):
        return errors
    drop_exact, drop_prefix = set(), []
    alloc = pre.get("allocation")
    if isinstance(alloc, dict):
        for key in alloc:
            if key not in ("A", "B"):
                drop_exact.add(msg(lang, "unknown", path="preregistration.allocation", key=key))
    for i, g in enumerate(pre.get("guardrails") or []):
        if isinstance(g, dict) and (g.get("type") == "check" or "criterion" in g) and (
                "margin_relative" in g or "direction" in g):
            drop_prefix.append(msg(lang, "oneOf", path="preregistration.guardrails[%d]" % i, m=0, n=2))
    return [e for e in errors if e not in drop_exact and not any(e.startswith(p) for p in drop_prefix)]


def check_preregistration(scenario, errors, lang="tr"):
    """Cross-field rules between the pre-registration block and the scenario.

    A schema can't say "the pre-registered primary KPI is the same metric the
    scenario marks primary"; these are checked here. A mismatch means the plan
    fixed before launch and the scenario that was reviewed describe two
    different tests. Both directions are checked for guardrails: a name the KPI
    box does not have, and a KPI-box guardrail the block dropped.
    """
    pre = scenario.get("preregistration")
    if not isinstance(pre, dict):
        check_sample(scenario.get("sample"), errors, lang)
        return
    check_prereg_block(pre, scenario.get("sample"), errors, lang)

    kpis = scenario.get("kpis") if isinstance(scenario.get("kpis"), list) else []
    by_name = {}
    for k in kpis:
        if isinstance(k, dict):
            by_name.setdefault(norm(k.get("name")), k)  # the first listing wins; a duplicate is its own error

    pkpi = pre.get("primary_kpi")
    primaries = [k.get("name") for k in kpis if isinstance(k, dict) and k.get("role") == "primary"]
    if isinstance(pkpi, dict) and len(primaries) == 1 and norm(pkpi.get("name")) != norm(primaries[0]):
        errors.append(msg(lang, "pre_primary", got=pkpi.get("name"), want=primaries[0]))

    if "variable" in pre and "variable" in scenario and norm(pre["variable"]) != norm(scenario["variable"]):
        errors.append(msg(lang, "pre_variable", got=pre["variable"], want=scenario["variable"]))

    hyp = scenario.get("hypothesis")
    expected = hyp.get("expected_direction") if isinstance(hyp, dict) else None
    direction = pkpi.get("direction") if isinstance(pkpi, dict) else None
    if expected in ("increase", "decrease") and direction in ("increase", "decrease") and expected != direction:
        errors.append(msg(lang, "pre_direction", pre=direction, hyp=expected))

    guards = pre.get("guardrails")
    if isinstance(guards, list) and by_name:
        listed = set()
        for i, g in enumerate(guards):
            if not isinstance(g, dict) or "name" not in g:
                continue
            listed.add(norm(g["name"]))
            match = by_name.get(norm(g["name"]))
            if match is None:
                errors.append(msg(lang, "pre_guardrail_missing", i=i, name=g["name"]))
            elif match.get("role") != "guardrail":
                errors.append(msg(lang, "pre_guardrail_role", i=i, name=g["name"], role=match.get("role")))
        for k in kpis:
            if isinstance(k, dict) and k.get("role") == "guardrail" and isinstance(k.get("name"), str) \
                    and norm(k["name"]) not in listed:
                errors.append(msg(lang, "pre_guardrail_dropped", name=k["name"]))


def validate(scenario, schema, lang="tr"):
    """Errors only. lint() returns the warnings."""
    errors = []
    walk(scenario, schema, "", errors, schema, lang)
    if isinstance(scenario, dict):
        check_kpi_roles(scenario, errors, lang)
        check_variants(scenario, errors, lang)
        check_source(scenario, errors, lang)
        check_ice(scenario, errors, lang)
        check_card(scenario, errors, lang)
        check_preregistration(scenario, errors, lang)
        errors = refine_prereg_errors(scenario.get("preregistration"), errors, lang)
    return errors


def validate_prereg_only(doc, schema, lang="tr"):
    """A bare {"preregistration": {...}} block, as ab-test-design emits it."""
    errors = []
    if not isinstance(doc, dict) or "preregistration" not in doc:
        return [msg(lang, "prereg_only_shape")]
    for key in doc:
        if key not in ("preregistration", "sample"):
            errors.append(msg(lang, "prereg_only_unknown", key=key))
    props = schema.get("properties", {})
    walk(doc["preregistration"], props.get("preregistration", {}), "preregistration", errors, schema, lang)
    if "sample" in doc:
        walk(doc["sample"], props.get("sample", {}), "sample", errors, schema, lang)
    check_prereg_block(doc["preregistration"], doc.get("sample"), errors, lang)
    name_errors, _ = kpi_name_problems(prereg_entries(doc["preregistration"]), lang)
    errors.extend(name_errors)
    return refine_prereg_errors(doc["preregistration"], errors, lang)


# -------------------------------------------------------------------- warnings

def prereg_warnings(pre, sample, lang="tr"):
    """Warnings internal to the pre-registration block (both modes)."""
    out = []
    if not isinstance(pre, dict):
        return out
    rule = pre.get("decision_rule") if isinstance(pre.get("decision_rule"), str) else ""
    to_be_verified = bool(VERIFY_RE.search(rule))
    windows = []  # (name, days) of everything read after a window

    def lagging(path, item):
        name = item.get("name")
        if not isinstance(name, str):
            return
        have = item.get("read_after_days")
        have = have if isinstance(have, int) and not isinstance(have, bool) else None
        stated = window_days(name)
        if have is not None:
            windows.append((name, have))
            if stated and have < stated:
                out.append(msg(lang, "pre_window_short", path=path, have=have, n=stated))
        elif to_be_verified:
            return
        elif stated:
            out.append(msg(lang, "pre_window_missing", path=path, name=name, n=stated))
        elif LAGGING_RE.search(name):
            out.append(msg(lang, "pre_lagging", path=path, name=name))

    pkpi = pre.get("primary_kpi")
    if isinstance(pkpi, dict):
        lagging("preregistration.primary_kpi", pkpi)
    for i, g in enumerate(pre.get("guardrails") or []):
        if isinstance(g, dict) and g.get("type") != "check":
            lagging("preregistration.guardrails[%d]" % i, g)
        elif isinstance(g, dict) and isinstance(g.get("read_after_days"), int) and isinstance(g.get("name"), str):
            windows.append((g["name"], g["read_after_days"]))

    if windows and not RULE_WINDOW_RE.search(rule):
        for name, days in windows:
            if not re.search(r"(?<!\d)%d(?!\d)" % days, rule):
                out.append(msg(lang, "rule_window", name=name, n=days))

    def num(value):
        return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None

    alpha, power = num(pre.get("alpha")), num(pre.get("power"))
    if alpha is not None and alpha > 0.1:
        out.append(msg(lang, "pre_alpha", v=alpha))
    if power is not None and power < 0.8:
        out.append(msg(lang, "pre_power", v=power))
    planned, days = num(pre.get("planned_n_per_arm")), num(pre.get("duration_days"))
    visitors = num(sample.get("daily_visitors")) if isinstance(sample, dict) else None
    if planned is not None and (num(pre.get("mde")) is None or power is None):
        out.append(msg(lang, "pre_n_inputs"))
    if days is not None:
        if visitors is None:
            out.append(msg(lang, "pre_duration_inputs"))
        elif planned is not None:
            need = int(math.ceil(planned * 2.0 / visitors))
            if days < need:
                out.append(msg(lang, "pre_duration_need", d=days, n=planned, v=visitors, need=need))
        if days < 14:
            out.append(msg(lang, "pre_duration_weeks", d=days))
    return out


def _text_fields(scenario):
    """(path, text) of the scenario's prose, for the quote check. The mockup
    markup is not prose: its attribute quotes are straight by necessity."""
    for key in ("title", "rationale", "objection", "variable"):
        if isinstance(scenario.get(key), str):
            yield key, scenario[key]
    hyp = scenario.get("hypothesis")
    if isinstance(hyp, dict):
        for key in ("change", "mechanism"):
            if isinstance(hyp.get(key), str):
                yield "hypothesis.%s" % key, hyp[key]
    for box in ("test_items", "dont_items"):
        for i, item in enumerate(scenario.get(box) if isinstance(scenario.get(box), list) else []):
            text = item if isinstance(item, str) else " ".join(
                str(item.get(k, "")) for k in ("label", "text")) if isinstance(item, dict) else ""
            yield "%s[%d]" % (box, i), text
    for i, k in enumerate(scenario.get("kpis") if isinstance(scenario.get("kpis"), list) else []):
        if isinstance(k, dict):
            yield "kpis[%d]" % i, "%s %s" % (k.get("name", ""), k.get("question", ""))
    for i, v in enumerate(scenario.get("variants") if isinstance(scenario.get("variants"), list) else []):
        if isinstance(v, dict) and isinstance(v.get("description"), str):
            yield "variants[%d].description" % i, v["description"]


def opens_with_compliance_gate(rule):
    """Gate sentences come first in a decision rule (what must be closed before
    the test takes traffic); the ship condition follows. True when one of those
    leading sentences is the compliance gate."""
    for sentence in re.split(r"(?<=[.;!?])\s+", rule.strip()):
        if GATE_RE.search(sentence):
            return True
        if SHIP_RE.search(sentence):
            return False
    return False


def lint(scenario, schema=None, lang="tr", include_card=True):
    """Warnings: things worth a second look that are not violations.

    `schema` is accepted for symmetry with validate() and not used. With
    include_card=False the mockup warnings are left out (the builder reports
    those itself when it builds).
    """
    out = []
    if not isinstance(scenario, dict):
        return out
    entries = kpi_entries(scenario)
    _, name_warnings = kpi_name_problems(entries, lang, glossary_ok=scenario.get("source") == "archive")
    out.extend(name_warnings)
    out.extend(complement_warnings(entries, lang))
    kpis = scenario.get("kpis") if isinstance(scenario.get("kpis"), list) else []
    for i, k in enumerate(kpis):
        if isinstance(k, dict) and k.get("role") == "guardrail" and not str(k.get("question") or "").strip():
            out.append(msg(lang, "kpi_no_question", i=i))

    title = scenario.get("title")
    if isinstance(title, str) and title.strip() and not title.rstrip().endswith("?"):
        out.append(msg(lang, "title_question"))
    if scenario.get("lang", "tr") == "tr":
        for path, text in _text_fields(scenario):
            if '"' in text:
                out.append(msg(lang, "straight_quotes", path=path))

    evidence, ice = scenario.get("evidence"), scenario.get("ice")
    if isinstance(evidence, dict) and isinstance(ice, dict) and evidence.get("level") == "intuition" \
            and ice.get("tier") in ("medium", "high") and not TIER_SOURCE_RE.search(str(evidence.get("note") or "")):
        out.append(msg(lang, "ice_source", tier=ice["tier"]))

    card = scenario.get("card") if isinstance(scenario.get("card"), dict) else None
    if card is not None:
        ease = ice.get("ease") if isinstance(ice, dict) else None
        if isinstance(ease, int) and not isinstance(ease, bool) and ease >= 8 \
                and card_device(scenario, card) == "phone" and card_difference(card) == "add":
            out.append(msg(lang, "ice_ease_native", ease=ease))
        variants = scenario.get("variants")
        first = variants[0] if isinstance(variants, list) and variants and isinstance(variants[0], dict) else {}
        if card.get("mockup_basis") == "shared_page" and first.get("is_current") is not True:
            out.append(msg(lang, "basis_current"))
        if isinstance(card.get("device"), str) and isinstance(scenario.get("device"), str) \
                and card["device"] != scenario["device"]:
            out.append(msg(lang, "card_device", card=card["device"], scn=scenario["device"]))

    pre = scenario.get("preregistration")
    if isinstance(pre, dict):
        out.extend(prereg_warnings(pre, scenario.get("sample"), lang))
        rule = pre.get("decision_rule") if isinstance(pre.get("decision_rule"), str) else ""
        context = " ".join(str(scenario.get(k) or "") for k in ("stage", "title", "rationale"))
        word = REGULATED_RE.search(context) or REGULATED_CASED_RE.search(context)
        if word and rule and not opens_with_compliance_gate(rule):
            out.append(msg(lang, "regulated_gate", word=word.group(0)))

    if include_card and card is not None:
        _, card_warnings = _card_report(scenario, card, lang)
        out.extend(msg(lang, "card_line", msg=w) for w in card_warnings)
    return out


def lint_prereg_only(doc, lang="tr"):
    """Warnings for a bare {"preregistration": {...}} block."""
    if not isinstance(doc, dict) or not isinstance(doc.get("preregistration"), dict):
        return []
    pre = doc["preregistration"]
    entries = prereg_entries(pre)
    _, out = kpi_name_problems(entries, lang)
    out.extend(complement_warnings(entries, lang))
    out.extend(prereg_warnings(pre, doc.get("sample"), lang))
    return out


def main(argv):
    ap = argparse.ArgumentParser(description="Validate scenario JSON against the schema.")
    ap.add_argument("files", nargs="+", help="scenario JSON file(s)")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA)
    ap.add_argument("--prereg-only", action="store_true",
                    help="each file is a bare {\"preregistration\": {...}} block (the fallback when no scenario JSON exists)")
    ap.add_argument("--strict", action="store_true", help="warnings count as violations (exit 1)")
    ap.add_argument("--lang", choices=("tr", "en"), default="tr", help="message language (default: tr)")
    args = ap.parse_args(argv)
    lang = args.lang

    if not os.path.isfile(args.schema):
        sys.stderr.write("validate_scenario_json: no schema at %s\n" % args.schema)
        return 2
    try:
        schema = load_schema(args.schema, lang)
    except SchemaError as exc:
        sys.stderr.write("validate_scenario_json: %s\n" % exc)
        return 2

    total_errors = total_warnings = 0
    for path in args.files:
        if not os.path.isfile(path):
            sys.stderr.write("validate_scenario_json: no such file: %s\n" % path)
            return 2
        with open(path, encoding="utf-8") as fh:
            try:
                doc = json.load(fh)
            except json.JSONDecodeError as exc:
                print(msg(lang, "invalid_json", file=path, err=exc))
                total_errors += 1
                continue
        if args.prereg_only:
            errors = validate_prereg_only(doc, schema, lang)
            warnings = lint_prereg_only(doc, lang)
        else:
            errors = validate(doc, schema, lang)
            warnings = lint(doc, schema, lang)
        if errors:
            print(msg(lang, "file_errors", file=path, n=len(errors)))
            for err in errors:
                print("  - %s" % err)
            total_errors += len(errors)
        else:
            print(msg(lang, "file_ok", file=path))
        if warnings:
            print(msg(lang, "file_warnings_strict" if args.strict else "file_warnings", file=path, n=len(warnings)))
            for warning in warnings:
                print("  ~ %s" % warning)
            total_warnings += len(warnings)

    if args.strict:
        total_errors += total_warnings
    if total_errors:
        print("\n" + msg(lang, "total", n=total_errors))
        return 1
    if total_warnings:
        print("\n" + msg(lang, "all_ok"))
        print(msg(lang, "total_warnings", n=total_warnings))
        return 0
    print("\n" + msg(lang, "all_ok"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
