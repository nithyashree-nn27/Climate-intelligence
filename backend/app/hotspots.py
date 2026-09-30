from typing import Any

from app.environment import get_current_air_quality
from app.forecast import forecast_pollution_risk


def detect_hotspots(
    locations: list[dict[str, Any]],
    citizen_reports: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    
    results = []

    for location in locations:

        latitude = location["latitude"]
        longitude = location["longitude"]

        try:
            environmental_data = get_current_air_quality(
                latitude=latitude,
                longitude=longitude
            )
            forecast = forecast_pollution_risk(environmental_data)

            current = environmental_data.get("current", {})

            pm25 = current.get("pm2_5")
            pm10 = current.get("pm10")
            no2 = current.get("nitrogen_dioxide")

            score = 0
            reasons = []
            
            # Citizen/Gemini evidence
            for report in citizen_reports or []:

                report_lat = report.get("latitude")
                report_lon = report.get("longitude")

                if (
                    report_lat == latitude
                    and report_lon == longitude
                ):
                    gemini = report.get("gemini_analysis", {})

                    if gemini.get("event_detected") is True:
                        score += 30
                        reasons.append(
                            "Citizen report indicates a potential pollution event"
                        )

                    if gemini.get("smoke_detected") is True:
                        score += 20
                        reasons.append(
                            "Visible smoke detected in citizen image"
                        )

            if pm25 is not None:

                if pm25 >= 75:
                    score += 40
                    reasons.append("High PM2.5")

                elif pm25 >= 35:
                    score += 25
                    reasons.append("Elevated PM2.5")

            if pm10 is not None:

                if pm10 >= 150:
                    score += 30
                    reasons.append("High PM10")

                elif pm10 >= 100:
                    score += 20
                    reasons.append("Elevated PM10")

            if no2 is not None:

                if no2 >= 80:
                    score += 20
                    reasons.append("Elevated NO2")

            score = min(score, 100)

            if score >= 70:
                risk = "high"
            elif score >= 40:
                risk = "medium"
            else:
                risk = "low"

            results.append({
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "pollution_score": score,
                "forecast": forecast,
                "risk_level": risk,
                "pollutants": {
                    "pm2_5": pm25,
                    "pm10": pm10,
                    "nitrogen_dioxide": no2
                },
                "reasons": reasons
            })

        except Exception as exc:

            results.append({
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "status": "error",
                "error": str(exc)
            })

    results.sort(
        key=lambda item: item.get("pollution_score", -1),
        reverse=True
    )

    hotspots = [
        result
        for result in results
        if result.get("pollution_score", 0) >= 40
    ]

    return {
        "locations_analyzed": len(results),
        "hotspots_detected": len(hotspots),
        "hotspots": hotspots,
        "all_locations": results
    }