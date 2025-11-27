# 🌍 Real-World Integration Guide: How to use ShieldX on Devices

Currently, ShieldX runs on a **Server** (Cloud/Docker). To use it on a **User's Device** (Phone/Laptop), you need to connect their apps to your ShieldX API.

## The Architecture
**[User's Device]**  --->  **[Internet]**  --->  **[ShieldX API (Cloud)]**

1.  **User** clicks a link or makes a payment.
2.  **App** sends the data to ShieldX API.
3.  **ShieldX** replies: "Safe" or "Fraud".
4.  **App** blocks the action if it's fraud.

---

## 📱 Scenario 1: Integrating with a Payment App (e.g., GPay Clone)
If you are building a mobile wallet, you would add this code **before** processing any payment.

### JavaScript (React Native / Node.js)
```javascript
async function checkFraud(amount, app, receiver_vpa) {
  const response = await fetch('https://your-shieldx-url.com/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'upi',
      amount: amount,
      app: app,
      receiver_vpa: receiver_vpa
    })
  });

  const result = await response.json();
  
  if (result.action === "BLOCK") {
    alert("🚨 Transaction Blocked! Potential Fraud Detected.");
    return false; // Stop transaction
  }
  
  return true; // Proceed
}
```

---

## 🌐 Scenario 2: Browser Extension (Link Scanner)
To protect a user while browsing, you would build a Chrome Extension that checks every link they click.

### JavaScript (Chrome Extension `background.js`)
```javascript
// Listen for link clicks
chrome.webRequest.onBeforeRequest.addListener(
  async function(details) {
    const response = await fetch('https://your-shieldx-url.com/predict/url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: details.url })
    });
    
    const result = await response.json();
    
    if (result.action === "BLOCK_IP") {
      return { cancel: true }; // Block the website loading
    }
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);
```

---

## 🚀 How to Deploy for Real Users
1.  **Deploy ShieldX to Cloud:** Use the [Deployment Guide](DEPLOYMENT.md) to put your API on Render or Google Cloud.
2.  **Get the Public URL:** e.g., `https://shieldx-api.onrender.com`.
3.  **Update Apps:** Replace `localhost:8000` in your mobile app code with the public URL.
