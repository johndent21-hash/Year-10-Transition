// The Year 10 transition yearly test: sections, questions, help boxes and answers.
// Every answer is calculated here from the numbers in the question, so the test and the marking guide always agree.
// 80% of the marks (Sections A to C, 44 marks) come from the three chapter reviews and the chapter booklets;
// 20% (Section D, 11 marks) come from the rest of the Stage 5 syllabus.
const F = require('./lib/figs');

// ---------- number formatting ----------
const NB = ' '; // thin space between thousands, as in the booklets ($4 900)
const group = (s) => s.replace(/\B(?=(\d{3})+(?!\d))/g, NB);
const money = (x) => {
  const [d, c] = (Math.round(x * 100) / 100).toFixed(2).split('.');
  return `$${group(d)}.${c}`;
};
const num = (x, dp = 0) => {
  const [d, c] = x.toFixed(dp).split('.');
  return c ? `${group(d)}.${c}` : group(d);
};
const round = (x, dp) => Math.round(x * 10 ** dp) / 10 ** dp;
const frac = (a, b) => `<span class="fr"><span>${a}</span><span>${b}</span></span>`;
const pi = Math.PI;

// ---------- help boxes ----------
// rows: [label, html] pairs. Labels are short: Formula, Example, Remember, Calculator.
const help = (...rows) => ({ rows });

