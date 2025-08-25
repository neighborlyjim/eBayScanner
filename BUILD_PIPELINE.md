# eBay Scanner - AWS Build Pipeline Documentation

## Overview

This document describes the complete CI/CD pipeline for the eBay Scanner application that builds Docker images and pushes them to AWS ECR (Elastic Container Registry).

## Architecture

### Components
- **Web Application**: Flask-based eBay search interface
- **Worker Application**: Background processing for scheduled tasks
- **Database**: PostgreSQL for data persistence
- **Infrastructure**: AWS ECR for container images, Terraform for infrastructure management

### AWS Free Tier Optimization
- **ECR Storage**: Optimized to use <500MB (free tier limit)
- **Image Retention**: Keep only 3 most recent images
- **Image Scanning**: Disabled by default (100 scans/month limit)
- **Lifecycle Policies**: Aggressive cleanup after 1 hour for untagged images
- **Monthly Cost**: $0 within free tier, ~$0.45/month after

### Build Pipeline
- **Source Control**: GitHub repository with feature branches
- **CI/CD**: GitHub Actions with automated builds and deployments
- **Infrastructure**: Terraform-managed AWS resources
- **Container Registry**: AWS ECR with automatic image lifecycle management

## Infrastructure Setup

### Prerequisites
1. AWS CLI installed and configured
2. Terraform >= 1.0
3. Docker Desktop
4. GitHub repository with appropriate permissions

### Terraform Configuration

The infrastructure is defined in the `terraform/` directory with the following resources:

#### ECR Repositories
- `ebay-scanner-web`: For web application images
- `ebay-scanner-worker`: For worker application images
- Automatic image scanning enabled
- Lifecycle policies to retain only 10 most recent images

#### IAM Resources
- **GitHub Actions User**: For CI/CD pipeline access
- **OIDC Provider**: For secure authentication (recommended)
- **Policies**: Granular permissions for ECR push/pull operations

#### Setup Commands
```bash
# Navigate to terraform directory
cd terraform

# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit terraform.tfvars with your values
# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply configuration
terraform apply

# Get outputs for GitHub Actions
terraform output github_secrets_summary
```

## GitHub Actions Pipeline

### Workflow File: `.github/workflows/build-and-deploy.yml`

#### Jobs Overview
1. **terraform-plan**: Validates Terraform on pull requests
2. **terraform-apply**: Applies infrastructure changes on main branch
3. **test**: Runs application tests
4. **build-and-push**: Builds and pushes Docker images to ECR
5. **deploy-staging**: Deploys to staging environment (develop branch)
6. **deploy-production**: Deploys to production environment (main branch)

#### Triggers
- **Push to main**: Full pipeline with production deployment
- **Push to develop**: Build and staging deployment
- **Pull Request to main**: Plan and test only
- **Manual trigger**: Via workflow_dispatch

