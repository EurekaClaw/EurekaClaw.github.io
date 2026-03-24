# Python API

## EurekaSession

**文件：** `eurekaclaw/main.py`

以编程方式运行研究任务的主入口。

```python
from eurekaclaw.main import EurekaSession, run_research, save_artifacts

session = EurekaSession()
```

### 构造函数

```python
class EurekaSession:
    def __init__(self, session_id: str | None = None) -> None
```

- `session_id` — 可选。若不提供，则自动生成 UUID。
- 创建一个 `KnowledgeBus`，并延迟初始化 `MetaOrchestrator`。

### 方法

```python
async def run(self, input_spec: InputSpec) -> ResearchOutput
```
从 `InputSpec` 运行完整的研究会话。这是内部使用的最底层异步入口。

```python
async def run_detailed(self, conjecture: str, domain: str = "") -> ResearchOutput
```
**级别 1：** 证明特定猜想。

```python
async def run_from_papers(self, paper_ids: list[str], domain: str) -> ResearchOutput
```
**级别 2：** 从参考论文中发现研究空白并生成假设。

```python
async def run_exploration(self, domain: str, query: str = "") -> ResearchOutput
```
**级别 3：** 对研究领域进行开放式探索。

### 属性

```python
@property
def orchestrator(self) -> MetaOrchestrator
```
延迟初始化的编排器。根据 `InputSpec.domain` 自动检测领域插件。

---

## 便捷函数

```python
def run_research(conjecture: str, domain: str = "") -> ResearchOutput
```
同步入口（封装 `asyncio.run()`）。运行级别 1 证明流水线。

```python
def save_artifacts(result: ResearchOutput, out_dir: str | Path) -> Path
```
将所有流水线产物写入磁盘并编译 PDF。

**写入内容：**
- `paper.tex` — LaTeX 源码
- `references.bib` — BibTeX 参考文献
- `theory_state.json` — 完整证明状态
- `research_brief.json` — 规划状态
- `experiment_result.json` — 数值结果（如有）

**LaTeX 编译步骤：**
1. `pdflatex paper.tex`（第 1 遍——生成 `.aux`）
2. `bibtex paper`（仅当 `references.bib` 存在且非空时执行）
3. `pdflatex paper.tex`（第 2 遍——解析引用）
4. `pdflatex paper.tex`（第 3 遍——最终定稿）

**引用校验：** 编译前，`_fix_missing_citations()` 会移除 `references.bib` 中没有对应条目的 `\cite{}` 键，防止输出 PDF 出现 `?` 符号。

**返回值：** 输出目录的 `Path`。

---

## KnowledgeBus

**文件：** `eurekaclaw/knowledge_bus/bus.py`

会话中所有智能体共享的中央内存产物存储。所有数据通过总线流转——智能体在轮次之间不保留私有状态。

```python
class KnowledgeBus:
    def __init__(self, session_id: str) -> None
```

### 类型化产物访问

```python
def put_research_brief(brief: ResearchBrief) -> None
def get_research_brief() -> ResearchBrief | None

def put_theory_state(state: TheoryState) -> None
def get_theory_state() -> TheoryState | None

def put_experiment_result(result: ExperimentResult) -> None
def get_experiment_result() -> ExperimentResult | None

def put_bibliography(bib: Bibliography) -> None
def get_bibliography() -> Bibliography | None
def append_citations(papers: list[Paper]) -> None

def put_pipeline(pipeline: TaskPipeline) -> None
def get_pipeline() -> TaskPipeline | None
```

### 通用键值存储

```python
def put(key: str, value: Any) -> None
def get(key: str, default: Any = None) -> Any
```

用于智能体之间共享任意数据（例如 `numerically_suspect` 引理 ID）。

### 响应式订阅

```python
def subscribe(artifact_type: str, callback: Callable) -> None
```
注册一个回调，在总线上指定类型的产物更新时触发。

### 持久化

```python
def persist(session_dir: Path) -> None
```
将所有产物序列化为 JSON 文件并保存到 `session_dir`。

```python
@classmethod
def load(session_id: str, session_dir: Path) -> KnowledgeBus
```
从之前持久化的会话目录重建总线。

---

## InputSpec

**文件：** `eurekaclaw/types/tasks.py`

指定研究内容。

