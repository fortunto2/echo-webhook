# Echo Webhook

[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?logo=cloudflare)](https://workers.cloudflare.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

Simple webhook service that echoes back any JSON payload. Built with **FastAPI + Pydantic** running on **Cloudflare Workers** (Python).

**Live:** https://echo-webhook.nameless-sunset-8f24.workers.dev

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service status |
| GET | `/health` | Health check with timestamp |
| POST | `/webhook` | Echo any JSON payload |
| POST | `/webhook/typed` | Echo with Pydantic validation |

## Quick Start

```bash
# Install dependencies
uv sync

# Run locally
uv run pywrangler dev

# Deploy
uv run pywrangler deploy
```

## Example

```bash
# Simple echo
curl -X POST https://echo-webhook.nameless-sunset-8f24.workers.dev/webhook \
  -H "Content-Type: application/json" \
  -d '{"hello": "world"}'
```

Response:
```json
{
  "status": "ok",
  "received_at": "2026-01-05T09:04:15.201999",
  "echo": {"hello": "world"}
}
```

### Typed endpoint with validation

```bash
curl -X POST https://echo-webhook.nameless-sunset-8f24.workers.dev/webhook/typed \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "data": {"foo": "bar"}}'
```

If payload doesn't match schema, returns 422 with validation errors.

## Extending to SGR Agent

This template is designed as a foundation for building **Schema-Guided Reasoning (SGR)** agents. SGR forces LLMs to reason through predefined Pydantic schemas.

Example extension in `src/entry.py`:

```python
from pydantic import BaseModel, Field
from enum import Enum

class ApproachType(str, Enum):
    direct_answer = "direct_answer"
    multi_step = "multi_step"
    clarification_needed = "clarification_needed"

class TaskAnalysis(BaseModel):
    """Step 1: LLM must fill all fields"""
    task_understanding: str = Field(description="Restate task in own words")
    key_entities: list[str] = Field(description="Key concepts involved")
    approach: ApproachType

class StepReasoning(BaseModel):
    """Step 2: Forced chain-of-thought"""
    step_1_gather: str = Field(description="What info is needed?")
    step_2_analyze: str = Field(description="Analysis of gathered info")
    step_3_synthesize: str = Field(description="Combine into answer")
    confidence: float = Field(ge=0, le=1)
    final_answer: str

@app.post("/agent")
async def sgr_agent(request: Request):
    body = await request.json()
    # Call LLM with TaskAnalysis schema (tool_use)
    # Then call with StepReasoning schema
    # Return structured reasoning trace
    ...
```

See [Schema-Guided Reasoning](https://abdullin.com/schema-guided-reasoning/) for more on SGR patterns.

## Why These Choices?

### Why Cloudflare Workers?

- **Global edge deployment** — runs in 330+ locations worldwide, ~50ms latency globally
- **No cold starts with memory snapshots** — Cloudflare captures Python runtime state at deploy time
- **Generous free tier** — 100,000 requests/day, no credit card required
- **Zero infrastructure management** — no servers, containers, or scaling to configure

### Why Python + FastAPI?

- **FastAPI** — modern async Python web framework with automatic OpenAPI docs
- **Pydantic** — runtime type validation with clear error messages
- **Python Workers** — Cloudflare's experimental Python support via Pyodide (WebAssembly)

### Key Configuration Decisions

#### `compatibility_date = "2025-10-16"`

Required for FastAPI + Pydantic to work. This date enables `python_dedicated_snapshot` optimization that:
- Reduces startup CPU from ~1800ms to within the 1000ms limit
- Pre-compiles heavy Python imports at deploy time
- Without this, deployment fails with "exceeded CPU limit" error

#### Comparison with alternatives

| Option | Cold Start | Global Edge | Free Tier |
|--------|-----------|-------------|-----------|
| Cloudflare Workers | ~1s (with snapshot) | Yes (330+ PoPs) | 100k req/day |
| AWS Lambda | 1-3s | No (regional) | 1M req/month |
| Google Cloud Run | 2-5s | No (regional) | 2M req/month |
| Vercel Functions | 1-2s | Yes | 100k req/month |

Cloudflare Workers offer the best combination of edge deployment and fast cold starts for simple webhook services.

## Project Structure

```
├── src/entry.py      # FastAPI app + Worker entrypoint
├── wrangler.toml     # Cloudflare Worker config
├── pyproject.toml    # Python dependencies (uv)
├── CLAUDE.md         # Instructions for Claude Code
└── python_modules/   # Bundled deps for Pyodide (auto-generated)
```

## Adding Secrets

For SGR agent with LLM calls:

```bash
# Add Anthropic API key
wrangler secret put ANTHROPIC_API_KEY

# Access in code via self.env.ANTHROPIC_API_KEY
```

## Troubleshooting

**"Python Worker startup exceeded CPU limit"**

```bash
rm -rf python_modules .venv-workers
uv run pywrangler deploy
```

This clears cached packages and forces fresh Pyodide-compatible installation.

**"Module not found" errors**

Only pure Python packages or those pre-compiled in Pyodide work. Check [Pyodide packages](https://pyodide.org/en/stable/usage/packages-in-pyodide.html).

## Related

- [Cloudflare Python Workers docs](https://developers.cloudflare.com/workers/languages/python/)
- [Schema-Guided Reasoning (SGR)](https://abdullin.com/schema-guided-reasoning/)
- [FastAPI on Workers](https://developers.cloudflare.com/workers/languages/python/packages/fastapi/)

## License

MIT
