import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
processed_dir = project_root / "data" / "processed"

orders_file = processed_dir / "orders_raw_export.csv"
returns_file = processed_dir / "returns_raw_export.csv"
people_file = processed_dir / "people_raw_export.csv"

orders = pd.read_csv(orders_file)
returns = pd.read_csv(returns_file)
people = pd.read_csv(people_file)


def clean_column_names(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
    )
    return df


def strip_text_columns(df):
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for col in text_cols:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    return df

orders = clean_column_names(orders)
returns = clean_column_names(returns)
people = clean_column_names(people)

orders = strip_text_columns(orders)
returns = strip_text_columns(returns)
people = strip_text_columns(people)

orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
orders["ship_date"] = pd.to_datetime(orders["ship_date"], errors="coerce")

orders = orders.drop_duplicates()
returns = returns.drop_duplicates()
people = people.drop_duplicates()

print("Shapes after cleaning:")
print("Orders:", orders.shape)
print("Returns:", returns.shape)
print("People:", people.shape)

print("\nMissing values in Orders:")
missing_orders = orders.isnull().sum()
print(missing_orders[missing_orders > 0])

print("\nOrders dtypes:")
print(orders.dtypes)

orders.to_csv(processed_dir / "orders_clean.csv", index=False)
returns.to_csv(processed_dir / "returns_clean.csv", index=False)
people.to_csv(processed_dir / "people_clean.csv", index=False)

print("\nClean files saved successfully to data/processed/")