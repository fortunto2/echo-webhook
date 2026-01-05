output "kv_namespace_id" {
  description = "KV namespace ID (for wrangler.toml)"
  value       = try(cloudflare_workers_kv_namespace.this[0].id, null)
}

output "d1_database_id" {
  description = "D1 database ID (for wrangler.toml)"
  value       = try(cloudflare_d1_database.this[0].id, null)
}

output "r2_bucket_name" {
  description = "R2 bucket name"
  value       = try(cloudflare_r2_bucket.this[0].name, null)
}

output "worker_url" {
  description = "Worker URL"
  value       = "https://${var.worker_name}.workers.dev"
}
