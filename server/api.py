#!/usr/bin/python
import requests

def apiCall(apiURL):
    request = requests.get(apiURL)
    return request.json()

if __name__ == '__main__':
    pass ## add tests here