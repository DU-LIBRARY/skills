// Convert a Slides artifact (project/ folder) into a .pptx: background image + editable text + Arabic as images.
const { chromium } = require('playwright');
const pptxgen = require('pptxgenjs');
const sharp = require('sharp');
const fs = require('fs'), path = require('path');
const [, , projDir, outFile] = process.argv;
const deck = JSON.parse(fs.readFileSync(path.join(projDir, 'deck.json'), 'utf8'));
const css = fs.readFileSync(path.join(projDir, 'deck.css'), 'utf8');
const links = Object.values(deck.faces).map(f => `<link rel="stylesheet" href="${f.href}">`).join('');
const BASE = `body{margin:0}section{position:relative;display:block;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}aside{display:none}*{animation:none!important;transition:none!important}`;
const PX = 1 / 144;                       // 1920px slide = 13.333in
const hex = c => { const m = c.match(/\d+(\.\d+)?/g).map(Number); return m.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(); };
function face(fam, wt) {
  fam = fam.split(',')[0].replace(/['"]/g, '').trim();
  if (/fell/i.test(fam)) return { face: 'IM FELL English', bold: false };
  if (/garamond/i.test(fam)) {
    if (wt >= 700) return { face: 'EB Garamond', bold: true };
    if (wt >= 600) return { face: 'EB Garamond SemiBold', bold: false };
    if (wt >= 500) return { face: 'EB Garamond Medium', bold: false };
    return { face: 'EB Garamond', bold: false };
  }
  return { face: fam, bold: wt >= 600 };
}
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const pageHi = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = deck.title;
  const work = path.join(path.dirname(outFile), 'work-' + path.basename(outFile, '.pptx')); fs.mkdirSync(work, { recursive: true });
  const anim = {};                         // slide index -> [[groupNo, objectName], ...]
  for (const [si, id] of deck.order.entries()) {
    const sec = fs.readFileSync(path.join(projDir, 'slides', id + '.html'), 'utf8');
    const html = `<!DOCTYPE html><html><head><meta charset="utf-8">${links}<style>${BASE}${css}</style></head><body>${sec}</body></html>`;
    const file = path.join(work, id + '.html'); fs.writeFileSync(file, html);
    await page.goto('file://' + file); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
    // --- collect text blocks
    const blocks = await page.evaluate((slideNo) => {
      const out = [], ar = /[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]/g, lat = /[A-Za-z]/g;
      const sec = document.querySelector('section');
      const els = [...sec.querySelectorAll('p,h1,h2,h3,.num')].filter(e => !e.closest('aside') && !e.closest('svg'));
      els.forEach((el, k) => {
        const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
        if (r.width === 0 || cs.visibility === 'hidden') return;
        const txt = el.classList.contains('num') ? String(slideNo) : el.innerText;
        if (!txt.trim()) return;
        const nAr = (txt.match(ar) || []).length, nLat = (txt.match(lat) || []).length;
        const isAr = el.classList.contains('ar') || cs.direction === 'rtl' || nAr > nLat;
        const g = el.closest('.d1,.d2,.d3,.d4'); const group = g ? +[...g.classList].find(c => /^d[1-4]$/.test(c)).slice(1) : 0;
        const runs = [];
        if (el.classList.contains('num')) runs.push({ t: txt, s: cs });
        else (function walk(n) {
          for (const c of n.childNodes) {
            if (c.nodeType === 3) { if (c.textContent) runs.push({ t: c.textContent, s: getComputedStyle(c.parentElement) }); }
            else if (c.nodeName === 'BR') runs.push({ br: true });
            else if (c.nodeType === 1) walk(c);
          }
        })(el);
        const mk = s => ({ color: s.color, italic: s.fontStyle === 'italic', weight: +s.fontWeight, family: s.fontFamily, size: parseFloat(s.fontSize), upper: s.textTransform === 'uppercase' });
        el.dataset.k = k;
        out.push({ k, isAr, group, x: r.left, y: r.top, w: r.width, h: r.height,
          size: parseFloat(cs.fontSize), lh: cs.lineHeight === 'normal' ? 1.2 * parseFloat(cs.fontSize) : parseFloat(cs.lineHeight),
          ls: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing), align: cs.textAlign, cls: el.className,
          runs: runs.map(r => r.br ? { br: true } : { t: r.t.replace(/\s+/g, ' '), ...mk(r.s) }) });
      });
      return out;
    }, si + 1);
    // --- background: everything except text
    await page.addStyleTag({ content: 'section, section * { color: transparent !important; text-shadow: none !important; }' });
    const bg = path.join(work, id + '-bg.jpg');
    await page.screenshot({ path: bg, type: 'jpeg', quality: 90 });
    // --- Arabic layer at 2x on transparent background
    const arKs = blocks.filter(b => b.isAr).map(b => b.k);
    let arPng = null;
    if (arKs.length) {
      await pageHi.goto('file://' + file); await pageHi.evaluate(() => document.fonts.ready); await pageHi.waitForTimeout(400);
      await pageHi.evaluate((ks) => {
        const els = [...document.querySelector('section').querySelectorAll('p,h1,h2,h3,.num')].filter(e => !e.closest('aside') && !e.closest('svg'));
        ks.forEach(k => els[k].classList.add('__ar'));
      }, arKs);
      await pageHi.addStyleTag({ content: `html,body,section{background:transparent!important}
        section *{visibility:hidden!important;background:transparent!important;border-color:transparent!important}
        section svg{display:none!important}
        section .__ar, section .__ar *{visibility:visible!important}` });
      arPng = path.join(work, id + '-ar.png');
      await pageHi.screenshot({ path: arPng, omitBackground: true });
    }
    // --- build the slide
    const slide = pres.addSlide();
    slide.background = { path: bg };
    anim[si] = [];
    let n = 0;
    for (const b of blocks) {
      const name = `a${b.group}_${n++}`;
      if (b.isAr) {
        const pad = 6, L = Math.max(0, Math.floor(b.x - pad)), T = Math.max(0, Math.floor(b.y - pad));
        const W = Math.min(1920 - L, Math.ceil(b.w + 2 * pad)), Hh = Math.min(1080 - T, Math.ceil(b.h + 2 * pad));
        const ext = await sharp(arPng).extract({ left: L * 2, top: T * 2, width: W * 2, height: Hh * 2 }).png().toBuffer();
        let crop;
        try { crop = await sharp(ext).trim({ threshold: 1 }).toBuffer({ resolveWithObject: true }); }
        catch (e) { console.log('  untrimmed:', id, b.cls, JSON.stringify(b.runs.map(r => r.t).join('')).slice(0, 40)); crop = await sharp(ext).toBuffer({ resolveWithObject: true }); }
        const info = crop.info; // trimmed: offsets are negative left/top shifts
        const ox = L + (-(info.trimOffsetLeft || 0)) / 2, oy = T + (-(info.trimOffsetTop || 0)) / 2;
        slide.addImage({ data: 'image/png;base64,' + crop.data.toString('base64'), x: ox * PX, y: oy * PX, w: info.width / 2 * PX, h: info.height / 2 * PX,
          objectName: name, altText: b.runs.map(r => r.t || ' ').join('') });
      } else {
        const runs = [];
        b.runs.forEach((r, i) => {
          if (r.br) { if (runs.length) runs[runs.length - 1].options.breakLine = true; return; }
          const f = face(r.family, r.weight);
          runs.push({ text: r.upper ? r.t.toUpperCase() : r.t, options: { color: hex(r.color), italic: r.italic, bold: f.bold, fontFace: f.face, fontSize: r.size / 2 } });
        });
        if (!runs.length) continue;
        runs[0].text = runs[0].text.replace(/^\s+/, ''); runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/\s+$/, '');
        const slack = Math.min(b.w * 0.07, 60);
        let x = b.x, w = b.w + slack;
        if (/\bnum\b/.test(b.cls)) { x = b.x - 40; w = b.w + 80; b.align = 'center'; }
        if (b.align === 'center') x -= slack / 2; else if (b.align === 'right' || b.align === 'end') x -= slack;
        slide.addText(runs, { x: x * PX, y: b.y * PX, w: w * PX, h: b.h * PX, margin: 0, valign: 'top', isTextBox: true,
          align: b.align === 'center' ? 'center' : (b.align === 'right' || b.align === 'end') ? 'right' : 'left',
          lineSpacing: +(b.lh / 2).toFixed(1), charSpacing: b.ls ? +(b.ls / 2).toFixed(2) : undefined,
          paraSpaceBefore: 0, paraSpaceAfter: 0, fit: 'none', objectName: name });
      }
      if (b.group) anim[si].push([b.group, name]);
    }
    const notes = (sec.match(/<aside>([\s\S]*?)<\/aside>/) || [, ''])[1]
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").trim();
    if (notes) slide.addNotes(notes);
    console.log(id, 'text', blocks.filter(b => !b.isAr).length, 'arabic', arKs.length);
  }
  await pres.writeFile({ fileName: outFile });
  fs.writeFileSync(outFile + '.anim.json', JSON.stringify(anim));
  await browser.close();
})();
