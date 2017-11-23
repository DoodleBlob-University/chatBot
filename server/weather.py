#!/usr/bin/python
import requests

class weather(object):
    def __init__(self):
        self.forcastApiKey = '1cd16597539dafae0c09187ef4dc19bc'

    def forcastRequest(self, location):
        url = 'https://api.darksky.net/forecast/{}/{},{}?units=si'.format(self.forcastApiKey, location.get('latitude'), location.get('longitude'))
        request = requests.get(url)
        return request.json()

    def weatherResponse(self, keysFound, clientaddress, extra):
        location = {}
        locationStr = ""
        if 'location' in keysFound:
            from geocode import geocode
            geoCode = geocode()
            location = geoCode.getLocationCoords(extra.get('location'))
            if not location:
                return "Sorry, I can't fetch information about that location right now."
            locationStr = " in {}".format(extra.get('location').capitalize())
        else:
            location = {'latitude': clientaddress['lat'], 'longitude': clientaddress['lon']}
        weatherData = self.forcastRequest(location)
        if 'time' not in keysFound:
            return 'It is currently {}{} and the temperature is {} Celsius'.format(weatherData['currently']['summary'],locationStr,str(weatherData['currently']['temperature']))
        if extra.get('time') == 'daily':
            response = 'Daily Weather Forcast{}:\nSummary: {}\n\n'.format(locationStr, str(weatherData['daily']['summary']))
            count = 0
            for day in weatherData['daily']['data']:
                response = response + '{}:\nSummary: {}\nMax: {} @ {}\nMin: {} @ {}\n\n'.format(self.unixTimeToDateTime(day['time']),day['summary'],day['temperatureMax'],self.unixTimeToDateTime(day['temperatureMaxTime']),day['temperatureMin'],self.unixTimeToDateTime(day['temperatureMinTime']))
                count += 1
                if count == 8:
                    break
            return response
        elif extra.get('time') == 'hourly':
            response = 'Hourly Weather Forcast{}:\nSummary: {}\n\n'.format(locationStr, str(weatherData['hourly']['summary']))
            count = 0
            for day in weatherData['hourly']['data']:
                response = response + '{}:\nSummary: {}\nTempature: {} Celsius\n\n'.format(self.unixTimeToDateTime(day['time']),day['summary'],day['temperature'])
                count += 1
                if count == 8:
                    break
            return response
        return None

    def unixTimeToDateTime(self, unixTime):
        import datetime
        return datetime.datetime.fromtimestamp(int(unixTime)).strftime('%Y-%m-%d %H:%M')
