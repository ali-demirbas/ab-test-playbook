#!/usr/bin/env node
// Render built scenario cards in headless Chromium and check what a reader
// would see against the card contract: the card's size, the title's lines, the
// frames (clipped content, blank phone screen, A/B alignment and width), the
// ring and its label (covering other screen elements, cut off by the screen
// edge), the size and contrast of every piece of mockup text, and the balance
// of the frames on the stage. Optionally writes a screenshot.
//
// This is a manual/orchestrator tool, not part of the unit suite: the suite
// stays stdlib-only Python, and Playwright is a Node dependency this repo does
// not ship. Point it at an existing install:
//
//   NODE_PATH=/path/to/node_modules node scripts/render_check.mjs card.html [more.html ...]
//   CHROMIUM_PATH=/path/to/chrome-headless-shell node scripts/render_check.mjs --shot card.html
//
// --shot    write card-<name>.png next to each card (abtest-card-x.html → card-x.png)
// --json    print one JSON object per card instead of the report
// --strict  warnings fail the run too
//
// The page part (collect) only measures; judge() turns the measurements into
// errors and warnings and is a pure function, so its rules and messages are
// unit-tested without a browser (tests/test_render_check.py). Every message
// names the variant and element it is about and the measurement that failed.
//
// What is measured
//
//   label            The ring label (.hl[data-note]::after) as the box that is
//                    painted: its border box. A pseudo-element is not matched by
//                    `*{box-sizing:border-box}`, so its computed width/height are
//                    content-box values and the padding is added.
//   screen elements  Every element in the frame that is neither the ring, inside
//                    it nor around it: its text as line boxes, or its box when it
//                    paints one (a filled button, a bordered field, a badge, a
//                    thumbnail). The ring is its element box grown by
//                    outline-offset + outline-width. A ring inside an
//                    .r-overlay (the ringed modal) sits over the dimming: the
//                    screen elements the overlay covers are not counted as
//                    covered by that ring or its label.
//   contrast         Text colour against its effective background: the element's
//                    and its ancestors' backgrounds composited up to the first
//                    opaque one (every stop of a gradient is tried, the worst
//                    counts). Text under an .r-overlay is dimmed by design and
//                    only checked for size.
//   clipped          The screen's scroll size against its client size (a frame
//                    is at most as tall as the stage; what does not fit is cut),
//                    and at the top: the element that starts furthest above the
//                    screen's top edge (a scroll size never counts what sticks
//                    out upwards, e.g. a modal centred in a box too small for it).
//   blank screen     On a phone frame, the gap between the lowest element and the
//                    frame's inner bottom edge.
//   status ribbons   The draft (#abtest-draft) and conditional
//                    (#abtest-conditional) ribbons the builder adds: absolutely
//                    positioned tabs in the card's top padding. They are not
//                    screen elements (no frame contains them); each must lie
//                    inside the card and off the title, the stage and the other
//                    ribbon.
//   pills            The Variant A / B pills' computed style: they must be equal
//                    (only the text differs; no winner colour).
//   ring breadth     A .hl box against its screen: more than 45% of the area, or
//                    more than 85% of the width and 40% of the height, rings a
//                    region, not the variable (.hl-soft rings are exempt).
//   sticky bar       An .r-sticky must end on its screen's bottom edge (±1px) in
//                    the first view and cover no first-view content; a ring whose
//                    label says pinned (PINNED_RE) must sit in an .r-sticky.
//   short screen     One phone per arm that fills less than 62% of the stage
//                    while a larger card.phone_scale still fits: the scale to use
//                    is named (an error with --strict, else a warning).
//   stages           Several phones in one column (.r-stage-break): each one is
//                    checked like a frame (clipping, rings, text at its rendered
//                    size, i.e. computed size × the phone's zoom) and needs a
//                    caption (the first lettered text before it) above it.
//   continuation     The sheet under the phone (.below > .below-screen, from
//                    .r-fold): no clipping, a caption, the same width as the
//                    phone's screen, inside the stage.
//
// Exit: 0 = no error (warnings allowed unless --strict), 1 = an error (with
// --strict also a warning), 2 = usage.
import { createRequire } from "node:module";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";

export const USAGE = "usage: render_check.mjs [--shot] [--json] [--strict] card.html [more.html ...]";
export const FLAGS = ["--shot", "--json", "--strict"];

// The contract's numbers (CONTRACT: card 1600 × 900, title ≤ 2 lines, phone
// blank ≤ 24px, text ≥ 12px, contrast 4.5:1 / 3:1 large, balance 40% / 45%).
export const LIMITS = {
  cardW: 1600,
  cardH: 900,
  titleLines: 2,
  blankPx: 24,
  minFontPx: 12,
  contrast: 4.5,
  contrastLarge: 3,
  largePx: 24,
  largeBoldPx: 18.66,
  balanceHeight: 0.4,
  balanceWidth: 0.45,
  overlapPx2: 4,
  labelGapPx: 6,
  alignPx: 1,
  ringArea: 0.45,
  ringWidth: 0.85,
  ringHeight: 0.4,
  stickyEdgePx: 1,
  fillHeight: 0.62,
  sheetWidthPx: 1.5,
};

// card.phone_scale values the builder accepts; 1.2 is the template default.
export const PHONE_SCALES = [1, 1.2, 1.4];
export const DEFAULT_PHONE_SCALE = 1.2;

// A ring label that says the element is pinned to the screen (same words as the builder's heuristic).
export const PINNED_RE = /(?<![\p{L}\p{N}])(sabit|sabitlen\p{L}*|yapışkan\p{L}*|sticky|pinned|fixed)(?![\p{L}\p{N}])/iu;
// Both lowercasings: Turkish turns "I" into "ı" (an English "FIXED" would be missed), plain JS misses "İ".
export const isPinned = (note) => [(note || "").toLocaleLowerCase("tr"), (note || "").toLowerCase()].some((s) => PINNED_RE.test(s));

