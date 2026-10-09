#!/usr/bin/env python3
"""
A/B test istatistik motoru (v2.1): oran testleri, guardrail (non-inferiority), örneklem ve süre
planı, SRM, sürekli metrikler, segment etkileşimi, Bayes görünümü.

Mesaj dili: --lang en|tr (varsayılan en). Sayısal alanlar ve alan adları iki dilde aynıdır.

Kullanım:
  Sonuç yorumlama (iki kol; normal yaklaşım geçersizse otomatik Fisher exact):
    python3 analyze_results.py significance \\
      --control-visitors 5000 --control-conversions 250 \\
      --variant-visitors 5000 --variant-conversions 290 [--alternative greater] [--planned-n 8000]

  A/B/n (her varyant kontrolle kıyaslanır, Holm düzeltmesi):
    python3 analyze_results.py significance --control-visitors 5000 --control-conversions 250 \\
      --variant 5000:290 --variant 5000:270

  Guardrail (non-inferiority; marj göreli kesir, ör. 0.02):
    python3 analyze_results.py significance ... --ni-margin 0.02 \\
      --guardrail-direction must_not_increase|must_not_decrease

  Örneklem büyüklüğü ve süre (ters yön: --weeks ile saptanabilir MDE):
    python3 analyze_results.py samplesize --baseline-rate 0.05 --mde 0.20 \\
      [--ratio 2] [--arms 3] [--alternative greater] [--daily-visitors 4000]
    python3 analyze_results.py samplesize --metric mean --baseline-mean 42 --baseline-sd 120 --mde 0.05
    python3 analyze_results.py samplesize --baseline-rate 0.05 --weeks 3 --daily-visitors 4000

  SRM (2 veya daha fazla kol):
    python3 analyze_results.py srm --control-visitors 5012 --variant-visitors 4988
    python3 analyze_results.py srm --visitors 5000,5100,4900 [--expected-ratios 1,1,1]

  Sürekli metrik (Welch t-testi, winsorize, bootstrap, CUPED):
    python3 analyze_results.py continuous --control-csv c.csv --variant-csv v.csv \\
      --value-column revenue [--id-column user_id --control-pre-csv cp.csv --variant-pre-csv vp.csv]
    python3 analyze_results.py continuous --control-n 5000 --control-mean 4.1 --control-sd 20 \\
      --variant-n 5000 --variant-mean 4.6 --variant-sd 22

  Segment etkileşimi (etki segmentler arasında gerçekten farklı mı?):
    python3 analyze_results.py interaction --seg1 4000:200,4000:260 --seg2 6000:300,6000:310 \\
      [--seg1-name mobil --seg2-name masaüstü]

  Bayes görünümü (alternatif bakış, frekansçı kararın yerine geçmez):
    python3 analyze_results.py bayes --control-visitors 5000 --control-conversions 250 \\
      --variant-visitors 5000 --variant-conversions 290 [--draws 100000 --seed 12345]

  Gelir/kâr yön göstergesi (çıkarım için 'continuous' kullanın):
    python3 analyze_results.py revenue ... [--margin-rate 0.35 --variant-margin-rate 0.28]

Tam sayı girdileri esnektir: 1000, 1e3, 1,000 ve 1_000 kabul edilir.
Sadece Python standart kütüphanesi kullanır. Dış bağımlılık yok.
"""
import argparse
import csv
import json
import math
import random
import re
import sys
from collections import Counter

_EPS = 3e-16
_FPMIN = 1e-300
DEFAULT_SEED = 12345
# Kâr erimesi uyarısı için küçük eşik (göreli %): bunun altındaki düşüş gürültü sayılır.
_PROFIT_DROP_WARN_PCT = 1.0

_DESCRIPTION_EN = """\
A/B test statistics engine (v2.1): proportion tests, guardrail (non-inferiority), sample-size and
duration planning, SRM, continuous metrics, segment interaction, Bayesian view.

Message language: --lang en|tr (default en). Numeric fields and field names are identical in both.

Examples:
  significance --control-visitors 5000 --control-conversions 250 --variant-visitors 5000 --variant-conversions 290
  significance ... --variant 5000:290 --variant 5000:270            (A/B/n, Holm)
  significance ... --ni-margin 0.02 --guardrail-direction must_not_increase   (guardrail)
  samplesize --baseline-rate 0.05 --mde 0.20 [--daily-visitors 4000]
  samplesize --metric mean --baseline-mean 42 --baseline-sd 120 --mde 0.05
  samplesize --baseline-rate 0.05 --weeks 3 --daily-visitors 4000   (inverse: detectable MDE)
  srm --visitors 5000,5100,4900
  continuous --control-csv c.csv --variant-csv v.csv --value-column revenue [--id-column user_id ...]
  interaction --seg1 4000:200,4000:260 --seg2 6000:300,6000:310
  bayes ... [--seed 12345]
  revenue ... [--margin-rate 0.35 --variant-margin-rate 0.28]

Integer inputs are flexible: 1000, 1e3, 1,000 and 1_000 are accepted. Python standard library only.
"""

# ---------------------------------------------------------------------------
# Dil
# ---------------------------------------------------------------------------

_LANGS = ("en", "tr")
LANG = "en"


def set_lang(lang):
    """Mesaj dilini ayarlar ('en' veya 'tr'). CLI bunu --lang ile çağırır."""
    global LANG
    if lang not in _LANGS:
        raise ValueError(f"lang must be one of {_LANGS} (given: {lang!r})")
    LANG = lang


def _t(tr, en):
    return tr if LANG == "tr" else en


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
        raise ValueError(_t("p, 0 ile 1 arasında olmalı", "p must be between 0 and 1"))

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
        raise ValueError(_t("q, 0 ile 1 arasında olmalı", "q must be between 0 and 1"))
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


def _t_p(t, df, alternative):
    """t istatistiğinden p: 'greater' = P(T >= t), 'less' = P(T <= t), iki yönlü = P(|T| >= |t|)."""
    p2 = t_sf_two_sided(t, df)
    if alternative == "greater":
        return p2 / 2 if t > 0 else 1 - p2 / 2
    if alternative == "less":
        return p2 / 2 if t < 0 else 1 - p2 / 2
    return p2


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


def _r(x, digits):
    return None if x is None else round(x, digits)


def _sided(lo, hi, alternative):
    """Tek yönlü hipotezde yalnızca karar yönündeki sınır raporlanır: greater → [alt, None]."""
    if alternative == "greater":
        return [lo, None]
    if alternative == "less":
        return [None, hi]
    return [lo, hi]


def _excludes_zero(ci, alternative, null=0.0):
    lo, hi = ci
    if alternative == "greater":
        return lo is not None and lo > null
    if alternative == "less":
        return hi is not None and hi < null
    return (lo is not None and lo > null) or (hi is not None and hi < null)


_ALTERNATIVES = ("two-sided", "greater", "less")
_GUARDRAIL_DIRECTIONS = ("must_not_decrease", "must_not_increase")


def _check_alternative(alternative, confidence=None):
    if alternative not in _ALTERNATIVES:
        raise ValueError(_t(f"alternative şunlardan biri olmalı: {', '.join(_ALTERNATIVES)} (verilen: {alternative})",
                            f"alternative must be one of: {', '.join(_ALTERNATIVES)} (given: {alternative})"))
    if confidence is not None and alternative != "two-sided" and confidence <= 0.5:
        raise ValueError(_t(f"tek yönlü testte güven düzeyi 0.5'ten büyük olmalı (verilen: {confidence})",
                            f"a one-sided test needs a confidence level above 0.5 (given: {confidence})"))


def _check_confidence(confidence):
    if not 0 < confidence < 1:
        raise ValueError(_t(f"güven düzeyi 0 ile 1 arasında olmalı (verilen: {confidence})",
                            f"confidence level must be between 0 and 1 (given: {confidence})"))


def _normalize_relative(value, flag):
    """Göreli kesir bekleyen girdiler (MDE, NI marjı): mutlak değeri 1'den büyükse yüzde sayılır
    (10 → 0.10). 1.5 gibi bir değer de %1.5 okunur; %150 kastediliyorsa bu araçla planlanmaz."""
    if abs(value) > 1:
        new = value / 100
        return new, _t(
            f"{flag} {value:g} 1'den büyük; yüzde olarak yorumlandı ({value:g} → {new:g}). "
            "Göreli değerler kesir olarak verilir: %10 için 0.10.",
            f"{flag} {value:g} is greater than 1, so it was read as a percentage ({value:g} → {new:g}). "
            "Relative values are fractions: 0.10 for 10%.")
    return value, None


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
        raise argparse.ArgumentTypeError(_t(f"tam sayı bekleniyordu (verilen: {s!r})",
                                            f"expected an integer (given: {s!r})"))
    if not math.isfinite(val) or val != int(val):
        raise argparse.ArgumentTypeError(_t(f"tam sayı bekleniyordu (verilen: {s!r})",
                                            f"expected an integer (given: {s!r})"))
    return int(val)


parse_count.__name__ = "tam_sayi"


def parse_arm(s):
    """'5000:290' → (5000, 290)."""
    parts = str(s).split(":")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(_t(
            f"ZİYARETÇİ:DÖNÜŞÜM biçimi bekleniyordu, ör. 5000:290 (verilen: {s!r})",
            f"expected VISITORS:CONVERSIONS, e.g. 5000:290 (given: {s!r})"))
    return parse_count(parts[0]), parse_count(parts[1])


parse_arm.__name__ = "kol"


def parse_segment(s):
    """'4000:200,4000:260' → ((4000, 200), (4000, 260)): önce kontrol (A), sonra varyant (B)."""
    parts = [p for p in str(s).split(",") if p.strip()]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError(_t(
            f"A_ZİY:A_DÖN,B_ZİY:B_DÖN biçimi bekleniyordu, ör. 4000:200,4000:260 (verilen: {s!r})",
            f"expected A_VIS:A_CONV,B_VIS:B_CONV, e.g. 4000:200,4000:260 (given: {s!r})"))
    return parse_arm(parts[0].strip()), parse_arm(parts[1].strip())


parse_segment.__name__ = "segment"


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


def _arm_name(ad):
    return {"kontrol": _t("kontrol", "control"), "varyant": _t("varyant", "variant")}.get(ad, ad)


def _validate_arm(ad, v, c):
    ad = _arm_name(ad)
    if v <= 0:
        raise ValueError(_t(f"{ad} ziyaretçi sayısı pozitif olmalı (verilen: {v})",
                            f"{ad} visitors must be positive (given: {v})"))
    if c < 0:
        raise ValueError(_t(f"{ad} dönüşüm sayısı negatif olamaz (verilen: {c})",
                            f"{ad} conversions cannot be negative (given: {c})"))
    if c > v:
        raise ValueError(_t(f"{ad} dönüşüm sayısı ({c}) ziyaretçi sayısından ({v}) büyük olamaz",
                            f"{ad} conversions ({c}) cannot exceed visitors ({v})"))


def _decision_text(code):
    return {
        "significant": _t("anlamlı", "significant"),
        "not_significant": _t("anlamlı değil", "not significant"),
        "interim_no_decision": _t("ara bakış: nihai karar verilmez", "interim look: no final decision"),
    }[code]


def _observed_power_note():
    return _t(
        "Gözlenen (post-hoc) güç, gözlenen etkiden ve p-değerinden türetilir; yeni bilgi taşımaz ve "
        "bir etkinin varlığı ya da yokluğu için kanıt değildir. Kararı bununla gerekçelendirmeyin; "
        "örneklem yeterliliği için mde_at_current_n_pct ve 'samplesize' kullanın.",
        "Observed (post-hoc) power is a function of the observed effect and the p-value; it adds no "
        "information and is not evidence for or against an effect. Don't justify a decision with it; "
        "use mde_at_current_n_pct and 'samplesize' to judge whether the sample was sufficient.")


# ---------------------------------------------------------------------------
# Guardrail: non-inferiority (göreli marj)
# ---------------------------------------------------------------------------

def _prepare_ni(margin, direction):
    if direction not in _GUARDRAIL_DIRECTIONS:
        raise ValueError(_t(
            f"guardrail yönü şunlardan biri olmalı: {', '.join(_GUARDRAIL_DIRECTIONS)} (verilen: {direction})",
            f"guardrail direction must be one of: {', '.join(_GUARDRAIL_DIRECTIONS)} (given: {direction})"))
    margin, conv_note = _normalize_relative(margin, "--ni-margin")
    if not 0 < margin < 1:
        raise ValueError(_t(f"non-inferiority marjı 0 ile 1 arasında göreli bir kesir olmalı, ör. 0.02 (verilen: {margin})",
                            f"non-inferiority margin must be a relative fraction between 0 and 1, e.g. 0.02 (given: {margin})"))
    theta = 1 - margin if direction == "must_not_decrease" else 1 + margin
    return margin, theta, conv_note


def _ni_result(margin, direction, theta, observed_rel, stat_name, stat, p_ni, p_harm, alpha,
               method, conv_note, df=None):
    passed = p_ni < alpha
    degraded = p_harm < alpha
    status = "clean" if passed else ("degraded" if degraded else "inconclusive")
    if direction == "must_not_decrease":
        h0 = _t(f"H0: varyant kontrolden marjdan (%{margin * 100:g}) fazla kötü (varyant ≤ {theta:g} × kontrol)",
                f"H0: variant is worse than control by more than the margin ({margin * 100:g}%) "
                f"(variant ≤ {theta:g} × control)")
    else:
        h0 = _t(f"H0: varyant kontrolü marjdan (%{margin * 100:g}) fazla artırıyor (varyant ≥ {theta:g} × kontrol)",
                f"H0: variant raises the metric by more than the margin ({margin * 100:g}%) "
                f"(variant ≥ {theta:g} × control)")
    status_txt = {
        "clean": _t("temiz: zarar marjın içinde kaldığı tek yönlü testle gösterildi",
                    "clean: the one-sided test shows the harm stays inside the margin"),
        "degraded": _t("kötüleşti: zarar anlamlı biçimde marjın ötesinde",
                       "degraded: the harm is significantly beyond the margin"),
        "inconclusive": _t("belirsiz: ne marj içinde kaldığı ne de marjı aştığı gösterilebildi — 'temiz' sayılmaz",
                           "inconclusive: neither inside nor beyond the margin could be shown — not 'clean'"),
    }[status]
    out = {
        "margin_relative": margin,
        "direction": direction,
        "threshold_ratio": round(theta, 6),
        "observed_relative_change_pct": _r(observed_rel * 100 if observed_rel is not None else None, 2),
        stat_name: round(stat, 4),
        "p_value": _round_p(p_ni),
        "p_value_degraded": _round_p(p_harm),
        "passed": passed,
        "status": status,
        "method": method,
        "null_hypothesis": h0,
        "note": " ".join(x for x in (status_txt, conv_note) if x),
    }
    if df is not None:
        out["df"] = round(df, 2)
    return out


