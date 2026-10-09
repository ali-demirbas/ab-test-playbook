#!/usr/bin/env python3
"""Validate scenario JSON files against templates/scenario.schema.json.

Stdlib-only by design (the repo takes no runtime dependencies), so this is a
deliberately small subset of JSON Schema rather than a general implementation:
type, required, enum, const, additionalProperties, minItems/maxItems,
minLength, pattern, minimum/maximum (inclusive and exclusive), oneOf and
dependentRequired.

On top of the shape, the cross-field rules a schema cannot express are checked
directly, because they are the whole point of having a schema here:

  * KPIs: exactly one with role "primary", and it is the first item (rule 2);
    at least one "guardrail" (rule 3)
  * source "adapted" names its archive original in adapted_from (rule 8), and
    an archive/adapted scenario is never labelled "intuition" (rule 8)
  * ice.tier matches the product of its three scores when they are given
  * card: ring placement matches card.difference (shared with build_card.py)
  * preregistration, when present: its variable, primary KPI and guardrail
    names are the scenario's own (whitespace and case normalised); the
    alternative agrees with the primary direction; allocation sums to 1;
    planned_n_per_arm / duration_days are numbers only when
    sample.traffic_known is true (rule 5)

What this tool deliberately does NOT check: whether `variable` really names a
single variable, whether the mechanism is causal, whether the primary KPI is
sensitive to the change. Those are judgement calls and belong to
agents/scenario-critic — a schema can only enforce shape.

Usage:
  validate_scenario_json.py <file.json> [more.json ...]
  validate_scenario_json.py --prereg-only <file.json>   # a bare {"preregistration": {...}}
  validate_scenario_json.py --lang en <file.json>        # messages in English (default: Turkish)
  validate_scenario_json.py --schema templates/scenario.schema.json <file.json>

In --prereg-only mode the file holds exactly what ab-test-design emits,
{"preregistration": {...}}, optionally with a sibling "sample" object; without
{"sample": {"traffic_known": true}} next to it, planned_n_per_arm and
duration_days must stay null.

Exit: 0 = all valid, 1 = violations found, 2 = usage error.
"""
import argparse
import json
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

try:  # one source of truth for ring placement: the builder's own rule
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from build_card import ring_problems, DIFFERENCE_ALIASES  # noqa: E402
except ImportError:  # pragma: no cover - build_card ships next to this file
    ring_problems = None
    DIFFERENCE_ALIASES = {}

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


def norm(text):
    """Whitespace- and case-insensitive comparison key for names typed twice."""
    return " ".join(str(text or "").split()).casefold()


def check_kpi_roles(scenario, errors, lang="tr"):
    """Rules 2 and 3 on the KPI list.

    Checked directly rather than via the generic walker: they are the reason
    this schema exists, and a silent miss here would let a scenario ship with
    five equally-weighted metrics and no guardrail — exactly what rules 2 and 3
    forbid. Rule 2 also fixes the order: the first item IS the primary metric.
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


def check_card(scenario, errors, lang="tr"):
    card = scenario.get("card")
    if not isinstance(card, dict) or ring_problems is None:
        return
    diff = card.get("difference")
    if not isinstance(diff, str):
        return
    diff = DIFFERENCE_ALIASES.get(diff.lower(), diff.lower())
    if diff not in ("change", "add", "move", "remove"):
        return
    for problem in ring_problems(diff, card.get("variant_a", ""), card.get("variant_b", ""),
                                 card.get("shift_note_b"), lang=lang):
        errors.append(msg(lang, "ring", msg=problem))


def check_prereg_block(pre, sample, errors, lang="tr"):
    """Rules internal to the pre-registration block (also run in --prereg-only)."""
    if not isinstance(pre, dict):
        return
    alloc = pre.get("allocation")
    if isinstance(alloc, dict):
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


def check_preregistration(scenario, errors, lang="tr"):
    """Cross-field rules between the pre-registration block and the scenario.

    A schema can't say "the pre-registered primary KPI is the same metric the
    scenario marks primary"; these are checked here. A mismatch means the plan
    fixed before launch and the scenario that was reviewed describe two
    different tests.
    """
    pre = scenario.get("preregistration")
    if not isinstance(pre, dict):
        return
    check_prereg_block(pre, scenario.get("sample"), errors, lang)

    kpis = scenario.get("kpis") if isinstance(scenario.get("kpis"), list) else []
    by_name = {norm(k.get("name")): k for k in kpis if isinstance(k, dict)}

    pkpi = pre.get("primary_kpi")
    primaries = [k.get("name") for k in kpis if isinstance(k, dict) and k.get("role") == "primary"]
    if isinstance(pkpi, dict) and len(primaries) == 1 and norm(pkpi.get("name")) != norm(primaries[0]):
        errors.append(msg(lang, "pre_primary", got=pkpi.get("name"), want=primaries[0]))

    if "variable" in pre and "variable" in scenario and norm(pre["variable"]) != norm(scenario["variable"]):
        errors.append(msg(lang, "pre_variable", got=pre["variable"], want=scenario["variable"]))

    guards = pre.get("guardrails")
    if isinstance(guards, list) and by_name:
        for i, g in enumerate(guards):
            if not isinstance(g, dict) or "name" not in g:
                continue
            match = by_name.get(norm(g["name"]))
            if match is None:
                errors.append(msg(lang, "pre_guardrail_missing", i=i, name=g["name"]))
            elif match.get("role") != "guardrail":
                errors.append(msg(lang, "pre_guardrail_role", i=i, name=g["name"], role=match.get("role")))


def validate(scenario, schema, lang="tr"):
    errors = []
    walk(scenario, schema, "", errors, schema, lang)
    if isinstance(scenario, dict):
        check_kpi_roles(scenario, errors, lang)
        check_source(scenario, errors, lang)
        check_ice(scenario, errors, lang)
        check_card(scenario, errors, lang)
        check_preregistration(scenario, errors, lang)
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
    return errors


def main(argv):
    ap = argparse.ArgumentParser(description="Validate scenario JSON against the schema.")
    ap.add_argument("files", nargs="+", help="scenario JSON file(s)")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA)
    ap.add_argument("--prereg-only", action="store_true",
                    help="each file is a bare {\"preregistration\": {...}} block (ab-test-design output)")
    ap.add_argument("--lang", choices=("tr", "en"), default="tr", help="message language (default: tr)")
    args = ap.parse_args(argv)
    lang = args.lang

    if not os.path.isfile(args.schema):
        sys.stderr.write("validate_scenario_json: no schema at %s\n" % args.schema)
        return 2
    with open(args.schema, encoding="utf-8") as fh:
        schema = json.load(fh)

    total_errors = 0
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
        else:
            errors = validate(doc, schema, lang)
        if errors:
            print(msg(lang, "file_errors", file=path, n=len(errors)))
            for err in errors:
                print("  - %s" % err)
            total_errors += len(errors)
        else:
            print(msg(lang, "file_ok", file=path))

    if total_errors:
        print("\n" + msg(lang, "total", n=total_errors))
        return 1
    print("\n" + msg(lang, "all_ok"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
