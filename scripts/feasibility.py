#!/usr/bin/env python3
"""Rough traffic feasibility from numbers the user gave (CLAUDE.md rule 5).

Run ONLY when the user states a baseline conversion rate and the eligible
visitors themselves; traffic is never asked for. Prints the rough minimum
detectable relative effect (MDE) for each run length and a verdict band, as
two chat lines: a range and a one-line caveat. It promises no result and sets
no sample size, duration or stop rule; the testing tool's own reporting reads
the finished test.

Formula (normal approximation, two-sided alpha 0.05, 80% power, equal split,
each variant compared with the control, no correction for more arms):

    n     = visitors_per_day * 7 * weeks / arms          (per arm)
    delta = (z_0.975 + z_0.80) * sqrt(2 * p * (1 - p) / n)
    MDE   = delta / p                                     (relative)

Verdict, on the longest run shown (methodology.md → Traffic feasibility):

    MDE <=  5%   small changes detectable
    MDE <= 15%   small changes not detectable
    MDE <= 30%   detectable for bold changes only
    MDE >  30%   not testable at this traffic

Usage:
  feasibility.py --rate 0.025 --visitors 1200 [--per day|week|month]
                 [--arms 2] [--weeks 2 4] [--lang tr|en]
  --rate also takes a percentage written with "%" ("2.5%").
"""
import argparse
import math
import re
import sys

Z_ALPHA = 1.959963984540054   # two-sided alpha 0.05
Z_POWER = 0.8416212335729143  # power 0.80
DAYS = {"day": 1.0, "week": 7.0, "month": 30.0}
# (upper bound of the relative MDE, verdict key), lowest first; above the last: not testable.
BANDS = ((0.05, "small_ok"), (0.15, "small_no"), (0.30, "bold_only"))

TEXT = {
    "tr": {
        "small_ok": "Küçük değişiklikler de ölçülebilir",
        "small_no": "Küçük değişiklikler ölçülemez",
        "bold_only": "Yalnızca cesur değişiklikler ölçülebilir",
        "not_testable": "Bu trafikle test edilemez",
        "row": "{weeks} haftada yaklaşık {mde}",
        "line": "Fizibilite (kaba, verdiğin rakamlarla: dönüşüm {rate}, günde {visitors} uygun ziyaretçi, {arms} kol): "
                "ölçülebilir en küçük göreli fark {rows}. {verdict}.",
        "caveat": "Kaba bir normal yaklaşım (%80 güç, iki yönlü alfa 0,05), sonuç sözü değil; testin sonucunu test "
                  "aracının kendi raporu okur.",
        "err_rate": "Hata: dönüşüm oranı 0 ile 1 arasında olmalı (ör. 0.025 ya da 2.5%); verilen: {v}",
        "err_visitors": "Hata: ziyaretçi sayısı pozitif bir sayı olmalı; verilen: {v}",
        "err_arms": "Hata: kol sayısı en az 2 olmalı; verilen: {v}",
        "err_weeks": "Hata: hafta sayısı pozitif bir sayı olmalı; verilen: {v}",
    },
    "en": {
        "small_ok": "Small changes are detectable too",
        "small_no": "Small changes are not detectable",
        "bold_only": "Detectable for bold changes only",
        "not_testable": "Not testable at this traffic",
        "row": "about {mde} in {weeks} weeks",
        "line": "Feasibility (rough, from your numbers: conversion {rate}, {visitors} eligible visitors a day, "
                "{arms} arms): smallest detectable relative difference {rows}. {verdict}.",
        "caveat": "A rough normal approximation (80% power, two-sided alpha 0.05), not a promise of a result; the "
                  "testing tool's own reporting reads the test.",
        "err_rate": "Error: the conversion rate must be between 0 and 1 (e.g. 0.025 or 2.5%); got: {v}",
        "err_visitors": "Error: the visitor count must be a positive number; got: {v}",
        "err_arms": "Error: arms must be at least 2; got: {v}",
        "err_weeks": "Error: weeks must be a positive number; got: {v}",
    },
}


