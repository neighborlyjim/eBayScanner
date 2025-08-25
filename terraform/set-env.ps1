#!/usr/bin/env powershell
# Environment Variables Setup Script
# Usage: .\set-env.ps1 -Environment dev|prod
#
# This script helps you set the required environment variables for Terraform deployment

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("dev", "prod")]
    [string]$Environment
)

Write-Host "🔧 Setting up environment variables for $Environment environment" -ForegroundColor Green
Write-Host ""

Write-Host "Please enter the following values (they will be set as TF_VAR_ environment variables):" -ForegroundColor Yellow
Write-Host ""

# Prompt for eBay API credentials
Write-Host "📧 eBay API Configuration:" -ForegroundColor Cyan
$EbayClientId = Read-Host "eBay Client ID"
$EbayClientSecret = Read-Host "eBay Client Secret" -AsSecureString
$EbayAppId = Read-Host "eBay App ID"  
$EbayDevId = Read-Host "eBay Dev ID"

Write-Host ""
Write-Host "🗄️  Database Configuration:" -ForegroundColor Cyan
$DbPassword = Read-Host "Database Password" -AsSecureString

Write-Host ""
Write-Host "☁️  AWS Configuration (optional - leave empty if using AWS CLI):" -ForegroundColor Cyan
$AWSAccessKey = Read-Host "AWS Access Key ID (optional)"
$AWSSecretKey = Read-Host "AWS Secret Access Key (optional)" -AsSecureString
$AWSSessionToken = Read-Host "AWS Session Token (optional)" -AsSecureString

# Convert secure strings to plain text for environment variables
$EbayClientSecretPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($EbayClientSecret))
$DbPasswordPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($DbPassword))

# Set eBay API environment variables
$Env:TF_VAR_ebay_client_id = $EbayClientId
$Env:TF_VAR_ebay_client_secret = $EbayClientSecretPlain
$Env:TF_VAR_ebay_app_id = $EbayAppId
$Env:TF_VAR_ebay_dev_id = $EbayDevId
$Env:TF_VAR_db_password = $DbPasswordPlain

# Set AWS credentials if provided
if ($AWSAccessKey) {
    $Env:AWS_ACCESS_KEY_ID = $AWSAccessKey
}

if ($AWSSecretKey.Length -gt 0) {
    $AWSSecretKeyPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($AWSSecretKey))
    $Env:AWS_SECRET_ACCESS_KEY = $AWSSecretKeyPlain
}

if ($AWSSessionToken.Length -gt 0) {
    $AWSSessionTokenPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($AWSSessionToken))
    $Env:AWS_SESSION_TOKEN = $AWSSessionTokenPlain
}

Write-Host ""
Write-Host "✅ Environment variables set successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Environment variables set:" -ForegroundColor Cyan
Write-Host "  - TF_VAR_ebay_client_id" -ForegroundColor Gray
Write-Host "  - TF_VAR_ebay_client_secret (hidden)" -ForegroundColor Gray  
Write-Host "  - TF_VAR_ebay_app_id" -ForegroundColor Gray
Write-Host "  - TF_VAR_ebay_dev_id" -ForegroundColor Gray
Write-Host "  - TF_VAR_db_password (hidden)" -ForegroundColor Gray

if ($AWSAccessKey) {
    Write-Host "  - AWS_ACCESS_KEY_ID" -ForegroundColor Gray
}
if ($AWSSecretKey.Length -gt 0) {
    Write-Host "  - AWS_SECRET_ACCESS_KEY (hidden)" -ForegroundColor Gray
}
if ($AWSSessionToken.Length -gt 0) {
    Write-Host "  - AWS_SESSION_TOKEN (hidden)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "🚀 Ready to deploy! Run:" -ForegroundColor Green
Write-Host ".\deploy.ps1 -Environment $Environment" -ForegroundColor Yellow

# Clear sensitive variables from memory
$EbayClientSecretPlain = $null
$DbPasswordPlain = $null
if ($AWSSecretKeyPlain) { $AWSSecretKeyPlain = $null }
if ($AWSSessionTokenPlain) { $AWSSessionTokenPlain = $null }
