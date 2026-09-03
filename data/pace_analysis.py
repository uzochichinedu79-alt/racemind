import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/processed/monaco_2025_laps_clean.csv")
OUTPUT_FILE = Path("data/processed/monaco_2025_pace.csv")


print("Loading cleaned lap data...")

laps = pd.read_csv(INPUT_FILE)

# Convert lap time back into seconds
laps["LapTimeSeconds"] = pd.to_timedelta(
    laps["LapTime"]
).dt.total_seconds()


# Calculate driver pace
pace = (
    laps.groupby("Driver")
    .agg(
        AverageLapTime=("LapTimeSeconds", "mean"),
        FastestLap=("LapTimeSeconds", "min"),
        ValidLaps=("LapTimeSeconds", "count"),
    )
    .reset_index()
)


# Round times for easier reading
pace["AverageLapTime"] = pace["AverageLapTime"].round(3)
pace["FastestLap"] = pace["FastestLap"].round(3)


# Sort fastest average pace first
pace = pace.sort_values("AverageLapTime")


# Save results
pace.to_csv(OUTPUT_FILE, index=False)


print("\n=== DRIVER PACE ===")
print(pace.to_string(index=False))s
print(f"\nSaved to: {OUTPUT_FILE}")