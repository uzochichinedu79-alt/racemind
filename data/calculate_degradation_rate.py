import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/processed/monaco_2025_laps_clean.csv")
OUTPUT_FILE = Path("data/processed/monaco_2025_degradation_rates.csv")

laps = pd.read_csv(INPUT_FILE)

laps["LapTimeSeconds"] = pd.to_timedelta(
    laps["LapTime"]
).dt.total_seconds()

results = []

for (driver, compound), group in laps.groupby(
    ["Driver", "Compound"]
):
    if len(group) < 10:
        continue

    x = group["TyreLife"]
    y = group["LapTimeSeconds"]

    # Calculate linear regression slope:
    # slope = change in lap time / change in tyre age
    slope = (
        ((x - x.mean()) * (y - y.mean())).sum()
        / ((x - x.mean()) ** 2).sum()
    )

    results.append(
        {
            "Driver": driver,
            "Compound": compound,
            "DegradationPerLap": slope,
            "ValidLaps": len(group),
        }
    )

degradation = pd.DataFrame(results)

degradation["DegradationPerLap"] = (
    degradation["DegradationPerLap"].round(4)
)

degradation = degradation.sort_values(
    "DegradationPerLap"
)

degradation.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=== TYRE DEGRADATION RATES ===")
print(degradation.to_string(index=False))

print(f"\nRows: {len(degradation)}")
print(f"Saved to: {OUTPUT_FILE}")