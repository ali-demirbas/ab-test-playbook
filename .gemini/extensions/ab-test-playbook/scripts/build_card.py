#!/usr/bin/env python3
"""Deterministically build a scenario card HTML from its template by copying the
template and substituting ONLY the placeholder regions — the cp-then-edit
mechanism CLAUDE.md mandates, done in code so it is correct every run.

Why a script rather than hand-editing:

  1. **Escaping is a correctness bug, not a style preference.** The card's text
     fields are interpolated straight into markup. A scenario titled
     "CTA < 3 kelime olmalı mı?" or a KPI item mentioning "kargo & iade"
     silently produces broken or unexpected tags. ab-test-card/SKILL.md already
     warns about this in prose; prose cannot enforce it. Here it is enforced:
     every text field goes through html.escape() before it reaches the template,
     and the bold label is applied AFTER escaping (the order SKILL.md specifies),
     so a label can never inject a tag.

  2. **The template's developer comment documents the same structure as the
     live skeleton.** A naive string replace would fill the comment too and ship
     a half-substituted example block inside the delivered card. This tool
     strips the comment first, then substitutes.

  3. **Retyping ~250 lines of fixed CSS per card is the pipeline's largest time
     cost and its main drift risk.** After writing, this tool self-verifies that
     every fixed line of the template survived unchanged and refuses to emit a
     card that drifted.

Input: ONE JSON per scenario. Two shapes are accepted.

  * The scenario shape (templates/scenario.schema.json, the canonical one — see
    examples/scenario.json). The card reads:
        title, rationale (→ description), lang, test_items, dont_items,
        kpis[{name, role, question}]  (→ KPI box, with a role pill per item),
        source / adapted_from / evidence.level / objection / ice (→ footer tags),
        card{variant_a, variant_b, difference, device, url, bottom_nav, brand,
             brand_note, mockup_basis, note_pos, shift_note_a, shift_note_b,
             footer_notes}
  * The legacy flat shape (kept working): title, desc, test_items, kpi_items,
    dont_items, variant_a, variant_b, device, url, bottom_nav at the top level.
    Any card field may also sit at the top level in this shape.

  device:     phone      native app screen; a tab bar only via bottom_nav
              phone-web  mobile browser: status bar + address bar (lock + domain
                         from url), never a tab bar
              web        desktop browser frame; wider mockups, 580px text column
  difference: change | add | move | remove (Turkish değiştir | ekle | taşı | kaldır
              accepted). The ring (.hl) placement is enforced — see ring_problems().
  lang:       tr (default) | en. Box headers, role pills and footer labels come
              from L10N below; <html lang> follows.
  brand:      {"primary": "#c9392b", "on_primary": "#fff", "name": "Marka"} →
              CSS variables used by .r-cta, .r-header, .r-logo, .r-tabs …
              Without it the neutral palette stays.

Text fields (title, description, each item's label/text, notes, tags, tab labels,
url) are ESCAPED. `variant_a` / `variant_b` are raw markup produced by the model
for the mockup region and are inserted verbatim — that region is generative by
design, only its surrounding skeleton is fixed, and the deny-list below is its
backstop.

Usage:
  build_card.py --template templates/scenario-card.html \
                --scenario scenario.json \
                --out abtest-card-kupon-alani.html

Exit: 0 = built and self-verified, 2 = usage error / invalid input / drift detected.
"""
import argparse
import html
import json
import os
import re
import sys

DEVICES = ("phone", "phone-web", "web")
DIFFERENCES = ("change", "add", "move", "remove")
# The archive's "Fark:" line spells the type in Turkish; the schema accepts
# those spellings, and the builder also forgives a missing Turkish letter.
DIFFERENCE_TR = {"değiştir": "change", "ekle": "add", "taşı": "move", "kaldır": "remove"}
DIFFERENCE_ALIASES = dict(DIFFERENCE_TR, degistir="change", tasi="move", kaldir="remove")
KPI_ROLES = ("primary", "guardrail", "secondary")
ROLE_ALIASES = {"birincil": "primary", "ikincil": "secondary"}
SOURCES = ("archive", "adapted", "generated")
EVIDENCE_LEVELS = ("user_data", "archive", "sector", "intuition")
ICE_TIERS = ("high", "medium", "low")
MOCKUP_BASES = ("shared_page", "described", "representative")
NOTE_POSITIONS = ("above", "below")

