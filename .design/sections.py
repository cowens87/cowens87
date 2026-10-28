"""Every section of the profile, drawn from profile.yml values."""
from lib import *


# ------------------------------------------------------------------ header
def hero(P):
    W, H = 1000, 330
    first, last = P["first_name"].upper(), P["last_name"].upper()
    o = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="url(#grid)"/>',
         f'<path d="M0,32 H{W}" stroke="{LINE}"/>']
    for i, c in enumerate([A2, A3, A1]):
        o.append(f'<circle cx="{22+i*16}" cy="16" r="5" fill="{c}"/>')
    o.append(text(W / 2, 21, f"~/{P['github_username']} — README.md", "mono", 11.5, MUTE, "middle"))
    # stacked poster name with an extruded drop
    ns = min(fit(first, "disp", 112, 420, 2), fit(last, "disp", 112, 420, 2))
    y2 = 280
    y1 = y2 - ns * 1.02
    for s, y, col, sh in [(first, y1, NAME1, shade(NAME1)), (last, y2, NAME2, shade(NAME2))]:
        for k in range(1, 7):
            o.append(text(40 + k, y + k, s, "disp", ns, sh, ls=2))
        o.append(text(40, y, s, "disp", ns, col, ls=2, extra=f'stroke="{INK}" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round"'))
    rx = 540
    for i, s in enumerate(P["focus"][:4]):
        y = 130 + i * 26
        o.append(f'<rect x="{rx}" y="{y-9}" width="6" height="6" fill="{[A1, A2, A3, NAME1][i]}"/>')
        o.append(text(rx + 18, y, s.upper(), "monob", fit(s.upper(), "monob", 12.5, 400, 2), MUTE, ls=2))
    t1, t2 = (P["tagline"] + ["", ""])[:2]
    o.append(text(rx, 256, t1, "interb", fit(t1, "interb", 24, 420), FG))
    o.append(text(rx, 288, t2, "interb", fit(t2, "interb", 24, 420), PRIMARY))
    focus = " · ".join(P["focus"])
    return svg(W, H, f"{P['first_name']} {P['last_name']}", f"{focus}. {' '.join(P['tagline'])}", "".join(o), bg=PANEL)


# ------------------------------------------------------------------ 01 about
def about(P):
    W = 1000
    lines = wrap(P["about"], "inter", 16, 880)
    H = 90 + len(lines) * 25 + 10
    o = [section_title(40, P.get("_nums", {}).get("about", "01"), "About")]
    for i, ln in enumerate(lines):
        o.append(text(60, 90 + i * 25, ln, "inter", 16, FG, extra='opacity=".9"'))
    return svg(W, H, "01 / About", P["about"], "".join(o))


# ------------------------------------------------------------------ 02 toolkit
def toolkit(P):
    W = 1000
    rows = P["toolkit"][:8]
    n = (len(rows) + 1) // 2
    H = 82 + n * 32 + 6
    o = [section_title(40, P.get("_nums", {}).get("toolkit", "02"), "Toolkit")]
    for i, (k, v) in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 60 + col * 450, 90 + row * 32
        o.append(text(x, y, k.upper(), "monob", fit(k.upper(), "monob", 11.5, 126, 1.4), PRIMARY, ls=1.4))
        o.append(text(x + 136, y, v, "inter", fit(v, "inter", 14, 300), FG))
    desc = "; ".join(f"{k}: {v}" for k, v in rows)
    return svg(W, H, "02 / Toolkit", desc, "".join(o))


