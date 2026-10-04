import json
from urllib.parse import quote
from urllib.request import urlopen


# ============================================================
# COMMON INDIAN CITY COORDINATES
# ============================================================

CITY_COORDINATES = {
    "bangalore": (12.9716, 77.5946, "Bengaluru", "India"),
    "bengaluru": (12.9716, 77.5946, "Bengaluru", "India"),
    "mangalore": (12.9141, 74.8560, "Mangaluru", "India"),
    "mangaluru": (12.9141, 74.8560, "Mangaluru", "India"),
    "mumbai": (19.0760, 72.8777, "Mumbai", "India"),
    "delhi": (28.6139, 77.2090, "Delhi", "India"),
    "new delhi": (28.6139, 77.2090, "New Delhi", "India"),
    "hyderabad": (17.3850, 78.4867, "Hyderabad", "India"),
    "chennai": (13.0827, 80.2707, "Chennai", "India"),
    "pune": (18.5204, 73.8567, "Pune", "India"),
    "mysore": (12.2958, 76.6394, "Mysuru", "India"),
    "mysuru": (12.2958, 76.6394, "Mysuru", "India"),
}


# ============================================================
# OPEN-METEO EXTERNAL API
# ============================================================

def get_weather(city: str) -> dict:

    city_key = city.strip().lower()

    if not city_key:
        raise ValueError("City name cannot be empty.")

    # --------------------------------------------------------
    # Use known Indian city coordinates
    # --------------------------------------------------------

    if city_key not in CITY_COORDINATES:

        raise ValueError(
            f"Weather lookup is not configured for '{city}'."
        )

    latitude, longitude, location_name, country = (
        CITY_COORDINATES[city_key]
    )

    # --------------------------------------------------------
    # Call Open-Meteo external API
    # --------------------------------------------------------

    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,"
        "relative_humidity_2m,"
        "precipitation,"
        "wind_speed_10m"
        "&daily=temperature_2m_max,"
        "temperature_2m_min,"
        "precipitation_probability_max"
        "&forecast_days=1"
        "&timezone=auto"
    )

    with urlopen(
        forecast_url,
        timeout=10
    ) as response:

        weather_data = json.loads(
            response.read().decode("utf-8")
        )

    current = weather_data.get(
        "current",
        {}
    )

    current_units = weather_data.get(
        "current_units",
        {}
    )

    daily = weather_data.get(
        "daily",
        {}
    )

    return {
        "city": location_name,
        "country": country,
        "temperature": current.get(
            "temperature_2m"
        ),
        "temperature_unit": current_units.get(
            "temperature_2m",
            "°C"
        ),
        "humidity": current.get(
            "relative_humidity_2m"
        ),
        "precipitation": current.get(
            "precipitation"
        ),
        "wind_speed": current.get(
            "wind_speed_10m"
        ),
        "max_temperature": (
            daily.get(
                "temperature_2m_max",
                [None]
            )[0]
        ),
        "min_temperature": (
            daily.get(
                "temperature_2m_min",
                [None]
            )[0]
        ),
        "precipitation_probability": (
            daily.get(
                "precipitation_probability_max",
                [None]
            )[0]
        ),
    }


# ============================================================
# FORMAT RESULT
# ============================================================

def format_weather_result(weather: dict) -> str:

    return (
        f"Weather for {weather['city']}, "
        f"{weather['country']}:\n"
        f"- Current temperature: "
        f"{weather['temperature']}"
        f"{weather['temperature_unit']}\n"
        f"- Humidity: "
        f"{weather['humidity']}%\n"
        f"- Precipitation: "
        f"{weather['precipitation']} mm\n"
        f"- Wind speed: "
        f"{weather['wind_speed']} km/h\n"
        f"- Today's minimum temperature: "
        f"{weather['min_temperature']}"
        f"{weather['temperature_unit']}\n"
        f"- Today's maximum temperature: "
        f"{weather['max_temperature']}"
        f"{weather['temperature_unit']}\n"
        f"- Maximum precipitation probability: "
        f"{weather['precipitation_probability']}%"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    weather = get_weather("Bangalore")

    print(
        format_weather_result(weather)
    )