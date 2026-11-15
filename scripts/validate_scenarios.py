#!/usr/bin/env python3
"""Senaryo arşivinin biçim denetimi.

knowledge/scenarios/*.md içindeki her senaryonun playbook kurallarına uyduğunu
doğrular. Yeni senaryo eklerken veya mevcut bir senaryoyu düzenlerken çalıştırın:

    python3 scripts/validate_scenarios.py            # hatalar + uyarılar
    python3 scripts/validate_scenarios.py --verbose  # sözlükte olmayan birincil KPI’ları da listeler
    python3 scripts/validate_scenarios.py taslak.md  # arşiv yerine verilen dosya(lar)ı denetler

Denetlenen kurallar (CLAUDE.md ve knowledge/methodology.md'den):
  1. Üç kutu eksiksiz: Test edilmesi gerekenler / Takip edilecek ana KPI'lar /
     Yapılmaması gerekenler.
  2. Her kutu 3 ile 6 madde (üretilen kaydın detay görünümüyle aynı aralık); test
     kutusunda en çok bir “Sonraki test:” maddesi.
  3. KPI listesinde en az bir guardrail ("…memeli/…mamalı" kalıbı).
  4. Test listesinde en az bir cihaz/segment kırılımı sorusu.
  5. Test maddeleri `Etiket: soru?` biçiminde.
  6. Senaryo başlığı soru işaretiyle biter.
  7. Düz tırnak kullanılmaz (kıvrık tırnak zorunlu).
  8. Başlığın hemen altında tek bir `Değişken: … · Fark: …` satırı; Fark yalnızca
     değiştir / ekle / taşı / kaldır; değişken boş değil ve en çok 80 karakter.
  9. Birincil (ilk) KPI guardrail kalıbıyla yazılmaz: birincil metrik bir hedeftir
     (“… artıyor mu?”), “bozulmamalı” cümlesi guardrail maddesine aittir.
 10. Yapılmaması gerekenler: arşiv genelinde birebir tekrar eden madde yok; genel
     test hijyeni kalıpları (“Test sırasında … değiştirmeyin”, “sık sık
     değiştirmeyin”, “Sadece … bakıp … atlamayın” …) yasak, onlar methodology →
     Test hygiene’de bir kez yazılı.
 11. Başka bir senaryoya “Başlık?” senaryosu biçiminde verilen atıf, iç içe
     tırnaklar normalleştirildikten sonra var olan bir `## ` başlığına çözülür.
 12. Kutuları neredeyse aynı olan iki senaryo (kelime kümesi Jaccard benzerliği
     eşiğin üstünde) ancak birinde diğerine “… senaryosundan farkı” atfı varsa
     geçer.
 13. Birincil KPI bir sayı (“Sayısı”) değildir ve paydası “gören/görüp” demez
     (“yalnız B” etiketli tanı satırı hariç; methodology → KPI rules).
 14. Gecikmeli bir birincil KPI ya da guardrail (iade, iptal, churn, durdurma,
     tekrar satın alma, hesap silme, geri ödeme) takip penceresini adında taşır:
     “İade Oranı (30 gün)”, “7. Gün Elde Tutma”.
 15. knowledge/kpi-glossary.md varsa: birincil KPI sözlükte kanonik addır
     (Türkçe kanonik ad, varsa İngilizce adı, kısaltmasız biçimi de olur).
 16. Değişken satırının altında `Etiket: id=… · mercek=… · düzey=… · sektör=… ·
     pazar=… · emek=… · durum=… · tarih=YYYY-AA` satırı: anahtarlar bu sırada,
     değerler izinli listeden; id arşivde benzersiz (knowledge/scenarios/FORMAT.md).
 17. Etiket satırının altında `EN: <English title>?` ve `EN-Variable: …` satırları;
     İngilizce başlık arşivde benzersiz, ikisi de Türkçeye özgü harf taşımaz.
 18. Her blokta `### EN` sonrası İngilizce gövde (zorunlu): giriş paragrafı,
     Türkçe kutularla aynı sayıda maddeli What to test / KPIs to track / What not
     to do kutuları, sözlüğün English name sütunundan birincil KPI, “must not”
     guardrail, çevrilmiş notlar, İngilizce başlıkla çözülen atıflar; İngilizce
     gövdede Türkçeye özgü harf (ğ ş ı İ) yok.
 19. Senaryo metninde iç kural numarası (“kural 6”, “rule 11”) yok; kuralın kendisi
     yazılır.
 20. Birincil KPI’ın sözlükteki paydası kollar arasında değişemez; sözlük satırı
     guardrail için atanan paydalı bir karşılık adlandırıyorsa (Teklif → Sözleşme →
     Sözleşme Oranı (30 gün)) guardrail o karşılıkla yazılır.
 21. Blokta uzun tire (—) yok; yerine virgül, noktalı virgül ya da ayrı cümle.
 FORMAT.md gibi büyük harfli dosyalar senaryo içermez ve denetlenmez;
 `--next-id <dosya>` sıradaki boş kimliği basar.

Uyarılar (çıkış kodunu etkilemez; sonda “Uyarı sayısı: N” satırı basılır):
  - Değişken ifadesi “ ve ” veya “/” içeriyor: iki değişken olabilir.
  - Birincil dışındaki bir KPI “Sayısı” içeriyor (kollar farklı büyüklükteyse
    sayı karşılaştırılamaz) veya paydası “gören/görüp” diyor (payda yalnızca
    B’de var olabilir); yalnızca ada bakılır, “… başına” yazan sayı, sözlükte
    kanonik adı olan satır ve “yalnız B” etiketli tanı satırı uyarı almaz.
  - Guardrail kalıbına uyan satırların hiçbiri bir metrik adlandırmıyor
    (“Kampanya Katılımı: performansı çökmemeli”).
  - Birincil dışındaki bir KPI adı sözlükte eş anlamlı (kanonik ad yazılır).
  - Guardrail, birincil KPI’ın tümleyeni: birincil bir tamamlama/dönüşüm/kayıt
    oranı, guardrail adımı yazılmamış “Terk Oranı” ya da “Sayfa Terk Oranı”.
  - Yapılmaması gerekenler kutusunda değişken yalıtımı maddesi yok (“Aynı
    testte …”, “… aynı anda …”, “… birlikte … değiştirmeyin”, “tek değişken”).
  - Başlığı ve Değişken ifadesi neredeyse aynı olan iki senaryo (dosyalar arası
    da), biri diğerine “… senaryosundan farkı” atfı vermiyorsa.
  - “Sonraki test:” maddesi kazananın yerini soruyor (“yeri”, “konumu”): her öğeye
    yapıştırılabilen bir kalıp, senaryonun kazanan varyantı üstüne kurulmuyor.
  - knowledge/kpi-glossary.md varsa: birincil KPI’ların kaçının sözlükte kanonik
    adla yazıldığı da basılır (“217/217”); kanonik olmayanlar kural 15'in
    hatalarıdır, --verbose ile liste.

SINIR: Bu araç bir BİÇİM denetçisidir, anlam denetçisi değildir. Etiketi anlamlı
görünen ama içeriği boş maddeler, birbirinin sonuna tek kelime eklenmiş
kopyala-yapıştır maddeler veya "mobil" kelimesinin alakasız bağlamda geçmesiyle
sağlanan segment koşulu regex ile yakalanamaz. Bir test maddesinin senaryonun
değişkeni yerine başka bir değişkeni sorup sormadığı da regex işi değildir
(agents/scenario-critic.md bunu denetler). İçerik kalitesinin son denetimi
insan okumasıdır; bu araç yalnızca kaba biçim hatalarını erken yakalar.

Sadece Python standart kütüphanesi kullanır. Çıkış kodu: hata varsa 1.
"""
import argparse
import itertools
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCENARIO_DIR = os.path.join(ROOT, "knowledge", "scenarios")
GLOSSARY_PATH = os.path.join(ROOT, "knowledge", "kpi-glossary.md")

