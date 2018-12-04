#!D:\MyPythonScripts\UmbrellaReminder\venv\Scripts\python

# UmbrellaReminder.py - Checks the weather on http://weather.gov/
# If there's a chance of rain / shower, send a text to user to remind to
# bring umbrella

import geocoder
import requests
from bs4 import BeautifulSoup
from textmyself import textmyself       # User class, using twilio API to text
import re
from datetime import datetime


def rain_check():
    location = geocoder.ip('me')        # Find user's longitude and latitude
    url = (f'https://forecast.weather.gov/'
           f'MapClick.php?lat={location.latlng[0]}&lon={location.latlng[1]}')

    # Go to the weather page
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text)

    # Select the forecast element
    weather_elems = soup.select('.col-sm-10.forecast-text')

    # Get the 'Today' forecast
    forecast = weather_elems[0].getText().lower()

    # Define the regular expressions to get % and whether it is rain or showers
    forecast_chance_regex = re.compile(r'(\d+) percent')
    weather_regex = re.compile(r'(rain|showers)')

    # If there's a chance of rain or showers
    if 'showers' in forecast or 'rain' in forecast:
        # Get the % chance
        forecast_chance = forecast_chance_regex.search(forecast).group(1)
        # Get weather (rain or showers)
        weather = weather_regex.search(forecast).group(1)
        # Send text if there will be rain or showers, and the probability
        textmyself(f'Today ({datetime.now().date()}): {forecast_chance}% '
                   f'chance of {weather}.')


if __name__ == "__main__":
    rain_check()
