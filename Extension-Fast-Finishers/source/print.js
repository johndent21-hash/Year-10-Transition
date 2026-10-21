// usage: node print.js in.html out.pdf [png-prefix]
const { chromium } = require('playwright');
(async () => {
  const [,, inp, out, png] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + require('path').resolve(inp));
  await p.evaluate(() => document.fonts.ready);
  const issues = await p.evaluate(() => {
    const r = [];
    document.querySelectorAll('.card').forEach((c, i) => {
      const body = c.querySelector('.body'), sp = c.querySelector('.space');
      const pg = c.closest('.page'); const idx = [...document.querySelectorAll('.page')].indexOf(pg) + 1;
      if (c.scrollHeight > c.clientHeight + 1) r.push(`page ${idx}: card overflow by ${c.scrollHeight - c.clientHeight}px`);
      else if (sp && sp.getBoundingClientRect().height < 30) r.push(`page ${idx}: card ${[...pg.querySelectorAll('.card')].indexOf(c)+1} working space only ${Math.round(sp.getBoundingClientRect().height)}px`);
      const fig = c.querySelector('.fig');
      if (fig && fig.getBoundingClientRect().width > body.getBoundingClientRect().width * 0.62 && !fig.classList.contains('center')) r.push(`page ${idx}: wide fig`);
    });
    document.querySelectorAll('.anscols').forEach(a => {
      const pg = a.closest('.page'); const idx = [...document.querySelectorAll('.page')].indexOf(pg) + 1;
      if (a.scrollWidth > a.clientWidth + 2) r.push(`page ${idx}: answers overflow (scrollWidth ${a.scrollWidth} > ${a.clientWidth})`);
    });
    return r;
  });
  console.log(issues.length ? issues.join('\n') : 'no overflow');
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
