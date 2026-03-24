# 错误检索

## `No skills available` / 证明立即失败

**原因：**初始技能集尚未安装。这是由于在安装过程中跳过了 `eurekaclaw install-skills` 命令造成的。

**修复：**

```bash
eurekaclaw install-skills
```

此操作会下载管道运行所需的内置种子技能（证明策略、领域启发式方法、Token模板）。您可以随时重新运行此操作，将技能重置为默认值。

---

## `paper.pdf` 未生成

**原因：** `pdflatex` 未安装或不在 `PATH` 中。

**修复：**
- Linux: `sudo apt install texlive-full`
- macOS: 安装 [MacTeX](https://www.tug.org/mactex/)
- `.env` 里设置 `LATEX_BIN=/usr/local/bin/pdflatex` 

`.tex` 和 `.bib` 文件始终会被保存——手动编译或上传到 Overleaf。

---

## 引用在 PDF 中显示为 `?`

**原因：** bibtex 未运行，或引用标签不匹配。

**修复：** 手动运行编译序列：

```bash
cd results/<session_id>
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

---

## `Parsed zero lemmas from architect response`

**原因：** LLM 返回了无法识别的证明计划格式。

**修复：** 已通过 4 次遍历解析器自动处理。如果问题仍然存在，请使用功能更强大的模型（`EUREKACLAW_MODEL`）并重试。

---

## 证明状态是 `abandoned`（被放弃）

**原因：** 在未证明所有引理的情况下达到 `THEORY_MAX_ITERATIONS`。

**修复可选方案：**
1. 增加 `THEORY_MAX_ITERATIONS=20`
2. 简化猜想——将其拆分成更小的部分
3. 使用 `--gate human` 参数在运行过程中提供提示

部分证明仍然保存在 `theory_state.json` 中。

---

## 证明被 `refuted`（反驳）

**原因：** 发现了一个反例——所提出的猜想是错误的，或者需要改进。

**修复：**
1. 查看 `theory_state.json → counterexamples[]` 以获取具体的反例。
2. 完善你的猜想（收紧条件，改变界限）
3. 使用更新后的猜想重新运行

---

## 速率限制/API 错误

**原因：**长时间运行期间，Anthropic API 达到速率限制。

**修复方法：** EurekaClaw 会自动使用指数退避算法重试（5 次尝试，每次等待 4-90 秒）。如果错误仍然存​​在：
- 减少 `MAX_TOKENS_AGENT` 和 `MAX_TOKENS_PROVER`
- 设置 `CONTEXT_COMPRESS_AFTER_TURNS=4`
- 设置 `EXPERIMENT_MODE=false`

---

## Lean4 验证未运行

**原因：**在 `PATH` 中找不到 `lean` 二进制文件。

**解决方法：**安装 Lean4 并设置 `LEAN4_BIN=/path/to/lean`。如果没有 Lean4，验证程序将回退到 LLM 同行评审。

---

## 输出文件存在 `[Unverified step]` 警告

**原因：**一个或多个词条的 `verified=false`。

**该怎么办：**
1. 检查 `theory_state.json → proven_lemmas` 中标记的词元
2. 使用 `--gate human` 参数重新运行，并在理论门处提供提示
3. 增加 `THEORY_MAX_ITERANTS`
4. 简化猜想或将其分解为更小的引理

---

## ConsistencyChecker: FAIL — Theorem Statement Truncated

**原因：** `TheoremCrystallizer` 在表达式执行过程中用完了Token。

**修复：** 在 `.env` 增加 `MAX_TOKENS_CRYSTALLIZER`：

```ini
MAX_TOKENS_CRYSTALLIZER=4096
```

如果问题仍然存在，则同时引发 `MAX_TOKENS_ASSEMBLER` 异常。

---

## 示例工作流程

### 验证已知结果（合理性检验）

```bash
eurekaclaw prove "The sum of the first n natural numbers equals n(n+1)/2" \
    --domain "combinatorics" --output ./results
```

预期结果：用 1-2 个简单引理在 5 分钟内证明。

### 探索开放研究领域

```bash
eurekaclaw explore "graph neural networks" \
    --query "What complexity-theoretic barriers exist for GNN expressiveness?" \
    --gate auto --output ./results
```

### 重现并扩展一篇论文

```bash
eurekaclaw from-papers 1706.03762 \
    --domain "transformer theory" --gate human --output ./results
```

### 特定领域（多臂Bandit）研究

```bash
eurekaclaw prove "UCB1 achieves O(sqrt(KT log K)) regret for K-armed Gaussian bandits" \
    --domain "multi-armed bandits" --output ./results
```

多臂Bandit(MAB)插件会自动激活，提供专门的工具和种子技能。
