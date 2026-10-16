// Builds the six-page revision booklet for the Year 10 transition yearly test.
// Page 1 cover and checklist, pages 2-5 one test section each (key ideas, worked examples, Try these), page 6 answers.
// The practice questions use different numbers from the test. Every answer is calculated here.
// Usage: node revision.js [--shots <dir>]
const fs = require('fs');
const path = require('path');
const F = require('./lib/figs');
const { sections } = require('./test');

const ROOT = __dirname;
const OUT = path.join(ROOT, '..', 'Yearly test');
const NAME = 'Year10-Transition-Yearly-Test-Revision';
const shotsIdx = process.argv.indexOf('--shots');
const shotsDir = shotsIdx > 0 ? path.resolve(process.argv[shotsIdx + 1]) : null;
const css = fs.readFileSync(path.join(ROOT, 'lib/test.css'), 'utf8') + fs.readFileSync(path.join(ROOT, 'lib/revision.css'), 'utf8');

// ---------- numbers ----------
const NB = '\u202F'; // narrow no-break space, so $1 500 never splits across lines
const group = (s) => s.replace(/\B(?=(\d{3})+(?!\d))/g, NB);
const money = (x) => { const [d, c] = (Math.round(x * 100) / 100).toFixed(2).split('.'); return `$${group(d)}.${c}`; };
const num = (x, dp = 0) => { const [d, c] = x.toFixed(dp).split('.'); return c ? `${group(d)}.${c}` : group(d); };
const frac = (a, b) => `<span class="fr"><span>${a}</span><span>${b}</span></span>`;
const nw = (t) => `<span class="nw">${t}</span>`;
const pi = Math.PI;
const tan = (deg) => Math.tan((deg * pi) / 180);
const i = (v) => `<i>${v}</i>`;
const sup = (b, p) => `${b}<sup>${p}</sup>`;

// Section marks and question numbers, the same way the test builder counts them.
let qn = 0;
sections.forEach((s) => {
  const real = s.qs.filter((q) => q.type !== 'info');
  s.first = qn + 1; qn += real.length; s.last = qn;
  s.marks = real.reduce((a, q) => a + q.marks, 0);
});
const S = Object.fromEntries(sections.map((s) => [s.id, s]));

