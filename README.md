# Amazon PPC ACoS Analyzer 📊

An end-to-end data analytics project that automates the analysis of Amazon Sponsored Products Search Term Reports. This project cleans raw advertising data, calculates key PPC KPIs using Python, stores processed data in SQL, and visualizes campaign performance through an interactive Power BI dashboard.

---

This project is designed to answer three critical Amazon PPC business questions that help sellers optimize advertising performance and maximize return on ad spend.

## 1️⃣ Which keywords are profitable and should be scaled?
## 2️⃣ Which keywords are wasting advertising spend and should be optimized or negated?
## 3️⃣ How can campaign performance be improved?
---
# 🚀 Project Overview

The Amazon PPC ACoS Analyzer helps Amazon sellers and PPC specialists quickly identify:

- Winning keywords
- High ACoS search terms
- Negative keyword opportunities
- Low CTR campaigns
- High ROAS keywords
- Campaign performance trends

Instead of manually analyzing thousands of search terms, this project automates the complete workflow.

## 🏗️ Directory Structure

Here is how the project files are organized. The workflow moves from raw data ingestion to SQL storage, Python-based KPI calculations, and finally to visual reporting.

```text
Amazon-PPC-ACoS-Analyzer/
│
├── data/
│   ├── raw/                  # Original Amazon Search Term reports (.xlsx)
│   └── processed/            # Cleaned, structured outputs ready for analysis
│
├── sql/
│   ├── create_database.sql   # Database schemas and tables
│   ├── import_data.sql       # Script to load processed data into SQL
│   └── analysis_queries.sql  # Deep-dive queries (ACoS, target keywords, etc.)
│
├── python/
│   ├── main.py               # Main pipeline execution script
│   ├── data_cleaning.py      # Standardizes raw inputs & handles missing values
│   ├── kpi_calculator.py     # Calculates ACoS, ROAS, CTR, and conversion rates
│   ├── classifier.py         # Categorizes search terms (e.g., Branded vs. Generic)
│   └── export_excel.py       # Formats and exports analysis back to Excel
│
├── powerbi/
│   └── Amazon_PPC_Dashboard.pbix  # Interactive Power BI report file
│
├── screenshots/              # Images used in this README
│   ├── GUI_screenshot.png
│   ├── Result.png
│   └── powerbi.png
│
├── output/                   # Final business-ready Excel reports
│   └── Amazon_PPC_Report.xlsx
│
├── README.md
├── requirements.txt          # Python dependencies
└── LICENSE
```
# 🏗️ Project Architecture

```
                  Amazon Search Term Report (.xlsx)
                               │
                               ▼
                     Excel Data Validation
              (Missing Values • Duplicates • Formatting)
                               │
                               ▼
                    Python Data Cleaning (Pandas)
                               │
                               ▼
                      KPI Calculations
        CTR • CPC • CVR • ACoS • ROAS • TACoS
                               │
                               ▼
                 Search Term Classification
       Winner • Watch • Waste • Negate Keywords
                               │
                               ▼
                  Export Clean Dataset (.xlsx)
                               │
                               ▼
                    PostgreSQL Database
                               │
                               ▼
                      SQL Analysis Queries
                               │
                               ▼
                    Power BI Dashboard
                               │
                               ▼
                   Business Recommendations
```

---
## GUI_screenshot

![GUI_screenshot](screenshots/GUI_screenshot.png)

## Result

![Result](screenshots/Result.png)

# 📊 KPI Calculations

| KPI | Formula |
|------|----------|
| CTR | Clicks ÷ Impressions |
| CPC | Spend ÷ Clicks |
| CVR | Orders ÷ Clicks |
| ACoS | Spend ÷ Sales |
| ROAS | Sales ÷ Spend |
| TACoS | Spend ÷ Total Sales |


## Recommendation

![Recommendation](screenshots/Recommendation.png)

# 📈 Recommendations
### Search Term Classification

Business Rules

| Condition | Classification |
|------------|---------------|
| ACoS ≤ 30% | Scale Winners |
| 30% < ACoS ≤ 40% | Optimize-Watch |
| ACoS > 40% | Waste |
| Spend > $10 & Sales = 0 | Negate |
| Clicks > 20 & Orders = 0 | Negate |


Based on the analysis, the project recommends:

## Scale Winners

- Increase bids
- Increase campaign budget
- Move search terms into Exact Match campaigns

## Optimize-Watch

- Reduce bids on high ACoS keywords
- Test new match types
- Improve product listings

## Waste-Negate

- Add Negative Keywords
- Pause consistently poor-performing keywords




