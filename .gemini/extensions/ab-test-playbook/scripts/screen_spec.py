#!/usr/bin/env python3
"""Screen spec compiler: the producer describes the screen, the builder draws it.

A record's card may carry, instead of the raw `variant_a` / `variant_b`
markup, a `screen` (a list of nodes, the page once) and a `change` (one
operation on one node: the tested element). compile() turns them into the
two mockup bodies the rest of the pipeline already knows: Variant A is the
screen as given, Variant B is a deep copy of A with the one operation
applied, the ring(s) placed where the difference type wants them. Nothing
downstream changes: the compiled markup enters build_card.py and
validate_scenario_json.py exactly where the raw markup enters today
(allowlist parser, card_problems, ring rules, A/B diff, manifest,
fingerprint, render_check).

Pure and deterministic: the same spec compiles to the same bytes, so two
records that share a screen list get a byte-identical Variant A, and every
page-colour override (fg, bg, border, radius, height) lands as inline style
in both arms by construction. Anything the compiler cannot draw (an unknown
kind, a missing target, a duplicate id, two changes) is a problem string;
the builder dies on it and the validator reports it. There is no silent
fallback.

Node shapes, one key names the kind (knowledge/mockup-style.md, "Screen spec"):

  {"header": {"logo": true|"Text", "nav": [..], "tel": "..", "icons": [{"icon": "close", "label": "Kapat"}], "line": false}}
  {"h": ".."}  {"sub": ".."}  {"text": "..", "align": "center"}  {"link": ".."}  {"help": ".."}  {"info": ".."}
  {"field": "placeholder", "label": "..", "select": true, "value": ".."}   {"row": [field, field]}
  {"cta": "..", "style": "filled"|"outline"|"ghost", "size": "sm"}
  {"check": "..", "on": true}  {"radio": "..", "on": true}
  {"chips": [{"label": "..", "on": true}]}  {"tabs": [{"label": "..", "on": true}]}
  {"steps": [{"label": "..", "state": "done"|"on"}]}  {"progress": 40}
  {"line": ["Ara toplam", "1.230 TL"], "total": true}
  {"item": {"name": "..", "meta": "..", "price": ".."}}
  {"plan": {"name": "..", "price": "..", "per": "/ay", "featured": true, "badge": "..", "cta": "..", "cta_style": "outline", "features": [".."]}}
  {"badge": "..", "style": "warn"|"brand"}  {"banner": ".."}  {"img": 150}  {"divider": true}  {"gap": 16}
  {"band": {"bg": "#f5f5f5", "items": [..], "pad": [top, bottom]}}
  {"fold": true}  {"stage": true}  {"sticky": node}  {"stack": {"items": [..], "gap": 16}}

Every node may carry "id" (the change's target), "mb" (margin-bottom in px,
instead of the screen's 16px rhythm) and the page-colour overrides "fg",
"bg", "border" (#rrggbb), "radius", "height" (px).

card.change, exactly one:
  {"op": "insert_after"|"insert_before", "target": id, "node": node, "label": "..", "label_pos": "below"|"above"}
  {"op": "replace", "target": id, "node": node, "label": "..", "label_a": ".."}
  {"op": "remove", "target": id, "label": ".."}
  {"op": "move_after"|"move_before", "target": id, "to": id, "label_a": "..", "label_b": ".."}
  {"op": "edit", "target": id, "set": {key: value, ..}, "label": ".."}
Any op may add "linked": [{"target": <a card.soft id>, "set": {..}}]: the
variable's linked consequences (an annual-default toggle switches the prices
under it), edits applied in B only to nodes card.soft rings in both arms.

card.soft: up to two node ids (or {"id": .., "note": ..}) wrapped in .hl-soft
in both arms, the variable's linked consequence.

Refused as well: a change B draws exactly like A (an identical replace, a move
to where the node already is, a hex colour differing only in case), a spacing
or size edit under MIN_PX_CHANGE px, a remove or move that leaves a container
empty, and a top-level-only node (fold, stage, sticky) moved into a container.
A header's "back" icon leads the bar (left of the logo); the other icons trail.

Python 3.9+, standard library only.
"""
import copy
import html
import re

GAP = 16            # the template's own rhythm between a screen's siblings (.screen gap)
LABEL_ROOM = 36     # room for a ring label placed below or above the ringed node (pill + offset)
BLEED = 20          # the screen's side (and bottom) padding a band bleeds through (.screen padding)
BLEED_TOP = 14      # the screen's top padding, bled through by a band that opens the screen
MAX_SOFT = 2
# A spacing or size edit smaller than this is not a difference a reader sees (mb 16 -> 17 is 1px).
MIN_PX_CHANGE = 8
PX_PROPS = ("mb", "height", "radius")
CONTAINER_EDITABLE = ("bg", "border", "radius", "height", "mb", "pad", "gap")
# An accordion's own state and header are one element each: opening it by
# default ("open": true) or rewording its header is a single change.
ACCORDION_EDITABLE = CONTAINER_EDITABLE + ("open", "title")
ACC_OPEN_SIGN, ACC_CLOSED_SIGN = "\u2212", "+"
ACC_BOX_STYLE = "border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb"
ACC_HEAD_STYLE = ("display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:44px;"
                  "font-weight:600;color:#111827")
ACC_SIGN_STYLE = "font-size:20px;font-weight:400;line-height:1;color:#374151"
ACC_BODY_STYLE = "padding-bottom:14px;color:#374151"

KINDS = ("header", "h", "sub", "text", "field", "row", "cta", "link", "help", "info", "check", "radio",
         "chips", "tabs", "steps", "progress", "line", "item", "plan", "badge", "banner", "img", "divider",
         "gap", "band", "fold", "stage", "sticky", "stack", "accordion")
COMMON_PROPS = ("id", "mb", "fg", "bg", "border", "radius", "height")
EXTRA_PROPS = {
    "text": ("align",),
    "field": ("label", "select", "value"),
    "cta": ("style", "size"),
    "check": ("on",),
    "radio": ("on",),
    "line": ("total",),
    "badge": ("style",),
}
TOP_ONLY = ("fold", "stage", "sticky")
CONTAINERS = ("row", "band", "stack", "sticky", "accordion")
OPS = ("insert_after", "insert_before", "replace", "remove", "move_after", "move_before", "edit")
# The difference type each op draws (card_problems checks the record's difference against the rings).
OP_DIFFERENCE = {"insert_after": "add", "insert_before": "add", "replace": "change", "edit": "change",
                 "remove": "remove", "move_after": "move", "move_before": "move"}
