
import os, time, requests
from datetime import datetime, timedelta

BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_TIMEMACHINE = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

def unix_last_year(ts=None):
    """برمی‌گرداند timestamp همان روز سال قبل (UTC)."""
    dt = datetime.utcfromtimestamp(ts or time.time())
    last_year = dt.replace(year=dt.year - 1)
    return int(last_year.timestamp())

def fetch_current(lat, lon, api_key, units="metric"):
    r = requests.get(BASE_URL_CURRENT, params={
        "lat": lat, "lon": lon, "appid": api_key, "units": units
    }, timeout=20)
    r.raise_for_status()
    j = r.json()
    return {
        "temp": j["main"]["temp"],
        "clouds": j["clouds"]["all"],                 # %
        "precip": extract_precip_current(j),          # mm (تقریبی)
        "city": j.get("name", ""),
        "dt": j["dt"],
        "units": units
    }

def extract_precip_current(j):
    # OWM در weather/current بارش را در کلیدهای optional می‌دهد
    rain = j.get("rain", {}).get("1h") or j.get("rain", {}).get("3h") or 0.0
    snow = j.get("snow", {}).get("1h") or j.get("snow", {}).get("3h") or 0.0
    return float(rain) + float(snow)

def fetch_last_year(lat, lon, api_key, units="metric"):
    ts = unix_last_year()
    r = requests.get(BASE_URL_TIMEMACHINE, params={
        "lat": lat, "lon": lon, "dt": ts, "appid": api_key, "units": units
    }, timeout=20)
    r.raise_for_status()
    j = r.json()
    # تمایل داریم از سَری ساعتی میانگین روز را بسازیم
    hourly = j.get("hourly", [])
    if not hourly:
        return {"temp": None, "clouds": None, "precip": None, "dt": ts, "units": units}
    avg_temp = sum(h["temp"] for h in hourly)/len(hourly)
    avg_clouds = int(sum(h.get("clouds", 0) for h in hourly)/len(hourly))
    precip = sum((h.get("rain", {}).get("1h", 0.0) or 0.0) +
                 (h.get("snow", {}).get("1h", 0.0) or 0.0) for h in hourly)
    return {"temp": round(avg_temp, 1), "clouds": avg_clouds, "precip": round(precip, 2), "dt": ts, "units": units}

def format_celsius(value, units):
    """برای یونیت‌تست: باید همیشه °C برگرداند وقتی units=metric است."""
    if units == "metric":
        return f"{value} °C"
    if units == "imperial":
        return f"{value} °F"
    return f"{value} K"
