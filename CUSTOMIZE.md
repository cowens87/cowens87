# Customizing your profile

Everything on the page comes from **`profile.yml`**. Edit it, commit, and the **Build profile** action redraws the images and rewrites `README.md` in about a minute. Don't edit `README.md` or `/assets` by hand; they're regenerated.

## Common edits

| To change… | Edit in `profile.yml` |
| --- | --- |
| Colour theme | `theme`: `dusk`, `orchid`, `sunset`, `flamingo`, `sakura`, `aurora`, `ember` or `lilac` |
| Name in the header | `first_name`, `last_name` (long names shrink to fit) |
| The four lines beside your name | `focus` |
| "Building systems. / Automating complexity." | `tagline` (two lines) |
| About text | `about` (two or three sentences) |
| Toolkit rows | `toolkit` (up to 8 rows: `["Label", "Tool · Tool"]`) |
| AI engineering columns | `ai_engineering` (3 columns), `ai_tools` (the small line at the right) |
| Featured builds | `builds` (up to 6). See below. |
| Currently exploring | `exploring` |
| Activity panel (off by default; GitHub shows its own graph below the README) | `show_activity: true` to add it |
| LinkedIn / Portfolio / Email buttons | `links`. Empty `""` hides the button. |
| "open to:" line | `open_to` |
| GitHub username | `github_username` (must match the repo name) |

### Featured builds

Each card has a `name`, a one-line `description`, and a `repo`:

```yaml
  - name: "KUBE.LAB"
    description: "Kubernetes simulations & learning"
    repo: "kube-lab"          # → links to github.com/cowens87/kube-lab
```

- `repo: ""` means the card shows **in progress** and isn't clickable. Use this for things you haven't published yet.
- To link somewhere other than a repo, add `url: "https://…"`.

## Rules for `profile.yml`

- Keep the quotes around text and the indentation as it is.
- Apostrophes are fine inside quotes. For a double quote, write `\"`.
- If a build fails, open the **Actions** tab. The red run's "Build README" step says what's wrong in plain words, e.g. `'builds' needs 1 to 6 entries`.

## Activity panel (optional)

Off by default, because GitHub already shows your contribution graph under the README. If you set `show_activity: true`, the action reads your contribution calendar and language mix from GitHub once a day, and every time you edit `profile.yml`. It shows public activity only. Until the first run, the panel shows an empty grid.

## Preview locally (optional)

```bash
pip install fonttools brotli pyyaml
python3 .design/make.py
```

Colors are in `.design/lib.py`; each section's drawing is in `.design/sections.py`.
Fonts: Anton, Inter, JetBrains Mono (SIL Open Font License), bundled in `.design/fonts`.