# Every word the card itself prints, per language. The scenario's own text is
# already in the user's language (rule 7); these are the frame around it.
# Turkish values start with a capital and use no em-dash (house style).
L10N = {
    "tr": {
        "h_test": "Test Edilmesi Gerekenler",
        "h_kpi": "Takip edilecek ana KPI’lar",
        "h_dont": "Yapılmaması Gerekenler",
        "role": {"primary": "Birincil", "guardrail": "Guardrail", "secondary": "İkincil"},
        "tag_source": "Kaynak", "tag_evidence": "Kanıt", "tag_objection": "İtiraz", "tag_ice": "ICE",
        "source": {"archive": "Arşivden", "adapted": "Arşivden uyarlandı",
                   "generated": "Bu sayfa için üretildi"},
        "evidence": {"user_data": "Kendi verin", "archive": "Arşiv emsali",
                     "sector": "Sektör gözlemi", "intuition": "Sezgi"},
        "ice": {"high": "Yüksek", "medium": "Orta", "low": "Düşük"},
        "brand_neutral": "Nötr palet kullanıldı; marka kılavuzunu (logo, renkler) gönderirsen kartı yeniden markalarım.",
        "brand_screen": "Renkleri ekran görüntüsünden aldım; resmî kılavuzu gönderirsen kartı güncellerim.",
        "basis_described": "Sayfanın tarifinden yeniden çizildi; gerçek sayfa farklı görünebilir.",
        "basis_representative": "Temsilî örnek; gerçek bir sitenin ekranı değildir.",
    },
    "en": {
        "h_test": "What to Test",
        "h_kpi": "Primary KPIs to Track",
        "h_dont": "Never Do",
        "role": {"primary": "Primary", "guardrail": "Guardrail", "secondary": "Secondary"},
        "tag_source": "Source", "tag_evidence": "Evidence", "tag_objection": "Objection", "tag_ice": "ICE",
        "source": {"archive": "From archive", "adapted": "Adapted from archive",
                   "generated": "Generated for this page"},
        "evidence": {"user_data": "Your own data", "archive": "Archive precedent",
                     "sector": "Industry observation", "intuition": "Intuition"},
        "ice": {"high": "High", "medium": "Medium", "low": "Low"},
        "brand_neutral": "Neutral palette used; send your brand guide (logo, colours) and I’ll rebrand the card.",
        "brand_screen": "I took the colours from the screenshot; send the official guide and I’ll update the card.",
        "basis_described": "Rebuilt from your description; the real page may look different.",
        "basis_representative": "Representative example, not a real site’s screen.",
    },
}

LIST_PLACEHOLDERS = {
    "{{TEST_ITEMS}}": "test_items",
    "{{KPI_ITEMS}}": "kpi_items",
    "{{DONT_ITEMS}}": "dont_items",
}
SCREEN_PLACEHOLDERS = {
    "{{VARIANT_A_SCREEN}}": "variant_a",
    "{{VARIANT_B_SCREEN}}": "variant_b",
}

# The developer comment in the template documents the skeleton and the
# components. It is guidance for whoever reads the template and has no place in
# a delivered card.
COMMENT_RE = re.compile(r"[ \t]*<!--.*?-->\n?", re.DOTALL)

