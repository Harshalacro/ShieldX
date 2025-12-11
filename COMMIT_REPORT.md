# 📝 Git Commit Report

**Date:** 2025-12-07
**Branch:** main

## 🚀 Major Features Added

### 1. ShieldX Browser Extension (`/extension`)
-   **New Feature:** Created a fully functional Chrome/Edge extension.
-   **Files:**
    -   `manifest.json`: Configuration and permissions.
    -   `popup.html/js`: UI for manual scanning and settings.
    -   `background.js`: Service worker for auto-scanning in the background.
    -   `icons/`: Generated and fixed extension icons.

### 2. Azure Deployment Guides
-   **`DEPLOYMENT_AZURE.md`**: Comprehensive guide for Docker-based deployment (ACR).
-   **`DEPLOYMENT_CLEAN.md`**: Simplified "Code Deploy" guide for Student Accounts (bypassing Docker build restrictions).

### 3. Documentation
-   **`USER_MANUAL.md`**: Completely rewritten to focus on Cloud usage, Extension installation, and Dashboard features.
-   **`EXTENSION_ARCHITECTURE.md`**: Technical documentation for the extension structure.

## 🐛 Bug Fixes & Improvements

### 1. Port Conflict Resolution
-   **`entrypoint.sh`**: Changed default Streamlit port from `8501` to `8000` to match Azure's health check requirements. Moved FastAPI to internal port `8001`.
-   **`dashboard/app.py`**: Updated API connection string to point to `localhost:8001`.

### 2. Data & Models
-   Updated synthetic datasets and re-trained models to ensure consistency.

---

## 💻 Git Commands to Push
Run these commands in your terminal to save everything:

```bash
git add .
git commit -m "feat: Add Browser Extension, Azure Deployment Guides, and fix Port Config"
git push origin main
```
