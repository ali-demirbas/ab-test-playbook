#!/usr/bin/env python3
"""Print a scenario record skeleton that the validator accepts once its hints are replaced.

Given the device, the difference type, the page or flow, the primary KPI (and the
language, the tested element and the score inputs), it writes everything the
validator decides from those facts the way the validator reads it: the glossary's
denominator for the KPI, the accessibility warning with every criterion an
interactive element needs (validate_scenario_json.a11y_example), the invariant,
the exposure sentence for an element shown conditionally (an accordion, tabs, or
--hidden below the first view), priority.inputs with the tier their score gives,
and a minimal card.screen with the one change op the difference type takes.

What only the author can know is a hint in ⟦…⟧ (the title, problem, mechanism,
variable, A and B, the notes, the rationale, the page copy on the card, the ring
labels, must_be_true). The validator refuses any string that still carries one,
so a skeleton is never mistaken for a record. Replace each hint with this page's
real value (never a ⟦ or ⟧ left), delete must_be_true if it doesn't apply, then:

  python3 scripts/validate_scenario_json.py <record.json>

Before printing, the skeleton is checked twice with validate_scenario_json.py:
with the hints in place every error must be a placeholder error, and with the
hints filled by sample text it must validate with no error and no warning. A
skeleton that fails either is a bug here and is not printed (exit 1).

Usage:
  new_record.py --device phone|phone-web|web --difference change|add|move|remove \\
                --page <stage, e.g. cart-checkout> --kpi "<glossary name>" [--lang tr|en]
                [--element cta|link|field|check|chips|tabs|accordion|text|help|badge|banner] [--hidden]
                [--evidence intuition|sector|archive|user_data|behaviour_data] [--adapted-from "<archive title>"]
                [--guardrail "<glossary name>"] [--impact structural|persuasive|cosmetic]
                [--effort low|medium|high] [--off-path] [--subtle] [--id <slug>] [--out <file>]

Exit: 0 = skeleton printed (or written to --out), 1 = the skeleton failed its own check, 2 = usage error
(an unknown KPI, a KPI that can't be a primary, an archive title not found, a difference the archive block
doesn't have). Python 3.9+, standard library only.
"""
import argparse
import copy
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_scenario_json as vsj  # noqa: E402

DEVICES = ("phone", "phone-web", "web")
DIFFERENCES = ("change", "add", "move", "remove")
ELEMENTS = ("cta", "link", "field", "check", "chips", "tabs", "accordion", "text", "help", "badge", "banner")
INTERACTIVE = ("cta", "link", "field", "check", "chips", "tabs", "accordion")
CONDITIONAL = ("tabs", "accordion")
EVIDENCE = {"intuition": ("intuition", "intuition"), "sector": ("sector", "archive_or_research"),
            "archive": ("archive", "archive_or_research"), "user_data": ("user_data", "user_data"),
            "behaviour_data": ("user_data", "behaviour_data")}
DIFFERENCE_TR = {"değiştir": "change", "ekle": "add", "taşı": "move", "kaldır": "remove"}
HARM_RE = re.compile(r"terk|çıkış|çıkma|hata|iade|iptal|şikâyet|şikayet|silme|kapatma|geri\s+alma|durdurma|dökülme"
                     r"|abandon|exit|error|return|refund|cancel|complaint|uninstall|opt-out|drop-off|bounce|stop",
                     re.IGNORECASE)

# What the element is called in prose and drawn as (TR, EN). The sample nouns trigger the validator's own
# keyword lists the way an author's words would, so the sample record proves the warnings are enough.
NOUN = {"cta": ("buton", "button"), "link": ("bağlantı", "link"), "field": ("form alanı", "form field"),
        "check": ("onay kutusu", "checkbox"), "chips": ("seçenek çipleri", "option chips"),
        "tabs": ("sekmeler", "tabs"), "accordion": ("akordeon", "accordion"), "text": ("açıklama metni", "description text"),
        "help": ("yardım satırı", "help line"), "badge": ("rozet", "badge"), "banner": ("duyuru şeridi", "banner")}

