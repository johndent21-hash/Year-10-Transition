"""Year 10 Extension (Fast Finishers) booklet generator.

Layout copied from the Year 9 Standard Chapter 10 extension booklet.
Each chapter file (ch1.py, ch2.py, ch4.py) supplies a CHAPTER dict;
build() turns it into one self-contained HTML page set printed to A4.
"""
import html, math

TYPES = {'U': ('Understanding', 'u'), 'R': ('Reasoning', 'r'), 'P': ('Problem solving', 'p')}

CSS = r"""
@font-face{font-family:Lexend;font-weight:400;src:url(assets/lexend-latin-400-normal.woff2)}
@font-face{font-family:Lexend;font-weight:500;src:url(assets/lexend-latin-500-normal.woff2)}
@font-face{font-family:Lexend;font-weight:600;src:url(assets/lexend-latin-600-normal.woff2)}
@font-face{font-family:Lexend;font-weight:700;src:url(assets/lexend-latin-700-normal.woff2)}
@font-face{font-family:Lexend;font-weight:800;src:url(assets/lexend-latin-800-normal.woff2)}
:root{
  --gold:#C9A227; --gold-light:#F3E3A6; --gold-pale:#FBF5E1; --gold-deep:#8A6B12; --gold-ink:#2E2308;
  --green:#1E5B3F; --green-mid:#2F7A55; --green-pale:#DCEFE3;
  --ink:#1E2A24; --muted:#5E6670; --line:#C9CDD3; --panel:#F4F5F2;
  --u:#5B6475; --u-bg:#E5E8EE; --r:#8A6B12; --r-bg:#F5EAC6; --p:#1E6B4A; --p-bg:#DCEFE4;
  --fig:#FBF1D0; --acc:#1E6B4A;
}
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:Lexend,'Liberation Sans',sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;background:#fff}
.page:last-child{page-break-after:auto;break-after:auto}
sup{font-size:.7em;line-height:0}
.math{font-family:'Liberation Serif',serif;font-style:italic;font-size:1.08em}

/* ---------- cover ---------- */
.cover{background:#C9A227 center/cover no-repeat}
.cover .logo{position:absolute;left:34px;top:30px;width:102px;height:66px;background:#fff;border-radius:9px;padding:7px 9px;box-shadow:0 2px 8px rgba(60,40,0,.25)}
.cover .logo img{width:100%;height:100%;object-fit:contain}
.cover .stage{position:absolute;right:42px;top:44px;padding:9px 18px;border-radius:9px;border:2px solid var(--green);
  background:linear-gradient(100deg,#FFF8DE 0%,#F3E3A6 45%,#FFF9E6 60%,#E9D284 100%);
  font-weight:700;font-size:13px;letter-spacing:.25em;color:var(--gold-ink)}
.cover .band{position:absolute;left:32px;right:32px;top:122px;height:96px;border-radius:16px;border:3px solid var(--gold-deep);
  outline:2px solid #fff;outline-offset:-7px;
  background:linear-gradient(100deg,#E2C35C 0%,#F6E7AE 30%,#FFF6D6 46%,#EED68A 62%,#D3AE3A 100%);
  box-shadow:0 4px 14px rgba(70,45,0,.35)}
.cover .bolt{position:absolute;left:24px;top:12px;width:68px;height:68px;border-radius:50%;background:var(--gold-deep);
  border:4px solid #FFF3C9;box-shadow:0 0 0 2px var(--green);display:flex;align-items:center;justify-content:center}
.cover .band h1{position:absolute;left:112px;top:16px;margin:0;font-size:37px;font-weight:800;letter-spacing:.06em;color:var(--gold-ink)}
.cover .band .sub{position:absolute;left:114px;top:62px;font-size:12.5px;font-weight:700;letter-spacing:.22em;color:var(--green)}
.cover .stack{position:absolute;left:48px;right:48px;top:278px;display:flex;flex-direction:column;gap:22px}
.cover .main{position:relative;border-radius:14px;padding-bottom:16px;
  background:rgba(251,245,225,.95);border-top:7px solid var(--gold-deep);box-shadow:0 0 0 1.5px var(--green) inset,0 4px 14px rgba(70,45,0,.3);padding:30px 34px 16px}
.cover .chapno{position:absolute;right:30px;top:-64px;width:124px;height:124px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#FFF6D6 0%,#F0D98E 40%,#C9A227 100%);
  border:6px solid var(--gold-deep);box-shadow:0 0 0 3px #FFF3C9,0 0 0 5px var(--green),0 4px 12px rgba(60,40,0,.35);
  text-align:center;padding-top:24px}
.cover .chapno small{display:block;font-size:9.5px;font-weight:700;letter-spacing:.25em;color:var(--green)}
.cover .chapno b{display:block;font-size:46px;font-weight:800;line-height:1.05;color:var(--gold-ink)}
.cover .kick{font-size:10.5px;font-weight:700;letter-spacing:.14em;color:var(--green);margin:0 140px 6px 0;line-height:1.6;white-space:nowrap}
.cover h2{margin:0 150px 8px 0;font-size:40px;line-height:1.08;font-weight:800;color:var(--gold-ink)}
.cover .intro{font-size:12.5px;color:#3D3A2E;line-height:1.45;margin:0 0 14px;max-width:470px}
.cover table{width:100%;border-collapse:separate;border-spacing:0 5px;font-size:12.5px}
.cover th{font-size:8.5px;letter-spacing:.2em;color:var(--muted);text-align:left;font-weight:700;padding:0 10px}
.cover td{background:#fff;padding:5px 10px;border-top:1px solid #EADFB8;border-bottom:1px solid #EADFB8}
.cover td:first-child{border-left:5px solid var(--gold-deep);border-radius:4px 0 0 4px;font-weight:700;width:62px;color:var(--gold-ink)}
.cover td:last-child{border-right:1px solid #EADFB8;border-radius:0 4px 4px 0;width:50px;text-align:center}
.cover td.pg{width:44px;text-align:center}
.cover .box{display:inline-block;width:13px;height:13px;border:1.5px solid var(--muted);border-radius:3px;vertical-align:middle}
.cover .legend{display:flex;gap:10px}
.cover .legend > div{flex:1;background:rgba(251,245,225,.95);border-radius:9px;padding:9px 11px;border-top:3px solid var(--gold-deep);font-size:9.5px;color:#3D3A2E;line-height:1.4}
.cover .legend h4{margin:0 0 5px;font-size:8.5px;letter-spacing:.16em;color:var(--gold-ink)}
.cover .namebar{height:56px;border-radius:10px;background:#fff;border-top:6px solid var(--gold-deep);
  box-shadow:0 0 0 1.5px var(--green) inset;display:flex;align-items:center;gap:14px;padding:0 22px;font-size:9px;font-weight:700;letter-spacing:.2em;color:var(--gold-ink)}
.cover .namebar span.l{flex:1;border-bottom:1.2px solid #555;height:14px}
.cover .art{position:absolute;right:48px;top:1052px;max-width:560px;background:rgba(251,245,225,.93);border-radius:6px;padding:5px 10px;font-size:9px;color:#3D3A2E}

/* shared chips */
.tag{display:inline-block;font-size:9.5px;font-weight:600;padding:2px 7px;border-radius:4px;line-height:1.35;white-space:nowrap}
.tag.u{background:var(--u-bg);color:var(--u)} .tag.r{background:var(--r-bg);color:var(--r)} .tag.p{background:var(--p-bg);color:var(--p)}
.tag.bar{border-left:3px solid}
.tag.rev{background:#ECEDEF;color:#2C2F36;border:1px solid #9AA0A8;font-weight:700}
.tag.draw{background:#fff;color:var(--ink);border:1.3px dashed var(--ink)}
.stars{font-size:13px;letter-spacing:1px;color:var(--gold-ink)}

/* ---------- exercise pages ---------- */
.hdr{position:absolute;left:0;right:0;top:0;height:58px;background:#fff center right/auto 100% no-repeat;border-bottom:4px solid var(--green)}
.hdr:before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#fff 0%,#fff 22%,rgba(255,255,255,.75) 45%,rgba(255,255,255,0) 75%)}
.hdr > *{position:absolute;z-index:1}
.hdr .logo{left:26px;top:9px;width:58px;height:36px;background:#fff;border-radius:4px;padding:2px}
.hdr .logo img{width:100%;height:100%;object-fit:contain}
.hdr .badge{left:96px;top:6px;width:82px;height:47px;border-radius:8px;background:var(--green);border:2.5px solid var(--gold);box-shadow:0 0 0 1.5px var(--green);
  color:#fff;text-align:center;padding-top:5px}
.hdr .badge small{display:block;font-size:7.5px;letter-spacing:.24em;font-weight:600;color:var(--gold-light)}
.hdr .badge b{display:block;font-size:19px;font-weight:700;line-height:1.15}
.hdr .kick{left:194px;top:8px;font-size:8.5px;font-weight:600;letter-spacing:.26em;color:var(--muted)}
.hdr h1{left:194px;top:21px;margin:0;font-size:19.5px;font-weight:700;color:var(--ink);white-space:nowrap}
.hdr .ff{right:26px;top:14px;padding:6px 13px;border:2px solid var(--green);border-radius:7px;background:linear-gradient(100deg,#FFF9E6,#F3E3A6 60%,#FFF6D6);
  font-size:9.5px;font-weight:700;letter-spacing:.2em;color:var(--gold-ink)}
.ext{position:absolute;left:28px;right:28px;top:72px;height:40px;border-radius:8px;background:var(--panel);border:1px solid #DADDD8;display:flex;align-items:center;padding:0 11px;gap:12px}
.ext .pill{background:var(--green);color:#fff;font-size:9px;font-weight:700;letter-spacing:.24em;padding:4px 9px;border-radius:4px}
.ext .msg{flex:1;font-size:10.3px;line-height:1.35}
.ext .types{display:flex;gap:5px}
.ref{position:absolute;left:28px;right:28px;top:118px;border-radius:8px;border:1px solid #E3D59F;background:var(--gold-pale);padding:6px 10px;font-size:9.8px}
.ref table{border-collapse:collapse;width:100%}
.ref td,.ref th{padding:1.5px 6px;border-bottom:1px solid #EADFB8;text-align:left}
.ref th{font-size:8.5px;letter-spacing:.12em;color:var(--gold-deep)}
.grid{position:absolute;left:28px;right:28px;top:122px;bottom:36px;display:grid;grid-template-columns:1fr 1fr;grid-auto-rows:1fr;gap:10px 12px}
.card{position:relative;border:1.3px solid #B9BEC6;border-left:5px solid var(--u);border-radius:9px;padding:9px 11px 8px 11px;display:flex;flex-direction:column;overflow:hidden;background:#fff}
.card.r{border-left-color:var(--r)} .card.p{border-left-color:var(--p)}
.card.span2{grid-column:span 2}
.card .top{display:flex;align-items:center;gap:6px;margin-bottom:6px}
.card .num{flex:0 0 22px;width:22px;height:22px;border-radius:50%;border:1.6px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700}
.card .top .stars{margin-left:auto}
.card .body{font-size:11.2px;line-height:1.42;display:flow-root}
.card .body p{margin:0 0 3px}
.card .fig{float:right;margin:0 0 4px 8px}
.card .fig.center{float:none;display:flex;justify-content:center;margin:2px 0 4px}
.card ol.parts{list-style:none;margin:1px 0 0;padding:0}
.card ol.parts li{position:relative;padding-left:15px;margin-bottom:1px}
.card ol.parts li b.pl{position:absolute;left:0;color:var(--green-mid);font-weight:700}
.card .space{flex:1;min-height:12px}
.card .space.dots{margin:4px 0 2px;background-image:radial-gradient(circle,#B4B9C0 0.9px,transparent 1.1px);background-size:14px 14px;background-position:3px 3px}
.card .answers{display:flex;gap:14px;font-size:10.5px;font-weight:600;align-items:flex-end}
.card .answers > span{flex:1;display:flex;align-items:flex-end;gap:5px}
.card .answers > span i{flex:1;border-bottom:1.2px solid #444;height:12px;font-style:normal}
.card .answers.stack{flex-direction:column;align-items:stretch;gap:8px}
table.t{border-collapse:collapse;font-size:10.4px;margin:3px 0}
table.t td,table.t th{border:1px solid #9097A0;padding:2px 6px;text-align:center;min-width:26px;height:18px}
table.t th{background:#F1E6BD;font-weight:600}
table.t td.l,table.t th.l{text-align:left}
table.t.ss th{background:#E8EAED;font-weight:500;color:#555;font-size:9.5px}
table.t.ss td{font-family:'Liberation Mono',monospace;font-size:10px;text-align:left}
table.sl{border-collapse:collapse;font-size:11px;margin:2px 0;font-family:'Liberation Mono',monospace}
table.sl td{padding:0 6px;text-align:left}
table.sl td.s{border-right:1.4px solid #333;text-align:right;font-weight:700}
table.sl tr.h td{font-family:Lexend,sans-serif;font-size:9px;font-weight:700;color:var(--muted)}
.key{font-size:9px;color:var(--muted)}
.ftr{position:absolute;left:28px;right:28px;bottom:10px;height:20px;font-size:9px;color:var(--muted);display:flex;align-items:center;justify-content:space-between}
.ftr .pn{position:absolute;left:50%;transform:translateX(-50%);width:24px;height:24px;border-radius:50%;border:2px solid var(--green);color:var(--ink);font-weight:700;font-size:10.5px;display:flex;align-items:center;justify-content:center;background:#fff;top:-3px}

/* ---------- answers ---------- */
.anscols{position:absolute;left:28px;right:28px;top:122px;bottom:36px;column-count:2;column-gap:20px;column-fill:balance;font-size:9.8px;line-height:1.38}
.ansex{break-inside:avoid-column;margin:0 0 9px}
.ansex h3{margin:0 0 4px;font-size:11px;font-weight:700;color:var(--ink);background:var(--gold-pale);border-left:4px solid var(--gold-deep);padding:3px 7px;border-radius:3px}
.ansex h3 b{color:var(--green)}
.ansq{display:flex;gap:6px;margin:0 0 3px;break-inside:avoid}
.ansq .n{flex:0 0 16px;height:16px;border-radius:50%;border:1.3px solid var(--ink);font-size:8.5px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:1px}
.ansq .w{flex:1}
.ansq .w b{color:var(--green)}
.ansq .w i.al{font-style:normal;font-weight:700;color:var(--gold-deep);margin-right:1px}
.about{break-inside:avoid-column;margin-top:10px;padding:8px 10px;border-radius:8px;background:var(--panel);border:1px solid #DADDD8;font-size:9.5px;line-height:1.4}
.about h4{margin:0 0 3px;font-size:8.5px;letter-spacing:.18em;color:var(--green)}
.about p{margin:0 0 6px}
"""

