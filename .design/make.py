"""Build everything from profile.yml: the images in /assets and README.md.

    python3 .design/make.py

Needs: pip install fonttools brotli pyyaml
The GitHub Action in .github/workflows/build-profile.yml runs this for you
whenever profile.yml changes, so you normally never run it by hand.
"""
import sys, pathlib, html
import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from lib import finalize  # noqa: E402
import hero, sections as s  # noqa: E402


def load():
    P = yaml.safe_load((ROOT / "profile.yml").read_text())
    P["github_username"] = str(P["github_username"]).strip().lstrip("@")
    problems = []
    for key in ("github_username", "first_name", "last_name", "title", "tagline", "intro", "quote"):
        if not str(P.get(key) or "").strip():
            problems.append(f"'{key}' is empty")
    if len(P.get("roles", [])) != 3:
        problems.append("'roles' needs exactly 3 lines")
    if len(P.get("projects", [])) != 4:
        problems.append("'projects' needs exactly 4 entries")
    if len(P.get("roadmap", [])) != 5:
        problems.append("'roadmap' needs exactly 5 stops")
    if len(P.get("toolbox", [])) != 4:
        problems.append("'toolbox' needs exactly 4 columns")
    if problems:
        sys.exit("profile.yml: " + "; ".join(problems))
    P.setdefault("links", {})
    return P


def write(name, svg, folder="assets"):
    d = ROOT / folder
    d.mkdir(exist_ok=True)
    (d / name).write_text(finalize(svg))


def readme(P):
    u = P["github_username"]
    a = lambda t: html.escape(" ".join(str(t).split()), quote=True)
    name = f"{P['first_name']} {P['last_name']}"
    tools = " ".join(f"{c['title']}: {', '.join(c['items'])}." for c in P["toolbox"])
    out = [f"<!-- Generated from profile.yml by .design/make.py. Edit profile.yml, not this file. -->", ""]

    def img(src, alt, width="100%", href=None):
        tag = f'<img src="{src}" width="{width}" alt="{a(alt)}" />'
        return f'<a href="{href}">{tag}</a>' if href else tag

    def block(*imgs):
        out.append('<p align="center">')
        out.extend("  " + i for i in imgs)
        out.append("</p>")
        out.append("")

    block(img("assets/hero.svg", f"{name} (@{u}). {' · '.join(P['roles'])}. {P['tagline']}"))
    block(img("assets/whoami.svg", f"01 / whoami. {name}, {P['title']}. {P['intro']}"))
    block(img("assets/glance.svg", f"02 / at a glance. {'; '.join(g[1] for g in s.GLANCE)}. “{P['quote']}”"))
    block(img("assets/toolbox.svg", f"03 / engineering toolbox. {tools}"))
    block(img("assets/projects.svg", "04 / featured projects"))
    cards = []
    for pr in P["projects"]:
        url = pr.get("url") or f"https://github.com/{u}/{pr['repo']}"
        cards.append(img(f"assets/project-{pr['repo']}.svg", f"{pr['repo']}: {pr['description']}", "49%", url))
    block(*cards[:2])
    block(*cards[2:])
    block(img("assets/roadmap.svg", "05 / currently building & learning. " + " → ".join(P["roadmap"]) + ". Always a work in progress."))
    block(img("assets/activity.svg", "06 / GitHub activity"))
    block(img("profile/contribution-grid.svg", f"Contribution calendar for @{u}"))
    block(img("profile/stats.svg", f"GitHub stats for @{u}", "49%"), img("profile/top-langs.svg", f"Most used languages for @{u}", "49%"))
    block(img("assets/connect.svg", "07 / connect. Let’s build something meaningful."))
    btns = [img("assets/btn-github.svg", f"GitHub: github.com/{u}", None, f"https://github.com/{u}")]
    L = P["links"]
    if L.get("linkedin"):
        btns.append(img("assets/btn-linkedin.svg", "LinkedIn", None, L["linkedin"]))
    if L.get("email"):
        btns.append(img("assets/btn-email.svg", f"Email: {L['email']}", None, f"mailto:{L['email']}"))
    if L.get("website"):
        btns.append(img("assets/btn-website.svg", "Website", None, L["website"]))
    wpc = {1: "32%", 2: "32%", 3: "32%", 4: "24%"}[len(btns)]
    block(*[b.replace('width="None"', f'width="{wpc}"') for b in btns])
    block(img("assets/footer.svg", f"{u}@github:~$ keep building. {P['footer']}"))
    return "\n".join(out)


def short(url):
    return url.split("://", 1)[-1].removeprefix("www.").rstrip("/")


def main():
    P = load()
    u = P["github_username"]
    old = {p.name for p in (ROOT / "assets").glob("*.svg")} if (ROOT / "assets").exists() else set()
    built = {
        "hero.svg": hero.build(P), "whoami.svg": s.whoami(P), "glance.svg": s.glance(P), "toolbox.svg": s.toolbox(P),
        "projects.svg": s.projects_header(P), "roadmap.svg": s.roadmap(P), "activity.svg": s.activity(P),
        "connect.svg": s.connect(P), "footer.svg": s.footer(P),
        "btn-github.svg": s.button("code", "GITHUB", f"github.com/{u}"),
    }
    L = P["links"]
    if L.get("linkedin"):
        built["btn-linkedin.svg"] = s.button("case", "LINKEDIN", short(L["linkedin"]))
    if L.get("email"):
        built["btn-email.svg"] = s.button("mail", "EMAIL", L["email"])
    if L.get("website"):
        built["btn-website.svg"] = s.button("globe", "WEBSITE", short(L["website"]))
    for i, pr in enumerate(P["projects"]):
        built[f"project-{pr['repo']}.svg"] = s.project_card(P, i)
    for name, svg in built.items():
        write(name, svg)
        print("  assets/" + name)
    for stale in old - set(built):          # e.g. a renamed project
        (ROOT / "assets" / stale).unlink()
        print("  removed assets/" + stale)
    # live-data placeholders: only when the workflow hasn't produced real ones yet
    for name, fn in [("contribution-grid.svg", s.ph_calendar),
                     ("stats.svg", lambda: s.ph_card("Repository stats", ["Total stars", "Total commits", "Pull requests", "Issues", "Contributed to"])),
                     ("top-langs.svg", lambda: s.ph_card("Most used languages"))]:
        if not (ROOT / "profile" / name).exists():
            write(name, fn(), "profile")
            print("  profile/" + name + " (placeholder)")
    (ROOT / "README.md").write_text(readme(P))
    print("  README.md\nDone.")


if __name__ == "__main__":
    main()
