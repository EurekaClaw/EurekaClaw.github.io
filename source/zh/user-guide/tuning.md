# 设置环境变量

## 预设配置

### 快速且便宜（适合探索）

```ini
CONTEXT_COMPRESS_AFTER_TURNS=4
AUTO_VERIFY_CONFIDENCE=0.80
STAGNATION_WINDOW=2
MAX_TOKENS_PROVER=2048
MAX_TOKENS_AGENT=4096
```

### 平衡（默认设置）

```ini
CONTEXT_COMPRESS_AFTER_TURNS=6
AUTO_VERIFY_CONFIDENCE=0.85
STAGNATION_WINDOW=3
```

### 最大（针对最终结果）

```ini
CONTEXT_COMPRESS_AFTER_TURNS=0   # no compression
AUTO_VERIFY_CONFIDENCE=0.99      # almost always do full peer review
STAGNATION_WINDOW=5
MAX_TOKENS_PROVER=4096
MAX_TOKENS_AGENT=8192
```

## 主要设置详解

**`CONTEXT_COMPRESS_AFTER_TURNS`**
：每使用工具 N 次，智能体的对话历史记录就会使用快速模型压缩成一个要点摘要。压缩率越低，成本越低，但智能体会“遗忘”更多上下文信息。设置为 `0` 可完全禁用压缩。

**`AUTO_VERIFY_CONFIDENCE`**
：如果证明者自述的置信度大于等于此值且不存在 `[GAP:]` 标志，则无需单独调用验证器即可接受该证明。值越低，所需的验证器调用次数越少（成本越低）。默认值 `0.85` 是一个不错的平衡点。

**`STAGNATION_WINDOW`**
：如果同一个引理连续 N 次失败且错误类型相似，则循环会强制进行猜想细化，而不是重试。这样可以避免在无法解决的证明路径上进行不必要的调用。

**`EXPERIMENT_MODE`** *(future work)*
：实验模式，目前仍在开发，请设为 `false`. 参考 [智能体参考](../reference/agents.md#experimentagent-under-development)、

**`THEORY_MAX_ITERATIONS`**
：最大证明循环迭代次数。对于非常困难的定理，增加此值；对于速度更快（但可能不完整）的结果，减少此值。

## Token限额调整

有关针对特定问题（截断定理、不完整的证明等）调整哪些 `MAX_TOKENS_*` 变量的指导，请参阅 [Token Limits](../reference/token-limits.md)。
