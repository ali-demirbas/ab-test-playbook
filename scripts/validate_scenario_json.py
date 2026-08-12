#!/usr/bin/env python3
"""Validate scenario JSON files against templates/scenario.schema.json.

Stdlib-only by design (the repo takes no runtime dependencies), so this is a
deliberately small subset of JSON Schema rather than a general implementation:
type, required, enum, additionalProperties, minItems/maxItems, minLength,
pattern, oneOf and dependentRequired — plus the two structural rules the schema
expresses with allOf/contains, which are checked directly because they are the
whole point of having a schema here:

  * exactly one KPI with role "primary"   (CLAUDE.md rule 2)
  * at least one KPI with role "guardrail" (CLAUDE.md rule 3)

What this tool deliberately does NOT check: whether `variable` really names a
single variable, whether the mechanism is causal, whether the primary KPI is
sensitive to the change. Those are judgement calls and belong to
agents/scenario-critic — a schema can only enforce shape.

Usage:
  validate_scenario_json.py <file.json> [more.json ...]
  validate_scenario_json.py --schema templates/scenario.schema.json <file.json>

Exit: 0 = all valid, 1 = violations found, 2 = usage error.
"""
import argparse
import json
import os
import re
import sys

DEFAULT_SCHEMA = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "templates",
    "scenario.schema.json",
)

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def type_ok(value, expected):
    names = expected if isinstance(expected, list) else [expected]
    for name in names:
        py = TYPES.get(name)
        if py is None:
            continue
        if name == "integer" and isinstance(value, bool):
            continue  # bool is an int in Python; not an integer here
        if name in ("number", "integer") and isinstance(value, bool):
            continue
        if isinstance(value, py):
            return True
    return False


def walk(value, schema, path, errors, root):
    if "$ref" in schema:
        schema = resolve(schema["$ref"], root)

    if "oneOf" in schema:
        matches = 0
        for sub in schema["oneOf"]:
            trial = []
            walk(value, sub, path, trial, root)
            if not trial:
                matches += 1
        if matches != 1:
            errors.append("%s: %d/%d oneOf branches matched (expected exactly 1)"
                          % (path, matches, len(schema["oneOf"])))
        return

    if "type" in schema and not type_ok(value, schema["type"]):
        errors.append("%s: expected type %s, got %s" % (path, schema["type"], type(value).__name__))
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append("%s: %r is not one of %s" % (path, value, schema["enum"]))

    if "const" in schema and value != schema["const"]:
        errors.append("%s: expected %r" % (path, schema["const"]))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append("%s: shorter than minLength %d" % (path, schema["minLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append("%s: %r does not match %s" % (path, value, schema["pattern"]))

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append("%s: below minimum %s" % (path, schema["minimum"]))
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append("%s: must be greater than %s" % (path, schema["exclusiveMinimum"]))
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errors.append("%s: must be less than %s" % (path, schema["exclusiveMaximum"]))

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append("%s: has %d item(s), minimum is %d" % (path, len(value), schema["minItems"]))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append("%s: has %d item(s), maximum is %d" % (path, len(value), schema["maxItems"]))
        if "items" in schema:
            for i, item in enumerate(value):
                walk(item, schema["items"], "%s[%d]" % (path, i), errors, root)

    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append("%s: missing required field %r" % (path, key))
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append("%s: unknown field %r" % (path, key))
        for key, sub in props.items():
            if key in value:
                walk(value[key], sub, "%s.%s" % (path, key) if path else key, errors, root)
        for key, needs in schema.get("dependentRequired", {}).items():
            if key in value:
                for need in needs:
                    if need not in value:
                        errors.append("%s: %r requires %r" % (path, key, need))


def resolve(ref, root):
    if not ref.startswith("#/"):
        return {}
    node = root
    for part in ref[2:].split("/"):
        node = node.get(part, {})
    return node


def check_kpi_roles(scenario, errors):
    """The two structural rules the schema states with allOf/contains.

    Checked directly rather than via the generic walker: they are the reason
    this schema exists, and a silent miss here would let a scenario ship with
    five equally-weighted metrics and no guardrail — exactly what rules 2 and 3
    forbid.
    """
    kpis = scenario.get("kpis")
    if not isinstance(kpis, list):
        return
    roles = [k.get("role") for k in kpis if isinstance(k, dict)]
    primaries = roles.count("primary")
    if primaries != 1:
        errors.append(
            "kpis: found %d KPI(s) with role 'primary', expected exactly 1 (rule 2)" % primaries
        )
    if roles.count("guardrail") < 1:
        errors.append("kpis: no KPI with role 'guardrail' (rule 3)")


def validate(scenario, schema):
    errors = []
    walk(scenario, schema, "", errors, schema)
    check_kpi_roles(scenario, errors)
    return errors


def main(argv):
    ap = argparse.ArgumentParser(description="Validate scenario JSON against the schema.")
    ap.add_argument("files", nargs="+", help="scenario JSON file(s)")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA)
    args = ap.parse_args(argv)

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
                scenario = json.load(fh)
            except json.JSONDecodeError as exc:
                print("%s: INVALID JSON — %s" % (path, exc))
                total_errors += 1
                continue
        errors = validate(scenario, schema)
        if errors:
            print("%s: %d ihlal" % (path, len(errors)))
            for err in errors:
                print("  - %s" % err)
            total_errors += len(errors)
        else:
            print("%s: ok" % path)

    if total_errors:
        print("\nTOPLAM: %d ihlal" % total_errors)
        return 1
    print("\nTüm senaryolar şemaya uyuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