# Hints, in the record's language. They avoid every keyword the validator reads in the change (no element,
# function, region or regulated word), so the hints alone ask for nothing the skeleton hasn't written.
HINTS = {
    "title": ("⟦Testin sorusu: B’nin değiştirdiği iş sonucunu soran kısa soru⟧?",
              "⟦The test's question: a short question naming the business outcome B moves⟧?"),
    "problem": ("⟦Sorun: bu sayfada görülen engel ya da fırsat, tek cümle⟧",
                "⟦Problem: the obstacle or opportunity seen on this page, one sentence⟧"),
    "mechanism": ("⟦Mekanizma: B davranışı neden değiştirir, soruna dayanan tek cümle, sayı yok⟧",
                  "⟦Mechanism: why B changes behaviour, one sentence resting on the problem, no number⟧"),
    "variable": ("⟦Değişken: tek bir şeyi adlandıran kısa isim⟧", "⟦Variable: a short noun phrase naming one thing⟧"),
    "a": ("⟦A: sayfanın bugünkü hâli⟧", "⟦A: the page as it is today⟧"),
    "b": ("⟦B: A ile aynı, yalnız değişkende farklı⟧", "⟦B: the same as A except the variable⟧"),
    "source_note": ("⟦Neden hiçbir arşiv senaryosu uymuyor ve bu fikir en yakınından nasıl ayrılıyor⟧",
                    "⟦Why no archive scenario fits and how this idea differs from the nearest one⟧"),
    "note": ("⟦Kanıt neye dayanıyor; sezgi ya da sektör gözlemiyse neden düşük güvenli⟧",
             "⟦What the evidence rests on; for intuition or an industry observation, why confidence is low⟧"),
    "rationale": ("⟦Girdilerin neye dayandığı, tek cümle, sayı yok⟧",
                  "⟦What the score inputs rest on, one sentence, no number⟧"),
    "exposure": ("⟦Kim maruz sayılır: öğenin gerçekten ekrana geldiği an⟧; tetikleyici iki kolda aynı noktada "
                 "kaydedilir.",
                 "⟦Who counts as exposed: the moment the element is actually on screen⟧; the trigger is logged at "
                 "the same point in both arms."),
    "guardrail": ("⟦Guardrail: birincil KPI iyileşirken kötüleşebilecek bağımsız bir zarar, sözlükteki adıyla⟧",
                  "⟦Guardrail: an independent harm that can worsen while the primary improves, by its glossary name⟧"),
    "guardrail_den": ("⟦Payda: iki kolda aynı kitle⟧", "⟦Denominator: a population present in both arms⟧"),
    "den_en": ("⟦“{payda}”, İngilizce⟧", "⟦the glossary's “{payda}”, in English⟧"),
    "belief": ("⟦B’nin kazanması için doğru olması gereken tek inanç, en çok 160 karakter; uymuyorsa bu nesneyi "
               "silin⟧",
               "⟦The one belief B needs to be true to win, at most 160 characters; delete this object if none⟧"),
    "probe": ("⟦Testten önce ucuz bir yoklama, ör. oturum kaydı ya da beş kullanıcı görüşmesi⟧",
              "⟦A cheap check before the test, e.g. session recordings or five user interviews⟧"),
    "page_title": ("⟦Sayfa başlığı⟧", "⟦Page heading⟧"),
    "context": ("⟦Sayfanın bir sonraki satırı⟧", "⟦The page's next line⟧"),
    "tail": ("⟦Sayfanın son satırı⟧", "⟦The page's last line⟧"),
    "first_view": ("⟦İlk ekranda görünen içerik⟧", "⟦What the first view shows⟧"),
    "second": ("⟦İkinci seçenek⟧", "⟦The second option⟧"),
    "element_a": ("⟦A’daki metin⟧", "⟦The copy in A⟧"),
    "element_b": ("⟦B’deki metin⟧", "⟦The copy in B⟧"),
    "label": ("⟦Halka etiketi⟧", "⟦Ring label⟧"),
    "label_a": ("⟦A’daki yeri⟧", "⟦Its place in A⟧"),
    "label_b": ("⟦B’deki yeri⟧", "⟦Its place in B⟧"),
}

