const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1440,height:900} });
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://127.0.0.1:8420/index.html',{waitUntil:'networkidle'});
  await p.waitForTimeout(800);

  const probe = async (label) => {
    const s = await p.evaluate(() => {
      const m = document.getElementById('map'), v = document.getElementById('veil'),
            d = document.getElementById('diorama');
      return { diving: document.body.dataset.diving,
               mapT: getComputedStyle(m).transform.slice(0,28),
               veil: getComputedStyle(v).opacity,
               dioHidden: d.hidden, dioOpacity: getComputedStyle(d).opacity };
    });
    console.log(`  ${label.padEnd(16)} diving=${String(s.diving).padEnd(5)} veil=${(+s.veil).toFixed(2)} dio=${s.dioHidden?'hidden':(+s.dioOpacity).toFixed(2)}  map ${s.mapT}`);
  };

  console.log('ZONE CLICK -> DIORAMA');
  await probe('before');
  await p.click('.zone-row');                       // expand the row
  await p.waitForTimeout(300);
  const hasBtn = await p.$('.zd-dio');
  console.log('  street-level button present:', !!hasBtn);
  await p.click('.zd-dio');                          // real entry point
  await p.waitForTimeout(180); await probe('t=180ms');
  await p.waitForTimeout(240); await probe('t=420ms');
  await p.waitForTimeout(700); await probe('t=1120ms');
  await p.screenshot({path:'shots/anim-arrived.png'});

  console.log('\nCLOSE -> REVERSE');
  await p.keyboard.press('Escape');
  await p.waitForTimeout(140); await probe('t=140ms');
  await p.waitForTimeout(420); await probe('t=560ms');

  console.log('\nSWEEP');
  await p.evaluate(() => document.getElementById('btn-run').click());
  await p.waitForTimeout(400);
  console.log('  sweeping class on body:', await p.evaluate(()=>document.body.classList.contains('sweeping')));
  console.log('  run button label:', await p.$eval('#btn-run', e=>e.textContent.trim()));
  await p.evaluate(()=>document.getElementById('btn-run').click());
  await p.waitForTimeout(200);
  console.log('  after stop, label:', await p.$eval('#btn-run', e=>e.textContent.trim()));

  console.log('\nerrors:', errs.length?errs.join(' | '):'none');
  await b.close();
})();
