#!/usr/bin/env python3
"""Validate scenario records against templates/scenario.schema.json.

Stdlib-only by design (the repo takes no runtime dependencies), so this is a
deliberately small subset of JSON Schema rather than a general implementation:
type, required, enum, const, additionalProperties, minItems/maxItems,
minLength, pattern, minimum and oneOf, which is what the schema uses. A schema
that uses any other keyword stops the tool (exit 2) instead of being
half-applied in silence. A oneOf whose branches all pin the same property with
const (guardrail.kind) is read as a tagged union: the tag picks the branch and
that branch's own errors are reported.

On top of the shape, the cross-field rules a schema cannot express are checked
directly, because they are the whole point of having a schema here.

ERRORS (exit 1):

  * the schema: the ten-field record (title, problem, mechanism, variable,
    variants, primary_kpi, guardrail, source, evidence, priority), a guardrail
    that is a metric (denominator + direction) or a check (criterion), at most
    three typed warnings, one to five invariants, review stamps that are PASS
    with a 64-hex fingerprint, the detail boxes' three to six items
  * source (rule 8): 'generated' carries a source_note; 'archive' and
    'adapted' name their archive scenario in adapted_from, and that title
    exists in knowledge/scenarios/*.md (whitespace-normalised, read relative to
    this script; without the archive folder the source cannot be verified and
    that is an error too); 'archive' keeps the archive block's Değişken as its
    variable (case and whitespace aside; Turkish records only, an English
    record's variable is a translation code cannot compare) and both keep its
    Fark as their difference (değiştir/ekle/taşı/kaldır = change/add/move/
    remove); an archive or adapted record is never labelled 'intuition'
  * evidence (rule 10): user_data and sector say what they rest on in
    evidence.note; intuition is never priority high; title, problem,
    mechanism, the priority rationale and the evidence note never write
    "garanti eder" / "guaranteed"
  * claims (rules 8, 10), in every free-text field of the record (title,
    problem, mechanism, variable, variants, priority rationale, evidence
    note, source_note, warnings, invariants, numeric_change, assumptions;
    not detail, not card): no result ("test edildi", "kazandı", "proven",
    "won" …) unless the evidence is the user's own data; no number tied to
    an outcome or chance word ("Dönüşüm %12 artar", "beklenen artış yüzde
    12", "win probability 70%", "doubles signups"), no other test's result
    ("benzer testlerde", "similar tests", "other companies saw") unless the
    user's own data with its source in evidence.note carries it (a forecast
    or a chance also says who reported it: "GA4’e göre", "<source> reports"),
    or a sector study is quoted with its source in the clause; the archive is
    never proof ("arşivde kazanmış"). Not claims: page figures (a discount,
    a price, a threshold), an observed baseline rate with no outcome word, a
    hypothesis without a number, anything negated
  * KPI meaning (rule 2): a name that encodes a conditional population
    (“→”, “Teklif Başına”, "per order", "among") over an assigned
    denominator, or a name that says per assigned visitor over an order,
    request or quote denominator; a canonical knowledge/kpi-glossary.md
    name (a synonym, a trailing window stripped) over a denominator of
    another family than the glossary's Payda (assigned, order, request,
    quote, session, reached-a-trigger); realized RPV that is normalized
  * assumptions (rules 9, 10): a critical item carries its question, each
    text is one sentence of at most 200 characters, and priority is never
    high while a critical one is open
  * numeric_change (rule 10): it says where its figure comes from (the page,
    the user, a derivation: "sayfadaki", "kullanıcının verdiği", "hesaplandı",
    "=", "×", "−", "from the page", "derived") or a critical assumption about
    the figure (sharing a number with it, or naming a price, amount, rate …)
    holds it open
  * KPIs (rules 2 and 3): the guardrail does not carry the primary's name and
    is not its complement (completion or a move to the next step, "geçiş",
    "proceed", against abandonment of that step over the same population);
    the primary's and a metric guardrail's denominator is a population
    present in both arms, not a count ("Sayısı"), the users who saw the
    change ("gören", "görüp", "gösterilen", "görüntüleyen", "maruz kalan",
    "saw", "seen", "shown", "exposed") or a B-only population ("yalnız B",
    "B only"); text after a "pay:" / "numerator:" label in the denominator
    field describes the numerator and is not read; a revenue primary on a change
    that touches a user benefit (coupon, discount, free shipping, refund,
    cancellation) has a guardrail on that benefit
  * what the change touches (rules 3, 4, 6, 11), read off the variable, the
    variants and the mechanism: an interactive element (link, button, field,
    modal …) needs an 'accessibility' warning stating a touch target as a
    size with its unit (at least 44 pt or px, 48 dp: "44×44 pt", "48×48 dp"),
    text contrast as a ratio (at least 4.5:1; a lower ratio is named as an
    error unless it is for large text or non-text parts beside the 4.5:1
    one), a bare "dokunma alanı" or "kontrast" states neither; a keyboard and
    screen-reader criterion, plus focus and closing for a modal or pop-up and
    pausing for an auto-advancing carousel;
    an interactive or functional element (coupon, payment, search, form …)
    needs `invariants`; a regulated-looking record (stage, title, problem,
    mechanism or variants mention insurance, pension, credit, loan, consent,
    KVKK, sigorta, emeklilik, BES, kredi, poliçe, rıza, onay) needs a
    'regulation' warning; urgency or scarcity wording in B or the mechanism
    needs a 'regulation' warning that names the real data source ("stok",
    "envanter", "gerçek", "inventory", "verified", "real")
  * detail (only when present): exactly one primary KPI and it is the first
    line, at least one guardrail, no metric listed twice, no complement
    guardrail, the primary line is not a count and has no "saw it"
    denominator (rules 2 and 3)
  * variants are "A" then "B", and the current page is A (rule 15)
  * card (optional; a record is valid without one): a difference type is
    stated (the record's; card.difference may only repeat it), the mockup markup passes the
    builder's allowlist, ring placement matches that difference, a ring has
    a label and no margin/padding, brand colours are real colours, a browser
    frame has its url and no tab bar, bottom_nav_active names a tab (all shared
    with build_card.py)

WARNINGS (printed, exit code unaffected; --strict turns them into errors):

  * title: not a question, longer than 90 characters
  * problem, mechanism or an invariant longer than one sentence; problem,
    mechanism, a variant description, an invariant, the priority rationale or
    a warning text longer than 240 characters
  * the title names an abandonment or completion outcome ("terk", "çıkış",
    "abandon") and the primary is a revenue metric, or the title names revenue
    ("gelir", "revenue") and the primary is a completion rate (a heuristic on
    free text: scenario-critic decides whether the primary fits)
  * borderline claim wording the code can't decide, "reviewer must judge":
    a number and an outcome word in one sentence without a clear link,
    vague magnitudes ("çok daha fazla", "ciddi artış", "much more")
  * intuition or sector evidence written with certainty ("kesin",
    "kesinlikle", "garanti", "mutlaka artırır", "certainly", "guaranteed",
    "will definitely") in problem, mechanism or the priority rationale
    (rule 10)
  * straight quotes in Turkish text (rule 7)
  * detail KPI lines: a rate with no stated denominator, a count or a "saw it"
    denominator off the primary (lines labelled "yalnız B" / "B only" and
    pass/fail checks are skipped), a guardrail with no question text
  * a card drawn from the shared page whose variant A is not marked current, a
    card device that differs from the record's, the card's own warnings (a
    colour only in B, a difference outside the ring …)

Every keyword rule above is a heuristic on wording (the lists are named
constants below, matched at word starts): it decides which questions a record
must answer, never that the answer is good. What this tool deliberately does
NOT check: whether `variable` really names a single variable, whether the
variants differ only in it, whether the mechanism is causal, whether the
primary KPI is sensitive to the change, whether the invariants and the
accessibility criteria are the right ones, whether the priority rationale
weighs impact, confidence and ease honestly. Those are judgement calls and
belong to agents/scenario-critic.

FINGERPRINT: `--fingerprint <file>` validates the record and, when it has no
errors, prints only record_fingerprint(): the sha256 of the record without its
`review` and `card`, serialised with sorted keys. scenario-critic stamps that
value into review.scenario_critic; build_card.py compares it before it builds.

Usage:
  validate_scenario_json.py <file.json> [more.json ...]
  validate_scenario_json.py --strict <file.json>         # warnings count as errors
  validate_scenario_json.py --lang en <file.json>        # messages in English (default: Turkish)
  validate_scenario_json.py --schema templates/scenario.schema.json <file.json>
  validate_scenario_json.py --fingerprint <file.json>    # validate, then print only the fingerprint

Exit: 0 = all valid, 1 = violations found, 2 = usage error.
"""
import argparse
import difflib
import glob
import hashlib
import html
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

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(DEFAULT_SCHEMA), "scenario-card.html")

# The archive an 'archive' or 'adapted' record must name (rule 8), resolved
# relative to this script so the check works from any working directory.
ARCHIVE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge",
                                            "scenarios"))

try:  # one source of truth for everything about the card: the builder's own rules
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build_card  # noqa: E402
    from build_card import DIFFERENCE_ALIASES  # noqa: E402
except ImportError:  # pragma: no cover - build_card ships next to this file
    build_card = None
    DIFFERENCE_ALIASES = {}

# Keywords walk() applies. A keyword outside this list (and outside the two
# below) would be silently inert, so load_schema() refuses a schema that has one.
IMPLEMENTED_KEYWORDS = frozenset((
    "type", "required", "enum", "const", "additionalProperties", "minItems", "maxItems", "minLength",
    "pattern", "minimum", "oneOf", "properties", "items", "$ref",
))
# Written in the schema for other tools; the same rule is enforced by hand in
# check_detail (exactly one primary, at least one guardrail).
HANDLED_ELSEWHERE = frozenset(("allOf", "contains", "minContains", "maxContains"))
ANNOTATIONS = frozenset(("$schema", "$id", "$defs", "title", "description"))

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}

