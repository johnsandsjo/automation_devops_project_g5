import os
import requests
import datetime as dt

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("open_api_key") 



geo_coding_url = "http://api.openweathermap.org/geo/1.0/direct"
weather_url = "https://api.openweathermap.org/data/2.5/weather"
history_url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

def get_coordinates(city_name):
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }
    response = requests.get(geo_coding_url, params=params)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError("City not found")
    return data[0]['lat'], data[0]['lon']
def get_current_weather(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "imperial"         # metric
    }

    response = requests.get(weather_url, params=params)
    response.raise_for_status()
    return response.json()


def get_historical_weather(lat, lon, date):
    timestamp = int(date.timestamp())
    params = {
        "lat": lat,
        "lon": lon,
        "dt": timestamp,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(history_url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":


    city = "Stockholm"
    lat, lon = get_coordinates(city)
    
    current_weather = get_current_weather(lat, lon)

    temp = current_weather['main']['temp']
    feels_like = current_weather['main']['feels_like']
    clouds = current_weather['weather'][0]['description']
    precipitation = current_weather.get('rain', {}).get('1h', 0)
    today = dt.datetime.now().date()


    print(f"Weather in {city} on {today}:")
    print(f"Temperature: {temp}°F, Feels like: {feels_like}°F,")
    print(f"Conditions: {clouds},")
    print(f"Precipitation: {precipitation}, mm")








    #historical_date = today - dt.timedelta(days=5)
    #historical_weather = get_historical_weather(lat, lon, historical_date)

    #print(f"Historical weather in {city} on {historical_date}: Temperature: {historical_weather['current']['temp']}°F, Conditions: {historical_weather['current']['weather'][0]['description']}")