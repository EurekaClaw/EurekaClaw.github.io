---
myst:
  html_meta:
    description: "EurekaClaw — The AI that catches your Eureka moments. Multi-agent research assistant that proves theorems, writes papers, and learns from every session."
    keywords: "AI, theorem proving, research assistant, arXiv, LaTeX, multi-agent"
---

# EurekaClaw Documentation

<p align="center">
<strong>The AI that catches your Eureka moments.</strong><br/>
Crawls arXiv · Generates theorems · Proves lemmas · Writes LaTeX papers · Runs experiments
</p>

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 🚀 Quick Start
:link: getting-started/quickstart
:link-type: doc

Up and running in 5 minutes. Install EurekaClaw, set your API key, and prove your first theorem.
:::

:::{grid-item-card} 📖 User Guide
:link: user-guide/index
:link-type: doc

Full walkthrough — input modes, gate mode, output files, tuning, troubleshooting, and example workflows.
:::

:::{grid-item-card} ⚙️ Configuration
:link: reference/configuration
:link-type: doc

All `.env` variables: backends, models, token limits, pipeline modes, retry settings.
:::

:::{grid-item-card} 🖥️ CLI Reference
:link: reference/cli
:link-type: doc

Every command, option, and exit code for the `eurekaclaw` command-line tool.
:::

:::{grid-item-card} 🏗️ Architecture
:link: reference/architecture
:link-type: doc

Pipeline stages, agent design, data flow, LaTeX compilation, and the theory inner loop.
:::

:::{grid-item-card} 🌐 Browser UI
:link: user-guide/browser-ui
:link-type: doc

Launch the visual interface — live agent track, pause/resume, gate overlays, skills manager, and config sliders.
:::

::::

---

## What EurekaClaw Does

EurekaClaw is a **multi-agent AI research assistant** that goes from a question to a publishable result — autonomously. It crawls the literature, generates and stress-tests hypotheses, runs experiments, and writes up findings.

```bash
$ eurekaclaw prove "Find recent papers on sparse attention + prove efficiency bound"

🦞 Crawling arXiv cs.LG (2024–2025)...
📄 Found 23 relevant papers. Summarizing...
💡 Hypothesis generated: O(n log n) via topological filtration
✨ Theorem 3.1 drafted. LaTeX ready. Proof complete.
🦞 Eureka! Paper draft saved to ./results/
```

::::{grid} 2 2 4 4
:gutter: 2

:::{grid-item-card} 🔍 Literature Crawler
Fetch, summarize, and cross-reference papers from arXiv and Semantic Scholar.
:::

:::{grid-item-card} 💡 Idea Generator
Brainstorm novel hypotheses by synthesizing patterns across thousands of papers.
:::

:::{grid-item-card} 🔢 Theorem Prover
Generate, verify, and formalize proofs via a 7-stage bottom-up pipeline.
:::

:::{grid-item-card} 📄 Paper Writer
Draft camera-ready LaTeX papers with theorem environments and citations.
:::

:::{grid-item-card} 🖥️ Runs Locally
Compatible with Every Major Model API — Privacy by Design.
:::

:::{grid-item-card} 🧠 Continual Learning
Distills proof strategies into skills after every session, improving over time.
:::

:::{grid-item-card} 🧪 Experiment Runner *(under development)*
Numerically validates theoretical bounds; flags low-confidence lemmas.
:::

:::{grid-item-card} 🌐 Browser UI
Visual interface with live progress, settings sliders, and results viewer.
:::

::::

---

## Installation

**macOS / Linux**

```bash
curl -fsSL https://eurekaclaw.ai/install.sh | bash
eurekaclaw onboard            # interactive setup wizard
```

**Windows Powershell**

```powershell
powershell -c "irm https://eurekaclaw.ai/install_win.ps1 | iex"
```

**Manual install (all platforms)**

```bash
git clone https://github.com/EurekaClaw/EurekaClaw
cd EurekaClaw
make install                  # pip install -e "." + npm install (frontend)
cp .env.example .env          # add ANTHROPIC_API_KEY
```

```bash
eurekaclaw install-skills     # install built-in proof skills (required, once)
eurekaclaw prove "The sample complexity of transformers is O(L·d·log(d)/ε²)" \
    --domain "ML theory" --output ./results
```

> No API key? Use a Claude Pro/Max subscription via [OAuth](getting-started/authentication.md).

---

## Documentation

```{toctree}
:maxdepth: 2
:caption: Getting Started

getting-started/installation
getting-started/quickstart
getting-started/authentication
```

```{toctree}
:maxdepth: 2
:caption: User Guide

user-guide/index
```

```{toctree}
:maxdepth: 2
:caption: Reference

reference/cli
reference/configuration
reference/api
reference/architecture
reference/agents
reference/tools
reference/memory
reference/skills
reference/token-limits
reference/domains
```

```{toctree}
:maxdepth: 1
:caption: Changelog

changelog/index
```

---

## Acknowledgements

EurekaClaw builds on ideas and inspiration from the broader AI-for-science community. We thank the authors of the following projects:

- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — multi-agent research orchestration
- [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) — automated research orchestration
- [EvoScientist](https://github.com/EvoScientist/EvoScientist) — evolutionary hypothesis generation
- [AI-Researcher](https://github.com/hkuds/ai-researcher) — automated research pipeline
- [Awesome AI for Science](https://github.com/ai-boost/awesome-ai-for-science) — curated resource list
- [Dr. Claw](https://github.com/OpenLAIR/dr-claw) — open research agent framework
- [OpenClaw](https://github.com/openclaw/openclaw) — open-source research claw
- [ClawTeam](https://github.com/HKUDS/ClawTeam) — collaborative research agents
- [ScienceClaw](https://github.com/beita6969/ScienceClaw) — science-focused research agent