def non_inferiority_proportions(x1, n1, x2, n2, margin, direction="must_not_decrease", confidence=0.95):
    """Oran için göreli marjlı non-inferiority (Wald, oran sınırı doğrusallaştırılmış):
    Δ = p_v − θ·p_k, Var = p_v(1−p_v)/n_v + θ²·p_k(1−p_k)/n_k; θ = 1 − marj (must_not_decrease)
    veya 1 + marj (must_not_increase). Tek yönlü; 'passed' = H0 (marjdan fazla zarar) reddedildi."""
    margin, theta, conv_note = _prepare_ni(margin, direction)
    alpha = 1 - confidence
    p1, p2 = x1 / n1, x2 / n2
    se = math.sqrt(p2 * (1 - p2) / n2 + theta * theta * p1 * (1 - p1) / n1)
    stat = p2 - theta * p1
    good = "greater" if direction == "must_not_decrease" else "less"
    bad = "less" if good == "greater" else "greater"
    if se > 0:
        z = stat / se
        p_ni, p_harm = _p_from_z(z, good), _p_from_z(z, bad)
    else:  # iki oran da 0 veya 1: Wald varyansı tanımsız, karar verilmez
        z, p_ni, p_harm = 0.0, 1.0, 1.0
    observed_rel = (p2 / p1 - 1) if p1 > 0 else None
    return _ni_result(margin, direction, theta, observed_rel, "z", z, p_ni, p_harm, alpha,
                      "wald-ratio-margin", conv_note)


def non_inferiority_means(m1, v1, n1, m2, v2, n2, margin, direction="must_not_decrease", confidence=0.95):
    """Ortalama için göreli marjlı non-inferiority (Welch tipi): t = (m_v − θ·m_k) / sqrt(v_v/n_v + θ²·v_k/n_k),
    sd Welch-Satterthwaite. Göreli marj için kontrol ortalaması pozitif olmalı."""
    margin, theta, conv_note = _prepare_ni(margin, direction)
    if m1 <= 0:
        raise ValueError(_t("göreli non-inferiority marjı için kontrol ortalaması pozitif olmalı",
                            "a relative non-inferiority margin needs a positive control mean"))
    alpha = 1 - confidence
    a1 = theta * theta * v1 / n1
    a2 = v2 / n2
    se2 = a1 + a2
    stat = m2 - theta * m1
    good = "greater" if direction == "must_not_decrease" else "less"
    bad = "less" if good == "greater" else "greater"
    if se2 > 0:
        den = (a1 * a1 / (n1 - 1) if a1 > 0 else 0.0) + (a2 * a2 / (n2 - 1) if a2 > 0 else 0.0)
        df = se2 * se2 / den
        t = stat / math.sqrt(se2)
        p_ni, p_harm = _t_p(t, df, good), _t_p(t, df, bad)
    else:
        df, t, p_ni, p_harm = None, 0.0, 1.0, 1.0
    return _ni_result(margin, direction, theta, m2 / m1 - 1, "t", t, p_ni, p_harm, alpha,
                      "welch-ratio-margin", conv_note, df)


def _ni_warning(ni):
    if ni["status"] == "degraded":
        return _t(f"Guardrail kötüleşti: varyant izin verilen marjın (%{ni['margin_relative'] * 100:g}) ötesinde "
                  f"(p = {ni['p_value_degraded']}). Birincil metrik ne gösterirse göstersin test durdurulmalı.",
                  f"Guardrail degraded: the variant is beyond the tolerated margin ({ni['margin_relative'] * 100:g}%) "
                  f"(p = {ni['p_value_degraded']}). Stop the test whatever the primary metric shows.")
    if ni["status"] == "inconclusive":
        return _t("Guardrail belirsiz: zararın marj içinde kaldığı gösterilemedi; 'temiz' diye raporlamayın.",
                  "Guardrail inconclusive: it couldn't be shown that the harm stays inside the margin; "
                  "don't report it as clean.")
    return None


# ---------------------------------------------------------------------------
# İki kollu ve A/B/n anlamlılık
# ---------------------------------------------------------------------------

def significance(control_visitors, control_conversions, variant_visitors, variant_conversions,
                 confidence=0.95, alternative="two-sided", planned_n=None, power_target=0.80,
                 ni_margin=None, guardrail_direction="must_not_decrease"):
    """İki oranın karşılaştırması. Normal yaklaşım geçerliyse iki-oranlı z-testi,
    değilse otomatik Fisher exact testi; karar KULLANILAN yöntemin p-değerine dayanır.
    Tek yönlü hipotezde 'confidence_interval_diff' yalnızca karar yönündeki sınırı taşır;
    iki yönlü aralık 'confidence_interval_diff_two_sided' alanındadır."""
    _validate_arm("kontrol", control_visitors, control_conversions)
    _validate_arm("varyant", variant_visitors, variant_conversions)
    _check_confidence(confidence)
    _check_alternative(alternative, confidence)
    if planned_n is not None and planned_n <= 0:
        raise ValueError(_t(f"planlanan örneklem pozitif olmalı (verilen: {planned_n})",
                            f"planned sample must be positive (given: {planned_n})"))

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
    ci2 = newcombe_diff_ci(control_conversions, n1, variant_conversions, n2, confidence)
    rel2 = relative_lift_ci(control_conversions, n1, variant_conversions, n2, confidence)
    if alternative == "two-sided":
        ci, rel_ci = list(ci2), (list(rel2) if rel2 else None)
    else:
        # Tek yönlü %c sınırı = iki yönlü %(2c−1) aralığının o yöndeki ucu.
        lvl = 2 * confidence - 1
        ci = _sided(*newcombe_diff_ci(control_conversions, n1, variant_conversions, n2, lvl), alternative)
        rel1 = relative_lift_ci(control_conversions, n1, variant_conversions, n2, lvl)
        rel_ci = _sided(*rel1, alternative) if rel1 else None
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
    ci_agrees = _excludes_zero(ci, alternative) == is_significant

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

    ni = None
    if ni_margin is not None:
        ni = non_inferiority_proportions(control_conversions, n1, variant_conversions, n2,
                                         ni_margin, guardrail_direction, confidence)

    # Uyarılar öncelik sırasıyla; 'note' en öncelikli olanı, 'warnings' hepsini taşır.
    warnings = []
    if not normal_approx_valid:
        warnings.append(_t(
            "Nadir olay uyarısı: beklenen dönüşüm/dönüşmeme sayılarından en az biri "
            f"{min_expected_count}'un altında (en küçüğü {min(expected_counts):.1f}); normal yaklaşım geçerli değil. "
            "p-değeri ve anlamlılık kararı bu yüzden Fisher exact testiyle hesaplandı; güven aralığı "
            "Newcombe skor aralığıdır. Veri az, sonucu kesin bir kanıt gibi okumayın.",
            "Rare-event warning: at least one expected conversion/non-conversion count is below "
            f"{min_expected_count} (smallest {min(expected_counts):.1f}); the normal approximation isn't valid. "
            "The p-value and the significance decision were therefore computed with Fisher's exact test; the "
            "confidence interval is the Newcombe score interval. Data is thin; don't read this as firm evidence."))
    if peeking_risk:
        warnings.append(_t(
            f"Ara bakış (peeking) riski: kol başına planlanan {planned_n:,} ziyaretçiye ulaşılmadı "
            f"(en küçük kol {min(n1, n2):,}). Planlanan örneklem dolmadan erken durdurma yanlış pozitif "
            "oranını şişirir; bu sonuç nihai karar değildir.",
            f"Peeking risk: the planned {planned_n:,} visitors per arm hasn't been reached "
            f"(smallest arm {min(n1, n2):,}). Stopping before the planned sample inflates the false-positive "
            "rate; this result is not a final decision."))
    if ni is not None and _ni_warning(ni):
        warnings.append(_ni_warning(ni))
    if low_sample_warning and normal_approx_valid:
        warnings.append(_t(
            "Dönüşüm sayısı 250'nin altında: bu kaba bir uyarı eşiğidir, formal yeterlilik kriteri değil. "
            "Gerçek yeterliliği bu testin baz oranı/MDE'siyle 'samplesize' komutunu çalıştırarak doğrulayın.",
            "Fewer than 250 conversions: this is a rough warning floor, not a formal sufficiency criterion. "
            "Check real sufficiency by running 'samplesize' with this test's baseline rate and MDE."))
    if not ci_agrees and normal_approx_valid:
        warnings.append(_t(
            "Sınır durumu: p-değeri (z-testi, birleşik varyans) ile güven sınırı (Newcombe) farklı yöntemlerle "
            "hesaplanır ve burada uyuşmuyor. Sonuç eşikte; kesin kanıt gibi okumayın.",
            "Borderline: the p-value (pooled z-test) and the confidence bound (Newcombe) use different methods "
            "and disagree here. The result sits on the threshold; don't read it as firm evidence."))

    if peeking_risk:
        code = "interim_no_decision"
    else:
        code = "significant" if is_significant else "not_significant"

    out = {
        "control_rate": round(p1, 5),
        "variant_rate": round(p2, 5),
        "absolute_diff": round(diff, 5),
        "absolute_diff_pp": round(diff * 100, 3),
        "relative_lift_pct": round(relative_lift * 100, 2) if relative_lift is not None else None,
        "z_score": round(z, 4),
        "method": method,
        "alternative": alternative,
        "p_value": _round_p(p_value),
        "p_value_z_test": _round_p(p_z),
        "confidence_level": confidence,
        "confidence_interval_diff": [_r(x, 5) for x in ci],
        "confidence_interval_diff_two_sided": [round(x, 5) for x in ci2],
        "confidence_interval_sided": {"two-sided": "two-sided", "greater": "lower-bound",
                                      "less": "upper-bound"}[alternative],
        "confidence_interval_diff_method": "newcombe-hybrid-score",
        "confidence_interval_diff_wald": [round(wald_ci[0], 5), round(wald_ci[1], 5)],
        "confidence_interval_relative_lift_pct":
            [_r(x * 100 if x is not None else None, 2) for x in rel_ci] if rel_ci else None,
        "confidence_interval_relative_lift_pct_two_sided":
            [round(rel2[0] * 100, 2), round(rel2[1] * 100, 2)] if rel2 else None,
        "ci_agrees_with_p": ci_agrees,
        "is_significant": is_significant,
        "decision": _decision_text(code),
        "decision_code": code,
        "normal_approx_valid": normal_approx_valid,
        "min_expected_count": round(min(expected_counts), 2),
        "low_sample_warning": low_sample_warning,
        "mde_at_current_n_pct": mde_pct,
        "mde_at_current_n_abs": round(mde_abs, 5) if mde_abs is not None else None,
        "observed_power": round(observed_power, 4) if observed_power is not None else None,
        "observed_power_note": _observed_power_note(),
        "planned_n_per_arm": planned_n,
        "peeking_risk": peeking_risk,
        "warnings": warnings,
        "note": warnings[0] if warnings else None,
    }
    if ni is not None:
        out["non_inferiority"] = ni
    return out


