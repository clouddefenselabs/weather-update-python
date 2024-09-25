import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env.latest
load_dotenv('.env')

# Use environment variables
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
STATION_ID = os.getenv('STATION_ID')

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def kmh_to_mph(kmh):
    return kmh * 0.621371

def degrees_to_cardinal(degrees):
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degrees / (360. / len(directions))) % len(directions)
    return directions[index]

def get_latest_weather_observation(station_id):
    observation_url = f'https://api.weather.gov/stations/{station_id}/observations/latest'
    headers = {'User-Agent': '(myweatherapp.com, contact@myweatherapp.com)'}

    try:
        response = requests.get(observation_url, headers=headers)
        observation_data = response.json()

        if 'properties' in observation_data:
            properties = observation_data['properties']
            
            # Extract and format the data
            temperature_c = properties.get('temperature', {}).get('value')
            temperature_f = celsius_to_fahrenheit(temperature_c) if temperature_c is not None else None
            condition = properties.get('textDescription', 'N/A')
            wind_speed_kmh = properties.get('windSpeed', {}).get('value')
            wind_speed_mph = kmh_to_mph(wind_speed_kmh) if wind_speed_kmh is not None else None
            wind_direction_degrees = properties.get('windDirection', {}).get('value')
            wind_direction_cardinal = degrees_to_cardinal(wind_direction_degrees) if wind_direction_degrees is not None else 'N/A'
            humidity = properties.get('relativeHumidity', {}).get('value')
            timestamp = properties.get('timestamp')

            # Format the message
            weather_info = (
                f'Latest Weather Observation for Station: {station_id}\n'
                f'Temperature: {temperature_f:.1f}°F\n'
                f'Condition: {condition}\n'
                f'Wind Speed: {wind_speed_mph:.1f} mph, Direction: {wind_direction_cardinal}\n'
                f'Humidity: {humidity:.1f}%\n'
                f'Timestamp: {timestamp}\n'
            )
            return weather_info
        else:
            return "Unable to retrieve observation data"
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {str(e)}"

def send_to_discord(webhook_url, content):
    data = {"content": content}
    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"Error sending message to Discord: {err}")
    else:
        print("Message sent to Discord successfully")

if __name__ == "__main__":
    # Specify the weather station ID (you can change this to any valid station)
    station_id = STATION_ID

    # Get the latest weather observation
    latest_weather = get_latest_weather_observation(station_id)
    print(latest_weather)

    # Your Discord webhook URL
    discord_webhook_url = DISCORD_WEBHOOK_URL

    # Send the weather information to Discord
    send_to_discord(discord_webhook_url, latest_weather)