# ------------------------------------------------------------------ 03 AI engineering
def ai(P):
    W, H = 1000, 250
    o = [section_title(40, P.get("_nums", {}).get("ai", "03"), "AI engineering", P.get("ai_tools"))]
    for i, col in enumerate(P["ai_engineering"][:3]):
        x, c = 60 + i * 300, [A1, A2, A3][i]
        o.append(f'<rect x="{x}" y="76" width="280" height="150" rx="10" fill="{PANEL}" stroke="{LINE}"/><rect x="{x}" y="76" width="280" height="3" rx="1.5" fill="{c}"/>')
        o.append(text(x + 20, 112, col["title"], "interb", fit(col["title"], "interb", 15, 244), FG))
        for j, it in enumerate(col["items"][:3]):
            o.append(text(x + 20, 144 + j * 26, "›", "monob", 14, c) + text(x + 36, 144 + j * 26, it, "inter", fit(it, "inter", 13.5, 224), MUTE))
    desc = (P.get("ai_tools", "") + ". " + "; ".join(f"{c['title']}: {', '.join(c['items'])}" for c in P["ai_engineering"]))
    return svg(W, H, "03 / AI engineering", desc, "".join(o))


# ------------------------------------------------------------------ 04 builds
def builds_header(P):
    return svg(1000, 64, "04 / Featured builds", "", section_title(40, P.get("_nums", {}).get("builds", "04"), "Featured builds"))


