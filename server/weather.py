#!/usr/bin/python
import requests

class weather(object):
    def __init__(self, time, coordinates):
        self.time = time
        self.coordinates = coordinates
        self.forcastApiKey = '1cd16597539dafae0c09187ef4dc19bc'
        self.url = 'https://api.darksky.net/forecast/{}/{},{}?units=auto'.format(self.forcastApiKey, self.coordinates['latitude'], self.coordinates['longitude'])
            
    def forcastRequest(self, url):
        request = requests.get(url)
        return request.json()
