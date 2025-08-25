# 🚀 Multi-Environment Deployment Guide

This guide shows you how to deploy the eBay Scanner to dev and prod environments using Terraform with environment-specific configurations.

## 📁 Environment Files

| File | Purpose | Usage |
|------|---------|-------|
| `dev.tfvars` | Development environment config | Cost-optimized, single instances, default VPC |
| `prod.tfvars` | Production environment config | High availability, custom VPC, load balancer |
| `deploy.ps1` | Deployment script | Handles environment variables and deployment |
| `set-env.ps1` | Environment setup | Interactive script to set required variables |

## 🔧 Quick Start

### 1. **Set Environment Variables**
```powershell
# Interactive setup (recommended)
.\set-env.ps1 -Environment dev

# Or set manually
$Env:TF_VAR_ebay_client_id = "your-ebay-client-id"
$Env:TF_VAR_ebay_client_secret = "your-ebay-client-secret"
$Env:TF_VAR_ebay_app_id = "your-ebay-app-id"
$Env:TF_VAR_ebay_dev_id = "your-ebay-dev-id"
$Env:TF_VAR_db_password = "your-database-password"
```

### 2. **Deploy to Development**
```powershell
.\deploy.ps1 -Environment dev
```

### 3. **Deploy to Production**
```powershell
.\deploy.ps1 -Environment prod
```

## 🏗️ Environment Differences

### **Development Environment** (`dev.tfvars`)
- **Cost**: Free tier optimized (~$0/month)
- **VPC**: Uses AWS default VPC (no NAT Gateway costs)
- **Scale**: 1 web + 1 worker instance
- **Resources**: 256 CPU / 512 MB RAM per service
- **Load Balancer**: Disabled (direct container access)
- **Logs**: 7-day retention
- **Database**: `ebay_scanner_dev` database

### **Production Environment** (`prod.tfvars`)
- **Cost**: Production scale (~$50-100/month)
- **VPC**: Custom VPC with public/private subnets
- **Scale**: 2 web + 2 worker instances (high availability)
- **Resources**: 512 CPU / 1024 MB RAM per service
- **Load Balancer**: Enabled with SSL termination
- **Logs**: 30-day retention
- **Database**: `ebay_scanner_prod` database

## 📋 Environment Variables Reference

### **Required Variables** (set via `TF_VAR_` prefix)
| Variable | Description | Example |
|----------|-------------|---------|
| `ebay_client_id` | eBay API Client ID | `your-client-id` |
| `ebay_client_secret` | eBay API Client Secret | `your-client-secret` |
| `ebay_app_id` | eBay Application ID | `your-app-id` |
| `ebay_dev_id` | eBay Developer ID | `your-dev-id` |
| `db_password` | Database password | `secure-password` |

### **Optional AWS Variables**
| Variable | Description | Note |
|----------|-------------|------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key | Use if not using AWS CLI |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key | Use if not using AWS CLI |
| `AWS_SESSION_TOKEN` | AWS Session Token | For temporary credentials |

## 🎯 Deployment Commands

### **Manual Terraform Commands**
```powershell
# Development
terraform plan -var-file="dev.tfvars"
terraform apply -var-file="dev.tfvars"

# Production  
terraform plan -var-file="prod.tfvars"
terraform apply -var-file="prod.tfvars"

# Destroy environment
terraform destroy -var-file="dev.tfvars"
```

### **Using Deployment Script** (Recommended)
```powershell
# Set environment variables interactively
.\set-env.ps1 -Environment dev

# Deploy with validation and confirmation
.\deploy.ps1 -Environment dev
```

## 🔄 Environment Separation Strategies

### **Option 1: Separate .tfvars Files** (Current)
```
terraform/
├── dev.tfvars     # Development config
├── prod.tfvars    # Production config
├── deploy.ps1     # Deployment script
└── *.tf          # Shared Terraform code
```

### **Option 2: Terraform Workspaces** (Alternative)
```powershell
# Create workspaces
terraform workspace new dev
terraform workspace new prod

# Switch environments
terraform workspace select dev
terraform apply -var-file="dev.tfvars"

terraform workspace select prod  
terraform apply -var-file="prod.tfvars"
```

### **Option 3: Separate State Files** (Advanced)
```powershell
# Different state files per environment
terraform apply -var-file="dev.tfvars" -state="dev.tfstate"
terraform apply -var-file="prod.tfvars" -state="prod.tfstate"
```

## 🔒 Security Best Practices

### **Environment Variables**
- ✅ Use `TF_VAR_` prefix for Terraform variables
- ✅ Never commit actual secrets to git
- ✅ Use placeholder values in `.tfvars` files
- ✅ Set real values via environment variables

### **AWS Credentials**
```powershell
# Option 1: AWS CLI (recommended)
aws configure

# Option 2: Environment variables
$Env:AWS_ACCESS_KEY_ID = "your-access-key"
$Env:AWS_SECRET_ACCESS_KEY = "your-secret-key"

# Option 3: IAM roles (for EC2/containers)
# No manual credentials needed
```

### **State File Security**
```hcl
# Enable remote state for production
terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "ebay-scanner/terraform.tfstate"
    region = "us-east-1"
    
    # Enable state locking and encryption
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

## 📊 Resource Comparison

| Resource | Dev Environment | Prod Environment |
|----------|----------------|------------------|
| **VPC** | Default VPC | Custom VPC (10.0.0.0/16) |
| **Subnets** | Default public | Public + Private subnets |
| **ECS Tasks** | 2 (1 web + 1 worker) | 4 (2 web + 2 worker) |
| **CPU/Memory** | 256/512 per task | 512/1024 per task |
| **Load Balancer** | None | Application LB |
| **NAT Gateway** | None | 1 per AZ |
| **CloudWatch Logs** | 7 days | 30 days |
| **Estimated Cost** | ~$0/month | ~$50-100/month |

## 🚨 Troubleshooting

### **Common Issues**

#### Missing Environment Variables
```
❌ Missing required environment variables:
  - TF_VAR_ebay_client_id
```
**Solution**: Run `.\set-env.ps1 -Environment dev`

#### AWS Credentials Not Found
```
❌ Error: No valid credential sources found
```
**Solution**: Run `aws configure` or set AWS environment variables

#### Terraform State Lock
```
❌ Error: Error acquiring the state lock
```
**Solution**: 
```powershell
terraform force-unlock LOCK_ID
```

#### Resource Already Exists
```
❌ Error: resource already exists
```
**Solution**: Import existing resource or use different naming
```powershell
terraform import aws_ecr_repository.web ebay-scanner-web
```

## 🎉 Success Indicators

After successful deployment, you should see:

```
✅ Terraform configuration is valid
✅ Terraform plan completed successfully  
✅ Deployment to dev completed successfully! 🎉

Outputs:
ecr_repository_web_url = "058727362332.dkr.ecr.us-east-1.amazonaws.com/ebay-scanner-web"
ecs_cluster_name = "ebay-scanner-cluster"
deployment_summary = {
  app_name = "ebay-scanner"
  environment = "dev"
  using_modules = true
}
```

## 🚀 Next Steps

1. **Build and push Docker images** to ECR repositories
2. **Configure database** connection and run migrations
3. **Set up monitoring** with CloudWatch alarms
4. **Configure CI/CD** pipeline for automated deployments
5. **Test application** functionality in both environments
