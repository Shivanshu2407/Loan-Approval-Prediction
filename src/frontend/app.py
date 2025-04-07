import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Loan Approval Prediction",
    page_icon="💰",
    layout="centered"
)

# Add custom CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

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
        credit_history = st.selectbox("Credit History", [1, 0], 
                                    help="1: Has credit history, 0: No credit history")
    
    with col2:
        applicant_income = st.number_input("Applicant Monthly Income", min_value=0)
        coapplicant_income = st.number_input("Co-applicant Monthly Income", min_value=0)
        loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0)
        loan_amount_term = st.number_input("Loan Term (in months)", min_value=0, value=360)
        property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    submitted = st.form_submit_button("Predict Loan Approval")

if submitted:
    data = {
        "gender": gender,
        "married": married,
        "dependents": dependents,
        "education": education,
        "self_employed": self_employed,
        "applicant_income": float(applicant_income),
        "coapplicant_income": float(coapplicant_income),
        "loan_amount": float(loan_amount),
        "loan_amount_term": float(loan_amount_term),
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
            
            # Additional information
            st.info("""
            **Note:** This prediction is based on historical data and should be used as a reference only. 
            The final decision may depend on additional factors and the lending institution's policies.
            """)
            
        else:
            st.error(f"Error: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the prediction service. Please make sure the backend server is running.") 