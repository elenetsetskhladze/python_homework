import requests

city = input("Enter city name: ")

geo_url = "https://geocoding-api.open-meteo.com/v1/search"

geo_params = {
    "name": city,
    "count": 1
}

response = requests.get(geo_url, params=geo_params)

data = response.json()

if "results" not in data:
    print("City not found")
else:
    latitude = data["results"][0]["latitude"]
    longitude = data["results"][0]["longitude"]
    city_name = data["results"][0]["name"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    response = requests.get(weather_url, params=weather_params)

    weather = response.json()

    print(f"City: {city_name}")
    print(f"Temperature: {weather['current']['temperature_2m']} °C")
    print(f"Wind Speed: {weather['current']['wind_speed_10m']} km/h")
    print(f"Time: {weather['current']['time']}")