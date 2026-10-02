from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_dataset(filename: str) -> pd.DataFrame:
    path = RAW_DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


def check_unique_key(
    df: pd.DataFrame,
    column: str,
    dataset_name: str,
) -> bool:
    duplicates = df[column].duplicated().sum()

    print(
        f"{dataset_name}.{column}: "
        f"{duplicates:,} duplicate values"
    )

    return duplicates == 0


def check_foreign_key(
    child_df: pd.DataFrame,
    child_column: str,
    parent_df: pd.DataFrame,
    parent_column: str,
    relationship_name: str,
) -> bool:
    child_values = set(child_df[child_column].dropna())
    parent_values = set(parent_df[parent_column].dropna())

    missing_values = child_values - parent_values

    print(
        f"{relationship_name}: "
        f"{len(missing_values):,} unmatched values"
    )

    return len(missing_values) == 0


def check_nulls(
    df: pd.DataFrame,
    dataset_name: str,
) -> bool:
    null_counts = df.isna().sum()
    null_counts = null_counts[null_counts > 0]

    print(f"{dataset_name}: ")

    if null_counts.empty:
        print("  No missing values")
        return True

    print(null_counts.to_string())
    return True


def check_order_status(df: pd.DataFrame) -> bool:
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

    actual_statuses = set(df["order_status"].dropna().unique())

    invalid_statuses = actual_statuses - valid_statuses

    print(
        f"orders.order_status: "
        f"{len(invalid_statuses):,} invalid values"
    )

    if invalid_statuses:
        print(f"  Invalid: {invalid_statuses}")

    return len(invalid_statuses) == 0


def check_review_scores(df: pd.DataFrame) -> bool:
    invalid_scores = df[
        ~df["review_score"].between(1, 5)
    ]

    print(
        f"reviews.review_score: "
        f"{len(invalid_scores):,} invalid values"
    )

    return len(invalid_scores) == 0


def check_non_negative_values(
    df: pd.DataFrame,
    column: str,
    dataset_name: str,
) -> bool:
    invalid = df[df[column] < 0]

    print(
        f"{dataset_name}.{column}: "
        f"{len(invalid):,} negative values"
    )

    return len(invalid) == 0


def main():
    print("=" * 80)
    print("RETAILPULSE DATA VALIDATION")
    print("=" * 80)

    customers = load_dataset(
        "olist_customers_dataset.csv"
    )

    orders = load_dataset(
        "olist_orders_dataset.csv"
    )

    order_items = load_dataset(
        "olist_order_items_dataset.csv"
    )

    order_payments = load_dataset(
        "olist_order_payments_dataset.csv"
    )

    reviews = load_dataset(
        "olist_order_reviews_dataset.csv"
    )

    products = load_dataset(
        "olist_products_dataset.csv"
    )

    sellers = load_dataset(
        "olist_sellers_dataset.csv"
    )

    print("\n--- PRIMARY KEY CHECKS ---")

    check_unique_key(
        customers,
        "customer_id",
        "customers",
    )

    check_unique_key(
        orders,
        "order_id",
        "orders",
    )

    check_unique_key(
        products,
        "product_id",
        "products",
    )

    check_unique_key(
        sellers,
        "seller_id",
        "sellers",
    )

    print("\n--- FOREIGN KEY CHECKS ---")

    check_foreign_key(
        orders,
        "customer_id",
        customers,
        "customer_id",
        "orders.customer_id -> customers.customer_id",
    )

    check_foreign_key(
        order_items,
        "order_id",
        orders,
        "order_id",
        "order_items.order_id -> orders.order_id",
    )

    check_foreign_key(
        order_items,
        "product_id",
        products,
        "product_id",
        "order_items.product_id -> products.product_id",
    )

    check_foreign_key(
        order_items,
        "seller_id",
        sellers,
        "seller_id",
        "order_items.seller_id -> sellers.seller_id",
    )

    check_foreign_key(
        order_payments,
        "order_id",
        orders,
        "order_id",
        "payments.order_id -> orders.order_id",
    )

    check_foreign_key(
        reviews,
        "order_id",
        orders,
        "order_id",
        "reviews.order_id -> orders.order_id",
    )

    print("\n--- DOMAIN CHECKS ---")

    check_order_status(orders)

    check_review_scores(reviews)

    check_non_negative_values(
        order_items,
        "price",
        "order_items",
    )

    check_non_negative_values(
        order_items,
        "freight_value",
        "order_items",
    )

    check_non_negative_values(
        order_payments,
        "payment_value",
        "order_payments",
    )

    print("\n--- NULL CHECKS ---")

    check_nulls(
        orders,
        "orders",
    )

    check_nulls(
        products,
        "products",
    )

    check_nulls(
        reviews,
        "reviews",
    )

    print("\nValidation completed.")


if __name__ == "__main__":
    main()