# Build and push Docker images for eBay Scanner
# This script builds both web and worker images and pushes them to ECR

param(
    [Parameter(Mandatory=$true)]
    [string]$Environment,
    
    [string]$Region = "us-east-1",
    [string]$Tag = "latest"
)

# Get ECR repository URLs from Terraform outputs
Write-Host "Getting ECR repository URLs from Terraform..." -ForegroundColor Green
cd terraform
$EcrWebRepo = (terraform output -raw ecr_web_repository_url)
$EcrWorkerRepo = (terraform output -raw ecr_worker_repository_url)
cd ..

if ([string]::IsNullOrEmpty($EcrWebRepo) -or [string]::IsNullOrEmpty($EcrWorkerRepo)) {
    Write-Error "Failed to get ECR repository URLs. Make sure Terraform has been applied."
    exit 1
}

Write-Host "ECR Web Repository: $EcrWebRepo" -ForegroundColor Yellow
Write-Host "ECR Worker Repository: $EcrWorkerRepo" -ForegroundColor Yellow

# Login to ECR
Write-Host "Logging into ECR..." -ForegroundColor Green
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin "$($EcrWebRepo.Split('/')[0])"

if ($LASTEXITCODE -ne 0) {
    Write-Error "ECR login failed"
    exit 1
}

# Build web image
Write-Host "Building web image..." -ForegroundColor Green
docker build -t "$EcrWebRepo`:$Tag" -f backend/Dockerfile backend/

if ($LASTEXITCODE -ne 0) {
    Write-Error "Web image build failed"
    exit 1
}

# Build worker image
Write-Host "Building worker image..." -ForegroundColor Green
docker build -t "$EcrWorkerRepo`:$Tag" -f backend/Dockerfile.worker backend/

if ($LASTEXITCODE -ne 0) {
    Write-Error "Worker image build failed"
    exit 1
}

# Push web image
Write-Host "Pushing web image..." -ForegroundColor Green
docker push "$EcrWebRepo`:$Tag"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Web image push failed"
    exit 1
}

# Push worker image
Write-Host "Pushing worker image..." -ForegroundColor Green
docker push "$EcrWorkerRepo`:$Tag"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Worker image push failed"
    exit 1
}

Write-Host "Successfully built and pushed both images!" -ForegroundColor Green
Write-Host "Web image: $EcrWebRepo`:$Tag" -ForegroundColor Yellow
Write-Host "Worker image: $EcrWorkerRepo`:$Tag" -ForegroundColor Yellow
