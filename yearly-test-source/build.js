// Builds the Year 10 transition yearly test and its marking guide as A4 PDFs.
// Usage: node build.js [--shots <dir>]   (--shots also saves a PNG of every page, for checking the layout)
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const OUT = path.join(ROOT, '..', 'Yearly test');
const shotsIdx = process.argv.indexOf('--shots');
const shotsDir = shotsIdx > 0 ? path.resolve(process.argv[shotsIdx + 1]) : null;

const { sections, layout, figs: F } = require('./test');
const css = fs.readFileSync(path.join(ROOT, 'lib/test.css'), 'utf8');

const TEST = { year: 2026, title: 'Mathematics Yearly Test', series: 'Year 10 Transition', working: '1 hour 15 minutes', reading: '5 minutes' };
const LETTERS = 'ABCD';
const marksText = (m) => `${m} mark${m === 1 ? '' : 's'}`;

// ---------- number every question and total the marks ----------
let n = 0;
sections.forEach((s) => {
  s.qs.forEach((q) => { if (q.type !== 'info') q.n = ++n; });
  const real = s.qs.filter((q) => q.type !== 'info');
  s.first = real[0].n; s.last = real[real.length - 1].n;
  s.marks = real.reduce((a, q) => a + q.marks, 0);
  real.forEach((q) => {
    if (q.parts) {
      const given = q.parts.filter((p) => p.marks).reduce((a, p) => a + p.marks, 0);
      const free = q.parts.filter((p) => !p.marks);
      free.forEach((p) => { p.marks = (q.marks - given) / free.length; });
      const sum = q.parts.reduce((a, p) => a + p.marks, 0);
      if (sum !== q.marks) throw new Error(`Question ${q.n}: part marks add to ${sum}, not ${q.marks}`);
    }
  });
});
const TOTAL = sections.reduce((a, s) => a + s.marks, 0);
const TIME = sections.reduce((a, s) => a + s.time, 0);

// ---------- pieces ----------
const helpBox = (h, cls = 'inline') => !h ? '' : `
  <div class="help ${cls}"><span class="tag">HELP</span>
    ${h.rows.map(([l, v]) => (v === 'pics' ? `<div class="row pics-row"><b>${l}</b><div class="pics">${F.shapePic([1, 3, 5, 3, 1], 'symmetrical')}${F.shapePic([5, 4, 2, 1, 1], 'skewed')}</div></div>` : `<div class="row"><b>${l}</b><div>${v}</div></div>`)).join('')}
  </div>`;

const head = (q) => `
  <div class="q-head"><span class="qn">${q.n}</span><div class="q-text">${q.text}</div><span class="q-marks">${marksText(q.marks)}</span></div>`;

const mc = (q) => `
<div class="q mc" data-q="${q.n}">
  ${head(q)}
  <div class="q-body">
    <div class="opts${q.optCols === 2 ? ' c2' : ''}">${q.options.map((o, i) => `<div class="opt${i === q.answer ? ' right' : ''}"><span class="ol">${LETTERS[i]}</span><span>${o}</span></div>`).join('')}</div>
    ${helpBox(q.help)}
  </div>
</div>`;

const answerLine = (p) => p.noLine ? '' : `
  <div class="ans"><span class="al">Answer</span><span class="line">${p.pre ? `<span>${p.pre}</span>` : ''}<span class="key kv">${p.key}</span></span>${p.unit ? `<span class="unit">${p.unit}</span>` : ''}</div>`;

const keyNote = (p) => p.keyNote ? `<span class="key knote">${p.keyNote}</span>` : '';

