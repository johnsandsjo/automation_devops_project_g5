import os
from flask import Flask, render_template_string, request, abort
from weather import fetch_current, fetch_last_year, format_celsius

# مختصات پیش‌فرض: استکهلم
DEFAULT_LAT = float(os.getenv("LAT", 59.3293))
DEFAULT_LON = float(os.getenv("LON", 18.0686))
UNITS = "metric"  # الزام پروژه: سلسیوس

API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)

TPL = """
<!doctype html>
<html lang="fa">
<head>
  <meta charset="utf-8"><title>Weather Compare</title>
  <style>body{font-family:sans-serif;background:#111;color:#eee}
  .card{background:#1a1a1a;padding:16px;border-radius:12px;margin:12px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
  </style>
</head>
<body>
  <h2>هواشناسی امروز vs سال قبل</h2>
  <form method="get">
    <label>Latitude: <input name="lat" value="{{lat}}"></label>
    <label>Longitude: <input name="lon" value="{{lon}}"></label>
    <button type="submit">برو</button>
  </form>
  <div class="grid">
    <div class="card">
      <h3>امروز</h3>
      <p>دما: {{cur.temp_fmt}}</p>
      <p>ابر: {{cur.clouds}}%</p>
      <p>بارش: {{cur.precip}} mm</p>
    </div>
    <div class="card">
      <h3>همین روز سال قبل</h3>
      <p>دما: {{prev.temp_fmt}}</p>
      <p>ابر: {{prev.clouds}}%</p>
      <p>بارش کل روز: {{prev.precip}} mm</p>
    </div>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    if not API_KEY:
        abort(500, "OPENWEATHER_API_KEY not set")
    lat = float(request.args.get("lat", DEFAULT_LAT))
    lon = float(request.args.get("lon", DEFAULT_LON))
    cur = fetch_current(lat, lon, API_KEY, UNITS)
    prev = fetch_last_year(lat, lon, API_KEY, UNITS)
    cur["temp_fmt"] = format_celsius(cur["temp"], UNITS)
    prev["temp_fmt"] = format_celsius(prev["temp"], UNITS)
    return render_template_string(TPL, cur=cur, prev=prev, lat=lat, lon=lon)
