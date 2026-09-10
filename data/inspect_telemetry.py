import pandas as pd


FILE = "data/raw/monaco_2025_norris_telemetry.csv"


telemetry = pd.read_csv(FILE)


print("=== TELEMETRY COLUMNS ===")
print(telemetry.columns.tolist())


print("\n=== DATASET SIZE ===")
print(f"Rows: {telemetry.shape[0]}")
print(f"Columns: {telemetry.shape[1]}")


print("\n=== FIRST 5 ROWS ===")
print(telemetry.head())


print("\n=== MISSING VALUES ===")
print(telemetry.isna().sum())