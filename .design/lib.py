"""Drawing kit for the dark profile: palette, fonts, text helpers, font embedding."""
import base64, io, pathlib, re
from fontTools.ttLib import TTFont
from fontTools import subset

FONTS = pathlib.Path(__file__).parent / "fonts"

# ── colour themes ─────────────────────────────────────────────────────
# Pick one with `theme:` in profile.yml. Roles:
#   name1/name2  the two lines of the big name     primary  section numbers, labels, tagline
#   a1/a2/a3     rotating accents (cards, chips)   bg/panel/line/grid/fg/mute  the dark base
THEMES = {
    "sakura": dict(bg="#120E16", panel="#1A1520", line="#342A3C", grid="#1E1825", fg="#F7EEF5", mute="#A898AE",
                   name1="#F9C6DD", name2="#8ED1F7", primary="#F2709C", a1="#8ED1F7", a2="#F2709C", a3="#F7E07A"),
    "orchid": dict(bg="#0E0B1A", panel="#161226", line="#2E2645", grid="#18142B", fg="#F1EDFF", mute="#9C94B8",
                   name1="#C9B6FF", name2="#FF6FB5", primary="#FF6FB5", a1="#9F7AEA", a2="#FF6FB5", a3="#5EEAD4"),
    "aurora": dict(bg="#0A1117", panel="#101A22", line="#22323D", grid="#13202A", fg="#E8F3F1", mute="#8EA3A8",
                   name1="#A7F3D0", name2="#7DD3FC", primary="#5EEAD4", a1="#5EEAD4", a2="#7DD3FC", a3="#C4B5FD"),
    "sunset": dict(bg="#140F14", panel="#1D161C", line="#3A2C35", grid="#21191F", fg="#FFF1EA", mute="#B39C9F",
                   name1="#FFB38A", name2="#FF5E8A", primary="#FF8A65", a1="#FFC857", a2="#FF5E8A", a3="#B8A1FF"),
    "dusk": dict(bg="#100C1A", panel="#181327", line="#322A47", grid="#19142B", fg="#F6EEFF", mute="#A198BA",
                 name1="#C9B6FF", name2="#FF7A6B", primary="#FF7A6B", a1="#FFC857", a2="#FF6FB5", a3="#9F7AEA"),
    "flamingo": dict(bg="#150F17", panel="#1E1621", line="#3B2B3D", grid="#22182A", fg="#FFF0F5", mute="#B49CAA",
                     name1="#FFB38A", name2="#FF6FB5", primary="#FF6FB5", a1="#FFC857", a2="#FF6FB5", a3="#B8A1FF"),
    "ember": dict(bg="#0D1117", panel="#161B22", line="#30363D", grid="#161D26", fg="#E6EDF3", mute="#8B949E",
                  name1="#E6EDF3", name2="#F78166", primary="#F78166", a1="#79C0FF", a2="#F78166", a3="#D2A8FF"),
    "lilac": dict(bg="#110F17", panel="#19161F", line="#332D3D", grid="#1C1824", fg="#F4F0FA", mute="#A39CB0",
                  name1="#E9D5FF", name2="#A78BFA", primary="#A78BFA", a1="#A78BFA", a2="#F0ABFC", a3="#93C5FD"),
}
T = THEMES["sakura"]


def _hex(c):
    c = c.lstrip("#")
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def shade(c, t=0.62):
    """Deeper version of colour c, mixed toward the background (for the name's 3D drop)."""
    a, b = _hex(c), _hex(T["bg"])
    return "#" + "".join(f"{round(x*(1-t) + y*t):02X}" for x, y in zip(a, b))


def use(theme):
    """Switch palette. Call before importing sections."""
    global T, BG, PANEL, LINE, GRID, FG, MUTE, NAME1, NAME2, PRIMARY, A1, A2, A3
    if theme not in THEMES:
        raise SystemExit(f"profile.yml: theme '{theme}' not found. Choose one of: {', '.join(THEMES)}")
    T = THEMES[theme]
    BG, PANEL, LINE, GRID, FG, MUTE = T["bg"], T["panel"], T["line"], T["grid"], T["fg"], T["mute"]
    NAME1, NAME2, PRIMARY, A1, A2, A3 = T["name1"], T["name2"], T["primary"], T["a1"], T["a2"], T["a3"]


use("sakura")
INK = "#0B0A10"

FONTMAP = {
    "disp":   ("Anton", "anton-latin-400-normal.woff2", 400, "Impact, 'Arial Narrow Bold', sans-serif"),
    "inter":  ("Inter", "inter-latin-400-normal.woff2", 400, "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"),
    "interb": ("InterB", "inter-latin-600-normal.woff2", 600, "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"),
    "interx": ("InterX", "inter-latin-800-normal.woff2", 800, "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"),
    "mono":   ("JBMono", "jetbrains-mono-latin-400-normal.woff2", 400, "ui-monospace, Menlo, Consolas, monospace"),
    "monob":  ("JBMonoB", "jetbrains-mono-latin-700-normal.woff2", 700, "ui-monospace, Menlo, Consolas, monospace"),
}
_m = {}


def _font(cls):
    if cls not in _m:
        f = TTFont(FONTS / FONTMAP[cls][1])
        _m[cls] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _m[cls]


def measure(s, cls, size, ls=0.0):
    cmap, hmtx, upm = _font(cls)
    return sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else upm * 0.55 for c in s) / upm * size + ls * max(len(s) - 1, 0)


def fit(s, cls, size, maxw, ls=0.0, minsize=8):
    while size > minsize and measure(s, cls, size, ls) > maxw:
        size -= 0.5
    return size


def wrap(s, cls, size, width, ls=0.0):
    lines, cur = [], ""
    for w in str(s).split():
        t = (cur + " " + w).strip()
        if measure(t, cls, size, ls) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text(x, y, s, cls, size, fill, anchor="start", ls=0, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size:.1f}" fill="{fill}"{a}{l} {extra}>{esc(s)}</text>'


def svg(w, h, title, desc, body, bg=None, rx=14):
    bg = bg or BG
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc><style>/*FONTS*/</style>'
            f'<defs><pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22,0 H0 V22" fill="none" stroke="{GRID}" stroke-width="1"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>{body}</svg>')


def section_title(y, num, title, note=None, x0=60, x1=940):
    o = text(x0, y, f"{num} /", "monob", 13, PRIMARY, ls=1) + text(x0 + measure(f"{num} /", "monob", 13, 1) + 10, y, title.upper(), "monob", 13, FG, ls=3)
    o += f'<path d="M{x0},{y+16} H{x1}" stroke="{LINE}"/>'
    if note:
        o += text(x1, y, note, "mono", 11, MUTE, "end")
    return o


def finalize(s):
    """Subset + embed every used font as base64 woff2 (GitHub's <img> sandbox blocks web fonts)."""
    css = []
    for cls, (fam, fn, w, fb) in FONTMAP.items():
        chars = set()
        for m in re.finditer(r'<text[^>]*class="%s"[^>]*>(.*?)</text>' % cls, s, re.S):
            t = re.sub(r"<[^>]+>", "", m.group(1)).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
            chars |= set(t)
        if not chars:
            continue
        font = TTFont(FONTS / fn)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt"]
        sub = subset.Subsetter(options=opts)
        sub.populate(text="".join(chars) + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        css.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{base64.b64encode(buf.getvalue()).decode()}) format('woff2');font-weight:{w};}}")
        css.append(f".{cls}{{font-family:'{fam}',{fb};font-weight:{w};}}")
    return s.replace("/*FONTS*/", "\n".join(css))