BOLT = ('<svg width="34" height="34" viewBox="0 0 24 24"><path d="M13.5 2 5 13.5h6L9.5 22 19 9.8h-6.2z" '
        'fill="#FFF3C9" stroke="#FFF3C9" stroke-width="1" stroke-linejoin="round"/></svg>')


def stars(n):
    return '<span class="stars">' + '★' * n + '☆' * (3 - n) + '</span>'


def tag(t, bar=False):
    name, cls = TYPES[t]
    return f'<span class="tag {cls}{" bar" if bar else ""}">{name}</span>'


def parts(*items, start='a'):
    """Lettered parts list."""
    out = []
    for i, it in enumerate(items):
        out.append(f'<li><b class="pl">{chr(ord(start) + i)}</b>{it}</li>')
    return '<ol class="parts">' + ''.join(out) + '</ol>'


def answers(spec):
    """spec: list of labels -> inline answer lines; ('stack', [labels]) -> stacked lines; None -> none."""
    if not spec:
        return ''
    cls = 'answers'
    if isinstance(spec, tuple) and spec[0] == 'stack':
        cls += ' stack'
        spec = spec[1]
    return f'<div class="{cls}">' + ''.join(f'<span>{html.escape(l)}<i></i></span>' for l in spec) + '</div>'


