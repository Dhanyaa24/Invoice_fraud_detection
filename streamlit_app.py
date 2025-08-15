import streamlit as st
import pandas as pd
import numpy as np
from invoice_parser import parse_pdf, parse_excel
from utils import load_model_and_artifacts
from features_extraction import extract_invoice_features, FEATURE_COLS

st.set_page_config(page_title='Invoice Fraud Detector', layout='wide')
st.title('Invoice Fraud Detection — Demo')

st.markdown('Upload an invoice (PDF or Excel). The app extracts fields and predicts probability of fraud using a trained model.')

uploaded = st.file_uploader('Upload invoice (PDF or Excel)', type=['pdf','xlsx','xls'])

if st.button('Run demo (sample invoice)'):
    # sample fallback invoice
    sample = {'invoice_no': 'INV-1234', 'vendor': 'Alpha Supplies', 'date': '2025-07-01', 'amount': 5000}
    st.session_state['parsed'] = sample

if uploaded is not None:
    bytes_data = uploaded.read()
    # write to temp file
    with open('temp_uploaded_' + uploaded.name, 'wb') as f:
        f.write(bytes_data)
    path = 'temp_uploaded_' + uploaded.name
    if uploaded.name.lower().endswith('.pdf'):
        parsed = parse_pdf(path)
    else:
        parsed = parse_excel(path)
    st.session_state['parsed'] = parsed

if 'parsed' in st.session_state:
    st.subheader("Parsed Invoice Data")
    st.json(st.session_state['parsed'])

    # Load model and artifacts
    model, scaler, stats = load_model_and_artifacts()

    # Extract features for model input
    features = extract_invoice_features(st.session_state['parsed'], stats)
    X = np.array([features])
    X_scaled = scaler.transform(X)

    # Predict probability
    proba = model.predict_proba(X_scaled)[0, 1]
    
    # More nuanced labeling based on risk levels
    if proba >= 0.7:
        label = "🚨 HIGH RISK - Likely Fraudulent"
        color = "red"
    elif proba >= 0.4:
        label = "⚠️ MEDIUM RISK - Suspicious"
        color = "orange"
    elif proba >= 0.2:
        label = "🟡 LOW RISK - Review Recommended"
        color = "yellow"
    else:
        label = "✅ LOW RISK - Likely Genuine"
        color = "green"

    st.subheader("Fraud Detection Results")
    
    # Create a visual risk indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.metric(label="Fraud Probability", value=f"{proba*100:.2f}%", delta=None)
    
    # Add a progress bar for visual impact
    st.progress(proba)
    
    # Risk level indicator
    risk_text = f"Risk Level: {proba*100:.0f}%"
    if proba >= 0.7:
        st.markdown(f"<div style='background-color: #ffebee; padding: 10px; border-radius: 5px; border-left: 5px solid #f44336;'><h4 style='color: #c62828; margin: 0;'>{risk_text}</h4></div>", unsafe_allow_html=True)
    elif proba >= 0.4:
        st.markdown(f"<div style='background-color: #fff3e0; padding: 10px; border-radius: 5px; border-left: 5px solid #ff9800;'><h4 style='color: #ef6c00; margin: 0;'>{risk_text}</h4></div>", unsafe_allow_html=True)
    elif proba >= 0.2:
        st.markdown(f"<div style='background-color: #fff8e1; padding: 10px; border-radius: 5px; border-left: 5px solid #ffc107;'><h4 style='color: #f57f17; margin: 0;'>{risk_text}</h4></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: #e8f5e8; padding: 10px; border-radius: 5px; border-left: 5px solid #4caf50;'><h4 style='color: #2e7d32; margin: 0;'>{risk_text}</h4></div>", unsafe_allow_html=True)
    
    # Display risk level with appropriate styling
    if color == "red":
        st.error(f"**Risk Level:** {label}")
    elif color == "orange":
        st.warning(f"**Risk Level:** {label}")
    elif color == "yellow":
        st.info(f"**Risk Level:** {label}")
    else:
        st.success(f"**Risk Level:** {label}")
    
    # Add explanation
    if proba >= 0.4:
        st.info("💡 **Recommendation:** This invoice requires further investigation before approval.")
    elif proba >= 0.2:
        st.info("💡 **Recommendation:** Review this invoice carefully before processing.")
    else:
        st.success("💡 **Recommendation:** This invoice appears safe to process.")
    
    # Add risk factor analysis
    st.subheader("🔍 Risk Factor Analysis")
    
    # Analyze the features to explain why this score was given
    risk_factors = []
    if features[1] == 1:  # is_round_amount
        risk_factors.append("• **Round Amount**: Invoice amount is divisible by 100 (suspicious)")
    if features[0] > 5000:  # amount > 5000
        risk_factors.append("• **High Amount**: Invoice amount exceeds $5,000 threshold")
    if abs(features[4]) > 1.0:  # amount_zscore > 1
        risk_factors.append("• **Unusual Amount**: Amount significantly differs from vendor's typical invoices")
    if features[3] < 100:  # vendor_freq < 100
        risk_factors.append("• **New Vendor**: Vendor has limited transaction history")
    
    if risk_factors:
        st.warning("**Key Risk Factors Detected:**")
        for factor in risk_factors:
            st.write(factor)
    else:
        st.success("**No significant risk factors detected.**")

    # Show features used
    with st.expander("Show Extracted Features for Model"):
        feature_df = pd.DataFrame({
            'Feature': FEATURE_COLS,
            'Value': features
        })
        st.dataframe(feature_df)
