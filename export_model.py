import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_auc_score
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

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    print("\nTraining the model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions on test set
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate performance metrics
    print("\nModel Performance Metrics:")
    print("-" * 50)
    print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision Score: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall Score: {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred):.4f}")
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

    # Cross-validation scores
    cv_scores = cross_val_score(model, X, y, cv=5)
    print(f"\n5-Fold Cross-Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

    # Print confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print("-" * 50)
    print("                  Predicted Negative  Predicted Positive")
    print(f"Actual Negative       {conf_matrix[0][0]}                {conf_matrix[0][1]}")
    print(f"Actual Positive       {conf_matrix[1][0]}                {conf_matrix[1][1]}")

    # Print classification report
    print("\nClassification Report:")
    print("-" * 50)
    print(classification_report(y_test, y_pred))

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance:")
    print("-" * 50)
    for idx, row in feature_importance.iterrows():
        print(f"{row['feature']}: {row['importance']:.4f}")

    # Create models directory if it doesn't exist
    os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Save the model
    print("\nSaving the model...")
    joblib.dump(model, model_path)
    print(f"Model has been successfully exported to: {model_path}")

except Exception as e:
    print(f"Error occurred: {str(e)}")
    raise 