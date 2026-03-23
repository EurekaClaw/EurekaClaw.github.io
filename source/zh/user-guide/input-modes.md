# Input Modes

EurekaClaw has three input modes. Pick the one that matches how well-defined your goal is.

## Level 1 — Prove a Specific Conjecture

Use `prove` when you have a concrete mathematical statement.

```bash
eurekaclaw prove "Any PAC-learnable class has finite VC dimension" \
    --domain "ML theory"

eurekaclaw prove "The VC dimension of depth-d width-w ReLU networks is O(wd·log(wd))" \
    --domain "deep learning theory"

eurekaclaw prove "For all n ≥ 1: Σᵢ₌₁ⁿ i = n(n+1)/2" \
    --domain "combinatorics"
```

The system uses your statement **exactly as given** — the direction-selection step is bypassed.

:::{tip} Writing good conjectures
- State the result precisely, including asymptotic notation (`O(...)`, `Ω(...)`) where relevant
- Include key parameters (e.g. `L` layers, `d` dimension, `ε` precision)
- Avoid vague language — prefer "runs in polynomial time" over "is efficient"
:::

## Level 2 — Start from Papers

Use `from-papers` when you have specific papers you want to extend or find gaps in.

```bash
# Attention mechanism papers
eurekaclaw from-papers 1706.03762 2005.14165 \
    --domain "attention mechanisms"

# Bandit theory papers
eurekaclaw from-papers 1602.01783 2106.01336 \
    --domain "multi-armed bandits"
```

The `SurveyAgent` fetches and analyses the papers. The `IdeationAgent` identifies research gaps and generates 5 candidate directions. The best-scoring direction is selected automatically, or by you with `--gate human`.

## Level 3 — Open Exploration

Use `explore` when you have a broad research area but no specific conjecture.

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

The system autonomously surveys the frontier, identifies open problems, proposes 5 directions, and selects the most promising one.

:::{note} Direction planning fallback
If the direction planner fails or returns an empty list, the pipeline pauses and prompts you to enter a research direction manually. Up to 5 open problems from the survey are shown as context.
:::
