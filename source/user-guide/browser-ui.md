# Browser UI

## Launching the UI

### One-line commands

```bash
# Production — build frontend, open browser, serve on :8080
make open

# Production — build frontend, serve on :8080 (no browser)
make start

# Development — hot-reload Vite on :5173 + Python backend on :7860
make dev

# Or via the CLI directly (serves the last build)
eurekaclaw ui --open-browser
```

With a custom host/port:

```bash
eurekaclaw ui --host 0.0.0.0 --port 8080 --open-browser
```

### How it works

| Mode | Frontend | Backend | URL |
|---|---|---|---|
| **Production** (`make start`) | Pre-built bundle in `eurekaclaw/ui/static/` | Python server + API on same port | `http://localhost:8080` |
| **Dev** (`make dev`) | Vite dev server with HMR | Python API on `:7860`; Vite proxies `/api/*` | `http://localhost:5173` |

### Frontend build (when you change React code)

```bash
make build       # tsc + vite build → eurekaclaw/ui/static/
make typecheck   # type-check only, no output
```

---

## Views

### Workspace

The main view when a session is selected. Contains:

- **Agent track** (left) — one card per pipeline stage (Survey · Ideation · Theory · Validation · Writing). Click any card to open the Agent Drawer with stage-specific details.
- **Tabs** (right):

| Tab | Content |
|---|---|
| **Live** | Real-time stage cards, log stream, thinking animation while running |
| **Proof** | Theorem block, lemma chain with confidence badges, counterexample warnings |
| **Paper** | PDF download, Generate PDF, LaTeX source viewer with copy button |
| **Logs** | Full raw log output |

### Skills

Browse, install, and delete skills. Left panel shows seed skills; right panel is the ClawHub external install panel. Each skill card shows usage count and success rate.

### Config

Edit all `.env` variables in the browser, including 12 `MAX_TOKENS_*` sliders. Changes are written directly to your `.env` file and take effect on the next run. See [Token Limits](../reference/token-limits.md) for what each slider controls.

### Onboarding

The interactive setup wizard (shown on first launch). Guides through model selection, API key setup, optional tools, and skills installation. Can be re-opened at any time via the Guide button in the bottom-right corner.

---

## Session Controls

### Pause / Resume

While a session is running, a **Pause proof** button appears. EurekaClaw stops gracefully at the next lemma boundary and writes a checkpoint to `~/.eurekaclaw/sessions/<session_id>/checkpoint.json`.

When paused, you can optionally type feedback before resuming:

```
📐 Guide the proof before resuming

Lemma chips: [concentration_bound] [main_result] ...
Textarea: "Use Bernstein instead of Hoeffding for lemma 2"
```

Feedback is injected directly into the next theory attempt.

### Session list status indicators

| Status | Visual |
|---|---|
| Running | Blue `RUNNING` tag |
| Pausing | Amber `PAUSING…` tag (pulsing) |
| Paused | Amber `PAUSED` tag |
| Resuming | Green `RESUMING…` tag (pulsing) |
| Completed | Green `FINISHED` tag |
| Failed | Red `FAILED` tag |

Failed sessions show a **Restart** button that carries the original query to a new run.

---

## Gate Overlays

Gates appear as overlay dialogs on top of the workspace — no matter which tab you are on. There are three gates:

| Gate | When it appears | What you can do |
|---|---|---|
| **Survey** | Literature survey finds 0 papers | Provide paper IDs or arXiv IDs to retry, or continue without papers |
| **Direction** | Ideation returns no candidate research directions | Type a custom direction or accept the original conjecture as-is |
| **Theory Review** | After the theorem-prover completes | Approve to continue to writing, or flag a specific lemma with a reason — flagging triggers a re-run with your feedback injected; auto-approved after `THEORY_REVIEW_MAX_RETRIES` retries (default 3) |