LABEL_POSITIONS = ("below", "above")
CTA_STYLES = ("filled", "outline", "ghost")
BADGE_STYLES = ("warn", "brand")
STEP_STATES = ("done", "on")
ICONS = ("close", "support", "menu", "search", "back")
ICON_LABELS = {
    "tr": {"close": "Kapat", "support": "Destek", "menu": "Menü", "search": "Ara", "back": "Geri"},
    "en": {"close": "Close", "support": "Support", "menu": "Menu", "search": "Search", "back": "Back"},
}
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}\Z")  # \Z: "#aabbcc\n" is not a colour

MSG = {
    "screen_type": ("card.screen must be a non-empty list of nodes",
                    "card.screen boş olmayan bir düğüm listesi olmalı"),
    "change_type": ("card.change must be one object {{\"op\": .., \"target\": ..}}: exactly one change per record",
                    "card.change tek bir nesne olmalı {{\"op\": .., \"target\": ..}}: kayıt başına tam bir değişiklik"),
    "change_missing": ("card.change is missing: a screen needs exactly one change (the tested element)",
                       "card.change eksik: bir ekranın tam bir değişikliği olmalı (test edilen öğe)"),
    "screen_missing": ("card.screen is missing: card.change needs the screen it applies to",
                       "card.screen eksik: card.change uygulanacağı ekranı ister"),
    "node_type": ("{path}: a node is an object with one kind key, got {what}",
                  "{path}: düğüm tek tür anahtarlı bir nesne olmalı, gelen {what}"),
    "kind_unknown": ("{path}: unknown node kind ({keys}); kinds are {kinds}",
                     "{path}: bilinmeyen düğüm türü ({keys}); türler {kinds}"),
    "kind_many": ("{path}: a node names one kind, this one names {n} ({keys})",
                  "{path}: düğüm tek tür adlandırır, bu düğüm {n} tür adlandırıyor ({keys})"),
    "prop_unknown": ("{path}: \"{key}\" is not a property of a {kind} node",
                     "{path}: \"{key}\" bir {kind} düğümünün özelliği değil"),
    "prop_value": ("{path}: \"{key}\" must be {want}, got {got!r}",
                   "{path}: \"{key}\" {want} olmalı, gelen {got!r}"),
    "value": ("{path}: a {kind} node's value must be {want}, got {got!r}",
              "{path}: {kind} düğümünün değeri {want} olmalı, gelen {got!r}"),
    "id_dup": ("{path}: id \"{id}\" is already used at {other}",
               "{path}: \"{id}\" kimliği zaten {other} yolunda kullanılıyor"),
    "top_only": ("{path}: a {kind} node sits only at the top level of the screen",
                 "{path}: {kind} düğümü yalnızca ekranın en üst düzeyinde durur"),
    "op_unknown": ("card.change.op must be one of {ops}, got {got!r}",
                   "card.change.op şunlardan biri olmalı: {ops}; gelen {got!r}"),
    "target_missing": ("card.change.target is missing: name the id of the node the change applies to",
                       "card.change.target eksik: değişikliğin uygulandığı düğümün kimliğini yazın"),
    "target_unknown": ("card.change.{key}: no node in card.screen has id \"{id}\"",
                       "card.change.{key}: card.screen içinde \"{id}\" kimlikli düğüm yok"),
    "change_key": ("card.change.{key}: {want}",
                   "card.change.{key}: {want}"),
    "change_extra": ("card.change: \"{key}\" is not a field of op {op}",
                     "card.change: \"{key}\" alanı {op} işleminin alanı değil"),
    "move_self": ("card.change: \"to\" names the moved node itself",
                  "card.change: \"to\" taşınan düğümün kendisini adlandırıyor"),
    "edit_key": ("card.change.set: \"{key}\" is not something a {kind} node has",
                 "card.change.set: \"{key}\" bir {kind} düğümünde yok"),
    "no_difference": ("card.change: B draws exactly what A draws ({why}); a test needs a difference the reader can see",
                      "card.change: B, A ile birebir aynı çiziliyor ({why}); testin okurun göreceği bir farkı olmalı"),
    "why_replace": ("the replacement node is the same as the target", "yeni düğüm hedefin aynısı"),
    "why_move": ("the moved node lands where it already is", "taşınan düğüm zaten durduğu yere iniyor"),
    "why_edit": ("the new values render the same, e.g. a hex colour differing only in case",
                 "yeni değerler aynı çiziliyor, ör. yalnızca büyük/küçük harfi farklı bir hex renk"),
    "why_generic": ("the change renders nothing new", "değişiklik yeni bir şey çizmiyor"),
    "px_small": ("card.change.set: \"{key}\" {old} -> {new} is a {d}px difference; under {min}px the arms look the same, "
                 "change it by at least {min}px or test something else",
                 "card.change.set: \"{key}\" {old} -> {new}, {d}px'lik bir fark; {min}px altında iki kol aynı görünür, "
                 "en az {min}px değiştirin ya da başka bir şeyi test edin"),
    "empty_container": ("card.change: the {op} leaves the {kind} at {where} empty in {arm}; an empty container draws "
                        "nothing (remove the container itself, or move a node that has siblings)",
                        "card.change: {op} işlemi {where} konumundaki {kind} kabını {arm} kolunda boş bırakıyor; boş kap "
                        "hiçbir şey çizmez (kabın kendisini kaldırın ya da kardeşi olan bir düğümü taşıyın)"),
    "move_top_only": ("card.change: a {kind} node sits only at the top level of the screen; it cannot move into "
                      "a {parent}",
                      "card.change: {kind} düğümü yalnızca ekranın en üst düzeyinde durur; bir {parent} içine taşınamaz"),
    "linked_type": ("card.change.linked must be a list of {{\"target\": <a card.soft id>, \"set\": {{..}}}}",
                    "card.change.linked bir {{\"target\": <card.soft kimliği>, \"set\": {{..}}}} listesi olmalı"),
    "edit_container": ("card.change.set: \"{key}\" on a {kind} reaches every element inside it, so B would change "
                       "several things at once; edit the one element inside instead (a {kind} itself takes only "
                       "bg, border, radius, height, mb, pad or gap)",
                       "card.change.set: bir {kind} üzerindeki \"{key}\" içindeki her öğeye ulaşır, B birden çok şeyi "
                       "değiştirirdi; içerideki tek öğeyi düzenleyin ({kind} kabının kendisinde yalnızca bg, border, "
                       "radius, height, mb, pad ya da gap değişir)"),
    "linked_label_a": ("card.change.linked with an edit or replace needs label_a: ring A's element too (\"Monthly by "
                       "default\"), so both arms show the variable next to its ringed consequence",
                       "card.change.linked, edit ya da replace ile label_a ister: A'daki öğeyi de halkalayın "
                       "(“Aylık varsayılan”), iki kol da değişkeni bağlı sonucunun yanında göstersin"),
    "linked_not_soft": ("card.change.linked: \"{id}\" is not in card.soft; a linked difference is the variable's "
                        "consequence and is drawn in a soft ring, so name the node in card.soft first",
                        "card.change.linked: \"{id}\" card.soft içinde değil; bağlı fark değişkenin sonucudur ve "
                        "yumuşak halkada çizilir, önce düğümü card.soft'a yazın"),
    "edit_same": ("card.change.set: every value already holds in A, so B would equal A",
                  "card.change.set: her değer A'da zaten geçerli, B A'ya eşit olurdu"),
    "soft_type": ("card.soft must be a list of up to {most} node ids (or {{\"id\": .., \"note\": ..}})",
                  "card.soft en çok {most} düğüm kimliğinin listesi olmalı (ya da {{\"id\": .., \"note\": ..}})"),
    "soft_unknown": ("card.soft: no node in card.screen has id \"{id}\"",
                     "card.soft: card.screen içinde \"{id}\" kimlikli düğüm yok"),
    "soft_target": ("card.soft: \"{id}\" is the change's own target; the soft ring marks a consequence, not the variable",
                    "card.soft: \"{id}\" değişikliğin kendi hedefi; yumuşak halka değişkeni değil sonucu işaretler"),
    "both_forms": ("card: both forms are given (variant_a/variant_b and screen/change); a card is drawn from one, "
                   "drop the raw markup or the screen spec",
                   "card: iki biçim birden verilmiş (variant_a/variant_b ve screen/change); kart tek biçimden çizilir, "
                   "ham işaretlemeyi ya da ekran tanımını kaldırın"),
    "no_form": ("card: a card needs either card.variant_a and card.variant_b (raw markup) or card.screen and "
                "card.change (screen spec)",
                "card: kart ya card.variant_a ile card.variant_b (ham işaretleme) ya da card.screen ile card.change "
                "(ekran tanımı) ister"),
    "raw_half": ("card: the raw form needs both card.variant_a and card.variant_b (card.{missing} is missing)",
                 "card: ham biçim card.variant_a ile card.variant_b'yi birlikte ister (card.{missing} eksik)"),
    "soft_without_spec": ("card.soft belongs to the screen spec form; with raw markup write .hl-soft in the markup",
                          "card.soft ekran tanımı biçimine aittir; ham işaretlemede .hl-soft doğrudan yazılır"),
}


