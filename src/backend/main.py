from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Loan Approval Prediction API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the model file
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model_path = os.path.join(current_dir, "models", "loan_model.joblib")

print(f"Loading model from: {model_path}")

# Load the model
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None

class LoanApplication(BaseModel):
    gender: str
    married: str
    dependents: str
    education: str
    self_employed: str
    applicant_income: float
    coapplicant_income: float
    loan_amount: float
    loan_amount_term: float
    credit_history: float
    property_area: str

@app.post("/predict")
async def predict_loan(application: LoanApplication):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Convert input data to model features
        features = [
            1 if application.gender == "Male" else 0,
            1 if application.married == "Yes" else 0,
            float(application.dependents.replace("3+", "4")),
            1 if application.education == "Graduate" else 0,
            1 if application.self_employed == "Yes" else 0,
            application.applicant_income,
            application.coapplicant_income,
            application.loan_amount,
            application.loan_amount_term,
            application.credit_history,
            1 if application.property_area == "Urban" else (2 if application.property_area == "Semiurban" else 0)
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][1]
        
        return {
            "loan_approved": bool(prediction),
            "approval_probability": float(probability)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 