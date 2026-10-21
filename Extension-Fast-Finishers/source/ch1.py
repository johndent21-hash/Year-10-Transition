from ff import *

TAX = ('<table><tr><th>TAXABLE INCOME</th><th>TAX ON THIS INCOME (2024–25 resident rates)</th></tr>'
       '<tr><td>$0 – $18 200</td><td>Nil</td></tr>'
       '<tr><td>$18 201 – $45 000</td><td>16c for each $1 over $18 200</td></tr>'
       '<tr><td>$45 001 – $135 000</td><td>$4288 plus 30c for each $1 over $45 000</td></tr>'
       '<tr><td>$135 001 – $190 000</td><td>$31 288 plus 37c for each $1 over $135 000</td></tr>'
       '<tr><td>$190 001 and over</td><td>$51 638 plus 45c for each $1 over $190 000</td></tr></table>'
       '<div style="margin-top:3px"><b>Medicare levy</b> = 2% of taxable income. &nbsp; <b>Taxable income</b> = gross income − deductions.</div>')


def interest_graph():
    x0, y0, w, h = 34, 128, 190, 110
    yt = [1000, 1200, 1400, 1600]
    out = axes(x0, y0, w, h, [(i / 5, str(i)) for i in range(6)], yt, 'Years', 'Value ($)', 1000, 1650)
    simple = [1000 + 100 * k for k in range(6)]
    comp = [1000 * 1.1 ** k for k in range(6)]
    for vals, col, dash, lab in ((simple, '#8A6B12', '5 3', 'A'), (comp, ACC, None, 'B')):
        pts = [(x0 + k / 5 * w, y0 - (v - 1000) / 650 * h) for k, v in enumerate(vals)]
        out += f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="2"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'
        out += ''.join(dot(x, y, 2.4, col) for x, y in pts)
        out += text(pts[-1][0] + 8, pts[-1][1] + 4, lab, 'start', col, 11, 700)
    return svg(240, 156, out, 0.85)


EX = []

EX.append(dict(code='1A', title='Review of percentages', note='Round percentages to <b>one decimal place</b> where needed.', cards=[
    dict(type='U', stars=1, text='<p>Copy and complete the table.</p>' + table(
        [['3/8', '', ''], ['', '0.45', ''], ['', '', '2.5%'], ['1¼', '', '']], ['Fraction', 'Decimal', 'Percentage']),
         fig=None, ans=None,
         worked='3/8 = <b>0.375 = 37.5%</b>; 0.45 = <b>9/20 = 45%</b>; 2.5% = <b>0.025 = 1/40</b>; 1¼ = <b>1.25 = 125%</b>.'),
    dict(type='U', stars=1, text='<p>These are all close in size.</p>' + parts(
        'Write each as a decimal: &nbsp;0.63, &nbsp;5/8, &nbsp;61%, &nbsp;2/3',
        'Write them in order, smallest to largest.',
        'Which is larger, 7/20 or 34%? Show how you know.'), ans=['b', 'c'],
         worked='a 0.63, 0.625, 0.61, 0.667 (3 d.p.) &nbsp;b <b>61%, 5/8, 0.63, 2/3</b> &nbsp;c 7/20 = 35%, so <b>7/20 is larger</b>.'),
    dict(type='R', stars=2, text='<p><b>Find the error.</b> Sam worked out 12% of $250 like this:</p>'
         '<p style="margin-left:10px;font-style:italic">12% of $250 = 250 ÷ 12 = $20.83</p>' + parts(
        'Explain Sam’s mistake.', 'Find the correct answer.', 'Show a quick way to check: find 10% and 2% of $250 and add.'),
         ans=['b', 'c'],
         worked='a 12% means 12/100, so multiply by 0.12 (or ÷ 100 × 12), not divide by 12. &nbsp;b 0.12 × 250 = <b>$30</b> &nbsp;c 10% = $25, 2% = $5, $25 + $5 = $30 ✓'),
    dict(type='P', stars=2, text='<p>In a class of 28 students, 9 walk to school, 12 catch the bus and the rest are driven.</p>' + parts(
        'What percentage walk?', 'What percentage are driven?', 'Do the three percentages add to 100%? Explain.'), ans=['a', 'b'],
         worked='a 9/28 × 100 = <b>32.1%</b> &nbsp;b 28 − 9 − 12 = 7; 7/28 = <b>25%</b> &nbsp;c Bus = 42.9%. 32.1 + 42.9 + 25 = 100% (all students counted once; rounding can make it 99.9% or 100.1%).'),
    dict(type='R', stars=2, review=None, text='<p>Mia scored 42 out of 56 in Test A and 33 out of 42 in Test B.</p>' + parts(
        'Write each score as a percentage.', 'In which test did she do better? Explain why comparing 42 and 33 is not enough.'),
         ans=['A', 'B', 'better'],
         worked='a A: 42/56 = <b>75%</b>; B: 33/42 = <b>78.6%</b> &nbsp;b <b>Test B</b>. The tests have different totals, so compare percentages, not raw marks.'),
    dict(type='P', stars=3, text='<p><b>Work backwards.</b> 15% of a number is 36.</p>' + parts(
        'Find 1% of the number.', 'Find the number.', 'Find 40% of the number.', 'Explain a different way to get c from 36.'),
         ans=['a', 'b', 'c'],
         worked='a 36 ÷ 15 = <b>2.4</b> &nbsp;b 2.4 × 100 = <b>240</b> &nbsp;c 0.4 × 240 = <b>96</b> &nbsp;d 5% = 36 ÷ 3 = 12, and 40% = 8 × 5% = 96.'),
]))

