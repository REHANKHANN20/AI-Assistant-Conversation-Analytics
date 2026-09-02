AI Assistant Conversation Analytics — End-to-End Data Engineering Pipeline

📌 Project Overview

This project develops an end-to-end Data Engineering and Business Intelligence pipeline for analyzing AI assistant conversations using the OpenAssistant Conversations Dataset (OASST1).

The project transforms raw conversation data into a structured SQLite database, performs SQL analysis and Python-based Exploratory Data Analysis (EDA), and presents the results through an interactive Power BI dashboard.

One-Line Project Definition

Raw AI Assistant Conversation Data → ETL → SQLite → SQL Analysis → Python EDA → Power BI → Business Insights & Recommendations

🎯 1. Problem Statement

AI assistants generate large volumes of conversation data containing messages, users, languages, timestamps, reviews, conversation relationships, and metadata.

Raw conversation data can be difficult to analyze because of:

Missing values
Inconsistent data formats
Complex conversation relationships
Large numbers of records
Metadata requiring validation
Lack of structured analytical storage

This project addresses these challenges by building a complete data pipeline that converts raw conversation data into clean, validated, structured, and analysis-ready information.

💡 2. Proposed Solution

The project implements the following end-to-end workflow:

OASST1 Raw Dataset
        ↓
     EXTRACT
        ↓
    TRANSFORM
        ↓
     VALIDATE
        ↓
      LOAD
        ↓
 SQLite Database
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
📊 3. Dataset
Dataset Used

OpenAssistant Conversations Dataset — OASST1

The dataset contains conversation-tree-based interactions collected for the OpenAssistant project.

Dataset Statistics
Metric	Value
Total Messages	88,838
Total Conversations	10,364
Unique Users	13,249
Languages	25
Final Message Fields	18
Duplicate Message IDs	0
Orphan Parent IDs	0
Empty Text Records	0
Dataset Period	January–April 2023
Role Distribution
Role	Messages	Share
Assistant	55,668	62.66%
Prompter	33,170	37.34%
🏗️ 4. Project Architecture
                    OASST1 DATASET
                          │
                          ▼
                     01_DATA/raw
                          │
                          ▼
                    ┌─────────────┐
                    │   EXTRACT   │
                    │  ingest.py  │
                    └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │  TRANSFORM  │
                    │ transform.py│
                    └─────────────┘
                          │
                          ▼
                   DATA VALIDATION
                          │
                          ▼
                  01_DATA/processed
                          │
                          ▼
                    ┌─────────────┐
                    │    LOAD     │
                    │   load.py   │
                    └─────────────┘
                          │
                          ▼
                    SQLite Database
                       oasst.db
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
           SQL Analysis        Python EDA
                 │                 │
                 └────────┬────────┘
                          ▼
                       Power BI
                          │
                          ▼
                Business Intelligence
                     │          │
                     ▼          ▼
                  Insights  Recommendations
🔄 5. ETL Pipeline
Extract

ingest.py loads the OASST1 training and validation datasets and verifies source availability, record counts, and column structure.

Training Records    : 84,437
Validation Records  : 4,401
Total Records       : 88,838
Transform

transform.py performs:

Dataset combination
Data standardization
Missing-value validation
Duplicate validation
Empty-text validation
Parent-child relationship validation
Review-count validation
Removal of unusable fields

The model_name field was removed because it contained 100% missing values.

Final Records  : 88,838
Final Columns  : 18

Output:

01_DATA/processed/oasst1_processed.csv
Load

load.py loads the processed data into SQLite.

The database contains:

conversations
messages

Validation result:

Conversations       : 10,364
Messages            : 88,838
Duplicate IDs       : 0
Foreign-Key Errors  : 0

Database:

03_DATABASE/oasst.db
⚙️ 6. Master Pipeline

pipeline.py orchestrates the complete ETL workflow:

ingest.py
    ↓
transform.py
    ↓
validate
    ↓
load.py
    ↓
SQLite Database

The complete pipeline was successfully executed.

ETL STATUS: PASSED

The actual pipeline execution completed in approximately 31 seconds during final testing.

The pipeline is designed for compatible datasets following the expected OASST1 structure and schema. A substantially different dataset schema would require changes to the transformation, database mapping, analysis, and Power BI model.

🗄️ 7. SQLite Database

SQLite is used as the structured analytical database.

