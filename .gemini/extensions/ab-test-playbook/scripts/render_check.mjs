#!/usr/bin/env node
// Render built scenario cards in headless Chromium and measure what a reader
// would see: the card's size, the text column, frames overflowing their column,
// mockup content clipped by the frame, ring labels covering other content, and
// layout shift between A and B. Optionally writes a 1600px-wide screenshot.
//
// This is a manual/orchestrator tool, not part of the unit suite: the suite
// stays stdlib-only Python with structural asserts, and Playwright is a Node
// dependency this repo does not ship. Point it at an existing install:
//
//   NODE_PATH=/path/to/node_modules node scripts/render_check.mjs card.html [more.html ...]
//   CHROMIUM_PATH=/path/to/chrome-headless-shell node scripts/render_check.mjs --shot card.html
//
// --shot   write card-<name>.png next to each card (abtest-card-x.html → card-x.png)
// --json   print one JSON object per card instead of the table
//
// Exit: 0 = no hard failure, 1 = a hard failure (horizontal overflow, a frame
// wider than its column, a web card whose text column is under 520px), 2 = usage.
import { createRequire } from "node:module";
import path from "node:path";
import fs from "node:fs";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
let playwright;
try {
  playwright = require("playwright");
} catch {
  console.error("render_check: playwright not found; set NODE_PATH to a node_modules that has it");
  process.exit(2);
}

const args = process.argv.slice(2);
const shot = args.includes("--shot");
const asJson = args.includes("--json");
const files = args.filter((a) => !a.startsWith("--"));
if (!files.length) {
  console.error("usage: render_check.mjs [--shot] [--json] card.html [more.html ...]");
  process.exit(2);
}

const launch = {};
if (process.env.CHROMIUM_PATH) launch.executablePath = process.env.CHROMIUM_PATH;
const browser = await playwright.chromium.launch(launch);
const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });

let hardFail = false;
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
      shift: null,
    };
    // A frame wider than its variant column spills into the neighbour.
    document.querySelectorAll(".variant").forEach((v, i) => {
      const frame = v.querySelector(".phone, .browser");
      if (frame && frame.getBoundingClientRect().width > v.getBoundingClientRect().width + 1) {
        out.frameOverflow.push(`variant ${i ? "B" : "A"}: frame ${Math.round(frame.getBoundingClientRect().width)}px > column ${Math.round(v.getBoundingClientRect().width)}px`);
      }
    });
    // Content cut off by the frame's fixed height (overflow:hidden on the frame).
    const screens = [...document.querySelectorAll(".screen, .browser-screen")];
    screens.forEach((s, i) => {
      const frame = s.closest(".phone, .browser");
      const limit = frame.getBoundingClientRect().bottom;
      let lowest = 0;
      s.querySelectorAll("*").forEach((el) => {
        if (el.closest(".r-overlay")) return;
        const b = el.getBoundingClientRect();
        if (b.height > 0) lowest = Math.max(lowest, b.bottom);
      });
      if (lowest > limit + 1) out.clipped.push(`variant ${i ? "B" : "A"}: ${Math.round(lowest - limit)}px below the frame`);
    });
    // Ring labels: ::after geometry from computed style, then compare against
    // every text-bearing element that is not inside the ring itself.
    screens.forEach((s, i) => {
      const frame = s.closest(".phone, .browser");
      const fr = r(frame);
      s.querySelectorAll(".hl[data-note]").forEach((hl) => {
        const cs = getComputedStyle(hl, "::after");
        const hb = r(hl);
        const w = parseFloat(cs.width), h = parseFloat(cs.height);
        const right = parseFloat(cs.right), top = parseFloat(cs.top), bottom = parseFloat(cs.bottom);
        const x2 = hb.r - right, x1 = x2 - w;
        const y1 = cs.top !== "auto" && !Number.isNaN(top) ? hb.y + top : hb.b - bottom - h;
        const lab = { x: x1, y: y1, r: x2, b: y1 + h };
        const note = hl.getAttribute("data-note");
        if (lab.x < fr.x || lab.r > fr.r || lab.y < fr.y || lab.b > fr.b) {
          out.labelProblems.push(`variant ${i ? "B" : "A"} "${note}": label outside the frame`);
        }
        let worst = 0;
        s.querySelectorAll("*").forEach((el) => {
          if (el === hl || hl.contains(el) || el.contains(hl)) return;
          const hasText = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
          if (!hasText) return;
          const range = document.createRange();
          range.selectNodeContents(el);
          for (const tb of range.getClientRects()) {
            worst = Math.max(worst, overlap(lab, { x: tb.left, y: tb.top, r: tb.right, b: tb.bottom }));
          }
        });
        if (worst > 4) out.labelProblems.push(`variant ${i ? "B" : "A"} "${note}": label covers ${Math.round(worst)}px² of text (try data-pos="below")`);
      });
    });
    // Layout shift between A and B: when both screens have the same number of
    // top-level blocks (change/move tests), block j should start at the same
    // offset in both. A ring that took layout space (the old border+padding
    // ring) shows up here as a non-zero shift; add/remove tests are n/a.
    if (screens.length === 2) {
      const [ka, kb] = screens.map((s) => [...s.children]);
      const oa = screens[0].getBoundingClientRect().top, ob = screens[1].getBoundingClientRect().top;
      if (ka.length === kb.length) {
        let maxd = 0;
        ka.forEach((a, j) => {
          maxd = Math.max(maxd, Math.abs((a.getBoundingClientRect().top - oa) - (kb[j].getBoundingClientRect().top - ob)));
        });
        out.shift = Math.round(maxd);
      }
    }
    return out;
  });

  const fails = [];
  if (m.page[0] > 1600) fails.push(`horizontal overflow: page is ${m.page[0]}px wide`);
  if (m.frameOverflow.length) fails.push(...m.frameOverflow);
  if (m.device === "web" && m.copy && m.copy[0] < 520) fails.push(`web text column ${m.copy[0]}px < 520px`);
  const warns = [...m.clipped.map((c) => `clipped: ${c}`), ...m.labelProblems];
  if (m.card && m.card[1] > 1150) warns.push(`card is ${m.card[1]}px tall (far from landscape)`);
  if (fails.length) hardFail = true;

  let png = null;
  if (shot) {
    const base = path.basename(abs, ".html").replace(/^abtest-card-/, "");
    png = path.join(path.dirname(abs), `card-${base}.png`);
    await page.screenshot({ path: png, fullPage: true });
  }

  if (asJson) {
    console.log(JSON.stringify({ file, ...m, fails, warns, png }));
  } else {
    console.log(`${path.basename(file)}  device=${m.device}  card=${m.card?.join("x")}  mockups=${m.mockups?.[0]}  copy=${m.copy?.[0]}  A/B shift=${m.shift ?? "n/a"}px${png ? "  → " + path.basename(png) : ""}`);
    for (const f of fails) console.log(`  FAIL ${f}`);
    for (const w of warns) console.log(`  warn ${w}`);
  }
}
await browser.close();
process.exit(hardFail ? 1 : 0);