const part = (p, i, many) => {
  const label = many ? `<span class="pl">${'abcdef'[i]}</span>` : '';
  const pm = p.showMarks ? `<span class="pm">${marksText(p.marks)}</span>` : '';
  const text = p.text ? `<div class="p-text">${label}<div>${p.text}</div>${pm}</div>` : '';
  if (p.choice) {
    return `<div class="part fixed">${text}<div class="choice">${p.choice.map((c) => `<span class="${c === p.key ? 'right' : ''}">${c}</span>`).join('')}</div></div>`;
  }
  if (p.short) return `<div class="part short">${text}${answerLine(p)}</div>`;
  if (p.compact) return `<div class="part fixed compact">${text}${answerLine(p)}</div>`;
  const extra = p.extra || '';
  if (p.noWork) return `<div class="part fixed">${text}${extra}${p.keyNote ? `<div style="position:relative;height:9mm">${keyNote(p)}</div>` : ''}</div>`;
  const work = `<div class="work"><span class="wl">Working</span>${keyNote(p)}</div>`;
  if (p.fig) return `<div class="part">${text}<div class="figwrap">${p.fig}${work}</div>${answerLine(p)}</div>`;
  return `<div class="part">${text}${extra}${work}${answerLine(p)}</div>`;
};

const keyCell = (c) => (typeof c === 'object' ? `<td class="blank"><span class="key kv">${c.key}</span></td>` : `<td class="done">${c}</td>`);

const saTable = (t) => `
  <table class="tbl"><colgroup><col class="c1"><col class="c2"><col class="c3"><col class="c4"></colgroup>
    <tr>${t.head.map((h) => `<th>${h}</th>`).join('')}</tr>
    ${t.rows.map((r) => `<tr>${r.map((c, j) => (j === 0 ? `<td><b>${c}</b></td>` : keyCell(c))).join('')}</tr>`).join('')}
    <tr class="total"><td colspan="3">${t.total[0]}</td>${keyCell(t.total[1])}</tr>
  </table>`;

const freqTable = (t) => `
  <table class="freq">
    <tr>${t.head.map((h) => `<th>${h}</th>`).join('')}</tr>
    ${t.rows.map((r) => `<tr><td>${r[0]}</td><td>${r[1]}</td></tr>`).join('')}
    <tr class="total"><td>Total</td><td class="blank"><span class="key kv">${t.total.key}</span></td></tr>
  </table>`;

const valueTable = (t) => `
  <table class="vt">
    <tr><th>x</th>${t.xs.map((x) => `<td>${x}</td>`).join('')}</tr>
    <tr><th>y</th>${t.ys.map((y) => `<td><span class="key kv">${y}</span></td>`).join('')}</tr>
  </table>`;

const orderBoxes = (o) => `
  <div class="order">Write the numbers in order first:&nbsp;${o.key.map((v) => `<i class="k"><span class="key">${v}</span></i>`).join('')}</div>`;

const sa = (q) => {
  q.parts = q.parts || [];
  const many = q.parts.length > 1;
  // A frequency table and histogram, or a table of values and a number plane, sit side by side above the parts.
  let top = '';
  let sideFig = q.fig || '';
  if (q.freqTable) {
    top = `<div class="q-wide">${freqTable(q.freqTable)}<div style="flex:1;display:flex;justify-content:center">${q.fig}</div></div>`;
    sideFig = '';
  }
  if (q.valueTable) q.parts[0].extra = `<div style="margin:2mm 0 1mm 7.5mm">${valueTable(q.valueTable)}</div>`;
  let parts = q.parts.map((p, i) => part(p, i, many)).join('');
  if (q.partsRow) parts = `<div class="parts-row">${parts}</div>`;
  const mainFig = q.figPos === 'main' ? `<div class="mainfig">${q.fig}</div>` : '';
  if (mainFig) sideFig = '';
  const pre = (q.order ? orderBoxes(q.order) : '') + (q.table ? saTable(q.table) : '');
  const helpTop = q.helpPos === 'top';
  const helpInMain = q.valueTable || helpTop;
  const main = `<div class="q-main">${helpTop ? helpBox(q.help, 'wide') : ''}${mainFig}${pre}${parts}${q.valueTable ? helpBox(q.help, 'wide') : ''}</div>`;
  const side = (sideFig || (q.help && !helpInMain)) ? `<div class="q-side">${sideFig}${helpInMain ? '' : helpBox(q.help, '')}</div>` : '';
  const grow = q.grow || q.marks;
  return `
<div class="q sa" data-q="${q.n}" style="flex-grow:${grow}">
  ${head(q)}
  ${top}
  <div class="q-body">${main}${side}</div>
</div>`;
};