EX.append(dict(code='1B', title='Applying percentages', note='Round money to the <b>nearest cent</b>. GST is 10%.', cards=[
    dict(type='U', stars=1, text=parts('Increase $80 by 15%.', 'Decrease $64 by 25%.',
                                       'Write the single number you multiply by to increase a price by 7%.',
                                       'Write the multiplier to decrease a price by 12%.'), ans=['a', 'b', 'c', 'd'],
         worked='a 80 × 1.15 = <b>$92</b> &nbsp;b 64 × 0.75 = <b>$48</b> &nbsp;c <b>1.07</b> &nbsp;d <b>0.88</b>'),
    dict(type='U', stars=1, review='1A', text=parts('Write 0.085 as a percentage.', 'Write 0.085 as a fraction in simplest form.',
                                                    'Write 3/40 as a percentage.'), ans=['a', 'b', 'c'],
         worked='a <b>8.5%</b> &nbsp;b 85/1000 = <b>17/200</b> &nbsp;c 3 ÷ 40 = 0.075 = <b>7.5%</b>'),
    dict(type='R', stars=2, text='<p>The same jacket is sold in two shops.</p>' + table(
        [['Shop A', '$120', '25% off'], ['Shop B', '$108', '$20 off']], ['', 'Price', 'Sale']) + parts(
        'Find the sale price at each shop.', 'Which shop is cheaper, and by how much?'), ans=['A', 'B', 'b'],
         worked='a A: 120 × 0.75 = <b>$90</b>; B: 108 − 20 = <b>$88</b> &nbsp;b <b>Shop B</b> is cheaper by <b>$2</b>, even though 25% sounds like more.'),
    dict(type='P', stars=2, text='<p><b>Work backwards.</b> A TV is on sale for $630 after a 30% discount.</p>' + parts(
        'What percentage of the original price is $630?', 'Find the original price.',
        'Ali says, “Just add 30% of $630 back on.” Show that this gives the wrong answer.'), ans=['a', 'b', 'c'],
         worked='a 100% − 30% = <b>70%</b> &nbsp;b 630 ÷ 0.7 = <b>$900</b> &nbsp;c 630 × 1.3 = $819 ≠ $900. The 30% was taken from $900, not from $630.'),
    dict(type='U', stars=2, text=parts('A meal costs $48 before GST. Find the price including GST.',
                                       'A phone costs $319 <b>including</b> GST. Find the price before GST.',
                                       'How much GST is in the $319?'), ans=['a', 'b', 'c'],
         worked='a 48 × 1.1 = <b>$52.80</b> &nbsp;b 319 ÷ 1.1 = <b>$290</b> &nbsp;c 319 − 290 = <b>$29</b>'),
    dict(type='R', stars=3, text='<p>A price of $200 is increased by 10%. The new price is then decreased by 10%.</p>' + parts(
        'Find the final price.', 'Explain why the price does not go back to $200.',
        'What single percentage change gives the same final price?'), ans=['a', 'c'],
         worked='a 200 × 1.1 = 220; 220 × 0.9 = <b>$198</b> &nbsp;b The 10% decrease is taken from the bigger amount ($220), so $22 comes off but only $20 went on. &nbsp;c 198/200 = 0.99, so a <b>1% decrease</b>.'),
]))

