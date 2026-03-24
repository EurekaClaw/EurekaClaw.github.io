# 智能体

EurekaClaw 包含五个专职智能体，由 `MetaOrchestrator` 统一调度。每个智能体运行一个工具调用循环，并定期对上下文进行压缩。

## BaseAgent

所有智能体均继承自 `eurekaclaw/agents/base.py`：

**核心方法：**

| 方法 | 说明 |
|---|---|
| `execute(task: Task) -> AgentResult` | 抽象方法。在给定任务上运行智能体 |
| `get_tool_names() -> list[str]` | 抽象方法。返回该智能体允许使用的工具名称列表 |
| `build_system_prompt(task: Task) -> str` | 合并角色提示词与注入的技能 |
| `run_agent_loop(task, initial_user_message, max_turns, max_tokens)` | 带上下文压缩的工具调用循环 |
| `_compress_history() -> str` | 每隔 N 轮使用快速模型对对话历史进行摘要 |
| `_call_model(system, messages, tools, max_tokens)` | 带指数退避重试的 LLM 调用 |

**上下文压缩：** 每隔 `CONTEXT_COMPRESS_AFTER_TURNS` 轮（默认 6 轮），当历史消息超过 12 条时，使用快速模型将其压缩为单条摘要。这可将长时运行中的输入 token 增长控制在合理范围内。

---

## SurveyAgent

**角色：** `SURVEY`
**文件：** `eurekaclaw/agents/survey/agent.py`
**最大轮次：** `SURVEY_MAX_TURNS`（默认 8）

**功能：** 检索文献，并将论文、开放问题及关键数学对象填充到 KnowledgeBus。

**工具：**
- `arxiv_search` — 在 arXiv 上检索相关论文
- `semantic_scholar_search` — 在 Semantic Scholar 上检索引用数和元数据
- `web_search` — 补充通用网络搜索
- `citation_manager` — 格式化并存储参考文献

**输入（来自 KnowledgeBus）：**
- `ResearchBrief.domain`
- `ResearchBrief.query`
- `ResearchBrief.conjecture`

**输出：**
- 将论文追加到总线上的 `Bibliography`
- 写入 `ResearchBrief`：
  - `open_problems` — 识别出的开放问题列表
  - `key_mathematical_objects` — 核心概念与结构

**输出 JSON 键：** `papers`、`open_problems`、`key_mathematical_objects`、`research_frontier`、`insights`

---

## IdeationAgent

**角色：** `IDEATION`
**文件：** `eurekaclaw/agents/ideation/agent.py`
**最大轮次：** 3

**功能：** 基于调研结果生成 5 个新颖的研究假设。每个方向在 `novelty_score`、`feasibility_score` 和 `impact_score` 三个维度上打分（内部映射到 `ResearchDirection` 的 `novelty_score`、`soundness_score`、`transformative_score` 字段）。

研究方向*选择*不在 IdeationAgent 内部完成。IdeationAgent 将 `ResearchBrief.directions` 写入后，编排器的 `direction_selection_gate` 任务会调用 `DivergentConvergentPlanner.converge()` 选出得分最高的方向，并设置 `ResearchBrief.selected_direction`。

**输入（来自 KnowledgeBus）：**
- 调研结果（`ResearchBrief`）
- `Bibliography`

**输出：**
- `ResearchBrief.directions` — 5 个带综合评分的 `ResearchDirection` 对象

---

## TheoryAgent

**角色：** `THEORY`
**文件：** `eurekaclaw/agents/theory/agent.py`
**最大迭代次数：** `THEORY_MAX_ITERATIONS`（默认 10）
**内层阶段最大轮次：** `THEORY_STAGE_MAX_TURNS`（默认 6）

**功能：** 通过 7 阶段自底向上的证明流水线，证明选定的研究方向。

**工具：**
- `arxiv_search` — 从论文中检索引理和技术方法
- `wolfram_alpha` — 符号计算与界的验证
- `lean4_verify` — 在 Lean4 中进行形式化证明验证
- `execute_python` — 数值检验与合理性测试

