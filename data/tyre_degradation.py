import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "data/processed/monaco_2025_laps_clean.csv"
)

OUTPUT_FILE = Path(
    "data/processed/monaco_2025_tyre_degradation.csv"
)


laps = pd.read_csv(INPUT_FILE)

laps["LapTimeSeconds"] = pd.to_timedelta(
    laps["LapTime"]
).dt.total_seconds()


degradation = (
    laps.groupby(["Driver", "Compound"])
    .agg(
        AverageLapTime=("LapTimeSeconds", "mean"),
        AverageTyreLife=("TyreLife", "mean"),
        ValidLaps=("LapTimeSeconds", "count"),
    )
    .reset_index()
)


degradation["AverageLapTime"] = (
    degradation["AverageLapTime"].round(3)
)

degradation["AverageTyreLife"] = (
    degradation["AverageTyreLife"].round(1)
)


degradation = degradation.sort_values(
    ["Driver", "Compound"]
)


degradation.to_csv(
    OUTPUT_FILE,
    index=False
)


print("=== TYRE DEGRADATION ANALYSIS ===")

print(
    degradation.to_string(index=False)
)

print(
    f"\nRows: {len(degradation)}"
)

print(
    f"Saved to: {OUTPUT_FILE}"
)