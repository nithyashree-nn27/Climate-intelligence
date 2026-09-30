from datetime import datetime, timezone
from uuid import uuid4

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    UploadFile
)

from app.gemini_vision import analyze_pollution_image, PollutionAnalysis
from app.environment import get_current_air_quality
from app.validation import validate_pollution_event
from app.forecast import forecast_pollution_risk
from app.hotspots import detect_hotspots
from app.image_provenance import check_image_provenance
from app.alerts import generate_municipal_alert


router = APIRouter(
    prefix="/reports",
    tags=["Citizen Reports"]
)


@router.post("/")
async def create_report(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    description: str = Form("")
):
    try:
        # ---------------------------------------------
        # 1. Read citizen image
        # ---------------------------------------------

        image_bytes = await image.read()

        # ---------------------------------------------
        # 2. Image provenance check
        # ---------------------------------------------

        image_provenance = check_image_provenance(
            image_bytes=image_bytes,
            mime_type=image.content_type or "image/jpeg"
        )

        # ---------------------------------------------
        # 3. Gemini visual analysis
        # ---------------------------------------------

        try:
            gemini_analysis = analyze_pollution_image(
                image_bytes=image_bytes,
                mime_type=image.content_type or "image/jpeg",
                description=description
            )
        except Exception:
            gemini_analysis = PollutionAnalysis(
                event_detected=False,
                smoke_detected=False,
                possible_source="unknown",
                severity="unclear",
                relevance="low",
                evidence=(
                    "AI visual analysis was unavailable for this image, so no "
                    "pollution claim was made from the image alone."
                )
            )

        gemini_result = gemini_analysis.model_dump()

        # ---------------------------------------------
        # 4. Fetch environmental conditions
        # ---------------------------------------------

        try:
            environmental_data = get_current_air_quality(
                latitude=latitude,
                longitude=longitude
            )
        except Exception:
            environmental_data = {
                "source": "Open-Meteo / CAMS Global",
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                },
                "current": {},
                "current_units": {},
                "forecast_24h": {}
            }

        # ---------------------------------------------
        # 4. Fuse independent evidence
        # ---------------------------------------------

        validation = validate_pollution_event(
            gemini_analysis=gemini_result,
            environmental_data=environmental_data
        )
        
        forecast = forecast_pollution_risk(
        environmental_data
        )
        
        hotspot_result = detect_hotspots(
            locations=[
                {
                    "latitude": latitude,
                    "longitude": longitude
                }
            ],
            citizen_reports=[
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "gemini_analysis": gemini_result
                }
            ]
        )
        hotspots = hotspot_result.get("hotspots", [])
        hotspot_for_alert = (
            hotspots[0]
            if hotspots
            else {
                "pollution_score": 0,
                "risk_level": "low",
                }
            )
        municipal_alert = generate_municipal_alert(
            location={"latitude": latitude, "longitude": longitude},
            hotspot=hotspot_for_alert,
            forecast=forecast,
            )
        # ---------------------------------------------
        # 5. Generate event ID
        # ---------------------------------------------

        event_id = f"EVT-{uuid4().hex[:8].upper()}"

        # ---------------------------------------------
        # 6. Return complete event
        # ---------------------------------------------

        return {
            "event_id": event_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),

            "location": {
                "latitude": latitude,
                "longitude": longitude
            },

            "citizen_report": {
                "filename": image.filename,
                "description": description
            },

            "image_provenance": image_provenance,

            "gemini_analysis": gemini_result,

            "environmental_data": {
                "source": environmental_data.get("source"),
                "current": environmental_data.get("current"),
                "current_units": environmental_data.get("current_units")
            },

            "validation": validation,
            
            "forecast": forecast,
            
            "hotspot": hotspot_result,
            
            "municipal_alert": municipal_alert,

            "status": "validated"
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Report processing failed: {str(exc)}"
        )