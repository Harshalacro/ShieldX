# 🛡️ ShieldX - AI Security Platform

ShieldX is a real-time, multi-domain fraud detection system powered by AI. It detects fraudulent transactions across **Credit Cards**, **UPI**, and **Crypto**, and identifies malicious **Phishing URLs**.

![ShieldX Dashboard](https://via.placeholder.com/800x400?text=ShieldX+Dashboard+Preview)

## 🚀 Features

*   **Multi-Domain Fraud Detection:**
    *   💳 **Credit Card:** Detects anomalies in amount, category, and card usage.
    *   📱 **UPI:** Flags suspicious digital payment patterns.
    *   ₿ **Crypto:** Monitors wallet addresses for high-risk activity.
*   **🔗 Link Scanner:** Real-time detection of malicious/phishing URLs.
*   **🕹️ Manual Simulator:** Interactive UI to manually test transactions and URLs against the AI models.
*   **☁️ Cloud-Ready:** Dockerized for easy deployment to Google Cloud Run, Render, or any VPS.
*   **📊 Interactive Dashboard:** Built with Streamlit for real-time visualization and static data analysis.

## 🛠️ Tech Stack

*   **Frontend:** Streamlit (Python)
*   **Backend:** FastAPI
*   **AI/ML:** Scikit-Learn (Random Forest), Pandas, NumPy
*   **Deployment:** Docker, Docker Compose

## 🏃‍♂️ How to Run

### Option 1: Using Docker (Recommended)
The easiest way to run ShieldX is using Docker.

1.  **Build the Image:**
    ```bash
    docker build -t shieldx .
    ```
2.  **Run the Container:**
    ```bash
    docker run -p 8501:8501 -p 8000:8000 shieldx
    ```
3.  **Access the Dashboard:**
    Open [http://localhost:8501](http://localhost:8501) in your browser.

### Option 2: Local Python Setup
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Start the API:**
    ```bash
    python src/api.py
    ```
3.  **Start the Dashboard:**
    ```bash
    streamlit run dashboard/app.py
    ```

## 📂 Project Structure

```
ShieldX/
├── dashboard/          # Streamlit Dashboard code
├── data/               # Synthetic datasets (Credit, UPI, Crypto, URLs)
├── models/             # Trained AI models (.joblib)
├── src/                # Source code
│   ├── api.py          # FastAPI backend
│   ├── generate_data.py# Data generation script
│   ├── train_model.py  # Model training script
│   └── simulate_traffic.py
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── entrypoint.sh       # Startup script for single-container deploy
└── requirements.txt    # Python dependencies
```

## ☁️ Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Google Cloud Run, Render, and Railway.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## 📜 License

MIT License
