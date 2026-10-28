# How to customize your profile

Everything personal lives in **one file: `profile.yml`**. You change text there, and a GitHub Action redraws every image and rewrites `README.md` for you. You never need to touch the artwork, the README, or any code.

---

## 1. First-time setup (once)

1. On GitHub, create a **new public repository named exactly your username** (e.g. `cpanda33`).
   GitHub shows a note saying it's your special profile repository. That's the one.
2. Upload everything in this kit to it, **including the hidden folders `.github` and `.design`**.
   *Easiest:* unzip, then drag the whole folder's contents onto the repo page ("uploading an existing file"). On a Mac, press `Cmd + Shift + .` in Finder to see hidden folders before dragging.
   Check that `.github/workflows/build-profile.yml` and the `.design` folder show up in the repo. If either is missing, upload that folder again on its own. For the workflow, you can also use **Add file → Create new file**, type `.github/workflows/build-profile.yml` as the name, and paste the file's contents.
3. Go to the repo's **Settings → Actions → General → Workflow permissions**, choose **Read and write permissions**, and save.
4. Go to the **Actions** tab → **Build profile** → **Run workflow**. After about a minute, your profile at `github.com/<username>` shows the finished page with your live stats.

---

## 2. Change your name, links or anything else

1. In your repo, open **`profile.yml`** and click the **pencil icon** (Edit).
2. Change the values between the quotes. For example:

   ```yaml
   first_name: "Cydnee"
   last_name: "Owens"
   ```

3. Click **Commit changes**.
4. Wait about a minute. The **Build profile** action runs by itself and updates the page. You can watch it in the **Actions** tab.

### Field reference

| To change… | Edit this in `profile.yml` | Notes |
| --- | --- | --- |
| Name in the big header | `first_name`, `last_name` | Long names shrink automatically to fit. |
| Job title in the terminal | `title` | |
| The three headline lines | `roles` | Exactly 3. |
| Tagline, intro paragraph, quote | `tagline`, `intro`, `quote` | |
| LinkedIn button | `links → linkedin` | Paste the full URL, e.g. `"https://www.linkedin.com/in/cydnee-owens"`. |
| Email button | `links → email` | Just the address, e.g. `"cydnee@example.com"`. |
| Website button | `links → website` | Optional. Full URL. |
| Hide a button | set it to `""` | The button disappears and the rest re-space themselves. |
| Project cards | `projects` | `repo` is the repository name. The card links to `github.com/<username>/<repo>`. To link somewhere else, add a line `url: "https://…"`. `scene` picks the illustration: `construction`, `rooftop`, `workshop` or `library`. |
| Toolbox | `toolbox` | 4 columns, up to 8 items each. Common tools get brand colors automatically. |
| Roadmap stops | `roadmap` | Exactly 5. |
| Footer line | `footer` | |

---

## 3. Change your GitHub username

Your username appears in the header, the terminal panels, the footer, the GitHub button and every project link. All of them come from one line.

**If you're setting this up under a different account:**
1. Name the profile repo after that account (step 1 above).
2. In `profile.yml`, set `github_username: "your-new-name"` and commit.

**If you renamed your GitHub account** (Settings → Account → Change username):
1. Rename the profile repo to match: repo **Settings → General → Repository name** → type the new username → **Rename**. Without this, GitHub stops showing it on your profile.
2. In `profile.yml`, set `github_username: "your-new-name"` and commit.

The activity cards (contribution calendar, stats, languages) always follow whichever account owns the repo, so they need no change.

---

## Rules for editing `profile.yml`

- Keep the **quotes** around every value.
- Apostrophes are fine inside quotes (`"I'm"`). For a double quote inside, write `\"`.
- Keep the **indentation** (spaces at the start of lines) exactly as it is.
- Lines starting with `#` are notes and are ignored.

## If something goes wrong

- **The page didn't change.** Check the **Actions** tab. A red ✗ means the build stopped. Click it and open the **Draw artwork** step to see the reason in plain words, e.g. `profile.yml: 'roles' needs exactly 3 lines`. Fix that line and commit again.
- **"Permission denied" / push failed.** Redo step 1.3 (Read and write permissions).
- **Stats cards say "placeholder".** Run **Build profile** once from the Actions tab (step 1.4). After that they refresh daily.
- **Don't edit `README.md` or `/assets` directly.** They are rebuilt from `profile.yml` on every change, so your edits there would be overwritten.

---

## Optional: build on your own computer

You only need this to preview changes before pushing, or to change the artwork itself (colors and drawings live in `.design/`).

```bash
pip install fonttools brotli pyyaml
python3 .design/make.py
```

Colors are in `.design/lib.py` (the `C` palette), the header illustration is in `.design/hero.py`, and all other sections are in `.design/sections.py`.

Fonts: Anton, Space Grotesk and JetBrains Mono (SIL Open Font License), and Permanent Marker (Apache 2.0). They are bundled in `.design/fonts` with their licenses.