# The record's length limits (methodology.md → The scenario record).
MAX_TITLE = 90
MAX_TEXT = 240
MAX_ASSUMPTION = 200  # assumptions[].text; load_schema() refuses maxLength, so it is checked here
# The warning type a regulated-looking record must carry (rule 11).
REGULATION = "regulation"

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
    "minItems": ("{path}: {have} öğe var, en az {n} olmalı", "{path}: has {have} item(s), minimum is {n}"),
    "maxItems": ("{path}: {have} öğe var, en fazla {n} olabilir", "{path}: has {have} item(s), maximum is {n}"),
    "required": ("{path}: zorunlu alan eksik: {key!r}", "{path}: missing required field {key!r}"),
    "unknown": ("{path}: tanımsız alan: {key!r}", "{path}: unknown field {key!r}"),
    "oneOf": ("{path}: oneOf dallarından {m}/{n} tanesi eşleşti (tam 1 olmalı)",
              "{path}: {m}/{n} oneOf branches matched (expected exactly 1)"),
    "closest": (" (en yakın dal: {detail})", " (closest branch: {detail})"),
    "file_errors": ("{file}: {n} ihlal", "{file}: {n} violation(s)"),
    "file_ok": ("{file}: ok", "{file}: ok"),
    "invalid_json": ("{file}: GEÇERSİZ JSON: {err}", "{file}: INVALID JSON: {err}"),
    "total": ("TOPLAM: {n} ihlal", "TOTAL: {n} violation(s)"),
    "all_ok": ("Tüm senaryolar şemaya uyuyor.", "All scenarios conform to the schema."),
    "root": ("(kök)", "(root)"),
    # ---- errors -----------------------------------------------------------
    "adapted_from": ("adapted_from: kaynak '{src}' ise kaydın dayandığı arşiv senaryosunun başlığı yazılmalı (kural 8)",
                     "adapted_from: a record with source '{src}' names the archive scenario it comes from (rule 8)"),
    "source_note": ("source_note: kaynak 'generated' ise hiçbir arşiv senaryosunun neden uymadığı ve bu fikrin "
                    "nasıl ayrıldığı yazılmalı (kural 8)",
                    "source_note: a 'generated' record says why no archive scenario fits and how this idea "
                    "differs (rule 8)"),
    "evidence_downgrade": ("evidence.level: '{src}' kaynaklı bir senaryo 'intuition' olarak etiketlenmez; kanıt arşiv örüntüsüdür (kural 8)",
                           "evidence.level: a '{src}' scenario is not labelled 'intuition'; its evidence is an archive pattern (rule 8)"),
    "archive_missing": ("adapted_from: arşiv bulunamadı ({dir}); '{src}' kaynağı doğrulanamaz (kural 8)",
                        "adapted_from: the archive was not found ({dir}); a '{src}' source cannot be verified (rule 8)"),
    "adapted_from_unknown": ("adapted_from: {val!r} arşivde bir senaryo başlığı değil; başlığı knowledge/scenarios/*.md "
                             "içindeki “## …” satırından birebir kopyalayın{hint} (kural 8)",
                             "adapted_from: {val!r} is not an archive scenario title; copy it exactly from a \"## …\" "
                             "line in knowledge/scenarios/*.md{hint} (rule 8)"),
    "closest_title": (" (en yakın: {title!r})", " (closest: {title!r})"),
    "archive_variable": ("variable: kaynak 'archive' ise değişken arşivdeki Değişken ile aynıdır: {exp!r}, gelen {got!r}; "
                         "başka bir değişken 'adapted' ya da 'generated' bir kayıttır (kural 8)",
                         "variable: a record with source 'archive' keeps the archive's Değişken: {exp!r}, got {got!r}; "
                         "a different variable makes it 'adapted' or 'generated' (rule 8)"),
    "archive_difference": ("difference: kaynak '{src}' ise fark arşivdeki Fark ile aynıdır: '{exp}' (Fark: {fark}), "
                           "gelen {got} (kural 8)",
                           "difference: a record with source '{src}' keeps the archive's Fark: '{exp}' (Fark: {fark}), "
                           "got {got} (rule 8)"),
    "missing_value": ("yok", "none"),
    "evidence_note": ("evidence.note: kanıt '{level}' ise neye dayandığı yazılır (hangi veri, hangi sektör gözlemi) "
                      "(kural 10)",
                      "evidence.note: '{level}' evidence says what it rests on (which data, which industry observation) "
                      "(rule 10)"),
    "intuition_high": ("priority.tier: kanıt 'intuition' iken öncelik 'high' olamaz; sezgiye dayanan bir fikir en fazla "
                       "'medium' olur (kural 9, 10)",
                       "priority.tier: an 'intuition' record cannot be priority 'high'; an idea resting on intuition is "
                       "'medium' at most (rules 9, 10)"),
    "overclaim": ("{path}: {word!r} bir sonuç iddiası; kanıt 'user_data' değilse senaryo test edilmiş, kanıtlanmış ya da "
                  "kazanmış diye sunulmaz, kazanma olasılığı ya da artış yüzdesi yazılmaz (kural 8, 10)",
                  "{path}: {word!r} claims a result; without 'user_data' evidence a scenario is never presented as "
                  "tested, proven or a win, and no chance of winning or uplift percentage is written (rules 8, 10)"),
    "uplift_claim": ("{path}: {word!r} bir sonuç iddiası: öngörülen ya da gerçekleşmiş bir artış veya kazanma "
                     "olasılığı. Bunu yalnızca kullanıcının kendi verisi taşır (kanıt 'user_data', kaynağı "
                     "evidence.note’ta; bir tahmin ya da olasılık kimin raporladığını da söyler: “<kaynak> raporuna "
                     "göre …”) ya da kaynağıyla alıntılanan bir sektör araştırması; yoksa hipotezi sayı olmadan "
                     "yazın (kural 8, 10)",
                     "{path}: {word!r} claims a result: a predicted or achieved uplift or a chance of winning. Only "
                     "the user's own data carries it ('user_data' evidence with its source in evidence.note; a "
                     "forecast or a chance also says who reported it: \"<source> reports …\"), or a sector study "
                     "quoted with its source; otherwise write the hypothesis without a number (rules 8, 10)"),
    "similar_claim": ("{path}: {word!r} başka testlerden bir sonuç iddiası (“benzer testlerde”, “başka şirketler "
                      "gördü”); bunu yalnızca kullanıcının kendi verisi taşır (kanıt 'user_data', kaynağı "
                      "evidence.note’ta), bir senaryo sonuç ödünç almaz (kural 8, 10)",
                      "{path}: {word!r} claims a result from other tests (\"similar tests\", \"other companies "
                      "saw\"); only the user's own data carries it ('user_data' evidence with its source in "
                      "evidence.note), a scenario never borrows a result (rules 8, 10)"),
    "archive_claim": ("{path}: {word!r} arşivden bir sonuç iddiası; arşiv bir test fikirleri kütüphanesidir, kazanan "
                      "testlerin kaydı değil: arşivde olmak hiçbir kanıtla test edilmiş, kanıtlanmış ya da kazanmış "
                      "diye sunulmaz (kural 8)",
                      "{path}: {word!r} claims a result from the archive; the archive is a library of test ideas, not "
                      "a log of wins, so being in it is never presented as tested, proven or a win, whatever the "
                      "evidence (rule 8)"),
    "claim_borderline": ("{path}: {word!r} kodun karar veremediği bir sonuç ya da etki ifadesi gibi okunuyor (bir "
                         "sonuç sözcüğünün yakınında bir sayı ya da belirsiz bir büyüklük); reviewer must judge: "
                         "yalnızca gözlenmiş bir rakam ya da sayısız bir hipotezse kalır (kural 8, 10)",
                         "{path}: {word!r} reads like a result or impact claim the code can't decide (a number near "
                         "an outcome word, or a vague magnitude); reviewer must judge: it stays only if it is an "
                         "observed figure or a hypothesis without a number (rules 8, 10)"),
    "assumption_long": ("{path}: {n} karakter; bir varsayım en fazla {max} karakterlik tek cümledir",
                        "{path}: {n} characters; an assumption is one sentence of at most {max}"),
    "assumption_question": ("{path}: kritik bir varsayım onu çözecek tek kısa soruyu taşır (turun tek sorusu en kritik "
                            "olanıdır, kural 19)",
                            "{path}: a critical assumption carries the one short question that settles it (the "
                            "turn's one question is the most critical of them, rule 19)"),
    "assumption_high": ("priority.tier: kritik bir varsayım varken ({text!r}) öncelik 'high' olamaz; doğrulanmamış "
                        "kritik bir olguya dayanan öneri en fazla 'medium' olur (kural 9, 10)",
                        "priority.tier: 'high' with a critical assumption ({text!r}); a proposal resting on an "
                        "unverified critical fact is medium at most (rules 9, 10)"),
    "objection_lang": ("objection: {val!r} kaydın dilinde değil ({lang}); {want!r} yazın (kural 7)",
                       "objection: {val!r} isn't in the record's language ({lang}); write {want!r} (rule 7)"),
    "statistics": ("{path}: {word!r} istatistik dili; bu playbook örneklem, süre, anlamlılık, güç, kazanan ya da "
                   "sayısal öncelik puanı hesaplamaz ve yazmaz, kayıt istatistik iddiası taşımaz (kural 5)",
                   "{path}: {word!r} is statistics language; this playbook doesn't compute or write sample size, "
                   "duration, significance, power, a winner or a numeric priority score, and a record carries no "
                   "statistical claim (rule 5)"),
    "never_claim": ("{path}: {word!r} hiçbir kanıtla yazılmaz; bir testin sonucu garanti edilemez (kural 10)",
                    "{path}: {word!r} is never written, whatever the evidence; no test result can be guaranteed "
                    "(rule 10)"),
    "guardrail_is_primary": ("guardrail.name: {name!r} birincil KPI’ın adı; guardrail bağımsız bir zararı ölçer (kural 3)",
                             "guardrail.name: {name!r} is the primary KPI’s name; a guardrail measures an "
                             "independent harm (rule 3)"),
    "denominator_count": ("{path}: {val!r} bir sayı; payda, iki kolda da aynı olan bir kitledir "
                          "(ör. “Teste atanan ziyaretçi”)",
                          "{path}: {val!r} is a count; the denominator is a population that is the same in both "
                          "arms (e.g. \"assigned visitors\")"),
    "denominator_saw": ("{path}: {val!r} “gören/gösterilen” bir kitle; görme B’deki değişikliğe bağlı olabilir, bu yüzden "
                        "payda iki kolda karşılaştırılamaz. Teste atanan kullanıcıyı ya da iki kolda aynı noktada "
                        "kaydedilen bir tetiği yazın: “<ekran> ekranına ulaşan kullanıcı” (methodology → KPI "
                        "denominator)",
                        "{path}: {val!r} is a \"users who saw it\" population; seeing can depend on B's change, so the "
                        "denominator can't be compared across arms. Write the assigned users or a trigger logged at the "
                        "same point in both arms: \"users who reached the <screen> screen\" (methodology → KPI "
                        "denominator)"),
    "denominator_b_only": ("{path}: {val!r} yalnızca B’de var olan bir kitle; payda iki kolda aynı olmalı "
                           "(methodology → KPI denominator)",
                           "{path}: {val!r} is a population that exists only in B; the denominator is the same in both "
                           "arms (methodology → KPI denominator)"),
    "complement": ("{path}: guardrail {name!r} birincil KPI'ın tümleyeni gibi görünüyor (aynı payda, 1 − birincil); "
                   "biri kazanırken diğeri bozulamaz, bağımsız bir zarar ölçün (sonraki adım, kalite, maliyet)",
                   "{path}: guardrail {name!r} looks like the complement of the primary (same denominator, "
                   "1 − primary); one cannot win while the other degrades, measure an independent harm (a later "
                   "step, quality, cost)"),
    "kpi_mismatch": ("{path}: {name!r} adı koşullu bir kitleyi ölçüyor ({word!r}: teklif ya da sipariş başına, "
                     "X yapanlar arasında) ama payda {den!r} atanan kitle; ad ve payda farklı şeyleri ölçüyor. "
                     "Atanan ziyaretçi başına metriğin adını yazın ya da koşullu paydayı yazıp metriği detayda "
                     "etiketli bir tanısal olarak tutun; birincil olmaz (kural 2)",
                     "{path}: the name {name!r} measures a conditional population ({word!r}: per quote or order, "
                     "among users who did X) but the denominator {den!r} is the assigned population; name and "
                     "denominator measure different things. Name the per-assigned-visitor metric, or write the "
                     "conditional denominator and keep the metric a labelled diagnostic in the detail view; it is "
                     "never the primary (rule 2)"),
    "kpi_mismatch_reverse": ("{path}: {name!r} adı atanan ziyaretçi başına diyor ama payda {den!r} bir {fam} "
                             "kitlesi; ad ve payda farklı şeyleri ölçüyor (kural 2)",
                             "{path}: the name {name!r} says per assigned visitor but the denominator {den!r} belongs "
                             "to the {fam} family; name and denominator measure different things (rule 2)"),
    "kpi_glossary_family": ("{path}: {name!r} sözlükte {canon!r}: {definition}; paydası “{payda}”, yani bir {gfam} "
                            "kitlesi. Kayıttaki payda {den!r} bir {rfam} kitlesi, bu yüzden kayıt bu adla başka bir "
                            "şeyi ölçüyor.{hint} Bir KPI adının tek anlamı vardır: paydası bu olan sözlük adını "
                            "kullanın ya da metriğe yeni bir ad verin (knowledge/kpi-glossary.md, kural 2)",
                            "{path}: {name!r} is the glossary's {canon!r}: {definition}; counted over “{payda}” (the "
                            "{gfam} family). The denominator {den!r} belongs to the {rfam} family, so the record "
                            "measures something else under this name.{hint} One KPI name has one meaning: use the glossary name "
                            "whose denominator this is, or give the metric a new name (knowledge/kpi-glossary.md, "
                            "rule 2)"),
    "kpi_trigger_hint": (" Atama o tetikte yapılıyorsa paydada söyleyin: “Teste atanan ziyaretçi (atama … "
                         "ulaşınca)”.",
                         " If assignment happens at that trigger, say so in the denominator: \"Visitors assigned "
                         "on reaching …\"."),
    "kpi_normalized_revenue": ("{path}: {name!r} gerçekleşmiş gelirdir (pencerede fiilen tahsil edilen tutar, atanan "
                               "ziyaretçi başına); {word!r} onu normalize bir değere çeviriyor, bu başka bir metrik: "
                               "“Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)”, tahsil edilen "
                               "tutar için “Tahsilat (gözlem penceresi, atanan ziyaretçi başına)” "
                               "(knowledge/kpi-glossary.md, kural 2)",
                               "{path}: {name!r} is realized revenue (the cash actually collected in the window, per "
                               "assigned visitor); {word!r} turns it into a normalized value, a different metric: "
                               "“Yeni Abonelik Değeri (aylığa normalize, atanan ziyaretçi başına)”, or “Tahsilat "
                               "(gözlem penceresi, atanan ziyaretçi başına)” for the cash collected "
                               "(knowledge/kpi-glossary.md, rule 2)"),
    "benefit_guardrail": ("guardrail: birincil KPI bir gelir metriği ({name!r}) ve değişiklik bir kullanıcı faydasına "
                          "dokunuyor ({word!r}); guardrail o faydayı ölçmeli (ör. “Kuponlu Sipariş Veren Ziyaretçi Oranı” düşmemeli), "
                          "yoksa faydanın kaybı gelir kazancı gibi okunur (kural 3)",
                          "guardrail: the primary KPI is a revenue metric ({name!r}) and the change touches a user "
                          "benefit ({word!r}); the guardrail must watch that benefit (e.g. \"Coupon-Order Visitor Rate\" must "
                          "not drop), or the lost benefit reads as a revenue win (rule 3)"),
    "a11y_missing": ("warnings: değişiklik etkileşimli bir öğeye dokunuyor ({word!r}); geçti/kaldı ölçütlerini taşıyan "
                     "'accessibility' türünde bir uyarı ekleyin: {criteria} (kural 3)",
                     "warnings: the change touches an interactive element ({word!r}); add a warning of type "
                     "'accessibility' that states its pass/fail criteria: {criteria} (rule 3)"),
    "a11y_criteria": ("warnings: erişilebilirlik uyarısında şu ölçüt(ler) yok: {criteria} ({word!r} için); her biri "
                      "geçti/kaldı ölçütü olarak yazılır (kural 3)",
                      "warnings: the accessibility warning does not state: {criteria} (for {word!r}); write each as a "
                      "pass/fail criterion (rule 3)"),
    "numeric_unsourced": ("numeric_change: {val!r} rakamın nereden geldiğini söylemiyor; sayfada görünüyorsa "
                          "“sayfadaki …”, kullanıcı verdiyse “kullanıcının verdiği …” ya da nasıl hesaplandığını "
                          "(“1.500 − 1.230 = 270”) yazın; doğrulanmadıysa rakamı sorusuyla bir kritik varsayım olarak "
                          "işaretleyin (kural 10; mockup-style → Numbers the mockup needs but must not invent)",
                          "numeric_change: {val!r} does not say where the figure comes from; write that the page shows "
                          "it (\"from the page\"), that the user gave it, or how it was derived (\"1,500 − 1,230 = "
                          "270\"); if it isn't verified, mark the figure as a critical assumption with its question "
                          "(rule 10; mockup-style → Numbers the mockup needs but must not invent)"),
    "a11y_threshold": ("warnings: erişilebilirlik uyarısındaki {what} {val!r} eşiğin altında; en az {need} "
                       "(kural 3)",
                       "warnings: the accessibility warning states {what} {val!r}, below the threshold: at least "
                       "{need} (rule 3)"),
    "invariants": ("invariants: değişiklik işlevsel bir öğeye dokunuyor ({word!r}); iki kolda aynı çalışması gereken "
                   "işlevleri (1-5 cümle) yazın, ör. “Geçerli bir kod iki kolda da aynı adımla uygulanır.” (kural 4)",
                   "invariants: the change touches a functional element ({word!r}); list the functions that must work "
                   "identically in both arms (1-5 sentences), e.g. \"A valid code applies in the same step in both "
                   "arms.\" (rule 4)"),
    "regulated": ("warnings: kayıt düzenlemeye tabi bir akışta görünüyor ({word}); 'regulation' türünde bir uyarı "
                  "ekleyin (kural 11), ör. “B’nin metni için uyum onayı alınmadan teste trafik açılmaz.”",
                  "warnings: the record looks like a regulated flow ({word}); add a warning of type 'regulation' "
                  "(rule 11), e.g. \"No traffic before compliance signs off on B's exact copy.\""),
    "urgency": ("warnings: B ya da mekanizma aciliyet veya kıtlık sinyali taşıyor ({word!r}); sinyalin dayandığı gerçek "
                "veri kaynağını (gerçek stok, envanter, doğrulanmış trafik) söyleyen 'regulation' türünde bir uyarı "
                "ekleyin, doğrulanamıyorsa önermeyin (kural 6)",
                "warnings: B or the mechanism carries an urgency or scarcity signal ({word!r}); add a warning of type "
                "'regulation' that names the real data source behind it (real stock, inventory, verified traffic), "
                "and don't propose it if it can't be verified (rule 6)"),
    "primary_count": ("detail.kpis: 'primary' rolünde {n} KPI var, tam 1 olmalı (kural 2)",
                      "detail.kpis: found {n} KPI(s) with role 'primary', expected exactly 1 (rule 2)"),
    "primary_first": ("detail.kpis[0]: ilk KPI birincil olmalı, gelen rol {role!r} (kural 2)",
                      "detail.kpis[0]: the first KPI must be the primary one, got role {role!r} (rule 2)"),
    "no_guardrail": ("detail.kpis: 'guardrail' rolünde KPI yok (kural 3)",
                     "detail.kpis: no KPI with role 'guardrail' (rule 3)"),
    "kpi_dup": ("detail.kpis[{i}]: {name!r} listede iki kez geçiyor (detail.kpis[{j}]); her metrik bir kez ve tek "
                "rolle yazılır",
                "detail.kpis[{i}]: {name!r} appears twice (detail.kpis[{j}]); each metric is listed once, with one role"),
    "kpi_count_primary": ("{path}: birincil KPI {name!r} bir sayı (“Sayısı”); kollar farklı büyüklükteyse "
                          "karşılaştırılamaz, atanan ziyaretçi başına orana çevirin",
                          "{path}: primary KPI {name!r} is a count; arms of different size cannot be compared, "
                          "turn it into a rate per assigned visitor"),
    "kpi_saw_primary": ("{path}: birincil KPI {name!r} paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda "
                        "iki kolda karşılaştırılamaz (methodology → KPI denominator)",
                        "{path}: primary KPI {name!r} has a \"users who saw\" denominator; a denominator that exists "
                        "only in B cannot be compared across arms (methodology → KPI denominator)"),
    "variants_ids": ("variants: kimlikler sırasıyla \"A\" ve \"B\" olmalı, gelen {ids}",
                     "variants: ids must be \"A\" then \"B\", got {ids}"),
    "variants_current": ("variants[1].is_current: mevcut sayfa her zaman A'dır (kural 15)",
                         "variants[1].is_current: the current page is always A (rule 15)"),
    "card_line": ("card: {msg}", "card: {msg}"),
    "card_difference": ("card.difference: kartta da kayıtta da `difference` yok (change / add / move / remove); "
                        "halka yerleşimi denetlenemez",
                        "card.difference: neither the card nor the record states a difference (change / add / move / "
                        "remove); ring placement cannot be checked"),
    # ---- warnings ---------------------------------------------------------
    "title_question": ("title: başlık soru işaretiyle bitmiyor; iddia cümlesi testi önceden yargılar",
                       "title: does not end with '?'; an assertion prejudges the test"),
    "title_long": ("title: {n} karakter; kısa bir soru olmalı (en fazla {max})",
                   "title: {n} characters; keep the question short (at most {max})"),
    "one_sentence": ("{path}: {n} cümle var; tek cümle olmalı", "{path}: {n} sentences; write one"),
    "too_long": ("{path}: {n} karakter; en fazla {max} karakterde tutun",
                 "{path}: {n} characters; keep it to {max}"),
    "title_kpi_revenue": ("primary_kpi.name: başlık {word!r} sonucunu soruyor ama birincil KPI {name!r} bir gelir "
                          "metriği; gelir kazancı kaybedilen bir faydayı gizleyebilir, başlığın sorduğu sonucu ölçün "
                          "(sezgisel uyarı, kural 2)",
                          "primary_kpi.name: the title asks about {word!r} but the primary KPI {name!r} is a revenue "
                          "metric; a revenue win can hide a lost benefit, measure the outcome the title names "
                          "(heuristic, rule 2)"),
    "title_kpi_completion": ("primary_kpi.name: başlık {word!r} sonucunu soruyor ama birincil KPI {name!r} bir "
                             "tamamlama ya da terk oranı; başlığın sorduğu sonucu ölçün (sezgisel uyarı, kural 2)",
                             "primary_kpi.name: the title asks about {word!r} but the primary KPI {name!r} is a "
                             "completion or abandonment rate; measure the outcome the title names (heuristic, "
                             "rule 2)"),
    "overconfident": ("{path}: kanıt '{level}' iken {word!r} fazla kesin; zayıf kanıt kazanç vaat etmez (kural 10)",
                      "{path}: {word!r} is too certain for '{level}' evidence; weak evidence promises no win (rule 10)"),
    "kpi_denominator": ("{path}: {name!r} bir oran ama paydası yazılmamış; varsayılan atanan ziyaretçidir, farklıysa "
                        "adına “(… başına)” ekleyin ya da denominator alanını doldurun",
                        "{path}: {name!r} is a rate with no stated denominator; assigned visitors is assumed, "
                        "otherwise add \"(per …)\" to the name or fill the denominator field"),
    "kpi_count": ("{path}: {role} KPI {name!r} bir sayı (“Sayısı”); kollar farklı büyüklükteyse karşılaştırılamaz, "
                  "atanan ziyaretçi başına orana çevirin",
                  "{path}: {role} KPI {name!r} is a count; arms of different size cannot be compared, turn it into "
                  "a rate per assigned visitor"),
    "kpi_saw": ("{path}: {role} KPI {name!r} paydası “gören/görüp” diyor; yalnızca B’de var olan bir payda iki kolda "
                "karşılaştırılamaz",
                "{path}: {role} KPI {name!r} has a \"users who saw\" denominator; a denominator that exists only in B "
                "cannot be compared across arms"),
    "kpi_no_question": ("{path}: guardrail için soru yazılmamış (neyin düşmemesi ya da artmaması gerektiği)",
                        "{path}: guardrail has no question text (what must not drop or rise)"),
    "straight_quotes": ("{path}: düz tırnak var; Türkçe metinde kıvrık tırnak kullanın (kural 7)",
                        "{path}: straight quotes; use curly quotes in scenario text (rule 7)"),
    "basis_current": ("card.mockup_basis: 'shared_page' ise variants[0].is_current: true beklenir (kural 15)",
                      "card.mockup_basis: 'shared_page' expects variants[0].is_current: true (rule 15)"),
    "card_device": ("card.device: '{card}', senaryonun device değeri '{scn}' ile farklı",
                    "card.device: '{card}' differs from the scenario's device '{scn}'"),
    "file_warnings": ("{file}: {n} uyarı (çıkış kodunu etkilemez)", "{file}: {n} warning(s) (exit code unaffected)"),
    "file_warnings_strict": ("{file}: {n} uyarı (--strict: ihlal sayılır)",
                             "{file}: {n} warning(s) (--strict: counted as violations)"),
    "total_warnings": ("TOPLAM: {n} uyarı (çıkış kodunu etkilemez; --strict ile ihlal sayılır)",
                       "TOTAL: {n} warning(s) (exit code unaffected; --strict counts them as violations)"),
    "bad_schema": ("şema, bu doğrulayıcının uygulamadığı anahtar sözcük(ler) kullanıyor: {kw}",
                   "schema uses keyword(s) this validator does not implement: {kw}"),
    "fingerprint_refused": ("{file}: {n} ihlal; parmak izi yazılmadı, önce kaydı düzeltin",
                            "{file}: {n} violation(s); no fingerprint printed, fix the record first"),
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


