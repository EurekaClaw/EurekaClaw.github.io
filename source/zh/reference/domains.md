# 领域插件系统

EurekaClaw 采用三层插件架构来支持领域特定的研究：

```
EurekaClaw (general pipeline)          ← domain-agnostic: survey / theory / experiment / writer
    └── DomainPlugin (e.g. MAB)        ← domain sub-interface: tools + skills + workflow + benchmark
            └── Workflow                ← per-domain research guidance injected into agent prompts
```

插件无需修改核心代码，即可为特定领域添加工具、技能和提示词引导。

---

## DomainPlugin 基类

**文件：** `eurekaclaw/domains/base.py`

```python
class DomainPlugin(ABC):
    name: str = ""            # machine identifier, e.g. "mab"
    display_name: str = ""    # human-readable, e.g. "Stochastic Multi-Armed Bandits"
    keywords: list[str] = []  # strings that trigger auto-detection
    description: str = ""
```

### 抽象方法

```python
@abstractmethod
def register_tools(self, registry: ToolRegistry) -> None:
    """Inject domain-specific tools into the shared ToolRegistry."""
    ...

@abstractmethod
def get_workflow_hint(self) -> str:
    """Return domain-specific research guidance (injected into agent system prompts)."""
    ...
```

### 可选方法

```python
def get_skills_dirs(self) -> list[Path]:
    """Return extra skill directories. Default: []."""
    return []

def get_benchmark_problems(self, level: str) -> list[dict]:
    """Return benchmark problems for 'level1', 'level2', or 'level3'. Default: []."""
    return []
```

---

## 插件注册表

**文件：** `eurekaclaw/domains/__init__.py`

### 注册

```python
@register_domain
class MyPlugin(DomainPlugin):
    name = "my_domain"
    ...
```

`@register_domain` 装饰器通过插件的 `name` 属性注册该插件类。

### 解析

```python
def resolve_domain(domain: str) -> DomainPlugin | None
```

从领域字符串或猜想关键词自动检测正确的插件。匹配顺序：
1. 与已注册插件名称进行精确匹配
2. 关键词扫描——返回 `keywords` 列表中包含 `domain` 中任意词的第一个插件

若无匹配插件，则返回 `None`（以通用模式运行）。

---

## MAB 领域插件

**包：** `eurekaclaw/domains/mab/`

用于随机多臂赌博机理论的内置示例插件。

```python
@register_domain
class MABDomainPlugin(DomainPlugin):
    name = "mab"
    display_name = "Stochastic Multi-Armed Bandits"
    description = "Regret bounds, concentration, lower bounds for K-armed bandits"
    keywords = [
        "bandit", "multi-armed", "mab", "ucb", "thompson", "regret",
        "exploration", "exploitation", "stochastic bandit",
    ]
```

**当领域包含以下词汇时自动检测：** `bandit`、`UCB`、`thompson`、`regret`、`exploration`、`multi-armed` 等。

### 包结构

```
domains/mab/
├── __init__.py            MABDomainPlugin
├── workflow.py            WORKFLOW_HINT (research guidance text)
├── envs/
│   ├── stochastic.py      GaussianBandit, BernoulliBandit environments
│   └── runner.py          run_experiment(), sweep_T() — UCB1 & Thompson Sampling
├── tools/
│   ├── concentration.py   Hoeffding, Bernstein, sub-Gaussian, UCB radius formulas
│   ├── regret.py          Regret decomposition, Lai-Robbins lower bound
│   ├── information.py     KL(Bernoulli), KL(Gaussian), Fano's inequality
│   └── bandit_tool.py     BanditExperimentTool (LLM-callable tool)
├── skills/
│   ├── ucb_regret_analysis.md
│   ├── thompson_sampling_analysis.md
│   ├── lower_bound_construction.md
│   └── bandit_simulation.md
└── benchmark/
    ├── level1.json        Reproduce known bounds (UCB1, Lai-Robbins)
    ├── level2.json        Refine existing results (Bernstein-UCB, MOSS, KL-UCB)
    └── level3.json        Open problems (heavy tails, infinite-arm, batched bandits)
```

---

## 如何添加新领域

1. **创建插件包：**

```python
# eurekaclaw/domains/my_domain/__init__.py
from eurekaclaw.domains.base import DomainPlugin
from eurekaclaw.domains import register_domain

@register_domain
class MyDomainPlugin(DomainPlugin):
    name = "my_domain"
    display_name = "My Research Domain"
    description = "Short description for display"
    keywords = ["keyword1", "keyword2", "related term"]

    def register_tools(self, registry: ToolRegistry) -> None:
        registry.register(MySpecialTool())

    def get_workflow_hint(self) -> str:
        return """
        When researching my_domain:
        - Always start by checking known results X and Y
        - Use technique Z for the main proof step
        ...
        """

    def get_skills_dirs(self) -> list[Path]:
        return [Path(__file__).parent / "skills"]

    def get_benchmark_problems(self, level: str) -> list[dict]:
        bm_file = Path(__file__).parent / "benchmark" / f"{level}.json"
        return json.loads(bm_file.read_text()) if bm_file.exists() else []
```

2. **在 `eurekaclaw/domains/__init__.py` 中注册导入：**

```python
_DOMAIN_PACKAGES = [
    "eurekaclaw.domains.mab",
    "eurekaclaw.domains.my_domain",  # add this line
]
```

3. **完成。** `resolve_domain("keyword1 problem")` 将自动选择您的插件。

---

## 领域插件集成方式

当 `MetaOrchestrator` 检测到领域插件并运行时，它将：

1. 调用 `plugin.register_tools(tool_registry)` — 将领域工具添加到注册表
2. 调用 `plugin.get_skills_dirs()` — 将领域技能加载到 `SkillRegistry`
3. 将 `plugin.get_workflow_hint()` 注入智能体系统提示词

无需修改任何核心智能体或编排器代码。
