#!/usr/bin/env python3
"""
A/B test istatistik motoru (v2): oran testleri, örneklem planı, SRM, sürekli metrikler, Bayes görünümü.

Kullanım:
  Sonuç yorumlama (iki kol; normal yaklaşım geçersizse otomatik Fisher exact):
    python3 analyze_results.py significance \
      --control-visitors 5000 --control-conversions 250 \
      --variant-visitors 5000 --variant-conversions 290

  A/B/n (her varyant kontrolle kıyaslanır, Holm düzeltmesi):
    python3 analyze_results.py significance --control-visitors 5000 --control-conversions 250 \
      --variant 5000:290 --variant 5000:270 --alternative two-sided --planned-n 8000

  Örneklem büyüklüğü (test planlama):
    python3 analyze_results.py samplesize \
      --baseline-rate 0.05 --mde 0.20 --confidence 0.95 --power 0.80 [--ratio 2] [--arms 3] [--alternative greater]

  SRM (2 veya daha fazla kol):
    python3 analyze_results.py srm --control-visitors 5012 --variant-visitors 4988
    python3 analyze_results.py srm --visitors 5000,5100,4900 [--expected-ratios 1,1,1]

  Sürekli metrik (ziyaretçi başına gelir vb.; Welch t-testi, bootstrap, CUPED):
    python3 analyze_results.py continuous --control-csv c.csv --variant-csv v.csv \
      [--winsorize 0.99] [--bootstrap 2000 --seed 42] [--control-pre-csv cp.csv --variant-pre-csv vp.csv]
    python3 analyze_results.py continuous --control-n 5000 --control-mean 4.1 --control-sd 20 \
      --variant-n 5000 --variant-mean 4.6 --variant-sd 22

  Bayes görünümü (alternatif bakış, frekansçı kararın yerine geçmez):
    python3 analyze_results.py bayes --control-visitors 5000 --control-conversions 250 \
      --variant-visitors 5000 --variant-conversions 290 [--draws 100000 --seed 1]

  Gelir/kâr yön göstergesi (çıkarım için 'continuous' kullanın):
    python3 analyze_results.py revenue ...

Tam sayı girdileri esnektir: 1000, 1e3, 1,000 ve 1_000 kabul edilir.
Sadece Python standart kütüphanesi kullanır (math, random, statistics). Dış bağımlılık yok.
"""
import argparse
import json
import math
import random
import re
import sys

_EPS = 3e-16
_FPMIN = 1e-300


# ---------------------------------------------------------------------------
# Dağılım fonksiyonları (stdlib)
# ---------------------------------------------------------------------------

def norm_cdf(x):
    """Standart normal dağılımın birikimli dağılım fonksiyonu."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def norm_ppf(p):
    """Standart normal dağılımın ters birikimli dağılım fonksiyonu (yüzde noktası).
    Acklam'ın rasyonel yaklaşım algoritması — sayısal analizde yaygın, kamu malı yöntem."""
    if p <= 0 or p >= 1:
        raise ValueError("p, 0 ile 1 arasında olmalı")

    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]

    p_low = 0.02425
    p_high = 1 - p_low

    if p < p_low:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def _fix(v):
    return _FPMIN if abs(v) < _FPMIN else v


