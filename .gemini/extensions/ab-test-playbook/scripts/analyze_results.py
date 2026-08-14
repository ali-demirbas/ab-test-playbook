#!/usr/bin/env python3
"""
İki-oranlı z-testi ve örneklem büyüklüğü hesaplayıcı.

Kullanım:
  Sonuç yorumlama (anlamlılık testi):
    python3 analyze_results.py significance \
      --control-visitors 5000 --control-conversions 250 \
      --variant-visitors 5000 --variant-conversions 290

  Örneklem büyüklüğü (test planlama):
    python3 analyze_results.py samplesize \
      --baseline-rate 0.05 --mde 0.20 --confidence 0.95 --power 0.80

Sadece Python standart kütüphanesi kullanır (math). Dış bağımlılık yok.
"""
import argparse
import json
import math
import sys


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


def significance(control_visitors, control_conversions, variant_visitors, variant_conversions, confidence=0.95):
    for ad, v, c in (("kontrol", control_visitors, control_conversions),
                     ("varyant", variant_visitors, variant_conversions)):
        if v <= 0:
            raise ValueError(f"{ad} ziyaretçi sayısı pozitif olmalı (verilen: {v})")
        if c < 0:
            raise ValueError(f"{ad} dönüşüm sayısı negatif olamaz (verilen: {c})")
        if c > v:
            raise ValueError(f"{ad} dönüşüm sayısı ({c}) ziyaretçi sayısından ({v}) büyük olamaz")
    if not 0 < confidence < 1:
        raise ValueError(f"güven düzeyi 0 ile 1 arasında olmalı (verilen: {confidence})")

    p1 = control_conversions / control_visitors
    p2 = variant_conversions / variant_visitors
    n1, n2 = control_visitors, variant_visitors

    p_pool = (control_conversions + variant_conversions) / (n1 + n2)
    se_pool = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se_pool if se_pool > 0 else 0.0
    # erfc, 2*(1-norm_cdf(z)) ile matematiksel olarak aynıdır ama büyük |z|'de
    # 0'a yuvarlanmaz: p hiçbir zaman tam 0.0 basılmaz (istatistiksel olarak yanıltıcıdır).
    p_value = math.erfc(abs(z) / math.sqrt(2))

    se_diff = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = norm_ppf(1 - (1 - confidence) / 2)
    diff = p2 - p1
    ci_low = diff - z_crit * se_diff
    ci_high = diff + z_crit * se_diff

    is_significant = p_value < (1 - confidence)
    relative_lift = (diff / p1) if p1 > 0 else None

    # --- Normal yaklaşımın geçerliliği (rare-event kontrolü) ---
    # z-testi normal yaklaşıma dayanır; bu yaklaşım her iki kolda hem beklenen dönüşüm
    # hem beklenen dönüşmeme sayısı yeterince büyükken geçerlidir. Standart kriter: pooled
    # oranla hesaplanan dört beklenen sayının hepsi >= 10. Nadir olaylarda (ör. 100.000
    # ziyaretçide 3 dönüşüm) bu koşul düşer ve p-değeri/güven aralığı güvenilmez olur —
    # örneklem "büyük" görünse bile. Bu, aşağıdaki 250 eşiğinden bağımsız bir kontroldür.
    min_expected_count = 10
    expected_counts = [n1 * p_pool, n1 * (1 - p_pool), n2 * p_pool, n2 * (1 - p_pool)]
    normal_approx_valid = min(expected_counts) >= min_expected_count

    # 250, formal bir güvenilirlik eşiği değil — kaba bir "muhtemelen çok küçük" uyarı sınırıdır.
    # Asıl yeterlilik, bu testin baz oranı ve hedeflenen MDE'siyle sample_size() çalıştırılarak
    # required_n_per_variant'a göre değerlendirilir; bu uyarı sadece hızlı bir bayraktır.
    min_reliable_conversions = 250
    low_sample_warning = control_conversions < min_reliable_conversions or variant_conversions < min_reliable_conversions

    notes = []
    if not normal_approx_valid:
        notes.append(
            "Nadir olay uyarısı: beklenen dönüşüm/dönüşmeme sayılarından en az biri "
            f"{min_expected_count}'un altında (en küçüğü {min(expected_counts):.1f}). Bu testte normal yaklaşım "
            "geçerli değil — p-değeri ve güven aralığı güvenilmez, sonucu anlamlı/anlamsız diye ilan etmeyin. "
            "Daha fazla veri toplayın veya nadir olaylar için uygun bir yöntem (exact test) kullanın."
        )
    if low_sample_warning:
        notes.append(
            "Dönüşüm sayısı 250'nin altında — bu kaba bir uyarı eşiğidir, formal yeterlilik kriteri değil. "
            "Gerçek yeterliliği bu testin baz oranı/MDE'siyle 'samplesize' komutunu çalıştırarak doğrulayın; "
            "iki hafta/yeterli örneklem koşulu sağlanmadan sonucu yorumlamayın."
        )

    return {
        "control_rate": round(p1, 5),
        "variant_rate": round(p2, 5),
        "absolute_diff": round(diff, 5),
        "relative_lift_pct": round(relative_lift * 100, 2) if relative_lift is not None else None,
        "z_score": round(z, 4),
        # Çok küçük p'yi 5 haneye yuvarlamak onu 0.0'a ezer; 0 basmak yanıltıcıdır.
        "p_value": round(p_value, 5) if p_value >= 1e-5 else p_value,
        "confidence_level": confidence,
        "confidence_interval_diff": [round(ci_low, 5), round(ci_high, 5)],
        "is_significant": is_significant,
        "normal_approx_valid": normal_approx_valid,
        "min_expected_count": round(min(expected_counts), 2),
        "low_sample_warning": low_sample_warning,
        "note": " ".join(notes) if notes else None,
    }


