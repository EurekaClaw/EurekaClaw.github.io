# Skills and Continual Learning

## What Are Skills?

Skills are Markdown files that encode successful proof strategies, domain conventions, and common techniques. They are injected into agent prompts before each task, improving results without retraining the model.

Skills live in `~/.eurekaclaw/skills/`.

## Viewing Your Skills

```bash
eurekaclaw skills
```

## Installing Built-in Skills

```bash
eurekaclaw install-skills
eurekaclaw install-skills --force   # overwrite existing
```

## Installing from ClawHub

```bash
eurekaclaw install-skills steipete/github
```

Downloads from the [ClawHub](https://clawhub.ai/) registry. Requires the `clawhub` CLI.

## How EurekaClaw Learns

After each session, the `ContinualLearningLoop` runs automatically. It:
1. Extracts unique failure patterns from the session
2. Distills successful proof strategies using the LLM
3. Writes new `.md` skill files to `~/.eurekaclaw/skills/`

These new skills are automatically used in future sessions.

## Learning Modes

Set `EUREKACLAW_MODE` in `.env`:

| Mode | What runs after each session |
|---|---|
| `skills_only` (default) | Distill failures into new skill files |
| `rl` | Skill distillation + Process Reward Model scoring of proof trajectories |
| `madmax` | Skill distillation + PRM scoring + cloud LoRA fine-tuning (GRPO) |

## Writing Skills Manually

Create a `.md` file in `~/.eurekaclaw/skills/`:

```markdown
---
name: my_technique
version: "1.0"
tags: [probability, concentration]
agent_roles: [theory]
pipeline_stages: [theory]
description: When to use Azuma-Hoeffding vs Bernstein
source: manual
created_at: 2026-03-21T00:00:00
---

# Azuma vs Bernstein

Use Azuma-Hoeffding when:
- Bounded differences condition holds
- Variance is unknown

Use Bernstein when:
- You have a bound on the variance
- Gives tighter constant factors for small variance
```

See [Skills Reference](../reference/skills.md) for the full skill system documentation.