def card(i, c):
    t = c['type']
    cls = 'card ' + TYPES[t][1] + (' span2' if c.get('span') == 2 else '')
    top = [f'<div class="num">{i}</div>', tag(t)]
    if c.get('review'):
        top.append(f'<span class="tag rev">Review {c["review"]}</span>')
    if c.get('draw'):
        top.append('<span class="tag draw">✎ Draw a diagram</span>')
    top.append(stars(c['stars']))
    fig = ''
    if c.get('fig'):
        fig = f'<div class="fig{" center" if c.get("figpos") == "center" else ""}">{c["fig"]}</div>'
    body = c['text']
    if c.get('figpos') == 'center':
        body = body + fig if c.get('figafter', True) else fig + body
    else:
        body = fig + body
    space = '<div class="space dots"></div>' if c.get('draw') else '<div class="space"></div>'
    return (f'<div class="{cls}"><div class="top">{"".join(top)}</div>'
            f'<div class="body">{body}</div>{space}{answers(c.get("ans"))}</div>')


def header(ch, badge_small, badge, title):
    tstyle = ' style="font-size:15px;top:24px"' if len(title) > 40 else ''
    return (f'<div class="hdr" style="background-image:url(assets/strip-ch{ch["n"]}.jpg)">'
            f'<div class="logo"><img src="assets/logo.png" alt=""></div>'
            f'<div class="badge"><small>{badge_small}</small><b>{badge}</b></div>'
            f'<div class="kick">MATHEMATICS · YEAR 10 · CHAPTER {ch["n"]} · EXTENSION</div>'
            f'<h1{tstyle}>{title}</h1><div class="ff">FAST FINISHERS</div></div>')