def relative_mde(rate, daily_visitors, arms=2, weeks=2.0):
    """The rough minimum detectable relative effect (0.27 = 27%)."""
    per_arm = daily_visitors * 7.0 * weeks / arms
    delta = (Z_ALPHA + Z_POWER) * math.sqrt(2.0 * rate * (1.0 - rate) / per_arm)
    return delta / rate


def verdict(mde):
    """The verdict key for a relative MDE."""
    for upper, key in BANDS:
        if mde <= upper:
            return key
    return "not_testable"


def parse_rate(raw):
    text = str(raw).strip().replace(",", ".")
    percent = text.endswith("%")
    value = float(text.rstrip("%").strip())
    if percent:
        value /= 100.0
    if not math.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError
    return value


THOUSANDS_RE = re.compile(r"^\d{1,3}(?:([.,])\d{3})(?:\1\d{3})*$")


def parse_positive(raw):
    text = str(raw).strip().replace("_", "").replace(" ", "")
    if THOUSANDS_RE.match(text):  # "1,200" / "1.200" / "40.000": a thousands separator, not a decimal
        text = re.sub(r"[.,]", "", text)
    value = float(text)
    if not math.isfinite(value) or value <= 0:
        raise ValueError
    return value


def fmt_percent(value, lang, decimals=0):
    number = ("%." + str(decimals) + "f") % (value * 100.0)
    if lang == "tr":
        return "%" + number.replace(".", ",")
    return number + "%"


def fmt_count(value, lang):
    number = "{:,}".format(int(round(value)))
    return number.replace(",", ".") if lang == "tr" else number


def fmt_rate(rate, lang):
    pct = rate * 100.0
    decimals = 0 if abs(pct - round(pct)) < 1e-9 else (1 if abs(pct * 10 - round(pct * 10)) < 1e-9 else 2)
    return fmt_percent(rate, lang, decimals)


def report(rate, daily, arms, weeks, lang):
    """The two chat lines: the range with its verdict, and the caveat."""
    t = TEXT[lang]
    weeks = sorted(set(weeks))
    rows = []
    for w in weeks:
        w_text = ("%g" % w).replace(".", ",") if lang == "tr" else "%g" % w
        rows.append(t["row"].format(weeks=w_text, mde=fmt_percent(relative_mde(rate, daily, arms, w), lang)))
    key = verdict(relative_mde(rate, daily, arms, weeks[-1]))
    line = t["line"].format(rate=fmt_rate(rate, lang), visitors=fmt_count(daily, lang), arms=arms,
                            rows=", ".join(rows), verdict=t[key])
    return line + "\n" + t["caveat"], key


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rough MDE from the user's own numbers (rule 5).")
    parser.add_argument("--rate", required=True, help="baseline conversion rate, 0-1 or with %%")
    parser.add_argument("--visitors", required=True, help="eligible visitors (all arms together)")
    parser.add_argument("--per", choices=sorted(DAYS), default="day", help="the period --visitors counts")
    parser.add_argument("--arms", default="2", help="arms including the control (default 2)")
    parser.add_argument("--weeks", nargs="+", default=["2", "4"], help="run lengths in weeks (default 2 4)")
    parser.add_argument("--lang", choices=("tr", "en"), default="tr")
    args = parser.parse_args(argv)
    t = TEXT[args.lang]
    try:
        rate = parse_rate(args.rate)
    except ValueError:
        print(t["err_rate"].format(v=args.rate), file=sys.stderr)
        return 2
    try:
        daily = parse_positive(args.visitors) / DAYS[args.per]
    except ValueError:
        print(t["err_visitors"].format(v=args.visitors), file=sys.stderr)
        return 2
    try:
        arms = int(args.arms)
        if arms < 2:
            raise ValueError
    except ValueError:
        print(t["err_arms"].format(v=args.arms), file=sys.stderr)
        return 2
    weeks = []
    for raw in args.weeks:
        try:
            weeks.append(parse_positive(raw))
        except ValueError:
            print(t["err_weeks"].format(v=raw), file=sys.stderr)
            return 2
    text, _ = report(rate, daily, arms, weeks, args.lang)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
