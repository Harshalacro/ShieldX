import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

def train_url_model():
    print("Loading URL data...")
    df = pd.read_csv("data/urls.csv")
    
    X = df['url']
    y = df['is_phishing']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training URL detection model...")
    # Create pipeline: TF-IDF -> Random Forest
    # We use character-level n-grams to catch patterns like 'paypal' inside 'paypal-secure'
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=5000)),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    # Save model
    output_path = "models/url_detection_model.joblib"
    joblib.dump(pipeline, output_path)
    print(f"Saved model to {output_path}")

if __name__ == "__main__":
    train_url_model()
