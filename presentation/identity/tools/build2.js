// Native conversion: HTML slide -> PowerPoint shapes (rects, lines), pictures (svg/img), editable text, Arabic as images.
const { chromium } = require('playwright'); const pptxgen = require('pptxgenjs'); const sharp = require('sharp');
const fs = require('fs'), path = require('path');
const [, , deckDir, outFile, bgHex] = process.argv;           // deckDir holds prev-<id>.html and project/
const deck = JSON.parse(fs.readFileSync(path.join(deckDir, 'project/deck.json'), 'utf8'));
const PX = 1 / 144;
const rgb = c => (c.match(/[\d.]+/g) || []).map(Number);
const hex = c => rgb(c).slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
const alpha = c => { const m = rgb(c); return m.length > 3 ? m[3] : 1; };
function face(fam, wt) {
  fam = fam.split(',')[0].replace(/['"]/g, '').trim();
  if (/fell/i.test(fam)) return { face: 'IM FELL English', bold: false };
  if (/garamond/i.test(fam)) return wt >= 700 ? { face: 'EB Garamond', bold: true } : wt >= 600 ? { face: 'EB Garamond SemiBold', bold: false } : wt >= 500 ? { face: 'EB Garamond Medium', bold: false } : { face: 'EB Garamond', bold: false };
  return { face: fam, bold: wt >= 600 };
}
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const hi = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = deck.title;
  const work = outFile.replace(/\.pptx$/, '-work'); fs.mkdirSync(work, { recursive: true });
  const svgCache = new Map(); let svgN = 0;
  for (const [si, id] of deck.order.entries()) {
    const file = path.join(deckDir, `prev-${id}.html`);
    for (const p of [page, hi]) { await p.goto('file://' + file); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300); }
    const items = await page.evaluate(() => {
      const sec = document.querySelector('section'); const out = []; let k = 0;
      const arRe = /[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]/g, latRe = /[A-Za-z]/g;
      const grp = el => { const g = el.closest('.d1,.d2,.d3'); return g ? +[...g.classList].find(c => /^d[123]$/.test(c)).slice(1) : 0; };
      const box = el => { const r = el.getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; };
      (function walk(el) {
        for (const c of el.children) {
          if (c.tagName === 'ASIDE' || c.classList.contains('grain')) continue;
          const cs = getComputedStyle(c);
          if (c.tagName.toLowerCase() === 'svg') { c.dataset.k = k; out.push({ k: k++, t: 'svg', g: grp(c), ...box(c) }); continue; }
          if (c.tagName === 'IMG') { out.push({ k: k++, t: 'img', src: c.src, g: grp(c), ...box(c) }); continue; }
          const b = box(c);
          const bg = cs.backgroundColor; const sides = ['Top', 'Right', 'Bottom', 'Left'].map(s => ({ s, w: parseFloat(cs['border' + s + 'Width']), c: cs['border' + s + 'Color'], st: cs['border' + s + 'Style'] }));
          const shape = { k: k++, t: 'box', g: grp(c), ...b, bg, sides };
          if (!/rgba\(0, 0, 0, 0\)|transparent/.test(bg) || sides.some(s => s.w > 0 && s.st !== 'none')) out.push(shape);
          if (/^(P|H1|H2|H3)$/.test(c.tagName)) {
            const txt = c.innerText; if (!txt.trim()) continue;
            const nAr = (txt.match(arRe) || []).length, nLat = (txt.match(latRe) || []).length;
            const isAr = c.classList.contains('ar') || nAr > nLat;
            const runs = [];
            (function w2(n) { for (const x of n.childNodes) { if (x.nodeType === 3) { if (x.textContent) { const s = getComputedStyle(x.parentElement); runs.push({ t: x.textContent.replace(/\s+/g, ' '), color: s.color, italic: s.fontStyle === 'italic', weight: +s.fontWeight, family: s.fontFamily, size: parseFloat(s.fontSize) }); } } else if (x.nodeName === 'BR') runs.push({ br: true }); else if (x.nodeType === 1) w2(x); } })(c);
            c.dataset.tk = k;
            out.push({ k: k++, t: isAr ? 'ar' : 'text', g: grp(c), ...b, size: parseFloat(cs.fontSize), lh: cs.lineHeight === 'normal' ? 1.2 * parseFloat(cs.fontSize) : parseFloat(cs.lineHeight),
              ls: cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing), align: cs.textAlign, runs, alt: txt });
            continue;
          }
          walk(c);
        }
      })(sec);
      return out;
    });
    // Arabic layer, transparent, 2x
    const arKs = items.filter(i => i.t === 'ar').map(i => i.k);
    let arPng = null;
    if (arKs.length) {
      await hi.evaluate((ks) => { document.querySelectorAll('[data-tk]').forEach(e => { if (ks.includes(+e.dataset.tk)) e.classList.add('__ar'); }); }, arKs);
      // the hi page has not run the collector; re-tag by running same walk order
      await hi.evaluate(() => {});
      await hi.addStyleTag({ content: 'html,body,section{background:transparent!important} section *{visibility:hidden!important;background:transparent!important;border-color:transparent!important} section svg, section img{display:none!important} section .__ar, section .__ar *{visibility:visible!important}' });
    }
    // tag Arabic elements on hi page by geometry instead (robust): mark elements whose box matches
    if (arKs.length) {
      const boxes = items.filter(i => i.t === 'ar').map(i => [i.x, i.y, i.w, i.h]);
      await hi.evaluate((bx) => { for (const e of document.querySelectorAll('section p, section h1, section h2, section h3')) { const r = e.getBoundingClientRect(); if (bx.some(b => Math.abs(b[0] - r.left) < 1 && Math.abs(b[1] - r.top) < 1 && Math.abs(b[2] - r.width) < 1)) e.classList.add('__ar'); } }, boxes);
      arPng = path.join(work, id + '-ar.png'); await hi.screenshot({ path: arPng, omitBackground: true });
    }
    const slide = pres.addSlide(); slide.background = { color: bgHex };
    for (const it of items) {
      const name = `a${it.g}_${it.k}`;
      if (it.t === 'svg') {
        const el = await page.$(`svg[data-k="${it.k}"]`); const html = await el.evaluate(e => e.outerHTML);
        let p = svgCache.get(html);
        if (!p) { p = path.join(work, `svg${svgN++}.png`); await hi.goto('about:blank'); await hi.setContent(`<body style="margin:0;background:transparent">${html}</body>`); await (await hi.$('svg')).screenshot({ path: p, omitBackground: true }); svgCache.set(html, p);
                  await hi.goto('file://' + file); }
        slide.addImage({ path: p, x: it.x * PX, y: it.y * PX, w: it.w * PX, h: it.h * PX, objectName: name, altText: '' });
      } else if (it.t === 'img') {
        slide.addImage({ path: decodeURIComponent(it.src.replace('file://', '')), x: it.x * PX, y: it.y * PX, w: it.w * PX, h: it.h * PX, objectName: name, altText: 'Institute calligraphy or logo' });
      } else if (it.t === 'box') {
        const { x, y, w, h } = it; const S = it.sides; const all = S.every(s => s.w === S[0].w && s.w > 0 && s.c === S[0].c && s.st === S[0].st);
        const fill = alpha(it.bg) > 0 ? { color: hex(it.bg) } : undefined;
        if (all || fill) {
          const bw = all ? S[0].w : 0;
          slide.addShape(pres.shapes.RECTANGLE, { x: (x + bw / 2) * PX, y: (y + bw / 2) * PX, w: (w - bw) * PX, h: (h - bw) * PX, fill: fill || { type: 'none' },
            line: all ? { color: hex(S[0].c), width: bw / 2 } : { type: 'none' }, objectName: all && !fill ? name : name });
        }
        if (!all) for (const s of S) {
          if (!(s.w > 0) || s.st === 'none') continue;
          const o = { line: { color: hex(s.c), width: s.w / 2, dashType: s.st === 'dotted' ? 'sysDot' : s.st === 'dashed' ? 'dash' : 'solid' }, objectName: name + s.s[0] };
          if (s.s === 'Top') slide.addShape(pres.shapes.LINE, { x: x * PX, y: (y + s.w / 2) * PX, w: w * PX, h: 0, ...o });
          if (s.s === 'Bottom') slide.addShape(pres.shapes.LINE, { x: x * PX, y: (y + h - s.w / 2) * PX, w: w * PX, h: 0, ...o });
          if (s.s === 'Left') slide.addShape(pres.shapes.LINE, { x: (x + s.w / 2) * PX, y: y * PX, w: 0, h: h * PX, ...o });
          if (s.s === 'Right') slide.addShape(pres.shapes.LINE, { x: (x + w - s.w / 2) * PX, y: y * PX, w: 0, h: h * PX, ...o });
        }
      } else if (it.t === 'ar') {
        const pad = 8, L = Math.max(0, Math.floor(it.x - pad)), T = Math.max(0, Math.floor(it.y - pad));
        const W = Math.min(1920 - L, Math.ceil(it.w + 2 * pad)), H = Math.min(1080 - T, Math.ceil(it.h + 2 * pad));
        const ext = await sharp(arPng).extract({ left: L * 2, top: T * 2, width: W * 2, height: H * 2 }).png().toBuffer();
        let c; try { c = await sharp(ext).trim({ threshold: 1 }).toBuffer({ resolveWithObject: true }); } catch (e) { console.log('  blank arabic', id, it.alt); continue; }
        const ox = L - (c.info.trimOffsetLeft || 0) / 2, oy = T - (c.info.trimOffsetTop || 0) / 2;
        slide.addImage({ data: 'image/png;base64,' + c.data.toString('base64'), x: ox * PX, y: oy * PX, w: c.info.width / 2 * PX, h: c.info.height / 2 * PX, objectName: name, altText: it.alt });
      } else {
        const runs = [];
        for (const r of it.runs) { if (r.br) { if (runs.length) runs[runs.length - 1].options.breakLine = true; continue; }
          const f = face(r.family, r.weight); runs.push({ text: r.t, options: { color: hex(r.color), italic: r.italic, bold: f.bold, fontFace: f.face, fontSize: r.size / 2 } }); }
        if (!runs.length) continue;
        runs[0].text = runs[0].text.replace(/^\s+/, ''); runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/\s+$/, '');
        const slack = Math.min(it.w * 0.07, 60); let x = it.x, w = it.w + slack, al = it.align;
        if (al === 'center') x -= slack / 2; else if (al === 'right' || al === 'end') x -= slack;
        if (it.w < 120) { x = it.x - 40; w = it.w + 80; al = 'center'; }      // page numbers, short labels
        slide.addText(runs, { x: x * PX, y: it.y * PX, w: w * PX, h: it.h * PX, margin: 0, valign: 'top', isTextBox: true,
          align: al === 'center' ? 'center' : (al === 'right' || al === 'end') ? 'right' : 'left', lineSpacing: +(it.lh / 2).toFixed(1),
          charSpacing: it.ls ? +(it.ls / 2).toFixed(2) : undefined, paraSpaceBefore: 0, paraSpaceAfter: 0, fit: 'none', objectName: name });
      }
    }
    const sec = fs.readFileSync(path.join(deckDir, 'project/slides', id + '.html'), 'utf8');
    const notes = (sec.match(/<aside>([\s\S]*?)<\/aside>/) || [, ''])[1].replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").trim();
    if (notes) slide.addNotes(notes);
    console.log(id, items.length, 'items');
  }
  await pres.writeFile({ fileName: outFile }); await browser.close();
})();
