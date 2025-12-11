document.addEventListener('DOMContentLoaded', function () {
    const scanBtn = document.getElementById('scan-btn');
    const resultArea = document.getElementById('result-area');
    const statusIcon = resultArea.querySelector('.status-icon');
    const statusText = resultArea.querySelector('.status-text');
    const scoreText = document.getElementById('score-text');
    const errorMsg = document.getElementById('error-msg');
    const currentUrlDisplay = document.getElementById('current-url');

    // get current api url - hardcoded for now, but could be dynamic
    const API_URL = "https://shieldx-1.onrender.com/predict/url";

    scanBtn.addEventListener('click', async () => {
        // UI Reset
        scanBtn.disabled = true;
        scanBtn.textContent = "Analyzing...";
        errorMsg.style.display = 'none';
        resultArea.className = 'status-box'; // reset classes
        statusIcon.textContent = '⏳';
        statusText.textContent = "Checking AI Models...";
        scoreText.textContent = "";

        try {
            // 1. Get current tab URL
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            if (!tab || !tab.url) {
                throw new Error("Cannot access tab URL.");
            }

            const urlToCheck = tab.url;
            currentUrlDisplay.textContent = urlToCheck;
            // currentUrlDisplay.style.display = 'block';

            // 2. Call ShieldX API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: urlToCheck })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const data = await response.json();

            // 3. Update UI based on result
            // API returns: { "is_phishing": bool, "probability": float, "action": str }

            const probPercent = (data.probability * 100).toFixed(1);

            if (data.is_phishing) {
                resultArea.classList.add('phishing');
                statusIcon.textContent = '⛔';
                statusText.textContent = "PHISHING DETECTED!";
                scoreText.textContent = `Confidence: ${probPercent}% (Risk High)`;
            } else if (data.probability > 0.4) {
                resultArea.classList.add('suspicious');
                statusIcon.textContent = '⚠️';
                statusText.textContent = "Suspicious";
                scoreText.textContent = `Risk Score: ${probPercent}% (Be Careful)`;
            } else {
                resultArea.classList.add('safe');
                statusIcon.textContent = '✅';
                statusText.textContent = "Safe Website";
                scoreText.textContent = `Safety Score: ${(100 - probPercent).toFixed(1)}%`;
            }

        } catch (error) {
            console.error(error);
            errorMsg.textContent = error.message;
            errorMsg.style.display = 'block';
            statusIcon.textContent = '❌';
            statusText.textContent = "Error";
        } finally {
            scanBtn.disabled = false;
            scanBtn.textContent = "Scan Page";
        }
    });
});
