const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
  await p.goto('http://127.0.0.1:8420/index.html',{waitUntil:'networkidle'}); await p.waitForTimeout(700);
  console.log(await p.evaluate(() => [...document.querySelectorAll('.rail-pane')].map(e=>{
    const r=e.getBoundingClientRect(); return e.querySelector('h2').textContent.trim().slice(0,20)+' -> '+Math.round(r.height)+'px';
  }).join('\n')));
  await b.close();
})();
