# Terraform Infrastructure for eBay Scanner

This directory contains Terraform configurations to set up AWS infrastructure for the eBay Scanner application.

## Overview

The Terraform configuration creates:

- **ECR Repositories**: For storing Docker images
  - `ebay-scanner-web`: Web application container
  - `ebay-scanner-worker`: Background worker container
- **IAM Resources**: For GitHub Actions authentication
  - IAM user with ECR push permissions
  - OIDC provider for secure authentication (recommended)
  - IAM roles and policies
- **Lifecycle Policies**: Automatic cleanup of old Docker images

## Quick Start

### Prerequisites

1. AWS CLI installed and configured
2. Terraform >= 1.0 installed
3. Appropriate AWS permissions to create ECR repositories and IAM resources
4. **AWS Free Tier account** (recommended for cost optimization)

### Free Tier Optimization

This configuration is optimized for AWS Free Tier usage:
- **ECR Storage**: Uses only ~450MB of 500MB free storage
- **Image Scanning**: Disabled by default (100 scans/month limit)
- **Lifecycle Policies**: Aggressive cleanup to minimize storage costs
- **Regional Resources**: All in us-east-1 to avoid data transfer charges

See `FREE_TIER_OPTIMIZATION.md` for detailed cost management strategies.

### Setup Steps

1. **Copy example variables:**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Edit terraform.tfvars:**
   ```hcl
   aws_region   = "us-east-1"
   environment  = "dev"
   project_name = "ebay-scanner"
   github_org   = "your-github-username"
   github_repo  = "eBayScanner"
   ```

3. **Initialize Terraform:**
   ```bash
   terraform init
   ```

4. **Plan the deployment:**
   ```bash
   terraform plan
   ```

5. **Apply the configuration:**
   ```bash
   terraform apply
   ```

6. **Get outputs for GitHub Actions:**
   ```bash
   terraform output github_secrets_summary
   ```

### GitHub Actions Setup

After running Terraform, you'll need to add these secrets to your GitHub repository:

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following secrets:

```bash
# Get these values from Terraform outputs
AWS_ACCESS_KEY_ID=$(terraform output -raw github_actions_access_key_id)
AWS_SECRET_ACCESS_KEY=$(terraform output -raw github_actions_secret_access_key)
AWS_ACCOUNT_ID=$(terraform output -raw aws_account_id)
AWS_REGION=$(terraform output -raw aws_region)
```

### Security Recommendations

**Option 1: OIDC (Recommended)**
Use the OIDC role instead of access keys for better security:
```bash
# Use this role ARN in GitHub Actions
terraform output github_actions_oidc_role_arn
```

**Option 2: Access Keys**
If using access keys, rotate them regularly and store them securely.

## Terraform State Management

For production use, consider using remote state management:

1. Create an S3 bucket for state storage
2. Create a DynamoDB table for state locking
3. Uncomment and configure the backend in `main.tf`

Example backend configuration:
```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "ebay-scanner/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

## Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `aws_region` | AWS region for resources | `us-east-1` |
| `environment` | Environment name | `dev` |
| `project_name` | Project name prefix | `ebay-scanner` |
| `github_org` | GitHub organization/username | `neighborlyjim` |
| `github_repo` | GitHub repository name | `eBayScanner` |
| `ecr_image_retention_count` | Number of images to retain | `10` |
| `enable_image_scanning` | Enable ECR image scanning | `true` |

## Outputs

| Output | Description |
|--------|-------------|
| `ecr_repository_web_url` | Web application ECR repository URL |
| `ecr_repository_worker_url` | Worker application ECR repository URL |
| `github_actions_access_key_id` | GitHub Actions access key ID |
| `github_actions_secret_access_key` | GitHub Actions secret access key (sensitive) |
| `github_actions_oidc_role_arn` | OIDC role ARN (recommended for security) |

## Manual Docker Commands

To manually build and push images:

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $(terraform output -raw aws_account_id).dkr.ecr.us-east-1.amazonaws.com

# Build and tag images
docker build -t ebay-scanner-web .
docker build -f Dockerfile.worker -t ebay-scanner-worker .

# Tag for ECR
docker tag ebay-scanner-web:latest $(terraform output -raw ecr_repository_web_url):latest
docker tag ebay-scanner-worker:latest $(terraform output -raw ecr_repository_worker_url):latest

# Push to ECR
docker push $(terraform output -raw ecr_repository_web_url):latest
docker push $(terraform output -raw ecr_repository_worker_url):latest
```

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

**Warning**: This will delete all ECR repositories and their contents!

## Troubleshooting

### Common Issues

1. **Insufficient permissions**: Ensure your AWS credentials have permissions to create ECR repositories and IAM resources
2. **Repository already exists**: If repositories exist from previous setups, Terraform will import them
3. **GitHub Actions failing**: Verify all secrets are correctly set in GitHub repository settings

### Getting Help

- Check Terraform plan output before applying
- Review AWS CloudTrail logs for permission issues
- Verify ECR repository access in AWS Console
