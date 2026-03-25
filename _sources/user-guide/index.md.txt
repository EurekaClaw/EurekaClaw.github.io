# User Guide

A practical walkthrough for using EurekaClaw — from installation to reading your first generated paper.

```{toctree}
:maxdepth: 1

input-modes
browser-ui
output
gate-mode
tuning
skills-learning
troubleshooting
```

---

## At a Glance

EurekaClaw has three input modes depending on how specific your goal is:

| Mode | Command | When to use |
|---|---|---|
| **Prove** | `eurekaclaw prove "<conjecture>"` | You have a precise mathematical statement |
| **From Papers** | `eurekaclaw from-papers <ids>` | You want to extend specific papers |
| **Explore** | `eurekaclaw explore "<domain>"` | You want to discover open problems |

After a run, artifacts land in `./results/<session_id>/` — LaTeX source, compiled PDF, proof state, and bibliography.

## Common Options

| Option | Default | Description |
|---|---|---|
| `--domain`, `-d` | `""` | Research domain (enables domain-specific tools and skills) |
| `--output`, `-o` | `./results` | Output directory |
| `--gate` | `none` | `none` / `auto` / `human` — how much to pause for review |
| `--mode` | `skills_only` | Post-run learning: `skills_only`, `rl`, `madmax` |
| `--verbose`, `-v` | — | Enable DEBUG logging |
