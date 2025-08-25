# ECS Cluster using a popular module
module "ecs_cluster" {
  source  = "umotif-public/ecs-fargate/aws"
  version = "~> 8.2"

  name_prefix = "${local.name_prefix}${var.app_name}-web${local.name_suffix}"

  # Cluster and VPC configuration
  cluster_id = aws_ecs_cluster.main.id
  vpc_id     = var.use_default_vpc ? data.aws_vpc.default[0].id : module.vpc.vpc_id

  # Networking
  private_subnet_ids           = var.use_default_vpc ? data.aws_subnets.default[0].ids : module.vpc.private_subnets
  task_container_assign_public_ip = var.use_default_vpc

  # Container configuration for web service
  task_container_image = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${local.name_prefix}${var.app_name}-web${local.name_suffix}:latest"
  task_container_port  = 5000
  task_host_port      = 5000

  # Resource allocation
  task_definition_cpu    = var.cpu_web
  task_definition_memory = var.memory_web
  desired_count         = var.instance_count_web

  # Environment variables
  task_container_environment = {
    FLASK_ENV           = var.environment
    DATABASE_URL        = "postgresql://${var.db_user}:${aws_ssm_parameter.db_password.value}@${var.db_host}:${var.db_port}/${var.db_name}"
    EBAY_CLIENT_ID      = aws_ssm_parameter.ebay_client_id.value
    EBAY_CLIENT_SECRET  = aws_ssm_parameter.ebay_client_secret.value
    EBAY_APP_ID         = aws_ssm_parameter.ebay_app_id.value
    EBAY_DEV_ID         = aws_ssm_parameter.ebay_dev_id.value
  }

  # Load balancing (optional)
  load_balanced = var.create_load_balancer

  # Logging
  enable_logs           = true
  log_retention_in_days = var.cloudwatch_retention_days

  # Security
  enable_execute_command = true  # For debugging

  # Tags
  tags = merge(local.common_tags, {
    Service = "web"
  })
}

# Separate ECS Cluster resource since the module doesn't create it
resource "aws_ecs_cluster" "main" {
  name = local.cluster_name

  configuration {
    execute_command_configuration {
      logging = "OVERRIDE"
      log_configuration {
        cloud_watch_log_group_name = aws_cloudwatch_log_group.ecs_logs.name
      }
    }
  }

  tags = merge(local.common_tags, {
    Name = local.cluster_name
  })
}

# Worker service using the same module but different configuration
module "ecs_worker" {
  count = var.instance_count_worker > 0 ? 1 : 0

  source  = "umotif-public/ecs-fargate/aws"
  version = "~> 8.2"

  name_prefix = "${local.name_prefix}${var.app_name}-worker${local.name_suffix}"

  # Cluster and VPC configuration
  cluster_id = aws_ecs_cluster.main.id
  vpc_id     = var.use_default_vpc ? data.aws_vpc.default[0].id : module.vpc.vpc_id

  # Networking
  private_subnet_ids           = var.use_default_vpc ? data.aws_subnets.default[0].ids : module.vpc.private_subnets
  task_container_assign_public_ip = var.use_default_vpc

  # Container configuration for worker service
  task_container_image = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/${local.name_prefix}${var.app_name}-worker${local.name_suffix}:latest"
  task_container_port  = 8080  # Different port for worker
  task_host_port      = 8080

  # Resource allocation
  task_definition_cpu    = var.cpu_worker
  task_definition_memory = var.memory_worker
  desired_count         = var.instance_count_worker

  # Environment variables (same as web but different service)
  task_container_environment = {
    FLASK_ENV           = var.environment
    DATABASE_URL        = "postgresql://${var.db_user}:${aws_ssm_parameter.db_password.value}@${var.db_host}:${var.db_port}/${var.db_name}"
    EBAY_CLIENT_ID      = aws_ssm_parameter.ebay_client_id.value
    EBAY_CLIENT_SECRET  = aws_ssm_parameter.ebay_client_secret.value
    EBAY_APP_ID         = aws_ssm_parameter.ebay_app_id.value
    EBAY_DEV_ID         = aws_ssm_parameter.ebay_dev_id.value
  }

  # No load balancer for worker
  load_balanced = false

  # Logging
  enable_logs           = true
  log_retention_in_days = var.cloudwatch_retention_days

  # Security
  enable_execute_command = true  # For debugging

  # Tags
  tags = merge(local.common_tags, {
    Service = "worker"
  })
}

# CloudWatch Log Group for ECS cluster
resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/aws/ecs/${local.cluster_name}"
  retention_in_days = var.cloudwatch_retention_days

  tags = merge(local.common_tags, {
    Name = "${local.cluster_name}-logs"
  })
}