// The pill properties that must be equal in A and B.
export const PILL_PROPS = ["fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "color", "backgroundColor",
  "backgroundImage", "borderTopWidth", "borderTopStyle", "borderTopColor", "borderRightWidth", "borderBottomWidth",
  "borderLeftWidth", "borderRadius", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "boxShadow", "height"];

export function parseArgs(argv) {
  const unknown = argv.filter((a) => a.startsWith("--") && !FLAGS.includes(a));
  if (unknown.length) return { error: `unknown option ${unknown.join(", ")}` };
  const files = argv.filter((a) => !a.startsWith("--"));
  if (!files.length) return { error: "no card given" };
  return { shot: argv.includes("--shot"), json: argv.includes("--json"), strict: argv.includes("--strict"), files };
}

// ---------------------------------------------------------------- colour

const hex2 = (n) => Math.round(n).toString(16).padStart(2, "0");
export const hex = (c) => `#${hex2(c[0])}${hex2(c[1])}${hex2(c[2])}`;

// `top` over `bottom`; bottom is opaque.
export function over(top, bottom) {
  const a = top[3] ?? 1;
  return [0, 1, 2].map((i) => top[i] * a + bottom[i] * (1 - a)).concat(1);
}

function luminance(c) {
  const ch = c.slice(0, 3).map((v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : ((s + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
}

export function contrastRatio(fg, bg) {
  const [l1, l2] = [luminance(fg), luminance(bg)].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
}

// Background layers (bottom → top, each a list of candidate colours: one for a
// solid colour, every stop for a gradient) → every opaque background the text
// can sit on.
export function backgrounds(layers) {
  let out = [[255, 255, 255, 1]];
  for (const layer of layers) {
    const next = [];
    for (const base of out) for (const c of layer) next.push(over(c, base));
    out = next;
  }
  return out;
}

export function isLarge(px, weight) {
  return px >= LIMITS.largePx || (px >= LIMITS.largeBoldPx && weight >= 700);
}

// ---------------------------------------------------------------- geometry

export function overlapArea(a, b) {
  return Math.max(0, Math.min(a.r, b.r) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.y, b.y));
}

// How far `inner` sticks out of `outer`, the worst side.
export function outside(inner, outer) {
  return Math.max(outer.x - inner.x, inner.r - outer.r, outer.y - inner.y, inner.b - outer.b, 0);
}

const px = (n) => `${Math.round(n)}px`;
// A measured gap: whole pixels stay whole, else one decimal (a 5.9px gap must not read as 6px).
const gapPx = (n) => `${Math.abs(n - Math.round(n)) < 0.05 ? Math.round(n) : n.toFixed(1)}px`;

// ---------------------------------------------------------------- the rules

// "rgb(17, 24, 39)" → "#111827"; anything else as it is.
function cssValue(s) {
  const c = /^rgba?\(([^)]+)\)$/.exec((s || "").trim());
  if (!c) return s;
  const p = c[1].split(/[,\s/]+/).filter(Boolean).map(parseFloat);
  return p.length > 3 && p[3] < 1 ? `${hex(p)}/${p[3]}` : hex(p);
}
const kebab = (prop) => prop.replace(/[A-Z]/g, (ch) => "-" + ch.toLowerCase());

// Clipping, blank screen, rings and labels, text and the sticky bar of one drawn screen: the variant's
// frame, one stage phone or the continuation sheet under the phone.
function checkFrame(who, v, column, m, errors, warnings, opts) {
  const L = LIMITS;
  const f = v.frame;
  const s = v.screen;
  const zoom = Math.min(1, v.zoom || 1);
  if (!opts.stage && f.w > column.w + 1) errors.push(`${who}: frame is ${px(f.w)} wide, wider than its ${px(column.w)} column`);

  // Clipping: the frame is at most as tall as the stage, so content that does
  // not fit is cut off. The author shows the relevant part of the screen.
  if (s.scrollH > s.clientH + 1) {
    errors.push(`${who}: screen content is clipped: ${px(s.scrollH)} of content in a ${px(s.clientH)} screen (${px(s.scrollH - s.clientH)} cut off at the bottom; draw only the part of the screen the test is about, or on a phone set card.phone_scale: 1; the frame is capped at the ${px(m.stage.h)} stage)`);
  }
  if (v.topmost && v.topmost.px > 1) {
    errors.push(`${who}: screen content is clipped at the top: ${v.topmost.what} starts ${px(v.topmost.px)} above the screen's top edge and is cut off (draw it inside the screen; a modal goes in an .r-overlay that is a direct child of the screen, the ring on its .r-modal)`);
  }
  if (s.scrollW > s.clientW + 1 || (v.widest && v.widest.px > 1)) {
    const by = Math.max(s.scrollW - s.clientW, v.widest ? v.widest.px : 0);
    errors.push(`${who}: content overflows the screen sideways by ${px(by)}${v.widest && v.widest.what ? ` (${v.widest.what})` : ""}`);
  }
  if (f.scrollH > f.clientH + 1) {
    errors.push(`${who}: frame content is clipped: ${px(f.scrollH)} of frame content in ${px(f.clientH)}`);
  }

  // A phone frame is as tall as its content: no empty screen under it.
  if (opts.blank && f.kind !== "web" && f.kind !== "sheet" && v.lowest) {
    const gap = f.innerBottom - v.lowest.y - (v.lowest.inScreen && f.padB ? f.padB : 0);
    if (gap > L.blankPx) {
      errors.push(`${who}: ${px(gap)} of blank screen under the last element (${v.lowest.what}); at most ${L.blankPx}px, the phone frame must end with its content`);
    }
  }

  // Rings and labels.
  v.rings.forEach((ring, k) => {
    const rw = `${who} ring “${ring.note}”`;
    const grown = ring.outline;
    const cut = outside(grown, s);
    if (cut > 0.5) errors.push(`${rw}: the ring is cut off by the screen edge (${px(cut)} outside the screen)`);
    // Breadth: a ring around most of the screen rings a region, not the variable.
    if (ring.box && !ring.soft && s.w > 0 && s.h > 0) {
      const wr = ring.box.w / s.w;
      const hr = ring.box.h / s.h;
      if (wr * hr > L.ringArea || (wr > L.ringWidth && hr > L.ringHeight)) {
        errors.push(`${rw}: ring too wide: it covers ${Math.round(100 * wr * hr)}% of the screen (${Math.round(100 * wr)}% of its width, ${Math.round(100 * hr)}% of its height; at most ${Math.round(100 * L.ringArea)}% of the area, or ${Math.round(100 * L.ringWidth)}% wide and ${Math.round(100 * L.ringHeight)}% tall): ring the variable, use .hl-soft for consequences`);
      }
    }
    // A pinned element is drawn as the bar at the bottom of the first view, not inside the page flow.
    if (!ring.soft && !ring.inSticky && isPinned(ring.note)) {
      const box0 = ring.box || { b: grown.b };
      errors.push(`${rw}: the label says pinned but the ring is in the page flow (it ends ${px(Math.max(0, s.b - box0.b))} above the screen's bottom edge); draw the bar as .r-sticky at the bottom of the first view, with .r-fold`);
    }
    // A ring on the modal sits over the dimming: what the overlay covers is not under the ring.
    const hidden = (item) => item.skip.includes(k) || (ring.overOverlay && item.dimmed);
    let worst = { area: 0, what: "" };
    for (const item of v.items) {
      if (hidden(item)) continue;
      for (const rect of item.rects) {
        const area = overlapArea(grown, rect);
        if (area > worst.area) worst = { area, what: item.what };
      }
    }
    if (worst.area > L.overlapPx2) {
      errors.push(`${rw}: ring covers screen elements: ${Math.round(worst.area)}px² of ${worst.what} lies under the ring (outline ${px(ring.grow)} outside the element); leave at least ${px(ring.grow + 1)} between the ringed element and its neighbours`);
    }
    const lab = ring.label;
    if (!lab) return;
    // A label in a rounded corner of the frame is clipped by the corner even when it is inside the screen box.
    const rad = f.radius || 0;
    // Each label corner against the frame corner it faces: outside the quarter circle means clipped.
    const cornerCut = rad > 0 && [[lab.rect.x, lab.rect.y, f.x + rad, f.y + rad, -1, -1],
      [lab.rect.r, lab.rect.y, f.r - rad, f.y + rad, 1, -1], [lab.rect.x, lab.rect.b, f.x + rad, f.b - rad, -1, 1],
      [lab.rect.r, lab.rect.b, f.r - rad, f.b - rad, 1, 1]]
      .some(([px0, py0, cx, cy, sx, sy]) =>
        (px0 - cx) * sx > 0 && (py0 - cy) * sy > 0 && Math.hypot(px0 - cx, py0 - cy) > rad + 0.5);
    if (cornerCut) errors.push(`${rw}: label is cut off by the frame's rounded corner; try data-pos="${lab.pos === "below" ? "above" : "below"}" or move the ringed element away from the corner`);
    const labCut = outside(lab.rect, s);
    if (labCut > 0.5) {
      errors.push(`${rw}: label is cut off by the screen edge (${px(labCut)} outside the screen); try data-pos="${lab.pos === "below" ? "above" : "below"}"`);
    }
    const labPx = Math.round(lab.px * zoom * 10) / 10;
    if (labPx < L.minFontPx) errors.push(`${rw}: label text is ${labPx}px${zoom < 1 ? ` rendered (${lab.px}px × zoom ${zoom.toFixed(2)})` : ""}, below ${L.minFontPx}px`);
    const lr = contrastRatio(lab.fg, over(lab.bg, [255, 255, 255, 1]));
    if (lr < L.contrast) errors.push(`${rw}: label contrast ${lr.toFixed(2)}:1 (${hex(lab.fg)} on ${hex(lab.bg)}) is below ${L.contrast}:1`);
    let hit = { area: 0, what: "" };
    const take = (rect, what) => {
      const area = overlapArea(lab.rect, rect);
      if (area > hit.area) hit = { area, what };
    };
    for (const item of v.items) {
      if (hidden(item)) continue;
      for (const rect of item.rects) take(rect, item.what);
    }
    v.rings.forEach((other, j) => {
      if (j === k || other.nested.includes(k) || ring.nested.includes(j)) return;
      take(other.outline, `the ring “${other.note}”`);
      if (other.label) take(other.label.rect, `the label “${other.note}”`);
    });
    if (hit.area > L.overlapPx2) {
      errors.push(`${rw}: label covers ${Math.round(hit.area)}px² of ${hit.what}; try data-pos="${lab.pos === "below" ? "above" : "below"}" or give the ringed element more room`);
    } else {
      // Not covering is not enough: a label that touches its neighbour reads as part of it.
      let near = { gap: Infinity, what: "" };
      for (const item of v.items) {
        if (hidden(item)) continue;
        for (const rect of item.rects) {
          const gap = Math.max(0, rect.x - lab.rect.r, lab.rect.x - rect.r, rect.y - lab.rect.b, lab.rect.y - rect.b);
          if (gap < near.gap) near = { gap, what: item.what };
        }
      }
      if (near.gap < L.labelGapPx) {
        errors.push(`${rw}: label sits ${gapPx(near.gap)} from ${near.what}; leave at least ${px(L.labelGapPx)} around the label (more room above the ringed element, or data-pos="${lab.pos === "below" ? "above" : "below"}")`);
      }
    }
  });

  // The sticky bar: on the first view's bottom edge, covering none of its content.
  (v.stickies || []).forEach((st, k) => {
    if (!st.firstView) {
      errors.push(`${who}: an .r-sticky lies outside the first view; the pinned bar belongs at the bottom of the phone's screen`);
      return;
    }
    const off = s.b - st.rect.b;
    if (Math.abs(off) > L.stickyEdgePx) {
      errors.push(`${who}: the .r-sticky bar ends ${px(Math.abs(off))} ${off > 0 ? "above" : "below"} the screen's bottom edge; it must touch it (±${L.stickyEdgePx}px)`);
    }
    let under = { area: 0, what: "" };
    for (const item of v.items) {
      if (item.sticky === k || item.dimmed) continue;
      for (const rect of item.rects) {
        const area = overlapArea(st.rect, rect);
        if (area > under.area) under = { area, what: item.what };
      }
    }
    if (under.area > L.overlapPx2) {
      errors.push(`${who}: the .r-sticky bar covers ${Math.round(under.area)}px² of ${under.what}; the first view keeps a bottom padding as tall as the bar`);
    }
  });

  // Text size (as rendered: a stage phone is zoomed out) and contrast, grouped so one colour mistake is one message.
  const small = new Map();
  const faint = new Map();
  for (const t of v.texts) {
    const shown = Math.round(t.px * zoom * 10) / 10;
    if (shown < L.minFontPx) {
      const key = `${shown}`;
      if (!small.has(key)) small.set(key, { t, n: 0, shown });
      small.get(key).n += 1;
    }
    if (t.dimmed || !t.fg) continue;
    const need = isLarge(t.px * zoom, t.weight) ? L.contrastLarge : L.contrast;
    let worstRatio = Infinity;
    let worstBg = null;
    for (const bg of backgrounds(t.layers)) {
      const ratio = contrastRatio(over(t.fg, bg), bg);
      if (ratio < worstRatio) {
        worstRatio = ratio;
        worstBg = bg;
      }
    }
    if (worstRatio < need) {
      const key = `${hex(t.fg)}|${hex(worstBg)}|${t.px}`;
      if (!faint.has(key)) faint.set(key, { t, n: 0, ratio: worstRatio, bg: worstBg, need });
      faint.get(key).n += 1;
    }
  }
  for (const { t, n, shown } of small.values()) {
    const size = zoom < 1 ? `${shown}px rendered (${t.px}px × zoom ${zoom.toFixed(2)})` : `${t.px}px`;
    errors.push(`${who}: text ${t.what} is ${size}, below ${L.minFontPx}px${n > 1 ? ` (${n} text nodes at this size)` : ""}`);
  }
  for (const { t, n, ratio, bg, need } of faint.values()) {
    errors.push(`${who}: text ${t.what} has contrast ${ratio.toFixed(2)}:1 (${hex(over(t.fg, bg))} on ${hex(bg)}, ${t.px}px) below ${need}:1${n > 1 ? ` (${n} text nodes alike)` : ""}`);
  }

  // Balance: a frame that uses little of the stage reads as a thumbnail.
  if (opts.balance) {
    if (f.h < L.balanceHeight * m.stage.h) {
      warnings.push(`${who}: frame is ${px(f.h)} tall, ${Math.round((100 * f.h) / m.stage.h)}% of the ${px(m.stage.h)} stage (at least ${Math.round(L.balanceHeight * 100)}%): show more of the screen`);
    }
    if (f.kind === "web" && f.w < L.balanceWidth * column.w) {
      warnings.push(`${who}: browser frame is ${px(f.w)} wide, ${Math.round((100 * f.w) / column.w)}% of the ${px(column.w)} column (at least ${Math.round(L.balanceWidth * 100)}%)`);
    }
  }
}

// The column a variant's phone and its continuation take, top of the frame to the bottom of the sheet.
function span(v) {
  const bottom = v.below ? Math.max(v.frame.b, v.below.frame.b) : v.frame.b;
  return { h: bottom - v.frame.y, gap: v.below ? Math.max(0, v.below.frame.y - v.frame.b) : 0, offset: v.frame.y - v.column.y };
}

export function judge(m, opts = {}) {
  const errors = [];
  const warnings = [];
  const L = LIMITS;

  if (Math.round(m.card.w) !== L.cardW || Math.round(m.card.h) !== L.cardH) {
    errors.push(`card is ${Math.round(m.card.w)}×${Math.round(m.card.h)}px; it must be exactly ${L.cardW}×${L.cardH}px`);
  }
  if (m.page.w > L.cardW || m.page.h > L.cardH) {
    errors.push(`page is ${m.page.w}×${m.page.h}px: something overflows the ${L.cardW}×${L.cardH}px card`);
  }
  if (m.card.scrollW > m.card.clientW + 1 || m.card.scrollH > m.card.clientH + 1) {
    errors.push(`card content overflows the card: ${m.card.scrollW}×${m.card.scrollH}px of content in ${m.card.clientW}×${m.card.clientH}px`);
  }
  // Status ribbons (draft, conditional): inside the card, covering nothing of it.
  const ribbons = m.ribbons || [];
  ribbons.forEach((rb, k) => {
    const who = `status ribbon #${rb.id}`;
    const cut = outside(rb, m.card);
    if (cut > 0.5) errors.push(`${who} lies ${px(cut)} outside the card; it hangs inside the card's top padding`);
    const onTitle = m.title && m.title.rect ? overlapArea(rb, m.title.rect) : 0;
    if (onTitle > L.overlapPx2) errors.push(`${who} covers ${Math.round(onTitle)}px² of the title`);
    const onStage = m.stage && m.stage.r !== undefined ? overlapArea(rb, m.stage) : 0;
    if (onStage > L.overlapPx2) errors.push(`${who} covers ${Math.round(onStage)}px² of the stage (pills and frames)`);
    ribbons.forEach((other, j) => {
      const area = j > k ? overlapArea(rb, other) : 0;
      if (area > L.overlapPx2) errors.push(`${who} covers the ribbon #${other.id} (${Math.round(area)}px²)`);
    });
  });
  if (m.title) {
    const lines = Math.round(m.title.h / m.title.lineHeight);
    if (lines > L.titleLines) {
      errors.push(`title wraps to ${lines} lines (${px(m.title.h)} at ${m.title.lineHeight}px line height); at most ${L.titleLines}: shorten it`);
    }
  } else {
    errors.push("title: no .title element in the card");
  }
  // Pills: one neutral style, only the text differs.
  const pills = m.pills || [];
  if (pills.length === 2) {
    const [pa, pb] = pills;
    const diff = PILL_PROPS.filter((p) => pa.style[p] !== pb.style[p]);
    if (diff.length) {
      const shown = diff.slice(0, 4).map((p) => `${kebab(p)} A ${cssValue(pa.style[p])}, B ${cssValue(pb.style[p])}`);
      errors.push(`pills differ in ${diff.length} propert${diff.length > 1 ? "ies" : "y"}: ${shown.join("; ")}${diff.length > 4 ? "; …" : ""}; both take one neutral style (white, 1px #d1d5db border, #111827 text)`);
    }
  }
  if (m.variants.length !== 2) {
    errors.push(`expected 2 frames (Variant A and B), found ${m.variants.length}`);
    return { errors, warnings };
  }

  for (const v of m.variants) {
    const who = `variant ${v.name}`;
    if (v.stages && v.stages.length > 1) {
      v.stages.forEach((st, j) => {
        const sw = `${who} stage ${j + 1}`;
        const cut = outside(st.frame, v.column);
        if (cut > 1) errors.push(`${sw}: phone sticks out of the ${px(v.column.w)} column by ${px(cut)}; the stage phones must fit side by side`);
        checkFrame(sw, st, v.column, m, errors, warnings, { stage: true, blank: true });
        const cap = st.caption;
        if (!cap || !cap.text) {
          errors.push(`${sw}: no caption above the phone (card.stage_captions gives one per stage)`);
        } else {
          if (cap.rect.b > st.frame.y + 1) errors.push(`${sw}: caption “${cap.text}” is not above its phone (it ends ${px(cap.rect.b - st.frame.y)} below the phone's top)`);
          if (cap.px < L.minFontPx) errors.push(`${sw}: caption “${cap.text}” renders at ${cap.px}px, below ${L.minFontPx}px`);
        }
      });
    } else {
      checkFrame(who, v, v.column, m, errors, warnings, { blank: true, balance: true });
    }
    // The continuation sheet under the phone (.r-fold): same width as the screen, a caption, nothing cut off.
    if (v.below) {
      const bw = `${who} continuation`;
      const sheet = v.below.screen;
      if (Math.abs(sheet.w - v.screen.w) > L.sheetWidthPx) {
        errors.push(`${bw}: sheet is ${px(sheet.w)} wide, the phone's screen ${px(v.screen.w)}; it must be the same width (same scale)`);
      }
      if (!v.below.caption || !v.below.caption.text) errors.push(`${bw}: no caption above the sheet`);
      if (m.stage && m.stage.b !== undefined && v.below.frame.b > m.stage.b + 1) {
        errors.push(`${bw}: sheet ends ${px(v.below.frame.b - m.stage.b)} below the stage and is cut off; draw less after .r-fold or set card.phone_scale: 1`);
      }
      checkFrame(bw, v.below, v.column, m, errors, warnings, { stage: true });
    }
  }

  const [a, b] = m.variants;
  if (Math.abs(a.frame.y - b.frame.y) > L.alignPx) {
    errors.push(`frames are not top-aligned: A starts at y=${Math.round(a.frame.y)}, B at y=${Math.round(b.frame.y)} (${px(Math.abs(a.frame.y - b.frame.y))} apart)`);
  }
  if (Math.abs(a.frame.w - b.frame.w) > L.alignPx) {
    errors.push(`frames differ in width: A is ${px(a.frame.w)}, B is ${px(b.frame.w)}`);
  }

  // A short screen: one phone per arm that fills little of the stage while a larger scale still fits.
  const single = m.variants.every((v) => !(v.stages && v.stages.length > 1) && (v.frame.kind === "phone" || v.frame.kind === "phone-web"));
  const clipped = m.variants.some((v) => v.screen.scrollH > v.screen.clientH + 1);
  if (m.phoneScale !== undefined && m.phoneScale !== null && single && !clipped && m.stage.h > 0) {
    const scale = PHONE_SCALES.includes(m.phoneScale) ? m.phoneScale : DEFAULT_PHONE_SCALE;
    // The shortest arm decides: both arms share one scale, and the larger one must still fit for both.
    const short = m.variants.reduce((x, y) => (span(y).h < span(x).h ? y : x));
    const h = span(short).h;
    if (h < L.fillHeight * m.stage.h) {
      const grown = (v, to) => {
        const sp = span(v);
        return (sp.h - sp.gap) * (to / scale) + sp.gap;
      };
      const fits = PHONE_SCALES.filter((to) => to > scale && m.variants.every((v) =>
        span(v).offset + grown(v, to) <= m.stage.h + 0.5 && v.frame.w * (to / scale) <= v.column.w + 1));
      if (fits.length) {
        const to = Math.max(...fits);
        const next = grown(short, to);
        const msg = `card: variant ${short.name}'s phone fills ${Math.round((100 * h) / m.stage.h)}% of the ${px(m.stage.h)} stage (${px(h)} at phone_scale ${scale}; at least ${Math.round(100 * L.fillHeight)}%); set card.phone_scale: ${to} (≈${px(next)}, ${Math.round((100 * next) / m.stage.h)}%; both arms still fit)`;
        (opts.strict ? errors : warnings).push(msg);
      }
    }
  }
  return { errors, warnings };
}

// Whether a card fails the run: any error, or with --strict any warning.
export function failed(result, strict) {
  return result.errors.length > 0 || (strict && result.warnings.length > 0);
}

export function summary(file, m, png) {
  const frames = m.variants
    .map((v) => `${v.name}=${Math.round(v.frame.w)}x${Math.round(v.frame.h)}${m.stage.h ? ` (${Math.round((100 * v.frame.h) / m.stage.h)}%)` : ""}`)
    .join(" ");
  const lines = m.title ? Math.round(m.title.h / m.title.lineHeight) : 0;
  return `${path.basename(file)}  device=${m.device}  card=${Math.round(m.card.w)}x${Math.round(m.card.h)}  title=${lines} line(s)  stage=${Math.round(m.stage.w)}x${Math.round(m.stage.h)}  frames ${frames}${png ? "  → " + path.basename(png) : ""}`;
}

// ---------------------------------------------------------------- the page

// Runs inside the page (Playwright serialises it): self-contained, returns
// plain data for judge().
function collect() {
  const num = (v) => parseFloat(v) || 0;
  const box = (el) => {
    const b = el.getBoundingClientRect();
    return { x: b.left, y: b.top, w: b.width, h: b.height, r: b.right, b: b.bottom };
  };
  const short = (text) => {
    const t = (text || "").replace(/\s+/g, " ").trim();
    return t.length > 28 ? t.slice(0, 28) + "…" : t;
  };
  const colour = (s) => {
    const m = /rgba?\(([^)]+)\)/.exec(s || "");
    if (!m) return null;
    const p = m[1].split(/[,\s/]+/).filter(Boolean).map(parseFloat);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  };
  const stops = (image) => (image && image !== "none" ? (image.match(/rgba?\([^)]+\)/g) || []).map(colour) : []);
  const alpha = (s) => (colour(s) || [0, 0, 0, 0])[3];
  const describe = (el, text) => {
    if (text) return `“${short(text)}”`;
    const b = el.getBoundingClientRect();
    const cls = el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/).join(".") : el.tagName.toLowerCase();
    return `a ${Math.round(b.width)}×${Math.round(b.height)}px ${cls} element`;
  };
  const RINGS = ".hl, .hl-soft";

  const card = document.querySelector(".card");
  const stageEl = document.querySelector(".stage");
  const titleEl = document.querySelector(".card .title");
  const scaleAttr = card ? card.getAttribute("data-phone-scale") : null;
  const out = {
    device: card ? card.getAttribute("data-device") : null,
    phoneScale: scaleAttr === null ? null : parseFloat(scaleAttr) || null,
    card: card
      ? { ...box(card), scrollW: card.scrollWidth, scrollH: card.scrollHeight, clientW: card.clientWidth, clientH: card.clientHeight }
      : { w: 0, h: 0, scrollW: 0, scrollH: 0, clientW: 0, clientH: 0 },
    page: { w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight },
    title: titleEl ? { h: titleEl.getBoundingClientRect().height, lineHeight: num(getComputedStyle(titleEl).lineHeight), text: titleEl.textContent, rect: box(titleEl) } : null,
    stage: stageEl ? box(stageEl) : { w: 0, h: 0 },
    ribbons: [...document.querySelectorAll("#abtest-draft, #abtest-conditional")].map((el) => ({ id: el.id, ...box(el) })),
    pills: [...document.querySelectorAll(".stage .pill-a, .stage .pill-b")].slice(0, 2).map((el) => {
      const cs = getComputedStyle(el);
      const style = {};
      for (const p of ["fontFamily", "fontSize", "fontWeight", "lineHeight", "letterSpacing", "color", "backgroundColor",
        "backgroundImage", "borderTopWidth", "borderTopStyle", "borderTopColor", "borderRightWidth", "borderBottomWidth",
        "borderLeftWidth", "borderRadius", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "boxShadow"]) style[p] = cs[p];
      style.height = `${Math.round(el.getBoundingClientRect().height * 10) / 10}px`;
      return { cls: el.classList.contains("pill-a") ? "pill-a" : "pill-b", style };
    }),
    variants: [],
  };

  // One drawn screen: frame (the phone or browser, or the continuation sheet) and its screen.
  const measure = (frame, screen, sheet) => {
    const fcs = getComputedStyle(frame);
    const frameBg = fcs.backgroundColor;
    const kind = sheet ? "sheet" : frame.classList.contains("browser") ? "web" : frame.querySelector(".m-addr") ? "phone-web" : "phone";
    const fb = box(frame);
    const v = {
      // innerBottom is the frame's inner edge; padB is the screen's own bottom padding as rendered (it scales
      // with a CSS zoom on the frame), so the blank check measures only space the layout didn't design.
      frame: { ...fb, kind, innerBottom: fb.b - num(fcs.borderBottomWidth), scrollH: 0, clientH: frame.clientHeight,
               padB: num(getComputedStyle(screen).paddingBottom) * (frame.offsetHeight ? fb.h / frame.offsetHeight : 1),
      radius: num(fcs.borderBottomRightRadius) * (frame.offsetWidth ? fb.w / frame.offsetWidth : 1) },
      screen: { ...box(screen), scrollH: 0, clientH: screen.clientHeight, scrollW: 0, clientW: screen.clientWidth },
      // Rendered size ÷ layout size: the CSS zoom the frame is drawn at (computed font sizes are unzoomed).
      zoom: frame.offsetWidth ? fb.w / frame.offsetWidth : 1,
      widest: null,
      topmost: null,
      lowest: null,
      texts: [],
      items: [],
      rings: [],
      stickies: [],
    };
    const ringEls = [...frame.querySelectorAll(RINGS)];
    const overlay = frame.querySelector(".r-overlay");
    const overlayEls = [...frame.querySelectorAll(".r-overlay")];
    const stickyEls = [...frame.querySelectorAll(".r-sticky")];

    // Labels hang outside their ring by design (and an absolutely positioned
    // label below the last element would count as overflow); hidden while
    // overflow is measured.
    const noLabels = document.createElement("style");
    noLabels.textContent = ".hl::after{display:none!important} .hl-soft::after{display:none!important}";
    document.head.appendChild(noLabels);
    v.frame.scrollH = frame.scrollHeight;
    v.screen.scrollH = screen.scrollHeight;
    v.screen.scrollW = screen.scrollWidth;
    const innerRight = screen.getBoundingClientRect().right;
    screen.querySelectorAll("*").forEach((el) => {
      if (el.closest(".r-overlay")) return;
      const b = el.getBoundingClientRect();
      if (!b.width) return;
      let right = b.right;
      if (el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflowX === "visible") {
        right = Math.max(right, b.left + el.scrollWidth);
      }
      const by = right - innerRight;
      if (by > 1 && (!v.widest || by > v.widest.px)) v.widest = { px: by, what: `“${short(el.textContent)}”` };
    });
    // Clipped at the top: no scroll size measures what sticks out upwards, so every element's top is read.
    const innerTop = screen.getBoundingClientRect().top + screen.clientTop;
    screen.querySelectorAll("*").forEach((el) => {
      const b = el.getBoundingClientRect();
      if (!b.width || !b.height) return;
      const up = innerTop - b.top;
      if (up > 1 && (!v.topmost || up > v.topmost.px)) v.topmost = { px: up, what: describe(el, (el.innerText || el.textContent).trim()) };
    });
    noLabels.remove();

    const paints = (cs) => {
      const bg = cs.backgroundColor;
      if (alpha(bg) > 0 && bg !== frameBg) return true;
      if (cs.backgroundImage && cs.backgroundImage !== "none") return true;
      return ["Top", "Right", "Bottom", "Left"].some(
        (side) => num(cs[`border${side}Width`]) > 0 && cs[`border${side}Style`] !== "none" && alpha(cs[`border${side}Color`]) > 0,
      );
    };
    const layersOf = (el) => {
      const layers = [];
      for (let n = el; n; n = n.parentElement) {
        const cs = getComputedStyle(n);
        const g = stops(cs.backgroundImage);
        if (g.length) {
          layers.unshift(g);
          if (g.every((c) => c[3] >= 1)) break;
        }
        const c = colour(cs.backgroundColor);
        if (c && c[3] > 0) {
          layers.unshift([c]);
          if (c[3] >= 1) break;
        }
        if (n === frame) break;
      }
      return layers;
    };
    const stickyOf = (el) => stickyEls.findIndex((st) => st === el || st.contains(el));

    frame.querySelectorAll("*").forEach((el) => {
      const cs = getComputedStyle(el);
      if (cs.display === "none" || cs.visibility === "hidden") return;
      const b = el.getBoundingClientRect();
      if (!b.width || !b.height) return;
      const textNodes = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim());
      const text = textNodes.map((n) => n.textContent).join(" ");
      const painted = paints(cs);
      const bar = stickyEls.includes(el);
      if (!text && !(painted && !el.children.length) && !bar) return;
      // Text rects only (no painted box): an ancestor's own text lies outside the ring it contains, so it counts.
      const glyphs = text && !painted && !bar;
      const skip = ringEls.map((hl, k) => (el === hl || hl.contains(el) || (el.contains(hl) && !glyphs) ? k : -1)).filter((k) => k >= 0);
      let rects = [box(el)];
      if (glyphs) {
        rects = [];
        for (const tn of textNodes) {
          const range = document.createRange();
          range.selectNodeContents(tn);
          for (const r of range.getClientRects()) rects.push({ x: r.left, y: r.top, r: r.right, b: r.bottom });
        }
      }
      const what = bar ? "the .r-sticky bar" : describe(el, text);
      // Under an overlay: outside it and inside the box it covers (dimmed by design).
      const dimmed = overlayEls.some((ov) => {
        if (ov.contains(el)) return false;
        const o = ov.getBoundingClientRect();
        return b.left >= o.left - 0.5 && b.right <= o.right + 0.5 && b.top >= o.top - 0.5 && b.bottom <= o.bottom + 0.5;
      });
      v.items.push({ what, rects, skip, dimmed, sticky: stickyOf(el) });
      if (!el.closest(".r-overlay") && (!v.lowest || b.bottom > v.lowest.y)) v.lowest = { y: b.bottom, what, inScreen: !!el.closest(".screen") };
      if (!text) return;
      v.texts.push({
        what,
        px: num(cs.fontSize),
        weight: num(cs.fontWeight) || 400,
        fg: colour(cs.color),
        layers: layersOf(el),
        dimmed: Boolean(overlay && screen.contains(el) && !overlay.contains(el)),
      });
    });
    stickyEls.forEach((st) => {
      v.stickies.push({ rect: box(st), firstView: !sheet && screen.contains(st) && !!st.closest(".phone") });
    });

    ringEls.forEach((hl) => {
      const hb = box(hl);
      const hcs = getComputedStyle(hl);
      const grow = num(hcs.outlineOffset) + num(hcs.outlineWidth);
      const ring = {
        note: hl.getAttribute("data-note") || "",
        grow,
        box: hb,
        soft: hl.classList.contains("hl-soft") && !hl.classList.contains("hl"),
        inSticky: Boolean(hl.closest(".r-sticky") || hl.querySelector(".r-sticky")),
        outline: { x: hb.x - grow, y: hb.y - grow, r: hb.r + grow, b: hb.b + grow },
        nested: ringEls.map((o, j) => (o !== hl && (o.contains(hl) || hl.contains(o)) ? j : -1)).filter((j) => j >= 0),
        overOverlay: Boolean(hl.parentElement && hl.parentElement.closest(".r-overlay")),
        label: null,
      };
      const cs = getComputedStyle(hl, "::after");
      if (hl.hasAttribute("data-note") && cs && cs.content !== "none" && cs.display !== "none") {
        const bb = cs.boxSizing === "border-box";
        const w = num(cs.width) + (bb ? 0 : num(cs.paddingLeft) + num(cs.paddingRight) + num(cs.borderLeftWidth) + num(cs.borderRightWidth));
        const h = num(cs.height) + (bb ? 0 : num(cs.paddingTop) + num(cs.paddingBottom) + num(cs.borderTopWidth) + num(cs.borderBottomWidth));
        // Positioned against the ring's padding box; top/right are used values (layout px: scaled by the zoom).
        const z = v.zoom || 1;
        const x2 = hb.r - (num(hcs.borderRightWidth) + num(cs.right)) * z;
        const y1 = hb.y + (num(hcs.borderTopWidth) + num(cs.top)) * z;
        ring.label = {
          rect: { x: x2 - w * z, y: y1, r: x2, b: y1 + h * z },
          pos: y1 >= hb.b - 1 ? "below" : "above",
          px: num(cs.fontSize),
          fg: colour(cs.color),
          bg: colour(cs.backgroundColor) || [0, 0, 0, 0],
        };
      }
      v.rings.push(ring);
    });
    return v;
  };

  // A stage caption: the first lettered text before the phone, after the previous phone (or the pill).
  const captionOf = (col, frame, prev) => {
    const walker = document.createTreeWalker(col, NodeFilter.SHOW_TEXT);
    let found = null;
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      const el = n.parentElement;
      if (!el || el.closest(".phone, .browser, .pill")) continue;
      if (prev && !(prev.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_FOLLOWING)) continue;
      if (!(frame.compareDocumentPosition(n) & Node.DOCUMENT_POSITION_PRECEDING)) break;
      if (!/\p{L}/u.test(n.textContent)) continue;
      const cs = getComputedStyle(el);
      const range = document.createRange();
      range.selectNodeContents(n);
      const r = range.getBoundingClientRect();
      const z = el.offsetWidth ? el.getBoundingClientRect().width / el.offsetWidth : 1;
      found = { text: short(n.textContent), px: Math.round(num(cs.fontSize) * z * 10) / 10, rect: { x: r.left, y: r.top, r: r.right, b: r.bottom } };
      break;
    }
    return found;
  };

  document.querySelectorAll(".stage > .variant").forEach((col, i) => {
    const frames = [...col.querySelectorAll(".phone, .browser")].filter((fr) => fr.querySelector(".screen, .browser-screen"));
    if (!frames.length) return;
    const first = measure(frames[0], frames[0].querySelector(".screen, .browser-screen"), false);
    const v = { name: i ? "B" : "A", column: box(col), ...first };
    if (frames.length > 1) {
      v.stages = frames.map((fr, j) => ({
        ...(j ? measure(fr, fr.querySelector(".screen, .browser-screen"), false) : first),
        caption: captionOf(col, fr, j ? frames[j - 1] : null),
      }));
    }
    const below = col.querySelector(".below");
    const sheet = below && below.querySelector(".below-screen");
    if (sheet) {
      const cap = below.querySelector(".below-cap");
      v.below = { ...measure(below, sheet, true), caption: cap && cap.textContent.trim() ? { text: short(cap.textContent) } : null };
    }
    out.variants.push(v);
  });
  return out;
}

