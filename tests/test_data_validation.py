from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_dataset(filename: str) -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / filename)


def test_primary_keys_are_unique():
    customers = load_dataset("olist_customers_dataset.csv")
    orders = load_dataset("olist_orders_dataset.csv")
    products = load_dataset("olist_products_dataset.csv")
    sellers = load_dataset("olist_sellers_dataset.csv")

    assert customers["customer_id"].is_unique
    assert orders["order_id"].is_unique
    assert products["product_id"].is_unique
    assert sellers["seller_id"].is_unique


def test_orders_reference_existing_customers():
    customers = load_dataset("olist_customers_dataset.csv")
    orders = load_dataset("olist_orders_dataset.csv")

    customer_ids = set(customers["customer_id"])

    assert orders["customer_id"].isin(customer_ids).all()


def test_order_items_reference_existing_orders():
    orders = load_dataset("olist_orders_dataset.csv")
    order_items = load_dataset("olist_order_items_dataset.csv")

    order_ids = set(orders["order_id"])

    assert order_items["order_id"].isin(order_ids).all()


def test_order_items_reference_existing_products():
    products = load_dataset("olist_products_dataset.csv")
    order_items = load_dataset("olist_order_items_dataset.csv")

    product_ids = set(products["product_id"])

    assert order_items["product_id"].isin(product_ids).all()


def test_order_items_reference_existing_sellers():
    sellers = load_dataset("olist_sellers_dataset.csv")
    order_items = load_dataset("olist_order_items_dataset.csv")

    seller_ids = set(sellers["seller_id"])

    assert order_items["seller_id"].isin(seller_ids).all()


def test_payments_reference_existing_orders():
    orders = load_dataset("olist_orders_dataset.csv")
    payments = load_dataset("olist_order_payments_dataset.csv")

    order_ids = set(orders["order_id"])

    assert payments["order_id"].isin(order_ids).all()


def test_reviews_reference_existing_orders():
    orders = load_dataset("olist_orders_dataset.csv")
    reviews = load_dataset("olist_order_reviews_dataset.csv")

    order_ids = set(orders["order_id"])

    assert reviews["order_id"].isin(order_ids).all()


def test_order_status_values_are_valid():
    orders = load_dataset("olist_orders_dataset.csv")

    valid_statuses = {
        "delivered",
        "shipped",
        "canceled",
        "unavailable",
        "invoiced",
        "processing",
        "created",
        "approved",
    }

    assert set(orders["order_status"].dropna()).issubset(
        valid_statuses
    )


def test_review_scores_are_valid():
    reviews = load_dataset("olist_order_reviews_dataset.csv")

    assert reviews["review_score"].between(1, 5).all()


def test_order_prices_are_non_negative():
    order_items = load_dataset("olist_order_items_dataset.csv")

    assert (order_items["price"] >= 0).all()


def test_freight_values_are_non_negative():
    order_items = load_dataset("olist_order_items_dataset.csv")

    assert (order_items["freight_value"] >= 0).all()


def test_payment_values_are_non_negative():
    payments = load_dataset("olist_order_payments_dataset.csv")

    assert (payments["payment_value"] >= 0).all()

def test_order_dates_are_parseable():
    orders = load_dataset("olist_orders_dataset.csv")

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        parsed = pd.to_datetime(
            orders[column],
            errors="coerce",
        )

        invalid_count = (
            parsed.isna() & orders[column].notna()
        ).sum()

        assert invalid_count == 0, (
            f"{column} contains "
            f"{invalid_count} invalid dates"
        )


def test_review_dates_are_parseable():
    reviews = load_dataset("olist_order_reviews_dataset.csv")

    date_columns = [
        "review_creation_date",
        "review_answer_timestamp",
    ]

    for column in date_columns:
        parsed = pd.to_datetime(
            reviews[column],
            errors="coerce",
        )

        invalid_count = (
            parsed.isna() & reviews[column].notna()
        ).sum()

        assert invalid_count == 0, (
            f"{column} contains "
            f"{invalid_count} invalid dates"
        )


def test_shipping_dates_are_parseable():
    order_items = load_dataset(
        "olist_order_items_dataset.csv"
    )

    parsed = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce",
    )

    invalid_count = (
        parsed.isna()
        & order_items["shipping_limit_date"].notna()
    ).sum()

    assert invalid_count == 0