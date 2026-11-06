# Smart Manufacturing Data Warehouse & ETL Pipeline

An end-to-end data engineering system designed to model, clean, extract, transform, and load raw manufacturing factory execution data into an optimized analytical warehouse.

## 📊 Data Architecture (Star Schema)
To optimize data reads and business intelligence parsing, this repository structures flat production inputs into distinct tables inside a **SQLite** architecture:
- **Fact Table:** `fact_production_events` (Tracks production metrics, logs quantities, defect rates, and environmental conditions)
- **Dimension Tables:** `dim_machines`, `dim_products` (Optimizes lookup speeds across execution lines)

## 🛠️ Tech Stack & Skills Demonstrated
- **Programming Languages:** Python, SQL
- **Libraries:** Pandas, SQLite3
- **Design Methods:** Dimensional Modeling, ETL Pipelines, Data Scrubbing, Modular Programming (OOP)

## 🚀 How to Execute
1. Initialize the SQLite Schema:
   ```bash
   python src/database_setup.py
   ```
2. Execute the Data Pipeline:
   ```bash
   python src/etl_pipeline.py
   ```
