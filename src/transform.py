# src/transform.py

def f_to_c(fahrenheit: float) -> float:
    """
    Convert Fahrenheit to Celsius and round to 1 decimal place.
    """
    return round((fahrenheit - 32) * 5/9, 1)


def transform_weather(payload: dict) -> dict:
    """
    Take the original OpenWeather API response and return a simplified dictionary
    that includes BOTH Fahrenheit and Celsius values.

    This does NOT require any change to app.py. You may call this function
    if/when you want structured weather data for UI or app display.
    """

    main = payload.get("main", {})
    weather0 = (payload.get("weather") or [{}])[0]

    temp_f = main.get("temp")
    feels_f = main.get("feels_like")

    temp_c = f_to_c(temp_f) if temp_f is not None else None
    feels_c = f_to_c(feels_f) if feels_f is not None else None

    return {
        "city": payload.get("name", ""),
        "description": weather0.get("description", ""),
        "temperature_f": temp_f,
        "temperature_c": temp_c,
        "feels_like_f": feels_f,
        "feels_like_c": feels_c,
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "precipitation_mm": payload.get("rain", {}).get("1h", 0),
    }
