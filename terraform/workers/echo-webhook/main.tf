# =============================================================================
# Echo Webhook Worker Infrastructure
# =============================================================================
# The worker code itself is deployed via: uv run pywrangler deploy
# This manages the surrounding infrastructure (KV, D1, routes, etc.)
# =============================================================================

variable "account_id" {
  type = string
}

variable "zone_id" {
  type    = string
  default = ""
}

variable "route_pattern" {
  type    = string
  default = ""
}

module "worker" {
  source = "../../modules/python-worker"

  account_id  = var.account_id
  worker_name = "echo-webhook"

  # Uncomment to add storage
  # kv_namespace_name = "echo-webhook-cache"
  # d1_database_name  = "echo-webhook-db"
  # r2_bucket_name    = "echo-webhook-storage"

  # Uncomment for custom domain routing
  # zone_id       = var.zone_id
  # route_pattern = var.route_pattern
  # dns_name      = "webhook"
}

output "worker_url" {
  value = module.worker.worker_url
}

output "kv_namespace_id" {
  value = module.worker.kv_namespace_id
}

output "d1_database_id" {
  value = module.worker.d1_database_id
}
