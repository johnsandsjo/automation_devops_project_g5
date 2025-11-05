from weather import format_celsius

def test_format_metric_is_celsius():
    assert format_celsius(21.5, "metric").endswith("°C")

def test_format_imperial_is_fahrenheit():
    assert format_celsius(70, "imperial").endswith("°F")