const info = (q, next) => `<div class="info">${q.html().replaceAll('{{n+1}}', next).replaceAll('{{n+2}}', next + 1)}</div>`;

const banner = (s) => `
<div class="banner">
  <div class="letter"><span>SECTION</span><b>${s.id}</b></div>
  <div>
    <h2>${s.title}</h2>
    <div class="meta">Questions <b>${s.first}–${s.last}</b> · <b>${s.marks} marks</b> · Suggested time <b>${s.time} minutes</b></div>
  </div>
  <div class="score"><i></i><b>/ ${s.marks}</b><br>Marker</div>
</div>`;

const mcNote = (s) => {
  const mcs = s.qs.filter((q) => q.type === 'mc');
  if (!mcs.length) return '';
  const r = mcs.length === 1 ? `Question ${mcs[0].n} is` : `Questions ${mcs[0].n}–${mcs[mcs.length - 1].n} are`;
  return `<div class="info mcn" style="padding:1.6mm 4mm;font-size:10pt">${r} <b>multiple choice</b>. Circle the letter of the correct answer, like this: <span class="ol" style="display:inline-flex;width:6.5mm;height:6.5mm;font-size:9.5pt;vertical-align:middle;box-shadow:0 0 0 0.6mm #fff,0 0 0 1.1mm var(--ink)">B</span></div>`;
};

// ---------- pages ----------
const pageHead = (s) => `
  <header class="ph"><img src="assets/kingscliff-logo-large.png" alt="Kingscliff High School">
    <div class="t"><b>Year 10 ${TEST.title} ${TEST.year}</b><br>Kingscliff High School</div>
    ${s ? `<span class="sec"><span>Section ${s.id}</span>${s.title}</span>` : ''}</header>`;
const pageFoot = (right) => `<footer class="pf"><span>Kingscliff High School · Year 10 Mathematics</span><span class="pn">Page {{PN}} of {{PT}}</span>${right}</footer>`;

const testPages = () => {
  const pages = [];
  sections.forEach((s, si) => {
    const groups = layout[s.id];
    groups.forEach((g, gi) => {
      const items = g.map((i) => s.qs[i]);
      const body = items.map((q, k) => {
        if (q.type === 'info') { const nxt = items.slice(k + 1).find((x) => x.n); return info(q, nxt.n); }
        return q.type === 'mc' ? mc(q) : sa(q);
      }).join('');
      const last = gi === groups.length - 1;
      const next = sections[si + 1];
      const right = !last ? '<span class="go">Section ' + s.id + ' continues on the next page →</span>'
        : next ? `<span class="end">End of Section ${s.id} · go on to Section ${next.id} →</span>` : '<span class="go">Turn over →</span>';
      pages.push(`
<section class="page">${pageHead(s)}
  <div class="content">${gi === 0 ? banner(s) + mcNote(s) : ''}${body}</div>
  ${pageFoot(right)}
</section>`);
    });
  });
  pages.push(`
<section class="page extra">${pageHead(null)}
  <div class="content">
    <div class="endbox"><h2>End of the test</h2><ul>
      <li>Did you answer <b>every</b> question? Have a go at any you missed.</li>
      <li>Did you write the <b>units</b> ($, cm, m², mL) and show your <b>working</b>?</li>
      <li>Use the space below if you need more room. Write the question number next to your working.</li></ul></div>
    <div class="work"><span class="wl">Extra working space</span></div>
  </div>
  ${pageFoot('<span class="end">End of the test</span>')}
</section>`);
  return pages;
};

