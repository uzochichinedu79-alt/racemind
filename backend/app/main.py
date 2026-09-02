from fastapi import FastAPI


app = FastAPI(
    title="RaceMind API",
    description="AI-powered Formula 1 race strategy intelligence platform",
    version="1.0.0",
)


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