def _betacf(a, b, x):
    """Düzenlenmiş eksik beta için sürekli kesir (modifiye Lentz)."""
    qab, qap, qam = a + b, a + 1, a - 1
    c = 1.0
    d = 1.0 / _fix(1 - qab * x / qap)
    h = d
    for m in range(1, 10000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 / _fix(1 + aa * d)
        c = _fix(1 + aa / c)
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 / _fix(1 + aa * d)
        c = _fix(1 + aa / c)
        de = d * c
        h *= de
        if abs(de - 1) < _EPS:
            break
    return h


def betainc_reg(a, b, x):
    """Düzenlenmiş eksik beta fonksiyonu I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    ln_bt = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return math.exp(ln_bt) * _betacf(a, b, x) / a
    return 1.0 - math.exp(ln_bt) * _betacf(b, a, 1 - x) / b


def gammaincc_reg(a, x):
    """Düzenlenmiş üst eksik gama Q(a, x) = 1 - P(a, x)."""
    if x <= 0:
        return 1.0
    ln_pre = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1:
        ap, s = a, 1.0 / a
        term = s
        for _ in range(100000):
            ap += 1
            term *= x / ap
            s += term
            if abs(term) < abs(s) * _EPS:
                break
        return max(0.0, 1.0 - s * math.exp(ln_pre))
    b = x + 1 - a
    c = 1.0 / _FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, 100000):
        an = -i * (i - a)
        b += 2
        d = 1.0 / _fix(an * d + b)
        c = _fix(b + an / c)
        de = d * c
        h *= de
        if abs(de - 1) < _EPS:
            break
    return math.exp(ln_pre) * h


def chi2_sf(chi2, df):
    """Ki-kare sağ kuyruk olasılığı."""
    if chi2 <= 0:
        return 1.0
    if df == 1:  # erfc: büyük chi2'de 0'a yuvarlanmaz
        return math.erfc(math.sqrt(chi2 / 2))
    return gammaincc_reg(df / 2.0, chi2 / 2.0)


def t_sf_two_sided(t, df):
    """Student t için iki yönlü p = P(|T| >= |t|)."""
    if math.isinf(df):
        return math.erfc(abs(t) / math.sqrt(2))
    return betainc_reg(df / 2.0, 0.5, df / (df + t * t))


def t_cdf(t, df):
    p2 = t_sf_two_sided(t, df)
    return 1 - p2 / 2 if t >= 0 else p2 / 2


def t_ppf(q, df):
    """Student t yüzde noktası (ikiye bölme)."""
    if not 0 < q < 1:
        raise ValueError("q, 0 ile 1 arasında olmalı")
    lo, hi = -1e6, 1e6
    for _ in range(300):
        mid = (lo + hi) / 2
        if t_cdf(mid, df) < q:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-12:
            break
    return (lo + hi) / 2


def _p_from_z(z, alternative):
    if alternative == "greater":
        return 0.5 * math.erfc(z / math.sqrt(2))
    if alternative == "less":
        return 0.5 * math.erfc(-z / math.sqrt(2))
    return math.erfc(abs(z) / math.sqrt(2))


def _z_alpha(alpha, alternative):
    return norm_ppf(1 - alpha) if alternative in ("greater", "less") else norm_ppf(1 - alpha / 2)


def _round_p(p, digits=5):
    # Çok küçük p'yi yuvarlamak onu 0.0'a ezer; 0 basmak yanıltıcıdır.
    return round(p, digits) if p >= 10 ** -digits else p


_ALTERNATIVES = ("two-sided", "greater", "less")


def _check_alternative(alternative):
    if alternative not in _ALTERNATIVES:
        raise ValueError(f"alternative şunlardan biri olmalı: {', '.join(_ALTERNATIVES)} (verilen: {alternative})")


# ---------------------------------------------------------------------------
# Esnek girdi ayrıştırma
# ---------------------------------------------------------------------------

def parse_count(s):
    """'1000', '1e3', '1,000', '1_000', '1000.0' → 1000. Tam sayı olmayanı reddeder."""
    if isinstance(s, int):
        return s
    txt = str(s).strip().replace("_", "")
    if re.fullmatch(r"[+-]?\d{1,3}(,\d{3})+", txt):
        txt = txt.replace(",", "")
    try:
        val = float(txt)
    except ValueError:
        raise argparse.ArgumentTypeError(f"tam sayı bekleniyordu (verilen: {s!r})")
    if not math.isfinite(val) or val != int(val):
        raise argparse.ArgumentTypeError(f"tam sayı bekleniyordu (verilen: {s!r})")
    return int(val)


parse_count.__name__ = "tam_sayi"


def parse_arm(s):
    """'5000:290' → (5000, 290)."""
    parts = str(s).split(":")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(f"ZİYARETÇİ:DÖNÜŞÜM biçimi bekleniyordu, ör. 5000:290 (verilen: {s!r})")
    return parse_count(parts[0]), parse_count(parts[1])


parse_arm.__name__ = "kol"


# ---------------------------------------------------------------------------
# Oran testleri
# ---------------------------------------------------------------------------

def _log_comb(n, k):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def fisher_exact(control_visitors, control_conversions, variant_visitors, variant_conversions,
                 alternative="two-sided"):
    """2x2 tablo için Fisher exact testi (hipergeometrik, log-faktöriyel ile).
    'greater' = varyant oranı kontrolden büyük. İki yönlü p: gözlenen tablodan
    daha olası olmayan tüm tabloların olasılık toplamı (R/scipy ile aynı tanım)."""
    _check_alternative(alternative)
    n1, n2 = control_visitors, variant_visitors
    x2 = variant_conversions
    k = control_conversions + variant_conversions
    n = n1 + n2
    lo, hi = max(0, k - n1), min(k, n2)
    denom = _log_comb(n, k)

    def pmf(x):
        return math.exp(_log_comb(n2, x) + _log_comb(n1, k - x) - denom)

    if alternative == "greater":
        return min(1.0, sum(pmf(x) for x in range(x2, hi + 1)))
    if alternative == "less":
        return min(1.0, sum(pmf(x) for x in range(lo, x2 + 1)))
    p_obs = pmf(x2)
    thr = p_obs * (1 + 1e-7)
    return min(1.0, sum(p for p in (pmf(x) for x in range(lo, hi + 1)) if p <= thr))


def wilson_interval(x, n, confidence=0.95):
    """Wilson skor aralığı (süreklilik düzeltmesiz)."""
    z = norm_ppf(1 - (1 - confidence) / 2)
    p = x / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def newcombe_diff_ci(x1, n1, x2, n2, confidence=0.95):
    """Newcombe (1998) hibrit skor aralığı, yöntem 10: (p2 - p1) farkı için.
    Wald aralığının %0/%100'de [0, 0]'a çöken dejenere halini önler."""
    p1, p2 = x1 / n1, x2 / n2
    l1, u1 = wilson_interval(x1, n1, confidence)
    l2, u2 = wilson_interval(x2, n2, confidence)
    d = p2 - p1
    return (d - math.sqrt((p2 - l2) ** 2 + (u1 - p1) ** 2),
            d + math.sqrt((u2 - p2) ** 2 + (p1 - l1) ** 2))


def relative_lift_ci(x1, n1, x2, n2, confidence=0.95):
    """Göreli lift (p2/p1 - 1) için güven aralığı: log oranda delta yöntemi (Katz).
    Kontrol veya varyant oranı 0 ise tanımsız → None."""
    if x1 == 0 or x2 == 0:
        return None
    p1, p2 = x1 / n1, x2 / n2
    se = math.sqrt((1 - p1) / x1 + (1 - p2) / x2)
    z = norm_ppf(1 - (1 - confidence) / 2)
    lr = math.log(p2 / p1)
    return math.exp(lr - z * se) - 1, math.exp(lr + z * se) - 1


def holm_adjust(p_values):
    """Holm-Bonferroni düzeltilmiş p-değerleri (girdi sırasıyla)."""
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p_values[i]))
        adjusted[i] = running
    return adjusted


def _validate_arm(ad, v, c):
    if v <= 0:
        raise ValueError(f"{ad} ziyaretçi sayısı pozitif olmalı (verilen: {v})")
    if c < 0:
        raise ValueError(f"{ad} dönüşüm sayısı negatif olamaz (verilen: {c})")
    if c > v:
        raise ValueError(f"{ad} dönüşüm sayısı ({c}) ziyaretçi sayısından ({v}) büyük olamaz")


def significance(control_visitors, control_conversions, variant_visitors, variant_conversions,
                 confidence=0.95, alternative="two-sided", planned_n=None, power_target=0.80):
    """İki oranın karşılaştırması. Normal yaklaşım geçerliyse iki-oranlı z-testi,
    değilse otomatik Fisher exact testi; karar KULLANILAN yöntemin p-değerine dayanır."""
    _validate_arm("kontrol", control_visitors, control_conversions)
    _validate_arm("varyant", variant_visitors, variant_conversions)
    if not 0 < confidence < 1:
        raise ValueError(f"güven düzeyi 0 ile 1 arasında olmalı (verilen: {confidence})")
    _check_alternative(alternative)
    if planned_n is not None and planned_n <= 0:
        raise ValueError(f"planlanan örneklem pozitif olmalı (verilen: {planned_n})")

    alpha = 1 - confidence
    p1 = control_conversions / control_visitors
    p2 = variant_conversions / variant_visitors
    n1, n2 = control_visitors, variant_visitors

    p_pool = (control_conversions + variant_conversions) / (n1 + n2)
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se_pool if se_pool > 0 else 0.0
    # erfc, 2*(1-norm_cdf(z)) ile matematiksel olarak aynıdır ama büyük |z|'de
    # 0'a yuvarlanmaz: p hiçbir zaman tam 0.0 basılmaz (istatistiksel olarak yanıltıcıdır).
    p_z = _p_from_z(z, alternative) if se_pool > 0 else 1.0

    diff = p2 - p1
    se_diff = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = norm_ppf(1 - alpha / 2)
    wald_ci = (diff - z_crit * se_diff, diff + z_crit * se_diff)
    ci_low, ci_high = newcombe_diff_ci(control_conversions, n1, variant_conversions, n2, confidence)
    rel_ci = relative_lift_ci(control_conversions, n1, variant_conversions, n2, confidence)
    relative_lift = (diff / p1) if p1 > 0 else None

    # --- Normal yaklaşımın geçerliliği (rare-event kontrolü) ---
    # Standart kriter: pooled oranla hesaplanan dört beklenen sayının hepsi >= 10.
    # Geçersizse p-değeri Fisher exact testiyle hesaplanır (z-testi p'si yalnızca bilgi için kalır).
    min_expected_count = 10
    expected_counts = [n1 * p_pool, n1 * (1 - p_pool), n2 * p_pool, n2 * (1 - p_pool)]
    normal_approx_valid = min(expected_counts) >= min_expected_count

    if normal_approx_valid:
        method, p_value = "z-test", p_z
    else:
        method = "fisher-exact"
        p_value = fisher_exact(n1, control_conversions, n2, variant_conversions, alternative)
    is_significant = p_value < alpha

    # --- Mevcut örneklemde güç / MDE ---
    z_a = _z_alpha(alpha, alternative)
    z_b = norm_ppf(power_target)
    if 0 < p1 < 1:
        mde_abs = (z_a + z_b) * math.sqrt(p1 * (1 - p1) * (1 / n1 + 1 / n2))
        mde_pct = round(mde_abs / p1 * 100, 2)
    else:
        mde_abs, mde_pct = None, None
    if se_diff > 0:
        eff = diff if alternative != "less" else -diff
        eff = abs(eff) if alternative == "two-sided" else eff
        observed_power = norm_cdf(eff / se_diff - z_a)
    else:
        observed_power = None

    # 250, formal bir güvenilirlik eşiği değil — kaba bir "muhtemelen çok küçük" uyarı sınırıdır.
    min_reliable_conversions = 250
    low_sample_warning = control_conversions < min_reliable_conversions or variant_conversions < min_reliable_conversions

    peeking_risk = planned_n is not None and min(n1, n2) < planned_n

    # Uyarılar öncelik sırasıyla; 'note' en öncelikli olanı, 'warnings' hepsini taşır.
    warnings = []
    if not normal_approx_valid:
        warnings.append(
            "Nadir olay uyarısı: beklenen dönüşüm/dönüşmeme sayılarından en az biri "
            f"{min_expected_count}'un altında (en küçüğü {min(expected_counts):.1f}); normal yaklaşım geçerli değil. "
            "p-değeri ve anlamlılık kararı bu yüzden Fisher exact testiyle hesaplandı; güven aralığı "
            "Newcombe skor aralığıdır. Veri az, sonucu kesin bir kanıt gibi okumayın."
        )
    if peeking_risk:
        warnings.append(
            f"Ara bakış (peeking) riski: kol başına planlanan {planned_n:,} ziyaretçiye ulaşılmadı "
            f"(en küçük kol {min(n1, n2):,}). Planlanan örneklem dolmadan erken durdurma yanlış pozitif "
            "oranını şişirir; bu sonuç nihai karar değildir."
        )
    if low_sample_warning and normal_approx_valid:
        warnings.append(
            "Dönüşüm sayısı 250'nin altında: bu kaba bir uyarı eşiğidir, formal yeterlilik kriteri değil. "
            "Gerçek yeterliliği bu testin baz oranı/MDE'siyle 'samplesize' komutunu çalıştırarak doğrulayın."
        )

    if peeking_risk:
        decision = "ara bakış: nihai karar verilmez"
    else:
        decision = "anlamlı" if is_significant else "anlamlı değil"

    return {
        "control_rate": round(p1, 5),
        "variant_rate": round(p2, 5),
        "absolute_diff": round(diff, 5),
        "relative_lift_pct": round(relative_lift * 100, 2) if relative_lift is not None else None,
        "z_score": round(z, 4),
        "method": method,
        "alternative": alternative,
        "p_value": _round_p(p_value),
        "p_value_z_test": _round_p(p_z),
        "confidence_level": confidence,
        "confidence_interval_diff": [round(ci_low, 5), round(ci_high, 5)],
        "confidence_interval_diff_method": "newcombe-hybrid-score",
        "confidence_interval_diff_wald": [round(wald_ci[0], 5), round(wald_ci[1], 5)],
        "confidence_interval_relative_lift_pct":
            [round(rel_ci[0] * 100, 2), round(rel_ci[1] * 100, 2)] if rel_ci else None,
        "is_significant": is_significant,
        "decision": decision,
        "normal_approx_valid": normal_approx_valid,
        "min_expected_count": round(min(expected_counts), 2),
        "low_sample_warning": low_sample_warning,
        "mde_at_current_n_pct": mde_pct,
        "mde_at_current_n_abs": round(mde_abs, 5) if mde_abs is not None else None,
        "observed_power": round(observed_power, 4) if observed_power is not None else None,
        "planned_n_per_arm": planned_n,
        "peeking_risk": peeking_risk,
        "warnings": warnings,
        "note": warnings[0] if warnings else None,
    }


def significance_multi(control_visitors, control_conversions, variants, confidence=0.95,
                       alternative="two-sided", planned_n=None):
    """A/B/n: her varyant kontrolle kıyaslanır, p-değerleri Holm ile düzeltilir.
    variants: [(ziyaretçi, dönüşüm), ...]"""
    if not variants:
        raise ValueError("en az bir varyant gerekli")
    names = [chr(ord("B") + i) if i < 25 else f"V{i + 1}" for i in range(len(variants))]
    comps = [significance(control_visitors, control_conversions, v, c, confidence, alternative, planned_n)
             for v, c in variants]
    raw = [c["p_value"] for c in comps]
    adj = holm_adjust(raw)
    alpha = 1 - confidence
    out = []
    for name, (v, c), r, pr, pa in zip(names, variants, comps, raw, adj):
        r = dict(r)
        r["arm"] = name
        r["variant_visitors"], r["variant_conversions"] = v, c
        r["p_value_raw"] = pr
        r["p_value_adjusted"] = _round_p(pa)
        r["is_significant_raw"] = r["is_significant"]
        r["is_significant"] = pa < alpha
        if r["peeking_risk"]:
            r["decision"] = "ara bakış: nihai karar verilmez"
        else:
            r["decision"] = "anlamlı" if r["is_significant"] else "anlamlı değil"
        out.append(r)
    note = (f"{len(variants)} varyant kontrolle kıyaslandı; çoklu karşılaştırma için Holm düzeltmesi "
            "uygulandı. Karar 'p_value_adjusted' üzerindendir.")
    return {
        "control_visitors": control_visitors,
        "control_conversions": control_conversions,
        "control_rate": round(control_conversions / control_visitors, 5),
        "n_comparisons": len(variants),
        "correction": "holm",
        "confidence_level": confidence,
        "alternative": alternative,
        "comparisons": out,
        "any_significant": any(r["is_significant"] for r in out),
        "peeking_risk": any(r["peeking_risk"] for r in out),
        "note": note,
    }


# ---------------------------------------------------------------------------
# SRM
# ---------------------------------------------------------------------------

def srm_multi(visitors, expected_ratios=None):
    """k kollu SRM: Pearson ki-kare uyum testi (k-1 serbestlik derecesi)."""
    if len(visitors) < 2:
        raise ValueError("SRM için en az 2 kol gerekli")
    if any(v < 0 for v in visitors):
        raise ValueError("ziyaretçi sayıları negatif olamaz")
    total = sum(visitors)
    if total == 0:
        raise ValueError("toplam ziyaretçi sayısı sıfır olamaz")
    if expected_ratios is None:
        expected_ratios = [1.0] * len(visitors)
    if len(expected_ratios) != len(visitors):
        raise ValueError(f"beklenen oran sayısı ({len(expected_ratios)}) kol sayısına ({len(visitors)}) eşit olmalı")
    if any(r <= 0 for r in expected_ratios):
        raise ValueError("beklenen oranlar pozitif olmalı")
    s = sum(expected_ratios)
    shares = [r / s for r in expected_ratios]
    expected = [total * sh for sh in shares]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(visitors, expected))
    df = len(visitors) - 1
    p_value = chi2_sf(chi2, df)
    approx_valid = min(expected) >= 5
    # SRM her testte koşulur; nominal %5 eşiği her 20 testte bir yanlış alarm verir.
    # Pratikte çok daha katı p < 0.001 eşiği kullanılır (tasarım tercihi).
    srm_detected = p_value < 0.001
    note = None
    if not approx_valid:
        note = (
            f"Uyarı: beklenen hücre sayılarından en az biri 5'in altında "
            f"(en küçüğü {min(expected):.1f}) — bu örneklemde ki-kare "
            "yaklaşımı zayıf, sonucu ihtiyatla okuyun; daha fazla veri toplayın."
        )
    return {
        "visitors": list(visitors),
        "observed_shares": [round(v / total, 5) for v in visitors],
        "expected_shares": [round(sh, 5) for sh in shares],
        "df": df,
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 6) if p_value >= 1e-6 else p_value,
        "srm_detected": srm_detected,
        "normal_approx_valid": approx_valid,
        "note": note,
    }


def srm(control_visitors, variant_visitors, expected_split=0.5):
    """Örneklem oranı uyuşmazlığı (SRM) kontrolü — bir sonuç metriği değil, testin
    RANDOMİZASYONUNUN kendisini denetler. 2 kollu biçim; k kol için srm_multi.
    SRM varsa test sonuçları güvenilmez — bu bir anlamlılık testi değildir."""
    if not 0 < expected_split < 1:
        raise ValueError(f"beklenen bölüşüm 0 ile 1 arasında olmalı (verilen: {expected_split})")
    r = srm_multi([control_visitors, variant_visitors], [expected_split, 1 - expected_split])
    total = control_visitors + variant_visitors
    r.update({
        "control_visitors": control_visitors,
        "variant_visitors": variant_visitors,
        "observed_split": round(control_visitors / total, 5),
        "expected_split": expected_split,
    })
    return r


# ---------------------------------------------------------------------------
# Örneklem büyüklüğü
# ---------------------------------------------------------------------------

def sample_size(baseline_rate, mde, confidence=0.95, power=0.80, alternative="two-sided",
                ratio=1.0, arms=2):
    """mde: göreli minimum tespit edilebilir fark (ör. 0.20 = %20 lift).
    ratio: varyant/kontrol örneklem oranı (n_varyant = ratio * n_kontrol).
    arms: toplam kol sayısı (kontrol dahil); alfa n-1 karşılaştırmaya Bonferroni ile bölünür."""
    if not 0 < baseline_rate < 1:
        raise ValueError(f"baz dönüşüm oranı 0 ile 1 arasında olmalı (verilen: {baseline_rate})")
    if mde == 0:
        raise ValueError(f"MDE sıfır olamaz (verilen: {mde})")
    if not 0 < confidence < 1:
        raise ValueError(f"güven düzeyi 0 ile 1 arasında olmalı (verilen: {confidence})")
    if not 0 < power < 1:
        raise ValueError(f"güç (power) 0 ile 1 arasında olmalı (verilen: {power})")
    _check_alternative(alternative)
    if ratio <= 0:
        raise ValueError(f"ratio pozitif olmalı (verilen: {ratio})")
    if arms < 2:
        raise ValueError(f"kol sayısı en az 2 olmalı (verilen: {arms})")

    notes = []
    if mde < 0:
        notes.append(f"Negatif MDE ({mde}) mutlak değeriyle ({abs(mde)}) kullanıldı; örneklem hesabı "
                     "artış yönünde hedef oranla yapıldı.")
        mde = abs(mde)

    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    if p2 >= 1:
        raise ValueError(f"hedef oran %100'ü aşıyor ({p2:.3f}); baz oran veya MDE'yi küçültün")

    comparisons = arms - 1
    alpha = (1 - confidence) / comparisons
    z_alpha = _z_alpha(alpha, alternative)
    z_beta = norm_ppf(power)
    k = ratio

    p_bar = (p1 + k * p2) / (1 + k)
    numerator = (z_alpha * math.sqrt(p_bar * (1 - p_bar) * (1 + 1 / k)) +
                 z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2) / k)) ** 2
    n_control = math.ceil(numerator / (p2 - p1) ** 2 - 1e-9)
    n_variant = math.ceil(n_control * k - 1e-9)
    total = n_control + comparisons * n_variant

    # Nadir-olay koruması: beklenen dönüşüm/dönüşmeme sayılarından biri 10'un altındaysa
    # plan normal yaklaşımın geçerli olmadığı bölgededir (tipik sebep: aşırı büyük MDE).
    expected = [n_control * p1, n_control * (1 - p1), n_variant * p2, n_variant * (1 - p2)]
    approx_valid = min(expected) >= 10
    if not approx_valid:
        notes.insert(0,
            "Uyarı: bu örneklem boyutunda beklenen dönüşüm/dönüşmeme sayılarından en az biri "
            f"10'un altında (en küçüğü {min(expected):.1f}) — hesap normal yaklaşımın geçerli "
            "olmadığı bölgede. Genelde sebep aşırı büyük bir MDE'dir; bu sayıyı test planı "
            "olarak kullanmayın, MDE'yi gerçekçi bir değere indirin.")
    if arms > 2:
        notes.append(f"{arms} kol: alfa {comparisons} karşılaştırmaya Bonferroni ile bölündü "
                     f"(karşılaştırma başına alfa {alpha:.4f}).")

    return {
        "baseline_rate": baseline_rate,
        "target_rate": round(p2, 5),
        "mde_relative_pct": round(mde * 100, 2),
        "confidence_level": confidence,
        "power": power,
        "alternative": alternative,
        "ratio": ratio,
        "arms": arms,
        "alpha_per_comparison": round(alpha, 6),
        "required_n_control": n_control,
        "required_n_variant": n_variant,
        "required_n_per_variant": n_control if ratio == 1 else n_variant,
        "required_n_total": total,
        "normal_approx_valid": approx_valid,
        "note": " ".join(notes) if notes else None,
    }


# ---------------------------------------------------------------------------
# Sürekli metrikler
# ---------------------------------------------------------------------------

def read_values_csv(path):
    """Satır başına bir sayı; boş satırlar ve sayı olmayan tek başlık satırı atlanır."""
    vals = []
    with open(path, encoding="utf-8-sig") as f:
        for i, line in enumerate(f):
            s = line.strip().split(",")[0].strip()
            if not s:
                continue
            try:
                vals.append(float(s))
            except ValueError:
                if i == 0 and not vals:
                    continue  # başlık satırı
                raise ValueError(f"{path}: {i + 1}. satır sayı değil ({s!r})")
    if not vals:
        raise ValueError(f"{path}: hiç sayısal değer yok")
    return vals


def _mean_var(xs):
    n = len(xs)
    m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / (n - 1) if n > 1 else 0.0
    return m, v


def _quantile(sorted_xs, q):
    """Doğrusal enterpolasyonlu yüzdelik (R tip 7)."""
    n = len(sorted_xs)
    h = (n - 1) * q
    lo = math.floor(h)
    hi = min(lo + 1, n - 1)
    return sorted_xs[lo] + (h - lo) * (sorted_xs[hi] - sorted_xs[lo])


def welch_test(m1, v1, n1, m2, v2, n2, confidence=0.95, alternative="two-sided"):
    """Welch t-testi (varyant - kontrol). v = örneklem varyansı."""
    _check_alternative(alternative)
    se2 = v1 / n1 + v2 / n2
    diff = m2 - m1
    if se2 <= 0:
        return {"t": 0.0, "df": None, "p_value": 1.0, "diff": diff, "se": 0.0,
                "ci_diff": [diff, diff]}
    se = math.sqrt(se2)
    num = se2 ** 2
    den = ((v1 / n1) ** 2 / (n1 - 1) if v1 > 0 else 0.0) + ((v2 / n2) ** 2 / (n2 - 1) if v2 > 0 else 0.0)
    df = num / den
    t = diff / se
    p2 = t_sf_two_sided(t, df)
    if alternative == "greater":
        p = p2 / 2 if t > 0 else 1 - p2 / 2
    elif alternative == "less":
        p = p2 / 2 if t < 0 else 1 - p2 / 2
    else:
        p = p2
    tc = t_ppf(1 - (1 - confidence) / 2, df)
    return {"t": t, "df": df, "p_value": p, "diff": diff, "se": se,
            "ci_diff": [diff - tc * se, diff + tc * se]}


def _rel_ci_means(m1, v1, n1, m2, v2, n2, confidence):
    """Ortalamalar oranı için delta yöntemi (log ölçekte). Ortalamalardan biri <= 0 ise None."""
    if m1 <= 0 or m2 <= 0:
        return None
    se = math.sqrt(v1 / (n1 * m1 * m1) + v2 / (n2 * m2 * m2))
    z = norm_ppf(1 - (1 - confidence) / 2)
    lr = math.log(m2 / m1)
    return [round((math.exp(lr - z * se) - 1) * 100, 2), round((math.exp(lr + z * se) - 1) * 100, 2)]


def continuous(control=None, variant=None, control_stats=None, variant_stats=None,
               confidence=0.95, alternative="two-sided", winsorize=None, bootstrap=0, seed=None,
               control_pre=None, variant_pre=None):
    """Sürekli metrik karşılaştırması (ör. ziyaretçi başına gelir; sıfırlar dahil).
    control/variant: kullanıcı başına değer listesi; ya da *_stats = (n, mean, sd)."""
    if not 0 < confidence < 1:
        raise ValueError(f"güven düzeyi 0 ile 1 arasında olmalı (verilen: {confidence})")
    _check_alternative(alternative)
    raw_mode = control is not None and variant is not None
    if not raw_mode and (control_stats is None or variant_stats is None):
        raise ValueError("ya iki CSV (kullanıcı başına değer) ya da iki kol için n/ortalama/sd verin")
    notes = []
    result = {"input": "raw" if raw_mode else "summary", "alternative": alternative,
              "confidence_level": confidence}

    if raw_mode:
        if len(control) < 2 or len(variant) < 2:
            raise ValueError("her kolda en az 2 gözlem gerekli")
        if winsorize is not None:
            if not 0.5 < winsorize < 1:
                raise ValueError(f"winsorize yüzdeliği 0.5 ile 1 arasında olmalı (verilen: {winsorize})")
            cap = _quantile(sorted(control + variant), winsorize)
            n_capped = sum(1 for x in control + variant if x > cap)
            control = [min(x, cap) for x in control]
            variant = [min(x, cap) for x in variant]
            result["winsorize"] = {"percentile": winsorize, "cap": round(cap, 4), "n_capped": n_capped}
            notes.append(f"Üst kuyruk iki kolun birleşik %{winsorize * 100:g} yüzdeliğinde ({cap:.4g}) "
                         f"kırpıldı ({n_capped} gözlem).")
        m1, v1 = _mean_var(control)
        m2, v2 = _mean_var(variant)
        n1, n2 = len(control), len(variant)
    else:
        (n1, m1, s1), (n2, m2, s2) = control_stats, variant_stats
        for ad, n, s in (("kontrol", n1, s1), ("varyant", n2, s2)):
            if n < 2:
                raise ValueError(f"{ad} örneklemi en az 2 olmalı (verilen: {n})")
            if s < 0:
                raise ValueError(f"{ad} standart sapması negatif olamaz (verilen: {s})")
        v1, v2 = s1 * s1, s2 * s2
        if winsorize is not None or bootstrap or control_pre is not None:
            notes.append("Özet istatistik girdisinde winsorize, bootstrap ve CUPED uygulanamaz; "
                         "kullanıcı başına CSV verin.")

    w = welch_test(m1, v1, n1, m2, v2, n2, confidence, alternative)
    alpha = 1 - confidence
    result.update({
        "control": {"n": n1, "mean": round(m1, 6), "sd": round(math.sqrt(v1), 6)},
        "variant": {"n": n2, "mean": round(m2, 6), "sd": round(math.sqrt(v2), 6)},
        "method": "welch-t-test",
        "absolute_diff": round(w["diff"], 6),
        "relative_lift_pct": round(w["diff"] / m1 * 100, 2) if m1 != 0 else None,
        "t_stat": round(w["t"], 4),
        "df": round(w["df"], 2) if w["df"] is not None else None,
        "p_value": _round_p(w["p_value"]),
        "confidence_interval_diff": [round(x, 6) for x in w["ci_diff"]],
        "confidence_interval_relative_lift_pct": _rel_ci_means(m1, v1, n1, m2, v2, n2, confidence),
        "is_significant": w["p_value"] < alpha,
    })

    if raw_mode and bootstrap:
        if bootstrap < 100:
            raise ValueError(f"bootstrap en az 100 tekrar olmalı (verilen: {bootstrap})")
        rng = random.Random(seed)
        diffs, rels = [], []
        for _ in range(bootstrap):
            bm1 = sum(rng.choices(control, k=n1)) / n1
            bm2 = sum(rng.choices(variant, k=n2)) / n2
            diffs.append(bm2 - bm1)
            if bm1 > 0:
                rels.append(bm2 / bm1 - 1)
        diffs.sort()
        rels.sort()
        result["bootstrap"] = {
            "resamples": bootstrap,
            "seed": seed,
            "ci_diff": [round(_quantile(diffs, alpha / 2), 6), round(_quantile(diffs, 1 - alpha / 2), 6)],
            "ci_relative_lift_pct": [round(_quantile(rels, alpha / 2) * 100, 2),
                                     round(_quantile(rels, 1 - alpha / 2) * 100, 2)] if len(rels) >= 100 else None,
            "method": "percentile",
        }

    if control_pre is not None or variant_pre is not None:
        if not raw_mode:
            pass
        elif control_pre is None or variant_pre is None:
            raise ValueError("CUPED için hem kontrol hem varyant ön-dönem CSV'si gerekli")
        else:
            if len(control_pre) != n1 or len(variant_pre) != n2:
                raise ValueError("ön-dönem CSV'leri metrik CSV'leriyle aynı satır sayısında olmalı "
                                 f"(kontrol {len(control_pre)} vs {n1}, varyant {len(variant_pre)} vs {n2})")
            ys = control + variant
            xs = control_pre + variant_pre
            my, vy = _mean_var(ys)
            mx, vx = _mean_var(xs)
            if vx == 0:
                raise ValueError("ön-dönem kovaryatının varyansı sıfır; CUPED uygulanamaz")
            cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)
            theta = cov / vx
            ca = [y - theta * (x - mx) for y, x in zip(control, control_pre)]
            va = [y - theta * (x - mx) for y, x in zip(variant, variant_pre)]
            cm, cv = _mean_var(ca)
            vm, vv = _mean_var(va)
            _, v_adj = _mean_var(ca + va)
            wc = welch_test(cm, cv, n1, vm, vv, n2, confidence, alternative)
            result["cuped"] = {
                "theta": round(theta, 6),
                "variance_reduction_pct": round((1 - v_adj / vy) * 100, 2) if vy > 0 else None,
                "control_mean_adj": round(cm, 6),
                "variant_mean_adj": round(vm, 6),
                "absolute_diff": round(wc["diff"], 6),
                "relative_lift_pct": round(wc["diff"] / cm * 100, 2) if cm != 0 else None,
                "t_stat": round(wc["t"], 4),
                "df": round(wc["df"], 2) if wc["df"] is not None else None,
                "p_value": _round_p(wc["p_value"]),
                "confidence_interval_diff": [round(x, 6) for x in wc["ci_diff"]],
                "is_significant": wc["p_value"] < alpha,
            }
            notes.append("CUPED: theta birleşik veriden hesaplandı; ön-dönem değeri test başlamadan "
                         "ölçülmüş olmalı, aksi halde düzeltme yanlıdır.")

    if min(n1, n2) < 30:
        notes.append("Kol başına 30'dan az gözlem: t yaklaşımı çarpık gelir verisinde zayıf, sonucu ihtiyatla okuyun.")
    result["note"] = " ".join(notes) if notes else None
    return result


# ---------------------------------------------------------------------------
# Bayes görünümü
# ---------------------------------------------------------------------------

def bayes(control_visitors, control_conversions, variant_visitors, variant_conversions,
          draws=100000, seed=None, credible=0.95):
    """Beta(1,1) önsel + Monte Carlo. ALTERNATİF bir bakıştır; frekansçı kararın yerine geçmez."""
    _validate_arm("kontrol", control_visitors, control_conversions)
    _validate_arm("varyant", variant_visitors, variant_conversions)
    if draws < 1000:
        raise ValueError(f"çekiliş sayısı en az 1000 olmalı (verilen: {draws})")
    if not 0 < credible < 1:
        raise ValueError(f"güvenilir aralık düzeyi 0 ile 1 arasında olmalı (verilen: {credible})")
    rng = random.Random(seed)
    a1, b1 = 1 + control_conversions, 1 + control_visitors - control_conversions
    a2, b2 = 1 + variant_conversions, 1 + variant_visitors - variant_conversions
    wins = 0
    loss_variant = loss_control = 0.0
    lifts = []
    for _ in range(draws):
        c = rng.betavariate(a1, b1)
        v = rng.betavariate(a2, b2)
        if v > c:
            wins += 1
            loss_control += v - c
        else:
            loss_variant += c - v
        if c > 0:
            lifts.append(v / c - 1)
    lifts.sort()
    q = (1 - credible) / 2
    return {
        "method": "bayesian-beta-binomial",
        "prior": "Beta(1,1)",
        "draws": draws,
        "seed": seed,
        "control_posterior_mean": round(a1 / (a1 + b1), 6),
        "variant_posterior_mean": round(a2 / (a2 + b2), 6),
        "prob_variant_beats_control": round(wins / draws, 4),
        "expected_loss_choose_variant": round(loss_variant / draws, 7),
        "expected_loss_choose_control": round(loss_control / draws, 7),
        "credible_level": credible,
        "credible_interval_relative_lift_pct": [round(_quantile(lifts, q) * 100, 2),
                                                round(_quantile(lifts, 1 - q) * 100, 2)],
        "note": "Alternatif bakış: bu Bayes özeti frekansçı 'significance' kararının yerine geçmez; "
                "karar kuralı test öncesinde belirlenmelidir.",
    }


def revenue(control_visitors, control_conversions, control_aov,
            variant_visitors, variant_conversions, variant_aov, margin_rate=None,
            variant_margin_rate=None):
    """Ziyaretçi başına gelir (RPV) ve — marj oranı verilirse — ziyaretçi başına brüt kâr
    karşılaştırması. Fiyat/indirim/paket testlerinde dönüşüm oranının geliri gizlemesini
    açığa çıkarır. Bu bir anlamlılık testi DEĞİLDİR: sipariş tutarı dağılımı çarpıktır,
    iki-oranlı z-testi burada geçerli değildir; sonuç yön göstergesidir."""
    for ad, v, c, aov in (("kontrol", control_visitors, control_conversions, control_aov),
                          ("varyant", variant_visitors, variant_conversions, variant_aov)):
        if v <= 0:
            raise ValueError(f"{ad} ziyaretçi sayısı pozitif olmalı (verilen: {v})")
        if c < 0:
            raise ValueError(f"{ad} dönüşüm sayısı negatif olamaz (verilen: {c})")
        if c > v:
            raise ValueError(f"{ad} dönüşüm sayısı ({c}) ziyaretçi sayısından ({v}) büyük olamaz")
        if aov < 0:
            raise ValueError(f"{ad} ortalama sipariş tutarı negatif olamaz (verilen: {aov})")
    for ad, mr in (("kontrol", margin_rate), ("varyant", variant_margin_rate)):
        if mr is not None and not 0 <= mr <= 1:
            raise ValueError(f"{ad} marj oranı 0 ile 1 arasında olmalı (verilen: {mr})")
    if variant_margin_rate is not None and margin_rate is None:
        raise ValueError("varyant marj oranı verildiyse kontrol marj oranı da verilmelidir")
    # Varyantın marjı ayrıca verilmediyse kontrolünkiyle aynı varsayılır.
    v_margin = variant_margin_rate if variant_margin_rate is not None else margin_rate

    cr_c = control_conversions / control_visitors
    cr_v = variant_conversions / variant_visitors
    rpv_c = control_conversions * control_aov / control_visitors
    rpv_v = variant_conversions * variant_aov / variant_visitors

    def pct_change(old, new):
        return ((new - old) / old * 100) if old > 0 else None

    cr_change = pct_change(cr_c, cr_v)
    aov_change = pct_change(control_aov, variant_aov)
    rpv_change = pct_change(rpv_c, rpv_v)

    result = {
        "control": {"cr": round(cr_c, 5), "aov": round(control_aov, 2), "rpv": round(rpv_c, 4)},
        "variant": {"cr": round(cr_v, 5), "aov": round(variant_aov, 2), "rpv": round(rpv_v, 4)},
        "cr_change_pct": round(cr_change, 2) if cr_change is not None else None,
        "aov_change_pct": round(aov_change, 2) if aov_change is not None else None,
        "rpv_change_pct": round(rpv_change, 2) if rpv_change is not None else None,
        "margin_rate": margin_rate,
        "profit_per_visitor": None,
        "warning": None,
        "note": "Bu bir anlamlılık testi değildir; sipariş tutarı dağılımı çarpık olduğu için "
                "z-testi burada geçerli değildir. Yön göstergesi olarak okuyun ve dönüşüm oranının "
                "anlamlılığını ayrıca 'significance' komutuyla kontrol edin. Ziyaretçi başına gelir için "
                "istatistiksel çıkarım (Welch t, bootstrap, CUPED) gerekiyorsa kullanıcı başına veriyle "
                "'continuous' komutunu kullanın.",
        "inference_command": "continuous",
    }

    if margin_rate is not None:
        profit_c = rpv_c * margin_rate
        profit_v = rpv_v * v_margin
        result["variant_margin_rate"] = v_margin
        result["profit_per_visitor"] = {
            "control": round(profit_c, 4),
            "variant": round(profit_v, 4),
            "change_pct": round(pct_change(profit_c, profit_v), 2) if profit_c > 0 else None,
        }
        if variant_margin_rate is None:
            result["profit_per_visitor"]["assumption"] = (
                "Varyantın brüt marj oranı kontrolünkiyle aynı varsayıldı. Fiyat, indirim veya "
                "paket değişikliği test ediliyorsa bu varsayım genelde yanlıştır: birim maliyet "
                "sabitken fiyat düşerse varyantın marjı da düşer. Gerçek oranı biliyorsanız "
                "--variant-margin-rate ile verin."
            )

    if cr_change is not None and rpv_change is not None and cr_change > 0 and rpv_change < 0:
        result["warning"] = (
            f"Dönüşüm oranı %{cr_change:.1f} arttı ama ziyaretçi başına gelir %{abs(rpv_change):.1f} DÜŞTÜ — "
            "bu testte kazanan kararı dönüşüm oranına göre verilirse gelir kaybedilir. "
            "Birincil metrik RPV olmalı."
        )
    elif cr_change is not None and rpv_change is not None and cr_change < 0 and rpv_change > 0:
        result["warning"] = (
            f"Dönüşüm oranı %{abs(cr_change):.1f} düştü ama ziyaretçi başına gelir %{rpv_change:.1f} arttı — "
            "daha az ama daha değerli sipariş. Dönüşüm oranına bakıp bu varyantı elemeyin."
        )

    return result


def format_text(command, r):
    """İnsan okunur özet — bağımsız CLI kullanımı için (--format text)."""
    if command == "significance" and "comparisons" in r:
        lines = [f"Kontrol: %{r['control_rate'] * 100:.2f} ({r['n_comparisons']} karşılaştırma, Holm düzeltmesi)"]
        for c in r["comparisons"]:
            lines.append(
                f"  {c['arm']}: %{c['variant_rate'] * 100:.2f}, p = {c['p_value_raw']} "
                f"(düzeltilmiş {c['p_value_adjusted']}, {c['method']}) → {c['decision']}")
        lines.append(r["note"])
        return "\n".join(lines)
    if command == "significance":
        lines = [
            f"Kontrol: %{r['control_rate'] * 100:.2f} → Varyant: %{r['variant_rate'] * 100:.2f}",
            f"Fark: {r['absolute_diff'] * 100:+.2f} yüzde puan"
            + (f" (göreli %{r['relative_lift_pct']:+.1f})" if r["relative_lift_pct"] is not None else ""),
            f"z = {r['z_score']}, p = {r['p_value']} [{r['method']}] → "
            + ("anlamlı" if r["is_significant"] else "anlamlı değil")
            + f" (güven düzeyi %{r['confidence_level'] * 100:.0f})"
            + ("" if r["normal_approx_valid"] else "  [nadir olay: Fisher exact kullanıldı]"),
            f"Farkın güven aralığı: [{r['confidence_interval_diff'][0] * 100:.2f}, "
            f"{r['confidence_interval_diff'][1] * 100:.2f}] yüzde puan",
        ]
        if r.get("confidence_interval_relative_lift_pct"):
            lo, hi = r["confidence_interval_relative_lift_pct"]
            lines.append(f"Göreli lift güven aralığı: [%{lo:+.1f}, %{hi:+.1f}]")
        if r.get("mde_at_current_n_pct") is not None:
            lines.append(f"Mevcut örneklemde %80 güçle saptanabilir en küçük göreli fark: %{r['mde_at_current_n_pct']:.1f}")
        if r.get("peeking_risk"):
            lines.append("Karar: ara bakış, nihai karar verilmez")
        for w in r.get("warnings") or ([r["note"]] if r.get("note") else []):
            lines.append(f"Uyarı: {w}")
        return "\n".join(lines)
    if command == "srm":
        if "observed_split" in r:
            head = f"Gözlenen bölüşüm: %{r['observed_split'] * 100:.2f} (beklenen %{r['expected_split'] * 100:.0f})"
        else:
            head = ("Gözlenen paylar: " + ", ".join(f"%{s * 100:.2f}" for s in r["observed_shares"])
                    + " (beklenen " + ", ".join(f"%{s * 100:.1f}" for s in r["expected_shares"]) + ")")
        lines = [
            head,
            f"chi2 = {r['chi2']} (sd {r['df']}), p = {r['p_value']} → "
            + ("SRM TESPİT EDİLDİ — sonuçlar güvenilmez" if r["srm_detected"] else "SRM yok")
            + ("" if r["normal_approx_valid"] else "  [yaklaşım zayıf, aşağıya bakın]"),
        ]
        if r["note"]:
            lines.append(f"Uyarı: {r['note']}")
        return "\n".join(lines)
    if command == "continuous":
        c, v = r["control"], r["variant"]
        lines = [
            f"Ortalama: {c['mean']:,.4f} → {v['mean']:,.4f}"
            + (f" (göreli %{r['relative_lift_pct']:+.1f})" if r["relative_lift_pct"] is not None else ""),
            f"Welch t = {r['t_stat']}, sd = {r['df']}, p = {r['p_value']} → "
            + ("anlamlı" if r["is_significant"] else "anlamlı değil"),
            f"Farkın güven aralığı: [{r['confidence_interval_diff'][0]:,.4f}, {r['confidence_interval_diff'][1]:,.4f}]",
        ]
        if r.get("bootstrap"):
            b = r["bootstrap"]
            lines.append(f"Bootstrap ({b['resamples']} tekrar) fark aralığı: [{b['ci_diff'][0]:,.4f}, {b['ci_diff'][1]:,.4f}]")
        if r.get("cuped"):
            cu = r["cuped"]
            lines.append(f"CUPED: varyans azalması %{cu['variance_reduction_pct']}, p = {cu['p_value']} → "
                         + ("anlamlı" if cu["is_significant"] else "anlamlı değil"))
        if r["note"]:
            lines.append(f"Not: {r['note']}")
        return "\n".join(lines)
    if command == "bayes":
        lo, hi = r["credible_interval_relative_lift_pct"]
        return "\n".join([
            f"P(varyant > kontrol) = %{r['prob_variant_beats_control'] * 100:.1f}",
            f"Beklenen kayıp — varyantı seçersen: {r['expected_loss_choose_variant']}, "
            f"kontrolü seçersen: {r['expected_loss_choose_control']}",
            f"Göreli lift %{r['credible_level'] * 100:.0f} güvenilir aralığı: [%{lo:+.1f}, %{hi:+.1f}]",
            r["note"],
        ])
    if command == "revenue":
        c, v = r["control"], r["variant"]
        lines = [
            f"Dönüşüm oranı: %{c['cr'] * 100:.2f} → %{v['cr'] * 100:.2f} "
            + (f"(%{r['cr_change_pct']:+.1f})" if r["cr_change_pct"] is not None else ""),
            f"Ortalama sipariş tutarı: {c['aov']:,.2f} → {v['aov']:,.2f} "
            + (f"(%{r['aov_change_pct']:+.1f})" if r["aov_change_pct"] is not None else ""),
            f"Ziyaretçi başına gelir (RPV): {c['rpv']:,.2f} → {v['rpv']:,.2f} "
            + (f"(%{r['rpv_change_pct']:+.1f})" if r["rpv_change_pct"] is not None else ""),
        ]
        if r["profit_per_visitor"]:
            p = r["profit_per_visitor"]
            lines.append(
                # İki kolun marjı farklıysa etiketi gizlemek yanıltıcı olur:
                # varyant değeri kendi marjıyla hesaplanmıştır, tek marj basma.
                f"Ziyaretçi başına brüt kâr (marj "
                + (f"%{r['margin_rate'] * 100:.0f} → %{r['variant_margin_rate'] * 100:.0f}"
                   if r.get("variant_margin_rate") not in (None, r["margin_rate"])
                   else f"%{r['margin_rate'] * 100:.0f}")
                + f"): {p['control']:,.2f} → {p['variant']:,.2f} "
                + (f"(%{p['change_pct']:+.1f})" if p["change_pct"] is not None else "")
            )
        if r["warning"]:
            lines.append(f"\nDİKKAT: {r['warning']}")
        lines.append(f"\n{r['note']}")
        return "\n".join(lines)
    return (
        f"Baz oran %{r['baseline_rate'] * 100:.2f}, hedef %{r['target_rate'] * 100:.2f} "
        f"(göreli %{r['mde_relative_pct']:.0f} lift) için varyant başına {r['required_n_per_variant']:,} "
        f"ziyaretçi gerekir (toplam {r['required_n_total']:,}; güven %{r['confidence_level'] * 100:.0f}, "
        f"güç %{r['power'] * 100:.0f})."
        + (f" Kontrol {r['required_n_control']:,} / varyant {r['required_n_variant']:,}."
           if r.get("ratio", 1) != 1 else "")
        + (f"\nNot: {r['note']}" if r.get("note") else "")
    )


def _parse_list(s, conv, label):
    try:
        return [conv(x) for x in str(s).split(",") if x.strip()]
    except (ValueError, argparse.ArgumentTypeError):
        raise ValueError(f"{label} virgülle ayrılmış sayılar olmalı (verilen: {s!r})")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    alt_help = "Hipotez yönü: two-sided (varsayılan), greater (varyant > kontrol), less"

    p1 = sub.add_parser("significance", help="Varyant(lar)ı kontrolle karşılaştır (z-testi / Fisher exact)")
    p1.add_argument("--control-visitors", type=parse_count, required=True)
    p1.add_argument("--control-conversions", type=parse_count, required=True)
    p1.add_argument("--variant-visitors", type=parse_count, default=None)
    p1.add_argument("--variant-conversions", type=parse_count, default=None)
    p1.add_argument("--variant", type=parse_arm, action="append", default=[],
                    help="Tekrarlanabilir ZİYARETÇİ:DÖNÜŞÜM, ör. --variant 5000:290 --variant 5000:270 (A/B/n)")
    p1.add_argument("--confidence", type=float, default=0.95)
    p1.add_argument("--alternative", choices=_ALTERNATIVES, default="two-sided", help=alt_help)
    p1.add_argument("--planned-n", type=parse_count, default=None,
                    help="Kol başına planlanan örneklem; altındaysa ara bakış (peeking) uyarısı verilir")
    p1.add_argument("--format", choices=["json", "text"], default="json")

    p3 = sub.add_parser("revenue", help="Gelir/kâr yön göstergesi (çıkarım için 'continuous' kullanın)")
    p3.add_argument("--control-visitors", type=parse_count, required=True)
    p3.add_argument("--control-conversions", type=parse_count, required=True)
    p3.add_argument("--control-aov", type=float, required=True, help="Kontrolde ortalama sipariş tutarı")
    p3.add_argument("--variant-visitors", type=parse_count, required=True)
    p3.add_argument("--variant-conversions", type=parse_count, required=True)
    p3.add_argument("--variant-aov", type=float, required=True, help="Varyantta ortalama sipariş tutarı")
    p3.add_argument("--margin-rate", type=float, default=None, help="Kontrol kolunun brüt marj oranı, ör. 0.35")
    p3.add_argument("--variant-margin-rate", type=float, default=None,
                    help="Varyantın brüt marj oranı farklıysa (fiyat/indirim testi); verilmezse kontrolünkiyle aynı varsayılır")
    p3.add_argument("--format", choices=["json", "text"], default="json")

    p4 = sub.add_parser("srm", help="Örneklem oranı uyuşmazlığı (SRM) kontrolü — randomizasyonu denetler, sonucu değil")
    p4.add_argument("--control-visitors", type=parse_count, default=None)
    p4.add_argument("--variant-visitors", type=parse_count, default=None)
    p4.add_argument("--expected-split", type=float, default=0.5, help="Kontrol koluna planlanan pay, ör. 0.5")
    p4.add_argument("--visitors", default=None, help="k kol için virgülle ayrılmış ziyaretçi sayıları, ör. 5000,5100,4900")
    p4.add_argument("--expected-ratios", default=None, help="k kol için planlanan oranlar, ör. 1,1,2 (varsayılan eşit)")
    p4.add_argument("--format", choices=["json", "text"], default="json")

    p2 = sub.add_parser("samplesize", help="Gereken örneklem büyüklüğünü hesapla")
    p2.add_argument("--baseline-rate", type=float, required=True, help="Ör. 0.05 (%5 dönüşüm)")
    p2.add_argument("--mde", type=float, required=True, help="Göreli minimum tespit edilebilir fark, ör. 0.20")
    p2.add_argument("--confidence", type=float, default=0.95)
    p2.add_argument("--power", type=float, default=0.80)
    p2.add_argument("--alternative", choices=_ALTERNATIVES, default="two-sided", help=alt_help)
    p2.add_argument("--ratio", type=float, default=1.0, help="Varyant/kontrol örneklem oranı (n_varyant = ratio * n_kontrol)")
    p2.add_argument("--arms", type=parse_count, default=2, help="Kontrol dahil toplam kol sayısı (Bonferroni)")
    p2.add_argument("--format", choices=["json", "text"], default="json")

    p5 = sub.add_parser("continuous", help="Sürekli metrik (ziyaretçi başına gelir vb.): Welch t, bootstrap, CUPED")
    p5.add_argument("--control-csv", default=None, help="Kontrol: satır başına bir kullanıcı değeri (sıfırlar dahil)")
    p5.add_argument("--variant-csv", default=None)
    p5.add_argument("--control-n", type=parse_count, default=None)
    p5.add_argument("--control-mean", type=float, default=None)
    p5.add_argument("--control-sd", type=float, default=None)
    p5.add_argument("--variant-n", type=parse_count, default=None)
    p5.add_argument("--variant-mean", type=float, default=None)
    p5.add_argument("--variant-sd", type=float, default=None)
    p5.add_argument("--confidence", type=float, default=0.95)
    p5.add_argument("--alternative", choices=_ALTERNATIVES, default="two-sided", help=alt_help)
    p5.add_argument("--winsorize", type=float, default=None, help="Üst kuyruğu bu yüzdelikte kırp, ör. 0.99")
    p5.add_argument("--bootstrap", type=parse_count, default=0, help="Yüzdelik bootstrap tekrar sayısı, ör. 2000")
    p5.add_argument("--seed", type=int, default=None)
    p5.add_argument("--control-pre-csv", default=None, help="CUPED: kontrol ön-dönem kovaryatı (aynı sıra)")
    p5.add_argument("--variant-pre-csv", default=None, help="CUPED: varyant ön-dönem kovaryatı (aynı sıra)")
    p5.add_argument("--format", choices=["json", "text"], default="json")

    p6 = sub.add_parser("bayes", help="Bayes görünümü (alternatif bakış; frekansçı kararın yerine geçmez)")
    p6.add_argument("--control-visitors", type=parse_count, required=True)
    p6.add_argument("--control-conversions", type=parse_count, required=True)
    p6.add_argument("--variant-visitors", type=parse_count, required=True)
    p6.add_argument("--variant-conversions", type=parse_count, required=True)
    p6.add_argument("--draws", type=parse_count, default=100000)
    p6.add_argument("--seed", type=int, default=None)
    p6.add_argument("--credible", type=float, default=0.95)
    p6.add_argument("--format", choices=["json", "text"], default="json")

    args = parser.parse_args()

    try:
        if args.command == "significance":
            variants = list(args.variant)
            if args.variant_visitors is not None or args.variant_conversions is not None:
                if args.variant_visitors is None or args.variant_conversions is None:
                    raise ValueError("--variant-visitors ve --variant-conversions birlikte verilmeli")
                variants.insert(0, (args.variant_visitors, args.variant_conversions))
            if not variants:
                raise ValueError("en az bir varyant verin: --variant-visitors/--variant-conversions veya --variant Z:D")
            if len(variants) == 1:
                result = significance(args.control_visitors, args.control_conversions,
                                      variants[0][0], variants[0][1], args.confidence,
                                      args.alternative, args.planned_n)
            else:
                result = significance_multi(args.control_visitors, args.control_conversions, variants,
                                            args.confidence, args.alternative, args.planned_n)
        elif args.command == "revenue":
            result = revenue(args.control_visitors, args.control_conversions, args.control_aov,
                             args.variant_visitors, args.variant_conversions, args.variant_aov,
                             args.margin_rate, args.variant_margin_rate)
        elif args.command == "srm":
            if args.visitors:
                ratios = _parse_list(args.expected_ratios, float, "--expected-ratios") if args.expected_ratios else None
                result = srm_multi(_parse_list(args.visitors, parse_count, "--visitors"), ratios)
            else:
                if args.control_visitors is None or args.variant_visitors is None:
                    raise ValueError("--control-visitors ve --variant-visitors (veya --visitors) verin")
                result = srm(args.control_visitors, args.variant_visitors, args.expected_split)
        elif args.command == "continuous":
            kw = dict(confidence=args.confidence, alternative=args.alternative, winsorize=args.winsorize,
                      bootstrap=args.bootstrap, seed=args.seed)
            if args.control_csv or args.variant_csv:
                if not (args.control_csv and args.variant_csv):
                    raise ValueError("--control-csv ve --variant-csv birlikte verilmeli")
                kw["control"] = read_values_csv(args.control_csv)
                kw["variant"] = read_values_csv(args.variant_csv)
                if args.control_pre_csv:
                    kw["control_pre"] = read_values_csv(args.control_pre_csv)
                if args.variant_pre_csv:
                    kw["variant_pre"] = read_values_csv(args.variant_pre_csv)
            else:
                stats = [args.control_n, args.control_mean, args.control_sd,
                         args.variant_n, args.variant_mean, args.variant_sd]
                if any(s is None for s in stats):
                    raise ValueError("CSV yoksa iki kol için de --*-n, --*-mean, --*-sd verilmeli")
                kw["control_stats"] = tuple(stats[:3])
                kw["variant_stats"] = tuple(stats[3:])
            result = continuous(**kw)
        elif args.command == "bayes":
            result = bayes(args.control_visitors, args.control_conversions,
                           args.variant_visitors, args.variant_conversions,
                           args.draws, args.seed, args.credible)
        else:
            result = sample_size(args.baseline_rate, args.mde, args.confidence, args.power,
                                 args.alternative, args.ratio, args.arms)
    except (ValueError, OSError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    if args.format == "text":
        print(format_text(args.command, result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
