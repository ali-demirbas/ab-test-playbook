#!/usr/bin/env node
// Render built scenario cards in headless Chromium and measure what a reader
// would see: the card's size, the text column, frames overflowing their column,
// mockup content clipped by the screen (below it or past its right edge), ring
// labels covering other content, and how far B's content moved against A.
// Optionally writes a 1600px-wide screenshot.
//
// This is a manual/orchestrator tool, not part of the unit suite: the suite
// stays stdlib-only Python with structural asserts, and Playwright is a Node
// dependency this repo does not ship. Point it at an existing install:
//
//   NODE_PATH=/path/to/node_modules node scripts/render_check.mjs card.html [more.html ...]
//   CHROMIUM_PATH=/path/to/chrome-headless-shell node scripts/render_check.mjs --shot card.html
//
// --shot    write card-<name>.png next to each card (abtest-card-x.html → card-x.png)
// --json    print one JSON object per card instead of the table
// --strict  warnings count as failures (exit 1), for an orchestrator that must not ship one
//
// What the measurements mean
//
//   label covers …   The ring label (.hl[data-note]::after) is measured as the box
//                    that is painted: its border box. A pseudo-element is not
//                    matched by the template's `*{box-sizing:border-box}`, so its
//                    computed width/height are content-box values and the padding
//                    has to be added (leaving it out made the label 14px narrower
//                    and 6px shorter than it is). It is compared with everything
//                    in the frame that is not the ring itself: text, and also any
//                    element that paints a box of its own (a numbered step circle,
//                    a badge, a checkbox, a thumbnail, a filled button), where the
//                    label can sit on the shape without touching a glyph.
//   A/B shift        change / move: how far the same top-level block starts in B
//                    against A; content ABOVE the ringed element must not move.
//                    add / remove: the content below moves by the added element's
//                    own height plus the container gap, and that is reported as
//                    "added element height + gap = Npx". More than that means
//                    something else takes space (a margin on the ring, a wrapper
//                    that exists only in one variant) and is a warning.
//   clipped          against the SCREEN, not the frame: on a phone card with a tab
//                    bar the screen ends where the bar starts. Horizontal overflow
//                    is read from scrollWidth, because an overflowing line keeps
//                    its element box inside the screen.
//
// Exit: 0 = no hard failure, 1 = a hard failure (horizontal overflow, a frame
// wider than its column, a web card whose text column is under 520px; with
// --strict also any warning), 2 = usage.
import { createRequire } from "node:module";
import path from "node:path";
import fs from "node:fs";
import { pathToFileURL } from "node:url";

const USAGE = "usage: render_check.mjs [--shot] [--json] [--strict] card.html [more.html ...]";
const FLAGS = new Set(["--shot", "--json", "--strict"]);
const args = process.argv.slice(2);
const unknown = args.filter((a) => a.startsWith("--") && !FLAGS.has(a));
if (unknown.length) {
  // A mistyped flag used to be dropped in silence ("--shots" ran with no screenshot).
  console.error(`render_check: unknown option ${unknown.join(", ")}\n${USAGE}`);
  process.exit(2);
}
const shot = args.includes("--shot");
const asJson = args.includes("--json");
const strict = args.includes("--strict");
const files = args.filter((a) => !a.startsWith("--"));
if (!files.length) {
  console.error(USAGE);
  process.exit(2);
}

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  console.error("render_check: playwright not found; set NODE_PATH to a node_modules that has it");
  process.exit(2);
}

const launch = {};
if (process.env.CHROMIUM_PATH) launch.executablePath = process.env.CHROMIUM_PATH;
const browser = await playwright.chromium.launch(launch);
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });

let hardFail = false;
let anyWarn = false;
for (const file of files) {
  const abs = path.resolve(file);
  if (!fs.existsSync(abs)) {
    console.error(`render_check: no such file: ${file}`);
    hardFail = true;
    continue;
  }
  await page.goto(pathToFileURL(abs).href);
  await page.evaluate(() => document.fonts && document.fonts.ready);
  const m = await page.evaluate(() => {
    const px = (v) => parseFloat(v) || 0;
    const r = (el) => {
      const b = el.getBoundingClientRect();
      return { x: b.left, y: b.top, w: b.width, h: b.height, r: b.right, b: b.bottom };
    };
    const size = (sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const b = el.getBoundingClientRect();
      return [Math.round(b.width), Math.round(b.height)];
    };
    const overlap = (a, b) =>
      Math.max(0, Math.min(a.r, b.r) - Math.max(a.x, b.x)) * Math.max(0, Math.min(a.b, b.b) - Math.max(a.y, b.y));
    const alpha = (color) => {
      const m = /rgba?\(([^)]+)\)/.exec(color || "");
      if (!m) return 0;
      const parts = m[1].split(/[,/ ]+/).filter(Boolean);
      return parts.length > 3 ? parseFloat(parts[3]) : 1;
    };
    const short = (text) => {
      const t = (text || "").replace(/\s+/g, " ").trim();
      return t.length > 24 ? t.slice(0, 24) + "…" : t;
    };
    const name = (i) => (i ? "B" : "A");

    const card = document.querySelector(".card");
    const out = {
      device: card ? card.getAttribute("data-device") : null,
      card: size(".card"),
      mockups: size(".mockups"),
      copy: size(".copy"),
      page: [document.documentElement.scrollWidth, document.documentElement.scrollHeight],
      frameOverflow: [],
      clipped: [],
      labelProblems: [],
      shiftProblems: [],
      shift: null,
      shiftText: "n/a",
    };
    // A frame wider than its variant column spills into the neighbour.
    document.querySelectorAll(".variant").forEach((v, i) => {
      const frame = v.querySelector(".phone, .browser");
      if (frame && frame.getBoundingClientRect().width > v.getBoundingClientRect().width + 1) {
        out.frameOverflow.push(`variant ${name(i)}: frame ${Math.round(frame.getBoundingClientRect().width)}px > column ${Math.round(v.getBoundingClientRect().width)}px`);
      }
    });

    const screens = [...document.querySelectorAll(".screen, .browser-screen")];

    // ---- clipping, against the screen ------------------------------------
    // Ring labels are hidden while this is measured: a label hangs 7px past its
    // ring by design, and that is reported by the label check, not as clipped content.
    const noLabels = document.createElement("style");
    noLabels.textContent = ".hl::after{display:none!important}";
    document.head.appendChild(noLabels);
    screens.forEach((s, i) => {
      const sb = s.getBoundingClientRect();
      let lowest = 0;
      let widest = 0;
      let widestText = "";
      s.querySelectorAll("*").forEach((el) => {
        if (el.closest(".r-overlay")) return;
        const b = el.getBoundingClientRect();
        if (b.height > 0) lowest = Math.max(lowest, b.bottom);
        // Horizontal: an overflowing line keeps its element box inside the
        // screen, so the box alone cannot show it; scrollWidth can.
        let right = b.right;
        if (el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflowX === "visible") {
          right = Math.max(right, b.left + el.scrollWidth);
        }
        if (b.width > 0 && right - sb.right > widest + 0.5) {
          widest = right - sb.right;
          widestText = short(el.textContent);
        }
      });
      if (lowest > sb.bottom + 1) out.clipped.push(`variant ${name(i)}: ${Math.round(lowest - sb.bottom)}px below the screen`);
      if (widest > 1) out.clipped.push(`variant ${name(i)}: "${widestText}" overflows the screen by ${Math.round(widest)}px on the right`);
    });
    noLabels.remove();

    // ---- ring labels -----------------------------------------------------
    // The label's painted box, from the pseudo-element's computed style.
    const labelRect = (hl) => {
      const cs = getComputedStyle(hl, "::after");
      if (!cs || cs.content === "none" || cs.display === "none") return null;
      const bb = cs.boxSizing === "border-box";
      const w = px(cs.width) + (bb ? 0 : px(cs.paddingLeft) + px(cs.paddingRight) + px(cs.borderLeftWidth) + px(cs.borderRightWidth));
      const h = px(cs.height) + (bb ? 0 : px(cs.paddingTop) + px(cs.paddingBottom) + px(cs.borderTopWidth) + px(cs.borderBottomWidth));
      // Positioned against the ring's padding box. `top` and `right` are used
      // values here (pixels), whichever of top/bottom the stylesheet set.
      const hb = r(hl);
      const hcs = getComputedStyle(hl);
      const x2 = hb.r - px(hcs.borderRightWidth) - px(cs.right);
      const y1 = hb.y + px(hcs.borderTopWidth) + px(cs.top);
      return { x: x2 - w, y: y1, r: x2, b: y1 + h };
    };
    const ringOutline = (hl) => {
      const b = r(hl);
      const grow = px(getComputedStyle(hl).outlineOffset) + px(getComputedStyle(hl).outlineWidth);
      return { x: b.x - grow, y: b.y - grow, r: b.r + grow, b: b.b + grow };
    };

    screens.forEach((s, i) => {
      const frame = s.closest(".phone, .browser");
      const fr = r(frame);
      const frameBg = getComputedStyle(frame).backgroundColor;
      const paintsBox = (cs) => {
        const bg = cs.backgroundColor;
        if (alpha(bg) > 0 && bg !== frameBg) return true;
        if (cs.backgroundImage && cs.backgroundImage !== "none") return true;
        return ["Top", "Right", "Bottom", "Left"].some(
          (side) => px(cs[`border${side}Width`]) > 0 && cs[`border${side}Style`] !== "none" && alpha(cs[`border${side}Color`]) > 0,
        );
      };
      const allRings = [...frame.querySelectorAll(".hl")];
      s.querySelectorAll(".hl[data-note]").forEach((hl) => {
        const lab = labelRect(hl);
        if (!lab) return;
        const note = hl.getAttribute("data-note");
        const who = `variant ${name(i)} "${note}"`;
        if (lab.x < fr.x || lab.r > fr.r || lab.y < fr.y || lab.b > fr.b) {
          out.labelProblems.push(`${who}: label outside the frame`);
        }
        let worst = 0;
        let worstWhat = "";
        const hit = (rect, what) => {
          const area = overlap(lab, rect);
          if (area > worst) {
            worst = area;
            worstWhat = what;
          }
        };
        frame.querySelectorAll("*").forEach((el) => {
          if (el === hl || hl.contains(el) || el.contains(hl)) return;
          const cs = getComputedStyle(el);
          if (cs.display === "none" || cs.visibility === "hidden") return;
          const box = r(el);
          if (!box.w || !box.h) return;
          const text = [...el.childNodes].filter((n) => n.nodeType === 3 && n.textContent.trim()).map((n) => n.textContent).join(" ");
          const boxed = paintsBox(cs);
          if (text) {
            if (boxed) {
              // A digit in a filled circle, a badge, a button: the shape is the element.
              hit(box, `"${short(text)}"`);
            } else {
              const range = document.createRange();
              range.selectNodeContents(el);
              for (const tb of range.getClientRects()) hit({ x: tb.left, y: tb.top, r: tb.right, b: tb.bottom }, `"${short(text)}"`);
            }
          } else if (!el.children.length && boxed) {
            // No text, no children, but painted: an icon, a checkbox, a dot, a thumbnail.
            hit(box, `a ${Math.round(box.w)}×${Math.round(box.h)}px ${el.className ? "." + String(el.className).split(/\s+/)[0] : el.tagName.toLowerCase()} element`);
          }
        });
        allRings.forEach((other) => {
          if (other === hl || other.contains(hl) || hl.contains(other)) return;
          hit(ringOutline(other), `the ring "${other.getAttribute("data-note") || ""}"`);
          const ol = other.hasAttribute("data-note") ? labelRect(other) : null;
          if (ol) hit(ol, `the label "${other.getAttribute("data-note")}"`);
        });
        if (worst > 4) {
          const other = lab.b <= r(hl).y + 1 ? "below" : "above"; // the side the label is NOT on now
          out.labelProblems.push(`${who}: label covers ${Math.round(worst)}px² of ${worstWhat} (try data-pos="${other}")`);
        }
      });
    });

    // ---- layout shift between A and B -------------------------------------
    if (screens.length === 2) {
      const [sa, sb] = screens;
      const tops = (s) => {
        const o = s.getBoundingClientRect().top;
        return [...s.children].filter((c) => getComputedStyle(c).display !== "none").map((c) => ({ el: c, top: c.getBoundingClientRect().top - o }));
      };
      const ringsA = [...sa.querySelectorAll(".hl")];
      const ringsB = [...sb.querySelectorAll(".hl")];
      const maxDiff = (a, b) => a.reduce((mx, x, j) => Math.max(mx, Math.abs(x.top - b[j].top)), 0);
      const withHidden = (rings, fn) => {
        const saved = rings.map((el) => el.style.display);
        rings.forEach((el) => (el.style.display = "none"));
        try {
          return fn();
        } finally {
          rings.forEach((el, j) => (el.style.display = saved[j]));
        }
      };
      // What a ringed element legitimately takes: its own height, plus one gap
      // of its container when it has a sibling to be separated from.
      const footprint = (rings) =>
        rings.reduce(
          (acc, hl) => {
            const parent = hl.parentElement;
            const pcs = getComputedStyle(parent);
            const stacked = (pcs.display.includes("flex") && pcs.flexDirection.startsWith("column")) || pcs.display.includes("grid");
            const gap = stacked && parent.children.length > 1 ? px(pcs.rowGap) : 0;
            return { height: acc.height + hl.getBoundingClientRect().height, gap: acc.gap + gap };
          },
          { height: 0, gap: 0 },
        );

      const onlyIn = ringsA.length && !ringsB.length ? "A" : ringsB.length && !ringsA.length ? "B" : null;
      const a0 = tops(sa);
      const b0 = tops(sb);
      if (onlyIn && a0.length === b0.length && a0.length) {
        // add / remove inside a block both screens have (the ring wraps the group that
        // gained or lost the element, or sits inside one): that block changes height
        // and everything below follows. Nothing else may move.
        const kind = onlyIn === "B" ? "added" : "removed";
        const ringed = onlyIn === "B" ? b0 : a0;
        const j = ringed.findIndex((t) => t.el.matches(".hl") || t.el.querySelector(".hl"));
        const growth = j === -1 ? 0 : Math.abs(b0[j].el.getBoundingClientRect().height - a0[j].el.getBoundingClientRect().height);
        const shift = maxDiff(a0, b0);
        out.shift = Math.round(shift);
        out.shiftText = `${Math.round(shift)}px (the block holding the ${kind} element is ${Math.round(growth)}px ${onlyIn === "B" ? "taller" : "shorter"} in B)`;
        if (shift > growth + 1) {
          out.shiftProblems.push(`${onlyIn === "B" ? "add" : "remove"}: content moves ${Math.round(shift)}px, more than the ${Math.round(growth)}px the ringed block changed by: ${Math.round(shift - growth)}px comes from something else`);
        }
      } else if (onlyIn) {
        // add (ring only in B) or remove (ring only in A) as a block of its own: one
        // screen has a block the other lacks.
        const rings = onlyIn === "B" ? ringsB : ringsA;
        const kind = onlyIn === "B" ? "added" : "removed";
        const top = rings.filter((el) => !rings.some((o) => o !== el && o.contains(el)));
        const fp = footprint(top);
        const expected = fp.height + fp.gap;
        // With the ringed element gone, the two screens must line up exactly.
        const residual = withHidden(top, () => {
          const a1 = tops(sa);
          const b1 = tops(sb);
          return a1.length === b1.length ? maxDiff(a1, b1) : null;
        });
        // The real shift: the blocks that survive hiding, measured with the ring in place.
        let shift = null;
        const keepA = withHidden(top, () => tops(sa).map((t) => t.el));
        const keepB = withHidden(top, () => tops(sb).map((t) => t.el));
        if (keepA.length === keepB.length && keepA.length) {
          const oa = sa.getBoundingClientRect().top;
          const ob = sb.getBoundingClientRect().top;
          shift = keepA.reduce((mx, el, j) => Math.max(mx, Math.abs((el.getBoundingClientRect().top - oa) - (keepB[j].getBoundingClientRect().top - ob))), 0);
        }
        if (shift !== null) {
          out.shift = Math.round(shift);
          out.shiftText = `${Math.round(shift)}px (${kind} element height ${Math.round(fp.height)}px + gap ${Math.round(fp.gap)}px = ${Math.round(expected)}px)`;
          if (shift > expected + 1) {
            out.shiftProblems.push(`${onlyIn === "B" ? "add" : "remove"}: content moves ${Math.round(shift)}px, more than the ${kind} element's own height + gap (${Math.round(expected)}px): ${Math.round(shift - expected)}px comes from something else (a margin on the ring or a wrapper that exists only in ${onlyIn}?)`);
          }
        } else {
          out.shiftText = `n/a (${kind} element height ${Math.round(fp.height)}px + gap ${Math.round(fp.gap)}px = ${Math.round(expected)}px)`;
        }
        if (residual === null) {
          out.shiftProblems.push(`${onlyIn === "B" ? "add" : "remove"}: with the ringed element hidden, A and B still have a different number of blocks: a second difference`);
        } else if (residual > 1) {
          out.shiftProblems.push(`${onlyIn === "B" ? "add" : "remove"}: with the ringed element hidden, B still differs from A by ${Math.round(residual)}px: a second difference`);
        }
      } else if (a0.length === b0.length && a0.length) {
        // change / move (or an add inside a block): the same blocks in both screens.
        const shift = maxDiff(a0, b0);
        out.shift = Math.round(shift);
        out.shiftText = `${Math.round(shift)}px`;
        const firstRing = (list) => {
          const idx = list.findIndex((t) => t.el.matches(".hl") || t.el.querySelector(".hl"));
          return idx === -1 ? list.length : idx;
        };
        const until = Math.min(firstRing(a0), firstRing(b0));
        for (let j = 0; j < until; j++) {
          const d = Math.abs(a0[j].top - b0[j].top);
          if (d > 1) {
            out.shiftProblems.push(`content above the ringed element starts ${Math.round(d)}px apart in A and B (block ${j + 1}, "${short(a0[j].el.textContent)}"): it should not move`);
            break;
          }
        }
      }
      // A ring that takes space of its own, whatever the difference type.
      [...ringsA.map((el) => ["A", el]), ...ringsB.map((el) => ["B", el])].forEach(([v, hl]) => {
        const cs = getComputedStyle(hl);
        const extra = ["marginTop", "marginBottom", "paddingTop", "paddingBottom"].filter((k) => hl.style[k] && px(cs[k]) > 0);
        if (extra.length) {
          const total = extra.reduce((sum, k) => sum + px(cs[k]), 0);
          out.shiftProblems.push(`ring in ${v} "${hl.getAttribute("data-note") || ""}" carries inline ${extra.map((k) => k.replace(/([A-Z])/g, "-$1").toLowerCase()).join(", ")}: it pushes content by ${Math.round(total)}px`);
        }
      });
    }
    return out;
  });

  const fails = [];
  if (m.page[0] > 1600) fails.push(`horizontal overflow: page is ${m.page[0]}px wide`);
  if (m.frameOverflow.length) fails.push(...m.frameOverflow);
  if (m.device === "web" && m.copy && m.copy[0] < 520) fails.push(`web text column ${m.copy[0]}px < 520px`);
  const warns = [...m.clipped.map((c) => `clipped: ${c}`), ...m.labelProblems, ...m.shiftProblems.map((s) => `shift: ${s}`)];
  if (m.card && m.card[1] > 1150) {
    warns.push(`card is ${m.card[1]}px tall (far from landscape): the text column sets the height, shorten the box items or the description`);
  }
  if (fails.length) hardFail = true;
  if (warns.length) anyWarn = true;

  let png = null;
  if (shot) {
    const base = path.basename(abs, ".html").replace(/^abtest-card-/, "");
    png = path.join(path.dirname(abs), `card-${base}.png`);
    await page.screenshot({ path: png, fullPage: true });
  }

  if (asJson) {
    console.log(JSON.stringify({ file, ...m, fails, warns, png }));
  } else {
    console.log(`${path.basename(file)}  device=${m.device}  card=${m.card?.join("x")}  mockups=${m.mockups?.[0]}  copy=${m.copy?.[0]}  A/B shift=${m.shiftText}${png ? "  → " + path.basename(png) : ""}`);
    for (const f of fails) console.log(`  FAIL ${f}`);
    for (const w of warns) console.log(`  warn ${w}`);
  }
}
await browser.close();
process.exit(hardFail || (strict && anyWarn) ? 1 : 0);