// ---------- content ----------
// card: { t: title, r: rule (formula or fact), x: worked example, fig }
// try:  { q: question, a: answer (short), w: working shown on the answers page, unit, pre,
//         lines: several labelled answer lines [{ pre, unit }], fig: a small table or graph beside the question }
// None of the examples or practice questions share numbers or answers with the test.
const stats = [4, 9, 2, 8, 4, 12, 10];
const sorted = [...stats].sort((a, b) => a - b);
const stem = { 1: [2, 5], 2: [0, 3, 3, 8], 3: [1, 4] };
const stemData = Object.entries(stem).flatMap(([s, ls]) => ls.map((l) => 10 * s + l));
const modeOf = (xs) => { const c = {}; xs.forEach((x) => { c[x] = (c[x] || 0) + 1; }); return +Object.keys(c).sort((a, b) => c[b] - c[a])[0]; };
const slTable = (rows, key) => `<table class="sl rv-sl"><tr><th>Stem</th><th>Leaf</th></tr>${Object.entries(rows).map(([s, ls]) => `<tr><td>${s}</td><td>${ls.join('&nbsp; ')}</td></tr>`).join('')}<tr><td colspan="2" class="sl-key">${key}</td></tr></table>`;
const trendPic = () => `<svg class="fig mini" viewBox="0 0 34 20" width="30mm" height="17.6mm" xmlns="http://www.w3.org/2000/svg">
  <line x1="4" y1="2" x2="4" y2="17" stroke="#1f2328" stroke-width="0.5"/><line x1="4" y1="17" x2="32" y2="17" stroke="#1f2328" stroke-width="0.5"/>
  <polyline points="7,4 12,6.5 17,7.5 22,11 27,12.5 31,15" fill="none" stroke="#1f2328" stroke-width="0.8"/>
  ${[[7, 4], [12, 6.5], [17, 7.5], [22, 11], [27, 12.5], [31, 15]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="0.9" fill="#1f2328"/>`).join('')}
  <text x="18" y="19.6" font-size="2.6" text-anchor="middle" fill="#1f2328">Month</text></svg>`;
const yTable = (xs) => `<table class="rv-vt"><tr><th><i>x</i></th>${xs.map((x) => `<td>${x}</td>`).join('')}</tr><tr><th><i>y</i></th>${xs.map(() => '<td></td>').join('')}</tr></table>`;

const PAGES = {
  A: {
    cards: [
      { t: 'Percentages', r: '% → decimal: ÷ 100 &nbsp;(15% = 0.15)<br>Score as a %: score ÷ total × 100', x: `15% of $240 = ${nw('0.15 × 240 = $36')}` },
      { t: 'Increase and decrease', r: 'Use a multiplier:<br>up 8% → × 1.08 &nbsp;·&nbsp; down 8% → × 0.92', x: `Increase $50 by 10%: ${nw('50 × 1.1 = $55')}` },
      { t: 'GST (10%)', r: 'Add GST: × 1.1<br>GST in a price (GST inc.): ÷ 11', x: `$44 (GST inc.): GST = ${nw('44 ÷ 11 = $4')}` },
      { t: 'Profit, mark-up, discount', r: 'Profit = selling price − cost price<br>Mark-up 20% → × 1.2 &nbsp;·&nbsp; discount 25% (25% off) → × 0.75', x: `Cost $10, mark-up 20%: ${nw('10 × 1.2 = $12')}, ${nw('profit = $2')}` },
      { t: 'Wages and overtime', r: 'Pay = hours × hourly rate<br>Time and a half × 1.5 &nbsp;·&nbsp; double time × 2', x: `$20 an hour, 3 hours at time and a half: ${nw('3 × 1.5 × 20 = $90')}` },
      { t: 'Commission, gross and net pay', r: 'Commission = % of sales<br>Gross pay = total pay before anything is taken out<br>Net pay (take-home pay) = gross pay − tax − super', x: `5% of $2${NB}000 = ${nw('0.05 × 2000 = $100')}` },
      { t: 'Loans', r: 'Total repaid = repayment × number of months (1 year = 12 months, 2 years = 24 months)<br>Interest = total repaid − amount borrowed', x: `Borrow $500, pay $50 a month for 1 year: ${nw('50 × 12 = $600')}, ${nw('interest $100')}` },
      { t: 'Simple and compound interest', r: `Simple: ${nw(`${i('I')} = ${i('P')} × ${i('R')} × ${i('N')}`)} &nbsp;·&nbsp; Compound: ${nw(`${i('A')} = ${i('P')}(1 + ${i('R')})${sup('', i('n'))}`)}<br>${i('P')} = amount invested, ${i('R')} = rate as a decimal (5% = 0.05), ${i('N')} or ${i('n')} = number of years`, x: `$1${NB}000 at 5% for 2 years: simple ${nw('1000 × 0.05 × 2 = $100')}; compound ${nw(`1000 × 1.05${sup('', 2)} = $1${NB}102.50`)}, ${nw('interest $102.50')}` },
    ],
    tries: [
      { q: 'A shop buys a hat for $12. It adds a 25% mark-up. How much profit does the shop make?', pre: '$', a: money(12 * 0.25), w: '12 × 1.25 = $15; 15 − 12' },
      { q: 'A jacket costs $66 (GST inc.). How much GST is in the price?', pre: '$', a: money(66 / 11), w: '66 ÷ 11' },
      { q: 'Shoes cost $90. They are 30% off. Find the new price.', pre: '$', a: money(90 * 0.7), w: '90 × 0.7' },
      { q: 'Lena earns $18 an hour. She works 2 hours of overtime at time and a half. How much is the overtime pay?', pre: '$', a: money(2 * 1.5 * 18), w: '2 × 1.5 × 18' },
      { q: `Jack earns 3% commission on sales of $1${NB}500. Find his commission.`, pre: '$', a: money(0.03 * 1500), w: '0.03 × 1500' },
      { q: 'Ava’s gross pay is $900. She pays $120 tax and $40 super. Find her net pay.', pre: '$', a: money(900 - 120 - 40), w: '900 − 120 − 40' },
      { q: 'Sam borrows $800 and repays $40 a month for 2 years. How much interest does he pay?', pre: '$', a: money(40 * 24 - 800), w: '40 × 24 = $960; 960 − 800' },
      { q: `$1${NB}000 is invested at 6% a year for 2 years. Find the interest with simple interest, then with compound interest.`, lines: [{ pre: 'simple $' }, { pre: 'compound $' }], a: `simple ${money(1000 * 0.06 * 2)}, compound ${money(1000 * 1.06 ** 2 - 1000)}`, w: `1000 × 0.06 × 2; 1000 × 1.06${sup('', 2)} = 1123.60, − 1000` },
    ],
  },
  B: {
    cards: [
      { t: 'Converting units', r: 'km → m × 1000 &nbsp;·&nbsp; m → cm × 100 &nbsp;·&nbsp; cm → mm × 10<br>L → mL × 1000 &nbsp;·&nbsp; kg → g × 1000 &nbsp;·&nbsp; going back: ÷', x: `2.4 km = ${nw(`2.4 × 1000 = 2${NB}400 m`)}` },
      { t: 'Scientific notation', r: 'One digit (1 to 9) before the decimal point, × a power of 10.<br>The power = how many places the point moves.', x: `${nw(`3${NB}400${NB}000 = 3.4 × ${sup(10, 6)}`)} (6 places)<br>${nw(`0.0005 = 5 × ${sup(10, '−4')}`)} (small: negative power)` },
      { t: 'Perimeter', r: 'Add up the lengths of all the sides.<br>Rectangle: 2 × (length + width)', x: `8 m by 3 m: ${nw('2 × (8 + 3) = 22 m')}` },
      { t: 'Circles', r: `${nw(`${i('C')} = 2 × π × ${i('r')}`)} (circumference)<br>${nw(`${i('A')} = π × ${i('r')} × ${i('r')}`)} (area)<br>${i('r')} is the radius (half the diameter)`, x: `Radius 5 cm:<br>${nw(`${i('C')} = 2 × π × 5 = ${num(2 * pi * 5, 1)} cm`)}<br>${nw(`${i('A')} = π × 5 × 5 = ${num(pi * 25, 1)} cm²`)}`, fig: F.circleRadius({ r: 6.5, label: '<tspan font-size="2.8" font-style="italic">r</tspan>' }) },
      { t: 'Area', r: 'Rectangle: length × width<br>Triangle: ½ × base × height<br>Trapezium: ½ × (top + bottom) × height (top and bottom are the parallel sides)', x: `Triangle with base 8 cm, height 5 cm: ${nw('½ × 8 × 5 = 20 cm²')}` },
      { t: 'Surface area', r: 'Add the area of every face.<br>A box has 3 pairs of matching faces.', x: `${nw('4 cm × 3 cm × 2 cm')} box: faces 12, 8 and 6 cm²; ${nw('2 × (12 + 8 + 6) = 52 cm²')}` },
      { t: 'Volume', r: `Box: length × width × height (cube: side × side × side)<br>Cylinder: ${nw(`${i('V')} = π × ${i('r')} × ${i('r')} × ${i('h')}`)}`, x: `${i('r')} = 3 cm, ${i('h')} = 10 cm: ${nw(`π × 3 × 3 × 10 = ${num(pi * 90, 1)} cm³`)}` },
      { t: 'Capacity', r: '1 cm³ holds 1 mL<br>1 m³ holds 1000 L', x: `A box with volume 250 cm³ holds ${nw('250 mL')}` },
    ],
    tries: [
      { q: 'Change 4.2 km into metres, and 3.5 L into millilitres.', lines: [{ unit: 'm' }, { unit: 'mL' }], a: `${num(4.2 * 1000)} m, ${num(3.5 * 1000)} mL`, w: '4.2 × 1000; 3.5 × 1000' },
      { q: `Write ${nw(`6${NB}300${NB}000`)} in scientific notation.`, a: `6.3 × ${sup(10, 6)}`, w: '6.3 (one digit before the point); the point moves 6 places' },
      { q: 'Find the perimeter of a rectangle 9&nbsp;m long and 5&nbsp;m wide.', unit: 'm', a: num(2 * (9 + 5)), w: '2 × (9 + 5)' },
      { q: 'A circle has radius 4&nbsp;cm. Find its circumference, to 1 decimal place.', unit: 'cm', a: num(2 * pi * 4, 1), w: '2 × π × 4' },
      { q: 'A circle has radius 4&nbsp;cm. Find its area, to 1 decimal place.', unit: 'cm²', a: num(pi * 16, 1), w: 'π × 4 × 4' },
      { q: 'A trapezium has parallel sides 4&nbsp;cm and 8&nbsp;cm, and height 5&nbsp;cm. Find its area.', unit: 'cm²', a: num(0.5 * (4 + 8) * 5), w: '½ × (4 + 8) × 5' },
      { q: `Find the surface area of a box ${nw('5 cm × 3 cm × 2 cm')}.`, unit: 'cm²', a: num(2 * (15 + 10 + 6)), w: '2 × (15 + 10 + 6)' },
      { q: 'A cylinder has radius 3&nbsp;cm and height 5&nbsp;cm. Find its volume (to 1 d.p.) and how many mL it holds.', lines: [{ unit: 'cm³' }, { unit: 'mL' }], a: `${num(pi * 9 * 5, 1)} cm³, ${num(pi * 9 * 5, 1)} mL`, w: 'π × 3 × 3 × 5; 1 cm³ holds 1 mL' },
    ],
  },
  C: {
    cards: [
      { t: 'Types of data', r: '<strong>Categorical</strong> (words): nominal, no order (eye colour) or ordinal, in order (small, medium, large)<br><strong>Numerical</strong> (numbers): discrete, counted (number of goals) or continuous, measured (height)', x: '' },
      { t: 'Mean, median, mode, range', r: 'Mean: add them up, ÷ how many<br>Median: middle number (in order)<br>Mode: most common &nbsp;·&nbsp; Range: biggest − smallest', x: `3, 4, 4, 13, 16: mean ${nw('40 ÷ 5 = 8')}, median 4, mode 4, range ${nw('16 − 3 = 13')}` },
      { t: 'Stem-and-leaf plots', r: 'The stem is the tens digit. Each leaf is a ones digit.', x: `Stem 2, leaf 5 ${nw('means 25')}`, fig: slTable({ 1: [3, 8], 2: [5, 5, 7] }, '2 | 5 means 25') },
      { t: 'Frequency tables', r: 'Total = add up the frequency column<br>Percentage frequency = frequency ÷ total × 100', x: `6 out of 24: ${nw('6 ÷ 24 × 100 = 25%')}` },
      { t: 'Histograms and shape', r: 'A column graph for groups. Each column is as tall as its frequency. The columns touch.', x: '', fig: `<div class="pics">${F.shapePic([1, 3, 5, 3, 1], 'symmetrical')}${F.shapePic([5, 4, 2, 1, 1], 'skewed')}</div>` },
      { t: 'Time-series graphs', r: 'Data over time. The trend is the overall direction.', x: 'The line goes up over time: <strong>upward trend</strong>. The line goes down: <strong>downward trend</strong>.' },
      { t: 'Probability', r: 'Probability = number of ways it can happen ÷ total number of ways<br>P(red) means “the probability of red” &nbsp;·&nbsp; 0 = impossible &nbsp;·&nbsp; 1 = certain', x: `A bag has 3 red and 7 blue counters: ${nw(`P(red) = ${frac(3, 10)}`)}`, wide: true },
    ],
    tries: [
      { q: 'What type of data is “hair colour”?', a: 'categorical, nominal', w: 'words, no order' },
      { q: `Data: ${stats.join(', ')}. Find the mean.`, a: num(stats.reduce((a, b) => a + b, 0) / stats.length), w: `${stats.reduce((a, b) => a + b, 0)} ÷ ${stats.length}` },
      { q: `Data: ${stats.join(', ')}. Find the median and the range.`, lines: [{ pre: 'median =' }, { pre: 'range =' }], a: `median ${sorted[3]}, range ${sorted[6] - sorted[0]}`, w: `in order: ${sorted.join(', ')}; range ${sorted[6]} − ${sorted[0]}` },
      { q: 'Use the stem-and-leaf plot. Find the lowest score and the mode.', fig: slTable(stem, '1 | 2 means 12'), lines: [{ pre: 'lowest =' }, { pre: 'mode =' }], a: `lowest ${Math.min(...stemData)}, mode ${modeOf(stemData)}`, w: '1 | 2 means 12; 23 appears twice' },
      { q: '5 out of 25 students walk to school. What percentage is this?', unit: '%', a: num((5 / 25) * 100), w: '5 ÷ 25 × 100' },
      { q: 'A letter is chosen from COCONUT. Find P(C) and P(vowel). (Vowels: A, E, I, O, U)', lines: [{ pre: 'P(C) =' }, { pre: 'P(vowel) =' }], a: `${frac(2, 7)}, ${frac(3, 7)}`, w: '2 C’s out of 7 letters; O, O, U' },
      { q: 'Describe the trend of this graph.', fig: trendPic(), a: 'downward trend', w: 'the line goes down over time' },
      { q: 'Is this histogram symmetrical or skewed?', fig: F.shapePic([1, 2, 5, 2, 1], ''), a: 'symmetrical', w: 'both sides match' },
    ],
  },
  D: {
    cards: [
      { t: 'Index laws', r: 'Multiply: <b>add</b> the powers<br>Divide: <b>subtract</b> the powers', x: `${nw(`${sup(i('y'), 3)} × ${sup(i('y'), 2)} = ${sup(i('y'), 5)}`)} &nbsp;·&nbsp; ${nw(`${sup(i('y'), 6)} ÷ ${sup(i('y'), 2)} = ${sup(i('y'), 4)}`)}` },
      { t: 'Substitution', r: `Put the number in place of the letter. ${nw(`3${i('a')} means 3 × ${i('a')}`)}.`, x: `${i('a')} = 5: ${nw(`3${i('a')} + 2 = 3 × 5 + 2 = 17`)}` },
      { t: 'Solving equations', r: 'Do the <b>opposite</b> to both sides.', x: `${nw(`2${i('x')} + 5 = 17`)} → take away 5: ${nw(`2${i('x')} = 12`)} → divide by 2: ${nw(`${i('x')} = 6`)}<br>${nw(`${frac(`${i('x')} + 3`, 2)} = 5`)} → times by 2: ${nw(`${i('x')} + 3 = 10`)} → take away 3: ${nw(`${i('x')} = 7`)}` },
      { t: 'Straight-line graphs', r: `Make a table of values, plot the points, join with a ruler.<br>${nw(`${i('y')} = ${i('m')}${i('x')} + ${i('c')}`)}: ${i('m')} is the gradient (how steep the line is), ${i('c')} is the ${i('y')}-intercept (where the line crosses the ${i('y')}-axis)`, x: `${nw(`${i('y')} = 5${i('x')} + 2`)}: gradient 5, ${i('y')}-intercept 2` },
      { t: 'Pythagoras’ theorem', r: `${nw(`${sup(i('c'), 2)} = ${sup(i('a'), 2)} + ${sup(i('b'), 2)}`)}<br>${i('c')} is the hypotenuse, the longest side`, x: `${i('a')} = 5, ${i('b')} = 12:<br>${nw(`${sup(i('c'), 2)} = 25 + 144 = 169`)}<br>${nw(`${i('c')} = √169 = 13`)}`, fig: F.rightTriangle({ base: 20, up: 13, lb: '<tspan font-size="3" font-style="italic">a</tspan>', lu: '<tspan font-size="3" font-style="italic">b</tspan>', lh: '<tspan font-size="3" font-style="italic">c</tspan>' }) },
      { t: 'Trigonometry', r: 'Use tan: tan (angle) = opposite ÷ adjacent<br>so opposite = adjacent × tan (angle)', x: `Angle 30°, adjacent 10 cm:<br>${nw(`10 × tan 30° = ${num(10 * tan(30), 1)} cm`)}<br>Calculator in <b>DEG</b> mode.`, fig: F.rightTriangle({ base: 20, up: 12, lb: '<tspan font-size="2.6">adjacent</tspan>', lu: '<tspan font-size="2.6">opposite</tspan>', angle: '' }) },
    ],
    tries: [
      { q: `Simplify ${sup(i('p'), 5)} × ${sup(i('p'), 3)}.`, a: sup(i('p'), 8), w: 'add the powers: 5 + 3' },
      { q: `If ${i('b')} = 6, find ${nw(`4${i('b')} − 5`)}.`, a: num(4 * 6 - 5), w: '4 × 6 − 5' },
      { q: `Solve ${nw(`3${i('x')} + 4 = 22`)}.`, pre: `${i('x')} =`, a: num((22 - 4) / 3), w: `take away 4: 3${i('x')} = 18; divide by 3` },
      { q: `Solve ${nw(`${frac(`${i('x')} − 1`, 2)} = 4`)}.`, pre: `${i('x')} =`, a: num(4 * 2 + 1), w: `times by 2: ${i('x')} − 1 = 8; add 1` },
      { q: `For ${nw(`${i('y')} = 3${i('x')} + 2`)}, find ${i('y')} when ${i('x')} = 0, 1 and 2. Fill in the table.`, fig: yTable([0, 1, 2]), noLine: true, a: [0, 1, 2].map((x) => 3 * x + 2).join(', '), w: '3 × 0 + 2, 3 × 1 + 2, 3 × 2 + 2' },
      { q: `Write the gradient and ${i('y')}-intercept of ${nw(`${i('y')} = 3${i('x')} + 2`)}.`, lines: [{ pre: 'gradient =' }, { pre: `${i('y')}-intercept =` }], a: 'gradient 3, y-intercept 2', w: `${i('m')} = 3, ${i('c')} = 2` },
      { q: 'A right-angled triangle has short sides 9&nbsp;cm and 12&nbsp;cm. Find the hypotenuse.', unit: 'cm', a: num(Math.hypot(9, 12)), w: '81 + 144 = 225, √225' },
      { q: 'A right-angled triangle has an angle of 40°. The side next to it (adjacent) is 10&nbsp;cm. Find the opposite side, to 1 decimal place.', unit: 'cm', a: num(10 * tan(40), 1), w: '10 × tan 40°' },
    ],
  },
};

// ---------- pieces ----------
const head = (s) => `
  <header class="ph"><img src="assets/kingscliff-logo-large.png" alt="Kingscliff High School">
    <div class="t"><b>Year 10 Mathematics Yearly Test · Revision</b><br>Kingscliff High School</div>
    ${s ? `<span class="sec"><span>Section ${s.id}</span>${s.title}</span>` : ''}</header>`;
const foot = (n, right) => `<footer class="pf"><span>Kingscliff High School · Year 10 Mathematics</span><span class="pn">Page ${n} of 6</span>${right}</footer>`;

const card = (c) => `
  <div class="rv-card${c.wide ? ' wide' : ''}">
    <h3>${c.t}</h3>
    <div class="rv-body"><div class="rv-text"><p class="rv-rule">${c.r}</p>${c.x ? `<p class="rv-ex"><b>Example</b> ${c.x}</p>` : ''}</div>${c.fig ? `<div class="rv-fig">${c.fig}</div>` : ''}</div>
  </div>`;

const ansLine = (l) => `<span class="rv-al">${l.pre ? `<span>${l.pre}</span>` : ''}<span class="ln"></span>${l.unit ? `<span>${l.unit}</span>` : ''}</span>`;
const tryItem = (t, k) => `
  <div class="rv-q"><span class="rv-n">${k + 1}</span><div class="rv-qt${t.fig ? ' hasfig' : ''}">${t.fig ? `<span>${t.q}</span><div class="rv-qfig">${t.fig}</div>` : t.q}</div>
    <div class="rv-a${t.lines ? ' multi' : ''}">${t.noLine ? '' : (t.lines || [t]).map(ansLine).join('')}</div></div>`;

const sectionPage = (id, n) => {
  const s = S[id], p = PAGES[id];
  return `
