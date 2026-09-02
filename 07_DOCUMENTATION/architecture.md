# System Architecture

## End-to-End Data Engineering Pipeline

Kaggle OASST1 Dataset
        ↓
01_DATA/raw
        ↓
ingest.py
        ↓
Extract
        ↓
transform.py
        ↓
Clean + Standardize + Validate
        ↓
01_DATA/processed
        ↓
load.py
        ↓
SQLite Database
        ↓
03_DATABASE/oasst.db
        ↓
SQL Analysis
        ↓
Python EDA
        ↓
Power BI
        ↓
Business Insights
        ↓
Recommendations

## Tools

| Tool | Purpose |
|---|---|
| Kaggle | Dataset source |
| Python | ETL and EDA |
| Pandas | Data transformation |
| SQLite | Structured database |
| SQL | Business analysis |
| Jupyter | Exploratory analysis |
| Power BI | Interactive dashboard |
| GitHub | Version control |
| VS Code | Development |

## ETL Architecture

Raw Data
   ↓
Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
   ↓
SQLite

The master pipeline.py orchestrates:
ingest.py → transform.py → load.py

## Analytical Layer

SQLite
   ↓
SQL Queries
   ↓
Python EDA
   ↓
Power BI
   ↓
Insights & Recommendations