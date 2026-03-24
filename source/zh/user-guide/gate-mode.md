# 门控模式和人类辅助审核

用 `--gate` 控制系统暂停你输入的次数。

## `--gate none` (默认)

全自动。端到端运行，没有任何互动。总结界面会打印出来，但流程从未暂停。

```bash
eurekaclaw prove "..." --gate none
```

## `--gate auto`

每个门控结束后有总结卡。仅在检测到低置信度引理（即理论阶段后 `verified=false`）时暂停进行人工审核。适合在不被频繁打扰的情况下探索问题。

```bash
eurekaclaw prove "..." --gate auto
```

## `--gate human`

在每个门控时停下来请求批准。批准证明后，你可以在下一位代理的提示中输入修正或提示：

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

## 理论证明审核门控

在 TheoryAgent 完成且在**WriterAgent**运行之前，EurekaClaw 总是会显示一个证明草图评审——无论是否采用 `--gate` 模式：

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

- **y / Enter** — 继续 WriterAgent
- **n** — 你指定哪个步骤有关键缺陷（例如 `L2`）并描述问题。TheoryAgent 会在注入你的反馈后重新运行一次。

## 暂停和回复

在下一阶段边界暂停跑步会话：

```bash
# In a separate terminal:
eurekaclaw pause <session_id>

# Or press Ctrl+C during the run — EurekaClaw saves a checkpoint instead of crashing
```

从检查点恢复：

```bash
eurekaclaw resume <session_id>
```

检查点保存在 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`。