<section class="page rv">${head(s)}
  <div class="content">
    <div class="rv-banner"><div class="letter"><span>SECTION</span><b>${id}</b></div>
      <div><h2>${s.title}</h2><p>In the test: Questions <b>${s.first}–${s.last}</b> · <b>${s.marks} marks</b> · about <b>${s.time} minutes</b></p></div></div>
    <p class="rv-h">Key ideas</p>
    <div class="rv-grid">${p.cards.map(card).join('')}</div>
    <div class="rv-try"><p class="rv-h">Try these <span>Work them out in your book · answers on page 6</span></p>
      <div class="rv-qs">${p.tries.map(tryItem).join('')}</div></div>
  </div>
  ${foot(n, `<span class="go">${n < 5 ? 'Next: Section ' + sections[n - 1].id + ' →' : 'Answers on page 6 →'}</span>`)}
</section>`;
};

const checklist = sections.map((s, k) => `
  <div class="rv-check"><p class="rv-ch"><b>${s.id}</b>${s.title}<span>page ${k + 2}</span></p>
    <table><tr><th></th><th>Can do</th><th>Practise</th></tr>${PAGES[s.id].cards.map((c) => `<tr><td>${c.t}</td><td class="tk"><i></i></td><td class="tk"><i></i></td></tr>`).join('')}</table></div>`).join('');

const cover = () => `
<section class="page rv rv-cover">
  <div class="content">
    <div class="cv-top"><img class="cv-logo" src="assets/kingscliff-logo-large.png" alt="Kingscliff High School"><span class="cv-series">YEAR 10 TRANSITION · 2026</span></div>
    <div class="cv-title"><h1>Yearly Test Revision</h1><p>Everything you need for the Year 10 Mathematics Yearly Test</p></div>
    <div class="cv-student" style="grid-template-columns:1.6fr 1fr"><div><span>Name</span><i></i></div><div><span>Class</span><i></i></div></div>
    <div class="cv-facts">
      <div class="fact"><span>Test time</span><b>1 hour 15 min</b><small>75 minutes</small></div>
      <div class="fact"><span>Total marks</span><b>55 marks</b><small>4 sections</small></div>
      <div class="fact"><span>Calculators</span><b>Allowed</b><small>bring your own</small></div>
      <div class="fact"><span>Bring</span><b>Pen, pencil</b><small>ruler, eraser, calculator</small></div>
    </div>
    <div class="rv-how">
      <p class="cv-h">How to use this booklet</p>
      <ol class="cv-steps">
        <li><i>1</i><span>Read the <b>key ideas</b> and <b>examples</b> for each section (pages 2–5).</span></li>
        <li><i>2</i><span>Do the <b>Try these</b> questions. Work them out in your book, then write the answer on the line.</span></li>
        <li><i>3</i><span>Check your answers on <b>page&nbsp;6</b>. Tick the checklist below.</span></li>
      </ol>
    </div>
    <div><p class="cv-h">My checklist <span class="rv-keyt"><i></i> I can do this &nbsp; <i></i> I need more practice</span></p>
      <div class="rv-checks">${checklist}</div></div>
  </div>
  ${foot(1, '<span class="go">Start on page 2 →</span>')}
