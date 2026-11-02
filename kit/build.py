"""Generic explainer builder. Copy this kit to ~/work/<topic>/explainer-html/, then edit CONFIG and write scenes_*.py.
Run with: /usr/bin/python3 build.py
Each scenes module exposes SCENES = [fn, ...]; each fn returns dict(title, narr, say, aud, svg)."""
import sys, os, json, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine import DEFS

# ---- CONFIG: edit these ----
TITLE = 'Example explainer'
BRAND = 'Example · fictional data'
OUT = 'explainer.html'
ORDER = [('example_scenes', 0), ('example_scenes', 1), ('example_scenes', 2), ('example_scenes', 3)]  # (module, index in SCENES)
BRIDGE = {}  # scene title -> "Next problem: ..." appended to the last beat of that step
# quiz: [cue, ask, [options], index of right answer, why]. rotate() moves the right answer around.
QS = [
 ['"Example question the room will ask?"', 'What do you say?', ['Wrong one', 'The right one', 'Another wrong one'], 1, 'Why the right one is right.'],
]
INTRO_PARAS = ['One or two plain sentences on what this is and who it is for.', 'Each step has a small animation, a plain explanation and a red box with the words to say.']
# ---- end CONFIG ----

def rotate(qs):
    out = []
    for i, (cue, ask, opts, ok, why) in enumerate(qs):
        k = [0, 2, 1][i % 3]
        opts2 = opts[k:] + opts[:k]
        out.append([cue, ask, opts2, (ok - k) % len(opts), why])
    return out

def collect():
    scenes = []
    for mod, k in ORDER:
        sc = importlib.import_module(mod).SCENES[k]()
        sc['svg'] = DEFS + sc['svg']
        br = BRIDGE.get(sc['title'])
        if br:
            sc['narr'][-1] += ' ' + br
            sc['say'][-1] += ' ' + br
        assert len(sc['say']) == len(sc['narr']), sc['title']
        scenes.append(sc)
    return scenes

if __name__ == '__main__':
    scenes = collect()
    paras = ''.join(f'<p>{p}</p>' for p in INTRO_PARAS)
    introhtml = '`<div class="card"><h2>' + TITLE + '</h2>' + paras + '<ol>${PY.map(s=>`<li>${s.title}</li>`).join(\'\')}</ol></div>`'
    intro = json.dumps({'kind': 'intro', 'title': TITLE, 'narr': ['Start']})
    tpl = open(f'{HERE}/template.html').read()
    out = (tpl.replace('__SCENES__', json.dumps(scenes, ensure_ascii=False)).replace('__INTRO__', intro)
              .replace('__QS__', json.dumps(rotate(QS), ensure_ascii=False)).replace('__INTROHTML__', introhtml)
              .replace('__TITLE__', TITLE).replace('__BRAND__', BRAND))
    open(f'{HERE}/{OUT}', 'w').write(out)
    print(len(scenes), 'scenes,', sum(len(s['narr']) for s in scenes), 'beats,', round(len(out) / 1024), 'KB')
