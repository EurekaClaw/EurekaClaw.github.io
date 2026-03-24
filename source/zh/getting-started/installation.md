# 安装

**支持平台：** macOS, Linux, Windows

```{note}
Windows installer可用（请参见下文）。如果遇到问题，请安装[WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install)（Ubuntu）并遵循WSL终端内部的macOS/Linux说明。
```

## 安装方式（推荐）

**macOS / Linux**

```bash
curl -fsSL https://eurekaclaw.ai/install.sh | bash
```

**Windows**

```powershell
powershell -c "irm https://eurekaclaw.ai/install_win.ps1 | iex"
```

macOS/Linux安装程序复制项目仓库，创建虚拟环境，安装EurekaClaw，并将 `eurekaclaw` 命令添加到路径中。然后运行 `eurekaclaw onboard` 来配置API密钥和设置。

## 手动安装

**要求：** Python ≥ 3.11, Node.js ≥ 20, Git

```bash
git clone https://github.com/EurekaClaw/EurekaClaw
cd EurekaClaw
make install                  # pip install -e "." + npm install (frontend)
```

## 额外功能安装

```bash
pip install -e ".[openai,oauth]"
```

| 安装选项 | 功能 |
|---|---|
| `openai` | OpenRouter和本地vLLM/Ollama后端 |
| `oauth` | 通过ccproxy登录Claude Pro/Max（无需API Key） |
| `pdf` | 通过Docling (`PaperReader`)进行完整PDF生成 |

## 可选系统工具

以下工具都是可选工具：

| Tool | Purpose | Install |
|---|---|---|
| **pdflatex** + bibtex | Compile `paper.tex` → `paper.pdf` | TeX Live / MacTeX |
| **Lean4** | Formal proof verification | [leanprover.github.io](https://leanprover.github.io) |
| **clawhub** | Install skills from ClawHub registry | `pip install clawhub` |

```{note}
**Docker / 沙盒代码执行** 作为可选工具列出，目前为**试用版**-实验运行程序和 `execute_python` 工具尚未安全地放入沙盒中供一般使用。可以设置`EXPERIMENT_MODE=false`。
```

## 安装种子技能

此代码可以安装种子技能到技能库：

```bash
eurekaclaw install-skills
```

此代码只需要运行一次，技能存储在 `~/.eurekaclaw/skills/` 中，并自动用于后续运行。

## 验证安装

```bash
eurekaclaw --help
eurekaclaw skills        # lists available seed skills
```