# The `want` phrases the messages carry, in Turkish (an English phrase inside a
# Turkish message read as a half-translated tool).
WANT_TR = {
    "a non-empty string": "boş olmayan bir metin",
    "a px integer": "px cinsinden bir tam sayı",
    "#rrggbb": "#rrggbb",
    "\"center\" or \"left\"": "\"center\" ya da \"left\"",
    "a string": "bir metin",
    "true or false": "true ya da false",
    "\"sm\"": "\"sm\"",
    "a list of nodes": "bir düğüm listesi",
    "a list of {\"label\": .., \"on\": bool}": "bir {\"label\": .., \"on\": bool} listesi",
    "a list of {\"label\": .., \"state\": done|on}": "bir {\"label\": .., \"state\": done|on} listesi",
    "an integer 0..100": "0..100 arası bir tam sayı",
    "[left, right]": "[sol, sağ]",
    "a height in px": "px cinsinden bir yükseklik",
    "true": "true",
    "one node": "tek bir düğüm",
    "\"below\" or \"above\"": "\"below\" ya da \"above\"",
    "a short label, two to four words": "iki ila dört kelimelik kısa bir etiket",
    "an object of the properties to change": "değişecek özelliklerin nesnesi",
    "the id of the node the moved node lands next to": "taşınan düğümün yanına ineceği düğümün kimliği",
}


def _m(_key, _lang, **kw):
    en, tr = MSG[_key]
    if _lang == "tr" and isinstance(kw.get("want"), str):
        want = kw["want"]
        if want.startswith("one of "):
            kw["want"] = "şunlardan biri: " + want[len("one of "):]
        else:
            kw["want"] = WANT_TR.get(want, want)
    return (tr if _lang == "tr" else en).format(**kw)


def esc(text):
    """Escaped text; a newline in the producer's text is a line break on the screen."""
    return html.escape(str(text), quote=True).replace("\n", "<br>")


# ------------------------------------------------------------------ the forms

def card_form(card):
    """'raw', 'spec', 'both' or None: which of the two card forms a card dict carries."""
    raw = "variant_a" in card or "variant_b" in card
    spec = "screen" in card or "change" in card
    if raw and spec:
        return "both"
    return "raw" if raw else ("spec" if spec else None)


def form_problems(card, lang="en"):
    """Exactly one of the two forms, and that form whole. [] when fine."""
    if not isinstance(card, dict):
        return []
    form = card_form(card)
    if form == "both":
        return [_m("both_forms", lang)]
    if form is None:
        return [_m("no_form", lang)]
    out = []
    if form == "raw":
        for key in ("variant_a", "variant_b"):
            if key not in card:
                out.append(_m("raw_half", lang, missing=key))
        if "soft" in card:
            out.append(_m("soft_without_spec", lang))
    else:
        if "screen" not in card:
            out.append(_m("screen_missing", lang))
        if "change" not in card:
            out.append(_m("change_missing", lang))
    return out


# ------------------------------------------------------------------ the tree

class _Node(object):
    __slots__ = ("kind", "value", "props", "kids", "raw", "ring", "soft")

    def __init__(self, kind, value, props, kids, raw):
        self.kind, self.value, self.props, self.kids, self.raw = kind, value, props, kids, raw
        self.ring = None   # (label, pos) when this node carries the ring in this arm
        self.soft = None   # (note or "") when this node carries a soft ring

    @property
    def id(self):
        return self.props.get("id")


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _str(v):
    return isinstance(v, str) and v.strip() != ""


