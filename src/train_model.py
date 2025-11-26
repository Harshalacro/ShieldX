import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_specific_model(name, csv_path, features):
    print(f"Training {name} model...")
    df = pd.read_csv(csv_path)
    
    X = df[features]
    y = df['is_fraud']
    
    # Simple preprocessing: One-Hot Encode categorical features
    X = pd.get_dummies(X)
    
    # Align columns (in production, we'd use a pipeline with OneHotEncoder, but this is quick)
    # For simplicity in this demo, we'll just use 'amount' for the generic logic if OneHot fails on new data
    # But let's try to be a bit robust.
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, f"models/{name}_model.joblib")
    print(f"Saved models/{name}_model.joblib")

if __name__ == "__main__":
    # Credit Card
    train_specific_model("credit", "data/credit_card.csv", ['amount', 'category', 'card_type'])
    
    # UPI
    train_specific_model("upi", "data/upi.csv", ['amount', 'app'])
    
    # Crypto
    train_specific_model("crypto", "data/crypto.csv", ['amount', 'currency'])
    
    print("All models trained.")
