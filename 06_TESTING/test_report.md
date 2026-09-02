# Testing & Validation Report

## 1. Testing Objective

The purpose of testing is to verify that the complete
Data Engineering pipeline works correctly and that
data remains consistent from ETL to Power BI.

Pipeline:

Raw Data → ETL → SQLite → SQL → EDA → Power BI


## 2. ETL Validation

- Raw OASST1 data successfully processed.
- Processed dataset contains 88,838 message records.
- Final processed dataset contains 18 fields.
- Data transformation completed successfully.

Status: PASS


## 3. Database Validation

SQLite database: oasst.db

- Messages: 88,838
- Conversations: 10,364
- Users: 13,249
- Languages: 25

Status: PASS


## 4. Data Integrity Validation

- Duplicate message IDs: 0
- Orphan parent IDs: 0
- Empty text records: 0
- Missing message IDs: 0
- Missing language: 0
- Missing role: 0
- Missing review count: 0

Status: PASS


## 5. SQL Validation

16 analytical SQL queries were executed successfully.

Major verified results:

- Total messages: 88,838
- Total conversations: 10,364
- Total users: 13,249
- Total languages: 25
- Average messages per conversation: 8.57

Status: PASS


## 6. EDA Validation

Python EDA was completed successfully.

The EDA results were cross-checked with SQL results.

Major verified results:

- Assistant messages: 55,668
- Prompter messages: 33,170
- English messages: 41,305
- Spanish messages: 23,975
- February 2023 messages: 60,932
- Deleted messages: 1,553

Status: PASS


## 7. Power BI Validation

Power BI dashboard was created using the validated data.

Dashboard checks:

- KPI values verified
- Charts verified
- Slicers verified
- Insights verified
- Business interpretation verified
- Recommendations verified
- Management actions verified

Status: PASS


## 8. SQL – EDA – Power BI Reconciliation

The major numerical results were cross-checked across:

SQL → Python EDA → Power BI

The values are consistent.

Status: PASS


## 9. Final QA Result

| Area | Status |
|------|--------|
| ETL | PASS |
| Database | PASS |
| Data Integrity | PASS |
| SQL Analysis | PASS |
| Python EDA | PASS |
| Power BI | PASS |
| Cross-validation | PASS |

## Overall Project QA: PASS