# Year 10 transition yearly test builder

Builds the Year 10 Mathematics Yearly Test and its marking guide as printable A4 PDFs. The finished PDFs are in
`Yearly test/` at the top of this repository.

| File | What it is |
|---|---|
| `Year10-Transition-Yearly-Test.pdf` | The student test: cover page, Sections A to D, and an extra working page (14 pages) |
| `Year10-Transition-Yearly-Test-Marking-Guide.pdf` | Answer summary with marking notes, a reporting page and class record, then the test with answers in red |
| `Year10-Transition-Yearly-Test-Revision.pdf` | Six-page student revision booklet: cover and checklist, one page of key ideas and practice per section, answers |

## The test

- 1 hour 15 minutes, 55 marks, 35 questions, calculators allowed.
- 80% (44 marks) from the three Cambridge MATHS GOLD 5.1 chapter reviews in this repository and the Year 10 transition
  booklets: Section A Financial mathematics (15), Section B Measurement (15), Section C Statistics and probability (14).
- 20% (11 marks) from the rest of the Year 10 syllabus: Section D index laws, substitution, equations (including one
  with a fraction), straight-line graphs with gradient and y-intercept, Pythagoras' theorem and trigonometry.
- Trickier questions have a HELP box with the formula and a worked example.

## Build

You need Node.js and Playwright (`npm install playwright && npx playwright install chromium`). Then:

```
node build.js
```

`node revision.js` builds the revision booklet the same way. This writes the PDFs into `../Yearly test/` and checks the layout of every page: it prints a warning if anything
overflows a page, spills out of its box, or leaves less than 14 mm of working space. `node build.js --shots <dir>`
also saves a PNG of every page.

## How it is made

- `test.js` holds every question: the text, help box, diagram and answer. Answers are calculated from the numbers in
  the question, so the test and the marking guide always agree. `layout` at the bottom sets which questions go on
  each page.
- `lib/figs.js` draws the diagrams (shapes, prism, cylinder, histogram, graphs, triangles) as SVG, to the sizes given.
- `lib/test.css` is the page design: the gold-and-green Year 10 transition colours and the Lexend font. Answers
  (class `key`) only show in the marking guide.
- `build.js` lays out the cover, section pages and marking guide, then prints them to PDF.
- `revision.js` holds the revision booklet: key ideas, worked examples and practice questions (different numbers from
  the test), with answers calculated in the same file. Its extra styles are in `lib/revision.css`.
