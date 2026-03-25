# Gate Mode and Human Review

EurekaClaw includes interactive gates that pause the pipeline and ask for your input at key decision points. Gates work in both the browser UI and the CLI.

## Browser UI Gates

When running `eurekaclaw ui`, gates appear as overlay dialogs on top of the workspace — no matter which tab you are on. There are three gates:

**Survey gate** — triggers when the literature survey finds 0 papers.

The overlay asks you to provide paper IDs or arXiv IDs to retry the survey, or to continue without papers.

**Direction gate** — triggers when ideation returns no candidate research directions (detailed/prove mode).

The overlay shows the original conjecture as a default and lets you type a custom direction, or accept the conjecture as-is.

**Theory review gate** — triggers after the theorem-prover completes.

The overlay shows the assembled proof and lets you either approve it (pipeline continues to experiments and writing) or flag a specific lemma with a reason. Flagging causes the theory agent to re-run with your feedback injected. After a configurable number of retries (`THEORY_REVIEW_MAX_RETRIES`, default 3) the proof is auto-approved.

## CLI Gates

When running from the terminal, the same gates appear as interactive prompts.

### `--gate none` (Default)

Fully automatic. Runs end-to-end with no interaction. Summary cards are printed but the pipeline never pauses.

```bash
eurekaclaw prove "..." --gate none
```

### `--gate auto`

Summary cards after each stage. Pauses for human review **only** when a low-confidence lemma is detected (i.e., `verified=false` after the theory stage). Good for catching problems without constant interruption.

```bash
eurekaclaw prove "..." --gate auto
```

### `--gate human`

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
