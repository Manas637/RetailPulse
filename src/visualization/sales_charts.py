import matplotlib.pyplot as plt
import pandas as pd


def plot_monthly_revenue(
    monthly_sales: pd.DataFrame,
    output_path: str | None = None,
) -> None:
    """Plot monthly total revenue."""
    plt.figure(figsize=(12, 6))

    plt.plot(
        monthly_sales["sales_month"],
        monthly_sales["total_revenue"],
        marker="o",
    )

    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (BRL)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.show()


def plot_category_revenue(
    category_sales: pd.DataFrame,
    top_n: int = 10,
    output_path: str | None = None,
) -> None:
    """Plot top product categories by merchandise revenue."""
    top_categories = (
        category_sales
        .nlargest(top_n, "merchandise_revenue")
        .sort_values("merchandise_revenue")
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top_categories["product_category_name"],
        top_categories["merchandise_revenue"],
    )

    plt.title(
        f"Top {top_n} Product Categories by Merchandise Revenue"
    )
    plt.xlabel("Merchandise Revenue (BRL)")
    plt.ylabel("Product Category")
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.show()


def plot_customer_segments(
    customer_behavior: pd.DataFrame,
    output_path: str | None = None,
) -> None:
    """Plot customer counts by customer segment."""
    segment_counts = (
        customer_behavior["customer_segment"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(9, 5))

    plt.bar(
        segment_counts.index.astype(str),
        segment_counts.values,
    )

    plt.title("Customers by Segment")
    plt.xlabel("Customer Segment")
    plt.ylabel("Customer Count")
    plt.xticks(rotation=20)
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches="tight")

    plt.show()