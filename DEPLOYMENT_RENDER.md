# Deploying ShieldX to Render (Free & Easy)

Since your application is already **Dockerized** and on **GitHub**, **Render** is the perfect free options. It reads your `Dockerfile` and deploys it automatically.

## Why Render?
*   **Free Tier:** Generous free tier for web services.
*   **Zero Config:** It just reads your `Dockerfile`.
*   **HTTPS:** Automatic SSL (needed for Browser Extensions).
*   **GitHub Integration:** Pushing to `main` deploys the new version.

## Step-by-Step Guide

### 1. Create a Render Account
1.  Go to [dashboard.render.com](https://dashboard.render.com/).
2.  Sign up/Login with **GitHub**.

### 2. Create a "Web Service"
1.  Click the **"New +"** button and select **"Web Service"**.
2.  Select **"Build and deploy from a Git repository"**.
3.  Find your **ShieldX** repository in the list and click **"Connect"**.

### 3. Configure the Service
Render will auto-detect Docker. Just check these settings:

*   **Name:** `shieldx-api` (or similar)
*   **Region:** Singapore (or closest to you)
*   **Runtime:** **Docker** (This is crucial! It should be auto-selected because you have a Dockerfile).
*   **Instance Type:** **Free**

### 4. Environment Variables (Optional)
If you still want to use your Azure Storage for models (since you already set it up), you can add the environment variable here.
1.  Scroll down to **"Advanced"**.
2.  Click **"Add Environment Variable"**.
3.  Key: `AZURE_STORAGE_CONNECTION_STRING`
4.  Value: *(Paste your connection string)*

*Note: If you skip this, ShieldX will just use the local models inside the Docker image, which works fine too!*

### 5. Deploy
1.  Click **"Create Web Service"**.
2.  Render will verify the Dockerfile, build the image, and deploy it.
3.  This takes about 3-5 minutes.

### 6. Get your URL
Once finished, you will see a URL like: `https://shieldx-api.onrender.com`.
**Copy this URL.** We will use it for the Browser Extension.