// ---------- Section A: Financial mathematics (Chapter 1 review + Chapter 1 booklet) ----------
const A = [
  {
    marks: 1, type: 'mc', src: 'Ch 1 review MC 1 · Booklet 1.1', topic: 'Percentage of an amount',
    text: 'What is 28% of $89?',
    options: [money(28), money(0.28 * 89), money(0.72 * 89), money(1.28 * 89)], answer: 1,
  },
  {
    marks: 1, type: 'mc', src: 'Ch 1 review MC 3 · Booklet 1.2', topic: 'GST',
    text: 'A price tag says <b>“$55 (GST inc.)”</b>. How much GST is included in the price?',
    options: [money(55 / 11), money(5.5), money(50), money(60.5)], answer: 0,
    help: help(['Remember', 'GST in a price (GST inc.) = price ÷ 11']),
  },
  {
    marks: 1, type: 'mc', src: 'Ch 1 review MC 7 · Booklet 1.3', topic: 'Discount',
    text: 'A shirt costs $56. It is <b>discounted by 26%</b>. What is the new price?',
    options: [money(0.26 * 56), money(26.56), money(30), money(56 * 0.74)], answer: 3,
    help: help(['Remember', 'Find 26% of $56, then <b>take it off</b> the price.']),
  },
  {
    marks: 1, type: 'mc', src: 'Ch 1 review MC 9 · Booklet 1.6', topic: 'Simple interest',
    text: 'Find the <b>simple interest</b> on $600 at 5% per year for 4 years.',
    options: [money(12), money(600 * 0.05), money(600 * 0.05 * 4), money(720)], answer: 2,
    help: help(['Formula', '<i>I</i> = <i>P</i> × <i>R</i> × <i>N</i> &nbsp;(5% → 0.05)']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 1 review SA 2, 3 · Booklet 1.2', topic: 'Percentage increase and decrease',
    text: 'Use a multiplier and your calculator.',
    parts: [
      { text: 'Increase $968 by 12%.', pre: '$', key: money(968 * 1.12).slice(1) },
      { text: 'Decrease $4900 by 7%.'.replace('4900', `4${NB}900`), pre: '$', key: money(4900 * 0.93).slice(1) },
    ],
    help: help(['Remember', 'Increase by 8% → × 1.08<br>Decrease by 8% → × 0.92'], ['Example', 'Increase $50 by 10%:<br>50 × 1.10 = $55']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 1 review SA 4 · Booklet 1.3', topic: 'Mark-up and profit',
    text: 'A shop buys a cap for $7.60. This is the <b>cost price</b>. The shop adds a <b>50% mark-up</b>.',
    parts: [
      { text: 'Find the selling price of the cap.', pre: '$', key: money(7.6 * 1.5).slice(1) },
      { text: 'How much profit does the shop make?', pre: '$', key: money(7.6 * 0.5).slice(1) },
    ],
    help: help(['Remember', 'Mark-up of 50% → × 1.5<br>Profit = selling price − cost price'], ['Example', 'Cost $10, mark-up 20%:<br>10 × 1.2 = $12, profit = $2']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 1 review MC 4, 6 · Booklet 1.4', topic: 'Wages and overtime',
    text: 'Tom is paid $15.78 per hour.',
    parts: [
      { text: 'Tom works 30 hours. How much is he paid?', pre: '$', key: money(30 * 15.78).slice(1) },
      { text: 'Tom also works 4 hours of overtime at <b>time and a half</b>. How much is he paid for the overtime?', pre: '$', key: money(4 * 1.5 * 15.78).slice(1) },
    ],
    help: help(['Remember', 'Pay = hours × hourly rate<br>Time and a half = 1.5 × hourly rate'], ['Example', '$20 per hour, 3 hours at time and a half:<br>3 × 1.5 × 20 = $90']),
  },
  {
    marks: 1, type: 'sa', src: 'Ch 1 review SA 12 · Booklet 1.5', topic: 'Commission',
    text: 'Pedro sells phones. He earns <b>4.5% commission</b> on his sales. His sales this week are $790. How much commission does he earn?',
    parts: [{ pre: '$', key: money(0.045 * 790).slice(1) }],
    help: help(['Remember', '4.5% → 0.045<br>Commission = 0.045 × sales']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 1 review SA 10 · Booklet 1.5', topic: 'Gross and net pay',
    text: 'Tranh works 36 hours at $28.89 per hour.',
    parts: [
      { text: 'Find Tranh’s <b>gross pay</b> (total pay before anything is taken out).', pre: '$', key: money(36 * 28.89).slice(1) },
      { text: 'Tranh pays $142.59 in tax and $22.50 in super. Find his <b>net pay</b>.', pre: '$', key: money(36 * 28.89 - 142.59 - 22.5).slice(1) },
    ],
    help: help(['Remember', 'Gross pay = hours × hourly rate<br>Net pay = gross pay − tax − super']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 1 review ER 1 · Booklet 1.7', topic: 'Compound interest',
    text: `$5${NB}000 is invested at 4% per year, <b>compounding</b> each year for 3 years.`,
    parts: [
      { text: 'Find the value of the investment after 3 years.', pre: '$', key: money(5000 * 1.04 ** 3).slice(1) },
      { text: 'How much interest is earned?', pre: '$', key: money(5000 * 1.04 ** 3 - 5000).slice(1) },
    ],
    help: help(['Formula', '<i>A</i> = <i>P</i>(1 + <i>R</i>)<sup><i>n</i></sup><br><i>P</i> = amount invested, <i>R</i> = rate as a decimal, <i>n</i> = number of years'],
      ['Example', `$2${NB}000 at 5% for 2 years:<br><i>A</i> = 2000 × 1.05<sup>2</sup> = $2${NB}205<br>Interest = 2205 − 2000 = $205`],
      ['Calculator', 'Type 2000 × 1.05 ^ 2 =']),
  },
];

// ---------- Section B: Measurement (Chapter 2 review + Chapter 2 booklet) ----------
const B = [
  {
    marks: 1, type: 'mc', src: 'Ch 2 review MC 1 · Booklet 2.1', topic: 'Units of length',
    text: 'How many metres are in 1 kilometre?',
    options: ['10', '100', num(1000), num(10000)], answer: 2,
  },
  {
    marks: 1, type: 'mc', src: 'Ch 2 review MC 5 · Booklet 2.4', topic: 'Area of a rectangle',
    text: 'What is the <b>area</b> of a rectangle 3 cm long and 4 cm wide?',
    options: ['7 cm²', '12 cm', '14 cm', `${3 * 4} cm²`], answer: 3,
  },
  {
    marks: 1, type: 'mc', src: 'Ch 2 review MC 9 · Booklet 2.7', topic: 'Volume of a cube',
    text: 'What is the <b>volume</b> of a cube with sides 3 cm long?',
    options: ['9 cm³', `${3 ** 3} cm³`, '27 cm²', '54 cm³'], answer: 1,
    help: help(['Formula', 'Volume of a cube = side × side × side']),
  },
  {
    marks: 1, type: 'mc', src: 'Ch 2 review SA 8a', topic: 'Scientific notation',
    text: `Which of these is ${num(232000)} written in <b>scientific notation</b>?`,
    options: ['2.32 × 10<sup>5</sup>', '23.2 × 10<sup>4</sup>', '2.32 × 10<sup>−5</sup>', '232 × 10<sup>3</sup>'], answer: 0, optCols: 2,
    help: help(['Example', `2${NB}350${NB}000 = 2.35 × 10<sup>6</sup><br>(one digit before the decimal point)`]),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 2 review SA 1a · Booklet 2.1', topic: 'Converting units',
    text: 'Convert each measurement.',
    parts: [
      { text: 'Change 5.3 km into metres.', unit: 'm', key: num(5.3 * 1000), short: true },
      { text: 'Change 2.5 L into millilitres.', unit: 'mL', key: num(2.5 * 1000), short: true },
    ],
    help: help(['Remember', 'km → m: × 1000<br>L → mL: × 1000']),
  },
  {
    marks: 1, type: 'sa', src: 'Ch 2 review SA 3 · Booklet 2.2', topic: 'Perimeter',
    text: 'A farmer puts a fence all the way around this rectangular paddock. How many metres of fence are needed?',
    helpPos: 'top',
    fig: F.rectangle({ w: 40, h: 23, bottom: '12 m', right: '7 m' }),
    parts: [{ unit: 'm', key: num(2 * (12 + 7)) }],
    help: help(['Remember', 'Perimeter = add up the lengths of <b>all</b> the sides.']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 2 review SA 4 · Booklets 2.3, 2.5', topic: 'Circumference and area of a circle',
    text: 'This circle has a radius of 3 m. Give your answers to 1 decimal place.',
    fig: F.circleRadius({ r: 15, label: '3 m' }),
    parts: [
      { text: 'Find the <b>circumference</b>.', unit: 'm', key: num(round(2 * pi * 3, 1), 1) },
      { text: 'Find the <b>area</b>.', unit: 'm²', key: num(round(pi * 9, 1), 1) },
    ],
    help: help(['Formula', '<i>C</i> = 2 × π × <i>r</i> &nbsp;(circumference)<br><i>A</i> = π × <i>r</i> × <i>r</i> &nbsp;(area)'],
      ['Example', `Radius 5 cm:<br><i>C</i> = 2 × π × 5 = ${num(2 * pi * 5, 1)} cm<br><i>A</i> = π × 5 × 5 = ${num(pi * 25, 1)} cm²`]),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 2 review MC 6, SA 6 · Booklet 2.4', topic: 'Area of a triangle and a trapezium',
    text: 'Find the area of each shape.',
    partsRow: true,
    parts: [
      { text: 'Triangle', unit: 'cm²', key: num(0.5 * 10 * 6), fig: F.triangleHeight({ b: 34, h: 21, apex: 0.22, base: '10 cm', height: '6 cm' }) },
      { text: 'Trapezium', unit: 'cm²', key: num(0.5 * (3 + 7) * 4), fig: F.trapezium({ a: 15, b: 35, h: 20, top: '3 cm', bottom: '7 cm', height: '4 cm' }) },
    ],
    help: help(['Formula', 'Triangle: <i>A</i> = ½ × base × height<br>Trapezium: <i>A</i> = ½ × (<i>a</i> + <i>b</i>) × <i>h</i><br>(<i>a</i> and <i>b</i> are the parallel sides)'],
      ['Example', 'Triangle, base 8 cm, height 5 cm:<br>½ × 8 × 5 = 20 cm²']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 2 review SA 7b · Booklet 2.6', topic: 'Surface area of a prism',
    text: 'Find the <b>surface area</b> of this box. Complete the table. The first row is done for you.',
    figPos: 'main',
    fig: F.prism({ l: 50, d: 20, t: 10, length: '10 cm', depth: '4 cm', height: '2 cm' }),
    table: {
      head: ['Faces', 'Area of one face', 'Number of faces', 'Area'],
      rows: [
        ['Top and bottom', '10 × 4 = 40 cm²', '2', '80 cm²'],
        ['Front and back', { key: `10 × 2 = ${10 * 2} cm²` }, '2', { key: `${2 * 10 * 2} cm²` }],
        ['The two ends', { key: `4 × 2 = ${4 * 2} cm²` }, '2', { key: `${2 * 4 * 2} cm²` }],
      ],
      total: ['Surface area (add the last column)', { key: `${2 * (40 + 20 + 8)} cm²` }],
    },
    help: help(['Remember', 'A box has 6 faces, in 3 matching pairs.<br>Surface area = add the areas of all 6 faces.']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 2 review MC 10, SA 9 · Booklet 2.7', topic: 'Volume and capacity of a cylinder',
    text: 'This cylinder has a radius of 2 cm and a height of 6 cm.',
    fig: F.cylinder({ r: 13, h: 34, radius: '2 cm', height: '6 cm' }),
    parts: [
      { text: 'Find the <b>volume</b>, to 1 decimal place.', unit: 'cm³', key: num(round(pi * 4 * 6, 1), 1) },
      { text: 'How many millilitres (mL) of water can it hold?', unit: 'mL', key: num(round(pi * 4 * 6, 1), 1) },
    ],
    help: help(['Formula', 'Volume of a cylinder:<br><i>V</i> = π × <i>r</i> × <i>r</i> × <i>h</i>'],
      ['Example', `<i>r</i> = 3 cm, <i>h</i> = 10 cm:<br><i>V</i> = π × 3 × 3 × 10 = ${num(pi * 90, 1)} cm³`],
      ['Remember', '1 cm³ holds 1 mL']),
  },
];

// ---------- Section C: Statistics and probability (Chapter 4 review + Chapter 4 booklet) ----------
const stem = { 2: [4, 9], 3: [1, 1, 7, 8], 4: [2, 4, 6], 5: [0, 4] };
const stemData = Object.entries(stem).flatMap(([s, ls]) => ls.map((l) => 10 * s + l));
const modeOf = (xs) => { const c = {}; xs.forEach((x) => { c[x] = (c[x] || 0) + 1; }); return +Object.keys(c).sort((a, b) => c[b] - c[a])[0]; };
const q25 = [8, 3, 13, 1, 5, 3, 9];
const q25s = [...q25].sort((a, b) => a - b);
const travel = { classes: ['0–9', '10–19', '20–29', '30–39'], freq: [9, 6, 3, 2] };
const travelTotal = travel.freq.reduce((a, b) => a + b, 0);
const word = 'INTEREST';
const count = (pred) => [...word].filter(pred).length;
const sales = { labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], values: [12, 15, 19, 22, 27, 30] };

const C = [
  {
    marks: 1, type: 'mc', src: 'Ch 4 review MC 6 · Booklet 4.1', topic: 'Types of data',
    text: 'A survey asks: <b>“What is your favourite sport to play?”</b> What type of data does this give?',
    options: ['numerical and discrete', 'numerical and continuous', 'categorical and ordinal', 'categorical and nominal'], answer: 3,
    optCols: 2,
    help: help(['Remember', 'Categorical = words or groups. Numerical = numbers.<br>Nominal = no order (colours, sports). Ordinal = has an order (small, medium, large).']),
  },
  {
    type: 'info', html: () => `
      <div class="info-row">
        <p>Use this <b>stem-and-leaf plot</b> for Questions <b>{{n+1}}</b> and <b>{{n+2}}</b>.<br>It shows the scores of 11 players in a game.</p>
        <table class="sl">
          <tr><th>Stem</th><th>Leaf</th></tr>
          ${Object.entries(stem).map(([s, ls]) => `<tr><td>${s}</td><td>${ls.join('&nbsp; ')}</td></tr>`).join('')}
          <tr><td colspan="2" class="sl-key">4 | 2 means 42</td></tr>
        </table>
      </div>`,
  },
  {
    marks: 1, type: 'mc', src: 'Ch 4 review MC 7 · Booklet 4.5', topic: 'Reading a stem-and-leaf plot',
    text: 'What is the <b>lowest</b> score?',
    options: ['4', '20', String(Math.min(...stemData)), '54'], answer: 2,
  },
  {
    marks: 1, type: 'mc', src: 'Ch 4 review MC 8 · Booklets 4.4, 4.5', topic: 'Mode',
    text: 'What is the <b>mode</b> (the most common score)?',
    options: ['3', String(modeOf(stemData)), '38', '42'], answer: 1,
  },
  {
    marks: 1, type: 'mc', src: 'Ch 4 review SA 1b', topic: 'Probability',
    text: 'A normal 6-sided die is rolled once. What is the probability of rolling an <b>even</b> number?',
    options: [frac(1, 6), frac(1, 3), frac(1, 2), frac(2, 3)], answer: 2,
    help: help(['Formula', 'Probability = number of ways it can happen ÷ total number of outcomes']),
  },
  {
    marks: 3, type: 'sa', src: 'Ch 4 review MC 9, SA 8 · Booklet 4.4', topic: 'Mean, median and range',
    text: `Here are the number of goals scored by a netball player in 7 games:<br><span class="data">${q25.join(',&nbsp; ')}</span>`,
    order: { n: q25.length, key: q25s },
    parts: [
      { text: 'Find the <b>mean</b>.', key: num(q25.reduce((a, b) => a + b, 0) / q25.length), short: true },
      { text: 'Find the <b>median</b>.', key: num(q25s[(q25.length - 1) / 2]), short: true },
      { text: 'Find the <b>range</b>.', key: num(q25s[q25.length - 1] - q25s[0]), short: true },
    ],
    help: help(['Mean', 'Add up the numbers, then ÷ how many there are'], ['Median', 'The middle number, when they are in order'], ['Range', 'Biggest − smallest']),
  },
  {
    marks: 2, type: 'sa', src: 'Ch 4 review SA 2', topic: 'Probability',
    text: `One letter is chosen at random from the word <span class="word">${[...word].map((l) => `<b>${l}</b>`).join('')}</span>`,
    parts: [
      { text: 'Find the probability that the letter is an <b>E</b>.', compact: true, key: `${frac(count((l) => l === 'E'), word.length)} or ${frac(1, 4)}`, keyText: '2/8 = 1/4' },
      { text: 'Find the probability that the letter is a <b>vowel</b> (A, E, I, O or U).', compact: true, key: frac(count((l) => 'AEIOU'.includes(l)), word.length), keyText: '3/8' },
    ],
    help: help(['Formula', 'Probability = number of ways it can happen ÷ total number of outcomes'],
      ['Example', `A letter from <b>BOOK</b>: P(O) = ${frac(2, 4)} = ${frac(1, 2)}`]),
  },
  {
    marks: 1, type: 'sa', src: 'Booklet 4.7', topic: 'Time-series graphs',
    text: 'This <b>time-series graph</b> shows how many umbrellas a shop sold each month.',
    figPos: 'main',
    fig: F.lineGraph({ ...sales, yMax: 35, yStep: 5, xTitle: 'Month', yTitle: 'Umbrellas sold', title: 'Umbrellas sold each month' }),
    parts: [{ text: 'Describe the <b>trend</b>. Circle one.', choice: ['upward trend', 'downward trend', 'no trend'], key: 'upward trend' }],
    help: help(['Remember', 'Upward trend: the line goes up over time.<br>Downward trend: the line goes down over time.']),
  },
  {
    marks: 4, type: 'sa', src: 'Ch 4 review SA 6 · Booklets 4.2, 4.3, 4.6', topic: 'Frequency tables, histograms and shape',
    text: 'Some students recorded how many minutes it takes them to travel to school.',
    freqTable: { head: ['Minutes', 'Frequency'], rows: travel.classes.map((c, i) => [c, travel.freq[i]]), total: { key: String(travelTotal) } },
    fig: F.histogram({ ...travel, drawn: 2, yMax: 10, xTitle: 'Minutes', yTitle: 'Frequency', title: 'Time to travel to school' }),
    parts: [
      { text: 'Fill in the <b>total</b> at the bottom of the table.', key: String(travelTotal), noLine: true, noWork: true, keyNote: `Total = ${travel.freq.join(' + ')} = ${travelTotal}` },
      { text: 'What <b>percentage</b> of the students took 0–9 minutes?', unit: '%', key: num((travel.freq[0] / travelTotal) * 100) },
      { text: 'Two columns of the histogram are drawn. <b>Draw the columns</b> for 20–29 and 30–39.', noLine: true, noWork: true, keyNote: `Columns of height ${travel.freq[2]} and ${travel.freq[3]}, touching, shown on the graph.` },
      { text: 'Is the data <b>symmetrical</b> or <b>skewed</b>? Circle one.', choice: ['symmetrical', 'skewed'], key: 'skewed' },
    ],
    help: help(['Formula', 'Percentage = frequency ÷ total × 100'], ['Shapes', 'pics']),
  },
];

// ---------- Section D: Other Year 10 topics (rest of the Stage 5 syllabus) ----------
const tableX = [0, 1, 2, 3];
const D = [
  {
    marks: 1, type: 'mc', src: 'Syllabus: Algebraic techniques', topic: 'Simplifying',
    text: 'Simplify &nbsp;<b>4<i>x</i> + 3<i>x</i></b>',
    options: [`${4 + 3}<i>x</i>`, '12<i>x</i>', '7<i>x</i><sup>2</sup>', '7'], answer: 0,
  },
  {
    marks: 1, type: 'sa', src: 'Syllabus: Algebraic techniques', topic: 'Substitution',
    text: 'If <b><i>a</i> = 4</b>, find the value of <b>5<i>a</i> − 2</b>.',
    parts: [{ key: num(5 * 4 - 2) }],
    help: help(['Remember', '5<i>a</i> means 5 × <i>a</i>'], ['Example', 'If <i>a</i> = 3, then 2<i>a</i> + 1 = 2 × 3 + 1 = 7']),
  },
  {
    marks: 2, type: 'sa', src: 'Syllabus: Equations', topic: 'Solving equations',
    text: 'Solve each equation.',
    parts: [
      { text: '<i>x</i> + 9 = 15', pre: '<i>x</i> =', key: num(15 - 9) },
      { text: '2<i>x</i> + 3 = 13', pre: '<i>x</i> =', key: num((13 - 3) / 2) },
    ],
    help: help(['Remember', 'Do the <b>opposite</b> to both sides.'],
      ['Example', '3<i>x</i> + 1 = 13<br>Take away 1: &nbsp;3<i>x</i> = 12<br>Divide by 3: &nbsp;<i>x</i> = 4']),
  },
  {
    marks: 3, type: 'sa', src: 'Syllabus: Linear relationships', topic: 'Table of values and graphing a line',
    text: 'The rule for a straight line is <b><i>y</i> = 2<i>x</i> + 1</b>.',
    valueTable: { xs: tableX, ys: tableX.map((x) => 2 * x + 1) },
    fig: F.plane({ xMax: 4, yMax: 9, ux: 11, uy: 6, xs: tableX, f: (x) => 2 * x + 1 }),
    parts: [
      { text: 'Complete the table of values.', marks: 2, noLine: true, noWork: true, keyNote: '2 marks: all four correct. 1 mark: two or three correct.' },
      { text: 'Plot the points on the grid and join them with a straight line.', marks: 1, noLine: true, noWork: true, keyNote: 'Points plotted correctly and joined with a ruled straight line.' },
    ],
    help: help(['Example', 'For <i>y</i> = 3<i>x</i> + 2, when <i>x</i> = 4:<br><i>y</i> = 3 × 4 + 2 = 14']),
  },
  {
    marks: 2, type: 'sa', src: 'Syllabus: Pythagoras’ theorem (Ch 2 review ER 2a)', topic: 'Pythagoras’ theorem',
    text: 'Find the length of the <b>hypotenuse</b>, <i>c</i>.',
    fig: F.rightTriangle({ base: 44, up: 33, lb: '8 cm', lu: '6 cm', lh: '<tspan font-style="italic">c</tspan>' }),
    parts: [{ pre: '<i>c</i> =', unit: 'cm', key: num(Math.hypot(6, 8)) }],
    help: help(['Formula', '<i>c</i><sup>2</sup> = <i>a</i><sup>2</sup> + <i>b</i><sup>2</sup> &nbsp;(<i>c</i> is the longest side)'],
      ['Example', '<i>a</i> = 3, <i>b</i> = 4:<br><i>c</i><sup>2</sup> = 9 + 16 = 25<br><i>c</i> = √25 = 5']),
  },
  {
    marks: 2, type: 'sa', src: 'Syllabus: Trigonometry', topic: 'Trigonometry: finding a side',
    text: 'Find the length of side <i>x</i>, to 1 decimal place.',
    fig: F.rightTriangle({ base: 40, up: 40 * Math.tan((35 * pi) / 180), lb: '8 cm', lbSub: '(adjacent)', lu: '<tspan font-style="italic">x</tspan>', luSub: '(opposite)', angle: '35°' }),
    parts: [{ pre: '<i>x</i> =', unit: 'cm', key: num(round(8 * Math.tan((35 * pi) / 180), 1), 1) }],
    help: help(['Formula', 'tan θ = opposite ÷ adjacent<br>so opposite = adjacent × tan θ'],
      ['Example', `Angle 20°, adjacent 5 cm:<br><i>x</i> = 5 × tan 20° = ${num(5 * Math.tan((20 * pi) / 180), 1)} cm`],
      ['Calculator', 'Check your calculator shows <b>D</b> or <b>DEG</b> (degrees).']),
  },
];

const sections = [
  { id: 'A', title: 'Financial mathematics', time: 20, topics: 'Percentages, GST, profit, discount, wages, commission, interest', qs: A, source: 'Chapter 1 review and booklet' },
  { id: 'B', title: 'Measurement', time: 20, topics: 'Units, perimeter, circles, area, surface area, volume', qs: B, source: 'Chapter 2 review and booklet' },
  { id: 'C', title: 'Statistics and probability', time: 20, topics: 'Types of data, stem-and-leaf, mean, median, graphs, probability', qs: C, source: 'Chapter 4 review and booklet' },
  { id: 'D', title: 'Other Year 10 topics', time: 15, topics: 'Algebra, equations, straight-line graphs, Pythagoras, trigonometry', qs: D, source: 'Rest of the Year 10 syllabus' },
];

// Which questions go on each page (by position in the section's list, info blocks included).
const layout = {
  A: [[0, 1, 2, 3, 4], [5, 6, 7], [8, 9]],
  B: [[0, 1, 2, 3, 4], [5, 6, 7], [8, 9]],
  C: [[0, 1, 2, 3, 4], [5, 6, 7], [8]],
  D: [[0, 1, 2], [3, 4], [5]],
};

module.exports = { sections, layout, figs: F, frac };