def _parse(raw, path, top, lang, problems, ids):
    """One node → _Node (or None after a problem). `ids` maps id → path."""
    if not isinstance(raw, dict):
        problems.append(_m("node_type", lang, path=path, what=type(raw).__name__))
        return None
    kinds = [k for k in raw if k in KINDS]
    if len(kinds) != 1:
        if kinds:
            problems.append(_m("kind_many", lang, path=path, n=len(kinds), keys=", ".join(kinds)))
        else:
            problems.append(_m("kind_unknown", lang, path=path, keys=", ".join(sorted(raw)) or "empty",
                               kinds=", ".join(KINDS)))
        return None
    kind = kinds[0]
    allowed = COMMON_PROPS + EXTRA_PROPS.get(kind, ())
    props = {}
    for key in raw:
        if key == kind:
            continue
        if key not in allowed:
            problems.append(_m("prop_unknown", lang, path=path, key=key, kind=kind))
            continue
        props[key] = raw[key]
    _check_props(kind, props, path, lang, problems)
    node_id = props.get("id")
    if _str(node_id):
        if node_id in ids:
            problems.append(_m("id_dup", lang, path=path, id=node_id, other=ids[node_id]))
        else:
            ids[node_id] = path
    if kind in TOP_ONLY and not top:
        problems.append(_m("top_only", lang, path=path, kind=kind))
    value = raw[kind]
    kids = None
    if not _check_value(kind, value, path, lang, problems):
        return None
    if kind == "row":
        kids = [n for n in (_parse(v, "%s.row[%d]" % (path, i), False, lang, problems, ids)
                            for i, v in enumerate(value)) if n is not None]
    elif kind in ("band", "stack"):
        kids = [n for n in (_parse(v, "%s.%s.items[%d]" % (path, kind, i), False, lang, problems, ids)
                            for i, v in enumerate(value["items"])) if n is not None]
    elif kind == "accordion":
        kids = [n for n in (_parse(v, "%s.accordion.items[%d]" % (path, i), False, lang, problems, ids)
                            for i, v in enumerate(value.get("items") or [])) if n is not None]
    elif kind == "sticky":
        one = _parse(value, "%s.sticky" % path, False, lang, problems, ids)
        kids = [one] if one is not None else []
    return _Node(kind, value, props, kids, raw)


def _want(problems, lang, path, key, cond, want, got):
    if not cond:
        problems.append(_m("prop_value", lang, path=path, key=key, want=want, got=got))


def _check_props(kind, props, path, lang, problems):
    for key, v in props.items():
        if key == "id":
            _want(problems, lang, path, key, _str(v), "a non-empty string", v)
        elif key in ("mb", "radius", "height"):
            _want(problems, lang, path, key, _is_int(v) and v >= 0, "a px integer", v)
        elif key in ("fg", "bg", "border"):
            _want(problems, lang, path, key, isinstance(v, str) and HEX_RE.match(v), "#rrggbb", v)
        elif key == "align":
            _want(problems, lang, path, key, v in ("center", "left"), "\"center\" or \"left\"", v)
        elif key == "label":
            _want(problems, lang, path, key, _str(v), "a non-empty string", v)
        elif key == "value":
            _want(problems, lang, path, key, isinstance(v, str), "a string", v)
        elif key in ("select", "on", "total"):
            _want(problems, lang, path, key, isinstance(v, bool), "true or false", v)
        elif key == "style":
            styles = CTA_STYLES if kind == "cta" else BADGE_STYLES
            _want(problems, lang, path, key, v in styles, "one of " + "/".join(styles), v)
        elif key == "size":
            _want(problems, lang, path, key, v == "sm", "\"sm\"", v)


def _labelled_list(value, state_key, states):
    if not isinstance(value, list) or not value:
        return False
    for it in value:
        if not isinstance(it, dict) or not _str(it.get("label")):
            return False
        if state_key in it and (it[state_key] not in states):
            return False
        if any(k not in ("label", state_key) for k in it):
            return False
    return True


def _check_value(kind, v, path, lang, problems):
    """True when the kind's value has the right shape (problems appended otherwise)."""
    ok, want = True, ""
    if kind in ("h", "sub", "text", "field", "cta", "link", "help", "info", "check", "radio", "badge", "banner"):
        ok, want = _str(v), "a non-empty string"
    elif kind == "header":
        ok, want = _header_ok(v), ("{\"logo\": true|\"Text\", \"nav\": [..], \"tel\": \"..\", \"icons\": [{\"icon\": "
                                   "close|support|menu|search|back, \"label\": \"..\"}], \"line\": false}")
    elif kind == "row":
        ok, want = isinstance(v, list) and len(v) >= 1, "a list of nodes"
    elif kind == "chips":
        ok, want = _labelled_list(v, "on", (True, False)), "a list of {\"label\": .., \"on\": bool}"
    elif kind == "tabs":
        ok, want = _labelled_list(v, "on", (True, False)), "a list of {\"label\": .., \"on\": bool}"
    elif kind == "steps":
        ok, want = _labelled_list(v, "state", STEP_STATES), "a list of {\"label\": .., \"state\": done|on}"
    elif kind == "progress":
        ok, want = _is_int(v) and 0 <= v <= 100, "an integer 0..100"
    elif kind == "line":
        ok, want = isinstance(v, list) and len(v) == 2 and all(isinstance(s, str) for s in v), "[left, right]"
    elif kind == "item":
        ok = isinstance(v, dict) and _str(v.get("name")) and all(k in ("name", "meta", "price") for k in v) \
            and all(isinstance(v[k], str) for k in v)
        want = "{\"name\": .., \"meta\": .., \"price\": ..}"
    elif kind == "plan":
        ok, want = _plan_ok(v), ("{\"name\": .., \"price\": .., \"per\": .., \"featured\": bool, \"badge\": .., "
                                 "\"cta\": .., \"cta_style\": .., \"features\": [..]}")
    elif kind == "img":
        ok, want = _is_int(v) and v > 0, "a height in px"
    elif kind in ("divider", "fold", "stage"):
        ok, want = v is True, "true"
    elif kind == "gap":
        ok, want = _is_int(v) and v > 0, "a height in px"
    elif kind == "band":
        ok = isinstance(v, dict) and isinstance(v.get("items"), list) and len(v["items"]) >= 1 \
            and all(k in ("bg", "items", "pad") for k in v) \
            and ("bg" not in v or (isinstance(v["bg"], str) and HEX_RE.match(v["bg"]))) \
            and ("pad" not in v or (isinstance(v["pad"], list) and len(v["pad"]) == 2
                                    and all(_is_int(p) and p >= 0 for p in v["pad"])))
        want = "{\"bg\": \"#rrggbb\", \"items\": [nodes], \"pad\": [top, bottom]}"
    elif kind == "sticky":
        ok, want = isinstance(v, dict), "one node"
    elif kind == "stack":
        ok = isinstance(v, dict) and isinstance(v.get("items"), list) and len(v["items"]) >= 1 \
            and all(k in ("items", "gap") for k in v) and ("gap" not in v or (_is_int(v["gap"]) and v["gap"] >= 0))
        want = "{\"items\": [nodes], \"gap\": px}"
    elif kind == "accordion":
        ok = isinstance(v, dict) and _str(v.get("title")) and all(k in ("title", "open", "items") for k in v) \
            and ("open" not in v or isinstance(v["open"], bool)) \
            and ("items" not in v or (isinstance(v["items"], list) and len(v["items"]) >= 1)) \
            and (not v.get("open") or bool(v.get("items")))
        want = "{\"title\": .., \"open\": bool, \"items\": [nodes]} (an open accordion needs its items)"
    if not ok:
        problems.append(_m("value", lang, path=path, kind=kind, want=want, got=v))
    return ok