### Required GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```bash
AWS_ACCESS_KEY_ID       # From terraform output
AWS_SECRET_ACCESS_KEY   # From terraform output  
AWS_ACCOUNT_ID          # From terraform output
AWS_REGION              # us-east-1 (or your chosen region)
```

## Docker Configuration

### Multi-Stage Builds
- **Base Image**: `python:3.13-slim`
- **System Dependencies**: gcc, postgresql-client, libpq-dev, python3-dev
- **Python Dependencies**: psycopg[binary]==3.2.3 (Python 3.13 compatible)
- **Security**: Non-root user execution
- **Health Checks**: Built-in container health monitoring

### Dockerfile Optimization
- Dependency caching for faster builds
- Multi-platform support (linux/amd64)
- Security scanning with Trivy
- Minimal layer count for smaller images

## Security Features

### Container Security
- **Non-root execution**: Applications run as dedicated users
- **Image scanning**: Automated vulnerability detection
- **Secret management**: Environment variables for sensitive data
- **Health checks**: Container health monitoring

### AWS Security
- **IAM best practices**: Minimal required permissions
- **OIDC authentication**: Recommended over long-lived access keys
- **Encryption**: ECR repositories encrypted at rest
- **VPC isolation**: Future ECS deployment in private subnets

### Build Security
- **Dependency scanning**: Automated security vulnerability checks
- **SARIF integration**: Security findings in GitHub Security tab
- **Branch protection**: Required status checks before merge
- **Secrets scanning**: Prevent credential exposure

## Deployment Process

### Automated Deployment Flow
1. **Code Push**: Developer pushes to main/develop branch
2. **Infrastructure**: Terraform applies any infrastructure changes
3. **Build**: Docker images built with latest code
4. **Test**: Security scanning and vulnerability assessment
5. **Push**: Images tagged and pushed to ECR
6. **Deploy**: ECS services updated with new images (placeholder)

### Manual Deployment Commands
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $(terraform output -raw aws_account_id).dkr.ecr.us-east-1.amazonaws.com

# Build images
docker build -t ebay-scanner-web .
docker build -f Dockerfile.worker -t ebay-scanner-worker .

# Tag for ECR
docker tag ebay-scanner-web:latest \
  $(terraform output -raw ecr_repository_web_url):latest
docker tag ebay-scanner-worker:latest \
  $(terraform output -raw ecr_repository_worker_url):latest

# Push to ECR
docker push $(terraform output -raw ecr_repository_web_url):latest
docker push $(terraform output -raw ecr_repository_worker_url):latest
```

## Monitoring and Maintenance

### Image Lifecycle
- **Retention**: Keep 10 most recent tagged images
- **Cleanup**: Automatic deletion of untagged images after 1 day
- **Storage costs**: Optimized through lifecycle policies

### Build Monitoring
- **GitHub Actions**: Build status and logs in repository
- **AWS CloudTrail**: Infrastructure change auditing
- **ECR Events**: Image push/pull monitoring

### Maintenance Tasks
- **Weekly**: Review build logs and security scan results
- **Monthly**: Update base image versions and dependencies
- **Quarterly**: Review and rotate access credentials

## Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check Terraform formatting
terraform fmt -check

# Validate Terraform configuration
terraform validate

# Test Docker builds locally
docker build -t test-web .
docker build -f Dockerfile.worker -t test-worker .
```

#### Permission Issues
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check ECR permissions
aws ecr describe-repositories

# Test ECR login
aws ecr get-login-password --region us-east-1
```

#### GitHub Actions Issues
- Check repository secrets are correctly set
- Verify branch protection rules allow CI/CD
- Review action logs for specific error messages

### Getting Help
1. Check GitHub Actions logs for detailed error messages
2. Review AWS CloudTrail for infrastructure issues
3. Validate Terraform configuration with `terraform plan`
4. Test Docker builds locally before pushing

## Performance Optimization

### Build Speed
- **Docker layer caching**: GitHub Actions cache for faster builds
- **Dependency caching**: pip and apt package caching
- **Parallel builds**: Multiple job execution where possible

### Cost Optimization
- **ECR lifecycle policies**: Automatic cleanup of old images
- **Multi-stage builds**: Smaller final image sizes
- **Regional optimization**: Resources in single AWS region

## Future Enhancements

### Planned Improvements
1. **ECS Integration**: Complete container orchestration setup
2. **Blue-Green Deployments**: Zero-downtime deployment strategy
3. **Environment Promotion**: Automated staging → production promotion
4. **Monitoring Dashboard**: Application performance monitoring
5. **Backup Strategy**: Database and configuration backup automation

### Security Enhancements
1. **OIDC Migration**: Complete transition from access keys
2. **Network Segmentation**: VPC and security group configuration
3. **Secrets Management**: AWS Secrets Manager integration
4. **Compliance Scanning**: Additional security policy enforcement

This build pipeline provides a robust, secure, and scalable foundation for the eBay Scanner application deployment to AWS infrastructure.