# `variant_a`/`variant_b` are inserted raw by design (SCREEN_PLACEHOLDERS above)
# — the mockup markup is generative, so it can't be html.escape()'d without also
# escaping the legitimate HTML it's made of. That leaves this deny-list as the
# only code-level backstop against a payload that survived into a variant from
# user-shared page text (CLAUDE.md rule 18). It is a deny-list, not an allowlist
# HTML sanitizer — a determined adversary could still find a bypass an allowlist
# parser would close; that would need an actual HTML-parsing dependency, which
# conflicts with this repo's stdlib-only convention (see analyze_results.py).
# Each pattern below is a known-live vector, not an exhaustive vocabulary of tag
# names — SKILL.md and CLAUDE.md's own claim about what's blocked has to match
# what this list actually checks, or the claim is a false one.
DANGEROUS_PATTERNS = (
    (re.compile(r"<script", re.IGNORECASE), "a <script> tag"),
    (re.compile(r'\bon[a-z]+\s*=\s*["\']', re.IGNORECASE), "an inline event-handler attribute (onerror=, onclick=, ...)"),
    (re.compile(r"javascript:", re.IGNORECASE), "a javascript: URI"),
    (re.compile(r"vbscript:", re.IGNORECASE), "a vbscript: URI"),
    (re.compile(r"<iframe", re.IGNORECASE), "an <iframe> tag"),
    (re.compile(r"<object", re.IGNORECASE), "an <object> tag"),
    (re.compile(r"<embed", re.IGNORECASE), "an <embed> tag"),
    (re.compile(r"data:text/html", re.IGNORECASE), "a data:text/html URI"),
)

# Provenance, added by the builder rather than kept in the template — the line
# above strips every template comment, so a notice living there would be
# removed from exactly the artifact that travels. Cards get shared, forwarded
# and pasted into decks long after they leave the repo; this is the only thing
# that still says where one came from. Invisible on screen by design: it costs
# nothing in a client presentation, and removing it from generated output means
# editing the generator, not deleting a line from a file.
PROVENANCE = (
    "<!--\n"
    "  Generated by ab-test-playbook — https://github.com/ali-demirbas/ab-test-playbook\n"
    "  Copyright (c) 2026 Ali Demirbaş · MIT License\n"
    "  This card was produced by scripts/build_card.py from templates/scenario-card.html.\n"
    "-->\n"
)

# Brand colours land inside <style>, where html.escape() is no protection: a
# value like `red}</style><script>` would close the block. Only plain colour
# syntax is accepted; anything else is refused rather than cleaned.
COLOR_RE = re.compile(
    r"^(?:#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})"
    r"|(?:rgb|rgba|hsl|hsla)\([0-9.,%\s/]+\)"
    r"|[a-zA-Z]{3,24})$"
)

HL_CLASS_RE = re.compile(r"""class\s*=\s*(["'])(.*?)\1""", re.IGNORECASE | re.DOTALL)


def escape(text):
    """Escape a value for interpolation into markup. Non-strings are stringified."""
    return html.escape(str(text), quote=True)


def die(msg):
    sys.stderr.write("build_card: %s\n" % msg)
    sys.exit(2)


# ---------------------------------------------------------------- input shape

def _pick(scenario, card, key, default=None):
    """A card field lives in `card` (scenario shape) or at the top level (flat)."""
    if key in card:
        return card[key]
    return scenario.get(key, default)


def normalize_difference(value):
    if value in (None, ""):
        return None
    key = str(value).strip()
    if key in DIFFERENCES:
        return key
    low = key.lower()
    if low in DIFFERENCES:
        return low
    if low in DIFFERENCE_ALIASES:
        return DIFFERENCE_ALIASES[low]
    die("difference must be one of %s (or değiştir/ekle/taşı/kaldır), got %r"
        % ("/".join(DIFFERENCES), value))


def normalize_role(value):
    if value in (None, ""):
        return None
    low = str(value).strip().lower()
    low = ROLE_ALIASES.get(low, low)
    if low not in KPI_ROLES:
        die("KPI role must be one of %s, got %r" % ("/".join(KPI_ROLES), value))
    return low