BOXES = ("Test edilmesi gerekenler", "Takip edilecek ana KPI’lar", "Yapılmaması gerekenler")
KPI_BOX, TEST_BOX, NEVER_BOX = BOXES[1], BOXES[0], BOXES[2]
# Kutu başına madde aralığı: üretilen kaydın detay görünümüyle aynı (3 ile 6).
MIN_ITEMS, MAX_ITEMS = 3, 6
NEXT_TEST_LABEL = "- Sonraki test:"
# Kazananın yerini ayrı testte sormak her öğeye yapıştırılabilen bir kalıptır;
# “Sonraki test” bu senaryonun kazanan varyantı üstüne kurulur.
GENERIC_NEXT_TEST = re.compile(r"\b(?:yeri|konumu|yerleşimi)\b", re.IGNORECASE)
# Senaryo metninde iç kural numarası (kural 6, rule 11) kullanıcıya dönük metne
# sızar; kuralın kendisi yazılır.
EM_DASH = "\u2014"
RULE_NUMBER = re.compile(r"\b(?:kural(?:ı|a|da|ın)?|rule)\s+\d+", re.IGNORECASE)
# Guardrail = "bozulmaması gereken" bir metrik. Yalnızca "…melidir" eki yetmez:
# "Müşteri memnun kalmalıdır" bir hedeftir, guardrail değil. Olumsuzlama şart.
GUARDRAIL_PATTERN = r"\w+(?:memeli|mamalı)|(?:düşme|bozulma|artma|uzama|kaybetme|çıkma|inme)meli"
SEGMENT_PATTERN = r"[Cc]ihaz|[Mm]obil|[Ss]egment|masaüstü|[Kk]ullanıcı tipi|[Pp]latform|[Kk]ategori"
MIN_ITEM_CHARS = 25  # tek kelimelik doldurma maddelerini ele

# Değişken satırı: "Değişken: <tek değişken> · Fark: <değiştir|ekle|taşı|kaldır>"
VARIABLE_PREFIX = "Değişken:"
VARIABLE_LINE = re.compile(r"^Değişken:\s*(?P<var>.*?)\s*·\s*Fark:\s*(?P<fark>.*?)\s*$")
FARK_VALUES = ("değiştir", "ekle", "taşı", "kaldır")
MAX_VARIABLE_CHARS = 80
# " ve " veya "/" iki ayrı değişkenin tek satıra sıkıştırıldığını düşündürür.
# Kesin değildir ("fiyat ve kargo bilgisini taşıyan blok" tek öğe olabilir),
# o yüzden hata değil uyarı.
TWO_VARIABLE_HINT = re.compile(r"\sve\s|/")

# Payda uyarıları: "Sayısı" kollar farklı büyüklükteyse karşılaştırılamaz;
# "gören/görüp" paydanın yalnızca yeni öğeyi gören B kolunda var olduğunu ima eder.
COUNT_HINT = re.compile(r"sayısı", re.IGNORECASE)
SAW_HINT = re.compile(r"\bgör(?:en|üp)", re.IGNORECASE)
PER_HINT = re.compile(r"başına", re.IGNORECASE)
# Yalnızca B kolunda var olan bir tanı satırı kollar arasında karşılaştırılmaz;
# öyle etiketlendiyse payda uyarısı anlamsızdır.
B_ONLY_HINT = re.compile(r"yalnız(?:ca)?\s+B\b|sadece\s+B\b")

# Gecikmeli metrik (iade, iptal, churn, durdurma, tekrar satın alma, silme,
# geri ödeme): test bittikten sonra olur, takip penceresi adın parçasıdır
# (“İade Oranı (30 gün)”; methodology → KPI rules, kpi-glossary.md → İade ve iptal).
LAGGING_HINT = re.compile(
    r"(?<!\w)(?:iade|iptal|churn|durdur|tekrar\s+satın|yeniden\s+satın|ikinci\s+sipariş|hesab?\w*\s+sil|geri\s+ödeme"
    r"|abonelik(?:ten)?\s+(?:çık|ayrıl|bırak)|elde\s+tut|refund|return|cancel|retention|repeat\s+purchase"
    r"|chargeback|account\s+delet)\w*", re.IGNORECASE)
WINDOW_HINT = re.compile(
    r"\([^()]*(?:\d|gün|hafta|\bay\b|aylık|yıl|süre|pencere|dönem|window|day|week|month|year)[^()]*\)"
    r"|(?<!\w)\d+\.?[\s-]*(?:gün|hafta|ay|yıl|day|week|month|year)\w*(?!\w)|(?<!\w)D\d+(?!\w)",
    re.IGNORECASE)

# Guardrail satırı bir metriği adlandırır: “Kampanya Katılımı: performansı
# çökmemeli” gibi bir cümle kalıba uysa da ölçülebilir bir metrik değildir.
METRIC_HINT = re.compile(
    r"oran|süre|gelir|marj|maliyet|tutar|değer|bedel|puan|skor|hız|sayı|talep|taleb|şikâyet|şikayet|hata|ağırlı|boyut"
    r"|\(anket\)|\b(?:LCP|INP|CLS|TTFB|CR|AOV|RPV|ARPU|NPS|CSAT|CTR)\b|rate|time|revenue|margin|cost|score",
    re.IGNORECASE)


def primary_problems(primary):
    """Birincil KPI satırının hataları (methodology → KPI rules): sayı ya da
    “gören/görüp” paydası. “yalnız B” etiketli satır tanıdır, karşılaştırılmaz."""
    out = []
    if B_ONLY_HINT.search(primary):
        return out
    label = kpi_label(primary)
    if COUNT_HINT.search(label) and not PER_HINT.search(label):
        out.append(f"birincil KPI bir sayı (“Sayısı”); kollar farklı büyüklükteyse karşılaştırılamaz, "
                   f"atanan ziyaretçi başına orana çevirin → {label}")
    if SAW_HINT.search(primary):
        out.append(f"birincil KPI paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda "
                   f"karşılaştırılamaz (methodology → KPI denominator) → {primary[2:70]}")
    return out


def is_guardrail_line(item):
    return bool(re.search(GUARDRAIL_PATTERN, item))


def kpi_window_problems(kpis):
    """Pencere adında yazılmamış gecikmeli birincil ya da guardrail adları (hata)."""
    out = []
    for i, item in enumerate(kpis):
        if i and not is_guardrail_line(item):
            continue
        label = kpi_label(item)
        if LAGGING_HINT.search(label) and not WINDOW_HINT.search(label):
            role = "birincil KPI" if i == 0 else "guardrail"
            out.append(f"{role} gecikmeli bir metrik ama takip penceresi adında yok; adın sonuna yazın "
                       f"(“İade Oranı (30 gün)”, kpi-glossary.md → İade ve iptal) → {label}")
    return out


def guardrail_metric_warnings(kpis, glossary=None):
    """Guardrail kalıbına uyan satırların hiçbiri bir metrik adlandırmıyorsa uyarı."""
    lines = [item for item in kpis[1:] if is_guardrail_line(item)]
    if not lines:
        return []
    for item in lines:
        label = kpi_label(item)
        if METRIC_HINT.search(label) or (glossary is not None and glossary_status(label, glossary) != "missing"):
            return []
    return ["guardrail satırları bir metrik adlandırmıyor (oran, süre, gelir, şikâyet …); “…memeli/…mamalı” "
            "kalıbı tek başına guardrail değildir, ölçülen metriği ve paydasını yazın → "
            + "; ".join(kpi_label(item) for item in lines)]


def primary_glossary_problems(primary, glossary):
    """Birincil KPI sözlükteki kanonik adla yazılır (methodology → KPI rules)."""
    label = kpi_label(primary)
    status = glossary_status(label, glossary)
    if status == "canonical":
        return []
    if status.startswith("synonym:"):
        return [f"birincil KPI sözlükte eş anlamlı; kanonik adı yazın → {label} → {status.split(':', 1)[1]}"]
    return [f"birincil KPI sözlükte yok; kpi-glossary.md’deki kanonik adı yazın ya da metriği sözlüğe "
            f"paydasıyla ekleyin → {label}"]


# Paydası kollar arasında değişen metrik (sözlükte “(kollar arasında değişebilir)”)
# birincil olmaz; sözlük satırı guardrail için atanan paydalı bir karşılık
# adlandırıyorsa guardrail o karşılıkla yazılır (methodology → KPI denominator).
VARYING_DENOMINATOR = re.compile(r"kollar arasında değiş", re.IGNORECASE)
GUARDRAIL_EQUIVALENT = re.compile(r"guardrail için atanan paydalı (?:bir )?(?:karşılığı|eşdeğeri) (?P<eq>.+?) seçilir")