def significance_multi(control_visitors, control_conversions, variants, confidence=0.95,
                       alternative="two-sided", planned_n=None, ni_margin=None,
                       guardrail_direction="must_not_decrease"):
    """A/B/n: her varyant kontrolle kıyaslanır, p-değerleri Holm ile düzeltilir.
    variants: [(ziyaretçi, dönüşüm), ...]"""
    if not variants:
        raise ValueError(_t("en az bir varyant gerekli", "at least one variant is required"))
    names = [chr(ord("B") + i) if i < 25 else f"V{i + 1}" for i in range(len(variants))]
    comps = [significance(control_visitors, control_conversions, v, c, confidence, alternative, planned_n,
                          ni_margin=ni_margin, guardrail_direction=guardrail_direction)
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
            code = "interim_no_decision"
        else:
            code = "significant" if r["is_significant"] else "not_significant"
        r["decision"], r["decision_code"] = _decision_text(code), code
        out.append(r)
    notes = [_t(
        f"{len(variants)} varyant kontrolle kıyaslandı; çoklu karşılaştırma için Holm düzeltmesi "
        "uygulandı. Karar 'p_value_adjusted' (Holm düzeltilmiş) üzerindendir; 'p_value' ve 'p_value_raw' "
        "düzeltilmemiş ham değerlerdir.",
        f"{len(variants)} variants were compared with control; a Holm correction was applied for multiple "
        "comparisons. The decision uses 'p_value_adjusted' (Holm-adjusted); 'p_value' and 'p_value_raw' are "
        "the raw, unadjusted values."),
        _t("Güven aralıkları düzeltilmemiştir (karşılaştırma başına); Holm ile tutarlı eşzamanlı aralık değildir. "
           "Bir aralığın 0'ı dışlaması tek başına Holm-anlamlı demek değildir.",
           "Confidence intervals are unadjusted (per comparison) and are not simultaneous Holm-consistent "
           "intervals. An interval excluding 0 does not by itself mean Holm-significant.")]
    if ni_margin is not None:
        notes.append(_t("Guardrail (non-inferiority) p-değerleri çoklu karşılaştırma için düzeltilmemiştir.",
                        "Guardrail (non-inferiority) p-values are not adjusted for multiple comparisons."))
    return {
        "control_visitors": control_visitors,
        "control_conversions": control_conversions,
        "control_rate": round(control_conversions / control_visitors, 5),
        "n_comparisons": len(variants),
        "correction": "holm",
        "decision_basis": "p_value_adjusted",
        "p_value_fields": {"p_value": "raw", "p_value_raw": "raw", "p_value_adjusted": "holm"},
        "ci_adjustment": "none",
        "confidence_level": confidence,
        "alternative": alternative,
        "comparisons": out,
        "any_significant": any(r["is_significant"] for r in out),
        "peeking_risk": any(r["peeking_risk"] for r in out),
        "note": " ".join(notes),
    }


# ---------------------------------------------------------------------------
# SRM
# ---------------------------------------------------------------------------

def srm_multi(visitors, expected_ratios=None):
    """k kollu SRM: Pearson ki-kare uyum testi (k-1 serbestlik derecesi)."""
    if len(visitors) < 2:
        raise ValueError(_t("SRM için en az 2 kol gerekli", "SRM needs at least 2 arms"))
    if any(v < 0 for v in visitors):
        raise ValueError(_t("ziyaretçi sayıları negatif olamaz", "visitor counts cannot be negative"))
    total = sum(visitors)
    if total == 0:
        raise ValueError(_t("toplam ziyaretçi sayısı sıfır olamaz", "total visitors cannot be zero"))
    if expected_ratios is None:
        expected_ratios = [1.0] * len(visitors)
    if len(expected_ratios) != len(visitors):
        raise ValueError(_t(f"beklenen oran sayısı ({len(expected_ratios)}) kol sayısına ({len(visitors)}) eşit olmalı",
                            f"number of expected ratios ({len(expected_ratios)}) must equal the number of arms ({len(visitors)})"))
    if any(r <= 0 for r in expected_ratios):
        raise ValueError(_t("beklenen oranlar pozitif olmalı", "expected ratios must be positive"))
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
        note = _t(
            f"Uyarı: beklenen hücre sayılarından en az biri 5'in altında "
            f"(en küçüğü {min(expected):.1f}) — bu örneklemde ki-kare "
            "yaklaşımı zayıf, sonucu ihtiyatla okuyun; daha fazla veri toplayın.",
            f"Warning: at least one expected cell count is below 5 (smallest {min(expected):.1f}) — the "
            "chi-square approximation is weak at this sample; read with caution and collect more data.")
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
        raise ValueError(_t(f"beklenen bölüşüm 0 ile 1 arasında olmalı (verilen: {expected_split})",
                            f"expected split must be between 0 and 1 (given: {expected_split})"))
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
# Örneklem büyüklüğü ve süre
# ---------------------------------------------------------------------------

def _check_plan_inputs(confidence, power, alternative, ratio, arms, daily_visitors, weeks):
    _check_confidence(confidence)
    if not 0 < power < 1:
        raise ValueError(_t(f"güç (power) 0 ile 1 arasında olmalı (verilen: {power})",
                            f"power must be between 0 and 1 (given: {power})"))
    _check_alternative(alternative)
    if ratio <= 0:
        raise ValueError(_t(f"ratio pozitif olmalı (verilen: {ratio})", f"ratio must be positive (given: {ratio})"))
    if arms < 2:
        raise ValueError(_t(f"kol sayısı en az 2 olmalı (verilen: {arms})", f"arms must be at least 2 (given: {arms})"))
    if daily_visitors is not None and daily_visitors <= 0:
        raise ValueError(_t(f"günlük ziyaretçi pozitif olmalı (verilen: {daily_visitors})",
                            f"daily visitors must be positive (given: {daily_visitors})"))
    if weeks is not None:
        if weeks <= 0:
            raise ValueError(_t(f"hafta sayısı pozitif olmalı (verilen: {weeks})",
                                f"weeks must be positive (given: {weeks})"))
        if daily_visitors is None:
            raise ValueError(_t("--weeks için --daily-visitors da gerekli",
                                "--weeks also needs --daily-visitors"))


def _prepare_mde(mde, notes):
    mde, conv = _normalize_relative(mde, "--mde")
    if conv:
        notes.append(conv)
    if mde == 0:
        raise ValueError(_t(f"MDE sıfır olamaz (verilen: {mde})", f"MDE cannot be zero (given: {mde})"))
    if mde < 0:
        notes.append(_t(f"Negatif MDE ({mde}) mutlak değeriyle ({abs(mde)}) kullanıldı; örneklem hesabı "
                        "artış yönünde hedef oranla yapıldı.",
                        f"Negative MDE ({mde}) was used as its absolute value ({abs(mde)}); the sample size was "
                        "computed for an increase."))
        mde = abs(mde)
    return mde


def _duration(total_n, daily_visitors, notes):
    """Süre: toplam örneklem / günlük toplam uygun ziyaretçi; tam haftaya yukarı yuvarlanır, en az 14 gün."""
    raw = math.ceil(total_n / daily_visitors - 1e-9)
    days = max(14, math.ceil(raw / 7) * 7)
    if raw < 14:
        notes.append(_t(f"Örneklem {raw} günde dolar ama süre 14 günlük tabana çıkarıldı (iki tam hafta kuralı).",
                        f"The sample fills in {raw} days, but the duration was raised to the 14-day floor "
                        "(two-full-weeks rule)."))
    elif days != raw:
        notes.append(_t(f"Süre {raw} günden tam haftaya ({days} gün) yuvarlandı; haftanın her günü eşit temsil edilsin.",
                        f"Duration was rounded up from {raw} days to whole weeks ({days} days) so every weekday "
                        "is equally represented."))
    return {"daily_visitors": daily_visitors, "duration_days_raw": raw,
            "duration_days": days, "duration_weeks": days // 7}


def _short_weeks_note(weeks, notes):
    if weeks < 2:
        notes.append(_t("2 haftadan kısa bir test süresi önerilmez (dış geçerlilik: haftalık döngü temsil edilmez).",
                        "A test shorter than 2 weeks is not recommended (external validity: the weekly cycle "
                        "isn't represented)."))


def _bisect_mde(n_needed, n_available, hi):
    """n_needed(mde) azalan; n_needed(mde) <= n_available sağlayan en küçük mde. Yoksa None."""
    lo = 1e-9
    if n_needed(hi) > n_available:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        if n_needed(mid) > n_available:
            lo = mid
        else:
            hi = mid
    return hi


def sample_size(baseline_rate, mde=None, confidence=0.95, power=0.80, alternative="two-sided",
                ratio=1.0, arms=2, daily_visitors=None, weeks=None):
    """Oran metriği için örneklem planı.
    mde: göreli minimum tespit edilebilir fark (ör. 0.20 = %20 lift); 1'den büyükse yüzde sayılır (10 → 0.10).
    ratio: varyant/kontrol örneklem oranı (n_varyant = ratio * n_kontrol).
    arms: toplam kol sayısı (kontrol dahil); alfa n-1 karşılaştırmaya Bonferroni ile bölünür.
    daily_visitors: tüm kollar toplamı günlük uygun ziyaretçi → süre (tam hafta, en az 14 gün).
    weeks (+ daily_visitors): ters yön — bu sürede saptanabilir en küçük göreli fark."""
    if not 0 < baseline_rate < 1:
        raise ValueError(_t(f"baz dönüşüm oranı 0 ile 1 arasında olmalı (verilen: {baseline_rate})",
                            f"baseline conversion rate must be between 0 and 1 (given: {baseline_rate})"))
    _check_plan_inputs(confidence, power, alternative, ratio, arms, daily_visitors, weeks)
    if mde is None and weeks is None:
        raise ValueError(_t("--mde verin (veya ters hesap için --weeks ve --daily-visitors)",
                            "give --mde (or --weeks and --daily-visitors for the inverse calculation)"))

    notes = []
    p1 = baseline_rate
    comparisons = arms - 1
    alpha = (1 - confidence) / comparisons
    z_alpha = _z_alpha(alpha, alternative)
    z_beta = norm_ppf(power)
    k = ratio

    def n_control_for(p2):
        p_bar = (p1 + k * p2) / (1 + k)
        numerator = (z_alpha * math.sqrt(p_bar * (1 - p_bar) * (1 + 1 / k)) +
                     z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2) / k)) ** 2
        return numerator / (p2 - p1) ** 2

    out = {
        "metric": "proportion",
        "baseline_rate": baseline_rate,
        "confidence_level": confidence,
        "power": power,
        "alternative": alternative,
        "ratio": ratio,
        "arms": arms,
        "alpha_per_comparison": round(alpha, 6),
    }

    if mde is not None:
        mde = _prepare_mde(mde, notes)
        p2 = p1 * (1 + mde)
        if p2 >= 1:
            raise ValueError(_t(f"hedef oran %100'ü aşıyor ({p2:.3f}); baz oran veya MDE'yi küçültün",
                                f"target rate exceeds 100% ({p2:.3f}); reduce the baseline rate or the MDE"))
        n_control = math.ceil(n_control_for(p2) - 1e-9)
        n_variant = math.ceil(n_control * k - 1e-9)
        total = n_control + comparisons * n_variant

        # Nadir-olay koruması: beklenen dönüşüm/dönüşmeme sayılarından biri 10'un altındaysa
        # plan normal yaklaşımın geçerli olmadığı bölgededir (tipik sebep: aşırı büyük MDE).
        expected = [n_control * p1, n_control * (1 - p1), n_variant * p2, n_variant * (1 - p2)]
        approx_valid = min(expected) >= 10
        if not approx_valid:
            notes.insert(0, _t(
                "Uyarı: bu örneklem boyutunda beklenen dönüşüm/dönüşmeme sayılarından en az biri "
                f"10'un altında (en küçüğü {min(expected):.1f}) — hesap normal yaklaşımın geçerli "
                "olmadığı bölgede. Genelde sebep aşırı büyük bir MDE'dir; bu sayıyı test planı "
                "olarak kullanmayın, MDE'yi gerçekçi bir değere indirin.",
                "Warning: at this sample size at least one expected conversion/non-conversion count is below "
                f"10 (smallest {min(expected):.1f}) — the calculation is outside the range where the normal "
                "approximation holds. The usual cause is an unrealistically large MDE; don't use this number as "
                "a test plan, lower the MDE to a realistic value."))
        out.update({
            "target_rate": round(p2, 5),
            "mde_relative_pct": round(mde * 100, 2),
            "required_n_control": n_control,
            "required_n_variant": n_variant,
            "required_n_per_variant": n_control if ratio == 1 else n_variant,
            "required_n_total": total,
            "normal_approx_valid": approx_valid,
        })
        if daily_visitors is not None:
            out.update(_duration(total, daily_visitors, notes))

    if weeks is not None:
        _short_weeks_note(weeks, notes)
        total_avail = weeks * 7 * daily_visitors
        n_c_avail = total_avail / (1 + comparisons * k)
        hi = (1 - 1e-9) / p1 - 1
        found = _bisect_mde(lambda m: n_control_for(p1 * (1 + m)), n_c_avail, hi)
        out.update({
            "weeks": weeks,
            "daily_visitors": daily_visitors,
            "available_n_total": total_avail,
            "available_n_control": math.floor(n_c_avail),
            "available_n_variant": math.floor(n_c_avail * k),
            "mde_detectable_relative_pct": round(found * 100, 2) if found is not None else None,
            "mde_detectable_target_rate": round(p1 * (1 + found), 5) if found is not None else None,
        })
        if found is None:
            notes.append(_t("Bu trafik ve sürede hiçbir gerçekçi fark saptanamaz; süreyi uzatın veya trafiği artırın.",
                            "No realistic effect is detectable with this traffic and duration; run longer or add traffic."))

    if arms > 2:
        notes.append(_t(f"{arms} kol: alfa {comparisons} karşılaştırmaya Bonferroni ile bölündü "
                        f"(karşılaştırma başına alfa {alpha:.4f}).",
                        f"{arms} arms: alpha was split across {comparisons} comparisons with Bonferroni "
                        f"(alpha per comparison {alpha:.4f})."))
    out["note"] = " ".join(notes) if notes else None
    return out


def sample_size_mean(baseline_mean, baseline_sd, mde=None, confidence=0.95, power=0.80,
                     alternative="two-sided", ratio=1.0, arms=2, daily_visitors=None, weeks=None):
    """Sürekli metrik (ortalama) için örneklem planı — iki örneklem normal yaklaşımı, iki kolda eşit sd:
    n_kontrol = (z_α + z_β)² · sd² · (1 + 1/ratio) / δ², δ = |ortalama| · mde."""
    if baseline_mean == 0:
        raise ValueError(_t("baz ortalama sıfır olamaz (göreli MDE tanımsız)",
                            "baseline mean cannot be zero (a relative MDE is undefined)"))
    if baseline_sd <= 0:
        raise ValueError(_t(f"baz standart sapma pozitif olmalı (verilen: {baseline_sd})",
                            f"baseline standard deviation must be positive (given: {baseline_sd})"))
    _check_plan_inputs(confidence, power, alternative, ratio, arms, daily_visitors, weeks)
    if mde is None and weeks is None:
        raise ValueError(_t("--mde verin (veya ters hesap için --weeks ve --daily-visitors)",
                            "give --mde (or --weeks and --daily-visitors for the inverse calculation)"))
    notes = []
    comparisons = arms - 1
    alpha = (1 - confidence) / comparisons
    zsum = _z_alpha(alpha, alternative) + norm_ppf(power)
    k = ratio
    m_abs = abs(baseline_mean)
    out = {
        "metric": "mean",
        "baseline_mean": baseline_mean,
        "baseline_sd": baseline_sd,
        "confidence_level": confidence,
        "power": power,
        "alternative": alternative,
        "ratio": ratio,
        "arms": arms,
        "alpha_per_comparison": round(alpha, 6),
    }
    if mde is not None:
        mde = _prepare_mde(mde, notes)
        delta = m_abs * mde
        n_control = math.ceil(zsum ** 2 * baseline_sd ** 2 * (1 + 1 / k) / delta ** 2 - 1e-9)
        n_variant = math.ceil(n_control * k - 1e-9)
        total = n_control + comparisons * n_variant
        out.update({
            "target_mean": round(baseline_mean + math.copysign(delta, baseline_mean), 6),
            "mde_relative_pct": round(mde * 100, 2),
            "mde_absolute": round(delta, 6),
            "required_n_control": n_control,
            "required_n_variant": n_variant,
            "required_n_per_variant": n_control if ratio == 1 else n_variant,
            "required_n_total": total,
        })
        if min(n_control, n_variant) < 30:
            notes.append(_t("Kol başına 30'dan az gözlem: normal yaklaşım zayıf, gerçek ihtiyaç daha yüksek olabilir.",
                            "Fewer than 30 observations per arm: the normal approximation is weak; the real "
                            "requirement may be higher."))
        if daily_visitors is not None:
            out.update(_duration(total, daily_visitors, notes))
    if weeks is not None:
        _short_weeks_note(weeks, notes)
        total_avail = weeks * 7 * daily_visitors
        n_c_avail = total_avail / (1 + comparisons * k)
        delta = zsum * baseline_sd * math.sqrt((1 + 1 / k) / n_c_avail)
        out.update({
            "weeks": weeks,
            "daily_visitors": daily_visitors,
            "available_n_total": total_avail,
            "available_n_control": math.floor(n_c_avail),
            "available_n_variant": math.floor(n_c_avail * k),
            "mde_detectable_relative_pct": round(delta / m_abs * 100, 2),
            "mde_detectable_absolute": round(delta, 6),
        })
    notes.append(_t("Normal yaklaşım, iki kolda eşit sd varsayar. Çarpık gelir verisinde sd'yi, analizde "
                    "uygulayacağınız winsorize ile aynı şekilde kırpılmış geçmiş veriden hesaplayın.",
                    "Normal approximation, equal SD in both arms. For skewed revenue data, compute the SD from "
                    "historical data capped the same way you will winsorize in the analysis."))
    if arms > 2:
        notes.append(_t(f"{arms} kol: alfa {comparisons} karşılaştırmaya Bonferroni ile bölündü "
                        f"(karşılaştırma başına alfa {alpha:.4f}).",
                        f"{arms} arms: alpha was split across {comparisons} comparisons with Bonferroni "
                        f"(alpha per comparison {alpha:.4f})."))
    out["note"] = " ".join(notes)
    return out


