from ff import *


def lab(x, y, s, a='middle', col=INK, size=10, weight=None):
    return text(x, y, s, a, col, size, weight)


def frac(a, b):
    return f'<sup>{a}</sup>⁄<sub>{b}</sub>'


# ------------------------------------------------------------------ diagrams
def spinner():
    cols = [('R', '#E8A0A0')] * 3 + [('B', '#A9C8E8')] * 2 + [('G', '#A8D5B5')] * 2 + [('Y', '#F3E3A6')]
    cx, cy, r = 48, 48, 42
    out = ''
    for k, (l, c) in enumerate(cols):
        a0, a1 = 90 - 45 * (k + 1), 90 - 45 * k
        out += sector_path(cx, cy, r, a0, a1, c, 1.3)
        am = math.radians((a0 + a1) / 2)
        out += lab(cx + 0.66 * r * math.cos(am), cy - 0.66 * r * math.sin(am) + 4, l, size=11, weight=700)
    out += f'<polygon points="{cx - 3},{cy} {cx + 3},{cy} {cx + 1},{cy - 30} {cx - 1},{cy - 30}" fill="{INK}"/>' + dot(cx, cy, 3.5)
    return svg(96, 96, out, 1.05)


def venn(a_only, both, b_only, neither, la='S', lb='N', w=170, h=96, blank=False):
    out = f'<rect x="4" y="4" width="{w - 8}" height="{h - 8}" rx="4" fill="#fff" stroke="{INK}" stroke-width="1.4"/>'
    cx1, cx2, cy, r = w * 0.39, w * 0.61, h / 2 + 2, h * 0.34
    out += f'<circle cx="{cx1}" cy="{cy}" r="{r}" fill="#F3E3A6" fill-opacity=".7" stroke="{INK}" stroke-width="1.4"/>'
    out += f'<circle cx="{cx2}" cy="{cy}" r="{r}" fill="#A8D5B5" fill-opacity=".55" stroke="{INK}" stroke-width="1.4"/>'
    out += lab(cx1 - r * 0.75, cy - r * 0.85, la, size=11, weight=700) + lab(cx2 + r * 0.75, cy - r * 0.85, lb, size=11, weight=700)
    for x, v in ((cx1 - r * 0.45, a_only), ((cx1 + cx2) / 2, both), (cx2 + r * 0.45, b_only)):
        out += lab(x, cy + 4, v, size=12, weight=600)
    out += lab(w - 16, h - 12, neither, size=12, weight=600)
    return svg(w, h, out)


def dot_plot():
    data = {0: 3, 1: 5, 2: 4, 3: 2, 4: 1}
    x0, y0, step = 16, 70, 34
    out = line(x0 - 8, y0, x0 + 4 * step + 8, y0, 1.3)
    for v in range(5):
        x = x0 + v * step
        out += line(x, y0, x, y0 + 4, 1) + lab(x, y0 + 15, str(v), size=9.5)
        for k in range(data[v]):
            out += dot(x, y0 - 8 - k * 11, 4, ACC)
    out += lab(x0 + 2 * step, y0 + 27, 'Goals scored per game', size=9)
    return svg(170, 102, out, 1.05)


def column_trunc():
    x0, y0, w, h = 40, 98, 120, 84
    vals = [('Jan', 45), ('Feb', 50), ('Mar', 48)]
    out = axes(x0, y0, w, h, [], [40, 42, 44, 46, 48, 50], '', 'Sales ($1000s)', 40, 50)
    for i, (m, v) in enumerate(vals):
        bx = x0 + 12 + i * 38
        bh = (v - 40) / 10 * h
        out += f'<rect x="{bx}" y="{y0 - bh}" width="26" height="{bh}" fill="#E9C35A" stroke="{INK}" stroke-width="1.2"/>'
        out += lab(bx + 13, y0 + 12, m, size=9)
    return svg(170, 114, out, 1.05)


def histogram(classes, freqs, xlabel, ymax, yt, w=170, h=96, bar_fill='#E9C35A', z=1.05):
    x0, y0 = 32, h + 8
    out = axes(x0, y0, w - 44, h - 10, [], yt, '', 'Frequency', 0, ymax)
    bw = (w - 54) / len(freqs)
    for i, f in enumerate(freqs):
        bh = f / ymax * (h - 10)
        out += f'<rect x="{x0 + 5 + i * bw:.1f}" y="{y0 - bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{bar_fill}" stroke="{INK}" stroke-width="1.1"/>'
        out += lab(x0 + 5 + (i + 0.5) * bw, y0 + 11, classes[i], size=7.5)
    if xlabel:
        out += lab(x0 + (w - 44) / 2, y0 + 23, xlabel, size=8.5)
    return svg(w, h + 36, out, z)


