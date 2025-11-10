import pytest
from weather_app.api_call import get_coordinates, get_current_weather

#pytestmark = pytest.mark.integration

def test_geocode_returns_coords():
    lat, lon = get_coordinates("Stockholm")
    assert isinstance(lat, float) and isinstance(lon, float)

def test_current_weather_has_main_and_temp():
    lat, lon = get_coordinates("Stockholm")
    data = get_current_weather(lat, lon)
    assert "main" in data and "temp" in data["main"]
