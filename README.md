# Cloudflare Python Agent Template

[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?logo=cloudflare)](https://workers.cloudflare.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

Template for building **multiple AI agents** on **Cloudflare Workers** with FastAPI + Pydantic.

**Live example:** https://echo-webhook.nameless-sunset-8f24.workers.dev

## Quick Start

```bash
git clone https://github.com/fortunto2/echo-webhook.git my-agents
cd my-agents
./setup-new-worker.sh my-agents
uv sync
uv run pywrangler deploy
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List agents with their schemas |
| GET | `/health` | Health check |
| GET | `/docs` | OpenAPI UI |
| POST | `/agents/{name}` | Run agent by name |

## Adding a New Agent

**1. Create agent file:**

```python
# src/agents/summarizer.py
from pydantic import BaseModel
from .base import BaseAgent
from .registry import register


class SummarizerInput(BaseModel):
    text: str
    max_length: int = 100

class SummarizerOutput(BaseModel):
    agent: str = "summarizer"
    summary: str


@register
class SummarizerAgent(BaseAgent):
    name = "summarizer"
    input_model = SummarizerInput
    output_model = SummarizerOutput

    async def run(self, input_data: SummarizerInput) -> SummarizerOutput:
        # Your logic here (call LLM, process data, etc.)
        summary = input_data.text[:input_data.max_length]
        return SummarizerOutput(summary=summary)
```

**2. Register agent:**

```python
# src/agents/__init__.py
from . import echo
from . import summarizer  # Add this line
```

**3. Done!** Endpoint `/agents/summarizer` is now available:

```bash
curl -X POST https://your-worker.workers.dev/agents/summarizer \
  -H "Content-Type: application/json" \
  -d '{"text": "Long text here...", "max_length": 50}'
```

## Project Structure

```
src/
├── entry.py              # FastAPI app + routes
├── core/
│   ├── models.py         # Shared Pydantic models
│   └── llm.py            # OpenAI client wrapper
└── agents/
    ├── base.py           # BaseAgent class
    ├── registry.py       # @register decorator
    └── echo.py           # Example agent
```

## Using LLM in Agents

```python
# src/agents/smart.py
from .base import BaseAgent
from .registry import register
from core.llm import get_openai_client, chat_completion

@register
class SmartAgent(BaseAgent):
    name = "smart"

    async def run(self, input_data):
        # Access API key from worker env
        client = get_openai_client(self.env.OPENAI_API_KEY)
        response = await chat_completion(client, [
            {"role": "user", "content": input_data.query}
        ])
        return {"result": response}
```

Add secret: `wrangler secret put OPENAI_API_KEY`

## Adding Storage

```bash
wrangler kv namespace create CACHE      # Key-value
wrangler d1 create my-db                # SQLite
wrangler r2 bucket create my-bucket     # Object storage
```

## Why Cloudflare Workers?

- **Global edge** — 330+ locations, ~50ms latency
- **No cold starts** — memory snapshots at deploy
- **Free tier** — 100k requests/day
- **Zero ops** — no servers to manage

## Troubleshooting

**CPU limit errors:**
```bash
rm -rf python_modules .venv-workers && uv run pywrangler deploy
```

**Module not found:** Check [Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html)

## License

MIT