def normalize(scenario):
    """Fold either input shape into one flat view the renderer works from."""
    if not isinstance(scenario, dict):
        die("scenario must be a JSON object")
    card = scenario.get("card") if isinstance(scenario.get("card"), dict) else {}

    lang = scenario.get("lang") or card.get("lang") or "tr"
    if lang not in L10N:
        die("lang must be one of %s, got %r" % ("/".join(sorted(L10N)), lang))

    device = card.get("device") or scenario.get("device") or "phone"
    if device == "both":
        die("device 'both' has no single frame to draw: pick phone (native app), "
            "phone-web (mobile browser) or web (desktop browser) for the card, "
            "and state the audience in the setup spec")
    if device not in DEVICES:
        die("device must be one of %s, got %r" % ("/".join(DEVICES), device))

    if isinstance(scenario.get("kpis"), list):
        kpi_items = []
        for k in scenario["kpis"]:
            if not isinstance(k, dict):
                die("each kpis[] entry must be an object with name and role")
            kpi_items.append({"label": k.get("name", ""), "text": k.get("question", ""),
                              "role": k.get("role")})
    else:
        kpi_items = scenario.get("kpi_items", [])

    desc = scenario["desc"] if "desc" in scenario else scenario.get("rationale", "")

    evidence = scenario.get("evidence")
    if isinstance(evidence, dict):
        evidence = evidence.get("level")

    basis = _pick(scenario, card, "mockup_basis")
    if basis is None and isinstance(scenario.get("variants"), list):
        current = any(isinstance(v, dict) and v.get("is_current") for v in scenario["variants"])
        basis = "shared_page" if current else "representative"
    if basis is not None and basis not in MOCKUP_BASES:
        die("mockup_basis must be one of %s, got %r" % ("/".join(MOCKUP_BASES), basis))

    note_pos = _pick(scenario, card, "note_pos") or "above"
    if note_pos not in NOTE_POSITIONS:
        die("note_pos must be 'above' or 'below', got %r" % note_pos)

    has_note_key = "brand_note" in card or "brand_note" in scenario
    return {
        "lang": lang,
        "device": device,
        "title": scenario.get("title", ""),
        "desc": desc,
        "test_items": scenario.get("test_items", []),
        "kpi_items": kpi_items,
        "dont_items": scenario.get("dont_items", []),
        "variant_a": _pick(scenario, card, "variant_a", ""),
        "variant_b": _pick(scenario, card, "variant_b", ""),
        "url": _pick(scenario, card, "url", "") or "",
        "bottom_nav": _pick(scenario, card, "bottom_nav"),
        "difference": normalize_difference(_pick(scenario, card, "difference")),
        "shift_note_a": _pick(scenario, card, "shift_note_a"),
        "shift_note_b": _pick(scenario, card, "shift_note_b"),
        "brand": _pick(scenario, card, "brand"),
        "brand_note": _pick(scenario, card, "brand_note"),
        "has_brand_note": has_note_key,
        "mockup_basis": basis,
        "note_pos": note_pos,
        "footer_notes": _pick(scenario, card, "footer_notes") or [],
        "source": scenario.get("source"),
        "adapted_from": scenario.get("adapted_from"),
        "evidence": evidence,
        "objection": scenario.get("objection"),
        "ice": scenario.get("ice"),
    }


# ------------------------------------------------------------------ the boxes

def render_item(item, lang="tr"):
    """One <li>. Accepts a plain string, or {"label": ..., "text": ..., "role": ...}.

    Escaping happens before the <b> wrapper is added, never after: a label of
    '<script>' must render as visible text, not as a tag. SKILL.md states this
    order in prose; this function is where it is actually guaranteed.

    A label is always followed by a colon (added when the label lacks one) so the
    archive's "Label: question?" format survives whatever the input wrote. A
    `role` (KPI items) renders as a pill before the label.
    """
    if not isinstance(item, dict):
        return "<li>%s</li>" % escape(item)
    label = str(item.get("label", "") or "").strip()
    text = str(item.get("text", "") or "").strip()
    role = normalize_role(item.get("role"))
    pill = ""
    if role:
        pill = '<span class="role role-%s">%s</span> ' % (role, escape(L10N[lang]["role"][role]))
    if label:
        shown = escape(label)
        if not label.endswith((":", "?", "：", "!")):
            shown += ":"
        body = "<b>%s</b>" % shown
        if text:
            body += " " + escape(text)
        return "<li>%s%s</li>" % (pill, body)
    return "<li>%s%s</li>" % (pill, escape(text))


def render_list(items, indent="        ", lang="tr"):
    if not items:
        return ""
    return ("\n" + indent).join(render_item(i, lang) for i in items)


