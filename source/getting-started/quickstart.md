# Quick Start

Five minutes from zero to a generated paper.

## 1. Install

**macOS / Linux**

```bash
curl -fsSL https://eurekaclaw.ai/install.sh | bash
eurekaclaw onboard            # interactive setup wizard (creates .env)
```

**Windows** *(under development — not fully supported yet)*

```powershell
powershell -c "irm https://eurekaclaw.ai/install_win.ps1 | iex"
```

**Manual install (Linux/MacOS)**

```bash
git clone https://github.com/EurekaClaw/EurekaClaw
cd EurekaClaw
make install                  # pip install -e "." + npm install (frontend)
cp .env.example .env
```

**Manual install (Windows)**

```bash
git clone https://github.com/EurekaClaw/EurekaClaw
cd EurekaClaw
powershell -ExecutionPolicy Bypass -File install_win.ps1    # pip install -e "." + npm install (frontend)
cp .env.example .env
```

Edit `.env` and add your `ANTHROPIC_API_KEY` (or see [Authentication](authentication.md)).

## 2. Install Skills

```bash
eurekaclaw install-skills
```

> **Required.** This step downloads the built-in seed skills (proof strategies, domain heuristics, lemma templates) that EurekaClaw needs to run. Skipping it will cause proofs to fail with `No skills available` or produce significantly degraded results.

## 3. Run Your First Proof

```bash
eurekaclaw prove "The sum of the first n natural numbers equals n(n+1)/2" \
    --domain "combinatorics" --output ./results
```

Expected output:

```
━━━━━━━━━━━━━━━ Survey Complete ━━━━━━━━━━━━━━━
 Papers found       3
 Open problems      1
 Key objects        induction, arithmetic series
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━ Theory Complete ━━━━━━━━━━━━━━━
 Status             proved
 Lemmas             2 (1 known · 1 new)
 Confidence         ✓ high on 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🦞 Paper saved to: ./results/<session_id>/paper.pdf
```

## 4. Read the Output

Open `./results/<session_id>/paper.pdf` for the compiled paper, or check:

| File | Contains |
|---|---|
| `paper.pdf` | Compiled PDF (needs pdflatex + bibtex) |
| `paper.tex` | Full LaTeX source |
| `theory_state.json` | Proof state — lemmas, confidence scores |
| `research_brief.json` | Planning state |

## Next Steps

::::{grid} 1 2 2 3
:gutter: 2

:::{grid-item-card} 📖 User Guide
:link: ../user-guide/index
:link-type: doc

Learn all three input modes, gate control, and tuning options.
:::

:::{grid-item-card} ⚙️ Configuration
:link: ../reference/configuration
:link-type: doc

Set models, token limits, and pipeline behavior via `.env`.
:::

:::{grid-item-card} 🌐 Browser UI
:link: ../user-guide/browser-ui
:link-type: doc

Launch the visual interface for live progress and settings sliders.
:::

::::
