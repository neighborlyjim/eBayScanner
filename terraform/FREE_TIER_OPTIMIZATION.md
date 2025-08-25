# AWS Free Tier Optimization for eBay Scanner

## Overview

This document outlines how the eBay Scanner build pipeline is optimized to stay within AWS Free Tier limits, minimizing costs while maintaining functionality.

## AWS Free Tier Limits (Relevant to Our Stack)

### Amazon ECR (Elastic Container Registry)
- **Storage**: 500 MB of storage per month
- **Image Scanning**: 100 vulnerability scans per month
- **Data Transfer**: 1 GB outbound data transfer per month

### Amazon IAM (Identity and Access Management)
- **Free**: Unlimited users, groups, roles, and policies

### Amazon CloudTrail
- **Free**: One trail with management events only

## Optimization Strategies

### 1. ECR Storage Optimization

**Image Retention Policy:**
- Keep only **3 most recent tagged images** (down from 10)
- Delete untagged images after **1 hour** (down from 1 day)
- Estimated storage per image: ~150MB
- Total estimated usage: ~450MB (within 500MB limit)

**Configuration:**
```hcl
variable "ecr_image_retention_count" {
  default = 3  # Reduced for free tier
}

# Aggressive cleanup policy
lifecycle_policy = {
  untagged_images_expiry = "1 hour"
}
```

### 2. Image Scanning Optimization

**Strategy:**
- **Disabled by default** to avoid exceeding 100 scans/month
- Can be enabled temporarily for security audits
- Alternative: Use GitHub Actions security scanning (free)

**Configuration:**
```hcl
variable "enable_image_scanning" {
  default = false  # Disabled for free tier
}
```

### 3. Build Frequency Management

**GitHub Actions Optimizations:**
- **Conditional builds**: Only build on main/develop branches
- **Build caching**: Docker layer caching to reduce build times
- **Parallel jobs**: Optimize pipeline efficiency

### 4. Data Transfer Optimization

**Strategies:**
- Use **same AWS region** for all resources (us-east-1)
- **Minimize cross-region transfers**
- **Aggressive image cleanup** to reduce storage costs

## Cost Monitoring

### Expected Monthly Costs

**Within Free Tier (Month 1-12):**
- ECR Storage: $0 (within 500MB limit)
- ECR Image Scanning: $0 (disabled)
- IAM: $0 (always free)
- Data Transfer: $0 (within 1GB limit)
- **Total: $0/month**

**After Free Tier (Month 13+):**
- ECR Storage: ~$0.45/month (450MB × $0.10/GB)
- ECR Scanning: $0 (disabled)
- IAM: $0 (always free)
- **Total: ~$0.45/month**

### Cost Monitoring Tools

1. **AWS Cost Explorer**: Monitor actual usage
2. **AWS Budgets**: Set alerts at $1/month threshold
3. **Terraform outputs**: Track resource usage

## Free Tier Extension Strategies

### 1. Multi-Account Strategy
- Use **separate AWS accounts** for different environments
- Each account gets **full free tier benefits**
- Example: dev-account, staging-account, prod-account

### 2. Image Optimization
```dockerfile
# Multi-stage builds to reduce image size
FROM python:3.13-slim AS builder
# ... build dependencies

FROM python:3.13-slim AS runtime
# ... only runtime files
```

### 3. Development Workflow
- **Local development** using docker-compose
- **Minimal cloud deployments** only for testing
- **Staging environment** in separate account

## Implementation Checklist

### ✅ ECR Optimization
- [x] Reduced image retention to 3 images
- [x] Aggressive untagged image cleanup (1 hour)
- [x] Disabled image scanning by default
- [x] Added cost tracking tags

### ✅ Build Pipeline Optimization
- [x] Conditional builds (main/develop only)
- [x] Docker layer caching
- [x] Parallel job execution
- [x] Build only on significant changes

### ✅ Monitoring Setup
- [ ] AWS Budget alert at $1/month
- [ ] CloudWatch cost monitoring
- [ ] Monthly cost review process

## Scaling Beyond Free Tier

### When to Consider Paid Resources

1. **Storage > 400MB**: Consider image optimization
2. **Frequent deployments**: Enable selective image scanning
3. **Production workloads**: Upgrade to production-grade monitoring

### Cost-Effective Scaling Options

1. **ECR**: Pay only for storage used (~$0.10/GB/month)
2. **ECS Fargate**: Pay only for running time
3. **RDS**: Consider Aurora Serverless for database
4. **CloudFront**: Use for static asset caching

## Alternative Free Resources

### Container Alternatives
- **GitHub Container Registry**: Free for public repositories
- **Docker Hub**: Free tier with rate limits
- **GitLab Container Registry**: Free with GitLab

### Deployment Alternatives
- **Heroku**: Free tier available (with limitations)
- **Railway**: Free tier for small applications
- **Render**: Free tier for web services

## Best Practices

### 1. Regular Cleanup
```bash
# Monthly cleanup script
aws ecr list-images --repository-name ebay-scanner-web --filter tagStatus=UNTAGGED
aws ecr batch-delete-image --repository-name ebay-scanner-web --image-ids imageDigest=<digest>
```

### 2. Cost Monitoring
```bash
# Check ECR repository sizes
aws ecr describe-repositories --repository-names ebay-scanner-web ebay-scanner-worker
```

### 3. Resource Tagging
```hcl
tags = {
  Environment = "dev"
  CostCenter  = "free-tier"
  Project     = "ebay-scanner"
}
```

## Emergency Cost Controls

### Automatic Shutoffs
- **Terraform destroy**: Quick resource cleanup
- **GitHub Actions limits**: Prevent runaway builds
- **Budget alerts**: Email notifications at thresholds

### Manual Cleanup
```bash
# Emergency cleanup - delete all images
terraform destroy -target=aws_ecr_repository.web
terraform destroy -target=aws_ecr_repository.worker
```

This optimization strategy ensures the eBay Scanner remains within AWS Free Tier limits while maintaining full CI/CD functionality.
