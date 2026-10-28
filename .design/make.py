"""Build every image in /assets and README.md from profile.yml.

    pip install fonttools brotli pyyaml
    python3 .design/make.py

The "Build profile" GitHub Action runs this for you whenever profile.yml
changes, and daily to refresh the activity panel.
"""
import html, json, pathlib, sys
import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from lib import finalize, TE, CU, LA  # noqa: E402
import sections as s  # noqa: E402


def load():
    P = yaml.safe_load((ROOT / "profile.yml").read_text())
    P["github_username"] = str(P.get("github_username", "")).strip().lstrip("@")
    errs = [f"'{k}' is empty" for k in ("github_username", "first_name", "last_name", "about") if not str(P.get(k) or "").strip()]
    if len(P.get("focus") or []) < 1:
        errs.append("'focus' needs at least one line")
    if len(P.get("ai_engineering") or []) != 3:
        errs.append("'ai_engineering' needs exactly 3 columns")
    if not (1 <= len(P.get("builds") or []) <= 6):
        errs.append("'builds' needs 1 to 6 entries")
    if errs:
        sys.exit("profile.yml: " + "; ".join(errs))
    P.setdefault("links", {})
    P.setdefault("exploring", [])
    P.setdefault("toolkit", [])
    return P


def build_url(P, b):
    if b.get("url"):
        return b["url"]
    if b.get("repo"):
        return f"https://github.com/{P['github_username']}/{b['repo']}"
    return None


def main():
    P = load()
    u = P["github_username"]
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    old = {p.name for p in assets.glob("*.svg")}
    out = {"hero.svg": s.hero(P), "about.svg": s.about(P), "ai.svg": s.ai(P),
           "builds.svg": s.builds_header(P), "connect.svg": s.connect(P), "footer.svg": s.footer(P)}
    if P["toolkit"]:
        out["toolkit.svg"] = s.toolkit(P)
    if P["exploring"]:
        out["exploring.svg"] = s.exploring(P)
    if P.get("show_activity", True):
        f = ROOT / "profile" / "activity.json"
        data = json.loads(f.read_text()) if f.exists() else None
        out["activity.svg"] = s.activity(P, data)
    for i, b in enumerate(P["builds"][:6]):
        out[f"build-{i+1}.svg"] = s.build_card(b, i)
    btns = []
    L = P["links"]
    for key, label, color, href in [("linkedin", "LinkedIn", TE, L.get("linkedin")), ("portfolio", "Portfolio", LA, L.get("portfolio")),
                                    ("email", "Email", CU, f"mailto:{L['email']}" if L.get("email") else None)]:
        if href:
            svg_, w = s.button(label, color)
            out[f"btn-{key}.svg"] = svg_
            btns.append((f"assets/btn-{key}.svg", label, href, w))
    for name, svg_ in out.items():
        (assets / name).write_text(finalize(svg_))
    for stale in old - set(out):
        (assets / stale).unlink()

    a = lambda t: html.escape(" ".join(str(t).split()), quote=True)
    R = ["<!-- Generated from profile.yml by .design/make.py. Edit profile.yml, not this file. -->", ""]

    def block(*imgs):
        R.extend(['<p align="center">', *["  " + i for i in imgs], "</p>", ""])

    def img(src, alt, width="100%", href=None):
        t = f'<img src="{src}" width="{width}" alt="{a(alt)}" />'
        return f'<a href="{href}">{t}</a>' if href else t

    name = f"{P['first_name']} {P['last_name']}"
    block(img("assets/hero.svg", f"{name}. {' · '.join(P['focus'])}. {' '.join(P.get('tagline', []))}"))
    block(img("assets/about.svg", "About: " + P["about"]))
    if "toolkit.svg" in out:
        block(img("assets/toolkit.svg", "Toolkit: " + "; ".join(f"{k}: {v}" for k, v in P["toolkit"])))
    block(img("assets/ai.svg", "AI engineering: " + "; ".join(f"{c['title']}: {', '.join(c['items'])}" for c in P["ai_engineering"])))
    block(img("assets/builds.svg", "Featured builds"))
    cards = [img(f"assets/build-{i+1}.svg", f"{b['name']}: {b['description']}" + ("" if build_url(P, b) else " (in progress)"), "32%", build_url(P, b))
             for i, b in enumerate(P["builds"][:6])]
    for k in range(0, len(cards), 3):
        block(*cards[k:k + 3])
    if "exploring.svg" in out:
        block(img("assets/exploring.svg", "Currently exploring: " + ", ".join(P["exploring"])))
    if "activity.svg" in out:
        block(img("assets/activity.svg", f"GitHub activity for @{u}"))
    block(img("assets/connect.svg", "Connect. Open to: " + P.get("open_to", "")))
    if btns:
        block(*[img(src, label, str(int(w * 0.8)), href) for src, label, href, w in btns])
    block(img("assets/footer.svg", f"{u}@github:~$ keep building"))
    (ROOT / "README.md").write_text("\n".join(R))
    print(f"built {len(out)} images and README.md")


if __name__ == "__main__":
    main()
