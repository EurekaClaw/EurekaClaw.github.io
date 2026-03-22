# Installation

**Requirements:** Python ≥ 3.11 · **Supported platforms:** macOS, Linux

```{note}
Windows support is **under development**. Native Windows installation is not fully supported yet. In the meantime, Windows users should install [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) (Ubuntu) and follow the instructions below inside the WSL terminal.
```

## From Source (Recommended)

```bash
git clone https://github.com/EurekaClaw/EurekaClaw_dev_zero
cd EurekaClaw_dev_zero
pip install -e "."
```

## With Optional Extras

```bash
pip install -e ".[openai,oauth]"
```

| Extra | Enables |
|---|---|
| `openai` | OpenRouter and local vLLM/Ollama backends |
| `oauth` | Claude Pro/Max login via ccproxy (no API key needed) |
| `pdf` | Full-PDF extraction via Docling (`PaperReader`) |

## Optional System Tools

EurekaClaw works without any of these — it skips the associated step if a tool is absent.

| Tool | Purpose | Install |
|---|---|---|
| **pdflatex** + bibtex | Compile `paper.tex` → `paper.pdf` | TeX Live / MacTeX |
| **Lean4** | Formal proof verification | [leanprover.github.io](https://leanprover.github.io) |
| **Docker** | Sandboxed code execution | [docker.com](https://www.docker.com) |
| **clawhub** | Install skills from ClawHub registry | `pip install clawhub` |

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
