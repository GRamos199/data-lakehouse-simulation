# Data Lakehouse Simulation - Terraform Configuration
# Simulates AWS services using LocalStack (local AWS emulation)
# Run: terraform init && terraform plan && terraform apply

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # LocalStack configuration (local AWS emulation)
  access_key = var.use_localstack ? "test" : null
  secret_key = var.use_localstack ? "test" : null

  # Skip validation for LocalStack
  skip_credentials_validation = var.use_localstack
  skip_metadata_api_check     = var.use_localstack
  skip_requesting_account_id  = var.use_localstack

  dynamic "endpoints" {
    for_each = var.use_localstack ? [1] : []
    content {
      s3            = "http://127.0.0.1:4566"
      dynamodb      = "http://127.0.0.1:4566"
      sns           = "http://127.0.0.1:4566"
      sqs           = "http://127.0.0.1:4566"
      cloudwatch    = "http://127.0.0.1:4566"
      logs          = "http://127.0.0.1:4566"
      events        = "http://127.0.0.1:4566"
      iam           = "http://127.0.0.1:4566"
      lambda        = "http://127.0.0.1:4566"
      glue          = "http://127.0.0.1:4566"
      stepfunctions = "http://127.0.0.1:4566"
    }
  }
}

provider "docker" {
  host = var.docker_host
}

# ============================================================================
# LOCAL VARIABLES
# ============================================================================

locals {
  tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    CreatedAt   = timestamp()
  }
}

# ============================================================================
# 1. S3 BUCKETS (Data Lake Storage)
# ============================================================================

# Raw data layer bucket
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-raw-${var.environment}"

  # Ensure LocalStack is ready before creating resources
  depends_on = [null_resource.localstack_health_check]

  tags = merge(
    local.tags,
    {
      Name  = "${var.project_name}-raw"
      Layer = "raw"
    }
  )
}

# Clean data layer bucket
resource "aws_s3_bucket" "clean_data" {
  bucket = "${var.project_name}-clean-${var.environment}"

  depends_on = [null_resource.localstack_health_check]

  tags = merge(
    local.tags,
    {
      Name  = "${var.project_name}-clean"
      Layer = "clean"
    }
  )
}

# Analytics layer bucket
resource "aws_s3_bucket" "analytics_data" {
  bucket     = "${var.project_name}-analytics-${var.environment}"
  depends_on = [null_resource.localstack_health_check]
  tags = merge(
    local.tags,
    {
      Name  = "${var.project_name}-analytics"
      Layer = "analytics"
    }
  )
}

# Enable versioning on all buckets
resource "aws_s3_bucket_versioning" "raw_versioning" {
  bucket = aws_s3_bucket.raw_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "clean_versioning" {
  bucket = aws_s3_bucket.clean_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "analytics_versioning" {
  bucket = aws_s3_bucket.analytics_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# ============================================================================
# 2. DynamoDB TABLES (Metadata & Pipeline State)
# ============================================================================

# Pipeline execution history
resource "aws_dynamodb_table" "pipeline_history" {
  name         = "${var.project_name}-pipeline-history"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "execution_id"
  range_key    = "timestamp"

  depends_on = [null_resource.localstack_health_check]

  attribute {
    name = "execution_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-pipeline-history"
    }
  )
}

# Data quality metrics
resource "aws_dynamodb_table" "data_quality_metrics" {
  name         = "${var.project_name}-data-quality"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dataset_id"
  range_key    = "check_timestamp"

  depends_on = [null_resource.localstack_health_check]

  attribute {
    name = "dataset_id"
    type = "S"
  }

  attribute {
    name = "check_timestamp"
    type = "S"
  }

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-data-quality"
    }
  )
}

# ============================================================================
# 3. EVENTBRIDGE (Workflow Orchestration - replaces Airflow in cloud)
# ============================================================================

# EventBridge rule for daily pipeline execution
resource "aws_cloudwatch_event_rule" "daily_pipeline" {
  name                = "${var.project_name}-daily-pipeline"
  description         = "Triggers data lakehouse pipeline daily at 2 AM UTC"
  schedule_expression = "cron(0 2 * * ? *)"

  depends_on = [null_resource.localstack_health_check]

  tags = local.tags
}

# ============================================================================
# 4. SNS TOPICS (Notifications)
# ============================================================================

resource "aws_sns_topic" "pipeline_notifications" {
  name = "${var.project_name}-pipeline-notifications"

  depends_on = [null_resource.localstack_health_check]

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-pipeline-notifications"
    }
  )
}

resource "aws_sns_topic" "data_quality_alerts" {
  name = "${var.project_name}-data-quality-alerts"

  depends_on = [null_resource.localstack_health_check]

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-data-quality-alerts"
    }
  )
}

# ============================================================================
# 5. CLOUDWATCH (Monitoring & Logging)
# ============================================================================

# Log group for pipeline execution logs
resource "aws_cloudwatch_log_group" "pipeline_logs" {
  name              = "/aws/${var.project_name}/pipeline"
  retention_in_days = 7

  depends_on = [null_resource.localstack_health_check]

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-pipeline-logs"
    }
  )
}

# Log group for data validation logs
resource "aws_cloudwatch_log_group" "data_validation_logs" {
  name              = "/aws/${var.project_name}/data-validation"
  retention_in_days = 7

  depends_on = [null_resource.localstack_health_check]

  tags = merge(
    local.tags,
    {
      Name = "${var.project_name}-data-validation-logs"
    }
  )
}

# ============================================================================
# 6. IAM ROLES & POLICIES (for Lambda, Glue, etc.)
# ============================================================================

resource "aws_iam_role" "pipeline_execution_role" {
  name = "${var.project_name}-pipeline-execution-role"

  depends_on = [null_resource.localstack_health_check]

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = [
            "lambda.amazonaws.com",
            "glue.amazonaws.com",
            "states.amazonaws.com"
          ]
        }
      }
    ]
  })

  tags = local.tags
}

resource "aws_iam_role_policy" "pipeline_s3_access" {
  name = "${var.project_name}-pipeline-s3-access"
  role = aws_iam_role.pipeline_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.raw_data.arn,
          "${aws_s3_bucket.raw_data.arn}/*",
          aws_s3_bucket.clean_data.arn,
          "${aws_s3_bucket.clean_data.arn}/*",
          aws_s3_bucket.analytics_data.arn,
          "${aws_s3_bucket.analytics_data.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "pipeline_dynamodb_access" {
  name = "${var.project_name}-pipeline-dynamodb-access"
  role = aws_iam_role.pipeline_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.pipeline_history.arn,
          aws_dynamodb_table.data_quality_metrics.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "pipeline_logs_access" {
  name = "${var.project_name}-pipeline-logs-access"
  role = aws_iam_role.pipeline_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = [
          "${aws_cloudwatch_log_group.pipeline_logs.arn}:*",
          "${aws_cloudwatch_log_group.data_validation_logs.arn}:*"
        ]
      }
    ]
  })
}

# ============================================================================
# DATA SOURCES
# ============================================================================

# Not needed with simplified bucket names, but keeping for future reference:
# data "aws_caller_identity" "current" {}


