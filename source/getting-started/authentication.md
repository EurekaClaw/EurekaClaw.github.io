# Authentication

EurekaClaw supports three authentication methods.

## Option A — Anthropic API Key (Most Common)

```bash
cp .env.example .env
```

Edit `.env`:

```ini
ANTHROPIC_API_KEY=sk-ant-...
```

## Option B — Claude Pro/Max via OAuth

No API key required. Uses your Claude Pro or Max subscription.

```bash
pip install "eurekaclaw[oauth]"
ccproxy auth login claude_api   # opens browser for one-time login
```

```ini
ANTHROPIC_AUTH_MODE=oauth
```

EurekaClaw automatically starts and stops ccproxy alongside your session.

## Option C — Codex via OAuth

No API key required. Uses your Codex subscription.

```bash
pip install "eurekaclaw[codex]"
codex auth login   # first login your own Codex
eurekaclaw login --provider openai-codex
```

## Option D — OpenRouter or Local Model

### OpenRouter

```ini
LLM_BACKEND=openrouter
OPENAI_COMPAT_BASE_URL=https://openrouter.ai/api/v1
OPENAI_COMPAT_API_KEY=sk-or-...
OPENAI_COMPAT_MODEL=anthropic/claude-sonnet-4-6
```

### Local Ollama / vLLM

```ini
LLM_BACKEND=local
OPENAI_COMPAT_BASE_URL=http://localhost:11434/v1
OPENAI_COMPAT_MODEL=llama3
```

### Minimax

```ini
LLM_BACKEND=minimax
MINIMAX_API_KEY=...
MINIMAX_MODEL=abab7-chat
```

See [Configuration](../reference/configuration.md) for all LLM backend options.
