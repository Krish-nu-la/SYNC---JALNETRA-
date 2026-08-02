const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8420/index.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(700);

  // Cloudburst + +120 -> ACT NOW
  await p.click('button[data-mm="120"]');
  await p.$eval('#scrub', el => { el.value = '4'; el.dispatchEvent(new Event('input', { bubbles: true })); });
  await p.waitForTimeout(600);
  console.log('state:', await p.$eval('#hero-state', e => e.textContent),
              '| action:', (await p.$eval('#hero-action', e => e.textContent)).slice(0,44));
  await p.screenshot({ path: 'shots/verify-5-cloudburst.png' });

  // expand a zone row
  await p.click('.zone-row');
  await p.waitForTimeout(400);
  await p.screenshot({ path: 'shots/verify-6-zone-expanded.png' });

  // diorama
  await p.click('.zd-dio');
  await p.waitForTimeout(2200);
  await p.screenshot({ path: 'shots/verify-7-diorama.png' });
  console.log('diorama header:', await p.$eval('#dio-level', e => e.textContent));
  await p.keyboard.press('Escape');
  await p.waitForTimeout(700);

  console.log(errs.length ? 'ERRORS: ' + errs.join(' | ') : 'no page errors');
  await b.close();
})();