const cover = () => `
<section class="page cover">
  <div class="content">
    <div class="cv-top">
      <img class="cv-logo" src="assets/kingscliff-logo-large.png" alt="Kingscliff High School">
      <span class="cv-series">${TEST.series.toUpperCase()} · ${TEST.year}</span>
    </div>
    <div class="cv-title"><h1>Year 10 ${TEST.title}</h1></div>
    <div class="cv-student">
      <div><span>Name</span><i></i></div><div><span>Class</span><i></i></div>
      <div><span>Teacher</span><i></i></div><div><span>Date</span><i></i></div>
    </div>
    <div class="cv-facts">
      <div class="fact"><span>Working time</span><b>1 hour 15 min</b><small>+ ${TEST.reading} reading</small></div>
      <div class="fact"><span>Total marks</span><b>${TOTAL} marks</b><small>${n} questions</small></div>
      <div class="fact"><span>Calculators</span><b>Allowed</b><small>bring your own</small></div>
      <div class="fact"><span>Bring</span><b>Pen, pencil</b><small>ruler, eraser, calculator</small></div>
    </div>
    <div>
      <p class="cv-h">What is in this test</p>
      <table class="cv-table">
        <tr><th></th><th>Section and topics</th><th class="n">Questions</th><th class="n">Marks</th><th class="n">Time</th><th style="text-align:right">Your mark</th></tr>
        ${sections.map((s) => `<tr><td class="sl"><b>${s.id}</b></td><td><b>${s.title}</b><br><span class="tp">${s.topics}</span></td><td class="n">${s.first}–${s.last}</td><td class="n"><b>${s.marks}</b></td><td class="n">${s.time} min</td><td class="mk"><i></i>/ ${s.marks}</td></tr>`).join('')}
        <tr class="total"><td></td><td>Total</td><td class="n">1–${n}</td><td class="n">${TOTAL}</td><td class="n">${TIME} min</td><td class="mk"><i></i>/ ${TOTAL}</td></tr>
      </table>
    </div>
    <div class="cv-cols">
      <div>
        <p class="cv-h">Instructions</p>
        <ul class="cv-steps">
          <li><i>1</i><span>Use a <b>blue or black pen</b>. Use a pencil and ruler for graphs and diagrams.</span></li>
          <li><i>2</i><span><b>Answer every question.</b> Write your answer on the <b>Answer</b> line.</span></li>
          <li><i>3</i><span><b>Show your working.</b> You can get marks for working, even if your answer is wrong.</span></li>
          <li><i>4</i><span><b>Multiple choice:</b> circle <b>one</b> letter, A, B, C or D.</span></li>
          <li><i>5</i><span>Watch the clock. Each section has a <b>suggested time</b>.</span></li>
        </ul>
      </div>
      <div class="cv-help">
        <p class="cv-h">Stuck? Look for HELP</p>
        <p style="font-size:9.5pt">Many questions have a <b>HELP</b> box. It gives you the <b>formula</b> and a worked <b>example</b>, like this:</p>
        ${helpBox({ rows: [['Formula', 'Area of a rectangle = length × width'], ['Example', 'Length 5 cm, width 3 cm: 5 × 3 = 15 cm²']] }, '')}
      </div>
    </div>
    <div class="cv-stop">Do not turn over until your teacher tells you to start. <span>Good luck!</span></div>
  </div>
</section>`;

