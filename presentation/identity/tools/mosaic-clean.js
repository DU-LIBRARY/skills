// Mosaic, simplified for the PDF: green, gold and cream only; no line patterns or faint numerals.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const D = 'mosaic', OUT = 'mosaic-clean';
const CSS = `
.mot, .num-f { display: none !important; }
.tile { border-radius: 14px; }
.grid { gap: 22px; }
.light { background: #F6F0E1 !important; color: #17433A !important; }
.light .gold-t, .light .cv-s, .light .rm-ar { color: #9A7A34 !important; }
.light .ln { background: #C9B98F !important; }
.gold.light .k, .gold.light p { color: #17433A; }
.deep { background: #17433A !important; color: #F2EBDC !important; }
.deep .q-ar, .deep .qq-ar, .deep .qq-lead, .deep .green-t, .deep .cv-ar { color: #F2EBDC !important; }
`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const deck = JSON.parse(fs.readFileSync(`${D}/project/deck.json`)); fs.mkdirSync(`${OUT}/pdf`, { recursive: true });
  for (const [i, id] of deck.order.entries()) {
    await p.goto('file://' + path.resolve(`${D}/prev-${id}.html`)); await p.addStyleTag({ content: CSS });
    await p.evaluate(({ id, logo }) => {
      const sec = document.querySelector('section'); const sr = sec.getBoundingClientRect();
      if (id === 'cover') {
        const terra = sec.querySelector('.tile.terra'), teal = sec.querySelector('.tile.teal');
        terra.className = teal.className.replace('teal', 'terra');
        terra.innerHTML = '<p class="dsp t60">1 UMMAH</p><p class="k">MANY BACKGROUNDS</p>';
      }
      // colour: the biggest tile keeps its colour (green, or gold if gold); smaller tiles go cream; gold only on big tiles
      const col = [...sec.querySelectorAll('.tile')].filter(t => /\b(navy|terra|teal|olive|grey|green|gold)\b/.test(t.className));
      const area = t => { const r = t.getBoundingClientRect(); return r.width * r.height; };
      const max = Math.max(0, ...col.map(area)); const top = col.filter(t => area(t) >= max * 0.97);
      for (const t of col) {
        const A = area(t), gold = t.classList.contains('gold');
        if (A >= max * 0.97) { if (!gold || top.length >= 3) t.classList.add('deep'); }
        else if (gold) { if (A < max * 0.5 && id !== 'cover') t.classList.add('light'); }
        else if (t.classList.contains('green') && A > max * 0.55) t.classList.add('deep');
        else t.classList.add('light');
      }
      if (id === 'cover') {
        const k = [...sec.querySelectorAll('p')].find(e => /^THE IMAM MUHAMMAD ADAM INSTITUTE/i.test(e.innerText.trim()));
        const W = 132, H = W * 649 / 659, gap = 26, r = k.getBoundingClientRect();
        let top = r.top - sr.top + r.height / 2 - H / 2; const dy = Math.max(0, 96 - top); top += dy;
        const img = document.createElement('img'); img.src = logo; img.alt = 'Imam Muhammad Adam Institute logo';
        Object.assign(img.style, { position: 'absolute', width: W + 'px', height: 'auto', left: (r.left - sr.left) + 'px', top: top + 'px', zIndex: 5 });
        k.style.transform = `translate(${W + gap}px, ${dy}px)`; sec.appendChild(img);
      }
    }, { id, logo: 'file://' + path.resolve('logo-mosaic.png') });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
    await p.screenshot({ path: `${OUT}/s-${String(i).padStart(2, '0')}.png` });
    await p.pdf({ path: `${OUT}/pdf/${String(i).padStart(2, '0')}.pdf`, width: '1920px', height: '1080px', printBackground: true, pageRanges: '1' });
  }
  await b.close();
})();
