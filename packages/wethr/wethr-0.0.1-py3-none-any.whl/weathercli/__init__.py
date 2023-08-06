from geopy.geocoders import Nominatim
from datetime import datetime
import requests
import argparse
import json
import sys


def Weather(place, date='today', typeof=1):

    today = datetime.today().strftime("%H:%M:%S")
    types = {1: 'Daily', 2: 'Hourbyhour', 3: '5day',
             4: 'Tenday', 5: 'weekend', 6: 'Monthly'}
    geolocator = Nominatim(user_agent='weatherapp')
    try:
        location = geolocator.geocode(place)
        if(location == None):
            sys.exit('No City Found')
    except:
        print("No City Found")

    print(location)

    if(date != 'today'):
        try:
            d = datetime.strptime(date, "%d/%m/%y")
            url = 'https://dsx.weather.com/wxd/v2/PastObsAvg/en_IN/'+d.strftime("%Y%m%d")+'/30/'+str(
                location.latitude)[:-5]+','+str(location.longitude)[:-5]+'?api=7bb1c920-7027-4289-9c96-ae5e263980bc&format=json'
            print(url)
            response = requests.get(url)
            data = json.loads(response.content)
            for i in data:
                # print(datetime.strptime(
                #		i['Temperatures']['highTmISO'][:-5], '%Y-%m-%dT%H:%M:%S').strftime('%d-%m-%Y'), end='  ')
                print('High Temp : ', i['Temperatures']['highC'],
                      ' at ', i['Temperatures']['highTm'], end='  ')
                print('Low Temp : ', i['Temperatures']
                      ['lowC'], ' at ', i['Temperatures']['lowTm'])

        except Exception as e:
            print(e)
            print("Invalid Date Format. Try DD/MM/YY [12/01/19]")

    elif(typeof == 2):
        start = 'https://api.weather.com/v2/turbo/vt1hourlyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode='
        end = '&language=en-IN&units=m'
        complete_url = start + str(location.latitude) + \
            "%2C" + str(location.longitude) + end
        print(complete_url)
        response = requests.get(complete_url)
        data = response.json()
        for time, temp, phrase in zip(data['vt1hourlyForecast']['processTime'], data['vt1hourlyForecast']['temperature'], data['vt1hourlyForecast']['phrase']):
            date = datetime.strptime(time[:-5], "%Y-%m-%dT%H:%M:%S")
            print(date.strftime("%d-%m-%Y %I:%M %p"), " ", temp, " ", phrase)
    elif(typeof == 1):
        base_url = 'https://api.weather.com/v2/turbo/vt1observation?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode='
        complete_url = base_url + \
            str(location.latitude) + "%2C" + \
            str(location.longitude) + "&language=en-IN&units=m"
        print(complete_url)
        response = requests.get(complete_url)
        #response = Request(url=complete_url, headers=headers)
        #html = urlopen(response)
        data = response.json()
        print(data['vt1observation']['observationTime'], data['vt1observation']
                  ['temperature'], data['vt1observation']['phrase'])

    elif(typeof == 3):
        base_url = 'https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode='
        complete_url = base_url + \
            str(location.latitude) + "%2C" + \
            str(location.longitude) + "&language=en-IN&units=m"
        print(complete_url)
        response = requests.get(complete_url)
        #response = Request(url=complete_url, headers=headers)
        #html = urlopen(response)
        data = response.json()
        i = 0
        if(datetime.now().strftime('%p') == "AM"):
            for day, temp, narrative in zip(data['vt1dailyForecast']['day']['dayPartName'], data['vt1dailyForecast']['day']['temperature'], data['vt1dailyForecast']['day']['narrative']):
                print(day, ': ', temp, "  ", narrative)
                i += 1
                if(i == 5):
                    break
        else:
            for day, temp, narrative in zip(data['vt1dailyForecast']['night']['dayPartName'], data['vt1dailyForecast']['night']['temperature'], data['vt1dailyForecast']['night']['narrative']):
                print(day, ': ', temp, "  ", narrative)
                i += 1
                if(i == 5):
                    break
    else:
        base_url = 'https://api.weather.com/v2/turbo/vt1dailyForecast?apiKey=d522aa97197fd864d36b418f39ebb323&format=json&geocode='
        complete_url = base_url + \
            str(location.latitude) + "%2C" + \
            str(location.longitude) + "&language=en-IN&units=m"
        print(complete_url)
        response = requests.get(complete_url)
        #response = Request(url=complete_url, headers=headers)
        #html = urlopen(response)
        data = response.json()
        if(datetime.now().strftime('%p') == "AM"):
            for day, temp, narrative in zip(data['vt1dailyForecast']['day']['dayPartName'], data['vt1dailyForecast']['day']['temperature'], data['vt1dailyForecast']['day']['narrative']):
                print(day, ': ', str(temp)+"ºC", "  ", narrative)
        else:
            for day, temp, narrative in zip(data['vt1dailyForecast']['night']['dayPartName'], data['vt1dailyForecast']['night']['temperature'], data['vt1dailyForecast']['night']['narrative']):
                print(day, ' :', str(temp)+"ºC", "  ", narrative)
    return response.content


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='Python CLI for Weather.com \n e.g python3 weather.py -p Bhopal -t 3')
    ap.add_argument("-p", "--place", required=True,
                    help="Name of the City/Place")
    ap.add_argument("-d", "--date", default='today',
                    help="Date \n[default : Current Time]")
    ap.add_argument("-t", "--type", default="daily", type=int,
                    help="Type of Forecast: 1: Daily, 2: Hourly, 3: 5-Days, 4: 10-Days, 5: Weekend, 6: Monthly. [Default: 1: Daily]")
    args = vars(ap.parse_args())
    Weather(args['place'], args['date'], args['type'])
