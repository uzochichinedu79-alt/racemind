from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from app.services.analytics import calculate_stint_summary


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/stints/{driver}")
def get_driver_stints(driver: str):
    laps_file = Path(
        "data/processed/monaco_2025_laps_clean.csv"
    )

    laps = pd.read_csv(laps_file)

    stints = calculate_stint_summary(laps)

    driver_stints = stints[
        stints["Driver"] == driver.upper()
    ]

    return driver_stints.to_dict(
        orient="records"
    )