def srm(control_visitors, variant_visitors, expected_split=0.5):
    """Örneklem oranı uyuşmazlığı (SRM) kontrolü — bir sonuç metriği değil, testin
    RANDOMİZASYONUNUN kendisini denetler. Gerçekleşen trafik bölüşümünün planlanan
    orana (varsayılan %50/50) rastlantıyla uyup uymadığını Pearson ki-kare uyum
    testiyle (1 serbestlik derecesi) sınar; 2 hücreli ki-kare, z=sqrt(chi2) ile
    zaten var olan norm_cdf'e indirgenir, ayrı bir dağılım fonksiyonu gerekmez.
    SRM varsa test sonuçları güvenilmez — bu bir anlamlılık testi değildir."""
    if control_visitors < 0 or variant_visitors < 0:
        raise ValueError("ziyaretçi sayıları negatif olamaz")
    total = control_visitors + variant_visitors
    if total == 0:
        raise ValueError("toplam ziyaretçi sayısı sıfır olamaz")
    if not 0 < expected_split < 1:
        raise ValueError(f"beklenen bölüşüm 0 ile 1 arasında olmalı (verilen: {expected_split})")

    expected_control = total * expected_split
    expected_variant = total * (1 - expected_split)
    chi2 = ((control_visitors - expected_control) ** 2 / expected_control +
            (variant_visitors - expected_variant) ** 2 / expected_variant)
    # erfc, 2*(1-norm_cdf(z)) ile aynıdır ama büyük chi2'de 0'a yuvarlanmaz
    # (significance()'daki aynı düzeltmeyle tutarlı — bkz. p_value yorumu orada).
    p_value = math.erfc(math.sqrt(chi2 / 2)) if chi2 > 0 else 1.0

    # Ki-kare yaklaşımının geçerlilik kriteri: her beklenen hücre >= 5 (yaygın eşik).
    normal_approx_valid = min(expected_control, expected_variant) >= 5

    # SRM kontrolü HER testte koşulur; nominal %5 eşiği kullanılırsa denenen her 20
    # testten biri salt rastlantıyla "SRM var" der. Bu yüzden pratikte çok daha katı
    # bir eşik (p < 0.001) kullanılır — az sayıda gerçek SRM'i kaçırma pahasına yanlış
    # alarmı sistematik olarak azaltır. Bu tasarım tercihidir, ölçülmüş bir sabit değil.
    srm_detected = p_value < 0.001

    note = None
    if not normal_approx_valid:
        note = (
            f"Uyarı: beklenen hücre sayılarından en az biri 5'in altında "
            f"(en küçüğü {min(expected_control, expected_variant):.1f}) — bu örneklemde ki-kare "
            "yaklaşımı zayıf, sonucu ihtiyatla okuyun; daha fazla veri toplayın."
        )

    return {
        "control_visitors": control_visitors,
        "variant_visitors": variant_visitors,
        "observed_split": round(control_visitors / total, 5),
        "expected_split": expected_split,
        "chi2": round(chi2, 4),
        "p_value": round(p_value, 6) if p_value >= 1e-6 else p_value,
        "srm_detected": srm_detected,
        "normal_approx_valid": normal_approx_valid,
        "note": note,
    }