EX.append(dict(code='1C', title='Income', note='Use 52 weeks, 26 fortnights or 12 months in a year.', cards=[
    dict(type='U', stars=1, text='<p>Ava earns a salary of $67 600 per year.</p>' + parts(
        'Find her weekly pay.', 'Find her fortnightly pay.', 'Find her monthly pay.'), ans=['a', 'b', 'c'],
         worked='a 67 600 ÷ 52 = <b>$1300</b> &nbsp;b × 2 = <b>$2600</b> &nbsp;c 67 600 ÷ 12 = <b>$5633.33</b>'),
    dict(type='U', stars=1, text='<p>Noah is paid $24.80 per hour.</p>' + parts(
        'Find his pay for a 38-hour week.', 'Find his time-and-a-half rate.', 'Find his double-time rate.'), ans=['a', 'b', 'c'],
         worked='a 38 × 24.80 = <b>$942.40</b> &nbsp;b 1.5 × 24.80 = <b>$37.20</b> &nbsp;c 2 × 24.80 = <b>$49.60</b>'),
    dict(type='P', stars=2, text='<p>Jack is paid $28 per hour. One week he works 38 normal hours, 4 hours at time and a half, and 3 hours on Sunday at double time.</p>' + parts(
        'Find his normal pay.', 'Find his overtime pay.', 'Find his total pay for the week.'), ans=['a', 'b', 'c'],
         worked='a 38 × 28 = <b>$1064</b> &nbsp;b 4 × 42 + 3 × 56 = 168 + 168 = <b>$336</b> &nbsp;c <b>$1400</b>'),
    dict(type='R', stars=2, text='<p><b>Job A</b> pays $1150 per week. <b>Job B</b> pays a retainer of $600 per week plus 5% commission on sales.</p>' + parts(
        'Find the weekly pay for Job B with sales of $9000.', 'What sales are needed for Job B to pay the same as Job A?',
        'Which job would you choose? Give a reason.'), ans=['a', 'b'],
         worked='a 600 + 0.05 × 9000 = <b>$1050</b> &nbsp;b Needs 1150 − 600 = $550 commission; 550 ÷ 0.05 = <b>$11 000</b> &nbsp;c Any reasoned answer, e.g. Job A is safer; Job B is better if you sell more than $11 000 a week.'),
    dict(type='U', stars=2, review='1B', text='<p>Zoe earns $26 per hour. She gets a 4% pay rise.</p>' + parts(
        'Find her new hourly rate.', 'Find her new pay for a 35-hour week.', 'How much more does she earn each week?'), ans=['a', 'b', 'c'],
         worked='a 26 × 1.04 = <b>$27.04</b> &nbsp;b 35 × 27.04 = <b>$946.40</b> &nbsp;c 946.40 − 910 = <b>$36.40</b>'),
    dict(type='P', stars=3, text='<p><b>Work backwards.</b> Mel earned $1092 in one week. She worked 36 normal hours and 4 hours at time and a half.</p>' + parts(
        'Explain why 4 hours at time and a half is worth the same as 6 normal hours.', 'Find Mel’s hourly rate.',
        'Check your answer by working out her pay.'), ans=['b', 'c'],
         worked='a 4 × 1.5 = 6, so it pays like 6 normal hours. &nbsp;b 36 + 6 = 42 hours; 1092 ÷ 42 = <b>$26</b> &nbsp;c 36 × 26 + 4 × 39 = 936 + 156 = $1092 ✓'),
]))

