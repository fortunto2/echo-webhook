# =============================================================================
# Outputs
# =============================================================================

output "echo_webhook_url" {
  description = "Echo webhook worker URL"
  value       = module.echo_webhook.worker_url
}

# output "another_worker_url" {
#   value = module.another_worker.worker_url
# }
