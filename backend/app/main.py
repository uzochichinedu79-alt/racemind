from fastapi import FastAPI

from app.api.routes.stints import router as stints_router
from app.core.database import Base, engine
from app.models.driver import Driver
from app.models.race import Race
from app.api.routes.drivers import router as drivers_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.strategy import router as strategy_router
from app.api.routes.ai import router as ai_router
app.include_router(analytics_router)
app.include_router(stints_router)
app.include_router(strategy_router)
app.include_router(ai_router)

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