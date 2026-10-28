"""Sections 01-07, project cards, buttons, footer and live-data placeholders."""
import math, random
from lib import *

W = 1000
S = f'stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"'


# ================================================================== icons
def icon(kind, x, y, accent=None):
    a = accent or C["sage"]
    g = f'<g transform="translate({x},{y})">'
    f = lambda col: f'fill="{col}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"'
    if kind == "layers":
        return g + f'<path d="M-16,8 L0,16 L16,8" {S}/><path d="M-16,2 L0,10 L16,2" {S}/><path d="M0,-13 L17,-4 L0,5 L-17,-4Z" {f(a)}/></g>'
    if kind == "cloud":
        return g + f'<path d="M-12,11 q-11,0 -11,-10 q0,-10 11,-10 q3,-11 15,-10 q12,0 14,11 q10,1 10,10 q0,9 -10,9 Z" {f(a)}/></g>'
    if kind == "spark":
        return g + f'<path d="M0,-16 C2,-5 5,-2 16,0 C5,2 2,5 0,16 C-2,5 -5,2 -16,0 C-5,-2 -2,-5 0,-16Z" {f(a)}/></g>'
    if kind == "loop":
        return g + f'<path d="M-13,-2 A13,13 0 0 1 11,-9" {S}/><path d="M11,-16 L12,-8 L4,-7" {S}/><path d="M13,2 A13,13 0 0 1 -11,9" {S}/><path d="M-11,16 L-12,8 L-4,7" {S}/><circle r="4.5" {f(a)}/></g>'
    if kind == "book":
        return g + f'<path d="M0,13 Q-9,7 -19,9 V-11 Q-9,-13 0,-7 Q9,-13 19,-11 V9 Q9,7 0,13Z" {f(a)}/><path d="M0,-7 V13" {S}/></g>'
    if kind == "branch":
        return g + f'<path d="M-8,-8 V9 M9,-1 Q9,8 -6,9" {S}/><circle cx="-8" cy="-12" r="4.5" {f(C["ivory"])}/><circle cx="-8" cy="13" r="4.5" {f(C["ivory"])}/><circle cx="9" cy="-5" r="4.5" {f(a)}/></g>'
    if kind == "agent":
        return g + f'<path d="M0,-10 V-15" {S}/><circle cx="0" cy="-16" r="3" {f(C["terra"])}/><rect x="-13" y="-10" width="26" height="20" rx="6" {f(a)}/><circle cx="-5" cy="0" r="2.4" fill="{INK}"/><circle cx="5" cy="0" r="2.4" fill="{INK}"/></g>'
    if kind == "chat":
        return g + f'<path d="M-16,-12 h32 a3,3 0 0 1 3,3 v15 a3,3 0 0 1 -3,3 h-18 l-9,7 v-7 h-5 a3,3 0 0 1 -3,-3 v-15 a3,3 0 0 1 3,-3Z" {f(a)}/><path d="M-8,-3 h16 M-8,3 h10" {S}/></g>'
    if kind == "people":
        return g + f'<path d="M-17,13 q0,-11 10,-11 q10,0 10,11 M0,13 q0,-11 9,-11 q10,0 10,11" {f(a)}/><circle cx="-7" cy="-7" r="5.5" {f(C["peach"])}/><circle cx="9" cy="-7" r="5.5" {f(C["peach"])}/></g>'
    if kind == "magnifier":
        return g + f'<path d="M8,8 L17,17" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="-2" cy="-2" r="12" {f(a)}/><path d="M-8,-6 q3,-4 8,-3" stroke="{C["ivory"]}" stroke-width="2.4" fill="none" stroke-linecap="round"/></g>'
    if kind == "blocks":
        return g + f'<rect x="-17" y="1" width="16" height="15" {f(C["peach"])}/><rect x="1" y="1" width="16" height="15" {f(a)}/><rect x="-8" y="-15" width="16" height="16" {f(C["gold"])}/></g>'
    if kind == "nodes":
        return g + f'<path d="M-12,8 L0,-9 L12,8 Z" {S}/><circle cx="-12" cy="8" r="6.5" {f(C["terra"])}/><circle cx="12" cy="8" r="6.5" {f(a)}/><circle cx="0" cy="-9" r="6.5" {f(C["gold"])}/></g>'
    if kind == "code":
        return g + f'<path d="M-6,-8 l-9,8 l9,8 M6,-8 l9,8 l-9,8 M3,-12 l-6,24" {S}/></g>'
    if kind == "case":
        return g + f'<path d="M-6,-8 v-4 a2,2 0 0 1 2,-2 h8 a2,2 0 0 1 2,2 v4" {S}/><rect x="-15" y="-8" width="30" height="20" rx="3" {f(a)}/><path d="M-15,1 h30" {S}/></g>'
    if kind == "mail":
        return g + f'<rect x="-15" y="-10" width="30" height="21" rx="3" {f(a)}/><path d="M-14,-8 l14,10 l14,-10" {S}/></g>'
    if kind == "globe":
        return g + f'<circle r="14" {f(a)}/><path d="M-14,0 h28 M0,-14 q-9,14 0,28 q9,-14 0,-28" {S}/></g>'
    return ""