Why SQLite?
Lightweight
Serverless
Easy to maintain
Supports SQL
Suitable for academic and analytical projects
Provides structured relational storage

The database separates conversation-level and message-level information for efficient analysis.

🔎 8. SQL Analysis

The SQL analysis layer is located at:

04_ANALYSIS/sql/analysis_queries.sql

A total of 16 SQL queries were executed successfully.

The analysis covers:

Dataset overview
Role distribution
Language distribution
Conversation length
Review coverage
Review-result categories
Synthetic data
Deleted messages
Language × role analysis
User activity
Monthly activity
Conversation statistics
Review coverage by role
Data integrity validation
Key SQL Results
Total Messages       : 88,838
Total Conversations  : 10,364
Total Users          : 13,249
Languages            : 25
Average Messages/Conversation : 8.57
Assistant Messages   : 62.66%
Prompter Messages    : 37.34%
Deleted Messages     : 1.75%
Duplicate IDs        : 0
Empty Text Records   : 0
📈 9. Exploratory Data Analysis

Python and Jupyter Notebook were used for Exploratory Data Analysis.

EDA covers:

Dataset profiling
Missing-value analysis
Role analysis
Language analysis
Conversation analysis
Review analysis
Monthly trends
Conversation-length analysis
Deleted-message analysis
Language × role analysis
User activity
Review coverage
Message-length analysis
Data-quality validation
SQL ↔ EDA consistency checks
Important Findings
Conversation Activity
Messages              : 88,838
Conversations         : 10,364
Average Messages      : 8.57
Minimum Messages      : 2
Maximum Messages      : 56
Language Distribution
English : 41,305 messages — 46.49%
Spanish : 23,975 messages — 26.99%

English and Spanish together account for approximately 73.5% of all messages.

Monthly Activity
Month	Messages
January 2023	3,206
February 2023	60,932
March 2023	16,479
April 2023	8,221

February 2023 represents the highest activity period.

Deleted Messages
Deleted Messages      : 1,553
Non-Deleted Messages  : 87,285
Deleted Rate          : 1.75%
Message Length
Role	Mean Characters	Median Characters
Assistant	716.97	482
Prompter	119.15	71

Assistant messages are substantially longer than prompter messages.

📊 10. Power BI Business Intelligence

Power BI converts the validated analytical data into an interactive Business Intelligence solution.

Page 1 — Executive Overview

The dashboard provides:

Total Messages
Total Conversations
Unique Users
Total Languages
Messages per Conversation
Review Coverage
Review-result analysis
Monthly trends
Role distribution
Language distribution
Data Quality indicators
Current Dashboard KPIs
KPI	Current Display
Total Messages	89K
Total Conversations	10K
Unique Users	13K
Languages	25
Messages / Conversation	8.57
Review Result 1 %	98.49%
Review Coverage	99.18%
Deleted %	1.75%
Page 2 — Insights & Recommendations

The second dashboard page provides:

Dynamic business insights
Business interpretation
Management actions
Recommendations
Data-quality observations
Language and engagement observations
Trend-based analysis

DAX measures are used to make relevant insights respond dynamically to Power BI filters and slicers.

🧠 11. Business Questions Answered
Engagement
How much conversation activity exists?
How many users and conversations are involved?
What is the average conversation size?
User Interaction
What proportion of messages are generated by the assistant?
How does prompter activity compare with assistant activity?
Language
Which languages dominate the dataset?
How concentrated is multilingual activity?
Temporal Trends
Which months show the highest activity?
How does conversation volume change over time?
Conversation Behavior
How long are typical conversations?
Are very long conversations common?
Quality
How much of the dataset has review information?
What are the observed review-result categories?
Data Quality & Safety
How many messages are deleted?
How complete are important metadata fields?
What areas require monitoring?
📌 12. Key Business Insights
The dataset contains 88,838 messages across 10,364 conversations.
Assistant messages represent 62.66% of all messages.
English and Spanish account for approximately 73.5% of all messages.
February 2023 recorded the highest activity with 60,932 messages.
Conversations contain an average of 8.57 messages.
Very long conversations are uncommon, with only 52 conversations containing 21+ messages.
Review coverage is very high and supports quality-oriented analysis.
Deleted messages represent approximately 1.75% of total messages.
Assistant messages are significantly longer than prompter messages.
Data integrity checks identified 0 duplicate message IDs and 0 orphan parent IDs.
⚠️ 13. Important Data Interpretation Rule

