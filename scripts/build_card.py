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
        card{variant_a, variant_b, difference, device, url, bottom_nav,
             bottom_nav_active, brand, brand_note, mockup_basis, note_pos,
             shift_note_a, shift_note_b, footer_notes}
    This shape is validated against the schema first (validate_scenario_json):
    a scenario with errors is refused, its warnings are printed and the card is
    still built. A scenario without a `card` object is a valid scenario but not
    a renderable one; the builder says so.
  * The legacy flat shape (kept working): title, desc, test_items, kpi_items,
    dont_items, variant_a, variant_b, device, url, bottom_nav at the top level.
    Any card field may also sit at the top level in this shape. It has no
    schema; the builder checks the three boxes itself (at least three real
    items each).

  device:     phone      native app screen; a tab bar only via bottom_nav (a
                         list of strings), its active tab via bottom_nav_active
                         (that tab's label or 0-based index)
              phone-web  mobile browser: status bar + address bar (lock + domain
                         from url), never a tab bar
              web        desktop browser frame; wider mockups, 580px text column
  difference: change | add | move | remove (Turkish değiştir | ekle | taşı | kaldır
              accepted). The ring (.hl) placement is enforced — see ring_problems().
  lang:       tr (default) | en. Box headers, role pills and footer labels come
              from L10N below; <html lang> follows.
  brand:      {"primary": "#c9392b", "on_primary": "#fff", "name": "Marka"} →
              CSS variables used by .r-cta, .r-header, .r-logo, .r-tabs …
              Without it the neutral palette stays. A colour is #hex, rgb()/
              hsl() or one of the CSS colour names; anything else is refused.

Text fields (title, description, each item's label/text, notes, tags, tab labels,
url) are ESCAPED. `variant_a` / `variant_b` are raw markup produced by the model
for the mockup region and are inserted verbatim — that region is generative by
design, only its surrounding skeleton is fixed. Because it is raw, it passes an
ALLOWLIST first (parse_markup): a closed set of inert tags and attributes, every
attribute value double-quoted, no comments, balanced tags, screened inline CSS.
A mockup that needs anything else is refused with a message naming the tag or
attribute; nothing is cleaned or rewritten.

Usage:
  build_card.py --template templates/scenario-card.html \
                --scenario scenario.json \
                --out abtest-card-kupon-alani.html [--lang tr]

--lang  language of the builder's own messages (en, the default, or tr).

Exit: 0 = built and self-verified (warnings, if any, go to stderr as
"build_card: warning: ..."), 2 = usage error / invalid input / drift detected.
"""
import argparse
import difflib
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

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

# Every {{NAME}} token the template may carry. Substitution is ONE pass over
# the template (see build()): text that was just inserted is never scanned
# again, so a title or a mockup that itself contains "{{AD}}" stays text.
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z_]+\}\}")

# ------------------------------------------------- the mockup markup allowlist
#
# `variant_a`/`variant_b` are inserted raw by design (SCREEN_PLACEHOLDERS above)
# — the mockup markup is generative, so it can't be html.escape()'d without also
# escaping the legitimate HTML it's made of. Text from a user's page can end up
# in it (CLAUDE.md rule 18), and whatever survives runs in the browser that
# opens the card. A deny-list cannot hold that line: HTML accepts unquoted
# handlers, entity-encoded schemes, <meta refresh>, <form action>, <style> and a
# dozen more shapes than any list of "bad" patterns names. So the rule is the
# other way round: only what is listed here gets in.
#
#   * tags: inert layout and text elements only. No element that loads, links,
#     submits, scripts, styles or embeds exists in this set.
#   * attributes: class, style, the ring's data-note/data-pos, and inert
#     labelling attributes. No on*= handler in any form, nothing URL-bearing.
#   * every attribute value in double quotes, attributes separated by
#     whitespace: the one spelling every HTML parser reads the same way. That
#     closes parser-differential tricks (class="a"onclick=…) by construction,
#     and keeps the ring's class attribute in the shape the reviewer greps for.
#   * no comments, declarations or processing instructions; tags balanced.
#   * inline style values are screened (CSS_FORBIDDEN).
#
# Nothing is cleaned or rewritten: a mockup either passes and is inserted byte
# for byte, or the card is refused with a message naming what to change.
ALLOWED_TAGS = ("div", "span", "p", "b", "strong", "i", "em", "u", "s", "small", "sup", "sub",
                "br", "hr", "ul", "ol", "li")
VOID_TAGS = ("br", "hr")
ALLOWED_ATTRS = ("class", "style", "data-note", "data-pos", "title", "role")
ARIA_ATTR_RE = re.compile(r"^aria-[a-z]+$")
# Named in the message when refused, because the reason differs from "unknown".
URL_ATTRS = ("href", "src", "srcset", "action", "formaction", "srcdoc", "data", "poster", "background",
             "xlink:href", "ping", "cite", "codebase", "manifest")
BLOCK_TAGS = ("div", "p", "ul", "ol", "li", "hr")

_WS = r"[ \t\r\n\f]"
_NAME = r"[a-zA-Z][a-zA-Z0-9:_.-]*"
_ATTR_SRC = r"%s+%s(?:%s*=%s*\"[^\"]*\")?" % (_WS, _NAME, _WS, _WS)
ATTR_RE = re.compile(r"%s+(%s)(?:%s*=%s*\"([^\"]*)\")?" % (_WS, _NAME, _WS, _WS))
START_TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9]*)((?:%s)*)%s*(/?)>" % (_ATTR_SRC, _WS))
END_TAG_RE = re.compile(r"</([a-zA-Z][a-zA-Z0-9]*)%s*>" % _WS)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0e-\x1f\x7f]")

# Inline CSS: anything that fetches (url, image-set, @import), scripts (legacy
# expression/behavior/-moz-binding, a javascript: value), escapes the phone
# frame (position:fixed), or hides one of those behind an escape or a comment.
CSS_FORBIDDEN = re.compile(
    r"url\s*\(|image-set\s*\(|expression\s*\(|@import|javascript\s*:|vbscript\s*:|behaviou?r\s*:|-moz-binding"
    r"|position\s*:\s*fixed|\\|/\*|[<>{}]",
    re.IGNORECASE,
)

# Second layer, kept on purpose: the raw variants are scanned again after
# entity decoding and with whitespace/control characters removed, so
# "jav&#x61;script:" and "java<TAB>script:" read as what a browser makes of
# them. It can only fire if the allowlist above has a hole; a defence that is
# never the only one. The tag-shaped half also runs over the whole built card,
# where an escaped text field can never produce a match; the scheme and handler
# half runs over the tags of the variants only, because ordinary text may say
# "JavaScript:".
DANGEROUS_TAGS = (
    (re.compile(r"<script", re.IGNORECASE), "a <script> tag"),
    (re.compile(r"<iframe", re.IGNORECASE), "an <iframe> tag"),
    (re.compile(r"<object", re.IGNORECASE), "an <object> tag"),
    (re.compile(r"<embed", re.IGNORECASE), "an <embed> tag"),
)
DANGEROUS_IN_MARKUP = (
    (re.compile(r"(?<![\w-])on[a-z]+\s*=", re.IGNORECASE), "an inline event-handler attribute (onerror=, onclick=, ...)"),
    (re.compile(r"javascript:", re.IGNORECASE), "a javascript: URI"),
    (re.compile(r"vbscript:", re.IGNORECASE), "a vbscript: URI"),
    (re.compile(r"data:text/html", re.IGNORECASE), "a data:text/html URI"),
)
DANGEROUS_PATTERNS = DANGEROUS_TAGS + DANGEROUS_IN_MARKUP
# A tag as the second layer reads it: from "<" + a letter or "/" to its ">",
# quoted values included.
TAG_SEGMENT_RE = re.compile(r"""<[a-zA-Z/](?:"[^"]*"|'[^']*'|[^>"'])*>?""")

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
# syntax is accepted; anything else is refused rather than cleaned. "Plain"
# also means "a colour a browser knows": any other word ("mavi") is valid CSS
# syntax that computes to nothing, and the CTA would render transparent with
# white text. So the name is checked against the closed CSS list, and the
# functional form has to carry three components.
COLOR_RE = re.compile(
    r"^(?:#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})"
    r"|(?:rgb|rgba|hsl|hsla)\(\s*[\d.]+%?(?:deg)?(?:\s*[, ]\s*[\d.]+%?){2}(?:\s*[,/]\s*[\d.]+%?)?\s*\)"
    r"|[a-zA-Z]{3,24})$"
)
NAMED_COLORS = frozenset("""
aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood
cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod darkgray
darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon darkseagreen
darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey dodgerblue
firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green greenyellow grey honeydew
hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral lightcyan
lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon lightseagreen lightskyblue lightslategray
lightslategrey lightsteelblue lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue
mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen mediumturquoise mediumvioletred
midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive olivedrab orange orangered orchid
palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum powderblue purple
rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen seashell sienna silver skyblue
slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white
whitesmoke yellow yellowgreen
""".split())

# Language of the builder's own messages (--lang). English by default, as
# before; every message added with the allowlist exists in Turkish too.
_MSG_LANG = "en"


def _t(en, tr, lang=None):
    return tr if (lang or _MSG_LANG) == "tr" else en


def escape(text):
    """Escape a value for interpolation into markup. Non-strings are stringified."""
    return html.escape(str(text), quote=True)


def die(msg):
    sys.stderr.write("build_card: %s\n" % msg)
    sys.exit(2)


def warn(msg):
    sys.stderr.write("build_card: warning: %s\n" % msg)


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
        "bottom_nav_active": _pick(scenario, card, "bottom_nav_active"),
        "variable": scenario.get("variable"),
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
    if isinstance(item, str):
        return "<li>%s</li>" % escape(item)
    if not isinstance(item, dict):
        # A None, a number or a nested list used to be printed as its Python
        # repr ("None", "['x']") inside the delivered card.
        die(_t("box items must be a string or {label, text}, got %r",
               "kutu maddeleri metin ya da {label, text} olmalı, gelen %r") % (item,))
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

def to_browser_skeleton(text):
    """Swap the live .phone skeleton for the .browser one (device: web).

    The template ships the phone skeleton live; the browser markup is rebuilt
    here from the same class names, so a web card never needs hand-copying.
    The address goes in as {{URL}} and is filled by build()'s single pass, like
    every other piece of user text.
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
            '          <span class="browser-url">{{URL}}</span>\n'
            "        </div>\n"
            '        <div class="browser-screen">%s</div>\n'
            "      </div>" % m.group(1)
        )

    out, n = pattern.subn(repl, text)
    if n != 2:
        die("template does not expose two .phone skeletons to convert (found %d)" % n)
    return out


BOTTOMNAV_RE = re.compile(r'[ \t]*<div class="bottomnav">.*?</div>\n?', re.DOTALL)


def apply_bottom_nav(text, show):
    """Keep or drop the phone frame's bottom navigation.

    The template ships a placeholder app tab bar. Drawing it on every phone card
    was a realism bug: a mobile *web* page (most landing, form and checkout pages)
    has no app tab bar, and an app's real tabs are rarely the template's. So the
    bar stays only when the scenario names its tabs; its content goes in as
    {{BOTTOM_NAV}} (see bottom_nav_html) and is filled by build()'s single pass.
    """
    if show:
        nav = '        <div class="bottomnav">{{BOTTOM_NAV}}</div>\n'
        out, n = BOTTOMNAV_RE.subn(lambda m: nav, text)
    else:
        out, n = BOTTOMNAV_RE.subn("", text)
    if n != 2:
        die("template does not expose two .bottomnav bars (found %d)" % n)
    return out


def _label_key(text):
    return " ".join(str(text).split()).casefold()


def bottom_nav_labels(labels):
    """card.bottom_nav → the list of tab labels, or [] for "no tab bar".

    A list of non-empty strings, nothing else: an object item used to be
    printed as a Python dict on the tab bar.
    """
    if labels is None or labels == []:
        return []
    if not isinstance(labels, list) or not all(isinstance(x, str) and x.strip() for x in labels):
        die(_t("bottom_nav must be a list of tab labels (non-empty strings), got %r; "
               "mark the active tab with bottom_nav_active (its label or 0-based index)",
               "bottom_nav sekme adlarının listesi olmalı (boş olmayan metinler), gelen %r; "
               "etkin sekmeyi bottom_nav_active ile belirtin (sekmenin adı ya da 0 tabanlı sırası)") % (labels,))
    return labels


def active_tab_index(labels, active):
    """card.bottom_nav_active → index into labels, or None when not given.

    Accepts the tab's label (case and spacing ignored) or its 0-based index.
    Returns -1 when the value names no tab; callers turn that into their own
    message (the builder dies, the validator reports).
    """
    if active is None or active == "":
        return None
    if isinstance(active, bool):
        return -1
    if isinstance(active, int):
        return active if 0 <= active < len(labels) else -1
    if isinstance(active, str):
        keys = [_label_key(x) for x in labels]
        return keys.index(_label_key(active)) if _label_key(active) in keys else -1
    return -1


def bottom_nav_html(labels, active=None):
    """The tab bar's spans (escaped: labels are text, not markup). The tab the
    screen belongs to is drawn as <span class="on">."""
    idx = active_tab_index(labels, active)
    if idx == -1:
        die(_t("bottom_nav_active %r names no tab; give one of %s or an index 0-%d",
               "bottom_nav_active %r hiçbir sekmeyle eşleşmiyor; %s adlarından birini ya da 0-%d arası sırayı yazın")
            % (active, ", ".join(repr(x) for x in labels), len(labels) - 1))
    return "".join('<span class="on">%s</span>' % escape(x) if i == idx else "<span>%s</span>" % escape(x)
                   for i, x in enumerate(labels))


STATUSBAR_RE = re.compile(r'([ \t]*)(<div class="statusbar">.*?</div>)\n', re.DOTALL)


def domain_of(url):
    """What a mobile browser shows in its address bar: the host, without www."""
    rest = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", str(url or "").strip())
    host = re.split(r"[/?#]", rest, maxsplit=1)[0]
    if host.lower().startswith("www."):
        host = host[4:]
    return host


def apply_mobile_address_bar(text):
    """device: phone-web. A mobile browser page: status bar, then an address bar
    with a lock and the domain ({{DOMAIN}}, filled by build()). Never a tab bar:
    that belongs to native apps."""
    text = apply_bottom_nav(text, False)
    bar = '<div class="m-addr"><span class="lock"></span><span class="m-url">{{DOMAIN}}</span></div>'

    def repl(m):
        return "%s%s\n%s%s\n" % (m.group(1), m.group(2), m.group(1), bar)

    out, n = STATUSBAR_RE.subn(repl, text)
    if n != 2:
        die("template does not expose two .statusbar lines (found %d)" % n)
    return out


# ------------------------------------------------- parsing the mockup markup

MARKUP_MSG = {
    "not_string": ("must be a string of markup, got {got}",
                   "işaretleme metni olmalı, gelen {got}"),
    "decl": ("comments, declarations and processing instructions (<!-- -->, <!…>, <?…>) are not allowed in a mockup",
             "mockup içinde yoruma, bildirime ve işlem yönergesine (<!-- -->, <!…>, <?…>) izin yok"),
    "control": ("control character {ch} is not allowed in a mockup",
                "mockup içinde {ch} denetim karakterine izin yok"),
    "malformed": ("malformed tag near {near}: write <tag attr=\"value\">, every attribute value in double quotes "
                  "and attributes separated by a space, and close what you open (a literal < in text is &lt;)",
                  "bozuk etiket, {near} yakınında: etiketi <tag attr=\"değer\"> biçiminde, her nitelik değerini çift "
                  "tırnak içinde ve nitelikleri boşlukla ayırarak yazın, açtığınızı kapatın (metindeki < için &lt;)"),
    "tag": ("tag <{tag}> is not allowed in a mockup (allowed: {allowed})",
            "<{tag}> etiketine mockup içinde izin yok (izinli: {allowed})"),
    "attr": ("attribute {attr}= on <{tag}> is not allowed (allowed: {allowed})",
             "<{tag}> üzerindeki {attr}= niteliğine izin yok (izinli: {allowed})"),
    "handler": ("event-handler attribute {attr}= on <{tag}> is not allowed: a card is static HTML",
                "<{tag}> üzerindeki {attr}= olay işleyicisine izin yok: kart durağan HTML’dir"),
    "url_attr": ("attribute {attr}= on <{tag}> is not allowed: a mockup carries no link, source or form target",
                 "<{tag}> üzerindeki {attr}= niteliğine izin yok: mockup bağlantı, kaynak ya da form hedefi taşımaz"),
    "dup_attr": ("attribute {attr}= is written twice on <{tag}>",
                 "{attr}= niteliği <{tag}> üzerinde iki kez yazılmış"),
    "style": ("style on <{tag}> contains a forbidden CSS construct “{what}” (no url(), image-set(), expression(), "
              "@import, javascript:, behavior:, -moz-binding, position:fixed, comments, backslash escapes or < > {{ }})",
              "<{tag}> üzerindeki style yasak bir CSS yapısı içeriyor: “{what}” (url(), image-set(), expression(), "
              "@import, javascript:, behavior:, -moz-binding, position:fixed, yorum, ters eğik çizgi kaçışı ve "
              "< > {{ }} kullanılamaz)"),
    "self_closing": ("<{tag}/> is not a void element; write <{tag}></{tag}>",
                     "<{tag}/> kendiliğinden kapanan bir etiket değil; <{tag}></{tag}> yazın"),
    "void_end": ("</{tag}> closes a void element; write <{tag}> only",
                 "</{tag}> kapanışı olmayan bir etiketi kapatıyor; yalnızca <{tag}> yazın"),
    "unbalanced": ("unbalanced markup: </{tag}> closes <{open}>",
                   "dengesiz işaretleme: </{tag}>, <{open}> etiketini kapatıyor"),
    "stray_end": ("unbalanced markup: </{tag}> has no opening tag (it would close the screen itself)",
                  "dengesiz işaretleme: </{tag}> için açılış etiketi yok (ekranın kendisini kapatır)"),
    "unclosed": ("unbalanced markup: <{tag}> is never closed",
                 "dengesiz işaretleme: <{tag}> hiç kapatılmamış"),
    "p_block": ("<{tag}> inside <p>: a browser closes the paragraph first; use a <div> instead of the <p>",
                "<p> içinde <{tag}>: tarayıcı önce paragrafı kapatır; <p> yerine <div> kullanın"),
    "li_parent": ("<li> must sit directly inside <ul> or <ol>",
                  "<li> doğrudan <ul> ya da <ol> içinde olmalı"),
    "disagree": ("internal check failed: the markup reads differently to two parsers; simplify it",
                 "iç denetim tutmadı: işaretleme iki ayrıştırıcıda farklı okunuyor; sadeleştirin"),
}


def _mm(key, lang, **kw):
    en, tr = MARKUP_MSG[key]
    return (tr if lang == "tr" else en).format(**kw)


class Node:
    """One element of a parsed mockup body."""

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    @property
    def is_ring(self):
        return "hl" in self.classes

    def key(self, ring_blind=False):
        """Structural identity. ring_blind drops the ring's own class and label
        so a ringed element compares equal to its un-ringed twin."""
        attrs = dict(self.attrs)
        if ring_blind:
            attrs.pop("data-note", None)
            attrs.pop("data-pos", None)
            attrs["class"] = " ".join(c for c in self.classes if c != "hl")
            if not attrs["class"]:
                del attrs["class"]
        return (self.tag, tuple(sorted(attrs.items())),
                tuple(k.key(ring_blind) if isinstance(k, Node) else k for k in self.kids))


class _TreeBuilder(HTMLParser):
    """Builds the element tree of a mockup that already passed the lexical
    allowlist, and checks nesting. Problems are (key, kwargs) pairs."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("#root", [], None)
        self.cur = self.root
        self.problems = []
        self.starts = 0

    def handle_starttag(self, tag, attrs):
        self.starts += 1
        if self.cur.tag == "p" and tag in BLOCK_TAGS:
            self.problems.append(("p_block", {"tag": tag}))
        if tag == "li" and self.cur.tag not in ("ul", "ol"):
            self.problems.append(("li_parent", {}))
        node = Node(tag, [(k, v or "") for k, v in attrs], self.cur)
        self.cur.kids.append(node)
        if tag not in VOID_TAGS:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.cur = self.cur.parent

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if self.cur is self.root:
            self.problems.append(("stray_end", {"tag": tag}))
            return
        if self.cur.tag != tag:
            self.problems.append(("unbalanced", {"tag": tag, "open": self.cur.tag}))
            return
        self.cur = self.cur.parent

    def handle_data(self, data):
        text = " ".join(data.split())
        if text:
            self.cur.kids.append(text)


def _allowed_attrs_text():
    return ", ".join(ALLOWED_ATTRS) + ", aria-*"


def _lex(markup, lang):
    """Lexical allowlist: every '<' either opens a strictly formed, allowed tag
    or is literal text. Returns (problems, number of start tags)."""
    problems, starts, seen = [], 0, set()

    def add(key, **kw):
        text = _mm(key, lang, **kw)
        if text not in seen:
            seen.add(text)
            problems.append(text)

    pos = 0
    while True:
        i = markup.find("<", pos)
        if i < 0:
            break
        nxt = markup[i + 1:i + 2]
        if nxt == "/":
            m = END_TAG_RE.match(markup, i)
            if not m:
                add("malformed", near=repr(markup[i:i + 40]))
                break
            tag = m.group(1).lower()
            if tag not in ALLOWED_TAGS:
                add("tag", tag=tag, allowed=", ".join(ALLOWED_TAGS))
            elif tag in VOID_TAGS:
                add("void_end", tag=tag)
            pos = m.end()
            continue
        if not ("a" <= nxt.lower() <= "z"):
            pos = i + 1  # a literal "<" in text ("3 < 5"): no browser reads it as a tag
            continue
        m = START_TAG_RE.match(markup, i)
        if not m:
            # Not in the strict spelling. Still name what is in it, so the
            # message says "<img>" and "onerror=" and not only "malformed".
            segment = TAG_SEGMENT_RE.match(markup, i).group(0)
            tag = re.match(r"<([a-zA-Z][a-zA-Z0-9]*)", segment).group(1).lower()
            if tag not in ALLOWED_TAGS:
                add("tag", tag=tag, allowed=", ".join(ALLOWED_TAGS))
            for handler in re.findall(r"(?<![\w-])(on[a-z]+)\s*=", segment, re.IGNORECASE):
                add("handler", attr=handler.lower(), tag=tag)
            add("malformed", near=repr(markup[i:i + 40]))
            break
        starts += 1
        tag = m.group(1).lower()
        if tag not in ALLOWED_TAGS:
            add("tag", tag=tag, allowed=", ".join(ALLOWED_TAGS))
        names = set()
        for am in ATTR_RE.finditer(m.group(2)):
            name = am.group(1).lower()
            value = html.unescape(am.group(2) or "")
            if name in names:
                add("dup_attr", attr=name, tag=tag)
            names.add(name)
            if name.startswith("on"):
                add("handler", attr=name, tag=tag)
            elif name in URL_ATTRS:
                add("url_attr", attr=name, tag=tag)
            elif name not in ALLOWED_ATTRS and not ARIA_ATTR_RE.match(name):
                add("attr", attr=name, tag=tag, allowed=_allowed_attrs_text())
            if name == "style":
                bad = CSS_FORBIDDEN.search(value) or CSS_FORBIDDEN.search(re.sub(r"\s+", "", value))
                if bad:
                    add("style", tag=tag, what=bad.group(0))
        if m.group(3) and tag not in VOID_TAGS:
            add("self_closing", tag=tag)
        pos = m.end()
    return problems, starts


def parse_markup(markup, lang="en"):
    """Check one mockup body against the allowlist and parse it.

    Returns (root, problems): `root` is the element tree (None when the markup
    was refused), `problems` the reasons in the requested language. An empty
    list means the string can be inserted into the card as it is.
    """
    if not isinstance(markup, str):
        return None, [_mm("not_string", lang, got=type(markup).__name__)]
    # By substring, not through the parser: how an unclosed "<!--" at the end of
    # input is read differs between Python versions, and a browser swallows the
    # rest of the card with it.
    if "<!" in markup or "<?" in markup:
        return None, [_mm("decl", lang)]
    ctl = CONTROL_RE.search(markup)
    if ctl:
        return None, [_mm("control", lang, ch="U+%04X" % ord(ctl.group(0)))]
    problems, starts = _lex(markup, lang)
    if problems:
        return None, problems
    builder = _TreeBuilder()
    builder.feed(markup)
    builder.close()
    problems = []
    for key, kw in builder.problems:
        text = _mm(key, lang, **kw)
        if text not in problems:
            problems.append(text)
    if builder.cur is not builder.root:
        problems.append(_mm("unclosed", lang, tag=builder.cur.tag))
    if builder.starts != starts:
        problems.append(_mm("disagree", lang))
    return (None if problems else builder.root), problems


def rings(node, out=None):
    """Every element under `node` that carries the `hl` class, in document order."""
    out = [] if out is None else out
    for k in node.kids:
        if isinstance(k, Node):
            if k.is_ring:
                out.append(k)
            rings(k, out)
    return out


class _RingCounter(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.count = 0

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == "class":  # the first class attribute is the one a browser keeps
                if "hl" in (value or "").split():
                    self.count += 1
                break

    handle_startendtag = handle_starttag


# ------------------------------------------------------- the changed element

def hl_count(markup):
    """How many elements in a mockup body carry the `hl` class.

    Counted from parsed start tags, the way a browser would see them: an
    unquoted `class=hl` is a ring, a `data-class="hl"` is not. Lenient on
    purpose (it also counts in markup the allowlist would refuse), so the ring
    rule can be reported next to the allowlist's own message.
    """
    if not isinstance(markup, str):
        return 0
    counter = _RingCounter()
    try:
        counter.feed(markup)
        counter.close()
    except Exception:  # pragma: no cover - HTMLParser does not raise on bad markup
        pass
    return counter.count


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


def _ring_placement(difference, a, b, shift_note_b, lang):
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


def ring_problems(difference, variant_a, variant_b, shift_note_b=None, lang="en"):
    """Where the ring must sit for each kind of difference (mockup-style.md).

    add    → the new element exists only in B, so only B can carry a ring
    remove → the element exists only in A; B is genuinely empty there, and a
             shift note under B says the content below moved up
    move   → the same element in two places: ringed in both
    change → ringed in B (ringing the old state in A too is allowed)

    Returns a list of problems (English by default, Turkish with lang="tr");
    empty means the placement is valid. card_problems() below runs this plus
    everything else that can be read off the two mockups.
    """
    if not difference:
        return []
    return _ring_placement(difference, hl_count(variant_a), hl_count(variant_b), shift_note_b, lang)


CARD_MSG = {
    "ring_label": ("ring in {v} has no data-note label (two or three words saying what changed)",
                   "{v} varyantındaki halkanın data-note etiketi yok (neyin değiştiğini söyleyen iki üç kelime)"),
    "ring_box": ("ring in {v} carries inline {prop}: a ring must not push content; give the spacing to the "
                 "children, and if the label collides use data-pos=\"below\" or card.note_pos",
                 "{v} varyantındaki halka satır içi {prop} taşıyor: halka içeriği itmemeli; boşluğu çocuk öğelere "
                 "verin, etiket çakışıyorsa data-pos=\"below\" ya da card.note_pos kullanın"),
    "class": ("variant_{vl}: class \"{cls}\" is not a template component; it would render unstyled "
              "(components are listed in the template's comment)",
              "variant_{vl}: \"{cls}\" sınıfı şablonda tanımlı bir bileşen değil; biçimsiz çizilir "
              "(bileşenler şablonun yorumunda listeli)"),
    "ring_style": ("ring in {v} carries inline {prop}: the ring wrapper adds no styling of its own "
                   "(mockup-style.md); put it on the element inside",
                   "{v} varyantındaki halka satır içi {prop} taşıyor: halka sarmalayıcısı kendi biçimini eklemez "
                   "(mockup-style.md); içteki öğeye yazın"),
    "label_long": ("ring label in {v} is {n} words (“{note}”); keep it to two or three",
                   "{v} varyantındaki halka etiketi {n} kelime (“{note}”); iki üç kelimede tutun"),
    "multi_ring": ("{n} rings in {v}: one change applied to {n} elements gets one ring around the group; "
                   "{n} rings read as {n} variables",
                   "{v} varyantında {n} halka var: {n} öğeye uygulanan tek değişiklik grubun etrafında tek halka alır; "
                   "{n} halka {n} değişken gibi okunur"),
    "move_diff": ("difference 'move': the ringed element differs between A and B; only its position may change "
                  "(same content, same label)",
                  "fark 'taşı': halkalı öğe A ile B arasında farklı; yalnızca yeri değişebilir "
                  "(aynı içerik, aynı etiket)"),
    "outside": ("A and B differ outside any ring ({where}: {na} node(s) in A, {nb} in B), e.g. {what}; a second "
                "variable, or a linked consequence the ring label or a shift note must name",
                "A ile B halkanın dışında da farklı ({where}: A'da {na}, B'de {nb} düğüm), ör. {what}; ikinci bir "
                "değişken ya da halka etiketinin veya kayma notunun adını koyması gereken bağlı bir sonuç"),
    "colour_b": ("inline colour only in Variant B: {vals}; a colour that exists only in B is a second variable "
                 "unless colour is what the test changes",
                 "yalnızca B varyantında geçen satır içi renk: {vals}; yalnızca B'de olan renk, test rengi "
                 "değiştirmiyorsa ikinci bir değişkendir"),
}

RING_PUSH_RE = re.compile(r"(?:^|;)\s*(margin|padding)(?:-[a-z-]+)?\s*:", re.IGNORECASE)
RING_STYLE_RE = re.compile(
    r"(?:^|;)\s*(border|outline|box-shadow|background|position|top|bottom|height|min-height|max-height|transform|float)"
    r"(?:-[a-z-]+)?\s*:", re.IGNORECASE)
COMPONENT_PREFIX = "r-"
COMPONENT_WORDS = ("ph", "hl", "img", "hero")
COLOUR_VALUE_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgb|hsl)a?\([^)]*\)|var\(--[\w-]+\)", re.IGNORECASE)
# The test is about colour when its variable or its ring label says so; then a
# colour that exists only in B is the tested difference, not a second one.
COLOUR_TOPIC_RE = re.compile(
    r"ren[kg]|colou?r|kontrast|contrast|\bton\b|dolgu|\bfill|zemin|arka\s*plan|background|vurgu|highlight",
    re.IGNORECASE)


