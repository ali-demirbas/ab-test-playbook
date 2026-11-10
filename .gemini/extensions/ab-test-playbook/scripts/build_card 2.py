#!/usr/bin/env python3
"""Deterministically build a scenario card HTML from its template by copying the
template and substituting ONLY the placeholder regions — the cp-then-edit
mechanism CLAUDE.md mandates, done in code so it is correct every run.

The card is the comparison and nothing else: the record's title (a question) at
the top, then Variant A and Variant B side by side in a device frame each, the
ring (.hl) around the changed element and its short label. None of the record's
other text (problem, KPI, guardrail, evidence, priority, warnings, invariants,
detail) is written into the card; what the user needs of it lives in the chat.

Why a script rather than hand-editing:

  1. **Escaping is a correctness bug, not a style preference.** The title is
     interpolated straight into markup; "CTA < 3 kelime olmalı mı?" would break
     it. Every text value (title, address, tab labels) goes through
     html.escape() before it reaches the template.

  2. **The template's developer comment documents the same structure as the
     live skeleton.** A naive string replace would fill the comment too and ship
     a half-substituted example block inside the delivered card. This tool
     strips the comment first, then substitutes.

  3. **Retyping ~200 lines of fixed CSS per card is the pipeline's largest time
     cost and its main drift risk.** After building, this tool self-verifies
     that every fixed line of the template (for the card's device frame)
     survived unchanged and refuses to emit a card that drifted.

Input: ONE scenario record (templates/scenario.schema.json; see
examples/scenario.json). The card reads title and lang (→ <html lang>), and
card{variant_a, variant_b, difference (the record's; when both are given they
must be equal, the card never overrides the record), device (else the
record's), url, bottom_nav, bottom_nav_active, brand, note_pos, phone_scale,
mobile_toolbar, stage_captions}; mockup_basis is
metadata for the mockup reviewer (written into the manifest, never drawn). The
gates also read variable, numeric_change and warnings, a critical item in
`assumptions` makes the card conditional (below), and the review gates read
review{scenario_critic, mockup_reviewer} (never drawn on the card). The
record is validated against the schema first (validate_scenario_json): a record
with errors is refused; its warnings are printed and don't block. A record
without a `card` object is a valid record but not a renderable one; the builder
says so.

  device:     phone      native app screen; a tab bar only via bottom_nav (a
                         list of strings), its active tab via bottom_nav_active
                         (that tab's label or 0-based index)
              phone-web  mobile browser: status bar + address bar (lock + domain
                         from url), never a tab bar
              web        desktop browser frame filling its column
  difference: change | add | move | remove (Turkish değiştir | ekle | taşı | kaldır
              accepted). The ring (.hl) placement is enforced — see ring_problems().
              card.difference that differs from the record's is refused
              (difference_problems): the card would show another test than
              the one reviewed. A move is drawn as a move, also below the
              first view or to a later screen (layout markers below; only the
              ring moves). Each arm's label says where the element is in that
              arm; the element's content is identical.
  layout:     phone and phone-web only. A bare <div class="r-fold"></div> at
              the top level of a screen splits it: what comes before is the
              first view (in the phone), what comes after is drawn under the
              phone as a continuation sheet (.below). Both arms or neither.
              <div class="r-sticky">one element</div> before the fold is a bar
              pinned to the bottom of the first view; a pinned element is
              drawn this way, never inside the page flow. A bare
              <div class="r-stage-break"></div> splits a screen into two
              stages, drawn as two small phones with card.stage_captions.
              card.mobile_toolbar (phone-web) draws the browser's bottom
              toolbar, the same in both arms. .hl-soft marks a linked
              consequence of the variable (at most two per arm, next to a .hl).
  lang:       tr (default) | en: <html lang> and the draft ribbon.
  brand:      {"primary": "#c9392b", "on_primary": "#fff", "name": "Marka"} →
              CSS variables used by .r-cta, .r-header, .r-logo, .r-tabs …
              Without it the neutral palette stays. A colour is #hex, rgb()/
              hsl() or one of the CSS colour names; anything else is refused.

`variant_a` / `variant_b` are raw markup produced by the model for the mockup
region and are inserted verbatim — that region is generative by design, only
its surrounding skeleton is fixed. Because it is raw, it passes an ALLOWLIST
first (parse_markup): a closed set of inert tags and attributes, every
attribute value double-quoted, no comments, balanced tags, screened inline CSS.
A mockup that needs anything else is refused with a message naming the tag or
attribute; nothing is cleaned or rewritten.

Mechanical quality gates (code checks what code can check; the reviewers
check the rest, and delivery needs both):

  * A/B diff. The two mockups are parsed and aligned. Any difference outside
    the rings refuses the card; every change inside the rings is listed in a
    diff manifest for mockup-reviewer (text, numbers, components, modifier
    classes, attributes and inline styles, each with its ring label).
  * Numbers. A price, amount, percentage, count or rating that differs
    between A and B, inside or outside a ring, refuses the card unless the
    record says why in `numeric_change`.
  * Accessibility. B adding an interactive component (or more of one) refuses
    the card unless the record carries an accessibility warning with the
    criteria that element needs.
  * Regulation and manipulation (heuristic keyword lists, see the constants):
    legal or mandatory text in A missing or changed in B (rule 11), security
    or verification text in A missing in B (rule 6), a consent box unticked
    in A and ticked in B, or shown in A and removed in B (rule 6).
  * Personal data. Values shaped like a TCKN, a TR IBAN, a card number, an
    e-mail address or a mobile number refuse the card; masks ("•••") and
    all-zero placeholders pass.

What a browser shows (size, clipping, ring and label overlap, font size,
contrast, A/B alignment) is measured by scripts/render_check.mjs, not here.

Conditional card. A record with at least one critical assumption
(`assumptions[].type == "critical"`) builds a conditional card: the final
bytes carry an amber ribbon ("KOŞULLU · doğrulama gerekli" / "CONDITIONAL ·
needs verification") at the card's top-left corner and <meta
name="abtest-status" content="conditional">; the build summary (draft and
stamped build) says "conditional card (not implementation-ready)". It is never
a final card. A record without one builds exactly as before.

Review gates. A draft (--draft) needs the scenario-critic stamp whose
fingerprint equals the record's (validate_scenario_json.record_fingerprint);
it writes the final card's HTML plus a draft ribbon overlaid on the card and
two meta tags, writes <out>.manifest.json and prints the final card's
fingerprint (of a conditional card: of its conditional bytes). A final build (the default) needs both stamps: scenario-critic =
the record's fingerprint, mockup-reviewer = the sha256 of the exact bytes it is
about to write. Everything is built in memory and written only when every gate
passed.

Usage:
  build_card.py --template templates/scenario-card.html \\
                --scenario scenario.json \\
                --out abtest-card-kupon-alani.draft.html --draft [--lang tr]
  build_card.py --template templates/scenario-card.html \\
                --scenario scenario.json \\
                --out abtest-card-kupon-alani.html [--lang tr]

--draft  build the review draft (ribbon, meta tags, manifest) instead of the
         final card.
--lang   language of the builder's own messages (en, the default, or tr).

Exit: 0 = written and self-verified (warnings, if any, go to stderr as
"build_card: warning: ..."), 1 = refused by a gate (the message names it;
nothing was written and an existing --out is left untouched), 2 = usage error
or unreadable input.
"""
import argparse
import collections
import difflib
import hashlib
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

# validate_scenario_json ships next to this file and is imported lazily below.
# Put this directory on the path so that also works under `python3 -I`, whose
# isolated mode leaves the script's own directory off sys.path.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import screen_spec as ss  # noqa: E402  (ships next to this file; the screen spec compiler)

DEVICES = ("phone", "phone-web", "web")
DIFFERENCES = ("change", "add", "move", "remove")
# The archive's "Fark:" line spells the type in Turkish; the schema accepts
# those spellings, and the builder also forgives a missing Turkish letter.
DIFFERENCE_TR = {"değiştir": "change", "ekle": "add", "taşı": "move", "kaldır": "remove"}
DIFFERENCE_ALIASES = dict(DIFFERENCE_TR, degistir="change", tasi="move", kaldir="remove")
MOCKUP_BASES = ("shared_page", "described", "representative")
NOTE_POSITIONS = ("above", "below")
# The phone frame is drawn 1.2× (fills its column); 1 keeps it at 420px so a tall screen fits the stage,
# 1.4 enlarges a short screen that would leave most of the stage empty.
PHONE_SCALES = (1.2, 1, 1.4)
# card.web_scale: a desktop browser frame is as tall as its content and its text a fixed 14px, so a short
# page (a cart summary, a pricing row) leaves most of the stage empty. 1.2 / 1.4 zoom the whole frame
# (proportions kept, the frame still fills its column). The rule is written only into cards that use it,
# so every other card's bytes stay the same.
WEB_SCALES = (1, 1.2, 1.4)
PHONE_SCALE_ATTR = {1.2: "1.2", 1: "1", 1.4: "1.4"}
# The card's own language: <html lang> and the draft ribbon. The title is
# already in the user's language (rule 7); the pills say "Variant A/B" in both.
CARD_LANGS = ("tr", "en")

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


DIFF_KEYS = {"change": "change", "add": "add", "move": "move", "remove": "remove"}
DIFF_KEYS.update(DIFFERENCE_ALIASES)

# card.difference no longer overrides the record's difference: the critic
# reviewed the record's, and a card drawn as another type (a move drawn as an
# added or a removed element) shows the user a different test than the one
# reviewed. The hint says how to draw the record's type.
DIFF_MSG = {
    "mismatch": ("card.difference '{card}' differs from the record's difference '{record}': the card would misrepresent "
                 "the variable the record states and the critic reviewed, so it is refused. The card draws the record's "
                 "difference: drop card.difference or set it to '{record}'. {hint}",
                 "card.difference '{card}', kaydın difference değeri '{record}' ile aynı değil: kart, kaydın söylediği ve "
                 "eleştirmenin incelediği değişkeni yanlış gösterir, bu yüzden reddedilir. Kart kaydın farkını çizer: "
                 "card.difference alanını kaldırın ya da '{record}' yapın. {hint}"),
    "move": ("To draw a move: ring the same element in both arms, with identical content and a label that says "
             "where it is in that arm, at its old place in A and its new place in B. A move below the first view or "
             "to a pinned bar: both arms split the screen with <div class=\"r-fold\"></div> at the same place; A "
             "rings the element in the continuation, B rings it in the first view, a pinned element inside "
             "<div class=\"r-sticky\"></div> before the fold. A move to a later screen: both arms split the screen "
             "with <div class=\"r-stage-break\"></div> (card.stage_captions names the two stages), B rings the "
             "element in the second stage.",
             "Taşıma şöyle çizilir: aynı öğeye iki kolda da aynı içerikle halka çizin, etiket öğenin o koldaki yerini "
             "söyler; A'da eski yerinde, B'de yeni yerinde. İlk ekranın altına ya da sabit bara taşıma: iki kol da "
             "ekranı aynı yerde <div class=\"r-fold\"></div> ile böler; A öğeyi devamında, B ilk ekranda halkalar, "
             "sabit öğe kıvrımdan önce <div class=\"r-sticky\"></div> içinde. Sonraki ekrana taşıma: iki kol da "
             "ekranı <div class=\"r-stage-break\"></div> ile böler (card.stage_captions iki aşamayı adlandırır), B "
             "öğeyi ikinci aşamada halkalar."),
    "add": ("To draw an addition: ring the new element in Variant B only; A has no ring.",
            "Ekleme şöyle çizilir: halka yalnızca B'deki yeni öğede; A'da halka yok."),
    "remove": ("To draw a removal: ring the element in Variant A only (labelled); B is genuinely empty in its place.",
               "Kaldırma şöyle çizilir: halka yalnızca A'daki öğede (etiketli); B'de o alan gerçekten boş."),
    "change": ("To draw a change: ring the changed element in Variant B (ringing its old state in A is allowed).",
               "Değiştirme şöyle çizilir: B'de değişen öğeye halka çizin (A'daki eski hâline halka çizmek serbest)."),
}


def _difference_key(value):
    """change/add/move/remove for a known spelling, else None (never dies)."""
    if not isinstance(value, str) or not value.strip():
        return None
    return DIFF_KEYS.get(value.strip().lower())


def difference_problems(scenario, lang="en"):
    """card.difference against the record's difference. Returns [] or one problem.

    Shared with validate_scenario_json.py. Silent when either side is missing
    (then the other one is the card's difference) or not a known spelling
    (the schema reports that); one problem when both are known and differ.
    """
    if not isinstance(scenario, dict) or not isinstance(scenario.get("card"), dict):
        return []
    card_value, record_value = scenario["card"].get("difference"), scenario.get("difference")
    card_diff, record_diff = _difference_key(card_value), _difference_key(record_value)
    if card_diff is None or record_diff is None or card_diff == record_diff:
        return []
    idx = 1 if lang == "tr" else 0
    return [DIFF_MSG["mismatch"][idx].format(card=card_value, record=record_value, hint=DIFF_MSG[record_diff][idx])]


NO_CARD_MSG = ("the record has no `card` object. It can be a valid record as it is (validate_scenario_json.py "
               "checks it without one), but a card needs card.variant_a and card.variant_b (and a difference, the "
               "card's or the record's): add `card` at render time",
               "kayıtta `card` nesnesi yok. Kayıt bu hâliyle geçerli olabilir (validate_scenario_json.py onu kartsız "
               "da denetler), ama kart için card.variant_a ve card.variant_b (ve kartın ya da kaydın difference "
               "değeri) gerekir: `card` nesnesini çizim aşamasında ekleyin")


