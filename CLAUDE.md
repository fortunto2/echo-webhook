# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Echo Webhook is a Python-based Cloudflare Worker using FastAPI and Pydantic. It echoes back any JSON payload sent to it.

**Deployed at:** https://echo-webhook.nameless-sunset-8f24.workers.dev

## Commands

```bash
# Install dependencies
uv sync

# Run locally
uv run pywrangler dev

# Deploy to Cloudflare
uv run pywrangler deploy
```

## Architecture

- **`src/entry.py`** - Single entry point containing:
  - FastAPI app with endpoints (`/`, `/health`, `/webhook`, `/webhook/typed`)
  - Pydantic models for request validation
  - `Default` class extending `WorkerEntrypoint` that bridges FastAPI to Cloudflare's ASGI handler

- **`wrangler.toml`** - Cloudflare Worker configuration. Must use `compatibility_date >= 2025-10-16` for FastAPI/Pydantic support (enables `python_dedicated_snapshot` optimization)

## Key Constraints

- Python Workers are experimental; require `python_workers` compatibility flag
- Only packages supported by Pyodide work (pure Python or pre-compiled for WebAssembly)
- Heavy packages like FastAPI/Pydantic need `compatibility_date >= 2025-10-16` to avoid CPU startup limits
- If deployment fails with CPU limit errors, clear `python_modules/` and `.venv-workers/` and redeploy
