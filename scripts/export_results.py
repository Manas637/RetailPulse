from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL
import os


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(exist_ok=True)

load_dotenv(PROJECT_ROOT / ".env")


def get_engine():
    required_variables = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    missing = [
        variable
        for variable in required_variables
        if not os.getenv(variable)
    ]

    if missing:
        raise RuntimeError(
            f"Missing database environment variables: {missing}"
        )

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    return create_engine(database_url)


EXPORTS = {
    "monthly_sales.csv": "SELECT * FROM rpt_sales_dashboard ORDER BY sales_month",
    "category_sales.csv": """
        SELECT *
        FROM rpt_category_dashboard
        ORDER BY merchandise_revenue DESC
    """,
    "seller_sales.csv": """
        SELECT *
        FROM rpt_seller_dashboard
        ORDER BY merchandise_revenue DESC
    """,
    "customer_segments.csv": """
        SELECT
            customer_segment,
            COUNT(*) AS customer_count,
            ROUND(AVG(total_customer_value), 2) AS average_customer_value,
            ROUND(SUM(total_customer_value), 2) AS total_customer_value,
            ROUND(AVG(order_count), 2) AS average_orders_per_customer
        FROM rpt_customer_dashboard
        GROUP BY customer_segment
        ORDER BY customer_count DESC
    """,
    "monthly_delivery.csv": """
        SELECT *
        FROM rpt_delivery_dashboard
        ORDER BY sales_month
    """,
}


def main():
    engine = get_engine()

    print("Exporting RetailPulse analytical results...\n")

    for filename, query in EXPORTS.items():
        output_path = RESULTS_DIR / filename

        df = pd.read_sql(query, engine)
        df.to_csv(output_path, index=False)

        print(f"{filename}: {len(df):,} rows")

    engine.dispose()

    print("\nAll results exported successfully.")


if __name__ == "__main__":
    main()