# ------------------------------------------------------------- device frames

def to_browser_skeleton(text, url):
    """Swap the live .phone skeleton for the .browser one (device: web).

    The template ships the phone skeleton live; the browser markup is rebuilt
    here from the same class names, so a web card never needs hand-copying.
    """
    pattern = re.compile(
        r'<div class="phone">\s*'
        r'<div class="statusbar">.*?</div>\s*'
        r'<div class="screen">\s*(\{\{VARIANT_[AB]_SCREEN\}\})\s*</div>\s*'
        r'<div class="bottomnav">.*?</div>\s*'
        r"</div>",
        re.DOTALL,
    )

    def repl(m):
        return (
            '<div class="browser">\n'
            '        <div class="browser-bar">\n'
            '          <span class="browser-dot"></span>'
            '<span class="browser-dot"></span>'
            '<span class="browser-dot"></span>\n'
            '          <span class="browser-url">%s</span>\n'
            "        </div>\n"
            '        <div class="browser-screen">%s</div>\n'
            "      </div>" % (escape(url), m.group(1))
        )

    out, n = pattern.subn(repl, text)
    if n != 2:
        die("template does not expose two .phone skeletons to convert (found %d)" % n)
    return out


BOTTOMNAV_RE = re.compile(r'[ \t]*<div class="bottomnav">.*?</div>\n?', re.DOTALL)


def apply_bottom_nav(text, labels):
    """Fill or drop the phone frame's bottom navigation.

    The template ships a placeholder app tab bar. Drawing it on every phone card
    was a realism bug: a mobile *web* page (most landing, form and checkout pages)
    has no app tab bar, and an app's real tabs are rarely the template's. So:
    a non-empty list of labels renders exactly those tabs (escaped - they are
    text, not markup); anything else (missing, null, empty) removes the bar.
    """
    if isinstance(labels, list) and any(str(x).strip() for x in labels):
        spans = "".join("<span>%s</span>" % escape(x) for x in labels if str(x).strip())
        nav = '        <div class="bottomnav">%s</div>\n' % spans
        out, n = BOTTOMNAV_RE.subn(lambda m: nav, text)
    else:
        out, n = BOTTOMNAV_RE.subn("", text)
    if n != 2:
        die("template does not expose two .bottomnav bars (found %d)" % n)
    return out


STATUSBAR_RE = re.compile(r'([ \t]*)(<div class="statusbar">.*?</div>)\n', re.DOTALL)


def domain_of(url):
    """What a mobile browser shows in its address bar: the host, without www."""
    rest = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", str(url or "").strip())
    host = re.split(r"[/?#]", rest, maxsplit=1)[0]
    if host.lower().startswith("www."):
        host = host[4:]
    return host


def apply_mobile_address_bar(text, url):
    """device: phone-web. A mobile browser page: status bar, then an address bar
    with a lock and the domain. Never a tab bar: that belongs to native apps."""
    text = apply_bottom_nav(text, None)
    bar = '<div class="m-addr"><span class="lock"></span><span class="m-url">%s</span></div>' % escape(domain_of(url))

    def repl(m):
        return "%s%s\n%s%s\n" % (m.group(1), m.group(2), m.group(1), bar)

    out, n = STATUSBAR_RE.subn(repl, text)
    if n != 2:
        die("template does not expose two .statusbar lines (found %d)" % n)
    return out


# ------------------------------------------------------- the changed element

def hl_count(markup):
    """How many elements in a mockup body carry the `hl` class."""
    return sum(1 for m in HL_CLASS_RE.finditer(markup or "") if "hl" in m.group(2).split())


