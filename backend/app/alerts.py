from typing import Any


def generate_municipal_alert(
    location: dict[str, Any],
    hotspot: dict[str, Any],
    forecast: dict[str, Any],
) -> dict[str, Any]:

    risk_level = hotspot.get("risk_level", "low")
    pollution_score = hotspot.get("pollution_score", 0)

    forecast_level = forecast.get("risk_level", "low")
    forecast_score = forecast.get("risk_score", 0)

    # Alert when either current hotspot risk or forecast risk is high.
    if risk_level == "high" or forecast_level == "high":
        priority = "high"
    elif risk_level == "medium" or forecast_level == "medium":
        priority = "medium"
    else:
        priority = "low"

    if priority == "high":
        action = (
            "Prioritize inspection of the reported area and review "
            "local pollution sources."
        )
    elif priority == "medium":
        action = (
            "Monitor the area and consider a field inspection if "
            "additional evidence is received."
        )
    else:
        action = (
            "Continue environmental monitoring; no immediate "
            "municipal action is indicated."
        )

    return {
        "alert_generated": priority in {"high", "medium"},
        "priority": priority,
        "recipient": "Municipal Environment Authority",
        "location": location,
        "pollution_score": pollution_score,
        "current_risk": risk_level,
        "forecast_risk": forecast_level,
        "forecast_score": forecast_score,
        "action": action,
        "message": (
            f"Potential pollution risk detected near "
            f"{location.get('latitude')}, {location.get('longitude')}. "
            f"Current risk: {risk_level}. "
            f"Forecast risk: {forecast_level}."
        ),
    }