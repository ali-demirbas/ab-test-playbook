#!/usr/bin/env python3
"""render_check.mjs için testler. Bağımlılıksız (unittest).

Ölçüm Playwright ister ve bu paketin bağımlılığı değildir. Burada tarayıcı
gerektirmeyen her şey sabitlenir: betik sözdizimi, seçenek ayrıştırma ve
kullanım hataları, renk ve kontrast hesabı, ve ölçümleri hata ile uyarıya
çeviren judge() kuralları ile mesaj biçimi (sentetik ölçümlerle, node
üzerinden; her mesaj varyantı/öğeyi ve ölçüyü adlandırır). Node yoksa atlanır.

Sözleşme 7'nin geometrik kuralları (hap eşitliği, halka genişliği, sabit çubuk,
kısa ekran, aşamalar, devam sayfası) ayrıca tests/fixtures/render_check/ altındaki
elle yazılmış kartlarla gerçek Chromium'da ölçülür: her kural için bir hatalı ve
bir temiz kart. Playwright (NODE_PATH) ya da tarayıcı yoksa bu sınıf atlanır.
"""
import json
import os
import pathlib
import shutil
import tempfile
import subprocess
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "render_check.mjs")
NODE = shutil.which("node")
FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "render_check")

with open(SCRIPT, encoding="utf-8") as _fh:
    SOURCE = _fh.read()

WHITE, INK, RING = [255, 255, 255, 1], [17, 24, 39, 1], [225, 29, 72, 1]


