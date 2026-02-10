# Airflow Sales ETL Pipeline (Portfolio Overview)

## Project Snapshot
Designed and implemented an end-to-end data engineering pipeline that transforms raw Superstore sales data into an analytics-ready star schema using **Apache Airflow**, **Python**, and **SQLite**.

- **Domain:** Retail sales analytics
- **Pipeline type:** Batch ETL
- **Orchestration:** Airflow DAG (`superstore_data_pipeline_sqlite`)
- **Warehouse model:** Star schema (1 fact + 4 dimensions)

---

## Business Problem
Raw sales CSV files are not optimized for analytics. This project builds a repeatable pipeline that standardizes raw records, computes business metrics, and publishes modeled tables for BI-style analysis.

---

## What I Built

### 1) ETL Orchestration with Airflow
- Built a DAG that orchestrates staging, dimensional modeling, and fact loading.
- Designed task dependencies with a parallel dimension build step for better runtime efficiency.

### 2) Transformation Layer
- Cleaned and standardized raw dataset fields.
- Engineered derived metrics such as:
  - `profit_margin`
  - `discount_amount`
  - `shipping_duration`
- Added business classifications (`profit_category`, `sales_tier`) to support richer analysis.

### 3) Dimensional Warehouse Model
- **Fact:** `fact_sales`
- **Dimensions:** `dim_customers`, `dim_products`, `dim_dates`, `dim_location`
- Enabled analytical joins and easier reporting across customer/product/time/geography axes.

### 4) Data Quality Validation
- Implemented `pytest` checks to validate:
  - fact table existence and non-empty load,
  - key integrity,
  - invalid numeric values,
  - duplicate prevention,
  - dimension relationship consistency.

---

## Technical Stack
- **Orchestration:** Apache Airflow
- **Processing:** Python, Pandas
- **Storage:** SQLite
- **Testing:** Pytest
- **Container Runtime:** Astronomer/Airflow Docker runtime

---

## Architecture at a Glance

1. Source CSV (`include/Superstore.csv`) ingested to staging table (`sales_data`)  
2. Dimension tables created from staged data  
3. Fact table assembled by joining staging with dimensions  
4. Data quality assertions executed post-load

Assets in repository:
- DAG graph: `airflow_graph.png`
- Star schema: `star_schema.png`
- Table snapshot: `sqlite_tables.png`

---

## Measurable Output (Current Repo Snapshot)
- `fact_sales`: **9,986** rows
- `dim_customers`: **793** rows
- `dim_products`: **1,862** rows
- `dim_dates`: **1,037** rows
- `dim_location`: **1,264** rows

---

## Why This Project Is Valuable
- Demonstrates practical understanding of **ETL lifecycle design**.
- Applies **dimensional modeling** patterns used in analytics engineering.
- Shows **workflow orchestration** and dependency management in Airflow.
- Includes **automated quality checks**, not just one-time scripting.

---

## Repository Entry Points
- Main DAG: `dags/superstore_pipeline_sqlite.py`
- Transform functions: `dags/superstore_transformation.py`
- Quality tests: `tests/test_data_quality.py`
- Full technical README: `README.md`
