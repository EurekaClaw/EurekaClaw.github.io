# EurekaClaw Documentation Site

Source for [https://eurekaclaw.github.io](https://eurekaclaw.github.io) — built with [Sphinx](https://www.sphinx-doc.org/) and the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/).

## Local Development

```bash
pip install -r requirements.txt
make html          # build once → open _build/html/index.html
make livehtml      # live-reload dev server at http://127.0.0.1:8000
```

## Structure

```
source/
├── conf.py                     Sphinx configuration
├── index.md                    Home page
├── getting-started/            Installation, quickstart, auth
├── user-guide/                 Modes, gate, tuning, output, troubleshooting
├── reference/                  CLI, config, API, architecture, agents, tools, memory, skills
├── changelog/                  Release notes
└── _static/
    ├── logo.svg
    └── css/custom.css
```

## Deployment

Docs are built and deployed automatically to GitHub Pages via `.github/workflows/docs.yml` on every push to `main`.

To enable GitHub Pages on your fork:
1. Go to **Settings → Pages**
2. Set **Source** to **GitHub Actions**

## Adding New Pages

1. Create a `.md` file in the appropriate `source/` subdirectory.
2. Add it to the `toctree` directive in the parent `index.md`.
3. Commit and push — the CI workflow builds and deploys automatically.
