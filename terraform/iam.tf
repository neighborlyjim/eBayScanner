# IAM resources for GitHub Actions to access ECR

# Get current AWS account ID
data "aws_caller_identity" "current" {}

# IAM policy for GitHub Actions ECR access
resource "aws_iam_policy" "github_actions_ecr" {
  name        = "${var.project_name}-github-actions-ecr"
  description = "Policy for GitHub Actions to push images to ECR"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:PutImage"
        ]
        Resource = [
          aws_ecr_repository.web.arn,
          aws_ecr_repository.worker.arn
        ]
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-github-actions-ecr"
  }
}

# IAM user for GitHub Actions
resource "aws_iam_user" "github_actions" {
  name = "${var.project_name}-github-actions"
  path = "/"

  tags = {
    Name        = "${var.project_name}-github-actions"
    Description = "IAM user for GitHub Actions CI/CD pipeline"
  }
}

# Attach ECR policy to GitHub Actions user
resource "aws_iam_user_policy_attachment" "github_actions_ecr" {
  user       = aws_iam_user.github_actions.name
  policy_arn = aws_iam_policy.github_actions_ecr.arn
}

# Access key for GitHub Actions user
resource "aws_iam_access_key" "github_actions" {
  user = aws_iam_user.github_actions.name
}

# OIDC provider for GitHub Actions (more secure alternative to access keys)
resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"

  client_id_list = [
    "sts.amazonaws.com",
  ]

  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd"
  ]

  tags = {
    Name = "${var.project_name}-github-oidc"
  }
}

# IAM role for GitHub Actions OIDC
resource "aws_iam_role" "github_actions_oidc" {
  name = "${var.project_name}-github-actions-oidc"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github.arn
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_org}/${var.github_repo}:*"
          }
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-github-actions-oidc"
  }
}

# Attach ECR policy to OIDC role
resource "aws_iam_role_policy_attachment" "github_actions_oidc_ecr" {
  role       = aws_iam_role.github_actions_oidc.name
  policy_arn = aws_iam_policy.github_actions_ecr.arn
}
