#!/usr/bin/python
import requests

class geoCode(object):

    def __init__(self):
        self.googleApiKey = 'AIzaSyDiqfHUyzaaCEPr2gF04NPFyhR7Iew30vs'

    def getLocationCoords(self, location, country):
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=+{}+{}&key={}'.format(location, country, self.googleApiKey)
        request = requests.get(url)
        placeinfo = request.json()
        return placeinfo['results'][0]['geometry']['location']['lat'], placeinfo['results'][0]['geometry']['location']['lng']