RING_MSG = {
    "add_b": ("difference 'add': ring the new element in Variant B (found no .hl in B)",
              "fark 'ekle': B'deki yeni öğeye halka çizin (B'de .hl yok)"),
    "add_a": ("difference 'add': the element does not exist in Variant A, so A carries no ring (found {a} .hl in A)",
              "fark 'ekle': öğe A'da yok, A'da halka olmaz (A'da {a} .hl var)"),
    "remove_a": ("difference 'remove': ring the element in Variant A (found no .hl in A)",
                 "fark 'kaldır': A'daki öğeye halka çizin (A'da .hl yok)"),
    "remove_b": ("difference 'remove': Variant B leaves that area genuinely empty, so B carries no ring (found {b} .hl in B)",
                 "fark 'kaldır': B'de o alan gerçekten boş kalır, B'de halka olmaz (B'de {b} .hl var)"),
    "remove_note": ("difference 'remove': shift_note_b is required (one line under B saying the content below moved up)",
                    "fark 'kaldır': shift_note_b zorunlu (B'nin altında, alttaki içeriğin yukarı kaydığını söyleyen tek satır)"),
    "move": ("difference 'move': ring the element in both variants (found {a} in A, {b} in B)",
             "fark 'taşı': öğeye iki varyantta da halka çizin (A'da {a}, B'de {b} var)"),
    "change": ("difference 'change': ring the changed element in Variant B (found no .hl in B)",
               "fark 'değiştir': B'deki değişen öğeye halka çizin (B'de .hl yok)"),
}


def ring_problems(difference, variant_a, variant_b, shift_note_b=None, lang="en"):
    """Where the ring must sit for each kind of difference (mockup-style.md).

    add    → the new element exists only in B, so only B can carry a ring
    remove → the element exists only in A; B is genuinely empty there, and a
             shift note under B says the content below moved up
    move   → the same element in two places: ringed in both
    change → ringed in B (ringing the old state in A too is allowed)

    Returns a list of problems (English by default, Turkish with lang="tr");
    empty means the placement is valid. Shared with validate_scenario_json.py
    so the two never disagree.
    """
    if not difference:
        return []
    a, b = hl_count(variant_a), hl_count(variant_b)
    keys = []
    if difference == "add":
        if b < 1:
            keys.append("add_b")
        if a:
            keys.append("add_a")
    elif difference == "remove":
        if a < 1:
            keys.append("remove_a")
        if b:
            keys.append("remove_b")
        if not (shift_note_b and str(shift_note_b).strip()):
            keys.append("remove_note")
    elif difference == "move":
        if a < 1 or b < 1:
            keys.append("move")
    elif difference == "change":
        if b < 1:
            keys.append("change")
    idx = 1 if lang == "tr" else 0
    return [RING_MSG[k][idx].format(a=a, b=b) for k in keys]


# ---------------------------------------------------------- brand and footer

def css_string(value):
    """A CSS string literal that cannot end the string or the <style> block."""
    out = []
    for ch in str(value):
        if ch in '\\"<>&' or ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\%x " % ord(ch))
        else:
            out.append(ch)
    return '"%s"' % "".join(out)


def brand_css(brand):
    """card.brand → one :root override line inside <style>, or nothing."""
    if not brand:
        return ""
    if not isinstance(brand, dict):
        die("brand must be an object like {\"primary\": \"#c9392b\", \"on_primary\": \"#fff\", \"name\": \"Marka\"}")
    decls = []
    for key, var in (("primary", "--brand"), ("on_primary", "--on-brand")):
        value = brand.get(key)
        if value in (None, ""):
            continue
        if not isinstance(value, str) or not COLOR_RE.match(value.strip()):
            die("brand.%s must be a plain colour (#hex, rgb(), hsl() or a colour name), got %r" % (key, value))
        decls.append("%s:%s" % (var, value.strip()))
    if brand.get("name"):
        decls.append("--brand-name:%s" % css_string(brand["name"]))
    if not decls:
        return ""
    return "  :root{%s}" % ";".join(decls)


def ice_label(ice, lang):
    if not ice:
        return None
    if isinstance(ice, str):
        tier, nums = ice, None
    elif isinstance(ice, dict):
        tier = ice.get("tier")
        parts = [ice.get(k) for k in ("impact", "confidence", "ease")]
        nums = parts if all(isinstance(p, int) and not isinstance(p, bool) for p in parts) else None
    else:
        die("ice must be an object like {\"tier\": \"medium\", \"impact\": 7, \"confidence\": 4, \"ease\": 9}")
    if tier not in ICE_TIERS:
        die("ice.tier must be one of %s, got %r" % ("/".join(ICE_TIERS), tier))
    label = L10N[lang]["ice"][tier]
    if nums:
        label += " (%d×%d×%d)" % tuple(nums)
    return label


