import pandas as pd


def calculate_driver_pace(laps: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average and fastest lap time for each driver.
    """

    laps = laps.copy()

    laps["LapTimeSeconds"] = pd.to_timedelta(
        laps["LapTime"]
    ).dt.total_seconds()

    pace = (
        laps.groupby("Driver")
        .agg(
            AverageLapTime=("LapTimeSeconds", "mean"),
            FastestLap=("LapTimeSeconds", "min"),
            ValidLaps=("LapTimeSeconds", "count"),
        )
        .reset_index()
    )

    pace["AverageLapTime"] = pace["AverageLapTime"].round(3)
    pace["FastestLap"] = pace["FastestLap"].round(3)

    return pace.sort_values("AverageLapTime")


def calculate_stint_summary(laps: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate tyre stint information for each driver.
    """

    stint_summary = (
        laps.groupby(["Driver", "Stint", "Compound"])
        .agg(
            StartLap=("LapNumber", "min"),
            EndLap=("LapNumber", "max"),
            Laps=("LapNumber", "count"),
            AverageTyreLife=("TyreLife", "mean"),
        )
        .reset_index()
    )

    stint_summary["AverageTyreLife"] = (
        stint_summary["AverageTyreLife"].round(1)
    )

    return stint_summary


def calculate_driver_consistency(
    laps: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measure how consistent each driver's lap times were.

    Lower standard deviation = more consistent lap times.
    """

    laps = laps.copy()

    laps["LapTimeSeconds"] = pd.to_timedelta(
        laps["LapTime"]
    ).dt.total_seconds()

    consistency = (
        laps.groupby("Driver")
        .agg(
            AverageLapTime=("LapTimeSeconds", "mean"),
            LapTimeStdDev=("LapTimeSeconds", "std"),
            ValidLaps=("LapTimeSeconds", "count"),
        )
        .reset_index()
    )

    consistency["AverageLapTime"] = (
        consistency["AverageLapTime"].round(3)
    )

    consistency["LapTimeStdDev"] = (
        consistency["LapTimeStdDev"].round(3)
    )

    return consistency.sort_values("LapTimeStdDev")