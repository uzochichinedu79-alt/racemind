from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.driver import Driver


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_drivers(db: Session = Depends(get_db)):
    drivers = db.query(Driver).all()

    return drivers

@router.get("/{abbreviation}")
def get_driver(abbreviation: str, db: Session = Depends(get_db)):
    driver = (
        db.query(Driver)
        .filter(Driver.abbreviation == abbreviation.upper())
        .first()
    )

    if not driver:
        return {
            "error": "Driver not found"
        }

    return driver