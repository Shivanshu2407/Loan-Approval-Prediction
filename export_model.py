import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib

# Get absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data", "LoanApprovalPrediction.csv")
model_path = os.path.join(current_dir, "models", "loan_model.joblib")

print(f"Loading data from: {data_path}")
print(f"Model will be saved to: {model_path}")

try:
    # Load and preprocess the data
    data = pd.read_csv(data_path)

    # Handle missing values
    for col in ['Gender', 'Married', 'Dependents', 'Self_Employed', 'Loan_Amount_Term', 'Credit_History']:
        data[col] = data[col].fillna(data[col].mode()[0])
    data['LoanAmount'] = data['LoanAmount'].fillna(data['LoanAmount'].mean())

    # Convert categorical variables
    data['Dependents'] = data['Dependents'].replace('3+', '4')
    data['Dependents'] = data['Dependents'].astype(float)

    # Create feature matrix X and target variable y
    X = pd.DataFrame({
        'Gender': (data['Gender'] == 'Male').astype(int),
        'Married': (data['Married'] == 'Yes').astype(int),
        'Dependents': data['Dependents'],
        'Education': (data['Education'] == 'Graduate').astype(int),
        'Self_Employed': (data['Self_Employed'] == 'Yes').astype(int),
        'ApplicantIncome': data['ApplicantIncome'],
        'CoapplicantIncome': data['CoapplicantIncome'],
        'LoanAmount': data['LoanAmount'],
        'Loan_Amount_Term': data['Loan_Amount_Term'],
        'Credit_History': data['Credit_History'],
        'Property_Area': data['Property_Area'].map({'Rural': 0, 'Semiurban': 2, 'Urban': 1})
    })

    y = (data['Loan_Status'] == 'Y').astype(int)

    # Train the model
    print("Training the model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the model
    print("Saving the model...")
    joblib.dump(model, model_path)
    print(f"Model has been successfully exported to: {model_path}")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    raise 