import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env.forecast
load_dotenv('.env')

# Use environment variables
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))

# Weather API function (your existing code)
def get_weather_forecast(latitude, longitude):
    # Your existing code to fetch the forecast data
    points_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    headers = {'User-Agent': '(myweatherapp.com, contact@myweatherapp.com)'}

    response = requests.get(points_url, headers=headers)
    points_data = response.json()
    forecast_url = points_data['properties']['forecast']

    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_data = forecast_response.json()

    # Extract the periods from the forecast data
    periods = forecast_data['properties']['periods']

    # Format the weather data into a string
    forecast_message = f"Weather Forecast for {latitude}, {longitude}\n"
    forecast_message += "=" * 40 + "\n\n"

    for period in periods[:5]:  # Display the next 5 periods
        start_time = datetime.fromisoformat(period['startTime']).strftime("%Y-%m-%d %H:%M")
        forecast_message += f"Period: {period['name']} (Starting {start_time})\n"
        forecast_message += f"Temperature: {period['temperature']}°{period['temperatureUnit']}\n"
        forecast_message += f"Conditions: {period['shortForecast']}\n"
        forecast_message += f"Wind: {period['windSpeed']} {period['windDirection']}\n"
        if period['probabilityOfPrecipitation']['value'] is not None:
            forecast_message += f"Precipitation Chance: {period['probabilityOfPrecipitation']['value']}%\n"
        forecast_message += f"Details: {period['detailedForecast']}\n\n"

    return forecast_message

# Discord webhook function
def send_to_discord(webhook_url, content):
    data = {
        "content": content
    }
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error sending message to Discord: {err}")
    else:
        print("Message sent to Discord successfully")

# Main execution
if __name__ == "__main__":
    # Your coordinates
    latitude = LATITUDE
    longitude = LONGITUDE

    # Get the weather forecast
    forecast = get_weather_forecast(latitude, longitude)

    # Your Discord webhook URL
    discord_webhook_url = DISCORD_WEBHOOK_URL

    # Send the forecast to Discord
    send_to_discord(discord_webhook_url, forecast)