# 错误检索

## `No skills available` / Proof Fails Immediately

**Cause:** The initial skill set has not been installed. This happens when `eurekaclaw install-skills` was skipped during setup.

**Fix:**

```bash
eurekaclaw install-skills
```

This downloads the built-in seed skills (proof strategies, domain heuristics, lemma templates) required for the pipeline to run. Re-run it any time you want to reset skills to the defaults.

---

## `paper.pdf` Not Generated

**Cause:** `pdflatex` not installed or not in `PATH`.

**Fix:**
- Linux: `sudo apt install texlive-full`
- macOS: install [MacTeX](https://www.tug.org/mactex/)
- Set `LATEX_BIN=/usr/local/bin/pdflatex` in `.env`

The `.tex` and `.bib` files are always saved — compile manually or upload to Overleaf.

---

## Citations Show as `?` in the PDF

**Cause:** bibtex not run, or cite keys mismatch.

**Fix:** Run the compile sequence manually:

```bash
cd results/<session_id>
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

---

## `Parsed zero lemmas from architect response`

**Cause:** LLM returned an unrecognized proof plan format.

**Fix:** Handled automatically via a 4-pass parser. If it persists, use a more capable model (`EUREKACLAW_MODEL`) and retry.

---

## Proof Status is `abandoned`

**Cause:** Hit `THEORY_MAX_ITERATIONS` without completing all lemmas.

**Fix options:**
1. Increase `THEORY_MAX_ITERATIONS=20`
2. Simplify the conjecture — split into smaller parts
3. Use `--gate human` to provide hints during the run

The partial proof is still saved in `theory_state.json`.

---

## Proof was `refuted`

**Cause:** A counterexample was found — the conjecture as stated is false or needs refinement.

**What to do:**
1. Check `theory_state.json → counterexamples[]` for the specific falsifying example
2. Refine your conjecture (tighten conditions, change the bound)
3. Re-run with the updated conjecture

---

## Rate Limit / API Errors

**Cause:** Anthropic API rate limit hit during a long run.

**Fix:** EurekaClaw retries automatically with exponential backoff (5 attempts, 4–90 second waits). If errors persist:
- Reduce `MAX_TOKENS_AGENT` and `MAX_TOKENS_PROVER`
- Set `CONTEXT_COMPRESS_AFTER_TURNS=4`
- Set `EXPERIMENT_MODE=false`

---

## Lean4 Verification Not Running

**Cause:** `lean` binary not found in `PATH`.

**Fix:** Install Lean4 and set `LEAN4_BIN=/path/to/lean`. Without Lean4, the verifier falls back to LLM peer review.

---

## The Output Paper Has `[Unverified step]` Warnings

**Cause:** One or more lemmas have `verified=false`.

**What to do:**
1. Check `theory_state.json → proven_lemmas` for flagged lemmas
2. Re-run with `--gate human` and provide hints at the theory gate
3. Increase `THEORY_MAX_ITERATIONS`
4. Simplify the conjecture or break it into smaller lemmas

---

## ConsistencyChecker: FAIL — Theorem Statement Truncated

**Cause:** `TheoremCrystallizer` ran out of tokens mid-expression.

**Fix:** Increase `MAX_TOKENS_CRYSTALLIZER` in `.env`:

```ini
MAX_TOKENS_CRYSTALLIZER=4096
```

If the issue persists, also raise `MAX_TOKENS_ASSEMBLER`.

---

## `AttributeError: 'ProofPausedException' object has no attribute 'paused_before_stage'`

**Cause:** Outdated code. The correct attribute is `stage_name`.

**Fix:** Pull the latest version: `git pull`

---

## Example Workflows

### Prove a Known Result (Sanity Check)

```bash
eurekaclaw prove "The sum of the first n natural numbers equals n(n+1)/2" \
    --domain "combinatorics" --output ./results
```

Expected: `proved` with 1–2 simple lemmas in under 5 minutes.

### Explore an Open Research Area

```bash
eurekaclaw explore "graph neural networks" \
    --query "What complexity-theoretic barriers exist for GNN expressiveness?" \
    --gate auto --output ./results
```

### Reproduce + Extend a Paper

```bash
eurekaclaw from-papers 1706.03762 \
    --domain "transformer theory" --gate human --output ./results
```

### Domain-Specific MAB Research

```bash
eurekaclaw prove "UCB1 achieves O(sqrt(KT log K)) regret for K-armed Gaussian bandits" \
    --domain "multi-armed bandits" --output ./results
```

The MAB domain plugin activates automatically, providing specialized tools and seed skills.
