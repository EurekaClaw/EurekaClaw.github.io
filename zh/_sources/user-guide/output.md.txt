# 输出内容

运行后，`./results/<session_id>/` 包含：

| 文件 | 描述 |
|---|---|
| `paper.pdf` | 编译后的 PDF 文件（需要 pdflatex 和 bibtex） |
| `paper.tex` | 完整的 LaTeX 源代码 — 如有需要，可编辑并重新编译 |
| `references.bib` | BibTeX 参考文献  |
| `theory_state.json` | 完整证明状态 — 引理、证明、置信度评分 |
| `research_brief.json` | 规划状态 — 研究方向评分和已选 |
| `experiment_result.json` | 数值验证结果（如果实验已运行） |

暂停的会话还会向 `~/.eurekaclaw/sessions/<session_id>/checkpoint.json` 写入一个检查点。

## 读取 `theory_state.json`

关键字段:

```
{
  "status": "proved",
  "proof_plan": [
    {
      "lemma_id": "concentration_bound",
      "provenance": "known",
      "statement": "For sub-Gaussian ..."
    }
  ],
  "proven_lemmas": {
    "main_result": {
      "verified": true,
      "confidence_score": 0.91,
      "verification_method": "llm_check",
      "proof_text": "..."
    }
  },
  "failed_attempts": [ ... ],
  "counterexamples": [ ... ]
}
```

### 证明状态

| 状态 | 含义 |
|---|---|
| `proved` | 所有引理均已验证，证明完毕 |
| `refuted` | 已找到反例；该猜想是错误的或需要完善 |
| `abandoned` | 未完成就达到了 `THEORY_MAX_ITERATIONS`；部分证明已保存 |

### 引理来源

| 来源 | 含义 |
|---|---|
| `known` | 可直接引用——无需新的证据 |
| `adapted` | 已验证的结果，经过修改以适应此上下文 |
| `new` | 真正意义上的创新——从零开始，完全验证 |

## 低置信度警告

如果某个词条的 `verified=false` 为真，则 PDF 包含：

```
[Unverified step]   ← orange text
```

以及一个 **Limitations** 部分解释了所有未经验证的步骤。请查看 `theory_state.json → proven_lemmas` 以了解哪些词条已被标记。

## 使用 Python API 访问结果

```python
import json

state = json.loads(result.theory_state_json)
print("Status:", state["status"])
print("Lemmas:", len(state["proof_plan"]))

brief = json.loads(result.research_brief_json)
direction = brief["selected_direction"]
print("Direction:", direction["title"])
print("Novelty score:", direction["novelty_score"])
```

有关完整详细信息，请参阅 [Python API](../reference/api.md)。
