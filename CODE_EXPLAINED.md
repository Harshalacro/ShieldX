# 🧠 How ShieldX Was Made: Code Breakdown

This document explains the core Python code used to build ShieldX. You can use this to explain the project to others.

## Step 1: Generating the Data (`src/generate_data.py`)
Before we could train an AI, we needed data. We used the `Faker` library to create realistic synthetic transactions.

```python
# We create fake data for Credit Cards, UPI, and Crypto
def generate_credit_card_data(num=5000):
    data = []
    for _ in range(num):
        # 3% chance of a transaction being fraud
        is_fraud = 1 if random.random() < 0.03 else 0
        
        data.append({
            'amount': round(random.uniform(10, 5000), 2),
            'category': random.choice(['grocery', 'travel', 'electronics']),
            'is_fraud': is_fraud
        })
    return pd.DataFrame(data)
```
*   **Logic:** We simulate thousands of transactions, randomly marking some as "fraud" to teach the model what bad patterns look like.

## Step 2: Training the AI (`src/train_model.py`)
We used **Random Forest**, a powerful machine learning algorithm, to "teach" the system.

```python
def train_model(name, csv_path, features):
    # 1. Load the data
    df = pd.read_csv(csv_path)
    
    # 2. Split into Input (X) and Target (y)
    X = df[features] # e.g., Amount, Category
    y = df['is_fraud'] # 0 or 1
    
    # 3. Train the Random Forest Model
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X, y)
    
    # 4. Save the "Brain" (.joblib file)
    joblib.dump(model, f"models/{name}_model.joblib")
```
*   **Logic:** The model looks at the features (Amount, Category) and learns to predict the target (Fraud/Safe).

## Step 3: The Brain / API (`src/api.py`)
We built a **FastAPI** server to make real-time predictions. This is the engine of the system.

```python
@app.post("/predict")
def predict(tx: Transaction):
    # 1. Load the correct model (Credit, UPI, or Crypto)
    model = models.get(tx.type)
    
    # 2. Ask the model for a prediction
    probability = model.predict_proba([tx.features])[0][1]
    
    # 3. Decide Action
    action = "BLOCK" if probability > 0.8 else "ALLOW"
    
    return {"is_fraud": probability > 0.5, "action": action}
```
*   **Logic:** When a new transaction comes in, the API sends it to the trained model, gets a probability score, and decides whether to Block or Allow it.

## Step 4: The Dashboard (`dashboard/app.py`)
We used **Streamlit** to create the user interface.

```python
# Display the Data Table
st.dataframe(
    df.style.apply(lambda x: ['background-color: #5a1a1a' if x['is_fraud'] == 1 else '' for i in x], axis=1)
)

# Manual Simulator Form
with st.form("simulation"):
    amount = st.number_input("Amount")
    if st.form_submit_button("Analyze"):
        # Send data to our API
        response = requests.post("http://localhost:8000/predict", json={...})
        st.write(response.json())
```
*   **Logic:** The dashboard talks to the API to get predictions and uses simple Python code to draw charts and tables.
