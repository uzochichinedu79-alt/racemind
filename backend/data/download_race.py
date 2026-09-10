session = fastf1.get_session(YEAR, GRAND_PRIX, "R")
session.load()

print("Loading telemetry...")

telemetry = session.laps.pick_drivers(["NOR"]).pick_fastest().get_telemetry()

telemetry.to_csv(
    DATA_DIR / "monaco_2025_norris_telemetry.csv",
    index=False
)

print("Telemetry saved.")
print(f"Telemetry rows: {len(telemetry)}")