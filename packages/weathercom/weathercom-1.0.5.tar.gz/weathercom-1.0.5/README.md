# Weathercom

A Python package to get weather reports for any location from weather.com. API for weather.com

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install weathercom.

```bash
pip install weathercom
```

## Usage

```python
import weathercom

weatherDetails = weathercom.getCityWeatherDetails("bangalore")
weatherDetails = weathercom.getCityWeatherDetails(city="bangalore", queryType="daily-data")

weatherDetails=weathercom.getCityWeatherDetails(city="bangalore", queryType="ten-days-data")
weatherDetails=weathercom.getCityWeatherDetails(city="bangalore", queryType="hourly-data")
weatherDetails=weathercom.getCityWeatherDetails(city="bangalore", queryType="monthly-data")

weatherDetais=weathercom.getCityWeatherDetails(city="bangalore", queryType="particular-date-data", date={'year':'2018','month':'09','date': '19')
```

## Defects to be corrected in next release
Better error handling, particular-date-data can only accept a date in the last five years, imporved user experience 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://github.com/prashanth-p/weathercom/blob/master/LICENSE.txt)