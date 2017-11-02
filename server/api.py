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
    count = 0
    limit = 3 # new limit
    url = 'http://api.cinelist.co.uk/search/cinemas/postcode/' 
    locality = post_code.replace(' ', '%20')
    final_url = url + locality 
    response = urllib.request.urlopen(final_url).read() 
    json_obj = str(response, 'utf-8')
    data = json.loads(json_obj)   
    for item in data['cinemas']:
        print (str(count+1),".",item['name'], item['distance'], "miles") #
        count += 1
        if count == limit: #print only first 3 cinemas
            break
locu_search(input("What is your postcode? ")) # take user input
#finding nearest cinema using postcode