def tagged_branch(value, branches):
    """The branch a tagged union picks for `value`.

    A oneOf whose branches all pin the same property with `const` (guardrail.kind:
    "metric" / "check") is a tagged union: the tag says which branch the value
    means, so that branch's errors are the useful ones ("missing required field
    'denominator'"), not "0/2 branches matched". Returns (branch, None) when the
    tag selects a branch, (None, (key, options)) when it names none, and
    (None, None) when the oneOf is untagged or the value carries no tag.
    """
    if not isinstance(value, dict):
        return None, None
    tags = None
    for branch in branches:
        pinned = {k for k, sub in (branch.get("properties") or {}).items() if isinstance(sub, dict) and "const" in sub}
        tags = pinned if tags is None else tags & pinned
    for key in sorted(tags or ()):
        if key not in value:
            continue
        options = [branch["properties"][key]["const"] for branch in branches]
        for branch, option in zip(branches, options):
            if value[key] == option:
                return branch, None
        return None, (key, options)
    return None, None


def walk(value, schema, path, errors, root, lang="tr"):
    if "$ref" in schema:
        schema = resolve(schema["$ref"], root)
    shown = path or msg(lang, "root")

    if "oneOf" in schema:
        branch, unknown_tag = tagged_branch(value, schema["oneOf"])
        if branch is not None:
            walk(value, branch, path, errors, root, lang)
            return
        if unknown_tag is not None:
            key, options = unknown_tag
            errors.append(msg(lang, "enum", path="%s.%s" % (path, key) if path else key, val=value[key], opts=options))
            return
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


def resolve(ref, root):
    if not ref.startswith("#/"):
        return {}
    node = root
    for part in ref[2:].split("/"):
        node = node.get(part, {})
    return node


def unsupported_keywords(schema):
    """Schema keywords walk() would ignore. Empty list = the schema is fully applied."""
    known = IMPLEMENTED_KEYWORDS | HANDLED_ELSEWHERE | ANNOTATIONS
    found = set()

    def visit(node):
        if not isinstance(node, dict):
            return
        found.update(k for k in node if k not in known)
        for key in ("properties", "$defs"):
            for sub in (node.get(key) or {}).values():
                visit(sub)
        for key in ("items", "contains"):
            visit(node.get(key))
        for key in ("oneOf", "allOf"):
            for sub in node.get(key) or []:
                visit(sub)

    visit(schema)
    return sorted(found)


class SchemaError(Exception):
    pass


def load_schema(path=DEFAULT_SCHEMA, lang="en"):
    """Read the schema and refuse one this validator cannot fully apply."""
    with open(path, encoding="utf-8") as fh:
        schema = json.load(fh)
    unknown = unsupported_keywords(schema)
    if unknown:
        raise SchemaError(msg(lang, "bad_schema", kw=", ".join(unknown)))
    return schema


def norm(text):
    """Whitespace- and case-insensitive comparison key for names typed twice."""
    return " ".join(str(text or "").split()).casefold()


def _obj(value):
    return value if isinstance(value, dict) else {}


def _filled(value):
    return isinstance(value, str) and bool(value.strip())


# ------------------------------------------------------- reading KPI wording
#
# These are heuristics on names and wording. They feed the denominator errors
# and the warnings; they never decide whether a metric is right for the test.

PER_RE = re.compile(r"başına|\bper\b", re.IGNORECASE)
RATE_RE = re.compile(r"\boran[ıi]?\b|\boranları\b|\brate\b|\bCR\b|\bCTR\b|%|\byüzde|\bshare\b|\bpay[ıi]\b", re.IGNORECASE)
COUNT_RE = re.compile(r"sayısı|adedi|\bcount\b|\bnumber\s+of\b", re.IGNORECASE)
# A "saw it" population: users who saw, were shown, viewed or were exposed to something, which can depend on B.
SAW_RE = re.compile(
    r"\bgör(?:en|üp|enler|dükten)|\bwho\s+(?:saw|see|viewed)\b|\bsaw\b|\bseen\b"
    r"|(?<!\w)(?:gösterilen|görüntüleyen|maruz\s+kalan)\s+(?:\w+\s+)?(?:kullanıcı|ziyaretçi|müşteri|kişi)"
    r"|\b(?:users?|visitors?|customers?|people)\s+(?:who\s+(?:were|are|was)\s+)?(?:shown|exposed|viewing)\b"
    r"|\b(?:shown|exposed|viewing)\s+(?:users?|visitors?|customers?)\b", re.IGNORECASE)
# A denominator field that also describes the numerator after a label ("…; pay: teklifi gösterilen ziyaretçiler"):
# the population checks read the part before it.
NUMERATOR_MARK_RE = re.compile(r"(?:^|(?<=[\s;,.(]))(?:pay|numerator)\s*:", re.IGNORECASE)
# The arm letter is matched case-sensitively ("B"), the words around it are not.
B_ONLY_RE = re.compile(r"(?i:yalnız(?:ca)?|sadece)\s+B\b|\bB\s+(?i:only)\b|(?i:\bonly)\s+(?:(?i:in)\s+)?B\b")
CHECK_NAME_RE = re.compile(r"kontrol|denetim|geçti\s*/\s*kaldı|\bcheck\b|pass\s*/\s*fail|\breview\b", re.IGNORECASE)
# The completion side of a complement pair: finishing a step or moving on to the next one ("Sepetten Ödemeye
# Geçiş Oranı" is 1 − "Sepet Terk Oranı" over one population).
COMPLETE_RE = re.compile(r"tamamlama|dönüşüm|kayıt|geçiş|ilerleme|ulaşma|completion|conversion|proceed|progression",
                         re.IGNORECASE)
ABANDON_RE = re.compile(r"terk\s+oran|abandon", re.IGNORECASE)
REGULATED_RE = re.compile(
    r"sigorta|emeklilik|kredi(?!\s+kart)|poliçe|\brıza|\bonay|insurance|pension|\bcredit\b(?!\s+card)|\bloan"
    r"|consent|KVKK", re.IGNORECASE)
REGULATED_CASED_RE = re.compile(r"\bBES\b")
# Mockup text holds every button and line of the screen, so a generic "onay" ("Siparişi onayla") would make any
# checkout look regulated: the mockup is read only for the strong signals below. A heuristic like the rest.
REGULATED_MOCKUP_RE = re.compile(
    r"KVKK|aydınlatma\s+metni|açık\s+rıza|sigorta|emeklilik|poliçe|kredi(?!\s+kart)|insurance|pension|privacy\s+notice"
    r"|\bconsent\b|\bloan", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]*>")
OVERCONFIDENT_RE = re.compile(
    r"\bkesin(?:likle)?\b|\bgaranti(?:dir)?\b|\bmutlaka\s+artırır\b|\bcertainly\b|\bguaranteed\b|\bwill\s+definitely\b",
    re.IGNORECASE)
WEAK_EVIDENCE = ("intuition", "sector")
# A sentence ends at . ! ? or … followed by space and a capital. The word before
# the stop is kept so an abbreviation ("ör.", "e.g.") doesn't count as an end.
SENTENCE_END_RE = re.compile(r"(\S*?)[.!?…]+[\"”’»)]*\s+(?=[\"“‘«(]*[A-ZÇĞİÖŞÜ])")
ABBREVIATIONS = frozenset(("ör", "örn", "vb", "vs", "bkz", "yy", "e.g", "i.e", "etc", "dr", "no"))


# ------------------------------------------------- what the change touches
#
# Keyword lists, not understanding (a heuristic, like everything in this
# section). Each list is matched case-insensitively at the start of a word: a
# Turkish entry is a stem that takes any suffix ("bağlantı" also reads
# "bağlantısının"), an English entry takes a plural at most ("tab" reads
# "tabs", never "table"). A hit decides which questions the record must answer
# (an accessibility warning, invariants, a guardrail on a benefit); it never
# decides that the answer is good, which is scenario-critic's call. A false
# positive costs one honest sentence; a false negative is the critic's to catch.

def keywords(stems=(), words=()):
    """One case-insensitive pattern for a keyword list (see above)."""
    def phrase(entry):
        return r"\s+".join(re.escape(part).replace("'", "['’]") for part in entry.split())
    parts = [phrase(s) + r"\w*" for s in stems] + [phrase(w) + r"(?:s|es)?(?!\w)" for w in words]
    return re.compile(r"(?<!\w)(?:%s)" % "|".join(parts), re.IGNORECASE)


# B changes something a user operates: rule 3 (accessibility warning) and rule 4 (invariants).
INTERACTIVE_TR = ("bağlantı", "link", "buton", "düğme", "dokun", "modal", "pop-up", "popup", "açılır pencere",
                  "alt sayfa", "diyalog", "iletişim kutusu",
                  "akordeon", "sekme", "karusel", "odak", "odağ", "form alanı", "alan", "onay kutusu", "menü",
                  "açılır liste")
INTERACTIVE_EN = ("button", "CTA", "tap", "overlay", "bottom sheet", "sheet", "dialog", "accordion", "tab", "toggle", "carousel", "slider", "focus",
                  "field", "input", "checkbox", "chip", "menu", "dropdown")
INTERACTIVE_RE = keywords(INTERACTIVE_TR, INTERACTIVE_EN)
# Words that start like an interactive one but mean attention, not keyboard focus.
NOT_INTERACTIVE = ("odaklan", "focus on")
# B changes a function both arms must keep working the same way: rule 4 (invariants).
FUNCTIONAL_TR = ("kupon", "indirim", "ödeme", "sepet", "filtre", "arama", "giriş", "kayıt", "form")
FUNCTIONAL_EN = ("coupon", "discount", "payment", "cart", "checkout", "filter", "search", "login", "signup",
                 "sign-up")
FUNCTIONAL_RE = keywords(FUNCTIONAL_TR, FUNCTIONAL_EN)
# Elements that take more accessibility criteria than a link or a button.
MODAL_RE = keywords(("modal", "pop-up", "popup", "açılır pencere", "alt sayfa", "diyalog", "iletişim kutusu"),
                    ("overlay", "bottom sheet", "sheet", "dialog"))
CAROUSEL_RE = keywords(("karusel",), ("carousel", "slider"))
AUTO_ADVANCE_RE = keywords(("otomatik", "kendiliğinden"), ("auto", "autoplay", "automatic", "automatically"))

# Two criteria are figures (rule 3): the touch target states a size with its unit (at least 44 pt or px, 48 dp;
# "44×44 pt", "48 dp") and the contrast a ratio (at least 4.5:1; "4,5:1", or a number right after "kontrast").
# A bare word ("dokunma alanı yeterli", "kontrast yüksek") states neither. A size next to a font, icon or spacing
# word ("yazı 16 px", "8 px boşluk") is not a target; a ratio next to a large-text or non-text word ("simgelerde
# 3:1") is WCAG's non-text criterion, never text contrast. Read like the rest: a heuristic on wording.
FIGURE_CLAUSE_RE = re.compile(r";|[,.](?!\d)")
RATIO_RE = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)?)\s*:\s*1(?![.,]?\d)")
CONTRAST_WORD_RE = re.compile(r"(?<!\w)(?:kontrast\w*|contrast)", re.IGNORECASE)
NUMBER_TOKEN_RE = re.compile(r"(?<![\w.,])%?\d+(?:[.,]\d+)*(?:\s*(?::|%|px|pt|dp|piksel|pixel))?", re.IGNORECASE)
PLAIN_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)?")
SIZE_RE = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)?)(?:\s*[×xX*]\s*(\d+(?:[.,]\d+)?))?\s*(pt|dp|px|piksel|pixels?)(?!\w)",
                     re.IGNORECASE)
TARGET_MINIMUM = {"dp": 48}  # every other unit: 44 (pt, CSS px)
NOT_TARGET_RE = keywords(("yazı", "punto", "harf", "satır", "boşluk", "aralık", "mesafe", "simge", "ikon"),
                         ("font", "font size", "text size", "line height", "spacing", "gap", "margin", "padding",
                          "icon", "letter"))
