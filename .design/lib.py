"""Shared drawing kit: palette, fonts, text fitting, inked shapes, finalising SVGs.

Style: bold ink outlines, flat colour, halftone/hatch shading and hard offset
shadows (urban print / poster feel). Everything is plain SVG so GitHub's
<img> sandbox renders it; fonts are subset and embedded at build time.
"""
import base64, io, math, random, re, pathlib
from fontTools.ttLib import TTFont
from fontTools import subset

HERE = pathlib.Path(__file__).parent
FONTS = HERE / "fonts"

C = dict(
    ivory="#F7EBD8", paper="#FBF3E6", terra="#C76B4D", forest="#244A3C", sage="#A3B89C",
    peach="#E8B39A", ink="#172326", gold="#D5A24C", brick="#A9533A", concrete="#D8CDBD",
    steel="#5B6770", sky="#F3D9BF", teal="#2F5D62", wood="#9A6A45", wood2="#7E5236",
    skin="#8B5A3C", skin2="#6E4329", hair="#1E1916", hair2="#4A372C",
    sagelt="#DDE6D5", peachlt="#F6D8C6", goldlt="#F2E0B6", teallt="#D3E0DC",
    term="#1B2A2D", termgreen="#A6D49F", rule="#E2D2B8",
)
INK = C["ink"]
LW = 3       # main ink weight
LW2 = 2      # detail ink weight

# css class -> (family, file, weight, fallback)
FONTMAP = {
    "disp":  ("Anton", "anton-latin-400-normal.woff2", 400, "Impact, 'Arial Narrow Bold', sans-serif"),
    "mark":  ("Marker", "permanent-marker-latin-400-normal.woff2", 400, "'Marker Felt', 'Comic Sans MS', cursive"),
    "sans":  ("Grotesk", "space-grotesk-latin-500-normal.woff2", 500, "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"),
    "sansb": ("GroteskB", "space-grotesk-latin-700-normal.woff2", 700, "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"),
    "mono":  ("JBMono", "jetbrains-mono-latin-400-normal.woff2", 400, "ui-monospace, Menlo, Consolas, monospace"),
    "monob": ("JBMonoB", "jetbrains-mono-latin-700-normal.woff2", 700, "ui-monospace, Menlo, Consolas, monospace"),
}
_metrics = {}


def _font(cls):
    if cls not in _metrics:
        f = TTFont(FONTS / FONTMAP[cls][1])
        _metrics[cls] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _metrics[cls]


# ------------------------------------------------------------------ text
def measure(s, cls, size, ls=0.0):
    cmap, hmtx, upm = _font(cls)
    w = sum(hmtx[cmap[ord(ch)]][0] if ord(ch) in cmap else upm * 0.5 for ch in s)
    return w / upm * size + ls * max(len(s) - 1, 0)


def fit(s, cls, size, maxw, ls=0.0, minsize=8):
    """Largest size <= `size` at which `s` fits in `maxw`."""
    while size > minsize and measure(s, cls, size, ls) > maxw:
        size -= 0.5
    return size


def wrap(s, cls, size, width, ls=0.0):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if measure(t, cls, size, ls) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text(x, y, s, cls, size, fill, anchor="start", ls=0, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size:.1f}" fill="{fill}"{a}{l} {extra}>{esc(s)}</text>'


def para(x, y, s, cls, size, fill, width, lh, anchor="start", ls=0, extra="", maxlines=99):
    lines = wrap(s, cls, size, width, ls)[:maxlines]
    return "\n".join(text(x, y + i * lh, ln, cls, size, fill, anchor, ls, extra) for i, ln in enumerate(lines)), len(lines)


# ------------------------------------------------------------------ document
def svg_open(w, h, title, desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">\n'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>\n<style>\n/*FONTS*/\n</style>\n{defs()}')


def defs():
    return f'''<defs>
<pattern id="dots" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="3.5" cy="3.5" r="1.25" fill="{INK}"/></pattern>
<pattern id="dotsL" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(30)"><circle cx="3.5" cy="3.5" r="1.25" fill="{C["ivory"]}"/></pattern>
<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{INK}" stroke-width="1.4"/></pattern>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22,0 H0 V22" fill="none" stroke="{C["rule"]}" stroke-width="1"/></pattern>
<filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" stitchTiles="stitch" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 0.09  0 0 0 0 0.11  0 0 0 0 0.10  0 0 0 0.5 -0.2"/>
</filter>
</defs>'''


def card(w, h, fill=None, rx=18, sh=7, grid=False):
    """The page-section card: thick ink outline + hard offset shadow."""
    fill = fill or C["ivory"]
    W, H = w - sh - 3, h - sh - 3
    out = (f'<rect x="{1.5+sh}" y="{1.5+sh}" width="{W}" height="{H}" rx="{rx}" fill="{INK}"/>'
           f'<rect x="1.5" y="1.5" width="{W}" height="{H}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{LW}"/>')
    if grid:
        out += f'<rect x="3" y="3" width="{W-3}" height="{H-3}" rx="{rx-1}" fill="url(#grid)" opacity=".7"/>'
    out += f'<rect x="1.5" y="1.5" width="{W}" height="{H}" rx="{rx}" filter="url(#grain)" opacity=".35"/>'
    return out


def panel(x, y, w, h, fill, rx=12, sh=5, lw=LW, shfill=None):
    return (f'<rect x="{x+sh}" y="{y+sh}" width="{w}" height="{h}" rx="{rx}" fill="{shfill or INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{INK}" stroke-width="{lw}"/>')


def bullet(cx, cy, label, fill, r=17, color=None, size=None):
    """Transit-line style route bullet."""
    color = color or (INK if fill in (C["sage"], C["gold"], C["peach"], C["ivory"]) else C["ivory"])
    size = size or r * 1.15
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{LW}"/>'
            + text(cx, cy + size * 0.36, label, "disp", size, color, "middle"))


