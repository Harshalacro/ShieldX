# 🛡️ ShieldX User Manual

Welcome to **ShieldX**, your real-time AI security platform. This guide will help you use the deployed application and the browser extension.

---

## 🌐 1. Accessing the Web Dashboard
Your application is now live on the cloud!

*   **URL:** `http://shieldx-final-app.azurewebsites.net`
    *(Note: If you used a different name during deployment, replace `shieldx-final-app` with your unique name)*

### Dashboard Features
*   **Credit Card / UPI / Crypto Tabs:** View historical data and fraud patterns.
*   **Link Scanner:** Manually check if a URL is safe.
*   **Manual Simulator:** Test the AI by creating fake transactions to see if they get caught.

---

## 🧩 2. Installing the Browser Extension
ShieldX comes with a Chrome/Edge extension that automatically scans websites you visit.

### Step A: Load the Extension
1.  Open **Google Chrome** or **Microsoft Edge**.
2.  Go to the Extensions page:
    *   **Chrome:** `chrome://extensions`
    *   **Edge:** `edge://extensions`
3.  Enable **Developer Mode** (toggle switch in the top right corner).
4.  Click **"Load unpacked"**.
5.  Select the `extension` folder inside your project directory:
    *   Path: `.../ShieldX/extension`

### Step B: Connect to Azure
1.  Click the **ShieldX Icon** 🛡️ in your browser toolbar.
2.  Click the **Settings (⚙️)** icon in the popup.
3.  **API URL:** Enter your Azure URL + `/predict`.
    *   Example: `https://shieldx-final-app.azurewebsites.net/predict`
    *   *(Make sure to use `https://` and add `/predict` at the end)*
4.  Click **Save**.

---

## 🕵️‍♂️ 3. Using the Extension
Once installed and connected, the extension works in two modes:

### Manual Scan
1.  Visit any website.
2.  Click the **ShieldX Icon**.
3.  Click **"Scan Current Page"**.
4.  The AI will analyze the URL and tell you if it is **SAFE** or **PHISHING**.

### Auto-Scan (Real-time Protection)
1.  Open the extension popup.
2.  Toggle **"Auto-Scan"** to ON.
3.  Now, whenever you visit a new page, ShieldX will silently scan it in the background.
4.  If a threat is detected, you will get a **Browser Notification** warning you immediately!

---

## ❓ Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"Failed to fetch" in Extension** | Check your API URL in Settings. It must end with `/predict`. Ensure the Azure app is running. |
| **Extension Icon missing** | Reload the extension in `chrome://extensions`. |
| **Azure App "Application Error"** | The app might be sleeping. Refresh the page and wait 1-2 minutes. |