// ---------- marking guide front pages ----------
const plain = (h) => String(h).replace(/<span class="fr"><span>(.*?)<\/span><span>(.*?)<\/span><\/span>/g, '$1/$2').replace(/<[^>]+>/g, '').replace(/&nbsp;/g, ' ');
const answerSummary = (q) => {
  if (q.type === 'mc') return `${LETTERS[q.answer]} &nbsp;(${q.options[q.answer]})`;
  if (q.table) return `${q.table.rows.slice(1).map((r) => plain(r[3].key)).join(', ')}; surface area ${plain(q.table.total[1].key)}`;
  if (q.valueTable) return `y = ${q.valueTable.ys.join(', ')}; points plotted and joined`;
  return q.parts.map((p, i) => {
    const v = p.keyText || plain(p.key || (p.keyNote ? 'see guide' : ''));
    const val = `${p.pre && p.pre.startsWith('$') ? '$' : ''}${v}${p.unit ? (p.unit === '%' ? '%' : ` ${p.unit}`) : ''}`;
    return `${q.parts.length > 1 ? `(${'abcdef'[i]}) ` : ''}${val}`;
  }).join('<br>');
};
const NOTES = {
  // Marking notes for questions where part marks or a range of answers are allowed.
  'Mark-up and profit': '(b) Follow-through from (a): accept selling price − 7.60.',
  'Gross and net pay': '(b) Follow-through: accept their (a) − 165.09.',
  'Compound interest': '(b) Follow-through: accept their (a) − 5000. Accept $5624.32 rounded to $5624.',
  'Circumference and area of a circle': 'Accept 2 d.p. (18.85, 28.27) or answers using π ≈ 3.14 (18.84, 28.26).',
  'Surface area of a prism': '1 mark: both rows correct (20, 40 and 8, 16). 1 mark: total 136 cm².',
  'Volume and capacity of a cylinder': 'Accept 75.40 or 75 (2 d.p. or whole). (b) Follow-through from (a).',
  'Mean, median and range': 'Order: 1, 3, 3, 5, 8, 9, 13.',
  'Frequency tables, histograms and shape': '(a) 20  (b) 9 ÷ 20 × 100 = 45%  (c) heights 3 and 2, touching  (d) skewed.',
  'Probability': '',
  'Table of values and graphing a line': '(a) 2 marks: all four correct; 1 mark: two or three correct. (b) Follow-through from their table.',
  'Pythagoras’ theorem': '1 mark: 6² + 8² = 100 (or c² = 100). 1 mark: c = 10 cm.',
  'Trigonometry: finding a side': '1 mark: x = 8 × tan 35°. 1 mark: 5.6 cm. (Radians mode gives −3.8: 1 mark for working.)',
  'Solving equations': 'Accept any correct method, or the answer checked by substitution.',
};

