// Slide artwork as one picture; English text as editable text on top; notes from <aside>.
const { chromium } = require('playwright'); const pptxgen = require('pptxgenjs'); const fs = require('fs'), path = require('path');
const [, , deckDir, outFile] = process.argv;
const deck = JSON.parse(fs.readFileSync(path.join(deckDir, 'project/deck.json'), 'utf8'));
const FM = JSON.parse(fs.readFileSync(path.join(__dirname, 'facemap.json'), 'utf8'));
const PX = 1 / 144;
const rgb = c => (c.match(/[\d.]+/g) || []).map(Number);
const hex = c => rgb(c).slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
function face(fam, wt, it) {
  fam = fam.split(',')[0].replace(/['"]/g, '').trim(); const st = it ? 'italic' : 'normal';
  const ws = [wt, 400, 500, 600, 700, 800, 300, 900].sort((a, b) => Math.abs(a - wt) - Math.abs(b - wt));
  for (const s of [st, 'normal']) for (const w of ws) { const m = FM[`${fam}|${w}|${s}`]; if (m) return { face: m.face, bold: m.bold, italic: it }; }
  return { face: fam, bold: wt >= 600, italic: it };
}
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 2 });
  const pres = new pptxgen(); pres.layout = 'LAYOUT_WIDE'; pres.title = deck.title;
  const work = outFile.replace(/\.pptx$/, '-work'); fs.mkdirSync(work, { recursive: true });
  for (const id of deck.order) {
    await page.goto('file://' + path.resolve(deckDir, `prev-${id}.html`)); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(300);
    const items = await page.evaluate(() => {
      const sec = document.querySelector('section'); const out = []; let k = 0;
      const arRe = /[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]/g, latRe = /[A-Za-z]/g;
      const grp = el => { const g = el.closest('.d1,.d2,.d3'); return g ? +[...g.classList].find(c => /^d[123]$/.test(c)).slice(1) : 0; };
      const plain = el => { for (let e = el; e && e !== sec; e = e.parentElement) { const s = getComputedStyle(e); if (parseFloat(s.opacity) < 1 || (s.mixBlendMode && s.mixBlendMode !== 'normal') || s.filter !== 'none' || s.transform !== 'none' || s.rotate !== 'none' || (s.writingMode || '').startsWith('vertical')) return false; } return true; };
      for (const c of sec.querySelectorAll('h1,h2,h3,p,li')) {
        if (c.closest('aside') || c.querySelector('p,h1,h2,h3,li')) continue;
        const txt = c.innerText; if (!txt.trim()) continue;
        const cs = getComputedStyle(c);
        if ((txt.match(arRe) || []).length > 0) continue;            // Arabic, or mixed with Arabic: keep in the artwork
        if (!(txt.match(latRe) || []).length && txt.trim().length > 4) continue;
        if (!plain(c)) continue;
        let shadow = false; for (const e of [c, ...c.querySelectorAll('*')]) { const s = getComputedStyle(e); if (s.textShadow !== 'none' || s.webkitTextStroke !== '0px' && parseFloat(s.webkitTextStrokeWidth) > 0 || s.backgroundClip === 'text') shadow = true; }
        if (shadow) continue;
        if (parseFloat(cs.opacity) < 1) continue;
        const r = c.getBoundingClientRect(); if (r.width < 2) continue;
        const runs = [];
        (function w2(n) { for (const x of n.childNodes) { if (x.nodeType === 3) { if (x.textContent) { const s = getComputedStyle(x.parentElement); runs.push({ t: x.textContent.replace(/\s+/g, ' '), color: s.color, italic: s.fontStyle === 'italic', weight: +s.fontWeight, family: s.fontFamily, size: parseFloat(s.fontSize), up: s.textTransform === 'uppercase', ul: s.textDecorationLine.includes('underline'), ls: s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing) }); } } else if (x.nodeName === 'BR') runs.push({ br: true }); else if (x.nodeType === 1) w2(x); } })(c);
        if (runs.some(r => !r.br && (r.color.match(/[\d.]+/g) || []).length > 3 && +(r.color.match(/[\d.]+/g))[3] < 1)) continue;
        const lines = Math.round((r.height - (parseFloat(cs.paddingTop)||0) - (parseFloat(cs.paddingBottom)||0)) / (cs.lineHeight === 'normal' ? 1.2 * parseFloat(cs.fontSize) : parseFloat(cs.lineHeight)));
        c.classList.add('__ed');
        const P = n => parseFloat(cs[n]) || 0; const pl = P('paddingLeft') + P('borderLeftWidth'), pr = P('paddingRight') + P('borderRightWidth'), pt = P('paddingTop') + P('borderTopWidth'), pb = P('paddingBottom') + P('borderBottomWidth');
        out.push({ k: k++, g: grp(c), x: r.left + pl, y: r.top + pt, w: r.width - pl - pr, h: r.height - pt - pb, size: parseFloat(cs.fontSize), lines,
          lh: cs.lineHeight === 'normal' ? 1.2 * parseFloat(cs.fontSize) : parseFloat(cs.lineHeight), align: cs.textAlign, runs });
      }
      return out;
    });
    await page.addStyleTag({ content: '.__ed, .__ed *{color:transparent!important;text-decoration-color:transparent!important} li.__ed::marker{color:transparent!important}' });
    const bg = path.join(work, id + '.jpg'); await page.screenshot({ path: bg, type: 'jpeg', quality: 88 });
    const slide = pres.addSlide();
    slide.addImage({ path: bg, x: 0, y: 0, w: 13.333, h: 7.5, objectName: 'bg', altText: 'Slide artwork' });
    for (const it of items) {
      const runs = [];
      for (const r of it.runs) { if (r.br) { if (runs.length) runs[runs.length - 1].options.breakLine = true; continue; }
        const f = face(r.family, r.weight, r.italic);
        runs.push({ text: r.up ? r.t.toUpperCase() : r.t, options: { color: hex(r.color), italic: f.italic, bold: f.bold, fontFace: f.face, fontSize: r.size / 2, underline: r.ul ? { style: 'sng' } : undefined, charSpacing: r.ls ? +(r.ls / 2).toFixed(2) : undefined } }); }
      if (!runs.length) continue;
      runs[0].text = runs[0].text.replace(/^\s+/, ''); runs[runs.length - 1].text = runs[runs.length - 1].text.replace(/\s+$/, '');
      const slack = it.lines <= 1 ? Math.min(it.w * 0.15, 120) : Math.min(it.w * 0.05, 40);
      let x = it.x, w = it.w + slack, al = it.align;
      if (al === 'center') x -= slack / 2; else if (al === 'right' || al === 'end') x -= slack;
      if (it.w < 140) { x = it.x - 50; w = it.w + 100; al = 'center'; }
      slide.addText(runs, { x: x * PX, y: it.y * PX, w: w * PX, h: it.h * PX, margin: 0, valign: 'top', isTextBox: true, wrap: it.lines > 1,
        align: al === 'center' ? 'center' : (al === 'right' || al === 'end') ? 'right' : 'left', lineSpacing: +(it.lh / 2).toFixed(1),
        paraSpaceBefore: 0, paraSpaceAfter: 0, fit: 'none', objectName: `a${it.g}_${it.k}` });
    }
    const sec = fs.readFileSync(path.join(deckDir, 'project/slides', id + '.html'), 'utf8');
    const notes = (sec.match(/<aside>([\s\S]*?)<\/aside>/) || [, ''])[1].replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'").trim();
    if (notes) slide.addNotes(notes);
    console.log(id, items.length);
  }
  await pres.writeFile({ fileName: outFile }); await browser.close();
})();
