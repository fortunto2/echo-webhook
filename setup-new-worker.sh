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
WORKER_NAME_UNDERSCORE="${WORKER_NAME//-/_}"

echo "Creating new worker: $WORKER_NAME"

# Update wrangler.toml
sed -i '' "s/name = \"echo-webhook\"/name = \"$WORKER_NAME\"/" wrangler.toml

# Update pyproject.toml
sed -i '' "s/name = \"echo-webhook\"/name = \"$WORKER_NAME\"/" pyproject.toml
sed -i '' "s/description = \".*\"/description = \"$WORKER_NAME - Cloudflare Python Worker\"/" pyproject.toml

# Update FastAPI app title
sed -i '' "s/title=\"Echo Webhook\"/title=\"$WORKER_NAME\"/" src/entry.py

# Update terraform
mv terraform/workers/echo-webhook "terraform/workers/$WORKER_NAME"
sed -i '' "s/worker_name = \"echo-webhook\"/worker_name = \"$WORKER_NAME\"/" "terraform/workers/$WORKER_NAME/main.tf"
sed -i '' "s/module \"echo_webhook\"/module \"$WORKER_NAME_UNDERSCORE\"/" terraform/main.tf
sed -i '' "s|./workers/echo-webhook|./workers/$WORKER_NAME|" terraform/main.tf
sed -i '' "s/echo_webhook_url/${WORKER_NAME_UNDERSCORE}_url/" terraform/outputs.tf
sed -i '' "s/module.echo_webhook/module.$WORKER_NAME_UNDERSCORE/" terraform/outputs.tf

echo ""
echo "✅ Done! Worker renamed to: $WORKER_NAME"
echo ""
echo "Next steps:"
echo "  1. Update README.md with your project description"
echo "  2. cp terraform/terraform.tfvars.example terraform/terraform.tfvars"
echo "  3. Add your API token to terraform/terraform.tfvars"
echo "  4. uv sync"
echo "  5. uv run pywrangler dev   # test locally"
echo "  6. uv run pywrangler deploy"
echo ""
