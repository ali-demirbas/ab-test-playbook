#!/usr/bin/env python3
"""Senaryo arşivinin biçim denetimi.

knowledge/scenarios/*.md içindeki her senaryonun playbook kurallarına uyduğunu
doğrular. Yeni senaryo eklerken veya mevcut bir senaryoyu düzenlerken çalıştırın:

    python3 scripts/validate_scenarios.py

Denetlenen kurallar (CLAUDE.md ve knowledge/methodology.md'den):
  1. Üç kutu eksiksiz: Test edilmesi gerekenler / Takip edilecek ana KPI'lar /
     Yapılmaması gerekenler.
  2. Her kutu tam 5 madde.
  3. KPI listesinde en az bir guardrail ("…memeli/…mamalı" kalıbı).
  4. Test listesinde en az bir cihaz/segment kırılımı sorusu.
  5. Test maddeleri `Etiket: soru?` biçiminde.
  6. Senaryo başlığı soru işaretiyle biter.
  7. Düz tırnak kullanılmaz (kıvrık tırnak zorunlu).

SINIR: Bu araç bir BİÇİM denetçisidir, anlam denetçisi değildir. Etiketi anlamlı
görünen ama içeriği boş maddeler, birbirinin sonuna tek kelime eklenmiş
kopyala-yapıştır maddeler veya "mobil" kelimesinin alakasız bağlamda geçmesiyle
sağlanan segment koşulu regex ile yakalanamaz. İçerik kalitesinin son denetimi
insan okumasıdır; bu araç yalnızca kaba biçim hatalarını erken yakalar.

Sadece Python standart kütüphanesi kullanır. Çıkış kodu: hata varsa 1.
"""
import os
import re
import sys

SCENARIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge", "scenarios")

BOXES = ("Test edilmesi gerekenler", "Takip edilecek ana KPI’lar", "Yapılmaması gerekenler")
ITEMS_PER_BOX = 5
# Guardrail = "bozulmaması gereken" bir metrik. Yalnızca "…melidir" eki yetmez:
# "Müşteri memnun kalmalıdır" bir hedeftir, guardrail değil. Olumsuzlama şart.
GUARDRAIL_PATTERN = r"\w+(?:memeli|mamalı)|(?:düşme|bozulma|artma|uzama|kaybetme|çıkma|inme)meli"
SEGMENT_PATTERN = r"[Cc]ihaz|[Mm]obil|[Ss]egment|masaüstü|[Kk]ullanıcı tipi|[Pp]latform|[Kk]ategori"
MIN_ITEM_CHARS = 25  # tek kelimelik doldurma maddelerini ele


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


def check_scenario(filename, title, body):
    errors = []
    where = f"{filename} → {title[:50]}"

    if not title.rstrip().endswith("?"):
        errors.append(f"{where}: başlık soru işaretiyle bitmiyor")

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

    kpis = box_items(body, "Takip edilecek ana KPI’lar")
    if kpis and not re.search(GUARDRAIL_PATTERN, "\n".join(kpis)):
        errors.append(
            f"{where}: KPI listesinde guardrail yok — bir metriğin 'bozulmaması gerektiği' "
            f"olumsuz kalıpla yazılmalı (…memeli/…mamalı); '…melidir' biten bir hedef cümlesi guardrail değildir"
        )

    tests = box_items(body, "Test edilmesi gerekenler")
    if tests:
        if not re.search(SEGMENT_PATTERN, "\n".join(tests)):
            errors.append(f"{where}: test listesinde cihaz/segment kırılımı sorusu yok")
        for item in tests:
            # 'Etiket: soru?' — etiket boş olmayacak, sorunun ardından örnek listesi gelebilir
            # ("Kaç rozet optimum? (1 / 3 / 5)"), o yüzden soru işareti sonda olmak zorunda değil.
            if not re.match(r"^- [^:\n]{2,}:\s*\S[^?]*\?", item):
                errors.append(f"{where}: test maddesi 'Etiket: soru?' biçiminde değil → {item[:45]}")

    return errors


def main():
    if not os.path.isdir(SCENARIO_DIR):
        print(f"HATA: senaryo dizini bulunamadı: {SCENARIO_DIR}")
        return 1

    all_errors = []
    total = 0
    per_file = {}

    for name in sorted(os.listdir(SCENARIO_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(SCENARIO_DIR, name)
        with open(path, encoding="utf-8") as f:
            text = f.read()

        if '"' in text:
            lines = [str(i) for i, l in enumerate(text.split("\n"), 1) if '"' in l]
            all_errors.append(f"{name}: düz tırnak kullanılmış (satır {', '.join(lines[:5])})")

        scenarios = parse_scenarios(text)
        per_file[name] = len(scenarios)
        total += len(scenarios)
        if not scenarios:
            # "## " başlığı hiç yoksa (ör. yanlışlıkla "### " kullanılmış) dosya
            # sessizce denetim dışı kalır; bunu temiz saymak yanlış güven üretir.
            all_errors.append(f"{name}: dosyada hiç senaryo bulunamadı ('## ' başlığı yok)")
        for title, body in scenarios:
            # Aynı kutu başlığı bir senaryoda iki kez geçerse yalnızca ilki
            # denetlenir; ikincisi çöp olsa da geçer. Mükerrer başlığı hata say.
            for header in BOXES:
                if body.count(f"**{header}**") > 1:
                    all_errors.append(f"{name} → {title[:50]}: '{header}' kutusu birden fazla kez tanımlı")
            all_errors.extend(check_scenario(name, title, body))

    print("Senaryo sayısı:")
    for name, count in per_file.items():
        print(f"  {name}: {count}")
    print(f"  TOPLAM: {total}")
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
