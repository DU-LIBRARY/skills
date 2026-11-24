// Cover with the logo top left: beside the Institute kicker (a lockup), or in the frame corner for Playbill.
const { chromium } = require('playwright'); const path = require('path');
const E = __dirname;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const d of ['playbill','workshop','mosaic','zine']) {
    await p.goto('file://' + path.resolve(`${d}/prev-cover.html`)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.evaluate(({ d, src }) => {
      const sec = document.querySelector('section'); const sr = sec.getBoundingClientRect();
      const k = [...sec.querySelectorAll('p')].find(e => /^THE IMAM MUHAMMAD ADAM INSTITUTE/i.test(e.innerText.trim()));
      const img = document.createElement('img'); img.src = src; img.alt = 'Imam Muhammad Adam Institute logo';
      img.style.position = 'absolute'; img.style.height = 'auto'; img.style.zIndex = 5;
      if (d === 'mosaic') {
        const terra = sec.querySelector('.tile.terra'); const teal = sec.querySelector('.tile.teal');
        terra.className = teal.className.replace('teal', 'terra');
        terra.innerHTML = '<p class="dsp t60">1 UMMAH</p><p class="k">MANY BACKGROUNDS</p>';
      }
      if (d === 'playbill') { img.style.width = '150px'; img.style.left = '118px'; img.style.top = '112px'; sec.appendChild(img); return; }
      const W = { workshop: 116, mosaic: 132, zine: 128 }[d]; const H = W * 649 / 659, gap = 26;
      const r = k.getBoundingClientRect();
      let top = r.top - sr.top + r.height / 2 - H / 2;
      const minTop = { workshop: 96, mosaic: 96, zine: 44 }[d]; const dy = Math.max(0, minTop - top); top += dy;
      img.style.width = W + 'px'; img.style.left = (r.left - sr.left) + 'px'; img.style.top = top + 'px';
      k.style.transform = `translate(${W + gap}px, ${dy}px)`;
      sec.appendChild(img);
    }, { d, src: `file://${E}/logo-${d === 'workshop' ? 'workshop-light' : d}.png` });
    await p.waitForTimeout(200);
    await p.screenshot({ path: `tl-${d}.png` });
    await p.pdf({ path: `${d}/pdf/00.pdf`, width: '1920px', height: '1080px', printBackground: true, pageRanges: '1' });
  }
  await b.close(); })();