def glossary_row(label, glossary):
    """Bir KPI adının sözlük satırı (kanonik ad, kısaltmasız biçim ya da eş anlamlı); yoksa None."""
    rows = getattr(glossary, "rows", None) or {}
    for c in (label, bare_label(label)):
        if c in rows:
            return c
        bare = [n for n in rows if bare_label(n) == c]
        if len(bare) == 1:
            return bare[0]
    status = glossary_status(label, glossary)
    return status.split(":", 1)[1] if status.startswith("synonym:") else None


def conditioned_kpi_problems(kpis, glossary):
    """Birincil KPI’ın paydası kollar arasında değişemez; adlandırılmış atanan paydalı
    karşılığı olan metrik guardrail olarak yazılmaz (sözlük satırı)."""
    out = []
    rows = getattr(glossary, "rows", None) or {}
    for i, item in enumerate(kpis):
        name = glossary_row(kpi_label(item), glossary)
        if name is None or name not in rows:
            continue
        row = rows[name]
        if i == 0 and VARYING_DENOMINATOR.search(row["payda"]):
            out.append(f"birincil KPI’ın paydası kollar arasında değişebilir (sözlük: {row['payda']}); birincil "
                       f"atanan ziyaretçi paydalı bir oran olur → {kpi_label(item)}")
        m = GUARDRAIL_EQUIVALENT.search(row["definition"])
        if i and m and is_guardrail_line(item):
            out.append(f"guardrail koşullu paydalı bir metrikle yazılmış; sözlükteki atanan paydalı karşılığını "
                       f"yazın → {kpi_label(item)} → {m.group('eq')}")
    return out


def glossary_name_warnings(kpis, glossary):
    """Sözlükte eş anlamlı olan bir KPI adı: arşiv kanonik adı yazar."""
    out = []
    for item in kpis:
        label = kpi_label(item)
        status = glossary_status(label, glossary)
        if status.startswith("synonym:"):
            out.append(f"KPI adı sözlükte eş anlamlı; arşiv kanonik adı yazar → {label} → "
                       f"{status.split(':', 1)[1]}")
    return out

# Tümleyen guardrail: birincil bir tamamlama/dönüşüm/kayıt oranıyken adımı
# yazılmamış terk oranı (sözlükteki “Terk Oranı” ve “Sayfa Terk Oranı”) aynı
# metriğin 1 − hâlidir. Sonraki adımın terki (“Ödeme Adımı Terk Oranı”) geçerli
# bir guardrail'dir ve bu kalıba girmez.
COMPLETE_HINT = re.compile(r"tamamlama|dönüşüm|kayıt", re.IGNORECASE)
GENERIC_ABANDON = re.compile(r"^(?:sayfa(?:yı)?\s+)?terk\s+oranı$", re.IGNORECASE)

# Değişken yalıtımı maddesi: senaryonun kendi değişkeninin yanında neyin
# değişmeyeceğini söyler (kural 4). Her senaryoda en az bir tane beklenir.
ISOLATION_HINT = re.compile(
    r"aynı testte|aynı anda|birlikte\s+(?:\S+\s+){0,8}?değiştirmeyin|tek değişken", re.IGNORECASE)

# Her senaryonun Yapılmaması gerekenler kutusu kendi varyantına özgüdür; genel
# test hijyeni methodology.md → Test hygiene'de bir kez yazılıdır. Bu kalıplar
# o genel kuralın senaryoya kopyalandığını gösterir.
BANNED_NEVER_DO = (
    (re.compile(r"^test (?:sırasında|süresince|boyunca)\b", re.IGNORECASE),
     "“Test sırasında/süresince …” genel dondurma kuralıdır"),
    (re.compile(r"\bsık sık değiştirmeyin", re.IGNORECASE),
     "“sık sık değiştirmeyin” genel hijyen kuralıdır"),
    (re.compile(r"\börneklem (?:dolmadan|tamamlanmadan)", re.IGNORECASE),
     "“örneklem dolmadan” genel istatistik hijyenidir"),
    (re.compile(r"\berken (?:kapatmayın|durdurmayın|sonlandırmayın|bitirmeyin)", re.IGNORECASE),
     "“erken kapatmayın” genel istatistik hijyenidir"),
    (re.compile(r"^(?:sadece|yalnızca)\s.+\sbakıp\s.+\satlamayın", re.IGNORECASE),
     "“Sadece … bakıp … atlamayın” genel sonuç okuma hijyenidir"),
)

# Başka bir senaryoya atıf: “Başlık?” senaryosu / senaryosundan / senaryolarından …
# Kapanış tırnağıyla "senaryo" arasında isteğe bağlı bir dosya adı olabilir:
# “Başlık?” (`mobile-app.md`) senaryosundan farkı …
CROSS_REF_TAIL = re.compile(r"”\s*(?:\(`?[\w.\-]+\.md`?\)\s*)?senaryo\w*")
QUOTE_CHARS = re.compile(r"[“”‘’'\"]")

# Kutuları neredeyse aynı iki senaryo: kelime kümesi Jaccard benzerliği.
NEAR_DUP_THRESHOLD = 0.28
# Başlık + Değişken ifadesi: iki senaryo aynı soruyu aynı değişkenle soruyorsa
# kutuları farklı yazılmış olsa da aynı testtir. Başlıklar kısa olduğu için eşik
# kutu benzerliğininkinden yüksektir.
TITLE_DUP_THRESHOLD = 0.5
NEAR_DUP_STOPWORDS = frozenset(
    "ve veya ile için bir bu şu daha çok en ne değil olarak gibi kadar ama hem iki "
    "aynı testte artıyor artırıyor azalıyor düşüyor oranı mı mi mu mü var yok her".split()
)


def parse_scenarios(text):
    """Dosyayı senaryolara böl; (başlık, gövde) çiftleri döndür.

    Baştaki "\n" eki: dosya doğrudan "## " ile başlıyorsa ilk senaryonun
    sessizce yutulmasını önler (split deseni "\n## " beklediği için)."""
    blocks = re.split(r"\n## ", "\n" + text)[1:]
    return [(b.split("\n")[0].strip(), b) for b in blocks]


def box_items(body, header):
    # (?:\n|$); dosyanın son satırında newline olmasa da son maddeyi yakala.
    m = re.search(r"\*\*" + re.escape(header) + r"\*\*\n((?:- .*(?:\n|$))+)", body)
    if not m:
        return None
    return [line for line in m.group(1).strip().split("\n") if line.startswith("- ")]


def kpi_label(item):
    """'- Dönüşüm Oranı (CR): açıklama' → 'Dönüşüm Oranı (CR)'."""
    return item[2:].split(":", 1)[0].strip()


def parse_variable_line(body):
    """Gövdedeki Değişken satırını çöz.

    Dönüş: (değişken, fark, hatalar). Satır yoksa veya bozuksa değişken/fark
    None olur ve hata listesi nedeni söyler."""
    lines = body.split("\n")[1:]  # ilk satır başlık
    var_lines = [l for l in lines if l.startswith(VARIABLE_PREFIX)]
    if not var_lines:
        return None, None, ["‘Değişken: … · Fark: …’ satırı yok (başlığın hemen altında olmalı)"]
    errors = []
    if len(var_lines) > 1:
        errors.append(f"{len(var_lines)} adet Değişken satırı var (tam bir tane olmalı)")
    first_content = next((l for l in lines if l.strip()), "")
    if not first_content.startswith(VARIABLE_PREFIX):
        errors.append("Değişken satırı başlığın hemen altında değil (başlık, boş satır, Değişken satırı)")
    m = VARIABLE_LINE.match(var_lines[0].strip())
    if not m:
        errors.append(f"Değişken satırı ‘Değişken: … · Fark: …’ biçiminde değil → {var_lines[0][:60]}")
        return None, None, errors
    var, fark = m.group("var"), m.group("fark")
    if not var:
        errors.append("Değişken boş")
    elif len(var) > MAX_VARIABLE_CHARS:
        errors.append(f"Değişken {len(var)} karakter (en çok {MAX_VARIABLE_CHARS}): kısa bir ad öbeği yazın")
    if fark not in FARK_VALUES:
        errors.append(f"Fark ‘{fark}’ geçersiz (yalnızca: {' / '.join(FARK_VALUES)})")
    return var, fark, errors


