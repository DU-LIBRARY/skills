const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const d of ['playbill','workshop','mosaic','zine']) { await p.goto('file://' + path.resolve(`${d}/prev-cover-logo.html`)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    await p.pdf({ path: `${d}/pdf/00.pdf`, width: '1920px', height: '1080px', printBackground: true, pageRanges: '1' }); }
  await b.close(); })();
