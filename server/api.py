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
    limit = 3
    url = 'http://api.cinelist.co.uk/search/cinemas/postcode/' 
    locality = post_code.replace(' ', '%20')
    final_url = url + locality 
    response = urllib.request.urlopen(final_url).read() 
    json_obj = str(response, 'utf-8')
    data = json.loads(json_obj)
    for item in data['cinemas']:
        print (str(count+1),".",item['name'],item['distance'], "miles")  
        print(" ")
        time.sleep(1.5)
        count += 1
        if count == limit:
            break
locu_search(input("What is your postcode? "))

def send_request(IDC):
    count = 0
    limit = 3
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=52.4,-1.5&distance=18",
            params={
                "countries": "GB",
            },
            headers={
                "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
            },
        )
        response = str(response.json())
        response_one = str(response.replace("'", '"'))
        response_one = str(response_one.replace("None", '"Null"'))
        data = json.loads(response_one)
        for item in data['cinemas']:
            IDC = str(item['id'])
            count = 0
            limit = 3
            user_cin = int(input("For which cinema do you want more information (pick a number)? "))
            if user_cin == 1:
                cinemaID = IDC
                print(cinemaID)  
                try:
                    response = requests.get(
                        url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaID,
                        params={
                            "countries": "GB",
                        },
                        headers={
                            "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
                        },
                    )
                    response = str(response.json())
                    response_one = str(response.replace("'", '"'))
                    response_one = str(response_one.replace("None", '"Null"'))                
                    data = json.loads(response_one)
                    for item in data['movies']:
                        print (str(count+1),".","Title:","",item['title'],"\n","Image:","",item['poster_image_thumbnail'])  
                        print(" ")
                        time.sleep(1.5)
                        count += 1
                        if count == limit:
                            break
            #print("For which cinema do you want more information (pick a number)? ")
            #user_cin = input().int()
                           
                except requests.exceptions.RequestException:
                    print('HTTP Request failed')
        
        
            #print (str(count+1),".","Name:","",item['name'],"\n","Telephone:","",item['telephone'])  
            #print(" ")
            #time.sleep(1.5)
            count += 1
            if count == limit:
                break
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
send_request("33223")
### Not finished
