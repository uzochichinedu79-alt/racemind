import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/processed/monaco_2025_laps_clean.csv")
OUTPUT_FILE = Path("data/processed/monaco_2025_tyre_analysis.csv")


print("Loading cleaned lap data...")

laps = pd.read_csv(INPUT_FILE)


# Convert lap time to seconds
laps["LapTimeSeconds"] = pd.to_timedelta(
    laps["LapTime"]
).dt.total_seconds()


# Calculate average pace for each tyre compound
tyre_analysis = (
    laps.groupby("Compound")
    .agg(
        AverageLapTime=("LapTimeSeconds", "mean"),
        FastestLap=("LapTimeSeconds", "min"),
        AverageTyreLife=("TyreLife", "mean"),
        ValidLaps=("LapTimeSeconds", "count"),
    )
    .reset_index()
)


# Round values
tyre_analysis["AverageLapTime"] = tyre_analysis["AverageLapTime"].round(3)
tyre_analysis["FastestLap"] = tyre_analysis["FastestLap"].round(3)
tyre_analysis["AverageTyreLife"] = tyre_analysis["AverageTyreLife"].round(1)


# Sort by average lap time
tyre_analysis = tyre_analysis.sort_values("AverageLapTime")


print("\n=== TYRE ANALYSIS ===")
print(tyre_analysis.to_string(index=False))


# Save results
tyre_analysis.to_csv(OUTPUT_FILE, index=False)


print(f"\nSaved to: {OUTPUT_FILE}")