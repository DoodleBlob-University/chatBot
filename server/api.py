#!/usr/bin/python
import requests
import urllib.request
import json

def apiCall(apiURL):
    request = requests.get(apiURL)
    return request.json()

if __name__ == '__main__':
    pass ## add tests here




#http://api.cinelist.co.uk/search/cinemas/postcode/LU12HN 
def locu_search(post_code):    
    url = 'http://api.cinelist.co.uk/search/cinemas/postcode/' 
    locality = post_code.replace(' ', '%20')
    final_url = url + locality 
    response = urllib.request.urlopen(final_url).read() 
    json_obj = str(response, 'utf-8')
    data = json.loads(json_obj)   
    for item in data['cinemas']:
        print (item['name'], item['distance'])
locu_search("CV12HR") 
#finding nearest cinema using postcode