# ---------------------------------------------------------------------------
# Sürekli metrikler: CSV okuma
# ---------------------------------------------------------------------------

def _is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    return True


def _resolve_column(spec, header, ncols, path, flag):
    """spec: sütun adı (başlıktan) veya 0'dan başlayan sıra numarası → sütun indeksi."""
    s = str(spec).strip()
    if header is not None:
        if s in header:
            return header.index(s)
        lower = [h.lower() for h in header]
        if s.lower() in lower:
            return lower.index(s.lower())
    if re.fullmatch(r"\d+", s):
        idx = int(s)
        if idx >= ncols:
            raise ValueError(_t(f"{path}: {flag} {idx} sütunu yok (dosyada {ncols} sütun var; sıra 0'dan başlar)",
                                f"{path}: {flag} {idx} doesn't exist (the file has {ncols} columns; index starts at 0)"))
        return idx
    avail = ", ".join(header) if header else _t(f"başlık yok, {ncols} sütun", f"no header, {ncols} columns")
    raise ValueError(_t(f"{path}: {flag} {s!r} sütunu bulunamadı (mevcut: {avail})",
                        f"{path}: {flag} column {s!r} not found (available: {avail})"))


def read_csv_table(path, value_column=None, id_column=None, value_flag="--value-column", inherited=False):
    """Kullanıcı başına CSV okur. Tek sütunlu dosyada --value-column gerekmez. Birden çok sütun varsa
    ve değer sütunu verilmediyse HATA verir: ilk sütunu sessizce okumak user_id gibi bir kimlik
    sütununu metrik sanıp sahte bir anlamlı sonuç üretir. Başlık satırı otomatik algılanır
    (ilk satırdaki tüm dolu hücreler sayı değilse başlıktır).
    inherited=True: sütun belirtimi başka bir dosyadan devralındı; tek sütunlu dosyada yok sayılır."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        raw = list(csv.reader(f))
    rows = [(i + 1, [c.strip() for c in r]) for i, r in enumerate(raw) if any(c.strip() for c in r)]
    if not rows:
        raise ValueError(_t(f"{path}: hiç sayısal değer yok", f"{path}: no numeric values"))
    first = list(rows[0][1])
    while len(first) > 1 and first[-1] == "":
        first.pop()
    ncols = len(first)
    has_header = all(not _is_number(c) for c in first if c)
    header = first if has_header else None
    data = rows[1:] if has_header else rows
    if inherited and ncols == 1 and id_column is None:
        value_column = None

    if value_column is None:
        if ncols > 1:
            cols = ", ".join(f"{i}={h}" for i, h in enumerate(header)) if header else str(ncols)
            raise ValueError(_t(
                f"{path}: {ncols} sütun var ({cols}); hangisinin metrik olduğunu {value_flag} AD|SIRA ile "
                "belirtin. İlk sütun sessizce okunmaz: kimlik sütunu metrik sanılırsa sahte bir anlamlı sonuç "
                "çıkar. Ondalık ayırıcı virgülse dosyayı nokta ondalıkla dışa aktarın.",
                f"{path}: the file has {ncols} columns ({cols}); say which one is the metric with {value_flag} "
                "NAME|INDEX. The first column is never read silently: an id column mistaken for the metric "
                "produces a fake significant result. If the decimal separator is a comma, export with a dot."))
        vi = 0
    else:
        vi = _resolve_column(value_column, header, ncols, path, value_flag)
    ii = _resolve_column(id_column, header, ncols, path, "--id-column") if id_column is not None else None
    if ii is not None and ii == vi:
        raise ValueError(_t(f"{path}: kimlik sütunu ile değer sütunu aynı olamaz",
                            f"{path}: the id column and the value column cannot be the same"))

    need = max(vi, ii if ii is not None else 0)
    values, ids = [], []
    for ln, r in data:
        if len(r) <= need or any(c for c in r[ncols:]):
            raise ValueError(_t(
                f"{path}: {ln}. satırın sütun sayısı ({len(r)}) başlıkla ({ncols}) uyuşmuyor; "
                "ondalık ayırıcı virgülse dosyayı nokta ondalıkla dışa aktarın",
                f"{path}: row {ln} has {len(r)} columns but the first row has {ncols}; "
                "if the decimal separator is a comma, export with a dot"))
        s = r[vi]
        if s == "":
            raise ValueError(_t(f"{path}: {ln}. satırda değer boş; eksik değerin 0 mı yoksa dışlanacak mı "
                                "olduğunu veride netleştirin",
                                f"{path}: row {ln} has an empty value; decide in the data whether a missing "
                                "value means 0 or should be excluded"))
        try:
            x = float(s)
        except ValueError:
            raise ValueError(_t(f"{path}: {ln}. satır sayı değil ({s!r})", f"{path}: row {ln} is not a number ({s!r})"))
        if not math.isfinite(x):
            raise ValueError(_t(f"{path}: {ln}. satırda sonlu olmayan değer ({s!r})",
                                f"{path}: row {ln} has a non-finite value ({s!r})"))
        values.append(x)
        if ii is not None:
            if r[ii] == "":
                raise ValueError(_t(f"{path}: {ln}. satırda kimlik boş", f"{path}: row {ln} has an empty id"))
            ids.append(r[ii])
    if not values:
        raise ValueError(_t(f"{path}: hiç sayısal değer yok", f"{path}: no numeric values"))
    if ii is not None:
        dups = [u for u, c in Counter(ids).items() if c > 1]
        if dups:
            raise ValueError(_t(
                f"{path}: {len(dups)} kimlik birden fazla satırda (ör. {dups[:3]}); dosya kullanıcı başına bir "
                "satır olmalı (sipariş başına satırlar önce kullanıcıya toplanmalı)",
                f"{path}: {len(dups)} ids appear on more than one row (e.g. {dups[:3]}); the file must have one "
                "row per user (aggregate per-order rows to users first)"))
    return {
        "values": values,
        "ids": ids if ii is not None else None,
        "has_header": has_header,
        "n_columns": ncols,
        "value_column": header[vi] if header else vi,
        "id_column": (header[ii] if header else ii) if ii is not None else None,
    }


def read_values_csv(path, value_column=None):
    """Geriye uyumlu yardımcı: tek sütunlu (veya --value-column verilmiş) dosyanın değerleri."""
    return read_csv_table(path, value_column)["values"]


def align_pre_by_id(ids, pre_ids, pre_values, arm):
    """Ön-dönem değerlerini metrik dosyasının kullanıcı sırasına kimlikle hizalar.
    Döner: (hizalanmış ön-dönem listesi, metrik dosyasında olmayan ön-dönem satırı sayısı)."""
    lookup = dict(zip(pre_ids, pre_values))
    missing = [u for u in ids if u not in lookup]
    if missing:
        raise ValueError(_t(
            f"CUPED ({arm}): {len(missing)} kullanıcının ön-dönem değeri yok (ör. {missing[:3]}); ön-dönemde "
            "etkinliği olmayan kullanıcılar için açıkça 0 (veya uygun değer) içeren satır ekleyin",
            f"CUPED ({arm}): {len(missing)} users have no pre-period value (e.g. {missing[:3]}); add explicit "
            "rows with 0 (or the appropriate value) for users with no pre-period activity"))
    id_set = set(ids)
    extra = sum(1 for u in pre_ids if u not in id_set)
    return [lookup[u] for u in ids], extra


def load_continuous_inputs(control_csv, variant_csv, control_pre_csv=None, variant_pre_csv=None,
                           value_column=None, pre_value_column=None, id_column=None):
    """CSV'leri okuyup continuous() için anahtar sözcükleri ve girdi bilgisini döndürür."""
    c = read_csv_table(control_csv, value_column, id_column)
    v = read_csv_table(variant_csv, value_column, id_column)
    kw = {"control": c["values"], "variant": v["values"]}
    notes = []
    info = {"value_column": c["value_column"], "id_column": c["id_column"]}
    if id_column is not None:
        overlap = set(c["ids"]) & set(v["ids"])
        if overlap:
            notes.append(_t(
                f"{len(overlap)} kullanıcı kimliği iki kolda da var: atama sızıntısı (aynı kullanıcı iki deneyimi "
                "gördü). Atamayı ve SRM'yi kontrol edin.",
                f"{len(overlap)} user ids appear in both arms: assignment leakage (the same user saw both "
                "experiences). Check assignment and SRM."))
    if control_pre_csv or variant_pre_csv:
        if not (control_pre_csv and variant_pre_csv):
            raise ValueError(_t("CUPED için hem kontrol hem varyant ön-dönem CSV'si gerekli",
                                "CUPED needs both control and variant pre-period CSVs"))
        spec = pre_value_column if pre_value_column is not None else value_column
        flag = "--pre-value-column" if pre_value_column is not None else _t(
            "--value-column (ön-dönem dosyasında farklıysa --pre-value-column verin)",
            "--value-column (pass --pre-value-column if the pre-period file differs)")
        # Tek sütunlu ön-dönem dosyasında metrikten devralınan sütun adı aranmaz (inherited).
        cp, vp = (read_csv_table(path, spec, id_column, flag, inherited=pre_value_column is None)
                  for path in (control_pre_csv, variant_pre_csv))
        info["pre_value_column"] = cp["value_column"]
        if id_column is not None:
            kw["control_pre"], ec = align_pre_by_id(c["ids"], cp["ids"], cp["values"], _t("kontrol", "control"))
            kw["variant_pre"], ev = align_pre_by_id(v["ids"], vp["ids"], vp["values"], _t("varyant", "variant"))
            kw["cuped_join"] = "id"
            if ec + ev:
                notes.append(_t(f"{ec + ev} ön-dönem satırı metrik dosyalarında olmayan kullanıcılara ait; yok sayıldı.",
                                f"{ec + ev} pre-period rows belong to users not in the metric files; ignored."))
        else:
            kw["control_pre"], kw["variant_pre"] = cp["values"], vp["values"]
            kw["cuped_join"] = "row-order"
    kw["extra_notes"] = notes
    return kw, info


# ---------------------------------------------------------------------------
# Sürekli metrikler: testler
# ---------------------------------------------------------------------------

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
    """Welch t-testi (varyant - kontrol). v = örneklem varyansı.
    'ci_diff' hipotez yönüne uyar (tek yönlüde tek sınır); 'ci_diff_two_sided' her zaman iki yönlü."""
    _check_alternative(alternative)
    se2 = v1 / n1 + v2 / n2
    diff = m2 - m1
    if se2 <= 0:
        return {"t": 0.0, "df": None, "p_value": 1.0, "diff": diff, "se": 0.0,
                "ci_diff": _sided(diff, diff, alternative), "ci_diff_two_sided": [diff, diff]}
    se = math.sqrt(se2)
    num = se2 ** 2
    den = ((v1 / n1) ** 2 / (n1 - 1) if v1 > 0 else 0.0) + ((v2 / n2) ** 2 / (n2 - 1) if v2 > 0 else 0.0)
    df = num / den
    t = diff / se
    p = _t_p(t, df, alternative)
    alpha = 1 - confidence
    tc2 = t_ppf(1 - alpha / 2, df)
    two = [diff - tc2 * se, diff + tc2 * se]
    if alternative == "two-sided":
        ci = two
    else:
        tc1 = t_ppf(1 - alpha, df)
        ci = _sided(diff - tc1 * se, diff + tc1 * se, alternative)
    return {"t": t, "df": df, "p_value": p, "diff": diff, "se": se, "ci_diff": ci, "ci_diff_two_sided": two}


def _rel_ci_means(m1, v1, n1, m2, v2, n2, confidence, alternative="two-sided"):
    """Ortalamalar oranı için delta yöntemi (log ölçekte). Ortalamalardan biri <= 0 ise None.
    Döner: (yöne uyan aralık, iki yönlü aralık) yüzde olarak."""
    if m1 <= 0 or m2 <= 0:
        return None, None
    se = math.sqrt(v1 / (n1 * m1 * m1) + v2 / (n2 * m2 * m2))
    lr = math.log(m2 / m1)

    def at(level):
        z = norm_ppf(1 - (1 - level) / 2)
        return (math.exp(lr - z * se) - 1) * 100, (math.exp(lr + z * se) - 1) * 100

    two = [round(x, 2) for x in at(confidence)]
    if alternative == "two-sided":
        return two, two
    return [_r(x, 2) for x in _sided(*at(2 * confidence - 1), alternative)], two


