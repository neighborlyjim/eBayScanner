# Input variables for eBay Scanner infrastructure
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ebay-scanner"
}

variable "app_name" {
  description = "Application name (for multi-app VPC support)"
  type        = string
  default     = "ebay-scanner"
}

variable "vpc_name" {
  description = "VPC name prefix (for multi-VPC support)"
  type        = string
  default     = "main"
}

variable "github_org" {
  description = "GitHub organization/username"
  type        = string
  default     = "neighborlyjim"
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
  default     = "eBayScanner"
}

# Networking Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones to use"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets (costs money, disabled for free tier)"
  type        = bool
  default     = false
}

variable "use_default_vpc" {
  description = "Use default VPC instead of creating a new one (free tier option)"
  type        = bool
  default     = true
}

# ECR Configuration
variable "ecr_image_retention_count" {
  description = "Number of images to retain in ECR (free tier: 500MB total storage)"
  type        = number
  default     = 3 # Reduced for free tier - keep only 3 most recent images
}

variable "enable_image_scanning" {
  description = "Enable image scanning on ECR repositories (free tier: 100 scans/month)"
  type        = bool
  default     = false # Disabled by default to stay within free tier limits
}

variable "enable_cost_optimization" {
  description = "Enable aggressive cost optimization for free tier usage"
  type        = bool
  default     = true
}

# Database configuration (existing RDS instance)
variable "db_host" {
  description = "Database hostname (existing RDS instance)"
  type        = string
  default     = "ebay-scanner.cq5c4w6q2zo6.us-east-1.rds.amazonaws.com"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "ebay_scanner"
}

variable "db_user" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

# ECS Configuration (optimized for free tier)
variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  type        = string
  default     = null # Will use project_name-cluster if not specified
}

variable "ecs_task_cpu" {
  description = "CPU units for ECS tasks (256 = 0.25 vCPU, free tier compatible)"
  type        = number
  default     = 256
}

variable "ecs_task_memory" {
  description = "Memory for ECS tasks in MB (512MB, free tier compatible)"
  type        = number
  default     = 512
}

variable "ecs_desired_count" {
  description = "Desired number of ECS tasks (1 for free tier)"
  type        = number
  default     = 1
}

variable "ecs_max_capacity" {
  description = "Maximum number of ECS tasks for auto-scaling"
  type        = number
  default     = 2
}

variable "ecs_min_capacity" {
  description = "Minimum number of ECS tasks for auto-scaling"
  type        = number
  default     = 1
}

# Security Group Configuration
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the application"
  type        = list(string)
  default     = ["0.0.0.0/0"] # Open to internet by default, restrict as needed
}

variable "app_port" {
  description = "Port the application runs on"
  type        = number
  default     = 5000
}

# Tagging
variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# Resource naming configuration
variable "resource_name_prefix" {
  description = "Prefix for all resource names (useful for multi-app deployments)"
  type        = string
  default     = ""
}

variable "resource_name_suffix" {
  description = "Suffix for all resource names"
  type        = string
  default     = ""
}

# Load balancer configuration
variable "create_load_balancer" {
  description = "Whether to create an Application Load Balancer"
  type        = bool
  default     = false
}

# CloudWatch configuration
variable "cloudwatch_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 7
}

# VPC Flow Logs
variable "enable_vpc_flow_logs" {
  description = "Whether to enable VPC Flow Logs"
  type        = bool
  default     = false
}

# ECS task configuration
variable "cpu_web" {
  description = "CPU units for web service (256, 512, 1024, etc.)"
  type        = number
  default     = 256
}

variable "memory_web" {
  description = "Memory (MB) for web service"
  type        = number
  default     = 512
}

variable "cpu_worker" {
  description = "CPU units for worker service (256, 512, 1024, etc.)"
  type        = number
  default     = 256
}

variable "memory_worker" {
  description = "Memory (MB) for worker service"
  type        = number
  default     = 512
}

variable "instance_count_web" {
  description = "Number of web service instances to run"
  type        = number
  default     = 1
}

variable "instance_count_worker" {
  description = "Number of worker service instances to run"
  type        = number
  default     = 1
}

# Database configuration
variable "db_port" {
  description = "Database port"
  type        = string
  default     = "5432"
}
