from ff import *

PI = 'Round to <b>2 decimal places</b>.'


def lab(x, y, s, a='middle', col=INK, size=10):
    return text(x, y, s, a, col, size)


def prism(front, depth, s, ang=35, k=0.5, labels='', ox=0, oy=0):
    """Oblique prism. front: polygon in units (x right, y up). Painter's algorithm for faces."""
    dx = depth * s * k * math.cos(math.radians(ang))
    dy = -depth * s * k * math.sin(math.radians(ang))
    F = [(ox + x * s, oy - y * s) for x, y in front]
    B = [(x + dx, y + dy) for x, y in F]
    area = sum(F[i][0] * F[(i + 1) % len(F)][1] - F[(i + 1) % len(F)][0] * F[i][1] for i in range(len(F)))
    out = poly(B, 'none', 1, '3 3')
    for i in range(len(F)):
        a, b = F[i], F[(i + 1) % len(F)]
        ex, ey = b[0] - a[0], b[1] - a[1]
        nx, ny = (ey, -ex) if area > 0 else (-ey, ex)   # outward normal (screen coords)
        if nx * dx + ny * dy > 0:
            out += poly([a, b, (b[0] + dx, b[1] + dy), (a[0] + dx, a[1] + dy)], '#F4E5B5')
    out += poly(F, FILL)
    return out + labels


