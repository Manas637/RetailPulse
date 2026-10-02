import matplotlib

matplotlib.use("Agg")

import pandas as pd

from src.visualization.sales_charts import (
    plot_category_revenue,
    plot_customer_segments,
    plot_monthly_revenue,
)


def test_plot_monthly_revenue():
    data = pd.DataFrame(
        {
            "sales_month": pd.to_datetime(
                ["2018-01-01", "2018-02-01"]
            ),
            "total_revenue": [1000, 1500],
        }
    )

    plot_monthly_revenue(data)


def test_plot_category_revenue():
    data = pd.DataFrame(
        {
            "product_category_name": [
                "electronics",
                "furniture",
            ],
            "merchandise_revenue": [1000, 500],
        }
    )

    plot_category_revenue(data, top_n=2)


def test_plot_customer_segments():
    data = pd.DataFrame(
        {
            "customer_segment": [
                "One-Time Customer",
                "One-Time Customer",
                "Repeat Customer",
            ]
        }
    )

    plot_customer_segments(data)