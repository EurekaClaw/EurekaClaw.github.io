# 门控模式和人类辅助审核

Control how much the system pauses for your input with `--gate`.

## `--gate none` (Default)

Fully automatic. Runs end-to-end with no interaction. Summary cards are printed but the pipeline never pauses.

```bash
eurekaclaw prove "..." --gate none
```

## `--gate auto`

Summary cards after each stage. Pauses for human review **only** when a low-confidence lemma is detected (i.e., `verified=false` after the theory stage). Good for catching problems without constant interruption.

```bash
eurekaclaw prove "..." --gate auto
```

## `--gate human`

Pauses at every stage gate and asks for approval. After approving, you can type a correction or hint injected into the next agent's prompt:

```
Approve theory stage? [y/n] y
Any feedback for the next stage? (Enter to skip): Use Bernstein instead of Hoeffding for lemma 3
```

```bash
eurekaclaw prove "..." --gate human
```

:::{note} Auto-escalation
Even with `--gate auto`, if any lemma has `verified=false`, the gate automatically escalates to human review for that stage.
:::

## Theory Review Gate

After the TheoryAgent completes and **before** the WriterAgent runs, EurekaClaw always shows a proof sketch review — regardless of `--gate` mode:

```
──────────────── Proof Sketch Review ────────────────
  L1  [✓] arm_pull_count_bound  verified
       For arm a with mean gap Δ_a ...
  L2  [~] regret_decomposition  low confidence
       Total regret decomposes as ...
  L3  [✓] main_theorem          verified
       UCB1 achieves O(√(KT log T)) regret ...
──────────────────────────────────────────────────────

Does this proof sketch look correct?
  y  — Proceed to writing
  n  — Flag the most logically problematic step
→
```

- **y / Enter** — proceed to the WriterAgent
- **n** — you specify which step has the critical gap (e.g. `L2`) and describe the issue. TheoryAgent re-runs once with your feedback injected.

## Pause and Resume

Pause a running session at the next stage boundary:

```bash
# In a separate terminal:
eurekaclaw pause <session_id>

# Or press Ctrl+C during the run — EurekaClaw saves a checkpoint instead of crashing
```

Resume from the checkpoint:

```bash
eurekaclaw resume <session_id>
```

The checkpoint is saved to `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`.