def build_card(b, i):
    W, H = 300, 96
    c = [A1, A2, A3][i % 3]
    linked = bool(b.get("repo") or b.get("url"))
    o = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>']
    o.append(f'<circle cx="24" cy="34" r="5" fill="{c}"/>')
    maxw = 210 if linked else 150
    o.append(text(38, 39, b["name"].upper(), "monob", fit(b["name"].upper(), "monob", 14, maxw, 1), FG, ls=1))
    o.append(text(20, 70, b["description"], "inter", fit(b["description"], "inter", 13, 262), MUTE))
    if linked:
        o.append(f'<path d="M{W-42},34 h12 m-5,-5 l5,5 l-5,5" stroke="{c}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        o.append(f'<rect x="{W-94}" y="24" width="76" height="20" rx="10" fill="none" stroke="{LINE}"/>' + text(W - 56, 38, "in progress", "mono", 9.5, MUTE, "middle"))
    return svg(W, H, b["name"], b["description"], "".join(o), rx=10)


# ------------------------------------------------------------------ 05 exploring
def exploring(P):
    W = 1000
    o = [section_title(40, P.get("_nums", {}).get("exploring", "05"), "Currently exploring", P.get("exploring_note", "updated quarterly"))]
    x, y = 60, 76
    for i, it in enumerate(P["exploring"]):
        s = "> " + it
        w = measure(s, "mono", 12) + 22
        if x + w > 940:
            x, y = 60, y + 36
        o.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="none" stroke="{[A1, A2, A3][i % 3]}" stroke-opacity=".6"/>' + text(x + 11, y + 17.5, s, "mono", 12, FG))
        x += w + 8
    H = y + 26 + 24
    return svg(W, H, "05 / Currently exploring", ", ".join(P["exploring"]), "".join(o))


# ------------------------------------------------------------------ 06 activity
# GitHub's own dark-mode contribution colors, so the calendar reads like the real thing
LEVELS = ["#161B22", "#0E4429", "#006D32", "#26A641", "#39D353"]
LANG_COLORS = [A1, A2, A3, NAME1, PRIMARY, MUTE]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LEVEL_INDEX = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def activity(P, data=None):
    """data = {"weeks": [[count|None]*7], "levels": [[level|None]*7], "starts": ["YYYY-MM-DD"], "total": int,
               "languages": [(name, share)]}, or None for a placeholder grid."""
    W, H = 1000, 300
    o = [section_title(40, P.get("_nums", {}).get("activity", "06"), "Activity", "live from GitHub · updated daily")]
    cell, gap = 12.5, 3.5
    step = cell + gap
    weeks = ((data or {}).get("weeks") or [[None] * 7 for _ in range(53)])[-53:]
    levels = ((data or {}).get("levels") or [])[-53:]
    starts = ((data or {}).get("starts") or [])[-53:]
    mx = max([c for w in weeks for c in w if c] or [1])
    gx, gy = 96 + (53 - len(weeks)) * step, 96
    # month labels along the top
    changes, prev = [], None
    for ci, d in enumerate(starts):
        m = int(d[5:7]) - 1
        if m != prev:
            changes.append((ci, m))
            prev = m
    if len(changes) > 1 and changes[1][0] - changes[0][0] < 3:
        changes = changes[1:]          # like GitHub: skip a stub first month
    for ci, m in changes:
        if ci < len(starts) - 2:
            o.append(text(gx + ci * step, gy - 10, MONTHS[m], "inter", 11, MUTE))
    # weekday labels
    for r, lab in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        o.append(text(60, gy + r * step + 10, lab, "inter", 11, MUTE))
    for ci, wk in enumerate(weeks):
        for r, cnt in enumerate(wk):
            if cnt is None and data:
                continue
            if levels:
                lvl = LEVEL_INDEX.get((levels[ci] or [None] * 7)[r] or "NONE", 0)
            else:
                lvl = 0 if not cnt else min(4, 1 + int(3.999 * (cnt - 1) / max(mx - 1, 1)))
            o.append(f'<rect x="{gx+ci*step:.1f}" y="{gy+r*step:.1f}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[lvl]}" '
                     f'stroke="#ffffff" stroke-opacity=".05"/>')
    yb = gy + 7 * step + 26
    # Less / More legend, right-aligned under the grid
    lx = 940 - 5 * step - measure("More", "inter", 11) - 8
    o.append(text(lx - 8, yb, "Less", "inter", 11, MUTE, "end"))
    for i, c in enumerate(LEVELS):
        o.append(f'<rect x="{lx+i*step:.1f}" y="{yb-10}" width="{cell}" height="{cell}" rx="2" fill="{c}" stroke="#ffffff" stroke-opacity=".05"/>')
    o.append(text(lx + 5 * step + 4, yb, "More", "inter", 11, MUTE))
    if data:
        o.append(text(60, yb, f"{data['total']:,} contributions in the last year", "interb", 13.5, FG))
        langs = data.get("languages", [])[:6]
        if langs:
            y2 = yb + 34
            x, bw = 60, 880
            for i, (name, share) in enumerate(langs):
                w = bw * share
                o.append(f'<rect x="{x:.1f}" y="{y2-8}" width="{max(w-2,1):.1f}" height="8" rx="4" fill="{LANG_COLORS[i]}"/>')
                x += w
            lx2 = 60
            for i, (name, share) in enumerate(langs):
                s_ = f"{name} {share*100:.0f}%"
                o.append(f'<circle cx="{lx2+4}" cy="{y2+16}" r="4" fill="{LANG_COLORS[i]}"/>' + text(lx2 + 13, y2 + 20, s_, "mono", 11, MUTE))
                lx2 += measure(s_, "mono", 11) + 30
        desc = f"Contribution calendar: {data['total']} contributions in the last year. Languages: " + ", ".join(f"{n} {s_*100:.0f}%" for n, s_ in langs)
    else:
        o.append(text(60, yb, "Live contributions appear here after the first workflow run.", "mono", 11.5, MUTE))
        desc = "Placeholder for the live contribution calendar."
    return svg(W, H, "06 / Activity", desc, "".join(o))


# ------------------------------------------------------------------ 07 connect
def connect(P):
    W, H = 1000, 96
    o = [section_title(40, P.get("_nums", {}).get("connect", "07"), "Connect")]
    if P.get("open_to"):
        o.append(text(60, 84, "open to: " + P["open_to"], "mono", 12, MUTE))
    return svg(W, H, "07 / Connect", "open to: " + P.get("open_to", ""), "".join(o))


def button(label, color):
    w = int(measure(label, "interb", 15) + 48)
    h = 44
    o = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{h/2-1}" fill="{PANEL}" stroke="{color}" stroke-opacity=".75" stroke-width="1.5"/>' + text(24, 28, label, "interb", 15, FG)
    return svg(w, h, label, "", o, bg="none", rx=h / 2), w


def footer(P):
    W, H = 1000, 70
    p = f"{P['github_username']}@github:~$ keep building"
    o = f'<path d="M60,1 H940" stroke="{LINE}"/>' + text(60, 42, p, "mono", 13, A1)
    o += f'<rect x="{60+measure(p + " ", "mono", 13):.0f}" y="31" width="8" height="14" fill="{A1}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>'
    return svg(W, H, "keep building", "", o)