EX.append(dict(code='1D', title='Income tax', note='Use the tax table below.', ref=TAX, gridtop=262, cards=[
    dict(type='U', stars=1, text='<p>Liam earns $58 000 a year. He claims $1400 of deductions for his uniform and union fees.</p>' + parts(
        'Find his taxable income.', 'Find the tax he pays.'), ans=['a', 'b'],
         worked='a 58 000 − 1400 = <b>$56 600</b> &nbsp;b 4288 + 0.30 × 11 600 = 4288 + 3480 = <b>$7768</b>'),
    dict(type='U', stars=1, text=parts('Find the tax on a taxable income of $30 000.', 'Find the tax on a taxable income of $16 500.',
                                       'Explain your answer to b.'), ans=['a', 'b'],
         worked='a 0.16 × (30 000 − 18 200) = 0.16 × 11 800 = <b>$1888</b> &nbsp;b <b>$0</b> &nbsp;c $16 500 is under the $18 200 tax-free threshold.'),
    dict(type='R', stars=2, text='<p><b>Find the error.</b> Zara says:</p><p style="margin-left:10px;font-style:italic">“I earn $50 000, so I pay 30% tax. 0.3 × 50 000 = $15 000.”</p>' + parts(
        'Explain Zara’s mistake.', 'Find the correct tax.'), ans=['b'],
         worked='a Only the dollars over $45 000 are taxed at 30c; the first $45 000 costs $4288. &nbsp;b 4288 + 0.3 × 5000 = <b>$5788</b>'),
    dict(type='P', stars=2, text='<p>Ben’s taxable income is $72 000.</p>' + parts(
        'Find his income tax.', 'Find his Medicare levy.', 'Find the total he pays.', 'What percentage of his income is this?'),
         ans=['a', 'b', 'c', 'd'],
         worked='a 4288 + 0.3 × 27 000 = <b>$12 388</b> &nbsp;b 0.02 × 72 000 = <b>$1440</b> &nbsp;c <b>$13 828</b> &nbsp;d 13 828 ÷ 72 000 = <b>19.2%</b>'),
    dict(type='P', stars=2, text='<p>Ruby’s employer takes $420 tax (PAYG) out of each fortnightly pay. Her taxable income for the year is $62 000.</p>' + parts(
        'How much tax was taken out over the year?', 'Find her tax plus Medicare levy.', 'Will she get a refund or owe money? How much?'),
         ans=['a', 'b', 'c'],
         worked='a 26 × 420 = <b>$10 920</b> &nbsp;b 4288 + 0.3 × 17 000 = 9388; Medicare 1240; total <b>$10 628</b> &nbsp;c 10 920 − 10 628: <b>refund of $292</b>'),
    dict(type='R', stars=3, text='<p><b>Work backwards.</b> Tom paid $6088 income tax (not counting Medicare).</p>' + parts(
        'Explain how you know his taxable income is more than $45 000.', 'Find his taxable income.'), ans=['b'],
         worked='a The tax on $45 000 is only $4288, and Tom paid more than that. &nbsp;b 6088 − 4288 = 1800; 1800 ÷ 0.30 = 6000; 45 000 + 6000 = <b>$51 000</b>'),
]))