# Hints that depend on the element: what the card's slots hold for it.
KIND_HINTS = {
    ("accordion", "tail"): ("⟦Sayfadaki başka bir akordeonun başlığı⟧", "⟦Another accordion's header on the page⟧"),
    ("accordion", "second"): ("⟦Akordeonun içeriği⟧", "⟦What the accordion holds⟧"),
    ("field", "element_a"): ("⟦A’daki alan etiketi⟧", "⟦The field's label in A⟧"),
    ("field", "element_b"): ("⟦B’deki alan etiketi⟧", "⟦The field's label in B⟧"),
    ("field", "second"): ("⟦Alanın içindeki ipucu metni⟧", "⟦The placeholder inside the field⟧"),
}

# Sample text for the self-check (never printed): plausible, one sentence each, in the shapes the hints ask.
SAMPLES = {
    "tr": {"title": "{Noun} değişince ana işlem artar mı?",
           "problem": "Sayfadaki {noun} kullanıcının bir sonraki adımı görmesini zorlaştırıyor.",
           "mechanism": "B’deki {noun} sonraki adımı açıkça gösterdiği için kullanıcı kararını daha az duraksayarak "
                        "verir.",
           "variable": "{Noun} biçimi",
           "a": {"change": "Bugünkü {noun}", "add": "{Noun} yok", "remove": "{Noun} duruyor",
                 "move": "{Noun} özetin sonunda"},
           "b": {"change": "Yeni {noun}", "add": "{Noun} eklendi", "remove": "{Noun} kaldırıldı",
                 "move": "Aynı {noun} başlığın hemen ardında"},
           "source_note": "Arşivde bu sayfanın bu öğesine uyan bir senaryo yok.",
           "note": "Bu sayfanın verisi yok, fikir sezgiye dayandığı için güven düşük.",
           "rationale": "Kanıt, öğenin yeri, fark edilirliği ve işin büyüklüğü bu bandı veriyor.",
           "exposure": "Sayfayı açıp öğeyi ekranında gören değil, öğenin ekrana geldiği ana ulaşan kullanıcılar",
           "guardrail": "Destek Talebi", "guardrail_den": "Teste atanan ziyaretçi",
           "belief": "Kullanıcılar bir sonraki adımı karar vermeden önce görmek istiyor.",
           "probe": "Oturum kayıtlarında bu adımdaki duraksamaları sayın.",
           "page_title": "Sepetim", "context": "Ara toplam ve teslimat özeti", "tail": "Teslimat adresi",
           "first_view": "Sepetteki ürünler", "second": "Diğer",
           "element_a": "Devam et", "element_b": "Teslimatı seç ve devam et",
           "label": "{Noun} değişti", "label_add": "{Noun} eklendi", "label_remove": "{Noun} kaldırıldı",
           "label_a": "Özetin sonunda", "label_b": "Başlığın ardında"},
    "en": {"title": "Does a new {noun} raise the main action?",
           "problem": "The {noun} on the page makes the next step hard to see.",
           "mechanism": "B's {noun} shows the next step plainly, so users decide with less hesitation.",
           "variable": "{Noun} design",
           "a": {"change": "Today's {noun}", "add": "No {noun}", "remove": "The {noun} is there",
                 "move": "The {noun} at the end of the summary"},
           "b": {"change": "A new {noun}", "add": "A {noun} is added", "remove": "The {noun} is removed",
                 "move": "The same {noun} right after the heading"},
           "source_note": "No archive scenario fits this element of this page.",
           "note": "There is no data for this page, the idea rests on intuition, so confidence is low.",
           "rationale": "The evidence, where the element sits, how noticeable B is and the size of the job give "
                        "this band.",
           "exposure": "Users who reach the moment the element is actually on screen",
           "guardrail": "Support Contact Rate", "guardrail_den": "Visitors assigned to the test",
           "belief": "Users want to see the next step before they decide.",
           "probe": "Count the pauses at this step in session recordings.",
           "page_title": "Your cart", "context": "Subtotal and delivery summary", "tail": "Delivery address",
           "first_view": "Items in the cart", "second": "Other",
           "element_a": "Continue", "element_b": "Pick delivery and continue",
           "label": "{Noun} changed", "label_add": "{Noun} added", "label_remove": "{Noun} removed",
           "label_a": "End of summary", "label_b": "After the heading"},
}


class UsageError(Exception):
    pass


def _cap(text):
    """Capitalise the first letter, Turkish-aware (i → İ)."""
    if not text:
        return text
    first = {"i": "İ", "ı": "I"}.get(text[0], text[0].upper())
    return first + text[1:]