def _cm(key, lang, **kw):
    en, tr = CARD_MSG[key]
    return (tr if lang == "tr" else en).format(**kw)


def component_classes(template_text):
    """Class names the template's <style> defines. Empty when the template has
    no component CSS (then class names cannot be checked)."""
    m = re.search(r"<style[^>]*>(.*?)</style>", template_text or "", re.DOTALL | re.IGNORECASE)
    if not m:
        return frozenset()
    names = frozenset(re.findall(r"\.([a-zA-Z_][\w-]*)", m.group(1)))
    return names if any(n.startswith(COMPONENT_PREFIX) for n in names) else frozenset()


def _walk(node):
    for k in node.kids:
        if isinstance(k, Node):
            yield k
            for sub in _walk(k):
                yield sub


def _norm_colour(value):
    v = re.sub(r"\s+", "", value.lower())
    if v.startswith("#") and len(v) in (4, 5):
        v = "#" + "".join(ch * 2 for ch in v[1:])
    return v


def inline_colours(root):
    """Every literal colour value written in a style attribute under `root`."""
    out = []
    for node in _walk(root):
        for value in COLOUR_VALUE_RE.findall(node.attrs.get("style") or ""):
            v = _norm_colour(value)
            if v not in out:
                out.append(v)
    return out


def _describe(k):
    if isinstance(k, str):
        return "“%s”" % k[:50]
    return ("<%s %s>" % (k.tag, " ".join('%s="%s"' % kv for kv in sorted(k.attrs.items()))))[:110]


