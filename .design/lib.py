"""Drawing kit for the dark profile: palette, fonts, text helpers, font embedding."""
import base64, io, pathlib, re
from fontTools.ttLib import TTFont
from fontTools import subset

FONTS = pathlib.Path(__file__).parent / "fonts"

# palette
BG, PANEL, LINE, FG, MUTE = "#0F1419", "#151C23", "#26313B", "#E6EDF3", "#8B98A5"
GRID = "#1B242C"
CU, TE, LA, GOLD = "#D9824A", "#4FB3A9", "#A99BE0", "#D5A24C"
INK = "#0B0F13"
ACCENTS = [CU, TE, LA]

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


def svg(w, h, title, desc, body, bg=BG, rx=14):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc><style>/*FONTS*/</style>'
            f'<defs><pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22,0 H0 V22" fill="none" stroke="{GRID}" stroke-width="1"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>{body}</svg>')


def section_title(y, num, title, note=None, x0=60, x1=940):
    o = text(x0, y, f"{num} /", "monob", 13, CU, ls=1) + text(x0 + measure(f"{num} /", "monob", 13, 1) + 10, y, title.upper(), "monob", 13, FG, ls=3)
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
