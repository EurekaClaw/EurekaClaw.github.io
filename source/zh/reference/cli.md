# CLI 参考

安装软件包（或运行 `python -m eurekaclaw`）后即可使用 `eurekaclaw` 命令。

## 全局选项

| 参数 | 说明 |
|---|---|
| `--verbose`, `-v` | 启用 DEBUG 日志 |

---

## 命令

### `prove` — 证明猜想

```bash
eurekaclaw prove "<conjecture>" [OPTIONS]
```

**参数：**
- `conjecture` — 要证明的数学猜想或命题（字符串）

**选项：**

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--domain`, `-d` | `""` | 研究领域。若省略，则从猜想自动推断 |
| `--mode` | `skills_only` | 运行后学习模式：`skills_only`、`rl`、`madmax` |
| `--skills` | *(all)* （全部） | 按名称固定特定技能（可重复使用）。固定技能始终优先出现在注入列表前面，不受使用分数影响 |
| `--gate` | `none` | 关卡控制：`human`、`auto`、`none` |
| `--output`, `-o` | `./results` | 产物输出目录 |

**示例：**
```bash
eurekaclaw prove "UCB1 achieves O(sqrt(KT log T)) expected cumulative regret in the stochastic multi-armed bandit setting" \
  --domain "multi-armed bandit theory" \
  --skills ucb_regret_analysis --skills concentration_inequalities \
  --gate human \
  --output ./results
```

---

### `explore` — 探索研究领域

```bash
eurekaclaw explore "<domain>" [OPTIONS]
```

**参数：**
- `domain` — 要探索的研究领域（字符串）

**选项：**

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--query`, `-q` | `""` | 领域内的具体研究问题 |
| `--mode` | `skills_only` | 运行后学习模式：`skills_only`、`rl`、`madmax` |
| `--gate` | `none` | 关卡控制：`human`、`auto`、`none` |
| `--output`, `-o` | `./results` | 产物输出目录 |

**示例：**
```bash
eurekaclaw explore "multi-armed bandit theory" \
  --query "tight regret bounds for heavy-tailed rewards" --output ./results
```

---

### `from-papers` — 从参考论文生成假设

```bash
eurekaclaw from-papers <paper_id> [<paper_id> ...] [OPTIONS]
```

**参数：**
- `paper_ids` — 一个或多个 arXiv ID 或 Semantic Scholar ID（可变参数）

**选项：**

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--domain`, `-d` | *（必填）* | 研究领域 |
| `--query`, `-q` | `""` | 论文范围内的具体研究问题或聚焦方向 |
| `--mode` | `skills_only` | 运行后学习模式 |
| `--skills` | *(all)* （全部） | 按名称固定特定技能（可重复使用）。固定技能始终优先出现在注入列表前面，不受使用分数影响 |
| `--gate` | `none` | 关卡控制 |
| `--output`, `-o` | `./results` | 输出目录 |

**示例：**
```bash
eurekaclaw from-papers 1602.01783 2301.00774 \
  --domain "bandit algorithms" --output ./results
```

---

### `pause` — 暂停正在运行的会话

```bash
eurekaclaw pause <session_id>
```

**参数：**
- `session_id` — 要暂停的正在运行的证明的会话 ID（在启动时的控制台头部可以找到）

在 `~/.eurekaclaw/sessions/<session_id>/` 中写入 `pause.flag` 文件。理论智能体在下一个阶段边界检测到该标志后，保存检查点并以 `ProofPausedException` 干净退出。部分证明状态保存在 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json` 中。

运行期间也可以按 **Ctrl+C** 暂停。EurekaClaw 会拦截 `SIGINT` 并写入暂停标志，而非直接抛出 `KeyboardInterrupt`，给智能体留出到达干净检查点边界的时间。

**示例：**
```bash
# In a separate terminal while a proof is running:
eurekaclaw pause abc12345
```

---

### `resume` — 恢复已暂停的会话

```bash
eurekaclaw resume <session_id>
```

**参数：**
- `session_id` — 要继续的已暂停证明的会话 ID

从 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json` 加载检查点，并从保存的阶段重新运行理论智能体，此时所有之前已证明的引理均已在 `TheoryState` 中。使用与原始会话相同的领域和查询。

**示例：**
```bash
eurekaclaw resume abc12345
```

---

### `replay-theory-tail` — 重放理论尾部阶段

```bash
eurekaclaw replay-theory-tail <session_id> [OPTIONS]
```

**参数：**
- `session_id` — 已完成运行的会话 ID

**选项：**

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--from` | `consistency_checker` | 重新启动的阶段：`assembler`、`theorem_crystallizer`、`consistency_checker` |

从已保存的 `theory_state.json` 重新运行理论流水线的最终阶段（Assembler → TheoremCrystallizer → ConsistencyChecker），无需重复调研、规划或引理证明阶段。适用于快速迭代结晶化或一致性检查失败的情况。