def call(fn, *args):
    """Call an exported function of render_check.mjs with JSON arguments; return its JSON result."""
    js = ("import * as rc from %s;\n"
          "let raw = ''; process.stdin.on('data', (d) => (raw += d));\n"
          "process.stdin.on('end', () => process.stdout.write(JSON.stringify(rc[%s](...JSON.parse(raw)))));\n"
          % (json.dumps(pathlib.Path(SCRIPT).resolve().as_uri()), json.dumps(fn)))
    p = subprocess.run([NODE, "--input-type=module", "-e", js], input=json.dumps(list(args)),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise AssertionError(p.stderr)
    return json.loads(p.stdout)


def variant(name):
    """One frame of a clean coupon card, as collect() measures it (phone-web, 420 × 447)."""
    x = 202 if name == "A" else 978
    y, w, h = 282, 420, 447
    return {
        "name": name,
        "column": {"x": x - 154, "y": 200, "w": 728, "h": 755},
        "frame": {"x": x, "y": y, "w": w, "h": h, "r": x + w, "b": y + h, "kind": "phone-web",
                  "innerBottom": y + h - 1, "scrollH": h - 2, "clientH": h - 2},
        "screen": {"x": x + 1, "y": y + 90, "w": w - 2, "h": h - 92, "r": x + w - 1, "b": y + h - 1,
                   "scrollH": h - 92, "clientH": h - 92, "scrollW": w - 2, "clientW": w - 2},
        "widest": None,
        "lowest": {"y": y + h - 21, "what": "“Ödemeye geç”"},
        "texts": [{"what": "“890 TL”", "px": 15, "weight": 600, "fg": INK, "layers": [[WHITE]], "dimmed": False}],
        "items": [{"what": "“890 TL”", "rects": [{"x": x + 348, "y": y + 148, "r": x + 399, "b": y + 166}], "skip": []},
                  {"what": "“Kupon kodunuz”", "rects": [{"x": x + 21, "y": y + 205, "r": x + 120, "b": y + 222}],
                   "skip": [0]}],
        "rings": [{"note": "kupon alanı açık", "grow": 7, "nested": [],
                   "outline": {"x": x + 14, "y": y + 191, "r": x + 406, "b": y + 285},
                   "label": {"rect": {"x": x + 299, "y": y + 174, "r": x + 406, "b": y + 194}, "pos": "above",
                             "px": 12.5, "fg": WHITE, "bg": RING}}],
    }


def card():
    return {
        "device": "phone-web",
        "card": {"x": 0, "y": 0, "w": 1600, "h": 900, "scrollW": 1600, "scrollH": 900, "clientW": 1600, "clientH": 900},
        "page": {"w": 1600, "h": 900},
        "title": {"h": 37.5, "lineHeight": 37.5, "text": "Kupon alanını … mı?"},
        "stage": {"w": 1504, "h": 755},
        "variants": [variant("A"), variant("B")],
    }


@unittest.skipUnless(NODE, "node not found")
class TestCli(unittest.TestCase):
    def test_syntax(self):
        self.assertEqual(subprocess.run([NODE, "--check", SCRIPT], capture_output=True).returncode, 0)

    def test_unknown_option_is_refused_before_anything_runs(self):
        p = subprocess.run([NODE, SCRIPT, "--shots", "card.html"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("--shots", p.stderr)
        self.assertIn("usage:", p.stderr)

    def test_no_file_is_a_usage_error(self):
        self.assertEqual(subprocess.run([NODE, SCRIPT, "--json"], capture_output=True).returncode, 2)

    def test_a_missing_card_is_named_before_the_browser_starts(self):
        # No Playwright needed to say so: the file check runs first.
        p = subprocess.run([NODE, SCRIPT, "--strict", "no-such-card.html"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("no such file: no-such-card.html", p.stderr)

    def test_importing_it_does_not_run_it(self):
        self.assertEqual(call("parseArgs", ["a.html"])["files"], ["a.html"])


@unittest.skipUnless(NODE, "node not found")
class TestOptions(unittest.TestCase):
    def test_flags(self):
        self.assertEqual(call("parseArgs", ["--shot", "--strict", "a.html", "b.html"]),
                         {"shot": True, "json": False, "strict": True, "files": ["a.html", "b.html"]})
        self.assertEqual(call("parseArgs", ["--json", "a.html"])["json"], True)
        self.assertEqual(call("parseArgs", ["--half", "a.html"])["half"], True)

    def test_unknown_flag_and_no_file(self):
        self.assertEqual(call("parseArgs", ["--shots", "a.html"]), {"error": "unknown option --shots"})
        self.assertEqual(call("parseArgs", ["--strict"]), {"error": "no card given"})

    def test_strict_turns_warnings_into_a_failure(self):
        self.assertFalse(call("failed", {"errors": [], "warnings": ["w"]}, False))
        self.assertTrue(call("failed", {"errors": [], "warnings": ["w"]}, True))
        self.assertTrue(call("failed", {"errors": ["e"], "warnings": []}, False))
        self.assertFalse(call("failed", {"errors": [], "warnings": []}, True))


@unittest.skipUnless(NODE, "node not found")
class TestColour(unittest.TestCase):
    def test_contrast_ratio(self):
        self.assertAlmostEqual(call("contrastRatio", [0, 0, 0, 1], WHITE), 21.0, places=2)
        self.assertAlmostEqual(call("contrastRatio", [107, 114, 128, 1], WHITE), 4.83, places=2)  # muted #6b7280
        self.assertGreaterEqual(call("contrastRatio", WHITE, RING), 4.5)  # the ring label

    def test_alpha_is_composited(self):
        self.assertEqual(call("over", [0, 0, 0, 0.5], WHITE), [127.5, 127.5, 127.5, 1])

    def test_every_gradient_stop_is_a_background(self):
        bgs = call("backgrounds", [[[31, 41, 55, 1], [55, 65, 81, 1]]])
        self.assertEqual([b[:3] for b in bgs], [[31, 41, 55], [55, 65, 81]])
        self.assertEqual(call("backgrounds", []), [WHITE])


@unittest.skipUnless(NODE, "node not found")
class TestJudge(unittest.TestCase):
    """judge(): each rule fires on its own measurement and its message names the element and the number."""

    def judge(self, m):
        return call("judge", m)

    def errors(self, m):
        return self.judge(m)["errors"]

    def assertOne(self, m, *fragments):
        errs = self.errors(m)
        self.assertEqual(len(errs), 1, errs)
        for fragment in fragments:
            self.assertIn(fragment, errs[0])

    def test_a_clean_card_passes(self):
        self.assertEqual(self.judge(card()), {"errors": [], "warnings": []})

    def test_card_size(self):
        m = card()
        m["card"]["h"] = 880
        self.assertOne(m, "card is 1600×880px; it must be exactly 1600×900px")

    def test_page_and_card_overflow(self):
        m = card()
        m["page"]["w"] = 1650
        self.assertOne(m, "page is 1650×900px")
        m = card()
        m["card"]["scrollH"] = 960
        self.assertOne(m, "card content overflows the card: 1600×960px of content in 1600×900px")

    def test_title_lines(self):
        m = card()
        m["title"]["h"] = 112.5
        self.assertOne(m, "title wraps to 3 lines (113px at 37.5px line height); at most 2")
        m["title"]["h"] = 75
        self.assertEqual(self.errors(m), [])

    def test_clipped_screen(self):
        m = card()
        m["variants"][1]["screen"]["scrollH"] = 700
        self.assertOne(m, "variant B: screen content is clipped: 700px of content in a 355px screen (345px cut off")

    def test_sideways_overflow_names_the_element(self):
        m = card()
        m["variants"][0]["widest"] = {"px": 18, "what": "“Çok uzun ürün adı”"}
        self.assertOne(m, "variant A: content overflows the screen sideways by 18px (“Çok uzun ürün adı”)")

    def test_scaled_screen_padding_is_not_blank(self):
        # zoom:1.2 on the phone renders the screen's 20px bottom padding as 24px: designed space, not blank.
        m = card()
        for v in m["variants"]:
            v["frame"]["padB"] = 24
            v["lowest"] = {"y": v["frame"]["innerBottom"] - 24, "what": "“Ödemeye geç”", "inScreen": True}
        self.assertEqual(self.errors(m), [])

    def test_blank_beyond_scaled_padding_is_still_an_error(self):
        m = card()
        v = m["variants"][0]
        v["frame"]["padB"] = 24
        v["lowest"] = {"y": v["frame"]["innerBottom"] - 74, "what": "“Ödemeye geç”", "inScreen": True}
        self.assertOne(m, "variant A: 50px of blank screen under the last element (“Ödemeye geç”); at most 24px")

    def test_blank_phone_screen(self):
        m = card()
        m["variants"][0]["lowest"]["y"] -= 100
        self.assertOne(m, "variant A: 120px of blank screen under the last element (“Ödemeye geç”); at most 24px")
        m["variants"][0]["frame"]["kind"] = "web"  # a browser frame has no such rule
        self.assertEqual(self.errors(m), [])

    def test_label_covering_an_element(self):
        m = card()
        m["variants"][0]["items"][0]["rects"][0]["b"] += 20  # “890 TL” now reaches into the label
        self.assertOne(m, "variant A ring “kupon alanı açık”: label covers", "of “890 TL”", 'try data-pos="below"')

    def test_label_touching_an_element(self):
        m = card()
        m["variants"][0]["items"][0]["rects"][0]["b"] += 5  # “890 TL” ends 3px above the label: not covered, touching
        self.assertOne(m, "variant A ring “kupon alanı açık”: label sits 3px from “890 TL”; leave at least 6px")
        m = card()
        m["variants"][0]["items"][0]["rects"][0]["b"] += 2  # 6px: enough room
        self.assertEqual(self.errors(m), [])

    def test_label_in_a_rounded_corner_is_cut(self):
        m = card()
        v = m["variants"][0]
        f = v["frame"]
        f["radius"] = 43
        lab = v["rings"][0]["label"]
        lab["rect"] = {"x": f["r"] - 60, "y": f["b"] - 22, "r": f["r"] - 4, "b": f["b"] - 4}  # bottom-right corner
        self.assertTrue(any("rounded corner" in e for e in self.errors(m)), self.errors(m))
        m = card()
        m["variants"][0]["frame"]["radius"] = 43  # the default label sits well away from the corners
        self.assertEqual(self.errors(m), [])
        # Near the right edge but above the corner's curve (a ring on a pinned bottom button): not clipped.
        m = card()
        v = m["variants"][0]
        f = v["frame"]
        f["radius"] = 43
        v["rings"][0]["label"]["rect"] = {"x": f["r"] - 155, "y": f["b"] - 100, "r": f["r"] - 16, "b": f["b"] - 82}
        self.assertFalse(any("rounded corner" in e for e in self.errors(m)), self.errors(m))

    def test_ring_covering_an_element(self):
        m = card()
        v = m["variants"][1]
        v["items"].append({"what": "“Sonra”", "rects": [{"x": 1380, "y": 500, "r": 1440, "b": 540}], "skip": []})
        self.assertOne(m, "variant B ring “kupon alanı açık”: ring covers screen elements:", "of “Sonra” lies under the ring",
                       "outline 7px outside the element")

    def test_elements_inside_the_ring_are_not_covered(self):
        m = card()
        m["variants"][0]["items"][1]["rects"][0]["y"] = 200  # inside the ring, under its label: skipped
        self.assertEqual(self.errors(m), [])

    def test_ring_and_label_cut_off_by_the_screen_edge(self):
        m = card()
        ring = m["variants"][0]["rings"][0]
        ring["label"]["rect"]["y"] = m["variants"][0]["screen"]["y"] - 11
        self.assertIn("variant A ring “kupon alanı açık”: label is cut off by the screen edge (11px outside the screen)",
                      self.errors(m)[0])
        m = card()
        m["variants"][0]["rings"][0]["outline"]["r"] = m["variants"][0]["screen"]["r"] + 5
        self.assertIn("the ring is cut off by the screen edge (5px outside the screen)", self.errors(m)[0])

    def test_small_text_is_counted_once(self):
        m = card()
        small = {"what": "“Dipnot”", "px": 10, "weight": 400, "fg": INK, "layers": [[WHITE]], "dimmed": False}
        m["variants"][0]["texts"] += [small, dict(small, what="“İkinci”")]
        self.assertOne(m, "variant A: text “Dipnot” is 10px, below 12px (2 text nodes at this size)")

    def test_low_contrast_names_the_colours(self):
        m = card()
        m["variants"][1]["texts"].append({"what": "“Soluk”", "px": 13, "weight": 400, "fg": [199, 203, 209, 1],
                                          "layers": [[WHITE]], "dimmed": False})
        self.assertOne(m, "variant B: text “Soluk” has contrast 1.63:1 (#c7cbd1 on #ffffff, 13px) below 4.5:1")

    def test_large_text_needs_3_to_1(self):
        grey = [140, 140, 140, 1]  # 3.4:1 on white
        m = card()
        m["variants"][0]["texts"].append({"what": "“Büyük”", "px": 24, "weight": 400, "fg": grey, "layers": [[WHITE]],
                                          "dimmed": False})
        self.assertEqual(self.errors(m), [])
        m["variants"][0]["texts"][-1]["px"] = 16
        self.assertOne(m, "below 4.5:1")

    def test_text_on_a_gradient_is_checked_against_its_worst_stop(self):
        m = card()
        m["variants"][0]["texts"].append({"what": "“Hero”", "px": 13, "weight": 400, "fg": [255, 255, 255, 0.88],
                                          "layers": [[[31, 41, 55, 1], [200, 200, 200, 1]]], "dimmed": False})
        self.assertOne(m, "“Hero” has contrast", "on #c8c8c8")

    def test_dimmed_text_under_an_overlay_is_not_a_contrast_error(self):
        m = card()
        m["variants"][0]["texts"].append({"what": "“Arkada”", "px": 13, "weight": 400, "fg": [199, 203, 209, 1],
                                          "layers": [[WHITE]], "dimmed": True})
        self.assertEqual(self.errors(m), [])

    def test_frames_are_top_aligned_and_equally_wide(self):
        m = card()
        m["variants"][1]["frame"]["y"] += 12
        self.assertOne(m, "frames are not top-aligned: A starts at y=282, B at y=294 (12px apart)")
        m = card()
        m["variants"][1]["frame"]["w"] = 400
        self.assertOne(m, "frames differ in width: A is 420px, B is 400px")

    def test_balance_is_a_warning(self):
        m = card()
        for v in m["variants"]:
            v["frame"]["h"] = 280
        result = self.judge(m)
        self.assertEqual(result["errors"], [])
        self.assertIn("variant A: frame is 280px tall, 37% of the 755px stage (at least 40%)", result["warnings"][0])

    def test_every_message_says_what_it_is_about(self):
        m = card()
        m["card"]["h"] = 880
        m["title"]["h"] = 112.5
        m["variants"][0]["lowest"]["y"] -= 100
        m["variants"][1]["screen"]["scrollH"] = 700
        m["variants"][1]["frame"]["y"] += 12
        for e in self.errors(m):
            self.assertRegex(e, r"^(card|page|title|frames|variant [AB])\b", e)
            self.assertRegex(e, r"\d", e)


class TestMeasurementRules(unittest.TestCase):
    """The measuring rules stay in the page code."""

    def test_label_is_measured_as_its_border_box(self):
        for prop in ("paddingLeft", "paddingRight", "paddingTop", "paddingBottom"):
            self.assertIn("cs.%s" % prop, SOURCE)
        self.assertIn('cs.boxSizing === "border-box"', SOURCE)

    def test_overlap_counts_painted_boxes_not_only_glyphs(self):
        self.assertIn("const paints = ", SOURCE)
        self.assertIn('frame.querySelectorAll("*")', SOURCE)

    def test_clipping_is_measured_with_the_labels_hidden(self):
        self.assertIn(".hl::after{display:none!important}", SOURCE)
        self.assertIn("screen.scrollHeight", SOURCE)
        self.assertIn("scrollWidth", SOURCE)

    def test_the_contract_numbers(self):
        for fragment in ("cardW: 1600", "cardH: 900", "titleLines: 2", "blankPx: 24", "minFontPx: 12", "contrast: 4.5",
                         "contrastLarge: 3", "balanceHeight: 0.4", "balanceWidth: 0.45", "ringArea: 0.45",
                         "ringWidth: 0.85", "ringHeight: 0.4", "stickyEdgePx: 1", "fillHeight: 0.62",
                         "PHONE_SCALES = [1, 1.2, 1.4]"):
            self.assertIn(fragment, SOURCE)

    def test_zoomed_frames_scale_the_label_box(self):
        # Computed lengths are unzoomed; the label box is drawn at the frame's zoom.
        self.assertIn("rect: { x: x2 - w * z, y: y1, r: x2, b: y1 + h * z }", SOURCE)
        self.assertIn("zoom: frame.offsetWidth ? fb.w / frame.offsetWidth : 1", SOURCE)


PILL = {"fontFamily": "Inter", "fontSize": "14px", "fontWeight": "600", "lineHeight": "14px", "letterSpacing": "normal",
        "color": "rgb(17, 24, 39)", "backgroundColor": "rgb(255, 255, 255)", "backgroundImage": "none",
        "borderTopWidth": "1px", "borderTopStyle": "solid", "borderTopColor": "rgb(209, 213, 219)", "borderRightWidth": "1px",
        "borderBottomWidth": "1px", "borderLeftWidth": "1px", "borderRadius": "999px", "paddingTop": "8px",
        "paddingRight": "16px", "paddingBottom": "8px", "paddingLeft": "16px", "boxShadow": "none", "height": "32px"}


def phone_card(scale=1.2, frame_h=380):
    """The clean card as a native phone card measured at a phone_scale, both frames frame_h tall."""
    m = card()
    m["device"] = "phone"
    m["phoneScale"] = scale
    m["stage"].update({"y": 200, "b": 955})
    for v in m["variants"]:
        f = v["frame"]
        f["kind"] = "phone"
        f["w"] = 420 * scale
        f["h"] = frame_h
        f["b"] = f["y"] + frame_h
        f["innerBottom"] = f["b"] - 1
        v["column"]["y"] = f["y"] - 46
        v["lowest"] = {"y": f["b"] - 21, "what": "“Ödemeye geç”"}
    return m


def stage_rec(v, dx, caption="1. Araç", zoom=0.8):
    """One stage phone of variant v, shifted dx px, with its caption above it."""
    rec = json.loads(json.dumps({k: v[k] for k in ("frame", "screen", "widest", "lowest", "texts", "items", "rings")}))
    for box in [rec["frame"], rec["screen"]]:
        box["x"] += dx
        box["r"] += dx
    rec["frame"]["w"] = rec["frame"]["r"] - rec["frame"]["x"]
    rec["rings"] = []
    rec["zoom"] = zoom
    rec["texts"] = [dict(t, px=15) for t in rec["texts"]]
    if caption is not None:
        y = rec["frame"]["y"]
        rec["caption"] = {"text": caption, "px": 13, "rect": {"x": rec["frame"]["x"], "y": y - 24, "r": rec["frame"]["x"] + 60, "b": y - 8}}
    return rec


def sheet(v, w=None, scroll_h=120):
    """The continuation sheet under variant v's phone."""
    s = v["screen"]
    w = s["w"] if w is None else w
    y = v["frame"]["b"] + 14
    return {"frame": {"x": s["x"], "y": y, "w": w, "h": 150, "r": s["x"] + w, "b": y + 150, "kind": "sheet",
                      "scrollH": 150, "clientH": 150},
            "screen": {"x": s["x"], "y": y + 22, "w": w, "h": 128, "r": s["x"] + w, "b": y + 150,
                       "scrollH": scroll_h, "clientH": 128, "scrollW": w, "clientW": w},
            "widest": None, "lowest": None, "texts": [], "items": [], "rings": [], "stickies": [],
            "caption": {"text": "Kaydırınca görünen kısım"}}


@unittest.skipUnless(NODE, "node not found")
class TestContract7Judge(unittest.TestCase):
    """The Contract 7 rules on synthetic measurements: each fires on its number and stays quiet just inside it."""

    def judge(self, m, strict=False):
        return call("judge", m, {"strict": strict})

    def errors(self, m, strict=False):
        return self.judge(m, strict)["errors"]

    def assertOne(self, m, *fragments, strict=False):
        errs = self.errors(m, strict)
        self.assertEqual(len(errs), 1, errs)
        for fragment in fragments:
            self.assertIn(fragment, errs[0])

    # 1. pills
    def test_pills_must_be_alike(self):
        m = card()
        m["pills"] = [{"cls": "pill-a", "style": dict(PILL)}, {"cls": "pill-b", "style": dict(PILL)}]
        self.assertEqual(self.errors(m), [])
        m["pills"][0]["style"].update(backgroundColor="rgb(17, 24, 39)", color="rgb(255, 255, 255)")
        self.assertOne(m, "pills differ in 2 properties: color A #ffffff, B #111827; background-color A #111827, B #ffffff")

    def test_pills_differing_only_in_padding(self):
        m = card()
        m["pills"] = [{"cls": "pill-a", "style": dict(PILL)}, {"cls": "pill-b", "style": dict(PILL, paddingLeft="20px")}]
        self.assertOne(m, "pills differ in 1 property: padding-left A 16px, B 20px")

    # 2. ring breadth
    def ringed(self, w_ratio, h_ratio, soft=False):
        m = card()
        v = m["variants"][1]
        s = v["screen"]
        ring = v["rings"][0]
        ring["box"] = {"x": s["x"] + 10, "y": s["y"] + 60, "w": s["w"] * w_ratio, "h": s["h"] * h_ratio,
                       "r": s["x"] + 10 + s["w"] * w_ratio, "b": s["y"] + 60 + s["h"] * h_ratio}
        ring["soft"] = soft
        return m

    def test_ring_too_wide_by_width_and_height(self):
        self.assertOne(self.ringed(0.93, 0.47), "variant B ring “kupon alanı açık”: ring too wide:",
                       "93% of its width, 47% of its height", "use .hl-soft for consequences")
        self.assertEqual(self.errors(self.ringed(0.93, 0.39)), [])  # a full-width bar is fine
        self.assertEqual(self.errors(self.ringed(0.84, 0.47)), [])

    def test_ring_too_wide_by_area(self):
        self.assertOne(self.ringed(0.8, 0.6), "ring too wide: it covers 48% of the screen")
        self.assertEqual(self.errors(self.ringed(0.8, 0.55)), [])  # 44%

    def test_a_soft_ring_may_be_wide(self):
        self.assertEqual(self.errors(self.ringed(0.95, 0.8, soft=True)), [])

    # 4. sticky
    def test_pinned_words(self):
        for note in ("Ekranın altında sabit", "Sabitlenmiş buton", "Yapışkan çubuk", "YAPIŞKAN", "SABİT", "Sticky CTA",
                     "Pinned bar", "FIXED", "STICKY"):
            self.assertTrue(call("isPinned", note), note)
        for note in ("Sabitçe", "Kaydırınca görünüyor", "Prefixed", "", None):
            self.assertFalse(call("isPinned", note), note)

    def test_a_pinned_ring_in_the_page_flow(self):
        m = card()
        ring = m["variants"][1]["rings"][0]
        ring["note"] = "Ekranın altında sabit"
        ring["box"] = {"x": 990, "y": 480, "w": 390, "h": 80, "r": 1380, "b": 560}
        self.assertOne(m, "variant B ring “Ekranın altında sabit”: the label says pinned but the ring is in the page flow",
                       "ends 168px above the screen's bottom edge", ".r-sticky")
        ring["inSticky"] = True
        self.assertEqual(self.errors(m), [])

    def sticky(self, bottom_off=0, first_view=True):
        m = card()
        v = m["variants"][1]
        s = v["screen"]
        v["stickies"] = [{"rect": {"x": s["x"], "y": s["b"] - 65 - bottom_off, "r": s["r"], "b": s["b"] - bottom_off},
                          "firstView": first_view}]
        return m

    def test_sticky_bar_touches_the_bottom_edge(self):
        self.assertEqual(self.errors(self.sticky(0)), [])
        self.assertEqual(self.errors(self.sticky(1)), [])
        self.assertOne(self.sticky(40), "variant B: the .r-sticky bar ends 40px above the screen's bottom edge; it must touch it (±1px)")

    def test_sticky_bar_belongs_in_the_first_view(self):
        self.assertOne(self.sticky(0, first_view=False), "variant B: an .r-sticky lies outside the first view")

    def test_sticky_bar_covers_no_content(self):
        m = self.sticky(0)
        v = m["variants"][1]
        v["items"].append({"what": "“Toplam”", "rects": [{"x": 1000, "y": v["screen"]["b"] - 40, "r": 1100,
                                                         "b": v["screen"]["b"] - 20}], "skip": [], "sticky": -1})
        self.assertOne(m, "variant B: the .r-sticky bar covers 2000px² of “Toplam”")
        v["items"][-1]["sticky"] = 0  # its own button
        self.assertEqual(self.errors(m), [])

    # 5. short screen
    def test_short_screen_names_the_larger_scale(self):
        m = phone_card(1.2, 380)
        res = self.judge(m)
        self.assertEqual(res["errors"], [])
        self.assertEqual(len(res["warnings"]), 1, res)
        self.assertIn("card: variant A's phone fills 50% of the 755px stage (380px at phone_scale 1.2; at least 62%); "
                      "set card.phone_scale: 1.4 (≈443px, 59%", res["warnings"][0])
        self.assertOne(m, "set card.phone_scale: 1.4", strict=True)

    def test_short_screen_from_scale_1_takes_the_largest_that_fits(self):
        self.assertOne(phone_card(1, 300), "set card.phone_scale: 1.4 (≈420px", strict=True)

    def test_short_screen_only_when_the_larger_scale_fits(self):
        # A sits short, but B with its continuation would overflow the stage at 1.4 (46 + 530 × 1.4 > 755): quiet.
        m = phone_card(1.2, 380)
        v = m["variants"][1]
        v["below"] = sheet(v)
        v["below"]["frame"]["b"] = v["frame"]["y"] + 650
        self.assertEqual(self.judge(m, True), {"errors": [], "warnings": []})

    def test_a_screen_that_fills_enough_or_cannot_grow(self):
        self.assertEqual(self.judge(phone_card(1.2, 470), True), {"errors": [], "warnings": []})  # 62%
        self.assertEqual(self.judge(phone_card(1.4, 380), True), {"errors": [], "warnings": []})  # no larger scale
        unscaled = phone_card(1.2, 380)
        unscaled["phoneScale"] = None  # not measured: the rule needs the scale
        self.assertEqual(self.judge(unscaled, True), {"errors": [], "warnings": []})

    def test_short_screen_never_for_a_browser(self):
        m = phone_card(1.2, 300)
        for v in m["variants"]:
            v["frame"]["kind"] = "web"
        self.assertEqual(self.errors(m, True), [])

    # 6. stages
    def staged(self, captions=("1. Araç", "2. Teklif"), zoom=0.8):
        m = card()
        for v in m["variants"]:
            c = v["column"]
            c.update({"r": c["x"] + c["w"], "b": c["y"] + c["h"]})
            v["stages"] = [stage_rec(v, 0, captions[0], zoom), stage_rec(v, 0, captions[1], zoom)]
            for k, st in enumerate(v["stages"]):
                w = 336
                st["frame"].update({"x": v["column"]["x"] + k * (w + 40), "w": w})
                st["frame"]["r"] = st["frame"]["x"] + w
                st["screen"].update({"x": st["frame"]["x"] + 1, "r": st["frame"]["r"] - 1, "w": w - 2})
                if st.get("caption"):
                    st["caption"]["rect"].update({"x": st["frame"]["x"], "r": st["frame"]["x"] + 60})
                st["lowest"] = None
        return m

    def test_clean_stages_pass(self):
        self.assertEqual(self.errors(self.staged()), [])

    def test_stage_needs_a_caption(self):
        m = self.staged()
        m["variants"][0]["stages"][1]["caption"] = None
        self.assertOne(m, "variant A stage 2: no caption above the phone")
        m = self.staged()
        m["variants"][1]["stages"][0]["caption"]["rect"]["b"] = m["variants"][1]["stages"][0]["frame"]["y"] + 20
        self.assertOne(m, "variant B stage 1: caption “1. Araç” is not above its phone (it ends 20px below the phone's top)")

    def test_stage_text_is_checked_at_its_rendered_size(self):
        m = self.staged()
        m["variants"][0]["stages"][0]["texts"][0]["px"] = 13
        self.assertOne(m, "variant A stage 1: text “890 TL” is 10.4px rendered (13px × zoom 0.80), below 12px")

    def test_stage_phone_inside_its_column(self):
        m = self.staged()
        st = m["variants"][1]["stages"][1]
        st["frame"]["r"] += 30
        self.assertIn("variant B stage 2: phone sticks out of the 728px column by 14px", " ".join(self.errors(m)))

    # 7. continuation sheet
    def test_continuation_sheet(self):
        m = card()
        for v in m["variants"]:
            v["below"] = sheet(v)
        self.assertEqual(self.errors(m), [])
        m["variants"][1]["below"] = sheet(m["variants"][1], w=360)
        self.assertOne(m, "variant B continuation: sheet is 360px wide, the phone's screen 418px; it must be the same width")
        m["variants"][1]["below"] = sheet(m["variants"][1], scroll_h=170)
        self.assertOne(m, "variant B continuation: screen content is clipped: 170px of content in a 128px screen")
        m["variants"][1]["below"] = sheet(m["variants"][1])
        m["variants"][1]["below"]["caption"] = None
        self.assertOne(m, "variant B continuation: no caption above the sheet")

    # 3. label clearance: the measured gap keeps its decimal
    def test_label_gap_is_reported_with_its_decimal(self):
        m = card()
        m["variants"][0]["items"][0]["rects"][0]["b"] += 2.1  # 5.9px from the label
        self.assertOne(m, "label sits 5.9px from “890 TL”; leave at least 6px")


def _playwright_ready():
    if not NODE:
        return False
    p = subprocess.run([NODE, "-e", "require.resolve('playwright')"], capture_output=True)
    return p.returncode == 0


@unittest.skipUnless(_playwright_ready(), "Playwright not found (NODE_PATH)")
class TestFixturesInChromium(unittest.TestCase):
    """Hand-written cards measured in Chromium: every new check has a failing and a passing card."""

    @classmethod
    def run_check(cls, names, strict):
        args = [NODE, SCRIPT, "--json"] + (["--strict"] if strict else []) + [os.path.join(FIXTURES, n + ".html") for n in names]
        p = subprocess.run(args, capture_output=True, text=True, timeout=180)
        if p.returncode == 2:
            raise unittest.SkipTest("render_check usage error: " + p.stderr.strip()[:200])
        if p.returncode == 3:
            raise unittest.SkipTest("render_check could not start a browser: " + p.stderr.strip()[:200])
        out = {}
        for line in p.stdout.splitlines():
            rec = json.loads(line)
            out[os.path.basename(rec["file"])[:-5]] = rec
        return out

    @classmethod
    def setUpClass(cls):
        names = sorted(f[:-5] for f in os.listdir(FIXTURES) if f.endswith(".html"))
        cls.strict = cls.run_check(names, True)
        cls.loose = cls.run_check(["short-screen-12"], False)

    def errs(self, name):
        return self.strict[name]["errors"]

    def assertOnly(self, name, *fragments):
        errs = self.errs(name)
        self.assertEqual(len(errs), len(fragments), errs)
        for err, fragment in zip(errs, fragments):
            self.assertIn(fragment, err)

    def test_clean_cards_pass_strict(self):
        for name in ("clean", "ring-narrow-pricing", "label-clear-field", "sticky-ok", "short-screen-14", "stages-ok"):
            self.assertEqual(self.strict[name]["errors"] + self.strict[name]["warnings"], [], name)

    def test_e_pill_a_darker_than_b(self):
        self.assertOnly("pills-darker-a", "pills differ in 3 properties: color A #ffffff, B #111827")

    def test_b_ring_around_a_whole_pricing_table(self):
        self.assertOnly("ring-wide-pricing", "variant B ring “Yıllık varsayılan, yıllık fiyatlar”: ring too wide")

    def test_c_ring_label_on_the_next_field_label(self):
        self.assertOnly("label-near-field", "variant B ring “Tek alan, ad soyad”: label covers")
        self.assertIn("of “Cep telefonu numarası”", self.errs("label-near-field")[0])

    def test_a_in_flow_bar_labelled_pinned(self):
        self.assertOnly("sticky-inflow", "variant B ring “Ekranın altında sabit”: the label says pinned but the ring is in the page flow")

    def test_sticky_bar_off_the_bottom_edge(self):
        errs = " | ".join(self.errs("sticky-floating"))
        self.assertIn("variant B: the .r-sticky bar ends 40px above the screen's bottom edge", errs)
        self.assertIn("variant B: the .r-sticky bar covers", errs)

    def test_d_short_screen_names_1_4(self):
        self.assertOnly("short-screen-12", "card: variant A's phone fills 47% of the 755px stage")
        self.assertIn("set card.phone_scale: 1.4", self.errs("short-screen-12")[0])
        self.assertEqual(self.loose["short-screen-12"]["errors"], [])
        self.assertIn("set card.phone_scale: 1.4", self.loose["short-screen-12"]["warnings"][0])

    def test_stage_phones(self):
        errs = self.errs("stages-bad")
        self.assertIn("variant B stage 2: no caption above the phone", " | ".join(errs))
        self.assertIn("variant A stage 1: text “12:41” is 11.2px rendered (14px × zoom 0.80), below 12px", errs)
        self.assertTrue(any("label text is 10px rendered" in e for e in errs), errs)

    def test_continuation_sheet(self):
        self.assertOnly("below-bad", "variant B continuation: sheet is 360px wide, the phone's screen 418px",
                        "variant B continuation: screen content is clipped: 148px of content in a 108px screen")


if __name__ == "__main__":
    unittest.main()


def _png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(24)
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


@unittest.skipUnless(NODE, "node not found")
class TestVisualStatus(unittest.TestCase):
    """Three outcomes stay apart: VERIFIED (0), VISUAL_CHECK_FAILED (1), VISUAL_CHECK_UNAVAILABLE (3)."""

    def run_rc(self, args, env_update=None, drop=()):
        env = {k: v for k, v in os.environ.items() if k not in drop}
        env.update(env_update or {})
        return subprocess.run([NODE, SCRIPT] + args, capture_output=True, text=True, timeout=180, env=env)

    def test_without_playwright_the_check_is_unavailable_not_failed(self):
        bare = {k: v for k, v in os.environ.items() if k != "NODE_PATH"}
        probe = subprocess.run([NODE, "-e", "require.resolve('playwright')"], capture_output=True,
                               cwd=os.path.dirname(SCRIPT), env=bare)
        if probe.returncode == 0:
            self.skipTest("playwright resolves without NODE_PATH here")
        with tempfile.TemporaryDirectory() as home:  # no ~/.abtest-visual either
            p = self.run_rc([os.path.join(FIXTURES, "clean.html")], {"HOME": home}, drop=("NODE_PATH",))
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertIn("VISUAL_CHECK_UNAVAILABLE", p.stderr)
        self.assertIn("nothing was measured", p.stderr)
        # The exit-3 message says the exact one-time install.
        self.assertIn("npm i --prefix ~/.abtest-visual playwright && npx --prefix ~/.abtest-visual playwright "
                      "install chromium", p.stderr)

    @unittest.skipUnless(_playwright_ready(), "Playwright not found (NODE_PATH)")
    def test_a_browser_that_does_not_start_is_unavailable(self):
        p = self.run_rc([os.path.join(FIXTURES, "clean.html")], {"CHROMIUM_PATH": "/nonexistent/chrome-headless-shell"})
        self.assertEqual(p.returncode, 3, p.stderr)
        self.assertIn("Chromium did not start", p.stderr)
        self.assertIn("VISUAL_CHECK_UNAVAILABLE", p.stderr)

    @unittest.skipUnless(_playwright_ready(), "Playwright not found (NODE_PATH)")
    def test_failed_and_verified_render_with_a_half_size_shot(self):
        failed = self.run_rc(["--strict", os.path.join(FIXTURES, "sticky-inflow.html")])
        if failed.returncode == 3:
            self.skipTest("no browser: " + failed.stderr[:200])
        self.assertEqual(failed.returncode, 1, failed.stdout)
        self.assertTrue(failed.stderr.rstrip().endswith("VISUAL_CHECK_FAILED"), failed.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("clean.html", "card.css"):
                shutil.copy(os.path.join(FIXTURES, name), tmp)
            ok = self.run_rc(["--strict", "--shot", "--half", os.path.join(tmp, "clean.html")])
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            self.assertTrue(ok.stderr.rstrip().endswith("VERIFIED"), ok.stderr)
            self.assertEqual(_png_size(os.path.join(tmp, "card-clean.png")), (1600, 900))
            self.assertEqual(_png_size(os.path.join(tmp, "card-clean-800.png")), (800, 450))


@unittest.skipUnless(NODE, "node not found")
class TestInheritedContrast(unittest.TestCase):
    """A contrast defect copied from the user's screen is reported, not passed, and only where it qualifies."""

    def m(self, a, b, listed):
        return {"inheritedContrast": listed, "variants": [{"texts": a}, {"texts": b}]}

    GREY = [119, 120, 121, 1]
    ENTRY = [{"text": "Adınız", "color": "#777879"}]

    def t(self, text="Adınız", fg=None, ring=False):
        return {"text": text, "fg": fg or self.GREY, "inRing": ring}

    def test_listed_identical_outside_rings_is_inherited(self):
        self.assertTrue(call("inheritedFrom", self.m([self.t()], [self.t()], self.ENTRY), self.t()))

    def test_not_listed_stays_an_error(self):
        self.assertFalse(call("inheritedFrom", self.m([self.t()], [self.t()], []), self.t()))

    def test_inside_a_ring_stays_an_error(self):
        ringed = self.t(ring=True)
        self.assertFalse(call("inheritedFrom", self.m([ringed], [ringed], self.ENTRY), ringed))

    def test_b_worse_or_different_stays_an_error(self):
        lighter = self.t(fg=[150, 150, 150, 1])
        self.assertFalse(call("inheritedFrom", self.m([self.t()], [lighter], self.ENTRY), self.t()))
        self.assertFalse(call("inheritedFrom", self.m([self.t()], [lighter], self.ENTRY), lighter))

    def test_b_only_text_stays_an_error(self):
        new = self.t("E-Posta (isteğe bağlı)")
        listed = [{"text": "E-Posta (isteğe bağlı)", "color": "#777879"}]
        self.assertFalse(call("inheritedFrom", self.m([self.t("E-Posta")], [new], listed), new))

    def test_an_icon_is_held_to_three_to_one(self):
        self.assertIn("contrastNonText: 3", SOURCE)
        self.assertIn("t.icon ? L.contrastNonText", SOURCE)
