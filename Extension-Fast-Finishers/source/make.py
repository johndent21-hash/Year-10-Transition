import sys, importlib, ff
for mod in sys.argv[1:]:
    ch = importlib.import_module(mod).CHAPTER
    open(f'{mod}.html', 'w').write(ff.build(ch))
