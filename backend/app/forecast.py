from typing import Any


def forecast_pollution_risk(
    environmental_data: dict[str, Any]
) -> dict[str, Any]:

    hourly = environmental_data.get("forecast_24h", {})

    times = hourly.get("time", [])
    pm25_values = hourly.get("pm2_5", [])
    pm10_values = hourly.get("pm10", [])
    no2_values = hourly.get("nitrogen_dioxide", [])

    if not times:
        return {
            "status": "unavailable",
            "message": "No hourly forecast data available."
        }

    # --------------------------------------------------
    # Helper: calculate percentage increase
    # --------------------------------------------------

    def percentage_change(first, last):
        if first in (None, 0) or last is None:
            return 0

        return ((last - first) / first) * 100

    # --------------------------------------------------
    # PM2.5 trend
    # --------------------------------------------------

    pm25_valid = [
        value for value in pm25_values
        if value is not None
    ]

    pm10_valid = [
        value for value in pm10_values
        if value is not None
    ]

    no2_valid = [
        value for value in no2_values
        if value is not None
    ]

    if not pm25_valid:
        return {
            "status": "unavailable",
            "message": "PM2.5 forecast is unavailable."
        }

    pm25_start = pm25_valid[0]
    pm25_peak = max(pm25_valid)
    pm25_peak_index = pm25_values.index(pm25_peak)

    pm25_end = pm25_valid[-1]

    pm25_change = percentage_change(
        pm25_start,
        pm25_end
    )

    # --------------------------------------------------
    # PM10 trend
    # --------------------------------------------------

    pm10_peak = max(pm10_valid) if pm10_valid else None

    # --------------------------------------------------
    # NO2 trend
    # --------------------------------------------------

    no2_peak = max(no2_valid) if no2_valid else None

    # --------------------------------------------------
    # Risk scoring
    # --------------------------------------------------

    risk_score = 0
    reasons = []

    # PM2.5 level
    if pm25_peak >= 75:
        risk_score += 40
        reasons.append(
            "Forecast PM2.5 reaches a high concentration."
        )
    elif pm25_peak >= 35:
        risk_score += 25
        reasons.append(
            "Forecast PM2.5 reaches an elevated concentration."
        )

    # PM10 level
    if pm10_peak is not None:
        if pm10_peak >= 150:
            risk_score += 25
            reasons.append(
                "Forecast PM10 reaches a high concentration."
            )
        elif pm10_peak >= 100:
            risk_score += 15
            reasons.append(
                "Forecast PM10 reaches an elevated concentration."
            )

    # NO2 level
    if no2_peak is not None:
        if no2_peak >= 80:
            risk_score += 15
            reasons.append(
                "Forecast NO₂ reaches an elevated concentration."
            )

    # Increasing PM2.5 trend
    if pm25_change >= 30:
        risk_score += 15
        reasons.append(
            "PM2.5 shows a significant increasing trend "
            "during the forecast period."
        )
    elif pm25_change >= 15:
        risk_score += 8
        reasons.append(
            "PM2.5 shows a moderate increasing trend."
        )

    risk_score = min(risk_score, 100)

    # --------------------------------------------------
    # Risk category
    # --------------------------------------------------

    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"

    # --------------------------------------------------
    # Peak forecast time
    # --------------------------------------------------

    peak_time = (
        times[pm25_peak_index]
        if pm25_peak_index < len(times)
        else None
    )

    return {
        "status": "available",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "forecast_peak": {
            "time": peak_time,
            "pm2_5": pm25_peak,
            "pm10": pm10_peak,
            "nitrogen_dioxide": no2_peak
        },
        "pm2_5_change_percent": round(pm25_change, 2),
        "reasons": reasons
    }