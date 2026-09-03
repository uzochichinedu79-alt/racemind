import pandas as pd
from pathlib import Path


RAW_FILE = Path("data/raw/monaco_2025_laps.csv")
PROCESSED_FILE = Path("data/processed/monaco_2025_laps_clean.csv")


print("Loading raw lap data...")

laps = pd.read_csv(RAW_FILE)


print(f"Raw rows: {len(laps)}")


# Convert time columns to pandas time values
time_columns = [
    "LapTime",
    "PitInTime",
    "PitOutTime",
    "Sector1Time",
    "Sector2Time",
    "Sector3Time",
]


for column in time_columns:
    laps[column] = pd.to_timedelta(laps[column], errors="coerce")


# Remove laps without a valid lap time
laps = laps.dropna(subset=["LapTime"])


# Keep only accurate laps
laps = laps[laps["IsAccurate"] == True]


# Sort the data
laps = laps.sort_values(["Driver", "LapNumber"])


# Save processed data
PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)

laps.to_csv(PROCESSED_FILE, index=False)


print(f"Clean rows: {len(laps)}")
print(f"Removed rows: {1425 - len(laps)}")
print(f"Saved to: {PROCESSED_FILE}")