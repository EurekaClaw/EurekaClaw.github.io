# 用户指南

使用EurekaClaw从安装到生成您的第一篇生成的论文。

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

## 功能一览

EurekaClaw有三种输入模式，具体取决于目标的具体程度：

| 模式 | 命令 | 使用场合 |
|---|---|---|
| **证明** | `eurekaclaw prove "<conjecture>"` | 你有一个精确的数学陈述 |
| **参考论文** | `eurekaclaw from-papers <ids>` | 要基于特定论文 |
| **浏览** | `eurekaclaw explore "<domain>"` | 你想探索开放问题 |

系统运行过后，文件生成于 `./results/<session_id>/` ，包括LaTeX文件、编译的PDF、证明描述和引用文献。

## 可用选项

| 选项 | 默认 | 描述 |
|---|---|---|
| `--domain`, `-d` | `""` | 研究领域（开启领域特定工具和技能） |
| `--output`, `-o` | `./results` | 输出文档 |
| `--gate` | `none` | `none` / `auto` / `human` 人类需要介入多少 |
| `--mode` | `skills_only` | 系统运行后怎么学习新技能 `skills_only`, `rl`, `madmax` |
| `--verbose`, `-v` | — | 开启 DEBUG 日志记录 |
