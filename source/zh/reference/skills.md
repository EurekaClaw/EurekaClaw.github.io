# 技能系统

技能是在每次任务前注入智能体提示词的可复用、领域特定的知识片段。它们编码了从之前运行中总结出的成功证明策略、领域约定和常见陷阱。

```
eurekaclaw/skills/
├── registry.py      SkillRegistry (load + store skills)
├── injector.py      SkillInjector (retrieve + format for prompts)
├── install.py       SkillInstaller (install seed skills or skills from ClawHub)
└── evolver.py       SkillEvolver (distill skills from proceeded session)
```

---

## 技能文件格式

每个技能是一个带 YAML frontmatter 的 Markdown 文件：

```markdown
---
name: ucb_regret_analysis
version: "1.0"
tags: [bandit, regret, ucb, concentration]
agent_roles: [theory, survey]
pipeline_stages: [theory]
description: How to decompose and bound UCB1 regret using concentration inequalities
source: seed           # seed | distilled | manual
created_at: 2026-01-01T00:00:00
usage_count: 0
success_rate: null     # float 0-1, or null if unknown
---

# UCB Regret Analysis

When bounding UCB1 regret, decompose into:
1. Suboptimal arm pulls where confidence bound held (good event)
2. Pulls where the bound failed (bad event, controlled by concentration)

Use Hoeffding for sub-Gaussian rewards, Bernstein when variance is known...
```