```python
class InputSpec(BaseModel):
    mode: Literal["detailed", "reference", "exploration"]
    conjecture: str | None = None     # Level 1: specific conjecture
    paper_ids: list[str] = []         # Level 2: reference paper IDs
    paper_texts: list[str] = []       # Level 2: raw paper texts (alternative)
    domain: str = ""                  # research domain string
    query: str = ""                   # Level 3: research question
    additional_context: str = ""      # extra context for agents
    selected_skills: list[str] = []   # manually select skill names to inject
```

---

## ResearchOutput

**文件：** `eurekaclaw/types/tasks.py`

完整研究会话的结果。

```python
class ResearchOutput(BaseModel):
    session_id: str
    latex_paper: str = ""           # full LaTeX source
    pdf_path: str | None = None     # path to compiled PDF (if successful)
    theory_state_json: str = ""     # TheoryState serialized as JSON
    experiment_result_json: str = "" # ExperimentResult serialized as JSON
    research_brief_json: str = ""   # ResearchBrief serialized as JSON
    bibliography_json: str = ""     # Bibliography serialized as JSON
    eval_report_json: str = ""      # evaluation report (if run)
    skills_distilled: list[str] = [] # names of new skills written this session
    completed_at: datetime
```

---

## 数据模型速查表

所有模型均为 Pydantic `BaseModel` 实例。字段级别的图示请参见 [architecture.md](architecture.md)。

| 模型 | 文件 | 说明 |
|---|---|---|
| `InputSpec` | `types/tasks.py` | 研究输入规范 |
| `ResearchOutput` | `types/tasks.py` | 完整会话结果 |
| `Task` | `types/tasks.py` | 单个流水线任务 |
| `TaskPipeline` | `types/tasks.py` | 有序任务序列 |
| `ResearchBrief` | `types/artifacts.py` | 调研结果 + 选定方向 |
| `ResearchDirection` | `types/artifacts.py` | 带评分的研究假设 |
| `TheoryState` | `types/artifacts.py` | 证明状态机 |
| `LemmaNode` | `types/artifacts.py` | 引理依赖 DAG 中的节点 |
| `ProofRecord` | `types/artifacts.py` | 单个引理的完整证明 |
| `ProofPlan` | `types/artifacts.py` | 带来源标注的计划引理 |
| `KnownResult` | `types/artifacts.py` | 从论文中提取的已知结论 |
| `FailedAttempt` | `types/artifacts.py` | 失败的证明尝试记录 |
| `Counterexample` | `types/artifacts.py` | 发现的反例 |
| `ExperimentResult` | `types/artifacts.py` | 数值验证结果 |
| `NumericalBound` | `types/artifacts.py` | 理论界与实验界的对比 |
| `Bibliography` | `types/artifacts.py` | 论文集合 + BibTeX |
| `Paper` | `types/artifacts.py` | 单篇论文元数据 |
| `AgentResult` | `types/agents.py` | 单个智能体任务的结果 |
| `SkillRecord` | `types/skills.py` | 带元数据的技能 |
| `EpisodicEntry` | `types/memory.py` | 会话级内存事件 |
| `CrossRunRecord` | `types/memory.py` | 跨会话持久化内存记录 |
| `KnowledgeNode` | `types/memory.py` | 知识图谱中的定理节点 |

---

## 示例：运行证明会话

```python
import asyncio
from eurekaclaw.main import EurekaSession, save_artifacts

async def main():
    session = EurekaSession()
    result = await session.run_detailed(
        conjecture="The sample complexity of transformers is O(L·d·log(d)/ε²)",
        domain="machine learning theory",
    )
    out = save_artifacts(result, "./results")
    print(f"Paper saved to: {out}")

asyncio.run(main())
```

## 示例：加载会话并重新生成产物

```python
from eurekaclaw.knowledge_bus.bus import KnowledgeBus
from eurekaclaw.types.artifacts import TheoryState, ResearchBrief
from eurekaclaw.main import save_artifacts, ResearchOutput
from pathlib import Path
import json

# Load existing session artifacts
session_dir = Path("results/my-session-id")
theory_state = TheoryState.model_validate_json((session_dir / "theory_state.json").read_text())
research_brief = ResearchBrief.model_validate_json((session_dir / "research_brief.json").read_text())

# Re-run writer agent
from eurekaclaw.agents.writer.agent import WriterAgent
from eurekaclaw.knowledge_bus.bus import KnowledgeBus

bus = KnowledgeBus(theory_state.session_id)
bus.put_theory_state(theory_state)
bus.put_research_brief(research_brief)
# ... run writer agent and save
```
