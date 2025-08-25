# SSM Parameters for sensitive configuration
# These store secrets for ECS tasks to consume
# Supports multi-app deployments with variable naming

# Database password
resource "aws_ssm_parameter" "db_password" {
  name  = "/${local.name_prefix}${var.app_name}${local.name_suffix}/${var.environment}/db_password"
  type  = "SecureString"
  value = "PLACEHOLDER_CHANGE_ME" # Change this after deployment

  description = "Database password for ${var.app_name}"

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-db-password${local.name_suffix}"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      Component   = "database"
    }
  )

  lifecycle {
    ignore_changes = [value] # Don't update value after initial creation
  }
}

# eBay API credentials
resource "aws_ssm_parameter" "ebay_client_id" {
  name  = "/${local.name_prefix}${var.app_name}${local.name_suffix}/${var.environment}/ebay_client_id"
  type  = "SecureString"
  value = "PLACEHOLDER_CHANGE_ME" # Change this after deployment

  description = "eBay API Client ID for ${var.app_name}"

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-ebay-client-id${local.name_suffix}"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      Component   = "api"
    }
  )

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "ebay_client_secret" {
  name  = "/${local.name_prefix}${var.app_name}${local.name_suffix}/${var.environment}/ebay_client_secret"
  type  = "SecureString"
  value = "PLACEHOLDER_CHANGE_ME" # Change this after deployment

  description = "eBay API Client Secret for ${var.app_name}"

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-ebay-client-secret${local.name_suffix}"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      Component   = "api"
    }
  )

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "ebay_app_id" {
  name  = "/${local.name_prefix}${var.app_name}${local.name_suffix}/${var.environment}/ebay_app_id"
  type  = "SecureString"
  value = "PLACEHOLDER_CHANGE_ME" # Change this after deployment

  description = "eBay API App ID for ${var.app_name}"

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-ebay-app-id${local.name_suffix}"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      Component   = "api"
    }
  )

  lifecycle {
    ignore_changes = [value]
  }
}

resource "aws_ssm_parameter" "ebay_dev_id" {
  name  = "/${local.name_prefix}${var.app_name}${local.name_suffix}/${var.environment}/ebay_dev_id"
  type  = "SecureString"
  value = "PLACEHOLDER_CHANGE_ME" # Change this after deployment

  description = "eBay API Dev ID for ${var.app_name}"

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-ebay-dev-id${local.name_suffix}"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      Component   = "api"
    }
  )

  lifecycle {
    ignore_changes = [value]
  }
}
