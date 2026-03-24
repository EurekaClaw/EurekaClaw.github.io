# 系统结构

## 概述

EurekaClaw 以**多智能体流水线**形式组织，由 `MetaOrchestrator` 统一调度。每个智能体专注于研究生命周期的某一阶段，产物通过中央 `KnowledgeBus` 在智能体之间共享。

## 流水线阶段

```{image} ../_static/images/pipeline-main.svg
:alt: EurekaClaw Main Pipeline
:width: 100%
:align: center
```

## 核心组件

### KnowledgeBus

所有智能体共享的中央内存产物存储。所有数据通过它流转——智能体在轮次之间不保留私有状态。

```
KnowledgeBus
├── ResearchBrief    — survey findings, selected direction
├── TheoryState      — proof state machine (lemma DAG, proofs, goals)
├── Bibliography     — all papers found during survey
├── ExperimentResult — numerical validation results
└── TaskPipeline     — current task execution plan
```

产物在每次会话结束时持久化到 `~/.eurekaclaw/runs/<session_id>/`。

### 智能体会话与上下文压缩

每个智能体在工具调用循环中维护一段对话历史（`AgentSession`）。为防止上下文无限增长：
- 历史每隔 N 轮**压缩一次**（通过 `CONTEXT_COMPRESS_AFTER_TURNS` 配置，默认 6）
- 快速模型将历史压缩为要点摘要
- 完整对话被替换为该摘要

### 技能注入

每次调用智能体之前，`SkillInjector` 从技能库中检索最相关的前 k 个技能，并以示例形式注入系统提示词。这是跨会话学习的主要机制。

### 领域插件系统

领域特定的行为（工具、技能、工作流提示）通过 `DomainPlugin` 类注入。正确的插件根据领域字符串或猜想关键词自动检测。详见 [domains.md](domains.md)。

## 数据模型

### TheoryState — 证明状态机

```
TheoryState
├── informal_statement      — plain-English conjecture
├── formal_statement        — LaTeX-formalized theorem
├── known_results[]         — KnownResult extracted from literature
├── research_gap            — GapAnalyst's finding
├── proof_plan[]            — ProofPlan (provenance: known/adapted/new)
├── lemma_dag{}             — LemmaNode graph (dependencies)
├── proven_lemmas{}         — lemma_id → ProofRecord
├── open_goals[]            — remaining lemma_ids to prove
├── failed_attempts[]       — FailedAttempt history
├── counterexamples[]       — Counterexample discoveries
├── assembled_proof         — final combined proof text
└── status                  — pending/in_progress/proved/refuted/abandoned
```

### ResearchBrief — 规划状态

```
ResearchBrief
├── domain, query, conjecture
├── directions[]            — ResearchDirection (scored 0-1)
│     ├── novelty_score
│     ├── soundness_score
│     ├── transformative_score
│     └── composite_score   — weighted average
├── selected_direction      — chosen after convergence
└── open_problems[], key_mathematical_objects[]
```

## TheoryAgent 内层循环（7 阶段）

`TheoryAgent` 运行一个**自底向上的证明流水线**，实现于 `inner_loop_yaml.py`：

| 阶段 | 类 | 输入 | 输出 |
|---|---|---|---|
| 1 | `PaperReader` | Bibliography | `known_results[]` |
| 2 | `GapAnalyst` | known_results + conjecture | `research_gap` |
| 3 | `ProofArchitect` | research_gap | `proof_plan[]`（带来源标注） |
| 4 | `LemmaDeveloper` | proof_plan, open_goals | `proven_lemmas{}` |
| 5 | `Assembler` | proven_lemmas | `assembled_proof` |
| 6 | `TheoremCrystallizer` | assembled_proof | `formal_statement` |
| 7 | `ConsistencyChecker` | 完整 TheoryState | 一致性报告 |

`LemmaDeveloper` 对每个引理运行独立的内层循环：

```{image} ../_static/images/pipeline-theory.svg
:alt: TheoryAgent Inner Loop and LemmaDeveloper Sub-Loop
:width: 100%
:align: center
```

## LaTeX 编译流水线

```{image} ../_static/images/pipeline-latex.svg
:alt: LaTeX Compilation Pipeline
:width: 90%
:align: center
```

## 方向规划回退机制

`IdeationAgent` 运行后，`MetaOrchestrator._handle_direction_gate()` 调用 `DivergentConvergentPlanner.diverge()` 生成 5 个研究方向。若规划器失败或返回空列表（例如 LLM 解析错误、API 超时），编排器不会静默地以无方向继续执行，而是**暂停并提示用户**：

1. 打印调研发现的最多 5 个开放问题作为上下文。
2. 请求用户手动输入一个假设/方向。
3. 根据输入构建 `ResearchDirection` 并写入 `ResearchBrief`。
4. 若用户未输入任何内容或按下 Ctrl+C，则抛出 `RuntimeError`，会话干净退出。

该逻辑实现于 `meta_orchestrator.py` 的 `_handle_manual_direction()` 中。

## 理论评审关卡

TheoryAgent 完成后、WriterAgent 运行前，`MetaOrchestrator` 执行 `theory_review_gate` 编排器任务。该关卡**独立于 `gate_mode`**，始终触发。

**流程：**
1. `GateController.theory_review_prompt()` 打印带编号的引理列表，每个已证明引理标注 `✓ verified` / `~ low confidence`，并显示所有未解决目标。
2. 询问用户：**y**（继续）或 **n**（标记最有问题的步骤）。
3. 拒绝时：
   - 用户输入引理编号（`L3`）或 ID，以及逻辑缺口的描述。
   - `MetaOrchestrator._handle_theory_review_gate()` 找到理论任务，将反馈以 `[User feedback]: ...` 形式注入，将任务重置为 `PENDING`，并重新运行 TheoryAgent 一次。
   - 修订后再次展示更新后的草稿（不再进一步重试）。
4. 第二次拒绝时，流水线仍会继续推进到 WriterAgent，并显示警告。

## 暂停 / 恢复

TheoryAgent 通过 `ProofCheckpoint`（`agents/theory/checkpoint.py`）支持在阶段边界优雅暂停。

**暂停流程：**
- `eurekaclaw pause <session_id>` 或 **Ctrl+C** 会在 `~/.eurekaclaw/sessions/<session_id>/pause.flag` 写入暂停标志。
- 在 `inner_loop_yaml._run_once()` 的每个阶段边界处，检查 `ProofCheckpoint.is_pause_requested()`。
- 检测到暂停时：清除标志，保存 `checkpoint.json`（当前阶段 + 完整 `TheoryState`），抛出 `ProofPausedException`。
- `ProofPausedException` 在 `_run_once` 和 `agent.py` 中均会显式重新抛出，向上传播。

**恢复流程：**
- `eurekaclaw resume <session_id>` 加载 `checkpoint.json`，重建 `TheoryState`，并从保存的阶段重新运行 TheoryAgent。

**检查点文件：** `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`

## 运行后学习

```{image} ../_static/images/pipeline-learning.svg
:alt: Post-Run Continual Learning
:width: 90%
:align: center
```
