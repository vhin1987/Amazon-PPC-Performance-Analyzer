# Amazon PPC ACoS Analyzer 📊

An end-to-end data engineering and analytics pipeline designed to ingest raw Amazon Search Term Reports, clean and process the data, perform SQL-based performance analysis, and visualize key advertising metrics like ACoS (Advertising Cost of Sales) and ROAS (Return on Ad Spend) in Power BI.

---

## 🏗️ Project Architecture & Directory Structure

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
│   ├── workflow.png
│   ├── dashboard.png
│   └── powerbi.png
│
├── output/                   # Final business-ready Excel reports
│   └── Amazon_PPC_Report.xlsx
│
├── README.md
├── requirements.txt          # Python dependencies
└── LICENSE

## GUI_screenshot
![GUI]screenshots/GUI_screenshot.png
