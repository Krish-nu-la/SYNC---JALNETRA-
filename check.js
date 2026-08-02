const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
  await p.goto('http://127.0.0.1:8420/index.html',{waitUntil:'networkidle'}); await p.waitForTimeout(700);
  const g = async (sel, prop) => p.$eval(sel, (e,pr)=>getComputedStyle(e)[pr], prop).catch(()=>'MISSING');
  console.log('wordmark JAL colour :', await g('.wordmark','color'));
  console.log('wordmark NETRA span :', await g('.wordmark span','color'));
  console.log('hero border (WATCH) :', await g('.hero-card','borderColor'));
  console.log('citizen border      :', await g('.nb-card','borderColor'));
  console.log('left rail exists    :', !!(await p.$('.rail-left')));
  for (const s of ['#rain','#presets','#btn-report','#legend-btn','#prov-btn'])
    console.log(('  '+s).padEnd(22), (await p.$(s)) ? 'present' : 'MISSING');
  console.log('drainage note       :', (await p.$('.attrib-note')) ? 'present' : 'MISSING');
  // escalate and re-read the hero border
  await p.click('button[data-mm="120"]');
  await p.$eval('#scrub', el=>{el.value='4';el.dispatchEvent(new Event('input',{bubbles:true}));});
  await p.waitForTimeout(600);
  console.log('hero state          :', await p.$eval('#hero-state', e=>e.textContent));
  console.log('hero border (ACT NOW):', await g('.hero-card','borderColor'));
  await b.close();
})();