NON_TEXT_RE = keywords(("büyük metin", "büyük yazı", "simge", "ikon", "kenarlık", "çerçeve", "odak gösterge",
                        "odak halka", "metin dışı", "metin olmayan", "bileşen", "grafik"),
                       ("large text", "icon", "border", "outline", "focus indicator", "focus ring", "non-text",
                        "component", "graphic", "boundary", "boundaries"))


def _figure_value(text):
    return float(text.replace(",", "."))


def _near(text, start, end, regex, before, after):
    """`regex` among the `before` words before text[start:end] and the `after` words after it, inside its clause."""
    left = FIGURE_CLAUSE_RE.split(text[:start])[-1].split()[-before:]
    right = FIGURE_CLAUSE_RE.split(text[end:])[0].split()[:after]
    return bool(regex.search(" ".join(left) + " | " + " ".join(right)))


def contrast_figures(text):
    """(figure, value, meets 4.5:1) of every contrast ratio the text states, non-text ratios left out."""
    out = []
    for m in RATIO_RE.finditer(text):
        if not _near(text, m.start(), m.end(), NON_TEXT_RE, 5, 2):
            value = _figure_value(m.group(1))
            out.append((" ".join(m.group(0).split()), value, value >= 4.5))
    for m in CONTRAST_WORD_RE.finditer(text):  # "kontrast oranı en az 4.5": the first number after the word
        window = FIGURE_CLAUSE_RE.split(text[m.end():m.end() + 40])[0]
        n = NUMBER_TOKEN_RE.search(window)
        if n and PLAIN_NUMBER_RE.fullmatch(n.group(0)) and not _near(text, m.start(), m.end(), NON_TEXT_RE, 5, 0):
            value = _figure_value(n.group(0))
            out.append((n.group(0), value, value >= 4.5))
    return out


def target_figures(text):
    """(figure, value, meets the minimum) of every touch-target size the text states."""
    out = []
    for m in SIZE_RE.finditer(text):
        if _near(text, m.start(), m.end(), NOT_TARGET_RE, 3, 1):
            continue
        value = min(_figure_value(m.group(1)), _figure_value(m.group(2) or m.group(1)))
        unit = m.group(3).lower()
        out.append((" ".join(m.group(0).split()), value, value >= TARGET_MINIMUM.get(unit, 44)))
    return out


class FigureCriterion(object):
    """A criterion stated as a figure. search() reads like a compiled pattern's (build_card reads these criteria
    too): a stated figure that meets the threshold, or None. below() is the first stated figure under it: always
    for contrast (a 3:1 beside a 4.5:1 is named), only when none meets it for a target (a spacing or icon size
    beside the target is no error)."""

    def __init__(self, figures, name_any_lower):
        self.figures, self.name_any_lower = figures, name_any_lower

    def search(self, text):
        return next((f for f in self.figures(text) if f[2]), None)

    def below(self, text):
        figures = self.figures(text)
        if not self.name_any_lower and any(f[2] for f in figures):
            return None
        return next((f[0] for f in figures if not f[2]), None)


# The criteria an 'accessibility' warning states (rule 3), as (Turkish label,
# English label, what counts as stating it). Code sees that the threshold or
# the word is there; whether the criterion fits the element is the critic's.
A11Y_BASE = (
    ("dokunma alanı (en az 44×44 pt / 48×48 dp)", "touch target (at least 44×44 pt / 48×48 dp)",
     FigureCriterion(target_figures, name_any_lower=False)),
    ("metin kontrastı (en az 4.5:1)", "text contrast (at least 4.5:1)",
     FigureCriterion(contrast_figures, name_any_lower=True)),
    ("klavyeyle erişim", "keyboard access", re.compile(r"klavye|keyboard", re.IGNORECASE)),
    ("ekran okuyucunun okuduğu ad", "a name screen readers announce",
     re.compile(r"ekran\s+okuyucu|screen[\s-]+reader", re.IGNORECASE)),
)
A11Y_THRESHOLD_LABELS = {  # what the below-threshold message calls each figure criterion: (TR, EN) what, need
    A11Y_BASE[0][2]: (("dokunma alanı", "44×44 pt / 48×48 dp"), ("touch target", "44×44 pt / 48×48 dp")),
    A11Y_BASE[1][2]: (("metin kontrastı", "4.5:1 (daha düşük bir oran yalnızca büyük metin ya da metin dışı öğeler "
                                          "için, onun yanında yazılır)"),
                      ("text contrast", "4.5:1 (a lower ratio only for large text or non-text parts, beside it)")),
}
A11Y_MODAL = (
    ("açılınca odağı alması", "taking focus when it opens", re.compile(r"odak|odağ|focus", re.IGNORECASE)),
    ("görünür bir kapat düğmesi", "a visible close control", re.compile(r"kapat|kapan|close|dismiss", re.IGNORECASE)),
    ("Esc ile kapanması", "closing with Esc", re.compile(r"\besc\b|escape", re.IGNORECASE)),
)
A11Y_AUTO_ADVANCE = (
    ("durdurulabilmesi", "a way to pause it", re.compile(r"durdur|duraklat|pause", re.IGNORECASE)),
)

# Rule 3: a revenue primary on a change to a user benefit can read the lost
# benefit as a win (hide a coupon field and code holders pay full price), so
# the guardrail watches that benefit. Grouped by benefit: "indirim kodu" in
# the change is answered by a "Kupon Kullanım Oranı" guardrail.
REVENUE_RE = keywords(("gelir", "sepet tutar", "sipariş tutar", "marj"), ("RPV", "AOV", "revenue", "margin"))
BENEFIT_FAMILIES = (
    keywords(("kupon", "indirim kodu", "promosyon kodu", "kampanya kodu", "hediye çeki"),
             ("coupon", "voucher", "promo code", "discount code", "gift card")),
    keywords(("ücretsiz kargo",), ("free shipping",)),
    keywords(("iade",), ("refund",)),
    keywords(("iptal",), ("cancel", "cancellation")),
)
# A discount or campaign the page simply shows is not at risk when B shows it
# more ("Yıllık (%20 indirim)" made the default): only a B that hides, removes,
# shrinks or moves it out of the way can let revenue rise from users missing it.
OFFER_BENEFIT = keywords(("indirim", "kampanya", "promosyon"), ("discount", "promo", "promotion"))
REDUCES_RE = re.compile(
    r"gizle|kaldır|arkasın|katla|daralt|küçült|sakla|geri\s+plan|kapat|bağlantıya|"
    r"\bhid(?:e|es|den|ing)\b|remov|\bbehind\b|collaps|\bfold|shrink|smaller|de-?emphas", re.IGNORECASE)

# Rule 6: urgency and scarcity in B or the mechanism is proposed only when the
# signal rests on real data, which a 'regulation' warning names.
URGENCY_RE = keywords(
    ("tükeniyor", "tükenmek üzere", "sınırlı stok", "sınırlı sayıda", "sınırlı süre", "stokta son", "düşük stok",
     "son fırsat", "son şans", "son gün", "az kaldı", "acele", "kaçırma", "geri sayım", "bitiyor", "sona eriyor",
     "kişi bakıyor", "kişi inceliyor", "kişi görüntülüyor"),
    ("hurry", "limited stock", "limited time", "low stock", "left in stock", "selling fast", "almost gone",
     "ends soon", "ending soon", "ends today", "countdown", "timer", "last chance", "don't miss",
     "people are viewing", "people are looking", "people are watching"))
URGENCY_COUNT_RE = re.compile(r"(?<!\w)(?:yalnızca|sadece|son)\s+\d+\s+(?:\w+\s+)?kaldı|\bonly\s+\d+\s+left\b",
                              re.IGNORECASE)
DATA_SOURCE_RE = keywords(("stok", "envanter", "gerçek"), ("verified", "inventory", "real"))

# Rules 8 and 10: the archive is a library of ideas, not a log of wins, so a
# result ("tested", "proven", a win) or a chance or uplift figure needs the
# user's own data, and a guarantee needs more than any data can give. Turkish
# negation is in the verb ("test edilmedi" is not a hit); English negation is
# a word before it ("not tested on this page" is not a claim either).
# Rule 5: statistics are out of scope, so no record field states one. Read in the
# record's own text only: `detail` repeats archive KPI questions ("anlamlı
# artıyor mu") and the mockups are page copy. A heuristic like the lists above.
STATISTICS_RE = re.compile(
    r"\bp\s*-?\s*(?:değeri|value)\b|\bp\s*[<≤]\s*0?[.,]\d|istatistiksel(?:\s+olarak)?\s+anlamlı|anlamlılık"
    r"|statistical(?:ly)?\s+significan|\bsignificance\b|örneklem|sample\s+size|güç\s+analiz|power\s+analysis"
    r"|istatistiksel\s+güç|statistical\s+power|güven\s+aralığı|confidence\s+interval|credible\s+interval|bayes"
    r"|(?-i:\bMDE\b|\bSRM\b|CUPED|\bA/A\b|\bICE\b)|ICE\s+(?:puan|skor|score)", re.IGNORECASE)
# "tested with a screen reader" describes a check, not a result.
OVERCLAIM_RE = re.compile(
    r"(?<!\w)(?:kanıtlanmış(?:tır)?|kanıtlandı|test\s+edilmiş(?:tir)?|test\s+edildi(?:ği)?|kazanmış(?:tır)?"
    r"|kazandı(?:ğı)?|işe\s+yaradığı\s+biliniyor|proven|tested(?!\s+(?:with|using|by|before|against|for)\b)"
    r"|known\s+to\s+work|won)(?![\w'’])",
    re.IGNORECASE)

# ---- result and impact claims (rules 8 and 10; contract: methodology.md → Claims and evidence)
#
# A claim is a number (%, yüzde, percent, a multiplier: 2x, 2 kat) tied to an
# outcome or chance word (artış/artar/arttı, yükselir, düşer, azalır, kazan…,
# olasılık, ihtimal; lift, rise, raise, grow, boost, drop, chance, probability,
# win …) in either order, at most CLAIM_WINDOW words apart inside one clause, or
# a phrase that borrows a result ("benzer testlerde", "similar tests", "other
# companies saw") or the archive's ("arşivde kazanmış"). Read in every
# free-text field of the record (claim_fields), never in `detail` (archive KPI
# questions) or `card` (page copy). Not claims: a figure the page shows (a
# number next to a price, a discount, a threshold or a design property), an
# observed baseline rate with no outcome word ("formu açanların %58'i çıkıyor"),
# a hypothesis without a number. Who may carry one: claim_exempt(). A number
# and an outcome word further apart, and vague magnitudes ("ciddi artış"), are
# warnings for the reviewer (--strict: errors). A heuristic, like the rest.
CLAIM_WINDOW = 3
CLAIM_NUM_RE = re.compile(
    r"(?<![\w.,])(?:%\s?\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s?%"
    r"|yüzde\s+(?:\d+(?:[.,]\d+)?|on|yirmi|otuz|kırk|elli|altmış|yetmiş|seksen|doksan|yüz|beş|iki|üç|dört|altı"
    r"|yedi|sekiz|dokuz)(?!\w)"
    r"|\d+(?:[.,]\d+)?\s*(?:percent|per\s+cent|percentage\s+points?|pp|yüzde\s+puan)(?!\w)"
    r"|(?P<mult>\d+(?:[.,]\d+)?[x×](?![\w×])|(?:\d+|iki|üç|dört|beş)\s+kat(?:ı|ına)?(?!\w)))"
    r"(?:['’](?P<suffix>\w+))?",
    re.IGNORECASE)
# A number right next to one of these is a figure on the page, not an outcome.
PAGE_FIGURE_BEFORE_RE = re.compile(
    r"^(?:fiyat|ücret|indirim|kampanya|faiz|komisyon|taksit|prim|aidat|kargo|vergi|kdv|eşik|eşiğ|kontrast|boyut"
    r"|punto|yazı|font|genişlik|yükseklik|opaklık|yakınlaştır|price|fee|discount|shipping|interest|tax|threshold"
    r"|contrast|size|width|height|opacity|zoom|text)\w*$", re.IGNORECASE)
PAGE_FIGURE_AFTER_RE = re.compile(
    r"^(?:indirim|kampanya|faiz|komisyon|taksit|vergi|kdv|cashback|off|discount|ucuz|cheaper|kontrast|contrast"
    r"|zoom|yakınlaştır)\w*$", re.IGNORECASE)
# Turkish outcome verbs: a stem and its suffix, read by tr_outcome().
TR_OUTCOME_RE = re.compile(
    r"(?<!\w)(kazandır|iyileştir|yükselt|yüksel|artır|art|düşür|düş|azalt|azal|kazan|iyileş|katla|büyü)(\w*)",
    re.IGNORECASE)
TR_ALLOWED_SUFFIX = {  # stems that are also other words: only these suffixes make the outcome verb
    "art": ("ış", "ar", "tı", "tığ", "tır", "abil", "acak", "acağ", "ma", "ıyor", "mış"),
    "düş": ("er", "üş", "tü", "tüğ", "ebil", "ecek", "eceğ", "me", "üyor", "müş"),
    "büyü": ("r", "me", "dü", "yor", "yecek", "yebil", "müş"),
}
TR_CAUSATIVE = ("kazandır", "iyileştir", "yükselt", "artır", "düşür", "azalt")
TR_NEGATIVE_RE = re.compile(r"^m[ae](?:z|d[ıi]|y[ae]c[ae]|m[ıi]ş|y[ae]bil|m[ae]l)")
TR_PAST_RE = re.compile(r"^(?:[td][ıiuü](?!r)|m[ıiuü]ş)")
TR_FUTURE_RE = re.compile(r"^(?:[aeıiuü]?r|y?[ae]c[ae][kğ]|y?[ae]bil)")  # aorist, future, potential
EN_OUTCOME_RE = re.compile(
    r"(?<!\w)(lift(?:s|ed|ing)?|uplifts?|increas(?:e|es|ed|ing)|ris(?:e|es|ing)|rose|rais(?:e|es|ed|ing)"
    r"|grow(?:s|n|ing|th)?|grew|boost(?:s|ed|ing)?|drop(?:s|ped|ping)?(?![\s-]*(?:off|out|down)\b)"
    r"|reduc(?:e|es|ed|ing|tion)|decreas(?:e|es|ed|ing)|improv(?:e|es|ed|ing|ement)|win(?:s|ning)?|won"
    r"|beat(?:s|ing)?|doubl(?:e|es|ed|ing)|tripl(?:e|es|ed|ing))(?!\w)", re.IGNORECASE)
EN_PAST = frozenset(("lifted", "increased", "rose", "raised", "grew", "grown", "boosted", "dropped", "reduced",
                     "decreased", "improved", "won", "doubled", "tripled"))
EN_PRESENT = frozenset(("lifts", "increases", "rises", "raises", "grows", "boosts", "drops", "reduces", "decreases",
                        "improves", "wins", "beats", "doubles", "triples"))
CHANCE_WORD_RE = re.compile(
    r"(?<!\w)(?:olasılı\w*|ihtimal\w*|şans\w*|chances?|probabilit(?:y|ies)|likel(?:y|ihood)|odds)(?!\w)",
    re.IGNORECASE)
# Only right after the number: "%12 daha fazla", "20% more" ("%20’den fazla" is "more than", not an uplift).
CLAIM_ADJACENT_RE = re.compile(r"\s+(?:daha\s+)?(?:fazla|iyi)(?!\w)|\s+(?:more|higher|lower|fewer|less|better)(?!\w)",
                               re.IGNORECASE)  # used with .match(text, pos)
MODAL_BEFORE_RE = re.compile(r"(?:\b(?:will|would|can|could|may|might|should|to)|['’]ll)(?:\s+\w+)?\s+$", re.IGNORECASE)
ESTIMATE_RE = re.compile(
    r"(?<!\w)(?:beklen\w*|tahmin\w*|öngör\w*|olur|olacak\w*|olabilir|expected|expects?|estimat\w*|projected"
    r"|projection\w*|forecast\w*|predict\w*|anticipat\w*|will|would)(?!\w)", re.IGNORECASE)