def continuous(control=None, variant=None, control_stats=None, variant_stats=None,
               confidence=0.95, alternative="two-sided", winsorize=None, bootstrap=0, seed=DEFAULT_SEED,
               control_pre=None, variant_pre=None, cuped_join=None, ni_margin=None,
               guardrail_direction="must_not_decrease", extra_notes=None):
    """Sürekli metrik karşılaştırması (ör. ziyaretçi başına gelir; sıfırlar dahil).
    control/variant: kullanıcı başına değer listesi; ya da *_stats = (n, mean, sd).
    cuped_join: 'id' (kimlikle hizalandı) veya 'row-order' (satır sırasıyla; varsayılan, uyarı notu eklenir)."""
    _check_confidence(confidence)
    _check_alternative(alternative, confidence)
    raw_mode = control is not None and variant is not None
    if not raw_mode and (control_stats is None or variant_stats is None):
        raise ValueError(_t("ya iki CSV (kullanıcı başına değer) ya da iki kol için n/ortalama/sd verin",
                            "give either two CSVs (one value per user) or n/mean/sd for both arms"))
    notes = []
    result = {"input": "raw" if raw_mode else "summary", "alternative": alternative,
              "confidence_level": confidence}

    if raw_mode:
        if len(control) < 2 or len(variant) < 2:
            raise ValueError(_t("her kolda en az 2 gözlem gerekli", "each arm needs at least 2 observations"))
        if winsorize is not None:
            if not 0.5 < winsorize < 1:
                raise ValueError(_t(f"winsorize yüzdeliği 0.5 ile 1 arasında olmalı (verilen: {winsorize})",
                                    f"winsorize percentile must be between 0.5 and 1 (given: {winsorize})"))
            cap = _quantile(sorted(control + variant), winsorize)
            n_capped = sum(1 for x in control + variant if x > cap)
            control = [min(x, cap) for x in control]
            variant = [min(x, cap) for x in variant]
            result["winsorize"] = {"percentile": winsorize, "cap": round(cap, 4), "n_capped": n_capped}
            notes.append(_t(f"Üst kuyruk iki kolun birleşik %{winsorize * 100:g} yüzdeliğinde ({cap:.4g}) "
                            f"kırpıldı ({n_capped} gözlem).",
                            f"The upper tail was capped at the pooled {winsorize * 100:g}th percentile ({cap:.4g}) "
                            f"of both arms ({n_capped} observations)."))
        m1, v1 = _mean_var(control)
        m2, v2 = _mean_var(variant)
        n1, n2 = len(control), len(variant)
    else:
        (n1, m1, s1), (n2, m2, s2) = control_stats, variant_stats
        for ad, n, s in (("kontrol", n1, s1), ("varyant", n2, s2)):
            ad = _arm_name(ad)
            if n < 2:
                raise ValueError(_t(f"{ad} örneklemi en az 2 olmalı (verilen: {n})",
                                    f"{ad} sample must be at least 2 (given: {n})"))
            if s < 0:
                raise ValueError(_t(f"{ad} standart sapması negatif olamaz (verilen: {s})",
                                    f"{ad} standard deviation cannot be negative (given: {s})"))
        v1, v2 = s1 * s1, s2 * s2
        if winsorize is not None or bootstrap or control_pre is not None:
            notes.append(_t("Özet istatistik girdisinde winsorize, bootstrap ve CUPED uygulanamaz; "
                            "kullanıcı başına CSV verin.",
                            "Winsorize, bootstrap and CUPED can't be applied to summary statistics; "
                            "give per-user CSVs."))

    w = welch_test(m1, v1, n1, m2, v2, n2, confidence, alternative)
    alpha = 1 - confidence
    rel_ci, rel_ci2 = _rel_ci_means(m1, v1, n1, m2, v2, n2, confidence, alternative)
    result.update({
        "control": {"n": n1, "mean": round(m1, 6), "sd": round(math.sqrt(v1), 6)},
        "variant": {"n": n2, "mean": round(m2, 6), "sd": round(math.sqrt(v2), 6)},
        "method": "welch-t-test",
        "absolute_diff": round(w["diff"], 6),
        "relative_lift_pct": round(w["diff"] / m1 * 100, 2) if m1 != 0 else None,
        "t_stat": round(w["t"], 4),
        "df": round(w["df"], 2) if w["df"] is not None else None,
        "p_value": _round_p(w["p_value"]),
        "confidence_interval_diff": [_r(x, 6) for x in w["ci_diff"]],
        "confidence_interval_diff_two_sided": [round(x, 6) for x in w["ci_diff_two_sided"]],
        "confidence_interval_sided": {"two-sided": "two-sided", "greater": "lower-bound",
                                      "less": "upper-bound"}[alternative],
        "confidence_interval_relative_lift_pct": rel_ci,
        "confidence_interval_relative_lift_pct_two_sided": rel_ci2,
        "is_significant": w["p_value"] < alpha,
    })

    if ni_margin is not None:
        ni = non_inferiority_means(m1, v1, n1, m2, v2, n2, ni_margin, guardrail_direction, confidence)
        result["non_inferiority"] = ni
        if _ni_warning(ni):
            notes.append(_ni_warning(ni))

    if raw_mode and bootstrap:
        if bootstrap < 100:
            raise ValueError(_t(f"bootstrap en az 100 tekrar olmalı (verilen: {bootstrap})",
                                f"bootstrap needs at least 100 resamples (given: {bootstrap})"))
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
        q_lo = alpha if alternative != "two-sided" else alpha / 2
        two = [round(_quantile(diffs, alpha / 2), 6), round(_quantile(diffs, 1 - alpha / 2), 6)]
        one = _sided(round(_quantile(diffs, q_lo), 6), round(_quantile(diffs, 1 - q_lo), 6), alternative)
        rel_ok = len(rels) >= 100
        result["bootstrap"] = {
            "resamples": bootstrap,
            "seed": seed,
            "ci_diff": one,
            "ci_diff_two_sided": two,
            "ci_relative_lift_pct": _sided(round(_quantile(rels, q_lo) * 100, 2),
                                           round(_quantile(rels, 1 - q_lo) * 100, 2), alternative) if rel_ok else None,
            "method": "percentile",
        }

    if control_pre is not None or variant_pre is not None:
        if not raw_mode:
            pass
        elif control_pre is None or variant_pre is None:
            raise ValueError(_t("CUPED için hem kontrol hem varyant ön-dönem CSV'si gerekli",
                                "CUPED needs both control and variant pre-period CSVs"))
        else:
            if len(control_pre) != n1 or len(variant_pre) != n2:
                raise ValueError(_t(
                    "ön-dönem CSV'leri metrik CSV'leriyle aynı satır sayısında olmalı "
                    f"(kontrol {len(control_pre)} vs {n1}, varyant {len(variant_pre)} vs {n2})",
                    "pre-period CSVs must have the same number of rows as the metric CSVs "
                    f"(control {len(control_pre)} vs {n1}, variant {len(variant_pre)} vs {n2})"))
            join = cuped_join or "row-order"
            ys = control + variant
            xs = control_pre + variant_pre
            my, vy = _mean_var(ys)
            mx, vx = _mean_var(xs)
            if vx == 0:
                raise ValueError(_t("ön-dönem kovaryatının varyansı sıfır; CUPED uygulanamaz",
                                    "the pre-period covariate has zero variance; CUPED can't be applied"))
            cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)
            theta = cov / vx
            ca = [y - theta * (x - mx) for y, x in zip(control, control_pre)]
            va = [y - theta * (x - mx) for y, x in zip(variant, variant_pre)]
            cm, cv = _mean_var(ca)
            vm, vv = _mean_var(va)
            _, v_adj = _mean_var(ca + va)
            wc = welch_test(cm, cv, n1, vm, vv, n2, confidence, alternative)
            result["cuped"] = {
                "join": join,
                "theta": round(theta, 6),
                "variance_reduction_pct": round((1 - v_adj / vy) * 100, 2) if vy > 0 else None,
                "control_mean_adj": round(cm, 6),
                "variant_mean_adj": round(vm, 6),
                "absolute_diff": round(wc["diff"], 6),
                "relative_lift_pct": round(wc["diff"] / cm * 100, 2) if cm != 0 else None,
                "t_stat": round(wc["t"], 4),
                "df": round(wc["df"], 2) if wc["df"] is not None else None,
                "p_value": _round_p(wc["p_value"]),
                "confidence_interval_diff": [_r(x, 6) for x in wc["ci_diff"]],
                "confidence_interval_diff_two_sided": [round(x, 6) for x in wc["ci_diff_two_sided"]],
                "is_significant": wc["p_value"] < alpha,
            }
            notes.append(_t("CUPED: theta birleşik veriden hesaplandı; ön-dönem değeri test başlamadan "
                            "ölçülmüş olmalı, aksi halde düzeltme yanlıdır.",
                            "CUPED: theta was estimated from the pooled data; the pre-period value must be "
                            "measured before the test started, otherwise the adjustment is biased."))
            if join == "row-order":
                notes.append(_t("CUPED ön-dönem değerleri SATIR SIRASIYLA eşleştirildi: dosyalar aynı kullanıcı "
                                "sırasında değilse sonuç sessizce yanlıştır. Kullanıcı kimliği sütunu varsa "
                                "--id-column verin.",
                                "CUPED pre-period values were matched BY ROW ORDER: if the files aren't in the "
                                "same user order the result is silently wrong. If there is a user id column, "
                                "pass --id-column."))

    if min(n1, n2) < 30:
        notes.append(_t("Kol başına 30'dan az gözlem: t yaklaşımı çarpık gelir verisinde zayıf, sonucu ihtiyatla okuyun.",
                        "Fewer than 30 observations per arm: the t approximation is weak for skewed revenue data; "
                        "read with caution."))
    notes.extend(extra_notes or [])
    result["note"] = " ".join(notes) if notes else None
    return result


# ---------------------------------------------------------------------------
# Segment etkileşimi
# ---------------------------------------------------------------------------

def interaction(seg1, seg2, confidence=0.95, names=("seg1", "seg2")):
    """İki segmentte tedavi etkisinin farkı (fark-içinde-fark). seg = ((A_ziy, A_dön), (B_ziy, B_dön));
    A = kontrol, B = varyant. Mutlak ölçek: (pB−pA)₁ − (pB−pA)₂, z = DiD / sqrt(Var₁ + Var₂), varyanslar
    havuzlanmamış. Göreli ölçek: log(pB/pA)₁ − log(pB/pA)₂, Katz varyansı (1−p)/x."""
    _check_confidence(confidence)
    alpha = 1 - confidence
    zc = norm_ppf(1 - alpha / 2)
    segs = []
    for name, ((na, xa), (nb, xb)) in zip(names, (seg1, seg2)):
        _validate_arm(f"{name} A", na, xa)
        _validate_arm(f"{name} B", nb, xb)
        pa, pb = xa / na, xb / nb
        seg = {
            "name": name,
            "control_rate": round(pa, 5),
            "variant_rate": round(pb, 5),
            "absolute_diff": round(pb - pa, 5),
            "absolute_diff_pp": round((pb - pa) * 100, 3),
            "relative_lift_pct": round((pb / pa - 1) * 100, 2) if pa > 0 else None,
            "_d": pb - pa,
            "_var": pa * (1 - pa) / na + pb * (1 - pb) / nb,
            "_log": math.log(pb / pa) if xa > 0 and xb > 0 else None,
            "_lvar": (1 - pa) / xa + (1 - pb) / xb if xa > 0 and xb > 0 else None,
            "_minexp": min(xa, na - xa, xb, nb - xb),
        }
        segs.append(seg)
    s1, s2 = segs
    did = s1["_d"] - s2["_d"]
    se = math.sqrt(s1["_var"] + s2["_var"])
    z = did / se if se > 0 else 0.0
    p = _p_from_z(z, "two-sided") if se > 0 else 1.0
    absolute = {
        "diff_in_diff": round(did, 5),
        "diff_in_diff_pp": round(did * 100, 3),
        "se": round(se, 6),
        "z": round(z, 4),
        "p_value": _round_p(p),
        "confidence_interval": [round(did - zc * se, 5), round(did + zc * se, 5)],
        "is_significant": p < alpha,
    }
    relative = None
    if s1["_log"] is not None and s2["_log"] is not None:
        ld = s1["_log"] - s2["_log"]
        lse = math.sqrt(s1["_lvar"] + s2["_lvar"])
        lz = ld / lse
        lp = _p_from_z(lz, "two-sided")
        relative = {
            "ratio_of_rate_ratios": round(math.exp(ld), 5),
            "log_diff": round(ld, 6),
            "se": round(lse, 6),
            "z": round(lz, 4),
            "p_value": _round_p(lp),
            "confidence_interval_ratio": [round(math.exp(ld - zc * lse), 5), round(math.exp(ld + zc * lse), 5)],
            "is_significant": lp < alpha,
        }
    warnings = []
    if min(s1["_minexp"], s2["_minexp"]) < 10:
        warnings.append(_t("Bir segment hücresinde 10'dan az dönüşüm/dönüşmeme var; normal yaklaşım zayıf, "
                           "etkileşim sonucunu güvenilir saymayın.",
                           "A segment cell has fewer than 10 conversions/non-conversions; the normal "
                           "approximation is weak, don't rely on the interaction result."))
    if relative is not None and relative["is_significant"] != absolute["is_significant"]:
        warnings.append(_t("Mutlak ve göreli ölçek farklı sonuç veriyor: etkileşim ölçeğe bağlı. 'Etki segmentte "
                           "farklı' demeyin; iki ölçeği birlikte raporlayın.",
                           "The absolute and relative scales disagree: the interaction is scale-dependent. Don't "
                           "say 'the effect differs by segment'; report both scales together."))
    differs = absolute["is_significant"]
    code = "effect_differs" if differs else "no_evidence_of_difference"
    note = _t(
        "Yalnızca test öncesinde belirlenmiş segmentler için kullanın; sonuç görüldükten sonra seçilen segmentte "
        "bu test p-hacking'dir. Etkileşim testinin gücü düşüktür (aynı büyüklükte bir farkı saptamak ana etkiye "
        "göre kabaca 4 kat örneklem ister); 'anlamlı değil' etkinin segmentlerde aynı olduğunu kanıtlamaz.",
        "Use only for segments declared before the test; on a segment picked after seeing results this test is "
        "p-hacking. Interaction tests have low power (detecting a difference of the same size needs roughly 4x "
        "the sample of the main effect); 'not significant' doesn't prove the effect is the same across segments.")
    for s in segs:
        for k in [k for k in s if k.startswith("_")]:
            del s[k]
    return {
        "method": "difference-in-differences-z",
        "confidence_level": confidence,
        "segments": segs,
        "interaction_absolute": absolute,
        "interaction_relative": relative,
        "effect_differs": differs,
        "decision_code": code,
        "decision": _t("etki segmentler arasında farklı", "effect differs between segments") if differs else
        _t("segmentler arasında fark kanıtı yok", "no evidence the effect differs between segments"),
        "warnings": warnings,
        "note": note,
    }


# ---------------------------------------------------------------------------
# Bayes görünümü
# ---------------------------------------------------------------------------

def bayes(control_visitors, control_conversions, variant_visitors, variant_conversions,
          draws=100000, seed=DEFAULT_SEED, credible=0.95):
    """Beta(1,1) önsel + Monte Carlo. ALTERNATİF bir bakıştır; frekansçı kararın yerine geçmez.
    Varsayılan tohum sabittir (12345): aynı girdi her zaman aynı sonucu verir."""
    _validate_arm("kontrol", control_visitors, control_conversions)
    _validate_arm("varyant", variant_visitors, variant_conversions)
    if draws < 1000:
        raise ValueError(_t(f"çekiliş sayısı en az 1000 olmalı (verilen: {draws})",
                            f"draws must be at least 1000 (given: {draws})"))
    if not 0 < credible < 1:
        raise ValueError(_t(f"güvenilir aralık düzeyi 0 ile 1 arasında olmalı (verilen: {credible})",
                            f"credible level must be between 0 and 1 (given: {credible})"))
    if seed is None:
        seed = DEFAULT_SEED
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
        "note": _t("Alternatif bakış: bu Bayes özeti frekansçı 'significance' kararının yerine geçmez; "
                   "karar kuralı test öncesinde belirlenmelidir.",
                   "Alternative view: this Bayesian summary doesn't replace the frequentist 'significance' "
                   "decision; the decision rule must be set before the test."),
    }


