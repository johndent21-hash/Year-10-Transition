// SVG diagrams for the yearly test. Units are millimetres: each diagram prints at the size given.
// Anything with class "key" (answers drawn on a diagram) only shows in the marking guide.
const INK = '#1f2328';
const SOFT = '#e9eef0';
const KEY = '#c62828';
const FS = 3.7; // label size in mm (about 10.5 pt)

const svg = (w, h, body, cls = '') =>
  `<svg class="fig ${cls}" viewBox="0 0 ${w} ${h}" width="${w}mm" height="${h}mm" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
const text = (x, y, s, o = {}) =>
  `<text x="${x}" y="${y}" font-size="${o.fs || FS}" text-anchor="${o.anchor || 'middle'}" dominant-baseline="${o.base || 'middle'}" font-weight="${o.bold ? 600 : 400}" fill="${o.fill || INK}"${o.italic ? ' font-style="italic"' : ''}>${s}</text>`;
const line = (x1, y1, x2, y2, o = {}) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${o.stroke || INK}" stroke-width="${o.w || 0.45}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''} stroke-linecap="round"/>`;
const poly = (pts, o = {}) =>
  `<polygon points="${pts.map((p) => p.join(',')).join(' ')}" fill="${o.fill || 'none'}" stroke="${o.stroke || INK}" stroke-width="${o.w || 0.5}" stroke-linejoin="round"/>`;
const pline = (pts, o = {}) =>
  `<polyline points="${pts.map((p) => p.join(',')).join(' ')}" fill="none" stroke="${o.stroke || INK}" stroke-width="${o.w || 0.5}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''} stroke-linejoin="round"/>`;
// Right-angle mark at corner (x, y); (ax, ay) and (bx, by) are unit vectors along the two arms.
const rightAngle = (x, y, ax, ay, bx, by, s = 2.6) =>
  pline([[x + ax * s, y + ay * s], [x + ax * s + bx * s, y + ay * s + by * s], [x + bx * s, y + by * s]], { w: 0.35 });

// Rectangle with its length along the bottom and width on the right.
const rectangle = ({ w, h, bottom, right }) => {
  const W = w + 24, H = h + 14, x = 6, y = 4;
  return svg(W, H, poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], { fill: SOFT }) +
    rightAngle(x, y + h, 1, 0, 0, -1) + rightAngle(x + w, y, -1, 0, 0, 1) +
    text(x + w / 2, y + h + 5, bottom) + text(x + w + 3, y + h / 2, right, { anchor: 'start' }));
};

// Circle with a radius drawn from the centre.
const circleRadius = ({ r, label }) => {
  const W = 2 * r + 12, H = 2 * r + 8, cx = W / 2, cy = H / 2;
  return svg(W, H, `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${SOFT}" stroke="${INK}" stroke-width="0.5"/>` +
    `<circle cx="${cx}" cy="${cy}" r="0.8" fill="${INK}"/>` + line(cx, cy, cx + r, cy, { w: 0.5 }) +
    text(cx + r / 2, cy - 3, label));
};

// Triangle with a dashed perpendicular height. Base along the bottom, apex at fraction `apex` of the base.
const triangleHeight = ({ b, h, apex = 0.35, base, height }) => {
  const x = 6, y = 4, W = b + 14, H = h + 14, ax = x + b * apex;
  return svg(W, H, poly([[x, y + h], [x + b, y + h], [ax, y]], { fill: SOFT }) +
    line(ax, y, ax, y + h, { dash: '1.6 1.2', w: 0.4 }) + rightAngle(ax, y + h, 1, 0, 0, -1, 2.2) +
    text(x + b / 2, y + h + 5, base) + text(ax + 2.2, y + h / 2, height, { anchor: 'start' }));
};