def normalize(scenario, msg_lang=None):
    """The scenario record → the flat view the renderer and the gates work from.

    Only the title and the card fields reach the card; variable,
    numeric_change and warnings are read by the gates, mockup_basis goes into
    the manifest, a critical assumption makes the card conditional. The
    card's difference is the record's: card.difference may repeat it (in any
    accepted spelling) but never overrides it (difference_problems). `msg_lang`
    is the language of the messages (default: --lang).
    """
    if not isinstance(scenario, dict):
        die("scenario must be a JSON object")
    card = scenario.get("card")
    if not isinstance(card, dict):
        die(_t(*NO_CARD_MSG))

    # Contract 8: the screen spec form (card.screen + card.change) compiles to
    # the two mockup bodies here, before anything else reads them, so every
    # gate below sees exactly the markup the card is drawn from. Both forms at
    # once, or a spec the compiler can't draw, refuse the card.
    screen_spec = False
    form = ss.card_form(card)
    if form in ("spec", "both") or "soft" in card:
        a, b, problems = ss.compile_card(card, msg_lang or _MSG_LANG)
        if problems:
            die(_t("the screen spec was refused; nothing was drawn, fix the input:\n  ",
                   "ekran tanımı reddedildi; hiçbir şey çizilmedi, girdiyi düzeltin:\n  ", msg_lang)
                + "\n  ".join(problems))
        card = dict(card, variant_a=a, variant_b=b)
        screen_spec = True

    lang = scenario.get("lang") or "tr"
    if lang not in CARD_LANGS:
        die("lang must be one of %s, got %r" % ("/".join(CARD_LANGS), lang))

    device = card.get("device") or scenario.get("device") or "phone"
    if device == "both":
        die("device 'both' has no single frame to draw: pick phone (native app), "
            "phone-web (mobile browser) or web (desktop browser) for the card, "
            "and state the audience in the setup notes")
    if device not in DEVICES:
        die("device must be one of %s, got %r" % ("/".join(DEVICES), device))

    basis = card.get("mockup_basis")
    if basis is None and isinstance(scenario.get("variants"), list):
        current = any(isinstance(v, dict) and v.get("is_current") for v in scenario["variants"])
        basis = "shared_page" if current else "representative"
    if basis is not None and basis not in MOCKUP_BASES:
        die("mockup_basis must be one of %s, got %r" % ("/".join(MOCKUP_BASES), basis))

    note_pos = card.get("note_pos") or "above"
    if note_pos not in NOTE_POSITIONS:
        die("note_pos must be 'above' or 'below', got %r" % note_pos)

    phone_scale = card.get("phone_scale", 1.2)
    if isinstance(phone_scale, bool) or phone_scale not in PHONE_SCALES:
        die("card.phone_scale must be 1, 1.2 (default) or 1.4, got %r" % (phone_scale,))
    if phone_scale != 1.2 and device not in ("phone", "phone-web"):
        die("card.phone_scale applies to a phone frame (device phone or phone-web), not %r" % device)
    inherited = card.get("inherited_contrast") or []
    if inherited:
        if basis != "shared_page":
            die("card.inherited_contrast is only for a shared page (card.mockup_basis shared_page): it documents a "
                "contrast defect copied from the user's own screen")
        if not isinstance(inherited, list):
            die("card.inherited_contrast must be a list of {\"text\": …, \"color\": \"#rrggbb\"}")
        for item in inherited:
            text_ok = isinstance(item, dict) and isinstance(item.get("text"), str) and item["text"].strip()
            if not text_ok or not re.match(r"^#[0-9a-fA-F]{6}$", str(item.get("color", ""))):
                die("card.inherited_contrast: each entry is {\"text\": <the element's exact text>, "
                    "\"color\": \"#rrggbb\" as measured on the screen}, got %r" % (item,))
            needle = ">%s<" % escape(item["text"].strip())
            in_a = card.get("variant_a", "").count(needle)
            in_b = card.get("variant_b", "").count(needle)
            if not in_a or in_a != in_b:
                die("card.inherited_contrast: %r must be the text of an element drawn the same in both arms "
                    "(A has it %d time(s), B %d)" % (item["text"], in_a, in_b))
    web_scale = card.get("web_scale", 1)
    if isinstance(web_scale, bool) or web_scale not in WEB_SCALES:
        die("card.web_scale must be 1 (default), 1.2 or 1.4, got %r" % (web_scale,))
    if web_scale != 1 and device != "web":
        die("card.web_scale applies to a desktop browser frame (device web), not %r" % device)

    mismatch = difference_problems(scenario, msg_lang or _MSG_LANG)
    if mismatch:
        die(mismatch[0])
    difference = card.get("difference")
    if difference in (None, ""):
        difference = scenario.get("difference")
    return {
        "lang": lang,
        "device": device,
        "title": scenario.get("title", ""),
        "variant_a": card.get("variant_a", ""),
        "variant_b": card.get("variant_b", ""),
        "url": card.get("url", "") or "",
        "bottom_nav": card.get("bottom_nav"),
        "bottom_nav_active": card.get("bottom_nav_active"),
        "variable": scenario.get("variable"),
        "difference": normalize_difference(difference),
        "brand": card.get("brand"),
        "mockup_basis": basis,
        "note_pos": note_pos,
        "phone_scale": PHONE_SCALE_ATTR[phone_scale],
        "web_scale": web_scale,
        "inherited_contrast": [{"text": i["text"].strip(), "color": i["color"].lower()} for i in inherited],
        # True when the two mockups were compiled from card.screen + card.change (screen_spec.py).
        "screen_spec": screen_spec,
        # Layout fields (layout_field_problems checks them, apply_layout draws them).
        "stage_captions": card.get("stage_captions"),
        "mobile_toolbar": card.get("mobile_toolbar", False),
        # Variant B's description: read by the pinned-element heuristic, never drawn.
        "change_text": variant_description(scenario, "B"),
        # Read by the mechanical gates (mockup_report), never drawn.
        "numeric_change": scenario.get("numeric_change"),
        "warnings": scenario.get("warnings") if isinstance(scenario.get("warnings"), list) else [],
        "kpi_names": [k.get("name") for k in (scenario.get("primary_kpi"), scenario.get("guardrail"))
                      if isinstance(k, dict) and isinstance(k.get("name"), str) and k.get("name").strip()],
        # Never drawn as text: a count > 0 adds the conditional ribbon and meta (conditional_html).
        "critical_assumptions": len(critical_assumptions(scenario)),
    }


def variant_description(scenario, vid):
    """The description of variant `vid` in the record's `variants`, or None."""
    for v in scenario.get("variants") or ():
        if isinstance(v, dict) and v.get("id") == vid and isinstance(v.get("description"), str):
            return v["description"]
    return None


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
            '          <span class="browser-url"><span class="lock"></span>{{URL}}</span>\n'
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


def apply_frame(text, device, bottom_nav=False):
    """The template's phone skeleton turned into the card's device frame.

    The frame helpers leave their user text as placeholders ({{URL}},
    {{DOMAIN}}, {{BOTTOM_NAV}}) for build()'s single substitution pass; the
    drift check (fixed_lines) applies the same transformation, so the frame's
    skeleton is checked line by line like the rest of the template.
    """
    if device == "web":
        return to_browser_skeleton(text)
    if device == "phone-web":
        return apply_mobile_address_bar(text)
    return apply_bottom_nav(text, bottom_nav)


# ------------------------------------------------------------- layout (S1, S2)
#
# What the screens' layout markers and the layout fields ask of the frame,
# applied to the frame skeleton BEFORE the single substitution pass (like
# apply_frame), so fixed_lines() can apply the same transformation and the drift
# check still covers every fixed line. A card without markers or fields gets
# its frame unchanged.

PHONE_BLOCK_RE = re.compile(r'(?ms)^([ \t]*)<div class="phone">\n.*?\{\{VARIANT_([AB])_SCREEN\}\}.*?^\1</div>\n')
SCREEN_CLOSE_RE = re.compile(r"(\{\{VARIANT_[AB]_SCREEN\}\}\n([ \t]*)</div>\n)")
TOOLBAR_HTML = ('<div class="m-toolbar"><div class="mt-row"><span class="mt-back"></span><span class="mt-fwd"></span>'
                '<span class="mt-share"></span><span class="mt-tabs"></span></div><div class="m-home"><span></span></div></div>')
STAGE_PLACEHOLDERS = ("SCREEN", "STAGE_TWO")
STAGE_CAPTIONS = ("{{STAGE_CAP_ONE}}", "{{STAGE_CAP_TWO}}")


def layout_of(view):
    """The layout a built card draws: {"fold", "sticky", "stages", "toolbar"}
    (stages: 1 = one screen). Read from the screens' markers and the fields."""
    fold = sticky = breaks = 0
    for key in ("variant_a", "variant_b"):
        f, b, st = layout_markers(view.get(key) or "")
        fold, breaks, sticky = max(fold, f), max(breaks, b), max(sticky, st)
    return {"fold": bool(fold), "sticky": bool(sticky), "stages": breaks + 1,
            "toolbar": view.get("device") == "phone-web" and view.get("mobile_toolbar") is True}


def apply_layout(text, layout=None):
    """The frame skeleton with the layout's pieces: the browser toolbar inside
    each phone, the pinned bar's padding on each screen, the continuation sheet
    after each phone ({{VARIANT_X_BELOW}}), or each phone repeated per stage
    ({{VARIANT_X_STAGE_TWO}}, captions {{STAGE_CAP_...}}). No layout: unchanged."""
    if not layout or not (layout.get("fold") or layout.get("sticky") or layout.get("toolbar")
                          or layout.get("stages", 1) > 1):
        return text

    def block(m):
        indent, arm, body = m.group(1), m.group(2), m.group(0)
        if layout.get("toolbar"):
            body = SCREEN_CLOSE_RE.sub(lambda s: "%s%s%s\n" % (s.group(1), s.group(2), TOOLBAR_HTML), body, count=1)
        if layout.get("sticky"):
            body = body.replace('<div class="screen">', '<div class="screen has-sticky">', 1)
        if layout.get("fold"):
            body += "%s{{VARIANT_%s_BELOW}}\n" % (indent, arm)
        stages = layout.get("stages", 1)
        if stages > 1:
            cols = []
            for k in range(stages):
                phone = body.replace("{{VARIANT_%s_SCREEN}}" % arm, "{{VARIANT_%s_%s}}" % (arm, STAGE_PLACEHOLDERS[k]))
                cols.append('%s<div class="stage-col"><div class="stage-cap">%s</div>\n%s%s</div>\n'
                            % (indent, STAGE_CAPTIONS[k], phone, indent))
            arrow = '%s<span class="stage-arrow" aria-hidden="true">→</span>\n' % indent
            body = '%s<div class="stages">\n%s%s</div>\n' % (indent, arrow.join(cols), indent)
        return body

    out, n = PHONE_BLOCK_RE.subn(block, text)
    if n != 2:
        die("template does not expose two .phone blocks for the card's layout (found %d)" % n)
    return out


def layout_values(view, layout):
    """The placeholders apply_layout() leaves, and the two screens split at
    their markers: {placeholder: value}. The markup halves go in raw (the
    allowlist already passed the whole screen); captions are escaped."""
    values = {}
    for arm, key in (("A", "variant_a"), ("B", "variant_b")):
        markup = view[key]
        if layout.get("fold"):
            first, rest = markup.split(FOLD_TAG, 1)
            values["{{VARIANT_%s_SCREEN}}" % arm] = first
            values["{{VARIANT_%s_BELOW}}" % arm] = (
                '<div class="below"><div class="below-cap">%s</div><div class="below-screen">%s</div></div>'
                % (escape(BELOW_CAPTION.get(view["lang"], BELOW_CAPTION["en"])), rest))
        elif layout.get("stages", 1) > 1:
            parts = markup.split(BREAK_TAG)
            for k, part in enumerate(parts):
                values["{{VARIANT_%s_%s}}" % (arm, STAGE_PLACEHOLDERS[k])] = part
    if layout.get("stages", 1) > 1:
        for k, caption in enumerate(view.get("stage_captions") or []):
            values[STAGE_CAPTIONS[k]] = escape(caption)
    return values


def frame_values(view):
    """The escaped values of the placeholders apply_frame() leaves."""
    device = view["device"]
    if device == "web":
        return {"{{URL}}": escape(view["url"])}
    if device == "phone-web":
        return {"{{DOMAIN}}": escape(domain_of(view["url"]))}
    labels = bottom_nav_labels(view["bottom_nav"])
    if not labels:
        return {}
    return {"{{BOTTOM_NAV}}": bottom_nav_html(labels, view["bottom_nav_active"])}


def has_bottom_nav(view):
    """A tab bar is drawn: a native phone frame whose record names its tabs."""
    return view["device"] == "phone" and bool(bottom_nav_labels(view["bottom_nav"]))


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


# The soft ring and the layout markers (CONTRACT 7, S1-S3). A layout marker is
# a bare <div> at the top level of a screen; the builder splits the screen's
# markup at its exact spelling, so the marker itself is never drawn.
SOFT_CLASS = "hl-soft"
RING_CLASSES = ("hl", SOFT_CLASS)
MAX_SOFT = 2
FOLD_CLASS, STICKY_CLASS, BREAK_CLASS = "r-fold", "r-sticky", "r-stage-break"
FOLD_TAG = '<div class="r-fold"></div>'
BREAK_TAG = '<div class="r-stage-break"></div>'
MARKER_TAGS = {FOLD_CLASS: FOLD_TAG, BREAK_CLASS: BREAK_TAG}
# Two stages fit a 728px column side by side at the stage phones' zoom with text
# of at least 12px; a third would not.
MAX_STAGES = 2
LAYOUT_DEVICES = ("phone", "phone-web")
BELOW_CAPTION = {"tr": "Kaydırınca görünen kısım", "en": "Below the first screen"}
# A move whose B side is described as pinned must draw the pinned bar
# (.r-sticky), not an element in the page flow. Turkish stems match as word
# starts (sabitlenmiş, yapışkan bar), the English words as whole words.
PINNED_STEMS = ("sabit", "sabitlen", "yapışkan")
PINNED_WORDS = ("sticky", "pinned", "fixed")


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

    @property
    def is_soft(self):
        """A soft ring (.hl-soft): a linked consequence of the variable, not the variable."""
        return SOFT_CLASS in self.classes

    def key(self, ring_blind=False):
        """Structural identity. ring_blind drops the ring's own class and label
        so a ringed element compares equal to its un-ringed twin."""
        attrs = dict(self.attrs)
        if ring_blind:
            attrs.pop("data-note", None)
            attrs.pop("data-pos", None)
            attrs["class"] = " ".join(c for c in self.classes if c not in RING_CLASSES)
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
    "move": ("difference 'move': ring the element in both variants (found {a} in A, {b} in B)",
             "fark 'taşı': öğeye iki varyantta da halka çizin (A'da {a}, B'de {b} var)"),
    "change": ("difference 'change': ring the changed element in Variant B (found no .hl in B)",
               "fark 'değiştir': B'deki değişen öğeye halka çizin (B'de .hl yok)"),
}


def _ring_placement(difference, a, b, lang):
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
    elif difference == "move":
        if a < 1 or b < 1:
            keys.append("move")
    elif difference == "change":
        if b < 1:
            keys.append("change")
    idx = 1 if lang == "tr" else 0
    return [RING_MSG[k][idx].format(a=a, b=b) for k in keys]


