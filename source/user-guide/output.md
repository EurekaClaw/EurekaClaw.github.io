# Understanding the Output

After a run, `./results/<session_id>/` contains:

| File | Description |
|---|---|
| `paper.pdf` | Compiled PDF (requires pdflatex + bibtex) |
| `paper.tex` | Full LaTeX source — edit and recompile if needed |
| `references.bib` | BibTeX bibliography |
| `theory_state.json` | Full proof state — lemmas, proofs, confidence scores |
| `research_brief.json` | Planning state — directions scored and selected |
| `experiment_result.json` | Numerical validation results (if experiment ran) |

Paused sessions also write a checkpoint to `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`.

## Reading `theory_state.json`

Key fields:

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

### Proof Status

| Status | Meaning |
|---|---|
| `proved` | All lemmas verified, assembled proof complete |
| `refuted` | A counterexample was found; the conjecture is false or needs refinement |
| `abandoned` | Hit `THEORY_MAX_ITERATIONS` without completing; partial proof saved |

### Lemma Provenance

| Provenance | Meaning |
|---|---|
| `known` | Directly citable — no new proof needed |
| `adapted` | A known result modified to fit this context |
| `new` | Genuinely novel — fully proved from scratch |

## Low-Confidence Warnings

If a lemma has `verified=false`, the PDF contains:

```
[Unverified step]   ← orange text
```

and a **Limitations** section explaining all unverified steps. Review `theory_state.json → proven_lemmas` to see which lemmas are flagged.

## Using the Python API to Access Results

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

See [Python API](../reference/api.md) for full details.