// Trapezium with parallel sides a (top) and b (bottom) and a dashed height.
const trapezium = ({ a, b, h, top, bottom, height }) => {
  const x = 4, y = 7, W = b + 10, H = h + 18, off = (b - a) / 2;
  return svg(W, H, poly([[x, y + h], [x + b, y + h], [x + off + a, y], [x + off, y]], { fill: SOFT }) +
    line(x + off, y, x + off, y + h, { dash: '1.6 1.2', w: 0.4 }) + rightAngle(x + off, y + h, 1, 0, 0, -1, 2.2) +
    text(x + off + a / 2, y - 3.5, top) + text(x + b / 2, y + h + 5, bottom) + text(x + off + 2, y + h / 2, height, { anchor: 'start' }));
};

// Rectangular prism drawn in oblique view. l = length (across), d = depth (back), t = height, all in mm on paper.
const prism = ({ l, d, t, length, depth, height }) => {
  const dx = d * 0.75, dy = d * 0.5, x = 13, y = 4 + dy, W = x + l + dx + 13, H = t + dy + 14;
  const A = [x, y + t], B = [x + l, y + t], C = [x + l, y], D = [x, y];
  const sh = (p) => [p[0] + dx, p[1] - dy];
  return svg(W, H,
    poly([D, C, sh(C), sh(D)], { fill: '#f4f6f7' }) + poly([B, C, sh(C), sh(B)], { fill: '#dfe5e8' }) +
    poly([A, B, C, D], { fill: SOFT }) +
    pline([A, sh(A), sh(B)], { dash: '1.4 1.1', w: 0.35 }) + line(...sh(A), ...sh(D), { dash: '1.4 1.1', w: 0.35 }) +
    text(x + l / 2, y + t + 5, length) +
    text(x + l + dx / 2 + 2.5, y + t - dy / 2 + 2, depth, { anchor: 'start' }) +
    text(x - 1.5, y + t / 2, height, { anchor: 'end' }), 'prism');
};

// Cylinder of radius r and height h (mm on paper), with the radius drawn on the top face.
const cylinder = ({ r, h, radius, height }) => {
  const ry = r * 0.32, x = 4, y = 4 + ry, W = 2 * r + 24, H = h + 2 * ry + 8, cx = x + r;
  return svg(W, H,
    `<path d="M ${x} ${y} L ${x} ${y + h} A ${r} ${ry} 0 0 0 ${x + 2 * r} ${y + h} L ${x + 2 * r} ${y}" fill="${SOFT}" stroke="${INK}" stroke-width="0.5"/>` +
    `<path d="M ${x} ${y + h} A ${r} ${ry} 0 0 1 ${x + 2 * r} ${y + h}" fill="none" stroke="${INK}" stroke-width="0.35" stroke-dasharray="1.4 1.1"/>` +
    `<ellipse cx="${cx}" cy="${y}" rx="${r}" ry="${ry}" fill="#f4f6f7" stroke="${INK}" stroke-width="0.5"/>` +
    `<circle cx="${cx}" cy="${y}" r="0.7" fill="${INK}"/>` + line(cx, y, cx + r, y, { w: 0.5 }) +
    text(x + 2 * r + 2.5, y, radius, { anchor: 'start' }) +
    text(x + 2 * r + 2.5, y + h / 2, height, { anchor: 'start' }));
};

// Right-angled triangle with the right angle at bottom right.
// base = horizontal leg, up = vertical leg (mm). Labels: lb (base), lu (vertical), lh (hypotenuse). angle: label at bottom-left.
const rightTriangle = ({ base, up, lb, lu, lh, angle, lbSub, luSub }) => {
  const x = 6, y = 5, W = base + (luSub ? 26 : 22), H = up + (lbSub ? 18 : 14);
  const P = [x, y + up], Q = [x + base, y + up], R = [x + base, y];
  const len = Math.hypot(base, up), nx = -up / len, ny = -base / len; // outward normal of the hypotenuse
  let s = poly([P, Q, R], { fill: SOFT }) + rightAngle(Q[0], Q[1], -1, 0, 0, -1);
  if (lb) s += text(x + base / 2, y + up + 5, lb);
  if (lbSub) s += text(x + base / 2, y + up + 9.5, lbSub, { fs: 3.1, fill: '#565b61' });
  if (lu) s += text(x + base + 2.5, y + up / 2 - (luSub ? 2.2 : 0), lu, { anchor: 'start' });
  if (luSub) s += text(x + base + 2.5, y + up / 2 + 2.6, luSub, { anchor: 'start', fs: 3.1, fill: '#565b61' });
  if (lh) s += text(x + base / 2 + nx * 4, y + up / 2 + ny * 4 + 1, lh);
  if (angle) {
    const t = Math.atan2(up, base), rr = 9;
    s += `<path d="M ${x + rr} ${y + up} A ${rr} ${rr} 0 0 0 ${x + rr * Math.cos(t)} ${y + up - rr * Math.sin(t)}" fill="none" stroke="${INK}" stroke-width="0.35"/>`;
    s += text(x + rr + 4.5, y + up - 2.4, angle, { fs: 3.4 });
  }
  return svg(W, H, s);
};

// Histogram on a grid. classes: labels; freq: heights; drawn: how many columns are drawn for the student;
// the rest are drawn as answers (key). yMax: top of the frequency axis.
const histogram = ({ classes, freq, drawn, yMax, xTitle, yTitle, title }) => {
  const u = 5.2, col = 13, left = 16, top = 9, gap = col / 2; // u = mm per unit of frequency
  const plotW = gap + col * classes.length + 6, W = left + plotW + 3, H = top + yMax * u + 17;
  const y0 = top + yMax * u;
  let s = text(left + plotW / 2, 3.6, title, { bold: true, fs: 3.6 });
  for (let i = 0; i <= yMax; i++) {
    s += line(left, y0 - i * u, left + plotW, y0 - i * u, { stroke: '#c9ccd1', w: 0.25 });
    s += text(left - 2, y0 - i * u, i, { anchor: 'end', fs: 3.1 });
  }
  for (let i = 0; i <= classes.length * 2 + 2; i++) {
    const xx = left + (i * col) / 2;
    if (xx <= left + plotW) s += line(xx, top, xx, y0, { stroke: '#e1e3e6', w: 0.2 });
  }
  classes.forEach((c, i) => {
    const x = left + gap + i * col;
    const shape = `<rect x="${x}" y="${y0 - freq[i] * u}" width="${col}" height="${freq[i] * u}"`;
    s += i < drawn ? `${shape} fill="#b9c7cd" stroke="${INK}" stroke-width="0.45"/>`
      : `<g class="key">${shape} fill="none" stroke="${KEY}" stroke-width="0.7"/></g>`;
    s += text(x + col / 2, y0 + 4, c, { fs: 3.1 });
  });
  s += line(left, y0, left + plotW, y0, { w: 0.5 }) + line(left, top, left, y0, { w: 0.5 });
  s += text(left + plotW / 2, y0 + 10, xTitle, { fs: 3.4 });
  s += `<text x="5" y="${top + (yMax * u) / 2}" font-size="3.4" text-anchor="middle" transform="rotate(-90 5 ${top + (yMax * u) / 2})" fill="${INK}">${yTitle}</text>`;
  return svg(W, H, s, 'hist');
};

// Little pictures for the symmetrical / skewed help box.
const shapePic = (heights, label) => {
  const u = 1.8, c = 3.8, W = heights.length * c + 4, H = 6 * u + 8.5;
  let s = '';
  heights.forEach((v, i) => { s += `<rect x="${2 + i * c}" y="${2 + (6 - v) * u}" width="${c}" height="${v * u}" fill="#b9c7cd" stroke="${INK}" stroke-width="0.3"/>`; });
  s += line(1, 2 + 6 * u, W - 1, 2 + 6 * u, { w: 0.4 }) + text(W / 2, H - 2.6, label, { fs: 3, bold: true });
  return svg(W, H, s, 'mini');
};

// Line graph (time series). values per label; yStep is the gap between grid lines.
const lineGraph = ({ labels, values, yMax, yStep, xTitle, yTitle, title }) => {
  const left = 17, top = 9, step = 11, plotW = step * (labels.length - 1) + 12, plotH = 38;
  const W = left + plotW + 3, H = top + plotH + 17, y0 = top + plotH, k = plotH / yMax;
  let s = text(left + plotW / 2, 3.6, title, { bold: true, fs: 3.6 });
  for (let v = 0; v <= yMax; v += yStep) {
    s += line(left, y0 - v * k, left + plotW, y0 - v * k, { stroke: '#c9ccd1', w: 0.25 });
    s += text(left - 2, y0 - v * k, v, { anchor: 'end', fs: 3.1 });
  }
  const pts = values.map((v, i) => [left + 6 + i * step, y0 - v * k]);
  s += pline(pts, { w: 0.7 });
  pts.forEach((p, i) => { s += `<circle cx="${p[0]}" cy="${p[1]}" r="1" fill="${INK}"/>` + text(p[0], y0 + 4, labels[i], { fs: 3.1 }); });
  s += line(left, y0, left + plotW, y0, { w: 0.5 }) + line(left, top, left, y0, { w: 0.5 });
  s += text(left + plotW / 2, y0 + 10, xTitle, { fs: 3.4 });
  s += `<text x="5" y="${top + plotH / 2}" font-size="3.4" text-anchor="middle" transform="rotate(-90 5 ${top + plotH / 2})" fill="${INK}">${yTitle}</text>`;
  return svg(W, H, s, 'tgraph');
};

// Number plane for plotting a straight line. xs: x values to plot (key), f: rule.
const plane = ({ xMax, yMax, ux, uy, xs, f }) => {
  const left = 10, top = 5, W = left + xMax * ux + 10, H = top + yMax * uy + 12, y0 = top + yMax * uy;
  let s = '';
  for (let i = 0; i <= xMax; i++) {
    s += line(left + i * ux, top, left + i * ux, y0, { stroke: '#c9ccd1', w: 0.25 });
    s += text(left + i * ux, y0 + 3.8, i, { fs: 3.1 });
  }
  for (let j = 0; j <= yMax; j++) {
    s += line(left, y0 - j * uy, left + xMax * ux, y0 - j * uy, { stroke: '#c9ccd1', w: 0.25 });
    if (j) s += text(left - 2.2, y0 - j * uy, j, { anchor: 'end', fs: 3.1 });
  }
  s += line(left, y0, left + xMax * ux + 5, y0, { w: 0.55 }) + line(left, y0, left, top - 1, { w: 0.55 });
  s += poly([[left + xMax * ux + 6, y0], [left + xMax * ux + 3.5, y0 - 1.2], [left + xMax * ux + 3.5, y0 + 1.2]], { fill: INK, w: 0.2 });
  s += text(left + xMax * ux + 7.5, y0, '<tspan font-style="italic">x</tspan>', { anchor: 'start', fs: 3.6 });
  s += text(left + 2.5, top + 0.8, '<tspan font-style="italic">y</tspan>', { anchor: 'start', fs: 3.6 });
  const P = xs.map((x) => [left + x * ux, y0 - f(x) * uy]);
  s += `<g class="key">${pline(P, { stroke: KEY, w: 0.6 })}${P.map((p) => `<circle cx="${p[0]}" cy="${p[1]}" r="1.1" fill="${KEY}"/>`).join('')}</g>`;
  return svg(W, H, s, 'plane');
};

module.exports = { rectangle, circleRadius, triangleHeight, trapezium, prism, cylinder, rightTriangle, histogram, shapePic, lineGraph, plane };