**示例：**
```bash
eurekaclaw replay-theory-tail abc12345 --from assembler
```

---

### `test-paper-reader` — 对单篇论文测试 PaperReader

```bash
eurekaclaw test-paper-reader <session_id> <paper_ref> [OPTIONS]
```

**参数：**
- `session_id` — 要使用其参考文献列表的已完成运行的会话 ID
- `paper_ref` — 论文 ID、arXiv ID，或标题的大小写不敏感子字符串

**选项：**

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--mode` | `both` | 提取模式：`abstract`、`pdf`、`both` |
| `--direction` | `""` | 提取提示词的研究方向覆盖 |

对单条参考文献条目执行 PaperReader 的摘要和/或 PDF 提取，无需运行完整流水线。

**示例：**
```bash
eurekaclaw test-paper-reader abc12345 "UCB1" --mode both
```

---

### `onboard` — 交互式配置向导

```bash
eurekaclaw onboard [OPTIONS]
```

**选项：**

| 选项 | 说明 |
|---|---|
| `--non-interactive` | 不提示直接写入默认值 |
| `--reset` | 覆盖现有 `.env` 而不合并 |
| `--env-file` | 要写入的 `.env` 文件路径（默认：`.env`） |

引导您完成 LLM 后端选择、API 密钥配置、搜索工具设置及系统行为配置，然后写入（或更新）`.env` 文件。

**示例：**
```bash
eurekaclaw onboard
eurekaclaw onboard --env-file ~/.eurekaclaw/.env
```

---

### `skills` — 列出可用技能

```bash
eurekaclaw skills
```

打印一个 Rich 面板，列出技能库中所有技能及其：
- 技能名称
- 标签
- 说明
- 来源（`seed`、`distilled` 或 `manual`）

---

### `eval-session` — 评估已完成的会话

```bash
eurekaclaw eval-session <session_id>
```

**参数：**
- `session_id` — 之前运行的会话 ID（在运行目录名称中可以找到）

打印包含证明质量指标的评估报告。

---

### `install-skills` — 安装种子技能

```bash
eurekaclaw install-skills [SKILLNAME] [--force]
```

**参数：**
- `skillname` *（可选）* — 按名称从 clawhub 安装特定技能

**选项：**

| 选项 | 说明 |
|---|---|
| `--force`, `-f` | 覆盖 `~/.eurekaclaw/skills/` 中现有技能 |

不带参数时，将包内所有种子技能复制到 `~/.eurekaclaw/skills/`。若提供了技能名称，则从 clawhub 下载该技能。

---

### `ui` — 启动浏览器 UI

```bash
eurekaclaw ui [OPTIONS]
```

**选项：**

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--host` | `127.0.0.1` | 绑定的网络接口 |
| `--port` | `8080` | 监听端口 |
| `--open-browser` / `--no-open-browser` | False | 启动时是否自动打开浏览器 |

**示例：**
```bash
eurekaclaw ui --open-browser
```

---

## 输出产物

三个研究命令（`prove`、`explore`、`from-papers`）均将产物写入 `<output>/<session_id>/`：

```
<output>/<session_id>/
├── paper.tex              LaTeX source
├── paper.pdf              Compiled PDF (requires pdflatex + bibtex)
├── references.bib         Bibliography in BibTeX format
├── theory_state.json      Full proof state (lemmas, proofs, status)
├── research_brief.json    Planning state (directions, selected direction)
└── experiment_result.json Numerical validation results (if run)
```

已暂停的会话还会将检查点写入 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`。

## 理论评审关卡

TheoryAgent 完成后、Writer 运行前，EurekaClaw 会显示带编号的证明草稿并请求确认：

```
──────────────── Proof Sketch Review ────────────────
  L1  [✓] arm_pull_count_bound  verified
       For arm a with mean gap Δ_a ...
  L2  [~] regret_decomposition  low confidence
       Total regret decomposes as ...
  L3  [✓] main_theorem          verified
       UCB1 achieves O(√(KT log T)) regret ...
──────────────────────────────────────────────────────

Does this proof sketch look correct?
  y  — Proceed to writing
  n  — Flag the most logically problematic step
→
```

- **y / 回车** — 继续执行 WriterAgent
- **n** — 系统询问哪个步骤存在最关键的逻辑缺口（例如 `L2` 或完整引理 ID），以及问题描述。TheoryAgent 会将您的反馈注入任务后重新运行一次，然后再次展示更新后的草稿。

理论评审关卡**始终显示**，不受 `--gate` 模式影响。

## 退出码

| 代码 | 含义 |
|---|---|
| `0` | 成功——论文已生成 |
| `1` | 运行时错误（详见控制台输出） |