**输入（来自 KnowledgeBus）：**
- `ResearchBrief.selected_direction`

**输出：**
- `TheoryState`，其中 `status` 为 `proved` / `refuted` / `abandoned`

**7 阶段内层循环**（`inner_loop_yaml.py`）：

| 阶段 | 类 | 输入 | 输出 |
|---|---|---|---|
| 1 | `PaperReader` | `Bibliography` | `known_results[]` |
| 2 | `GapAnalyst` | known_results + conjecture | `research_gap` |
| 3 | `ProofArchitect` | research_gap + known_results | `proof_plan[]`（带来源标注） |
| 4 | `LemmaDeveloper` | proof_plan, open_goals | `proven_lemmas{}` |
| 5 | `Assembler` | proven_lemmas | `assembled_proof` |
| 6 | `TheoremCrystallizer` | assembled_proof | `formal_statement` |
| 7 | `ConsistencyChecker` | 完整 TheoryState | 一致性报告 |

**LemmaDeveloper 内层循环**（逐引理）：
```
for each open_goal:
    Prover → Verifier → (if failed) Refiner → repeat
    CounterexampleSearcher runs in parallel
    Stagnation detection: if same error N times → force Refiner
```

**来源标注系统：** 证明计划中的每个引理均被标注为 `known`（可直接引用）、`adapted`（需修改）或 `new`（必须完整证明）。只有 `adapted` 和 `new` 引理进入证明循环。

**自动验证：** 置信度大于等于 `AUTO_VERIFY_CONFIDENCE`（默认 0.95）的证明无需调用 LLM 验证器即可被接受。LLM 验证器本身使用独立的通过阈值 `VERIFIER_PASS_CONFIDENCE`（默认 0.90）。

**ProofArchitect 重试策略：** 若完整的带来源标注计划失败（例如 LLM 将某字段返回为 `null`），则使用简化的 3 引理提示词重试（基础引理 → 核心界 → 主要结论）。只有两次尝试均失败时，才回退到单个 `main_result` 目标。

**外层迭代循环：** Assembler 运行后，`TheoremCrystallizer` + `ConsistencyChecker` 最多迭代 `theory_max_iterations` 次。`ConsistencyChecker` 将每次失败分为三个严重级别，并据此选择重试路径：

| 严重级别 | 含义 | 重试路径 |
|---|---|---|
| `uncited` | 证明逻辑正确，但已证明引理未在汇总文本中被引用 | 内联重新运行 `TheoremCrystallizer`，随即将证明标记为 `proved` 并退出外层循环——**不进行第二次 ConsistencyChecker 检验** |
| `major` | 某个引理不正确，或两个引理之间的逻辑关联断裂 | 重新运行 `LemmaDeveloper → Assembler → TheoremCrystallizer → ConsistencyChecker`（一次尝试）。若仍失败，升级为 `all_wrong` |
| `all_wrong` | 证明根本性失败——思路错误或多个引理不正确 | 从 `ProofArchitect`（新证明计划）重新运行完整流水线 |

若 LLM 未返回严重级别字段，则启发式推断：仅含 `uncited_lemmas` 且无 `issues` 的失败归类为 `uncited`；其余均归类为 `major`。

**引用约定：** Assembler 被要求在汇总证明中使用方括号引用每个已证明引理的标识符，例如 `By [arm_pull_count_bound], ...`。ConsistencyChecker 验证所有已证明引理的 ID 是否出现在汇总证明中，并标出缺失的部分。

**知识图谱写入：** 无论最终一致性检查是否通过，只要引理被证明，引理节点和依赖边就会写入 Tier 3 知识图谱。即使定理语句结晶化失败，引理级别的图也会被保留。

---

## ExperimentAgent *（开发中）*

```{note}
ExperimentAgent 及 `execute_python` 工具属于**未来工作**。针对 LLM 生成的 Python 代码进行自动化执行，目前尚未为通用场景提供安全的沙箱隔离。在未来版本正式引入沙箱之前，请将 `EXPERIMENT_MODE` 保持为 `false`。
```

