# Echo Webhook

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

#### Why not use standard Python hosting?

| Option | Cold Start | Global Edge | Free Tier |
|--------|-----------|-------------|-----------|
| Cloudflare Workers | ~1s (with snapshot) | Yes (330+ PoPs) | 100k req/day |
| AWS Lambda | 1-3s | No (regional) | 1M req/month |
| Google Cloud Run | 2-5s | No (regional) | 2M req/month |
| Vercel Functions | 1-2s | Yes | 100k req/month |

Cloudflare Workers offer the best combination of edge deployment and fast cold starts for simple webhook services.

### Project Structure

```
├── src/entry.py      # FastAPI app + Worker entrypoint
├── wrangler.toml     # Cloudflare Worker config
├── pyproject.toml    # Python dependencies (uv)
└── python_modules/   # Bundled deps for Pyodide (auto-generated)
```

## Troubleshooting

**"Python Worker startup exceeded CPU limit"**

```bash
rm -rf python_modules .venv-workers
uv run pywrangler deploy
```

This clears cached packages and forces fresh Pyodide-compatible installation.

## License

MIT
