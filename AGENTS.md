# Agent instructions for JasonYao/resume

Use these instructions as the starting point; search the repo only if something here is missing or found to be wrong.

## What this is
A small data-driven resume generator. Python 3.14 (managed by `uv` 0.13.6) renders resume data through Jinja2 templators into a LaTeX file, JSON-LD, raw JSON and a biography text file. XeLaTeX then builds the PDF and ImageMagick 7 makes a PNG thumbnail. Deployed to GitHub Pages by CI from the `source` branch (commits generated files to `master`).

## Layout
- `data/resume_data.py` – the resume content (`all_data`); most content edits happen here. `data/tests/` – pytest tests (bio, LaTeX template syntax, lockdown).
- `main.py` – entry point: `load_data(all_data)` → `template_data` → each templator `.write()`.
- `pyresume/` – library. `pyresume/templators/{biography,json_ld,json_raw,latex_2_column_resume}/` each output one format; `templating.py` is shared. LaTeX Jinja templates live in `pyresume/templators/latex_2_column_resume/templates/`.
- `two-column-resume.cls` – LaTeX class (uses fontspec, xltxtra, xunicode); `fonts/`, `assets/` – fonts, logos, watermark.
- `bin/` – scripts (all Bash, shellcheck-linted): `install_dependencies` (TeX Live into /tmp/texlive + ImageMagick 7 + policy.xml; needs sudo/network; must be `source`d), `test`, `build`, `deploy` (CI only), `lockdown` (CI trust-store hardening), `comment_pr`, `utils.sh`. `git/pre-push` is an optional hook.
- `pyproject.toml` / `uv.lock` – deps (dacite, Jinja2, pycountry, python-dateutil; dev: pytest). No other linter/formatter config.

## Commands (validated)
- Install Python deps: `uv sync --locked --all-extras --dev` (always before tests).
- Python tests only: `uv run pytest` → 8 passed, 2 skipped (~2s). This is the quickest, reliable check.
- Full test: `bin/test` = `shellcheck -x` on every script listed in `bin/test` (`bash_files`) then `uv run pytest`. It fails with "shellcheck: command not found" unless `sudo apt-get install -y shellcheck`. If you add/rename a bash script, add it to `bash_files` in `bin/test`.
- Build: `bin/build` runs `uv run python main.py`, then `xelatex` 3 times, then `magick` for the PNG. Needs TeX Live in `/tmp/texlive/bin/x86_64-linux` (installed by `source bin/install_dependencies`), `fonts-font-awesome`, `ghostscript`, ImageMagick 7; these are absent in a bare environment, so the LaTeX/PNG steps will fail there. `uv run python main.py` alone works to validate data/templating changes (it writes the output files below).
- CI (`.github/workflows/main.yml`): lockdown → uv sync → apt deps → install_dependencies → `bin/test` → `bin/build` → artifact upload / PR comment. Environment setup is mirrored in `.github/workflows/copilot-setup-steps.yml`.

## IMPORTANT: never commit generated files
`bin/build` / `main.py` create `Resume_Jason_Yao.pdf`, `Resume_Jason_Yao.png`, `Resume_Jason_Yao.tex`, `biography.txt`, `json-schema.json`, `raw-data.json` in the repo root. They are only committed by the deploy step on `master`. They are NOT in `.gitignore` (deploy does `git add`), so never stage or commit them in a PR; delete them or avoid `git add -A`/`git add .`. Check `git status` before committing. Also don't commit `.venv/`.

## Notes
- Edit `bin/lockdown` rather than workflows when changing distrusted CAs; keep scripts shellcheck-clean (`set -e` style, `source`d `utils.sh` with `# shellcheck source=` directives).
- After changing templates or data, run `uv run pytest` and `uv run python main.py`, then remove generated files.
