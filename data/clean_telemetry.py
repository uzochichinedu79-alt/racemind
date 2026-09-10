import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/raw/monaco_2025_norris_telemetry.csv")
OUTPUT_FILE = Path("data/processed/monaco_2025_norris_telemetry_clean.csv")


print("Loading telemetry...")

telemetry = pd.read_csv(INPUT_FILE)


# Keep the measurements RaceMind needs for analysis
telemetry = telemetry[
    [
        "Time",
        "Speed",
        "RPM",
        "nGear",
        "Throttle",
        "Brake",
        "DRS",
        "Distance",
        "RelativeDistance",
        "X",
        "Y",
        "Z",
    ]
]


# Remove rows with missing values
telemetry = telemetry.dropna()


# Sort by distance around the circuit
telemetry = telemetry.sort_values("Distance")


# Reset row numbers
telemetry = telemetry.reset_index(drop=True)


# Save cleaned telemetry
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

telemetry.to_csv(OUTPUT_FILE, index=False)


print(f"Clean telemetry rows: {len(telemetry)}")
print(f"Clean telemetry columns: {len(telemetry.columns)}")
print(f"Saved to: {OUTPUT_FILE}")