def ring_problems(difference, variant_a, variant_b, lang="en"):
    """Where the ring must sit for each kind of difference (mockup-style.md).

    add    → the new element exists only in B, so only B can carry a ring
    remove → the element exists only in A, ringed and labelled there; B is
             genuinely empty in its place
    move   → the same element in two places: ringed in both
    change → ringed in B (ringing the old state in A too is allowed)

    Returns a list of problems (English by default, Turkish with lang="tr");
    empty means the placement is valid. card_problems() below runs this plus
    everything else that can be read off the two mockups.
    """
    if not difference:
        return []
    return _ring_placement(difference, hl_count(variant_a), hl_count(variant_b), lang)


CARD_MSG = {
    "ring_label": ("ring in {v} has no data-note label (two to four words saying what changed)",
                   "{v} varyantındaki halkanın data-note etiketi yok (neyin değiştiğini söyleyen iki ila dört kelime)"),
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
    "label_long": ("ring label in {v} is {n} words (“{note}”); keep it to two to four",
                   "{v} varyantındaki halka etiketi {n} kelime (“{note}”); iki ila dört kelimede tutun"),
    "label_case": ("ring label in {v} starts with a lowercase letter (“{note}”); a Turkish label starts with a "
                   "capital letter",
                   "{v} varyantındaki halka etiketi küçük harfle başlıyor (“{note}”); Türkçe etiket büyük harfle "
                   "başlar"),
    "multi_ring": ("{n} rings in {v}: one change applied to {n} elements gets one ring around the group; "
                   "{n} rings read as {n} variables",
                   "{v} varyantında {n} halka var: {n} öğeye uygulanan tek değişiklik grubun etrafında tek halka alır; "
                   "{n} halka {n} değişken gibi okunur"),
    "move_content": ("difference 'move': the ringed element's content differs between A and B ({what}); only its "
                     "position may change, a changed copy, size or style is a second variable",
                     "fark 'taşı': halkalı öğenin içeriği A ile B arasında farklı ({what}); yalnızca yeri "
                     "değişebilir, değişen metin, boyut ya da biçim ikinci bir değişkendir"),
    "outside": ("A and B differ outside any ring ({where}: {na} node(s) in A, {nb} in B), e.g. {what}; a second "
                "variable is refused, and a linked consequence of the variable belongs inside the ring (one ring "
                "around the group, its label naming the consequence)",
                "A ile B halkanın dışında da farklı ({where}: A'da {na}, B'de {nb} düğüm), ör. {what}; ikinci bir "
                "değişken reddedilir, değişkenin bağlı bir sonucu halkanın içine alınır (grubun etrafında tek halka, "
                "etiketi sonucu adlandırır)"),
    "colour_b": ("inline colour only in Variant B, inside the ring: {vals}; a colour that exists only in B is a "
                 "second variable unless colour is what the test changes (the manifest lists it for the reviewer)",
                 "yalnızca B varyantında, halkanın içinde geçen satır içi renk: {vals}; yalnızca B'de olan renk, "
                 "test rengi değiştirmiyorsa ikinci bir değişkendir (manifest gözden geçiren için listeler)"),
    "colour_b_outside": ("inline colour only in Variant B on an element outside the ring: {vals}; a colour change "
                         "outside the ring is a second variable, whatever the test changes",
                         "yalnızca B varyantında, halkanın dışındaki bir öğede geçen satır içi renk: {vals}; "
                         "halkanın dışındaki renk değişikliği, test neyi değiştirirse değiştirsin ikinci bir "
                         "değişkendir"),
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
    tag = ("<%s %s>" % (k.tag, " ".join('%s="%s"' % kv for kv in sorted(k.attrs.items()))))[:110]
    text = _node_text(k)
    return "%s “%s”" % (tag, text[:50]) if text else tag


# ------------------------------------------------------- the A/B diff
#
# The two mockups are aligned level by level. Un-ringed nodes are aligned
# first and become anchors; what lies between two anchors is a "span" on each
# side. A span may differ only where a ring explains it:
#
#   * rings only (on either side or both): an element added, removed or moved
#   * loose nodes on one side against ring(s) on the other, and no ring on the
#     loose side: the element's old state in A against its ringed state in B
#     (or the other way round)
#   * one un-ringed node against one un-ringed node with the same tag and
#     attributes: the difference is deeper, the walk goes into it
#
# Anything else is a difference outside the rings and refuses the card. A ring
# region that passes becomes material for the manifest (what changed inside it).
#
# One structural wrapper counts as part of its ring: an added (or removed)
# modal is drawn as <div class="r-overlay"><div class="r-modal hl" …>…</div>
# </div> (mockup-style.md: the ring goes around .r-modal, the dimming is its
# linked consequence). An .r-overlay whose only content is that one ring is
# treated as ringed; an overlay with anything else in it (text, a second
# element, a ring that isn't the modal) stays an ordinary node, so nothing else
# that differs outside the rings gets through.
# The pinned bar is the second one: <div class="r-sticky"> whose only child is
# one ring stands for that ring, so a bar that exists only in B around the
# moved element is the move itself, not a difference outside the ring. A bar
# with anything else in it stays an ordinary node.
# A soft ring (.hl-soft) covers what differs inside it like a ring does (the
# variable's linked consequence, listed as "linked" in the manifest), but it
# never counts for the ring placement rules and never stands for the variable.
# Aligning the loose nodes first matters for 'move': a ringed element that
# trades places with its neighbour must not steal the neighbour's match.

def _overlay_ring(node):
    """The ring an .r-overlay only wraps, else None.

    The overlay qualifies when it isn't a ring itself and its whole content is
    one ring around .r-modal: the modal ringed itself (class "r-modal hl") or a
    bare ring wrapper whose only content is the modal."""
    if not isinstance(node, Node) or node.is_ring or "r-overlay" not in node.classes or len(node.kids) != 1:
        return None
    ring = node.kids[0]
    if not isinstance(ring, Node) or not ring.is_ring:
        return None
    if "r-modal" in ring.classes:
        return ring
    if (ring.classes == ["hl"] and len(ring.kids) == 1 and isinstance(ring.kids[0], Node)
            and "r-modal" in ring.kids[0].classes):
        return ring
    return None


def _sticky_ring(node):
    """The ring an .r-sticky bar only wraps, else None: the bar isn't a ring
    itself, carries nothing but class="r-sticky", and its whole content is one
    ring (.hl)."""
    if (not isinstance(node, Node) or node.is_ring or node.tag != "div"
            or node.attrs != {"class": STICKY_CLASS}):
        return None
    kids = _solid_kids(node)
    if len(kids) == 1 and isinstance(kids[0], Node) and kids[0].is_ring:
        return kids[0]
    return None


def _ring_node(k):
    """The ring node that stands for k: k itself, or the ring an overlay or a
    pinned bar wraps."""
    if isinstance(k, Node) and k.is_ring:
        return k
    return _overlay_ring(k) or _sticky_ring(k)


def _mark_node(k):
    """The ring or soft ring that stands for k, else None."""
    ring = _ring_node(k)
    if ring is None and isinstance(k, Node) and k.is_soft:
        return k
    return ring


def _ringed(k):
    return _mark_node(k) is not None


def _soft_only(nodes):
    """Every marked node in `nodes` is a soft ring (and there is one)."""
    marks = [_mark_node(n) for n in nodes]
    marks = [m for m in marks if m is not None]
    return bool(marks) and all(m.is_soft and not m.is_ring for m in marks)


def _rkey(k):
    return k.key(True) if isinstance(k, Node) else k


def _same_shell(x, y):
    return isinstance(x, Node) and isinstance(y, Node) and x.tag == y.tag and x.attrs == y.attrs


def _span(sa, sb, path, start, regions, outside):
    if not sa and not sb:
        return
    if all(_ringed(k) for k in sa + sb):
        regions.append((list(sa), list(sb)))
        return
    sm = difflib.SequenceMatcher(None, [_rkey(k) for k in sa], [_rkey(k) for k in sb], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        ma, mb = sa[i1:i2], sb[j1:j2]
        if op == "equal":
            if any(_ringed(k) for k in ma + mb):
                regions.append((list(ma), list(mb)))  # a ring around content that is the same in A and B
            continue
        rings_a = [k for k in ma if _ringed(k)]
        rings_b = [k for k in mb if _ringed(k)]
        loose_a = [k for k in ma if not _ringed(k)]
        loose_b = [k for k in mb if not _ringed(k)]
        if len(loose_a) == 1 and len(loose_b) == 1 and _same_shell(loose_a[0], loose_b[0]):
            _compare(loose_a[0], loose_b[0], "%s > %s[%d]" % (path, loose_a[0].tag, start + i1), regions, outside)
            if rings_a or rings_b:
                regions.append((rings_a, rings_b))
            continue
        covered_a = not loose_a or (rings_b and not loose_b and not rings_a)
        covered_b = not loose_b or (rings_a and not loose_a and not rings_b)
        if covered_a and covered_b:
            regions.append((list(ma), list(mb)))
            continue
        if _has_soft(ma + mb) and _soft_span(loose_a, loose_b, rings_a, rings_b, path, start + i1, regions, outside):
            continue
        loose = [k for k in (loose_b if not covered_b else []) + (loose_a if not covered_a else [])]
        outside.append(("%s, child %d" % (path, start + i1), len(ma), len(mb), _describe(loose[0])))


def _has_soft(nodes):
    """A soft ring among `nodes` or anywhere inside them."""
    return any(isinstance(k, Node) and (k.is_soft or any(n.is_soft for n in _walk(k))) for k in nodes)


def _shell(k):
    return (k.tag, tuple(sorted(k.attrs.items()))) if isinstance(k, Node) else ("#text", k)


def _soft_span(loose_a, loose_b, rings_a, rings_b, path, start, regions, outside):
    """A stretch the plain rules refuse, when a soft ring is in it: the variable
    (a ring) next to an element whose linked consequence sits deeper (a soft
    ring inside a card both arms draw). Un-ringed nodes with the same shell on
    both sides are paired and compared inside (strictly, as everywhere); what
    is left must be covered by the rings exactly as above. Only cards that use
    .hl-soft reach this; every other card's diff is unchanged. True when the
    stretch is explained (its regions and inner differences recorded)."""
    sm = difflib.SequenceMatcher(None, [_shell(k) for k in loose_a], [_shell(k) for k in loose_b], autojunk=False)
    pairs = []
    for i, j, n in sm.get_matching_blocks():
        pairs.extend((loose_a[i + t], loose_b[j + t]) for t in range(n))
    if not pairs:
        return False
    paired = {id(x) for pair in pairs for x in pair}
    rest_a = [k for k in loose_a if id(k) not in paired]
    rest_b = [k for k in loose_b if id(k) not in paired]
    covered_a = not rest_a or (rings_b and not rest_b and not rings_a)
    covered_b = not rest_b or (rings_a and not rest_a and not rings_b)
    if not (covered_a and covered_b):
        return False
    for x, y in pairs:
        _compare(x, y, "%s > %s[%d]" % (path, x.tag, start), regions, outside)
    if rest_a or rest_b or rings_a or rings_b:
        regions.append((rest_a + rings_a, rest_b + rings_b))
    return True


def _compare(a, b, path="screen", regions=None, outside=None):
    """Align two parsed mockups (or two nodes with the same shell).

    Returns (regions, outside): `regions` are the ring regions as (A nodes,
    B nodes), the material of the manifest; `outside` the differences no ring
    explains, as (where, nodes in A, nodes in B, example).
    """
    regions = [] if regions is None else regions
    outside = [] if outside is None else outside
    ka, kb = a.kids, b.kids
    la = [i for i, k in enumerate(ka) if not _ringed(k)]
    lb = [j for j, k in enumerate(kb) if not _ringed(k)]
    sm = difflib.SequenceMatcher(None, [_rkey(ka[i]) for i in la], [_rkey(kb[j]) for j in lb], autojunk=False)
    anchors = []
    for i, j, n in sm.get_matching_blocks():
        anchors.extend((la[i + t], lb[j + t]) for t in range(n))
    anchors.append((len(ka), len(kb)))
    pa = pb = -1
    for ai, bj in anchors:
        _span(ka[pa + 1:ai], kb[pb + 1:bj], path, pa + 1, regions, outside)
        pa, pb = ai, bj
    return regions, outside


def _outside_ring_diff(a, b, path="screen"):
    """Differences between two parsed mockups that no ring covers."""
    return _compare(a, b, path)[1]


def _is_wrapper_ring(node):
    """A ring that only wraps (class "hl" and nothing else of its own)."""
    return isinstance(node, Node) and node.is_ring and node.classes == ["hl"]


def _solid_kids(node):
    return [k for k in node.kids if not (isinstance(k, str) and not k.strip())]


def _ring_content_key(node):
    """What a moved element is, wrapper or not: its ring-blind content. A
    pinned bar around the ring (.r-sticky) is looked through: the bar is the
    pinned state's own drawing, the element inside it is what moved."""
    node = _sticky_ring(node) or node
    if _is_wrapper_ring(node):
        return tuple(_rkey(k) for k in node.kids)
    return (_rkey(node),)


def _in_ring(node):
    while node is not None:
        if isinstance(node, Node) and (node.is_ring or node.is_soft):
            return True
        node = node.parent
    return False


# ------------------------------------------------- layout markers and soft rings

LAYOUT_MSG = {
    "marker_bare": ("{v}: write the {what} exactly as {tag} (a bare marker: no other class, attribute, spacing or "
                    "content)",
                    "{v}: {what} tam olarak {tag} biçiminde yazılır (yalın işaret: başka sınıf, nitelik, boşluk ya da "
                    "içerik yok)"),
    "marker_top": ("{v}: .{cls} must be a direct child of the screen, not inside another element or a ring",
                   "{v}: .{cls} doğrudan ekranın çocuğu olmalı, başka bir öğenin ya da halkanın içinde değil"),
    "marker_many": ("{v}: {n} .{cls} in one screen; at most {most}",
                    "{v}: bir ekranda {n} .{cls} var; en fazla {most}"),
    "fold_one_arm": ("only Variant {has} has a .r-fold: the fold is drawn in both arms or in neither (both show a first "
                     "view and its continuation, split at the same place)",
                     "yalnızca {has} varyantında .r-fold var: kıvrım iki kolda da çizilir ya da hiçbirinde (ikisi de "
                     "ilk ekranı ve devamını aynı yerden bölünmüş gösterir)"),
    "fold_empty": ("{v}: nothing {side} the .r-fold; the first view and the continuation both show content",
                   "{v}: .r-fold {side_tr} hiçbir şey yok; ilk ekran da devamı da içerik gösterir"),
    "breaks": ("Variant A has {a} .r-stage-break, Variant B {b}: both arms show the same number of stages",
               "A varyantında {a}, B varyantında {b} .r-stage-break var: iki kol da aynı sayıda aşama gösterir"),
    "stage_empty": ("{v}: stage {n} is empty; every stage shows its screen",
                    "{v}: {n}. aşama boş; her aşama kendi ekranını gösterir"),
    "fold_stages": ("{v}: .r-fold and .r-stage-break don't mix: a screen either continues below its first view or is "
                    "split into stages",
                    "{v}: .r-fold ile .r-stage-break birlikte kullanılmaz: ekran ya ilk görünümün altında devam eder "
                    "ya da aşamalara bölünür"),
    "sticky_attrs": ("{v}: .r-sticky takes class=\"r-sticky\" only (no other class, style or attribute; the ring goes "
                     "on the element inside)",
                     "{v}: .r-sticky yalnızca class=\"r-sticky\" taşır (başka sınıf, style ya da nitelik yok; halka "
                     "içteki öğeye çizilir)"),
    "sticky_content": ("{v}: .r-sticky holds exactly one element (the pinned element, ringed when it is the variable) "
                       "and no loose text",
                       "{v}: .r-sticky tam olarak bir öğe taşır (sabit öğe; değişken oysa halkalı), çıplak metin "
                       "taşımaz"),
    "sticky_fold": ("{v}: .r-sticky is the bar at the bottom of the first view: the screen needs a .r-fold and the "
                    "bar comes before it",
                    "{v}: .r-sticky ilk ekranın altındaki bardır: ekranda bir .r-fold olmalı ve bar ondan önce gelir"),
    "pinned": ("difference 'move': {where} says the element is pinned (“{word}”) but Variant B has no .r-sticky: a "
               "pinned element is drawn as a bar at the bottom of the first view (.r-sticky with .r-fold), not inside "
               "the page flow",
               "fark 'taşı': {where_tr} öğenin sabit olduğunu söylüyor (“{word}”) ama B varyantında .r-sticky yok: "
               "sabit öğe sayfa akışının içinde değil, ilk ekranın altında bir bar olarak çizilir (.r-sticky ve "
               ".r-fold)"),
    "soft_alone": (".hl-soft marks a linked consequence of the variable: the card also needs a .hl around the "
                   "variable itself",
                   ".hl-soft değişkenin bağlı bir sonucunu işaretler: kartta değişkenin kendisinin etrafında da bir "
                   ".hl olmalı"),
    "soft_many": ("{v}: {n} .hl-soft rings; at most {most} per arm (more read as more variables)",
                  "{v}: {n} .hl-soft halka var; kol başına en fazla {most} (fazlası fazla değişken gibi okunur)"),
    "soft_nested": ("{v}: a .hl-soft sits next to the ring, never inside or around a ring (.hl or .hl-soft)",
                    "{v}: .hl-soft halkanın yanında durur, hiçbir halkanın (.hl ya da .hl-soft) içinde ya da "
                    "etrafında değil"),
    "soft_both": ("{v}: an element is either the variable (.hl) or a linked consequence (.hl-soft), not both",
                  "{v}: bir öğe ya değişkendir (.hl) ya bağlı sonuçtur (.hl-soft), ikisi birden değil"),
    "soft_box": ("soft ring in {v} carries inline {prop}: a ring must not push content; give the spacing to the "
                 "children",
                 "{v} varyantındaki yumuşak halka satır içi {prop} taşıyor: halka içeriği itmemeli; boşluğu çocuk "
                 "öğelere verin"),
    "soft_case": ("soft ring label in {v} starts with a lowercase letter (“{note}”); a Turkish label starts with a "
                  "capital letter",
                  "{v} varyantındaki yumuşak halka etiketi küçük harfle başlıyor (“{note}”); Türkçe etiket büyük "
                  "harfle başlar"),
    "device": ("{what} draws a phone screen: only valid with device phone or phone-web, not '{device}'",
               "{what} telefon ekranı çizer: yalnızca device phone ya da phone-web ile kullanılır, '{device}' ile "
               "değil"),
    "captions_missing": ("the screens have {n} stages: card.stage_captions needs {n} short captions, one per stage, "
                         "the same in both arms",
                         "ekranlarda {n} aşama var: card.stage_captions her aşama için bir tane olmak üzere {n} kısa "
                         "başlık ister, iki kolda aynı"),
    "captions_count": ("card.stage_captions has {got} caption(s) for {n} stage(s); give one per stage",
                       "card.stage_captions {n} aşama için {got} başlık taşıyor; her aşamaya bir başlık yazın"),
    "captions_unused": ("card.stage_captions is given but the screens have no .r-stage-break",
                        "card.stage_captions verilmiş ama ekranlarda .r-stage-break yok"),
    "captions_item": ("card.stage_captions: every caption is a short non-empty text, got {got!r}",
                      "card.stage_captions: her başlık kısa ve boş olmayan bir metindir, gelen {got!r}"),
    "captions_case": ("card.stage_captions: “{text}” starts with a lowercase letter; a Turkish caption starts with a "
                      "capital letter",
                      "card.stage_captions: “{text}” küçük harfle başlıyor; Türkçe başlık büyük harfle başlar"),
    "toolbar": ("card.mobile_toolbar draws a mobile browser's bottom toolbar: only valid with device 'phone-web', "
                "not '{device}'",
                "card.mobile_toolbar mobil tarayıcının alt araç çubuğunu çizer: yalnızca device 'phone-web' ile "
                "kullanılır, '{device}' ile değil"),
    "toolbar_type": ("card.mobile_toolbar must be true or false, got {got!r}",
                     "card.mobile_toolbar true ya da false olmalı, gelen {got!r}"),
}
WHAT_NAMES = {
    FOLD_CLASS: ("fold", "kıvrım"),
    BREAK_CLASS: ("stage break", "aşama ayracı"),
}


def _lm(key, lang, **kw):
    en, tr = LAYOUT_MSG[key]
    return (tr if lang == "tr" else en).format(**kw)


def _top_level(root, cls):
    """Every node with class `cls` under root, split into (top-level, nested)."""
    top, nested = [], []
    for node in _walk(root):
        if cls in node.classes:
            (top if node.parent is root else nested).append(node)
    return top, nested


def _split_kids(root, cls):
    """The root's children as runs between its top-level `cls` markers."""
    runs = [[]]
    for k in root.kids:
        if isinstance(k, Node) and cls in k.classes and k.parent is root:
            runs.append([])
        else:
            runs[-1].append(k)
    return runs


def layout_markers(markup):
    """What a screen's markup asks of the layout: (folds, stage breaks, pinned
    bars), counted on the parsed tree (0s when the markup doesn't parse)."""
    root, _ = parse_markup(markup)
    if root is None:
        return 0, 0, 0
    return tuple(sum(1 for n in _walk(root) if cls in n.classes) for cls in (FOLD_CLASS, BREAK_CLASS, STICKY_CLASS))


def layout_problems(trees, raws, lang="en", card_lang=None, layout=None):
    """The rules of .r-fold, .r-stage-break and .r-sticky (and, with `layout`,
    the card fields that go with them). Returns (errors, warnings)."""
    errors, warnings = [], []
    counts = {}
    for (field, name), raw in zip((("variant_a", "A"), ("variant_b", "B")), raws):
        root = trees[field]
        c = counts[name] = {}
        for cls, most in ((FOLD_CLASS, 1), (BREAK_CLASS, MAX_STAGES - 1)):
            top, nested = _top_level(root, cls)
            c[cls] = len(top) + len(nested)
            if nested:
                errors.append(_lm("marker_top", lang, v=name, cls=cls))
            what = WHAT_NAMES[cls][1 if lang == "tr" else 0]
            bare = all(n.tag == "div" and n.attrs == {"class": cls} and not n.kids for n in top + nested)
            if not bare or str(raw).count(MARKER_TAGS[cls]) != c[cls]:
                errors.append(_lm("marker_bare", lang, v=name, what=what, tag=MARKER_TAGS[cls]))
            if c[cls] > most:
                errors.append(_lm("marker_many", lang, v=name, n=c[cls], cls=cls, most=most))
        if c[FOLD_CLASS] and c[BREAK_CLASS]:
            errors.append(_lm("fold_stages", lang, v=name))
        if c[FOLD_CLASS] == 1 and not _top_level(root, FOLD_CLASS)[1]:
            first, rest = _split_kids(root, FOLD_CLASS)
            for side, side_tr, run in (("before", "öncesinde", first), ("after", "sonrasında", rest)):
                if not [k for k in run if not (isinstance(k, Node) and STICKY_CLASS in k.classes)]:
                    errors.append(_lm("fold_empty", lang, v=name, side=side, side_tr=side_tr))
        if c[BREAK_CLASS] and not _top_level(root, BREAK_CLASS)[1]:
            for n, run in enumerate(_split_kids(root, BREAK_CLASS), 1):
                if not run:
                    errors.append(_lm("stage_empty", lang, v=name, n=n))
        # The pinned bar: top level, before the screen's fold, one element in it, nothing of its own.
        top, nested = _top_level(root, STICKY_CLASS)
        c[STICKY_CLASS] = len(top) + len(nested)
        if nested:
            errors.append(_lm("marker_top", lang, v=name, cls=STICKY_CLASS))
        if c[STICKY_CLASS] > 1:
            errors.append(_lm("marker_many", lang, v=name, n=c[STICKY_CLASS], cls=STICKY_CLASS, most=1))
        for bar in top + nested:
            if bar.tag != "div" or bar.attrs != {"class": STICKY_CLASS}:
                errors.append(_lm("sticky_attrs", lang, v=name))
            kids = _solid_kids(bar)
            if len(kids) != 1 or not isinstance(kids[0], Node):
                errors.append(_lm("sticky_content", lang, v=name))
        if top:
            kids = [k for k in root.kids if isinstance(k, Node)]
            folds = [i for i, k in enumerate(kids) if FOLD_CLASS in k.classes]
            if not folds or any(kids.index(bar) > folds[0] for bar in top):
                errors.append(_lm("sticky_fold", lang, v=name))
    if bool(counts["A"][FOLD_CLASS]) != bool(counts["B"][FOLD_CLASS]):
        errors.append(_lm("fold_one_arm", lang, has="A" if counts["A"][FOLD_CLASS] else "B"))
    breaks_a, breaks_b = counts["A"][BREAK_CLASS], counts["B"][BREAK_CLASS]
    if breaks_a != breaks_b:
        errors.append(_lm("breaks", lang, a=breaks_a, b=breaks_b))
    if layout is not None:
        errors += layout_field_problems(layout, max(breaks_a, breaks_b),
                                        any(counts[v][c] for v in "AB" for c in (FOLD_CLASS, STICKY_CLASS)),
                                        lang, card_lang)
    return errors, warnings


def layout_field_problems(layout, breaks, folded, lang="en", card_lang=None):
    """card.stage_captions and card.mobile_toolbar against the screens and the
    device. `breaks` is the number of stage breaks per screen, `folded` whether
    a screen has a fold or a pinned bar."""
    out = []
    device = layout.get("device")
    if device not in LAYOUT_DEVICES:
        if folded:
            out.append(_lm("device", lang, what=".r-fold / .r-sticky", device=device))
        if breaks:
            out.append(_lm("device", lang, what=".r-stage-break", device=device))
    toolbar = layout.get("mobile_toolbar", False)
    if toolbar is not None and not isinstance(toolbar, bool):
        out.append(_lm("toolbar_type", lang, got=toolbar))
    elif toolbar and device != "phone-web":
        out.append(_lm("toolbar", lang, device=device))
    captions = layout.get("stage_captions")
    if captions in (None, []):
        if breaks:
            out.append(_lm("captions_missing", lang, n=breaks + 1))
        return out
    if not isinstance(captions, list):
        out.append(_lm("captions_item", lang, got=captions))
        return out
    if not breaks:
        out.append(_lm("captions_unused", lang))
        return out
    if len(captions) != breaks + 1:
        out.append(_lm("captions_count", lang, got=len(captions), n=breaks + 1))
    for text in captions:
        if not isinstance(text, str) or not text.strip():
            out.append(_lm("captions_item", lang, got=text))
        elif card_lang == "tr" and text.strip()[:1].islower():
            out.append(_lm("captions_case", lang, text=text))
    return out


def soft_problems(trees, ring_lists, lang="en", card_lang=None):
    """The soft ring's rules: next to a .hl in the card, at most MAX_SOFT per
    arm, never nested with a ring, no margin or padding of its own."""
    out = []
    any_soft = False
    for field, name in (("variant_a", "A"), ("variant_b", "B")):
        softs = [n for n in _walk(trees[field]) if n.is_soft]
        any_soft = any_soft or bool(softs)
        if len(softs) > MAX_SOFT:
            out.append(_lm("soft_many", lang, v=name, n=len(softs), most=MAX_SOFT))
        for soft in softs:
            if soft.is_ring:
                out.append(_lm("soft_both", lang, v=name))
                continue
            up, nested = soft.parent, False
            while isinstance(up, Node) and up.tag != "#root":
                nested = nested or up.is_ring or up.is_soft
                up = up.parent
            if nested or any(n.is_ring or n.is_soft for n in _walk(soft)):
                out.append(_lm("soft_nested", lang, v=name))
            push = RING_PUSH_RE.search(soft.attrs.get("style") or "")
            if push:
                out.append(_lm("soft_box", lang, v=name, prop=push.group(1).lower()))
            note = (soft.attrs.get("data-note") or "").strip()
            if card_lang == "tr" and note[:1].islower():
                out.append(_lm("soft_case", lang, v=name, note=note))
    if any_soft and not (ring_lists["A"] or ring_lists["B"]):
        out.insert(0, _lm("soft_alone", lang))
    seen, unique = set(), []
    for text in out:
        if text not in seen:
            seen.add(text)
            unique.append(text)
    return unique


def pinned_problems(difference, tree_a, tree_b, rings_b, variable=None, change_text=None, lang="en"):
    """Heuristic (PINNED_RE): a move whose B side is described as pinned is drawn
    with the pinned bar (.r-sticky), never as an element in the page flow. Silent
    when A draws the bar (the move takes a pinned element into the flow)."""
    if difference != "move" or any(STICKY_CLASS in n.classes for t in (tree_a, tree_b) for n in _walk(t)):
        return []
    sources = [("the ring label in B", "B'deki halka etiketi", r.attrs.get("data-note") or "") for r in rings_b]
    sources += [("the variable", "değişken", variable or ""), ("Variant B's description", "B'nin tanımı",
                                                                change_text or "")]
    for where, where_tr, text in sources:
        m = PINNED_RE.search(_fold(text)) if isinstance(text, str) else None
        if m:
            return [_lm("pinned", lang, where=where, where_tr=where_tr, word=m.group(0))]
    return []


def card_problems(difference, variant_a, variant_b, lang="en", variable=None, classes=None, card_lang=None,
                  change_text=None, layout=None):
    """Everything that can be read off the two mockup bodies' markup.

    Returns (errors, warnings). Errors refuse the card: markup outside the
    allowlist, ring placement against the difference type, a ring without a
    label, a ring that carries its own margin or padding, a class that is not a
    template component (only when `classes`, the template's own class names, is
    given), any difference between A and B outside the rings, a colour that
    exists only in B on an element outside the ring, and a 'move' whose
    element changed, the layout markers' rules (layout_problems), the soft
    rings' rules (soft_problems) and a pinned element drawn in the page flow
    (pinned_problems). Warnings are for the reviewer: a long label, several
    rings, a colour only in B inside the ring when colour isn't the variable.

    `change_text` is Variant B's description (the pinned heuristic reads it
    next to `variable` and B's ring labels); `layout` the card's layout
    fields ({"device", "stage_captions", "mobile_toolbar"}), checked only when
    given (the builder gives them).

    Shared with validate_scenario_json.py, so the two never disagree. The
    record-dependent gates (numbers, accessibility, regulation, personal data)
    are mockup_report()'s.
    """
    errors, warnings, trees = [], [], {}
    for field, markup in (("variant_a", variant_a), ("variant_b", variant_b)):
        root, problems = parse_markup(markup, lang)
        errors += ["%s: %s" % (field, p) for p in problems]
        trees[field] = root
    if difference:
        errors += _ring_placement(difference, hl_count(variant_a), hl_count(variant_b), lang)
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
            # card_lang is the card's own language (the record's lang); lang only picks the message language.
            if card_lang == "tr" and note[:1].islower():
                errors.append(_cm("label_case", lang, v=name, note=note))
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

    # A move's labels say where the element sits in each arm ("Kaydırınca görünüyor" / "Ekranın altında sabit"),
    # so they may differ; every ring still needs one (above). Only the element itself must be identical.
    if difference == "move" and ring_lists["A"] and ring_lists["B"]:
        ka = sorted(repr(_ring_content_key(r)) for r in ring_lists["A"])
        kb = sorted(repr(_ring_content_key(r)) for r in ring_lists["B"])
        if ka != kb:
            changed = _region_changes(ring_lists["A"], ring_lists["B"])
            what = "; ".join(_change_text(c) for c in changed[:3]) or "-"
            errors.append(_cm("move_content", lang, what=what))

    lay_errors, lay_warnings = layout_problems(trees, (variant_a, variant_b), lang, card_lang, layout)
    errors += lay_errors
    warnings += lay_warnings
    errors += soft_problems(trees, ring_lists, lang, card_lang)
    errors += pinned_problems(difference, trees["variant_a"], trees["variant_b"], ring_lists["B"], variable,
                              change_text, lang)

    for where, na, nb, what in _outside_ring_diff(trees["variant_a"], trees["variant_b"]):
        errors.append(_cm("outside", lang, where=where, na=na, nb=nb, what=what))

    labels = " ".join((r.attrs.get("data-note") or "") for r in ring_lists["A"] + ring_lists["B"])
    in_a = set(inline_colours(trees["variant_a"]))
    only_b_outside, only_b_inside = [], []
    for node in _walk(trees["variant_b"]):
        for value in COLOUR_VALUE_RE.findall(node.attrs.get("style") or ""):
            v = _norm_colour(value)
            if v in in_a:
                continue
            bucket = only_b_inside if _in_ring(node) else only_b_outside
            if v not in bucket:
                bucket.append(v)

    def listed(vals):
        return ", ".join(vals[:4]) + (" (+%d)" % (len(vals) - 4) if len(vals) > 4 else "")

    if only_b_outside:
        errors.append(_cm("colour_b_outside", lang, vals=listed(only_b_outside)))
    if only_b_inside and not COLOUR_TOPIC_RE.search("%s %s" % (variable or "", labels)):
        warnings.append(_cm("colour_b", lang, vals=listed(only_b_inside)))
    return errors, warnings


# ------------------------------------------------------------- the manifest
#
# Every change inside the rings, as flat items a reviewer can tick off one by
# one. Each item names its ring (the label), the variant whose ring it is, the
# kind of change and the two sides:
#
#   {"ring": "Kupon alanı bağlantıda", "variant": "B", "kind": "text", "change": "changed", "a": "…", "b": "…"}
#   kind  text       a text node (a/b: the strings)
#         number     a numeric token (a/b: the tokens as written)
#         component  an r-* (or ph/img/hero) class (value: the class; a/b: counts)
#         class      a modifier class on a component (element, value; a/b: counts); a class that
#                    moves between siblings is listed on each element it leaves or reaches ("at": its text)
#         attribute  an attribute or inline style (element, attribute; a/b: values)
#   change  added | removed | changed

MANIFEST_FORMAT = "ab-test-playbook/diff-manifest"
MANIFEST_VERSION = 1
RING_OWN_ATTRS = ("class", "data-note", "data-pos")


def _elem_sig(node):
    comps = [c for c in node.classes if c not in RING_CLASSES and (c.startswith(COMPONENT_PREFIX) or c in COMPONENT_WORDS)]
    return node.tag + "".join("." + c for c in comps)


def _facts(nodes):
    """Texts (in order, each with the element it sits in), component counts,
    modifier counts and attributes of nodes."""
    texts, comps, mods, attrs = [], collections.Counter(), collections.Counter(), collections.Counter()

    def visit(k, where="#root"):
        if isinstance(k, str):
            texts.append((where, k))
            return
        sig = _elem_sig(k)
        for c in k.classes:
            if c in RING_CLASSES:
                continue
            if c.startswith(COMPONENT_PREFIX) or c in COMPONENT_WORDS:
                comps[c] += 1
            else:
                mods[(sig, c)] += 1
        wrapper = _is_wrapper_ring(k)
        for name, value in sorted(k.attrs.items()):
            if name in RING_OWN_ATTRS or (wrapper and name == "style"):
                continue
            attrs[(sig, name, value)] += 1
        for kid in k.kids:
            visit(kid, sig)

    for n in nodes:
        visit(n)
    return texts, comps, mods, attrs


def _seq_changes(kind, seq_a, seq_b):
    """(element, value) sequences → changes. Inside a replaced stretch a value
    is paired with the next one in the same kind of element ("Uygula" on a
    button against "Kodu kullan" on a button); the rest are added or removed."""
    out = []
    sm = difflib.SequenceMatcher(None, seq_a, seq_b, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        xa, xb = list(seq_a[i1:i2]), list(seq_b[j1:j2])
        pairs, rest_b = [], list(xb)
        for ea in xa:
            match = next((eb for eb in rest_b if eb[0] == ea[0]), None)
            if match is not None:
                rest_b.remove(match)
            pairs.append((ea, match))
        pairs += [(None, eb) for eb in rest_b]
        for ea, eb in pairs:
            change = "changed" if ea and eb else ("added" if ea is None else "removed")
            out.append({"kind": kind, "change": change, "element": (ea or eb)[0],
                        "a": ea[1] if ea else None, "b": eb[1] if eb else None})
    return out


def _count_changes(kind, ca, cb, element=None):
    out = []
    for key in sorted(set(ca) | set(cb)):
        if ca[key] == cb[key]:
            continue
        item = {"kind": kind, "change": "added" if cb[key] > ca[key] else "removed"}
        if element is not None:
            item["element"], item["value"] = key
        else:
            item["value"] = key
        item["a"], item["b"] = ca[key], cb[key]
        out.append(item)
    return out


def _elements(nodes):
    """Every element under `nodes` in document order: (signature, its modifier
    classes, its text)."""
    out = []

    def visit(k):
        if isinstance(k, Node):
            mods = frozenset(c for c in k.classes if c not in RING_CLASSES
                             and not (c.startswith(COMPONENT_PREFIX) or c in COMPONENT_WORDS))
            out.append((_elem_sig(k), mods, _short(_node_text(k), 40)))
            for kid in k.kids:
                visit(kid)

    for n in nodes:
        visit(n)
    return out


def _moved_class_changes(nodes_a, nodes_b, counted):
    """A modifier class that moves between siblings (.on from one chip, radio or
    tab to another) keeps its count, so _count_changes() can't see it. The
    elements are aligned by signature, position by position; a modifier that
    differs on an aligned pair is listed on that element ("at": its text),
    unless the count already reported it for that element kind (`counted`)."""
    ea, eb = _elements(nodes_a), _elements(nodes_b)
    out = []
    sm = difflib.SequenceMatcher(None, [e[0] for e in ea], [e[0] for e in eb], autojunk=False)
    for i, j, n in sm.get_matching_blocks():
        for t in range(n):
            (sig, mods_a, text_a), (_, mods_b, text_b) = ea[i + t], eb[j + t]
            for cls in sorted(mods_a ^ mods_b):
                if (sig, cls) in counted:
                    continue
                added = cls in mods_b
                out.append({"kind": "class", "change": "added" if added else "removed", "element": sig,
                            "value": cls, "at": text_b if added else text_a, "a": int(not added), "b": int(added)})
    return out


def _region_changes(nodes_a, nodes_b):
    ta, ca, ma, aa = _facts(nodes_a)
    tb, cb, mb, ab = _facts(nodes_b)
    out = _seq_changes("text", ta, tb)
    out += _seq_changes("number", _numbers_in(ta), _numbers_in(tb))
    out += _count_changes("component", ca, cb)
    counted = _count_changes("class", ma, mb, element=True)
    out += counted
    out += _moved_class_changes(nodes_a, nodes_b, {(c["element"], c["value"]) for c in counted})
    only_a, only_b = aa - ab, ab - aa
    groups = collections.OrderedDict()
    for (sig, name, value), n in sorted(only_a.items()):
        groups.setdefault((sig, name), ([], []))[0].extend([value] * n)
    for (sig, name, value), n in sorted(only_b.items()):
        groups.setdefault((sig, name), ([], []))[1].extend([value] * n)
    for (sig, name), (va, vb) in groups.items():
        for k in range(max(len(va), len(vb))):
            a = va[k] if k < len(va) else None
            b = vb[k] if k < len(vb) else None
            change = "changed" if a is not None and b is not None else ("added" if a is None else "removed")
            out.append({"kind": "attribute", "change": change, "element": sig, "attribute": name, "a": a, "b": b})
    return out


def _region_label(nodes_a, nodes_b):
    labels = []
    for node in list(nodes_b) + list(nodes_a):
        if _ringed(node):
            note = (_mark_node(node).attrs.get("data-note") or "").strip()
            if note and note not in labels:
                labels.append(note)
    side_a, side_b = any(_ringed(n) for n in nodes_a), any(_ringed(n) for n in nodes_b)
    variant = "A+B" if side_a and side_b else ("B" if side_b else "A")
    return " / ".join(labels), variant


def ring_regions(regions):
    """Tag each ring region added / removed / changed / moved / linked.

    A region whose only marks are soft rings is "linked" (the variable's
    consequence). A ring region that holds rings on one side only is an added
    (B) or a removed (A) element, unless an A-only and a B-only region hold
    the same content: that pair is one moved element and is merged (a pinned
    bar around the element is looked through, _ring_content_key).
    """
    out, a_only, b_only = [], [], []
    for na, nb in regions:
        if _soft_only(list(na) + list(nb)):
            out.append(("linked", na, nb))
        elif na and not nb and all(_ringed(n) for n in na):
            a_only.append(na)
        elif nb and not na and all(_ringed(n) for n in nb):
            b_only.append(nb)
        else:
            out.append(("changed", na, nb))
    for na in a_only:
        key = sorted(repr(_ring_content_key(n)) for n in na)
        match = next((nb for nb in b_only if sorted(repr(_ring_content_key(n)) for n in nb) == key), None)
        if match is not None:
            b_only.remove(match)
            out.append(("moved", na, match))
        else:
            out.append(("removed", na, []))
    out += [("added", [], nb) for nb in b_only]
    return out


def manifest_entries(regions):
    """Ring regions from _compare() → (rings, changes) for the manifest.

    rings:   [{"ring": n, "label", "variant": "A"|"B"|"A+B",
               "kind": "added"|"removed"|"changed"|"moved"|"linked"|"unchanged", "changes": count}]
    changes: [{"ring": n, "label", "kind", "change", "a", "b", ...}] (see above)
    """
    rings_out, changes = [], []
    for n, (kind, na, nb) in enumerate(ring_regions(regions), 1):
        label, variant = _region_label(na, nb)
        if kind == "moved":  # the pinned bar is the moved element's drawing, not a change of it
            items = _region_changes([_sticky_ring(k) or k for k in na], [_sticky_ring(k) or k for k in nb])
        else:
            items = _region_changes(na, nb)
        if kind == "changed" and not items:
            kind = "unchanged"
        rings_out.append({"ring": n, "label": label, "variant": variant, "kind": kind, "changes": len(items)})
        for item in items:
            entry = {"ring": n, "label": label}
            entry.update(item)
            changes.append(entry)
    return rings_out, changes


def _change_text(item):
    """One manifest item as a short line (messages)."""
    what = " ".join(str(x) for x in (item.get("element"), item.get("attribute") or item.get("value")) if x)
    return "%s %s %s: %r → %r" % (item["kind"], item["change"], what, item.get("a"), item.get("b"))


# --------------------------------------------- numbers, a11y, regulation, PII
#
# These gates read the record as well as the mockups (numeric_change,
# warnings), so they live here and not in card_problems(), which the validator
# shares. Every keyword list below is a HEURISTIC: it catches the common shapes
# of a problem, and what it can't see is the reviewers' to catch. A miss is
# never proof that a mockup is clean.

# A numeric token as a mockup prints it: grouped thousands in either
# convention ("1.299", "1,299.00", "1.299,90"), a plain number with an optional
# decimal part ("890", "4,5", "4.5"), a percentage either side ("%20", "20%").
# Not glued to a word ("A4", "x2" are not counts); the whole run of digits is
# one token ("1.2345" is one number, not "1.234" and "5").
_NUM_CORE = r"\d{1,3}(?:[.,  ]\d{3})+(?:[.,]\d+)?(?!\d)|\d+(?:[.,]\d+)?(?!\d)"
NUMBER_RE = re.compile(r"(?<!\w)(%\s?)?(" + _NUM_CORE + r")(\s?%)?")


def number_tokens(text):
    """The numeric tokens of one text, as written (spacing around % removed)."""
    out = []
    for m in NUMBER_RE.finditer(text or ""):
        out.append(("%" if m.group(1) else "") + m.group(2) + ("%" if m.group(3) else ""))
    return out


def _numbers_of(texts):
    """Numeric tokens of (element, text) pairs, values only."""
    return [value for _, value in _numbers_in(texts)]


def _numbers_in(texts):
    """Numeric tokens of (element, text) pairs, each with its element."""
    out = []
    for where, t in texts:
        out.extend((where, n) for n in number_tokens(t))
    return out


# Interactive components (CONTRACT: r-cta, r-link, r-field, r-check, r-radio,
# r-chip, r-tabs, r-search, r-overlay, r-modal). B adding one, or more of one,
# needs an accessibility warning whose criteria fit that element.
INTERACTIVE_COMPONENTS = ("r-cta", "r-link", "r-field", "r-check", "r-radio", "r-chip", "r-tabs", "r-search",
                          "r-overlay", "r-modal")
DIALOG_COMPONENTS = ("r-overlay", "r-modal")
# The criteria themselves (touch target, contrast, keyboard, screen reader; for
# a dialog also focus and close) are the validator's A11Y_BASE / A11Y_MODAL,
# read through accessibility_criteria(): one definition, so the record check
# and the mockup check can never ask for different things.

# Rule 11: legal or mandatory text. A text node in A that contains one of these
# must reach B unchanged (a regulated display changed → the variant is held).
LEGAL_TERMS = ("KVKK", "aydınlatma", "açık rıza", "gizlilik", "cayma", "faiz", "toplam maliyet", "yıllık maliyet",
               "sözleşme", "ön bilgilendirme", "koşulları", "terms", "privacy", "APR", "right of withdrawal")
# Rule 6: security and verification controls. B showing fewer of these than A
# means a protection was weakened or removed.
AUTH_TERMS = ("doğrula", "SMS kodu", "CAPTCHA", "şifre", "parola", "iki adımlı", "tek kullanımlık", "güvenlik kodu",
              "robot değilim", "verification code", "password", "two-factor", "2FA", "OTP", "CVV", "CVC",
              "3D Secure", "not a robot")
# Rule 6: a consent checkbox (r-check whose text reads as consent or as having
# read a legal notice) that A leaves unticked must not be ticked (.on) in B, and
# one that A shows must not be gone in B. Word starts, like the lists above
# ("onay veriyorum", "kabul ediyorum", "açık rıza", "okudum"/"okuduğumu").
CONSENT_TERMS = ("onay", "rıza", "açık rıza", "kabul", "izin", "izn", "okudu", "aydınlatma", "consent", "agree",
                 "accept", "I have read")
# Whole words: "read" (not "ready"), "ileti" with its suffixes ("ticari
# elektronik iletiler") but not "iletişim" (contact details, no consent).
# A marketing opt-in worded as a wish ("Ürün haberlerini e-postayla almak
# istiyorum", "I want to receive offers") is a consent box too.
CONSENT_WORDS = (r"(?<!\w)read(?!\w)|(?<!\w)ileti(?!ş)|almak\s+isti(?:yorum|yoruz)|gönderilmesini\s+isti"
                 r"|(?<!\w)receive\b|(?<!\w)subscribe")


def _fold(text):
    """Case- and dotted/dotless-i-insensitive form of TR or EN text."""
    return (str(text).replace("İ", "i").replace("I", "i").lower().replace("ı", "i").replace("̇", ""))


def _term_re(terms):
    """One regex for a keyword list, on folded text: an acronym (all capitals)
    matches as a whole word, any other term as a word start (Turkish suffixes:
    "sözleşmesi", "KVKK’nın")."""
    parts = []
    for term in terms:
        folded = re.escape(_fold(term))
        parts.append(r"(?<!\w)%s(?!\w)" % folded if term.isupper() else r"(?<!\w)%s" % folded)
    return re.compile("|".join(parts))


LEGAL_RE = _term_re(LEGAL_TERMS)
PINNED_RE = re.compile("|".join([r"(?<!\w)%s\w*" % re.escape(_fold(t)) for t in PINNED_STEMS]
                                + [r"(?<!\w)%s(?!\w)" % re.escape(t) for t in PINNED_WORDS]))
CONSENT_RE = re.compile(_term_re(CONSENT_TERMS).pattern + "|" + CONSENT_WORDS)

# Rule 15: values shaped like personal data. A mask ("•••", "****") breaks the
# digit runs these need, so it never matches; an all-zero placeholder matches
# and is let through by PII_PLACEHOLDER below.
PII_PATTERNS = (
    ("iban", re.compile(r"(?<![A-Za-z0-9])TR\s?\d{2}(?:\s?\d{4}){5}\s?\d{2}(?!\d)", re.IGNORECASE)),
    ("card", re.compile(r"(?<!\d)\d{4}([ -]?)\d{4}\1\d{4}\1\d{4}(?!\d)")),
    ("mobile", re.compile(r"(?<![\d+])(?:\+?90[\s-]?)?\(?0?5\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)")),
    ("tckn", re.compile(r"(?<!\d)[1-9]\d{10}(?!\d)")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")),
)
# Reserved for documentation (RFC 2606 / 6761): an address there is a
# placeholder, never a person's.
EMAIL_PLACEHOLDER_RE = re.compile(r"@(?:[\w-]+\.)*(?:example\.(?:com|net|org)|[\w-]+\.(?:example|test|invalid|localhost))$",
                                  re.IGNORECASE)


def _pii_placeholder(kind, value):
    digits = re.sub(r"\D", "", value)
    if kind == "email":
        return bool(EMAIL_PLACEHOLDER_RE.search(value))
    if kind == "mobile":
        return set(digits[-7:]) == {"0"}  # the subscriber number all zero: "0500 000 00 00"
    if kind == "iban":
        return set(digits[2:]) <= {"0"}  # after the check digits
    return set(digits[4:]) <= {"0"}  # card: "0000 0000 0000 0000"


def _mask(value):
    """Enough of a match to find it, not enough to read it."""
    keep = re.sub(r"\s", "", value)
    if len(keep) <= 4:
        return "•" * len(keep)
    return keep[:2] + "•" * (len(keep) - 4) + keep[-2:]


GATE_MSG = {
    "numbers": ("numbers differ between A and B (only in A: {a}; only in B: {b}): a price, amount, percentage, count "
                "or rating that changes between the arms is a second variable, unless the record says why in "
                "`numeric_change`",
                "sayılar A ile B arasında farklı (yalnızca A'da: {a}; yalnızca B'de: {b}): kollar arasında değişen "
                "bir fiyat, tutar, yüzde, adet ya da puan ikinci bir değişkendir; kayıt nedenini `numeric_change` "
                "alanında söylemedikçe"),
    "a11y_none": ("B adds an interactive element ({what}) and the record has no accessibility warning (rule 3): add a "
                  "warnings item of type accessibility whose pass/fail criteria fit the element ({need})",
                  "B etkileşimli bir öğe ekliyor ({what}) ve kayıtta erişilebilirlik uyarısı yok (kural 3): öğeye "
                  "uyan geçti/kaldı ölçütleriyle accessibility türünde bir warnings maddesi ekleyin ({need})"),
    "a11y_missing": ("B adds an interactive element ({what}); the accessibility warning lacks: {missing} (rule 3; "
                     "criteria for this element: {need})",
                     "B etkileşimli bir öğe ekliyor ({what}); erişilebilirlik uyarısında eksik: {missing} (kural 3; "
                     "bu öğenin ölçütleri: {need})"),
    "legal": ("rule 11: legal or mandatory text in A is missing or changed in B (“{text}”); a variant that changes a "
              "regulated display is held until the market's rule is verified, it isn't rendered",
              "kural 11: A'daki yasal ya da zorunlu metin B'de yok ya da değişmiş (“{text}”); düzenlemeye tabi bir "
              "gösterimi değiştiren varyant, pazarın kuralı doğrulanana dek bekletilir, çizilmez"),
    "auth": ("rule 6: B drops security or verification text that A shows (“{term}”: {na} in A, {nb} in B); security "
             "and compliance controls aren't test subjects",
             "kural 6: B, A'nın gösterdiği güvenlik ya da doğrulama metnini düşürüyor (“{term}”: A'da {na}, B'de "
             "{nb}); güvenlik ve uyum denetimleri test konusu yapılmaz"),
    "consent": ("rule 6: a consent box that A leaves unticked is ticked in B (“{text}”); a pre-ticked consent is a "
                "dark pattern and is refused",
                "kural 6: A'da işaretsiz duran onay kutusu B'de işaretli (“{text}”); önceden işaretlenmiş onay "
                "karanlık bir örüntüdür ve reddedilir"),
    "consent_removed": ("rule 6: B removes a consent box that A shows (“{text}”); legal consent is a compliance "
                        "control, never a test subject: the scenario is not produced, and improving the consent step "
                        "is the compliance team's work",
                        "kural 6: B, A'nın gösterdiği onay kutusunu kaldırıyor (“{text}”); yasal onay bir uyum "
                        "denetimidir, test konusu yapılmaz: senaryo üretilmez, onay adımını iyileştirmek uyum "
                        "ekibinin işidir"),
    "metadata": ("{field}: the mockup shows the record's own metadata (“{text}”); the card shows only the title, the "
                 "two mockups and the ring labels, and a KPI, guardrail, evidence or priority line is never drawn into "
                 "a mockup (rule 9)",
                 "{field}: mockup kaydın kendi bilgisini gösteriyor (“{text}”); kart yalnızca başlığı, iki mockup'ı ve "
                 "halka etiketlerini gösterir, KPI, guardrail, kanıt ya da öncelik satırı mockup'a çizilmez (kural 9)"),
    "pii": ("{field}: a value shaped like personal data ({kind}: “{masked}”); rule 15: personal data never reaches a "
            "card. Draw the field empty with its label, mask the value (“•••”) or use an all-zero placeholder",
            "{field}: kişisel veri biçiminde bir değer ({kind}: “{masked}”); kural 15: kişisel veri karta asla "
            "taşınmaz. Alanı etiketiyle boş çizin, değeri maskeleyin (“•••”) ya da sıfırlı bir yer tutucu kullanın"),
}
PII_KIND = {
    "en": {"tckn": "TCKN", "iban": "IBAN", "card": "card number", "email": "e-mail address", "mobile": "mobile number"},
    "tr": {"tckn": "TCKN", "iban": "IBAN", "card": "kart numarası", "email": "e-posta adresi", "mobile": "cep telefonu"},
}


def _gm(key, lang, **kw):
    en, tr = GATE_MSG[key]
    return (tr if lang == "tr" else en).format(**kw)


def _short(text, n=60):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n - 1] + "…"


def _node_text(node):
    parts = []
    for k in node.kids:
        parts.append(k if isinstance(k, str) else _node_text(k))
    return " ".join(p for p in parts if p)


def _all_texts(root):
    """Every text node under root, in order."""
    return [text for _, text in _facts([root])[0]]


def number_problems(tree_a, tree_b, numeric_change, lang="en"):
    if isinstance(numeric_change, str) and numeric_change.strip():
        return []
    ca = collections.Counter(_numbers_of(_facts([tree_a])[0]))
    cb = collections.Counter(_numbers_of(_facts([tree_b])[0]))
    if ca == cb:
        return []
    only_a = ", ".join(sorted((ca - cb).elements())) or "-"
    only_b = ", ".join(sorted((cb - ca).elements())) or "-"
    return [_gm("numbers", lang, a=only_a, b=only_b)]


def accessibility_criteria(dialog=False):
    """validate_scenario_json's criteria: (TR label, EN label, compiled regex) each."""
    import validate_scenario_json as vsj  # here, not at module level: the validator imports this module
    return list(vsj.A11Y_BASE) + (list(vsj.A11Y_MODAL) if dialog else [])


def accessibility_problems(tree_a, tree_b, warnings, lang="en"):
    ca, cb = _facts([tree_a])[1], _facts([tree_b])[1]
    added = [c for c in INTERACTIVE_COMPONENTS if cb[c] > ca[c]]
    if not added:
        return []
    import validate_scenario_json as vsj
    what = ", ".join("%s %d → %d" % (c, ca[c], cb[c]) for c in added)
    criteria = accessibility_criteria(dialog=any(c in DIALOG_COMPONENTS for c in added))
    label = 0 if lang == "tr" else 1
    need = ", ".join(c[label] for c in criteria)
    stated = vsj.warning_text({"warnings": warnings or []}, "accessibility")
    if not stated:
        return [_gm("a11y_none", lang, what=what, need=need)]
    missing = [c[label] for c in criteria if not c[2].search(stated)]
    if missing:
        return [_gm("a11y_missing", lang, what=what, missing=", ".join(missing), need=need)]
    return []


def consent_boxes(root):
    """Every consent checkbox under root: an r-check whose text reads as consent."""
    return [n for n in _walk(root) if "r-check" in n.classes and CONSENT_RE.search(_fold(_node_text(n)))]


def regulation_problems(tree_a, tree_b, lang="en"):
    out = []
    boxes_a, boxes_b = consent_boxes(tree_a), consent_boxes(tree_b)
    # Rule 6, not rule 11: B shows fewer consent boxes than A, so a consent step is gone (not reworded, which
    # keeps the count and stays a rule-11 hold below). Each A box whose text B lacks is reported as removed.
    removed = []
    if len(boxes_b) < len(boxes_a):
        missing = (collections.Counter(_node_text(n) for n in boxes_a)
                   - collections.Counter(_node_text(n) for n in boxes_b))
        for node in boxes_a:
            if missing[_node_text(node)] > 0:
                missing[_node_text(node)] -= 1
                removed.append(node)
                out.append(_gm("consent_removed", lang, text=_short(_node_text(node))))
    reported = collections.Counter(t for node in removed for t in _all_texts(node))
    texts_a, texts_b = _all_texts(tree_a), _all_texts(tree_b)
    legal_b = collections.Counter(texts_b)
    for text, n in collections.Counter(t for t in texts_a if LEGAL_RE.search(_fold(t))).items():
        if legal_b[text] < n - reported[text]:
            out.append(_gm("legal", lang, text=_short(text)))
    fa, fb = _fold(" \n ".join(texts_a)), _fold(" \n ".join(texts_b))
    for term in AUTH_TERMS:
        pattern = _term_re((term,))
        na, nb = len(pattern.findall(fa)), len(pattern.findall(fb))
        if nb < na:
            out.append(_gm("auth", lang, term=term, na=na, nb=nb))

    ticked_in_a = {_node_text(n) for n in boxes_a if "on" in n.classes}
    for node in boxes_b:
        if "on" in node.classes and _node_text(node) not in ticked_in_a:
            out.append(_gm("consent", lang, text=_short(_node_text(node))))
    return out


# Words that only the record uses, never a page: a mockup that carries them is
# the old card's text smuggled into the drawing.
METADATA_RE = re.compile(r"\b(?:birincil\s+kpi|primary\s+kpi|guardrail|kanıt\s*:|evidence\s*:|öncelik\s*:|priority\s*:"
                         r"|daha\s+güçlü\s+alternatif|stronger\s+alternative)", re.IGNORECASE)


def metadata_problems(field, root, kpi_names, lang="en"):
    """Rule 9: the record's KPI, guardrail, evidence or priority never reaches the drawing."""
    out = []
    for text in _all_texts(root):
        folded = text.casefold()
        hit = METADATA_RE.search(text)
        name = next((n for n in kpi_names if n.casefold() in folded), None)
        if hit or name:
            out.append(_gm("metadata", lang, field=field, text=(hit.group(0) if hit else name)))
            break
    return out


def pii_problems(field, root, lang="en"):
    out, seen = [], set()
    values = list(_all_texts(root))
    for node in _walk(root):
        for name, value in node.attrs.items():
            if name not in ("class", "style") and value:
                values.append(value)
    for value in values:
        taken = []  # spans already matched in this value: an IBAN is not also a card number
        for kind, pattern in PII_PATTERNS:
            for m in pattern.finditer(value):
                hit = m.group(0)
                if any(m.start() < e and s < m.end() for s, e in taken):
                    continue
                taken.append(m.span())
                if _pii_placeholder(kind, hit) or (kind, hit) in seen:
                    continue
                seen.add((kind, hit))
                out.append(_gm("pii", lang, field=field, kind=PII_KIND[lang if lang == "tr" else "en"][kind],
                               masked=_mask(hit)))
    return out


def layout_fields(view):
    """The card fields layout_field_problems() checks, from a normalized view."""
    return {"device": view.get("device"), "stage_captions": view.get("stage_captions"),
            "mobile_toolbar": view.get("mobile_toolbar", False)}


def mockup_report(view, lang="en", classes=None):
    """Every mechanical gate on the two mockups of one card.

    Returns (errors, warnings, manifest): card_problems() (markup, rings, the
    outside-ring diff, colour), plus the record-dependent gates (numbers,
    accessibility, regulation and manipulation, personal data), and the
    manifest of the changes inside the rings: {"rings": [...], "changes": [...]}.
    """
    a, b = view["variant_a"], view["variant_b"]
    errors, warnings = card_problems(view["difference"], a, b, lang=lang, variable=view["variable"], classes=classes,
                                     card_lang=view.get("lang"), change_text=view.get("change_text"),
                                     layout=layout_fields(view))
    manifest = {"rings": [], "changes": []}
    tree_a, _ = parse_markup(a, lang)
    tree_b, _ = parse_markup(b, lang)
    if tree_a is None or tree_b is None:
        return errors, warnings, manifest
    errors += number_problems(tree_a, tree_b, view.get("numeric_change"), lang)
    errors += accessibility_problems(tree_a, tree_b, view.get("warnings"), lang)
    errors += regulation_problems(tree_a, tree_b, lang)
    errors += pii_problems("variant_a", tree_a, lang) + pii_problems("variant_b", tree_b, lang)
    errors += metadata_problems("variant_a", tree_a, view.get("kpi_names") or [], lang)
    errors += metadata_problems("variant_b", tree_b, view.get("kpi_names") or [], lang)
    regions, _ = _compare(tree_a, tree_b)
    manifest["rings"], manifest["changes"] = manifest_entries(regions)
    return errors, warnings, manifest


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


# ---------------------------------------------------------------- brand

def css_string(value):
    """A CSS string literal that cannot end the string or the <style> block."""
    out = []
    for ch in str(value):
        if ch in '\\"<>&' or ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\%x " % ord(ch))
        else:
            out.append(ch)
    return '"%s"' % "".join(out)


def web_scale_css(scale):
    """card.web_scale → one zoom rule for the browser frame, or nothing (default 1)."""
    if scale == 1:
        return ""
    return "  .browser{zoom:%s}\n" % scale


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


# ------------------------------------------------------------------- building

def build(template_text, scenario, warnings=None, lang=None, manifest=None):
    """Fill the template from one scenario record and return the card's HTML.

    Dies (exit 2) on anything that must not reach a card: every mechanical gate
    of mockup_report() runs here, so no caller gets a card around them.
    Non-blocking remarks about the mockups are appended to `warnings` when a
    list is passed; main() prints them. When a dict is passed as `manifest` it
    receives the inside-ring changes ({"rings": [...], "changes": [...]}).
    `lang` is the language of the messages (default: --lang).

    The title is the only text of the record that reaches the card (escaped);
    the rest of the card is the two mockups and their frame. Nothing in the
    HTML comes from `review`: the card's fingerprint is the sha256 of these
    bytes, and a stamp that changed them would never match.
    """
    lang = lang or _MSG_LANG
    view = normalize(scenario, lang)

    for key in ("variant_a", "variant_b"):
        value = view[key]
        if value in (None, ""):
            die(_t("scenario is missing required card field: card.%s",
                   "senaryoda zorunlu kart alanı eksik: card.%s", lang) % key)
        if not isinstance(value, str) or not value.strip():
            die(_t("card field %s must be a non-empty string of markup, got %s",
                   "%s kart alanı boş olmayan bir işaretleme metni olmalı, gelen %s", lang)
                % (key, type(value).__name__))

    errors, notes, found = mockup_report(view, lang=lang, classes=component_classes(template_text))
    if errors:
        die(_t("the mockup was refused; nothing was cleaned or rewritten, fix the input:\n  ",
               "mockup reddedildi; hiçbir şey temizlenmedi ya da yeniden yazılmadı, girdiyi düzeltin:\n  ", lang)
            + "\n  ".join(errors))
    if warnings is not None:
        warnings.extend(notes)
    if manifest is not None:
        manifest.update(found)

    # User text never goes into the template directly: the frame helpers leave a
    # placeholder and its value joins the one substitution pass below.
    values = frame_values(view)
    layout = layout_of(view)
    text = apply_layout(apply_frame(COMMENT_RE.sub("", template_text), view["device"], has_bottom_nav(view)), layout)
    values.update({
        "{{TITLE}}": escape(view["title"]),
        "{{LANG}}": view["lang"],
        "{{DEVICE}}": view["device"],
        "{{NOTE_POS}}": view["note_pos"],
        "{{PHONE_SCALE}}": view["phone_scale"],
        "{{BRAND_CSS}}": brand_css(view["brand"]) + web_scale_css(view["web_scale"]),
    })
    # Screens go in raw: this is the generative region, checked above. A screen
    # with a fold or stage breaks goes in as its pieces (layout_values).
    for ph, key in SCREEN_PLACEHOLDERS.items():
        values[ph] = view[key]
    values.update(layout_values(view, layout))

    # The template is checked BEFORE anything is filled in, so a "{{AD}}" inside
    # a title or a mockup is never mistaken for a placeholder of the template.
    unknown = sorted(set(PLACEHOLDER_RE.findall(text)) - set(values))
    if unknown:
        die("template has placeholders this tool does not fill: %s" % ", ".join(unknown))

    # Drop the line of a placeholder that fills with nothing (no brand override)
    # so the delivered source carries no whitespace-only line. Done on the
    # template, not on the filled card: the mockups are inserted byte for byte
    # and their own blank lines are not ours to remove.
    for ph, value in values.items():
        if value == "":
            text = re.sub(r"(?m)^[ \t]*%s[ \t]*\n" % re.escape(ph), "", text)

    # One pass. Inserted text is never scanned again: a title that says
    # "{{VARIANT_B_SCREEN}}" stays a title.
    text = PLACEHOLDER_RE.sub(lambda m: values[m.group(0)], text)

    # A proposal resting on an unverified critical fact is delivered marked as
    # such: the ribbon and the meta are part of the final bytes, so the mockup
    # reviewer reviews (and its stamp approves) the card as the user sees it.
    if view["critical_assumptions"]:
        text = conditional_html(text, view["lang"])
    # A contrast defect copied from the user's own screen, documented element by
    # element: render_check reports it as inherited (not a pass) instead of
    # failing the card, and only where the element is identical in both arms and
    # outside the rings. Everything else keeps the 4.5:1 / 3:1 floor.
    if view["inherited_contrast"]:
        head_end = text.find("</head>")
        meta = '<meta name="abtest-inherited-contrast" content="%s">\n' % escape(
            json.dumps(view["inherited_contrast"], ensure_ascii=False, separators=(",", ":")))
        text = text[:head_end] + meta + text[head_end:]

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


def fixed_lines(template_text, device="phone", bottom_nav=False, layout=None):
    """Lines of the template that must survive verbatim into the built card.

    The template is first turned into the card's frame (apply_frame: the
    device swaps the phone skeleton for a browser or adds the address bar, a
    native phone keeps its tab bar only when the record names its tabs), so the
    frames and the pills are checked like everything else. Excluded:
    placeholder lines (language, device, title, the mockups, the brand
    override), developer comments (intentionally dropped) and blank lines.
    """
    text = apply_layout(apply_frame(COMMENT_RE.sub("", template_text), device, bottom_nav), layout)
    return [line for line in text.splitlines() if line.strip() and "{{" not in line]


def self_verify(built_text, template_text, device="phone", bottom_nav=False, variants=None, layout=None):
    """Refuse to emit a card that drifted from the template's fixed skeleton,
    or that carries executable markup.

    `device` and `bottom_nav` name the frame the card was built with (the
    view's device and has_bottom_nav()), `layout` its layout (layout_of());
    fixed_lines() applies the same frame and layout.

    `variants` are the two raw mockup strings. The allowlist in build() is the
    gate; this is the second layer behind it. Tag-shaped patterns (<script,
    <iframe …) are searched in the whole built card, where escaped text can
    never match them. Scheme and handler patterns are searched inside the tags
    of the raw variants only, after entity decoding and with whitespace and
    control characters removed: a title or a line of mockup text saying
    "JavaScript:" is ordinary text, a "jav&#x61;script:" in an attribute is not.
    """
    missing = [line.strip() for line in fixed_lines(template_text, device, bottom_nav, layout) if line not in built_text]
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
            "representative one)",
            "card.url: device '{device}' adres çubuğu çizer; alan adını yazın (görünmüyorsa temsilî bir adres "
            "yazın)"),
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


def preflight(scenario, lang="en"):
    """What must hold before a card is built. Returns (errors, warnings).

    The record goes through the same validator the skills run
    (validate_scenario_json), whatever its shape: only scenario records build.
    A record without `card` gets one more error saying what a card needs.
    """
    # Imported here, not at module level: the validator imports this module.
    import validate_scenario_json as vsj
    schema = vsj.load_schema()
    errors = vsj.validate(scenario, schema, lang)
    warnings = vsj.lint(scenario, schema, lang, include_card=False)
    if not isinstance(scenario.get("card"), dict):
        errors.append(_t(*NO_CARD_MSG, lang=lang))
    return errors, warnings


# ------------------------------------------------- fingerprints and review gates
#
# Two stamps in the record's `review`, each written only on a PASS:
#   review.scenario_critic.fingerprint = record_fingerprint(record)
#       (validate_scenario_json.py; the record without `review` and `card`)
#   review.mockup_reviewer.fingerprint = sha256 of the exact bytes the final
#       build writes (html_fingerprint of final_html()), printed by --draft
# A draft needs the first, a final build both. Any edit after a review changes
# the fingerprint it approved, by design: the edit goes back to that reviewer.

REVIEWERS = {"scenario_critic": "scenario-critic", "mockup_reviewer": "mockup-reviewer"}
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")
DRAFT_BANNER = {"tr": "TASLAK · incelenmedi", "en": "DRAFT · not reviewed"}
# The draft marker is a tab hanging from the card's top edge at its right
# corner, inside the card's 40px top padding: absolutely positioned, so it
# overlays the card without moving anything in it (the draft lays out exactly
# like the final card it stands for) and covers no content.
DRAFT_RIBBON_STYLE = ("position:absolute;top:0;right:48px;z-index:20;padding:8px 14px;border-radius:0 0 8px 8px;"
                      "background:#b42318;color:#ffffff;font:700 13px/1 -apple-system,\"Segoe UI\",Inter,Roboto,"
                      "\"Helvetica Neue\",Arial,sans-serif;letter-spacing:.04em;white-space:nowrap;pointer-events:none")
CARD_OPEN_RE = re.compile(r'<div class="card"[^>]*>\n')
MANIFEST_SUFFIX = ".manifest.json"

# A record with at least one critical assumption (`assumptions[].type ==
# "critical"`: feasibility, legality or single-variable status rests on a fact
# the user hasn't confirmed) builds a CONDITIONAL card. Unlike the draft
# ribbon this one is part of the final card: the user sees that the proposal
# waits on an answer. It hangs from the card's top edge at the LEFT corner, so
# on the draft of a conditional card both ribbons show; like the draft ribbon
# it is absolutely positioned inside the card's 40px top padding and moves
# nothing. Light on purpose (a small amber note, not a second title): amber
# text on a light amber surface with a thin amber border, 12px, 7.0:1. Once the
# user confirms, the assumption leaves the record (critic again), and the card
# builds without the ribbon.
CONDITIONAL_BANNER = {"tr": "KOŞULLU · doğrulama gerekli", "en": "CONDITIONAL · needs verification"}
CONDITIONAL_SUMMARY = "conditional card (not implementation-ready)"
CONDITIONAL_META = '<meta name="abtest-status" content="conditional">\n'
CONDITIONAL_RIBBON_STYLE = ("position:absolute;top:0;left:48px;z-index:20;padding:5px 10px;border:1px solid #fcd34d;"
                            "border-top:0;border-radius:0 0 6px 6px;background:#fffbeb;color:#92400e;"
                            "font:600 12px/1 -apple-system,\"Segoe UI\",Inter,Roboto,\"Helvetica Neue\",Arial,sans-serif;"
                            "letter-spacing:.02em;white-space:nowrap;pointer-events:none")


def critical_assumptions(scenario):
    """The record's well-formed critical assumptions (`assumptions` items whose
    type is "critical"). Tolerant: no field, or a field of another shape, is
    none (the validator reports the shape)."""
    items = scenario.get("assumptions") if isinstance(scenario, dict) else None
    if not isinstance(items, list):
        return []
    return [a for a in items if isinstance(a, dict) and a.get("type") == "critical"]


def is_conditional(scenario):
    """True when the record's card is built as a conditional card."""
    return bool(critical_assumptions(scenario))


def conditional_html(text, card_lang="tr"):
    """A filled card plus the conditional ribbon and <meta name="abtest-status"
    content="conditional">: the meta closes <head>, the ribbon is its own line
    right after the card's opening tag. Nothing else changes."""
    head_end = text.find("</head>")
    card = CARD_OPEN_RE.search(text)
    if head_end < 0 or card is None or card.start() < head_end:
        die("template has no <head>…</head> and <div class=\"card\">: the conditional ribbon and meta tag have "
            "nowhere to go")
    ribbon = '  <div id="abtest-conditional" role="note" style="%s">%s</div>\n' % (
        escape(CONDITIONAL_RIBBON_STYLE), escape(CONDITIONAL_BANNER.get(card_lang, CONDITIONAL_BANNER["en"])))
    text = text[:head_end] + CONDITIONAL_META + text[head_end:]
    card = CARD_OPEN_RE.search(text)
    return text[:card.end()] + ribbon + text[card.end():]


def html_fingerprint(text):
    """sha256 hex of the bytes a card file holds (UTF-8, written as is)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def final_html(template_text, scenario, lang=None):
    """The final card, built and self-verified in memory: (html, manifest, warnings).

    Dies on anything a gate refuses. The draft and the final build both start
    from this, so the bytes a mockup reviewer approves are the bytes the final
    build writes.
    """
    warnings, manifest = [], {}
    built = build(template_text, scenario, warnings=warnings, lang=lang, manifest=manifest)
    view = normalize(scenario)
    self_verify(built, template_text, view["device"], has_bottom_nav(view),
                variants=(view["variant_a"], view["variant_b"]), layout=layout_of(view))
    return built, manifest, warnings


def final_fingerprint(template_text, scenario, lang=None):
    """The fingerprint a mockup-reviewer stamp must carry for this record and template."""
    return html_fingerprint(final_html(template_text, scenario, lang)[0])


def draft_html(final_text, fingerprint, card_lang="tr"):
    """The final card plus the draft ribbon and the two draft meta tags.

    The ribbon is its own line right after the card's opening tag; the meta
    tags close <head>. Nothing else of the final card changes. On a
    conditional card the draft's metas go in just before the conditional
    meta, so the first abtest-status a reader finds says "draft".
    """
    head_end = final_text.find("</head>")
    card = CARD_OPEN_RE.search(final_text)
    if head_end < 0 or card is None or card.start() < head_end:
        die("template has no <head>…</head> and <div class=\"card\">: the draft ribbon and meta tags have "
            "nowhere to go")
    metas = ('<meta name="abtest-status" content="draft">\n'
             '<meta name="abtest-final-fingerprint" content="%s">\n' % fingerprint)
    ribbon = '  <div id="abtest-draft" role="status" style="%s">%s</div>\n' % (
        escape(DRAFT_RIBBON_STYLE), escape(DRAFT_BANNER.get(card_lang, DRAFT_BANNER["en"])))
    at = final_text.find(CONDITIONAL_META, 0, head_end)
    at = head_end if at < 0 else at
    text = final_text[:at] + metas + final_text[at:]
    card = CARD_OPEN_RE.search(text)
    return text[:card.end()] + ribbon + text[card.end():]


def record_fingerprint_of(record):
    """validate_scenario_json.record_fingerprint, the one definition of it."""
    import validate_scenario_json as vsj  # here, not at module level: the validator imports this module
    fn = getattr(vsj, "record_fingerprint", None)
    if fn is None:
        die("validate_scenario_json.py has no record_fingerprint(); the record's fingerprint can't be computed")
    return fn(record)


STAMP_MSG = {
    "missing_critic": ("missing review stamp: review.scenario_critic. Run scenario-critic on the record; on PASS "
                       "stamp {{\"verdict\": \"PASS\", \"fingerprint\": <what validate_scenario_json.py "
                       "--fingerprint prints>}}",
                       "inceleme damgası eksik: review.scenario_critic. Kaydı scenario-critic'e inceletin; PASS "
                       "gelirse {{\"verdict\": \"PASS\", \"fingerprint\": <validate_scenario_json.py --fingerprint "
                       "çıktısı>}} damgasını ekleyin"),
    "missing_mockup": ("missing review stamp: review.mockup_reviewer. Build the draft (--draft), have mockup-reviewer "
                       "review the draft and its manifest; on PASS stamp the final fingerprint the draft build printed",
                       "inceleme damgası eksik: review.mockup_reviewer. Taslağı kurun (--draft), taslağı ve "
                       "manifestini mockup-reviewer'a inceletin; PASS gelirse taslak kurulumunun yazdığı nihai parmak "
                       "izini damgalayın"),
    "verdict": ("review.{key}.verdict is {val!r}: only a PASS is ever stamped (FIX and RET go back to {name})",
                "review.{key}.verdict değeri {val!r}: yalnızca PASS damgalanır (FIX ve RET {name} adımına geri döner)"),
    "format": ("review.{key}.fingerprint must be a sha256 hex string (64 lowercase characters), got {val!r}",
               "review.{key}.fingerprint bir sha256 onaltılık dizesi olmalı (64 küçük harf karakter), gelen {val!r}"),
    "stale_critic": ("review.scenario_critic.fingerprint ({val}…) doesn't match the record: the record changed after "
                     "scenario-critic reviewed it, so it goes back to scenario-critic",
                     "review.scenario_critic.fingerprint ({val}…) kayıtla eşleşmiyor: kayıt scenario-critic "
                     "incelemesinden sonra değişmiş, yeniden scenario-critic'e gider"),
    "stale_mockup": ("review.mockup_reviewer.fingerprint ({val}…) doesn't match the card this build would write: the "
                     "record's card, its text or the template changed after mockup-reviewer reviewed the draft; build "
                     "a new draft and have it reviewed",
                     "review.mockup_reviewer.fingerprint ({val}…) bu kurulumun yazacağı kartla eşleşmiyor: "
                     "mockup-reviewer taslağı inceledikten sonra kaydın kartı, metni ya da şablon değişmiş; yeni bir "
                     "taslak kurup inceletin"),
}


def _sm(msg_id, lang, **kw):
    en, tr = STAMP_MSG[msg_id]
    return (tr if lang == "tr" else en).format(**kw)


def stamp_problems(scenario, key, expected, lang="en"):
    """Why review.<key> doesn't approve `expected` (a fingerprint), or []."""
    review = scenario.get("review")
    stamp = review.get(key) if isinstance(review, dict) else None
    if not isinstance(stamp, dict):
        return [_sm("missing_critic" if key == "scenario_critic" else "missing_mockup", lang)]
    if stamp.get("verdict") != "PASS":
        return [_sm("verdict", lang, key=key, val=stamp.get("verdict"), name=REVIEWERS[key])]
    fp = stamp.get("fingerprint")
    if not isinstance(fp, str) or not FINGERPRINT_RE.match(fp):
        return [_sm("format", lang, key=key, val=fp)]
    if fp != expected:
        return [_sm("stale_critic" if key == "scenario_critic" else "stale_mockup", lang, val=fp[:12])]
    return []


def manifest_document(scenario, view, manifest, final_fp, record_fp, draft_path):
    """The JSON written next to a draft: what the mockup reviewer checks item by item."""
    numeric = view.get("numeric_change")
    doc = {
        "format": MANIFEST_FORMAT,
        "version": MANIFEST_VERSION,
        "draft": os.path.basename(draft_path),
        "id": scenario.get("id"),
        "title": scenario.get("title"),
        "variable": view.get("variable"),
        "difference": view.get("difference"),
        # What the mockups are drawn from: shared_page → compare A with the shared page.
        "mockup_basis": view.get("mockup_basis"),
        "numeric_change": numeric if isinstance(numeric, str) and numeric.strip() else None,
        "record_fingerprint": record_fp,
        "final_fingerprint": final_fp,
        "rings": manifest.get("rings", []),
        "changes": manifest.get("changes", []),
    }
    if view.get("screen_spec"):
        doc["screen_spec"] = True  # the mockups were compiled from card.screen + card.change
    return doc


GATES = {
    "validator": ("record validation", "kayıt doğrulaması"),
    "card": ("card checks", "kart denetimleri"),
    "review": ("review stamps", "inceleme damgaları"),
}


def build_summary(built, view):
    """The build's one-line summary; a conditional card says so."""
    summary = "%d bytes, device=%s, lang=%s, difference=%s" % (
        len(built.encode("utf-8")), view["device"], view["lang"], view["difference"] or "-")
    n = view.get("critical_assumptions") or 0
    if n:
        summary += ", %s: %d critical assumption%s" % (CONDITIONAL_SUMMARY, n, "" if n == 1 else "s")
    return summary


class _Refused(Exception):
    """A gate refused the build. `problems` are printed by main(); empty when
    the refusing stage (a die() inside it) has printed its own message."""

    def __init__(self, gate, problems=(), header=None):
        Exception.__init__(self, gate)
        self.gate, self.problems, self.header = gate, list(problems), header


def _gate(gate, fn, *args, **kw):
    """Run one stage; a die() inside it is a refusal at `gate`."""
    try:
        return fn(*args, **kw)
    except SystemExit as exc:
        if exc.code in (0, None):
            raise
        raise _Refused(gate)


def _not_written(gate, paths, lang):
    """The closing lines of every failure: which gate, and that nothing changed on disk."""
    if gate is not None:
        name = GATES[gate][1 if lang == "tr" else 0]
        sys.stderr.write(_t("build_card: REFUSED at the “%s” gate; nothing was written.\n",
                            "build_card: “%s” kapısında REDDEDİLDİ; hiçbir şey yazılmadı.\n", lang) % name)
    for path in paths:
        if os.path.exists(path):
            sys.stderr.write(_t("build_card: %s already exists and was NOT updated.\n",
                                "build_card: %s zaten var ve GÜNCELLENMEDİ.\n", lang) % path)


def _write_all(files):
    """Write every (path, text) or none: each goes to a temporary file in its
    directory first, and all are moved into place only once all are written."""
    import tempfile
    # mkstemp creates the file 0600; a card is an ordinary file, so give it the
    # permissions open() would (0666 minus the umask), or a local web server running
    # as another user can't read it.
    umask = os.umask(0)
    os.umask(umask)
    staged = []
    try:
        for path, text in files:
            directory = os.path.dirname(os.path.abspath(path))
            if not os.path.isdir(directory):
                os.makedirs(directory, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=directory, prefix=".build_card-", suffix=".tmp")
            with os.fdopen(fd, "wb") as fh:  # bytes: the fingerprint is of exactly these bytes
                fh.write(text.encode("utf-8"))
            os.chmod(tmp, 0o666 & ~umask)
            staged.append((tmp, path))
        for tmp, path in staged:
            os.replace(tmp, path)
    finally:
        for tmp, _ in staged:
            if os.path.exists(tmp):
                os.remove(tmp)


def _run(args, lang):
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

    errors, warnings = preflight(scenario, lang)
    if errors:
        raise _Refused("validator", errors, header=_t(
            "the scenario was refused (%d problem(s)):", "senaryo reddedildi (%d sorun):", lang) % len(errors))

    built, manifest, notes = _gate("card", final_html, template_text, scenario, lang)
    warnings += notes
    view = normalize(scenario)
    final_fp = html_fingerprint(built)

    record_fp = _gate("validator", record_fingerprint_of, scenario)
    problems = stamp_problems(scenario, "scenario_critic", record_fp, lang)
    if not args.draft:
        problems += stamp_problems(scenario, "mockup_reviewer", final_fp, lang)
    if problems:
        raise _Refused("review", problems, header=_t(
            "the %s build was refused:" % ("draft" if args.draft else "final"),
            "taslak kurulumu reddedildi:" if args.draft else "nihai kurulum reddedildi:", lang))

    summary = build_summary(built, view)
    if args.draft:
        draft = draft_html(built, final_fp, view["lang"])
        manifest_path = args.out + MANIFEST_SUFFIX
        doc = manifest_document(scenario, view, manifest, final_fp, record_fp, args.out)
        _write_all([(args.out, draft), (manifest_path, json.dumps(doc, ensure_ascii=False, indent=2) + "\n")])
        print("draft: %s (%s%s)" % (args.out, summary, ", %d warning(s)" % len(warnings) if warnings else ""))
        print("manifest: %s (%d change(s) inside %d ring(s))" % (manifest_path, len(doc["changes"]), len(doc["rings"])))
        print("final fingerprint: %s" % final_fp)
        stale = stamp_problems(scenario, "mockup_reviewer", final_fp, lang)
        review = scenario.get("review") if isinstance(scenario.get("review"), dict) else {}
        if stale and "mockup_reviewer" in review:
            warnings.append(stale[0])
    else:
        _write_all([(args.out, built)])
        print("built %s (%s%s)" % (args.out, summary, ", %d warning(s)" % len(warnings) if warnings else ""))
        print("final fingerprint: %s" % final_fp)
        print(_t("reviews: scenario-critic PASS, mockup-reviewer PASS (both stamps match)",
                 "incelemeler: scenario-critic PASS, mockup-reviewer PASS (iki damga da eşleşiyor)", lang))
    for note in warnings:
        warn(note)
    return 0


def main(argv):
    global _MSG_LANG
    ap = argparse.ArgumentParser(description="Build a scenario card from the template.")
    ap.add_argument("--template", required=True, help="path to templates/scenario-card.html")
    ap.add_argument("--scenario", required=True, help="JSON file describing the scenario")
    ap.add_argument("--out", required=True, help="path to write the card to")
    ap.add_argument("--draft", action="store_true",
                    help="build the review draft (ribbon, meta tags, <out>.manifest.json) instead of the final card")
    ap.add_argument("--lang", choices=("en", "tr"), default="en",
                    help="language of this tool's messages (default: en)")
    args = ap.parse_args(argv)
    _MSG_LANG = args.lang
    lang = args.lang
    paths = [args.out] + ([args.out + MANIFEST_SUFFIX] if args.draft else [])
    try:
        return _run(args, lang)
    except _Refused as refusal:
        if refusal.problems:
            sys.stderr.write("build_card: %s\n  - %s\n" % (
                refusal.header or _t("refused:", "reddedildi:", lang), "\n  - ".join(refusal.problems)))
        _not_written(refusal.gate, paths, lang)
        return 1
    except SystemExit as exc:
        if exc.code not in (0, None):
            _not_written(None, paths, lang)
        raise


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
