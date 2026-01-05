# =============================================================================
# Reusable Python Worker Module
# =============================================================================
# Note: Python Workers deployment is still best done via pywrangler.
# This module manages the surrounding infrastructure:
# - KV namespaces
# - D1 databases
# - R2 buckets
# - Secrets
# - Routes (custom domains)
# =============================================================================

# KV Namespace (optional)
resource "cloudflare_workers_kv_namespace" "this" {
  count = var.kv_namespace_name != "" ? 1 : 0

  account_id = var.account_id
  title      = var.kv_namespace_name
}

# D1 Database (optional)
resource "cloudflare_d1_database" "this" {
  count = var.d1_database_name != "" ? 1 : 0

  account_id = var.account_id
  name       = var.d1_database_name
}

# R2 Bucket (optional)
resource "cloudflare_r2_bucket" "this" {
  count = var.r2_bucket_name != "" ? 1 : 0

  account_id = var.account_id
  name       = var.r2_bucket_name
  location   = var.r2_location
}

# Worker Route (for custom domain)
resource "cloudflare_worker_route" "this" {
  count = var.route_pattern != "" ? 1 : 0

  zone_id     = var.zone_id
  pattern     = var.route_pattern
  script_name = var.worker_name
}

# DNS Record (optional, for subdomain)
resource "cloudflare_record" "this" {
  count = var.dns_name != "" ? 1 : 0

  zone_id = var.zone_id
  name    = var.dns_name
  content = "${var.worker_name}.${var.account_id}.workers.dev"
  type    = "CNAME"
  proxied = true
}
