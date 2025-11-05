import os, pytest
from weather import fetch_current

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@pytest.mark.skipif(not API_KEY, reason="No OPENWEATHER_API_KEY provided")
def test_fetch_current_ok():
    data = fetch_current(59.3293, 18.0686, API_KEY, units="metric")
    assert "temp" in data and isinstance(data["temp"], (int, float))
    assert data["units"] == "metric"
