from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from app.services.analytics import calculate_driver_pace

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

@router.get("/pace")
def get_driver_pace():
    laps_file = Path(
        "data/processed/monaco_2025_laps_clean.csv"
    )

    laps = pd.read_csv(laps_file)

    pace = calculate_driver_pace(laps)

    return pace.to_dict(orient="records")