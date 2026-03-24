# 研究工具

工具是通过 Anthropic 工具调用 API 暴露给智能体的可调用函数。每个工具包含名称、描述、输入模式和异步 `call()` 方法。

## 工具架构

```python
class BaseTool(ABC):
    name: ClassVar[str]
    description: ClassVar[str]

    def input_schema(self) -> dict: ...    # JSON Schema for inputs
    async def call(self, **kwargs) -> str: ...   # returns JSON string
    def to_anthropic_tool_def(self) -> dict: ... # format for API
```

工具存储在 `ToolRegistry` 中。默认注册表（`build_default_registry()`）包含 7 个内置工具。领域插件可通过 `DomainPlugin.register_tools()` 添加额外工具。

---

## 内置工具

### `arxiv_search`

**文件：** `eurekaclaw/tools/arxiv.py`

**功能：** 在 arXiv 上搜索学术论文。

**输入：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `query` | string | 必填 | 搜索查询 |
| `max_results` | integer | 8 | 结果数量（上限为 `ARXIV_MAX_RESULTS`） |
| `sort_by` | string | `relevance` | 排序方式：`relevance`、`lastUpdatedDate`、`submittedDate` |

**输出：** JSON 数组，每项包含：
```json
[{
  "arxiv_id": "2301.00774",
  "title": "...",
  "authors": ["Author A", "Author B"],
  "abstract": "...",
  "published": "2023-01-02",
  "pdf_url": "https://arxiv.org/pdf/2301.00774",
  "categories": ["cs.LG", "stat.ML"]
}]
```

**外部依赖：** `arxiv` Python 包

---

### `semantic_scholar_search`

**文件：** `eurekaclaw/tools/semantic_scholar.py`

**功能：** 在 Semantic Scholar 上搜索带引用数和期刊信息的论文。

**输入：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `query` | string | 必填 | 搜索查询 |
| `limit` | integer | 10 | 结果数量 |
| `year_range` | string | `""` | 可选年份过滤（例如 `"2020-2024"`） |

**输出：** JSON 数组，每项包含：
```json
[{
  "s2_id": "...",
  "title": "...",
  "authors": ["..."],
  "year": 2023,
  "abstract": "...",
  "citation_count": 42,
  "venue": "NeurIPS",
  "arxiv_id": "2301.00774",
  "url": "https://www.semanticscholar.org/paper/..."
}]
```

**外部依赖：** Semantic Scholar Graph API v1。设置 `S2_API_KEY` 可获得更高速率限制。

---

### `web_search`

**文件：** `eurekaclaw/tools/web_search.py`

**功能：** 通用网络搜索，用于补充研究背景。

**输入：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `query` | string | 必填 | 搜索查询 |
| `count` | integer | 5 | 结果数量 |

**输出：** JSON 数组：
```json
[{"title": "...", "url": "...", "description": "..."}]
```

**后端：** Brave Search（首选，需要 `BRAVE_SEARCH_API_KEY`）或 SerpAPI（回退，需要 `SERPAPI_KEY`）。

---

### `lean4_verify`

**文件：** `eurekaclaw/tools/lean4.py`

**功能：** 使用 Lean4 定理证明器对证明进行形式化验证。

**输入：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `proof_code` | string | 必填 | Lean4 证明代码 |
| `theorem_name` | string | `""` | 可选的定理名称（用于报告） |

**输出：**
```json
{
  "verified": true,
  "theorem": "my_theorem",
  "message": "Proof checked successfully"
}
```
失败时：
```json
{
  "verified": false,
  "lean4_output": "error: ...",
  "message": "Verification failed"
}
```

**外部依赖：** `LEAN4_BIN` 路径下的 Lean4 二进制文件（默认：`lean`）。导入 Mathlib 和 Aesop。超时：120 秒。最大心跳数：400,000。

---

### `execute_python` *（开发中）*