def sample_size(baseline_rate, mde, confidence=0.95, power=0.80):
    """mde: göreli minimum tespit edilebilir fark (ör. 0.20 = %20 lift).
    Dönüş: varyant başına gereken minimum ziyaretçi sayısı."""
    if not 0 < baseline_rate < 1:
        raise ValueError(f"baz dönüşüm oranı 0 ile 1 arasında olmalı (verilen: {baseline_rate})")
    if mde <= 0:
        raise ValueError(f"MDE pozitif olmalı (verilen: {mde})")
    if not 0 < confidence < 1:
        raise ValueError(f"güven düzeyi 0 ile 1 arasında olmalı (verilen: {confidence})")
    if not 0 < power < 1:
        raise ValueError(f"güç (power) 0 ile 1 arasında olmalı (verilen: {power})")

    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    if p2 >= 1:
        raise ValueError(f"hedef oran %100'ü aşıyor ({p2:.3f}); baz oran veya MDE'yi küçültün")

    z_alpha = norm_ppf(1 - (1 - confidence) / 2)
    z_beta = norm_ppf(power)

    p_bar = (p1 + p2) / 2
    numerator = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
                 z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2
    n = numerator / denominator

    n_int = math.ceil(n)
    # significance yolundaki nadir-olay korumasının simetriği: hesaplanan n'de
    # beklenen dönüşüm/dönüşmeme sayılarından biri 10'un altındaysa bu plan normal
    # yaklaşımın geçerli olmadığı bölgededir (tipik sebep: aşırı büyük MDE).
    expected = [n_int * p1, n_int * (1 - p1), n_int * p2, n_int * (1 - p2)]
    approx_valid = min(expected) >= 10
    result = {
        "baseline_rate": baseline_rate,
        "target_rate": round(p2, 5),
        "mde_relative_pct": round(mde * 100, 2),
        "confidence_level": confidence,
        "power": power,
        "required_n_per_variant": n_int,
        "required_n_total": n_int * 2,
        "normal_approx_valid": approx_valid,
        "note": None,
    }
    if not approx_valid:
        result["note"] = (
            "Uyarı: bu örneklem boyutunda beklenen dönüşüm/dönüşmeme sayılarından en az biri "
            f"10'un altında (en küçüğü {min(expected):.1f}) — hesap normal yaklaşımın geçerli "
            "olmadığı bölgede. Genelde sebep aşırı büyük bir MDE'dir; bu sayıyı test planı "
            "olarak kullanmayın, MDE'yi gerçekçi bir değere indirin."
        )
    return result


