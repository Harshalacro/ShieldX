# ShieldX Automated Deployment Script
# This script will deploy your app to Azure for Students automatically.

Write-Host "=========================================="
Write-Host "   ShieldX Azure Deployment Assistant"
Write-Host "=========================================="
Write-Host ""

# 1. Check Login
Write-Host "Checking Azure login status..."
$account = az account show 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to Azure..."
    az login
}

# 2. Get Inputs
$appName = Read-Host "Step 1: Enter a unique name for your App (e.g., shieldx-yourname-001)"
if ([string]::IsNullOrWhiteSpace($appName)) {
    Write-Error "App Name is required."
    exit 1
}

$connStr = Read-Host "Step 2: Paste your Azure Storage CONNECTION STRING (from the previous step)"
if ([string]::IsNullOrWhiteSpace($connStr)) {
    Write-Error "Connection String is required."
    exit 1
}

# 3. Create & Deploy
Write-Host ""
Write-Host "Step 3: Deploying App to Azure (This takes 5-10 minutes)..."
Write-Host "Creating 'ShieldX-RG' resource group and deploying app..."

# Using Python 3.10 as 3.9 is deprecated in some regions
# Using F1 (Free) tier
az webapp up --runtime "PYTHON:3.10" --sku F1 --name $appName --resource-group ShieldX-RG

if ($LASTEXITCODE -ne 0) {
    Write-Error "Deployment failed. Please check the error message above."
    exit 1
}

# 4. Configure Settings
Write-Host ""
Write-Host "Step 4: Configuring Connection String..."
az webapp config appsettings set --name $appName --resource-group ShieldX-RG --settings AZURE_STORAGE_CONNECTION_STRING="$connStr"

Write-Host ""
Write-Host "=========================================="
Write-Host "SUCCESS! Your app is live."
Write-Host "URL: https://$appName.azurewebsites.net"
Write-Host "=========================================="
Write-Host ""
Read-Host "Press Enter to exit..."
