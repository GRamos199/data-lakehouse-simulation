# LocalStack Docker Container Configuration
# Provides local AWS service emulation for development/testing
# (required_providers and docker provider are configured in main.tf)

# ============================================================================
# LOCALSTACK CONTAINER (Local AWS Emulation)
# ============================================================================

resource "docker_image" "localstack" {
  name          = "localstack/localstack:latest"
  keep_locally  = false
}

resource "docker_container" "localstack" {
  name  = "data-lakehouse-localstack"
  image = docker_image.localstack.image_id

  # LocalStack services to enable
  env = [
    "SERVICES=s3,dynamodb,sns,sqs,cloudwatch,logs,events,lambda,iam",
    "DEBUG=1",
    "DATA_DIR=/tmp/localstack/data",
    "DOCKER_HOST=unix:///var/run/docker.sock"
  ]

  # Port mappings
  ports {
    internal = 4566
    external = 4566
  }

  # Volumes for persistence
  volumes {
    host_path      = "/var/run/docker.sock"
    container_path = "/var/run/docker.sock"
  }

  volumes {
    host_path      = "/tmp/localstack"
    container_path = "/tmp/localstack/data"
  }

  # Health check
  healthcheck {
    test     = ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
    interval = "5s"
    timeout  = "2s"
    retries  = 5
  }

  # Capability to access Docker daemon
  capabilities {
    add = ["NET_ADMIN"]
  }
}
