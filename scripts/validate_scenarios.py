#!/usr/bin/env python3
"""Senaryo arşivinin biçim denetimi.

knowledge/scenarios/*.md içindeki her senaryonun playbook kurallarına uyduğunu
doğrular. Yeni senaryo eklerken veya mevcut bir senaryoyu düzenlerken çalıştırın:

    python3 scripts/validate_scenarios.py            # hatalar + uyarılar
    python3 scripts/validate_scenarios.py --verbose  # sözlükte olmayan birincil KPI’ları da listeler

Denetlenen kurallar (CLAUDE.md ve knowledge/methodology.md'den):
  1. Üç kutu eksiksiz: Test edilmesi gerekenler / Takip edilecek ana KPI'lar /
     Yapılmaması gerekenler.
  2. Her kutu tam 5 madde.
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
     değiştirmeyin” …) yasak, onlar methodology → Test hygiene’de bir kez yazılı.
 11. Başka bir senaryoya “Başlık?” senaryosu biçiminde verilen atıf, iç içe
     tırnaklar normalleştirildikten sonra var olan bir `## ` başlığına çözülür.
 12. Kutuları neredeyse aynı olan iki senaryo (kelime kümesi Jaccard benzerliği
     eşiğin üstünde) ancak birinde diğerine “… senaryosundan farkı” atfı varsa
     geçer.

Uyarılar (çıkış kodunu etkilemez):
  - Değişken ifadesi “ ve ” veya “/” içeriyor: iki değişken olabilir.
  - Birincil KPI “Sayısı” içeriyor (kollar farklı büyüklükteyse sayı
    karşılaştırılamaz) veya “gören/görüp” diyor (payda yalnızca B’de var olabilir).
  - knowledge/kpi-glossary.md varsa: sözlükte kanonik adı olmayan birincil KPI
    sayısı (--verbose ile liste).

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
ITEMS_PER_BOX = 5
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
)

# Başka bir senaryoya atıf: “Başlık?” senaryosu / senaryosundan / senaryolarından …
# Kapanış tırnağıyla "senaryo" arasında isteğe bağlı bir dosya adı olabilir:
# “Başlık?” (`mobile-app.md`) senaryosundan farkı …
CROSS_REF_TAIL = re.compile(r"”\s*(?:\(`?[\w.\-]+\.md`?\)\s*)?senaryo\w*")
QUOTE_CHARS = re.compile(r"[“”‘’'\"]")

# Kutuları neredeyse aynı iki senaryo: kelime kümesi Jaccard benzerliği.
NEAR_DUP_THRESHOLD = 0.28
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
    # (?:\n|$) — dosyanın son satırında newline olmasa da son maddeyi yakala.
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


def check_scenario(filename, title, body):
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
        if len(items) != ITEMS_PER_BOX:
            errors.append(f"{where}: '{header}' {len(items)} madde (beklenen {ITEMS_PER_BOX})")
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
            f"{where}: KPI listesinde guardrail yok — bir metriğin 'bozulmaması gerektiği' "
            f"olumsuz kalıpla yazılmalı (…memeli/…mamalı); '…melidir' biten bir hedef cümlesi guardrail değildir"
        )
    if kpis and re.search(GUARDRAIL_PATTERN, kpis[0]):
        errors.append(
            f"{where}: birincil KPI guardrail gibi yazılmış (“…memeli/…mamalı”); birincil metrik "
            f"bir hedeftir (“… artıyor mu?”), bozulmama cümlesini bir guardrail maddesine taşıyın → {kpis[0][:60]}"
        )

    tests = box_items(body, TEST_BOX)
    if tests:
        if not re.search(SEGMENT_PATTERN, "\n".join(tests)):
            errors.append(f"{where}: test listesinde cihaz/segment kırılımı sorusu yok")
        for item in tests:
            # 'Etiket: soru?' — etiket boş olmayacak, sorunun ardından örnek listesi gelebilir
            # ("Kaç rozet optimum? (1 / 3 / 5)"), o yüzden soru işareti sonda olmak zorunda değil.
            if not re.match(r"^- [^:\n]{2,}:\s*\S[^?]*\?", item):
                errors.append(f"{where}: test maddesi 'Etiket: soru?' biçiminde değil → {item[:45]}")

    for item in box_items(body, NEVER_BOX) or []:
        text = item[2:].strip()
        for pattern, why in BANNED_NEVER_DO:
            if pattern.search(text):
                errors.append(
                    f"{where}: Yapılmaması gerekenler maddesi genel kural ({why}; "
                    f"methodology → Test hygiene), varyanta özgü yazın → {text[:50]}"
                )

    return errors


def check_warnings(filename, title, body):
    """Hata olmayan ama bakılması gereken durumlar."""
    warnings = []
    where = f"{filename} → {title[:50]}"
    var, _, _ = parse_variable_line(body)
    if var and TWO_VARIABLE_HINT.search(var):
        warnings.append(f"{where}: değişken iki değişken gibi görünüyor (“ ve ” / “/”) → {var}")
    kpis = box_items(body, KPI_BOX)
    if kpis:
        primary = kpis[0]
        if COUNT_HINT.search(kpi_label(primary)):
            warnings.append(
                f"{where}: birincil KPI bir sayı (“Sayısı”); kollar farklı büyüklükteyse karşılaştırılamaz, "
                f"atanan ziyaretçi başına orana çevirin → {kpi_label(primary)}"
            )
        if SAW_HINT.search(primary):
            warnings.append(
                f"{where}: birincil KPI paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda "
                f"karşılaştırılamaz (methodology → KPI denominator) → {primary[2:70]}"
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


# --- KPI sözlüğü --------------------------------------------------------------

def parse_glossary(text):
    """kpi-glossary.md tablolarından {kanonik ad: [eş anlamlılar]} çıkar.

    Satır biçimi: | **Kanonik Ad** | Tanım | Payda | eş1; eş2 |"""
    glossary = {}
    for line in text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not cells[0].startswith("**"):
            continue
        name = cells[0].strip("*").strip()
        synonyms = [s.strip() for s in cells[3].split(";") if s.strip() and s.strip() != "-"]
        glossary[name] = synonyms
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
    for c in candidates:
        if c in glossary:
            return "canonical"
    for canon, syns in glossary.items():
        for c in candidates:
            if c in syns:
                return f"synonym:{canon}"
    return "missing"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Senaryo arşivinin biçim denetimi.")
    parser.add_argument("--verbose", action="store_true",
                        help="sözlükte kanonik adı olmayan birincil KPI’ları da listele")
    args = parser.parse_args(argv)

    if not os.path.isdir(SCENARIO_DIR):
        print(f"HATA: senaryo dizini bulunamadı: {SCENARIO_DIR}")
        return 1

    all_errors, all_warnings = [], []
    total = 0
    per_file = {}
    file_texts, scenarios = [], []

    for name in sorted(os.listdir(SCENARIO_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(SCENARIO_DIR, name)
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
        for title, body in parsed:
            scenarios.append((name, title, body))
            # Aynı kutu başlığı bir senaryoda iki kez geçerse yalnızca ilki
            # denetlenir; ikincisi çöp olsa da geçer. Mükerrer başlığı hata say.
            for header in BOXES:
                if body.count(f"**{header}**") > 1:
                    all_errors.append(f"{name} → {title[:50]}: '{header}' kutusu birden fazla kez tanımlı")
            all_errors.extend(check_scenario(name, title, body))
            all_warnings.extend(check_warnings(name, title, body))

    all_errors.extend(find_duplicate_never_do(scenarios))
    all_errors.extend(find_unresolved_cross_refs(file_texts, [t for _, t, _ in scenarios]))
    dup_errors, dup_infos = find_near_duplicates(scenarios)
    all_errors.extend(dup_errors)

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

    glossary = load_glossary()
    if glossary is not None:
        missing = []
        for name, title, body in scenarios:
            kpis = box_items(body, KPI_BOX)
            if not kpis:
                continue
            status = glossary_status(kpi_label(kpis[0]), glossary)
            if status != "canonical":
                hint = f" → kanonik ad: {status.split(':', 1)[1]}" if status.startswith("synonym:") else ""
                missing.append(f"{name} → {title[:40]}: {kpi_label(kpis[0])}{hint}")
        print(f"KPI sözlüğü: {len(glossary)} kanonik ad; {len(missing)}/{total} birincil KPI sözlükte kanonik ad olarak yok "
              f"(uyarı{'' if args.verbose or not missing else '; liste için --verbose'}).")
        if args.verbose:
            for m in missing:
                print(f"  - {m}")
        print()

    if all_warnings:
        print(f"{len(all_warnings)} uyarı (çıkış kodunu etkilemez):")
        for w in all_warnings:
            print(f"  - {w}")
        print()

    if all_errors:
        print(f"{len(all_errors)} sorun bulundu:")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print("Tüm senaryolar biçim kurallarına uyuyor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
