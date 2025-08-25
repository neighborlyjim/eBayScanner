# Terraform configuration for multi-app, multi-VPC eBay Scanner using modules
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # Uncomment and configure for remote state management
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "${var.project_name}/${var.app_name}/${var.environment}/terraform.tfstate"
  #   region = var.aws_region
  # }
}

# Provider configuration with comprehensive default tags
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = merge(
      {
        Project           = var.project_name
        Application       = var.app_name
        Environment       = var.environment
        ManagedBy         = "Terraform"
        VPCName          = var.vpc_name
        TerraformVersion = "~> 5.0"
        DeployedAt       = timestamp()
      },
      var.additional_tags
    )
  }
}

# Local values for consistent resource naming across all modules
locals {
  # Construct naming patterns for all resources
  name_prefix = var.resource_name_prefix != "" ? "${var.resource_name_prefix}-" : ""
  name_suffix = var.resource_name_suffix != "" ? "-${var.resource_name_suffix}" : ""
  
  # Standard naming patterns
  cluster_name = "${local.name_prefix}${var.app_name}-cluster${local.name_suffix}"
  vpc_name = var.use_default_vpc ? "default" : "${local.name_prefix}vpc${local.name_suffix}"
  
  # Common tags to be applied to all resources
  common_tags = merge(
    {
      Project           = var.project_name
      Application       = var.app_name
      Environment       = var.environment
      VPCName          = var.vpc_name
      ManagedBy         = "Terraform"
      ResourcePrefix    = local.name_prefix
      ResourceSuffix    = local.name_suffix
    },
    var.additional_tags
  )
}
