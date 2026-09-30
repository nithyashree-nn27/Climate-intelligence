import requests

OPEN_METEO_AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_current_air_quality(latitude: float, longitude: float):

    # ---------------------------------------------------------
    # 1. Air-quality data from CAMS
    # ---------------------------------------------------------
    air_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "pm10,pm2_5,nitrogen_dioxide,ozone",
        "hourly": "pm10,pm2_5,nitrogen_dioxide,ozone",
        "forecast_hours": 24,
        "timezone": "auto",
        "domains": "cams_global",
    }

    air_response = requests.get(
        OPEN_METEO_AIR_URL,
        params=air_params,
        timeout=10,
    )

    air_response.raise_for_status()
    air_data = air_response.json()

    # ---------------------------------------------------------
    # 2. Weather data
    # ---------------------------------------------------------
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,wind_direction_10m",
        "timezone": "auto",
    }

    weather_response = requests.get(
        OPEN_METEO_WEATHER_URL,
        params=weather_params,
        timeout=10,
    )

    weather_response.raise_for_status()
    weather_data = weather_response.json()

    # ---------------------------------------------------------
    # 3. Combine environmental signals
    # ---------------------------------------------------------
    current_air = air_data.get("current", {})
    current_weather = weather_data.get("current", {})

    current_units_air = air_data.get("current_units", {})
    current_units_weather = weather_data.get("current_units", {})

    combined_current = {
        **current_air,
        **current_weather,
    }

    combined_units = {
        **current_units_air,
        **current_units_weather,
    }

    return {
        "source": "Open-Meteo / CAMS Global + Open-Meteo Weather",
        "location": {
            "latitude": air_data.get("latitude", latitude),
            "longitude": air_data.get("longitude", longitude),
            "timezone": air_data.get("timezone"),
        },
        "current": combined_current,
        "current_units": combined_units,
        "forecast_24h": air_data.get("hourly", {}),
    }