"""Tiny DSL for the step-by-step Domain 1 explainer. Everything is inline SVG with data-* beat attributes."""
INK, GREY, RED, SOFT = '#111111', '#6b7280', '#d71f26', '#eceef1'

def A(**k):
    return ''.join(f' data-{key}="{v}"' for key, v in k.items() if v is not None)

def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def T(x, y, t, size=30, fill=INK, anchor='start', w=400, **k):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{A(**k)}>{esc(t)}</text>'

def TL(x, y, lines, size=28, fill=INK, anchor='start', w=400, lh=None, **k):
    lh = lh or size * 1.28
    inner = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else lh}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{w}"{A(**k)}>{inner}</text>'

def R(x, y, w, h, fill='#fff', stroke=INK, sw=4, rx=14, dash=None, **k):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{A(**k)}/>'

def Gp(inner, **k):
    return f'<g{A(**k)}>{inner}</g>'

def Ln(x1, y1, x2, y2, stroke=INK, sw=4, arrow=False, dash=None, **k):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = (' marker-end="url(#%s)"' % {RED: 'ahr', GREY: 'ahg'}.get(stroke, 'ah')) if arrow else ''
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{stroke}" stroke-width="{sw}" fill="none"{d}{m}{A(**k)}/>'

def Box(x, y, w, h, label, size=30, sub=None, fill='#fff', stroke=INK, sw=4, dash=None, rx=14, **k):
    cx = x + w / 2
    if sub:
        body = T(cx, y + h / 2 - 2, label, size, INK, 'middle', 700) + T(cx, y + h / 2 + 28, sub, 22, GREY, 'middle', 400)
    else:
        body = T(cx, y + h / 2 + size * 0.35, label, size, INK, 'middle', 700)
    return Gp(R(x, y, w, h, fill, stroke, sw, rx, dash) + body, **k)

def wid(t, size, pad=40):
    return int(len(t) * size * 0.56 + pad)

def Bub(x, y, t, size=26, fill='#fff', stroke=INK, w=None, **k):
    w = w or wid(t, size)
    return Gp(R(x, y, w, size + 30, fill, stroke, 3, 18) + T(x + w / 2, y + size + 8, t, size, INK, 'middle', 400), **k)

def Person(x, y, label='You', **k):
    return Gp(f'<circle cx="{x}" cy="{y-30}" r="22" fill="#fff" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M{x-36} {y+44} a36 36 0 0 1 72 0 z" fill="#fff" stroke="{INK}" stroke-width="4"/>'
              + T(x, y + 84, label, 26, INK, 'middle', 700), **k)

def Key(x, y, color=RED, s=1.0, **k):
    return Gp(f'<g transform="translate({x},{y}) scale({s})"><circle cx="10" cy="15" r="9" fill="none" stroke="{color}" stroke-width="4.5"/>'
              f'<path d="M19 15 H46 M38 15 V25 M44 15 V23" stroke="{color}" stroke-width="4.5" fill="none"/></g>', **k)

def Lock(x, y, color=INK, s=1.0, **k):
    return Gp(f'<g transform="translate({x},{y}) scale({s})"><rect x="0" y="14" width="30" height="22" rx="4" fill="{color}"/>'
              f'<path d="M5 14 V9 a10 10 0 0 1 20 0 V14" fill="none" stroke="{color}" stroke-width="4.5"/></g>', **k)

def Doc(x, y, w=70, h=90, **k):
    return Gp(R(x, y, w, h, '#fff', INK, 3, 6) + ''.join(f'<path d="M{x+12} {y+22+i*20} H{x+w-12}" stroke="{GREY}" stroke-width="3"/>' for i in range(3)), **k)

DEFS = '<defs>' + ''.join(f'<marker id="{i}" markerUnits="userSpaceOnUse" markerWidth="18" markerHeight="18" refX="15" refY="9" orient="auto"><path d="M0 0 L16 9 L0 18 Z" fill="{c}"/></marker>' for i, c in (('ah', INK), ('ahr', RED), ('ahg', GREY))) + '</defs>'

def Cap(t, s=None, e=None, y=560, col=INK, size=26):
    return T(480, y, t, size, col, 'middle', 700, s=s, e=e)

def Card(x, y, w, h, title, sub=None, hot=False, dash=None, **k):
    body = R(x, y, w, h, '#fff', RED if hot else INK, 4, 14, dash)
    if sub:
        body += T(x + w / 2, y + h / 2 - 2, title, 26, RED if hot else INK, 'middle', 700) + T(x + w / 2, y + h / 2 + 28, sub, 20, GREY, 'middle')
    else:
        body += T(x + w / 2, y + h / 2 + 9, title, 26, RED if hot else INK, 'middle', 700)
    return Gp(body, **k)

def Tag(x, y, t, size=20, **k):
    w = int(len(t) * size * 0.6 + 24)
    return Gp(R(x, y, w, size + 14, '#fff', RED, 2, 8) + T(x + w / 2, y + size + 1, t, size, RED, 'middle', 700), **k)

