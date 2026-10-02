import pandas as pd

from src.analysis.sales_analysis import (
    calculate_category_sales,
    calculate_customer_behavior,
    calculate_delivery_metrics,
    calculate_monthly_sales,
)


def test_calculate_monthly_sales():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_purchase_timestamp": pd.to_datetime(
                ["2018-01-10", "2018-01-20"]
            ),
        }
    )

    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2"],
            "order_item_id": [1, 1],
            "product_id": ["p1", "p2"],
            "price": [100.0, 200.0],
            "freight_value": [10.0, 20.0],
        }
    )

    order_items["item_total_value"] = (
        order_items["price"]
        + order_items["freight_value"]
    )

    result = calculate_monthly_sales(
        orders,
        order_items,
    )

    assert len(result) == 1
    assert result.iloc[0]["order_count"] == 2
    assert result.iloc[0]["merchandise_revenue"] == 300.0
    assert result.iloc[0]["freight_revenue"] == 30.0
    assert result.iloc[0]["total_revenue"] == 330.0
    assert result.iloc[0]["average_order_value"] == 165.0


def test_calculate_category_sales():
    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_item_id": [1, 1, 1],
            "product_id": ["p1", "p1", "p2"],
            "price": [100.0, 150.0, 200.0],
            "freight_value": [10.0, 15.0, 20.0],
        }
    )

    order_items["item_total_value"] = (
        order_items["price"]
        + order_items["freight_value"]
    )

    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2"],
            "product_category_name": [
                "electronics",
                "furniture",
            ],
        }
    )

    result = calculate_category_sales(
        order_items,
        products,
    )

    electronics = result[
        result["product_category_name"] == "electronics"
    ].iloc[0]

    assert electronics["order_count"] == 2
    assert electronics["merchandise_revenue"] == 250.0


def test_calculate_delivery_metrics():
    orders = pd.DataFrame(
        {
            "order_purchase_timestamp": pd.to_datetime(
                ["2018-01-01", "2018-01-01"]
            ),
            "order_delivered_customer_date": pd.to_datetime(
                ["2018-01-05", "2018-01-10"]
            ),
            "order_estimated_delivery_date": pd.to_datetime(
                ["2018-01-06", "2018-01-08"]
            ),
        }
    )

    result = calculate_delivery_metrics(orders)

    assert result["delivered_orders"] == 2
    assert result["on_time_orders"] == 1
    assert result["late_orders"] == 1
    assert result["late_delivery_rate"] == 0.5


def test_customer_segmentation():
    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3", "o4"],
            "customer_id": ["c1", "c2", "c2", "c3"],
            "order_purchase_timestamp": pd.to_datetime(
                [
                    "2018-01-01",
                    "2018-01-02",
                    "2018-02-02",
                    "2018-01-03",
                ]
            ),
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": ["c1", "c2", "c3"],
            "customer_unique_id": ["u1", "u2", "u3"],
            "customer_city": ["A", "B", "C"],
            "customer_state": ["SP", "RJ", "MG"],
        }
    )

    result = calculate_customer_behavior(
        orders,
        customers,
    )

    u1 = result[result["customer_unique_id"] == "u1"].iloc[0]
    u2 = result[result["customer_unique_id"] == "u2"].iloc[0]

    assert u1["order_count"] == 1
    assert u1["customer_segment"] == "One-Time Customer"

    assert u2["order_count"] == 2
    assert u2["customer_segment"] == "Repeat Customer"