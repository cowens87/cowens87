"""Every section of the profile, drawn from profile.yml values."""
from lib import *


# ------------------------------------------------------------------ header
def hero(P):
    W, H = 1000, 330
    first, last = P["first_name"].upper(), P["last_name"].upper()
    o = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>',
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="url(#grid)"/>',
         f'<path d="M0,32 H{W}" stroke="{LINE}"/>']
    for i, c in enumerate(["#E5534B", "#C69026", "#57AB5A"]):
        o.append(f'<circle cx="{22+i*16}" cy="16" r="5" fill="{c}"/>')
    o.append(text(W / 2, 21, f"~/{P['github_username']} — README.md", "mono", 11.5, MUTE, "middle"))
    # stacked poster name with an extruded drop
    ns = min(fit(first, "disp", 112, 420, 2), fit(last, "disp", 112, 420, 2))
    y2 = 280
    y1 = y2 - ns * 1.02
    for s, y, col, sh in [(first, y1, TE, "#0A3B37"), (last, y2, CU, "#5A2A12")]:
        for k in range(1, 7):
            o.append(text(40 + k, y + k, s, "disp", ns, sh, ls=2))
        o.append(text(40, y, s, "disp", ns, col, ls=2, extra=f'stroke="{INK}" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round"'))
    rx = 540
    for i, s in enumerate(P["focus"][:4]):
        y = 130 + i * 26
        o.append(f'<rect x="{rx}" y="{y-9}" width="6" height="6" fill="{[CU, TE, LA, CU][i]}"/>')
        o.append(text(rx + 18, y, s.upper(), "monob", fit(s.upper(), "monob", 12.5, 400, 2), MUTE, ls=2))
    t1, t2 = (P["tagline"] + ["", ""])[:2]
    o.append(text(rx, 256, t1, "interb", fit(t1, "interb", 24, 420), FG))
    o.append(text(rx, 288, t2, "interb", fit(t2, "interb", 24, 420), TE))
    focus = " · ".join(P["focus"])
    return svg(W, H, f"{P['first_name']} {P['last_name']}", f"{focus}. {' '.join(P['tagline'])}", "".join(o), bg=PANEL)


# ------------------------------------------------------------------ 01 about
def about(P):
    W = 1000
    lines = wrap(P["about"], "inter", 16, 880)
    H = 90 + len(lines) * 25 + 10
    o = [section_title(40, "01", "About")]
    for i, ln in enumerate(lines):
        o.append(text(60, 90 + i * 25, ln, "inter", 16, FG, extra='opacity=".9"'))
    return svg(W, H, "01 / About", P["about"], "".join(o))


# ------------------------------------------------------------------ 02 toolkit
def toolkit(P):
    W = 1000
    rows = P["toolkit"][:8]
    n = (len(rows) + 1) // 2
    H = 82 + n * 32 + 6
    o = [section_title(40, "02", "Toolkit")]
    for i, (k, v) in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 60 + col * 450, 90 + row * 32
        o.append(text(x, y, k.upper(), "monob", fit(k.upper(), "monob", 11.5, 126, 1.4), CU, ls=1.4))
        o.append(text(x + 136, y, v, "inter", fit(v, "inter", 14, 300), FG))
    desc = "; ".join(f"{k}: {v}" for k, v in rows)
    return svg(W, H, "02 / Toolkit", desc, "".join(o))


# ------------------------------------------------------------------ 03 AI engineering
def ai(P):
    W, H = 1000, 250
    o = [section_title(40, "03", "AI engineering", P.get("ai_tools"))]
    for i, col in enumerate(P["ai_engineering"][:3]):
        x, c = 60 + i * 300, ACCENTS[(i + 1) % 3] if False else [TE, CU, LA][i]
        o.append(f'<rect x="{x}" y="76" width="280" height="150" rx="10" fill="{PANEL}" stroke="{LINE}"/><rect x="{x}" y="76" width="280" height="3" rx="1.5" fill="{c}"/>')
        o.append(text(x + 20, 112, col["title"], "interb", fit(col["title"], "interb", 15, 244), FG))
        for j, it in enumerate(col["items"][:3]):
            o.append(text(x + 20, 144 + j * 26, "›", "monob", 14, c) + text(x + 36, 144 + j * 26, it, "inter", fit(it, "inter", 13.5, 224), MUTE))
    desc = (P.get("ai_tools", "") + ". " + "; ".join(f"{c['title']}: {', '.join(c['items'])}" for c in P["ai_engineering"]))
    return svg(W, H, "03 / AI engineering", desc, "".join(o))


