import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="💰",
    layout="centered"
)

st.title("Loan Approval Prediction")
st.write("Enter your information below to check loan approval probability")

with st.form("loan_prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Married", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])
        self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    
    with col2:
        applicant_income = st.number_input("Applicant Income", min_value=0)
        coapplicant_income = st.number_input("Co-applicant Income", min_value=0)
        loan_amount = st.number_input("Loan Amount", min_value=0)
        loan_amount_term = st.number_input("Loan Amount Term (in months)", min_value=0)
        credit_history = st.selectbox("Credit History", [0, 1], help="0 = No credit history, 1 = Has credit history")
        property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    submitted = st.form_submit_button("Predict Loan Approval")

if submitted:
    data = {
        "gender": gender,
        "married": married,
        "dependents": dependents,
        "education": education,
        "self_employed": self_employed,
        "applicant_income": applicant_income,
        "coapplicant_income": coapplicant_income,
        "loan_amount": loan_amount,
        "loan_amount_term": loan_amount_term,
        "credit_history": float(credit_history),
        "property_area": property_area
    }

    try:
        response = requests.post("http://localhost:8000/predict", json=data)
        if response.status_code == 200:
            result = response.json()
            
            st.write("---")
            if result["loan_approved"]:
                st.success("🎉 Congratulations! Your loan is likely to be approved!")
            else:
                st.error("😔 Sorry, your loan is likely to be rejected.")
            
            probability = result["approval_probability"] * 100
            st.write(f"Approval Probability: {probability:.2f}%")
            
            # Progress bar for visualization
            st.progress(result["approval_probability"])
            
        else:
            st.error(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction service. Please make sure the backend server is running.") 