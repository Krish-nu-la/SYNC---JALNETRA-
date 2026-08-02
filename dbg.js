const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
  await p.goto('http://127.0.0.1:8420/index.html',{waitUntil:'networkidle'}); await p.waitForTimeout(800);
  const r = await p.evaluate(() => {
    const g = id => { const e = document.getElementById(id) || document.querySelector(id); if(!e) return null;
      const c = getComputedStyle(e), b = e.getBoundingClientRect();
      return {pos:c.position, z:c.zIndex, rect:[Math.round(b.x),Math.round(b.y),Math.round(b.width),Math.round(b.height)],
              parent:e.parentElement.className}; };
    return { map:g('map'), wrap:g('.map-wrap'), hud:g('.hud'), col:g('.col-main'), rail:g('.rail-right'),
             leaf:g('.leaflet-container') };
  });
  console.log(JSON.stringify(r,null,1));
  await b.close();
})();