def kpi_entry(name, lang, role):
    """(name as written, the glossary denominator in the record's language or a hint, the glossary row)."""
    canon = vsj.glossary_canonical(name)
    row = vsj.glossary_rows().get(canon) if canon else None
    if not row:
        raise UsageError("%r is not a knowledge/kpi-glossary.md name; look it up with grep -niE '<word>' "
                         "knowledge/kpi-glossary.md and pass the canonical name" % name)
    window = re.search(r"\s*(\([^()]*\))\s*$", name)
    key = vsj.fold_tr(vsj._strip_window(name))
    own = [canon] + row["synonyms"] if lang == "tr" else row.get("english", [])
    if any(vsj.fold_tr(vsj._strip_window(label)) == key for label in own):
        written = name.strip()
    else:
        written = canon if lang == "tr" else (row.get("english") or [canon])[0]
        if window and not re.search(r"\([^()]*\)\s*$", written):
            written += " " + window.group(1)
    fams = vsj.families(row["payda"])
    if role == "primary" and ("değişebilir" in row["payda"] or (fams and fams <= vsj.POST_ASSIGNMENT)):
        raise UsageError("%r is counted per “%s”, a population B can change; a primary is counted per assigned "
                         "visitor or a trigger both arms share (rule 2), e.g. “Dönüşüm Oranı (CR)”" %
                         (written, row["payda"]))
    den = vsj.payda_text(row["payda"], lang)
    if den is None:
        den = HINTS["den_en"][1].format(payda=row["payda"])
    return written, den


def archive_block(title):
    """(Değişken, difference) of the archive scenario `title` names, or UsageError."""
    archive = vsj.load_archive()
    if not archive:
        raise UsageError("the archive (knowledge/scenarios/) was not found")
    folded = {vsj.quote_fold(" ".join(t.split())): v for t, v in archive.items()}
    found = folded.get(vsj.quote_fold(" ".join(title.split())))
    if not found:
        raise UsageError("%r is not an archive scenario title; copy it from a “## …” line in knowledge/scenarios/"
                         % title)
    variable, fark = found
    return variable, DIFFERENCE_TR.get(fark.strip().casefold(), fark)


def element_node(kind, text, second, ident=None):
    """A screen-spec node of `kind` showing `text` (`second`: the other chip, tab or the accordion's body)."""
    node = {"chips": {"chips": [{"label": text, "on": True}, {"label": second}]},
            "tabs": {"tabs": [{"label": text, "on": True}, {"label": second}]},
            "accordion": {"accordion": {"title": text, "open": False, "items": [{"text": second}]}},
            "field": {"field": second, "label": text}}.get(kind, {kind: text})
    node = copy.deepcopy(node)
    if ident:
        node["id"] = ident
    return node


def edit_set(kind, text, second):
    """The one property an edit sets on the element for B."""
    if kind in ("chips", "tabs"):
        return {kind: [{"label": text, "on": True}, {"label": second}]}
    if kind == "accordion":
        return {"open": True}
    if kind == "field":
        return {"label": text}
    return {kind: text}


def card(device, difference, kind, hidden, page, t):
    """A minimal card: a heading, a context line, the element, and the one change op."""
    screen = [{"h": t["page_title"]}, {"text": t["context"], "id": "baglam"}]
    target = element_node(kind, t["element_a"], t["second"], "hedef")
    tail = [{"text": t["tail"], "id": "son"}]
    if kind == "accordion":  # a page with one accordion has more: B's added one draws no colour A lacks
        tail = [{"accordion": {"title": t["tail"], "open": False, "items": [{"text": t["second"]}]}, "id": "son"}]
    if difference == "add":
        change = {"op": "insert_after", "target": "baglam", "node": element_node(kind, t["element_b"], t["second"]),
                  "label": t["label_add"]}
        body = screen + tail
    elif difference == "remove":
        change = {"op": "remove", "target": "hedef", "label": t["label_remove"]}
        body = screen + [target] + tail
    elif difference == "move":
        change = {"op": "move_after", "target": "hedef", "to": "son", "label_a": t["label_a"], "label_b": t["label_b"]}
        body = screen + [target] + tail
    else:
        change = {"op": "edit", "target": "hedef", "set": edit_set(kind, t["element_b"], t["second"]),
                  "label": t["label"]}
        body = screen + [target] + tail
    if hidden and device != "web":
        body = body[:1] + [{"text": t["first_view"]}, {"fold": True}] + body[1:]
    out = {"device": device, "mockup_basis": "representative", "screen": body, "change": change}
    if device != "phone":
        out["url"] = "site.example/%s" % page
    return out