def _outside_ring_diff(a, b, path="screen"):
    """Differences between two parsed mockups that no ring covers.

    The children of A and B are aligned on ring-blind structural keys; a region
    that differs must consist of ringed nodes (the tested element), or be a
    like-for-like pair that can be looked into. Anything else is reported.
    Returns [(where, nodes in A, nodes in B, example)].
    """
    def ringed(k):
        return isinstance(k, Node) and k.is_ring

    def key(k):
        return k.key(True) if isinstance(k, Node) else k

    ka, kb = a.kids, b.kids
    found = []
    sm = difflib.SequenceMatcher(None, [key(k) for k in ka], [key(k) for k in kb], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        ma, mb = ka[i1:i2], kb[j1:j2]
        if all(ringed(k) for k in ma + mb):
            continue  # ring against ring, or a ring that exists on one side only (add, remove, move)
        if len(ma) == 1 and len(mb) == 1 and (ringed(ma[0]) or ringed(mb[0])):
            continue  # the element in A against its ringed state in B
        if (len(ma) == 1 and len(mb) == 1 and isinstance(ma[0], Node) and isinstance(mb[0], Node)
                and ma[0].tag == mb[0].tag and ma[0].attrs == mb[0].attrs):
            found += _outside_ring_diff(ma[0], mb[0], "%s > %s[%d]" % (path, ma[0].tag, i1))
            continue
        loose = [k for k in mb + ma if not ringed(k)]
        found.append(("%s, child %d" % (path, i1), len(ma), len(mb), _describe(loose[0])))
    return found


def card_problems(difference, variant_a, variant_b, shift_note_b=None, lang="en",
                  variable=None, classes=None):
    """Everything that can be read off the two mockup bodies.

    Returns (errors, warnings). Errors refuse the card: markup outside the
    allowlist, ring placement against the difference type, a ring without a
    label, a ring that carries its own margin or padding, a class that is not a
    template component (only when `classes`, the template's own class names, is
    given). Warnings are for the reviewer: a long label, several rings, a
    'move' whose element changed, a difference no ring covers, a colour that
    exists only in B.

    Shared with validate_scenario_json.py, so the two never disagree.
    """
    errors, warnings, trees = [], [], {}
    for field, markup in (("variant_a", variant_a), ("variant_b", variant_b)):
        root, problems = parse_markup(markup, lang)
        errors += ["%s: %s" % (field, p) for p in problems]
        trees[field] = root
    if difference:
        errors += _ring_placement(difference, hl_count(variant_a), hl_count(variant_b), shift_note_b, lang)
    if trees["variant_a"] is None or trees["variant_b"] is None:
        return errors, warnings

    ring_lists = {}
    for field, name in (("variant_a", "A"), ("variant_b", "B")):
        found = rings(trees[field])
        ring_lists[name] = found
        for ring in found:
            note = (ring.attrs.get("data-note") or "").strip()
            style = ring.attrs.get("style") or ""
            if not note:
                errors.append(_cm("ring_label", lang, v=name))
            elif len(note.split()) > 4:
                warnings.append(_cm("label_long", lang, v=name, n=len(note.split()), note=note))
            push = RING_PUSH_RE.search(style)
            if push:
                errors.append(_cm("ring_box", lang, v=name, prop=push.group(1).lower()))
            extra = RING_STYLE_RE.search(style)
            if extra:
                warnings.append(_cm("ring_style", lang, v=name, prop=extra.group(1).lower()))
        if len(found) > 1:
            warnings.append(_cm("multi_ring", lang, v=name, n=len(found)))
        if classes:
            for node in _walk(trees[field]):
                for cls in node.classes:
                    if (cls.startswith(COMPONENT_PREFIX) or cls in COMPONENT_WORDS) and cls not in classes:
                        text = _cm("class", lang, vl=name.lower(), cls=cls)
                        if text not in errors:
                            errors.append(text)

    if difference == "move" and ring_lists["A"] and ring_lists["B"]:
        ka = sorted(repr(r.key(True)) for r in ring_lists["A"])
        kb = sorted(repr(r.key(True)) for r in ring_lists["B"])
        na = sorted((r.attrs.get("data-note") or "").strip() for r in ring_lists["A"])
        nb = sorted((r.attrs.get("data-note") or "").strip() for r in ring_lists["B"])
        if ka != kb or na != nb:
            warnings.append(_cm("move_diff", lang))

    for where, na, nb, what in _outside_ring_diff(trees["variant_a"], trees["variant_b"]):
        warnings.append(_cm("outside", lang, where=where, na=na, nb=nb, what=what))

    labels = " ".join((r.attrs.get("data-note") or "") for r in ring_lists["A"] + ring_lists["B"])
    if not COLOUR_TOPIC_RE.search("%s %s" % (variable or "", labels)):
        in_a = set(inline_colours(trees["variant_a"]))
        only_b = [c for c in inline_colours(trees["variant_b"]) if c not in in_a]
        if only_b:
            vals = ", ".join(only_b[:4]) + (" (+%d)" % (len(only_b) - 4) if len(only_b) > 4 else "")
            warnings.append(_cm("colour_b", lang, vals=vals))
    return errors, warnings


COLOR_MSG = {
    "syntax": ("brand.{key} must be a plain colour (#hex, rgb(), hsl() or a CSS colour name), got {val!r}",
               "brand.{key} düz bir renk olmalı (#hex, rgb(), hsl() ya da bir CSS renk adı), gelen {val!r}"),
    "name": ("brand.{key}: {val!r} is not a colour name a browser knows, so the button would render transparent; "
             "give the colour as #hex (e.g. #0b4dc2), rgb()/hsl() or a CSS colour name such as navy",
             "brand.{key}: {val!r} tarayıcının tanıdığı bir renk adı değil, buton saydam çizilir; rengi #hex "
             "(ör. #0b4dc2), rgb()/hsl() ya da navy gibi bir CSS renk adı olarak yazın"),
}


def color_problem(value, key="primary", lang="en"):
    """Why `value` is not usable as a brand colour, or None when it is."""
    idx = 1 if lang == "tr" else 0
    if not isinstance(value, str) or not COLOR_RE.match(value.strip()):
        return COLOR_MSG["syntax"][idx].format(key=key, val=value)
    v = value.strip()
    if v[0] != "#" and "(" not in v and v.lower() not in NAMED_COLORS:
        return COLOR_MSG["name"][idx].format(key=key, val=value)
    return None


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
        problem = color_problem(value, key, _MSG_LANG)
        if problem:
            die(problem)
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

def build(template_text, scenario, warnings=None, lang=None):
    """Fill the template from one scenario and return the card's HTML.

    Dies (exit 2) on anything that must not reach a card. Non-blocking remarks
    about the mockups are appended to `warnings` when a list is passed; main()
    prints them. `lang` is the language of those messages (default: --lang).
    """
    lang = lang or _MSG_LANG
    view = normalize(scenario)
    card_lang = view["lang"]
    L = L10N[card_lang]

    for key in ("variant_a", "variant_b"):
        value = view[key]
        if value in (None, ""):
            die(_t("scenario is missing required card field: %s",
                   "senaryoda zorunlu kart alanı eksik: %s", lang) % key)
        if not isinstance(value, str) or not value.strip():
            die(_t("card field %s must be a non-empty string of markup, got %s",
                   "%s kart alanı boş olmayan bir işaretleme metni olmalı, gelen %s", lang)
                % (key, type(value).__name__))

    errors, notes = card_problems(view["difference"], view["variant_a"], view["variant_b"],
                                  view["shift_note_b"], lang=lang, variable=view["variable"],
                                  classes=component_classes(template_text))
    if errors:
        die(_t("the mockup was refused; nothing was cleaned or rewritten, fix the input:\n  ",
               "mockup reddedildi; hiçbir şey temizlenmedi ya da yeniden yazılmadı, girdiyi düzeltin:\n  ", lang)
            + "\n  ".join(errors))
    if warnings is not None:
        warnings.extend(notes)

    text = COMMENT_RE.sub("", template_text)

    # User text never goes into the template directly: the frame helpers leave a
    # placeholder and its value joins the one substitution pass below.
    values = {}
    device = view["device"]
    if device == "web":
        text = to_browser_skeleton(text)
        values["{{URL}}"] = escape(view["url"])
    elif device == "phone-web":
        text = apply_mobile_address_bar(text)
        values["{{DOMAIN}}"] = escape(domain_of(view["url"]))
    else:
        labels = bottom_nav_labels(view["bottom_nav"])
        text = apply_bottom_nav(text, bool(labels))
        if labels:
            values["{{BOTTOM_NAV}}"] = bottom_nav_html(labels, view["bottom_nav_active"])

    values.update({
        "{{TITLE}}": escape(view["title"]),
        "{{DESC}}": escape(view["desc"]),
        "{{LANG}}": card_lang,
        "{{DEVICE}}": device,
        "{{NOTE_POS}}": view["note_pos"],
        "{{H_TEST}}": escape(L["h_test"]),
        "{{H_KPI}}": escape(L["h_kpi"]),
        "{{H_DONT}}": escape(L["h_dont"]),
        "{{SHIFT_NOTE_A}}": shift_note(view["shift_note_a"]),
        "{{SHIFT_NOTE_B}}": shift_note(view["shift_note_b"]),
        "{{FOOTER}}": render_footer(view),
        "{{BRAND_CSS}}": brand_css(view["brand"]),
    })
    for ph, key in LIST_PLACEHOLDERS.items():
        values[ph] = render_list(view[key], lang=card_lang)
    # Screens go in raw: this is the generative region, checked above.
    for ph, key in SCREEN_PLACEHOLDERS.items():
        values[ph] = view[key]

    # The template is checked BEFORE anything is filled in, so a "{{AD}}" inside
    # a title or a mockup is never mistaken for a placeholder of the template.
    unknown = sorted(set(PLACEHOLDER_RE.findall(text)) - set(values))
    if unknown:
        die("template has placeholders this tool does not fill: %s" % ", ".join(unknown))

    # Drop the line of a placeholder that fills with nothing (an absent shift
    # note or footer) so the delivered source carries no whitespace-only line.
    # Done on the template, not on the filled card: the mockups are inserted
    # byte for byte and their own blank lines are not ours to remove.
    for ph, value in values.items():
        if value == "":
            text = re.sub(r"(?m)^[ \t]+%s[ \t]*\n" % re.escape(ph), "", text)

    # One pass. Inserted text is never scanned again: a footer note that says
    # "{{VARIANT_B_SCREEN}}" stays a footer note.
    text = PLACEHOLDER_RE.sub(lambda m: values[m.group(0)], text)

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


def self_verify(built_text, template_text, device=None, variants=None):
    """Refuse to emit a card that drifted from the template's fixed skeleton,
    or that carries executable markup.

    `device` is accepted for call-site symmetry but no longer changes the check:
    the device-dependent region is excluded structurally by fixed_lines().

    `variants` are the two raw mockup strings. The allowlist in build() is the
    gate; this is the second layer behind it. Tag-shaped patterns (<script,
    <iframe …) are searched in the whole built card, where escaped text can
    never match them. Scheme and handler patterns are searched inside the tags
    of the raw variants only, after entity decoding and with whitespace and
    control characters removed: a box label or a line of mockup text saying
    "JavaScript:" is ordinary text, a "jav&#x61;script:" in an attribute is not.
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
    for pattern, description in DANGEROUS_TAGS:
        if pattern.search(built_text):
            die("cards are static HTML; refusing to emit a card containing %s" % description)
    for raw in variants or ():
        # Only what sits inside a tag: the mockup's visible text may well say
        # "JavaScript: on" or show "&lt;script&gt;" as text.
        for tag in TAG_SEGMENT_RE.findall(str(raw)):
            decoded = html.unescape(tag)
            packed = re.sub(r"[\x00-\x20]+", "", decoded)
            for pattern, description in DANGEROUS_PATTERNS:
                # Both readings: with its spacing (an attribute needs the space
                # before it) and packed (a scheme survives a tab in its middle).
                if pattern.search(decoded) or pattern.search(packed):
                    die("cards are static HTML; refusing to emit a card whose mockup contains %s" % description)


# -------------------------------------------------------- checks before building

FRAME_MSG = {
    "nav_device": ("card.bottom_nav: only valid with device 'phone' (native app); a '{device}' frame draws no tab bar",
                   "card.bottom_nav: yalnızca device 'phone' (yerel uygulama) ile kullanılır; '{device}' çerçevesinde "
                   "sekme çubuğu çizilmez"),
    "url": ("card.url: device '{device}' draws an address bar; give the domain (if it was not visible, use a "
            "representative one and say so in footer_notes)",
            "card.url: device '{device}' adres çubuğu çizer; alan adını yazın (görünmüyorsa temsilî bir adres yazıp "
            "footer_notes'ta belirtin)"),
    "nav_active": ("card.bottom_nav_active: {val!r} names no tab in bottom_nav; give a tab's label or its 0-based index",
                   "card.bottom_nav_active: {val!r} bottom_nav'daki hiçbir sekmeyle eşleşmiyor; sekmenin adını ya da "
                   "0 tabanlı sırasını yazın"),
}


def frame_problems(device, url, bottom_nav, bottom_nav_active=None, lang="en"):
    """Frame fields that would otherwise be dropped or drawn empty in silence.

    Shared with validate_scenario_json.py. Returns a list of problems.
    """
    idx = 1 if lang == "tr" else 0
    out = []
    has_nav = isinstance(bottom_nav, list) and len(bottom_nav) > 0
    if device in ("web", "phone-web"):
        if has_nav:
            out.append(FRAME_MSG["nav_device"][idx].format(device=device))
        if not (isinstance(url, str) and url.strip()):
            out.append(FRAME_MSG["url"][idx].format(device=device))
    elif has_nav and all(isinstance(x, str) for x in bottom_nav):
        if active_tab_index(bottom_nav, bottom_nav_active) == -1:
            out.append(FRAME_MSG["nav_active"][idx].format(val=bottom_nav_active))
    return out


LEGACY_BOXES = ("test_items", "kpi_items", "dont_items")
MIN_BOX_ITEMS = 3


def is_scenario_shape(scenario):
    """The canonical shape carries `kpis` and/or a `card` object; the legacy
    flat shape carries kpi_items and the card fields at the top level."""
    return isinstance(scenario.get("kpis"), list) or isinstance(scenario.get("card"), dict)


def preflight(scenario, lang="en"):
    """What must hold before a card is built. Returns (errors, warnings).

    The scenario shape goes through the same validator the skills run
    (validate_scenario_json): the builder used to enforce ring counts only, so
    empty boxes, four primary KPIs or a null list item all produced a card.
    The legacy flat shape has no schema; its three boxes are checked here.
    """
    errors, warnings = [], []
    if is_scenario_shape(scenario):
        if not isinstance(scenario.get("card"), dict):
            return [_t("the scenario has no `card` object. It can be a valid scenario as it is "
                       "(validate_scenario_json.py checks it without one), but a card needs card.variant_a, "
                       "card.variant_b and card.difference: add `card` at render time",
                       "senaryoda `card` nesnesi yok. Senaryo bu hâliyle geçerli olabilir (validate_scenario_json.py "
                       "onu kartsız da denetler), ama kart için card.variant_a, card.variant_b ve card.difference "
                       "gerekir: `card` nesnesini çizim aşamasında ekleyin", lang)], warnings
        # Imported here, not at module level: the validator imports this module.
        import validate_scenario_json as vsj
        schema = vsj.load_schema()
        errors = vsj.validate(scenario, schema, lang)
        warnings = vsj.lint(scenario, schema, lang, include_card=False)
        return errors, warnings

    for box in LEGACY_BOXES:
        items = scenario.get(box)
        if not isinstance(items, list) or len(items) < MIN_BOX_ITEMS:
            have = len(items) if isinstance(items, list) else 0
            errors.append(_t("%s: has %d item(s), a box needs at least %d",
                             "%s: %d madde var, bir kutuda en az %d olmalı", lang) % (box, have, MIN_BOX_ITEMS))
            continue
        for i, item in enumerate(items):
            if isinstance(item, str):
                ok = bool(item.strip())
            elif isinstance(item, dict):
                ok = isinstance(item.get("text"), str) and bool(item["text"].strip())
            else:
                ok = False
            if not ok:
                errors.append(_t("%s[%d]: a box item is a non-empty string or {label, text} with a non-empty text, got %r",
                                 "%s[%d]: kutu maddesi boş olmayan bir metin ya da metni dolu bir {label, text} olmalı, "
                                 "gelen %r", lang) % (box, i, item))
    device = scenario.get("device") or "phone"
    errors += frame_problems(device, scenario.get("url"), scenario.get("bottom_nav"),
                             scenario.get("bottom_nav_active"), lang)
    if not scenario.get("difference"):
        warnings.append(_t("no `difference` (change / add / move / remove): ring placement was not checked",
                           "`difference` yok (change / add / move / remove): halka yerleşimi denetlenmedi", lang))
    return errors, warnings


def main(argv):
    global _MSG_LANG
    ap = argparse.ArgumentParser(description="Build a scenario card from the template.")
    ap.add_argument("--template", required=True, help="path to templates/scenario-card.html")
    ap.add_argument("--scenario", required=True, help="JSON file describing the scenario")
    ap.add_argument("--out", required=True, help="path to write the card to")
    ap.add_argument("--lang", choices=("en", "tr"), default="en",
                    help="language of this tool's messages (default: en)")
    args = ap.parse_args(argv)
    _MSG_LANG = args.lang

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

    errors, warnings = preflight(scenario, args.lang)
    if errors:
        die(_t("the scenario was refused (%d problem(s)); no card was written:\n  - ",
               "senaryo reddedildi (%d sorun); kart yazılmadı:\n  - ") % len(errors) + "\n  - ".join(errors))

    built = build(template_text, scenario, warnings=warnings)
    view = normalize(scenario)
    self_verify(built, template_text, view["device"], variants=(view["variant_a"], view["variant_b"]))

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(built)

    for note in warnings:
        warn(note)
    print("built %s (%d bytes, device=%s, lang=%s, difference=%s%s)" % (
        args.out, len(built.encode("utf-8")), view["device"], view["lang"],
        view["difference"] or "-", ", %d warning(s)" % len(warnings) if warnings else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
