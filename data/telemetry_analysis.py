import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "data/processed/monaco_2025_norris_telemetry_clean.csv"
)


telemetry = pd.read_csv(INPUT_FILE)


max_speed = telemetry["Speed"].max()
average_speed = telemetry["Speed"].mean()

max_rpm = telemetry["RPM"].max()

average_throttle = telemetry["Throttle"].mean()

braking_percentage = (
    telemetry["Brake"].astype(bool).mean() * 100
)

total_distance = telemetry["Distance"].max()


print("=== NORRIS TELEMETRY ANALYSIS ===")

print(f"Maximum speed: {max_speed:.1f} km/h")
print(f"Average speed: {average_speed:.1f} km/h")
print(f"Maximum RPM: {max_rpm:.0f}")
print(f"Average throttle: {average_throttle:.1f}%")
print(f"Braking percentage: {braking_percentage:.1f}%")
print(f"Distance covered: {total_distance:.1f} m")