# ⚡ One-Click Azure Deployment

We have created an automated script to handle the deployment for you, avoiding all the Azure Portal glitches.

## Prerequisites
1.  **Azure Connection String**: You should have this from the Storage Account setup you already did.
2.  **Azure CLI**: You already checked this is installed.

## How to Deploy

1.  **Open Terminal** in this project folder.
2.  **Run the script**:
    ```powershell
    ./deploy_azure.ps1
    ```
3.  **Follow the prompts**:
    *   It will ask you to Login (if not already).
    *   Enter a **Unique App Name** (e.g., `shieldx-beta-harshal`).
    *   Paste your **Connection String**.

**That's it!** The script will:
*   Create the App Service (correctly configured as Code, not Container).
*   Upload and build your code.
*   Set your Connection String automatically.
*   Give you the final URL.

---

## Alternative: Manual Commands (Azure CLI)

If you prefer to run the commands yourself (or if PowerShell is giving you trouble), just run these 3 lines in your terminal one by one:

1.  **Login**:
    ```bash
    az login
    ```
2.  **Create & Deploy** (Replace `unique-app-name` with your own name):
    ```bash
    az webapp up --runtime PYTHON:3.10 --sku F1 --resource-group ShieldX-RG --name unique-app-name
    ```
3.  **Set Connection String**:
    ```bash
    az webapp config appsettings set --name unique-app-name --resource-group ShieldX-RG --settings AZURE_STORAGE_CONNECTION_STRING="<PASTE_YOUR_CONNECTION_STRING_HERE>"
    ```

---
*Note: If `deploy_azure.ps1` gives a security error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.*