# A chance claim needs no number.
CHANCE_PHRASE_RE = re.compile(
    r"(?<!\w)(?:kazanma\s+(?:olasılı|ihtimal|şans)\w*|büyük\s+(?:bir\s+)?ihtimalle\s+kazan\w*"
    r"|(?:chances?|probability|odds|likelihood)\s+(?:of|to)\s+(?:winning|win|beat\w*)|likely\s+to\s+(?:win|beat)"
    r"|win(?:ning)?\s+(?:probability|chance)s?|probability\s+to\s+be\s+best)(?!\w)", re.IGNORECASE)
# Another test's result, with or without a number.
SIMILAR_RE = re.compile(
    r"(?<!\w)(?:benzer\s+(?:test|deney|denem|kampanya)\w*"
    r"|(?:başka|diğer)\s+(?:şirket|marka|site|firma|ekip|mağaza)\w*\s+(?:\w+\s+){0,4}?"
    r"(?:art|yüksel|düş|azal|kazan|gör|elde|sonuç)\w*"
    r"|(?:önceki|geçmiş)\s+(?:test|deney)\w*\s+(?:\w+\s+){0,3}?(?:art|yüksel|kazan|göster|kanıtla)\w*"
    r"|similar\s+(?:tests?|experiments?|campaigns?)"
    r"|other\s+(?:companies|brands|sites|retailers|teams|stores)\s+(?:\w+\s+){0,3}?"
    r"(?:saw|see|seen|got|found|reported|achieved|lifted|increased|won|gained)"
    r"|(?:previous|past|prior|earlier)\s+(?:tests?|experiments?)\s+(?:\w+\s+){0,3}?"
    r"(?:showed|show|lifted|won|increased|proved))(?!\w)", re.IGNORECASE)
# The archive as proof: never, whatever the evidence (rule 8).
ARCHIVE_PROOF_RE = re.compile(
    r"(?<!\w)(?:arşiv\w*\s+(?:\w+\s+){0,3}?(?:kazan\w*|işe\s+yara\w*|başarılı\w*|kanıtla\w*|sonuç\s+ver\w*)"
    r"|archive\s+(?:winners?|wins?)|(?:won|worked|proven)\s+in\s+the\s+archive|archive\s+(?:shows|proves))(?!\w)",
    re.IGNORECASE)
DOUBLE_RE = re.compile(r"(?<!\w)(?:doubl(?:e|es|ed|ing)|tripl(?:e|es|ed|ing)|ikiye\s+katla\w*|katına\s+çık\w*)(?![\w-])",
                       re.IGNORECASE)
METRIC_NOUN_RE = re.compile(
    r"(?<!\w)(?:conversions?|signups?|sign-ups|sales|orders|revenue|purchases|clicks|leads|registrations"
    r"|subscriptions|bookings|CR|CTR|RPV|AOV|sipariş\w*|satış\w*|gelir\w*|dönüşüm\w*|kayıt\w*|kaydı\w*|talep\w*"
    r"|tıklama\w*|abonelik\w*|ciro\w*)(?!\w)", re.IGNORECASE)
CLAIM_VAGUE_RE = re.compile(
    r"(?<!\w)(?:çok\s+daha\s+(?:fazla|yüksek|iyi)|(?:ciddi|belirgin|büyük|kayda\s+değer)\s+(?:bir\s+)?"
    r"(?:artış|düşüş|kazanç|iyileşme|sıçrama)\w*|dramatik\w*|katlanarak|much\s+(?:more|higher|better)"
    r"|significantly\s+(?:more|higher|better|increas\w*|improv\w*|lift\w*)"
    r"|substantial(?:ly)?\s+(?:more|higher|lift|increase|uplift|gain)|dramatic(?:ally)?"
    r"|(?:huge|massive|big)\s+(?:lift|increase|uplift|gain))(?!\w)", re.IGNORECASE)
# "<source> raporuna göre …", "GA4’e göre …", "according to …", "<source> reports …".
ATTRIBUTION_RE = re.compile(
    r"(?<!\w)(?:(?:rapor|araştırma|çalışma|anket|veri|analiz|ölçüm|panel|kayıt|test|deney)\w*\s+göre"
    r"|according\s+to|reports?|reported|found\s+that|shows?\s+that|bildir\w*|belirt\w*|raporla\w*)(?!\w)",
    re.IGNORECASE)
ATTRIBUTION_PROPER_RE = re.compile(r"(?<!\w)[A-ZÇĞİÖŞÜ0-9][\w.-]*(?:['’]\w+)?\s+göre(?!\w)")
# evidence.note names its source: a source word, or a proper name (GA4, Hotjar, Baymard …).
SOURCE_WORD_RE = re.compile(
    r"(?<!\w)(?:rapor|report|veri|data|panel|dashboard|analiz|analytics|anket|survey|export|ölçüm|kayıt|log|araç"
    r"|tool|huni|funnel|test|deney|experiment|araştırma|çalışma|study|research|kaynak|source)", re.IGNORECASE)
SOURCE_PROPER_RE = re.compile(r"(?<=\s)[A-ZÇĞİÖŞÜ][\w-]+|(?<!\w)[A-Z]{2,}\w*|(?<!\w)[A-Za-z]+\d\w*")
CLAUSE_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+")
# A guarantee is never written. Only the claim is matched: "garanti" alone is
# also a warranty ("iade garantisi"), which a scenario may well be about.
NEVER_CLAIM_RE = re.compile(
    r"\bgaranti\s+(?:eder|ediyor|edecek|eden|edilir|edilen|edilmiş(?:tir)?)(?!\w)|\bgarantidir\b|\bguaranteed\b"
    r"|\bguarantees?\s+(?:a|an|the|that|more|higher)\b|\bwill\s+guarantee\b",
    re.IGNORECASE)
NEGATION_BEFORE_RE = re.compile(r"(?:\b(?:not|never|no|without)|n['’]t)(?:\s+\w+){0,2}\s+$", re.IGNORECASE)
NEGATION_AFTER_RE = re.compile(r"\s+değil", re.IGNORECASE)
# Rule 10 (contract: mockup-style.md → Numbers the mockup needs but must not invent): numeric_change silences
# the builder's numbers gate, so it says where the figure comes from: the page, the user, or how it was derived
# ("1.500 − 1.230 = 270"). Without that, a critical assumption about the figure (one sharing a number with it, or
# naming a price, amount, rate …) holds it open. "A’ya göre" compares the arms, it names no source.
NUMERIC_SOURCE_RE = re.compile(
    r"(?<!\w)(?:sayfa(?:da|daki|dan|nın|ndaki|ya)|ekran(?:da|daki|dan)|ekran\s+görüntüs\w*"
    r"|kullanıcının\s+(?:verdiği|paylaştığı|ilettiği|yazdığı|gönderdiği|veri\w*)|verilen|paylaşılan|iletilen"
    r"|hesapla\w*|türetil\w*|çıkarıl\w*|bölün\w*|çarpıl\w*|toplanarak"
    r"|(?<!A['’]ya\s)(?<!B['’]ye\s)(?<!koluna\s)göre"
    r"|from\s+the\s+(?:page|screen|screenshot)|on\s+the\s+(?:page|screen|screenshot)"
    r"|the\s+page\s+(?:shows|lists|states|gives)|user\s+(?:gave|shared|provided|supplied)|given|provided|supplied"
    r"|deriv\w*|comput\w*|calculat\w*|according\s+to|based\s+on)(?!\w)"
    r"|[=×÷]|\d\s*[−\-/x*]\s*\d", re.IGNORECASE)
FIGURE_WORD_RE = keywords(("fiyat", "tutar", "ücret", "indirim", "oran", "rakam", "eşik", "değer", "prim", "taksit",
                           "faiz", "komisyon", "kargo", "bedel", "aidat"),
                          ("price", "pricing", "amount", "figure", "fee", "rate", "discount", "threshold", "number",
                           "value", "cost", "total"))
FIGURE_NUMBER_RE = re.compile(r"\d+(?:[.,]\d+)*")
# Evidence levels that must say what they rest on (rule 10).
NOTED_EVIDENCE = ("user_data", "sector")

# The title's business outcome against the primary's family (a warning only:
# titles are free text). An abandonment question decided by revenue can read a
# lost benefit as a win; a revenue question decided by a completion rate
# answers another question.
TITLE_EXIT_RE = keywords(("terk", "çıkış", "tamamla"), ("abandon", "abandonment", "exit", "completion"))

_GLOSSARY = []  # loaded once, on first use: [glossary dict or None]


def _glossary():
    if not _GLOSSARY:
        try:
            import validate_scenarios
            _GLOSSARY.append(validate_scenarios.load_glossary())
        except Exception:  # the glossary is optional; without it nothing is exempted
            _GLOSSARY.append(None)
    return _GLOSSARY[0]


def _in_glossary(name):
    glossary = _glossary()
    if not glossary:
        return False
    import validate_scenarios
    return validate_scenarios.glossary_status(" ".join(str(name).split()), glossary) != "missing"


# ------------------------------------------------ what a KPI name means (rule 2)
#
# One KPI name has one meaning across scenarios: the glossary's canonical name
# fixes its denominator family. A denominator is read into families by its
# words (a heuristic): "Teste atanan ziyaretçi (atama sepete ulaşınca)" is the
# assigned population (+ a trigger), "Tamamlanan sipariş" an order population.
# An assigned word dominates: "Kasko teklif formunu açıp teste atanan ziyaretçi"
# is assigned visitors, the rest qualifies when they were assigned.

GLOSSARY_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "knowledge",
                                              "kpi-glossary.md"))
FAMILY_RES = (
    ("assigned", re.compile(r"(?<!\w)(?:atan\w*|atama\w*|assign\w*|randomi[sz]\w*)", re.IGNORECASE)),
    ("trigger", re.compile(r"(?<!\w)(?:ulaş\w*|reach\w*|tetik\w*|trigger\w*)", re.IGNORECASE)),
    ("order", re.compile(r"(?<!\w)(?:sipariş\w*|orders?\b|satın\s+al\w*|purchase\w*|alıcı\w*|buyers?\b)",
                         re.IGNORECASE)),
    ("request", re.compile(r"(?<!\w)(?:talep\w*|taleb\w*|başvuru\w*|leads?\b|requests?\b|applications?\b|fırsat\w*"
                           r"|opportunit\w*|inquir\w*)", re.IGNORECASE)),
    ("quote", re.compile(r"(?<!\w)(?:teklif\w*|quotes?\b)", re.IGNORECASE)),
    ("session", re.compile(r"(?<!\w)(?:oturum\w*|sessions?\b)", re.IGNORECASE)),
)
FAMILY_LABEL = {"assigned": ("atanan ziyaretçi/kullanıcı", "assigned visitor/user"), "order": ("sipariş", "order"),
                "request": ("talep", "request/lead"), "quote": ("teklif", "quote"), "session": ("oturum", "session"),
                "trigger": ("bir tetiğe ulaşan", "reached-a-trigger")}
POST_ASSIGNMENT = frozenset(("order", "request", "quote"))
BARE_VISITOR_RE = re.compile(r"(?:tüm\s+|all\s+)?(?:mobil\s+|mobile\s+|yeni\s+|new\s+)?"
                             r"(?:ziyaretçi\w*|kullanıcı\w*|müşteri\w*|visitors?|users?|customers?)", re.IGNORECASE)
# A name that encodes a population conditioned on a step after assignment.
CONDITIONAL_NAME_RE = re.compile(
    r"→|->|(?<!\w)(?:teklif|sipariş|talep|sepet|deneme|kayıt|başvuru)\w*\s+başına(?!\w)"
    r"|(?<!\w)per\s+(?:orders?|quotes?|requests?|trials?|sign-?ups?|leads?|applications?|purchases?|carts?)(?!\w)"
    r"|(?<!\w)(?:among|arasında)(?!\w)", re.IGNORECASE)
NAME_ASSIGNED_RE = re.compile(
    r"atanan\s+(?:\w+\s+){0,2}?(?:ziyaretçi|kullanıcı|müşteri)\w*\s+başına|per\s+assigned\s+(?:visitor|user|customer)s?",
    re.IGNORECASE)
# Realized revenue against a normalized value (SaaS annual plans).
REALIZED_REVENUE = ("Ziyaretçi Başına Gelir (RPV)", "Ziyaretçi Başına Net Gelir")
NORMALIZED_RE = re.compile(
    r"normali[sz]\w*|aylığa\s+(?:çevr|normali|indirge|böl)\w*|aylık\s+karşılı\w*|monthly[\s-]+equivalent"
    r"|annuali[sz]ed|yıllığa\s+çevr\w*", re.IGNORECASE)

_GLOSSARY_ROWS = []  # loaded once: [{canonical: {"definition", "payda", "synonyms"}} or {}]


def glossary_rows(path=GLOSSARY_FILE):
    """Every glossary row: {canonical name: {"definition", "payda", "synonyms"}}.

    The table format validate_scenarios.py reads: | **Name** | Tanım | Payda | syn; syn |.
    """
    if path != GLOSSARY_FILE or not _GLOSSARY_ROWS:
        rows = {}
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
                    if len(cells) < 4 or not cells[0].startswith("**"):
                        continue
                    rows[cells[0].strip("*").strip()] = {
                        "definition": cells[1], "payda": cells[2],
                        "synonyms": [s.strip() for s in cells[3].split(";") if s.strip() and s.strip() != "-"]}
        if path != GLOSSARY_FILE:
            return rows
        _GLOSSARY_ROWS.append(rows)
    return _GLOSSARY_ROWS[0]


def _strip_window(name):
    """'Kayıt Oranı (7 gün)' → 'Kayıt Oranı': one trailing parenthetical (a window, a population)."""
    return re.sub(r"\s*\([^()]*\)\s*$", "", name)


_GLOSSARY_INDEX = []


def glossary_canonical(name):
    """The canonical glossary name `name` stands for (itself, a synonym, either
    with a trailing window or population stripped), or None."""
    if not _GLOSSARY_INDEX:
        exact, stripped = {}, {}
        for canon, row in glossary_rows().items():
            for label in [canon] + row["synonyms"]:
                exact.setdefault(fold_tr(label), canon)
                key = fold_tr(_strip_window(label))
                stripped[key] = canon if stripped.get(key, canon) == canon else None  # None: ambiguous
        _GLOSSARY_INDEX.append((exact, stripped))
    exact, stripped = _GLOSSARY_INDEX[0]
    for key in (fold_tr(name), fold_tr(_strip_window(name))):
        if key in exact:
            return exact[key]
    return stripped.get(fold_tr(_strip_window(name)))


def families(text):
    """The population families a denominator names (empty: unknown)."""
    found = {family for family, regex in FAMILY_RES if regex.search(str(text or ""))}
    if "assigned" in found:
        return {"assigned"} | (found & {"trigger"})
    return found


def families_compatible(glossary, record):
    """A record's denominator family fits the glossary's: they share one, or a
    trigger logged in both arms narrows an assigned population (triggered analysis)."""
    if not glossary or not record or glossary & record:
        return True
    return "assigned" in glossary and record <= {"trigger"}


def _family_label(fams, lang):
    idx = 1 if lang == "en" else 0
    return " + ".join(FAMILY_LABEL[f][idx] for f in sorted(fams))


def kpi_meaning_entries(scenario):
    """(path, name, denominator) of the KPI lines whose name and denominator are both written."""
    out = []
    primary, guardrail = _obj(scenario.get("primary_kpi")), _obj(scenario.get("guardrail"))
    if isinstance(primary.get("name"), str) and _filled(primary.get("denominator")):
        out.append(("primary_kpi", primary["name"], primary["denominator"]))
    if guardrail.get("kind") == "metric" and isinstance(guardrail.get("name"), str) \
            and _filled(guardrail.get("denominator")):
        out.append(("guardrail", guardrail["name"], guardrail["denominator"]))
    kpis = _obj(scenario.get("detail")).get("kpis")
    for i, k in enumerate(kpis if isinstance(kpis, list) else []):
        if isinstance(k, dict) and isinstance(k.get("name"), str) and _filled(k.get("denominator")):
            out.append(("detail.kpis[%d]" % i, k["name"], k["denominator"]))
    return out