# --- Etiket ve İngilizce satırları (knowledge/scenarios/FORMAT.md) -------------
#
# Başlık bloğu sabit sıradadır, her satır kendi paragrafıdır:
#   Değişken: … · Fark: …
#   Etiket: id=cc-001 · mercek=… · düzey=… · sektör=… · pazar=… · emek=… · durum=… · tarih=YYYY-MM
#   EN: <English title>
#   EN-Variable: <English variable>
# İngilizce gövde (zorunlu) bloğun sonunda “### EN” satırından sonra gelir (FORMAT.md).

TAG_PREFIX = "Etiket:"
EN_TITLE_PREFIX = "EN:"
EN_VARIABLE_PREFIX = "EN-Variable:"
EN_BODY_MARKER = "### EN"
TAG_KEYS = ("id", "mercek", "düzey", "sektör", "pazar", "emek", "durum", "tarih")
# Öğe düzeyi: sayfadaki bir öğenin görünüşü, yeri, metni ya da bilgisi. Yapı düzeyi:
# teklifin, fiyatın, akışın, kişiye göre içeriğin ya da yaşam döngüsünün kendisi.
ELEMENT_LEVELS = ("görsel", "gezinme", "bilgi", "form", "metin", "güven", "sosyal-kanıt", "sürtünme")
STRUCTURAL_LEVELS = ("teklif", "fiyat", "kişiselleştirme", "akış", "elde-tutma", "onboarding")
TAG_VALUES = {
    "mercek": ("Güven", "Fiyat", "Uygunluk", "Zamanlama", "Çaba", "Netlik"),
    "düzey": ELEMENT_LEVELS + STRUCTURAL_LEVELS,
    "sektör": ("genel", "e-ticaret", "moda", "saas", "b2b", "finans", "ilan"),
    "pazar": ("TR", "global"),
    "emek": ("düşük", "orta", "yüksek"),
    "durum": ("güncel", "klasik"),
}
MAX_SECTORS = 2
# Kimliğin öneki bloğun ilk yazıldığı dosyayı söyler; blok başka dosyaya taşınsa da
# kimlik değişmez (geçmiş ve backlog dosyaları kimlikle eşleşir).
ID_PREFIXES = {
    "cart-checkout.md": "cc", "category-listing.md": "cl", "dashboard.md": "db",
    "finance-pension.md": "fp", "forms-signup.md": "fs", "home-landing.md": "hl",
    "mobile-app.md": "ma", "pricing.md": "pr", "product-detail.md": "pd",
    "saas-b2b.md": "sb", "search-filtering.md": "sf", "thank-you.md": "ty",
    "ui-elements.md": "ui",
}
ID_RE = re.compile(r"^(?P<prefix>[a-z]{2})-(?P<num>\d{3})$")
DATE_RE = re.compile(r"^20\d\d-(?:0[1-9]|1[0-2])$")
# İngilizce başlıkta yalnız Türkçeye özgü harf: çevrilmemiş başlık işareti.
TURKISH_ONLY = re.compile(r"[ğĞşŞıİ]")
EN_BOXES = ("What to test", "KPIs to track", "What not to do")
EN_GUARDRAIL = re.compile(r"\b(?:must not|should not|must never|mustn’t|shouldn’t)\b", re.IGNORECASE)
EN_SEGMENT = re.compile(r"[Dd]evice|[Mm]obile|[Ss]egment|[Dd]esktop|[Uu]ser type|[Pp]latform|[Cc]ategor|"
                        r"[Nn]ew and returning|[Rr]eturning")
EN_CROSS_REF_TAIL = re.compile(r"”\s*(?:\(`?[\w.\-]+\.md`?\)\s*)?scenario\w*")
NOTE_PAIRS = (("Pazar notu", "Market note"), ("Ölçüm notu", "Measurement note"),
              ("Güncellik notu", "Freshness note"))
# Güncellik notu: “> **Güncellik notu (2026-11):** …” (methodology → When the archive goes stale).
FRESHNESS_NOTE = re.compile(r"^> \*\*Güncellik notu \((?P<date>[^)]*)\):\*\* \S")
FRESHNESS_NOTE_EN = re.compile(r"^> \*\*Freshness note \((?P<date>[^)]*)\):\*\* \S")


def head_lines(body):
    """Başlıktan sonra, ilk paragrafa kadar gelen dolu satırlar (Değişken, Etiket, EN …)."""
    out = []
    for line in body.split("\n")[1:]:
        s = line.strip()
        if not s:
            continue
        if s.startswith((VARIABLE_PREFIX, TAG_PREFIX, EN_TITLE_PREFIX, EN_VARIABLE_PREFIX)):
            out.append(s)
            continue
        break
    return out


def parse_tag_line(line):
    """'Etiket: id=… · mercek=… …' → ({anahtar: değer}, hatalar)."""
    errors = []
    rest = line[len(TAG_PREFIX):].strip()
    pairs = [p.strip() for p in rest.split("·")]
    tags, keys = {}, []
    for p in pairs:
        if "=" not in p:
            errors.append(f"Etiket satırında ‘anahtar=değer’ olmayan parça → {p[:30]}")
            continue
        k, v = (x.strip() for x in p.split("=", 1))
        keys.append(k)
        tags[k] = v
    if keys != list(TAG_KEYS) and not errors:
        errors.append(f"Etiket anahtarları bu sırada olmalı: {' · '.join(TAG_KEYS)} (bulunan: {' · '.join(keys)})")
    for k in TAG_KEYS:
        v = tags.get(k)
        if not v:
            if k in tags or not errors:
                errors.append(f"Etiket ‘{k}’ boş ya da yok")
            continue
        if k == "id":
            m = ID_RE.match(v)
            if not m or m.group("prefix") not in ID_PREFIXES.values():
                errors.append(f"Etiket id ‘{v}’ geçersiz (biçim: <önek>-<üç hane>, önek: "
                              f"{', '.join(sorted(set(ID_PREFIXES.values())))})")
        elif k == "tarih":
            if not DATE_RE.match(v):
                errors.append(f"Etiket tarih ‘{v}’ geçersiz (YYYY-AA, ör. 2026-11)")
        elif k == "sektör":
            values = [s.strip() for s in v.split(",")]
            bad = [s for s in values if s not in TAG_VALUES[k]]
            if bad:
                errors.append(f"Etiket sektör ‘{', '.join(bad)}’ geçersiz (yalnızca: {' / '.join(TAG_VALUES[k])})")
            if len(values) > MAX_SECTORS or len(set(values)) != len(values):
                errors.append(f"Etiket sektör en çok {MAX_SECTORS} farklı değer alır → {v}")
        elif v not in TAG_VALUES[k]:
            errors.append(f"Etiket {k} ‘{v}’ geçersiz (yalnızca: {' / '.join(TAG_VALUES[k])})")
    return tags, errors