**角色：** `EXPERIMENT`
**文件：** `eurekaclaw/agents/experiment/agent.py`
**最大轮次：** 5

**功能：** 通过数值实验对理论界进行实证验证，尤其针对置信度较低的引理。

**工具：**
- `execute_python` — 运行数值模拟*（未来工作——见上方说明）*
- `wolfram_alpha` — 符号界检验
- 领域特定工具（例如 MAB 领域的 `run_bandit_experiment`）

**自动跳过逻辑：** 智能体在运行前检查 `TheoryState.formal_statement` 中的定量信号：
- **运行实验：** `O(`、`\Omega(`、不等式运算符、`sample complexity`、`regret`、收敛/泛化相关词汇
- **跳过：** `\exists`、存在量词、纯代数/组合结构

**低置信度引理测试：**
- 将 `proven_lemmas` 分为 `verified` 和 `low_confidence` 两组
- 对每个低置信度引理：随机采样实例，检验结论是否成立，计算 `violation_rate`
- `violation_rate > 1%` 的引理被标记为 `numerically_suspect`

**输入（来自 KnowledgeBus）：**
- `TheoryState`（已证明引理、形式语句）

**输出：**
- KnowledgeBus 上的 `ExperimentResult`，包含 `alignment_score` 及逐引理检验结果

---

## WriterAgent

**角色：** `WRITER`
**文件：** `eurekaclaw/agents/writer/agent.py`
**最大轮次：** `WRITER_MAX_TURNS`（默认 4）

**功能：** 基于所有流水线产物，生成完整的 LaTeX（或 Markdown）格式学术论文。

**工具：**
- `citation_manager` — 格式化参考文献条目并生成一致的引用键

**输入（来自 KnowledgeBus）：**
- `ResearchBrief`（领域、猜想、选定方向）
- `TheoryState`（所有证明、引理、形式语句）
- `Bibliography`（带精确引用键的论文列表）
- `ExperimentResult`（如有）

**输出：**
- 存储于 `ResearchOutput` 中的 `latex_paper` 字符串

**LaTeX 特性：**
- 完整的 `LATEX_PREAMBLE`，包含 13 个定理环境：`theorem`、`lemma`、`corollary`、`definition`、`proposition`、`assumption`、`conjecture`、`claim`、`example`、`fact`、`observation`、`maintheorem`、`remark`
- 常用数学宏：`\R`、`\N`、`\Z`、`\E`、`\Prob`、`\softmax`、`\Att`、`\argmax`、`\argmin`、`\norm`、`\abs`、`\inner`

**`_extract_latex` 规范化流水线：**
1. 去除前言 / `\begin{document}` / `\end{document}` 包装
2. 规范化环境名称（`\begin{Proof}` → `\begin{proof}`，`rem` → `remark`，`prop` → `proposition` 等）
3. 将 Markdown 标题转换为 LaTeX 章节命令
4. 移除 `tikzpicture` 环境及空的 `figure` 环境
5. 修复语法错误（`\begin lemma}` → `\begin{lemma}`，`\begin{flushright` → `\begin{flushright}` 等）
6. 将 `\endproof` 替换为 `\end{proof}`
7. 移除手动 QED 框（`\begin{flushright}$\square$\end{flushright}`）
8. 从正文中去除 `\bibliographystyle` 和 `\bibliography` 行
9. 关闭未闭合的环境（两轮处理：先移除孤立的 `\end{X}`，再补充缺失的环境结束标记）

**证明风格强制执行**（`ENFORCE_PROOF_STYLE=true`）：
- 禁止在没有立即理由的情况下使用省略词（"clearly"、"trivially"、"by standard arguments"）
- 每个不等式必须注明所用引理或定理
- 每个引理证明以非正式直觉作为开头
- 低置信度引理用 `\textcolor{orange}{[Unverified step]}` 标注
- 局限性章节对所有未验证步骤进行说明

**引用一致性：** 写作提示词中每个参考文献均使用 `\cite{key}` 形式，且与 `main.py` 中 `_generate_bibtex` 采用相同的键生成算法。
