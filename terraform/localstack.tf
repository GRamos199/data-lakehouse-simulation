# LocalStack Docker Container Configuration
# Provides local AWS service emulation for development/testing
# (required_providers and docker provider are configured in main.tf)

# ============================================================================
# LOCALSTACK HEALTH CHECK (Wait for services to be ready)
# ============================================================================

resource "null_resource" "localstack_health_check" {
  # Only run health check when using LocalStack
  count = var.use_localstack ? 1 : 0

  provisioner "local-exec" {
    command = "bash -c '${file("${path.module}/scripts/wait-localstack.sh")}'"
  }

  depends_on = [docker_container.localstack[0]]
}

# ============================================================================
# LOCALSTACK CONTAINER (Local AWS Emulation)
# ============================================================================

resource "docker_image" "localstack" {
  # Only pull image when using LocalStack
  count = var.use_localstack ? 1 : 0

  name         = "localstack/localstack:latest"
  keep_locally = false
}

resource "docker_container" "localstack" {
  # Only create container when using LocalStack
  count = var.use_localstack ? 1 : 0

  name  = "data-lakehouse-localstack"
  image = docker_image.localstack[0].image_id

  # LocalStack services to enable
  env = [
    "SERVICES=s3,dynamodb,sns,sqs,cloudwatch,logs,events,lambda,iam",
    "DEBUG=1",
    "DATA_DIR=/tmp/localstack/data",
    "DOCKER_HOST=unix:///var/run/docker.sock",
    "EAGER_SERVICE_LOADING=true",
    "HOSTNAME=localhost",
    "LOCALSTACK_API_FORWARDING=true"
  ]

  # Port mappings - explicit IPv4
  ports {
    internal = 4566
    external = 4566
    ip       = "127.0.0.1"
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

  # Health check - longer startup period and more retries
  healthcheck {
    test         = ["CMD", "curl", "-f", "http://127.0.0.1:4566/_localstack/health"]
    interval     = "2s"
    timeout      = "3s"
    retries      = 30
    start_period = "45s"
  }

  # Capability to access Docker daemon
  capabilities {
    add = ["NET_ADMIN"]
  }

  # Ensure container always runs
  must_run = true
}