def heading(x, y, num, label, color=None, note=None, right=None):
    color = color or C["terra"]
    out = bullet(x + 18, y - 8, num, color, 18, size=19)
    out += text(x + 46, y + 1, label.upper(), "disp", 27, INK, ls=1.2)
    if note and right:
        out += text(right, y, note, "mark", 19, C["terra"], "end")
    return out


def chip(x, y, label, fill, color=INK, cls="monob", size=10.5, padx=9, h=22, lw=LW2):
    w = measure(label, cls, size) + padx * 2
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{INK}" stroke-width="{lw}"/>'
            + text(x + padx, y + h / 2 + size * 0.36, label, cls, size, color)), w


def arrow_btn(cx, cy, r=17, fill=None, color=None):
    fill = fill or C["terra"]
    color = color or C["ivory"]
    return (f'<circle cx="{cx+3}" cy="{cy+3}" r="{r}" fill="{INK}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{INK}" stroke-width="{LW}"/>'
            f'<path d="M{cx-7},{cy} H{cx+7} M{cx+1},{cy-6} L{cx+7},{cy} L{cx+1},{cy+6}" stroke="{color}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


# ------------------------------------------------------------------ nature, inked
def leaf(x, y, length, width, angle, fill, lw=LW2, rib=True):
    L, W = length, width / 2
    p = f"M0,0 C{W},{-L*0.25} {W*0.9},{-L*0.75} 0,{-L} C{-W*0.9},{-L*0.75} {-W},{-L*0.25} 0,0Z"
    out = f'<g transform="translate({x:.1f},{y:.1f}) rotate({angle:.1f})"><path d="{p}" fill="{fill}" stroke="{INK}" stroke-width="{lw}" stroke-linejoin="round"/>'
    if rib:
        out += f'<path d="M0,-2 Q{W*0.15},{-L*0.5} 0,{-L*0.8}" stroke="{INK}" stroke-width="{lw*0.6:.1f}" fill="none" stroke-linecap="round"/>'
    return out + "</g>"


def sprig(x, y, scale=1.0, angle=0, color=None, n=5, seed=1):
    color = color or C["sage"]
    rnd = random.Random(seed)
    L = 110
    out = [f'<path d="M0,0 C8,-36 -6,-74 4,{-L}" stroke="{INK}" stroke-width="{LW2/scale:.2f}" fill="none" stroke-linecap="round"/>']
    for i in range(n):
        t = (i + 1) / (n + 1)
        side = 1 if i % 2 == 0 else -1
        ln = 36 * (1 - 0.4 * t)
        out.append(leaf(2 * t, -L * t, ln, ln * 0.45, side * (50 + rnd.uniform(-8, 8)), color, LW2 / scale))
    out.append(leaf(4, -L, 26, 12, 4, color, LW2 / scale))
    return f'<g transform="translate({x},{y}) rotate({angle}) scale({scale})">{"".join(out)}</g>'


def pot(x, y, w, h, fill, band=None):
    """Planter whose top-centre is (x, y)."""
    out = (f'<path d="M{x-w/2},{y} L{x+w/2},{y} L{x+w/2-w*0.12},{y+h} L{x-w/2+w*0.12},{y+h}Z" fill="{fill}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
           f'<path d="M{x+w*0.12},{y+3} L{x+w/2-3},{y+3} L{x+w/2-w*0.12-2},{y+h-2} L{x+w*0.2},{y+h-2}Z" fill="url(#hatch)" opacity=".35"/>')
    if band:
        out += f'<rect x="{x-w/2-4}" y="{y-8}" width="{w+8}" height="11" rx="2" fill="{band}" stroke="{INK}" stroke-width="{LW}"/>'
    return out


# ------------------------------------------------------------------ city
def building(x, base, w, h, fill, win=None, rows=None, cols=None, seed=0, roof=None, lw=LW2, lit=0.35):
    """Inked building with a window grid. `roof`: None | 'tank' | 'antenna' | 'step' | 'spire'."""
    rnd = random.Random(seed)
    win = win or C["ivory"]
    top = base - h
    out = [f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{lw}"/>']
    cols = cols or max(1, int(w // 12))
    rows = rows or max(1, int((h - 10) // 15))
    cw = (w - 8) / cols
    for r in range(rows):
        for c in range(cols):
            wx = x + 4 + c * cw + cw * 0.18
            wy = top + 8 + r * 15
            if wy + 8 > base - 4:
                continue
            on = rnd.random() < lit
            out.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{cw*0.64:.1f}" height="8" fill="{C["gold"] if on else win}" stroke="{INK}" stroke-width="1"/>')
    if roof == "tank":
        tx = x + w * 0.62
        out.append(f'<path d="M{tx-6},{top} l2,-10 M{tx+6},{top} l-2,-10" stroke="{INK}" stroke-width="1.6"/>'
                   f'<rect x="{tx-9}" y="{top-26}" width="18" height="16" fill="{C["wood"]}" stroke="{INK}" stroke-width="{lw}"/>'
                   f'<path d="M{tx-11},{top-26} L{tx},{top-35} L{tx+11},{top-26}Z" fill="{C["wood2"]}" stroke="{INK}" stroke-width="{lw}" stroke-linejoin="round"/>'
                   f'<path d="M{tx-9},{top-20} h18 M{tx-9},{top-15} h18" stroke="{INK}" stroke-width="1"/>')
    elif roof == "antenna":
        ax = x + w / 2
        out.append(f'<path d="M{ax},{top} V{top-30}" stroke="{INK}" stroke-width="{lw}"/><circle cx="{ax}" cy="{top-31}" r="2.6" fill="{C["terra"]}" stroke="{INK}" stroke-width="1.2"/>')
    elif roof == "step":
        out.append(f'<rect x="{x+w*0.18}" y="{top-12}" width="{w*0.64}" height="12" fill="{fill}" stroke="{INK}" stroke-width="{lw}"/>'
                   f'<rect x="{x+w*0.34}" y="{top-22}" width="{w*0.32}" height="10" fill="{fill}" stroke="{INK}" stroke-width="{lw}"/>')
    elif roof == "spire":
        out.append(f'<path d="M{x+w*0.25},{top} L{x+w/2},{top-34} L{x+w*0.75},{top}Z" fill="{fill}" stroke="{INK}" stroke-width="{lw}" stroke-linejoin="round"/>')
    # shade the right edge with hatching
    out.append(f'<rect x="{x+w-w*0.18}" y="{top+1}" width="{w*0.18-1}" height="{h-2}" fill="url(#hatch)" opacity=".28"/>')
    return "".join(out)


def skyline(x0, x1, base, seed=3, fills=None, hmin=40, hmax=120, lw=LW2, lit=0.3):
    rnd = random.Random(seed)
    fills = fills or [C["concrete"], C["peach"], C["sage"], C["terra"], C["steel"]]
    out, x, i = [], x0, 0
    roofs = [None, "tank", None, "antenna", "step", None, "spire", "tank"]
    while x < x1:
        w = rnd.choice([26, 30, 34, 40, 46])
        h = rnd.randint(hmin, hmax)
        out.append(building(x, base, w, h, fills[i % len(fills)], seed=seed * 31 + i, roof=roofs[i % len(roofs)], lw=lw, lit=lit))
        x += w + rnd.choice([0, 2, 4])
        i += 1
    return "".join(out)


def transit(points, color, w=8):
    """Thick transit-map line (rounded, with an ink casing)."""
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    return (f'<path d="{d}" stroke="{INK}" stroke-width="{w+4}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linejoin="round" stroke-linecap="round"/>')


def station(x, y, r=7):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{C["ivory"]}" stroke="{INK}" stroke-width="{LW}"/>'


# ------------------------------------------------------------------ finalise
def _resolve_defaults(svg):
    """Attributes written as x-name are defaults, dropped where `name` is set explicitly."""
    def fix(m):
        tag = m.group(0)
        explicit = {n for x, n in re.findall(r'\s(x-)?([\w:-]+)="', tag) if not x}
        return re.sub(r'\sx-([\w:-]+)="([^"]*)"', lambda a: "" if a.group(1) in explicit else f' {a.group(1)}="{a.group(2)}"', tag)
    return re.sub(r"<[a-zA-Z][^>]*>", fix, svg)


def _chars(svg, cls):
    chars = set()
    for m in re.finditer(r'<(text|tspan)[^>]*class="%s"[^>]*>(.*?)</\1>' % cls, svg, re.S):
        s = re.sub(r"<[^>]+>", "", m.group(2))
        s = s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
        chars |= set(s)
    return "".join(sorted(chars))


def finalize(svg):
    """Resolve default attrs, then subset + embed each used font as base64 woff2."""
    svg = _resolve_defaults(svg)
    css = []
    for cls, (fam, fn, w, fb) in FONTMAP.items():
        chars = _chars(svg, cls)
        if not chars:
            continue
        font = TTFont(FONTS / fn)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt"]
        sub = subset.Subsetter(options=opts)
        sub.populate(text=chars + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        b64 = base64.b64encode(buf.getvalue()).decode()
        css.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b64}) format('woff2');font-weight:{w};}}")
        css.append(f".{cls}{{font-family:'{fam}',{fb};font-weight:{w};}}")
    return svg.replace("/*FONTS*/", "\n".join(css))
