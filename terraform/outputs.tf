output "raw_data_bucket" {
  value       = aws_s3_bucket.raw_data.id
  description = "S3 bucket name for raw data layer"
}

output "clean_data_bucket" {
  value       = aws_s3_bucket.clean_data.id
  description = "S3 bucket name for clean data layer"
}

output "analytics_data_bucket" {
  value       = aws_s3_bucket.analytics_data.id
  description = "S3 bucket name for analytics data layer"
}

output "pipeline_history_table" {
  value       = aws_dynamodb_table.pipeline_history.name
  description = "DynamoDB table name for pipeline execution history"
}

output "data_quality_metrics_table" {
  value       = aws_dynamodb_table.data_quality_metrics.name
  description = "DynamoDB table name for data quality metrics"
}

output "pipeline_execution_role_arn" {
  value       = aws_iam_role.pipeline_execution_role.arn
  description = "ARN of the pipeline execution IAM role"
}

output "pipeline_notifications_topic_arn" {
  value       = aws_sns_topic.pipeline_notifications.arn
  description = "ARN of SNS topic for pipeline notifications"
}

output "data_quality_alerts_topic_arn" {
  value       = aws_sns_topic.data_quality_alerts.arn
  description = "ARN of SNS topic for data quality alerts"
}

output "pipeline_logs_group" {
  value       = aws_cloudwatch_log_group.pipeline_logs.name
  description = "CloudWatch log group name for pipeline execution"
}

output "aws_region" {
  value       = var.aws_region
  description = "AWS region being used"
}

output "environment" {
  value       = var.environment
  description = "Environment name"
}

output "localstack_endpoint" {
  value       = var.use_localstack ? "http://localhost:4566" : "AWS API"
  description = "Endpoint being used (LocalStack or real AWS)"
}
