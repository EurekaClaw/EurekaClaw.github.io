# Token 限制

本文档介绍 UI 中"每次调用类型的 Token 限制"控制项及对应的后端设置。

这些限制**不会**改变模型的总上下文窗口大小。它们控制的是**特定阶段中单次模型调用的最大输出长度**。

实际效果：
- 提高某个限制，可让该阶段有更多空间来完成证明、定理语句或草稿。
- 降低某个限制，可使该阶段更省钱、更快，但增加被截断的风险。
- 最有调优价值的限制取决于您使用的是哪个理论流水线。

## 设置位置

后端配置位于：
- `eurekaclaw/config.py`

UI 配置映射位于：
- `eurekaclaw/ui/server.py`（`_CONFIG_FIELDS`）

UI 表单位于：
- `frontend/index.html`
- `eurekaclaw/ui/static/index.html`

## 速查表

| 变量 | 默认值 | 使用者 |
|---|---|---|
| `MAX_TOKENS_AGENT` | `8192` | 通用智能体循环（SurveyAgent、WriterAgent、回退路径） |
| `MAX_TOKENS_PROVER` | `4096` | `Prover` — 引理证明生成 |
| `MAX_TOKENS_PLANNER` | `4096` | `DivergentConvergentPlanner`（diverge 阶段）；converge 使用一半 |
| `MAX_TOKENS_ARCHITECT` | `3072` | `default` 流水线中的 `ProofArchitect` |
| `MAX_TOKENS_DECOMPOSER` | `4096` | `KeyLemmaExtractor` 和遗留分解阶段 |
| `MAX_TOKENS_ASSEMBLER` | `6144` | `Assembler` — 完整证明叙述 |
| `MAX_TOKENS_FORMALIZER` | `4096` | `Formalizer`、`Refiner`、`CounterexampleSearcher`、`ResourceAnalyst`、`PaperReader` |
| `MAX_TOKENS_CRYSTALLIZER` | `4096` | `TheoremCrystallizer` — 最终定理语句 |
| `MAX_TOKENS_ANALYST` | `1536` | `MemoryGuidedAnalyzer`、`TemplateSelector`、`ProofSkeletonBuilder`（`memory_guided` 流水线） |
| `MAX_TOKENS_SKETCH` | `1024` | `SketchGenerator` — Lean4/Coq 草图 |
| `MAX_TOKENS_VERIFIER` | `2048` | `Verifier` 和同行评审调用 |
| `MAX_TOKENS_COMPRESS` | `512` | 上下文压缩摘要（快速模型） |

## 各流水线使用情况

理论流水线有两种：
- `default`
- `memory_guided`

### `default` 流水线

对 `default` 流水线影响最大的阶段：
- `Architect`
- `Prover`
- `Assembler`
- `TheoremCrystallizer`
- `Verifier`

相关代码：
- [default_proof_pipeline.yaml](eurekaclaw/agents/theory/proof_pipelines/default_proof_pipeline.yaml)
- [proof_architect.py](eurekaclaw/agents/theory/proof_architect.py)
- [prover.py](eurekaclaw/agents/theory/prover.py)
- [assembler.py](eurekaclaw/agents/theory/assembler.py)
- [theorem_crystallizer.py](eurekaclaw/agents/theory/theorem_crystallizer.py)
- [verifier.py](eurekaclaw/agents/theory/verifier.py)

若 `default` 流水线遇到问题，通常最有效的调节顺序为：
1. `Architect`
2. `Prover`
3. `Assembler`
4. `TheoremCrystallizer`
5. `Verifier`

### `memory_guided` 流水线

对 `memory_guided` 流水线影响最大的阶段：
- `Analyst`
- `Decomposer`
- `Prover`
- `Assembler`
- `TheoremCrystallizer`
- `Verifier`

相关代码：
- [memory_guided_proof_pipeline.yaml](eurekaclaw/agents/theory/proof_pipelines/memory_guided_proof_pipeline.yaml)
- [analysis_stages.py](eurekaclaw/agents/theory/analysis_stages.py)
- [key_lemma_extractor.py](eurekaclaw/agents/theory/key_lemma_extractor.py)
- [prover.py](eurekaclaw/agents/theory/prover.py)
- [assembler.py](eurekaclaw/agents/theory/assembler.py)
- [theorem_crystallizer.py](eurekaclaw/agents/theory/theorem_crystallizer.py)
- [verifier.py](eurekaclaw/agents/theory/verifier.py)

若 `memory_guided` 流水线遇到问题，通常最有效的调节顺序为：
1. `Analyst`
2. `Decomposer`
3. `Prover`
4. `Assembler`
5. `TheoremCrystallizer`
6. `Verifier`

## 各重要阶段的作用

### 智能体循环

用于通用智能体调用，包括：
- `SurveyAgent`
- `WriterAgent`
- 所有回退到通用基础智能体路径的阶段

