import pandas as pd

from app.core.database import SessionLocal
from app.models.driver import Driver


RESULTS_FILE = "data/raw/monaco_2025_results.csv"


print("Loading driver data...")

results = pd.read_csv(RESULTS_FILE)

db = SessionLocal()

try:
    for _, row in results.iterrows():

        existing_driver = (
            db.query(Driver)
            .filter(Driver.abbreviation == row["Abbreviation"])
            .first()
        )

        if existing_driver:
            continue

        driver = Driver(
            abbreviation=row["Abbreviation"],
            full_name=row["FullName"],
            team_name=row["TeamName"],
        )

        db.add(driver)

    db.commit()

    print("Drivers successfully added to database!")

finally:
    db.close()