import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

raw_file = project_root / "data" / "raw" / "Global Superstore Data.xlsx"
processed_dir = project_root / "data" / "processed"
processed_dir.mkdir(parents=True, exist_ok=True)

excel_file = pd.ExcelFile(raw_file)

print("Sheet names:")
print(excel_file.sheet_names)

orders = pd.read_excel(excel_file, sheet_name="Orders")
returns = pd.read_excel(excel_file, sheet_name="Returns")
people = pd.read_excel(excel_file, sheet_name="People")

print("\nShapes:")
print("Orders:", orders.shape)
print("Returns:", returns.shape)
print("People:", people.shape)

orders.to_csv(processed_dir / "orders_raw_export.csv", index=False)
returns.to_csv(processed_dir / "returns_raw_export.csv", index=False)
people.to_csv(processed_dir / "people_raw_export.csv", index=False)

print("\nCSV files exported successfully to data/processed/")