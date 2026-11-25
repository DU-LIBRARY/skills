// Mosaic, simplified for the PDF: green, gold and cream only; no line patterns or faint numerals.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const D = 'mosaic', OUT = 'mosaic-clean';
const CSS = `
.mot, .num-f { display: none !important; }
.tile { border-radius: 14px; }
.grid { gap: 20px; }
.green { background: #1F4A40 !important; color: #F2EBDC !important; }
.navy { background: #44515A !important; color: #F2EBDC !important; }
.terra { background: #8E5F45 !important; color: #F6EDE0 !important; }
.teal { background: #5C7063 !important; color: #F2EBDC !important; }
.olive { background: #6A6544 !important; color: #F2EBDC !important; }
.gold { background: #CDB27A !important; color: #1F3B34 !important; }
.cream { background: #F4EEE0 !important; color: #1F3B34 !important; }
.grey { background: #C9C0AC !important; color: #2E2C27 !important; }
section.bone { background: #E6DFCF !important; }
.kufi { font-family: 'Noto Kufi Arabic', sans-serif !important; font-weight: 600 !important; line-height: 1.45 !important; }
.gold-t, .cv-s, .rm-ar { color: #E3CD98 !important; }
.gold .gold-t { color: #1F3B34 !important; }
.ln { background: #CDB27A !important; }
`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const deck = JSON.parse(fs.readFileSync(`${D}/project/deck.json`)); fs.mkdirSync(`${OUT}/pdf`, { recursive: true });
  for (const [i, id] of deck.order.entries()) {
    await p.goto('file://' + path.resolve(`${D}/prev-${id}.html`)); await p.addStyleTag({ url: 'https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@500;600;700&display=swap' }); await p.addStyleTag({ content: CSS }); await p.evaluate(() => document.fonts.load('600 40px "Noto Kufi Arabic"', 'هويتنا')); await p.evaluate(() => document.fonts.ready);
    await p.evaluate(({ id, logo }) => {
      const sec = document.querySelector('section'); const sr = sec.getBoundingClientRect();
      if (id === 'cover') {
        const terra = sec.querySelector('.tile.terra'), teal = sec.querySelector('.tile.teal');
        terra.className = teal.className.replace('teal', 'terra');
        terra.innerHTML = '<p class="dsp t60">1 UMMAH</p><p class="k">MANY BACKGROUNDS</p>';
      }
      // Arabic display: Noto Kufi Arabic is taller than Reem Kufi, so scale it a little and keep it inside its tile
      for (const e of sec.querySelectorAll('.kufi')) e.style.fontSize = (parseFloat(getComputedStyle(e).fontSize) * 0.86) + 'px';
      for (const e of sec.querySelectorAll('.kufi')) {
        const box = e.closest('.tile') || sec; let n = 0;
        while (n++ < 30 && (e.scrollWidth > e.clientWidth + 1 || (box !== sec && (box.scrollHeight > box.clientHeight + 1 || box.scrollWidth > box.clientWidth + 1)))) e.style.fontSize = (parseFloat(e.style.fontSize) * 0.95) + 'px';
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
