"""
Weather Service for AgroVision
Fetches real-time microclimate data using Open-Meteo API (free, open, no-key required)
Calculates pathogen & fungal outbreak risks based on humidity, temperature, and rain trends.
"""

from typing import Dict, Any, Optional
import requests

def get_coordinates_for_location(location_name: str) -> Optional[Dict[str, Any]]:
    """Geocode a city or district name into lat/long."""
    if not location_name or not location_name.strip():
        return None
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_name.strip()}&count=1&language=en&format=json"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return {
                    "name": result.get("name"),
                    "country": result.get("country", ""),
                    "admin1": result.get("admin1", ""),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude")
                }
    except Exception:
        pass
    return None

def fetch_farm_weather(location_name: str = "Bengaluru") -> Dict[str, Any]:
    """
    Fetch current weather metrics and calculate early disease proliferation risk.
    """
    geo = get_coordinates_for_location(location_name)
    lat = geo["latitude"] if geo else 12.9716
    lon = geo["longitude"] if geo else 77.5946
    display_name = f"{geo['name']}, {geo.get('admin1', '')} ({geo.get('country', '')})" if geo else location_name

    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,"
            f"precipitation,rain,weather_code,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min,"
            f"precipitation_probability_max&timezone=auto"
        )
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            current = data.get("current", {})
            daily = data.get("daily", {})

            temp = current.get("temperature_2m", 26.0)
            humidity = current.get("relative_humidity_2m", 65.0)
            rain = current.get("rain", 0.0)
            wind = current.get("wind_speed_10m", 12.0)
            rain_prob = daily.get("precipitation_probability_max", [20])[0]

            # Assess Early Pathogen / Disease Risk
            # High humidity (>70%) + Warm Temp (20°C - 30°C) is ideal for Late Blight, Rust, Downy Mildew
            if humidity >= 75 and 18 <= temp <= 32:
                pathogen_risk = "HIGH"
                risk_summary = "Favorable conditions for fungal spores (Downy Mildew, Leaf Spots, Late Blight). Foliar moisture remains high."
                risk_badge_color = "#e53935"
            elif humidity >= 60 and 22 <= temp <= 35:
                pathogen_risk = "MODERATE"
                risk_summary = "Moderate humidity. Keep foliage well-spaced and monitor lower canopies for leaf spotting."
                risk_badge_color = "#fb8c00"
            elif temp > 36 and humidity < 40:
                pathogen_risk = "HEAT_STRESS"
                risk_summary = "High evaporative demand. Watch out for flower drop, sunscald, and spider mite flare-ups."
                risk_badge_color = "#d81b60"
            else:
                pathogen_risk = "LOW"
                risk_summary = "Stable weather parameters. Low baseline fungal spore germination pressure."
                risk_badge_color = "#43a047"

            return {
                "success": True,
                "location": display_name,
                "temperature_c": temp,
                "humidity_percent": humidity,
                "rain_mm": rain,
                "wind_kmh": wind,
                "rain_probability": rain_prob,
                "pathogen_risk": pathogen_risk,
                "risk_summary": risk_summary,
                "risk_badge_color": risk_badge_color
            }
    except Exception as e:
        pass

    # Safe fallback if network is unreachable
    return {
        "success": False,
        "location": location_name,
        "temperature_c": 27.5,
        "humidity_percent": 68.0,
        "rain_mm": 0.0,
        "wind_kmh": 14.0,
        "rain_probability": 30,
        "pathogen_risk": "MODERATE",
        "risk_summary": "Moderate baseline humidity. Preemptive inspection recommended.",
        "risk_badge_color": "#fb8c00"
    }
