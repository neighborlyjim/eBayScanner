# eBay Scanner - AI Agent Instructions

## 🏗️ Architecture Overview

This is a **multi-service eBay price monitoring application** with AI-powered DevOps workflow:

- **Frontend**: React/TypeScript (`frontend/`) with dark theme CSS
- **Backend**: Flask app (`app.py`) with eBay API integration via `scout.py`
- **Database**: PostgreSQL with SQLAlchemy models (TrackedItem, BuyItNowAverage)
- **Infrastructure**: Terraform modules (`terraform/`) for AWS ECS/ECR deployment
- **AI Integration**: MCP servers (`.vscode/mcp.json`) for natural language DevOps

## 🔧 Key Development Patterns

### Infrastructure as Code (Terraform)
- **Module-based approach**: Uses `terraform-aws-modules/vpc` and `umotif-public/ecs-fargate` instead of raw resources
- **Multi-app deployment**: Variables `resource_name_prefix/suffix` enable multiple apps in same VPC
- **Cost optimization**: `use_default_vpc=true` for free tier, aggressive ECR lifecycle policies
- **AWS Provider**: Requires `~> 6.0` (not 5.x) due to VPC module dependencies

### Container Strategy
- **Two services**: Web (`Dockerfile`) and Worker (`Dockerfile.worker`) with shared codebase
- **Python 3.13**: Uses `psycopg3` for PostgreSQL (not psycopg2)
- **Multi-stage builds**: Optimized for ECR 500MB free tier limit
- **Health checks**: Built into Dockerfiles for ECS readiness

### MCP-Powered Workflow
Essential for AI agents - enables natural language commands:
```bash
# Start MCP servers first
docker ps --filter name=upbeat_ride  # Terraform MCP container
uvx mcp-server-git --help             # Git operations
```

## 🚀 Critical Workflows

### Infrastructure Deployment
```bash
cd terraform
terraform init -upgrade  # Required after adding modules
terraform validate        # Check syntax
terraform plan           # Preview changes
terraform apply          # Deploy to AWS
```

### Local Development
```bash
docker-compose up -d      # Start local stack (PostgreSQL + Redis)
python app.py            # Run Flask locally
python scout.py          # Test eBay API integration
```

### Multi-App Deployment Pattern
```bash
# Deploy second app in same VPC
terraform apply -var='app_name=inventory-tracker' -var='resource_name_suffix=v2'

# Production environment with custom VPC
terraform apply -var='environment=prod' -var='use_default_vpc=false'
```

## 📊 eBay Integration Specifics

### API Structure
- **Finding API**: Used in `scout.py` for search and completed listings
- **Sandbox mode**: Uses `domain="svcs.sandbox.ebay.com"`
- **Price analysis**: `is_undervalued()` compares current vs historical averages
- **Background polling**: APScheduler runs every 5 minutes

### Database Schema
```python
# TrackedItem: Active auctions being monitored
# BuyItNowAverage: Historical price data for comparison
```

## 🔐 Security & Configuration

### Environment Variables
- **Database**: `DB_HOST/NAME/USER/PASSWORD` (RDS: `ebay-scanner.cq5c4w6q2zo6.us-east-1.rds.amazonaws.com`)
- **eBay API**: `EBAY_CLIENT_ID/SECRET/APP_ID/DEV_ID`
- **AWS**: Use SSM parameters in production (`terraform/ecr-ssm.tf`)

### Terraform Variables Pattern
```hcl
# Always use these locals for naming consistency
locals {
  name_prefix = var.resource_name_prefix != "" ? "${var.resource_name_prefix}-" : ""
  name_suffix = var.resource_name_suffix != "" ? "-${var.resource_name_suffix}" : ""
  cluster_name = "${local.name_prefix}${var.app_name}-cluster${local.name_suffix}"
}
```

## 🚨 Common Gotchas

1. **Provider Version**: Terraform requires AWS provider `~> 6.0` for VPC module compatibility
2. **psycopg3**: Python 3.13 requires `psycopg[binary]` not `psycopg2-binary`
3. **ECS Module**: Creates services but NOT cluster - need separate `aws_ecs_cluster` resource
4. **Default VPC**: Always check `var.use_default_vpc` conditions for data sources vs module outputs
5. **MCP Docker**: Terraform MCP server runs in container `upbeat_ride` - don't recreate

## 🎯 AI Agent Capabilities

With MCP integration, you can use natural language for:
- **Infrastructure**: "Deploy the latest Terraform changes"
- **Git operations**: "Create feature branch for new eBay categories"
- **Market analysis**: "Fetch current PlayStation 5 prices from eBay"
- **File operations**: "Update the requirements.txt with new dependencies"

## 📁 Key Files for Understanding

- `terraform/main.tf`: Module configuration and naming patterns
- `terraform/ecs.tf`: Two-service ECS setup with shared environment
- `app.py`: Flask routes and database models
- `scout.py`: eBay API integration and pricing logic
- `.github/workflows/build-and-deploy.yml`: CI/CD pipeline
- `terraform/terraform.tfvars.example`: Deployment configuration examples

Always check current file contents before making edits - this codebase evolves rapidly with module-based infrastructure.