def _header_ok(v):
    if not isinstance(v, dict) or not v:
        return False
    for k, x in v.items():
        if k == "logo":
            if not (x is True or _str(x)):
                return False
        elif k == "nav":
            if not (isinstance(x, list) and x and all(_str(s) for s in x)):
                return False
        elif k == "tel":
            if not _str(x):
                return False
        elif k == "line":
            if not isinstance(x, bool):
                return False
        elif k == "icons":
            if not (isinstance(x, list) and x):
                return False
            for ic in x:
                if not isinstance(ic, dict) or ic.get("icon") not in ICONS:
                    return False
                if any(key not in ("icon", "label", "fg") for key in ic):
                    return False
                if "label" in ic and not _str(ic["label"]):
                    return False
                if "fg" in ic and not (isinstance(ic["fg"], str) and HEX_RE.match(ic["fg"])):
                    return False
        else:
            return False
    return True


def _plan_ok(v):
    if not isinstance(v, dict) or not _str(v.get("name")) or not _str(v.get("price")):
        return False
    for k, x in v.items():
        if k in ("name", "price", "per", "badge", "cta"):
            if not isinstance(x, str):
                return False
        elif k == "featured":
            if not isinstance(x, bool):
                return False
        elif k == "cta_style":
            if x not in CTA_STYLES:
                return False
        elif k == "features":
            if not (isinstance(x, list) and all(isinstance(s, str) for s in x)):
                return False
        else:
            return False
    return True


def _find(root, node_id):
    """(parent, index) of the node with `node_id`, searching containers depth first; None when absent."""
    for i, kid in enumerate(root.kids):
        if kid.id == node_id:
            return root, i
        if kid.kids:
            hit = _find(kid, node_id)
            if hit:
                return hit
    return None


def _ids_of(root, out=None):
    out = {} if out is None else out
    for kid in root.kids:
        if _str(kid.id):
            out[kid.id] = True
        if kid.kids:
            _ids_of(kid, out)
    return out


# ------------------------------------------------------------------ drawing

def _decls(node):
    """The page-colour overrides as CSS declarations, in a fixed order."""
    p = node.props
    out = []
    if "fg" in p:
        out.append("color:%s" % p["fg"].lower())
    if "bg" in p:
        out.append("background:%s" % p["bg"].lower())
    if "border" in p:
        out.append("border-color:%s" % p["border"].lower())
    if "radius" in p:
        out.append("border-radius:%dpx" % p["radius"])
    if "height" in p:
        out.append("min-height:%dpx" % p["height"])
    return out


def _attrs(classes, decls):
    out = ""
    if classes:
        out += ' class="%s"' % " ".join(classes)
    if decls:
        out += ' style="%s"' % ";".join(decls)
    return out


def _icon(ic, lang):
    label = ic.get("label") or ICON_LABELS["tr" if lang == "tr" else "en"][ic["icon"]]
    colour = ic["fg"].lower() if "fg" in ic else "currentColor"
    head = '<span role="img" aria-label="%s" style="' % esc(label)
    kind = ic["icon"]
    if kind == "close":
        return head + 'font-size:22px;line-height:1;color:%s">✕</span>' % colour
    if kind == "support":
        return head + ('display:inline-block;width:22px;height:19px;border:2px solid %s;border-bottom:0;'
                       'border-radius:11px 11px 0 0"></span>' % colour)
    if kind == "menu":
        bar = '<span style="display:block;height:2px;background:%s"></span>' % colour
        return head + 'display:inline-flex;flex-direction:column;gap:4px;width:20px">' + bar * 3 + '</span>'
    if kind == "search":
        return head + ('display:inline-flex;align-items:flex-start;width:22px;height:22px">'
                       '<span style="display:inline-block;width:12px;height:12px;border:2px solid %s;'
                       'border-radius:50%%"></span>'
                       '<span style="display:inline-block;width:8px;height:2px;background:%s;'
                       'transform:rotate(45deg);margin:13px 0 0 -3px"></span></span>' % (colour, colour))
    # back: a chevron drawn with two borders
    return head + ('display:inline-block;width:11px;height:11px;border-left:2px solid %s;border-bottom:2px solid %s;'
                   'transform:rotate(45deg);margin-left:4px"></span>' % (colour, colour))


def _header(node, lang, extra):
    v = node.value
    decls = _decls(node)
    if v.get("line") is False:
        decls.append("border-bottom:0")
    decls += extra
    parts = []
    icons = v.get("icons") or []
    lead = [ic for ic in icons if ic.get("icon") == "back"]  # a back icon leads the bar, as on a real page
    trail = [ic for ic in icons if ic.get("icon") != "back"]
    if lead:
        parts.append('<span style="display:flex;align-items:center;gap:22px">%s</span>'
                     % "".join(_icon(ic, lang) for ic in lead))
    if v.get("logo") is True:
        parts.append('<span class="r-logo"></span>')
    elif _str(v.get("logo")):
        parts.append('<span class="r-logo">%s</span>' % esc(v["logo"]))
    if v.get("nav"):
        parts.append('<span class="r-nav">%s</span>' % "".join("<span>%s</span>" % esc(s) for s in v["nav"]))
    if v.get("tel"):
        parts.append('<span class="r-tel">%s</span>' % esc(v["tel"]))
    if trail:
        push = "" if (v.get("nav") or v.get("tel")) else "margin-left:auto;"
        parts.append('<span style="%sdisplay:flex;align-items:center;gap:22px">%s</span>'
                     % (push, "".join(_icon(ic, lang) for ic in trail)))
    return "<div%s>%s</div>" % (_attrs(["r-header"], decls), "".join(parts))


def _field(node, extra):
    p, v = node.props, node.value
    classes = ["r-field"]
    if "value" not in p:
        classes.append("empty")
    if p.get("select"):
        classes.append("select")
    shown = p["value"] if "value" in p else v
    field = "<div%s>%s</div>" % (_attrs(classes, _decls(node) + ([] if "label" in p else extra)), esc(shown))
    if "label" in p:
        return "<div%s><div class=\"r-label\">%s</div>%s</div>" % (_attrs([], extra), esc(p["label"]), field)
    return field


def _plan(node, extra):
    v = node.value
    classes = ["r-plan"] + (["featured"] if v.get("featured") else [])
    body = []
    if v.get("badge"):
        body.append('<div><span class="r-badge brand">%s</span></div>' % esc(v["badge"]))
    body.append('<div class="r-plan-name">%s</div>' % esc(v["name"]))
    per = '<span class="r-per">%s</span>' % esc(v["per"]) if v.get("per") else ""
    body.append('<div class="r-plan-price">%s%s</div>' % (esc(v["price"]), per))
    if v.get("features"):
        body.append('<ul class="r-plan-feat">%s</ul>' % "".join("<li>%s</li>" % esc(f) for f in v["features"]))
    if v.get("cta"):
        cta_classes = ["r-cta"] + ([v["cta_style"]] if v.get("cta_style") in ("outline", "ghost") else [])
        body.append('<div class="%s">%s</div>' % (" ".join(cta_classes), esc(v["cta"])))
    return "<div%s>%s</div>" % (_attrs(classes, _decls(node) + extra), "".join(body))


