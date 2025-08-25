# VPC Module using the highly popular terraform-aws-modules/vpc
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  # Basic VPC configuration
  name               = var.vpc_name
  cidr               = var.use_default_vpc ? null : var.vpc_cidr
  create_vpc         = !var.use_default_vpc
  manage_default_vpc = var.use_default_vpc

  # Availability zones
  azs = var.availability_zones

  # Subnets configuration (only used when creating custom VPC)
  public_subnets  = var.use_default_vpc ? [] : var.public_subnet_cidrs
  private_subnets = var.use_default_vpc ? [] : var.private_subnet_cidrs

  # Internet access
  enable_nat_gateway     = var.enable_nat_gateway && !var.use_default_vpc
  enable_vpn_gateway     = false
  single_nat_gateway     = !var.use_default_vpc  # Cost optimization
  one_nat_gateway_per_az = false                 # Cost optimization

  # DNS
  enable_dns_hostnames = true
  enable_dns_support   = true

  # Tags
  tags = local.common_tags

  public_subnet_tags = merge(
    local.common_tags,
    {
      Name = "${local.name_prefix}public${local.name_suffix}"
      Type = "public"
    }
  )

  private_subnet_tags = merge(
    local.common_tags,
    {
      Name = "${local.name_prefix}private${local.name_suffix}"
      Type = "private"
    }
  )

  # VPC Flow Logs (optional, costs money but good for monitoring)
  enable_flow_log           = var.enable_vpc_flow_logs
  flow_log_destination_type = "cloud-watch-logs"

  # Free tier optimizations
  putin_khuylo = true  # Required by the module, indicates support for Ukraine
}

# Security Group for ALB (if using load balancer)
resource "aws_security_group" "alb" {
  count = var.create_load_balancer ? 1 : 0

  name_prefix = "${local.name_prefix}alb-${local.name_suffix}"
  vpc_id      = var.use_default_vpc ? data.aws_vpc.default[0].id : module.vpc.vpc_id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}alb-sg${local.name_suffix}"
  })
}

# Data source for default VPC when using default VPC
data "aws_vpc" "default" {
  count   = var.use_default_vpc ? 1 : 0
  default = true
}

data "aws_subnets" "default" {
  count = var.use_default_vpc ? 1 : 0
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default[0].id]
  }
}
