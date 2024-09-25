# Weather Update Generator

This project consists of two Python scripts that fetch weather data from the National Weather Service API (api.weather.gov) and send updates to a Discord channel. One script provides hourly weather updates, while the other gives daily forecasts.

## Features

- `latest.py`: Retrieves the latest weather observation hourly
- `forecast.py`: Fetches a daily weather forecast at 6:00 AM
- Both scripts send data to a specified Discord channel via webhook
- Displays temperature in Fahrenheit, wind speed in mph, and wind direction as cardinal directions

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system
- `requests` library installed
- A Linux system with cron (for automated scheduling)
- A Discord webhook URL

## Installation

1. Clone this repository
2.  Navigate to the project directory:  ```bash
cd weather-update-python
```
3. ```bash
    pip install -r requirements.txt
    ```
4. Make the scripts executable:```bash
chmod +x latest.py forecast.py
```

## Configuration

1. Open `latest.py` and `forecast.py` in a text editor.

2. In both files, replace `"YOUR_DISCORD_WEBHOOK_URL_HERE"` with your actual Discord webhook URL.

3. In `latest.py`, set the `station_id` variable to your desired weather station ID.

4. In `forecast.py`, set the `latitude` and `longitude` variables to your desired location.

## Usage

You can run the scripts manually:
python latest.py
python forecast.py

However, these scripts are designed to be run automatically using cron jobs.

### Setting up Cron Jobs

1. Open your crontab file for editing:
```bash
contab -e
```
2. Add the following lines to your crontab:
```bash
0 * * * * /usr/bin/python3 /path/to/latest.py
0 6 * * * /usr/bin/python3 /path/to/forecast.py
```
(Change as needed for timing)

Replace `/path/to/` with the actual path to your scripts.
3. Save and exit the crontab editor.

This setup will run `latest.py` every hour and `forecast.py` every day at 6:00 AM.

## Script Details

### latest.py

This script fetches the latest weather observation for a specified weather station. It includes:

- Temperature in Fahrenheit
- Current weather conditions
- Wind speed in mph and direction as cardinal points
- Humidity percentage
- Timestamp of the observation

### forecast.py

This script retrieves a weather forecast for specified coordinates. It provides:

- Forecast for the next 5 periods
- Temperature in Fahrenheit
- Weather conditions
- Wind information
- Precipitation chances
- Detailed forecast for each period

## Environment Variables

This project uses a .env file to manage environment variables. Before running the scripts, modify the .env file to match your environment:
DISCORD_WEBHOOK_URL=YOUR_DISCORD_WEBHOOK_URL
LATITUDE=YOUR_LATITUDE_COORDINATES
LONGITUDE=YOUR_LONGITUDE_COORDINATES
STATION_ID=WEATHER_STATION_ID_YOU_WANT

  For the Latitude/Longitude, I used [https://www.latlong.net](LatLong.net)
  For the STATION_ID, I did the following:
``` 
  Make a request to the National Weather Service API using this format:
  https://api.weather.gov/points/{latitude},{longitude}
  For example: https://api.weather.gov/points/47.62350,-122.33290
  In the response, look for the "observationStations" URL:
  This URL will list the nearby weather stations.
  Visit the "observationStations" URL (You'll see a list of stations with their identifiers.)
  Look for the "stationIdentifier" in the results. This is the station ID you'll use in your .env file for STATION_ID.
```

## Troubleshooting

- If the scripts are not running as expected, check the system logs or add logging to the scripts.
- Ensure that the user running the cron jobs has the necessary permissions.
- Verify that the Discord webhook URL is correct and the webhook has not been revoked.

## Contributing

Contributions to this project are welcome. Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Weather data provided by the [National Weather Service API](https://www.weather.gov/documentation/services-web-api)

## Contact

If you have any questions or feedback, please open an issue on this repository.