def build(args, sample=False):
    """The record for `args`: hints in place, or (sample=True) the self-check's sample text."""
    lang = args.lang
    i = 1 if lang == "en" else 0
    noun = NOUN[args.element][i]
    s = SAMPLES[lang]

    def text(key, **kw):
        if sample:
            value = s[key]
            if isinstance(value, dict):
                value = value[args.difference]
            return value.replace("{Noun}", _cap(noun)).replace("{noun}", noun)
        return KIND_HINTS.get((args.element, key), HINTS[key])[i]

    level, ev_input = EVIDENCE[args.evidence]
    if args.adapted_from:
        _, fark = archive_block(args.adapted_from)
        if fark != args.difference:
            raise UsageError("the archive block's Fark is %r: an adapted record keeps it, pass --difference %s or "
                             "make it a generated record" % (fark, fark))
        level, ev_input = "archive", "archive_or_research"
    elif args.evidence == "archive":
        raise UsageError("archive evidence needs --adapted-from \"<the archive scenario's title>\"")
    primary, primary_den = kpi_entry(args.kpi, lang, "primary")
    effort = args.effort or ("medium" if args.device == "phone" else "low")
    inputs = {"evidence": ev_input, "impact": args.impact, "main_path": not args.off_path,
              "noticeable": not args.subtle, "effort": effort}
    tier = vsj.score_tier(vsj.priority_score(inputs)[0])

    rec = {"id": args.id or "%s-%s-%s-01" % (re.sub(r"[^a-z0-9]+", "-", args.page.lower()).strip("-") or "page",
                                              args.element, args.difference),
           "title": text("title"), "lang": lang, "stage": args.page, "device": args.device,
           "problem": text("problem"), "mechanism": text("mechanism"), "variable": text("variable"),
           "variants": [{"id": "A", "description": text("a")}, {"id": "B", "description": text("b")}],
           "difference": args.difference,
           "primary_kpi": {"name": primary, "denominator": primary_den,
                           "direction": "decrease" if HARM_RE.search(primary) else "increase"}}
    if args.guardrail:
        name, den = kpi_entry(args.guardrail, lang, "guardrail")
    else:
        name, den = text("guardrail"), text("guardrail_den")
    harm = bool(HARM_RE.search(name)) if args.guardrail else True  # the hint's default: a harm that rises
    rec["guardrail"] = {"name": name, "kind": "metric", "denominator": den,
                        "direction": "must_not_increase" if harm else "must_not_decrease"}
    if args.adapted_from:
        rec["source"], rec["adapted_from"] = "adapted", args.adapted_from
        rec["evidence"] = {"level": level, "note": ("Arşivde derlenmiş bir test fikrine dayanıyor, bir test sonucu "
                                                    "değil.", "Rests on a test idea curated in the archive, not on a "
                                                    "test result.")[i]}
    else:
        rec["source"], rec["source_note"] = "generated", text("source_note")
        rec["evidence"] = {"level": level, "note": text("note")}
        if sample and level in ("user_data", "sector"):
            rec["evidence"]["note"] = ("GA4 raporuna göre bu adımda çıkış yoğun.",
                                       "Per the GA4 report, exits cluster at this step.")[i] \
                if level == "user_data" else ("Sektör raporlarında sık görülen bir gözlem.",
                                              "An observation common in industry reports.")[i]
    rec["priority"] = {"tier": tier, "rationale": text("rationale"), "inputs": inputs}
    if args.element in CONDITIONAL or args.hidden:
        rec["exposure"] = (s["exposure"] + HINTS["exposure"][i].split("⟧", 1)[1]) if sample else HINTS["exposure"][i]
    if args.element in INTERACTIVE:
        rec["warnings"] = [{"type": "accessibility", "text": vsj.a11y_example(list(vsj.A11Y_BASE), lang)}]
        rec["invariants"] = [vsj.invariant_example(NOUN[args.element][0] if lang == "tr" else NOUN[args.element][1],
                                                   lang)]
    rec["must_be_true"] = {"belief": text("belief"), "probe": text("probe")}
    t = {k: text(k) for k in ("page_title", "context", "tail", "first_view", "second", "element_a", "element_b",
                              "label_a", "label_b")}
    t["label"] = s["label"].replace("{Noun}", _cap(noun)) if sample else HINTS["label"][i]
    t["label_add"] = s["label_add"].replace("{Noun}", _cap(noun)) if sample else HINTS["label"][i]
    t["label_remove"] = s["label_remove"].replace("{Noun}", _cap(noun)) if sample else HINTS["label"][i]
    rec["card"] = card(args.device, args.difference, args.element, args.hidden, args.page, t)
    return rec


