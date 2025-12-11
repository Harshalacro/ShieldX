# ☁️ Deploying ShieldX to Microsoft Azure

This guide explains how to host the **ShieldX** application on Microsoft Azure using **Azure Web App for Containers**. This is a scalable and easy-to-manage way to run Docker containers in the cloud.

## Prerequisites
-   **Azure Account:** [Sign up for free](https://azure.microsoft.com/free/).
    > **🎓 Student Tip:** If you have an **Azure for Students** account, the `B1` SKU used in this guide is covered by your free credits ($100/year). You won't be charged as long as you have credits remaining.
-   **Azure CLI:** [Install the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
-   **Docker:** Installed locally.

---

## Step 1: Login to Azure
Open your terminal and log in to your Azure account:
```bash
az login
```
> **⚠️ Login Error?** If you see `AADSTS50076` (MFA Required), try this command instead:
> ```bash
> az login --use-device-code
> ```
> It will give you a code to enter at [microsoft.com/devicelogin](https://microsoft.com/devicelogin).

## Step 2: Create a Resource Group
A resource group is a container that holds related resources for an Azure solution.
```bash
az group create --name ShieldXGroup --location eastus
```

## Step 3: Create an Azure Container Registry (ACR)
You need a place to store your Docker images.

> **⚠️ Common Error:** If you see `MissingSubscriptionRegistration`, run this command to register the provider:
> ```bash
> az provider register --namespace Microsoft.ContainerRegistry
> ```
> *It may take a few minutes to take effect.*

```bash
az acr create --resource-group ShieldXGroup --name shieldxregistry --sku Basic --admin-enabled true
```
*Note: The name `shieldxregistry` must be unique globally. If it fails, try adding some numbers (e.g., `shieldxregistry2024`).*

## Step 4: Build and Push Docker Image
### Option A: Using Azure Cloud Shell (Easiest)
Since Cloud Shell doesn't run Docker, use **ACR Tasks** to build in the cloud:

1.  **Get the Code (If you haven't already):**
    ```bash
    git clone https://github.com/YOUR_USERNAME/ShieldX.git
    cd ShieldX
    ```
    *(Replace `YOUR_USERNAME` with your actual GitHub username)*

    > **🔍 Verify:** Run `ls` and make sure you see `Dockerfile` in the list.

2.  **Build in the Cloud:**
    ```bash
    az acr build --registry shieldxregistry --image shieldx:latest .
    ```
    *(This builds and pushes the image automatically!)*

### Option B: Building Locally (If you have Docker Desktop)
1.  **Login to ACR:**
    ```bash
    az acr login --name shieldxregistry
    ```

2.  **Build & Push:**
    ```bash
    docker build -t shieldxregistry.azurecr.io/shieldx:latest .
    docker push shieldxregistry.azurecr.io/shieldx:latest
    ```

### Option C: Deploy as Code (If Docker Build Fails)
If you see `TasksOperationsNotAllowed`, your student account might block Cloud Builds. Use this method instead (it deploys the Python code directly):

1.  **Deploy the App:**
    ```bash
    az webapp up --name shieldx-app-unique --resource-group ShieldXGroup --sku B1 --runtime "PYTHON:3.9"
    ```
    *(Replace `shieldx-app-unique` with a unique name like `shieldx-sahil-123`)*

2.  **Configure Startup Command:**
    ```bash
    az webapp config set --name shieldx-app-unique --resource-group ShieldXGroup --startup-file "sh entrypoint.sh"
    ```
    *(Remember to use the same name you chose above!)*

## Step 5: Create an App Service Plan
This defines the compute resources for your web app.
```bash
az appservice plan create --name ShieldXPlan --resource-group ShieldXGroup --sku B1 --is-linux
```

## Step 6: Create the Web App
Now, deploy the container to a Web App.
```bash
az webapp create --resource-group ShieldXGroup --plan ShieldXPlan --name shieldx-app --deployment-container-image-name shieldxregistry.azurecr.io/shieldx:latest
```
*Note: `shieldx-app` must also be unique. Try `shieldx-app-yourname` if needed.*

## Step 7: Configure Environment Variables
ShieldX needs to know which port to listen on. Azure Web Apps listen on port 80 or 8080 by default, but our container uses 8501 (Streamlit) or 8000 (API).

**For Streamlit Dashboard (Recommended for User Interface):**
We need to tell Azure to route traffic to port 8501.
```bash
az webapp config appsettings set --resource-group ShieldXGroup --name shieldx-app --settings WEBSITES_PORT=8501
```

## Step 8: Browse Your App
Your application is now live!
Go to: `http://shieldx-app.azurewebsites.net`

---

## Troubleshooting
-   **Application Error:** Check the logs using:
    ```bash
    az webapp log tail --resource-group ShieldXGroup --name shieldx-app
    ```
-   **Slow Startup:** The first start might take a few minutes as it pulls the image.
