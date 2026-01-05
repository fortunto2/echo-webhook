# Template Repository

This repository is designed to be used as a template for creating new Cloudflare Python Workers.

## After Creating from Template

1. Run the setup script:
   ```bash
   ./setup-new-worker.sh your-worker-name
   ```

2. Set up credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your Cloudflare account ID and API token
   ```

3. Deploy:
   ```bash
   uv sync
   uv run pywrangler deploy
   ```

## What Gets Renamed

The setup script automatically updates:
- `wrangler.toml` - worker name
- `pyproject.toml` - package name
- `src/entry.py` - FastAPI app title
- `terraform/` - module names and references
