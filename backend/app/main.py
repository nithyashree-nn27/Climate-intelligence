from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.environment import get_current_air_quality
from app.reports import router as reports_router
from app.hotspots import detect_hotspots


app = FastAPI(
    title="ClimatePulse API",
    description="AI-powered environmental intelligence platform",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "ClimatePulse API is running",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
    
@app.post("/hotspots")
def get_hotspots(locations: list[dict]):
    return detect_hotspots(locations)
    
@app.get("/environment/current")
def current_environment(
    latitude: float,
    longitude: float
):
    return get_current_air_quality(
        latitude=latitude,
        longitude=longitude
    )


app.include_router(reports_router)