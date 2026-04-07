# API Key授权

EurekaClaw支持4种认证方式。

:::{note} 
注意：Anthropic等订阅模型供应商可能不再支持通过OAuth途径使用订阅，请谨慎选择
:::

## 选项一 — Anthropic API Key

```bash
cp .env.example .env
```

修改 `.env`：

```ini
ANTHROPIC_API_KEY=sk-ant-...
```

## 选项二 — Claude Pro/Max（通过 OAuth）

不需要API Key。用您的Claude Pro/Max订阅。

```bash
pip install "eurekaclaw[oauth]"
ccproxy auth login claude_api   # opens browser for one-time login
```

```ini
ANTHROPIC_AUTH_MODE=oauth
```

EurekaClaw 在你的对话过程中自动开启和停止ccproxy。

## 选项三 — Codex（通过 OAuth）

不需要API Key。用您的Codex订阅。

```bash
pip install "eurekaclaw[codex]"
codex auth login   # first login your own Codex
eurekaclaw login --provider openai-codex
```

## 选项四 — OpenRouter、Novita AI或者本地模型

### OpenRouter

```ini
LLM_BACKEND=openrouter
OPENAI_COMPAT_BASE_URL=https://openrouter.ai/api/v1
OPENAI_COMPAT_API_KEY=sk-or-...
OPENAI_COMPAT_MODEL=anthropic/claude-sonnet-4-6
```

### Novita AI

```ini
LLM_BACKEND=novita
OPENAI_COMPAT_BASE_URL=https://api.novita.ai/openai
NOVITA_API_KEY=<Your API Key>
NOVITA_MODEL=deepseek/deepseek-v3.2
```

### 本地 Ollama / vLLM

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

参考 [配置](../reference/configuration.md) 查看所有LLM支持.
