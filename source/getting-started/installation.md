# Installation

**Supported platforms:** macOS, Linux, Windows *(Windows under active development)*

```{note}
Native Windows support is under active development. A Windows installer is available (see below) but not yet fully supported. If you run into issues, install [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) (Ubuntu) and follow the macOS/Linux instructions inside the WSL terminal.
```

## Installer Script (Recommended)

**macOS / Linux**

```bash
curl -fsSL https://eurekaclaw.ai/install.sh | bash
```

**Windows** *(under development — not fully supported yet)*

```powershell
powershell -c "irm https://eurekaclaw.ai/install_win.ps1 | iex"
```

The macOS/Linux installer clones the repo, creates a virtual environment, installs EurekaClaw, and adds the `eurekaclaw` command to your PATH. Run `eurekaclaw onboard` afterwards to configure your API key and settings.

## Manual Install

**Requirements:** Python ≥ 3.11, Node.js ≥ 20, Git

```bash
git clone https://github.com/EurekaClaw/EurekaClaw
cd EurekaClaw
make install                  # pip install -e "." + npm install (frontend)
```

## With Optional Extras

```bash
pip install -e ".[openai,oauth]"
```

| Extra | Enables |
|---|---|
| `openai` | OpenRouter and local vLLM/Ollama backends |
| `codex` | Codex login via oauth (no API key needed) |
| `oauth` | Claude Pro/Max login via ccproxy (no API key needed) |
| `pdf` | Full-PDF extraction via Docling (`PaperReader`) |

## Optional System Tools

EurekaClaw works without any of these — it skips the associated step if a tool is absent.

| Tool | Purpose | Install |
|---|---|---|
| **pdflatex** + bibtex | Compile `paper.tex` → `paper.pdf` | TeX Live / MacTeX |
| **Lean4** | Formal proof verification | [leanprover.github.io](https://leanprover.github.io) |
| **clawhub** | Install skills from ClawHub registry | `pip install clawhub` |

```{note}
**Docker / sandboxed code execution** is listed as an optional tool but is **future work** — the experiment runner and `execute_python` tool are not yet safely sandboxed for general use. Keep `EXPERIMENT_MODE=false` until a future release adds proper sandbox support.
```

## Install Seed Skills

After installation, copy the bundled seed skills to your local skill bank:

```bash
eurekaclaw install-skills
```

This is a one-time step. Skills are saved to `~/.eurekaclaw/skills/` and automatically used by agents on future runs.

## Verify Installation

```bash
eurekaclaw --help
eurekaclaw skills        # lists available seed skills
```
