# Financial Fraud Detection & Risk Analytics

## Overview

This project analyzes a large credit card transaction dataset to identify patterns that may indicate fraudulent or unusual activity. The goal is to practice the full data analytics workflow: loading a large dataset, cleaning messy transaction records, transforming features, preparing data for modeling, and applying anomaly detection techniques to support fraud and risk analysis.

The project is built in Python and focuses on a realistic financial services use case: detecting suspicious transaction behavior from historical credit card activity.

## Business Problem

Financial institutions process millions of transactions every day. Within those transactions, fraudulent activity is usually rare, which makes fraud detection challenging. This project explores how transaction-level data can be cleaned, prepared, and modeled to help identify potentially high-risk activity.

This type of analysis is useful for roles in:

- Fraud analytics
- Risk operations
- Banking technology
- Financial data analysis
- Transaction monitoring
- Data engineering support for financial systems

## Dataset

The notebook uses the IBM credit card transactions dataset stored as a ZIP file:

```text
credit_card_transactions-ibm_v2.zip
```

The dataset contains over 24 million transaction records with fields such as:

- User and card identifiers
- Transaction date and time
- Transaction amount
- Chip, swipe, or online transaction method
- Merchant name, city, state, and ZIP code
- Merchant category code, also known as MCC
- Fraud label

## Tools & Technologies

- Python
- pandas
- NumPy
- matplotlib
- scikit-learn
- Jupyter Notebook

## Project Workflow

### 1. Data Loading

The transaction data is loaded directly from a compressed ZIP file using pandas. This allows the project to work with a large dataset without manually extracting the CSV file first.

### 2. Initial Data Review

The notebook reviews the dataset structure, column types, missing values, duplicates, and sample transaction records. This step helps identify which fields need cleaning before analysis or modeling.

### 3. Data Cleaning

Several cleaning steps are performed, including:

- Filling missing merchant state values with `Online`
- Filling missing ZIP codes with `0000`
- Dropping the `Errors?` column because most values are missing
- Removing dollar signs from the `Amount` field
- Converting transaction amounts to numeric values
- Converting the fraud label into a binary format
- Removing duplicate records

### 4. Feature Engineering

The notebook prepares transaction data for analysis and modeling by creating or transforming features such as:

- Transaction hour and minute from the original time field
- Encoded transaction method from the `Use Chip` column
- Encoded merchant state values
- Merchant city frequency encoding
- Numeric transaction amount
- Binary fraud target variable

### 5. Fraud & Anomaly Detection

The project applies an Isolation Forest model to detect unusual transaction behavior. Isolation Forest is useful for anomaly detection because it identifies records that are easier to separate from normal transaction patterns.

The improved model includes:

- Robust feature scaling
- Hyperparameter tuning across multiple contamination values
- Increased estimator count
- Anomaly score analysis
- ROC-AUC and precision-recall evaluation
- Feature importance analysis using permutation importance

## Key Skills Demonstrated

- Working with large financial datasets
- Data cleaning and preprocessing
- Handling missing values
- Feature engineering for transaction data
- Fraud analytics concepts
- Anomaly detection with machine learning
- Model evaluation and interpretation
- Python-based data analysis workflow

## Why This Project Matters

This project demonstrates how data analytics and machine learning can support fraud detection and financial risk monitoring. It connects technical skills like Python, pandas, and scikit-learn with a real business problem in banking and financial operations.

For a financial institution, a workflow like this could help analysts flag suspicious transactions, prioritize investigations, and better understand risk patterns across customers, merchants, and transaction types.

## How to Run This Project

1. Clone the repository:

```bash
git clone https://github.com/Rodney864/DataProjects.git
```

2. Navigate to the project folder:

```bash
cd DataProjects/FinancialData.ipynb
```

3. Install the required Python libraries:

```bash
pip install pandas numpy matplotlib scikit-learn
```

4. Add the dataset ZIP file to the project folder:

```text
credit_card_transactions-ibm_v2.zip
```

5. Open and run the notebook:

```bash
jupyter notebook FinancialData.ipynb
```

## Future Improvements

Potential next steps for this project include:

- Add SQL queries for transaction aggregation and customer-level analysis
- Build a Power BI or Tableau dashboard for fraud trends
- Add more customer-level risk indicators
- Compare Isolation Forest with other models such as Random Forest, Logistic Regression, or XGBoost
- Create a fraud risk scoring system
- Deploy the workflow as a scheduled batch pipeline
- Store cleaned data in PostgreSQL, AWS RDS, or Amazon Redshift

## Author

**Rodney Smith**

Computer Science graduate focused on data analytics, financial technology, fraud detection, and technical operations.
