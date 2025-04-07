# Loan Approval Prediction Web Application

This web application provides an interface for predicting loan approval using machine learning. It consists of a FastAPI backend and a Streamlit frontend.

## Project Structure
```
project_root/
├── data/
│   └── LoanApprovalPrediction.csv    # Dataset file (36KB)
├── models/
│   └── loan_model.joblib             # Trained ML model
├── notebooks/
│   └── Loan_approval_Prediction.ipynb # Original model development notebook
├── powerbi_dashboard/                 # PowerBI dashboard files
├── visuals/                          # Project visualizations
├── src/
│   ├── backend/
│   │   └── main.py                   # FastAPI backend server
│   └── frontend/
│       └── app.py                    # Streamlit frontend application
├── export_model.py                    # Script to train and export model
├── requirements.txt                   # Project dependencies
└── README.md                         # Project documentation
```

## Setup Instructions

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Export your trained model:
```bash
python export_model.py
```

## Running the Application

1. Start the FastAPI backend:
```bash
cd src/backend
uvicorn main:app --reload
```
The backend will be available at http://localhost:8000

2. In a new terminal, start the Streamlit frontend:
```bash
cd src/frontend
streamlit run app.py
```
The frontend will be available at http://localhost:8501

## Dependencies
- fastapi>=0.104.1
- uvicorn>=0.24.0
- streamlit>=1.29.0
- pandas>=2.1.4
- scikit-learn>=1.3.2
- numpy>=1.26.2
- python-multipart>=0.0.6
- pydantic>=2.5.2
- joblib>=1.3.2

## Features
- User-friendly web interface
- Real-time loan approval prediction
- Probability score for loan approval
- Comprehensive input validation
- Detailed prediction results
- Visual probability indicator

## Input Parameters
1. Personal Information:
   - Gender (Male/Female)
   - Marital Status (Yes/No)
   - Number of Dependents (0, 1, 2, 3+)
   - Education (Graduate/Not Graduate)
   - Self Employed (Yes/No)

2. Financial Information:
   - Applicant Monthly Income
   - Co-applicant Monthly Income
   - Loan Amount (in thousands)
   - Loan Term (in months)
   - Credit History (0/1)
   - Property Area (Urban/Semiurban/Rural)

## API Documentation
The FastAPI backend provides automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Additional Resources
- Original dataset in `data/` directory
- Model development notebook in `notebooks/` directory
- PowerBI dashboard in `powerbi_dashboard/` directory
- Project visualizations in `visuals/` directory 