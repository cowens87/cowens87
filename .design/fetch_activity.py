"""Fetch the contribution calendar and language mix for the profile owner.

Run by the workflow with GITHUB_TOKEN set; writes profile/activity.json.
On any failure it leaves the previous file untouched, so the page keeps
showing the last good data.
"""
import json, os, pathlib, sys, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
login = os.environ.get("PROFILE_USER") or yaml.safe_load((ROOT / "profile.yml").read_text())["github_username"]
token = os.environ.get("GITHUB_TOKEN")
if not token:
    sys.exit("GITHUB_TOKEN not set; skipping activity fetch")

QUERY = """query($login: String!) {
  user(login: $login) {
    contributionsCollection { contributionCalendar { totalContributions
      weeks { firstDay contributionDays { contributionCount contributionLevel weekday } } } }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      nodes { languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name } } } } }
  }
}"""

req = urllib.request.Request("https://api.github.com/graphql",
                             data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
                             headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.load(r)
    user = res["data"]["user"]
    cal = user["contributionsCollection"]["contributionCalendar"]
except Exception as e:  # noqa: BLE001
    sys.exit(f"activity fetch failed, keeping previous data: {e}")

weeks, levels, starts = [], [], []
for w in cal["weeks"]:
    days, lv = [None] * 7, [None] * 7
    for d in w["contributionDays"]:
        days[d["weekday"]] = d["contributionCount"]
        lv[d["weekday"]] = d["contributionLevel"]
    weeks.append(days)
    levels.append(lv)
    starts.append(w["firstDay"])

sizes = {}
for repo in user["repositories"]["nodes"]:
    for e in repo["languages"]["edges"]:
        sizes[e["node"]["name"]] = sizes.get(e["node"]["name"], 0) + e["size"]
top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
total = sum(v for _, v in top) or 1
langs = [(k, round(v / total, 4)) for k, v in top]

out = ROOT / "profile" / "activity.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"weeks": weeks, "levels": levels, "starts": starts, "total": cal["totalContributions"], "languages": langs}))
print(f"activity: {cal['totalContributions']} contributions, {len(langs)} languages")