def mini_hists():
    out = ''
    for k, (name, fs) in enumerate((('A', [8, 6, 3, 2, 1]), ('B', [1, 3, 6, 3, 1]))):
        ox = 8 + k * 92
        out += line(ox, 70, ox + 78, 70, 1.2)
        for i, f in enumerate(fs):
            out += f'<rect x="{ox + 2 + i * 15}" y="{70 - f * 7}" width="15" height="{f * 7}" fill="#E9C35A" stroke="{INK}" stroke-width="1"/>'
        out += lab(ox + 39, 84, 'Graph ' + name, size=9.5, weight=600)
    return svg(184, 90, out, 1.05)


def line_graph(xlabels, series, ymin, ymax, yt, ylab, w=200, h=100, legend=None, z=1.05, xtitle=''):
    x0, y0 = 36, h + 6
    gw, gh = w - 50, h - 6
    out = axes(x0, y0, gw, gh, [(i / (len(xlabels) - 1), l) for i, l in enumerate(xlabels)], yt, xtitle, ylab, ymin, ymax)
    styles = [(ACC, None), ('#8A6B12', '5 3')]
    for si, vals in enumerate(series):
        col, dash = styles[si]
        pts = [(x0 + i / (len(vals) - 1) * gw, y0 - (v - ymin) / (ymax - ymin) * gh) for i, v in enumerate(vals)]
        out += (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="2"'
                + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
        out += ''.join(dot(x, y, 2.6, col) for x, y in pts)
    if legend:
        for si, name in enumerate(legend):
            col, dash = styles[si]
            lx = x0 + 8 + si * 80
            out += line(lx, 8, lx + 16, 8, 2, dash, col) + lab(lx + 20, 11, name, 'start', size=8.5)
    return svg(w, h + (40 if xtitle else 26), out, z)


def blank_grid(xlabels, ymin, ymax, yt, ylab, w=210, h=96, z=1.05):
    x0, y0 = 36, h + 6
    gw, gh = w - 50, h - 6
    out = axes(x0, y0, gw, gh, [(i / (len(xlabels) - 1), l) for i, l in enumerate(xlabels)], yt, '', ylab, ymin, ymax)
    for i in range(len(xlabels)):
        x = x0 + i / (len(xlabels) - 1) * gw
        out += line(x, y0, x, y0 - gh, 0.6, None, '#D5D8DC')
    return svg(w, h + 26, out, z)


def dice_grid():
    head = [''] + [str(i) for i in range(1, 7)]
    rows = [[f'<b>{r}</b>'] + (['2', '3', '4', '5', '6', '7'] if r == 1 else [''] * 6) for r in range(1, 7)]
    return table(rows, head).replace('<table class="t">', '<table class="t" style="font-size:9.5px">')


def back_to_back():
    rows = [('', '4', '5 9'), ('8 2', '5', '5'), ('7 4 1', '6', '0 2 6 8'), ('5 3 0', '7', '1 9'), ('8 1', '8', '5')]
    b = ''.join(f'<tr><td style="text-align:right">{l}</td><td class="s" style="border-left:1.4px solid #333;text-align:center">{s}</td><td>{r}</td></tr>' for l, s, r in rows)
    h = '<tr class="h"><td style="text-align:right">Class A</td><td class="s" style="border-left:1.4px solid #333">Stem</td><td>Class B</td></tr>'
    return f'<table class="sl">{h}{b}</table><div class="key">6 | 1 means 61</div>'


EX = []

EX.append(dict(code='4A', title='Review of probability', note='Write probabilities as fractions in simplest form.', cards=[
    dict(type='U', stars=1, fig=spinner(), text='<p>This spinner has 8 equal sections: R red, B blue, G green, Y yellow.</p>' + parts(
        'P(red)', 'P(not blue)', 'P(red or yellow)', 'P(purple)'), ans=['a', 'b', 'c', 'd'],
         worked=f'a <b>{frac(3, 8)}</b> &nbsp;b {frac(6, 8)} = <b>{frac(3, 4)}</b> &nbsp;c {frac(4, 8)} = <b>{frac(1, 2)}</b> &nbsp;d <b>0</b> (impossible)'),
    dict(type='U', stars=1, text='<p>A letter is chosen at random from the word <b>MATHEMATICS</b>.</p>' + parts(
        'How many letters are there?', 'Find P(M).', 'Find P(a vowel).', 'Find P(not T).'), ans=['a', 'b', 'c', 'd'],
         worked=f'a <b>11</b> &nbsp;b <b>{frac(2, 11)}</b> &nbsp;c A, E, A, I: <b>{frac(4, 11)}</b> &nbsp;d <b>{frac(9, 11)}</b>'),
    dict(type='R', stars=2, text='<p><b>Find the error.</b> Josh says, “When you roll a die you either get a 6 or you don’t. So P(6) = ½.”</p>' + parts(
        'Explain why Josh is wrong.', 'Find the correct probability of rolling a 6.'), ans=['b'],
         worked=f'a The two outcomes are not equally likely: “not 6” covers five outcomes (1–5). &nbsp;b <b>{frac(1, 6)}</b>'),
    dict(type='P', stars=2, draw=True, text='<p><b>Work backwards.</b> A bag has 5 red, 3 blue and some green counters. The probability of red is ½.</p>' + parts(
        'How many counters are in the bag?', 'How many are green?', 'Find P(blue).'), ans=['a', 'b', 'c'],
         worked=f'a 5 is half the total, so <b>10</b> &nbsp;b 10 − 5 − 3 = <b>2</b> &nbsp;c <b>{frac(3, 10)}</b>'),
    dict(type='U', stars=2, text='<p>Two coins are tossed.</p>' + parts('List the sample space.', 'Find P(two heads).', 'Find P(at least one head).',
                                                                       'Find P(one head and one tail).'), ans=['b', 'c', 'd'],
         worked=f'a <b>HH, HT, TH, TT</b> &nbsp;b <b>{frac(1, 4)}</b> &nbsp;c <b>{frac(3, 4)}</b> &nbsp;d {frac(2, 4)} = <b>{frac(1, 2)}</b>'),
    dict(type='R', stars=3, fig=dice_grid(), text='<p>Two dice are rolled and the numbers are added.</p>' + parts(
        'Complete the table of totals.', 'Find P(total of 7).', 'Find P(total more than 9).', 'Which total is most likely? Explain.'),
         ans=['b', 'c', 'd'],
         worked=f'a 36 totals from 2 to 12 &nbsp;b {frac(6, 36)} = <b>{frac(1, 6)}</b> &nbsp;c 10, 11, 12: 3 + 2 + 1 = 6, so <b>{frac(1, 6)}</b> &nbsp;d <b>7</b>; it appears 6 times, more than any other total.'),
]))

EX.append(dict(code='4B', title='Venn diagrams and two-way tables', note='Check that the numbers in your diagram or table add to the total.', cards=[
    dict(type='U', stars=1, fig=venn('7', '3', '5', '5'), text='<p>20 students were asked if they play soccer (S) or netball (N).</p>' + parts(
        'How many play soccer?', 'Find P(both).', 'Find P(neither).', 'Find P(netball only).'), ans=['a', 'b', 'c', 'd'],
         worked=f'a 7 + 3 = <b>10</b> &nbsp;b <b>{frac(3, 20)}</b> &nbsp;c {frac(5, 20)} = <b>{frac(1, 4)}</b> &nbsp;d {frac(5, 20)} = <b>{frac(1, 4)}</b>'),
    dict(type='U', stars=1, text='<p>30 families were asked if they own a cat or a dog. Copy and complete the table.</p>' + table(
        [['<b>Cat</b>', '4', '6', '10'], ['<b>No cat</b>', '9', '', ''], ['<b>Total</b>', '', '', '30']], ['', 'Dog', 'No dog', 'Total']) + parts(
        'Find P(cat and dog).', 'Find P(no pets).', start='b'), ans=['b', 'c'],
         worked=f'a No cat/no dog <b>11</b>; no cat total <b>20</b>; dog total <b>13</b>; no dog total <b>17</b> &nbsp;b {frac(4, 30)} = <b>{frac(2, 15)}</b> &nbsp;c <b>{frac(11, 30)}</b>'),
    dict(type='R', stars=2, draw=True, text='<p>Of 30 students, 18 like maths (M), 14 like music (Mu) and 6 like both.</p>' + parts(
        'Draw a Venn diagram showing this.', 'How many like neither?', 'Find P(maths only).'), ans=['b', 'c'],
         worked=f'a M only 12, both 6, Mu only 8, neither 4 &nbsp;b 30 − 12 − 6 − 8 = <b>4</b> &nbsp;c {frac(12, 30)} = <b>{frac(2, 5)}</b>'),
    dict(type='P', stars=2, text='<p>40 people were surveyed. 22 drink coffee, 15 drink tea and 8 drink both.</p>' + table(
        [['<b>Tea</b>', '', '', ''], ['<b>No tea</b>', '', '', ''], ['<b>Total</b>', '', '', '40']], ['', 'Coffee', 'No coffee', 'Total']) + parts(
        'Find P(neither).', 'Find P(tea or coffee).', start='b'), ans=['b', 'c'],
         worked=f'a Tea: 8, 7, 15. No tea: 14, 11, 25. Total: 22, 18, 40 &nbsp;b <b>{frac(11, 40)}</b> &nbsp;c 8 + 7 + 14 = 29, so <b>{frac(29, 40)}</b>'),
    dict(type='R', stars=2, review='4A', text='<p>Events are <b>mutually exclusive</b> if they cannot happen at the same time. Are these mutually exclusive? Explain.</p>' + parts(
        'Rolling a die: getting a 2 and getting an odd number.', 'Choosing a card from a deck: getting a heart and getting a king.',
        'Find P(heart or king) for a 52-card deck.'), ans=['a', 'b', 'c'],
         worked=f'a <b>Yes</b>: 2 is not odd. &nbsp;b <b>No</b>: the king of hearts is both. &nbsp;c 13 + 4 − 1 = 16, so {frac(16, 52)} = <b>{frac(4, 13)}</b>'),
    dict(type='P', stars=3, draw=True, text='<p><b>Work backwards.</b> In a class of 28, 17 study Art, 12 study Drama and 4 study neither.</p>' + parts(
        'How many study both? Explain your method.', 'Draw a Venn diagram.', 'Find P(a student studies exactly one of the subjects).'),
         ans=['a', 'c'],
         worked=f'a 28 − 4 = 24 study at least one; 17 + 12 = 29, so <b>5</b> are counted twice. &nbsp;b Art only 12, both 5, Drama only 7, neither 4 &nbsp;c <b>{frac(19, 28)}</b>'),
]))

EX.append(dict(code='4C', title='Using relative frequencies to estimate probabilities', note='Relative frequency = frequency ÷ total number of trials.', cards=[
    dict(type='U', stars=1, text='<p>A coin is tossed 50 times and lands on heads 28 times.</p>' + parts(
        'Find the relative frequency of heads.', 'How many heads would you expect in 50 tosses?', 'Does this mean the coin is unfair? Explain.'),
         ans=['a', 'b'],
         worked='a 28 ÷ 50 = <b>0.56</b> &nbsp;b <b>25</b> &nbsp;c Not necessarily. Results vary by chance; 28 is close to 25.'),
    dict(type='U', stars=1, text='<p>A die is rolled 60 times.</p>' + table([['8', '11', '9', '12', '7', '13']], ['1', '2', '3', '4', '5', '6']) + parts(
        'Find the relative frequency of a 6.', 'Find the relative frequency of an even number.', 'How many 6s would you expect in 60 rolls?'),
         ans=['a', 'b', 'c'],
         worked=f'a {frac(13, 60)} ≈ <b>0.22</b> &nbsp;b (11 + 12 + 13) ÷ 60 = <b>0.6</b> &nbsp;c {frac(1, 6)} × 60 = <b>10</b>'),
    dict(type='R', stars=2, text='<p>Mel counts 200 cars passing her school. 46 are white.</p>' + parts(
        'Estimate the probability that the next car is white.', 'How many white cars would you expect in the next 1000 cars?'), ans=['a', 'b'],
         worked='a 46 ÷ 200 = <b>0.23</b> &nbsp;b 0.23 × 1000 = <b>230</b>'),
    dict(type='P', stars=2, text='<p>Mia shoots 48 free throws and scores 36.</p>' + parts(
        'Estimate the probability that she scores.', 'How many would you expect her to score in her next 20 shots?',
        'Would 200 shots give a better estimate? Explain.'), ans=['a', 'b'],
         worked='a 36 ÷ 48 = <b>0.75</b> &nbsp;b 0.75 × 20 = <b>15</b> &nbsp;c <b>Yes</b>. More trials give a more reliable estimate.'),
    dict(type='R', stars=2, text='<p>A spinner with three colours is spun 200 times.</p>' + table([['42', '38', '120']], ['Red', 'Blue', 'Green']) + parts(
        'Do you think the three colours have equal sections? Explain.', 'Estimate what fraction of the spinner is green.'), ans=['b'],
         worked=f'a <b>No</b>. With equal sections each colour would come up about 67 times, but green came up 120 times. &nbsp;b 120 ÷ 200 = <b>{frac(3, 5)}</b> (about 60%)'),
    dict(type='P', stars=3, review='4B', text='<p>80 people were asked how they mostly watch TV shows.</p>' + table(
        [['<b>Under 30</b>', '28', '7', ''], ['<b>30 and over</b>', '20', '25', ''], ['<b>Total</b>', '', '', '80']], ['', 'Streaming', 'Free-to-air', 'Total']) + parts(
        'Complete the totals.', 'Estimate the probability that a person prefers streaming.', 'Estimate P(streaming) for people under 30.',
        'In a town of 5000 people, how many would you expect to prefer streaming?'), ans=['b', 'c', 'd'],
         worked='a 35, 45; 48, 32 &nbsp;b 48 ÷ 80 = <b>0.6</b> &nbsp;c 28 ÷ 35 = <b>0.8</b> &nbsp;d 0.6 × 5000 = <b>3000</b>'),
]))

EX.append(dict(code='4D', title='Types of data and collecting data', note='Categorical: nominal or ordinal. Numerical: discrete or continuous.', cards=[
    dict(type='U', stars=1, text='<p>Classify each type of data.</p>' + parts('the number of siblings you have', 'your height',
                                                                              'your favourite colour', 'shirt sizes S, M, L, XL',
                                                                              'postcodes (e.g. 2487)'), ans=None,
         worked='a <b>numerical, discrete</b> &nbsp;b <b>numerical, continuous</b> &nbsp;c <b>categorical, nominal</b> &nbsp;d <b>categorical, ordinal</b> &nbsp;e <b>categorical, nominal</b>: postcodes are labels, not amounts.'),
    dict(type='U', stars=1, text='<p>A <b>census</b> collects data from everyone. A <b>sample</b> uses part of the group.</p>' + parts(
        'Recording the height of every student in your class: census or sample?', 'Testing 50 light globes from a batch of 10 000: census or sample?',
        'Why would the factory not test every globe?'), ans=['a', 'b'],
         worked='a <b>census</b> &nbsp;b <b>sample</b> &nbsp;c Testing destroys the globes, and it would take too long and cost too much.'),
    dict(type='R', stars=2, text='<p>A council wants to know how residents travel to work. It surveys people at the train station at 8 am.</p>' + parts(
        'Explain why the results may be biased.', 'Suggest a better way to collect the data.'), ans=None,
         worked='a Almost everyone there uses the train, so drivers, cyclists and people who work from home are missed. &nbsp;b Survey a random sample of residents, e.g. by post or online, at different places and times.'),
    dict(type='R', stars=2, text='<p>A survey asks: <i>“Don’t you agree that school should start later?”</i></p>' + parts(
        'Explain why this is a poor survey question.', 'Rewrite the question so that it is fair.'), ans=None,
         worked='a It is a leading question that pushes people to say yes. &nbsp;b E.g. “What time would you like school to start?” or “Should school start earlier, later or at the same time?”'),
    dict(type='P', stars=2, text='<p>20 students were asked how many pets they have:</p>'
         '<p style="letter-spacing:.06em">0 2 1 1 3 0 2 1 4 1 0 2 1 3 1 2 0 1 2 1</p>' + parts(
        'Make a frequency table.', 'What is the mode?', 'What percentage of students have 2 or more pets?'), ans=['b', 'c'],
         worked='a 0: 4, 1: 8, 2: 5, 3: 2, 4: 1 (total 20) &nbsp;b <b>1</b> &nbsp;c (5 + 2 + 1) ÷ 20 = <b>40%</b>'),
    dict(type='P', stars=3, text='<p>A school of 900 students wants a sample of 60 that represents each year group fairly.</p>' + table(
        [['180', '165', '150', '150', '135', '120']], ['Yr 7', 'Yr 8', 'Yr 9', 'Yr 10', 'Yr 11', 'Yr 12']) + parts(
        'What fraction of the school is in the sample?', 'How many from each year should be in the sample?'), ans=['a'],
         worked=f'a {frac(60, 900)} = <b>{frac(1, 15)}</b> &nbsp;b ÷ 15: <b>12, 11, 10, 10, 9, 8</b> (total 60)'),
]))

EX.append(dict(code='4E', title='Displaying and describing data', note='For stem-and-leaf plots, always read the key.', cards=[
    dict(type='U', stars=1, fig=dot_plot(), text='<p>The dot plot shows the goals a team scored in each game.</p>' + parts(
        'How many games were played?', 'What is the mode?', 'In what percentage of games did they score 3 or more?'), ans=['a', 'b', 'c'],
         worked='a 3 + 5 + 4 + 2 + 1 = <b>15</b> &nbsp;b <b>1 goal</b> &nbsp;c 3 ÷ 15 = <b>20%</b>'),
    dict(type='U', stars=1, fig=stemleaf([(1, [5, 8]), (2, [0, 3, 3, 7]), (3, [1, 4, 6, 9]), (4, [2, 5])], '2 | 3 means 23'),
         text=parts('How many values are there?', 'Find the range.', 'Find the mode.', 'Find the median.'), ans=['a', 'b', 'c', 'd'],
         worked='a <b>12</b> &nbsp;b 45 − 15 = <b>30</b> &nbsp;c <b>23</b> &nbsp;d (27 + 31) ÷ 2 = <b>29</b>'),
    dict(type='R', stars=2, text='<p>Scores in a quiz:</p><p style="letter-spacing:.04em">34 27 41 29 36 22 38 45 31 27 33 40</p>' + parts(
        'Draw an ordered stem-and-leaf plot with a key.', 'Find the median.', 'Is the data roughly symmetrical or skewed?'), ans=['b', 'c'],
         worked='a 2 | 2 7 7 9; 3 | 1 3 4 6 8; 4 | 0 1 5 &nbsp;b (33 + 34) ÷ 2 = <b>33.5</b> &nbsp;c <b>roughly symmetrical</b>'),
    dict(type='R', stars=2, fig=column_trunc(), text='<p>A shop shows its sales on this graph.</p>' + parts(
        'Why does the graph make February look much better than January?', 'Find the real percentage increase from January to February.'),
         ans=['b'],
         worked='a The vertical axis starts at 40, not 0, so the Feb column looks twice as tall. &nbsp;b 5 ÷ 45 = <b>11.1%</b>'),
    dict(type='P', stars=2, fig=back_to_back(), text='<p>Test scores for two classes.</p>' + parts(
        'Find the median of each class.', 'Find the range of each class.', 'Which class did better? Give a reason.'), ans=['A', 'B', 'c'],
         worked='a A: (67 + 70) ÷ 2 = <b>68.5</b>; B: (62 + 66) ÷ 2 = <b>64</b> &nbsp;b A: 88 − 52 = <b>36</b>; B: 85 − 45 = <b>40</b> &nbsp;c <b>Class A</b>: higher median and less spread.'),
    dict(type='R', stars=3, review='4D', fig=stemleaf([(1, [2, 5, 8]), (2, [1, 4, 4, 7]), (3, ['0', '<span style="border:1.2px solid #333;padding:0 4px">&nbsp;</span>'])], '2 | 1 means 21 push-ups'),
         text='<p>This plot shows push-ups done in one minute. One leaf is missing. The range is 26.</p>' + parts(
             'Find the missing leaf.', 'Find the median.', 'Is this data discrete or continuous? Explain.'), ans=['a', 'b', 'c'],
         worked='a 12 + 26 = 38, so the leaf is <b>8</b> &nbsp;b 9 values, so the 5th: <b>24</b> &nbsp;c <b>Discrete</b>: push-ups are counted in whole numbers.'),
]))

EX.append(dict(code='4F', title='Frequency tables and histograms', note='Percentage frequency = frequency ÷ total × 100%.', cards=[
    dict(type='U', stars=1, text='<p>Copy and complete the table.</p>' + table(
        [['0–9', '3', ''], ['10–19', '7', ''], ['20–29', '6', ''], ['30–39', '4', ''], ['<b>Total</b>', '', '']], ['Class', 'Frequency', '% frequency']) + parts(
        'Which is the modal class?', start='b'), ans=['b'],
         worked='a Total 20; 15%, 35%, 30%, 20% (100%) &nbsp;b <b>10–19</b>'),
    dict(type='U', stars=1, fig=histogram(['150–', '155–', '160–', '165–', '170–'], [2, 5, 8, 6, 3], 'Height (cm)', 8, [0, 2, 4, 6, 8]),
         text='<p>The histogram shows the heights of a group of students.</p>' + parts(
             'How many students are there?', 'Which is the modal class?', 'How many students are 165 cm or taller?', 'What percentage are under 160 cm?'),
         ans=['a', 'b', 'c', 'd'],
         worked='a 2 + 5 + 8 + 6 + 3 = <b>24</b> &nbsp;b <b>160–164 cm</b> &nbsp;c 6 + 3 = <b>9</b> &nbsp;d 7 ÷ 24 = <b>29.2%</b>'),
    dict(type='R', stars=2, text='<p>Minutes 20 students spent on their phone before school:</p>'
         '<p style="letter-spacing:.03em">12 25 7 33 18 41 22 15 9 28 36 19 24 31 14 27 20 38 11 26</p>' + parts(
        'Make a frequency table using classes 0–9, 10–19, … 40–49. Include a % frequency column.', 'Describe the shape of the data.'), ans=None,
         worked='a 2 (10%), 6 (30%), 7 (35%), 4 (20%), 1 (5%) &nbsp;b <b>roughly symmetrical</b>, peaking at 20–29 minutes'),
    dict(type='R', stars=2, fig=mini_hists(), text=parts('Which graph is symmetrical and which is positively skewed?',
                                                         'Give a real example of data that might look like graph A.'), ans=['a'],
         worked='a <b>B is symmetrical</b>; <b>A is positively skewed</b> (tail to the right). &nbsp;b E.g. the number of pets per family, or weekly income: most values are small and a few are large.'),
    dict(type='P', stars=2, review='4E', fig=stemleaf([(1, [3, 6, 9]), (2, [0, 2, 5, 5, 8]), (3, [1, 4, 7]), (4, [0])], '2 | 5 means 25'),
         text=parts('Make a frequency table with classes 10–19, 20–29, 30–39 and 40–49.', 'Which is the modal class?',
                    'What percentage of values are 30 or more?'), ans=['b', 'c'],
         worked='a 3, 5, 3, 1 (total 12) &nbsp;b <b>20–29</b> &nbsp;c 4 ÷ 12 = <b>33.3%</b>'),
    dict(type='P', stars=3, text='<p><b>Work backwards.</b> 40 students did a quiz out of 19.</p>' + table(
        [['0–4', '10%', ''], ['5–9', '', ''], ['10–14', '30%', ''], ['15–19', '20%', '']], ['Score', '% freq.', 'Frequency']) + parts(
        'Find the missing percentage.', 'Find each frequency.', 'How many students scored 10 or more?', 'Can you tell how many scored exactly 12? Explain.'),
         ans=['a', 'c'],
         worked='a 100 − 60 = <b>40%</b> &nbsp;b <b>4, 16, 12, 8</b> &nbsp;c 12 + 8 = <b>20</b> &nbsp;d <b>No</b>. Grouped data only shows how many are in 10–14, not each score.'),
]))

EX.append(dict(code='4G', title='Time-series data', note='A time series shows how data changes over time. Look for a trend.', cards=[
    dict(type='U', stars=1, fig=line_graph(['6am', '8am', '10am', '12pm', '2pm', '4pm', '6pm'], [[12, 14, 19, 22, 25, 23, 18]], 10, 26, [10, 14, 18, 22, 26], 'Temp (°C)', w=230),
         figpos='center', figafter=False, text=parts('What was the highest temperature, and when?', 'By how much did it rise from 6 am to 2 pm?',
                                                     'In which 2-hour period did it rise the fastest?'), ans=['a', 'b', 'c'],
         worked='a <b>25 °C at 2 pm</b> &nbsp;b 25 − 12 = <b>13 °C</b> &nbsp;c <b>8 am to 10 am</b> (up 5 °C)'),
    dict(type='U', stars=1, text='<p>Electric cars sold in a state (thousands):</p>' + table(
        [['2', '3', '5', '9', '14', '21', '30']], ['2019', '2020', '2021', '2022', '2023', '2024', '2025']) + parts(
        'Describe the trend.', 'Is the number growing by the same amount each year? Explain.', 'Predict the sales for 2026.'), ans=['c'],
         worked='a <b>Upward</b> trend &nbsp;b <b>No</b>: the increases are 1, 2, 4, 5, 7, 9, so it is growing faster each year. &nbsp;c About <b>40 000</b> (anything about 38 000–45 000 with a reason)'),
    dict(type='R', stars=2, fig=blank_grid(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], 50, 90, [50, 60, 70, 80, 90], 'Dam level (%)'),
         figpos='center', figafter=True, text='<p>Dam levels: Jan 82%, Feb 76%, Mar 70%, Apr 65%, May 61%, Jun 58%.</p>' + parts(
             'Plot the data on the grid and join the points.', 'Describe the trend.', 'Predict the level for July.'), ans=['c'],
         worked='a Points plotted and joined with straight lines &nbsp;b <b>Downward</b>, but falling more slowly each month &nbsp;c About <b>55%</b>'),
    dict(type='P', stars=2, fig=line_graph(['Summer', 'Autumn', 'Winter', 'Spring'], [[480, 300, 120, 340], [90, 210, 400, 180]], 0, 500, [0, 100, 200, 300, 400, 500],
                                           'Sales', w=210, legend=['Ice-creams', 'Hot chocolates']),
         figpos='center', figafter=False, text=parts('In which season were the most hot chocolates sold?', 'Describe the pattern in the two graphs.',
                                                     'In which season did hot chocolate outsell ice-cream?'), ans=['a', 'c'],
         worked='a <b>Winter</b> &nbsp;b Seasonal and opposite: ice-cream is high in summer and low in winter; hot chocolate is the reverse. &nbsp;c <b>Winter</b> only'),
    dict(type='R', stars=2, review='1A', fig=line_graph(['2021', '2022', '2023'], [[10500, 12000, 15000]], 9000, 15000, [9000, 11000, 13000, 15000], '', w=170),
         text='<p>The graph shows visitors to a museum.</p><p><b>Find the error.</b> Tim says, “Visitors went up 100% from 2022 to 2023, because the graph doubled in height.”</p>' + parts(
             'Explain Tim’s mistake.', 'Find the real percentage increase.'), ans=['b'],
         worked='a The axis starts at 9000, not 0, so heights above the axis are misleading. &nbsp;b 3000 ÷ 12 000 = <b>25%</b>'),
    dict(type='P', stars=3, draw=True, text='<p>Population of a town:</p>' + table(
        [['4200', '4600', '5100', '5500', '6000', '6400']], ['2000', '2005', '2010', '2015', '2020', '2025']) + parts(
        'Draw a time-series graph.', 'Find the average increase every 5 years.', 'Predict the population in 2030.',
        'Why are predictions far into the future less reliable?'), ans=['b', 'c'],
         worked='a Graph with year on the horizontal axis &nbsp;b (6400 − 4200) ÷ 5 = <b>440</b> &nbsp;c 6400 + 440 ≈ <b>6840</b> &nbsp;d The trend may change (new housing, jobs, people moving away).'),
]))