def check_kpi_meaning(scenario, errors, lang="tr"):
    """Rule 2: a KPI's name and denominator measure the same thing, and a
    canonical glossary name keeps the glossary's meaning."""
    rows = glossary_rows()
    for path, name, den in kpi_meaning_entries(scenario):
        rec = families(den)
        if NAME_ASSIGNED_RE.search(name) and "assigned" not in rec and rec & POST_ASSIGNMENT:
            errors.append(msg(lang, "kpi_mismatch_reverse", path=path, name=name, den=den,
                              fam=_family_label(rec & POST_ASSIGNMENT, lang)))
            continue
        canon = glossary_canonical(name)
        row = rows.get(canon) if canon else None
        glossary_fams = families(row["payda"]) if row else set()
        if glossary_fams:
            if not families_compatible(glossary_fams, rec):
                definition = re.split(r"[;.]\s", row["definition"], maxsplit=1)[0].rstrip(".")
                hint = msg(lang, "kpi_trigger_hint") if glossary_fams == {"trigger"} and rec == {"assigned"} else ""
                errors.append(msg(lang, "kpi_glossary_family", path=path, name=name, canon=canon, hint=hint,
                                  definition=definition, payda=row["payda"],
                                  gfam=_family_label(glossary_fams, lang), den=den, rfam=_family_label(rec, lang)))
                continue
        else:
            hit = CONDITIONAL_NAME_RE.search(name)
            bare = BARE_VISITOR_RE.fullmatch(_strip_window(" ".join(den.split())))
            if hit and ("assigned" in rec or bare):
                errors.append(msg(lang, "kpi_mismatch", path=path, name=name, word=hit.group(0), den=den))
                continue
        if canon in REALIZED_REVENUE:
            word = NORMALIZED_RE.search(name + " " + den)
            if word:
                errors.append(msg(lang, "kpi_normalized_revenue", path=path, name=name, word=word.group(0)))


def sentence_count(text):
    """How many sentences `text` holds, by its stops (a heuristic)."""
    ends = [m for m in SENTENCE_END_RE.finditer(text.strip())
            if m.group(1).lstrip("(“\"‘«[").casefold() not in ABBREVIATIONS]
    return len(ends) + 1


def denominator_of(name, field=None):
    """The denominator a KPI line states, normalised, or '' when it states none.

    "… Oranı (sepete ulaşan kullanıcı başına, 30 gün)" → "sepete ulaşan kullanıcı".
    A parenthesis that only gives a window or an abbreviation is not one.
    """
    if isinstance(field, str) and field.strip():
        return norm(field)
    text = str(name or "")
    m = re.search(r"([^(),;]*?)\s+başına", text, re.IGNORECASE)
    if m:
        return norm(m.group(1))
    m = re.search(r"\bper\s+([^(),;]+)", text, re.IGNORECASE)
    if m:
        return norm(m.group(1))
    return ""


def record_entries(scenario):
    """primary_kpi and guardrail as KPI lines the complement check reads."""
    out = []
    for path, role in (("primary_kpi", "primary"), ("guardrail", "guardrail")):
        k = _obj(scenario.get(path))
        if isinstance(k.get("name"), str):
            out.append({"path": path, "role": role, "name": k["name"], "denominator": k.get("denominator"),
                        "question": None, "is_check": k.get("kind") == "check"})
    return out


def detail_entries(scenario):
    """The detail view's KPI lines as the name checks read them."""
    kpis = _obj(scenario.get("detail")).get("kpis")
    out = []
    for i, k in enumerate(kpis if isinstance(kpis, list) else []):
        if not isinstance(k, dict) or not isinstance(k.get("name"), str):
            continue
        out.append({"path": "detail.kpis[%d]" % i, "role": k.get("role"), "name": k["name"],
                    "denominator": k.get("denominator"), "question": k.get("question"),
                    "is_check": bool(CHECK_NAME_RE.search(k["name"]))})
    return out


def population_problems(kpi, path, lang="tr"):
    """A record KPI's denominator is a population present in both arms: not a
    count, not the users who saw the change, not a B-only population. "Saw"
    and "B only" are read in the name too ("Gören kullanıcı başına …").
    Errors on the primary and on a metric guardrail."""
    out = []
    den = kpi.get("denominator")
    if isinstance(den, str):
        den = NUMERATOR_MARK_RE.split(den, maxsplit=1)[0].rstrip(" ;,.(")
        if COUNT_RE.search(den):
            out.append(msg(lang, "denominator_count", path=path + ".denominator", val=den))
        if SAW_RE.search(den):
            out.append(msg(lang, "denominator_saw", path=path + ".denominator", val=den))
        if B_ONLY_RE.search(den):
            out.append(msg(lang, "denominator_b_only", path=path + ".denominator", val=den))
    name = kpi.get("name")
    if isinstance(name, str):
        if SAW_RE.search(name):
            out.append(msg(lang, "denominator_saw", path=path + ".name", val=name))
        if B_ONLY_RE.search(name):
            out.append(msg(lang, "denominator_b_only", path=path + ".name", val=name))
    return out


def kpi_name_problems(entries, lang="tr", glossary_ok=False):
    """Denominator rules on the detail view's KPI names. Returns (errors, warnings).

    A count or a "saw it" denominator is an error on the primary (the decision
    metric cannot be compared between arms) and a warning on the other lines.
    A rate with no denominator is a warning on every line: assigned visitors is
    the default when nothing is written. Pass/fail checks and lines labelled
    "yalnız B" / "B only" (a diagnostic that exists in one arm) are skipped.
    `glossary_ok`: an archive scenario's canonical glossary names inherit the
    glossary's denominator; a produced scenario writes it out.
    """
    errors, warnings = [], []
    for e in entries:
        name, path, role = e["name"], e["path"], e["role"]
        if e["is_check"] or B_ONLY_RE.search(name):
            continue
        has_per = bool(PER_RE.search(name)) or _filled(e.get("denominator"))
        primary = role == "primary"
        if COUNT_RE.search(name) and not has_per:
            if primary:
                errors.append(msg(lang, "kpi_count_primary", path=path, name=name))
            else:
                warnings.append(msg(lang, "kpi_count", path=path, role=role, name=name))
        if SAW_RE.search(name):
            if primary:
                errors.append(msg(lang, "kpi_saw_primary", path=path, name=name))
            else:
                warnings.append(msg(lang, "kpi_saw", path=path, role=role, name=name))
        if RATE_RE.search(name) and not has_per and not (glossary_ok and _in_glossary(name)):
            warnings.append(msg(lang, "kpi_denominator", path=path, name=name))
    return errors, warnings


def complement_problems(entries, lang="tr"):
    """A guardrail that is 1 − primary: completion against abandonment of the
    same step over the same (or no stated) denominator. An error (rule 3)."""
    primary = next((e for e in entries if e["role"] == "primary"), None)
    if primary is None or not COMPLETE_RE.search(primary["name"]):
        return []
    out = []
    p_den = denominator_of(primary["name"], primary.get("denominator"))
    for e in entries:
        if e["role"] != "guardrail" or e["is_check"] or not ABANDON_RE.search(e["name"]):
            continue
        g_den = denominator_of(e["name"], e.get("denominator"))
        if p_den and g_den and p_den != g_den:
            continue  # a different population: a later step, which is what a guardrail should be
        out.append(msg(lang, "complement", path=e["path"], name=e["name"]))
    return out


# ------------------------------------------------------------------ the checks

def check_kpis(scenario, errors, lang="tr"):
    """Rules 2 and 3 on the record: the guardrail is neither the primary under
    another role nor its complement, and both are measured over a population
    both arms have."""
    primary, guardrail = _obj(scenario.get("primary_kpi")), _obj(scenario.get("guardrail"))
    if isinstance(primary.get("name"), str) and isinstance(guardrail.get("name"), str) \
            and norm(primary["name"]) == norm(guardrail["name"]):
        errors.append(msg(lang, "guardrail_is_primary", name=guardrail["name"]))
    errors.extend(population_problems(primary, "primary_kpi", lang))
    if guardrail.get("kind") == "metric":
        errors.extend(population_problems(guardrail, "guardrail", lang))
    errors.extend(complement_problems(record_entries(scenario), lang))
    check_kpi_meaning(scenario, errors, lang)


def check_detail(scenario, errors, lang="tr"):
    """Rules 2 and 3 on the detail view's KPI box, when the user asked for it.

    Checked directly rather than via the generic walker: a silent miss here
    would let the detailed card show five equally weighted metrics and no
    guardrail. The first line IS the primary metric, and a metric listed twice
    (a "guardrail" carrying the primary's own name) is refused.
    """
    kpis = _obj(scenario.get("detail")).get("kpis")
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
    seen = {}
    for i, k in enumerate(kpis):
        if not isinstance(k, dict) or not isinstance(k.get("name"), str):
            continue
        key = norm(k["name"])
        if key in seen:
            errors.append(msg(lang, "kpi_dup", i=i, name=k["name"], j=seen[key]))
        else:
            seen[key] = i
    entries = detail_entries(scenario)
    name_errors, _ = kpi_name_problems(entries, lang)
    errors.extend(name_errors)
    errors.extend(complement_problems(entries, lang))


def check_variants(scenario, errors, lang="tr"):
    variants = scenario.get("variants")
    if not isinstance(variants, list) or len(variants) != 2 or not all(isinstance(v, dict) for v in variants):
        return
    ids = [v.get("id") for v in variants]
    if all(i in ("A", "B") for i in ids) and ids != ["A", "B"]:
        errors.append(msg(lang, "variants_ids", ids=ids))
    if variants[1].get("is_current") is True:
        errors.append(msg(lang, "variants_current"))


def check_source(scenario, errors, lang="tr"):
    source = scenario.get("source")
    if source in ("archive", "adapted") and not _filled(scenario.get("adapted_from")):
        errors.append(msg(lang, "adapted_from", src=source))
    if source == "generated" and not _filled(scenario.get("source_note")):
        errors.append(msg(lang, "source_note"))
    level = _obj(scenario.get("evidence")).get("level")
    if source in ("archive", "adapted") and level == "intuition":
        errors.append(msg(lang, "evidence_downgrade", src=source))
    check_archive(scenario, errors, lang)


_ARCHIVE = {}  # archive folder → {title: (Değişken, Fark)} or None, read once per folder
ARCHIVE_LINE_RE = re.compile(r"^Değişken:\s*(?P<var>.*?)\s*·\s*Fark:\s*(?P<fark>\S+)\s*$")


def load_archive(directory=None):
    """Every archive title with its `Değişken: … · Fark: …` line.

    A line scan of knowledge/scenarios/*.md ("## " opens a block, its first
    Değişken line describes it), not a parse of the prose; titles are
    whitespace-normalised. None when the folder holds no archive file.
    """
    directory = directory or ARCHIVE_DIR
    if directory not in _ARCHIVE:
        blocks = {}
        files = sorted(glob.glob(os.path.join(directory, "*.md")))
        for path in files:
            title = None
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("## "):
                        title = " ".join(line[3:].split())
                        blocks.setdefault(title, (None, None))
                    elif title and blocks[title] == (None, None):
                        m = ARCHIVE_LINE_RE.match(line.strip())
                        if m:
                            blocks[title] = (m.group("var"), m.group("fark"))
        _ARCHIVE[directory] = blocks if files else None
    return _ARCHIVE[directory]


def fold_tr(text):
    """Turkish-aware case and whitespace folding ("İ" → "i", "I" → "ı")."""
    return " ".join(text.replace("İ", "i").replace("I", "ı").split()).casefold()


def check_archive(scenario, errors, lang="tr"):
    """Rule 8, checked against the archive itself: adapted_from is a real
    title; 'archive' keeps its Değişken and both keep its Fark.

    An English record names the Turkish title but translates the variable, so
    its variable is left to scenario-critic.
    """
    source, title = scenario.get("source"), scenario.get("adapted_from")
    if source not in ("archive", "adapted") or not _filled(title):
        return
    archive = load_archive()
    if archive is None:
        errors.append(msg(lang, "archive_missing", src=source, dir=ARCHIVE_DIR))
        return
    key = " ".join(title.split())
    if key not in archive:
        close = difflib.get_close_matches(key, list(archive), n=1)
        hint = msg(lang, "closest_title", title=close[0]) if close else ""
        errors.append(msg(lang, "adapted_from_unknown", val=title, hint=hint))
        return
    variable, fark = archive[key]
    if fark is None:
        return  # a block without its Değişken line: validate_scenarios.py reports the archive itself
    expected = DIFFERENCE_ALIASES.get(fark, fark)
    diff = scenario.get("difference")
    if diff != expected:
        got = repr(diff) if diff is not None else msg(lang, "missing_value")
        errors.append(msg(lang, "archive_difference", src=source, exp=expected, fark=fark, got=got))
    record_variable = scenario.get("variable")
    if source == "archive" and scenario.get("lang", "tr") == "tr" and isinstance(record_variable, str) \
            and fold_tr(record_variable) != fold_tr(variable):
        errors.append(msg(lang, "archive_variable", exp=variable, got=record_variable))


def claim_in(regex, text):
    """The first hit of `regex` in `text` that is not negated, or None."""
    for m in regex.finditer(text):
        if NEGATION_BEFORE_RE.search(text[:m.start()]) or NEGATION_AFTER_RE.match(text, m.end()):
            continue
        return m.group(0)
    return None


def negated(text, start, end):
    """A claim at text[start:end] that the words around it negate."""
    return bool(NEGATION_BEFORE_RE.search(text[:start]) or NEGATION_AFTER_RE.match(text, end))


def claim_fields(scenario):
    """(path, text) of every free-text field the claim checks read: not
    `detail` (archive KPI questions) and not `card` (page copy)."""
    pairs = [(key, scenario.get(key)) for key in ("title", "problem", "mechanism", "variable")]
    pairs += [("variants[%d].description" % i, v.get("description"))
              for i, v in enumerate(_list(scenario.get("variants"))) if isinstance(v, dict)]
    pairs += [("priority.rationale", _obj(scenario.get("priority")).get("rationale")),
              ("evidence.note", _obj(scenario.get("evidence")).get("note")),
              ("source_note", scenario.get("source_note"))]
    pairs += [("warnings[%d].text" % i, w.get("text")) for i, w in enumerate(_list(scenario.get("warnings")))
              if isinstance(w, dict)]
    pairs += _invariant_fields(scenario)
    pairs.append(("numeric_change", scenario.get("numeric_change")))
    for i, item in enumerate(_list(scenario.get("assumptions"))):
        if isinstance(item, dict):
            pairs += [("assumptions[%d].%s" % (i, key), item.get(key)) for key in ("text", "question")]
    return _strings(pairs)


def outcome_words(clause):
    """(start, end, tense) of every outcome or chance word in `clause`.

    tense: 'chance', 'past' (arttı, rose), 'future' (artar, artacak, rises,
    will raise) or 'neutral' (artış, uplift, artıyor). A passive causative
    ("fiyatı artırılır") is a change made to the page, not an outcome.
    """
    out = []
    for m in TR_OUTCOME_RE.finditer(clause):
        stem, suffix = m.group(1).casefold(), m.group(2).casefold()
        if stem == "art" and suffix.startswith("tır"):
            stem, suffix = "artır", suffix[3:]
        allowed = TR_ALLOWED_SUFFIX.get(stem)
        if allowed is not None and not suffix.startswith(allowed):
            continue  # artı, artık, düşük, düşün, büyük, büyüt …
        if TR_NEGATIVE_RE.match(suffix) or (stem in TR_CAUSATIVE and re.match(r"[ıiuü]l", suffix)):
            continue
        tense = "past" if TR_PAST_RE.match(suffix) else "future" if TR_FUTURE_RE.match(suffix) else "neutral"
        out.append((m.start(), m.end(), tense))
    for m in EN_OUTCOME_RE.finditer(clause):
        word = m.group(1).casefold()
        if word in EN_PAST:
            tense = "past"
        elif word in EN_PRESENT or MODAL_BEFORE_RE.search(clause[:m.start()]):
            tense = "future"
        else:
            tense = "neutral"
        out.append((m.start(), m.end(), tense))
    out += [(m.start(), m.end(), "chance") for m in CHANCE_WORD_RE.finditer(clause)]
    return out


