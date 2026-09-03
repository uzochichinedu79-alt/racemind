import fastf1
from pathlib import Path


YEAR = 2025
GRAND_PRIX = "Monaco"


DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


print("Loading F1 race data...")

session = fastf1.get_session(YEAR, GRAND_PRIX, "R")
session.load()

print("Race loaded successfully!")


results = session.results[
    [
        "Abbreviation",
        "FullName",
        "TeamName",
        "Position",
        "Points",
    ]
]

laps = session.laps[
    [
        "Driver",
        "DriverNumber",
        "LapNumber",
        "LapTime",
        "Stint",
        "Compound",
        "TyreLife",
        "PitInTime",
        "PitOutTime",
        "Sector1Time",
        "Sector2Time",
        "Sector3Time",
        "Position",
        "TrackStatus",
        "IsAccurate",
    ]
]


results.to_csv(DATA_DIR / "monaco_2025_results.csv", index=False)
laps.to_csv(DATA_DIR / "monaco_2025_laps.csv", index=False)


print("Race results saved.")
print("Lap data saved.")
print(f"Results rows: {len(results)}")
print(f"Lap rows: {len(laps)}")