def footer(ch, pn):
    return (f'<div class="ftr"><span>Kingscliff High School · Year 10 Mathematics</span>'
            f'<span class="pn">{pn}</span><span>Chapter {ch["n"]} · {ch["topic"]} · Extension</span></div>')


def ex_page(ch, ex, pn):
    note = ex.get('note', '')
    types = ''.join(tag(t, bar=True) for t in 'URP')
    ext = (f'<div class="ext"><span class="pill">EXTENSION</span><div class="msg">Finished exercise {ex["code"]}? '
           f'Try these. Show your working in each box.{"<br>" + note if note else ""}</div>'
           f'<div class="types">{types}</div></div>')
    ref = ''
    grid_style = ''
    if ex.get('ref'):
        ref = f'<div class="ref">{ex["ref"]}</div>'
        grid_style = f' style="top:{ex.get("gridtop", 230)}px"'
    cards = ''.join(card(i + 1, c) for i, c in enumerate(ex['cards']))
    rows = ex.get('rows')
    if rows:
        grid_style = grid_style[:-1] + f';grid-template-rows:{rows}"' if grid_style else f' style="grid-template-rows:{rows}"'
    return (f'<section class="page">{header(ch, "EXERCISE", ex["code"], ex["title"])}{ext}{ref}'
            f'<div class="grid"{grid_style}>{cards}</div>{footer(ch, pn)}</section>')


