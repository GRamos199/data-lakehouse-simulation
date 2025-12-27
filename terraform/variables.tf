variable "use_localstack" {
  description = "Use LocalStack for local AWS simulation"
  type        = bool
  default     = true
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "docker_host" {
  description = "Docker daemon host (unix socket for local development)"
  type        = string
  default     = "unix:///var/run/docker.sock"
}

variable "environment" {
  description = "Environment name (local, dev, staging, prod)"
  type        = string
  default     = "local"

  validation {
    condition     = contains(["local", "dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: local, dev, staging, prod."
  }
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "data-lakehouse"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*$", var.project_name))
    error_message = "Project name must start with lowercase letter and contain only lowercase letters, numbers, and hyphens."
  }
}
