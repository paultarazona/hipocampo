import sys, importlib, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svglib
mods = sys.argv[1:]
for m in mods:
    mod = importlib.import_module(m)
    for k in sorted(dir(mod)):
        if k.startswith('d') and k[1:].isdigit():
            p = getattr(mod, k)()
            png = os.path.join(os.path.dirname(__file__), 'png') + '/' + os.path.basename(p)[:-4] + '.png'
            os.makedirs(os.path.join(os.path.dirname(__file__), 'png'), exist_ok=True)
            subprocess.run(['rsvg-convert', '-w', '1400', p, '-o', png], check=True)
            print('ok', p)
for w in svglib.WARN: print('WARN', w)