# ---------------------------------------------------------------------------
# Gelir / kâr
# ---------------------------------------------------------------------------

def revenue(control_visitors, control_conversions, control_aov,
            variant_visitors, variant_conversions, variant_aov, margin_rate=None,
            variant_margin_rate=None):
    """Ziyaretçi başına gelir (RPV) ve — marj oranı verilirse — ziyaretçi başına brüt kâr
    karşılaştırması. Fiyat/indirim/paket testlerinde dönüşüm oranının geliri gizlemesini
    açığa çıkarır. Bu bir anlamlılık testi DEĞİLDİR: sipariş tutarı dağılımı çarpıktır,
    iki-oranlı z-testi burada geçerli değildir; sonuç yön göstergesidir."""
    for ad, v, c, aov in (("kontrol", control_visitors, control_conversions, control_aov),
                          ("varyant", variant_visitors, variant_conversions, variant_aov)):
        _validate_arm(ad, v, c)
        if aov < 0:
            raise ValueError(_t(f"{_arm_name(ad)} ortalama sipariş tutarı negatif olamaz (verilen: {aov})",
                                f"{_arm_name(ad)} average order value cannot be negative (given: {aov})"))
    for ad, mr in (("kontrol", margin_rate), ("varyant", variant_margin_rate)):
        if mr is not None and not 0 <= mr <= 1:
            raise ValueError(_t(f"{_arm_name(ad)} marj oranı 0 ile 1 arasında olmalı (verilen: {mr})",
                                f"{_arm_name(ad)} margin rate must be between 0 and 1 (given: {mr})"))
    if variant_margin_rate is not None and margin_rate is None:
        raise ValueError(_t("varyant marj oranı verildiyse kontrol marj oranı da verilmelidir",
                            "if the variant margin rate is given, the control margin rate must be given too"))
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
        "warnings": [],
        "note": _t("Bu bir anlamlılık testi değildir; sipariş tutarı dağılımı çarpık olduğu için "
                   "z-testi burada geçerli değildir. Yön göstergesi olarak okuyun ve dönüşüm oranının "
                   "anlamlılığını ayrıca 'significance' komutuyla kontrol edin. Ziyaretçi başına gelir için "
                   "istatistiksel çıkarım (Welch t, bootstrap, CUPED) gerekiyorsa kullanıcı başına veriyle "
                   "'continuous' komutunu kullanın.",
                   "This is not a significance test; order value is skewed, so a z-test isn't valid here. "
                   "Read it as a directional signal and check the conversion rate's significance separately "
                   "with 'significance'. For statistical inference on revenue per visitor (Welch t, bootstrap, "
                   "CUPED), use 'continuous' with per-user data."),
        "inference_command": "continuous",
    }

    profit_change = None
    if margin_rate is not None:
        profit_c = rpv_c * margin_rate
        profit_v = rpv_v * v_margin
        profit_change = pct_change(profit_c, profit_v) if profit_c > 0 else None
        result["variant_margin_rate"] = v_margin
        result["profit_per_visitor"] = {
            "control": round(profit_c, 4),
            "variant": round(profit_v, 4),
            "change_pct": round(profit_change, 2) if profit_change is not None else None,
        }
        if variant_margin_rate is None:
            result["profit_per_visitor"]["assumption"] = _t(
                "Varyantın brüt marj oranı kontrolünkiyle aynı varsayıldı. Fiyat, indirim veya "
                "paket değişikliği test ediliyorsa bu varsayım genelde yanlıştır: birim maliyet "
                "sabitken fiyat düşerse varyantın marjı da düşer. Gerçek oranı biliyorsanız "
                "--variant-margin-rate ile verin.",
                "The variant's gross margin rate was assumed equal to the control's. When price, discount "
                "or bundling is being tested this is usually wrong: with unit cost fixed, a lower price "
                "lowers the variant's margin too. If you know the real rate, pass --variant-margin-rate.")

    warnings = result["warnings"]
    if cr_change is not None and rpv_change is not None and cr_change > 0 and rpv_change < 0:
        warnings.append(_t(
            f"Dönüşüm oranı %{cr_change:.1f} arttı ama ziyaretçi başına gelir %{abs(rpv_change):.1f} DÜŞTÜ — "
            "bu testte kazanan kararı dönüşüm oranına göre verilirse gelir kaybedilir. "
            "Birincil metrik RPV olmalı.",
            f"Conversion rate rose {cr_change:.1f}% but revenue per visitor FELL {abs(rpv_change):.1f}% — "
            "picking the winner on conversion rate loses revenue in this test. The primary metric should be RPV."))
    elif cr_change is not None and rpv_change is not None and cr_change < 0 and rpv_change > 0:
        warnings.append(_t(
            f"Dönüşüm oranı %{abs(cr_change):.1f} düştü ama ziyaretçi başına gelir %{rpv_change:.1f} arttı — "
            "daha az ama daha değerli sipariş. Dönüşüm oranına bakıp bu varyantı elemeyin.",
            f"Conversion rate fell {abs(cr_change):.1f}% but revenue per visitor rose {rpv_change:.1f}% — "
            "fewer but more valuable orders. Don't drop this variant on conversion rate alone."))

    # Marj erimesi: yalnızca varyantın kendi marjı verildiğinde anlamlıdır (aksi halde kâr = RPV × sabit).
    if variant_margin_rate is not None and profit_change is not None:
        margins = (f"%{margin_rate * 100:g} → %{variant_margin_rate * 100:g}" if LANG == "tr"
                   else f"{margin_rate * 100:g}% → {variant_margin_rate * 100:g}%")
        if rpv_change is not None and rpv_change > 0 and profit_change < 0:
            warnings.append(_t(
                f"Marj erimesi: ziyaretçi başına gelir %{rpv_change:.1f} arttı ama ziyaretçi başına brüt kâr "
                f"%{abs(profit_change):.1f} DÜŞTÜ (marj {margins}). Gelir artışı kâr kaybını gizliyor; "
                "fiyat/indirim testinde birincil metrik kâr olmalı.",
                f"Margin erosion: revenue per visitor rose {rpv_change:.1f}% but gross profit per visitor FELL "
                f"{abs(profit_change):.1f}% (margin {margins}). The revenue gain hides a profit loss; in a "
                "price/discount test the primary metric should be profit."))
        elif profit_change < -_PROFIT_DROP_WARN_PCT:
            warnings.append(_t(
                f"Ziyaretçi başına brüt kâr %{abs(profit_change):.1f} düştü (marj {margins}). "
                "Bu varyantı kâr kaybını kabul etmeden kazanan ilan etmeyin.",
                f"Gross profit per visitor fell {abs(profit_change):.1f}% (margin {margins}). "
                "Don't declare this variant a winner without accepting the profit loss."))

    result["warning"] = " ".join(warnings) if warnings else None
    return result


# ---------------------------------------------------------------------------
# Metin çıktısı
# ---------------------------------------------------------------------------

def _pct(x, fmt="+.1f"):
    return f"%{x:{fmt}}" if LANG == "tr" else f"{x:{fmt}}%"


def _interval(ci, scale=1.0, fmt=".2f"):
    lo, hi = ci
    a = "−∞" if lo is None else f"{lo * scale:{fmt}}"
    b = "+∞" if hi is None else f"{hi * scale:{fmt}}"
    return f"[{a}, {b}]"


def _pct_interval(ci, fmt="+.1f"):
    lo, hi = ci
    a = "−∞" if lo is None else _pct(lo, fmt)
    b = "+∞" if hi is None else _pct(hi, fmt)
    return f"[{a}, {b}]"


def _sig_word(flag):
    return _t("anlamlı", "significant") if flag else _t("anlamlı değil", "not significant")


def _ni_line(ni):
    return _t(f"Guardrail ({ni['direction']}, marj %{ni['margin_relative'] * 100:g}): {ni['status']}, "
              f"p = {ni['p_value']}",
              f"Guardrail ({ni['direction']}, margin {ni['margin_relative'] * 100:g}%): {ni['status']}, "
              f"p = {ni['p_value']}")


