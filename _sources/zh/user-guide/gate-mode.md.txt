# 门控模式和人类辅助审核

EurekaClaw 包含交互式门控，在关键决策点暂停流水线并请求你的输入。门控在浏览器 UI 和 CLI 中均可使用。

## 浏览器 UI 门控

运行 `eurekaclaw ui` 时，门控以悬浮对话框的形式出现在工作区之上——无论你在哪个标签页都会弹出。共有三种门控：

**文献门控（Survey gate）** — 当文献调研未找到任何论文时触发。

悬浮框要求你提供论文 ID 或 arXiv ID 以重试调研，或选择在没有论文的情况下继续。

**方向门控（Direction gate）** — 当构思阶段未返回任何候选研究方向时触发（详细/证明模式）。

悬浮框默认显示原始猜想，允许你输入自定义方向，或直接接受猜想本身。

**理论审核门控（Theory review gate）** — 在定理证明器完成后触发。

悬浮框显示已组装的证明，允许你批准它（流水线继续进入实验与写作阶段），或标记某个具体引理并说明原因。标记后，理论智能体会将你的反馈注入后重新运行。经过可配置次数的重试（`THEORY_REVIEW_MAX_RETRIES`，默认 3 次）后，证明将自动通过。

## CLI 门控

从终端运行时，同样的门控以交互式提示的形式出现。

### `--gate none` (默认)

全自动。端到端运行，没有任何互动。总结界面会打印出来，但流程从未暂停。

```bash
eurekaclaw prove "..." --gate none
```

### `--gate auto`

每个门控结束后有总结卡。仅在检测到低置信度引理（即理论阶段后 `verified=false`）时暂停进行人工审核。适合在不被频繁打扰的情况下探索问题。

```bash
eurekaclaw prove "..." --gate auto
```

### `--gate human`

在每个门控时停下来请求批准。批准证明后，你可以在下一位代理的提示中输入修正或提示：

```
Approve theory stage? [y/n] y
Any feedback for the next stage? (Enter to skip): Use Bernstein instead of Hoeffding for lemma 3
```

```bash
eurekaclaw prove "..." --gate human
```

:::{note} 自动升级
即使设置了 `--gate auto`，如果任何引理的 `verified=false`，门控也会自动升级为人工审核。
:::

## 暂停和恢复

在下一阶段边界暂停运行中的会话：

```bash
# 在另一个终端中：
eurekaclaw pause <session_id>

# 或在运行时按 Ctrl+C — EurekaClaw 会保存检查点而不是直接崩溃
```

从检查点恢复：

```bash
eurekaclaw resume <session_id>
```

检查点保存在 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`。
