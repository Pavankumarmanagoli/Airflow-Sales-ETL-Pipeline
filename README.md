

# Airflow Sales ETL Pipeline 

An end-to-end **ETL + Data Warehouse** project built with **Apache Airflow, Docker, Python, and SQLite** using the Superstore dataset to transform raw sales data into a structured analytical data warehouse.

This project demonstrates how a real-world data engineering pipeline is designed, orchestrated, monitored, and validated using production-style practices.

---

##  What this project does

The pipeline:

1. Ingests raw sales data from `include/Superstore.csv`
2. Cleans and enriches the data with business metrics
3. Loads it into a **staging table (`sales_data`)**
4. Builds a **star-schema data warehouse**:

   * Dimensions: `dim_customers`, `dim_products`, `dim_dates`, `dim_location`
   * Fact: `fact_sales`
5. Runs **automated data-quality tests** using `pytest`

The main Airflow DAG is:

```
superstore_data_pipeline_sqlite
```

---

##  Architecture Overview

### Data Source & Storage

* **Input:** `include/Superstore.csv`
* **Warehouse:** `include/superstore.db` (SQLite — created at runtime by Airflow)

> Note: The SQLite warehouse is generated automatically when the DAG runs inside Docker.

---

##  Star Schema (Warehouse Design)

![Star Schema](images/star_schema.png)

This diagram shows:

* Central fact table: **`fact_sales`**
* Surrounding dimensions:

  * `dim_customers`
  * `dim_products`
  * `dim_dates`
  * `dim_location`

### Why this matters

* Separates **business facts (sales, profit, quantity)** from **descriptive attributes (customer, product, date, location)**
* Enables fast analytics
* Mirrors industry-standard data warehouse design

---

## ⚙️ Airflow Orchestration

### DAG Files

* **`dags/superstore_pipeline_sqlite.py`**

  * Main orchestration DAG controlling the entire workflow

* **`dags/superstore_transformation.py`**

  * Contains reusable transformation functions:

    * `create_dim_customers`
    * `create_dim_products`
    * `create_dim_dates`
    * `create_dim_location`
    * `create_fact_sales`

---

##  Pipeline Flow (Task Graph)

![Airflow DAG Graph](images/airflow_graph.png)

### Step-by-step execution

1. **process_and_load_data (Extract–Transform–Load)**

   * Reads CSV
   * Standardizes schema
   * Parses dates
   * Creates metrics:

     * `profit_margin`
     * `discount_amount`
     * `shipping_duration`
     * `profit_category`
     * `sales_tier`
   * Loads into **staging table `sales_data`**

2. **Build Dimensions (in parallel)**

   * `create_dim_customers`
   * `create_dim_products`
   * `create_dim_dates`
   * `create_dim_location`

3. **Build Fact**

   * `create_fact_sales`
   * Joins staging with all dimensions
   * Creates final analytical table **`fact_sales`**

This parallel design improves performance and reflects real production pipelines.

---

##  Airflow Grid View (Successful Run)

![Airflow Grid](images/airflow_grid.png)

The grid view confirms that:

* Staging completed
* All dimension tables were built
* Fact table was created successfully

---

##  SQLite Warehouse Output

![SQLite Tables](images/sqlite_tables.png)

After the DAG runs, your warehouse contains:

```
sales_data  
dim_customers  
dim_products  
dim_dates  
dim_location  
fact_sales   (~9,986 rows)  
```

Inspect inside Docker:

```bash
docker compose exec airflow-webserver sqlite3 /opt/airflow/include/superstore.db
.tables
SELECT COUNT(*) FROM fact_sales;
```

---

## 🛠️ Tech Stack

* **Apache Airflow** — workflow orchestration
* **Docker** — containerized runtime
* **Python & Pandas** — data transformation
* **SQLAlchemy + sqlite3** — DB access
* **SQLite** — lightweight analytical warehouse
* **Pytest** — automated data validation

---

## 📂 Repository Structure

```
.
├── dags/
│   ├── superstore_pipeline_sqlite.py
│   ├── superstore_transformation.py
│   └── exampledag.py
├── include/
│   ├── Superstore.csv
│   └── superstore.db   # created at runtime
├── model/
│   ├── sales_data.py
│   ├── dim_customers.py
│   ├── dim_products.py
│   ├── dim_dates.py
│   ├── dim_location.py
│   └── fact_sales.py
├── tests/
│   ├── dags/test_dag_example.py
│   └── test_data_quality.py
├── images/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run (Docker — Recommended)

Start Airflow:

```bash
docker compose up
```

Open UI:

```
http://localhost:8080
```

Trigger DAG:

```
superstore_data_pipeline_sqlite
```

---

## 🧪 Data Quality Tests

Tests are in:

```
tests/test_data_quality.py
```

They check:

* `fact_sales` exists and is populated
* No missing critical keys
* No negative sales
* No non-positive quantity
* No duplicate `order_product_id`
* Every sale has a valid customer

Run all tests:

```bash
pytest -q
```

Run only data quality tests:

```bash
pytest -q tests/test_data_quality.py
```

---

## 🚀 Future Improvements

* Migrate SQLite → PostgreSQL / Snowflake
* Add incremental loads
* Add dbt layer
* Add Power BI / Tableau dashboard
* Add CI pipeline for automated testing