```{warning}
安全的沙箱化代码执行属于**未来工作**。在未正确配置 Docker 的情况下，此工具会直接在宿主子进程中运行 LLM 生成的 Python 代码，没有任何文件系统或网络隔离。在未来版本添加适当的沙箱支持之前，请勿启用 `EXPERIMENT_MODE`。
```

**文件：** `eurekaclaw/tools/code_exec.py`

**功能：** 执行 Python 代码以进行数值实验和合理性检验。

**输入：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `code` | string | 必填 | 要执行的 Python 代码 |
| `requirements` | list[string] | `[]` | 运行前需额外安装的包 |

**输出：**
```json
{"output": "stdout + stderr from execution"}
```
出错时：
```json
{"error": "exception message"}
```

**沙箱：** 带有 30 秒超时的子进程。设置 `USE_DOCKER_SANDBOX=true` 可在 Docker 容器（`python:3.11-slim`，512 MB 内存，禁用网络）中运行，而非在宿主机上。若 Docker 不可用，则静默回退到宿主子进程。包安装使用 `uv pip`（回退到 `pip`）。

---

### `wolfram_alpha`

**文件：** `eurekaclaw/tools/wolfram.py`

**功能：** 符号计算、公式化简和界的验证。

**输入：**

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `query` | string | 必填 | 自然语言或符号查询 |

**输出：** Wolfram Alpha pod 的 JSON 数组：
```json
[{"title": "Result", "result": "..."}]
```

**外部依赖：** Wolfram Alpha API v2。需要 `WOLFRAM_APP_ID`。

---

### `citation_manager`

**文件：** `eurekaclaw/tools/citation.py`

**功能：** 生成 BibTeX 条目并统一格式化引用键。

**操作：**

| 操作 | 说明 |
|---|---|
| `generate_bibtex` | 从论文元数据生成 BibTeX 条目 |
| `format_cite` | 返回论文的 `\cite{key}` 命令 |
| `list_entries` | 列出当前会话中所有引用条目 |

**输出：** 包含 `cite_key` 和 `bibtex` 字符串的 JSON。

**说明：** 使用与 `main.py` 中 `_generate_bibtex` 相同的键生成算法，确保 Writer 的 `\cite{}` 命令与 `.bib` 文件保持一致。

---

## ToolRegistry

**文件：** `eurekaclaw/tools/registry.py`

```python
class ToolRegistry:
    def register(tool: BaseTool) -> None
    def get(name: str) -> BaseTool | None
    def all_definitions() -> list[dict]         # all tools as Anthropic defs
    def definitions_for(names: list[str]) -> list[dict]  # subset
    async def call(name: str, inputs: dict) -> str
    def __contains__(name: str) -> bool
    def __len__() -> int

def build_default_registry() -> ToolRegistry   # create with all 7 built-in tools
```

---

## 领域特定工具

领域插件可通过 `DomainPlugin.register_tools(registry)` 注册额外工具。

### MAB 领域：`run_bandit_experiment`

**文件：** `eurekaclaw/domains/mab/tools/bandit_tool.py`

**功能：** 运行多臂赌博机模拟，对遗憾界进行实证验证。

**输入：**

| 参数 | 类型 | 说明 |
|---|---|---|
| `algorithm` | string | `ucb1` 或 `thompson_sampling` |
| `n_arms` | integer | 臂数 K |
| `n_rounds` | integer | 时间跨度 T |
| `distribution` | string | `gaussian` 或 `bernoulli` |
| `n_trials` | integer | 用于平均的蒙特卡洛试验次数 |

**输出：** 包含实验遗憾、每臂统计数据及与理论界对比的 JSON。

**支持模块：**
- `domains/mab/envs/stochastic.py` — `GaussianBandit`、`BernoulliBandit`
- `domains/mab/envs/runner.py` — `run_experiment()`、`sweep_T()`
- `domains/mab/tools/concentration.py` — Hoeffding、Bernstein、次高斯界
- `domains/mab/tools/regret.py` — 遗憾分解、Lai-Robbins 下界
- `domains/mab/tools/information.py` — KL(Bernoulli)、KL(Gaussian)、Fano 不等式
