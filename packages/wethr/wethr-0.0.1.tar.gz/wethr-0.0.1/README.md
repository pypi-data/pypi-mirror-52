# WeatherCLI

Web Scraping tool and a Command Line Interface for **Weather.com**


# Installatoin

Install via PIP 
`pip install weathercli`

**or**

Git Clone using 
`git clone https://github.com/AbinashSinha/WeatherCLI`


## Usage 
Name of the City/Place  `-p PLACE, --place`

Date `-d DATE, --date [default : Current Time]` 

Type of Forecast: 

`1` : Daily, `2` : Hourly,`3` : 5-Days, `4`: 10-Days, `5`: Weekend, `6` : Monthly.

`-t TYPE, --type [Default: 1: Daily]`

`weather -p Bhopal -t 3`

`weather -p Bhopal -t 2`

`weather -p Bhopal -d 12/03/19`

## API

*Return a JSON file*

usage:
`from weathercli import Weather`

`Weather(place='Bhopal')`

`Weather(palce='Bhoapl',date='20/03/19')`

`Weather(place='Bhopal,typeof='2' )`