# ------------------------------------------------------------------ diagrams
def ruler():
    s = 22; x0, y0 = 10, 34
    x0 = 26
    out = f'<rect x="{x0 - 6}" y="{y0}" width="{8 * s + 12}" height="30" rx="3" fill="#FFF8E2" stroke="{INK}" stroke-width="1.3"/>'
    for mm in range(0, 81):
        x = x0 + mm * s / 10
        hgt = 11 if mm % 10 == 0 else (7 if mm % 5 == 0 else 4)
        out += line(x, y0, x, y0 + hgt, 0.8)
        if mm % 10 == 0:
            out += text(x, y0 + 22, str(mm // 10), size=8.5)
    out += f'<rect x="{x0}" y="{y0 - 14}" width="{6.3 * s}" height="12" rx="2" fill="{ACC}" opacity=".85"/>'
    out += text(x0 - 4, y0 + 22, 'cm', 'end', size=8)
    out += line(x0 + 6.3 * s, y0 - 18, x0 + 6.3 * s, y0 + 12, 1, '2 2', '#B33')
    return svg(8 * s + 40, 72, out, 1.15)


def lshape():
    s = 10; ox, oy = 26, 94
    P = [(0, 0), (10, 0), (10, 5), (6, 5), (6, 8), (0, 8)]
    pts = [(ox + x * s, oy - y * s) for x, y in P]
    out = poly(pts)
    out += lab(ox + 50, oy + 13, '10 m') + lab(ox - 4, oy - 40, '8 m', 'end') + lab(ox + 30, oy - 84, '6 m')
    out += lab(ox + 63, oy - 68, '3 m', 'start') + lab(ox + 86, oy - 54, '?', col=ACC, size=11) + lab(ox + 104, oy - 22, '?', 'start', ACC, 11)
    return svg(140, 112, out, 1.1)


def tri_x():
    s = 8.6; ox, oy = 8, 56
    A, B = (ox, oy), (ox + 14 * s, oy)
    C = (ox + 145 / 28 * s, oy - math.sqrt(49 - (145 / 28) ** 2) * s)
    out = poly([A, B, C]) + lab((A[0] + B[0]) / 2, oy + 13, '2<tspan font-style="italic">x</tspan>')
    out += lab((A[0] + C[0]) / 2 - 6, (A[1] + C[1]) / 2 - 2, '<tspan font-style="italic">x</tspan>', 'end')
    out += lab((B[0] + C[0]) / 2 + 6, (B[1] + C[1]) / 2 - 2, '<tspan font-style="italic">x</tspan> + 3', 'start')
    return svg(140, 72, out)


def fence():
    s = 6; ox, oy = 10, 84
    W, H = 18 * s, 12 * s
    out = f'<rect x="{ox}" y="{oy - H}" width="{W}" height="{H}" fill="{FILL}" stroke="none"/>'
    g0, g1 = ox + 7.5 * s, ox + 10.5 * s
    out += poly([(g0, oy), (ox, oy), (ox, oy - H), (ox + W, oy - H), (ox + W, oy), (g1, oy)], close=False)
    out += line(g0, oy, g0 + 2 * s, oy - 2.2 * s, 1.3)
    out += lab(ox + W / 2, oy - H - 5, '18 m') + lab(ox + W + 4, oy - H / 2 + 4, '12 m', 'start') + lab((g0 + g1) / 2, oy + 13, 'gate 3 m', col=ACC, size=9.5)
    return svg(150, 100, out)


def stairs():
    s = 20; ox, oy = 12, 92
    P = [(0, 0), (4, 0), (4, 4), (3, 4), (3, 3), (2, 3), (2, 2), (1, 2), (1, 1), (0, 1)]
    out = poly([(ox + x * s, oy - y * s) for x, y in P])
    out += lab(ox + 40, oy + 13, '4 m') + lab(ox + 4 * s + 4, oy - 36, '4 m', 'start')
    return svg(130, 104, out)


def semi_quarter():
    s = 8
    out = sector_path(50, 56, 5 * s, 0, 180) + dot(50, 56, 1.8) + lab(50, 70, '10 cm')
    out += sector_path(134, 66, 6 * s, 0, 90) + lab(158, 78, '6 cm') + lab(130, 42, '6 cm', 'end') + rightangle(134, 66, 1, -1)
    return svg(190, 82, out, 1.15)

def track():
    s = 1.05; ox, oy = 40, 12
    L, D = 85 * s, 64 * s; r = D / 2
    out = (f'<path d="M{ox},{oy} L{ox + L},{oy} A{r},{r} 0 0 1 {ox + L},{oy + D} L{ox},{oy + D} A{r},{r} 0 0 1 {ox},{oy} Z" '
           f'fill="{FILL}" stroke="{INK}" stroke-width="1.6"/>')
    out += line(ox + L, oy, ox + L, oy + D, 1, '3 3') + lab(ox + L - 4, oy + r + 4, '64 m', 'end')
    out += lab(ox + L / 2, oy - 4, '85 m')
    return svg(int(ox * 2 + L), int(D + 22), out)


def tri_para():
    s = 7.5; oy = 58
    out = poly([(6, oy), (6 + 9 * s, oy), (6 + 3 * s, oy - 6 * s)]) + line(6 + 3 * s, oy, 6 + 3 * s, oy - 6 * s, 1, '3 3') + rightangle(6 + 3 * s, oy, 1, -1, 6)
    out += lab(6 + 4.5 * s, oy + 12, '9 cm') + lab(6 + 3 * s + 3, oy - 12, '6 cm', 'start', size=9)
    x0 = 92
    out += poly([(x0, oy), (x0 + 8 * s, oy), (x0 + 10 * s, oy - 5 * s), (x0 + 2 * s, oy - 5 * s)])
    out += line(x0 + 2 * s, oy, x0 + 2 * s, oy - 5 * s, 1, '3 3') + rightangle(x0 + 2 * s, oy, 1, -1, 6)
    out += lab(x0 + 4 * s, oy + 12, '8 cm') + lab(x0 + 2 * s + 3, oy - 15, '5 cm', 'start', size=9)
    return svg(176, 74, out, 1.35)

def trap_rhombus():
    s = 6.5; oy = 58
    out = poly([(6, oy), (6 + 10 * s, oy), (6 + 8 * s, oy - 5 * s), (6 + 2 * s, oy - 5 * s)])
    out += line(6 + 2 * s, oy, 6 + 2 * s, oy - 5 * s, 1, '3 3') + rightangle(6 + 2 * s, oy, 1, -1, 6)
    out += lab(6 + 5 * s, oy + 12, '10 cm') + lab(6 + 5 * s, oy - 5 * s - 4, '6 cm') + lab(6 + 2 * s + 3, oy - 14, '5 cm', 'start', size=9)
    cx, cy, q = 128, 34, 9
    out += poly([(cx - 4 * q, cy), (cx, cy - 3 * q), (cx + 4 * q, cy), (cx, cy + 3 * q)])
    out += line(cx - 4 * q, cy, cx + 4 * q, cy, 1, '3 3') + line(cx, cy - 3 * q, cx, cy + 3 * q, 1, '3 3')
    out += lab(cx, cy + 3 * q + 11, 'diagonals 8 cm and 6 cm', size=8.5)
    return svg(176, 76, out, 1.3)

def backyard():
    s = 7; ox, oy = 8, 74
    out = f'<rect x="{ox}" y="{oy - 9 * s}" width="{15 * s}" height="{9 * s}" fill="#E2F0E5" stroke="{INK}" stroke-width="1.6"/>'
    out += f'<rect x="{ox + 6 * s}" y="{oy - 6 * s}" width="{6 * s}" height="{3 * s}" fill="#CFE3F1" stroke="{INK}" stroke-width="1.4"/>'
    out += lab(ox + 9 * s, oy - 4.2 * s, 'pool', size=9) + lab(ox + 9 * s, oy - 6 * s - 3, '6 m', size=9) + lab(ox + 12 * s + 3, oy - 3.5 * s, '3 m', 'start', size=9)
    out += lab(ox + 7.5 * s, oy + 12, '15 m') + lab(ox + 15 * s + 4, oy - 4.5 * s + 4, '9 m', 'start')
    return svg(150, 88, out)


def wall():
    s = 17; ox, oy = 8, 80
    out = poly([(ox, oy), (ox + 6 * s, oy), (ox + 6 * s, oy - 2.4 * s), (ox + 3 * s, oy - 3.9 * s), (ox, oy - 2.4 * s)])
    out += line(ox, oy - 2.4 * s, ox + 6 * s, oy - 2.4 * s, 1, '3 3') + line(ox + 3 * s, oy - 2.4 * s, ox + 3 * s, oy - 3.9 * s, 1, '3 3')
    out += lab(ox + 3 * s, oy + 12, '6 m') + lab(ox + 6 * s + 4, oy - 1.2 * s + 4, '2.4 m', 'start') + lab(ox + 3 * s + 3, oy - 2.85 * s, '1.5 m', 'start', size=9)
    return svg(160, 94, out)


def two_circles():
    out = circle(32, 34, 25) + dot(32, 34, 1.8) + line(32, 34, 57, 34, 1.2) + lab(43, 30, '5 cm', size=8.5)
    out += circle(112, 34, 22.5) + line(89.5, 34, 134.5, 34, 1.2) + dot(112, 34, 1.8) + lab(112, 30, '9 m', size=9)
    return svg(150, 68, out, 1.4)


def semi_quarter_area():
    s = 5
    out = sector_path(30, 50, 4 * s, 0, 180) + dot(30, 50, 1.6) + line(30, 50, 50, 50, 1.2) + lab(40, 62, '4 cm', size=9)
    out += sector_path(76, 60, 10 * s, 0, 90) + rightangle(76, 60, 1, -1) + lab(101, 72, '10 cm', size=9)
    return svg(140, 76, out, 1.35)


def two_sectors():
    s = 8.5
    out = sector_path(10, 62, 6 * s, 0, 60) + lab(32, 74, '6 cm', size=9) + lab(22, 56, '60°', 'start', ACC, 9)
    out += text(30, 12, 'A', weight=700)
    cx = 128
    out += sector_path(cx, 62, 4 * s, 0, 135) + lab(cx + 17, 74, '4 cm', size=9) + lab(cx + 6, 50, '135°', 'middle', ACC, 9)
    out += text(cx + 8, 12, 'B', weight=700)
    return svg(170, 80, out, 1.2)


def pizza():
    r = 38; cx, cy = 42, 42
    out = circle(cx, cy, r)
    out += sector_path(cx, cy, r, 45, 90, '#E9C35A')
    for k in range(8):
        a = math.radians(45 * k)
        out += line(cx, cy, cx + r * math.cos(a), cy - r * math.sin(a), 1)
    out += lab(cx, cy + r + 12, '30 cm diameter', size=9)
    return svg(90, 96, out)


def ring():
    s = 5.6; cx, cy = 50, 50
    out = circle(cx, cy, 8 * s, '#E9C35A') + circle(cx, cy, 5 * s, '#fff')
    out += dot(cx, cy, 1.8) + line(cx, cy, cx + 8 * s * 0.7071, cy - 8 * s * 0.7071, 1.1) + lab(cx + 30, cy - 34, '8 cm', 'start', size=9)
    out += line(cx, cy, cx + 5 * s, cy, 1.1) + lab(cx + 14, cy + 12, '5 cm', size=9)
    return svg(110, 100, out)


def rect_semi():
    s = 9.5; ox, oy = 6, 62
    w, h = 8 * s, 5 * s
    out = (f'<path d="M{ox},{oy} L{ox + w},{oy} A{h / 2},{h / 2} 0 0 0 {ox + w},{oy - h} L{ox},{oy - h} Z" fill="{FILL}" stroke="{INK}" stroke-width="1.6"/>')
    out += line(ox + w, oy, ox + w, oy - h, 1, '3 3') + lab(ox + w / 2, oy + 12, '8 cm') + lab(ox - 2, oy - h / 2 + 4, '', 'end')
    out += lab(ox + w - 4, oy - h / 2 + 4, '5 cm', 'end', size=9.5)
    return svg(112, 76, out)


def lshape2():
    s = 6.8; ox, oy = 32, 74
    P = [(0, 0), (12, 0), (12, 5), (7, 5), (7, 9), (0, 9)]
    out = poly([(ox + x * s, oy - y * s) for x, y in P])
    out += lab(ox + 6 * s, oy + 12, '12 cm') + lab(ox - 4, oy - 4.5 * s + 4, '9 cm', 'end') + lab(ox + 3.5 * s, oy - 9 * s - 4, '7 cm')
    out += lab(ox + 7 * s + 3, oy - 8 * s + 3, '4 cm', 'start', size=9) + lab(ox + 9.5 * s, oy - 5 * s - 4, '5 cm', size=9)
    return svg(124, 90, out, 1.1)

def house():
    s = 11; ox, oy = 8, 84
    out = poly([(ox, oy), (ox + 6 * s, oy), (ox + 6 * s, oy - 4 * s), (ox + 3 * s, oy - 7 * s), (ox, oy - 4 * s)])
    out += line(ox, oy - 4 * s, ox + 6 * s, oy - 4 * s, 1, '3 3') + line(ox + 3 * s, oy - 4 * s, ox + 3 * s, oy - 7 * s, 1, '3 3')
    out += lab(ox + 3 * s, oy + 12, '6 m') + lab(ox + 6 * s + 4, oy - 2 * s + 4, '4 m', 'start') + lab(ox + 3 * s + 3, oy - 4.4 * s, '3 m', 'start', size=9)
    return svg(100, 98, out, 1.2)

def square_circle():
    s = 7.5; ox, oy = 6, 6
    out = f'<rect x="{ox}" y="{oy}" width="{10 * s}" height="{10 * s}" fill="#E9C35A" stroke="{INK}" stroke-width="1.6"/>'
    out += circle(ox + 5 * s, oy + 5 * s, 5 * s, '#fff') + lab(ox + 5 * s, oy + 10 * s + 13, '10 cm')
    return svg(90, 100, out)


def field():
    s = 0.95; ox, oy = 34, 8
    L, D = 100 * s, 60 * s; r = D / 2
    out = (f'<path d="M{ox},{oy} L{ox + L},{oy} A{r},{r} 0 0 1 {ox + L},{oy + D} L{ox},{oy + D} A{r},{r} 0 0 1 {ox},{oy} Z" '
           f'fill="#E2F0E5" stroke="{INK}" stroke-width="1.6"/>')
    out += f'<rect x="{ox}" y="{oy}" width="{L}" height="{D}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>'
    out += lab(ox + L / 2, oy + D / 2 + 4, '100 m') + lab(ox + L - 4, oy + D / 2 + 18, '60 m', 'end', size=9)
    return svg(int(L + 2 * ox), int(D + 16), out)


def window():
    s = 46; ox, oy = 10, 112
    w, h = 1.2 * s, 1.5 * s
    out = (f'<path d="M{ox},{oy} L{ox + w},{oy} L{ox + w},{oy - h} A{w / 2},{w / 2} 0 0 0 {ox},{oy - h} Z" fill="#DDEBF3" stroke="{INK}" stroke-width="2"/>')
    out += line(ox, oy - h, ox + w, oy - h, 1, '3 3') + lab(ox + w / 2, oy + 12, '1.2 m') + lab(ox + w + 4, oy - h / 2 + 4, '1.5 m', 'start')
    return svg(110, 126, out)


def cube_box():
    b1, x1, _ = box3d(4, 4, 4, 9, ox=4, oy=None, labels=('4 cm', '', ''))
    b2, _, _ = box3d(5, 3, 2, 11, ox=x1 + 36, oy=26, labels=('5 cm', '3 cm', '2 cm'))
    return svg(190, 84, b1 + b2, 1.2)

def net():
    s = 5.6; ox, oy = 4, 4
    faces = [(4, 0, 6, 3), (4, 3, 6, 4), (4, 7, 6, 3), (4, 10, 6, 4), (0, 3, 4, 4), (10, 3, 4, 4)]
    out = ''
    for x, y, w, h in faces:
        out += f'<rect x="{ox + x * s:.1f}" y="{oy + y * s:.1f}" width="{w * s:.1f}" height="{h * s:.1f}" fill="{FILL}" stroke="{INK}" stroke-width="1.3"/>'
    out += lab(ox + 7 * s, oy + 1.5 * s + 4, '6 cm', size=9) + lab(ox + 10 * s - 3, oy + 5 * s + 3, '4 cm', 'end', size=9) + lab(ox + 4 * s + 3, oy + 8.5 * s + 4, '3 cm', 'start', size=9)
    return svg(int(14 * s + 8), int(14 * s + 8), out, 1.3)


def tri_prism_345():
    s = 11; ox, oy = 26, 80
    body = prism([(0, 0), (4, 0), (0, 3)], 10, s, ox=ox, oy=oy)
    body += rightangle(ox, oy, 1, -1, 5)
    body += lab(ox + 2 * s, oy + 12, '4 cm') + lab(ox - 4, oy - 1.5 * s + 4, '3 cm', 'end', size=9.5)
    body += lab(ox + 1.3 * s, oy - 0.75 * s + 3, '5 cm', 'middle', size=8.5)
    body += lab(ox + 12, oy - 3 * s - 16, '10 cm', 'end', size=9.5)
    return svg(140, 94, body)

def open_box():
    b, _, _ = box3d(40, 30, 20, 2.1, ox=40, labels=('40 cm', '30 cm', '20 cm'), open_top=True)
    return svg(180, 84, b.replace('#F1E3B0', '#FFFFFF'))

def two_cubes():
    b1, x1, _ = box3d(3, 3, 3, 9, ox=26, oy=46, labels=('3 cm', '', ''))
    b2, _, _ = box3d(6, 6, 6, 9, ox=x1 + 20, oy=None, labels=('6 cm', '', ''))
    return svg(170, 94, b1 + b2)


def toblerone():
    s = 11; ox, oy = 30, 96
    body = prism([(0, 0), (6, 0), (3, 4)], 20, s, ox=ox, oy=oy, k=0.35)
    body += line(ox + 3 * s, oy, ox + 3 * s, oy - 4 * s, 1, '3 3') + rightangle(ox + 3 * s, oy, 1, -1, 5)
    body += lab(ox + 3 * s, oy + 12, '6 cm') + lab(ox + 3 * s + 3, oy - 1.2 * s, '4 cm', 'start', size=8.5) + lab(ox + 1.5 * s - 5, oy - 2 * s, '5 cm', 'end', size=9)
    body += lab(ox + 6 * s + 40, oy - 16, '20 cm', 'start', size=9.5)
    return svg(200, 110, body)

def box_cube_vol():
    b1, x1, _ = box3d(8, 5, 3, 8, ox=34, oy=40, labels=('8 cm', '5 cm', '3 cm'))
    b2, _, _ = box3d(6, 6, 6, 7.5, ox=x1 + 34, oy=None, labels=('6 cm', '', ''))
    return svg(220, 80, b1 + b2)

def tri_prism_vol():
    s = 10; ox, oy = 8, 76
    body = prism([(0, 0), (6, 0), (2, 4)], 10, s, ox=ox, oy=oy)
    body += line(ox + 2 * s, oy, ox + 2 * s, oy - 4 * s, 1, '3 3') + rightangle(ox + 2 * s, oy, 1, -1, 5)
    body += lab(ox + 3 * s, oy + 12, '6 cm') + lab(ox + 2 * s + 3, oy - 1.0 * s, '4 cm', 'start', size=9) + lab(ox + 6 * s + 24, oy - 10, '10 cm', 'start', size=9.5)
    return svg(150, 92, body)

def cyl(r_lab, h_lab, r=20, h=50):
    return svg(int(2 * r + 60), int(h + 2 * r * 0.32 * 2 + 12), cylinder(r + 8, r * 0.32 + 8, r, h, rlab=r_lab, hlab=h_lab))


EX = []

EX.append(dict(code='2A', title='Converting units of measurement', note='1 L = 1000 mL and 1 cm³ holds 1 mL.', cards=[
    dict(type='U', stars=1, text='<p>Convert:</p>' + parts('3.6 km to m', '450 mm to m', '2.5 L to mL', '7200 g to kg'), ans=['a', 'b', 'c', 'd'],
         worked='a <b>3600 m</b> &nbsp;b <b>0.45 m</b> &nbsp;c <b>2500 mL</b> &nbsp;d <b>7.2 kg</b>'),
    dict(type='U', stars=1, text='<p>Convert:</p>' + parts('3 m² to cm²', '45 000 mm² to cm²', '2 m³ to cm³'), ans=['a', 'b', 'c'],
         worked='a 3 × 100² = <b>30 000 cm²</b> &nbsp;b 45 000 ÷ 10² = <b>450 cm²</b> &nbsp;c 2 × 100³ = <b>2 000 000 cm³</b>'),
    dict(type='R', stars=2, draw=True, text='<p><b>Find the error.</b> Ben says, “5 m² = 500 cm², because there are 100 cm in a metre.”</p>' + parts(
        'Draw a 1 m by 1 m square and label its sides in cm. Use it to explain Ben’s mistake.', 'Find the correct answer.'), ans=['b'],
         worked='a A 1 m square is 100 cm × 100 cm = 10 000 cm², so for area you multiply by 100² not 100. &nbsp;b 5 × 10 000 = <b>50 000 cm²</b>'),
    dict(type='P', stars=2, fig=svg(170, 82, box3d(60, 30, 40, 1.15, ox=42, oy=None, labels=('60 cm', '30 cm', '40 cm'))[0]),
         text='<p>A fish tank is a rectangular prism.</p>' + parts('Find its volume in cm³.', 'Find its capacity in litres.',
                                                                 'How many 9 L buckets of water will fill it?'), ans=['a', 'b', 'c'],
         worked='a 60 × 30 × 40 = <b>72 000 cm³</b> &nbsp;b 72 000 mL = <b>72 L</b> &nbsp;c 72 ÷ 9 = <b>8 buckets</b>'),
    dict(type='P', stars=2, text='<p>A running track is 400 m around.</p>' + parts('How many laps make 5 km?',
                                                                                  'Jess runs 3.2 km every day for 2 weeks. How far is this in km and in m?'),
         ans=['a', 'b'],
         worked='a 5000 ÷ 400 = <b>12.5 laps</b> &nbsp;b 3.2 × 14 = <b>44.8 km = 44 800 m</b>'),
    dict(type='R', stars=3, text='<p>A rectangular paddock is 0.8 km long and 350 m wide. 1 hectare (ha) = 10 000 m².</p>' + parts(
        'Find its area in m².', 'Find its area in hectares.', 'Find its area in km².', 'Explain why you must change both lengths to the same unit first.'),
         ans=['a', 'b', 'c'],
         worked='a 800 × 350 = <b>280 000 m²</b> &nbsp;b ÷ 10 000 = <b>28 ha</b> &nbsp;c 0.8 × 0.35 = <b>0.28 km²</b> &nbsp;d 0.8 × 350 = 280 mixes km and m and gives a meaningless number.'),
]))

EX.append(dict(code='2B', title='Accuracy of measuring instruments', note='Limits of accuracy: ± 0.5 × the smallest unit of measurement.', cards=[
    dict(type='U', stars=1, text='<p>Give the lower and upper limits for each measurement.</p>' + parts(
        '8 cm, measured to the nearest cm', '3.6 kg, to the nearest 0.1 kg', '250 mL, to the nearest 10 mL'), ans=['a', 'b', 'c'],
         worked='a <b>7.5 cm – 8.5 cm</b> &nbsp;b <b>3.55 kg – 3.65 kg</b> &nbsp;c <b>245 mL – 255 mL</b>'),
    dict(type='U', stars=1, fig=ruler(), figpos='center', figafter=False, text=parts(
        'Read the length of the green bar, to the nearest millimetre.', 'What are the limits of accuracy of this reading?'), ans=['a', 'b'],
         worked='a <b>6.3 cm</b> (63 mm) &nbsp;b <b>6.25 cm – 6.35 cm</b>'),
    dict(type='R', stars=2, text='<p>A rope is 12 m long, measured to the nearest metre.</p>' + parts(
        'Explain why the rope cannot be 12.6 m long.', 'Could the rope be 11.5 m long? Explain.', 'Write the range of possible lengths.'), ans=['c'],
         worked='a 12.6 m rounds to 13 m, not 12 m. &nbsp;b Yes. 11.5 m is the lower limit; it rounds up to 12 m. &nbsp;c <b>11.5 m ≤ length &lt; 12.5 m</b>'),
    dict(type='P', stars=2, draw=True, text='<p>A rectangle is measured as 7 cm by 4 cm, both to the nearest cm.</p>' + parts(
        'Write the limits for each side.', 'Find the smallest possible perimeter.', 'Find the largest possible perimeter.'), ans=['b', 'c'],
         worked='a 6.5–7.5 cm and 3.5–4.5 cm &nbsp;b 2(6.5 + 3.5) = <b>20 cm</b> &nbsp;c 2(7.5 + 4.5) = <b>24 cm</b>'),
    dict(type='P', stars=2, review='2A', text='<p>A bag of flour is labelled 2.5 kg, to the nearest 0.1 kg.</p>' + parts(
        'Write its limits of accuracy in grams.', 'A recipe uses 300 g. Can you always make 8 batches from one bag? Explain.'), ans=['a'],
         worked='a <b>2450 g – 2550 g</b> &nbsp;b 8 × 300 = 2400 g, which is less than the smallest possible amount (2450 g), so <b>yes</b>.'),
    dict(type='R', stars=3, text='<p>A square tile has a side of 10 cm, measured to the nearest cm.</p>' + parts(
        'Find the smallest and largest possible area.', 'How far could the true area be from 100 cm²?',
        'The side could be out by 5%. Explain why the area could be out by about 10%.'), ans=['a', 'b'],
         worked='a 9.5² = <b>90.25 cm²</b>, 10.5² = <b>110.25 cm²</b> &nbsp;b up to <b>10.25 cm²</b> &nbsp;c Area = side × side, so the error happens twice (1.05 × 1.05 ≈ 1.10).'),
]))

EX.append(dict(code='2C', title='Very small and very large units', note='Scientific notation: <span class="math">a</span> × 10<sup><span class="math">m</span></sup>, where 1 ≤ <span class="math">a</span> &lt; 10.', cards=[
    dict(type='U', stars=1, text='<p>Write in scientific notation.</p>' + parts('45 000', '0.0072', '3 080 000'), ans=['a', 'b', 'c'],
         worked='a <b>4.5 × 10<sup>4</sup></b> &nbsp;b <b>7.2 × 10<sup>−3</sup></b> &nbsp;c <b>3.08 × 10<sup>6</sup></b>'),
    dict(type='U', stars=1, text=parts('Write 6.1 × 10<sup>5</sup> as a basic numeral.', 'Write 2.4 × 10<sup>−4</sup> as a basic numeral.',
                                       'Which is larger: 9.9 × 10<sup>3</sup> or 1.1 × 10<sup>4</sup>? Explain.'), ans=['a', 'b', 'c'],
         worked='a <b>610 000</b> &nbsp;b <b>0.000 24</b> &nbsp;c <b>1.1 × 10<sup>4</sup></b> = 11 000, which is more than 9900. Compare the powers of 10 first.'),
    dict(type='R', stars=2, text=parts('Round 0.004 862 to 2 significant figures.', 'Round 38 470 to 3 significant figures.',
                                       'How many significant figures are in 0.0305? Explain which zeros count.'), ans=['a', 'b', 'c'],
         worked='a <b>0.0049</b> &nbsp;b <b>38 500</b> &nbsp;c <b>3</b>. The leading zeros don’t count; the zero between 3 and 5 does.'),
    dict(type='P', stars=2, review='2A', text=parts('How many seconds are in 1 day? Write your answer in scientific notation.',
                                                    'How many seconds are in a year of 365 days? Give your answer in scientific notation to 3 significant figures.',
                                                    '1 millisecond (ms) = 0.001 s. How many ms are in one minute?'), ans=['a', 'b', 'c'],
         worked='a 24 × 60 × 60 = 86 400 = <b>8.64 × 10<sup>4</sup></b> &nbsp;b 31 536 000 ≈ <b>3.15 × 10<sup>7</sup></b> &nbsp;c 60 ÷ 0.001 = <b>60 000 ms</b>'),
    dict(type='U', stars=2, text='<p>1 KB = 1000 bytes, 1 MB = 1000 KB, 1 GB = 1000 MB.</p>' + parts(
        'A phone has 64 GB of storage. How many 4.5 MB photos fit?', 'Write 64 GB in bytes, in scientific notation.'), ans=['a', 'b'],
         worked='a 64 000 ÷ 4.5 = 14 222.2, so <b>14 222 photos</b> &nbsp;b 64 × 10<sup>9</sup> = <b>6.4 × 10<sup>10</sup> bytes</b>'),
    dict(type='R', stars=3, text='<p>A human hair is about 8 × 10<sup>−5</sup> m wide. A sheet of paper is about 1 × 10<sup>−4</sup> m thick.</p>' + parts(
        'Which is thicker? Explain.', 'How many hairs side by side would make 1 cm?',
        'The Sun is 1.5 × 10<sup>8</sup> km away. Light travels 3 × 10<sup>5</sup> km each second. How long does sunlight take to reach us?'),
         ans=['a', 'b', 'c'],
         worked='a <b>The paper</b>: 0.0001 m &gt; 0.000 08 m &nbsp;b 0.01 ÷ 0.000 08 = <b>125 hairs</b> &nbsp;c 1.5 × 10<sup>8</sup> ÷ (3 × 10<sup>5</sup>) = <b>500 s = 8 min 20 s</b>'),
]))

EX.append(dict(code='2D', title='Perimeter', note='Mark any missing lengths on the diagram before you add.', cards=[
    dict(type='U', stars=1, fig=lshape(), text='<p>Find the missing lengths marked ?, then find the perimeter of the shape.</p>', ans=['?', '?', 'P ='],
         worked='Missing: 10 − 6 = <b>4 m</b> and 8 − 3 = <b>5 m</b>. P = 10 + 8 + 6 + 3 + 4 + 5 = <b>36 m</b>'),
    dict(type='U', stars=1, draw=True, text='<p><b>Work backwards.</b> A rectangle has a perimeter of 46 cm and a length of 15 cm.</p>' + parts(
        'Find its width.', 'A square has the same perimeter. Find its side length.'), ans=['a', 'b'],
         worked='a 46 ÷ 2 = 23; 23 − 15 = <b>8 cm</b> &nbsp;b 46 ÷ 4 = <b>11.5 cm</b>'),
    dict(type='R', stars=2, fig=tri_x(), text=parts('Write an expression for the perimeter.', 'The perimeter is 31 cm. Find <span class="math">x</span>.',
                                                     'Find the length of each side.'), ans=['a', 'b', 'c'],
         worked='a <span class="math">x</span> + <span class="math">x</span> + 3 + 2<span class="math">x</span> = <b>4<span class="math">x</span> + 3</b> &nbsp;b 4<span class="math">x</span> = 28, <b><span class="math">x</span> = 7</b> &nbsp;c <b>7 cm, 10 cm, 14 cm</b>'),
    dict(type='P', stars=2, fig=fence(), text='<p>A yard is fenced on all four sides, leaving a 3 m gap for a gate. Fencing costs $45 per metre.</p>' + parts(
        'Find the length of fencing needed.', 'Find the cost.'), ans=['a', 'b'],
         worked='a 2(18 + 12) − 3 = <b>57 m</b> &nbsp;b 57 × 45 = <b>$2565</b>'),
    dict(type='P', stars=2, review='2A', draw=True, text='<p>A rectangular garden is 3.6 m by 240 cm. Edging is sold in 1.2 m lengths at $8.50 each.</p>' + parts(
        'Find the perimeter in metres.', 'How many lengths of edging are needed?', 'Find the cost.'), ans=['a', 'b', 'c'],
         worked='a 240 cm = 2.4 m; 2(3.6 + 2.4) = <b>12 m</b> &nbsp;b 12 ÷ 1.2 = <b>10</b> &nbsp;c 10 × 8.50 = <b>$85</b>'),
    dict(type='R', stars=3, fig=stairs(), text='<p>Each step is 1 m wide and 1 m high.</p>' + parts(
        'Find the perimeter of the shape.', 'Explain a quick way to get the answer without adding every side.',
        'Would the perimeter change with 8 steps each 0.5 m? Explain.'), ans=['a'],
         worked='a 4 + 4 + 8 × 1 = <b>16 m</b> &nbsp;b The vertical steps add to 4 m and the horizontal steps add to 4 m, so P is the same as a 4 m × 4 m square. &nbsp;c <b>No</b>, still 16 m: the steps still add to 4 m each way.'),
]))

EX.append(dict(code='2E', title='Circumference', note='Use <span class="math">C</span> = π<span class="math">d</span> or <span class="math">C</span> = 2π<span class="math">r</span>. ' + PI, cards=[
    dict(type='U', stars=1, draw=True, text='<p>Find the circumference of a circle with:</p>' + parts('diameter 12 cm', 'radius 4.5 m'), ans=['a', 'b'],
         worked='a π × 12 = <b>37.70 cm</b> &nbsp;b 2 × π × 4.5 = <b>28.27 m</b>'),
    dict(type='U', stars=1, draw=True, text='<p><b>Work backwards.</b> A circle has a circumference of 50 cm.</p>' + parts('Find its diameter.', 'Find its radius.'),
         ans=['a', 'b'], worked='a 50 ÷ π = <b>15.92 cm</b> &nbsp;b 15.92 ÷ 2 = <b>7.96 cm</b>'),
    dict(type='R', stars=2, text='<p>A bike wheel has a diameter of 66 cm.</p>' + parts('Find its circumference.',
                                                                                         'How many full turns does the wheel make in 1 km?',
                                                                                         'Explain why you must change 1 km to cm first.'), ans=['a', 'b'],
         worked='a π × 66 = <b>207.35 cm</b> &nbsp;b 100 000 ÷ 207.35 = 482.3, so <b>482 full turns</b> &nbsp;c The circumference is in cm, so both distances must be in the same unit.'),
    dict(type='U', stars=2, fig=semi_quarter(), figpos='center', figafter=False,
         text='<p>Find the perimeter of each shape. Include the straight edges.</p>', ans=['semicircle', 'quarter circle'],
         worked='Semicircle: π × 10 ÷ 2 + 10 = <b>25.71 cm</b>. Quarter circle: 2 × π × 6 ÷ 4 + 6 + 6 = <b>21.42 cm</b>'),
    dict(type='P', stars=2, review='2B', text='<p>A coin has a diameter of 2.5 cm, measured to the nearest mm.</p>' + parts(
        'Write the limits of accuracy for the diameter.', 'Find the smallest and largest possible circumference.'), ans=['a', 'b'],
         worked='a <b>2.45 cm – 2.55 cm</b> &nbsp;b π × 2.45 = <b>7.70 cm</b>; π × 2.55 = <b>8.01 cm</b>'),
    dict(type='P', stars=3, fig=track(), figpos='center', figafter=False, text='<p>A track has two 85 m straights and two semicircular ends.</p>' + parts(
        'Find the length of one lap.', 'How many laps must Ivy run to cover at least 3 km?'), ans=['a', 'b'],
         worked='a 2 × 85 + π × 64 = 170 + 201.06 = <b>371.06 m</b> &nbsp;b 3000 ÷ 371.06 = 8.08, so <b>9 laps</b>'),
]))

EX.append(dict(code='2F', title='Area', note='Write the formula first, then substitute.', cards=[
    dict(type='U', stars=1, fig=tri_para(), figpos='center', figafter=False, text='<p>Find the area of the triangle and the parallelogram.</p>',
         ans=['triangle', 'parallelogram'], worked='Triangle: ½ × 9 × 6 = <b>27 cm²</b>. Parallelogram: 8 × 5 = <b>40 cm²</b>'),
    dict(type='U', stars=1, fig=trap_rhombus(), figpos='center', figafter=False, text='<p>Find the area of the trapezium and the rhombus.</p>',
         ans=['trapezium', 'rhombus'], worked='Trapezium: ½ × 5 × (6 + 10) = <b>40 cm²</b>. Rhombus: ½ × 8 × 6 = <b>24 cm²</b>'),
    dict(type='R', stars=2, draw=True, text='<p><b>Work backwards.</b></p>' + parts('A triangle has an area of 36 cm² and a base of 9 cm. Find its height.',
                                                                                    'A rectangle has an area of 84 m² and a length of 12 m. Find its width.'),
         ans=['a', 'b'], worked='a ½ × 9 × <span class="math">h</span> = 36, so <span class="math">h</span> = 72 ÷ 9 = <b>8 cm</b> &nbsp;b 84 ÷ 12 = <b>7 m</b>'),
    dict(type='P', stars=2, review='2D', fig=backyard(), text='<p>A backyard has a pool. The rest is covered in turf costing $12.50 per m².</p>' + parts(
        'Find the area of turf.', 'Find the cost of the turf.', 'Find the perimeter of the pool.'), ans=['a', 'b', 'c'],
         worked='a 15 × 9 − 6 × 3 = 135 − 18 = <b>117 m²</b> &nbsp;b 117 × 12.50 = <b>$1462.50</b> &nbsp;c 2(6 + 3) = <b>18 m</b>'),
    dict(type='R', stars=2, draw=True, text='<p><b>Find the error.</b> Ella says the area of a triangle with base 10 cm and height 7 cm is 70 cm².</p>' + parts(
        'Draw the triangle inside a 10 cm by 7 cm rectangle and use it to explain her mistake.', 'Find the correct area.'), ans=['b'],
         worked='a The triangle is half of the rectangle, so you must multiply by ½. &nbsp;b ½ × 10 × 7 = <b>35 cm²</b>'),
    dict(type='P', stars=3, fig=wall(), text='<p>The end wall of a shed is a rectangle with a triangle on top. It needs two coats of paint. 1 L covers 12 m².</p>' + parts(
        'Find the area of the wall.', 'Paint is sold in 1 L tins. How many tins are needed?'), ans=['a', 'b'],
         worked='a 6 × 2.4 + ½ × 6 × 1.5 = 14.4 + 4.5 = <b>18.9 m²</b> &nbsp;b 2 × 18.9 = 37.8 m²; 37.8 ÷ 12 = 3.15 L, so <b>4 tins</b>'),
]))

EX.append(dict(code='2G', title='Area of circles and sectors', note='Sector area = <sup>θ</sup>⁄<sub>360</sub> × π<span class="math">r</span><sup>2</sup>. ' + PI, cards=[
    dict(type='U', stars=1, fig=two_circles(), figpos='center', figafter=False, text='<p>Find the area of each circle.</p>', ans=['left', 'right'],
         worked='Left: π × 5² = <b>78.54 cm²</b>. Right: r = 4.5, π × 4.5² = <b>63.62 m²</b>'),
    dict(type='U', stars=1, fig=semi_quarter_area(), figpos='center', figafter=False, text='<p>Find the area of the semicircle and the quarter circle.</p>',
         ans=['semicircle', 'quarter'], worked='Semicircle: ½ × π × 4² = <b>25.13 cm²</b>. Quarter circle: ¼ × π × 10² = <b>78.54 cm²</b>'),
    dict(type='R', stars=2, fig=two_sectors(), figpos='center', figafter=False, text=parts('Find the area of each sector.',
                                                                                        'Explain how a smaller radius can give the same area.'),
         ans=['A', 'B'],
         worked='a A: 60/360 × π × 6² = <b>18.85 cm²</b>; B: 135/360 × π × 4² = <b>18.85 cm²</b> (both 6π) &nbsp;b B has a smaller radius but a bigger angle, so it is a bigger fraction of its circle.'),
    dict(type='P', stars=2, fig=pizza(), text='<p>A pizza is cut into 8 equal slices.</p>' + parts('Find the angle of each slice.',
                                                                                                   'Find the area of one slice.',
                                                                                                   'Find the area of 3 slices.'), ans=['a', 'b', 'c'],
         worked='a 360 ÷ 8 = <b>45°</b> &nbsp;b π × 15² ÷ 8 = <b>88.36 cm²</b> &nbsp;c 3 × 88.357 = <b>265.07 cm²</b>'),
    dict(type='R', stars=2, review='2E', draw=True, text='<p><b>Work backwards.</b> A circle has a circumference of 37.70 cm.</p>' + parts(
        'Find its radius.', 'Find its area.'), ans=['a', 'b'],
         worked='a 37.70 ÷ (2π) = <b>6 cm</b> &nbsp;b π × 6² = <b>113.10 cm²</b>'),
    dict(type='P', stars=3, fig=ring(), text='<p>A metal washer is a ring shape.</p>' + parts('Find the area of the outer circle.',
                                                                                             'Find the area of the hole.', 'Find the area of the shaded ring.',
                                                                                             'Tom says the ring area is π × 3². Explain why he is wrong.'),
         ans=['a', 'b', 'c'],
         worked='a π × 8² = <b>201.06 cm²</b> &nbsp;b π × 5² = <b>78.54 cm²</b> &nbsp;c <b>122.52 cm²</b> &nbsp;d You subtract the areas (64π − 25π = 39π), not the radii first. π × 3² = 28.27 cm² is far too small.'),
]))

EX.append(dict(code='2H', title='Composite shapes', note='Split into shapes you know. ' + PI, cards=[
    dict(type='U', stars=1, fig=rect_semi(), text='<p>A rectangle has a semicircle on one end.</p>' + parts('Find its area.', 'Find its perimeter.'), ans=['a', 'b'],
         worked='a 8 × 5 + ½ × π × 2.5² = 40 + 9.82 = <b>49.82 cm²</b> &nbsp;b 8 + 8 + 5 + ½ × π × 5 = 21 + 7.85 = <b>28.85 cm</b>'),
    dict(type='R', stars=1, fig=lshape2(), text=parts('Find the area by <b>adding</b> two rectangles.', 'Find the area by <b>subtracting</b> a rectangle.',
                                                       'Which method do you prefer? Why?'), ans=['a', 'b'],
         worked='a 12 × 5 + 7 × 4 = 60 + 28 = <b>88 cm²</b> &nbsp;b 12 × 9 − 5 × 4 = 108 − 20 = <b>88 cm²</b> &nbsp;c Either, with a reason.'),
    dict(type='U', stars=2, fig=house(), text='<p>Find the area of the front of this cubby house.</p>', ans=['A ='],
         worked='6 × 4 + ½ × 6 × 3 = 24 + 9 = <b>33 m²</b>'),
    dict(type='P', stars=2, fig=square_circle(), text='<p>A circle fits exactly inside a square. The corners are shaded.</p>' + parts(
        'Find the shaded area.', 'What percentage of the square is shaded?'), ans=['a', 'b'],
         worked='a 10² − π × 5² = 100 − 78.54 = <b>21.46 cm²</b> &nbsp;b 21.46 ÷ 100 = <b>21.5%</b>'),
    dict(type='P', stars=2, review='2E', fig=field(), figpos='center', figafter=False, text='<p>A sports field is a rectangle with a semicircle on each end.</p>' + parts(
        'Find its area.', 'Find its perimeter.'), ans=['a', 'b'],
         worked='a 100 × 60 + π × 30² = 6000 + 2827.43 = <b>8827.43 m²</b> &nbsp;b 2 × 100 + π × 60 = <b>388.50 m</b>'),
    dict(type='P', stars=3, fig=window(), text='<p>A window is a rectangle with a semicircle on top.</p>' + parts(
        'Find the area of glass.', 'Find the length of the outside frame (not the dashed line).', 'The frame costs $35 per metre. Find its cost.'),
         ans=['a', 'b', 'c'],
         worked='a 1.2 × 1.5 + ½ × π × 0.6² = 1.8 + 0.57 = <b>2.37 m²</b> &nbsp;b 1.5 + 1.5 + 1.2 + ½ × π × 1.2 = <b>6.08 m</b> &nbsp;c 6.085 × 35 = <b>$212.97</b> (or $212.80 using 6.08 m)'),
]))

EX.append(dict(code='2I', title='Surface area of prisms', note='Surface area = total area of all faces. Sketch the net.', cards=[
    dict(type='U', stars=1, fig=cube_box(), figpos='center', figafter=False, text='<p>Find the surface area of the cube and the rectangular prism.</p>',
         ans=['cube', 'prism'], worked='Cube: 6 × 4² = <b>96 cm²</b>. Prism: 2(5 × 3 + 5 × 2 + 3 × 2) = 2 × 31 = <b>62 cm²</b>'),
    dict(type='U', stars=1, fig=net(), text='<p>This is the net of a rectangular prism.</p>' + parts('What are the length, width and height of the prism?',
                                                                                                    'Find its surface area.'), ans=['a', 'b'],
         worked='a <b>6 cm × 4 cm × 3 cm</b> &nbsp;b 2(24 + 18 + 12) = <b>108 cm²</b>'),
    dict(type='R', stars=2, review='2F', fig=tri_prism_345(), text='<p>This prism has right-angled triangles at each end.</p>' + parts(
        'Find the area of one triangle.', 'Find the surface area of the prism.'), ans=['a', 'b'],
         worked='a ½ × 4 × 3 = <b>6 cm²</b> &nbsp;b 2 × 6 + 10 × (3 + 4 + 5) = 12 + 120 = <b>132 cm²</b>'),
    dict(type='P', stars=2, fig=open_box(), text='<p>A storage box has <b>no lid</b>.</p>' + parts('Find the area of cardboard needed in cm².',
                                                                                                  'Change your answer to m².'), ans=['a', 'b'],
         worked='a 40 × 30 + 2 × 40 × 20 + 2 × 30 × 20 = 1200 + 1600 + 1200 = <b>4000 cm²</b> &nbsp;b ÷ 10 000 = <b>0.4 m²</b>'),
    dict(type='R', stars=2, fig=two_cubes(), figpos='center', figafter=False, text=parts('Find the surface area of each cube.',
                                                                                      'The side doubled. What happened to the surface area? Explain why.'),
         ans=['a', 'b'],
         worked='a 6 × 3² = <b>54 cm²</b>; 6 × 6² = <b>216 cm²</b> &nbsp;b It is <b>4 times</b> bigger: each face is 2 × 2 = 4 times the area.'),
    dict(type='P', stars=3, fig=toblerone(), text='<p>A chocolate box is a triangular prism. Each end is an isosceles triangle.</p>' + parts(
        'Use Pythagoras’ theorem to check the sloping sides are 5 cm.', 'Find the surface area of the box.'), ans=['a', 'b'],
         worked='a Half the base is 3 cm: √(3² + 4²) = √25 = <b>5 cm</b> ✓ &nbsp;b 2 × ½ × 6 × 4 + 20 × (5 + 5 + 6) = 24 + 320 = <b>344 cm²</b>'),
]))

EX.append(dict(code='2J', title='Volume of prisms and cylinders', note='<span class="math">V = Ah</span> and 1 cm³ = 1 mL. ' + PI, cards=[
    dict(type='U', stars=1, fig=box_cube_vol(), figpos='center', figafter=False, text='<p>Find the volume of the rectangular prism and the cube.</p>',
         ans=['prism', 'cube'], worked='Prism: 8 × 5 × 3 = <b>120 cm³</b>. Cube: 6³ = <b>216 cm³</b>'),
    dict(type='U', stars=1, fig=tri_prism_vol(), text='<p>Find the volume of this triangular prism.</p>', ans=['V ='],
         worked='A = ½ × 6 × 4 = 12 cm²; V = 12 × 10 = <b>120 cm³</b>'),
    dict(type='U', stars=2, fig=cyl('5 cm', '12 cm', 18, 46), text='<p>A tin is a cylinder.</p>' + parts('Find its volume.',
                                                                                                      'How many litres does it hold?'), ans=['a', 'b'],
         worked='a π × 5² × 12 = <b>942.48 cm³</b> &nbsp;b 942.48 mL = <b>0.94 L</b>'),
    dict(type='R', stars=2, draw=True, text='<p><b>Work backwards.</b></p>' + parts('A rectangular prism has a volume of 360 cm³ and a base 9 cm by 8 cm. Find its height.',
                                                                                     'A cylinder with radius 5 cm holds exactly 1 L. Find its height.'),
         ans=['a', 'b'],
         worked='a 360 ÷ (9 × 8) = <b>5 cm</b> &nbsp;b 1 L = 1000 cm³; 1000 ÷ (π × 5²) = <b>12.73 cm</b>'),
    dict(type='P', stars=2, fig=cyl('1.5 m', '2 m', 22, 34), text='<p>A rainwater tank is a cylinder with diameter 3 m and height 2 m.</p>' + parts(
        'Find its volume in m³.', 'How many litres does it hold? (1 m³ = 1000 L)', 'A family uses 450 L a day. How many full days will a full tank last?'),
         ans=['a', 'b', 'c'],
         worked='a π × 1.5² × 2 = <b>14.14 m³</b> &nbsp;b <b>14 137 L</b> &nbsp;c 14 137 ÷ 450 = 31.4, so <b>31 days</b>'),
    dict(type='P', stars=3, review='2A', draw=True, text='<p>A concrete path is 12 m long, 1.2 m wide and 10 cm deep. Concrete costs $230 per m³.</p>' + parts(
        'Find the volume of concrete in m³.', 'Find the cost.', 'Concrete is only sold in multiples of 0.2 m³. How much must be ordered, and what will it cost?'),
         ans=['a', 'b', 'c'],
         worked='a 12 × 1.2 × 0.1 = <b>1.44 m³</b> &nbsp;b 1.44 × 230 = <b>$331.20</b> &nbsp;c <b>1.6 m³</b>, costing 1.6 × 230 = <b>$368</b>'),
]))

CHAPTER = dict(
    n=2, topic='Measurement', exercises=EX,
    answer_pages=[['2A', '2B', '2C', '2D', '2E'], ['2F', '2G', '2H', '2I', '2J']],
    artwork_short='the “elephants” of Elephant Valley, part of the Mandelbrot set, coloured gold.',
    artwork_long='The pictures in this booklet are parts of the Mandelbrot set, drawn by a computer that repeats one simple rule, '
                 'z → z² + c, hundreds of times for every point. This one is Elephant Valley, where curling shapes like elephant trunks '
                 'line up along the edge of the set. Zoom in on any part of the edge and you find more detail, forever. Maths can make beautiful things.',
)