EX.append(dict(code='1E', title='Budgeting', note='Use 52 weeks, 26 fortnights or 12 months in a year.', cards=[
    dict(type='U', stars=1, text='<p>Convert each amount.</p>' + parts('$45 per week to per year', '$1200 per quarter to per year',
                                                                       '$1200 per quarter to per month', '$180 per fortnight to per week'),
         ans=['a', 'b', 'c', 'd'],
         worked='a 45 × 52 = <b>$2340</b> &nbsp;b 1200 × 4 = <b>$4800</b> &nbsp;c 4800 ÷ 12 = <b>$400</b> &nbsp;d 180 ÷ 2 = <b>$90</b>'),
    dict(type='U', stars=1, text='<p>Kai’s weekly net pay is $1150.</p>' + table(
        [['Rent', '$420'], ['Food', '$160'], ['Transport', '$65'], ['Phone', '$15'], ['Fun', '$90']], ['Expense', 'Per week'], firstcol_left=True) + parts(
        'Find his total weekly expenses.', 'How much is left over each week?', 'What percentage of his pay goes on rent?'),
         ans=['a', 'b', 'c'],
         worked='a 420 + 160 + 65 + 15 + 90 = <b>$750</b> &nbsp;b 1150 − 750 = <b>$400</b> &nbsp;c 420 ÷ 1150 = <b>36.5%</b>'),
    dict(type='R', stars=2, review='1C', text='<p>Ella earns $23.50 per hour and works 30 hours a week. She saves 15% of her pay.</p>' + parts(
        'Find her weekly pay.', 'How much does she save each week?', 'How many weeks to save $1000?'), ans=['a', 'b', 'c'],
         worked='a 30 × 23.50 = <b>$705</b> &nbsp;b 0.15 × 705 = <b>$105.75</b> &nbsp;c 1000 ÷ 105.75 = 9.46, so <b>10 weeks</b>'),
    dict(type='P', stars=2, text='<p>Milan’s car costs:</p>' + table(
        [['Registration', '$780 per year'], ['Insurance', '$96 per month'], ['Servicing', '$450 every 6 months'], ['Fuel', '$55 per week']],
        firstcol_left=True) + parts('Find the total cost for one year.', 'Find the average cost per week.'), ans=['a', 'b'],
         worked='a 780 + 1152 + 900 + 2860 = <b>$5692</b> &nbsp;b 5692 ÷ 52 = <b>$109.46</b>'),
    dict(type='R', stars=2, text='<p>Ali’s fortnightly net pay is $1400. He budgets 30% for rent, 20% for food, 15% for transport, 10% for savings and the rest for other things.</p>' + parts(
        'What percentage is for other things?', 'How much does he save each fortnight?', 'How many fortnights to save $2100 for a holiday?'),
         ans=['a', 'b', 'c'],
         worked='a 100 − 75 = <b>25%</b> &nbsp;b 0.1 × 1400 = <b>$140</b> &nbsp;c 2100 ÷ 140 = <b>15 fortnights</b>'),
    dict(type='P', stars=3, text='<p>Sophie wants a $1350 laptop in 12 weeks. She already has $270. She earns $310 a week and spends $235.</p>' + parts(
        'How much does she need to save each week to reach her goal?', 'Will she reach her goal in 12 weeks? Show working.',
        'If not, how many weeks will it take?'), ans=['a', 'b', 'c'],
         worked='a (1350 − 270) ÷ 12 = <b>$90</b> &nbsp;b She saves 310 − 235 = $75 a week. 270 + 12 × 75 = $1170, so <b>no</b> ($180 short). &nbsp;c 1080 ÷ 75 = 14.4, so <b>15 weeks</b>'),
]))

EX.append(dict(code='1F', title='Simple interest', note='Use <span class="math">I = PRN</span>. Round money to the <b>nearest cent</b>.', cards=[
    dict(type='U', stars=1, text='<p>$3000 is invested at 4% p.a. simple interest for 5 years.</p>' + parts(
        'Find the interest.', 'Find the total value of the investment.'), ans=['a', 'b'],
         worked='a 3000 × 0.04 × 5 = <b>$600</b> &nbsp;b <b>$3600</b>'),
    dict(type='U', stars=1, text='<p>$2500 is invested at 6% p.a. simple interest.</p>' + parts(
        'Find the interest for 18 months.', 'Find the interest for 9 months.', 'Explain why b is half of a.'), ans=['a', 'b'],
         worked='a N = 1.5: 2500 × 0.06 × 1.5 = <b>$225</b> &nbsp;b N = 0.75: <b>$112.50</b> &nbsp;c Simple interest grows by the same amount each month, so half the time gives half the interest.'),
    dict(type='R', stars=2, text='<p><b>Find the error.</b> Jo finds the simple interest on $800 at 5% p.a. for 3 years:</p><p style="margin-left:10px;font-style:italic"><span class="math">I</span> = 800 × 5 × 3 = $12 000</p>' + parts(
        'Explain why the answer must be wrong.', 'Find the error and the correct interest.'), ans=['b'],
         worked='a The interest can’t be 15 times the amount invested. &nbsp;b R must be a decimal: 0.05. 800 × 0.05 × 3 = <b>$120</b>'),
    dict(type='P', stars=2, text='<p><b>Work backwards.</b> $4000 is invested for 3 years and earns $540 simple interest.</p>' + parts(
        'Find the interest earned in one year.', 'Find the interest rate.'), ans=['a', 'b'],
         worked='a 540 ÷ 3 = <b>$180</b> &nbsp;b 180 ÷ 4000 = 0.045 = <b>4.5% p.a.</b>'),
    dict(type='P', stars=2, text='<p><b>Work backwards.</b> How long will it take $2000 to earn $350 simple interest at 3.5% p.a.?</p>' + parts(
        'Find the interest for one year.', 'Find the number of years.'), ans=['a', 'b'],
         worked='a 2000 × 0.035 = <b>$70</b> &nbsp;b 350 ÷ 70 = <b>5 years</b>'),
    dict(type='R', stars=3, review='1E', text='<p>Max borrows $6000 for a car at 8% p.a. simple interest for 3 years. He repays it in equal monthly amounts.</p>' + parts(
        'Find the interest.', 'Find the total amount he repays.', 'Find the monthly repayment.',
        'Max’s budget allows $230 a month for the car. Can he afford it?'), ans=['a', 'b', 'c', 'd'],
         worked='a 6000 × 0.08 × 3 = <b>$1440</b> &nbsp;b <b>$7440</b> &nbsp;c 7440 ÷ 36 = <b>$206.67</b> &nbsp;d <b>Yes</b>, $206.67 is less than $230.'),
]))

