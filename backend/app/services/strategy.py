import pandas as pd
from pathlib import Path

def calculate_strategy_time(
    laps: pd.DataFrame,
    driver: str,
    strategy: list[str],
) -> float:
    """
    Estimate race time for a proposed tyre strategy.

    The model uses:
    - The driver's historical average pace for each compound.
    - The driver's estimated degradation rate for each compound.
    - The number of laps assigned to each stint.
    """

    driver = driver.upper()

    driver_laps = laps[
        laps["Driver"] == driver
    ].copy()

    driver_laps["LapTimeSeconds"] = pd.to_timedelta(
        driver_laps["LapTime"]
    ).dt.total_seconds()

    if driver_laps.empty:
        raise ValueError(
            f"No valid lap data found for {driver}"
        )

    if not strategy:
        raise ValueError(
            "Strategy cannot be empty."
        )

    # Load degradation data.
    degradation_file = Path(
        "data/processed/monaco_2025_degradation_rates.csv"
    )

    degradation = pd.read_csv(
        degradation_file
    )

    driver_degradation = degradation[
        degradation["Driver"] == driver
    ]

    degradation_rates = dict(
        zip(
            driver_degradation["Compound"],
            driver_degradation["DegradationPerLap"],
        )
    )

    # Make sure we have pace data for every
    # compound in the proposed strategy.
    available_compounds = set(
        driver_laps["Compound"].dropna()
    )

    for compound in strategy:
        if compound not in available_compounds:
            raise ValueError(
                f"No pace data available for {compound}"
            )

    # Count the actual valid laps in each real stint.
    actual_stints = (
        driver_laps.groupby("Stint")
        .size()
        .tolist()
    )

    total_laps = len(driver_laps)

    # If proposed strategy has the same number
    # of stints as the actual race strategy,
    # preserve the actual stint lengths.
    if len(strategy) == len(actual_stints):

        stint_lengths = actual_stints

    else:

        base_length = (
            total_laps // len(strategy)
        )

        remainder = (
            total_laps % len(strategy)
        )

        stint_lengths = []

        for i in range(len(strategy)):

            length = base_length

            if i == len(strategy) - 1:
                length += remainder

            stint_lengths.append(length)

    total_time = 0.0

    # Simulate every lap of every proposed stint.
    for compound, stint_laps in zip(
        strategy,
        stint_lengths,
    ):

        compound_laps = driver_laps[
            driver_laps["Compound"] == compound
        ]

        average_pace = (
            compound_laps["LapTimeSeconds"].mean()
        )

        average_tyre_age = (
            compound_laps["TyreLife"].mean()
        )

        degradation_rate = degradation_rates.get(
            compound,
            0.0
        )

        for tyre_age in range(
            1,
            stint_laps + 1
        ):

            predicted_lap_time = (
                average_pace
                + degradation_rate
                * (
                    tyre_age
                    - average_tyre_age
                )
            )

            total_time += predicted_lap_time

    return round(total_time, 3)

def compare_strategies(
    laps: pd.DataFrame,
    driver: str,
    strategies: dict[str, list[str]],
) -> pd.DataFrame:
    results = []

    for name, strategy in strategies.items():
        estimated_time = calculate_strategy_time(
            laps,
            driver,
            strategy,
        )

        results.append(
            {
                "Strategy": name,
                "Tyres": " → ".join(strategy),
                "EstimatedRaceTime": estimated_time,
            }
        )

    comparison = pd.DataFrame(results)

    comparison["TimeDifference"] = (
        comparison["EstimatedRaceTime"]
        - comparison["EstimatedRaceTime"].min()
    ).round(3)

    return comparison.sort_values(
        "EstimatedRaceTime"
    )

