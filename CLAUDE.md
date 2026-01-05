# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agent Service - Python-based Cloudflare Worker using FastAPI and Pydantic. Template for building multiple AI agents in a single worker.

**Deployed at:** https://echo-webhook.nameless-sunset-8f24.workers.dev

## Commands

```bash
uv sync                    # Install dependencies
uv run pywrangler dev      # Run locally
uv run pywrangler deploy   # Deploy to Cloudflare
```

## Architecture

```
src/
├── entry.py           # FastAPI app, routes, worker entrypoint
├── core/
│   ├── models.py      # Shared Pydantic models
│   └── llm.py         # OpenAI client wrapper
└── agents/
    ├── base.py        # BaseAgent abstract class
    ├── registry.py    # @register decorator, AGENTS dict
    └── echo.py        # Example agent
```

## Adding a New Agent

1. Create `src/agents/myagent.py`:
```python
from typing import Any
from pydantic import BaseModel
from .base import BaseAgent
from .registry import register


class MyInput(BaseModel):
    query: str

class MyOutput(BaseModel):
    agent: str = "myagent"
    result: str

@register
class MyAgent(BaseAgent):
    name = "myagent"
    input_model = MyInput
    output_model = MyOutput

    async def run(self, input_data: MyInput) -> MyOutput:
        # Your logic here
        return MyOutput(result=f"Processed: {input_data.query}")
```

2. Add import in `src/agents/__init__.py`:
```python
from . import echo
from . import myagent  # Add this line
```

3. Done! Endpoint `/agents/myagent` is now available.

## Key Constraints

- Python Workers require `python_workers` compatibility flag
- Only Pyodide-supported packages work (pure Python or pre-compiled for WebAssembly)
- Need `compatibility_date >= 2025-10-16` for FastAPI/Pydantic
- If deployment fails with CPU limit errors: `rm -rf python_modules .venv-workers && uv run pywrangler deploy`

## Endpoints

- `GET /` — list agents with their schemas
- `GET /health` — health check
- `GET /docs` — OpenAPI UI
- `POST /agents/{name}` — run agent by name
