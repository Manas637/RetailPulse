from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

csv_path = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "olist_order_reviews_dataset.csv"
)


df = pd.read_csv(csv_path)

print("=" * 70)
print("ORDER REVIEWS DUPLICATE CHECK")
print("=" * 70)

print(f"Rows: {len(df):,}")
print(f"Unique review IDs: {df['review_id'].nunique():,}")
print(
    f"Duplicate review IDs: "
    f"{df['review_id'].duplicated().sum():,}"
)

duplicates = (
    df[df["review_id"].duplicated(keep=False)]
    .sort_values("review_id")
)

print("\nDuplicate review IDs:")

if duplicates.empty:
    print("None")
else:
    print(
        duplicates[
            [
                "review_id",
                "order_id",
                "review_score",
            ]
        ].to_string(index=False)
    )