The review_result field contains values such as 0 and 1, along with missing values.

Unless the exact semantic meaning of these values is formally verified from the dataset documentation, this project does not automatically interpret:

1 = Positive
0 = Negative

Instead, the dashboard treats them as review-result categories.

This prevents unsupported interpretation of the source data.

🧪 14. Testing & Validation

The project was validated across the complete data flow:

Raw Dataset
     ↓
ETL
     ↓
Processed Dataset
     ↓
SQLite
     ↓
SQL
     ↓
EDA
     ↓
Power BI

Validation included:

Record-count verification
Duplicate checks
Missing-value checks
Empty-text checks
Parent-child relationship checks
SQLite validation
SQL result verification
EDA consistency checks
Power BI KPI verification

The major analytical values were cross-checked between SQL, EDA, and Power BI.

📁 15. Project Structure
AI-Assistant-Conversation-Analytics/
│
├── 01_DATA/
│   ├── raw/
│   └── processed/
│       └── oasst1_processed.csv
│
├── 02_ETL/
│   ├── ingest.py
│   ├── transform.py
│   ├── load.py
│   └── pipeline.py
│
├── 03_DATABASE/
│   ├── oasst.db
│   └── schema.sql
│
├── 04_ANALYSIS/
│   ├── sql/
│   │   ├── analysis_queries.sql
│   │   └── run_analysis.py
│   │
│   └── eda/
│       └── oasst_eda.ipynb
│
├── 05_POWER_BI/
│   └── oasst_dashboard.pbix
│
├── 06_TESTING/
│   └── test_report.md
│
├── 07_DOCUMENTATION/
│   ├── data_dictionary.md
│   ├── architecture.md
│   └── project_report.md
│
├── 08_PRESENTATION/
│   └── final_presentation.pptx
│
├── requirements.txt
├── .gitignore
└── README.md
🛠️ 16. Technology Stack
Technology	Purpose
Python	ETL and EDA
Pandas	Data transformation and analysis
SQLite	Structured database
SQL	Business and analytical queries
Jupyter Notebook	Exploratory Data Analysis
Power BI	Business Intelligence dashboard
DAX	KPIs, insights and recommendations
VS Code	Development environment
GitHub	Version control and project repository
▶️ 17. How to Run the Project
Step 1 — Run Complete ETL Pipeline
python 02_ETL/pipeline.py

This executes:

Extract
   ↓
Transform
   ↓
Validate
   ↓
Load

and creates or updates the SQLite database.

Step 2 — Run SQL Analysis
python 04_ANALYSIS/sql/run_analysis.py
Step 3 — Run EDA

Open:

04_ANALYSIS/eda/oasst_eda.ipynb

and execute the notebook.

Step 4 — Open Power BI

Open:

05_POWER_BI/oasst_dashboard.pbix

Refresh the data/model and verify the dashboard.

⚠️ 18. Limitations
The dataset represents a specific OASST1 collection period and does not represent all AI-assistant usage.
The available dataset covers January–April 2023.
Response-time analysis is limited because the dataset does not provide a direct production-style response-time metric.
User IDs are anonymous identifiers and should not be treated as personally identifiable information.
Review-result values require semantic verification before being interpreted as positive or negative.
A completely different dataset schema would require modifications to the ETL and analytical model.
Power BI visuals and DAX calculations depend on the available fields and data model.
🚀 19. Future Scope

Potential future improvements include:

Real-time conversation analytics
Response-time monitoring
Sentiment analysis
Intent classification
Conversation-resolution prediction
Advanced user segmentation
Automated anomaly detection
ML-based quality prediction
Cloud-based data warehouse integration
Automated Power BI refresh
Production-scale orchestration
🎓 20. Conclusion

This project demonstrates a complete end-to-end Data Engineering and Business Intelligence workflow for AI assistant conversation analytics.

Starting from raw OASST1 conversation data, the project performs:

Extract
   ↓
Transform
   ↓
Validate
   ↓
Load
   ↓
SQLite
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

The final solution transforms raw conversation records into structured analytical data and provides an interactive Business Intelligence layer for understanding:

AI assistant activity
Conversation behavior
Language distribution
User interaction
Data quality
Review coverage
Deleted content
Temporal activity patterns

The project demonstrates how Data Engineering + SQL + Python + Power BI can work together to transform raw data into meaningful and actionable business intelligence.