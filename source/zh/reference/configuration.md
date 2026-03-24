# 配置

所有设置均从环境变量（或项目根目录下的 `.env` 文件）中读取。运行前请将 `.env.example` 复制为 `.env` 并进行编辑。

## LLM 后端

| 变量 | 默认值 | 说明 |
|---|---|---|
| `LLM_BACKEND` | `anthropic` | 后端：`anthropic`、`openrouter`、`local`、`minimax` |
| `ANTHROPIC_API_KEY` | `""` | Anthropic API 密钥。若为空，则回退到 ccproxy OAuth（`~/.claude/.credentials.json`） |
| `ANTHROPIC_AUTH_MODE` | `api_key` | `api_key` 或 `oauth`（ccproxy） |
| `ANTHROPIC_BASE_URL` | `""` | 覆盖 Anthropic 客户端的基础 URL（例如用于代理或测试服务器） |
| `CCPROXY_PORT` | `8000` | ccproxy 服务器端口 |
| `OPENAI_COMPAT_BASE_URL` | `""` | OpenAI 兼容端点的基础 URL（OpenRouter / 本地 vLLM） |
| `OPENAI_COMPAT_API_KEY` | `""` | OpenAI 兼容端点的 API 密钥 |
| `OPENAI_COMPAT_MODEL` | `""` | OpenAI 兼容端点的模型名称 |

**后端快捷说明：**

| `LLM_BACKEND` | 备注 |
|---|---|
| `anthropic` | 默认。使用 `ANTHROPIC_API_KEY` 或 ccproxy OAuth |
| `openrouter` | 设置 `OPENAI_COMPAT_API_KEY=sk-or-...` |
| `local` | 默认连接 `http://localhost:8000/v1`（vLLM / Ollama） |
| `minimax` | 设置 `MINIMAX_API_KEY` 和 `MINIMAX_MODEL` |

**Minimax 专用变量：**

| 变量 | 默认值 | 说明 |
|---|---|---|
| `MINIMAX_API_KEY` | `""` | Minimax API 密钥 |
| `MINIMAX_MODEL` | `""` | Minimax 模型名称（例如 `abab7-chat`） |

## 模型

| 变量 | 默认值 | 说明 |
|---|---|---|
| `EUREKACLAW_MODEL` | `claude-sonnet-4-6` | 主推理模型（所有智能体） |
| `EUREKACLAW_FAST_MODEL` | `claude-haiku-4-5-20251001` | 用于压缩、形式化、反例搜索的快速/低成本模型 |

`settings.active_model` 和 `settings.active_fast_model` 是**只读派生属性**，用于解析当前后端对应的正确模型字符串。所有智能体均使用这两个属性——从不直接使用原始的 `EUREKACLAW_MODEL` 变量。

## 外部 API

| 变量 | 默认值 | 说明 |
|---|---|---|
| `S2_API_KEY` | `""` | Semantic Scholar API 密钥（可选——更高速率限制） |
| `BRAVE_SEARCH_API_KEY` | `""` | Brave Search API 密钥（网络搜索） |
| `SERPAPI_KEY` | `""` | SerpAPI 密钥（网络搜索回退） |
| `WOLFRAM_APP_ID` | `""` | Wolfram Alpha App ID（符号计算） |

## 流水线模式

| 变量 | 默认值 | 选项 | 说明 |
|---|---|---|---|
| `EUREKACLAW_MODE` | `skills_only` | `skills_only`、`rl`、`madmax` | 运行后学习模式 |
| `GATE_MODE` | `auto` | `auto`、`human`、`none` | 阶段关卡行为 |
| `THEORY_PIPELINE` | `default` | `default`、`memory_guided` | 使用哪个理论证明流水线 |
| `OUTPUT_FORMAT` | `latex` | `latex`、`markdown` | 论文输出格式 |
| `EXPERIMENT_MODE` | `auto` | `auto`、`true`、`false` | 实验阶段：自动检测 / 强制运行 / 强制跳过*（未来工作——建议设为 `false`）* |

**关卡模式说明：**
- `none` — 无阶段卡片或审批提示
- `auto` — 打印阶段摘要卡片；仅在检测到低置信度引理时提示
- `human` — 打印卡片并在每个关卡提示；接受注入下一个智能体的文本反馈

## 证明与理论

