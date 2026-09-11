import pandas as pd

from app.services.analytics import (
    calculate_driver_pace,
    calculate_stint_summary,
    calculate_driver_consistency,
)


FILE = "data/processed/monaco_2025_laps_clean.csv"

laps = pd.read_csv(FILE)


print("=== DRIVER PACE ===")

pace = calculate_driver_pace(laps)

print(pace.to_string(index=False))


print("\n=== STINT SUMMARY ===")

stints = calculate_stint_summary(laps)

print(stints.to_string(index=False))


print("\n=== DRIVER CONSISTENCY ===")

consistency = calculate_driver_consistency(laps)

print(consistency.to_string(index=False))