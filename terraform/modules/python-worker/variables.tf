variable "account_id" {
  description = "Cloudflare account ID"
  type        = string
}

variable "worker_name" {
  description = "Worker script name (must match wrangler.toml)"
  type        = string
}

variable "zone_id" {
  description = "Cloudflare zone ID (required for routes/DNS)"
  type        = string
  default     = ""
}

# KV
variable "kv_namespace_name" {
  description = "KV namespace name (empty to skip)"
  type        = string
  default     = ""
}

# D1
variable "d1_database_name" {
  description = "D1 database name (empty to skip)"
  type        = string
  default     = ""
}

# R2
variable "r2_bucket_name" {
  description = "R2 bucket name (empty to skip)"
  type        = string
  default     = ""
}

variable "r2_location" {
  description = "R2 bucket location"
  type        = string
  default     = "WEUR"
}

# Routing
variable "route_pattern" {
  description = "Worker route pattern, e.g. api.example.com/*"
  type        = string
  default     = ""
}

variable "dns_name" {
  description = "DNS subdomain name (empty to skip)"
  type        = string
  default     = ""
}
