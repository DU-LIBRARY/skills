const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const d of process.argv.slice(2)) {
    const deck = JSON.parse(fs.readFileSync(`${d}/project/deck.json`)); fs.mkdirSync(`${d}/pdf`, { recursive: true });
    for (const [i, id] of deck.order.entries()) {
      await p.goto('file://' + path.resolve(`${d}/prev-${id}.html`)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(250);
      await p.pdf({ path: `${d}/pdf/${String(i).padStart(2, '0')}.pdf`, width: '1920px', height: '1080px', printBackground: true, pageRanges: '1' });
    }
    console.log(d);
  }
  await b.close();
})();