def split_en_body(body):
    """(Türkçe bölüm, İngilizce gövde ya da None): '### EN' satırı bloğu ikiye böler."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if line.strip() == EN_BODY_MARKER:
            return "\n".join(lines[:i]), "\n".join(lines[i + 1:])
    return body, None


def check_metadata(filename, title, body, glossary=None):
    """Etiket satırı, İngilizce başlık ve varsa İngilizce gövde (FORMAT.md).

    Dönüş: (tags, en_title, hatalar). Arşiv geneli denetimler (benzersiz id ve
    İngilizce başlık) find_metadata_duplicates içindedir."""
    errors = []
    where = f"{filename} → {title[:50]}"
    head = head_lines(body)
    tags, en_title = {}, None
    if len(head) < 2 or not head[1].startswith(TAG_PREFIX):
        errors.append(f"{where}: Değişken satırının altında ‘Etiket: id=… · mercek=… …’ satırı yok (FORMAT.md)")
    else:
        tags, tag_errors = parse_tag_line(head[1])
        errors.extend(f"{where}: {e}" for e in tag_errors)
    if len(head) < 3 or not head[2].startswith(EN_TITLE_PREFIX):
        errors.append(f"{where}: Etiket satırının altında ‘EN: <English title>’ satırı yok (FORMAT.md)")
    else:
        en_title = head[2][len(EN_TITLE_PREFIX):].strip()
        if not en_title:
            errors.append(f"{where}: EN başlığı boş")
        elif not en_title.endswith("?"):
            errors.append(f"{where}: EN başlığı soru işaretiyle bitmiyor → {en_title[:50]}")
        elif TURKISH_ONLY.search(en_title):
            errors.append(f"{where}: EN başlığında Türkçe harf var, çevrilmemiş olabilir → {en_title[:50]}")
    en_variable = None
    extra = head[3:]
    if extra and extra[0].startswith(EN_VARIABLE_PREFIX):
        en_variable = extra[0][len(EN_VARIABLE_PREFIX):].strip()
        if not en_variable:
            errors.append(f"{where}: EN-Variable boş")
        elif len(en_variable) > MAX_VARIABLE_CHARS:
            errors.append(f"{where}: EN-Variable {len(en_variable)} karakter (en çok {MAX_VARIABLE_CHARS})")
        elif TURKISH_ONLY.search(en_variable):
            errors.append(f"{where}: EN-Variable içinde Türkçe harf var, çevrilmemiş olabilir → {en_variable[:50]}")
        extra = extra[1:]
    for line in extra:
        errors.append(f"{where}: başlık bloğunda fazla ya da sırası bozuk satır (sıra: Değişken, Etiket, EN, "
                      f"EN-Variable) → {line[:50]}")

    tr_part, en_body = split_en_body(body)
    for line in body.split("\n"):
        if line.startswith("> **Güncellik notu") and not FRESHNESS_NOTE.match(line):
            errors.append(f"{where}: güncellik notu ‘> **Güncellik notu (YYYY-AA):** …’ biçiminde değil")
        m = FRESHNESS_NOTE.match(line)
        if m and not DATE_RE.match(m.group("date")):
            errors.append(f"{where}: güncellik notunun tarihi ‘{m.group('date')}’ geçersiz (YYYY-AA)")
    if en_body is None:
        errors.append(f"{where}: İngilizce gövde yok; her blok, Türkçe gövdeden sonra yalnız ‘### EN’ yazan bir "
                      f"satır ve onun altında giriş paragrafı, What to test / KPIs to track / What not to do "
                      f"kutuları ve notlarla Türkçenin paralel çevirisini taşır"
                      + ("" if en_variable is not None else "; başlık bloğuna ‘EN-Variable: …’ satırı da eklenir")
                      + " (FORMAT.md → English)")
    else:
        errors.extend(f"{where}: {e}" for e in en_body_problems(tr_part, en_body, en_variable, glossary))
    return tags, en_title, errors


def en_body_problems(tr_part, en_body, en_variable, glossary=None):
    """İngilizce gövde, Türkçe kutuların paralel çevirisidir (FORMAT.md)."""
    out = []
    if en_variable is None:
        out.append("İngilizce gövde var ama başlık bloğunda ‘EN-Variable: …’ satırı yok")
    leftovers = [line.strip() for line in en_body.split("\n") if TURKISH_ONLY.search(line)]
    if leftovers:
        out.append(f"İngilizce gövdede Türkçe harf var, çevrilmemiş metin olabilir ({len(leftovers)} satır) → "
                   f"{leftovers[0][:60]}")
    paras = [p for p in en_body.split("\n\n") if p.strip()]
    if not paras or paras[0].lstrip().startswith(("**", "- ", ">")):
        out.append("İngilizce gövde bir giriş paragrafıyla başlamıyor (Türkçe girişin çevirisi)")
    for tr_header, en_header in zip(BOXES, EN_BOXES):
        tr_items = box_items(tr_part, tr_header) or []
        en_items = box_items(en_body, en_header)
        if en_items is None:
            out.append(f"İngilizce gövdede ‘**{en_header}**’ kutusu yok")
            continue
        if len(en_items) != len(tr_items):
            out.append(f"‘{en_header}’ {len(en_items)} madde, Türkçe karşılığı {len(tr_items)} madde (paralel çeviri)")
        if en_header == EN_BOXES[0]:
            for item in en_items:
                if not re.match(r"^- [^:\n]{2,}:\s*\S[^?]*\?", item):
                    out.append(f"İngilizce test maddesi ‘Label: question?’ biçiminde değil → {item[:45]}")
            if en_items and not EN_SEGMENT.search("\n".join(en_items)):
                out.append("İngilizce test listesinde cihaz/segment kırılımı sorusu yok")
        if en_header == EN_BOXES[1] and en_items:
            if not EN_GUARDRAIL.search("\n".join(en_items[1:])):
                out.append("İngilizce KPI listesinde guardrail yok (“… must not …”)")
            if EN_GUARDRAIL.search(en_items[0]):
                out.append("İngilizce birincil KPI guardrail gibi yazılmış (“must not”)")
            if glossary is not None:
                label = kpi_label(en_items[0])
                english = getattr(glossary, "english", {})
                if not any(c in english for c in (label, bare_label(label))) and \
                        not any(bare_label(n) == bare_label(label) for n in english):
                    out.append(f"İngilizce birincil KPI sözlüğün ‘English name’ sütununda yok → {label}")
    for tr_note, en_note in NOTE_PAIRS:
        if f"**{tr_note}" in tr_part and f"**{en_note}" not in en_body:
            out.append(f"Türkçe bölümde ‘{tr_note}’ var, İngilizce gövdede ‘{en_note}’ yok")
    return out


def find_metadata_duplicates(meta):
    """meta: [(dosya, başlık, tags, en_title)]. Tekrar eden id ve İngilizce başlık."""
    out = []
    for key, label in (("id", "id"), ("en", "EN başlığı")):
        seen = {}
        for name, title, tags, en_title in meta:
            value = tags.get("id") if key == "id" else (en_title.casefold() if en_title else None)
            if value:
                seen.setdefault(value, []).append(f"{name} → {title[:40]}")
        out.extend(f"{label} birden fazla senaryoda aynı: “{value}” ({'; '.join(places)})"
                   for value, places in seen.items() if len(places) > 1)
    return out


def next_free_id(filename, meta):
    """Bir dosya için sıradaki boş kimlik (ör. cc-023)."""
    prefix = ID_PREFIXES[os.path.basename(filename)]
    used = [int(m.group("num")) for _, _, tags, _ in meta
            for m in [ID_RE.match(tags.get("id", ""))] if m and m.group("prefix") == prefix]
    return f"{prefix}-{(max(used) if used else 0) + 1:03d}"


def find_unresolved_en_cross_refs(meta, en_bodies):
    """İngilizce gövdedeki “English title” scenario atıfları var olan bir EN başlığına çözülür."""
    known = {normalize_title(en) for _, _, _, en in meta if en}
    problems = []
    for where, text in en_bodies:
        for m in EN_CROSS_REF_TAIL.finditer(text):
            start = _quoted_before(text, m.start())
            if start is None:
                continue
            quoted = text[start + 1: m.start()]
            if normalize_title(quoted) not in known:
                problems.append(f"{where}: İngilizce atıf yapılan senaryo başlığı bulunamadı → “{quoted[:70]}”")
    return problems


def unclosed_blocks(parsed):
    """Titles of blocks (all but a file's last) that don't end with a `---` line.

    The skills read one block from its title line to the next `---`; a missing
    separator makes that read run into the neighbouring scenario, which the
    `## ` split above would never notice."""
    out = []
    for title, body in parsed[:-1]:
        lines = [l.strip() for l in body.rstrip().split("\n") if l.strip()]
        if not lines or lines[-1] != "---":
            out.append(title)
    return out


def check_scenario(filename, title, body, glossary=None):
    """Biçim hataları. glossary verilirse (kpi-glossary.md) birincil KPI'ın
    sözlükte kanonik ad olması da denetlenir."""
    errors = []
    where = f"{filename} → {title[:50]}"

    if not title.rstrip().endswith("?"):
        errors.append(f"{where}: başlık soru işaretiyle bitmiyor")

    _, _, var_errors = parse_variable_line(body)
    errors.extend(f"{where}: {e}" for e in var_errors)

    for header in BOXES:
        items = box_items(body, header)
        if items is None:
            errors.append(f"{where}: '{header}' kutusu yok veya madde listesi bulunamadı")
            continue
        if not MIN_ITEMS <= len(items) <= MAX_ITEMS:
            errors.append(f"{where}: '{header}' {len(items)} madde ({MIN_ITEMS} ile {MAX_ITEMS} arası olmalı)")
        if header == TEST_BOX and sum(1 for i in items if i.startswith(NEXT_TEST_LABEL)) > 1:
            errors.append(f"{where}: test kutusunda birden fazla ‘Sonraki test:’ maddesi var (en çok bir)")
        # Doldurma maddesi denetimi: tekrar eden veya çok kısa madde.
        bodies = [i[2:].strip() for i in items]
        if len(set(bodies)) != len(bodies):
            errors.append(f"{where}: '{header}' kutusunda birebir tekrar eden madde var")
        for b in bodies:
            if len(b) < MIN_ITEM_CHARS:
                errors.append(f"{where}: '{header}' maddesi doldurma gibi (çok kısa) → {b[:40]}")

    kpis = box_items(body, KPI_BOX)
    if kpis and not re.search(GUARDRAIL_PATTERN, "\n".join(kpis)):
        errors.append(
            f"{where}: KPI listesinde guardrail yok; bir metriğin 'bozulmaması gerektiği' "
            f"olumsuz kalıpla yazılmalı (…memeli/…mamalı); '…melidir' biten bir hedef cümlesi guardrail değildir"
        )
    if kpis and re.search(GUARDRAIL_PATTERN, kpis[0]):
        errors.append(
            f"{where}: birincil KPI guardrail gibi yazılmış (“…memeli/…mamalı”); birincil metrik "
            f"bir hedeftir (“… artıyor mu?”), bozulmama cümlesini bir guardrail maddesine taşıyın → {kpis[0][:60]}"
        )

    if kpis:
        errors.extend(f"{where}: {e}" for e in primary_problems(kpis[0]))
        errors.extend(f"{where}: {e}" for e in kpi_window_problems(kpis))
        if glossary is not None:
            errors.extend(f"{where}: {e}" for e in primary_glossary_problems(kpis[0], glossary))
            errors.extend(f"{where}: {e}" for e in conditioned_kpi_problems(kpis, glossary))

    tests = box_items(body, TEST_BOX)
    if tests:
        if not re.search(SEGMENT_PATTERN, "\n".join(tests)):
            errors.append(f"{where}: test listesinde cihaz/segment kırılımı sorusu yok")
        for item in tests:
            # 'Etiket: soru?'; etiket boş olmayacak, sorunun ardından örnek listesi gelebilir
            # ("Kaç rozet optimum? (1 / 3 / 5)"), o yüzden soru işareti sonda olmak zorunda değil.
            if not re.match(r"^- [^:\n]{2,}:\s*\S[^?]*\?", item):
                errors.append(f"{where}: test maddesi 'Etiket: soru?' biçiminde değil → {item[:45]}")

    dashes = sum(1 for line in body.split("\n") if EM_DASH in line)
    if dashes:
        errors.append(f"{where}: {dashes} satırda uzun tire (—) var; virgül, noktalı virgül ya da ayrı cümle yazın")

    hits = sorted({m.group(0) for m in RULE_NUMBER.finditer(body)})
    if hits:
        errors.append(f"{where}: senaryo metninde iç kural numarası var ({', '.join(hits)}); kullanıcıya dönük "
                      f"metinde kural numarası değil kuralın kendisi yazılır")

    for item in box_items(body, NEVER_BOX) or []:
        text = item[2:].strip()
        for pattern, why in BANNED_NEVER_DO:
            if pattern.search(text):
                errors.append(
                    f"{where}: Yapılmaması gerekenler maddesi genel kural ({why}; "
                    f"methodology → Test hygiene), varyanta özgü yazın → {text[:50]}"
                )

    return errors


def bare_label(label):
    """Sondaki tek parantez niteleyicisi olmadan ad: 'Terk Oranı (CR)' → 'Terk Oranı'."""
    return re.sub(r"\s*\([^()]*\)$", "", label).strip()


def check_warnings(filename, title, body, glossary=None):
    """Hata olmayan ama bakılması gereken durumlar.

    glossary verilirse (kpi-glossary.md), sözlükte adı olan ikincil satırlar
    sayı uyarısı almaz: o satır paydasını sözlükten devralır."""
    warnings = []
    where = f"{filename} → {title[:50]}"
    var, _, _ = parse_variable_line(body)
    if var and TWO_VARIABLE_HINT.search(var):
        warnings.append(f"{where}: değişken iki değişken gibi görünüyor (“ ve ” / “/”) → {var}")
    kpis = box_items(body, KPI_BOX)
    if kpis:
        primary = kpis[0]
        for item in kpis[1:]:
            label = kpi_label(item)
            if B_ONLY_HINT.search(item):
                continue
            # Birincil dışındaki satırlarda yalnızca ada bakılır: soru metni
            # “süreci görüp vazgeçme” gibi paydayla ilgisiz ifadeler taşır.
            in_glossary = glossary is not None and glossary_status(label, glossary) != "missing"
            if COUNT_HINT.search(label) and not PER_HINT.search(label) and not in_glossary:
                warnings.append(
                    f"{where}: KPI bir sayı (“Sayısı”); kollar farklı büyüklükteyse karşılaştırılamaz, "
                    f"atanan ziyaretçi başına orana çevirin ya da sözlüğe paydasıyla ekleyin → {label}"
                )
            if SAW_HINT.search(label):
                warnings.append(
                    f"{where}: KPI paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda "
                    f"karşılaştırılamaz (methodology → KPI denominator) → {label}"
                )
        if COMPLETE_HINT.search(kpi_label(primary)):
            for item in kpis[1:]:
                if GENERIC_ABANDON.match(bare_label(kpi_label(item))) and re.search(GUARDRAIL_PATTERN, item):
                    warnings.append(
                        f"{where}: guardrail birincil KPI’ın tümleyeni gibi görünüyor (aynı adımın terki, "
                        f"1 − birincil); bağımsız bir zarar ölçün: sonraki adım, kalite, maliyet → {kpi_label(item)}"
                    )
    if kpis:
        # Uyarı, hata değil: ikincil satırlarda sözlük dışı ad serbesttir (paydası yazılıysa) ve
        # metrik adı denetimi bir sezgidir.
        warnings.extend(f"{where}: {w}" for w in guardrail_metric_warnings(kpis, glossary))
        if glossary is not None:
            warnings.extend(f"{where}: {w}" for w in glossary_name_warnings(kpis[1:], glossary))
    for item in box_items(body, TEST_BOX) or []:
        if item.startswith(NEXT_TEST_LABEL) and GENERIC_NEXT_TEST.search(item):
            warnings.append(f"{where}: ‘Sonraki test’ kazananın yerini soruyor; bu her öğeye yapıştırılabilen bir "
                            f"kalıptır, bu senaryonun kazanan varyantı üstüne kurulan bir soru yazın ya da maddeyi "
                            f"çıkarın → {item[2:70]}")
    nevers = box_items(body, NEVER_BOX)
    if nevers and not any(ISOLATION_HINT.search(item) for item in nevers):
        warnings.append(
            f"{where}: Yapılmaması gerekenler kutusunda değişken yalıtımı maddesi yok "
            f"(“Aynı testte … değiştirmeyin” ailesi; kural 4)"
        )
    return warnings


# --- Arşiv geneli denetimler -------------------------------------------------

def normalize_title(title):
    """İç içe tırnak farkını (‘’ / “” / düz) ve boşlukları yok say."""
    return re.sub(r"\s+", " ", QUOTE_CHARS.sub("'", title)).strip().casefold()


def _quoted_before(text, close_idx):
    """text[close_idx] == '”' ise eşleşen açılış tırnağının indeksini döndür.

    İç içe “…” tırnaklarını sayarak geriye yürür: “A, “B” C?” tek başlıktır."""
    depth = 0
    for i in range(close_idx, -1, -1):
        ch = text[i]
        if ch == "”":
            depth += 1
        elif ch == "“":
            depth -= 1
            if depth == 0:
                return i
    return None


def extract_cross_refs(text):
    """Metindeki “Başlık” senaryo… atıflarını bul.

    Dönüş: [(alıntılanan başlık, satır no, satırda 'fark' geçiyor mu)].
    “A” ve “B” senaryolarından biçimindeki çoklu atıf da çözülür."""
    refs = []
    for m in CROSS_REF_TAIL.finditer(text):
        close = m.start()
        line_start = text.rfind("\n", 0, close) + 1
        line_end = text.find("\n", close)
        line = text[line_start: line_end if line_end != -1 else len(text)]
        line_no = text.count("\n", 0, close) + 1
        has_fark = "fark" in line.casefold()
        while True:
            start = _quoted_before(text, close)
            if start is None or start < line_start:
                break
            refs.append((text[start + 1: close], line_no, has_fark))
            # “A” ve “B” / “A”, “B” → bir önceki alıntıya da bak.
            prev = re.search(r"”\s*(?:ve|,)\s*$", text[line_start:start])
            if not prev:
                break
            close = line_start + prev.start()
    return refs


def find_unresolved_cross_refs(file_texts, titles):
    """Var olmayan bir başlığa yapılan atıfları döndür."""
    known = {normalize_title(t) for t in titles}
    problems = []
    for name, text in file_texts:
        for quoted, line_no, _ in extract_cross_refs(text):
            if normalize_title(quoted) not in known:
                problems.append(
                    f"{name}:{line_no}: atıf yapılan senaryo başlığı bulunamadı → “{quoted[:70]}”"
                )
    return problems


def find_duplicate_never_do(scenarios):
    """scenarios: [(dosya, başlık, gövde)]. Arşiv genelinde birebir aynı
    Yapılmaması gerekenler maddelerini döndür."""
    seen = {}
    for name, title, body in scenarios:
        for item in box_items(body, NEVER_BOX) or []:
            seen.setdefault(item[2:].strip(), []).append(f"{name} → {title[:40]}")
    return [
        f"Yapılmaması gerekenler maddesi {len(places)} senaryoda birebir aynı, varyanta özgü yazın: "
        f"“{text[:60]}” ({'; '.join(places)})"
        for text, places in seen.items() if len(places) > 1
    ]


def box_tokens(body):
    words = []
    for header in BOXES:
        for item in box_items(body, header) or []:
            words.extend(re.findall(r"\w+", item[2:].casefold()))
    return {w for w in words if len(w) > 2 and w not in NEAR_DUP_STOPWORDS}


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


def find_near_duplicates(scenarios, threshold=NEAR_DUP_THRESHOLD):
    """Kutuları eşiğin üstünde benzeyen senaryo çiftleri.

    Dönüş: (hatalar, bilgiler). Çiftten biri diğerine “… senaryosundan farkı”
    atfı veriyorsa çift bilinçli bir kardeş senaryodur (bilgi); vermiyorsa hata."""
    prepared = []
    for name, title, body in scenarios:
        refs = {normalize_title(q) for q, _, has_fark in extract_cross_refs(body) if has_fark}
        prepared.append((name, title, box_tokens(body), refs))
    errors, infos = [], []
    for (n1, t1, k1, r1), (n2, t2, k2, r2) in itertools.combinations(prepared, 2):
        score = jaccard(k1, k2)
        if score < threshold:
            continue
        pair = f"{n1} → {t1[:40]} ⟷ {n2} → {t2[:40]} (benzerlik {score:.2f})"
        if normalize_title(t2) in r1 or normalize_title(t1) in r2:
            infos.append(pair)
        else:
            errors.append(
                f"neredeyse aynı kutular, ama ikisi de diğerine “… senaryosundan farkı” atfı vermiyor: {pair}"
            )
    return errors, infos


def title_tokens(title, variable):
    words = re.findall(r"\w+", f"{title} {variable or ''}".casefold())
    return {w for w in words if len(w) > 2 and w not in NEAR_DUP_STOPWORDS}


def find_title_variable_duplicates(scenarios, threshold=TITLE_DUP_THRESHOLD):
    """Başlığı ve Değişken ifadesi neredeyse aynı olan senaryo çiftleri
    (dosyalar arası da).

    Dönüş: (uyarılar, bilgiler). Kutu benzerliği denetimi (find_near_duplicates)
    aynı testi farklı kelimelerle yazılmış kutularda kaçırır; bu denetim soruya
    ve değişkene bakar. Çiftten biri diğerine “… senaryosundan farkı” atfı
    veriyorsa bilinçli bir kardeş senaryodur (bilgi)."""
    prepared = []
    for name, title, body in scenarios:
        var, _, _ = parse_variable_line(body)
        refs = {normalize_title(q) for q, _, has_fark in extract_cross_refs(body) if has_fark}
        prepared.append((name, title, title_tokens(title, var), refs))
    warnings, infos = [], []
    for (n1, t1, k1, r1), (n2, t2, k2, r2) in itertools.combinations(prepared, 2):
        score = jaccard(k1, k2)
        if score < threshold:
            continue
        pair = f"{n1} → {t1[:50]} ⟷ {n2} → {t2[:50]} (benzerlik {score:.2f})"
        if normalize_title(t2) in r1 or normalize_title(t1) in r2:
            infos.append(pair)
        else:
            warnings.append(
                f"başlık ve Değişken neredeyse aynı, ama ikisi de diğerine “… senaryosundan farkı” atfı vermiyor: {pair}"
            )
    return warnings, infos


# --- KPI sözlüğü --------------------------------------------------------------

class Glossary(dict):
    """{kanonik ad: [eş anlamlılar]}; `english` = {İngilizce ad: kanonik ad};
    `rows` = parse_glossary_rows çıktısı (tanım ve payda).

    İngilizce ad bir eş anlamlı değil, kaydın İngilizce kanonik adıdır:
    glossary_status onu 'canonical' sayar."""

    def __init__(self, *args, **kwargs):
        super(Glossary, self).__init__(*args, **kwargs)
        self.english = {}
        self.rows = {}


# Sözlük tablolarının sütunları başlık satırından okunur; başka bir sütun
# (ör. İngilizce kanonik ad) eklendiğinde eş anlamlılar yanlış sütundan okunmaz.
_COL_RES = (
    ("english", re.compile(r"ingilizce|english|^en(?:\s|$)|\(en\)", re.IGNORECASE)),
    ("synonyms", re.compile(r"eş\s*anlam|synonym", re.IGNORECASE)),
    ("payda", re.compile(r"payda|denominator", re.IGNORECASE)),
    ("definition", re.compile(r"tanım|definition", re.IGNORECASE)),
    ("turkish", re.compile(r"kanonik|canonical|türkçe|turkish", re.IGNORECASE)),
)
_LEGACY_COLUMNS = {"definition": 1, "payda": 2, "synonyms": 3}


def _header_columns(cells):
    """Bir tablo başlık satırının {rol: sütun no} haritası; başlık değilse None."""
    if any(c.startswith("**") for c in cells):
        return None
    cols = {}
    for i, cell in enumerate(cells):
        for role, regex in _COL_RES:
            if role not in cols and regex.search(cell):
                cols[role] = i
                break
    return cols if ("synonyms" in cols or "payda" in cols or "english" in cols) else None


def _split_names(cell):
    return [s.strip().strip("*").strip() for s in cell.split(";") if s.strip() and s.strip() not in ("-", "\u2014", "\u2013")]


def parse_glossary_rows(text):
    """kpi-glossary.md tablolarının her satırı:
    {kanonik ad: {"definition", "payda", "synonyms", "english"}}.

    Satır biçimi: | **Kanonik Ad** | Tanım | Payda | eş1; eş2 |. Sütunlar her
    tablonun başlık satırından bulunur (Tanım/Payda/eş anlamlılar, varsa
    İngilizce ad); başlıksız tabloda eski sıra geçerlidir. İlk sütunu
    İngilizce ad olan bir tablo (ayrı bir İngilizce bölüm), Türkçe kanonik
    adı gösteren bir sütunu varsa o satırın İngilizce adını ekler."""
    rows = {}
    english_only = []  # (İngilizce ad, Türkçe kanonik ad) ayrı bölümden
    cols = None
    for line in text.split("\n"):
        if not line.startswith("|"):
            cols = None  # a table ends at its first non-table line
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        header = _header_columns(cells)
        if header is not None:
            cols = header
            continue
        if not cells or not cells[0].startswith("**"):
            continue
        use = cols or _LEGACY_COLUMNS
        name = cells[0].strip("*").strip()

        def cell(role):
            i = use.get(role)
            return cells[i] if i is not None and i < len(cells) else ""

        if use.get("english") == 0 and use.get("turkish") not in (None, 0):
            english_only.append((name, cell("turkish").strip("*").strip()))
            continue
        if cols is None and len(cells) < 4:
            continue
        rows[name] = {"definition": cell("definition"), "payda": cell("payda"),
                      "synonyms": _split_names(cell("synonyms")), "english": _split_names(cell("english"))}
    for en, tr in english_only:
        if tr in rows and en not in rows[tr]["english"]:
            rows[tr]["english"].append(en)
    return rows


def parse_glossary(text):
    """kpi-glossary.md tablolarından {kanonik ad: [eş anlamlılar]} çıkar
    (Glossary; İngilizce kanonik adlar `english` içinde, satırların tamamı `rows`)."""
    glossary = Glossary()
    glossary.rows = parse_glossary_rows(text)
    for name, row in glossary.rows.items():
        glossary[name] = row["synonyms"]
        for en in row["english"]:
            glossary.english.setdefault(en, name)
    return glossary


def load_glossary(path=GLOSSARY_PATH):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return parse_glossary(f.read())


def glossary_status(label, glossary):
    """'canonical' | 'synonym:<kanonik>' | 'missing'.

    Sondaki tek bir parantez niteleyicisi yok sayılır:
    'Nitelikli Fırsat Oranı (atanan ziyaretçi başına)' → 'Nitelikli Fırsat Oranı'."""
    candidates = [label, re.sub(r"\s*\([^()]*\)$", "", label)]
    english = getattr(glossary, "english", {})
    for c in candidates:
        if c in glossary or c in english:
            return "canonical"
    # 'Dönüşüm Oranı' is 'Dönüşüm Oranı (CR)' without its abbreviation.
    for c in candidates:
        bare = [name for name in list(glossary) + list(english) if re.sub(r"\s*\([^()]*\)$", "", name) == c]
        if len(bare) == 1:
            return "canonical"
    for canon, syns in glossary.items():
        for c in candidates:
            if c in syns:
                return f"synonym:{canon}"
    return "missing"


def archive_files(directory=SCENARIO_DIR):
    """Aşama dosyaları: küçük harfli adlar (cart-checkout.md). FORMAT.md gibi büyük
    harfli belgeler senaryo içermez ve denetlenmez."""
    return [n for n in sorted(os.listdir(directory)) if re.match(r"^[a-z0-9-]+\.md$", n)]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Senaryo arşivinin biçim denetimi.")
    parser.add_argument("files", nargs="*",
                        help="arşiv yerine denetlenecek .md dosyaları (ör. kullanıcının yazdığı tek senaryo)")
    parser.add_argument("--verbose", action="store_true",
                        help="sözlükte kanonik adı olmayan birincil KPI’ları da listele")
    parser.add_argument("--next-id", metavar="DOSYA",
                        help="bu arşiv dosyası için sıradaki boş kimliği bas (ör. cart-checkout.md → cc-023)")
    args = parser.parse_args(argv)

    if args.next_id:
        name = os.path.basename(args.next_id)
        if name not in ID_PREFIXES:
            print(f"HATA: bilinen bir arşiv dosyası değil: {name} (ID_PREFIXES)")
            return 1
        meta = []
        for n in archive_files():
            with open(os.path.join(SCENARIO_DIR, n), encoding="utf-8") as f:
                for title, body in parse_scenarios(f.read()):
                    tags, en_title, _ = check_metadata(n, title, body)
                    meta.append((n, title, tags, en_title))
        print(next_free_id(name, meta))
        return 0

    if args.files:
        paths = list(args.files)
        missing_files = [p for p in paths if not os.path.isfile(p)]
        if missing_files:
            print(f"HATA: dosya bulunamadı: {', '.join(missing_files)}")
            return 1
    else:
        if not os.path.isdir(SCENARIO_DIR):
            print(f"HATA: senaryo dizini bulunamadı: {SCENARIO_DIR}")
            return 1
        paths = [os.path.join(SCENARIO_DIR, n) for n in archive_files()]

    all_errors, all_warnings = [], []
    total = 0
    per_file = {}
    file_texts, scenarios, meta, en_bodies = [], [], [], []
    glossary = load_glossary()

    for path in paths:
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        file_texts.append((name, text))

        if '"' in text:
            lines = [str(i) for i, l in enumerate(text.split("\n"), 1) if '"' in l]
            all_errors.append(f"{name}: düz tırnak kullanılmış (satır {', '.join(lines[:5])})")

        parsed = parse_scenarios(text)
        per_file[name] = len(parsed)
        total += len(parsed)
        if not parsed:
            # "## " başlığı hiç yoksa (ör. yanlışlıkla "### " kullanılmış) dosya
            # sessizce denetim dışı kalır; bunu temiz saymak yanlış güven üretir.
            all_errors.append(f"{name}: dosyada hiç senaryo bulunamadı ('## ' başlığı yok)")
        for title in unclosed_blocks(parsed):
            all_errors.append(f"{name} → {title[:50]}: blok '---' satırıyla kapanmıyor; arama bir sonraki senaryoyu da okur")
        for title, body in parsed:
            scenarios.append((name, title, body))
            # Aynı kutu başlığı bir senaryoda iki kez geçerse yalnızca ilki
            # denetlenir; ikincisi çöp olsa da geçer. Mükerrer başlığı hata say.
            for header in BOXES:
                if body.count(f"**{header}**") > 1:
                    all_errors.append(f"{name} → {title[:50]}: '{header}' kutusu birden fazla kez tanımlı")
            all_errors.extend(check_scenario(name, title, body, glossary=glossary))
            all_warnings.extend(check_warnings(name, title, body, glossary=glossary))
            tags, en_title, meta_errors = check_metadata(name, title, body, glossary=glossary)
            all_errors.extend(meta_errors)
            meta.append((name, title, tags, en_title))
            en_body = split_en_body(body)[1]
            if en_body is not None:
                en_bodies.append((f"{name} → {title[:50]}", en_body))

    all_errors.extend(find_metadata_duplicates(meta))
    all_errors.extend(find_unresolved_en_cross_refs(meta, en_bodies))
    all_errors.extend(find_duplicate_never_do(scenarios))
    all_errors.extend(find_unresolved_cross_refs(file_texts, [t for _, t, _ in scenarios]))
    dup_errors, dup_infos = find_near_duplicates(scenarios)
    all_errors.extend(dup_errors)
    title_warnings, title_infos = find_title_variable_duplicates(scenarios)
    all_warnings.extend(title_warnings)

    print("Senaryo sayısı:")
    for name, count in per_file.items():
        print(f"  {name}: {count}")
    print(f"  TOPLAM: {total}")
    print()

    if dup_infos:
        print(f"Benzer kutulu {len(dup_infos)} kardeş senaryo çifti (birbirine ‘farkı’ atfı veriyor):")
        for i in dup_infos:
            print(f"  - {i}")
        print()
    if title_infos:
        print(f"Başlığı ve değişkeni benzer {len(title_infos)} kardeş senaryo çifti (birbirine ‘farkı’ atfı veriyor):")
        for i in title_infos:
            print(f"  - {i}")
        print()

    if glossary is not None:
        # Kural 15'in özeti: hatalar sorun listesinde ayrıca yazılır; bu satır yalnızca sayar.
        missing, primaries = [], 0
        for name, title, body in scenarios:
            kpis = box_items(body, KPI_BOX)
            if not kpis:
                continue
            primaries += 1
            status = glossary_status(kpi_label(kpis[0]), glossary)
            if status != "canonical":
                hint = f" → kanonik ad: {status.split(':', 1)[1]}" if status.startswith("synonym:") else ""
                missing.append(f"{name} → {title[:40]}: {kpi_label(kpis[0])}{hint}")
        line = (f"KPI sözlüğü: {len(glossary)} kanonik ad; {primaries - len(missing)}/{primaries} birincil KPI "
                f"sözlükte kanonik adla yazılmış")
        if missing:
            line += (f"; {len(missing)} tanesi sözlükte yok ya da eş anlamlı (hata"
                     f"{'' if args.verbose else '; liste için --verbose'})")
        print(line + ".")
        if args.verbose:
            for m in missing:
                print(f"  - {m}")
        print()

    tagged = [tags for _, _, tags, _ in meta if tags.get("düzey") in TAG_VALUES["düzey"]]
    if tagged:
        structural = sum(1 for t in tagged if t["düzey"] in STRUCTURAL_LEVELS)
        classic = sum(1 for t in tagged if t.get("durum") == "klasik")
        en_full = len(en_bodies)
        print(f"Etiketler: {len(tagged)}/{total} senaryo; öğe düzeyi {len(tagged) - structural}, yapı düzeyi "
              f"{structural}; klasik {classic}; tam İngilizce gövde {en_full}.")
        print()

    if all_warnings:
        print(f"{len(all_warnings)} uyarı (çıkış kodunu etkilemez):")
        for w in all_warnings:
            print(f"  - {w}")
        print()
    print(f"Uyarı sayısı: {len(all_warnings)}")

    if all_errors:
        print(f"{len(all_errors)} sorun bulundu:")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("Tüm senaryolar biçim kurallarına uyuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
