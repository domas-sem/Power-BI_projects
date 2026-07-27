# Insurance Fraud Analytics Dashboard

End-to-end data analytics project: Python ETL pipeline → Power BI interactive dashboard, 
analyzing insurance claims to identify fraud patterns and risk factors.

## Overview
This project cleans and transforms a raw insurance claims dataset using Python (pandas), 
then visualizes key fraud and risk indicators in an interactive Power BI dashboard.

## Tools Used
- Python (pandas, numpy) — data cleaning and transformation
- Power BI Desktop — dashboard design, DAX measures, interactive filtering

## Dashboard Preview
![Dashboard](powerbi/dashboard_screenshot.png)

## Key Features
- KPI cards: Total Claims, Fraud Rate %, Avg Claim Amount, High Risk Claims Count
- Fraud rate breakdown by incident type and policy state
- Age vs Claim Amount scatter plot with trend line, segmented by fraud status
- Interactive slicers: Fraud Status, Incident Severity, Policy State

## Data Cleaning Steps (Python)
- Replaced missing value markers ('?') with NaN
- Handled outliers in numeric columns using conditional logic
- Removed duplicate rows and unused columns
- Converted date columns to datetime format
- Encoded target variable (fraud_reported) into binary format
- Created customer tenure groups and high-risk claim flags using custom functions

## Files
- `insurance_data_cleaning.py` — data cleaning and feature engineering script
- `insurance_claims.csv` — raw dataset
- `insurance_claims_sutvarkytas.csv` — cleaned dataset used in Power BI
- `powerbi/Insurance Claims & Fraud Analysis Dashboard.pbix` — Power BI report file