def cover(ch, first_pages):
    rows = ''.join(f'<tr><td>{e["code"]}</td><td>{e["title"]}</td><td class="pg">{p}</td><td><span class="box"></span></td></tr>'
                   for e, p in zip(ch['exercises'], first_pages))
    legend = (
        '<div><h4>EVERY CARD HAS A TYPE</h4>' + tag('U', True) + ' ' + tag('R', True) + '<div style="height:4px"></div>' + tag('P', True) + '</div>'
        f'<div><h4>MIXED IN</h4><span class="tag rev">Review {ch["exercises"][0]["code"]}</span> questions from earlier exercises</div>'
        '<div><h4>NO DIAGRAM?</h4><span class="tag draw">✎ Draw a diagram</span> first, in the dotted space</div>'
        '<div><h4>CHALLENGE</h4><span class="stars">★☆☆</span> to <span class="stars">★★★</span><br>The last card on each page is the challenge.</div>')
    return (f'<section class="page cover" style="background-image:url(assets/cover-ch{ch["n"]}.jpg)">'
            f'<div class="logo"><img src="assets/logo.png" alt="Kingscliff High School"></div>'
            f'<div class="stage">YEAR 10 TRANSITION</div>'
            f'<div class="band"><div class="bolt">{BOLT}</div><h1>EXTENSION BOOKLET</h1>'
            f'<div class="sub">FOR FAST FINISHERS · CHALLENGE QUESTIONS</div></div>'
            f'<div class="stack"><div class="main"><div class="chapno"><small>CHAPTER</small><b>{ch["n"]}</b></div>'
            f'<div class="kick">YEAR 10 MATHEMATICS · CHAPTER {ch["n"]} · EXTENSION: FAST FINISHERS</div>'
            f'<h2>{ch["topic"]}</h2>'
            f'<p class="intro">One page of harder questions for each exercise in Chapter {ch["n"]}. Finish the exercise '
            f'in your Chapter {ch["n"]} booklet first, then come here. Worked answers are at the back.</p>'
            f'<table><tr><th>EXERCISE</th><th>EXTENSION TOPIC</th><th>PAGE</th><th>DONE</th></tr>{rows}</table></div>'
            f'<div class="legend">{legend}</div>'
            f'<div class="namebar">NAME <span class="l"></span> CLASS <span class="l" style="flex:.55"></span> TEACHER <span class="l" style="flex:.6"></span></div></div>'
            f'<div class="art">Artwork: {ch["artwork_short"]}</div></section>')


