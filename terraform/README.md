# Terraform Configuration Guide

## Overview
This Terraform configuration sets up the AWS infrastructure for the Data Lakehouse Simulation project. It can work with:
- **LocalStack** (local AWS emulation for development) - DEFAULT
- **Real AWS** (for production deployment)

## Quick Start

### 1. Prerequisites
```bash
# Install Terraform
brew install terraform  # macOS
# or apt-get install terraform  # Linux

# Install AWS CLI (optional, for debugging)
pip install awscli-local  # For LocalStack
```

### 2. Start LocalStack (Local AWS)
```bash
# Option A: Using Docker Compose
docker-compose -f docker-compose.yml up -d

# Option B: Using Terraform
cd terraform
terraform apply -target=docker_container.localstack
```

### 3. Initialize and Deploy Terraform
```bash
cd terraform
terraform init

# Plan changes (review what will be created)
terraform plan

# Apply changes (create AWS resources in LocalStack)
terraform apply
```

### 4. Verify Resources
```bash
# List created S3 buckets
aws s3 ls --endpoint-url http://localhost:4566

# List DynamoDB tables
aws dynamodb list-tables --endpoint-url http://localhost:4566 --region us-east-1

# Check CloudWatch logs
aws logs describe-log-groups --endpoint-url http://localhost:4566 --region us-east-1
```

## File Structure

```
terraform/
├── main.tf              # Core AWS resources (S3, DynamoDB, SNS, CloudWatch)
├── localstack.tf        # LocalStack Docker container (local AWS)
├── backend.tf           # Terraform state backend
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── terraform.tfstate    # Terraform state file (gitignored)
└── README.md           # This file
```

## Resources Created

### Data Storage (S3)
- **raw-data-bucket**: Raw data layer (JSON from APIs, CSV files)
- **clean-data-bucket**: Transformed clean data
- **analytics-data-bucket**: Final analytics tables and reports
- **Versioning enabled** on all buckets for data recovery

### Metadata Storage (DynamoDB)
- **pipeline-history**: Tracks all pipeline executions
- **data-quality-metrics**: Stores data quality check results

### Orchestration & Notifications
- **CloudWatch Log Groups**: Centralized logging
- **SNS Topics**: Notifications for success/failure
- **EventBridge Rules**: Scheduled pipeline triggers

### Security (IAM)
- **pipeline-execution-role**: Role for Lambda/Glue services
- **S3 Access**: Read/write to data buckets
- **DynamoDB Access**: Query and store metadata
- **CloudWatch Access**: Write logs and metrics

## Variables

### use_localstack (default: true)
- **true**: Use LocalStack (http://localhost:4566) - Development
- **false**: Use real AWS - Production

### aws_region (default: us-east-1)
- AWS region for resource deployment

### environment (default: local)
- Environment name (local, dev, staging, prod)

### project_name (default: data-lakehouse)
- Project name for resource naming

## Usage Examples

### Deploy to LocalStack (Development)
```bash
terraform apply -var="use_localstack=true" -var="environment=local"
```

### Deploy to Real AWS (Production)
```bash
terraform apply -var="use_localstack=false" -var="environment=prod"
```

### Destroy All Resources
```bash
terraform destroy
```

## Integration with Pipeline

The created AWS resources integrate with your Python pipeline:

1. **S3 Buckets**: Replace local `data/` directories
2. **DynamoDB**: Store execution history and data quality metrics
3. **CloudWatch**: Centralized logging
4. **SNS**: Notifications on pipeline completion

### Update Python Code for AWS Integration
```python
# Example: Upload to S3 instead of local filesystem
import boto3
s3 = boto3.client('s3', endpoint_url='http://localhost:4566')
s3.put_object(Bucket='data-lakehouse-clean', Key='data.csv', Body=data)
```

## Troubleshooting

### LocalStack not starting
```bash
# Check if port 4566 is already in use
lsof -i :4566

# View LocalStack logs
docker logs data-lakehouse-localstack
```

### Terraform state conflicts
```bash
# Clean up local state (be careful!)
rm terraform.tfstate*

# Re-initialize
terraform init
```

### Cannot connect to AWS
```bash
# Verify LocalStack is running
curl http://localhost:4566/_localstack/health

# Check AWS CLI endpoint
aws s3 ls --endpoint-url http://localhost:4566 --region us-east-1
```

## Best Practices

1. **Always review before apply**: Run `terraform plan` first
2. **Use workspaces for environments**: `terraform workspace new prod`
3. **Version your Terraform**: Keep `.terraform.versions` updated
4. **Document changes**: Add comments to modified files
5. **Backup state**: Store `terraform.tfstate` safely (use S3 backend in production)

## Next Steps

1. ✅ Configure AWS backend: Use S3 + DynamoDB for state locking in production
2. ✅ Add monitoring: CloudWatch dashboards and alarms
3. ✅ Implement data quality checks: Automated validation rules
4. ✅ Set up CI/CD: GitHub Actions for Terraform deployment
5. ✅ Create Lambda functions: Replace Airflow tasks with serverless functions

## Cost Optimization (LocalStack)
- LocalStack is **FREE** - no AWS charges
- Great for development and testing
- Move to real AWS only when needed
- Use reserved instances for production cost savings
