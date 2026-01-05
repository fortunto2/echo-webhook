terraform {
  required_version = ">= 1.0"

  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }

  # Uncomment for remote state (recommended for team use)
  # backend "s3" {
  #   bucket = "your-terraform-state"
  #   key    = "cloudflare-workers/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

# =============================================================================
# Workers - add each worker as a module call
# =============================================================================

module "echo_webhook" {
  source = "./workers/echo-webhook"

  account_id = var.cloudflare_account_id

  # Optional: custom domain routing
  # zone_id = var.cloudflare_zone_id
  # route_pattern = "api.example.com/webhook/*"
}

# module "another_worker" {
#   source = "./workers/another-worker"
#   account_id = var.cloudflare_account_id
# }
