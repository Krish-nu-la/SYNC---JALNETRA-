const { chromium } = require('playwright');
(async () => {
  const [out, url, full, w, h] = [process.argv[2], process.argv[3] || 'index.html',
    process.argv[4] === 'full', +(process.argv[5]||1440), +(process.argv[6]||900)];
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push('PAGEERROR: ' + e.message));
  await page.goto('http://127.0.0.1:8420/' + url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(900);
  await page.screenshot({ path: 'shots/' + out, fullPage: full });
  if (errs.length) console.log('CONSOLE ERRORS:\n  ' + errs.join('\n  '));
  else console.log('no console errors');
  await browser.close();
})();