| 变量 | 默认值 | 说明 |
|---|---|---|
| `THEORY_MAX_ITERATIONS` | `10` | LemmaDeveloper 循环的最大证明迭代次数 |
| `THEORY_REVIEW_MAX_RETRIES` | `3` | 人工审阅者标记证明步骤时的最大重试次数 |
| `AUTO_VERIFY_CONFIDENCE` | `0.95` | 置信度高于等于此阈值的证明自动接受（跳过 LLM 验证器调用） |
| `VERIFIER_PASS_CONFIDENCE` | `0.90` | LLM 验证器将引理标记为通过的置信度阈值 |
| `STAGNATION_WINDOW` | `3` | 相同错误重复 N 次时强制执行 Refiner |
| `ENFORCE_PROOF_STYLE` | `true` | 将证明可读性规则注入 WriterAgent 提示词 |

## 上下文与压缩

| 变量 | 默认值 | 说明 |
|---|---|---|
| `CONTEXT_COMPRESS_AFTER_TURNS` | `6` | 每隔 N 轮使用快速模型压缩智能体历史 |

## Token 限制（按调用类型）

| 变量 | 默认值 | 适用范围 |
|---|---|---|
| `MAX_TOKENS_AGENT` | `8192` | 主智能体推理循环（所有智能体） |
| `MAX_TOKENS_PROVER` | `4096` | 证明生成（Prover） |
| `MAX_TOKENS_PLANNER` | `4096` | 研究方向规划（diverge 阶段）；converge 阶段使用一半 |
| `MAX_TOKENS_DECOMPOSER` | `4096` | 引理分解（LemmaDecomposer、KeyLemmaExtractor） |
| `MAX_TOKENS_ASSEMBLER` | `6144` | 证明汇总叙述（Assembler） |
| `MAX_TOKENS_CRYSTALLIZER` | `4096` | 最终定理语句提取（TheoremCrystallizer） |
| `MAX_TOKENS_ARCHITECT` | `3072` | 证明计划生成（ProofArchitect） |
| `MAX_TOKENS_ANALYST` | `1536` | 分析阶段（MemoryGuidedAnalyzer、TemplateSelector、ProofSkeletonBuilder） |
| `MAX_TOKENS_SKETCH` | `1024` | Lean4/Coq 草图生成（SketchGenerator） |
| `MAX_TOKENS_FORMALIZER` | `4096` | 形式化、Refiner、CounterexampleSearcher、ResourceAnalyst、PaperReader |
| `MAX_TOKENS_VERIFIER` | `2048` | 证明验证（Verifier）和同行评审 |
| `MAX_TOKENS_COMPRESS` | `512` | 上下文压缩摘要（快速模型） |

所有 12 个值均可在 Web UI 的设置标签页中调整。

## 论文阅读器

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PAPER_READER_USE_PDF` | `true` | 除摘要外还下载并提取完整 PDF |
| `PAPER_READER_ABSTRACT_PAPERS` | `10` | 从摘要中提取的最大论文数 |
| `PAPER_READER_PDF_PAPERS` | `3` | 从完整 PDF 中提取的最大论文数 |

## 轮次限制

| 变量 | 默认值 | 说明 |
|---|---|---|
| `SURVEY_MAX_TURNS` | `8` | SurveyAgent 循环中的工具调用轮次 |
| `THEORY_STAGE_MAX_TURNS` | `6` | 每个内层理论阶段的轮次 |
| `WRITER_MAX_TURNS` | `4` | WriterAgent 的轮次 |

## 搜索与检索

| 变量 | 默认值 | 说明 |
|---|---|---|
| `ARXIV_MAX_RESULTS` | `10` | arXiv 搜索结果的硬性上限 |

## 重试与容错

| 变量 | 默认值 | 说明 |
|---|---|---|
| `LLM_RETRY_ATTEMPTS` | `5` | 5xx / 速率限制错误时的重试次数 |
| `LLM_RETRY_WAIT_MIN` | `4` | 指数退避最小等待时间（秒） |
| `LLM_RETRY_WAIT_MAX` | `90` | 指数退避最大等待时间（秒） |

## 文件路径与工具

| 变量 | 默认值 | 说明 |
|---|---|---|
| `EUREKACLAW_DIR` | `~/.eurekaclaw` | 技能、内存和运行产物的基础目录 |
| `LEAN4_BIN` | `lean` | Lean4 二进制文件路径 |
| `LATEX_BIN` | `pdflatex` | pdflatex 二进制文件路径 |
| `USE_DOCKER_SANDBOX` | `false` | 使用 Docker 容器执行 Python 代码*（未来工作——沙箱尚未完全集成）* |

## 派生路径（`settings` 上的只读属性）

| 属性 | 值 |
|---|---|
| `settings.skills_dir` | `EUREKACLAW_DIR/skills` |
| `settings.memory_dir` | `EUREKACLAW_DIR/memory` |
| `settings.runs_dir` | `EUREKACLAW_DIR/runs` |
| `settings.fast_model` | `EUREKACLAW_FAST_MODEL`（若未设置则回退到主模型） |
