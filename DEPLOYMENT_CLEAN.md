# 🚀 ShieldX: Clean Deployment Guide (Azure Cloud Shell)

This guide is a **fresh start**. We will use the **"Code Deploy"** method.
This method **skips Docker builds** entirely, which fixes the `TasksOperationsNotAllowed` error you faced.

---

## Step 1: Prepare Cloud Shell
1.  Open the **Azure Cloud Shell** (top right `>_` icon in Azure Portal).
2.  Run these commands to clean up any old files and get a fresh copy of your code:

    ```bash
    cd ~
    rm -rf ShieldX
    git clone https://github.com/YOUR_GITHUB_USERNAME/ShieldX.git
    cd ShieldX
    ```
    *(Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username)*

---

## Step 2: Check Available Python Versions
Azure changes supported versions often. Let's see what is available for you.

1.  Run this command:
    ```bash
    az webapp list-runtimes --os linux --output table | grep PYTHON
    ```
2.  Look for the latest supported version (e.g., `PYTHON:3.10` or `PYTHON:3.11`).
    *   *We will use `PYTHON:3.10` in the next step, but if you see 3.11 is available, you can use that too.*

---

## Step 3: Deploy the App
We will create a **NEW** resource group and app to avoid any conflicts with the old errors.

1.  Run this command (it does everything in one go):
    ```bash
    az webapp up --name shieldx-final-app --resource-group ShieldX_Clean_RG --sku B1 --os-type Linux --runtime "PYTHON:3.10"
    ```
    *   **Note:** If `shieldx-final-app` is taken, change it to something unique like `shieldx-final-yourname`.
    *   **Note:** If it complains about the runtime, use the exact string you found in Step 2 (e.g., `PYTHON|3.10`).

    *Wait for this to finish. It might take 2-3 minutes.*

---

## Step 4: Configure Startup
Once the app is created, we need to tell it how to start (run both API and Dashboard).

1.  Run this command:
    ```bash
    az webapp config set --name shieldx-final-app --resource-group ShieldX_Clean_RG --startup-file "sh entrypoint.sh"
    ```
    *(Make sure to use the same app name you used in Step 3!)*

---

## Step 5: Verify
1.  Go to your URL: `http://shieldx-final-app.azurewebsites.net`
    *(Or whatever name you chose)*
2.  It might take 1-2 minutes to start up. If you see "Application Error", wait a bit and refresh.

---

## 🛑 Troubleshooting
*   **"Runtime not supported":** Make sure you ran Step 2 and picked a valid version from the list.
*   **"Resource group exists":** We used `ShieldX_Clean_RG` to be safe.
*   **"MSI token audience" / "Credential problem":**
    This is a Cloud Shell glitch. Run these commands to refresh your session:
    ```bash
    az logout
    az login
    ```
    Then run the `az webapp up` command again.
