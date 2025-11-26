import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

def generate_url_dataset(num_urls=5000):
    print(f"Generating {num_urls} URLs...")
    data = []
    
    suspicious_keywords = ['login', 'verify', 'account', 'update', 'secure', 'banking', 'confirm']
    safe_domains = ['google.com', 'amazon.com', 'wikipedia.org', 'github.com', 'stackoverflow.com', 'example.com']
    tlds = ['.com', '.org', '.net', '.io', '.co']
    
    for _ in range(num_urls):
        is_phishing = 0
        url = ""
        
        if random.random() < 0.2: # 20% phishing
            is_phishing = 1
            # Phishing patterns
            if random.random() < 0.5:
                # IP address URL
                url = f"http://{fake.ipv4()}/{random.choice(suspicious_keywords)}"
            else:
                # Typosquatting or long random subdomains
                domain = random.choice(safe_domains).replace('.', '-')
                url = f"http://{fake.word()}-{domain}{random.choice(tlds)}/{random.choice(suspicious_keywords)}"
        else:
            # Safe URL
            url = f"https://www.{random.choice(safe_domains)}/{fake.uri_path()}"
            
        data.append({'url': url, 'is_phishing': is_phishing})
        
    return pd.DataFrame(data)

def generate_credit_card_data(num=5000):
    print(f"Generating {num} Credit Card transactions...")
    data = []
    for _ in range(num):
        is_fraud = 0
        amount = round(random.uniform(10, 5000), 2)
        if random.random() < 0.03: is_fraud = 1
        
        data.append({
            'timestamp': fake.date_time_this_year().isoformat(),
            'amount': amount,
            'merchant': fake.company(),
            'category': random.choice(['grocery', 'travel', 'electronics', 'dining']),
            'card_type': random.choice(['Visa', 'MasterCard', 'Amex']),
            'is_fraud': is_fraud
        })
    return pd.DataFrame(data)

def generate_upi_data(num=5000):
    print(f"Generating {num} UPI transactions...")
    data = []
    for _ in range(num):
        is_fraud = 0
        amount = round(random.uniform(1, 1000), 2)
        if random.random() < 0.05: is_fraud = 1
        
        data.append({
            'timestamp': fake.date_time_this_year().isoformat(),
            'amount': amount,
            'app': random.choice(['GPay', 'PhonePe', 'Paytm']),
            'receiver_vpa': fake.email(), # Simulating VPA
            'is_fraud': is_fraud
        })
    return pd.DataFrame(data)

def generate_crypto_data(num=5000):
    print(f"Generating {num} Crypto transactions...")
    data = []
    for _ in range(num):
        is_fraud = 0
        amount = round(random.uniform(0.001, 2.0), 4) # BTC/ETH amounts
        if random.random() < 0.1: is_fraud = 1 # Higher fraud in crypto
        
        data.append({
            'timestamp': fake.date_time_this_year().isoformat(),
            'amount': amount,
            'currency': random.choice(['BTC', 'ETH', 'SOL']),
            'wallet_address': fake.sha256()[:30],
            'is_fraud': is_fraud
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate and Save Datasets
    cc_df = generate_credit_card_data()
    cc_df.to_csv("data/credit_card.csv", index=False)
    print("Saved data/credit_card.csv")
    
    upi_df = generate_upi_data()
    upi_df.to_csv("data/upi.csv", index=False)
    print("Saved data/upi.csv")
    
    crypto_df = generate_crypto_data()
    crypto_df.to_csv("data/crypto.csv", index=False)
    print("Saved data/crypto.csv")
    
    # Keep URL data for Link Scanner
    url_df = generate_url_dataset(2000)
    url_df.to_csv("data/urls.csv", index=False)
    print("Saved data/urls.csv")
