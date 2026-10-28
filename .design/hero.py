"""Header: loft-window city scene with the engineer at her desk."""
import math, random
from lib import *

W, H = 1000, 660
CX = 720


def hair(cx, cy, rx, ry, seed=4):
    rnd = random.Random(seed)
    blobs = []
    n = 30
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.04, 0.04)
        r = rnd.uniform(15, 21)
        blobs.append((cx + math.cos(a) * (rx - 14), cy + math.sin(a) * (ry - 14), r))
    core = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-12}" ry="{ry-12}"'
    # outline trick: stroked silhouette underneath, flat fill on top
    out = [core + f' fill="{INK}" stroke="{INK}" stroke-width="7"/>']
    out += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{INK}" stroke="{INK}" stroke-width="7"/>' for x, y, r in blobs]
    out.append(core + f' fill="{C["hair"]}"/>')
    out += [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{C["hair"]}"/>' for x, y, r in blobs]
    for _ in range(120):
        a = rnd.uniform(0, 2 * math.pi)
        d = math.sqrt(rnd.uniform(0.05, 1)) * 0.98
        x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        r = rnd.uniform(3, 5.2)
        out.append(f'<path d="M{x-r:.1f},{y:.1f} a{r:.1f},{r:.1f} 0 1,1 {r*1.5:.1f},{r*0.8:.1f}" transform="rotate({rnd.uniform(0,360):.0f} {x:.1f} {y:.1f})" '
                   f'stroke="{C["hair2"]}" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def monstera(x, y):
    out = []
    for ang, ln in [(-96, 104), (-70, 128), (-44, 138), (-20, 112), (-118, 82), (4, 88)]:
        rad = math.radians(ang)
        ex, ey = x + math.sin(rad) * ln * 0.5, y - math.cos(rad) * ln * 0.5
        out.append(f'<path d="M{x},{y} Q{(x+ex)/2+4:.1f},{(y+ey)/2:.1f} {ex:.1f},{ey:.1f}" stroke="{INK}" stroke-width="{LW}" fill="none" stroke-linecap="round"/>')
        for k, off in enumerate([-26, -13, 0, 13, 26]):
            out.append(leaf(ex, ey, ln * 0.56 * (1 - abs(off) / 75), 17, ang + off, C["forest"] if k % 2 else "#2F6150", LW2))
    return "".join(out)


def snake_plant(x, y):
    out = []
    for i, (dx, h, lean) in enumerate([(-18, 142, -9), (-6, 176, -2), (7, 160, 5), (18, 128, 12), (-28, 100, -18), (28, 104, 18)]):
        bx, tx, ty = x + dx, x + dx + lean * 2.4, y - h
        col = C["forest"] if i % 2 else "#3C6B52"
        out.append(f'<path d="M{bx-8},{y} C{bx-9},{y-h*0.5} {tx-5},{ty+30} {tx},{ty} C{tx+5},{ty+30} {bx+9},{y-h*0.5} {bx+8},{y}Z" fill="{col}" stroke="{INK}" stroke-width="{LW2}" stroke-linejoin="round"/>')
        for b in range(4):
            yy = y - h * (0.2 + b * 0.17)
            out.append(f'<path d="M{bx-5+lean*0.45*(b+1):.1f},{yy:.1f} q5,-4 10,0" stroke="{C["sage"]}" stroke-width="2" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def view(x0, y0, x1, y1):
    """The city through the window."""
    o = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{C["sky"]}"/>']
    o.append(f'<circle cx="{x0+300}" cy="{y0+150}" r="62" fill="{C["peach"]}" stroke="{INK}" stroke-width="{LW}"/>'
             f'<circle cx="{x0+300}" cy="{y0+150}" r="62" fill="url(#dots)" opacity=".18"/>')
    # sun rays / sky bands
    for k, yy in enumerate([y0 + 60, y0 + 84, y0 + 104]):
        o.append(f'<path d="M{x0},{yy} H{x0+150-k*30}" stroke="{C["peach"]}" stroke-width="5" stroke-linecap="round"/>')
    # far skyline (lighter, thinner ink)
    o.append(f'<g opacity=".9">{skyline(x0-10, x1+10, y1-70, seed=8, fills=[C["concrete"], C["peachlt"], C["sagelt"]], hmin=50, hmax=120, lw=1.6, lit=0.15)}</g>')
    # bridge
    by = y1 - 96
    o.append(f'<path d="M{x0},{by} H{x1}" stroke="{INK}" stroke-width="{LW}"/>'
             f'<path d="M{x0},{by-4} Q{x0+60},{by-50} {x0+110},{by-62} Q{x0+170},{by-4} {x0+230},{by-62} Q{x0+260},{by-30} {x0+300},{by-6}" stroke="{C["terra"]}" stroke-width="{LW}" fill="none"/>')
    for tx in (x0 + 110, x0 + 230):
        o.append(f'<rect x="{tx-6}" y="{by-74}" width="12" height="74" fill="{C["terra"]}" stroke="{INK}" stroke-width="{LW2}"/><rect x="{tx-3}" y="{by-64}" width="6" height="10" fill="{C["sky"]}" stroke="{INK}" stroke-width="1.2"/>')
    for k in range(1, 22):
        xx = x0 + k * 14
        o.append(f'<path d="M{xx},{by} v-{8+ (abs(math.sin(k*0.55))*30):.0f}" stroke="{INK}" stroke-width=".9" opacity=".6"/>')
    # near skyline
    o.append(skyline(x0 - 6, x1 + 6, y1, seed=21, fills=[C["terra"], C["steel"], C["forest"], C["concrete"], C["brick"], C["sage"]], hmin=26, hmax=70, lw=LW2, lit=0.35))
    return "".join(o)


def build(P):
    first, last, handle = P["first_name"], P["last_name"], "@" + P["github_username"]
    o = [svg_open(W, H, f"{first} {last} — {handle}",
                  f"Illustrated header: {first} {last}, a Black woman engineer with voluminous natural curls and glasses, works at a desk "
                  "in front of a big loft window looking out on a city skyline and bridge, with plants, books, a laptop, a coffee cup reading "
                  "Automate Create Iterate Repeat, a terminal window and a transit-map style infrastructure diagram.")]
    o.append(card(W, H, C["ivory"], grid=True))

    # ---------- loft window ----------
    x0, y0, x1, y1 = 478, 44, 962, 476
    o.append(f'<clipPath id="win"><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}"/></clipPath>')
    o.append(f'<g clip-path="url(#win)">{view(x0, y0, x1, y1)}</g>')
    # steel mullions
    for gx in (x0 + (x1 - x0) / 3, x0 + 2 * (x1 - x0) / 3):
        o.append(f'<path d="M{gx:.1f},{y0} V{y1}" stroke="{C["steel"]}" stroke-width="7"/><path d="M{gx:.1f},{y0} V{y1}" stroke="{INK}" stroke-width="7" fill="none" stroke-dasharray="0" opacity=".0"/>')
        o.append(f'<path d="M{gx-3.5:.1f},{y0} V{y1} M{gx+3.5:.1f},{y0} V{y1}" stroke="{INK}" stroke-width="1.6"/>')
    for gy in (y0 + 108, y0 + 216, y0 + 324):
        o.append(f'<path d="M{x0},{gy} H{x1}" stroke="{C["steel"]}" stroke-width="6"/><path d="M{x0},{gy-3} H{x1} M{x0},{gy+3} H{x1}" stroke="{INK}" stroke-width="1.4"/>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="{INK}" stroke-width="10"/>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="{C["steel"]}" stroke-width="5"/>')
    o.append(f'<rect x="{x0-6}" y="{y0-6}" width="{x1-x0+12}" height="{y1-y0+12}" fill="none" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(f'<rect x="{x0+6}" y="{y0+6}" width="{x1-x0-12}" height="{y1-y0-12}" fill="none" stroke="{INK}" stroke-width="1.6"/>')

    # ---------- transit-map infra line across the sky ----------
    pts = [(640, 132), (700, 132), (730, 102), (860, 102), (884, 126), (884, 190)]
    o.append(transit(pts, C["gold"], 7))
    for (sx, sy, lab, dx, dy, anc) in [(700, 132, "vpc", 0, 26, "middle"), (790, 102, "eks", 0, -14, "middle"),
                                       (884, 126, "argo", -14, 5, "end"), (884, 190, "ai", -14, 5, "end")]:
        o.append(station(sx, sy, 6.5))
        lw_ = measure(lab, "monob", 10) + 10
        bx = sx - lw_ / 2 if anc == "middle" else sx + dx - lw_ + 5
        o.append(f'<rect x="{bx:.1f}" y="{sy+dy-11}" width="{lw_:.1f}" height="15" rx="3" fill="{C["ivory"]}" stroke="{INK}" stroke-width="1.6"/>')
        o.append(text(bx + lw_ / 2, sy + dy, lab, "monob", 10, INK, "middle"))

    # ---------- terminal ----------
    tx, ty, tw, th = 450, 72, 192, 128
    o.append(panel(tx, ty, tw, th, C["term"], 9, 6))
    o.append(f'<path d="M{tx+1.5},{ty+20} H{tx+tw-1.5}" stroke="{INK}" stroke-width="{LW2}"/>')
    for i, col in enumerate([C["terra"], C["gold"], C["sage"]]):
        o.append(f'<circle cx="{tx+13+i*12}" cy="{ty+10.5}" r="3.6" fill="{col}" stroke="{INK}" stroke-width="1.2"/>')
    lines = [("$ terraform apply", C["paper"]), ("+ aws_eks_cluster.core", C["termgreen"]),
             ("$ kubectl get pods -n ai", C["paper"]), ("agent-runner  1/1 Running", C["termgreen"]),
             ("$ n8n run ai-triage", C["paper"]), ("> workflow complete", C["gold"])]
    for i, (s, col) in enumerate(lines):
        o.append(text(tx + 11, ty + 38 + i * 15, s, "mono", 9.5, col))

    # ---------- figure ----------
    fig = []
    hx, hy = CX, 318
    fig.append(hair(CX, 284, 98, 82))
    # torso: bomber jacket over tee
    fig.append(f'<path d="M616,482 C616,424 646,392 694,384 L746,384 C794,392 824,424 824,482Z" fill="{C["forest"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    fig.append(f'<path d="M694,384 L720,452 L746,384Z" fill="{C["terra"]}" stroke="{INK}" stroke-width="{LW2}" stroke-linejoin="round"/>')
    fig.append(f'<path d="M686,388 L712,470 M754,388 L728,470" stroke="{INK}" stroke-width="{LW2}" fill="none"/>')
    fig.append(f'<path d="M640,482 C642,446 650,424 664,408 M800,482 C798,446 790,424 776,408" stroke="{INK}" stroke-width="{LW2}" fill="none"/>')
    fig.append(f'<path d="M772,420 h22 v14 h-22z" fill="{C["gold"]}" stroke="{INK}" stroke-width="1.6"/>')  # patch
    fig.append(f'<path d="M694,386 Q720,396 746,386" stroke="{C["sage"]}" stroke-width="7" fill="none"/><path d="M692,382 Q720,393 748,382 M694,391 Q720,401 746,391" stroke="{INK}" stroke-width="1.4" fill="none"/>')
    # neck
    fig.append(f'<path d="M703,344 L703,388 Q720,398 737,388 L737,344Z" fill="{C["skin"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    fig.append(f'<path d="M703,350 Q720,368 737,350 L737,364 Q720,378 703,364Z" fill="{C["skin2"]}"/>')
    # headphones around neck
    fig.append(f'<path d="M688,384 Q720,416 752,384" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M688,384 Q720,416 752,384" stroke="{C["steel"]}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    for ex in (684, 756):
        fig.append(f'<ellipse cx="{ex}" cy="382" rx="10" ry="13" fill="{C["terra"]}" stroke="{INK}" stroke-width="{LW}"/>')
    # ears
    for ex in (686, 754):
        fig.append(f'<ellipse cx="{ex}" cy="322" rx="7" ry="10" fill="{C["skin"]}" stroke="{INK}" stroke-width="{LW2}"/>'
                   f'<circle cx="{ex}" cy="340" r="6.5" fill="none" stroke="{INK}" stroke-width="4.5"/><circle cx="{ex}" cy="340" r="6.5" fill="none" stroke="{C["gold"]}" stroke-width="2"/>')
    # face
    fig.append(f'<ellipse cx="{hx}" cy="{hy}" rx="34" ry="42" fill="{C["skin"]}" stroke="{INK}" stroke-width="{LW}"/>')
    fig.append(f'<path d="M{hx+14},{hy-38} Q{hx+38},{hy-4} {hx+20},{hy+36} Q{hx+31},{hy+16} {hx+33},{hy} Q{hx+30},{hy-26} {hx+14},{hy-38}Z" fill="{C["skin2"]}"/>')
    # hairline
    rnd = random.Random(21)
    for i in range(15):
        a = math.radians(202 + i * (136 / 14))
        x, y = hx + math.cos(a) * 35, hy - 9 + math.sin(a) * 37
        fig.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(8,11):.1f}" fill="{C["hair"]}"/>')
    # brows
    fig.append(f'<path d="M695,300 Q705,294 714,299 M726,299 Q735,294 745,300" stroke="{INK}" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
    # eyes looking down at the laptop
    for ex in (705, 735):
        fig.append(f'<path d="M{ex-7},{317} Q{ex},{311} {ex+7},{317} Q{ex},{322} {ex-7},{317}Z" fill="{C["paper"]}"/>'
                   f'<circle cx="{ex}" cy="{318}" r="3.3" fill="{INK}"/>'
                   f'<path d="M{ex-8},{317} Q{ex},{310} {ex+8},{317}" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    # glasses
    for ex in (705, 735):
        fig.append(f'<rect x="{ex-13}" y="306" width="26" height="21" rx="9" fill="{C["paper"]}" fill-opacity=".12" stroke="{INK}" stroke-width="3.2"/>')
    fig.append(f'<path d="M718,314 Q720,311 722,314" stroke="{INK}" stroke-width="3" fill="none"/>'
               f'<path d="M692,313 L687,316 M748,313 L753,316" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>')
    fig.append(f'<path d="M722,326 Q719,334 714,338 Q719,341 726,339" stroke="{INK}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    fig.append(f'<path d="M707,348 Q714,344 720,346 Q726,344 733,348 Q720,357 707,348Z" fill="#7A3B2E" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    o.append("".join(fig))

    # ---------- desk ----------
    o.append(f'<rect x="440" y="478" width="540" height="16" rx="3" fill="{C["wood"]}" stroke="{INK}" stroke-width="{LW}"/>')
    o.append(f'<path d="M462,494 V590 M958,494 V590" stroke="{INK}" stroke-width="9"/><path d="M462,494 V590 M958,494 V590" stroke="{C["steel"]}" stroke-width="4"/>')
    o.append(f'<path d="M462,528 H958" stroke="{INK}" stroke-width="{LW}"/>')

    # skateboard under the desk
    o.append(f'<path d="M548,572 Q540,572 541,566 L543,563 H700 L702,566 Q703,572 695,572Z" fill="{C["terra"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
             f'<path d="M560,567 H684" stroke="{C["gold"]}" stroke-width="3" stroke-dasharray="10 6"/>')
    for wx in (572, 670):
        o.append(f'<rect x="{wx-8}" y="572" width="16" height="4" fill="{C["steel"]}" stroke="{INK}" stroke-width="1.6"/>'
                 f'<circle cx="{wx-6}" cy="580" r="5" fill="{C["gold"]}" stroke="{INK}" stroke-width="{LW2}"/><circle cx="{wx+6}" cy="580" r="5" fill="{C["gold"]}" stroke="{INK}" stroke-width="{LW2}"/>')

    # laptop
    o.append(f'<path d="M660,478 L664,412 Q664,404 672,404 L768,404 Q776,404 776,412 L780,478Z" fill="{C["concrete"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>'
             f'<path d="M760,410 L770,410 L774,474 L764,474Z" fill="url(#hatch)" opacity=".35"/>'
             f'<rect x="646" y="474" width="148" height="7" rx="3.5" fill="{C["steel"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    # stickers
    o.append(f'<circle cx="720" cy="438" r="13" fill="{C["forest"]}" stroke="{INK}" stroke-width="{LW2}"/>' + leaf(720, 447, 17, 9, 0, C["sage"], 1.6))
    o.append(f'<g transform="rotate(-10 692 424)"><rect x="680" y="416" width="26" height="15" rx="3" fill="{C["gold"]}" stroke="{INK}" stroke-width="1.8"/>' + text(693, 427, "k8s", "monob", 8, INK, "middle") + '</g>')
    o.append(f'<g transform="rotate(8 752 458)"><rect x="738" y="450" width="28" height="15" rx="7.5" fill="{C["terra"]}" stroke="{INK}" stroke-width="1.8"/>' + text(752, 461, "IaC", "monob", 8, C["ivory"], "middle") + '</g>')
    o.append(f'<path d="M688,462 l6,-8 l6,8z" fill="{C["peach"]}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')

    # books
    books = [(500, 458, 120, 20, C["terra"], "SITE RELIABILITY"), (508, 438, 104, 20, C["sage"], "KUBERNETES"),
             (502, 420, 112, 18, C["gold"], "INFRA AS CODE"), (514, 404, 92, 16, C["steel"], "SYSTEMS DESIGN")]
    for (x, y, w, h, col, label) in books:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{col}" stroke="{INK}" stroke-width="{LW2}"/>'
                 f'<line x1="{x+9}" y1="{y}" x2="{x+9}" y2="{y+h}" stroke="{INK}" stroke-width="1.4"/>'
                 + text(x + 15, y + h / 2 + 3, label, "monob", 7.5, C["ivory"] if col not in (C["gold"], C["sage"]) else INK, ls=1))

    # mug
    o.append(f'<path d="M888,428 q22,2 17,21 q-4,13 -21,10" stroke="{INK}" stroke-width="5" fill="none"/>')
    o.append(f'<path d="M826,404 L896,404 L890,472 Q861,480 832,472Z" fill="{C["paper"]}" stroke="{INK}" stroke-width="{LW}" stroke-linejoin="round"/>')
    o.append(f'<path d="M878,408 L891,408 L886,470 L875,472Z" fill="url(#dots)" opacity=".25"/>')
    o.append(f'<ellipse cx="861" cy="404" rx="35" ry="5" fill="{C["wood2"]}" stroke="{INK}" stroke-width="{LW2}"/>')
    for i, word in enumerate(["AUTOMATE", "CREATE", "ITERATE", "REPEAT"]):
        o.append(text(859, 422 + i * 12.5, word, "disp", 11, C["forest"] if i % 2 == 0 else C["terra"], "middle", ls=1))
    for sx in (848, 866):
        o.append(f'<path d="M{sx},396 c-6,-8 6,-12 0,-20 c-5,-7 4,-10 1,-16" stroke="{INK}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')

    # plants (break the frame)
    o.append(monstera(470, 418))
    o.append(pot(470, 426, 54, 52, C["terra"], C["brick"]))
    o.append(snake_plant(946, 430))
    o.append(pot(946, 436, 58, 42, C["sage"], C["forest"]))

    # ---------- left text block ----------
    o.append(text(52, 72, f"~/{P['github_username']}  /  README.md", "monob", 11.5, C["forest"], ls=1.5))
    o.append(f'<path d="M52,86 H400" stroke="{INK}" stroke-width="{LW2}"/><path d="M52,86 H120" stroke="{C["terra"]}" stroke-width="6"/>')
    nsize = min(fit(first.upper(), "disp", 104, 384, 2), fit(last.upper(), "disp", 104, 384, 2))
    # names sit on fixed baselines so shorter/longer names never move the rest of the layout
    ys = [200, 306]
    if nsize < 104:
        ys = [200 - (104 - nsize) * 0.5, 306 - (104 - nsize) * 0.0]
        ys[0] = ys[1] - nsize * 1.08
    off = max(2, nsize * 0.05)
    for s_, y, col in [(first.upper(), ys[0], C["forest"]), (last.upper(), ys[1], C["terra"])]:
        o.append(text(52 + off, y + off, s_, "disp", nsize, INK, ls=2))
        o.append(text(52, y, s_, "disp", nsize, col, ls=2, extra=f'stroke="{INK}" stroke-width="{max(1.5, nsize*0.03):.1f}" paint-order="stroke" stroke-linejoin="round"'))
    # sticker with the handle
    hs = fit(handle, "mark", 26, 300)
    sw = measure(handle, "mark", hs) + 34
    sy = 330
    o.append(f'<g transform="rotate(-4 {52+sw/2:.0f} {sy+22})">' + panel(52, sy, sw, 44, C["gold"], 8, 5)
             + text(52 + 17, sy + 30, handle, "mark", hs, INK) + "</g>")
    ry = sy + 88
    cols = [C["terra"], C["forest"], C["gold"]]
    for i, s in enumerate(P["roles"][:3]):
        y = ry + i * 34
        o.append(bullet(64, y - 6, str(i + 1), cols[i], 11, size=13))
        o.append(text(86, y, s.upper(), "sansb", fit(s.upper(), "sansb", 16, 320, 1.6), INK, ls=1.6))
    p, n = para(52, ry + 112, P["tagline"], "sans", 15, INK, 372, 22, maxlines=3)
    o.append(p)

    vals = "CREATIVE ENGINEER  ·  INFRASTRUCTURE THINKER  ·  AI BUILDER  ·  LIFELONG LEARNER"
    o.append(f'<path d="M24,{H-56} H{W-34}" stroke="{INK}" stroke-width="{LW2}"/>')
    o.append(text((W - 7) / 2, H - 30, vals, "monob", 11, INK, "middle", ls=2.2))
    o.append("</svg>")
    return "\n".join(o)
