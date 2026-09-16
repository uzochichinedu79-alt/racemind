from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from app.services.strategy import (
    calculate_strategy_time,
    explain_strategy,
)


router = APIRouter(
    prefix="/strategy",
    tags=["Strategy"],
)


@router.post("/compare/{driver}")
def compare_driver_strategies(
    driver: str,
    strategies: dict[str, list[str]],
):
    laps_file = Path(
        "data/processed/monaco_2025_laps_clean.csv"
    )

    laps = pd.read_csv(laps_file)

    results = []

    for name, strategy in strategies.items():
        try:
            estimated_time = calculate_strategy_time(
                laps,
                driver,
                strategy,
            )

            breakdown = explain_strategy(
                laps,
                driver,
                strategy,
            )

            results.append(
                {
                    "Strategy": name,
                    "Tyres": " → ".join(strategy),
                    "EstimatedRaceTime": estimated_time,
                    "Status": "Valid",
                    "Reason": None,
                    "Breakdown": breakdown.to_dict(
                        orient="records"
                    ),
                }
            )

        except ValueError as error:
            results.append(
                {
                    "Strategy": name,
                    "Tyres": " → ".join(strategy),
                    "EstimatedRaceTime": None,
                    "Status": "Rejected",
                    "Reason": str(error),
                    "Breakdown": [],
                }
            )

    valid_times = [
        result["EstimatedRaceTime"]
        for result in results
        if result["EstimatedRaceTime"] is not None
    ]

    if valid_times:
        fastest_time = min(valid_times)

        for result in results:
            if result["EstimatedRaceTime"] is not None:
                result["TimeDifference"] = round(
                    result["EstimatedRaceTime"]
                    - fastest_time,
                    3,
                )
            else:
                result["TimeDifference"] = None
    else:
        for result in results:
            result["TimeDifference"] = None

    return {
        "driver": driver.upper(),
        "strategies": results,
    }