def format_text(command, r):
    """İnsan okunur özet — bağımsız CLI kullanımı için (--format text)."""
    if command == "significance" and "comparisons" in r:
        lines = [_t(f"Kontrol: %{r['control_rate'] * 100:.2f} ({r['n_comparisons']} karşılaştırma, Holm düzeltmesi)",
                    f"Control: {r['control_rate'] * 100:.2f}% ({r['n_comparisons']} comparisons, Holm correction)")]
        for c in r["comparisons"]:
            lines.append(_t(
                f"  {c['arm']}: %{c['variant_rate'] * 100:.2f}, ham p = {c['p_value_raw']}, "
                f"Holm düzeltilmiş p = {c['p_value_adjusted']} ({c['method']}) → {c['decision']}",
                f"  {c['arm']}: {c['variant_rate'] * 100:.2f}%, raw p = {c['p_value_raw']}, "
                f"Holm-adjusted p = {c['p_value_adjusted']} ({c['method']}) → {c['decision']}"))
            if c.get("non_inferiority"):
                lines.append("    " + _ni_line(c["non_inferiority"]))
        lines.append(r["note"])
        return "\n".join(lines)
    if command == "significance":
        sided = r.get("confidence_interval_sided", "two-sided")
        ci_label = {"two-sided": _t("Farkın güven aralığı", "Confidence interval of the difference"),
                    "lower-bound": _t("Farkın tek yönlü alt güven sınırı", "One-sided lower confidence bound"),
                    "upper-bound": _t("Farkın tek yönlü üst güven sınırı", "One-sided upper confidence bound")}[sided]
        lines = [
            _t(f"Kontrol: %{r['control_rate'] * 100:.2f} → Varyant: %{r['variant_rate'] * 100:.2f}",
               f"Control: {r['control_rate'] * 100:.2f}% → Variant: {r['variant_rate'] * 100:.2f}%"),
            _t(f"Fark: {r['absolute_diff'] * 100:+.2f} yüzde puan", f"Difference: {r['absolute_diff'] * 100:+.2f} percentage points")
            + (_t(f" (göreli {_pct(r['relative_lift_pct'])})", f" (relative {_pct(r['relative_lift_pct'])})")
               if r["relative_lift_pct"] is not None else ""),
            f"z = {r['z_score']}, p = {r['p_value']} [{r['method']}] → "
            + _sig_word(r["is_significant"])
            + _t(f" (güven düzeyi %{r['confidence_level'] * 100:.0f})", f" (confidence level {r['confidence_level'] * 100:.0f}%)")
            + ("" if r["normal_approx_valid"] else _t("  [nadir olay: Fisher exact kullanıldı]",
                                                      "  [rare event: Fisher exact used]")),
            f"{ci_label}: {_interval(r['confidence_interval_diff'], 100)} " + _t("yüzde puan", "percentage points"),
        ]
        if r.get("confidence_interval_relative_lift_pct"):
            lines.append(_t("Göreli lift güven aralığı: ", "Relative lift confidence interval: ")
                         + _pct_interval(r["confidence_interval_relative_lift_pct"]))
        if r.get("mde_at_current_n_pct") is not None:
            lines.append(_t(f"Mevcut örneklemde %80 güçle saptanabilir en küçük göreli fark: %{r['mde_at_current_n_pct']:.1f}",
                            f"Smallest relative effect detectable at 80% power with the current sample: "
                            f"{r['mde_at_current_n_pct']:.1f}%"))
        if r.get("non_inferiority"):
            lines.append(_ni_line(r["non_inferiority"]))
        if r.get("peeking_risk"):
            lines.append(_t("Karar: ara bakış, nihai karar verilmez", "Decision: interim look, no final decision"))
        for w in r.get("warnings") or ([r["note"]] if r.get("note") else []):
            lines.append(_t("Uyarı: ", "Warning: ") + w)
        return "\n".join(lines)
    if command == "srm":
        if "observed_split" in r:
            head = _t(f"Gözlenen bölüşüm: %{r['observed_split'] * 100:.2f} (beklenen %{r['expected_split'] * 100:.0f})",
                      f"Observed split: {r['observed_split'] * 100:.2f}% (expected {r['expected_split'] * 100:.0f}%)")
        else:
            head = (_t("Gözlenen paylar: ", "Observed shares: ") + ", ".join(_pct(s * 100, ".2f") for s in r["observed_shares"])
                    + _t(" (beklenen ", " (expected ") + ", ".join(_pct(s * 100, ".1f") for s in r["expected_shares"]) + ")")
        lines = [
            head,
            f"chi2 = {r['chi2']} (" + _t("sd", "df") + f" {r['df']}), p = {r['p_value']} → "
            + (_t("SRM TESPİT EDİLDİ — sonuçlar güvenilmez", "SRM DETECTED — results are not trustworthy")
               if r["srm_detected"] else _t("SRM yok", "no SRM"))
            + ("" if r["normal_approx_valid"] else _t("  [yaklaşım zayıf, aşağıya bakın]", "  [weak approximation, see below]")),
        ]
        if r["note"]:
            lines.append(_t("Uyarı: ", "Warning: ") + r["note"])
        return "\n".join(lines)
    if command == "continuous":
        c, v = r["control"], r["variant"]
        lines = [
            _t("Ortalama: ", "Mean: ") + f"{c['mean']:,.4f} → {v['mean']:,.4f}"
            + (_t(f" (göreli {_pct(r['relative_lift_pct'])})", f" (relative {_pct(r['relative_lift_pct'])})")
               if r["relative_lift_pct"] is not None else ""),
            f"Welch t = {r['t_stat']}, " + _t("sd", "df") + f" = {r['df']}, p = {r['p_value']} → "
            + _sig_word(r["is_significant"]),
            _t("Farkın güven aralığı: ", "Confidence interval of the difference: ")
            + _interval(r["confidence_interval_diff"], 1, ",.4f"),
        ]
        if r.get("non_inferiority"):
            lines.append(_ni_line(r["non_inferiority"]))
        if r.get("bootstrap"):
            b = r["bootstrap"]
            lines.append(_t(f"Bootstrap ({b['resamples']} tekrar) fark aralığı: ",
                            f"Bootstrap ({b['resamples']} resamples) difference interval: ")
                         + _interval(b["ci_diff"], 1, ",.4f"))
        if r.get("cuped"):
            cu = r["cuped"]
            lines.append(_t(f"CUPED: varyans azalması %{cu['variance_reduction_pct']}, p = {cu['p_value']} → ",
                            f"CUPED: variance reduction {cu['variance_reduction_pct']}%, p = {cu['p_value']} → ")
                         + _sig_word(cu["is_significant"]))
        if r["note"]:
            lines.append(_t("Not: ", "Note: ") + r["note"])
        return "\n".join(lines)
    if command == "interaction":
        lines = []
        for s in r["segments"]:
            lines.append(f"{s['name']}: " + _pct(s["control_rate"] * 100, ".2f") + " → "
                         + _pct(s["variant_rate"] * 100, ".2f")
                         + f" ({s['absolute_diff_pp']:+.2f} " + _t("yüzde puan", "pp") + ")")
        a = r["interaction_absolute"]
        lines.append(_t(f"Fark-içinde-fark: {a['diff_in_diff_pp']:+.2f} yüzde puan, z = {a['z']}, p = {a['p_value']}",
                        f"Difference-in-differences: {a['diff_in_diff_pp']:+.2f} pp, z = {a['z']}, p = {a['p_value']}"))
        if r["interaction_relative"]:
            rel = r["interaction_relative"]
            lines.append(_t(f"Göreli ölçek: oranların oranı {rel['ratio_of_rate_ratios']}, p = {rel['p_value']}",
                            f"Relative scale: ratio of rate ratios {rel['ratio_of_rate_ratios']}, p = {rel['p_value']}"))
        lines.append("→ " + r["decision"])
        for w in r["warnings"]:
            lines.append(_t("Uyarı: ", "Warning: ") + w)
        lines.append(r["note"])
        return "\n".join(lines)
    if command == "bayes":
        lo, hi = r["credible_interval_relative_lift_pct"]
        return "\n".join([
            _t("P(varyant > kontrol) = ", "P(variant > control) = ") + _pct(r["prob_variant_beats_control"] * 100, ".1f"),
            _t(f"Beklenen kayıp — varyantı seçersen: {r['expected_loss_choose_variant']}, "
               f"kontrolü seçersen: {r['expected_loss_choose_control']}",
               f"Expected loss — choosing variant: {r['expected_loss_choose_variant']}, "
               f"choosing control: {r['expected_loss_choose_control']}"),
            _t(f"Göreli lift %{r['credible_level'] * 100:.0f} güvenilir aralığı: ",
               f"Relative lift {r['credible_level'] * 100:.0f}% credible interval: ") + _pct_interval([lo, hi]),
            _t(f"Tohum (seed): {r['seed']}", f"Seed: {r['seed']}"),
            r["note"],
        ])
    if command == "revenue":
        c, v = r["control"], r["variant"]

        def chg(x):
            return f"({_pct(x)})" if x is not None else ""

        lines = [
            _t("Dönüşüm oranı: ", "Conversion rate: ") + f"{_pct(c['cr'] * 100, '.2f')} → {_pct(v['cr'] * 100, '.2f')} "
            + chg(r["cr_change_pct"]),
            _t("Ortalama sipariş tutarı: ", "Average order value: ") + f"{c['aov']:,.2f} → {v['aov']:,.2f} "
            + chg(r["aov_change_pct"]),
            _t("Ziyaretçi başına gelir (RPV): ", "Revenue per visitor (RPV): ") + f"{c['rpv']:,.2f} → {v['rpv']:,.2f} "
            + chg(r["rpv_change_pct"]),
        ]
        if r["profit_per_visitor"]:
            p = r["profit_per_visitor"]
            # İki kolun marjı farklıysa etiketi gizlemek yanıltıcı olur:
            # varyant değeri kendi marjıyla hesaplanmıştır, tek marj basma.
            if r.get("variant_margin_rate") not in (None, r["margin_rate"]):
                mtxt = f"{_pct(r['margin_rate'] * 100, '.0f')} → {_pct(r['variant_margin_rate'] * 100, '.0f')}"
            else:
                mtxt = _pct(r["margin_rate"] * 100, ".0f")
            lines.append(_t(f"Ziyaretçi başına brüt kâr (marj {mtxt}): ", f"Gross profit per visitor (margin {mtxt}): ")
                         + f"{p['control']:,.2f} → {p['variant']:,.2f} " + chg(p["change_pct"]))
        if r["warning"]:
            lines.append(_t("\nDİKKAT: ", "\nCAUTION: ") + r["warning"])
        lines.append(f"\n{r['note']}")
        return "\n".join(lines)
    # samplesize
    lines = []
    if "required_n_total" in r:
        if r.get("metric") == "mean":
            lines.append(_t(
                f"Baz ortalama {r['baseline_mean']:g} (sd {r['baseline_sd']:g}), hedef {r['target_mean']:g} "
                f"(göreli %{r['mde_relative_pct']:g} fark) için varyant başına {r['required_n_per_variant']:,} "
                f"gözlem gerekir (toplam {r['required_n_total']:,}; güven %{r['confidence_level'] * 100:.0f}, "
                f"güç %{r['power'] * 100:.0f}).",
                f"Baseline mean {r['baseline_mean']:g} (sd {r['baseline_sd']:g}), target {r['target_mean']:g} "
                f"({r['mde_relative_pct']:g}% relative effect) needs {r['required_n_per_variant']:,} observations per "
                f"variant ({r['required_n_total']:,} total; confidence {r['confidence_level'] * 100:.0f}%, "
                f"power {r['power'] * 100:.0f}%)."))
        else:
            lines.append(_t(
                f"Baz oran %{r['baseline_rate'] * 100:.2f}, hedef %{r['target_rate'] * 100:.2f} "
                f"(göreli %{r['mde_relative_pct']:g} lift) için varyant başına {r['required_n_per_variant']:,} "
                f"ziyaretçi gerekir (toplam {r['required_n_total']:,}; güven %{r['confidence_level'] * 100:.0f}, "
                f"güç %{r['power'] * 100:.0f}).",
                f"Baseline rate {r['baseline_rate'] * 100:.2f}%, target {r['target_rate'] * 100:.2f}% "
                f"({r['mde_relative_pct']:g}% relative lift) needs {r['required_n_per_variant']:,} visitors per "
                f"variant ({r['required_n_total']:,} total; confidence {r['confidence_level'] * 100:.0f}%, "
                f"power {r['power'] * 100:.0f}%)."))
        if r.get("ratio", 1) != 1:
            lines[-1] += _t(f" Kontrol {r['required_n_control']:,} / varyant {r['required_n_variant']:,}.",
                            f" Control {r['required_n_control']:,} / variant {r['required_n_variant']:,}.")
        if r.get("duration_days") is not None and r.get("weeks") is None:
            lines.append(_t(f"Süre: {r['duration_days']} gün ({r['duration_weeks']} hafta; günde "
                            f"{r['daily_visitors']:,} ziyaretçiyle örneklem {r['duration_days_raw']} günde dolar).",
                            f"Duration: {r['duration_days']} days ({r['duration_weeks']} weeks; at "
                            f"{r['daily_visitors']:,} visitors/day the sample fills in {r['duration_days_raw']} days)."))
    if r.get("weeks") is not None:
        mde = r.get("mde_detectable_relative_pct")
        lines.append(_t(f"{r['weeks']} haftada (günde {r['daily_visitors']:,} ziyaretçi) saptanabilir en küçük göreli fark: "
                        + (f"%{mde:g}" if mde is not None else "yok"),
                        f"Smallest relative effect detectable in {r['weeks']} weeks ({r['daily_visitors']:,} visitors/day): "
                        + (f"{mde:g}%" if mde is not None else "none")))
    if r.get("note"):
        lines.append(_t("Not: ", "Note: ") + r["note"])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

class _StoreOnce(argparse._StoreAction):
    """Tekrarlanan tek değerli bayrakları kaydeder; main() bunları hata olarak raporlar.
    argparse varsayılan olarak sonuncuyu sessizce tutar — ör. iki kez verilen --variant-visitors
    k kollu SRM'de ilk kolu kaybeder."""

    def __call__(self, parser, namespace, values, option_string=None):
        seen = getattr(namespace, "_seen_flags", None)
        if seen is None:
            seen = {}
            setattr(namespace, "_seen_flags", seen)
        flag = self.option_strings[-1] if self.option_strings else self.dest
        seen.setdefault(self.dest, [flag, []])[1].append(values)
        setattr(namespace, self.dest, values)


def _repeated_flag_error(args):
    seen = getattr(args, "_seen_flags", None) or {}
    for dest, (flag, vals) in seen.items():
        if len(vals) > 1:
            shown = ", ".join(str(v) for v in vals)
            msg = _t(f"{flag} birden fazla verildi ({shown}); yalnızca sonuncusu okunurdu, bu yüzden reddedildi.",
                     f"{flag} was given more than once ({shown}); only the last value would be read, so this is rejected.")
            if args.command == "srm" and dest in ("variant_visitors", "control_visitors"):
                msg += _t(" k kollu SRM için tüm kolları tek bayrakla verin: srm --visitors 5000,5100,4900",
                          " For k-arm SRM give every arm in one flag: srm --visitors 5000,5100,4900")
            elif args.command == "significance" and dest in ("variant_visitors", "variant_conversions"):
                msg += _t(" A/B/n için her varyantı --variant ZİYARETÇİ:DÖNÜŞÜM ile tekrarlayın, ör. "
                          "--variant 5000:290 --variant 5000:270",
                          " For A/B/n repeat --variant VISITORS:CONVERSIONS per arm, e.g. "
                          "--variant 5000:290 --variant 5000:270")
            return msg
    return None


def _parse_list(s, conv, label):
    try:
        return [conv(x) for x in str(s).split(",") if x.strip()]
    except (ValueError, argparse.ArgumentTypeError):
        raise ValueError(_t(f"{label} virgülle ayrılmış sayılar olmalı (verilen: {s!r})",
                            f"{label} must be comma-separated numbers (given: {s!r})"))