EX.append(dict(code='1G', title='Compound interest', note='Use <span class="math">A = P</span>(1 + <span class="math">R</span>)<sup><span class="math">n</span></sup>. Round money to the <b>nearest cent</b>.', cards=[
    dict(type='U', stars=1, text='<p>$1000 is invested at 5% p.a., compounded annually. Copy and complete the table.</p>' + table(
        [['1', '$1000', '', ''], ['2', '', '', ''], ['3', '', '', '']], ['Year', 'Start', 'Interest', 'End']), ans=None,
         worked='Year 1: $1000, $50, <b>$1050</b>. Year 2: $1050, $52.50, <b>$1102.50</b>. Year 3: $1102.50, $55.13, <b>$1157.63</b>'),
    dict(type='U', stars=1, text='<p>$5000 is invested at 6% p.a., compounded annually, for 4 years.</p>' + parts(
        'Find the final amount <span class="math">A</span>.', 'Find the interest earned.'), ans=['a', 'b'],
         worked='a 5000 × 1.06<sup>4</sup> = <b>$6312.38</b> &nbsp;b <b>$1312.38</b>'),
    dict(type='R', stars=2, review='1F', text='<p>$4000 is invested for 3 years at 5% p.a.</p>' + parts(
        'Find the simple interest.', 'Find the compound interest (compounded annually).', 'Explain why compound interest gives more.'),
         ans=['a', 'b'],
         worked='a 4000 × 0.05 × 3 = <b>$600</b> &nbsp;b 4000 × 1.05<sup>3</sup> = 4630.50, so <b>$630.50</b> &nbsp;c With compound interest you also earn interest on the interest from earlier years.'),
    dict(type='U', stars=2, text='<p>$2000 is invested at 6% p.a., <b>compounded monthly</b>, for 2 years.</p>' + parts(
        'Find the rate per month, <span class="math">R</span>, as a decimal.', 'Find the number of months, <span class="math">n</span>.',
        'Find the final amount.'), ans=['a', 'b', 'c'],
         worked='a 0.06 ÷ 12 = <b>0.005</b> &nbsp;b 2 × 12 = <b>24</b> &nbsp;c 2000 × 1.005<sup>24</sup> = <b>$2254.32</b>'),
    dict(type='R', stars=2, text='<p><b>Find the error.</b> To find $3000 at 4% p.a. compounded annually for 2 years, Kim writes:</p><p style="margin-left:10px;font-style:italic"><span class="math">A</span> = 3000(1 + 4)<sup>2</sup> = $75 000</p>' + parts(
        'Explain Kim’s mistake.', 'Find the correct amount.'), ans=['b'],
         worked='a 4% must be written as 0.04, so the bracket is 1.04, not 5. &nbsp;b 3000 × 1.04<sup>2</sup> = <b>$3244.80</b>'),
    dict(type='P', stars=3, text='<p>$5000 is invested at 8% p.a., compounded annually.</p>' + parts(
        'Find its value after 5 years.', 'Try different numbers of years to find when it first becomes more than $10 000.',
        'Would it take twice as long to reach $20 000? Explain.'), ans=['a', 'b'],
         worked='a 5000 × 1.08<sup>5</sup> = <b>$7346.64</b> &nbsp;b 9 years: $9995.02; 10 years: $10 794.62, so <b>10 years</b> &nbsp;c No. 18 years gives $19 980.10 and 19 years gives $21 578.60, so <b>19 years</b>. Once it reaches $10 000 it doubles again in about 9 more years, because each year’s interest is bigger than the last.'),
]))

