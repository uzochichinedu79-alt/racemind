import pandas as pd


RESULTS_FILE = "data/raw/monaco_2025_results.csv"
LAPS_FILE = "data/raw/monaco_2025_laps.csv"


results = pd.read_csv(RESULTS_FILE)
laps = pd.read_csv(LAPS_FILE)


print("=== RESULTS ===")
print(results)

print("\n=== DATASET SIZE ===")
print(f"Results: {results.shape}")
print(f"Laps: {laps.shape}")

print("\n=== DRIVERS ===")
print(laps["Driver"].unique())

print("\n=== TYRE COMPOUNDS ===")
print(laps["Compound"].value_counts())

print("\n=== LAPS PER DRIVER ===")
print(laps["Driver"].value_counts())

print("\n=== MISSING VALUES ===")
print(laps.isna().sum())