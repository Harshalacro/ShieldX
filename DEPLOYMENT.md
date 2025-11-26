# 🚀 Deploying ShieldX to the Cloud

This guide explains how to deploy the **ShieldX AI Security Platform** to various cloud providers.

## Prerequisites
- [Docker](https://www.docker.com/) installed locally.
- A GitHub repository containing this code.

---

## Option 1: Google Cloud Run (Recommended for Scalability)
Google Cloud Run is a serverless platform that automatically scales your containers.

### 1. Install Google Cloud SDK
Download and install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

### 2. Authenticate & Configure
```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

### 3. Build & Push Docker Image
We will deploy the API and Dashboard as separate services or a single container. For simplicity, let's deploy the **Dashboard** (which talks to the API). *Note: In a production environment, you'd deploy them separately.*

**Dockerfile Adjustment (Optional):**
Ensure your `Dockerfile` exposes the correct port (Streamlit uses 8501).

**Deploy Command:**
```bash
gcloud run deploy shieldx-dashboard \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

*Follow the prompts. Once finished, Google Cloud will give you a public URL (e.g., `https://shieldx-dashboard-xyz.a.run.app`).*

---

## Option 2: Render / Railway (Easiest)
Platforms like Render or Railway allow you to deploy directly from GitHub.

### 1. Push Code to GitHub
Ensure your project is in a public or private GitHub repository.

### 2. Create New Web Service
- Go to [Render Dashboard](https://dashboard.render.com/).
- Click **New +** -> **Web Service**.
- Connect your GitHub repo.

### 3. Configure
- **Runtime:** Docker
- **Build Command:** (Leave empty, it uses Dockerfile)
- **Start Command:** (Leave empty, it uses CMD from Dockerfile)
- **Environment Variables:**
    - `PORT`: `8501` (Render expects the app to listen on this port)

### 4. Deploy
Click **Create Web Service**. Render will build your Docker image and deploy it.

---

## Option 3: Local Docker (Testing)
To run the entire stack (API + Dashboard + Simulator) on your machine or a VPS (like EC2/DigitalOcean).

### 1. Build & Run
```bash
docker-compose up --build -d
```

### 2. Access
- **Dashboard:** [http://localhost:8501](http://localhost:8501)
- **API:** [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Stop
```bash
docker-compose down
```