const guidePages = () => {
  const rowsFor = (list) => list.map((s) => `
    <tr class="sec"><td colspan="5">Section ${s.id} · ${s.title} · ${s.marks} marks · ${s.source}</td></tr>
    ${s.qs.filter((q) => q.type !== 'info').map((q) => `<tr><td class="c"><b>${q.n}</b></td><td>${q.topic}<br><span class="src">${q.src}</span></td><td class="ansc">${answerSummary(q)}</td><td class="c">${q.marks}</td><td>${NOTES[q.topic] || ''}</td></tr>`).join('')}`).join('');
  const table = (list) => `
    <table class="mg-table">
      <tr><th style="width:8mm">Q</th><th style="width:58mm">Topic and where it comes from</th><th>Answer</th><th style="width:11mm">Marks</th><th style="width:58mm">Marking notes</th></tr>
      ${rowsFor(list)}
    </table>`;
  const chapterMarks = sections.filter((s) => s.id !== 'D').reduce((a, s) => a + s.marks, 0);
  const p1 = `
<section class="page mg">${pageHead(null)}
  <div class="content">
    <div><h1>Marking guide</h1><p class="sub">Year 10 ${TEST.title} ${TEST.year} · ${TOTAL} marks · ${TEST.working}. Answers for every question are below, and the test pages that follow have the answers written in red.</p></div>
    ${table(sections.slice(0, 2))}
  </div>
  ${pageFoot('<span>Marking guide</span>')}
</section>`;
  const p2 = `
<section class="page mg">${pageHead(null)}
  <div class="content">
    ${table(sections.slice(2))}
    <div class="info mg-note"><b>General marking notes</b>
      <ul>
        <li>Give full marks for a correct answer, even with no working.</li>
        <li>Where a part uses an earlier answer, follow through: mark the method using the student’s earlier answer.</li>
        <li>Do not take marks off for a missing $ sign or unit if the number is correct; note it for feedback.</li>
        <li>Rounding: accept 1 or 2 decimal places unless the question asks for a set number of places.</li>
      </ul>
    </div>
  </div>
  ${pageFoot('<span>Marking guide</span>')}
</section>`;
  const p3 = `
<section class="page mg">${pageHead(null)}
  <div class="content">
    <div><h1>Reporting</h1><p class="sub">Each section is one content area, so each section total can be reported on its own.</p></div>
    <table class="rep">
      <tr><th>Section</th><th>Content area</th><th>Where it comes from</th><th>Marks</th><th>Share of test</th></tr>
      ${sections.map((s) => `<tr><td><b>${s.id}</b></td><td><b>${s.title}</b><br>${s.topics}</td><td>${s.source}</td><td>${s.marks}</td><td>${Math.round((s.marks / TOTAL) * 100)}%</td></tr>`).join('')}
      <tr><td></td><td><b>Chapter reviews and booklets (Sections A–C)</b></td><td>Chapters 1, 2 and 4</td><td><b>${chapterMarks}</b></td><td><b>${Math.round((chapterMarks / TOTAL) * 100)}%</b></td></tr>
      <tr><td></td><td><b>Rest of the Year 10 syllabus (Section D)</b></td><td>Algebraic techniques, equations, linear relationships, Pythagoras’ theorem, trigonometry</td><td><b>${TOTAL - chapterMarks}</b></td><td><b>${Math.round(((TOTAL - chapterMarks) / TOTAL) * 100)}%</b></td></tr>
    </table>
    <p class="cv-h" style="margin-top:1mm">Class record</p>
    <table class="rec">
      <tr><th style="text-align:left">Student</th>${sections.map((s) => `<th>${s.id} / ${s.marks}</th>`).join('')}<th>Total / ${TOTAL}</th><th>%</th></tr>
      ${Array.from({ length: 16 }, (_, i) => `<tr><td><span style="color:#9da1a6;font-size:7.5pt;padding-left:1.5mm">${i + 1}</span></td>${sections.map(() => '<td class="m"></td>').join('')}<td class="m"></td><td class="m"></td></tr>`).join('')}
      <tr><td style="font-weight:600;padding-left:1.5mm">Class average</td>${sections.map(() => '<td class="m"></td>').join('')}<td class="m"></td><td class="m"></td></tr>
    </table>
  </div>
  ${pageFoot('<span>Marking guide</span>')}
</section>`;
  return [p1, p2, p3];
};

// ---------- assemble ----------
const doc = (pages, key) => {
  const total = pages.length;
  const body = pages.map((p, i) => p.replace('{{PN}}', i + 1).replace('{{PT}}', total)
    .replace('<section class="page', key && !p.includes('page mg') ? '<section class="page"><div class="keybar">MARKING GUIDE · ANSWERS IN RED</div><section class="pg-inner' : '<section class="page')).join('');
  return `<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>Year 10 ${TEST.title} ${TEST.year}${key ? ' · Marking guide' : ''}</title>
<style>${css}</style></head><body class="${key ? 'keymode' : ''}">${body}</body></html>`;
};

// The answer pages keep the test's page numbers, so the key bar is drawn inside the same page box.
const keyDoc = () => {
  const test = testPages();
  const all = [...guidePages(), ...test];
  const total = all.length;
  const body = all.map((p, i) => {
    let h = p.replace('{{PN}}', i + 1).replace('{{PT}}', total);
    if (!p.includes('page mg')) h = h.replace(/<section class="page( extra)?">/, (m) => `${m}<div class="keybar">MARKING GUIDE · ANSWERS IN RED</div>`);
    return h;
  }).join('');
  return `<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>Year 10 ${TEST.title} ${TEST.year} · Marking guide</title>
<style>${css}</style></head><body class="keymode">${body}</body></html>`;
};

const studentDoc = () => {
  const all = [cover(), ...testPages()];
  const total = all.length;
  const body = all.map((p, i) => p.replace('{{PN}}', i + 1).replace('{{PT}}', total)).join('');
  return `<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>Year 10 ${TEST.title} ${TEST.year}</title>
<style>${css}</style></head><body>${body}</body></html>`;
};