// ---------------------------------------------------------------- main

async function main(argv) {
  const opts = parseArgs(argv);
  if (opts.error) {
    // A mistyped flag used to be dropped in silence ("--shots" ran with no screenshot).
    console.error(`render_check: ${opts.error}\n${USAGE}`);
    return 2;
  }
  const missing = opts.files.filter((f) => !fs.existsSync(path.resolve(f)));
  if (missing.length) {
    console.error(`render_check: no such file: ${missing.join(", ")}`);
    return 2;
  }
  const require = createRequire(import.meta.url);
  let playwright;
  try {
    playwright = require("playwright");
  } catch {
    console.error("render_check: playwright not found; set NODE_PATH to a node_modules that has it");
    return 2;
  }
  const launch = {};
  if (process.env.CHROMIUM_PATH) launch.executablePath = process.env.CHROMIUM_PATH;
  const browser = await playwright.chromium.launch(launch);
  const page = await browser.newPage({ viewport: { width: LIMITS.cardW, height: LIMITS.cardH } });
  let anyFailed = false;
  try {
    for (const file of opts.files) {
      const abs = path.resolve(file);
      await page.goto(pathToFileURL(abs).href);
      await page.evaluate(() => document.fonts && document.fonts.ready);
      const m = await page.evaluate(collect);
      const { errors, warnings } = judge(m, { strict: opts.strict });
      if (failed({ errors, warnings }, opts.strict)) anyFailed = true;
      let png = null;
      if (opts.shot) {
        const base = path.basename(abs, ".html").replace(/^abtest-card-/, "");
        png = path.join(path.dirname(abs), `card-${base}.png`);
        await page.screenshot({ path: png, fullPage: true });
      }
      if (opts.json) {
        const frames = m.variants.map((v) => ({ name: v.name, kind: v.frame.kind, x: v.frame.x, y: v.frame.y, w: v.frame.w, h: v.frame.h, column: v.column.w }));
        console.log(JSON.stringify({ file, device: m.device, card: [m.card.w, m.card.h], stage: [m.stage.w, m.stage.h], frames, errors, warnings, png }));
      } else {
        console.log(summary(file, m, png));
        for (const e of errors) console.log(`  ERROR ${e}`);
        for (const w of warnings) console.log(`  warn  ${w}`);
      }
    }
  } finally {
    await browser.close();
  }
  return anyFailed ? 1 : 0;
}

// Run only as a script; imported (the unit tests do), it only exports.
function isEntry() {
  try {
    return fs.realpathSync(process.argv[1]) === fs.realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}
if (isEntry()) process.exit(await main(process.argv.slice(2)));