def format_text(command, r):
    """İnsan okunur özet — bağımsız CLI kullanımı için (--format text)."""
    if command == "significance":
        lines = [
            f"Kontrol: %{r['control_rate'] * 100:.2f} → Varyant: %{r['variant_rate'] * 100:.2f}",
            f"Fark: {r['absolute_diff'] * 100:+.2f} yüzde puan"
            + (f" (göreli %{r['relative_lift_pct']:+.1f})" if r["relative_lift_pct"] is not None else ""),
            f"z = {r['z_score']}, p = {r['p_value']} → "
            + ("anlamlı" if r["is_significant"] else "anlamlı değil")
            + f" (güven düzeyi %{r['confidence_level'] * 100:.0f})"
            + ("" if r["normal_approx_valid"] else "  [GEÇERSİZ — nadir olay, aşağıya bakın]"),
            f"Farkın güven aralığı: [{r['confidence_interval_diff'][0] * 100:.2f}, "
            f"{r['confidence_interval_diff'][1] * 100:.2f}] yüzde puan",
        ]
        if r["note"]:
            lines.append(f"Uyarı: {r['note']}")
        return "\n".join(lines)
    if command == "srm":
        lines = [
            f"Gözlenen bölüşüm: %{r['observed_split'] * 100:.2f} (beklenen %{r['expected_split'] * 100:.0f})",
            f"chi2 = {r['chi2']}, p = {r['p_value']} → "
            + ("SRM TESPİT EDİLDİ — sonuçlar güvenilmez" if r["srm_detected"] else "SRM yok")
            + ("" if r["normal_approx_valid"] else "  [yaklaşım zayıf, aşağıya bakın]"),
        ]
        if r["note"]:
            lines.append(f"Uyarı: {r['note']}")
        return "\n".join(lines)
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
    )


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
                "anlamlılığını ayrıca 'significance' komutuyla kontrol edin.",
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


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p1 = sub.add_parser("significance", help="İki varyantın sonucunu karşılaştır")
    p1.add_argument("--control-visitors", type=int, required=True)
    p1.add_argument("--control-conversions", type=int, required=True)
    p1.add_argument("--variant-visitors", type=int, required=True)
    p1.add_argument("--variant-conversions", type=int, required=True)
    p1.add_argument("--confidence", type=float, default=0.95)
    p1.add_argument("--format", choices=["json", "text"], default="json")

    p3 = sub.add_parser("revenue", help="Gelir/kâr karşılaştırması (fiyat, indirim, paket testleri)")
    p3.add_argument("--control-visitors", type=int, required=True)
    p3.add_argument("--control-conversions", type=int, required=True)
    p3.add_argument("--control-aov", type=float, required=True, help="Kontrolde ortalama sipariş tutarı")
    p3.add_argument("--variant-visitors", type=int, required=True)
    p3.add_argument("--variant-conversions", type=int, required=True)
    p3.add_argument("--variant-aov", type=float, required=True, help="Varyantta ortalama sipariş tutarı")
    p3.add_argument("--margin-rate", type=float, default=None, help="Kontrol kolunun brüt marj oranı, ör. 0.35")
    p3.add_argument("--variant-margin-rate", type=float, default=None,
                    help="Varyantın brüt marj oranı farklıysa (fiyat/indirim testi); verilmezse kontrolünkiyle aynı varsayılır")
    p3.add_argument("--format", choices=["json", "text"], default="json")

    p4 = sub.add_parser("srm", help="Örneklem oranı uyuşmazlığı (SRM) kontrolü — randomizasyonu denetler, sonucu değil")
    p4.add_argument("--control-visitors", type=int, required=True)
    p4.add_argument("--variant-visitors", type=int, required=True)
    p4.add_argument("--expected-split", type=float, default=0.5, help="Kontrol koluna planlanan pay, ör. 0.5")
    p4.add_argument("--format", choices=["json", "text"], default="json")

    p2 = sub.add_parser("samplesize", help="Gereken örneklem büyüklüğünü hesapla")
    p2.add_argument("--baseline-rate", type=float, required=True, help="Ör. 0.05 (%5 dönüşüm)")
    p2.add_argument("--mde", type=float, required=True, help="Göreli minimum tespit edilebilir fark, ör. 0.20")
    p2.add_argument("--confidence", type=float, default=0.95)
    p2.add_argument("--power", type=float, default=0.80)
    p2.add_argument("--format", choices=["json", "text"], default="json")

    args = parser.parse_args()

    try:
        if args.command == "significance":
            result = significance(args.control_visitors, args.control_conversions,
                                   args.variant_visitors, args.variant_conversions, args.confidence)
        elif args.command == "revenue":
            result = revenue(args.control_visitors, args.control_conversions, args.control_aov,
                             args.variant_visitors, args.variant_conversions, args.variant_aov,
                             args.margin_rate, args.variant_margin_rate)
        elif args.command == "srm":
            result = srm(args.control_visitors, args.variant_visitors, args.expected_split)
        else:
            result = sample_size(args.baseline_rate, args.mde, args.confidence, args.power)
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    if args.format == "text":
        print(format_text(args.command, result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
