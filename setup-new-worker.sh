#!/bin/bash
# Setup script for creating a new worker from this template
# Usage: ./setup-new-worker.sh my-new-worker

set -e

if [ -z "$1" ]; then
    echo "Usage: ./setup-new-worker.sh <worker-name>"
    echo "Example: ./setup-new-worker.sh my-api-worker"
    exit 1
fi

WORKER_NAME="$1"

echo "Creating new worker: $WORKER_NAME"

# Update wrangler.toml
sed -i '' "s/name = \"echo-webhook\"/name = \"$WORKER_NAME\"/" wrangler.toml

# Update pyproject.toml
sed -i '' "s/name = \"echo-webhook\"/name = \"$WORKER_NAME\"/" pyproject.toml
sed -i '' "s/description = \".*\"/description = \"$WORKER_NAME - Cloudflare Python Worker\"/" pyproject.toml

# Update FastAPI app title
sed -i '' "s/title=\"Echo Webhook\"/title=\"$WORKER_NAME\"/" src/entry.py

echo ""
echo "Done! Worker renamed to: $WORKER_NAME"
echo ""
echo "Next steps:"
echo "  1. uv sync"
echo "  2. uv run pywrangler dev   # test locally"
echo "  3. uv run pywrangler deploy"
echo ""
