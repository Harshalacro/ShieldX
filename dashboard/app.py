import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ShieldX Dashboard", layout="wide", page_icon="🛡️")

st.title("🛡️ ShieldX - Multi-Domain Fraud Detection")

# Load Datasets
@st.cache_data
def load_data():
    return {
        'credit': pd.read_csv("data/credit_card.csv"),
        'upi': pd.read_csv("data/upi.csv"),
        'crypto': pd.read_csv("data/crypto.csv"),
        'urls': pd.read_csv("data/urls.csv")
    }

data = load_data()

# Custom CSS for Premium Look & Better Contrast
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Tables */
    .stDataFrame {
        border: 1px solid #30333F;
        border-radius: 5px;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #00CC96; /* Green for numbers */
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E2130;
        border-radius: 5px;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4C4CFF !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💳 Credit Card", "📱 UPI", "₿ Crypto", "🔗 Link Scanner", "🕹️ Manual Simulator"])

def show_dataset(df, name):
    st.subheader(f"{name} Transactions")
    
    # Metrics
    total = len(df)
    fraud = df[df['is_fraud'] == 1].shape[0]
    rate = (fraud/total) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("Fraud Detected", fraud)
    col3.metric("Fraud Rate", f"{rate:.2f}%")
    
    # Highlight Fraud: Dark Red background with White text for better contrast in Dark Mode
    st.dataframe(
        df.style.apply(lambda x: ['background-color: #5a1a1a; color: #ffcccc' if x['is_fraud'] == 1 else '' for i in x], axis=1),
        use_container_width=True,
        height=600
    )

with tab1:
    show_dataset(data['credit'], "Credit Card")

with tab2:
    show_dataset(data['upi'], "UPI")

with tab3:
    show_dataset(data['crypto'], "Crypto")

with tab4:
    st.subheader("Malicious URL Database")
    df_url = data['urls']
    st.dataframe(
        df_url.style.apply(lambda x: ['background-color: #5a1a1a; color: #ffcccc' if x['is_phishing'] == 1 else '' for i in x], axis=1),
        use_container_width=True
    )

with tab5:
    st.subheader("Interactive Simulator")
    st.info("Test the models with custom inputs.")
    
    type_ = st.selectbox("Transaction Type", ["credit", "upi", "crypto"])
    amount = st.number_input("Amount", value=100.0)
    
    payload = {"type": type_, "amount": amount}
    
    if type_ == "credit":
        payload['category'] = st.selectbox("Category", ['grocery', 'travel', 'electronics', 'dining'])
        payload['card_type'] = st.selectbox("Card Type", ['Visa', 'MasterCard', 'Amex'])
    elif type_ == "upi":
        payload['app'] = st.selectbox("App", ['GPay', 'PhonePe', 'Paytm'])
    elif type_ == "crypto":
        payload['currency'] = st.selectbox("Currency", ['BTC', 'ETH', 'SOL'])
        
    if st.button("Predict"):
        try:
            res = requests.post("http://localhost:8000/predict", json=payload)
            if res.status_code == 200:
                result = res.json()
                if result['is_fraud']:
                    st.error(f"FRAUD DETECTED! ({result['fraud_probability']:.2f})")
                else:
                    st.success(f"SAFE ({result['fraud_probability']:.2f})")
        except:
            st.error("API Error")
