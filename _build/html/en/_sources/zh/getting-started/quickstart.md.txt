# 快速开始

5分钟从零生成论文

## 1. 安装

**macOS / Linux**

```bash
curl -fsSL https://eurekaclaw.ai/install.sh | bash
eurekaclaw onboard            # interactive setup wizard (creates .env)
```

**Windows**

```powershell
powershell -c "irm https://eurekaclaw.ai/install_win.ps1 | iex"
```

**手动安装（全平台）**

```bash
git clone https://github.com/EurekaClaw/EurekaClaw
cd EurekaClaw
make install                  # pip install -e "." + npm install (frontend)
cp .env.example .env
```

编辑 `.env` 并加上API Key（例如 `ANTHROPIC_API_KEY`，参见 [授权](authentication.md)）.

## 2. 安装技能

```bash
eurekaclaw install-skills
```

> **此操作为必要操作。** 此步骤下载EurekaClaw需要运行的内置种子技能（证明策略、领域限定、引理模板）。跳过它将导致`No skills available`（没有可用技能）并导致证明失败，或产生严重的能力下降。

## 3. 证明定理

```bash
eurekaclaw prove "The sum of the first n natural numbers equals n(n+1)/2" \
    --domain "combinatorics" --output ./results
```

预期输出

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

## 4. 读取输出

打开 `./results/<session_id>/paper.pdf` 读取编译好的论文，或者参考下面的输出文件：

| File | Contains |
|---|---|
| `paper.pdf` | Compiled PDF (needs pdflatex + bibtex) |
| `paper.tex` | Full LaTeX source |
| `theory_state.json` | Proof state — lemmas, confidence scores |
| `research_brief.json` | Planning state |

## 下一步...

::::{grid} 1 2 2 3
:gutter: 2

:::{grid-item-card} 📖 用户指南
:link: ../user-guide/index
:link-type: doc

了解所有三种输入模式、门控设计和设置选项。
:::

:::{grid-item-card} ⚙️ 配置
:link: ../reference/configuration
:link-type: doc

通过`.env`设置模型、Token限制和流程控制。
:::

:::{grid-item-card} 🌐 浏览器UI界面
:link: ../user-guide/browser-ui
:link-type: doc

启动实时进度和设置滑块的可视化界面。
:::

::::