</section>`;

const answersPage = () => `
<section class="page rv">${head(null)}
  <div class="content">
    <div class="rv-banner ans"><div class="letter"><span>CHECK</span><b>✓</b></div><div><h2>Answers</h2><p>The working is shown in grey. Got one wrong? Read that key idea again, then try it once more.</p></div></div>
    <div class="rv-answers">${sections.map((s) => `
      <div class="rv-ans"><p class="rv-ch"><b>${s.id}</b>${s.title}</p>
        <ol>${PAGES[s.id].tries.map((t) => `<li><b>${t.lines ? t.a : `${t.pre && !t.pre.startsWith('$') ? t.pre + ' ' : ''}${t.a}${t.unit ? (t.unit === '%' ? '%' : ` ${t.unit}`) : ''}`}</b><span class="wk">${t.w}</span></li>`).join('')}</ol></div>`).join('')}
    </div>
    <div class="rv-tips">
      <div><p class="cv-h">On test day</p><ul>
        <li>Check your calculator is in <b>DEG</b> mode.</li>
        <li>Read each question twice. Look for the <b>HELP</b> box.</li>
        <li>Show your working and write the <b>units</b>.</li>
        <li>Answer every question. Never leave a blank.</li></ul></div>
      <div><p class="cv-h">Calculator keys</p><ul>
        <li><b>^</b> or <b>x<sup>■</sup></b> for powers: 1.05 ^ 2</li>
        <li><b>π</b> for circles · <b>√</b> for Pythagoras</li>
        <li><b>tan</b> for trigonometry: 10 × tan 40</li>
        <li>Use brackets: (8 + 3) × 2</li></ul></div>
    </div>
  </div>
  ${foot(6, '<span class="end">Good luck!</span>')}
