# 输出模式

EurekaClaw 有三种输入模式。选择一个符合你目标明确程度的方案。

## 第一级 — 证明一个特定猜想

当你有一个具体的数学陈述时，使用 `prove` 。

```bash
eurekaclaw prove "Any PAC-learnable class has finite VC dimension" \
    --domain "ML theory"

eurekaclaw prove "The VC dimension of depth-d width-w ReLU networks is O(wd·log(wd))" \
    --domain "deep learning theory"

eurekaclaw prove "For all n ≥ 1: Σᵢ₌₁ⁿ i = n(n+1)/2" \
    --domain "combinatorics"
```

系统会完全按照你的语句使用**给定**的研究方向，方向选择步骤被跳过了。

:::{tip} 写一个好的猜想
- 精确陈述结果，包括渐近符号 (`O(...)`, `Ω(...)`) 
- 包含关键参数（例如 `L` 层，`d` 维, `ε` 精确度）
- 避免模糊的措辞——更倾向于“多项式时间内运行”而非“高效”
:::

## 第二级 — 从论文开始

当你有具体的论文需要扩展或寻找缺陷和未尽研究时，可以使用 `from-papers`。

```bash
# Attention mechanism papers
eurekaclaw from-papers 1706.03762 2005.14165 \
    --domain "attention mechanisms"

# Bandit theory papers
eurekaclaw from-papers 1602.01783 2106.01336 \
    --domain "multi-armed bandits"
```

`SurveyAgent` 负责调取并分析这些文件。`IdeationAgent` 识别研究空白并生成 5 个候选研究方向。最佳得分方向由你自动选择，或者你用 `--gate human` 选择。

## 第三级 — 开放探索

当你有广泛的研究领域但没有具体猜想时，使用`explore`。

```bash
# Broad domain exploration
eurekaclaw explore "spectral graph theory"

# Domain + guiding question
eurekaclaw explore "multi-armed bandit theory" \
    --query "What are the tightest known bounds for heavy-tailed rewards?"

# Pure math
eurekaclaw explore "algebraic topology" \
    --query "What are open problems in persistent homology?"
```

该系统自主勘察前沿，识别未解决问题，提出 5 个研究方向，并选择最有前景的方向。

:::{note} 研究方向规划的备选方案
如果研究方向规划器失败或返回空列表，流程会暂停，提示你手动输入研究方向。最多显示调查中 5 个未解决的问题作为上下文。
:::