def tile(x, y, kind, fill, size=52, accent=None):
    return panel(x - size / 2, y - size / 2, size, size, fill, 10, 4) + icon(kind, x, y, accent)


# ================================================================== 01 whoami
def whoami(P):
    H = 420
    name = f"{P['first_name']} {P['last_name']}"
    o = [svg_open(W, H, f"01 / whoami — {name}, {P['title']}", f"Terminal: whoami returns {name}, {P['title']}. {P['intro']}")]
    o.append(card(W, H))
    o.append(heading(40, 58, "01", "whoami"))
    tx, ty, tw, th = 40, 92, 548, 286
    o.append(panel(tx, ty, tw, th, C["term"], 14, 7))
    o.append(f'<path d="M{tx+1.5},{ty+30} H{tx+tw-1.5}" stroke="{INK}" stroke-width="{LW}"/>')
    for i, col in enumerate([C["terra"], C["gold"], C["sage"]]):
        o.append(f'<circle cx="{tx+20+i*17}" cy="{ty+15}" r="5" fill="{col}" stroke="{INK}" stroke-width="1.6"/>')
    user = P["github_username"]
    o.append(text(tx + tw / 2, ty + 20, f"{user} — zsh", "mono", 10.5, "#8FA3A0", "middle"))
    prompt = f"{user}@github:~$ "
    fs = fit(prompt + "cat focus.txt", "mono", 13.5, tw - 50)
    pw = measure(prompt, "monob", fs)
    rows = [("cmd", "whoami"), ("out", "> " + name), ("out", "> " + P["title"]),
            ("out", "> " + " | ".join(P["roles"])),
            ("gap", ""), ("cmd", "cat focus.txt"), ("dim", "> reliable platforms · intelligent automation"),
            ("dim", "> developer productivity · AI in the loop"), ("gap", ""), ("cursor", "")]
    y = ty + 62
    for kind, s in rows:
        if kind == "gap":
            y += 8
            continue
        if kind in ("cmd", "cursor"):
            o.append(text(tx + 24, y, prompt, "monob", fs, C["gold"]))
            if kind == "cmd":
                o.append(text(tx + 24 + pw, y, s, "mono", fs, C["paper"]))
            else:
                o.append(f'<rect x="{tx+26+pw:.1f}" y="{y-12}" width="9" height="16" fill="{C["termgreen"]}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
        else:
            o.append(text(tx + 24, y, s, "mono", fit(s, "mono", fs, tw - 48), C["termgreen"] if kind == "out" else "#C9D8C3"))
        y += 22
    ix = 628
    o.append(text(ix, 120, "hello, world —", "mark", 27, C["terra"]))
    p, n = para(ix, 154, P["intro"], "sans", 14.5, INK, 330, 22, maxlines=7)
    o.append(p)
    dy = 154 + n * 22 + 30
    for i, (k, lab, col) in enumerate([("magnifier", "curiosity", C["peachlt"]), ("blocks", "building", C["sagelt"]),
                                       ("book", "learning", C["goldlt"]), ("nodes", "together", C["teallt"])]):
        x = ix + 28 + i * 86
        o.append(tile(x, dy + 8, k, col, 54, C["sage"]))
        o.append(text(x + 2, dy + 62, lab, "mark", 15, INK, "middle"))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== 02 at a glance
GLANCE = [("layers", "Platform & infrastructure", "Paved roads that make shipping safe, fast and a little boring.", C["sage"]),
          ("cloud", "Cloud-native", "Containers, Kubernetes, GitOps and infrastructure as code.", C["peach"]),
          ("spark", "AI-assisted development", "Claude Code, Copilot and agents as everyday teammates.", C["gold"]),
          ("loop", "Intelligent automation", "Workflows that quietly handle the toil.", C["terra"]),
          ("book", "Continuous learning", "Labs, notes and experiments, shared in public.", C["sage"]),
          ("branch", "Open-source collaboration", "Building with, and for, the community.", C["peach"])]


def glance(P):
    H = 440
    o = [svg_open(W, H, "02 / at a glance", "; ".join(g[1] for g in GLANCE) + ". Quote: " + P["quote"])]
    o.append(card(W, H))
    o.append(heading(40, 58, "02", "at a glance", C["forest"]))
    for i, (ic, t, d, acc) in enumerate(GLANCE):
        col, row = i % 2, i // 2
        x, y = 40 + col * 292, 96 + row * 104
        o.append(panel(x, y, 272, 92, C["paper"], 12, 5))
        o.append(f'<circle cx="{x+38}" cy="{y+46}" r="25" fill="{C["ivory"]}" stroke="{INK}" stroke-width="{LW2}"/>')
        o.append(icon(ic, x + 38, y + 46, acc))
        o.append(text(x + 74, y + 29, t, "sansb", fit(t, "sansb", 14.5, 186), INK))
        p, _ = para(x + 74, y + 48, d, "sans", 12, INK, 182, 15.5, maxlines=3, extra='opacity=".8"')
        o.append(p)
    qx, qy, qw, qh = 640, 96, 318, 300
    o.append(panel(qx, qy, qw, qh, C["forest"], 16, 7))
    o.append(f'<clipPath id="q"><rect x="{qx}" y="{qy}" width="{qw}" height="{qh}" rx="16"/></clipPath>')
    o.append(f'<g clip-path="url(#q)"><rect x="{qx}" y="{qy}" width="{qw}" height="{qh}" fill="url(#dotsL)" opacity=".07"/>'
             + skyline(qx - 10, qx + qw + 10, qy + qh + 2, seed=5, fills=["#2F6150", "#1C3A30", "#3C6B52"], hmin=26, hmax=64, lw=1.8, lit=0.25) + "</g>")
    o.append(f'<rect x="{qx}" y="{qy}" width="{qw}" height="{qh}" rx="16" fill="none" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(text(qx + 26, qy + 72, "“", "disp", 80, C["gold"]))
    qs = 27
    lines = wrap(P["quote"], "mark", qs, qw - 56)
    while len(lines) > 4 and qs > 16:
        qs -= 1
        lines = wrap(P["quote"], "mark", qs, qw - 56)
    for i, ln in enumerate(lines):
        o.append(text(qx + 28, qy + 104 + i * qs * 1.32, ln, "mark", qs, C["ivory"]))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== 03 toolbox
KNOWN = {
    "aws": ("aws", "#FF9900", INK), "kubernetes": ("k8s", "#326CE5", "#fff"), "terraform": ("tf", "#7B42BC", "#fff"),
    "docker": ("dkr", "#2496ED", "#fff"), "argo cd": ("argo", "#EF7B4D", "#fff"), "helm": ("helm", "#0F1689", "#fff"),
    "linux": ("lnx", "#FCC624", INK), "networking": ("net", "#5B6770", "#fff"), "ruby": ("rb", "#CC342D", "#fff"),
    "python": ("py", "#3776AB", "#fff"), "bash": ("sh", "#4EAA25", "#fff"), "github actions": ("gha", "#2088FF", "#fff"),
    "apis": ("api", "#6B7B8C", "#fff"), "ci/cd": ("ci", C["terra"], "#fff"), "scripting": ("$_", C["forest"], "#fff"),
    "claude code": ("cc", "#D97757", "#fff"), "mcp": ("mcp", INK, "#fff"), "n8n": ("n8n", "#EA4B71", "#fff"),
    "github copilot": ("cop", "#6E40C9", "#fff"), "llms": ("llm", C["forest"], "#fff"), "prompt engineering": ("pe", C["gold"], INK),
    "ai agents": ("agt", C["teal"], "#fff"), "rag": ("rag", C["wood2"], "#fff"), "prometheus": ("prom", "#E6522C", "#fff"),
    "grafana": ("graf", "#F46800", "#fff"), "opentelemetry": ("otel", "#425CC7", "#fff"), "logging": ("log", "#5B6770", "#fff"),
    "metrics": ("met", C["teal"], "#fff"), "tracing": ("trc", "#7A5C99", "#fff"), "alerting": ("alrt", C["terra"], "#fff"),
    "go": ("go", "#00ADD8", "#fff"), "typescript": ("ts", "#3178C6", "#fff"), "javascript": ("js", "#F7DF1E", INK),
    "azure": ("az", "#0078D4", "#fff"), "gcp": ("gcp", "#4285F4", "#fff"), "ansible": ("ans", "#EE0000", "#fff"),
    "jenkins": ("jen", "#D24939", "#fff"), "postgresql": ("pg", "#4169E1", "#fff"), "redis": ("rds", "#DC382D", "#fff"),
}
SUB = {"mcp": "Model Context Protocol", "rag": "Retrieval-Augmented Gen."}
COLS = [(C["sage"], C["sagelt"], "cloud"), (C["terra"], C["peachlt"], "loop"), (C["gold"], C["goldlt"], "spark"), (C["teal"], C["teallt"], "layers")]


def toolbox(P):
    H = 500
    desc = "; ".join(f"{c['title']}: " + ", ".join(c["items"]) for c in P["toolbox"])
    o = [svg_open(W, H, "03 / engineering toolbox", desc)]
    o.append(card(W, H))
    o.append(heading(40, 58, "03", "engineering toolbox", C["gold"], "tools I reach for, daily", 955))
    pw, gap = 214, 18
    for i, colcfg in enumerate(P["toolbox"][:4]):
        acc, bg, ic = COLS[i]
        x, y = 40 + i * (pw + gap), 92
        o.append(panel(x, y, pw, 366, bg, 14, 6))
        o.append(f'<path d="M{x+1.5},{y+70} H{x+pw-1.5}" stroke="{INK}" stroke-width="{LW}"/>')
        o.append(f'<path d="M{x+14},{y+1.5} H{x+pw-14} a12.5,12.5 0 0 1 12.5,12.5 V{y+68.5} H{x+1.5} V{y+14} a12.5,12.5 0 0 1 12.5,-12.5Z" fill="{acc}"/>')
        o.append(f'<rect x="{x}" y="{y}" width="{pw}" height="366" rx="14" fill="none" stroke="{INK}" stroke-width="{LW}"/>')
        o.append(f'<path d="M{x},{y+70} H{x+pw}" stroke="{INK}" stroke-width="{LW}"/>')
        o.append(f'<circle cx="{x+32}" cy="{y+35}" r="20" fill="{C["ivory"]}" stroke="{INK}" stroke-width="{LW2}"/>' + icon(ic, x + 32, y + 35, bg))
        words = colcfg["title"].upper().split()
        # two-line title, split near the middle
        best = min(range(1, len(words) + 1), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:])))) if len(words) > 1 else 1
        t1, t2 = " ".join(words[:best]), " ".join(words[best:])
        tsz = min(fit(t1, "disp", 18, pw - 74, 0.8), fit(t2, "disp", 18, pw - 74, 0.8) if t2 else 18)
        tc = C["ivory"] if acc in (C["terra"], C["teal"]) else INK
        o.append(text(x + 62, y + (32 if t2 else 42), t1, "disp", tsz, tc, ls=0.8))
        if t2:
            o.append(text(x + 62, y + 54, t2, "disp", tsz, tc, ls=0.8))
        for j, name in enumerate(colcfg["items"][:8]):
            ab, col, fg = KNOWN.get(name.lower(), (name.lower().replace(" ", "")[:3], acc, INK if acc == C["gold"] else "#fff"))
            ry = y + 84 + j * 34
            o.append(f'<rect x="{x+12}" y="{ry}" width="{pw-24}" height="28" rx="8" fill="{C["paper"]}" stroke="{INK}" stroke-width="1.8"/>')
            o.append(f'<rect x="{x+17}" y="{ry+4}" width="32" height="20" rx="5" fill="{col}" stroke="{INK}" stroke-width="1.6"/>')
            o.append(text(x + 33, ry + 18, ab, "monob", 8.5 if len(ab) > 3 else 9.5, fg, "middle"))
            if name.lower() in SUB:
                o.append(text(x + 57, ry + 13, name, "sansb", 12, INK))
                o.append(text(x + 57, ry + 23.5, SUB[name.lower()], "sans", 8.3, INK, extra='opacity=".7"'))
            else:
                o.append(text(x + 57, ry + 18.5, name, "sansb", fit(name, "sansb", 12.5, pw - 80), INK))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== 04 project scenes
