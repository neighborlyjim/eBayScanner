#!/usr/bin/env powershell
# Terraform Environment Deployment Script
# Usage: .\deploy.ps1 -Environment dev|prod
# 
# This script:
# 1. Validates required environment variables are set
# 2. Applies terraform with the appropriate .tfvars file
# 3. Uses TF_VAR_ environment variables to override sensitive values

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "prod")]
    [string]$Environment
)

# Color output functions
function Write-Success { param($Message) Write-Host "✅ $Message" -ForegroundColor Green }
function Write-Warning { param($Message) Write-Host "⚠️  $Message" -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host "❌ $Message" -ForegroundColor Red }
function Write-Info { param($Message) Write-Host "ℹ️  $Message" -ForegroundColor Cyan }

Write-Info "Deploying eBay Scanner to $Environment environment..."

# Required environment variables for sensitive data
$RequiredEnvVars = @(
    "TF_VAR_ebay_client_id",
    "TF_VAR_ebay_client_secret", 
    "TF_VAR_ebay_app_id",
    "TF_VAR_ebay_dev_id",
    "TF_VAR_db_password"
)

# Optional AWS credential environment variables
$AWSEnvVars = @(
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN"
)

# Validate required environment variables
Write-Info "Validating environment variables..."
$MissingVars = @()

foreach ($EnvVar in $RequiredEnvVars) {
    if (-not (Get-ChildItem Env: | Where-Object Name -eq $EnvVar.Replace("TF_VAR_", ""))) {
        if (-not (Get-ChildItem Env: | Where-Object Name -eq $EnvVar)) {
            $MissingVars += $EnvVar
        }
    }
}

if ($MissingVars.Count -gt 0) {
    Write-Error "Missing required environment variables:"
    foreach ($Var in $MissingVars) {
        Write-Host "  - $Var" -ForegroundColor Red
    }
    Write-Host ""
    Write-Warning "Set environment variables before running:"
    Write-Host '$Env:TF_VAR_ebay_client_id = "your-client-id"' -ForegroundColor Yellow
    Write-Host '$Env:TF_VAR_ebay_client_secret = "your-client-secret"' -ForegroundColor Yellow  
    Write-Host '$Env:TF_VAR_ebay_app_id = "your-app-id"' -ForegroundColor Yellow
    Write-Host '$Env:TF_VAR_ebay_dev_id = "your-dev-id"' -ForegroundColor Yellow
    Write-Host '$Env:TF_VAR_db_password = "your-db-password"' -ForegroundColor Yellow
    exit 1
}

Write-Success "All required environment variables are set"

# Check AWS credentials
$AWSCredsSet = $false
foreach ($AWSVar in $AWSEnvVars) {
    if (Get-ChildItem Env: | Where-Object Name -eq $AWSVar) {
        $AWSCredsSet = $true
        break
    }
}

if (-not $AWSCredsSet) {
    Write-Warning "No AWS credential environment variables detected"
    Write-Info "Assuming AWS credentials are configured via AWS CLI or IAM role"
}

# Validate terraform files exist
$TfVarsFile = "$Environment.tfvars"
if (-not (Test-Path $TfVarsFile)) {
    Write-Error "Terraform vars file not found: $TfVarsFile"
    exit 1
}

Write-Success "Found terraform vars file: $TfVarsFile"

# Initialize terraform if needed
if (-not (Test-Path ".terraform")) {
    Write-Info "Initializing Terraform..."
    terraform init
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Terraform init failed"
        exit 1
    }
    Write-Success "Terraform initialized"
}

# Validate terraform configuration
Write-Info "Validating Terraform configuration..."
terraform validate
if ($LASTEXITCODE -ne 0) {
    Write-Error "Terraform validation failed"
    exit 1
}
Write-Success "Terraform configuration is valid"

# Plan deployment
Write-Info "Planning Terraform deployment for $Environment..."
terraform plan -var-file="$TfVarsFile" -out="$Environment.tfplan"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Terraform plan failed"
    exit 1
}

Write-Success "Terraform plan completed successfully"
Write-Info "Plan saved to: $Environment.tfplan"

# Ask for confirmation before applying
Write-Host ""
Write-Warning "Ready to apply Terraform plan for $Environment environment"
$Confirmation = Read-Host "Do you want to apply these changes? (yes/no)"

if ($Confirmation -eq "yes") {
    Write-Info "Applying Terraform plan..."
    terraform apply "$Environment.tfplan"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Deployment to $Environment completed successfully! 🎉"
        Write-Info "To view outputs: terraform output"
        Write-Info "To destroy: terraform destroy -var-file='$TfVarsFile'"
    } else {
        Write-Error "Terraform apply failed"
        exit 1
    }
} else {
    Write-Info "Deployment cancelled. To apply later, run:"
    Write-Host "terraform apply $Environment.tfplan" -ForegroundColor Yellow
}
