# Output values for multi-app, multi-VPC eBay Scanner infrastructure using modules
# These outputs support multiple applications in multiple VPCs

# Core infrastructure information
output "aws_account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

# Application and environment information
output "app_name" {
  description = "Application name used in resource naming"
  value       = var.app_name
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

# Resource naming information
output "resource_name_prefix" {
  description = "Resource name prefix used"
  value       = local.name_prefix
}

output "resource_name_suffix" {
  description = "Resource name suffix used"
  value       = local.name_suffix
}

# VPC outputs from module
output "vpc_id" {
  description = "ID of the VPC"
  value       = var.use_default_vpc ? data.aws_vpc.default[0].id : module.vpc.vpc_id
}

output "vpc_name" {
  description = "Name of the VPC"
  value       = var.vpc_name
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = var.use_default_vpc ? data.aws_vpc.default[0].cidr_block : module.vpc.vpc_cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = var.use_default_vpc ? data.aws_subnets.default[0].ids : module.vpc.public_subnets
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = var.use_default_vpc ? [] : module.vpc.private_subnets
}

output "availability_zones" {
  description = "Availability zones used"
  value       = var.availability_zones
}

# ECR repository outputs
output "ecr_repository_web_url" {
  description = "URL of the web application ECR repository"
  value       = aws_ecr_repository.web.repository_url
}

output "ecr_repository_worker_url" {
  description = "URL of the worker application ECR repository"
  value       = aws_ecr_repository.worker.repository_url
}

output "ecr_repository_web_name" {
  description = "Name of the web application ECR repository"
  value       = aws_ecr_repository.web.name
}

output "ecr_repository_worker_name" {
  description = "Name of the worker application ECR repository"
  value       = aws_ecr_repository.worker.name
}

output "ecr_registry_url" {
  description = "ECR registry URL"
  value       = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}

# ECS cluster outputs
output "ecs_cluster_id" {
  description = "ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_cluster_arn" {
  description = "ARN of the ECS cluster"
  value       = aws_ecs_cluster.main.arn
}

# ECS service outputs from modules
output "ecs_service_web_name" {
  description = "Name of the ECS web service"
  value       = module.ecs_cluster.service_name
}

output "ecs_service_worker_name" {
  description = "Name of the ECS worker service"
  value       = var.instance_count_worker > 0 ? module.ecs_worker[0].service_name : null
}

output "ecs_task_definition_web_arn" {
  description = "ARN of the web task definition"
  value       = module.ecs_cluster.task_definition_arn
}

output "ecs_task_definition_worker_arn" {
  description = "ARN of the worker task definition"
  value       = var.instance_count_worker > 0 ? module.ecs_worker[0].task_definition_arn : null
}

# IAM role outputs from modules
output "ecs_task_execution_role_arn" {
  description = "ARN of the ECS task execution role"
  value       = module.ecs_cluster.execution_role_arn
}

output "ecs_task_role_arn" {
  description = "ARN of the ECS task role"
  value       = module.ecs_cluster.task_role_arn
}

# CloudWatch outputs
output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.ecs_logs.name
}

output "cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.ecs_logs.arn
}

# SSM Parameter outputs (names only for security)
output "ssm_db_password_name" {
  description = "Name of the DB password SSM parameter"
  value       = aws_ssm_parameter.db_password.name
}

output "ssm_ebay_client_id_name" {
  description = "Name of the eBay Client ID SSM parameter"
  value       = aws_ssm_parameter.ebay_client_id.name
}

output "ssm_ebay_client_secret_name" {
  description = "Name of the eBay Client Secret SSM parameter"
  value       = aws_ssm_parameter.ebay_client_secret.name
}

output "ssm_ebay_app_id_name" {
  description = "Name of the eBay App ID SSM parameter"
  value       = aws_ssm_parameter.ebay_app_id.name
}

output "ssm_ebay_dev_id_name" {
  description = "Name of the eBay Dev ID SSM parameter"
  value       = aws_ssm_parameter.ebay_dev_id.name
}

# Useful commands
output "ecr_login_command" {
  description = "Command to login to ECR"
  value       = "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}

# Deployment summary for multi-app environments
output "deployment_summary" {
  description = "Summary of this deployment for multi-app tracking"
  value = {
    app_name              = var.app_name
    environment           = var.environment
    vpc_type              = var.use_default_vpc ? "default" : "custom"
    vpc_name              = var.vpc_name
    cluster_name          = local.cluster_name
    web_repository_url    = aws_ecr_repository.web.repository_url
    worker_repository_url = aws_ecr_repository.worker.repository_url
    region                = var.aws_region
    resource_prefix       = local.name_prefix
    resource_suffix       = local.name_suffix
    using_modules         = true
  }
}

# Multi-app deployment guidance
output "multi_app_deployment_examples" {
  description = "Examples for deploying additional apps using modules"
  value = {
    same_vpc_different_app = {
      command     = "terraform apply -var='app_name=my-other-app' -var='resource_name_suffix=v2'"
      description = "Deploy another app in the same VPC with different naming"
    }
    different_vpc_same_app = {
      command     = "terraform apply -var='vpc_name=production-vpc' -var='environment=prod' -var='use_default_vpc=false'"
      description = "Deploy the same app in a custom VPC for production"
    }
    staging_environment = {
      command     = "terraform apply -var='environment=staging' -var='resource_name_suffix=staging' -var='instance_count_web=1'"
      description = "Deploy a staging version with reduced capacity"
    }
  }
}

# Module information
output "modules_used" {
  description = "Information about Terraform modules used"
  value = {
    vpc_module = {
      source  = "terraform-aws-modules/vpc/aws"
      version = "~> 6.0"
      purpose = "VPC and networking infrastructure"
    }
    ecs_module = {
      source  = "umotif-public/ecs-fargate/aws"
      version = "~> 8.2"
      purpose = "ECS Fargate services"
    }
  }
}