EX.append(dict(code='1H', title='Investments and loans', note='Round money to the <b>nearest cent</b>.', cards=[
    dict(type='U', stars=1, text='<p>Chloe borrows $15 000 for a car. She repays $380 per month for 4 years.</p>' + parts(
        'Find the total amount she repays.', 'Find the interest she pays.'), ans=['a', 'b'],
         worked='a 380 × 48 = <b>$18 240</b> &nbsp;b 18 240 − 15 000 = <b>$3240</b>'),
    dict(type='U', stars=1, text='<p>A fridge costs $1800. It can be bought with a 10% deposit, then $85 per month for 2 years.</p>' + parts(
        'Find the deposit.', 'Find the total amount paid.', 'How much more is this than the cash price?'), ans=['a', 'b', 'c'],
         worked='a 0.1 × 1800 = <b>$180</b> &nbsp;b 180 + 85 × 24 = <b>$2220</b> &nbsp;c <b>$420</b>'),
    dict(type='R', stars=2, review='1F', text='<p>Look at Chloe’s loan in question 1.</p>' + parts(
        'Find the interest she pays each year.', 'Find the simple interest rate for the loan.'), ans=['a', 'b'],
         worked='a 3240 ÷ 4 = <b>$810</b> &nbsp;b 810 ÷ 15 000 = 0.054 = <b>5.4% p.a.</b>'),
    dict(type='P', stars=2, text='<p>Dev borrows $1000. Interest of 1% is added each month, then he repays $200. Copy and complete the table.</p>' + table(
        [['1', '$1000.00', '', '$200', ''], ['2', '', '', '$200', ''], ['3', '', '', '$200', '']],
        ['Month', 'Start', 'Interest', 'Repay', 'Owing']), ans=None,
         worked='Month 1: 1000, $10, 200, <b>$810.00</b>. Month 2: 810, $8.10, 200, <b>$618.10</b>. Month 3: 618.10, $6.18, 200, <b>$424.28</b>'),
    dict(type='R', stars=2, text='<p>Lena has $10 000 to invest for 3 years.<br><b>Option A:</b> 4.2% p.a. simple interest<br><b>Option B:</b> 4% p.a. compounded annually</p>' + parts(
        'Find the interest for each option.', 'Which option is better, and by how much?'), ans=['A', 'B', 'b'],
         worked='a A: 10 000 × 0.042 × 3 = <b>$1260</b>; B: 10 000 × 1.04<sup>3</sup> − 10 000 = <b>$1248.64</b> &nbsp;b <b>Option A</b>, by <b>$11.36</b>'),
    dict(type='P', stars=3, text='<p>A phone costs $1200. Three ways to pay:</p>'
         '<p>1: cash, with a 5% discount<br>2: 24 payments of $55 per month<br>3: $200 deposit, then $45 per month for 24 months</p>' + parts(
        'Find the total cost of each option.', 'Find the difference between the cheapest and dearest options.',
        'Give one reason someone might still choose option 2.'), ans=['1', '2', '3', 'b'],
         worked='a 1: <b>$1140</b>; 2: <b>$1320</b>; 3: 200 + 1080 = <b>$1280</b> &nbsp;b 1320 − 1140 = <b>$180</b> &nbsp;c E.g. they don’t have $1140 or $200 now, and $55 a month fits their budget.'),
]))

