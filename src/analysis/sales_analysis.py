from pathlib import Path

import pandas as pd


def load_orders(data_path: str | Path) -> pd.DataFrame:
    """Load the raw orders dataset and parse timestamp columns."""
    df = pd.read_csv(data_path)

    timestamp_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in timestamp_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def load_order_items(data_path: str | Path) -> pd.DataFrame:
    """Load order items and calculate item-level total value."""
    df = pd.read_csv(data_path)

    df["item_total_value"] = df["price"] + df["freight_value"]

    return df


def calculate_monthly_sales(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate monthly order and revenue metrics.

    Revenue is based on order-item merchandise value plus freight.
    """
    item_summary = (
        order_items.groupby("order_id", as_index=False)
        .agg(
            merchandise_revenue=("price", "sum"),
            freight_revenue=("freight_value", "sum"),
            total_order_value=("item_total_value", "sum"),
            item_count=("order_item_id", "count"),
        )
    )

    df = orders[
        ["order_id", "order_purchase_timestamp"]
    ].merge(
        item_summary,
        on="order_id",
        how="left",
    )

    df["sales_month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly = (
        df.groupby("sales_month", as_index=False)
        .agg(
            order_count=("order_id", "count"),
            merchandise_revenue=("merchandise_revenue", "sum"),
            freight_revenue=("freight_revenue", "sum"),
            total_revenue=("total_order_value", "sum"),
            average_order_value=("total_order_value", "mean"),
            average_items_per_order=("item_count", "mean"),
        )
        .sort_values("sales_month")
    )

    return monthly


def calculate_category_sales(
    order_items: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate merchandise revenue and order metrics by product category."""
    products = products[
        ["product_id", "product_category_name"]
    ].copy()

    df = order_items.merge(
        products,
        on="product_id",
        how="left",
    )

    df["product_category_name"] = df["product_category_name"].fillna(
        "Unknown"
    )

    category_sales = (
        df.groupby("product_category_name", as_index=False)
        .agg(
            item_count=("order_id", "count"),
            order_count=("order_id", "nunique"),
            product_count=("product_id", "nunique"),
            merchandise_revenue=("price", "sum"),
            freight_revenue=("freight_value", "sum"),
            total_item_value=("item_total_value", "sum"),
            average_item_price=("price", "mean"),
        )
        .sort_values(
            "merchandise_revenue",
            ascending=False,
        )
    )

    return category_sales


def calculate_delivery_metrics(orders: pd.DataFrame) -> dict:
    """
    Calculate overall delivery performance.

    Late delivery rate is calculated only among delivered orders
    that can be classified as on-time or late.
    """
    delivered = orders[
        orders["order_delivered_customer_date"].notna()
    ].copy()

    delivered["delivery_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    delivered["delivery_vs_estimated_days"] = (
        delivered["order_delivered_customer_date"]
        - delivered["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    delivered["delivery_performance"] = delivered[
        "delivery_vs_estimated_days"
    ].apply(
        lambda x: "On Time" if x <= 0 else "Late"
    )

    on_time_orders = (
        delivered["delivery_performance"] == "On Time"
    ).sum()

    late_orders = (
        delivered["delivery_performance"] == "Late"
    ).sum()

    classified_orders = on_time_orders + late_orders

    late_delivery_rate = (
        late_orders / classified_orders
        if classified_orders
        else 0
    )

    return {
        "delivered_orders": len(delivered),
        "on_time_orders": int(on_time_orders),
        "late_orders": int(late_orders),
        "late_delivery_rate": late_delivery_rate,
        "average_delivery_days": delivered["delivery_days"].mean(),
        "average_delivery_vs_estimated_days": (
            delivered["delivery_vs_estimated_days"].mean()
        ),
    }


def calculate_customer_behavior(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Calculate customer-level order frequency and value."""
    customer_orders = orders[
        ["order_id", "customer_id", "order_purchase_timestamp"]
    ].merge(
        customers[
            [
                "customer_id",
                "customer_unique_id",
                "customer_city",
                "customer_state",
            ]
        ],
        on="customer_id",
        how="inner",
    )

    customer_behavior = (
        customer_orders.groupby(
            "customer_unique_id",
            as_index=False,
        )
        .agg(
            order_count=("order_id", "nunique"),
            first_order_date=(
                "order_purchase_timestamp",
                "min",
            ),
            last_order_date=(
                "order_purchase_timestamp",
                "max",
            ),
            customer_city=("customer_city", "first"),
            customer_state=("customer_state", "first"),
        )
    )

    customer_behavior["customer_segment"] = pd.cut(
        customer_behavior["order_count"],
        bins=[0, 1, 3, float("inf")],
        labels=[
            "One-Time Customer",
            "Repeat Customer",
            "Frequent Customer",
        ],
    )

    return customer_behavior


if __name__ == "__main__":
    print("RetailPulse sales analysis module loaded successfully.")