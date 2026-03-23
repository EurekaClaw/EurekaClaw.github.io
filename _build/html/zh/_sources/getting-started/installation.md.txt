# 安装

**支持平台：** macOS, Linux, Windows

```{note}
Native Windows support is under active development. A Windows installer is available (see below) but not yet fully supported. If you run into issues, install [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/install) (Ubuntu) and follow the macOS/Linux instructions inside the WSL terminal.
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

After installation, copy the bundled seed skills to your local skill bank:

```bash
eurekaclaw install-skills
```

This is a one-time step. Skills are saved to `~/.eurekaclaw/skills/` and automatically used by agents on future runs.

## 验证安装

```bash
eurekaclaw --help
eurekaclaw skills        # lists available seed skills
```