def _element(node, lang, extra, top):
    """The node's own markup; `extra` are the margin declarations of its outer element."""
    k, v, p = node.kind, node.value, node.props
    d = _decls(node)
    if k == "header":
        return _header(node, lang, extra)
    if k in ("h", "sub", "link", "help", "info", "banner"):
        return "<div%s>%s</div>" % (_attrs(["r-" + k], d + extra), esc(v))
    if k == "text":
        align = ["text-align:center"] if p.get("align") == "center" else []
        return "<div%s>%s</div>" % (_attrs([], align + d + extra), esc(v))
    if k == "field":
        return _field(node, extra)
    if k == "row":
        return "<div%s>%s</div>" % (_attrs(["r-row"], d + extra), "".join(_render(kid, [], lang, False)
                                                                         for kid in node.kids))
    if k == "cta":
        classes = ["r-cta"]
        if p.get("style") in ("outline", "ghost"):
            classes.append(p["style"])
        if p.get("size") == "sm":
            classes.append("sm")
        return "<div%s>%s</div>" % (_attrs(classes, d + extra), esc(v))
    if k in ("check", "radio"):
        return "<div%s>%s</div>" % (_attrs(["r-" + k] + (["on"] if p.get("on") else []), d + extra), esc(v))
    if k == "chips":
        chips = "".join('<span class="%s">%s</span>' % ("r-chip on" if c.get("on") else "r-chip", esc(c["label"]))
                        for c in v)
        return "<div%s>%s</div>" % (_attrs(["r-chips"], d + extra), chips)
    if k == "tabs":
        tabs = "".join(('<span class="on">%s</span>' if t.get("on") else "<span>%s</span>") % esc(t["label"])
                       for t in v)
        return "<div%s>%s</div>" % (_attrs(["r-tabs"], d + extra), tabs)
    if k == "steps":
        steps = "".join(('<span class="%s">%s</span>' % (s["state"], esc(s["label"]))) if s.get("state")
                        else "<span>%s</span>" % esc(s["label"]) for s in v)
        return "<div%s>%s</div>" % (_attrs(["r-steps"], d + extra), steps)
    if k == "progress":
        return '<div%s><i style="width:%d%%"></i></div>' % (_attrs(["r-progress"], d + extra), v)
    if k == "line":
        classes = ["r-line"] + (["total"] if p.get("total") else [])
        return "<div%s><span>%s</span><span>%s</span></div>" % (_attrs(classes, d + extra), esc(v[0]), esc(v[1]))
    if k == "item":
        body = '<div class="r-name">%s</div>' % esc(v["name"])
        if v.get("meta"):
            body += '<div class="r-meta">%s</div>' % esc(v["meta"])
        price = '<div class="r-price">%s</div>' % esc(v["price"]) if v.get("price") else ""
        return ('<div%s><div class="ph img r-thumb"></div><div class="r-item-body">%s</div>%s</div>'
                % (_attrs(["r-item"], d + extra), body, price))
    if k == "plan":
        return _plan(node, extra)
    if k == "badge":
        classes = ["r-badge"] + ([p["style"]] if p.get("style") else [])
        return "<div%s><span%s>%s</span></div>" % (_attrs([], extra), _attrs(classes, d), esc(v))
    if k == "img":
        return "<div%s></div>" % _attrs(["ph", "img"], ["height:%dpx" % v] + d + extra)
    if k == "divider":
        return "<div%s></div>" % _attrs(["r-divider"], d + extra)
    if k == "gap":
        return "<div%s></div>" % _attrs([], ["height:%dpx" % v] + extra)
    if k == "fold":
        return '<div class="r-fold"></div>'
    if k == "stage":
        return '<div class="r-stage-break"></div>'
    if k == "sticky":
        return '<div class="r-sticky">%s</div>' % "".join(_render(kid, [], lang, False) for kid in node.kids)
    if k == "band":
        pad = v.get("pad")
        padding = "padding:%dpx %dpx %dpx" % (pad[0], BLEED, pad[1]) if pad else "padding:%dpx" % BLEED
        decls = ["margin:0 -%dpx" % BLEED, padding]
        if "bg" in v:
            decls.append("background:%s" % v["bg"].lower())
        decls += d
        return "<div%s>\n%s\n</div>" % (_attrs([], decls + extra), _children(node.kids, GAP, lang, False))
    if k == "accordion":
        is_open = bool(v.get("open"))
        # Drawn with inline style, the same in both arms (a template class would
        # change every shipped card's bytes): a header row with its +/- state,
        # and the body only when open.
        head = ('<div role="button" aria-expanded="%s" style="%s"><span>%s</span>'
                '<span style="%s">%s</span></div>'
                % ("true" if is_open else "false", ACC_HEAD_STYLE, esc(v["title"]), ACC_SIGN_STYLE,
                   ACC_OPEN_SIGN if is_open else ACC_CLOSED_SIGN))
        body = ""
        if is_open and node.kids:
            body = '<div style="%s">\n%s\n</div>' % (ACC_BODY_STYLE, _children(node.kids, GAP, lang, False))
        return "<div%s>%s%s</div>" % (_attrs([], [ACC_BOX_STYLE] + d + extra), head, body)
    if k == "stack":
        gap = v.get("gap", GAP)
        return "<div%s>\n%s\n</div>" % (_attrs([], ["display:flex", "flex-direction:column"] + d + extra),
                                        _children(node.kids, gap, lang, False))
    raise ValueError(k)  # pragma: no cover - every kind in KINDS is drawn above


def _render(node, margins, lang, top):
    """One node with its margin declarations, inside its soft/ring wrappers.

    A ringed node's non-negative margins (its rhythm and its label's room) sit
    on the ring element, so the ring hugs the content and the label lies in
    the room between the ring and its neighbour. A negative margin (a band's
    bleed) stays on the node: the ring itself never pulls."""
    outer = []
    if node.ring:
        outer = [m for m in margins if not m.split(":", 1)[1].lstrip().startswith("-")]
        margins = [m for m in margins if m not in outer]
    out = _element(node, lang, margins, top)
    if node.ring:
        label, pos = node.ring
        pos_attr = ' data-pos="%s"' % pos if pos else ""
        style = ' style="%s"' % ";".join(outer) if outer else ""
        out = '<div class="hl" data-note="%s"%s%s>%s</div>' % (esc(label), pos_attr, style, out)
    if node.soft is not None:
        note = ' data-note="%s"' % esc(node.soft) if node.soft else ""
        out = '<div class="hl-soft"%s>%s</div>' % (note, out)
    return out


