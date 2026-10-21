import numpy as np, sys
from PIL import Image

def escape(cx, cy, width, W, H, maxit=600):
    h = width * H / W
    x = np.linspace(cx - width/2, cx + width/2, W)
    y = np.linspace(cy + h/2, cy - h/2, H)
    C = x[None, :] + 1j * y[:, None]
    Z = np.zeros_like(C)
    N = np.full(C.shape, maxit, dtype=float)
    alive = np.ones(C.shape, bool)
    for i in range(maxit):
        Z[alive] = Z[alive]**2 + C[alive]
        esc = alive & (np.abs(Z) > 4)
        if esc.any():
            az = np.abs(Z[esc])
            N[esc] = i + 1 - np.log(np.log(az)) / np.log(2)
            alive &= ~esc
        if not alive.any():
            break
    return N, alive

def hexc(h):
    h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)

def render(cx, cy, width, W, H, base_a, base_b, fil, inside, maxit=600, gain=1.0, gamma=0.55):
    N, inset = escape(cx, cy, width, W, H, maxit)
    lo = np.percentile(N[~inset], 5); hi = np.percentile(N[~inset], 99.7)
    t = np.clip((N - lo) / (hi - lo), 0, 1) ** gamma * gain
    t = np.clip(t, 0, 1)
    # diagonal base gradient
    yy, xx = np.mgrid[0:H, 0:W]
    g = ((xx / W) * 0.6 + (yy / H) * 0.4)[..., None]
    base = hexc(base_a) * (1 - g) + hexc(base_b) * g
    img = base * (1 - t[..., None]) + hexc(fil) * t[..., None]
    img[inset] = hexc(inside)
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))

if __name__ == '__main__':
    cx, cy, w = map(float, sys.argv[1:4]); W, H = int(sys.argv[4]), int(sys.argv[5]); out = sys.argv[6]
    mode = sys.argv[7] if len(sys.argv) > 7 else 'cover'
    if mode == 'cover':
        im = render(cx, cy, w, W, H, '#B48A16', '#D6B44A', '#FFF6D6', '#7E6214', gamma=0.42)
    else:  # header strip: pale gold, soft filaments
        im = render(cx, cy, w, W, H, '#E6CF86', '#D9BD62', '#FFFBEA', '#DCC370', gamma=0.42)
    im.save(out, quality=88)