</section>`;

const html = () => {
  const body = [cover(), ...['A', 'B', 'C', 'D'].map((id, k) => sectionPage(id, k + 2)), answersPage()].join('')
    .split(/(<svg[\s\S]*?<\/svg>)/).map((x, k) => (k % 2 ? x : x.replace(/²/g, '<sup>2</sup>').replace(/³/g, '<sup>3</sup>'))).join('');
  return `<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>Year 10 Mathematics Yearly Test Revision</title><style>${css}</style></head><body>${body}</body></html>`;
};

// ---------- checks (in the browser) ----------
const check = () => {
  const MM = 3.78, out = [], r = (el) => el.getBoundingClientRect();
  document.querySelectorAll('.page').forEach((p, k) => {
    const pg = `page ${k + 1}`, c = p.querySelector('.content'), cb = r(c);
    if (c.scrollHeight > c.clientHeight + 1) out.push(`${pg}: content overflows by ${Math.round((c.scrollHeight - c.clientHeight) / MM)} mm`);
    p.querySelectorAll('.rv-card, .rv-q, .rv-try, .rv-ans, .rv-check, svg.fig, table').forEach((el) => {
      const b = r(el);
      if (b.bottom > cb.bottom + 1 || b.right > cb.right + 1) out.push(`${pg}: ${el.className.baseVal ?? el.className} runs off the page`);
    });
    p.querySelectorAll('.rv-card').forEach((el) => {
      if (el.scrollHeight > el.clientHeight + 2) out.push(`${pg}: card "${el.querySelector('h3').textContent}" is cut off`);
      el.querySelectorAll('.nw, svg.fig, .pics').forEach((t) => { if (r(t).right > r(el).right + 0.5) out.push(`${pg}: text or picture runs out of card "${el.querySelector('h3').textContent}"`); });
    });
    p.querySelectorAll('.rv-q').forEach((el) => { if (el.scrollHeight > el.clientHeight + 2) out.push(`${pg}: practice question cut off: ${el.textContent.trim().slice(0, 40)}`); });
  });
  return out;
};

(async () => {
  let chromium;
  try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'))); }
  fs.mkdirSync(OUT, { recursive: true });
  const htmlPath = path.join(ROOT, `${NAME}.html`);
  fs.writeFileSync(htmlPath, html());
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.goto(`file://${htmlPath}`);
  await page.evaluate(() => document.fonts.ready);
  const problems = await page.evaluate(check);
  problems.forEach((x) => console.log(`  ! ${x}`));
  await page.pdf({ path: path.join(OUT, `${NAME}.pdf`), format: 'A4', printBackground: true, preferCSSPageSize: true });
  if (shotsDir) {
    fs.mkdirSync(shotsDir, { recursive: true });
    const els = await page.$$('.page');
    for (let k = 0; k < els.length; k++) await els[k].screenshot({ path: path.join(shotsDir, `${NAME}-p${k + 1}.png`) });
  }
  console.log(`${NAME}.pdf: ${await page.$$eval('.page', (x) => x.length)} pages. ${problems.length ? `${problems.length} layout problem(s).` : 'Layout checks passed.'}`);
  await browser.close();
  if (!process.argv.includes("--keep-html")) fs.unlinkSync(htmlPath);
})();