def render_footer(view):
    """Tags, brand note and mockup disclaimer: one muted block under the card."""
    lang = view["lang"]
    L = L10N[lang]
    tags = []

    source = view["source"]
    if source:
        if source not in SOURCES:
            die("source must be one of %s, got %r" % ("/".join(SOURCES), source))
        value = escape(L["source"][source])
        if source == "adapted" and view["adapted_from"]:
            value += " (“%s”)" % escape(view["adapted_from"])
        tags.append((L["tag_source"], value))
    if view["evidence"]:
        if view["evidence"] not in EVIDENCE_LEVELS:
            die("evidence level must be one of %s, got %r" % ("/".join(EVIDENCE_LEVELS), view["evidence"]))
        tags.append((L["tag_evidence"], escape(L["evidence"][view["evidence"]])))
    if view["objection"]:
        tags.append((L["tag_objection"], escape(view["objection"])))
    ice = ice_label(view["ice"], lang)
    if ice:
        tags.append((L["tag_ice"], escape(ice)))

    lines = []
    if tags:
        lines.append('<div class="tags">%s</div>' % "".join(
            "<span><b>%s:</b> %s</span>" % (escape(k), v) for k, v in tags))

    if view["has_brand_note"]:
        note = view["brand_note"]
    else:
        note = L["brand_screen"] if view["brand"] else L["brand_neutral"]
    if note:
        lines.append('<div class="foot-note">%s</div>' % escape(note))

    basis = view["mockup_basis"]
    if basis in ("described", "representative"):
        lines.append('<div class="foot-note">%s</div>' % escape(L["basis_" + basis]))

    notes = view["footer_notes"]
    if isinstance(notes, str):
        notes = [notes]
    for n in notes:
        if str(n).strip():
            lines.append('<div class="foot-note">%s</div>' % escape(n))

    if not lines:
        return ""
    return '<footer class="card-foot">\n    %s\n  </footer>' % "\n    ".join(lines)


def shift_note(text):
    if not text or not str(text).strip():
        return ""
    return '<div class="shift-note">%s</div>' % escape(text)


# ------------------------------------------------------------------- building

def build(template_text, scenario):
    view = normalize(scenario)
    lang = view["lang"]
    L = L10N[lang]

    for key in ("variant_a", "variant_b"):
        if not str(view[key] or "").strip():
            die("scenario is missing required card field: %s" % key)

    problems = ring_problems(view["difference"], view["variant_a"], view["variant_b"],
                             view["shift_note_b"])
    if problems:
        die("ring placement does not match the difference type:\n  " + "\n  ".join(problems))

    text = COMMENT_RE.sub("", template_text)

    device = view["device"]
    if device == "web":
        text = to_browser_skeleton(text, view["url"])
    elif device == "phone-web":
        text = apply_mobile_address_bar(text, view["url"])
    else:
        text = apply_bottom_nav(text, view["bottom_nav"])

    simple = {
        "{{TITLE}}": escape(view["title"]),
        "{{DESC}}": escape(view["desc"]),
        "{{LANG}}": lang,
        "{{DEVICE}}": device,
        "{{NOTE_POS}}": view["note_pos"],
        "{{H_TEST}}": escape(L["h_test"]),
        "{{H_KPI}}": escape(L["h_kpi"]),
        "{{H_DONT}}": escape(L["h_dont"]),
        "{{SHIFT_NOTE_A}}": shift_note(view["shift_note_a"]),
        "{{SHIFT_NOTE_B}}": shift_note(view["shift_note_b"]),
        "{{FOOTER}}": render_footer(view),
        "{{BRAND_CSS}}": brand_css(view["brand"]),
    }
    for ph, value in simple.items():
        if ph in text:
            text = text.replace(ph, value)

    for ph, key in LIST_PLACEHOLDERS.items():
        if ph in text:
            text = text.replace(ph, render_list(view[key], lang=lang))

    # Screens go in last and raw: this is the generative region.
    for ph, key in SCREEN_PLACEHOLDERS.items():
        if ph in text:
            text = text.replace(ph, str(view[key]))

    leftover = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if leftover:
        die("template has placeholders this tool does not fill: %s" % ", ".join(sorted(set(leftover))))

    # Drop lines a placeholder emptied (an absent shift note, footer or brand
    # override) so the delivered source carries no stray whitespace-only lines.
    text = re.sub(r"\n[ \t]+\n", "\n", text)

    # After the strip, so it survives; before <html>, so it is the first thing
    # anyone reading the source sees. Case-insensitive on purpose: `<!doctype`
    # is equally valid HTML, and putting the notice above the doctype drops the
    # browser into quirks mode — a layout bug caused by a copyright line.
    if text.lstrip()[:9].upper() == "<!DOCTYPE":
        head, sep, rest = text.partition("\n")
        text = head + sep + PROVENANCE + rest
    else:
        text = PROVENANCE + text

    return text