def build_parser():
    """Seçili dile (LANG) göre yardım metinleriyle ayrıştırıcıyı kurar. Yardım metinlerinde '%' yerine
    '%%' yazılır: argparse yardım metnini %-biçimlendirmeden geçirir, tek '%' --help'i çökertir."""
    parser = argparse.ArgumentParser(description=__doc__ if LANG == "tr" else _DESCRIPTION_EN,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    lang_help = _t("Mesaj dili (en|tr, varsayılan en)", "Message language (en|tr, default en)")
    parser.add_argument("--lang", choices=_LANGS, default="en", help=lang_help)
    sub = parser.add_subparsers(dest="command", required=True)
    alt_help = _t("Hipotez yönü: two-sided (varsayılan), greater (varyant > kontrol), less",
                  "Hypothesis direction: two-sided (default), greater (variant > control), less")
    fmt_help = _t("Çıktı biçimi: json (varsayılan) veya text", "Output format: json (default) or text")
    conf_help = _t("Güven düzeyi, ör. 0.95", "Confidence level, e.g. 0.95")
    ni_help = _t("Guardrail non-inferiority marjı (göreli kesir, ör. 0.02 = 2 yüzde); tek yönlü test edilir",
                 "Guardrail non-inferiority margin (relative fraction, e.g. 0.02 = 2 percent); tested one-sided")
    dir_help = _t("Guardrail yönü: must_not_decrease (varsayılan; ör. dönüşüm, marj) veya must_not_increase "
                  "(ör. iade oranı, hata oranı, LCP)",
                  "Guardrail direction: must_not_decrease (default; e.g. conversion, margin) or must_not_increase "
                  "(e.g. return rate, error rate, LCP)")

    def new(name, help_text):
        p = sub.add_parser(name, help=help_text, description=help_text)
        p.register("action", None, _StoreOnce)
        p.add_argument("--lang", choices=_LANGS, default=argparse.SUPPRESS, help=lang_help)
        return p

    p1 = new("significance", _t("Varyant(lar)ı kontrolle karşılaştır (z-testi / Fisher exact)",
                                "Compare variant(s) with control (z-test / Fisher exact)"))
    p1.add_argument("--control-visitors", type=parse_count, required=True)
    p1.add_argument("--control-conversions", type=parse_count, required=True)
    p1.add_argument("--variant-visitors", type=parse_count, default=None)
    p1.add_argument("--variant-conversions", type=parse_count, default=None)
    p1.add_argument("--variant", type=parse_arm, action="append", default=[],
                    help=_t("Tekrarlanabilir ZİYARETÇİ:DÖNÜŞÜM, ör. --variant 5000:290 --variant 5000:270 (A/B/n)",
                            "Repeatable VISITORS:CONVERSIONS, e.g. --variant 5000:290 --variant 5000:270 (A/B/n)"))
    p1.add_argument("--confidence", type=float, default=0.95, help=conf_help)
    p1.add_argument("--alternative", choices=_ALTERNATIVES, default="two-sided", help=alt_help)
    p1.add_argument("--planned-n", type=parse_count, default=None,
                    help=_t("Kol başına planlanan örneklem; altındaysa ara bakış (peeking) uyarısı verilir",
                            "Planned sample per arm; below it the result is flagged as an interim look (peeking)"))
    p1.add_argument("--ni-margin", type=float, default=None, help=ni_help)
    p1.add_argument("--guardrail-direction", choices=_GUARDRAIL_DIRECTIONS, default="must_not_decrease", help=dir_help)
    p1.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)

    p3 = new("revenue", _t("Gelir/kâr yön göstergesi (çıkarım için 'continuous' kullanın)",
                           "Revenue/profit directional check (use 'continuous' for inference)"))
    p3.add_argument("--control-visitors", type=parse_count, required=True)
    p3.add_argument("--control-conversions", type=parse_count, required=True)
    p3.add_argument("--control-aov", type=float, required=True,
                    help=_t("Kontrolde ortalama sipariş tutarı", "Average order value in control"))
    p3.add_argument("--variant-visitors", type=parse_count, required=True)
    p3.add_argument("--variant-conversions", type=parse_count, required=True)
    p3.add_argument("--variant-aov", type=float, required=True,
                    help=_t("Varyantta ortalama sipariş tutarı", "Average order value in the variant"))
    p3.add_argument("--margin-rate", type=float, default=None,
                    help=_t("Kontrol kolunun brüt marj oranı, ör. 0.35", "Control arm gross margin rate, e.g. 0.35"))
    p3.add_argument("--variant-margin-rate", type=float, default=None,
                    help=_t("Varyantın brüt marj oranı farklıysa (fiyat/indirim testi); verilmezse kontrolünkiyle "
                            "aynı varsayılır. Verilirse kâr erimesi uyarısı açılır.",
                            "Variant gross margin rate if it differs (price/discount test); assumed equal to "
                            "control if omitted. When given, the margin-erosion warning is enabled."))
    p3.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)

    p4 = new("srm", _t("Örneklem oranı uyuşmazlığı (SRM) kontrolü — randomizasyonu denetler, sonucu değil",
                       "Sample ratio mismatch (SRM) check — audits randomization, not the result"))
    p4.add_argument("--control-visitors", type=parse_count, default=None)
    p4.add_argument("--variant-visitors", type=parse_count, default=None)
    p4.add_argument("--expected-split", type=float, default=0.5,
                    help=_t("Kontrol koluna planlanan pay, ör. 0.5", "Planned control share, e.g. 0.5"))
    p4.add_argument("--visitors", default=None,
                    help=_t("k kol için virgülle ayrılmış ziyaretçi sayıları, ör. 5000,5100,4900",
                            "Comma-separated visitors for k arms, e.g. 5000,5100,4900"))
    p4.add_argument("--expected-ratios", default=None,
                    help=_t("k kol için planlanan oranlar, ör. 1,1,2 (varsayılan eşit)",
                            "Planned ratios for k arms, e.g. 1,1,2 (default equal)"))
    p4.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)

    p2 = new("samplesize", _t("Gereken örneklem büyüklüğü ve süre", "Required sample size and duration"))
    p2.add_argument("--metric", choices=["proportion", "mean"], default="proportion",
                    help=_t("proportion (dönüşüm oranı, varsayılan) veya mean (sürekli metrik)",
                            "proportion (conversion rate, default) or mean (continuous metric)"))
    p2.add_argument("--baseline-rate", type=float, default=None,
                    help=_t("Ör. 0.05 (5 yüzde dönüşüm); --metric proportion için", "E.g. 0.05 (5 percent conversion); for --metric proportion"))
    p2.add_argument("--baseline-mean", type=float, default=None,
                    help=_t("Baz ortalama; --metric mean için", "Baseline mean; for --metric mean"))
    p2.add_argument("--baseline-sd", type=float, default=None,
                    help=_t("Baz standart sapma; --metric mean için", "Baseline standard deviation; for --metric mean"))
    p2.add_argument("--mde", type=float, default=None,
                    help=_t("Göreli minimum tespit edilebilir fark, ör. 0.20 (1'den büyükse yüzde sayılır: 10 = 0.10)",
                            "Relative minimum detectable effect, e.g. 0.20 (values above 1 are read as percent: 10 = 0.10)"))
    p2.add_argument("--confidence", type=float, default=0.95, help=conf_help)
    p2.add_argument("--power", type=float, default=0.80, help=_t("İstatistiksel güç, ör. 0.80", "Statistical power, e.g. 0.80"))
    p2.add_argument("--alternative", choices=_ALTERNATIVES, default="two-sided", help=alt_help)
    p2.add_argument("--ratio", type=float, default=1.0,
                    help=_t("Varyant/kontrol örneklem oranı (n_varyant = ratio * n_kontrol)",
                            "Variant/control sample ratio (n_variant = ratio * n_control)"))
    p2.add_argument("--arms", type=parse_count, default=2,
                    help=_t("Kontrol dahil toplam kol sayısı (alfa Bonferroni ile bölünür)",
                            "Total arms including control (alpha split with Bonferroni)"))
    p2.add_argument("--daily-visitors", type=parse_count, default=None,
                    help=_t("Tüm kollar toplamı günlük uygun ziyaretçi → süre (tam hafta, en az 14 gün)",
                            "Total daily eligible visitors across all arms → duration (whole weeks, 14-day floor)"))
    p2.add_argument("--weeks", type=parse_count, default=None,
                    help=_t("Ters hesap: bu kadar haftada saptanabilir en küçük göreli fark (--daily-visitors gerekir)",
                            "Inverse: smallest relative effect detectable in this many weeks (needs --daily-visitors)"))
    p2.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)

    p5 = new("continuous", _t("Sürekli metrik (ziyaretçi başına gelir vb.): Welch t, bootstrap, CUPED",
                              "Continuous metric (revenue per visitor etc.): Welch t, bootstrap, CUPED"))
    p5.add_argument("--control-csv", default=None,
                    help=_t("Kontrol: kullanıcı başına bir satır (sıfırlar dahil)", "Control: one row per user (zeros included)"))
    p5.add_argument("--variant-csv", default=None,
                    help=_t("Varyant: kullanıcı başına bir satır", "Variant: one row per user"))
    p5.add_argument("--value-column", default=None,
                    help=_t("Metrik sütunu: başlık adı veya 0'dan başlayan sıra. Birden çok sütunlu CSV'de zorunlu",
                            "Metric column: header name or 0-based index. Required when the CSV has more than one column"))
    p5.add_argument("--id-column", default=None,
                    help=_t("Kullanıcı kimliği sütunu (ad veya sıra): CUPED ön-dönem dosyaları kimlikle eşleştirilir, "
                            "tekrarlanan kimlik ve kollar arası sızıntı denetlenir",
                            "User id column (name or index): CUPED pre-period files are joined by id, duplicate "
                            "ids and cross-arm leakage are checked"))
    p5.add_argument("--pre-value-column", default=None,
                    help=_t("Ön-dönem dosyalarındaki değer sütunu (varsayılan: --value-column)",
                            "Value column in the pre-period files (default: --value-column)"))
    p5.add_argument("--control-n", type=parse_count, default=None)
    p5.add_argument("--control-mean", type=float, default=None)
    p5.add_argument("--control-sd", type=float, default=None)
    p5.add_argument("--variant-n", type=parse_count, default=None)
    p5.add_argument("--variant-mean", type=float, default=None)
    p5.add_argument("--variant-sd", type=float, default=None)
    p5.add_argument("--confidence", type=float, default=0.95, help=conf_help)
    p5.add_argument("--alternative", choices=_ALTERNATIVES, default="two-sided", help=alt_help)
    p5.add_argument("--winsorize", type=float, default=None,
                    help=_t("Üst kuyruğu bu yüzdelikte kırp, ör. 0.99", "Cap the upper tail at this percentile, e.g. 0.99"))
    p5.add_argument("--bootstrap", type=parse_count, default=0,
                    help=_t("Yüzdelik bootstrap tekrar sayısı, ör. 2000", "Percentile bootstrap resamples, e.g. 2000"))
    p5.add_argument("--seed", type=int, default=DEFAULT_SEED,
                    help=_t(f"Bootstrap tohumu (varsayılan {DEFAULT_SEED})", f"Bootstrap seed (default {DEFAULT_SEED})"))
    p5.add_argument("--control-pre-csv", default=None,
                    help=_t("CUPED: kontrol ön-dönem kovaryatı", "CUPED: control pre-period covariate"))
    p5.add_argument("--variant-pre-csv", default=None,
                    help=_t("CUPED: varyant ön-dönem kovaryatı", "CUPED: variant pre-period covariate"))
    p5.add_argument("--ni-margin", type=float, default=None, help=ni_help)
    p5.add_argument("--guardrail-direction", choices=_GUARDRAIL_DIRECTIONS, default="must_not_decrease", help=dir_help)
    p5.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)

    p7 = new("interaction", _t("Segment etkileşimi: tedavi etkisi iki segmentte gerçekten farklı mı (fark-içinde-fark)",
                               "Segment interaction: does the treatment effect really differ between two segments (diff-in-diff)"))
    p7.add_argument("--seg1", type=parse_segment, required=True,
                    help=_t("1. segment: A_ZİY:A_DÖN,B_ZİY:B_DÖN (A = kontrol), ör. 4000:200,4000:260",
                            "Segment 1: A_VIS:A_CONV,B_VIS:B_CONV (A = control), e.g. 4000:200,4000:260"))
    p7.add_argument("--seg2", type=parse_segment, required=True, help=_t("2. segment, aynı biçim", "Segment 2, same format"))
    p7.add_argument("--seg1-name", default="seg1", help=_t("1. segmentin adı", "Name of segment 1"))
    p7.add_argument("--seg2-name", default="seg2", help=_t("2. segmentin adı", "Name of segment 2"))
    p7.add_argument("--confidence", type=float, default=0.95, help=conf_help)
    p7.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)

    p6 = new("bayes", _t("Bayes görünümü (alternatif bakış; frekansçı kararın yerine geçmez)",
                         "Bayesian view (alternative lens; doesn't replace the frequentist decision)"))
    p6.add_argument("--control-visitors", type=parse_count, required=True)
    p6.add_argument("--control-conversions", type=parse_count, required=True)
    p6.add_argument("--variant-visitors", type=parse_count, required=True)
    p6.add_argument("--variant-conversions", type=parse_count, required=True)
    p6.add_argument("--draws", type=parse_count, default=100000,
                    help=_t("Monte Carlo çekiliş sayısı", "Monte Carlo draws"))
    p6.add_argument("--seed", type=int, default=DEFAULT_SEED,
                    help=_t(f"Rastgele tohum (varsayılan {DEFAULT_SEED}; tekrarlanabilirlik için sabit)",
                            f"Random seed (default {DEFAULT_SEED}; fixed for reproducibility)"))
    p6.add_argument("--credible", type=float, default=0.95,
                    help=_t("Güvenilir aralık düzeyi", "Credible interval level"))
    p6.add_argument("--format", choices=["json", "text"], default="json", help=fmt_help)
    return parser


def _run(args):
    dup = _repeated_flag_error(args)
    if dup:
        raise ValueError(dup)
    if args.command == "significance":
        variants = list(args.variant)
        if args.variant_visitors is not None or args.variant_conversions is not None:
            if args.variant_visitors is None or args.variant_conversions is None:
                raise ValueError(_t("--variant-visitors ve --variant-conversions birlikte verilmeli",
                                    "--variant-visitors and --variant-conversions must be given together"))
            variants.insert(0, (args.variant_visitors, args.variant_conversions))
        if not variants:
            raise ValueError(_t("en az bir varyant verin: --variant-visitors/--variant-conversions veya --variant Z:D",
                                "give at least one variant: --variant-visitors/--variant-conversions or --variant V:C"))
        ni = dict(ni_margin=args.ni_margin, guardrail_direction=args.guardrail_direction)
        if len(variants) == 1:
            return significance(args.control_visitors, args.control_conversions,
                                variants[0][0], variants[0][1], args.confidence,
                                args.alternative, args.planned_n, **ni)
        return significance_multi(args.control_visitors, args.control_conversions, variants,
                                  args.confidence, args.alternative, args.planned_n, **ni)
    if args.command == "revenue":
        return revenue(args.control_visitors, args.control_conversions, args.control_aov,
                       args.variant_visitors, args.variant_conversions, args.variant_aov,
                       args.margin_rate, args.variant_margin_rate)
    if args.command == "srm":
        if args.visitors:
            ratios = _parse_list(args.expected_ratios, float, "--expected-ratios") if args.expected_ratios else None
            return srm_multi(_parse_list(args.visitors, parse_count, "--visitors"), ratios)
        if args.control_visitors is None or args.variant_visitors is None:
            raise ValueError(_t("--control-visitors ve --variant-visitors (veya --visitors) verin",
                                "give --control-visitors and --variant-visitors (or --visitors)"))
        return srm(args.control_visitors, args.variant_visitors, args.expected_split)
    if args.command == "continuous":
        kw = dict(confidence=args.confidence, alternative=args.alternative, winsorize=args.winsorize,
                  bootstrap=args.bootstrap, seed=args.seed, ni_margin=args.ni_margin,
                  guardrail_direction=args.guardrail_direction)
        info = None
        if args.control_csv or args.variant_csv:
            if not (args.control_csv and args.variant_csv):
                raise ValueError(_t("--control-csv ve --variant-csv birlikte verilmeli",
                                    "--control-csv and --variant-csv must be given together"))
            loaded, info = load_continuous_inputs(args.control_csv, args.variant_csv,
                                                  args.control_pre_csv, args.variant_pre_csv,
                                                  args.value_column, args.pre_value_column, args.id_column)
            kw.update(loaded)
        else:
            stats = [args.control_n, args.control_mean, args.control_sd,
                     args.variant_n, args.variant_mean, args.variant_sd]
            if any(s is None for s in stats):
                raise ValueError(_t("CSV yoksa iki kol için de --*-n, --*-mean, --*-sd verilmeli",
                                    "without CSVs, give --*-n, --*-mean and --*-sd for both arms"))
            kw["control_stats"] = tuple(stats[:3])
            kw["variant_stats"] = tuple(stats[3:])
        result = continuous(**kw)
        if info is not None:
            result["input_columns"] = info
        return result
    if args.command == "interaction":
        return interaction(args.seg1, args.seg2, args.confidence, (args.seg1_name, args.seg2_name))
    if args.command == "bayes":
        return bayes(args.control_visitors, args.control_conversions,
                     args.variant_visitors, args.variant_conversions,
                     args.draws, args.seed, args.credible)
    # samplesize
    plan = dict(confidence=args.confidence, power=args.power, alternative=args.alternative, ratio=args.ratio,
                arms=args.arms, daily_visitors=args.daily_visitors, weeks=args.weeks)
    if args.metric == "mean":
        if args.baseline_mean is None or args.baseline_sd is None:
            raise ValueError(_t("--metric mean için --baseline-mean ve --baseline-sd gerekli",
                                "--metric mean needs --baseline-mean and --baseline-sd"))
        return sample_size_mean(args.baseline_mean, args.baseline_sd, args.mde, **plan)
    if args.baseline_rate is None:
        raise ValueError(_t("--baseline-rate gerekli (sürekli metrik için --metric mean kullanın)",
                            "--baseline-rate is required (use --metric mean for a continuous metric)"))
    return sample_size(args.baseline_rate, args.mde, **plan)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    # Dil, yardım metinleri kurulmadan önce belirlenmeli: --lang komutun neresinde olursa olsun okunur.
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--lang", choices=_LANGS, default="en")
    known, _ = pre.parse_known_args(argv)
    set_lang(known.lang)

    args = build_parser().parse_args(argv)
    try:
        result = _run(args)
    except (ValueError, OSError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    if args.format == "text":
        print(format_text(args.command, result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
