# 技能和持续学习

## What Are Skills?

技能是 Markdown 文件，其中编码了成功的证明策略、领域内的惯例和常用技巧。它们会在每次任务执行前注入到代理提示词中，从而无需重新训练模型即可提升结果。

技能文件位于 `~/.eurekaclaw/skills/` 目录下。

## 查看您的技能

```bash
eurekaclaw skills
```

## 安装内置技能

```bash
eurekaclaw install-skills
eurekaclaw install-skills --force   # overwrite existing
```

## 从 ClawHub 安装

```bash
eurekaclaw install-skills steipete/github
```

从 [ClawHub](https://clawhub.ai/) 下载。需要 `clawhub` 命令行界面。

## EurekaClaw 如何学习

每次学习结束后，`ContinualLearningLoop` 都会自动运行。它：
1. 从会话中提取独特的故障模式
2. 运用大语言模型提炼成功的证明策略
3. 将新的 `.md` 技能文件写入 `~/.eurekaclaw/skills/` 目录

这些新技能将在以后的课程中自动应用。

## 学习模式

在 `.env` 文件中设置 `EUREKACLAW_MODE`：

| 模式 | 每次会话结束后运行的内容 |
|---|---|
| `skills_only` (默认) | 将失败结果提炼成新的技能文件 |
| `rl` | 技能提炼 + 过程奖励模型对证明轨迹进行评分 |
| `madmax` | 技能提炼 + PRM 评分 + 云端 LoRA 微调 (GRPO) |

## 手动写作技巧

在 `~/.eurekaclaw/skills/` 目录下创建一个 `.md` 文件：

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

# 样例：Azuma 与 Bernstein 

在以下情况下使用 Azuma-Hoeffding 算法：
- 有界差分条件成立
- 方差未知

在以下情况下使用Bernstein定理：
- 你已经设定了方差的上限
- 对于小方差，可提供更精确的常数因子
```

有关完整的技能系统文档，请参阅[技能参考](../reference/skills.md)。