# ------------------------------------------------------------------ 04 builds
def builds_header(P):
    return svg(1000, 64, "04 / Featured builds", "", section_title(40, "04", "Featured builds"))


def build_card(b, i):
    W, H = 300, 96
    c = [TE, LA, CU][i % 3]
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
    return svg(W, H, b["name"], b["description"], "".join(o), bg=BG, rx=10)


# ------------------------------------------------------------------ 05 exploring
def exploring(P):
    W = 1000
    o = [section_title(40, "05", "Currently exploring", P.get("exploring_note", "updated quarterly"))]
    x, y = 60, 76
    for i, it in enumerate(P["exploring"]):
        s = "> " + it
        w = measure(s, "mono", 12) + 22
        if x + w > 940:
            x, y = 60, y + 36
        o.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="26" rx="13" fill="none" stroke="{[TE, CU, LA][i % 3]}" stroke-opacity=".6"/>' + text(x + 11, y + 17.5, s, "mono", 12, FG))
        x += w + 8
    H = y + 26 + 24
    return svg(W, H, "05 / Currently exploring", ", ".join(P["exploring"]), "".join(o))


# ------------------------------------------------------------------ 06 activity
LEVELS = ["#1C252E", "#1E4A47", "#2C6F69", "#3E9188", "#4FB3A9"]
LANG_COLORS = [TE, CU, LA, GOLD, "#6B7A88", "#3E9188"]


def activity(P, data=None):
    """data = {"weeks": [[count]*7]*53, "total": int, "languages": [(name, share 0-1)]} or None for a placeholder."""
    W, H = 1000, 270
    o = [section_title(40, "06", "Activity", "live from GitHub · updated daily")]
    cell, gap = 13, 3.6
    weeks = (data or {}).get("weeks") or [[None] * 7 for _ in range(53)]
    weeks = weeks[-53:]
    mx = max([c for w in weeks for c in w if c] or [1])
    x0 = 60 + (53 - len(weeks)) * (cell + gap)
    for ci, wk in enumerate(weeks):
        for r, cnt in enumerate(wk):
            if cnt is None and data:
                continue
            lvl = 0 if not cnt else min(4, 1 + int(3.999 * (cnt - 1) / max(mx - 1, 1)))
            o.append(f'<rect x="{x0+ci*(cell+gap):.1f}" y="{76+r*(cell+gap):.1f}" width="{cell}" height="{cell}" rx="2.5" fill="{LEVELS[lvl]}"/>')
    if data:
        o.append(text(60, 216, f"{data['total']:,} contributions in the last year", "interb", 14, FG))
        langs = data.get("languages", [])[:6]
        if langs:
            x, bw = 520, 420
            for i, (name, share) in enumerate(langs):
                w = bw * share
                o.append(f'<rect x="{x:.1f}" y="206" width="{max(w-2,1):.1f}" height="8" rx="4" fill="{LANG_COLORS[i]}"/>')
                x += w
            lx = 520
            for i, (name, share) in enumerate(langs):
                s = f"{name} {share*100:.0f}%"
                if lx + measure(s, "mono", 11) > 940:
                    break
                o.append(f'<circle cx="{lx+4}" cy="236" r="4" fill="{LANG_COLORS[i]}"/>' + text(lx + 13, 240, s, "mono", 11, MUTE))
                lx += measure(s, "mono", 11) + 30
        desc = f"Contribution calendar: {data['total']} contributions in the last year. Languages: " + ", ".join(f"{n} {s*100:.0f}%" for n, s in langs)
    else:
        o.append(text(60, 216, "Live contributions and languages appear here after the first workflow run.", "mono", 11.5, MUTE))
        desc = "Placeholder for the live contribution calendar."
    return svg(W, H, "06 / Activity", desc, "".join(o))


# ------------------------------------------------------------------ 07 connect
def connect(P):
    W, H = 1000, 96
    o = [section_title(40, "07", "Connect")]
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
    o = f'<path d="M60,1 H940" stroke="{LINE}"/>' + text(60, 42, p, "mono", 13, TE)
    o += f'<rect x="{60+measure(p + " ", "mono", 13):.0f}" y="31" width="8" height="14" fill="{TE}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>'
    return svg(W, H, "keep building", "", o)
