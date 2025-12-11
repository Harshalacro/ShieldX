# ☁️ Azure for Students Deployment Guide

This guide is specifically designed for deploying **ShieldX** using an **Azure for Students** subscription.

## Prerequisites

1.  **Azure for Students Account**: [Sign up here](https://azure.microsoft.com/en-us/free/students/) (requires student email).
2.  **Azure CLI**: [Install here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
3.  **GitHub Account**: Your code should be pushed to a GitHub repository.

---

## Part 1: Set up Storage (Blob Storage)

We use Azure Blob Storage to host your datasets and models, so they are accessible from anywhere.

1.  **Login to Azure Portal**: [portal.azure.com](https://portal.azure.com).
2.  **Create Storage Account**:
    *   Search for "Storage accounts".
    *   Click **+ Create**.
    *   **Resource Group**: Create new (e.g., `ShieldX-RG`).
    *   **Storage account name**: Unique name (e.g., `shieldxdata123`).
    *   **Region**: Select one near you.
    *   **Redundancy**: "Locally-redundant storage (LRS)" (Cheaper).
    *   Click **Review + create** -> **Create**.
3.  **Get Connection String**:
    *   Go to your new Storage Account resource.
    *   On left menu, look for **Security + networking** -> **Access keys**.
    *   Copy the **Connection string** under `key1`.
    *   **SAVE THIS STRING!** You will need it later.
4.  **Upload Data & Models**:
    *   Go to **Data storage** -> **Containers**.
    *   Create a container named `data`. Upload your CSV files (`credit_card.csv`, etc.) here.
    *   Create a container named `models`. Upload your `.joblib` files here.

---

## Part 2: Deploy Web App

We will use **Azure Web App for Containers** to run your Dockerized application.

1.  **Open Terminal** (in VS Code).
2.  **Login to Azure CLI**:
    ```bash
    az login
    ```
3.  **Create App Service Plan** (Free Tier):
    ```bash
    az appservice plan create --name ShieldXPlan --resource-group ShieldX-RG --sku F1 --is-linux
    ```
    *(Note: If F1 (Free) is not available in your region, try B1 (Basic) which uses credits).*
4.  **Create Web App**:
    ```bash
    az webapp create --resource-group ShieldX-RG --plan ShieldXPlan --name shieldx-app-[YOUR_NAME] --deployment-container-image-name python:3.9
    ```
    *(Replace `[YOUR_NAME]` with a unique name).*

5.  **Configure Environment Variables**:
    This is where we connect the storage!
    ```bash
    az webapp config appsettings set --resource-group ShieldX-RG --name shieldx-app-[YOUR_NAME] --settings AZURE_STORAGE_CONNECTION_STRING="[PASTE_YOUR_CONNECTION_STRING_HERE]"
    ```

6.  **Deploy Code**:
    Since we have a `Dockerfile`, we can deploy directly.
    
    **Option A: GitHub Actions (Recommended)**
    *   Go to your App in Azure Portal -> **Deployment Center**.
    *   Source: **GitHub**.
    *   Authorize and select your repo.
    *   Azure will automatically create a workflow to build and deploy your Docker image.

    **Option B: Local Build & Push (If you have Docker Registry)**
    *   (Advanced: Push to Azure Container Registry first).

    **Option C: Zip Deploy (Simplest for code-only)**
    *   If not using Docker, you can deploy the code directly:
      ```bash
      az webapp up --sku F1 --name shieldx-app-[YOUR_NAME] --resource-group ShieldX-RG
      ```
---

## Part 3: Verify

1.  Go to your app URL: `https://shieldx-app-[YOUR_NAME].azurewebsites.net`.
2.  The app should load.
3.  It will attempt to download models/data from your Blob Storage on startup.