def strip_mockup_region(text):
    """Drop everything between the mockups block and the copy block.

    That region is the only part of the card whose *skeleton* legitimately
    differs between builds: the device swaps the frame. Excluding it by
    boundary — rather than by guessing which lines mention 'phone' — keeps the
    drift check honest about everything else.
    """
    start = text.find('<div class="mockups">')
    end = text.find('<div class="copy">')
    if start == -1 or end == -1 or end < start:
        return text
    return text[:start] + text[end:]


def fixed_lines(template_text):
    """Lines of the template that must survive verbatim into the built card.

    Excluded: placeholder lines (swappable by design: language, device, headers,
    footer, brand override), developer comments (intentionally dropped), blank
    lines, and the mockup region (device-dependent). Everything else — every CSS
    rule, the box skeleton, the pills — is checked.
    """
    stripped = strip_mockup_region(COMMENT_RE.sub("", template_text))
    out = []
    for line in stripped.splitlines():
        if "{{" in line:
            continue
        if not line.strip():
            continue
        out.append(line)
    return out


def self_verify(built_text, template_text, device=None):
    """Refuse to emit a card that drifted from the template's fixed skeleton.

    `device` is accepted for call-site symmetry but no longer changes the check:
    the device-dependent region is excluded structurally by fixed_lines().
    """
    haystack = strip_mockup_region(built_text)
    missing = []
    for line in fixed_lines(template_text):
        if line not in haystack:
            missing.append(line.strip())
    if missing:
        preview = "\n  ".join(missing[:5])
        die(
            "drift: %d fixed template line(s) missing from the built card:\n  %s"
            % (len(missing), preview)
        )
    for pattern, description in DANGEROUS_PATTERNS:
        if pattern.search(built_text):
            die("cards are static HTML; refusing to emit a card containing %s" % description)


def main(argv):
    ap = argparse.ArgumentParser(description="Build a scenario card from the template.")
    ap.add_argument("--template", required=True, help="path to templates/scenario-card.html")
    ap.add_argument("--scenario", required=True, help="JSON file describing the scenario")
    ap.add_argument("--out", required=True, help="path to write the card to")
    args = ap.parse_args(argv)

    for path in (args.template, args.scenario):
        if not os.path.isfile(path):
            die("no such file: %s" % path)

    with open(args.template, encoding="utf-8") as fh:
        template_text = fh.read()
    with open(args.scenario, encoding="utf-8") as fh:
        try:
            scenario = json.load(fh)
        except json.JSONDecodeError as exc:
            die("scenario is not valid JSON: %s" % exc)

    if not isinstance(scenario, dict) or not scenario.get("title"):
        die("scenario is missing required field: title")

    built = build(template_text, scenario)
    view = normalize(scenario)
    self_verify(built, template_text, view["device"])

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(built)

    print("built %s (%d bytes, device=%s, lang=%s, difference=%s)" % (
        args.out, len(built.encode("utf-8")), view["device"], view["lang"],
        view["difference"] or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
