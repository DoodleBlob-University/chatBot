#!/usr/bin/python
import requests

class geocode(object):

    def __init__(self):
        self.googlePlaces = 'AIzaSyDQ-mcgK1gSnI6soXWZnAA2Z9MeDnb5ZRo'
        self.googleGeocode = 'AIzaSyDiqfHUyzaaCEPr2gF04NPFyhR7Iew30vs'

    def getLocationCoords(self, location):
        placeID = self.getPlaceID(location)
        if placeID != "":
            url = 'https://maps.googleapis.com/maps/api/geocode/json?place_id={}&key={}'.format(placeID, self.googleGeocode)
            request = requests.get(url)
            placeinfo = request.json()
            if placeinfo['status'] == 'OK':
                return placeinfo['results'][0]['geometry']['location']['lat'], placeinfo['results'][0]['geometry']['location']['lng']
        return "",""

    def getPlaceID(self, location):
        url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={}&types=geocode&key={}'.format(location, self.googlePlaces)
        request = requests.get(url)
        placeinfo = request.json()
        if placeinfo['status'] == "OK":
            return placeinfo['predictions'][0]['place_id']
        return ""

    #ChIJtyJuZVGxcEgRiQZPVvVg9gQ