def self_check(args):
    """[] when the skeleton is sound: with hints only placeholder errors, with sample text nothing at all."""
    schema = vsj.load_schema()
    problems = []
    skeleton = build(args)
    for e in vsj.validate(skeleton, schema, args.lang):
        if "placeholder" not in e and "yer tutucu" not in e:
            problems.append("skeleton: " + e)
    sample = build(args, sample=True)
    if vsj.placeholder_paths(sample):
        problems.append("sample: a hint left in %s" % vsj.placeholder_paths(sample)[0][0])
    problems += ["sample: " + e for e in vsj.validate(sample, schema, args.lang)]
    problems += ["sample warning: " + w for w in vsj.lint(sample, schema, args.lang)]
    return skeleton, problems


def parse_args(argv):
    ap = argparse.ArgumentParser(description="Print a scenario record skeleton the validator accepts once its "
                                             "⟦hints⟧ are replaced.")
    ap.add_argument("--device", required=True, choices=DEVICES)
    ap.add_argument("--difference", required=True, choices=DIFFERENCES)
    ap.add_argument("--page", required=True, help="the page or flow (stage), e.g. cart-checkout")
    ap.add_argument("--kpi", required=True, help="the primary KPI's knowledge/kpi-glossary.md name")
    ap.add_argument("--lang", choices=("tr", "en"), default="tr")
    ap.add_argument("--element", choices=ELEMENTS, default="cta", help="what the change touches (default: cta)")
    ap.add_argument("--hidden", action="store_true", help="the element sits below the first view or in a closed "
                                                          "region: exposure is written")
    ap.add_argument("--evidence", choices=sorted(EVIDENCE), default="intuition")
    ap.add_argument("--adapted-from", help="the archive scenario's title (source adapted, evidence archive)")
    ap.add_argument("--guardrail", help="the guardrail's glossary name (default: a hint)")
    ap.add_argument("--impact", choices=sorted(vsj.SCORE_IMPACT), default="persuasive")
    ap.add_argument("--effort", choices=sorted(vsj.SCORE_EFFORT), help="default: medium on phone (an app release), "
                                                                      "else low")
    ap.add_argument("--off-path", action="store_true", help="the element is off the main conversion path")
    ap.add_argument("--subtle", action="store_true", help="a user wouldn't notice B within seconds")
    ap.add_argument("--id", help="the record id (default: <page>-<element>-<difference>-01)")
    ap.add_argument("--out", help="write the skeleton here instead of stdout")
    args = ap.parse_args(argv)
    if args.id and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", args.id):
        ap.error("--id is a lowercase slug, e.g. cart-checkout-coupon-field-01")
    return args


def main(argv):
    args = parse_args(argv)
    try:
        skeleton, problems = self_check(args)
    except UsageError as exc:
        sys.stderr.write("new_record: %s\n" % exc)
        return 2
    if problems:
        sys.stderr.write("new_record: the skeleton failed its own check (a bug in new_record.py):\n")
        sys.stderr.writelines("  - %s\n" % p for p in problems)
        return 1
    text = json.dumps(skeleton, ensure_ascii=False, indent=2) + "\n"
    hints = len(vsj.placeholder_paths(skeleton))
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    where = args.out or "<record.json>"
    sys.stderr.write(("new_record: %d ⟦…⟧ ipucu var; her birini bu sayfanın gerçek değeriyle değiştirin, sonra: "
                      "python3 scripts/validate_scenario_json.py %s\n" if args.lang == "tr" else
                      "new_record: %d ⟦…⟧ hints; replace each with this page's real value, then: "
                      "python3 scripts/validate_scenario_json.py %s\n") % (hints, where))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