EX.append(dict(code='1I', title='Comparing interest using technology', note='In spreadsheet formulas <b>*</b> means × and <b>^</b> means “to the power of”.', cards=[
    dict(type='U', stars=1, fig=spreadsheet([['Principal', '5000'], ['Rate', '0.04'], ['Years', '6'], ['Interest', '=B1*B2*B3'], ['Total', '']], 'AB'),
         text='<p>This spreadsheet works out simple interest.</p>' + parts('What number will cell B4 show?',
                                                                            'Write a formula for B5 to give the total value.'), ans=['a', 'b'],
         worked='a 5000 × 0.04 × 6 = <b>1200</b> &nbsp;b <b>=B1+B4</b> (gives 6200)'),
    dict(type='U', stars=1, text='<p>Use the cells from question 1. Which formula gives the value of $5000 invested at 4% p.a. <b>compounded annually</b> for 6 years?</p>'
         '<p style="font-family:Liberation Mono,monospace;font-size:10.5px">A &nbsp;=B1*B2^B3<br>B &nbsp;=B1*(1+B2)^B3<br>C &nbsp;=B1*(1+B2*B3)</p>' + parts(
        'Choose the correct formula and find its value.', 'What does formula C work out?'), ans=['a', 'b'],
         worked='a <b>B</b>: 5000 × 1.04<sup>6</sup> = <b>$6326.60</b> &nbsp;b C gives the simple interest total, $6200.'),
    dict(type='R', stars=2, fig=spreadsheet([['Year', 'Balance'], ['0', '2000'], ['1', '=B2*1.05'], ['2', ''], ['3', ''], ['4', '']], 'AB'),
         text='<p>Cell B3 contains =B2*1.05 and is filled down.</p>' + parts(
             'What interest rate is used?', 'Find the balances shown in B3 to B6.'), ans=['a'],
         worked='a <b>5% p.a.</b> compounded annually &nbsp;b <b>2100, 2205, 2315.25, 2431.01</b>'),
    dict(type='P', stars=2, fig=interest_graph(), figpos='center', text='<p>$1000 is invested at 10% p.a. for 5 years. One graph is simple interest and one is compound interest.</p>' + parts(
        'Which graph is compound interest? How can you tell?', 'Find the difference in value after 5 years.'), ans=['b'],
         worked='a <b>B</b>. It curves upward because the interest grows each year; A goes up $100 each year (straight line). &nbsp;b 1610.51 − 1500 = <b>$110.51</b>'),
    dict(type='R', stars=2, review='1G', text='<p>A spreadsheet finds compound interest paid <b>monthly</b> with the formula</p>'
         '<p style="font-family:Liberation Mono,monospace;font-size:10.5px">=B1*(1+B2/12)^(B3*12)</p><p>B1 is the principal, B2 the yearly rate and B3 the number of years.</p>' + parts(
        'Explain why it uses B2/12 and B3*12.', 'Find the value for $3000 at 6% p.a. for 2 years.'), ans=['b'],
         worked='a The yearly rate is split into 12 monthly rates, and there are 12 compounding periods each year. &nbsp;b 3000 × 1.005<sup>24</sup> = <b>$3381.48</b>'),
    dict(type='P', stars=3, text='<p>Lucy has $8000 to invest.<br><b>Bank A:</b> 4.5% p.a. simple interest<br><b>Bank B:</b> 4.2% p.a. compounded annually</p>' + parts(
        'Find the value at each bank after 4 years.', 'Find the value at each bank after 5 years.',
        'Which bank is better for a long-term investment? Explain.'), ans=['a', 'b'],
         worked='a A: <b>$9440</b>; B: 8000 × 1.042<sup>4</sup> = <b>$9431.07</b> (A better) &nbsp;b A: <b>$9800</b>; B: <b>$9827.17</b> (B better) &nbsp;c <b>Bank B</b> for 5 years or more, because compound interest keeps growing faster.'),
]))

CHAPTER = dict(
    n=1, topic='Financial mathematics', exercises=EX,
    answer_pages=[['1A', '1B', '1C', '1D', '1E'], ['1F', '1G', '1H', '1I']],
    artwork_short='a spiral from the tail of a seahorse in Seahorse Valley, part of the Mandelbrot set, coloured gold.',
    artwork_long='The pictures in this booklet are parts of the Mandelbrot set, drawn by a computer that repeats one simple rule, '
                 'z → z² + c, hundreds of times for every point. This one is a spiral from the tail of a “seahorse” in Seahorse Valley. '
                 'Zoom in on any part of the edge and you find more detail, forever. Maths can make beautiful things.',
)