def _words_around(clause, start, end):
    """The word right before clause[start:end] and up to two words right
    after it, without crossing punctuation."""
    before = re.search(r"(\w+)[\s(“\"‘«]*$", clause[:start])
    after = re.split(r"[,;:.!?)”\"’»]", clause[end:], maxsplit=1)[0]
    return (before.group(1) if before else ""), re.findall(r"\w+", after)[:2]


def page_figure(clause, m):
    """A number the page shows (a price, discount, threshold or design value), not an outcome."""
    before, after = _words_around(clause, m.start(), m.end())
    return bool(PAGE_FIGURE_BEFORE_RE.match(before) or any(PAGE_FIGURE_AFTER_RE.match(w) for w in after)
                or re.search(r"(?:katkı\s+pay|contribution)\w*\s*$", clause[:m.start()], re.IGNORECASE))


def _gap(clause, a_end, b_start):
    """Words between two spans, or None when punctuation separates them."""
    between = clause[a_end:b_start]
    if re.search(r"[,;:()]", between):
        return None
    return len(re.findall(r"\w+", between))


def number_claims(clause):
    """(word, tense, linked) of every claim-shaped number in `clause`.

    linked: the number and an outcome or chance word sit at most CLAIM_WINDOW
    words apart in one clause (a claim); otherwise the pair is borderline.
    """
    words = outcome_words(clause)
    estimate = bool(ESTIMATE_RE.search(clause))
    found = []
    for m in CLAIM_NUM_RE.finditer(clause):
        if page_figure(clause, m):
            continue
        ablative = (m.group("suffix") or "").casefold().startswith(("den", "dan", "ten", "tan"))
        adjacent = CLAIM_ADJACENT_RE.match(clause, m.end())
        if adjacent and not ablative and not negated(clause, m.start(), adjacent.end()):
            found.append((clause[m.start():adjacent.end()], "future" if estimate else "neutral", True))
            continue
        if m.group("mult"):
            before, after = _words_around(clause, m.start(), m.end())
            if METRIC_NOUN_RE.fullmatch(before) or (after and METRIC_NOUN_RE.fullmatch(after[0])):
                found.append((m.group(0), "future" if estimate else "neutral", True))
                continue
        best = None
        for start, end, tense in words:
            if end <= m.start():
                gap, span = _gap(clause, end, m.start()), (start, m.end())
            elif start >= m.end():
                gap, span = _gap(clause, m.end(), start), (m.start(), end)
            else:
                continue
            if negated(clause, *span):
                continue
            linked = gap is not None and gap <= CLAIM_WINDOW
            if tense == "chance":
                kind = "chance"
            else:
                kind = "future" if estimate else tense
            candidate = (not linked, gap if gap is not None else 99, clause[span[0]:span[1]], kind)
            best = candidate if best is None or candidate < best else best
        if best is not None:
            found.append((best[2], best[3], not best[0]))
    for m in DOUBLE_RE.finditer(clause):
        if negated(clause, m.start(), m.end()):
            continue
        for n in METRIC_NOUN_RE.finditer(clause):
            gap = _gap(clause, n.end(), m.start()) if n.end() <= m.start() else \
                _gap(clause, m.end(), n.start()) if n.start() >= m.end() else None
            if gap is not None and gap <= CLAIM_WINDOW:
                past = re.search(r"(?:ed|d[ıiuü]|t[ıiuü])$", m.group(0), re.IGNORECASE)
                found.append((m.group(0), "past" if past and not estimate else "future", True))
                break
    return found


def text_claims(text):
    """(claims, borderline) in `text`, each a list of (word, kind, clause).

    kind: 'archive' (the archive as proof), 'similar' (another test's result),
    'chance', 'past', 'future', 'neutral'; borderline adds 'vague'.
    """
    claims, borderline = [], []
    for clause in CLAUSE_SPLIT_RE.split(text):
        for regex, kind in ((ARCHIVE_PROOF_RE, "archive"), (SIMILAR_RE, "similar"), (CHANCE_PHRASE_RE, "chance")):
            claims += [(m.group(0), kind, clause) for m in regex.finditer(clause)
                       if not negated(clause, m.start(), m.end())]
        for word, kind, linked in number_claims(clause):
            (claims if linked else borderline).append((word, kind, clause))
        borderline += [(m.group(0), "vague", clause) for m in CLAIM_VAGUE_RE.finditer(clause)]
    return claims, borderline


def source_named(note):
    """evidence.note says where the figure comes from (a heuristic: a source
    word or a proper name; scenario-critic judges whether it is real)."""
    return _filled(note) and bool(SOURCE_WORD_RE.search(note) or SOURCE_PROPER_RE.search(note))


def claim_exempt(scenario, kind, clause):
    """Whether the record's evidence carries a claim of this kind.

    The user's own data with its source carries an observed or achieved
    figure and another test's result; a forecast or a chance also says who
    reported it in its own clause ("GA4’e göre", "<source> reports"). A sector
    study carries a figure quoted with its source in the clause. The archive
    is never proof (rule 8).
    """
    evidence = _obj(scenario.get("evidence"))
    level = evidence.get("level")
    if kind == "archive" or not source_named(evidence.get("note")):
        return False
    attributed = bool(ATTRIBUTION_RE.search(clause) or ATTRIBUTION_PROPER_RE.search(clause))
    if level == "user_data":
        return kind in ("past", "neutral", "similar") or attributed
    if level == "sector":
        return kind != "similar" and attributed
    return False


CLAIM_MESSAGE = {"archive": "archive_claim", "similar": "similar_claim"}


def check_claims(scenario, errors, lang="tr"):
    """Rules 8 and 10 in every free-text field: no result ("tested", "won"),
    no uplift, chance or borrowed result the evidence can't carry. One
    message per field: the first claim found."""
    level = _obj(scenario.get("evidence")).get("level")
    for path, text in claim_fields(scenario):
        word = claim_in(OVERCLAIM_RE, text) if level != "user_data" else None
        if word:
            errors.append(msg(lang, "overclaim", path=path, word=word))
            continue
        found, _ = text_claims(text)
        for word, kind, clause in found:
            if not claim_exempt(scenario, kind, clause):
                errors.append(msg(lang, CLAIM_MESSAGE.get(kind, "uplift_claim"), path=path, word=word))
                break


def claim_warnings(scenario, lang="tr"):
    """The borderline wording code can't decide, for the reviewer (--strict: errors)."""
    out = []
    for path, text in claim_fields(scenario):
        _, borderline = text_claims(text)
        for word, kind, clause in borderline:
            if kind == "vague" or not claim_exempt(scenario, kind, clause):
                out.append(msg(lang, "claim_borderline", path=path, word=word))
                break
    return out


def check_evidence(scenario, errors, lang="tr"):
    """Rule 10: the evidence says what it rests on, weak evidence is not
    ranked high, and no field promises a guarantee (claims: check_claims)."""
    evidence = _obj(scenario.get("evidence"))
    level = evidence.get("level")
    if level in NOTED_EVIDENCE and not _filled(evidence.get("note")):
        errors.append(msg(lang, "evidence_note", level=level))
    if level == "intuition" and _obj(scenario.get("priority")).get("tier") == "high":
        errors.append(msg(lang, "intuition_high"))
    pairs = [(key, scenario.get(key)) for key in ("title", "problem", "mechanism")]
    pairs += [("priority.rationale", _obj(scenario.get("priority")).get("rationale")), ("evidence.note", evidence.get("note"))]
    for path, text in _strings(pairs):
        word = claim_in(NEVER_CLAIM_RE, text)
        if word:
            errors.append(msg(lang, "never_claim", path=path, word=word))
    check_claims(scenario, errors, lang)


# The six objection lenses (methodology.md → The idea-generation lens), English → Turkish.
OBJECTIONS = {"Trust": "Güven", "Price": "Fiyat", "Fit": "Uygunluk", "Timing": "Zamanlama", "Effort": "Çaba",
              "Clarity": "Netlik"}


def check_objection(scenario, errors, lang="tr"):
    """Rule 7: the objection is written in the record's language, like every other field."""
    value = scenario.get("objection")
    if not isinstance(value, str):
        return
    record_lang = scenario.get("lang") or "tr"
    word = value.strip()
    if record_lang == "tr" and word in OBJECTIONS:
        errors.append(msg(lang, "objection_lang", val=value, lang=record_lang, want=OBJECTIONS[word]))
    elif record_lang == "en" and word in OBJECTIONS.values():
        want = next(k for k, v in OBJECTIONS.items() if v == word)
        errors.append(msg(lang, "objection_lang", val=value, lang=record_lang, want=want))


def check_assumptions(scenario, errors, lang="tr"):
    """Rules 9 and 10: an unverified critical fact carries the question that
    settles it and keeps the proposal medium at most; each item is one short
    sentence. The shape (type, at most three) is the schema's."""
    critical = None
    for i, item in enumerate(_list(scenario.get("assumptions"))):
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str) and len(text.strip()) > MAX_ASSUMPTION:
            errors.append(msg(lang, "assumption_long", path="assumptions[%d].text" % i, n=len(text.strip()),
                              max=MAX_ASSUMPTION))
        if item.get("type") == "critical":
            critical = critical or (text if isinstance(text, str) else "")
            if not _filled(item.get("question")):
                errors.append(msg(lang, "assumption_question", path="assumptions[%d].question" % i))
    if critical is not None and _obj(scenario.get("priority")).get("tier") == "high":
        errors.append(msg(lang, "assumption_high", text=critical))


def check_numeric_change(scenario, errors, lang="tr"):
    """Rule 10: numeric_change says where its figure comes from, or a critical assumption holds the figure open."""
    text = scenario.get("numeric_change")
    if not _filled(text) or NUMERIC_SOURCE_RE.search(text):
        return
    numbers = set(FIGURE_NUMBER_RE.findall(text))
    for item in _list(scenario.get("assumptions")):
        if not isinstance(item, dict) or item.get("type") != "critical":
            continue
        about = " ".join(t for t in (item.get("text"), item.get("question")) if isinstance(t, str))
        if numbers & set(FIGURE_NUMBER_RE.findall(about)) or FIGURE_WORD_RE.search(about):
            return
    errors.append(msg(lang, "numeric_unsourced", val=text.strip()))


def check_statistics(scenario, errors, lang="tr"):
    """Rule 5: no field of the record itself states a statistic or a numeric score."""
    primary, guardrail = _obj(scenario.get("primary_kpi")), _obj(scenario.get("guardrail"))
    pairs = [(key, scenario.get(key)) for key in ("title", "problem", "mechanism", "variable", "source_note",
                                                  "numeric_change")]
    pairs += [("variants[%d].description" % i, v.get("description"))
              for i, v in enumerate(_list(scenario.get("variants"))) if isinstance(v, dict)]
    pairs += [("priority.rationale", _obj(scenario.get("priority")).get("rationale")),
              ("evidence.note", _obj(scenario.get("evidence")).get("note"))]
    pairs += [("primary_kpi." + k, primary.get(k)) for k in ("name", "denominator")]
    pairs += [("guardrail." + k, guardrail.get(k)) for k in ("name", "denominator", "criterion")]
    pairs += [("warnings[%d].text" % i, w.get("text")) for i, w in enumerate(_list(scenario.get("warnings")))
              if isinstance(w, dict)]
    pairs += [("invariants[%d]" % i, t) for i, t in enumerate(_list(scenario.get("invariants")))]
    pairs += [("assumptions[%d].%s" % (i, k), a.get(k)) for i, a in enumerate(_list(scenario.get("assumptions")))
              if isinstance(a, dict) for k in ("text", "question")]
    for path, text in _strings(pairs):
        hit = STATISTICS_RE.search(text)
        if hit:
            errors.append(msg(lang, "statistics", path=path, word=hit.group(0)))


def first_hit(regex, text, exclude=()):
    """The first keyword `regex` finds in `text`, skipping words that start
    with one of `exclude`; None when there is none."""
    for m in regex.finditer(text):
        if not text[m.start():].casefold().startswith(exclude):
            return m.group(0)
    return None


def change_text(scenario):
    """How the record describes its change: the variable, the mechanism and B.

    A's description is the page as it is, and an element it merely names (the
    unchanged "Sepete ekle butonu") isn't what the test changes; it is read
    only for a removal, where the changed element exists in A alone.
    """
    parts = [scenario.get("variable"), scenario.get("mechanism")]
    removal = card_difference(scenario, {}) == "remove"
    parts += [v.get("description") for v in _list(scenario.get("variants"))
              if isinstance(v, dict) and (v.get("id") != "A" or removal)]
    return " ".join(p for p in parts if isinstance(p, str))


def warning_text(scenario, kind):
    """The text of every warning of type `kind`, joined."""
    return " ".join(w["text"] for w in _list(scenario.get("warnings"))
                    if isinstance(w, dict) and w.get("type") == kind and isinstance(w.get("text"), str))


def check_accessibility(scenario, text, word, errors, lang="tr"):
    """Rule 3: an interactive change carries an accessibility warning that
    states the criteria its element needs."""
    needed = list(A11Y_BASE)
    if MODAL_RE.search(text):
        needed += A11Y_MODAL
    if CAROUSEL_RE.search(text) and AUTO_ADVANCE_RE.search(text):
        needed += A11Y_AUTO_ADVANCE
    label = 1 if lang == "en" else 0
    stated = warning_text(scenario, "accessibility")
    if not stated:
        errors.append(msg(lang, "a11y_missing", word=word, criteria=", ".join(c[label] for c in needed)))
        return
    missing, lower = [], []
    for c in needed:
        figure = c[2].below(stated) if isinstance(c[2], FigureCriterion) else None
        if figure:
            lower.append((c[2], figure))
        elif not c[2].search(stated):
            missing.append(c[label])
    if missing:
        errors.append(msg(lang, "a11y_criteria", word=word, criteria=", ".join(missing)))
    for criterion, figure in lower:
        what, need = A11Y_THRESHOLD_LABELS[criterion][label]
        errors.append(msg(lang, "a11y_threshold", what=what, val=figure, need=need))


def check_benefit_guardrail(scenario, text, errors, lang="tr"):
    """Rule 3: a revenue primary on a change to a user benefit is guarded on that benefit."""
    name = _obj(scenario.get("primary_kpi")).get("name")
    if not isinstance(name, str) or not REVENUE_RE.search(name):
        return
    guardrail = _obj(scenario.get("guardrail"))
    watched = " ".join(str(guardrail.get(key) or "") for key in ("name", "criterion"))
    codes = BENEFIT_FAMILIES[0]
    hit = codes.search(text)
    if hit:  # a change to a code field: any change can hide it from code holders
        if not codes.search(watched):
            errors.append(msg(lang, "benefit_guardrail", name=name, word=hit.group(0)))
        return
    # Any other benefit is at risk only when B hides, removes, shrinks or moves it out of the way.
    variant_b = next((v for v in _list(scenario.get("variants")) if isinstance(v, dict) and v.get("id") == "B"), {})
    reducing = " ".join(p for p in (variant_b.get("description"), scenario.get("mechanism")) if isinstance(p, str))
    if not (card_difference(scenario, {}) == "remove" or REDUCES_RE.search(reducing)):
        return
    for family in BENEFIT_FAMILIES[1:] + (OFFER_BENEFIT,):
        hit = family.search(text)
        if hit and not (family.search(watched) or (family is OFFER_BENEFIT and codes.search(watched))):
            errors.append(msg(lang, "benefit_guardrail", name=name, word=hit.group(0)))
            return