def letters(w):
    import re
    return re.sub(r'(^|&nbsp;)([a-e]) ', r'\1<i class="al">\2</i> ', w)


def answer_pages(ch, start_pn):
    out = []
    groups = ch['answer_pages']
    exmap = {e['code']: e for e in ch['exercises']}
    for gi, group in enumerate(groups):
        blocks = []
        for code in group:
            e = exmap[code]
            qs = ''.join(f'<div class="ansq"><div class="n">{i + 1}</div><div class="w">{letters(c["worked"])}</div></div>'
                         for i, c in enumerate(e['cards']))
            blocks.append(f'<div class="ansex"><h3><b>{code}</b> · {e["title"]}</h3>{qs}</div>')
        if gi == len(groups) - 1:
            blocks.append(
                '<div class="about"><h4>ABOUT THE ARTWORK</h4>'
                f'<p>{ch["artwork_long"]}</p>'
                '<h4>ACKNOWLEDGEMENT OF COUNTRY</h4><p style="margin:0">We acknowledge the Bundjalung people, the Traditional '
                'Custodians of the land on which Kingscliff High School stands, and pay our respects to Elders past and present.</p></div>')
        ext = ('<div class="ext"><span class="pill">ANSWERS</span><div class="msg">Worked answers. Check your method as well as '
               'your answer. Rounded answers may differ slightly in the last decimal place.</div></div>')
        out.append(f'<section class="page">{header(ch, "ANSWERS", "Ch " + str(ch["n"]), "Worked answers")}{ext}'
                   f'<div class="anscols">{"".join(blocks)}</div>{footer(ch, start_pn + gi)}</section>')
    return out


