# Terraform - Cloudflare Workers Infrastructure

Manages infrastructure for multiple Python Workers on Cloudflare.

## What This Manages

- **KV Namespaces** - key-value storage
- **D1 Databases** - SQLite at the edge
- **R2 Buckets** - object storage
- **Worker Routes** - custom domain routing
- **DNS Records** - subdomains

**Note:** Worker code deployment is done via `pywrangler deploy`. Terraform manages the surrounding infrastructure.

## Setup

```bash
cd terraform

# Copy and fill in your credentials
cp terraform.tfvars.example terraform.tfvars

# Get your account ID:
# Cloudflare Dashboard → Workers & Pages → right side shows Account ID

# Create API token:
# Cloudflare Dashboard → My Profile → API Tokens → Create Token
# Use "Edit Cloudflare Workers" template, add D1/R2/KV permissions as needed
```

## Usage

```bash
cd terraform

# Initialize
terraform init

# Preview changes
terraform plan

# Apply
terraform apply
```

## Adding a New Worker

1. Create worker directory:
```bash
mkdir workers/my-new-worker
```

2. Create `workers/my-new-worker/main.tf`:
```hcl
variable "account_id" { type = string }

module "worker" {
  source = "../../modules/python-worker"

  account_id  = var.account_id
  worker_name = "my-new-worker"

  # Add storage as needed
  # kv_namespace_name = "my-worker-cache"
  # d1_database_name  = "my-worker-db"
}

output "worker_url" {
  value = module.worker.worker_url
}
```

3. Add to `main.tf`:
```hcl
module "my_new_worker" {
  source     = "./workers/my-new-worker"
  account_id = var.cloudflare_account_id
}
```

4. Run `terraform apply`

5. Copy output IDs to your worker's `wrangler.toml`

## Workflow

```
┌─────────────────┐     ┌──────────────────┐
│ terraform apply │ ──▶ │ Creates KV/D1/R2 │
└─────────────────┘     │ Returns IDs      │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ Update wrangler  │
                        │ .toml with IDs   │
                        └────────┬─────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ pywrangler deploy│
                        └──────────────────┘
```

## Structure

```
terraform/
├── main.tf                 # Root module, provider config
├── variables.tf            # Input variables
├── outputs.tf              # Output values
├── terraform.tfvars        # Your credentials (gitignored)
├── modules/
│   └── python-worker/      # Reusable worker infrastructure
└── workers/
    ├── echo-webhook/       # Echo webhook worker
    └── another-worker/     # Add more workers here
```
