# 设置环境变量

## Preset Configurations

### Quick and Cheap (Good for Exploration)

```ini
CONTEXT_COMPRESS_AFTER_TURNS=4
AUTO_VERIFY_CONFIDENCE=0.80
STAGNATION_WINDOW=2
MAX_TOKENS_PROVER=2048
MAX_TOKENS_AGENT=4096
```

### Balanced (Default Settings)

```ini
CONTEXT_COMPRESS_AFTER_TURNS=6
AUTO_VERIFY_CONFIDENCE=0.85
STAGNATION_WINDOW=3
```

### Maximum Thoroughness (For Final Results)

```ini
CONTEXT_COMPRESS_AFTER_TURNS=0   # no compression
AUTO_VERIFY_CONFIDENCE=0.99      # almost always do full peer review
STAGNATION_WINDOW=5
MAX_TOKENS_PROVER=4096
MAX_TOKENS_AGENT=8192
```

## Key Settings Explained

**`CONTEXT_COMPRESS_AFTER_TURNS`**
: Every N tool-use turns, the agent's conversation history is compressed to a bullet summary using the fast model. Lower = cheaper but agents "forget" more context. Set to `0` to disable compression entirely.

**`AUTO_VERIFY_CONFIDENCE`**
: If the prover's self-reported confidence ≥ this value and no `[GAP:]` flags are present, the proof is accepted without a separate verifier call. Lower = fewer verifier calls (cheaper). Default `0.85` is a good balance.

**`STAGNATION_WINDOW`**
: If the same lemma fails N consecutive times with a similar error, the loop forces a conjecture refinement instead of retrying. Prevents wasted calls on an unresolvable proof path.

**`EXPERIMENT_MODE`** *(future work)*
: Numerical experiment execution is not yet safely sandboxed. Keep this set to `false`. See the [Agents reference](../reference/agents.md#experimentagent-under-development) for details.

**`THEORY_MAX_ITERATIONS`**
: Maximum proof loop iterations. Increase for very hard theorems; decrease for faster (but potentially incomplete) results.

## Token Limit Tuning

See [Token Limits](../reference/token-limits.md) for guidance on which `MAX_TOKENS_*` variables to adjust for specific issues (truncated theorems, incomplete proofs, etc.).
