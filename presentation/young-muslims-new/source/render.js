const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  for (const f of process.argv.slice(2)) { await p.goto('file://' + path.resolve(f)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    await p.screenshot({ path: f.replace('.html', '.png') }); await p.pdf({ path: f.replace('.html', '.pdf'), width: '1920px', height: '1080px', printBackground: true, pageRanges: '1' }); }
  await b.close(); })();