技能根据其来源存储在三个位置之一（详见下方[技能生命周期](#技能生命周期)）。

---

## SkillRegistry

**文件：** `eurekaclaw/skills/registry.py`

```python
class SkillRegistry:
    def __init__(skills_dir: Path | None = None) -> None
```

### 加载

```python
def load_all() -> list[SkillRecord]
```
从已注册目录加载所有技能。加载顺序（后者覆盖前者）：
1. `eurekaclaw/skills/seed_skills/` 中的种子技能
2. 领域插件技能（来自 `get_skills_dirs()` 的额外目录）
3. `~/.eurekaclaw/skills/` 中的用户技能（最高优先级）

```python
def add_skills_dir(path: Path) -> None
```
注册额外的技能目录（由领域插件使用）。

```python
def reload() -> None
```
从磁盘重新加载所有技能（例如蒸馏写入新文件后）。

### 检索

```python
def get(name: str) -> SkillRecord | None
```
按精确名称检索技能。

```python
def get_by_tags(tags: list[str]) -> list[SkillRecord]
```
返回所有包含至少一个给定标签的技能。

```python
def get_by_role(role: str) -> list[SkillRecord]
```
返回所有 `agent_roles` 包含 `role` 的技能。

```python
def get_by_pipeline_stage(stage: str) -> list[SkillRecord]
```
返回指定流水线阶段的所有技能。

### 存储

```python
def upsert(skill: SkillRecord) -> None
```
将技能写入磁盘并注册到内存。在 `~/.eurekaclaw/skills/` 中创建或覆盖 `.md` 文件。

---

## SkillInjector

**文件：** `eurekaclaw/skills/injector.py`

检索与任务最相关的技能并将其格式化，注入智能体系统提示词。

```python
class SkillInjector:
    def __init__(
        registry: SkillRegistry,
        selected_skills: list[str] | None = None,
    ) -> None
```

`selected_skills` — 可选的技能名称列表，用于**固定**技能。固定技能始终排在前 k 个结果的最前面，优先于按使用次数排序的可选技能。若固定技能名称在注册表中未找到，则记录警告并静默跳过。

### 检索

```python
def top_k(
    task: Task,
    role: str,
    k: int = 5,
    strategy: Literal["tag", "semantic", "hybrid"] = "tag"
) -> list[SkillRecord]
```

**检索策略：**

| 策略 | 说明 |
|---|---|
| `tag` | 按匹配的 `agent_roles` 和 `pipeline_stages` 过滤；固定技能优先，其余按 `usage_count` 排序 |
| `semantic` | 基于 `sentence-transformers` 的嵌入相似度（若已安装） |
| `hybrid` | 标签过滤（3×k 候选），再按文本相似度排序 |

**固定技能优先级：** 当 `selected_skills` 非空时，`tag`（及 `hybrid`）检索将候选分为：
1. **必须包含** — 同时在 `selected_skills` 和角色/阶段集合中的技能 → 始终排在前面
2. **可选** — 剩余候选 → 按 `usage_count` 降序排序

合并后的列表截断为 `k` 个。

### 格式化

```python
def render_for_prompt(skills: list[SkillRecord]) -> str
```

返回注入智能体系统提示词的 XML 块：

```xml
<skills>
<skill name="ucb_regret_analysis">
# UCB Regret Analysis
...
</skill>
<skill name="concentration_inequalities">
...
</skill>
</skills>
```

---

## 数据模型

**文件：** `eurekaclaw/types/skills.py`

```python
class SkillMeta(BaseModel):
    name: str
    version: str = "1.0"
    tags: list[str] = []
    agent_roles: list[str] = []       # e.g., ["theory", "survey"]
    pipeline_stages: list[str] = []   # e.g., ["theory", "experiment"]
    description: str = ""
    source: Literal["seed", "distilled", "manual"] = "seed"
    created_at: datetime
    usage_count: int = 0
    success_rate: float | None = None

class SkillRecord(BaseModel):
    meta: SkillMeta
    content: str        # Markdown body after frontmatter
    file_path: str = "" # absolute path to the .md file
    embedding: list[float] | None = None  # populated on first semantic retrieval

    @property
    def full_markdown(self) -> str: ...  # frontmatter + content
```

---

## 技能蒸馏（运行后学习）

每次成功的会话结束后，`ContinualLearningLoop.post_run()` 从会话中蒸馏新技能：

```
ContinualLearningLoop.post_run()
    ├── extract failures (FailedAttempt[]) from TheoryState
    ├── deduplicate — only unique failure patterns (skip low-novelty)
    ├── compress successes — proof text trimmed to 300 chars
    ├── SkillEvolver.distill_from_session()
    │       → new SkillRecord .md files in ~/.eurekaclaw/skills/
    └── (rl/madmax modes) ProcessRewardModel scoring
```

**`SkillEvolver.distill_from_session()`** 使用主 LLM：
1. 从成功的证明中识别可推广的模式
2. 编写带有适当标签和角色的新技能 Markdown 文件
3. 在 frontmatter 中设置 `source: distilled`

新技能通过 `SkillRegistry.reload()` 在下一次会话中立即可用。

---

## 种子技能（MAB 领域）

MAB 领域插件内置四个种子技能：

| 技能 | 标签 | 说明 |
|---|---|---|
| `ucb_regret_analysis` | bandit, regret, ucb | 通过集中不等式进行 UCB1 遗憾分解 |
| `thompson_sampling_analysis` | bandit, thompson, bayesian | Thompson Sampling 遗憾分析 |
| `lower_bound_construction` | bandit, lower-bound, information | Lai-Robbins 和基于 Fano 的下界 |
| `bandit_simulation` | bandit, simulation, experiment | 如何运行和解读赌博机模拟 |

---

## 安装种子技能

```bash
eurekaclaw install-skills                      # copy seeds to ~/.eurekaclaw/skills/
eurekaclaw install-skills --force              # overwrite existing copies
eurekaclaw install-skills <skillname>          # install a skill from ClawHub
```

`<skillname>` 形式通过 `clawhub` CLI（需单独安装）从 [ClawHub](https://clawhub.ai/) 注册表获取技能。示例：

```bash
eurekaclaw install-skills steipete/github
```

此命令仅用于检查和手动编辑。智能体**不需要**执行此命令——种子技能始终直接从包中获取。

---

## 技能生命周期

了解技能的物理存储位置，可以避免对 `~/.eurekaclaw/skills/` 中未包含某些技能的困惑。

### 三个存储位置

| 位置 | 写入者 | 时机 |
|---|---|---|
| `eurekaclaw/skills/seed_skills/` | 包开发者（您） | 提交到代码库；随 `pip install` 打包 |
| `eurekaclaw/domains/<domain>/skills/` | 领域插件作者 | 通过 `add_skills_dir()` 在插件加载时注册 |
| `~/.eurekaclaw/skills/` | `install-skills` CLI + `SkillEvolver` + ClawHub | 按需写入；用户可编辑 |

### 运行时加载顺序

每次 `SkillRegistry._load()` 运行时，按以下顺序读取所有三个来源。同名技能后来者覆盖前者：

```
1. eurekaclaw/skills/seed_skills/**/*.md        (lowest priority)
2. domain plugin skill dirs (extra_dirs)        (medium priority)
3. ~/.eurekaclaw/skills/**/*.md                 (highest priority — overrides seeds)
```

**结论：** 向 `seed_skills/` 添加文件后，智能体在下一次运行时即可看到该技能，无需将任何内容复制到 `~/.eurekaclaw/skills/`。`~/.eurekaclaw/skills/` 中缺少某个种子技能不会降低智能体能力。

### 新技能的生成方式

技能通过三条路径进入系统：

#### 1. 种子技能（开发者编写）

在 `eurekaclaw/skills/seed_skills/<category>/` 中创建 `.md` 文件：

```bash
# e.g. for a new theory skill
touch eurekaclaw/skills/seed_skills/theory/my_new_skill.md
```

在 frontmatter 中设置 `source: seed`。文件保存后，智能体立即可用——无需 CLI 步骤。

#### 2. LLM 蒸馏（自动，运行后）

每次成功的会话结束后，`SkillEvolver.distill_from_session()` 使用会话中最多 5 条 `FailedAttempt` 记录和 5 条 `ProofRecord` 成功记录进行调用。它使用快速模型发起蒸馏提示，并将响应解析为新的 `SkillRecord`。

新技能通过 `SkillRegistry.upsert()` 写入 `~/.eurekaclaw/skills/<name>.md`，带有：
- `source: distilled`
- `name: distilled_<session_id[:8]>_<random_hex>`
- 从 LLM 响应中提取的标签、角色和阶段

后续会话无需重启即可立即使用。

```
Session completes
    └── SkillEvolver.distill_from_session(failures, successes)
            └── LLM call (fast model, max_tokens=1024)
                    └── _parse_skill_response()
                            └── SkillRegistry.upsert()  →  ~/.eurekaclaw/skills/<name>.md
```

#### 3. ClawHub 技能

```bash
eurekaclaw install-skills <author>/<skillname>
```

通过 `clawhub` CLI 从 [ClawHub](https://clawhub.ai/) 注册表下载技能并放置在 `~/.eurekaclaw/skills/` 中。需要安装 `clawhub`（`pip install clawhub` 或等效方式）。

#### 4. 手动用户技能

将任何带有有效 YAML frontmatter 的 `.md` 文件直接放入 `~/.eurekaclaw/skills/`，下一次会话加载时即可使用。在 frontmatter 中使用 `source: manual` 与蒸馏技能区分。

### 技能统计更新

每次会话结束后，`SkillRegistry.update_stats(name, success)` 会以更新后的 `usage_count` 和 `success_rate`（指数移动平均，α=0.3）重写技能文件。这仅影响 `~/.eurekaclaw/skills/` 中已存在的技能——包内的种子技能不会被运行会话修改。

### 为何 `~/.eurekaclaw/skills/` 可能看起来是空的

全新安装且尚未运行任何会话时，`~/.eurekaclaw/skills/` 目录将为空。这是正常现象。智能体并未"缺失"任何技能——它们在运行时直接读取种子技能和领域插件技能。`~/.eurekaclaw/skills/` 会随时间通过以下方式逐渐填充：

- `eurekaclaw install-skills`（一次性复制，用于检查/编辑）
- 已完成的会话（自动蒸馏）
- 手动放置的自定义 `.md` 文件
