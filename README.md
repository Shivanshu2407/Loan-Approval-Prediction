# Loan Approval Prediction Web Application

This web application provides an interface for predicting loan approval using machine learning. It consists of a FastAPI backend and a Streamlit frontend.

## Project Structure
```
├── models/
│   └── loan_model.joblib    # Your trained model file
├── src/
│   ├── backend/
│   │   └── main.py         # FastAPI backend
│   └── frontend/
│       └── app.py          # Streamlit frontend
├── requirements.txt
└── README.md
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

3. Export your trained model as 'loan_model.joblib' and place it in the models/ directory.

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

## Using the Application

1. Open your web browser and navigate to http://localhost:8501
2. Fill in the loan application form with the required information
3. Click "Predict Loan Approval" to see the prediction result

## API Documentation

The FastAPI backend provides automatic API documentation. You can access it at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 