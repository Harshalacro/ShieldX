import requests
import time
import random
import pandas as pd
from datetime import datetime

API_URL = "http://localhost:8000"

def simulate_traffic():
    print("Starting ShieldX Traffic Simulator...")
    print("Press Ctrl+C to stop.")
    
    # Load data for simulation
    try:
        transactions_df = pd.read_csv("data/transactions.csv")
        urls_df = pd.read_csv("data/urls.csv")
        print(f"Loaded {len(transactions_df)} transactions and {len(urls_df)} URLs.")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    while True:
        # Randomly choose between sending a transaction or checking a URL
        if random.random() < 0.7:
            # --- Send Transaction ---
            row = transactions_df.sample(1).iloc[0]
            
            payload = {
                "amount": float(row['amount']),
                "category": row['category'],
                "distance_from_home": float(row['distance_from_home']),
                "merchant": row['merchant'],
                "region": row['region'],
                "actual_label": int(row['is_fraud']) # Sending ground truth for False Alarm tracking
            }
            
            try:
                response = requests.post(f"{API_URL}/predict", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    status = "🔴 FRAUD" if result['is_fraud'] else "🟢 Clean"
                    action = result.get('action', 'ALLOW')
                    print(f"[TX] {status} (${payload['amount']}) -> Action: {action}")
            except Exception as e:
                print(f"[TX] Error: {e}")
                
        else:
            # --- Check URL ---
            row = urls_df.sample(1).iloc[0]
            
            payload = {
                "url": row['url'],
                "actual_label": int(row['is_phishing'])
            }
            
            try:
                response = requests.post(f"{API_URL}/predict/url", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    status = "🔴 PHISHING" if result['is_phishing'] else "🟢 Safe"
                    action = result.get('action', 'ALLOW')
                    print(f"[URL] {status} ({payload['url'][:30]}...) -> Action: {action}")
            except Exception as e:
                print(f"[URL] Error: {e}")
        
        # Random delay
        time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    simulate_traffic()
