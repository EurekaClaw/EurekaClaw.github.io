# Browser UI

Launch the local web interface:

```bash
eurekaclaw ui --open-browser
```

With a custom host/port:

```bash
eurekaclaw ui --host 0.0.0.0 --port 8080 --open-browser
```

## Panels

| Panel | Description |
|---|---|
| **Run** | Enter conjecture/domain, configure options, start a session |
| **Live progress** | Real-time stage cards and log stream |
| **Results viewer** | Browse the generated paper, theory state, and experiment results |
| **Settings** | Edit all `.env` variables including 12 token-limit sliders |
| **Skills** | Browse and manage the skill bank |

## Token Limit Sliders

The Settings tab exposes all 12 `MAX_TOKENS_*` variables as sliders. Changes are written directly to your `.env` file and take effect on the next run. See [Token Limits](../reference/token-limits.md) for what each slider controls.
