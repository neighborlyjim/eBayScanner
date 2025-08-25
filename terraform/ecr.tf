# ECR repositories for eBay Scanner application components
# Optimized for AWS Free Tier (500MB ECR storage, 100 image scans/month)
# Supports multi-app deployments with variable naming

# ECR repository for web application
resource "aws_ecr_repository" "web" {
  name         = "${local.name_prefix}${var.app_name}-web${local.name_suffix}"
  force_delete = true

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = var.enable_image_scanning
  }

  encryption_configuration {
    encryption_type = "AES256" # Free tier compatible
  }

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-web${local.name_suffix}"
      Component   = "web"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      CostCenter  = "free-tier"
    }
  )
}

# ECR repository for worker application
resource "aws_ecr_repository" "worker" {
  name         = "${local.name_prefix}${var.app_name}-worker${local.name_suffix}"
  force_delete = true

  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = var.enable_image_scanning
  }

  encryption_configuration {
    encryption_type = "AES256" # Free tier compatible
  }

  tags = merge(
    var.additional_tags,
    {
      Name        = "${local.name_prefix}${var.app_name}-worker${local.name_suffix}"
      Component   = "worker"
      Environment = var.environment
      Project     = var.project_name
      App         = var.app_name
      CostCenter  = "free-tier"
    }
  )
}

# Aggressive lifecycle policy for web repository - optimized for free tier
resource "aws_ecr_lifecycle_policy" "web" {
  repository = aws_ecr_repository.web.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only last ${var.ecr_image_retention_count} tagged images (free tier optimization)"
        selection = {
          tagStatus   = "tagged"
          countType   = "imageCountMoreThan"
          countNumber = var.ecr_image_retention_count
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Delete untagged images immediately (free tier storage optimization)"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "hours"
          countNumber = 1 # Delete untagged images after 1 hour
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# Aggressive lifecycle policy for worker repository - optimized for free tier
resource "aws_ecr_lifecycle_policy" "worker" {
  repository = aws_ecr_repository.worker.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep only last ${var.ecr_image_retention_count} tagged images (free tier optimization)"
        selection = {
          tagStatus   = "tagged"
          countType   = "imageCountMoreThan"
          countNumber = var.ecr_image_retention_count
        }
        action = {
          type = "expire"
        }
      },
      {
        rulePriority = 2
        description  = "Delete untagged images immediately (free tier storage optimization)"
        selection = {
          tagStatus   = "untagged"
          countType   = "sinceImagePushed"
          countUnit   = "hours"
          countNumber = 1 # Delete untagged images after 1 hour
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}