def _margins(node, gap, last, top):
    """The spacing declarations of a child: the rhythm (or its "mb") to the next
    sibling, plus the room a ring label placed below or above it needs. At the
    top level the template's own gap already separates siblings, so only the
    difference is written.

    _render moves these declarations onto the ring element when the node is
    ringed, so the room lies outside the ring (card_problems allows a
    non-negative margin-top or margin-bottom on a ring). On a neighbour it
    would change A, which must stay byte-identical across records that share
    a screen."""
    wanted = node.props.get("mb", gap) if not last else 0
    mt = 0
    if node.ring:
        pos = node.ring[1]
        if pos == "below":
            wanted = max(wanted, LABEL_ROOM)
        elif pos == "above":
            mt = LABEL_ROOM
    if top:
        wanted = wanted - GAP if wanted else 0
        mt = mt - GAP if mt else 0
    elif last:
        wanted = wanted if node.ring and node.ring[1] == "below" else 0
    out = []
    if mt:
        out.append("margin-top:%dpx" % mt)
    if wanted:
        out.append("margin-bottom:%dpx" % wanted)
    return out


def _children(kids, gap, lang, top):
    lines = []
    for i, kid in enumerate(kids):
        if kid.kind in ("fold", "stage"):
            lines.append(_render(kid, [], lang, top))
            continue
        margins = _margins(kid, gap, i == len(kids) - 1, top)
        if top and kid.kind == "band":
            # A band is full-bleed: one that opens or closes the screen also covers the screen's own
            # top or bottom padding, so the grey region reaches the frame's edge like the real page.
            if i == 0:
                margins = ["margin-top:-%dpx" % BLEED_TOP] + margins
            if i == len(kids) - 1:
                margins = margins + ["margin-bottom:-%dpx" % BLEED]
        lines.append(_render(kid, margins, lang, top))
    return "\n".join(lines)


# ------------------------------------------------------------------ the change

def _change_keys(op):
    base = ("op", "target", "linked")
    if op in ("insert_after", "insert_before"):
        return base + ("node", "label", "label_pos")
    if op == "replace":
        return base + ("node", "label", "label_a", "label_pos")
    if op == "remove":
        return base + ("label", "label_pos")
    if op in ("move_after", "move_before"):
        return base + ("to", "label_a", "label_b", "label_pos")
    return base + ("set", "label", "label_a", "label_pos")


def _apply_edit(node, settings, lang, problems):
    """The edited node's raw dict after `set`, or None."""
    raw = copy.deepcopy(node.raw)
    kind = node.kind
    allowed = COMMON_PROPS + EXTRA_PROPS.get(kind, ())
    changed = False
    if kind in CONTAINERS:
        # A container's colour or content reaches every element inside it: one edit would
        # change several texts at once. Only the container's own box may be edited.
        editable = ACCORDION_EDITABLE if kind == "accordion" else CONTAINER_EDITABLE
        bad = [key for key in settings if key not in editable]
        if bad:
            problems.append(_m("edit_container", lang, kind=kind, key=bad[0]))
            return None
    for key, val in settings.items():
        if key in PX_PROPS and _is_int(val):
            old = raw.get(key, GAP if key == "mb" else None)
            if old is not None and _is_int(old) and val != old and abs(val - old) < MIN_PX_CHANGE:
                problems.append(_m("px_small", lang, key=key, old=old, new=val, d=abs(val - old), min=MIN_PX_CHANGE))
                return None
        if key == kind or (key == "text" and isinstance(raw[kind], (str, int, bool, list))):
            if raw[kind] != val:
                changed = True
            raw[kind] = val
        elif key in allowed and key != "id":
            if raw.get(key) != val:
                changed = True
            raw[key] = val
        elif isinstance(raw[kind], dict):
            if raw[kind].get(key) != val:
                changed = True
            raw[kind][key] = val
        else:
            problems.append(_m("edit_key", lang, key=key, kind=kind))
            return None
    if not changed:
        problems.append(_m("edit_same", lang))
        return None
    return raw


def _apply(root_a, root_b, change, lang, problems):
    """Place the one change: mutate B (and ring A where the op wants it)."""
    if not isinstance(change, dict):
        problems.append(_m("change_type", lang))
        return
    op = change.get("op")
    if op not in OPS:
        problems.append(_m("op_unknown", lang, ops="/".join(OPS), got=op))
        return
    for key in change:
        if key not in _change_keys(op):
            problems.append(_m("change_extra", lang, key=key, op=op))
    target = change.get("target")
    if not _str(target):
        problems.append(_m("target_missing", lang))
        return
    hit_a, hit_b = _find(root_a, target), _find(root_b, target)
    if hit_a is None or hit_b is None:
        problems.append(_m("target_unknown", lang, key="target", id=target))
        return
    parent_a, ia = hit_a
    parent_b, ib = hit_b
    pos = change.get("label_pos")
    if pos is not None and pos not in LABEL_POSITIONS:
        problems.append(_m("change_key", lang, key="label_pos", want="\"below\" or \"above\""))
        pos = None

    def label(key):
        v = change.get(key)
        if not _str(v):
            problems.append(_m("change_key", lang, key=key, want="a short label, two to four words"))
            return None
        return v.strip()

    if op in ("insert_after", "insert_before", "replace"):
        note = label("label")
        ids = _ids_of(root_b)
        if op == "replace":
            ids.pop(target, None)
        new = _parse(change.get("node"), "card.change.node", parent_b is root_b, lang, problems, ids)
        if new is None or note is None:
            return
        new.ring = (note, pos)
        if op == "insert_after":
            parent_b.kids.insert(ib + 1, new)
        elif op == "insert_before":
            parent_b.kids.insert(ib, new)
        else:
            parent_b.kids[ib] = new
            if _str(change.get("label_a")):
                parent_a.kids[ia].ring = (change["label_a"].strip(), pos)
    elif op == "remove":
        note = label("label")
        if note is None:
            return
        parent_a.kids[ia].ring = (note, pos)
        del parent_b.kids[ib]
    elif op in ("move_after", "move_before"):
        note_a, note_b = label("label_a"), label("label_b")
        to = change.get("to")
        if not _str(to):
            problems.append(_m("change_key", lang, key="to", want="the id of the node the moved node lands next to"))
            return
        if to == target:
            problems.append(_m("move_self", lang))
            return
        if note_a is None or note_b is None:
            return
        moved = parent_b.kids.pop(ib)
        dest = _find(root_b, to)
        if dest is None:
            problems.append(_m("target_unknown", lang, key="to", id=to))
            return
        dest_parent, idx = dest
        if moved.kind in TOP_ONLY and dest_parent is not root_b:
            problems.append(_m("move_top_only", lang, kind=moved.kind, parent=dest_parent.kind))
            return
        dest_parent.kids.insert(idx + 1 if op == "move_after" else idx, moved)
        moved.ring = (note_b, pos)
        parent_a.kids[ia].ring = (note_a, pos)
    else:  # edit
        note = label("label")
        settings = change.get("set")
        if not isinstance(settings, dict) or not settings:
            problems.append(_m("change_key", lang, key="set", want="an object of the properties to change"))
            return
        raw = _apply_edit(parent_b.kids[ib], settings, lang, problems)
        if raw is None or note is None:
            return
        ids = _ids_of(root_b)
        ids.pop(target, None)
        new = _parse(raw, "card.change.set", parent_b is root_b, lang, problems, ids)
        if new is None:
            return
        new.ring = (note, pos)
        parent_b.kids[ib] = new
        if _str(change.get("label_a")):
            parent_a.kids[ia].ring = (change["label_a"].strip(), pos)