相关代码：
- [base.py](eurekaclaw/agents/base.py)
- [agent.py](eurekaclaw/agents/survey/agent.py)
- [agent.py](eurekaclaw/agents/writer/agent.py)

在以下情况时提高：
- 调研结果过短
- Writer 频繁提前停止

### Prover

用于引理级别的定理证明生成。

相关代码：
- [prover.py](eurekaclaw/agents/theory/prover.py)

在以下情况时提高：
- 引理证明在论证中途停止
- Prover 频繁省略技术步骤

### Architect

用于 `default` 流水线中的 `ProofArchitect`。

相关代码：
- [proof_architect.py](eurekaclaw/agents/theory/proof_architect.py)

在以下情况时提高：
- 证明计划过于浅层
- Architect 返回不完整的引理结构

### Analyst

用于 `memory_guided` 流水线中的 `MemoryGuidedAnalyzer`、`TemplateSelector` 和 `ProofSkeletonBuilder`。

相关代码：
- [analysis_stages.py](eurekaclaw/agents/theory/analysis_stages.py)

在以下情况时提高：
- 流水线选择了较差的证明模板
- 证明框架过于粗略
- 记忆引导分析内容过薄

### Decomposer

用于分解式阶段，包括 `KeyLemmaExtractor`。

相关代码：
- [key_lemma_extractor.py](eurekaclaw/agents/theory/key_lemma_extractor.py)
- [decomposer.py](eurekaclaw/agents/theory/decomposer.py)

在以下情况时提高：
- 关键引理缺失
- 分解粒度过粗

### Assembler

用于生成 `state.assembled_proof`。

相关代码：
- [assembler.py](eurekaclaw/agents/theory/assembler.py)

在以下情况时提高：
- 证明正文在句子中途结束
- `assembled_proof` 看起来被截断
- 后续定理提取失败，因为证明叙述不完整

### TheoremCrystallizer

用于生成 `state.formal_statement`。

相关代码：
- [theorem_crystallizer.py](eurekaclaw/agents/theory/theorem_crystallizer.py)

在以下情况时提高：
- 定理语句被截断
- 定理在公式中途结束
- 定理块中缺少汇总证明中存在的假设或术语

### Verifier

用于：
- 引理同行评审
- 一致性检查

相关代码：
- [verifier.py](eurekaclaw/agents/theory/verifier.py)
- [consistency_checker.py](eurekaclaw/agents/theory/consistency_checker.py)

在以下情况时提高：
- 审阅者输出过于简短
- 一致性检查遗漏了明显问题

### Formalizer / Refiner

多个定理支撑阶段的共享预算：
- `Formalizer`
- `Refiner`
- `CounterexampleSearcher`
- `ResourceAnalyst`
- `PaperReader`

相关代码：
- [formalizer.py](eurekaclaw/agents/theory/formalizer.py)
- [refiner.py](eurekaclaw/agents/theory/refiner.py)
- [counterexample.py](eurekaclaw/agents/theory/counterexample.py)
- [resource_analyst.py](eurekaclaw/agents/theory/resource_analyst.py)
- [paper_reader.py](eurekaclaw/agents/theory/paper_reader.py)

在以下情况时提高：
- 论文提取内容过浅
- 反例搜索结果过少
- 改进建议不完整

## 实践指南

### 若汇总证明被截断

依次提高：
1. `Assembler`
2. 若引理证明也过短，提高 `Prover`

### 若定理语句被截断

依次提高：
1. `TheoremCrystallizer`
2. 若证明叙述本身不完整，提高 `Assembler`

### 若 `default` 规划效果较弱

依次提高：
1. `Architect`
2. `Prover`

### 若 `memory_guided` 规划效果较弱

依次提高：
1. `Analyst`
2. `Decomposer`
3. `Prover`

### 若 Writer 或 Survey 输出过短

提高：
1. `Agent loop`

## 重要区别

这些控制项**不等同于**模型的完整上下文窗口。

它们仅控制：
- 单个阶段在一次调用中最多输出多少内容

它们**不直接控制**：
- 可发送的总对话历史量
- 模型完整上下文窗口的大小

因此，一个阶段可能以两种不同方式失败：
- 该阶段自身的 token 限制过低，导致输出过短
- 整个请求过于繁重或复杂，即使单次调用限制足够大也会失败

## 当前 UI 覆盖范围

UI 现已暴露两个理论流水线使用的主要 token 限制控制项，包括：
- `Architect`
- `Assembler`
- `TheoremCrystallizer`
- `Analyst`
- `Sketch`

若后续在后端添加了新的 `max_tokens_*` 字段，请记得同步更新：
- [server.py](eurekaclaw/ui/server.py)
- [frontend/index.html](frontend/index.html)
- [index.html](eurekaclaw/ui/static/index.html)
