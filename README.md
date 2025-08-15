Invoice Fraud Detection System

An AI-powered tool to detect fraudulent invoices by analyzing vendor details, invoice amounts, dates, and other patterns.
Built with Python, Random Forest Classifier, and an interactive Streamlit web app.

Features

1.Upload invoices in PDF or Excel format.
2.Automatic invoice parsing (vendor, amount, date, etc.).
3.Feature extraction for fraud detection (e.g., round amounts, unusual vendor activity).
4.Machine learning model (Random Forest) trained on synthetic invoice data.
5.raud probability score with risk levels (Low / Medium / High).
6.Explainable results — see why an invoice was flagged.

Tech Stack

1.Python
2.Streamlit – web interface
3.scikit-learn – machine learning
4.pdfplumber – PDF parsing
5.openpyxl – Excel parsing

ReportLab – sample invoice generation

Installation
# 1. Clone the repository
git clone https://github.com/Dhanyaa24/Invoice_fraud_detection.git
cd Invoice_fraud_detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train the model (optional, model.pkl already provided)
python model_train.py

# 4. Run the Streamlit app
streamlit run streamlit_app.py

Project Structure
Invoice_fraud_detection/
│
├── create_pdf_invoice.py      # Generates sample invoices
├── features_extraction.py     # Extracts ML features from invoice data
├── invoice_parser.py           # Parses invoice details
├── model_train.py              # Trains and saves the ML model
├── sample_invoices.py          # Creates example invoices
├── streamlit_app.py            # Streamlit front-end app
├── utils.py                    # Helper functions
├── requirements.txt
└── data/
    ├── synthetic_invoices.csv  # Generated training data
    └── model_artifacts/        # Saved model & scaler

How It Works

Invoice Parsing – Extract vendor, date, amount, and metadata.

Feature Extraction – Create numerical features from invoice patterns.

Model Prediction – Random Forest Classifier predicts fraud probability.

Result Display – Streamlit app shows fraud score and explanation.

License

This project is open-source under the MIT License.