def build(ch):
    n_ex = len(ch['exercises'])
    pages = [cover(ch, [i + 2 for i in range(n_ex)])]
    for i, ex in enumerate(ch['exercises']):
        pages.append(ex_page(ch, ex, i + 2))
    pages += answer_pages(ch, n_ex + 2)
    title = f'Year 10 Chapter {ch["n"]} {ch["topic"]} extension booklet'
    return (f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>{title}</title>'
            f'<style>{CSS}</style></head><body>{"".join(pages)}</body></html>')


# ---------------------------------------------------------------- SVG helpers
INK = '#1E2A24'
FILL = '#FBF1D0'
ACC = '#1E6B4A'


def svg(w, h, body, z=1):
    return (f'<svg width="{w * z:.0f}" height="{h * z:.0f}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Lexend, sans-serif" font-size="10.5">{body}</svg>')


def poly(pts, fill=FILL, sw=1.6, dash=None, close=True):
    p = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    tagn = 'polygon' if close else 'polyline'
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<{tagn} points="{p}" fill="{fill if close else "none"}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"{d}/>'


def line(x1, y1, x2, y2, sw=1.4, dash=None, col=INK):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d}/>'


def text(x, y, s, anchor='middle', col=INK, size=None, weight=None):
    a = f' font-size="{size}"' if size else ''
    b = f' font-weight="{weight}"' if weight else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" fill="{col}"{a}{b}>{s}</text>'


def rightangle(x, y, dx, dy, s=7):
    """Small square at corner (x,y); dx,dy = +1/-1 direction into the shape."""
    return (f'<polyline points="{x + dx * s:.1f},{y:.1f} {x + dx * s:.1f},{y + dy * s:.1f} {x:.1f},{y + dy * s:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width="1"/>')


