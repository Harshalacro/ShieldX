chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url && tab.url.startsWith('http')) {

        const { apiUrl, autoScan } = await chrome.storage.sync.get(['apiUrl', 'autoScan']);

        if (autoScan && apiUrl) {
            try {
                const response = await fetch(`${apiUrl}/predict`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: "url", data: tab.url })
                });

                const result = await response.json();

                // If Phishing/Fraud detected, alert the user
                if (result.prediction && result.prediction.toLowerCase() !== 'safe') {
                    chrome.notifications.create({
                        type: 'basic',
                        iconUrl: 'icons/icon128.png',
                        title: '⚠️ Security Alert',
                        message: `ShieldX detected potential threat: ${result.prediction}`,
                        priority: 2
                    });
                }

            } catch (error) {
                console.error("ShieldX Auto-Scan Error:", error);
            }
        }
    }
});
