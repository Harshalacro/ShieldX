document.addEventListener('DOMContentLoaded', async () => {
    const scanBtn = document.getElementById('scanBtn');
    const resultBox = document.getElementById('result');
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsPanel = document.getElementById('settingsPanel');
    const saveBtn = document.getElementById('saveBtn');
    const apiUrlInput = document.getElementById('apiUrl');
    const autoScanToggle = document.getElementById('autoScanToggle');

    // Load settings
    const data = await chrome.storage.sync.get(['apiUrl', 'autoScan']);
    if (data.apiUrl) apiUrlInput.value = data.apiUrl;
    if (data.autoScan) autoScanToggle.checked = data.autoScan;

    // Toggle Settings Panel
    settingsBtn.addEventListener('click', () => {
        settingsPanel.style.display = settingsPanel.style.display === 'flex' ? 'none' : 'flex';
    });

    // Save Settings
    saveBtn.addEventListener('click', () => {
        const url = apiUrlInput.value.trim();
        if (url) {
            chrome.storage.sync.set({ apiUrl: url }, () => {
                alert('Settings saved!');
                settingsPanel.style.display = 'none';
            });
        }
    });

    // Toggle Auto-Scan
    autoScanToggle.addEventListener('change', (e) => {
        chrome.storage.sync.set({ autoScan: e.target.checked });
    });

    // Scan Button Logic
    scanBtn.addEventListener('click', async () => {
        const { apiUrl } = await chrome.storage.sync.get('apiUrl');
        if (!apiUrl) {
            showResult('Please set API URL in Settings', 'danger');
            return;
        }

        let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        if (!tab) return;

        showResult('Scanning...', '');

        try {
            const response = await fetch(`${apiUrl}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ type: "url", data: tab.url })
            });

            const result = await response.json();

            // Assuming API returns { prediction: "Phishing" | "Safe" }
            const isSafe = result.prediction.toLowerCase() === 'safe';
            showResult(result.prediction, isSafe ? 'safe' : 'danger');

        } catch (error) {
            console.error(error);
            showResult('Error connecting to server', 'danger');
        }
    });

    function showResult(text, className) {
        resultBox.style.display = 'flex';
        resultBox.innerText = text;
        resultBox.className = 'result-box'; // Reset
        if (className) resultBox.classList.add(className);
    }
});
