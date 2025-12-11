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
4.  **Upload Data & Models** (Detailed Steps):
    *   **STOP:** If you are seeing "Storage Center" or "Storage Browser", you are in the wrong place.
    *   **Go to the right place**:
        1.  In the **Global Search Bar** (very top center of the blue strip at the top of the webpage), type "Storage accounts".
        2.  Click usually the first result **Storage accounts** ( Service ).
        3.  You should see a list of accounts. Click on the **Name** of the one you created (e.g., `shieldxdata123`).
    *   **Now find Containers**:
        *   Once you are inside YOUR account blade (you will see your account name at the top left), look at the left sidebar.
        *   Scroll down to **Data storage**.
        *   Click **Containers**.
    *   **Create 'data' Container**:
        *   Click **+ Container**.
        *   Name it `data`.
        *   Click **Create**.
    *   **Upload CSVs**:
        *   Click into the `data` container.
        *   Click **Upload**, browse to your project `data/` folder, select all CSVs, and upload.
    *   **Create 'models' Container**:
        *   Go back to **Containers**.
        *   Create container `models`.
        *   Upload all `.joblib` files from `models/` folder.

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
    *   **Go to Deployment Center**: In your Web App's left menu, click **Deployment Center**.
    *   **Select Source**:
        *   **CRITICAL:** Do NOT select "Container Registry" (the first option).
        *   **CRITICAL:** If you see fields like "Registry user name", "Registry password", or "index.docker.io", you are on the WRONG OPTION.
        *   Click the **radio button** next to **GitHub Actions** (usually the second option).
    *   **TROUBLESHOOTING:**
        *   **Problem:** "Save" button is greyed out/disabled.
        *   **Reason:** You are seeing a section called **"Registry settings"** asking for an image. This means "Container Registry" is selected.
        *   **Fix 1:** Scroll back up to **Source** and click **GitHub Actions** again.
        *   **Fix 2 (If it's stuck):** The Azure Portal might be glitching. Click the **Discard** button at the top of the page ...
        *   **Fix 3 (The "Start Over" Fix - Recommended):**
            *   If you are stuck in this "Containers" view and can't find a "Disconnect" or "Source" button, **stop fighting the menu.**
            *   Go to the **Overview** page (top left of the menu).
            *   Click **Delete** (trash icon at the top) to delete this specific Web App.
            *   Create a new Web App (Step 2 of this guide). It only takes 1 minute.
            *   This time, **select GitHub Actions immediately** in the Deployment Center. This is much faster than debugging!
    *   **Authorize GitHub**:
        *   Click the **Authorize** button and sign in to your GitHub account.
    *   **Configure Build**:
        *   **Organization**: Select your GitHub username.
        *   **Repository**: Select `ShieldX` (or whatever you named your repo).
        *   **Branch**: Select `main`.
    *   **Save**:
        *   Click **Save** at the top left of the page.
    *   *Azure will now automatically create a workflow file in your GitHub repo, build your Docker image, and deploy it. This takes about 5-10 minutes.*
---

## Part 3: Verify

1.  Go to your app URL: `https://shieldx-app-[YOUR_NAME].azurewebsites.net`.
2.  The app should load.
3.  It will attempt to download models/data from your Blob Storage on startup.
