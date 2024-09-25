import requests
import json
from datetime import datetime

# Define the coordinates
latitude = 34.2384
longitude = -84.4167

# Step 1: Get the forecast URL for the given coordinates
points_url = f'https://api.weather.gov/points/{latitude},{longitude}'
headers = {'User-Agent': '(myweatherapp.com, contact@myweatherapp.com)'}

response = requests.get(points_url, headers=headers)
points_data = response.json()
forecast_url = points_data['properties']['forecast']

# Step 2: Fetch the forecast data
forecast_response = requests.get(forecast_url, headers=headers)
forecast_data = forecast_response.json()

# Step 3: Extract and display the weather updates
periods = forecast_data['properties']['periods']

print(f"Weather Forecast for {latitude}, {longitude}")
print("=" * 40)

for period in periods[:5]:  # Display the next 5 periods
    start_time = datetime.fromisoformat(period['startTime']).strftime("%Y-%m-%d %H:%M")
    print(f"\nPeriod: {period['name']} (Starting {start_time})")
    print(f"Temperature: {period['temperature']}°{period['temperatureUnit']}")
    print(f"Conditions: {period['shortForecast']}")
    print(f"Wind: {period['windSpeed']} {period['windDirection']}")
    if period['probabilityOfPrecipitation']['value'] is not None:
        print(f"Precipitation Chance: {period['probabilityOfPrecipitation']['value']}%")
    print(f"Details: {period['detailedForecast']}")