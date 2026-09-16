from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ai_analyst import (
    analyze_driver_comparison,
)


router = APIRouter(
    prefix="/ai",
    tags=["AI Analyst"],
)


class DriverComparisonRequest(BaseModel):
    driver_a: str
    driver_b: str


@router.post("/compare")
def compare_drivers(
    request: DriverComparisonRequest,
):
    analysis = analyze_driver_comparison(
        request.driver_a,
        request.driver_b,
    )

    return {
        "driver_a": request.driver_a.upper(),
        "driver_b": request.driver_b.upper(),
        "analysis": analysis,
    }