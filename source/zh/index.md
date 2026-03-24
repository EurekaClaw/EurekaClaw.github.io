---
myst:
  html_meta:
    description: "EurekaClaw-捕捉你的Eureka瞬间的AI。多智能体研究助理，证明定理，撰写论文，并从每次对话中学习。"
    keywords: "AI, 定理证明, 研究助手, arXiv, LaTeX, 多智能体"
---

# EurekaClaw 文档

<p align="center">
<strong>捕捉你的Eureka瞬间的AI。</strong><br/>
爬取 arXiv · 生成定理 · 证明引理 · 编写LaTeX论文 · 进行实验
</p>

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 🚀 快速开始
:link: zh/getting-started/quickstart
:link-type: doc

5分钟上手EurekaClaw：安装、设置API并证明第一个定理！
:::

:::{grid-item-card} 📖 用户指南
:link: zh/user-guide/index
:link-type: doc

详细指南，包括输入模式、门控机制、输出文件、系统调优、错误索引和样例。
:::

:::{grid-item-card} ⚙️ 配置
:link: zh/reference/configuration
:link-type: doc

所有`.env`环境变量：后端、模型、Token限制、流水线模式和重试设置。
:::

:::{grid-item-card} 🖥️ CLI 参考
:link: zh/reference/cli
:link-type: doc

EurekaClaw命令行界面的命令、选项和退出代码。
:::

:::{grid-item-card} 🏗️ 系统架构
:link: zh/reference/architecture
:link-type: doc

流水线阶段、智能体设计、数据流、LaTeX编译和推理循环。
:::

:::{grid-item-card} 🌐 浏览器UI界面
:link: zh/user-guide/browser-ui
:link-type: doc

打开UI虚拟界面：实时智能体追踪、中断/继续、门控界面、技能管理、设置界面。
:::

::::

---

## EurekaClaw能做什么

EurekaClaw是一个**多智能体人工智能研究助手**，可以自主地从一个开放问题生成一个可发布的结果。EurekaClaw能爬取文献，提出假设并进行检验，运行实验，并生成调查结果。

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

:::{grid-item-card} 🔍 文献爬取
检索、总结和交叉引用arXiv和Semantic Scholar的论文。
:::

:::{grid-item-card} 💡 想法生成
通过综合数千篇论文中的想法，集思广益地提出新的假设。
:::

:::{grid-item-card} 🔢 定理证明
通过7级自下而上的管道生成、验证和形式化证明定理。
:::

:::{grid-item-card} 📄 论文写作
起草LaTeX论文并配好定理环境和引用。
:::

:::{grid-item-card} 🖥️ 本地运行
兼容每一个主要的模型API，保护隐私。
:::

:::{grid-item-card} 🧠 持续学习
每次对话结束后，将证明策略提炼为技能，随着时间的推移系统不断优化。
:::

:::{grid-item-card} 🧪 实验运行
用实验结果验证理论；识别并标出低可信度的引理。
:::

:::{grid-item-card} 🌐 浏览器UI界面
具有实时进度、滑块设置和结果查看的可视化界面。
:::

::::

---

## 安装

**macOS / Linux**

```bash
curl -fsSL https://eurekaclaw.ai/install.sh | bash
eurekaclaw onboard            # interactive setup wizard
```

**Windows Powershell**

```powershell
powershell -c "irm https://eurekaclaw.ai/install_win.ps1 | iex"
```

**手动安装（全平台）**

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

> 没有API Key？EurekaClaw支持Claude Pro/Max订阅：[OAuth](zh/getting-started/authentication.md).

---

## 文档

```{toctree}
:maxdepth: 2
:caption: 快速开始

getting-started/installation
getting-started/quickstart
getting-started/authentication
```

```{toctree}
:maxdepth: 2
:caption: 用户指南

user-guide/index
```

```{toctree}
:maxdepth: 2
:caption: 参考文档

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
:caption: 开发日志

changelog/index
```

---

## 致谢

EurekaClaw站在AI智能体开发和AI赋能的科学研究成果的肩膀上。我们感谢以下项目的作者：

- [MetaClaw](https://github.com/aiming-lab/MetaClaw) — multi-agent research orchestration
- [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) — automated research orchestration
- [EvoScientist](https://github.com/EvoScientist/EvoScientist) — evolutionary hypothesis generation
- [AI-Researcher](https://github.com/hkuds/ai-researcher) — automated research pipeline
- [Awesome AI for Science](https://github.com/ai-boost/awesome-ai-for-science) — curated resource list
- [Dr. Claw](https://github.com/OpenLAIR/dr-claw) — open research agent framework
- [OpenClaw](https://github.com/openclaw/openclaw) — open-source research claw
- [ClawTeam](https://github.com/HKUDS/ClawTeam) — collaborative research agents
- [ScienceClaw](https://github.com/beita6969/ScienceClaw) — science-focused research agent
