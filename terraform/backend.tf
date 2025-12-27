# Backend configuration for Terraform state management
# Uses local file backend for local development

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}