// ---------- layout checks (run in the browser) ----------
const check = () => {
  const MM = 3.78, out = [];
  const r = (el) => el.getBoundingClientRect();
  document.querySelectorAll('.page').forEach((p, i) => {
    const pg = `page ${i + 1}`;
    const c = p.querySelector('.content');
    if (!c) return;
    const cb = r(c);
    if (c.scrollHeight > c.clientHeight + 1) out.push(`${pg}: content overflows by ${Math.round((c.scrollHeight - c.clientHeight) / MM)} mm`);
    p.querySelectorAll('.q, .info, .banner, .help, svg.fig, table, .ans, .choice').forEach((el) => {
      const b = r(el);
      if (b.bottom > cb.bottom + 1 || b.right > cb.right + 1) out.push(`${pg}: ${el.className.baseVal ?? el.className} runs off the page (q ${el.closest('[data-q]')?.dataset.q || '-'})`);
      const box = el.parentElement.closest('.q');
      if (box) { const pb = r(box); if (b.bottom > pb.bottom + 1 || b.right > pb.right + 1) out.push(`${pg}: ${el.className.baseVal ?? el.className} spills out of question ${box.dataset.q}`); }
    });
    p.querySelectorAll('.q').forEach((q) => {
      if (q.scrollHeight > q.clientHeight + 2) out.push(`${pg}: question ${q.dataset.q} is cut off at the bottom`);
      q.querySelectorAll('.q-text, .p-text, .opt, td, th').forEach((t) => { if (t.scrollWidth > t.clientWidth + 2) out.push(`${pg}: text too wide in question ${q.dataset.q}: "${t.textContent.trim().slice(0, 40)}"`); });
      const marks = +q.querySelector('.q-marks').textContent.split(' ')[0];
      q.querySelectorAll('.work').forEach((w) => {
        const h = r(w).height / MM;
        if (h < 14) out.push(`${pg}: working space in question ${q.dataset.q} is only ${h.toFixed(0)} mm`);
      });
      void marks;
    });
    const wk = [...p.querySelectorAll('.q .work')].map((w) => `${w.closest('.q').dataset.q}:${(r(w).height / MM).toFixed(0)}`);
    if (wk.length) out.push(`info ${pg}: working heights (mm) ${wk.join(' ')}`);
  });
  return out;
};

// ---------- build ----------
(async () => {
  let chromium;
  try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'))); }
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const jobs = [
    ['Year10-Transition-Yearly-Test', studentDoc()],
    ['Year10-Transition-Yearly-Test-Marking-Guide', keyDoc()],
  ];
  let problems = 0;
  for (const [name, html] of jobs) {
    const htmlPath = path.join(ROOT, `${name}.html`); // beside assets/ so relative paths work
    fs.writeFileSync(htmlPath, html);
    const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
    await page.goto(`file://${htmlPath}`);
    await page.evaluate(() => document.fonts.ready);
    const res = await page.evaluate(check);
    res.filter((x) => !x.startsWith('info')).forEach((x) => { problems++; console.log(`  ! ${name}: ${x}`); });
    if (process.argv.includes('--verbose')) res.filter((x) => x.startsWith('info')).forEach((x) => console.log(`    ${x}`));
    await page.pdf({ path: path.join(OUT, `${name}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
    if (shotsDir) {
      fs.mkdirSync(shotsDir, { recursive: true });
      const els = await page.$$('.page');
      for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(shotsDir, `${name}-p${String(i + 1).padStart(2, '0')}.png`) });
    }
    const pages = await page.$$eval('.page', (x) => x.length);
    console.log(`${name}.pdf: ${pages} pages`);
    await page.close();
    fs.unlinkSync(htmlPath);
  }
  await browser.close();
  console.log(`Total ${TOTAL} marks, ${n} questions, suggested time ${TIME} min. ${problems ? `${problems} layout problem(s).` : 'Layout checks passed.'}`);
  sections.forEach((s) => console.log(`  Section ${s.id} ${s.title}: Q${s.first}-${s.last}, ${s.marks} marks (${Math.round((s.marks / TOTAL) * 100)}%)`));
})();