EX.append(dict(code='4H', title='Measures of centre and spread', note='Mean = sum ÷ number of values. Median = middle value in order.', cards=[
    dict(type='U', stars=1, text=parts('For 4, 7, 7, 9, 13 find the mean, median, mode and range.',
                                       'For 12, 15, 18, 20, 23, 26 find the median.'), ans=('stack', ['mean', 'median', 'mode', 'range', 'b median']),
         worked='a mean 40 ÷ 5 = <b>8</b>; median <b>7</b>; mode <b>7</b>; range <b>9</b> &nbsp;b (18 + 20) ÷ 2 = <b>19</b>'),
    dict(type='U', stars=1, text='<p>Goals scored in 20 games:</p>' + table([['4', '6', '5', '3', '2']], ['0', '1', '2', '3', '4']).replace('<tr><th>0', '<tr><th>Goals</th><th>0').replace('<tr><td>4', '<tr><th>Games</th><td>4') + parts(
        'Find the total number of goals.', 'Find the mean.', 'Find the mode.', 'Find the median.'), ans=['a', 'b', 'c', 'd'],
         worked='a 0 + 6 + 10 + 9 + 8 = <b>33</b> &nbsp;b 33 ÷ 20 = <b>1.65</b> &nbsp;c <b>1</b> &nbsp;d 10th value is 1, 11th is 2, so <b>1.5</b>'),
    dict(type='R', stars=2, text='<p>The ages of people in a car pool are 14, 15, 15, 16, 15, 14, 16 and 62.</p>' + parts(
        'Find the mean age.', 'Find the median age.', 'Which better describes a typical age? Explain.'), ans=['a', 'b'],
         worked='a 167 ÷ 8 = <b>20.9</b> &nbsp;b <b>15</b> &nbsp;c The <b>median</b>: the outlier (62) pulls the mean up.'),
    dict(type='P', stars=2, text='<p><b>Work backwards.</b> The mean of 5 test scores is 72. Four of the scores are 65, 80, 70 and 74.</p>' + parts(
        'Find the total of all 5 scores.', 'Find the fifth score.'), ans=['a', 'b'],
         worked='a 5 × 72 = <b>360</b> &nbsp;b 360 − 289 = <b>71</b>'),
    dict(type='R', stars=2, review='4E', fig=stemleaf([(2, [3, 5, 8]), (3, [0, 4, 4, 9]), (4, [1, 6])], '3 | 4 means 34'),
         text=parts('Find the mean.', 'Find the median.', 'Find the mode.', 'Find the range.'), ans=['a', 'b', 'c', 'd'],
         worked='a 300 ÷ 9 = <b>33.3</b> &nbsp;b <b>34</b> &nbsp;c <b>34</b> &nbsp;d 46 − 23 = <b>23</b>'),
    dict(type='P', stars=3, text='<p>Ben’s mean score for 4 tests is 68. Each test is out of 100.</p>' + parts(
        'What must he score on test 5 to raise his mean to 72?', 'Can he raise his mean to 85 with one more test? Explain.',
        'What is the highest mean he could have after 5 tests?'), ans=['a', 'c'],
         worked='a 5 × 72 − 4 × 68 = 360 − 272 = <b>88</b> &nbsp;b <b>No</b>: he would need 425 − 272 = 153, more than 100. &nbsp;c (272 + 100) ÷ 5 = <b>74.4</b>'),
]))

CHAPTER = dict(
    n=4, topic='Probability and statistics', exercises=EX,
    answer_pages=[['4A', '4B', '4C', '4D'], ['4E', '4F', '4G', '4H']],
    artwork_short='a tiny copy of the whole set, hanging on branching filaments, part of the Mandelbrot set, coloured gold.',
    artwork_long='The pictures in this booklet are parts of the Mandelbrot set, drawn by a computer that repeats one simple rule, '
                 'z → z² + c, hundreds of times for every point. This one shows a tiny copy of the whole set hanging on branching filaments. '
                 'Zoom in on any part of the edge and you find more detail, forever. Maths can make beautiful things.',
)