def _apply_soft(roots, soft, target, lang, problems):
    if soft is None:
        return
    if not isinstance(soft, list) or len(soft) > MAX_SOFT:
        problems.append(_m("soft_type", lang, most=MAX_SOFT))
        return
    for entry in soft:
        if isinstance(entry, str):
            node_id, note = entry, ""
        elif isinstance(entry, dict) and _str(entry.get("id")) and all(k in ("id", "note") for k in entry) \
                and isinstance(entry.get("note", ""), str):
            node_id, note = entry["id"], entry.get("note", "")
        else:
            problems.append(_m("soft_type", lang, most=MAX_SOFT))
            return
        if node_id == target:
            problems.append(_m("soft_target", lang, id=node_id))
            continue
        for root in roots:
            hit = _find(root, node_id)
            if hit is None:
                if root is roots[0]:
                    problems.append(_m("soft_unknown", lang, id=node_id))
                continue
            parent, i = hit
            parent.kids[i].soft = note.strip()


def compile(screen, change, lang="en", soft=None):
    """(variant_a_html, variant_b_html, problems). The two bodies are "" when
    there is any problem: nothing half-drawn leaves the compiler."""
    lang = "tr" if lang == "tr" else "en"
    problems = []
    if not isinstance(screen, list) or not screen:
        problems.append(_m("screen_type", lang))
        return "", "", problems
    ids = {}
    kids = [n for n in (_parse(raw, "card.screen[%d]" % i, True, lang, problems, ids)
                        for i, raw in enumerate(screen)) if n is not None]
    if problems:
        return "", "", problems
    root_a = _Node("#root", None, {}, kids, None)
    root_b = copy.deepcopy(root_a)
    if change is None:
        problems.append(_m("change_missing", lang))
        return "", "", problems
    _apply(root_a, root_b, change, lang, problems)
    target = change.get("target") if isinstance(change, dict) else None
    _apply_soft((root_a, root_b), soft, target, lang, problems)
    if not problems:
        _apply_linked(root_b, change, soft, lang, problems)
    if not problems:
        _empty_containers((root_a, root_b), change.get("op"), lang, problems)
    if problems:
        return "", "", problems
    if _bare(root_a, lang) == _bare(root_b, lang):
        why = {"replace": "why_replace", "move_after": "why_move", "move_before": "why_move",
               "edit": "why_edit"}.get(change.get("op"), "why_generic")
        return "", "", [_m("no_difference", lang, why=_m(why, lang))]
    return _children(root_a.kids, GAP, lang, True), _children(root_b.kids, GAP, lang, True), []


def _bare(root, lang):
    """The arm drawn without its rings (and so without the label room): what a reader compares."""
    bare = copy.deepcopy(root)

    def strip(node):
        for kid in node.kids:
            kid.ring, kid.soft = None, None
            if kid.kids:
                strip(kid)
    strip(bare)
    return _children(bare.kids, GAP, lang, True)


def _empty_containers(roots, op, lang, problems):
    """A remove or move that takes a row's (band's, stack's) last child leaves a
    container that draws nothing; refused rather than drawn."""
    for arm, root in zip(("A", "B"), roots):
        def visit(node, where):
            for i, kid in enumerate(node.kids):
                here = "%s[%d]" % (where, i)
                drawn = kid.kind != "accordion" or bool(kid.value.get("open"))  # a closed one hides its body
                if kid.kind in CONTAINERS and kid.kind != "sticky" and drawn and not kid.kids:
                    problems.append(_m("empty_container", lang, op=op, kind=kid.kind, where=here, arm=arm))
                if kid.kids:
                    visit(kid, here)
        visit(root, "card.screen")


def _apply_linked(root_b, change, soft, lang, problems):
    """card.change.linked: the variable's linked consequences, each an edit of a
    node named in card.soft, applied in B only (an annual-default toggle and
    the prices it switches). The soft ring stays around the node in both arms.
    An edit or replace with linked consequences rings A's element too
    (label_a): each arm then reads ring, then consequence, and the A/B diff
    sees the two regions side by side."""
    linked = change.get("linked")
    if linked is None:
        return
    if change.get("op") in ("edit", "replace") and not _str(change.get("label_a")):
        problems.append(_m("linked_label_a", lang))
        return
    soft_ids = set()
    for entry in soft or []:
        soft_ids.add(entry if isinstance(entry, str) else entry.get("id") if isinstance(entry, dict) else None)
    if not isinstance(linked, list) or not linked:
        problems.append(_m("linked_type", lang))
        return
    for item in linked:
        if not isinstance(item, dict) or set(item) != {"target", "set"} or not _str(item.get("target")) \
                or not isinstance(item.get("set"), dict) or not item["set"]:
            problems.append(_m("linked_type", lang))
            return
        target = item["target"]
        if target not in soft_ids:
            problems.append(_m("linked_not_soft", lang, id=target))
            continue
        hit = _find(root_b, target)
        if hit is None:
            problems.append(_m("target_unknown", lang, key="linked", id=target))
            continue
        parent, i = hit
        old = parent.kids[i]
        raw = _apply_edit(old, item["set"], lang, problems)
        if raw is None:
            continue
        ids = _ids_of(root_b)
        ids.pop(target, None)
        new = _parse(raw, "card.change.linked", parent is root_b, lang, problems, ids)
        if new is None:
            continue
        new.soft = old.soft
        parent.kids[i] = new


def compile_card(card, lang="en"):
    """compile() from a card dict: (variant_a, variant_b, problems); the form
    problems (both forms, a half form) come first."""
    problems = form_problems(card, lang)
    if problems or card_form(card) != "spec":
        return "", "", problems
    return compile(card.get("screen"), card.get("change"), lang, card.get("soft"))