def check_change(scenario, errors, lang="tr"):
    """What the change touches, read off its wording (the keyword lists
    above): accessibility (rule 3), invariants (rule 4), a benefit guardrail
    (rule 3), regulation (rule 11) and urgency backed by real data (rule 6)."""
    text = change_text(scenario)
    interactive = first_hit(INTERACTIVE_RE, text, NOT_INTERACTIVE)
    if interactive:
        check_accessibility(scenario, text, interactive, errors, lang)
    functional = interactive or first_hit(FUNCTIONAL_RE, text)
    if functional and "invariants" not in scenario:
        errors.append(msg(lang, "invariants", word=functional))
    check_benefit_guardrail(scenario, text, errors, lang)
    word = regulated_word(scenario)
    if word and not has_regulation_warning(scenario):
        errors.append(msg(lang, "regulated", word=word))
    variant_b = next((v for v in _list(scenario.get("variants")) if isinstance(v, dict) and v.get("id") == "B"), {})
    signal = " ".join(p for p in (variant_b.get("description"), scenario.get("mechanism")) if isinstance(p, str))
    count = URGENCY_COUNT_RE.search(signal)
    urgency = first_hit(URGENCY_RE, signal) or (count.group(0) if count else None)
    if urgency and not DATA_SOURCE_RE.search(warning_text(scenario, REGULATION)):
        errors.append(msg(lang, "urgency", word=urgency))


_CLASSES = []  # the default template's component classes, read once


def _template_classes():
    if not _CLASSES:
        names = frozenset()
        if build_card is not None and os.path.isfile(DEFAULT_TEMPLATE):
            with open(DEFAULT_TEMPLATE, encoding="utf-8") as fh:
                names = build_card.component_classes(fh.read())
        _CLASSES.append(names)
    return _CLASSES[0]


def card_difference(scenario, card):
    """The card's difference type: the record's own; card.difference only
    when the record states none (a different one is refused, check_card)."""
    diff = scenario.get("difference") or card.get("difference")
    if not isinstance(diff, str):
        return None
    diff = DIFFERENCE_ALIASES.get(diff.lower(), diff.lower())
    return diff if diff in ("change", "add", "move", "remove") else None


def card_device(scenario, card):
    for value in (card.get("device"), scenario.get("device")):
        if isinstance(value, str) and value:
            return value
    return "phone"


def _card_report(scenario, card, lang):
    """(errors, warnings) of the two mockups, from the builder's own function."""
    a, b = card.get("variant_a"), card.get("variant_b")
    diff = card_difference(scenario, card)
    # Both must be strings: the walker has already reported the wrong type, and
    # markup rules have nothing to say about a number.
    if build_card is None or not isinstance(a, str) or not isinstance(b, str) or diff is None:
        return [], []
    return build_card.card_problems(diff, a, b, lang=lang, variable=scenario.get("variable"),
                                    classes=_template_classes(), card_lang=scenario.get("lang") or "tr")


def check_card(scenario, errors, lang="tr"):
    card = scenario.get("card")
    if not isinstance(card, dict) or build_card is None:
        return
    if not card.get("difference") and not scenario.get("difference"):
        errors.append(msg(lang, "card_difference"))
    if hasattr(build_card, "difference_problems"):  # card.difference never overrides the record's
        errors.extend(msg(lang, "card_line", msg=p) for p in build_card.difference_problems(scenario, lang))
    card_errors, _ = _card_report(scenario, card, lang)
    errors.extend(msg(lang, "card_line", msg=p) for p in card_errors)
    brand = card.get("brand")
    if isinstance(brand, dict):
        for key in ("primary", "on_primary"):
            value = brand.get(key)
            if isinstance(value, str) and value:
                problem = build_card.color_problem(value, key, lang)
                # The schema's pattern already speaks for a value that is not colour syntax at all.
                if problem and not any(e.startswith("card.brand.%s:" % key) for e in errors):
                    errors.append(msg(lang, "card_line", msg=problem))
    nav = card.get("bottom_nav")
    url = card.get("url")
    errors.extend(build_card.frame_problems(card_device(scenario, card), url if isinstance(url, str) else None,
                                            nav if isinstance(nav, list) else None,
                                            card.get("bottom_nav_active"), lang))


def validate(scenario, schema, lang="tr"):
    """Errors only. lint() returns the warnings."""
    errors = []
    walk(scenario, schema, "", errors, schema, lang)
    if isinstance(scenario, dict):
        check_kpis(scenario, errors, lang)
        check_detail(scenario, errors, lang)
        check_variants(scenario, errors, lang)
        check_source(scenario, errors, lang)
        check_evidence(scenario, errors, lang)
        check_statistics(scenario, errors, lang)
        check_objection(scenario, errors, lang)
        check_assumptions(scenario, errors, lang)
        check_numeric_change(scenario, errors, lang)
        check_change(scenario, errors, lang)
        check_card(scenario, errors, lang)
    return errors


# Left out of the fingerprint: the stamps that carry it, and the card, whose
# own fingerprint (the bytes of the final HTML) build_card.py computes.
FINGERPRINT_EXCLUDED = ("review", "card")


def record_fingerprint(record):
    """sha256 hex of the record without `review` and `card`, as sorted compact
    JSON (ensure_ascii off, UTF-8). Key order and whitespace never change it;
    any other edit to the record does."""
    body = {key: value for key, value in record.items() if key not in FINGERPRINT_EXCLUDED}
    data = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# -------------------------------------------------------------------- warnings

def _item_text(item):
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return " ".join(str(item.get(k, "")) for k in ("label", "text"))
    return ""


def _list(value):
    return value if isinstance(value, list) else []


def _strings(pairs):
    return [(path, text) for path, text in pairs if isinstance(text, str)]


def _bounded_fields(scenario):
    """(path, text) of the record's sentences that have a length limit."""
    pairs = [("problem", scenario.get("problem")), ("mechanism", scenario.get("mechanism"))]
    pairs += [("variants[%d].description" % i, v.get("description"))
              for i, v in enumerate(_list(scenario.get("variants"))) if isinstance(v, dict)]
    pairs += _invariant_fields(scenario)
    pairs.append(("priority.rationale", _obj(scenario.get("priority")).get("rationale")))
    pairs += [("warnings[%d].text" % i, w.get("text"))
              for i, w in enumerate(_list(scenario.get("warnings"))) if isinstance(w, dict)]
    return _strings(pairs)


def _invariant_fields(scenario):
    return [("invariants[%d]" % i, text) for i, text in enumerate(_list(scenario.get("invariants")))]


def _text_fields(scenario):
    """(path, text) of the record's prose, for the quote check. The mockup
    markup is not prose: its attribute quotes are straight by necessity."""
    pairs = [(key, scenario.get(key)) for key in
             ("title", "problem", "mechanism", "variable", "objection", "adapted_from", "source_note",
              "numeric_change")]
    pairs.append(("evidence.note", _obj(scenario.get("evidence")).get("note")))
    pairs += [p for p in _bounded_fields(scenario) if p[0] not in ("problem", "mechanism")]
    for key, fields in (("primary_kpi", ("name", "denominator")), ("guardrail", ("name", "denominator", "criterion"))):
        kpi = _obj(scenario.get(key))
        pairs += [("%s.%s" % (key, f), kpi.get(f)) for f in fields]
    detail = _obj(scenario.get("detail"))
    for box in ("test_items", "dont_items"):
        pairs += [("detail.%s[%d]" % (box, i), _item_text(item)) for i, item in enumerate(_list(detail.get(box)))]
    pairs += [("detail.kpis[%d]" % i, " ".join(str(k.get(f) or "") for f in ("name", "question", "denominator")))
              for i, k in enumerate(_list(detail.get("kpis"))) if isinstance(k, dict)]
    pairs += _assumption_fields(scenario)
    return _strings(pairs)


def _assumption_fields(scenario):
    return [("assumptions[%d].%s" % (i, k), a.get(k)) for i, a in enumerate(_list(scenario.get("assumptions")))
            if isinstance(a, dict) for k in ("text", "question")]


def regulated_word(scenario):
    """The word that makes the record look like a regulated flow, or None.

    Read in the record's prose (stage, title, problem, mechanism, variants, invariants) and, for the strong
    signals only, in the text the two mockups show (a KVKK line or a consent box on the screen is enough).
    """
    parts = [scenario.get(k) for k in ("stage", "title", "problem", "mechanism")]
    parts += [v.get("description") for v in _list(scenario.get("variants")) if isinstance(v, dict)]
    parts += _list(scenario.get("invariants"))
    context = " ".join(p for p in parts if isinstance(p, str))
    word = REGULATED_RE.search(context) or REGULATED_CASED_RE.search(context)
    if word:
        return word.group(0)
    card = scenario.get("card") if isinstance(scenario.get("card"), dict) else {}
    shown = " ".join(html.unescape(TAG_RE.sub(" ", card[k])) for k in ("variant_a", "variant_b")
                     if isinstance(card.get(k), str))
    word = REGULATED_MOCKUP_RE.search(shown) or REGULATED_CASED_RE.search(shown)
    return "%s (card)" % word.group(0) if word else None


def has_regulation_warning(scenario):
    """Rule 11: a record inside a regulated flow says so in a 'regulation' warning."""
    return any(isinstance(w, dict) and w.get("type") == REGULATION for w in _list(scenario.get("warnings")))


def title_kpi_warnings(title, primary, lang="tr"):
    """The title's outcome against the primary's family (a heuristic, see TITLE_EXIT_RE)."""
    if not isinstance(primary, str):
        return []
    revenue = bool(REVENUE_RE.search(primary))
    completion = bool(COMPLETE_RE.search(primary) or ABANDON_RE.search(primary))
    exit_word, revenue_word = TITLE_EXIT_RE.search(title), REVENUE_RE.search(title)
    if exit_word and not revenue_word and revenue and not completion:
        return [msg(lang, "title_kpi_revenue", word=exit_word.group(0), name=primary)]
    if revenue_word and not exit_word and completion and not revenue:
        return [msg(lang, "title_kpi_completion", word=revenue_word.group(0), name=primary)]
    return []


def lint(scenario, schema=None, lang="tr", include_card=True):
    """Warnings: things worth a second look that are not violations.

    `schema` is accepted for symmetry with validate() and not used. With
    include_card=False the mockup warnings are left out (the builder reports
    those itself when it builds).
    """
    out = []
    if not isinstance(scenario, dict):
        return out

    entries = detail_entries(scenario)
    _, name_warnings = kpi_name_problems(entries, lang, glossary_ok=scenario.get("source") == "archive")
    out.extend(name_warnings)
    for e in entries:
        if e["role"] == "guardrail" and not _filled(e["question"]):
            out.append(msg(lang, "kpi_no_question", path=e["path"]))

    title = scenario.get("title")
    if isinstance(title, str) and title.strip():
        if not title.rstrip().endswith("?"):
            out.append(msg(lang, "title_question"))
        if len(title.strip()) > MAX_TITLE:
            out.append(msg(lang, "title_long", n=len(title.strip()), max=MAX_TITLE))
        out.extend(title_kpi_warnings(title, _obj(scenario.get("primary_kpi")).get("name"), lang))
    for path, text in _strings([("problem", scenario.get("problem")), ("mechanism", scenario.get("mechanism"))]
                               + _invariant_fields(scenario) + _assumption_fields(scenario)):
        if text.strip() and sentence_count(text) > 1:
            out.append(msg(lang, "one_sentence", path=path, n=sentence_count(text)))
    for path, text in _bounded_fields(scenario):
        if len(text.strip()) > MAX_TEXT:
            out.append(msg(lang, "too_long", path=path, n=len(text.strip()), max=MAX_TEXT))

    out.extend(claim_warnings(scenario, lang))
    level = _obj(scenario.get("evidence")).get("level")
    if level in WEAK_EVIDENCE:
        for path, text in _strings([("problem", scenario.get("problem")), ("mechanism", scenario.get("mechanism")),
                                    ("priority.rationale", _obj(scenario.get("priority")).get("rationale"))]):
            hit = OVERCONFIDENT_RE.search(text)
            if hit:
                out.append(msg(lang, "overconfident", path=path, level=level, word=hit.group(0)))

    if scenario.get("lang", "tr") == "tr":
        for path, text in _text_fields(scenario):
            if '"' in text:
                out.append(msg(lang, "straight_quotes", path=path))

    card = scenario.get("card") if isinstance(scenario.get("card"), dict) else None
    if card is not None:
        variants = _list(scenario.get("variants"))
        first = variants[0] if variants and isinstance(variants[0], dict) else {}
        if card.get("mockup_basis") == "shared_page" and first.get("is_current") is not True:
            out.append(msg(lang, "basis_current"))
        if isinstance(card.get("device"), str) and isinstance(scenario.get("device"), str) \
                and card["device"] != scenario["device"]:
            out.append(msg(lang, "card_device", card=card["device"], scn=scenario["device"]))

    if include_card and card is not None:
        _, card_warnings = _card_report(scenario, card, lang)
        out.extend(msg(lang, "card_line", msg=w) for w in card_warnings)
    return out


def read_json(path, lang="tr"):
    """(document, None), or (None, the INVALID JSON message)."""
    with open(path, encoding="utf-8") as fh:
        try:
            return json.load(fh), None
        except json.JSONDecodeError as exc:
            return None, msg(lang, "invalid_json", file=path, err=exc)


def print_fingerprint(path, schema, lang="tr", strict=False):
    """--fingerprint: validate, then print only the fingerprint on stdout.
    Errors (and, with --strict, warnings) go to stderr and nothing is printed
    on stdout, so a caller can never stamp a record that does not validate."""
    doc, invalid = read_json(path, lang)
    if invalid:
        sys.stderr.write(invalid + "\n")
        return 1
    errors, warnings = validate(doc, schema, lang), lint(doc, schema, lang)
    if strict:
        errors, warnings = errors + warnings, []
    if errors:
        sys.stderr.write(msg(lang, "fingerprint_refused", file=path, n=len(errors)) + "\n")
        sys.stderr.writelines("  - %s\n" % err for err in errors)
        return 1
    sys.stderr.writelines("  ~ %s\n" % warning for warning in warnings)
    print(record_fingerprint(doc))
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description="Validate scenario records against the schema.")
    ap.add_argument("files", nargs="*", help="scenario JSON file(s)")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA)
    ap.add_argument("--strict", action="store_true", help="warnings count as violations (exit 1)")
    ap.add_argument("--lang", choices=("tr", "en"), default="tr", help="message language (default: tr)")
    ap.add_argument("--fingerprint", metavar="FILE",
                    help="validate FILE, then print only its record fingerprint (refused when it has errors)")
    args = ap.parse_args(argv)
    lang = args.lang
    if args.fingerprint and args.files:
        ap.error("--fingerprint takes exactly one file")
    if not args.fingerprint and not args.files:
        ap.error("no scenario file given")

    if not os.path.isfile(args.schema):
        sys.stderr.write("validate_scenario_json: no schema at %s\n" % args.schema)
        return 2
    try:
        schema = load_schema(args.schema, lang)
    except SchemaError as exc:
        sys.stderr.write("validate_scenario_json: %s\n" % exc)
        return 2

    for path in args.files or [args.fingerprint]:
        if not os.path.isfile(path):
            sys.stderr.write("validate_scenario_json: no such file: %s\n" % path)
            return 2
    if args.fingerprint:
        return print_fingerprint(args.fingerprint, schema, lang, args.strict)

    total_errors = total_warnings = 0
    for path in args.files:
        doc, invalid = read_json(path, lang)
        if invalid:
            print(invalid)
            total_errors += 1
            continue
        errors = validate(doc, schema, lang)
        warnings = lint(doc, schema, lang)
        if errors:
            print(msg(lang, "file_errors", file=path, n=len(errors)))
            for err in errors:
                print("  - %s" % err)
            total_errors += len(errors)
        else:
            print(msg(lang, "file_ok", file=path))
        if warnings:
            print(msg(lang, "file_warnings_strict" if args.strict else "file_warnings", file=path, n=len(warnings)))
            for warning in warnings:
                print("  ~ %s" % warning)
            total_warnings += len(warnings)

    if args.strict:
        total_errors += total_warnings
    if total_errors:
        print("\n" + msg(lang, "total", n=total_errors))
        return 1
    if total_warnings:
        print("\n" + msg(lang, "all_ok"))
        print(msg(lang, "total_warnings", n=total_warnings))
        return 0
    print("\n" + msg(lang, "all_ok"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
