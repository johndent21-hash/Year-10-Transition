# Year 10 Extension (Fast Finishers) booklets: source

These files rebuild the PDFs one folder up. The layout matches the Year 9 Standard extension booklets.

- `ch1.py`, `ch2.py`, `ch4.py` hold the questions, diagrams and worked answers for each chapter. Edit these to change content.
- `ff.py` holds the shared layout (cover, page header, cards and answers pages).
- `ch1.html`, `ch2.html` and `ch4.html` are the built pages. You can open them in a browser, or edit them directly for quick text fixes.
- `assets/` holds the school logo, the Lexend font and the gold Mandelbrot artwork (made by `mandel.py`).

To rebuild (Python 3 and Node with Playwright are needed):

    python3 make.py ch1 ch2 ch4
    node print.js ch1.html ch1.pdf
