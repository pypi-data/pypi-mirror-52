import requests
import json
from datetime import date


def getCityWeatherDetails(city=None,queryType=None,date={'year': None, 'month': None, 'date': None}):
    # print("DD: " + str(date['date']))
    # print("MM: " + str(date['month']))
    # print("YYYY: " + str(date['year']))
    weatherObject = WeatherDetails(city,queryType,date)    
    weatherDetails = weatherObject.driverCodeBasedOnQuerySelector()
    return weatherDetails
