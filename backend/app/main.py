from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.driver import Driver
from app.models.race import Race
from app.api.routes.drivers import router as drivers_router
from app.api.routes.analytics import router as analytics_router
app.include_router(analytics_router)

app = FastAPI(
    title="RaceMind API",
    description="AI-powered Formula 1 race strategy intelligence platform",
    version="1.0.0",
)


app.include_router(drivers_router)


@app.get("/")
def root():
    return {
        "message": "RaceMind API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }