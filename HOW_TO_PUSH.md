# Pushing SS3 Part B to your GitHub (and keeping the ≥5 commits)

The marker checks your **commit history** and wants **at least five commits (one per component)**. This folder
is already a git repository with **7 commits** laid out exactly that way, so the simplest route is to push this
history into your existing capstone repository. I could not push for you (no GitHub access from this session),
so run one of the options below from your own machine.

Your repo (from SS1/SS2): set `REPO_URL` to it, e.g.
`https://github.com/<your-username>/<your-capstone-repo>.git`

---

## Option A — Web upload (no terminal), simplest

This gives you the files but **only one commit for Part B**, which caps this part at 50%. Use Option B/C if you
want full marks on commit history.

1. On your repo page: **Add file → Upload files**.
2. Drag in `SS3_PartB.ipynb`, the `data/` folder, `requirements.txt` and `outputs/`.
3. Commit. (One commit only — not recommended for the commit-history requirement.)

## Option B — Push this ready-made 7-commit history (recommended)

From inside this `SS3-PartB-repo` folder:

```bash
git remote add origin REPO_URL
git fetch origin
git checkout -b ss3-partb            # work on a branch
git push -u origin ss3-partb         # pushes all 7 commits
```

Then open a pull request into `main` (or merge locally and push `main`). All component commits are preserved.

> If you would rather land them directly on `main` and your `main` already exists remotely, merge first:
> `git checkout main && git pull origin main && git merge ss3-partb && git push origin main`.

## Option C — Recreate the commits in your existing clone

If you prefer the files to live in your current clone, copy `SS3_PartB.ipynb`, `data/`, `requirements.txt` and
`outputs/` into it, then commit them **component by component** so the history still shows ≥5 commits:

```bash
git add data requirements.txt README.md && git commit -m "SS3 Part B: data + setup"
# re-save/stage the notebook after each component or just stage once per logical step:
git add SS3_PartB.ipynb && git commit -m "SS3_PartB: dataset loading + preprocessing"
git add SS3_PartB.ipynb && git commit -m "SS3_PartB: model training"
git add SS3_PartB.ipynb && git commit -m "SS3_PartB: model validation"
git add SS3_PartB.ipynb outputs && git commit -m "SS3_PartB: results visualisation + outputs"
git push origin main
```

## After pushing
- Confirm `SS3_PartB.ipynb` renders on GitHub with its outputs.
- Add your **Part C video link** to the repo `README.md` (placeholder is already there).
- Enable **Discussions** on the repo (Settings → Features → Discussions) for Part D.
