# 记忆系统

EurekaClaw 使用由 `MemoryManager` 管理的**四层记忆系统**。

```
eurekaclaw/memory/
├── manager.py          MemoryManager (main interface)
├── episodic.py         EpisodicMemory (in-RAM ring buffer)
├── persistent.py       PersistentMemory (cross-run JSON file)
└── knowledge_graph.py  KnowledgeGraph (theorem dependency network)

eurekaclaw/learning/
└── memory_extractor.py  SessionMemoryExtractor (Tier 4: domain markdown insights)
```

`~/.eurekaclaw/`（可通过 `EUREKACLAW_DIR` 配置）下的存储布局：

```
~/.eurekaclaw/
├── memory/
│   ├── persistent.json        ← Tier 2: cross-run key-value store
│   └── knowledge_graph.json   ← Tier 3: theorem dependency graph
├── memories/
│   └── <domain>/
│       ├── YYYYMMDD_<slug>.md ← Tier 4: per-domain insight files
│       └── _index.json        ← Tier 4: index for semantic search
└── skills/                    ← skill files updated by ContinualLearningLoop
```

---

## 第一层 — 情节记忆（会话级）

**文件：** `eurekaclaw/memory/episodic.py`

内存中的环形缓冲区（最多 500 条）。记录当前会话中的智能体事件。进程结束后丢失——永不持久化到磁盘。

```python
def log_event(
    agent_role: str,
    content: str,
    metadata: dict | None = None
) -> EpisodicEntry
```
记录来自智能体的结构化事件（工具调用、结果、决策、错误）。由 `BaseAgent` 在每次工具调用后自动调用。

```python
def recent_events(
    n: int = 20,
    agent_role: str | None = None
) -> list[EpisodicEntry]
```
返回最近 N 条事件，可按智能体角色过滤。

---

## 第二层 — 持久化记忆（跨会话键值存储）

**文件：** `eurekaclaw/memory/persistent.py`
**存储：** `~/.eurekaclaw/memory/persistent.json`

存储可跨会话保存的任意 JSON 可序列化键值记录。

```python
def remember(
    key: str,
    value: Any,
    tags: list[str] | None = None,
    source_session: str = ""
) -> None
```
保存或覆盖一条跨会话记录。`key` 通常有命名空间（例如 `"theory.failed_strategies.concentration_bounds"`）。

```python
def recall(key: str) -> Any | None
```
按精确键检索值。若未找到则返回 `None`。

```python
def recall_by_tag(tag: str) -> list[CrossRunRecord]
```
返回所有包含指定标签的记录。

---

## 第三层 — 知识图谱（定理依赖网络）

**文件：** `eurekaclaw/memory/knowledge_graph.py`
**存储：** `~/.eurekaclaw/memory/knowledge_graph.json`

跟踪所有会话中已证明定理及其依赖关系的有向图。可导出为 networkx 格式进行分析。

```python
def add_theorem(
    theorem_name: str,
    formal_statement: str,
    domain: str = "",
    session_id: str = "",
    tags: list[str] | None = None
) -> KnowledgeNode
```
注册一个新证明的定理。

```python
def link_theorems(from_id: str, to_id: str, relation: str = "uses") -> None
```
记录两个定理之间的依赖关系。关系类型：`"uses"`、`"generalizes"`、`"specializes"`、`"contradicts"`。

```python
def find_related_theorems(node_id: str, depth: int = 2) -> list[KnowledgeNode]
```
BFS 遍历——返回距 `node_id` 在 `depth` 跳以内的定理。

---

## 第四层 — 领域记忆（跨会话 Markdown 洞察）

**文件：** `eurekaclaw/learning/memory_extractor.py`
**存储：** `~/.eurekaclaw/memories/<domain>/YYYYMMDD_<slug>.md`

跨会话学习的主要机制。每次会话结束后，`SessionMemoryExtractor` 使用快速模型分析 `TheoryState`，并按四个类别提取结构化洞察：

| 类别 | 保存内容 |
|---|---|
| `domain_knowledge` | 本次发现或确认的新事实、引理、定理 |
| `proof_strategy` | 在该领域有效（或失败）的证明技术 |
| `open_problems` | 提出但未解决的猜想 |
| `pitfalls` | 看似有前途但最终失败的方法及其根本原因 |

仅保存 `confidence >= 0.5` 的条目。sha256 指纹索引（`_index.json`）用于去除精确重复。对于关键词重叠超过 40% 的近重复内容，由 LLM 检查并在冗余时合并。

### 注入到未来会话

每次会话开始时，`BaseAgent.build_system_prompt()` 调用：

```python
memory.load_for_injection(domain, k=4, query=task_description)
```

该函数通过余弦相似度对 `query` 选出领域内 4 个最**相关**的高置信度 `.md` 文件，去除 frontmatter 后以 `<memories>...</memories>` 形式注入系统提示词。

**语义排序：** 每个记忆文件的嵌入向量在写入时存储于 `_index.json`（通过 `eurekaclaw/memory/embedding_utils.py`）。检索时，候选文件按 `cosine_similarity(query_embedding, memory_embedding)` 打分，返回前 k 个。若嵌入向量不可用，则回退到按时间倒序排序。

---

## 生命周期

```
During session
  BaseAgent.execute() → memory.log_event() → Tier 1 (RAM only)

After session (ContinualLearningLoop.post_run())
  SessionMemoryExtractor.extract_and_save()
    → LLM analysis of TheoryState (proven lemmas + failed attempts)
    → write ~/.eurekaclaw/memories/<domain>/YYYYMMDD_<slug>.md  [Tier 4]

  ToolPatternExtractor.extract_and_save()
    → analyse tool-call patterns → generate new Skill files

  SkillRegistry.update_stats()
    → EMA α=0.3 update on success_rate for all injected skills

Next session startup
  MetaOrchestrator → MemoryManager.load_for_injection(domain)
    → top-4 Tier 4 files → injected into agent system prompts
```

---

## 数据模型

**文件：** `eurekaclaw/types/memory.py`

### EpisodicEntry

```python
class EpisodicEntry(BaseModel):
    entry_id: str
    session_id: str
    agent_role: str      # "survey", "theory", "writer", etc.
    content: str         # free-text event description
    metadata: dict = {}  # structured data (tool name, paper_id, etc.)
    timestamp: datetime
```

### CrossRunRecord

```python
class CrossRunRecord(BaseModel):
    record_id: str
    key: str             # namespaced key, e.g. "theory.failed_strategies.sample_complexity"
    value: Any           # arbitrary JSON-serializable value
    tags: list[str] = []
    source_session: str = ""
    created_at: datetime
    updated_at: datetime
```

### KnowledgeNode

```python
class KnowledgeNode(BaseModel):
    node_id: str
    theorem_name: str
    formal_statement: str
    domain: str = ""
    session_id: str = ""  # session that proved this theorem
    tags: list[str] = []
    created_at: datetime
```

---

## 存储位置

| 层级 | 存储方式 | 位置 |
|---|---|---|
| 第一层：情节记忆 | 内存（进程生命周期） | — |
| 第二层：持久化记忆 | JSON 文件 | `~/.eurekaclaw/memory/persistent.json` |
| 第三层：知识图谱 | JSON 文件 | `~/.eurekaclaw/memory/knowledge_graph.json` |
| 第四层：领域洞察 | Markdown 文件 | `~/.eurekaclaw/memories/<domain>/` |
| 运行产物 | 每个会话的 JSON | `~/.eurekaclaw/runs/<session_id>/` |
