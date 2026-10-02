from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

load_dotenv(PROJECT_ROOT / ".env")


DATASETS = [
    {
        "name": "customers",
        "file": "olist_customers_dataset.csv",
        "table": "customers",
    },
    {
        "name": "sellers",
        "file": "olist_sellers_dataset.csv",
        "table": "sellers",
    },
    {
        "name": "products",
        "file": "olist_products_dataset.csv",
        "table": "products",
    },
    {
        "name": "orders",
        "file": "olist_orders_dataset.csv",
        "table": "orders",
    },
    {
        "name": "order_items",
        "file": "olist_order_items_dataset.csv",
        "table": "order_items",
    },
    {
        "name": "order_payments",
        "file": "olist_order_payments_dataset.csv",
        "table": "order_payments",
    },
    {
        "name": "order_reviews",
        "file": "olist_order_reviews_dataset.csv",
        "table": "order_reviews",
    },
    {
        "name": "geolocation",
        "file": "olist_geolocation_dataset.csv",
        "table": "geolocation",
    },
    {
        "name": "category_translation",
        "file": "product_category_name_translation.csv",
        "table": "category_translation",
    },
]


def get_engine():
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )

    return create_engine(database_url)


def load_csv(filename):
    path = RAW_DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    return pd.read_csv(path)


def prepare_dates(df, table):
    date_columns = {
        "orders": [
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
        "order_items": [
            "shipping_limit_date"
        ],
        "order_reviews": [
            "review_creation_date",
            "review_answer_timestamp",
        ],
    }

    for column in date_columns.get(table, []):
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df


def prepare_products(df):
    rename_map = {
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length",
    }

    return df.rename(columns=rename_map)


def prepare_dataframe(df, table):

    if table == "products":
        df = prepare_products(df)

    df = prepare_dates(df, table)

    return df


def get_table_count(engine, table):

    query = text(
        f'SELECT COUNT(*) FROM "{table}"'
    )

    with engine.connect() as connection:
        return connection.execute(query).scalar_one()


def load_table(engine, dataframe, table):

    # PostgreSQL COPY works with CSV formatted data.
    csv_data = dataframe.to_csv(
        index=False,
        header=False,
        na_rep="\\N",
    )

    raw_connection = engine.raw_connection()

    try:
        cursor = raw_connection.cursor()

        columns = list(dataframe.columns)

        column_list = ", ".join(
            f'"{column}"'
            for column in columns
        )

        copy_sql = f"""
            COPY "{table}" ({column_list})
            FROM STDIN
            WITH (
                FORMAT CSV,
                NULL '\\N',
                HEADER FALSE
            )
        """

        from io import StringIO

        buffer = StringIO(csv_data)

        cursor.copy_expert(
            copy_sql,
            buffer
        )

        raw_connection.commit()

    except Exception:
        raw_connection.rollback()
        raise

    finally:
        cursor.close()
        raw_connection.close()

    return len(dataframe)


def main():

    engine = get_engine()

    print("=" * 80)
    print("RETAILPULSE DATA LOADER")
    print("=" * 80)

    for dataset in DATASETS:

        name = dataset["name"]
        filename = dataset["file"]
        table = dataset["table"]

        print(f"\nLoading: {name}")

        existing_rows = get_table_count(
            engine,
            table
        )

        if existing_rows > 0:

            print(
                f"Already loaded: "
                f"{existing_rows:,} rows"
            )

            print("Skipping...")
            continue

        dataframe = load_csv(filename)

        dataframe = prepare_dataframe(
            dataframe,
            table
        )

        expected_rows = len(dataframe)

        print(
            f"CSV rows: "
            f"{expected_rows:,}"
        )

        loaded_rows = load_table(
            engine,
            dataframe,
            table
        )

        database_rows = get_table_count(
            engine,
            table
        )

        print(
            f"Loaded rows: "
            f"{loaded_rows:,}"
        )

        print(
            f"Database rows: "
            f"{database_rows:,}"
        )

        if database_rows != expected_rows:

            raise RuntimeError(
                f"Row count mismatch for {table}: "
                f"expected {expected_rows:,}, "
                f"found {database_rows:,}"
            )

    print(
        "\nAll datasets loaded successfully."
    )


if __name__ == "__main__":
    main()