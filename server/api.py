#!/usr/bin/python
import requests
import urllib.request
import json
import time

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
        print (str(count+1),".",item['name'], item['distance'], "miles") 
        print(" ")
        time.sleep(1.5) # slow down the iteration
        count += 1
        if count == limit: #print only first 3 cinemas
            break
locu_search(input("What is your postcode? ")) # take user input
#finding nearest cinema using postcode

#https://api.themoviedb.org/3/movie/popular?api_key
def locu_search(region):
    region = region.upper()
    with open('Country.json') as data_file:
        dataC = json.load(data_file)
    for i in dataC['country']: #check if the country is real using json file
        if region in i['Name']:
            api_key = '2f04aec7f1a13d66bdce37ee3db645cb'
            count = 0
            limit = 3
            url = 'https://api.themoviedb.org/3/movie/popular?' 
            locality = region.replace(' ', '%20')
            final_url = url + 'api_key=' + api_key + '&language=en-US&page=1&region=' + locality 
            response = urllib.request.urlopen(final_url).read() 
            json_obj = str(response, 'utf-8')
            data = json.loads(json_obj) 
            print("The first three most popular movies now:")
            time.sleep(1.5)
            for item in data['results']:
                print (str(count+1),".","Title:","",item['original_title'],"\n","Overview:","",item['overview'],"\n","Release date:","",item['release_date'])  
                print(" ")
                time.sleep(1.5)
                count += 1
                if count == limit:
                    break
        else:
            print("Not a country!")
locu_search(input("What is your region? "))
#gives the first three most popular movies  
