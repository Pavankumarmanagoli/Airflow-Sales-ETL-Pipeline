# 🚀 Superstore Data Engineering Pipeline

### Apache Airflow + Docker + SQLite Star Schema

An end-to-end Data Engineering project that builds a production-style
ETL pipeline using **Apache Airflow**, **Docker**, **WSL**, and
**SQLite**, transforming raw transactional CSV data into a dimensional
**Star Schema** data warehouse.

---

## 📌 Project Overview

This project demonstrates how raw business data (CSV) can be:

-   Extracted
-   Cleaned and transformed
-   Modeled into Fact & Dimension tables
-   Orchestrated using Apache Airflow
-   Stored in a SQLite data warehouse

---

## Airflow View 
1. Airflow DAG Graph View
![Airflow DAG Graph View](images/airflow_graph.png)

2. Airflow Performance Metrics
![Airflow Performance Metrics](images/airflow_task_duration_charts.png)

---

## 🏗️ Architecture
![Architecture](images/Architecture.png)

---

## 📊 Airflow DAG Flow

1.  process_and_load_data\
2.  create_dim_products\
3.  create_dim_customers\
4.  create_dim_dates\
5.  create_dim_location\
6.  create_fact_sales

---

## 🧠 Data Modeling (Star Schema)

![Star Schema](images/star_schema.png)

### Fact Table: fact_sales

Contains: - order_id - customer_key - product_key - date_key -
location_key - sales - quantity - discount - profit - profit_margin -
discount_amount - shipping_duration - profit_category - sales_tier

### Dimension Tables

**dim_customers** - customer_id - customer_name - segment

**dim_products** - product_id - category - sub_category - product_name

**dim_dates** - year - quarter - month - day

**dim_location** - country - state - city - region

---

## 🔄 ETL Workflow

### Extract

-   Load Superstore.csv
-   Parse date fields
-   Validate schema

### Transform

-   Profit margin calculation
-   Shipping duration calculation
-   Discount amount calculation
-   Sales tier classification
-   Normalize into dimension tables

### Load

-   Insert into staging table
-   Create dimension tables
-   Build fact table with relationships

---

## 🗄️ Database Verification

Example:

SELECT COUNT(\*) FROM fact_sales;

Result: 9986 rows

SQLite Tables View and Fact Table Query Result
![SQLite Tables](images/sqlite_tables.png)

---

## 📂 Project Structure

Airflow-data-pipeline/
│
├── dags/
│   ├── superstore_pipeline_sqlite.py
│   └── superstore_transformation.py
│
├── include/
│   ├── Superstore.csv
│   └── superstore.db
│
├── docker-compose.yml
├── requirements.txt
└── README.md
└── screenshots/
    ├── 01_airflow_dag_graph.png
    ├── 02_airflow_performance_metrics.png
    ├── 03_sqlite_tables.png
    ├── 04_fact_sales_query.png


---

## ⚙️ How to Run

1.  Start WSL\
    wsl

2.  Navigate to project\
    cd \~/Airflow-data-pipeline

3.  Start containers\
    docker compose up -d

4.  Open Airflow UI\
    http://localhost:8080

5.  Enable and trigger DAG\
    superstore_data_pipeline_sqlite

---

## 🛠️ Tech Stack

-   Apache Airflow
-   Docker
-   WSL
-   SQLite
-   Pandas
-   SQLAlchemy
-   Python

---

## 🚀 Future Improvements

-   Replace SQLite with PostgreSQL
-   Add Data Quality Checks
-   Add Unit Testing
-   Implement Incremental Loads
-   Add CI/CD Pipeline
-   Deploy to Cloud

---

## License

This repository is licensed under the terms in `MIT LICENSE`.