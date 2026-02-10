"""Data quality tests for warehouse tables.

These checks are intended to run after the DAG has populated the warehouse model,
with a focus on the `fact_sales` table.
"""

from pathlib import Path
import sqlite3

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
ALT_ROOT = Path(__file__).resolve().parents[2]

# Primary path for this repo layout, with a fallback for alternate test execution layouts.
DB_PATH = REPO_ROOT / "include" / "superstore.db"
if not DB_PATH.exists():
    DB_PATH = ALT_ROOT / "include" / "superstore.db"


def _fetch_scalar(query: str) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(query)
        return int(cur.fetchone()[0])


@pytest.fixture(scope="module", autouse=True)
def _require_database() -> None:
    """Skip quality checks when the local warehouse DB is not present."""
    if not DB_PATH.exists():
        pytest.skip(f"Database not found at {DB_PATH}. Run the DAG first.")



def test_fact_sales_table_exists_and_is_populated() -> None:
    table_exists = _fetch_scalar(
        """
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE type = 'table' AND name = 'fact_sales'
        """
    )
    assert table_exists == 1, "fact_sales table does not exist."

    row_count = _fetch_scalar("SELECT COUNT(*) FROM fact_sales")
    assert row_count > 0, "fact_sales table is empty."



def test_no_missing_critical_keys_in_fact_sales() -> None:
    missing_count = _fetch_scalar(
        """
        SELECT COUNT(*)
        FROM fact_sales
        WHERE order_product_id IS NULL
           OR order_id IS NULL
           OR customer_id IS NULL
           OR product_id IS NULL
        """
    )
    assert missing_count == 0, f"Found {missing_count} rows with missing critical keys."



def test_no_invalid_sales_or_quantity_values() -> None:
    negative_sales = _fetch_scalar("SELECT COUNT(*) FROM fact_sales WHERE sales < 0")
    assert negative_sales == 0, f"Found {negative_sales} rows with negative sales."

    invalid_quantity = _fetch_scalar("SELECT COUNT(*) FROM fact_sales WHERE quantity <= 0")
    assert invalid_quantity == 0, f"Found {invalid_quantity} rows with non-positive quantity."



def test_no_duplicate_order_product_rows() -> None:
    duplicate_groups = _fetch_scalar(
        """
        SELECT COUNT(*)
        FROM (
            SELECT order_product_id
            FROM fact_sales
            GROUP BY order_product_id
            HAVING COUNT(*) > 1
        )
        """
    )
    assert duplicate_groups == 0, f"Found {duplicate_groups} duplicate order_product_id groups."



def test_every_sale_has_a_valid_customer() -> None:
    missing_customer_fk = _fetch_scalar(
        """
        SELECT COUNT(*)
        FROM fact_sales f
        LEFT JOIN dim_customers c
          ON f.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
        """
    )
    assert (
        missing_customer_fk == 0
    ), f"Found {missing_customer_fk} fact_sales rows without a matching customer."