def ground(y, x0=0, x1=480, fill=None):
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="60" fill="{fill or C["concrete"]}" stroke="{INK}" stroke-width="{LW}"/>'


def scene_construction():
    o = [f'<rect x="0" y="0" width="480" height="200" fill="{C["sky"]}"/>',
         f'<circle cx="388" cy="52" r="26" fill="{C["gold"]}" stroke="{INK}" stroke-width="{LW}"/><circle cx="388" cy="52" r="26" fill="url(#dots)" opacity=".2"/>',
         f'<g opacity=".95">{skyline(-6, 96, 150, seed=4, fills=[C["concrete"], C["peachlt"]], hmin=30, hmax=74, lw=1.8, lit=.15)}</g>',
         f'<g opacity=".95">{skyline(330, 490, 150, seed=9, fills=[C["concrete"], C["sagelt"]], hmin=30, hmax=70, lw=1.8, lit=.15)}</g>']
    floors = [("vpc · subnets · iam", C["forest"], C["ivory"]), ("eks · rds · s3", C["sage"], INK), ("alb · dns", C["gold"], INK), ("app", C["terra"], C["ivory"])]
    bx, bw = 110, 132
    for k, (lab, col, fg) in enumerate(floors):
        y = 150 - (k + 1) * 22
        o.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="22" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>')
        o.append(text(bx + bw / 2, y + 15, lab, "monob", 9, fg, "middle"))
    # girders above
    top = 150 - 4 * 22
    for k in range(2):
        y0 = top - (k + 1) * 20
        o.append(f'<rect x="{bx}" y="{y0}" width="{bw}" height="20" fill="none" stroke="{C["terra"]}" stroke-width="3"/>')
        for c in range(4):
            xx = bx + c * bw / 4
            o.append(f'<path d="M{xx},{y0+20} L{xx+bw/4},{y0}" stroke="{C["terra"]}" stroke-width="2"/>')
        o.append(f'<rect x="{bx}" y="{y0}" width="{bw}" height="20" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    # crane
    cx = 330
    o.append(f'<rect x="{cx-6}" y="22" width="12" height="128" fill="{C["gold"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    for yy in range(26, 146, 12):
        o.append(f'<path d="M{cx-6},{yy} L{cx+6},{yy+12}" stroke="{INK}" stroke-width="1.2"/>')
    o.append(f'<rect x="{cx-120}" y="18" width="160" height="10" fill="{C["gold"]}" stroke="{INK}" stroke-width="{LW2}"/>'
             f'<rect x="{cx+18}" y="28" width="20" height="16" fill="{C["steel"]}" stroke="{INK}" stroke-width="{LW2}"/>'
             f'<path d="M{cx-44},28 V70" stroke="{INK}" stroke-width="1.6"/>'
             f'<rect x="{cx-64}" y="70" width="40" height="18" fill="{C["peach"]}" stroke="{INK}" stroke-width="{LW2}"/>' + text(cx - 44, 83, "ai", "monob", 10, INK, "middle"))
    o.append(ground(150))
    o.append(f'<path d="M0,162 H480" stroke="{INK}" stroke-width="1.4" stroke-dasharray="14 10"/>')
    for x in (60, 120, 400):
        o.append(f'<path d="M{x-7},150 L{x},134 L{x+7},150Z" fill="{C["terra"]}" stroke="{INK}" stroke-width="1.6"/><path d="M{x-4},144 h8" stroke="{C["ivory"]}" stroke-width="2"/>')
    return "".join(o)


def scene_rooftop():
    o = [f'<rect x="0" y="0" width="480" height="200" fill="{C["peachlt"]}"/>',
         f'<g opacity=".95">{skyline(-6, 490, 120, seed=14, fills=[C["concrete"], C["sky"], C["sagelt"]], hmin=24, hmax=70, lw=1.6, lit=.1)}</g>']
    # brownstone
    o.append(f'<rect x="96" y="104" width="288" height="100" fill="{C["brick"]}" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(f'<rect x="88" y="96" width="304" height="12" fill="{C["concrete"]}" stroke="{INK}" stroke-width="{LW}"/>')
    for wx in range(118, 370, 52):
        o.append(f'<rect x="{wx}" y="124" width="26" height="34" fill="{C["gold"] if wx % 3 else C["ivory"]}" stroke="{INK}" stroke-width="{LW2}"/><path d="M{wx+13},124 v34 M{wx},141 h26" stroke="{INK}" stroke-width="1.4"/>')
    o.append(f'<rect x="96" y="104" width="288" height="100" fill="url(#hatch)" opacity=".12"/>')
    # greenhouse
    gx, gy = 240, 96
    o.append(f'<path d="M{gx-64},{gy} V{gy-40} L{gx},{gy-78} L{gx+64},{gy-40} V{gy}Z" fill="{C["sagelt"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    for dx in (-32, 0, 32):
        o.append(f'<path d="M{gx+dx},{gy} V{gy-40-38*(1-abs(dx)/64):.1f}" stroke="{INK}" stroke-width="1.8"/>')
    o.append(f'<path d="M{gx-64},{gy-40} H{gx+64}" stroke="{INK}" stroke-width="1.8"/>')
    for sx in (gx - 48, gx - 16, gx + 16, gx + 48):
        o.append(leaf(sx, gy - 2, 18, 10, -30, C["forest"], 1.6, False) + leaf(sx, gy - 2, 18, 10, 30, C["sage"], 1.6, False))
    # antenna + signal
    ax = 350
    o.append(f'<path d="M{ax},96 V40 M{ax-12},96 L{ax},60 L{ax+12},96" stroke="{INK}" stroke-width="{LW2}" fill="none"/><circle cx="{ax}" cy="38" r="5" fill="{C["terra"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    for r in (14, 24, 34):
        o.append(f'<path d="M{ax+r*0.7:.1f},{38-r*0.7:.1f} A{r},{r} 0 0 1 {ax+r*0.7:.1f},{38+r*0.7:.1f}" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    # constellation of agents
    nodes = [(54, 34), (100, 22), (92, 64), (424, 30), (452, 66)]
    for a, b in [(0, 1), (1, 2), (0, 2), (3, 4)]:
        o.append(f'<path d="M{nodes[a][0]},{nodes[a][1]} L{nodes[b][0]},{nodes[b][1]}" stroke="{INK}" stroke-width="1.6" stroke-dasharray="3 3"/>')
    for i, (x, y) in enumerate(nodes):
        o.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{[C["terra"], C["gold"], C["forest"]][i % 3]}" stroke="{INK}" stroke-width="{LW2}"/>')
    o.append(panel(134, 40, 60, 22, INK, 6, 0) + f'<path d="M150,62 l-4,9 l11,-9Z" fill="{INK}"/>' + text(164, 55, "mcp://", "monob", 9, C["termgreen"], "middle"))
    return "".join(o)


def scene_workshop():
    o = [f'<rect x="0" y="0" width="480" height="200" fill="{C["goldlt"]}"/>']
    o.append(f'<rect x="40" y="10" width="400" height="160" fill="{C["forest"]}" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(f'<rect x="40" y="10" width="400" height="160" fill="url(#dotsL)" opacity=".08"/>')
    # sign
    o.append(panel(150, 20, 180, 30, C["ivory"], 4, 4) + text(240, 43, "THE TOOLKIT", "disp", 22, INK, "middle", ls=2))
    # awning
    aw = 400 / 10
    for k in range(10):
        col = C["terra"] if k % 2 == 0 else C["ivory"]
        x = 40 + k * aw
        o.append(f'<path d="M{x},60 H{x+aw} V80 Q{x+aw/2},92 {x},80Z" fill="{col}" stroke="{INK}" stroke-width="{LW2}" stroke-linejoin="round"/>')
    o.append(f'<rect x="36" y="56" width="408" height="8" fill="{C["steel"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    # window
    o.append(f'<rect x="60" y="94" width="250" height="70" fill="{C["sky"]}" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(f'<rect x="72" y="104" width="226" height="50" fill="{C["peach"]}" stroke="{INK}" stroke-width="1.6"/>')
    for x in range(80, 296, 12):
        for y in range(110, 152, 12):
            o.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{INK}" opacity=".4"/>')

    def gear(cx, cy, r, n, fill):
        pts = []
        for i in range(n * 2):
            a = math.pi * i / n
            rr = r if i % 2 == 0 else r * 0.76
            for da in (-0.2, 0.2):
                pts.append(f"{cx+math.cos(a+da*3/n)*rr:.1f},{cy+math.sin(a+da*3/n)*rr:.1f}")
        return (f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="{LW2}" stroke-linejoin="round"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{r*0.3:.1f}" fill="{C["ivory"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    o.append(gear(150, 128, 20, 9, C["gold"]) + gear(184, 142, 12, 7, C["sage"]))
    o.append(f'<g transform="translate(102,128) rotate(-35)"><rect x="-4.5" y="-20" width="9" height="38" rx="3" fill="{C["teal"]}" stroke="{INK}" stroke-width="{LW2}"/>'
             f'<path d="M-11,-28 a11,11 0 1,0 22,0 l-6,0 l0,7 l-10,0 l0,-7Z" fill="{C["teal"]}" stroke="{INK}" stroke-width="{LW2}"/></g>')
    o.append(panel(222, 112, 58, 34, C["term"], 4, 3) + text(230, 134, ">_ ship", "monob", 10, C["termgreen"]))
    # door
    o.append(f'<rect x="336" y="94" width="76" height="76" fill="{C["terra"]}" stroke="{INK}" stroke-width="{LW}"/>'
             f'<rect x="348" y="104" width="52" height="30" fill="{C["sky"]}" stroke="{INK}" stroke-width="{LW2}"/>'
             f'<circle cx="402" cy="148" r="3.5" fill="{C["gold"]}" stroke="{INK}" stroke-width="1.4"/>'
             f'<rect x="354" y="110" width="40" height="16" rx="3" fill="{C["ivory"]}" stroke="{INK}" stroke-width="1.4"/>' + text(374, 122, "OPEN", "disp", 11, C["terra"], "middle", ls=1))
    o.append(ground(170))
    o.append(pot(452, 150, 22, 20, C["terra"]) + leaf(452, 148, 22, 11, -18, C["sage"], 1.6) + leaf(452, 148, 22, 11, 22, C["forest"], 1.6))
    return "".join(o)


def scene_library():
    o = [f'<rect x="0" y="0" width="480" height="200" fill="{C["teallt"]}"/>',
         f'<circle cx="84" cy="44" r="20" fill="{C["peach"]}" stroke="{INK}" stroke-width="{LW}"/>']
    # pop-up city rising out of the book
    o.append(skyline(130, 352, 132, seed=33, fills=[C["terra"], C["sage"], C["gold"], C["steel"], C["peach"]], hmin=36, hmax=96, lw=LW2, lit=.4))
    # open book
    o.append(f'<path d="M240,150 Q180,122 92,132 V166 H388 V132 Q300,122 240,150Z" fill="{C["paper"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    o.append(f'<path d="M92,166 Q170,156 240,172 Q310,156 388,166 V178 H92Z" fill="{C["forest"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    o.append(f'<path d="M240,150 V172" stroke="{INK}" stroke-width="{LW2}"/>')
    for k in range(3):
        o.append(f'<path d="M{110+k*8},{140+k*6} q50,-8 110,4" stroke="{INK}" stroke-width="1.3" fill="none" opacity=".5"/>'
                 f'<path d="M260,{144+k*6} q50,-12 {110-k*8},-4" stroke="{INK}" stroke-width="1.3" fill="none" opacity=".5"/>')
    # transit sign
    o.append(f'<path d="M420,176 V96" stroke="{INK}" stroke-width="5"/><path d="M420,176 V96" stroke="{C["steel"]}" stroke-width="2"/>')
    o.append(panel(380, 66, 80, 32, C["forest"], 6, 4) + bullet(396, 82, "L", C["gold"], 10, INK, 12) + text(412, 87, "NOTES", "disp", 14, C["ivory"], ls=1))
    o.append(f'<path d="M0,178 H480" stroke="{INK}" stroke-width="{LW}"/>')
    for (x, y) in [(176, 36), (194, 46)]:
        o.append(f'<path d="M{x-7},{y} q7,-6 7,0 q0,-6 7,0" stroke="{INK}" stroke-width="2" fill="none"/>')
    return "".join(o)


SCENES = {"construction": scene_construction, "rooftop": scene_rooftop, "workshop": scene_workshop, "library": scene_library}
CARD_ACC = [C["forest"], C["terra"], C["gold"], C["teal"]]


def project_card(P, i):
    pr = P["projects"][i]
    name, desc, tags = pr["repo"], pr["description"], pr.get("tags", [])
    scene = SCENES.get(pr.get("scene", ""), list(SCENES.values())[i % 4])
    acc = CARD_ACC[i % 4]
    w, h = 490, 328
    o = [svg_open(w, h, f"{name} — repository", f"{desc} Tags: {', '.join(tags)}.")]
    o.append(card(w, h, C["paper"], 18, 7))
    o.append(f'<clipPath id="win"><rect x="16" y="16" width="448" height="160" rx="12"/></clipPath>')
    o.append(f'<g clip-path="url(#win)"><svg x="16" y="16" width="448" height="160" viewBox="0 0 480 172" preserveAspectRatio="xMidYMax slice">{scene()}</svg></g>')
    o.append(f'<rect x="16" y="16" width="448" height="160" rx="12" fill="none" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(icon("branch", 34, 206, C["peach"]).replace("translate(34,206)", "translate(34,206) scale(.8)"))
    o.append(text(54, 213, name, "monob", fit(name, "monob", 19, 340), acc if acc != C["gold"] else "#8A6215"))
    p, n = para(28, 240, desc, "sans", 13.5, INK, 410, 19, maxlines=2, extra='opacity=".85"')
    o.append(p)
    x = 28
    for t in tags[:4]:
        c, cw = chip(x, 272, t, C["ivory"], INK, "monob", 10, 9, 22)
        if x + cw > 410:
            break
        o.append(c)
        x += cw + 8
    o.append(arrow_btn(440, 283, 17, acc))
    o.append("</svg>")
    return "\n".join(o)


def projects_header(P):
    H = 92
    o = [svg_open(W, H, "04 / featured projects", "")]
    o.append(card(W, H, sh=6))
    o.append(heading(40, 54, "04", "featured projects", C["teal"], "a few things on the workbench", 955))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== 05 roadmap as a transit line
def roadmap(P):
    H = 360
    steps = P["roadmap"][:5]
    o = [svg_open(W, H, "05 / currently building & learning", "Stops: " + "; ".join(f"{i+1}. {s}" for i, s in enumerate(steps)) + ". Always a work in progress.")]
    o.append(card(W, H, grid=True))
    o.append(heading(40, 58, "05", "currently building & learning", C["terra"]))
    o.append(text(955, 64, "Always a work in progress.", "mark", 22, C["terra"], "end"))
    xs = [110, 300, 490, 680, 870]
    ys = [200, 200, 200, 200, 200]
    pts = [(46, 250), (80, 250), (110, 220), (110, 200)] + [(x, 200) for x in xs[1:]] + [(900, 200), (930, 170), (958, 170)]
    o.append(transit([(46, 200), (870, 200), (900, 170), (938, 170)], C["terra"], 10))
    accents = [C["forest"], C["terra"], C["gold"], C["teal"], C["forest"]]
    for k, s in enumerate(steps):
        x, y = xs[k], ys[k]
        o.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{C["ivory"]}" stroke="{INK}" stroke-width="{LW}"/><circle cx="{x}" cy="{y}" r="6" fill="{INK}"/>')
        up = k % 2 == 1
        o.append(bullet(x, y - 46 if up else y + 46, str(k + 1), accents[k], 16, size=18))
        o.append(f'<path d="M{x},{y - 15 if up else y + 15} V{y - 30 if up else y + 30}" stroke="{INK}" stroke-width="{LW2}"/>')
        lines = wrap(s, "sansb", 13.5, 168)[:3]
        if up:
            base = y - 76 - (len(lines) - 1) * 18
        else:
            base = y + 86
        for j, ln in enumerate(lines):
            o.append(text(x, base + j * 18, ln, "sansb", 13.5, INK, "middle"))
    # end-of-line marker
    o.append(f'<rect x="938" y="150" width="20" height="40" rx="3" fill="{C["gold"]}" stroke="{INK}" stroke-width="{LW2}"/>' + text(948, 176, "→", "monob", 14, INK, "middle"))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== 06 activity
def activity(P):
    H = 160
    o = [svg_open(W, H, "06 / github activity", "Live GitHub activity follows: contribution calendar, repository stats and language mix.")]
    o.append(card(W, H))
    o.append(heading(40, 58, "06", "github activity", C["sage"], "live from GitHub", 955))
    p, _ = para(40, 108, "Contribution calendar, repository stats and language mix — rendered live from GitHub, styled to match this page.",
                "sans", 14, INK, 560, 21, extra='opacity=".85"')
    o.append(p)
    lx = 742
    o.append(text(lx, 118, "less", "monob", 10, INK, "end"))
    for i, col in enumerate(["#EFE3CC", "#CFDCC6", C["sage"], "#5E8270", C["forest"]]):
        o.append(f'<rect x="{lx+8+i*20}" y="104" width="16" height="16" rx="3" fill="{col}" stroke="{INK}" stroke-width="1.6"/>')
    o.append(text(lx + 8 + 5 * 20 + 4, 118, "more", "monob", 10, INK))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== 07 connect
def connect(P):
    H = 250
    o = [svg_open(W, H, "07 / connect — Let's build something meaningful.", "Contact links follow.")]
    o.append(card(W, H))
    o.append(f'<clipPath id="cc"><rect x="1.5" y="1.5" width="{W-10-1.5}" height="{H-10-1.5}" rx="18"/></clipPath>')
    o.append(f'<g clip-path="url(#cc)">{skyline(-10, W, H - 10, seed=77, fills=[C["sagelt"], C["peachlt"], C["concrete"], C["goldlt"]], hmin=24, hmax=70, lw=LW2, lit=.15)}</g>')
    o.append(f'<path d="M1.5,{H-10} H{W-10}" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(heading(40, 58, "07", "connect", C["forest"]))
    msg = "Let’s build something meaningful."
    o.append(f'<rect x="{(W-7)/2 - 330}" y="86" width="660" height="70" rx="10" fill="{C["ivory"]}"/>')
    o.append(text((W - 7) / 2 + 3, 136 + 3, msg, "mark", 40, INK, "middle"))
    o.append(text((W - 7) / 2, 136, msg, "mark", 40, C["terra"], "middle"))
    o.append("</svg>")
    return "\n".join(o)


def button(kind, label, sub):
    w, h = 310, 74
    o = [svg_open(w, h, f"{label}: {sub}", "")]
    o.append(card(w, h, C["paper"], 14, 5))
    o.append(f'<circle cx="38" cy="34" r="21" fill="{C["ivory"]}" stroke="{INK}" stroke-width="{LW2}"/>' + icon(kind, 38, 34, C["peach"]))
    o.append(text(70, 28, label, "monob", 10.5, C["terra"], ls=2))
    o.append(text(70, 47, sub, "sansb", fit(sub, "sansb", 14, 180), INK))
    o.append(arrow_btn(270, 33, 13, C["forest"]))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== footer
def footer(P):
    H = 170
    o = [svg_open(W, H, f"{P['github_username']}@github:~$ keep building", P["footer"])]
    o.append(card(W, H, C["term"]))
    o.append(f'<clipPath id="ff"><rect x="1.5" y="1.5" width="{W-11.5}" height="{H-11.5}" rx="18"/></clipPath>')
    o.append(f'<g clip-path="url(#ff)" opacity=".55">{skyline(-10, W, 46, seed=91, fills=["#24363A", "#2A3F42", "#1F3033"], hmin=14, hmax=40, lw=1.6, lit=.3)}</g>')
    o.append(f'<path d="M1.5,46 H{W-10}" stroke="#2F4447" stroke-width="2"/>')
    prompt = f"{P['github_username']}@github:~$ "
    pw = measure(prompt, "monob", 22)
    o.append(text(46, 96, prompt, "monob", 22, C["gold"]))
    o.append(text(46 + pw, 96, "keep building", "mono", 22, C["paper"]))
    cx = 46 + pw + measure("keep building ", "mono", 22)
    o.append(f'<rect x="{cx:.1f}" y="77" width="13" height="24" fill="{C["termgreen"]}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
    o.append(f'<path d="M46,118 H{W-56}" stroke="#2F4447" stroke-width="1.5"/>')
    o.append(text(46, 144, P["footer"], "monob", fit(P["footer"], "monob", 11.5, 700, 2.4), C["sage"], ls=2.4))
    o.append(text(W - 56, 144, "made with care", "mark", 15, C["peach"], "end"))
    o.append("</svg>")
    return "\n".join(o)


# ================================================================== placeholders for live data
PH = "PLACEHOLDER · LIVE DATA APPEARS AFTER THE FIRST WORKFLOW RUN"


def ph_calendar():
    w, h = 1000, 200
    o = [svg_open(w, h, "Contribution calendar placeholder", "Placeholder: replaced by the live contribution calendar when the profile workflow runs.")]
    o.append(card(w, h, C["paper"], 16, 6))
    cell, gap = 14, 3.4
    x0 = (w - 6 - (53 * cell + 52 * gap)) / 2
    for c in range(53):
        for r in range(7):
            o.append(f'<rect x="{x0+c*(cell+gap):.1f}" y="{26+r*(cell+gap):.1f}" width="{cell}" height="{cell}" rx="3" fill="#EFE3CC" stroke="{C["rule"]}" stroke-width="1"/>')
    o.append(text((w - 6) / 2, 172, PH, "monob", 10, C["terra"], "middle", ls=1.6))
    o.append("</svg>")
    return "\n".join(o)


def ph_card(title, rows=None):
    w, h = 495, 200
    o = [svg_open(w, h, f"{title} placeholder", f"Placeholder: replaced by live {title.lower()} when the profile workflow runs.")]
    o.append(card(w, h, C["paper"], 16, 6))
    o.append(text(26, 40, title, "sansb", 17, INK))
    if rows:
        for i, lab in enumerate(rows):
            y = 72 + i * 22
            o.append(f'<circle cx="32" cy="{y-4}" r="4" fill="none" stroke="{C["terra"]}" stroke-width="2"/>' + text(46, y, lab, "sans", 13, INK, extra='opacity=".8"'))
            o.append(f'<rect x="290" y="{y-11}" width="60" height="12" rx="6" fill="#EFE3CC" stroke="{C["rule"]}"/>')
        o.append(f'<circle cx="412" cy="100" r="38" fill="none" stroke="{C["rule"]}" stroke-width="7" stroke-dasharray="4 4"/>' + text(412, 106, "—", "monob", 16, INK, "middle"))
    else:
        o.append(f'<rect x="26" y="58" width="436" height="10" rx="5" fill="#EFE3CC" stroke="{C["rule"]}"/>')
        for i in range(6):
            cx, cy = 34 + (i % 2) * 220, 98 + (i // 2) * 24
            o.append(f'<circle cx="{cx}" cy="{cy-4}" r="5" fill="none" stroke="{C["sage"]}" stroke-width="2"/><rect x="{cx+12}" y="{cy-10}" width="110" height="11" rx="5.5" fill="#EFE3CC" stroke="{C["rule"]}"/>')
    o.append(text((w - 6) / 2, 180, "PLACEHOLDER · FILLED BY THE PROFILE WORKFLOW", "monob", 9.5, C["terra"], "middle", ls=1.4))
    o.append("</svg>")
    return "\n".join(o)
