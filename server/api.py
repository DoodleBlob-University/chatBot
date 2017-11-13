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

print("What is your postcode? ")
post_code = input().lower()
def cinemaSearch():
    """This function takes a postcode as input and gives the first three closest cinemas as output"""
    count = 0
    limit = 3
    url = 'http://api.cinelist.co.uk/search/cinemas/postcode/' 
    locality = post_code.replace(' ', '%20')
    final_url = url + locality 
    response = urllib.request.urlopen(final_url).read() 
    json_obj = str(response, 'utf-8')
    data = json.loads(json_obj) 
    print("Searching. Please wait... ")
    time.sleep(1.5)
    for item in data['cinemas']:
        print (str(count+1),".","Cinema name: ",item['name'], "\n"," ","Distance:",item['distance'], "miles")   
        print(" ")
        time.sleep(1.5)
        count += 1
        if count == limit:
            break
cinemaSearch()

def findLocation():
    """This function use the postcode from the previous function and gives the location as an output, but do not print it"""
    #https://api.getaddress.io/find/" + post_code + "?api-key=yKq60w4JvkuDFJUgGjtHjg11049
    try:
        response = requests.get(
            url="https://api.getaddress.io/find/" + post_code + "?api-key=TQoCHFHv8EeFKg8CXzXISQ11057",
        )
        longlat = []
        response = str(response.json())
        response_one = str(response.replace("'", '"'))
        response_one = str(response_one.replace("None", '"Null"'))
        data = json.loads(response_one)
        longlat.append(round(data['latitude'], 1))
        longlat.append(round(data['longitude'], 1))
        return(longlat)
    except requests.exceptions.RequestException:
        print('HTTP Request failed') 
findLocation()

def cinemaID():
    """This function takes the location from the previous one as input and gives 
    all information about the closest cinemas as output but do not print it to the user"""
    longlat = list(findLocation())
    count = 0
    limit = 1
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=" + str(longlat[0]) + "," + str(longlat[1]) + "&distance=18",
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
        IDC = []
        count1 = 0
        for item in data['cinemas']:
            IDC.append(str(item['id']))
            IDC.append(str(item['telephone']))
            IDC.append(str(item['website']))
            IDC.append(str(item['name']))
            count1 += 1
            if count1 > 5:
                break  
        return (IDC)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
cinemaID()

user_cin = int(input("For which cinema do you want more information (pick a number)? "))
def showTime(IDC):
    """This function is using information from the previous function 
    as input and present to the user all the iformation and the showtime asoutput"""
    cinemaIDlist = list(IDC)
    print("Loading...")
    time.sleep(1.5)
    print(" ")
    if user_cin == 1:
        try:
            response = requests.get(
                url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[8],
                params={
                    "countries": "GB",
                },
                headers={
                    "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
                },
            )
            countnew = 0
            limitnew = 5
            response = str(response.json())
            response_one = str(response.replace("'", '"'))
            response_one = str(response_one.replace('"s ',"'s "))
            response_one1 = str(response_one.replace("None", '"Null"'))
            data = json.loads(response_one1)
            print('Cinema name: ' + str(cinemaIDlist[11]))
            print('Telepehone: ' + str(cinemaIDlist[9]))
            print('Website: ' + str(cinemaIDlist[10]))
            print("")
            print("Showtime for this cinema:")
            for item in data['movies']:
                print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                print(" ")
                time.sleep(0.8)
                countnew += 1
                if countnew == limitnew:
                    break
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
    elif user_cin == 2:
        try:
            response = requests.get(
                url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[4],
                params={
                    "countries": "GB",
                },
                headers={
                    "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
                },
            )
            countnew = 0
            limitnew = 5
            response = str(response.json())
            response_one = str(response.replace("'", '"'))
            response_one = str(response_one.replace('"s ',"'s "))
            response_one1 = str(response_one.replace("None", '"Null"'))
            data = json.loads(response_one1)
            print('Cinema name: ' + str(cinemaIDlist[7]))
            print('Telepehone: ' + str(cinemaIDlist[5]))
            print('Website: ' + str(cinemaIDlist[6]))
            print("")
            print("Showtime for this cinema:")
            for item in data['movies']:
                print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                print(" ")
                time.sleep(0.8)
                countnew += 1
                if countnew == limitnew:
                    break
        except requests.exceptions.RequestException:
            print('HTTP Request failed') 
    elif user_cin == 3:
        try:
            response = requests.get(
                url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[16],
                params={
                    "countries": "GB",
                },
                headers={
                    "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
                },
            )
            countnew = 0
            limitnew = 5
            response = str(response.json())
            response_one = str(response.replace("'", '"'))
            response_one = str(response_one.replace('"s ',"'s "))
            response_one1 = str(response_one.replace("None", '"Null"'))
            data = json.loads(response_one1)
            print('Cinema name: ' + str(cinemaIDlist[7]))
            print('Telepehone: ' + str(cinemaIDlist[17]))
            print('Website: ' + str(cinemaIDlist[18]))
            print("")
            print("Showtime for this cinema:")
            for item in data['movies']:
                print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                print(" ")
                time.sleep(0.8)
                countnew += 1
                if countnew == limitnew:
                    break
        except requests.exceptions.RequestException:
            print('HTTP Request failed')       
showTime(cinemaID())
print("Thank you! Have a nice day!")
exit = input("Press enter!")
