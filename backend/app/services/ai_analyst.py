from pathlib import Path
import pandas as pd

from app.services.strategy import (
    calculate_strategy_time,
    explain_strategy,
)

from app.services.analytics import (
    calculate_driver_pace,
    calculate_driver_consistency,
    calculate_stint_summary,
)
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text

def build_race_prompt(driver_a: str, driver_b: str, pace_data: str) -> str:
    prompt = f"""
You are RaceMind, an AI Formula 1 race strategy analyst.

Analyse the following race data from the 2025 Monaco Grand Prix.
Driver comparison:
{driver_a}
{driver_b}

Pace data:
{pace_data}

Explain:
1. Which driver had better average pace.
2. Which driver had the faster fastest lap.
3. What the pace difference suggests.
4. Any important limitations in the data.

Keep the analysis concise, technical, and easy to understand.
Do not invent information that is not present in the data."""

    return prompt

def analyze_race(driver_a: str, driver_b: str, pace_data: str) -> str:
    prompt = build_race_prompt(
        driver_a,
        driver_b,
        pace_data,
    )

    return ask_gemini(prompt)

def get_driver_analysis(driver_a: str, driver_b: str) -> str:
    laps_file = Path("data/processed/monaco_2025_laps_clean.csv")

    laps = pd.read_csv(laps_file)

    pace = calculate_driver_pace(laps)
    consistency = calculate_driver_consistency(laps)

    drivers = [driver_a.upper(), driver_b.upper()]

    pace_data = pace[
        pace["Driver"].isin(drivers)
    ]

    consistency_data = consistency[
        consistency["Driver"].isin(drivers)
    ][
        ["Driver", "LapTimeStdDev"]
    ]

    analysis = pace_data.merge(
        consistency_data,
        on="Driver",
        how="left",
    )

    return analysis.to_string(index=False)

def get_stint_analysis(driver_a: str, driver_b: str) -> str:
    laps_file = Path("data/processed/monaco_2025_laps_clean.csv")

    laps = pd.read_csv(laps_file)

    stints = calculate_stint_summary(laps)

    drivers = [driver_a.upper(), driver_b.upper()]

    driver_stints = stints[
        stints["Driver"].isin(drivers)
    ]

    return driver_stints.to_string(index=False)

def get_pit_stop_analysis(driver_a: str, driver_b: str) -> str:
    pit_stops_file = Path("data/raw/monaco_2025_pit_stops.csv")

    pit_stops = pd.read_csv(pit_stops_file)

    drivers = [driver_a.upper(), driver_b.upper()]

    driver_pit_stops = pit_stops[
        pit_stops["Driver"].isin(drivers)
    ]

    return driver_pit_stops.to_string(index=False)

def get_degradation_analysis(driver_a: str, driver_b: str) -> str:
    degradation_file = Path(
        "data/processed/monaco_2025_degradation_rates.csv"
    )

    degradation = pd.read_csv(degradation_file)

    drivers = [driver_a.upper(), driver_b.upper()]

    driver_degradation = degradation[
        degradation["Driver"].isin(drivers)
    ]

    return driver_degradation.to_string(index=False)

def get_full_race_context(driver_a: str, driver_b: str) -> str:
    pace = get_driver_analysis(driver_a, driver_b)
    stints = get_stint_analysis(driver_a, driver_b)
    pit_stops = get_pit_stop_analysis(driver_a, driver_b)
    degradation = get_degradation_analysis(driver_a, driver_b)

    return f"""
=== DRIVER PACE & CONSISTENCY ===
{pace}

=== STINTS ===
{stints}

=== PIT STOPS ===
{pit_stops}

=== TYRE DEGRADATION ===
{degradation}
"""

def analyze_driver_comparison(driver_a: str, driver_b: str) -> str:
    race_context = get_full_race_context(driver_a, driver_b)

    prompt = f"""
You are RaceMind, an AI Formula 1 race strategy analyst.

Analyse the following real race data from the 2025 Monaco Grand Prix.
This data comes specifically from the Monaco Grand Prix Race session.

{race_context}

Provide:

1. Pace comparison
2. Consistency comparison
3. Stint strategy comparison
4. Pit-stop comparison
5. Tyre degradation comparison
6. Overall strategic assessment
7. Important limitations

Rules:
- Only make claims supported by the supplied data.
- Do not invent race events, Safety Cars, traffic, fuel loads, or driver decisions.
- Negative degradation values mean the measured lap-time trend decreased with tyre age; they do NOT automatically prove that the tyre became faster.
- Treat the degradation values as estimated trends because fuel, traffic, and track evolution are not controlled for.
- Keep the analysis concise, technical, and easy to understand.
"""

    return ask_gemini(prompt)

def analyze_strategy(
    driver: str,
    strategies: dict[str, list[str]],
) -> str:
    """
    Compare proposed strategies using the strategy engine,
    then ask Gemini to explain the results.
    """

    laps_file = Path(
        "data/processed/monaco_2025_laps_clean.csv"
    )

    laps = pd.read_csv(laps_file)

    strategy_results = []

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

            strategy_results.append(
                f"""
STRATEGY: {name}

Tyres:
{" → ".join(strategy)}

Estimated race time:
{estimated_time} seconds

Breakdown:
{breakdown.to_string(index=False)}
"""

            )

        except ValueError as error:

            strategy_results.append(
                f"""
STRATEGY: {name}

Tyres:
{" → ".join(strategy)}

STATUS:
Rejected by the simulation model.

REASON:
{error}
"""
            )

    strategy_context = "\n".join(
        strategy_results
    )

    prompt = f"""
You are RaceMind, an AI Formula 1 race strategy analyst.

Analyse the following strategy simulation for
{driver.upper()} at the 2025 Monaco Grand Prix.

The Python strategy engine produced these results:

{strategy_context}

Your job is to explain the simulation results clearly.

Provide:

1. Strategy comparison
2. Which strategies were successfully simulated
3. Which strategies were rejected and why
4. The estimated time difference between valid strategies
5. The strategic implication
6. Important limitations

Rules:

- Treat the Python calculations as authoritative.
- Do not invent strategies or race events.
- Do not invent Safety Cars, traffic, fuel loads,
  weather, driver decisions, or pit-stop losses.
- A rejected strategy means the available data does not
  support that simulation.
- Do not describe an estimated time as an actual race result.
- Explain that degradation rates are observational trends
  affected by fuel load, traffic, and track evolution.
- Keep the explanation technical but easy to understand.
"""

    return ask_gemini(prompt)