def arc_path(cx, cy, r, a0, a1):
    """Arc from angle a0 to a1 (degrees, anticlockwise from +x, y up)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f'M{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 {large} 0 {x1:.1f},{y1:.1f}'


def sector(cx, cy, r, a0, a1, fill=FILL):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    return (f'<path d="M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} {arc_path(cx, cy, r, a0, a1)[1 + len(f"{x0:.1f},{y0:.1f} "):]} Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')


def sector_path(cx, cy, r, a0, a1, fill=FILL, sw=1.6):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{cx:.1f},{cy:.1f} L{x0:.1f},{y0:.1f} A{r:.1f},{r:.1f} 0 {large} 0 {x1:.1f},{y1:.1f} Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')


def circle(cx, cy, r, fill=FILL, sw=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"{d}/>'


def dot(x, y, r=2.2, col=INK):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'


def box3d(L, W, H, s, ox=6, oy=None, labels=('', '', ''), fill=FILL, open_top=False):
    """Oblique rectangular prism. L across, H up, W receding at 45deg (half scale)."""
    dx = dy = W * s * 0.5 * 0.7071
    a, h = L * s, H * s
    oy = oy if oy is not None else dy + 4
    f = [(ox, oy + h), (ox + a, oy + h), (ox + a, oy), (ox, oy)]
    top = [(ox, oy), (ox + a, oy), (ox + a + dx, oy - dy), (ox + dx, oy - dy)]
    side = [(ox + a, oy + h), (ox + a + dx, oy + h - dy), (ox + a + dx, oy - dy), (ox + a, oy)]
    body = poly(top, '#FFF8E2' if not open_top else '#F1E3B0') + poly(side, '#F4E5B5') + poly(f, fill)
    body += line(ox, oy + h, ox + dx, oy + h - dy, 1, '3 3') + line(ox + dx, oy + h - dy, ox + a + dx, oy + h - dy, 1, '3 3') + line(ox + dx, oy + h - dy, ox + dx, oy - dy, 1, '3 3')
    lL, lW, lH = labels
    if lL: body += text(ox + a / 2, oy + h + 13, lL)
    if lW: body += text(ox + a + dx / 2 + 6, oy + h - dy / 2 + 10, lW, 'start')
    if lH: body += text(ox - 4, oy + h / 2 + 4, lH, 'end')
    return body, ox + a + dx, oy + h


def cylinder(cx, top, r, h, ry=None, fill=FILL, rlab='', hlab='', rlabel_pos='top'):
    ry = ry or r * 0.32
    b = top + h
    body = (f'<path d="M{cx - r:.1f},{top:.1f} L{cx - r:.1f},{b:.1f} A{r:.1f},{ry:.1f} 0 0 0 {cx + r:.1f},{b:.1f} L{cx + r:.1f},{top:.1f}" '
            f'fill="{fill}" stroke="{INK}" stroke-width="1.6"/>'
            f'<path d="M{cx - r:.1f},{b:.1f} A{r:.1f},{ry:.1f} 0 0 1 {cx + r:.1f},{b:.1f}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>'
            f'<ellipse cx="{cx:.1f}" cy="{top:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="#FFF8E2" stroke="{INK}" stroke-width="1.6"/>')
    if rlab:
        body += line(cx, top, cx + r, top, 1.2) + dot(cx, top, 1.8) + text(cx + r / 2, top - ry - 4, rlab, size=10)
    if hlab:
        body += text(cx + r + 5, top + h / 2 + 4, hlab, 'start')
    return body


def axes(x0, y0, w, h, xt, yt, xlab='', ylab='', ymin=0, ymax=10, grid=True, xs=None):
    """Simple axes: xt = list of (value_pos_fraction, label); yt = list of y values."""
    out = []
    if grid:
        for v in yt:
            y = y0 - (v - ymin) / (ymax - ymin) * h
            out.append(line(x0, y, x0 + w, y, 0.6, None, '#D5D8DC'))
    out.append(line(x0, y0, x0 + w, y0, 1.3) + line(x0, y0, x0, y0 - h - 4, 1.3))
    for v in yt:
        y = y0 - (v - ymin) / (ymax - ymin) * h
        out.append(line(x0 - 3, y, x0, y, 1) + text(x0 - 5, y + 3.5, f'{v:g}', 'end', size=8.5))
    for fx, lab in xt:
        out.append(text(x0 + fx * w, y0 + 12, lab, size=8.5))
    if xlab:
        out.append(text(x0 + w / 2, y0 + 24, xlab, size=9))
    if ylab:
        out.append(f'<text x="{x0 - 26:.1f}" y="{y0 - h / 2:.1f}" text-anchor="middle" font-size="9" fill="{INK}" '
                   f'transform="rotate(-90 {x0 - 26:.1f} {y0 - h / 2:.1f})">{ylab}</text>')
    return ''.join(out)


def table(rows, head=None, cls='t', firstcol_left=False):
    h = ''
    if head:
        h = '<tr>' + ''.join(f'<th{" class=l" if (firstcol_left and i == 0) else ""}>{c}</th>' for i, c in enumerate(head)) + '</tr>'
    b = ''.join('<tr>' + ''.join(f'<td{" class=l" if (firstcol_left and i == 0) else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<table class="{cls}">{h}{b}</table>'


def spreadsheet(cells, cols='ABC', widths=None):
    """cells: list of rows (list of strings). Rendered like a spreadsheet extract."""
    head = '<tr><th></th>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr>'
    body = ''.join(f'<tr><th>{i + 1}</th>' + ''.join(f'<td>{v}</td>' for v in r) + '</tr>' for i, r in enumerate(cells))
    return f'<table class="t ss">{head}{body}</table>'


def stemleaf(rows, key, head=True):
    h = '<tr class="h"><td class="s">Stem</td><td>Leaf</td></tr>' if head else ''
    b = ''.join(f'<tr><td class="s">{s}</td><td>{" ".join(str(x) for x in l)}</td></tr>' for s, l in rows)
    return f'<table class="sl">{h}{b}</table><div class="key">{key}</div>'