def calculate_strategy_time(
    laps: pd.DataFrame,
    driver: str,
    strategy: list[str],
) -> float:
    """
    Estimate race time for a proposed tyre strategy.

    The model uses:
    - Historical compound pace.
    - Historical degradation rate.
    - Actual valid race-lap counts.
    - Observed maximum tyre life for each compound.

    Strategies that require tyre ages beyond the driver's
    observed data are rejected rather than extrapolated.
    """

    driver = driver.upper()

    driver_laps = laps[
        laps["Driver"] == driver
    ].copy()

    driver_laps["LapTimeSeconds"] = pd.to_timedelta(
        driver_laps["LapTime"]
    ).dt.total_seconds()

    if driver_laps.empty:
        raise ValueError(
            f"No valid lap data found for {driver}"
        )

    if not strategy:
        raise ValueError(
            "Strategy cannot be empty."
        )

    # Load degradation rates.
    degradation_file = Path(
        "data/processed/monaco_2025_degradation_rates.csv"
    )

    degradation = pd.read_csv(
        degradation_file
    )

    driver_degradation = degradation[
        degradation["Driver"] == driver
    ]

    degradation_rates = dict(
        zip(
            driver_degradation["Compound"],
            driver_degradation["DegradationPerLap"],
        )
    )

    # Check that every proposed compound exists
    # in the driver's historical data.
    available_compounds = set(
        driver_laps["Compound"].dropna()
    )

    for compound in strategy:

        if compound not in available_compounds:

            raise ValueError(
                f"No pace data available for {compound}"
            )

    # Count actual valid laps in the driver's
    # real stints.
    actual_stints = (
        driver_laps.groupby("Stint")
        .size()
        .tolist()
    )

    total_laps = len(driver_laps)

    # Preserve actual stint lengths when the proposed
    # strategy has the same number of stints.
    if len(strategy) == len(actual_stints):

        stint_lengths = actual_stints

    else:

        base_length = (
            total_laps // len(strategy)
        )

        remainder = (
            total_laps % len(strategy)
        )

        stint_lengths = []

        for i in range(len(strategy)):

            length = base_length

            if i == len(strategy) - 1:
                length += remainder

            stint_lengths.append(length)

    total_time = 0.0

    for compound, stint_laps in zip(
        strategy,
        stint_lengths,
    ):

        compound_laps = driver_laps[
            driver_laps["Compound"] == compound
        ]

        # Find the maximum tyre age actually observed
        # for this driver and compound.
        maximum_tyre_life = (
            compound_laps["TyreLife"].max()
        )

        # Reject unsupported extrapolation.
        if stint_laps > maximum_tyre_life:

            raise ValueError(
                f"{driver} has only demonstrated "
                f"{maximum_tyre_life:.0f} laps on "
                f"{compound}, but this strategy requires "
                f"{stint_laps} laps."
            )

        average_pace = (
            compound_laps["LapTimeSeconds"].mean()
        )

        average_tyre_age = (
            compound_laps["TyreLife"].mean()
        )

        degradation_rate = degradation_rates.get(
            compound,
            0.0
        )

        # Estimate pace at tyre age 0.
        baseline_pace = (
            average_pace
            - (
                degradation_rate
                * average_tyre_age
            )
        )

        for tyre_age in range(
            1,
            stint_laps + 1
        ):

            predicted_lap_time = (
                baseline_pace
                + (
                    degradation_rate
                    * tyre_age
                )
            )

            total_time += predicted_lap_time

    return round(total_time, 3)

def explain_strategy(
    laps: pd.DataFrame,
    driver: str,
    strategy: list[str],
) -> pd.DataFrame:
    """
    Break a proposed strategy into individual stints.

    Returns the estimated time for each stint so we can
    understand how the total strategy time was calculated.
    """

    driver = driver.upper()

    driver_laps = laps[
        laps["Driver"] == driver
    ].copy()

    driver_laps["LapTimeSeconds"] = pd.to_timedelta(
        driver_laps["LapTime"]
    ).dt.total_seconds()

    if driver_laps.empty:
        raise ValueError(
            f"No valid lap data found for {driver}"
        )

    degradation_file = Path(
        "data/processed/monaco_2025_degradation_rates.csv"
    )

    degradation = pd.read_csv(
        degradation_file
    )

    driver_degradation = degradation[
        degradation["Driver"] == driver
    ]

    degradation_rates = dict(
        zip(
            driver_degradation["Compound"],
            driver_degradation["DegradationPerLap"],
        )
    )

    # Count the actual valid laps in the driver's
    # real stints.
    actual_stints = (
        driver_laps.groupby("Stint")
        .size()
        .tolist()
    )

    total_laps = len(driver_laps)

    if len(strategy) == len(actual_stints):

        stint_lengths = actual_stints

    else:

        base_length = (
            total_laps // len(strategy)
        )

        remainder = (
            total_laps % len(strategy)
        )

        stint_lengths = []

        for i in range(len(strategy)):

            length = base_length

            if i == len(strategy) - 1:
                length += remainder

            stint_lengths.append(length)

    results = []

    for stint_number, (compound, stint_laps) in enumerate(
        zip(strategy, stint_lengths),
        start=1,
    ):

        compound_laps = driver_laps[
            driver_laps["Compound"] == compound
        ]

        average_pace = (
            compound_laps["LapTimeSeconds"].mean()
        )

        average_tyre_age = (
            compound_laps["TyreLife"].mean()
        )

        degradation_rate = degradation_rates.get(
            compound,
            0.0
        )

        baseline_pace = (
            average_pace
            - (
                degradation_rate
                * average_tyre_age
            )
        )

        stint_time = 0.0

        for tyre_age in range(
            1,
            stint_laps + 1
        ):

            predicted_lap_time = (
                baseline_pace
                + (
                    degradation_rate
                    * tyre_age
                )
            )

            stint_time += predicted_lap_time

        results.append(
            {
                "Stint": stint_number,
                "Compound": compound,
                "Laps": stint_laps,
                "DegradationPerLap": degradation_rate,
                "EstimatedStintTime": round(
                    stint_time,
                    3,
                ),
            }
        )

    breakdown = pd.DataFrame(results)

    breakdown["CumulativeTime"] = (
        breakdown["EstimatedStintTime"]
        .cumsum()
        .round(3)
    )

    return breakdown