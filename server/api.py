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

def checkPostcode():
    """This function takes a postcode as an inpit and check it is valid or not - Mitko Donchev"""
    #https://api.postcodes.io/postcodes//validate
    post_code1 = []
    while True:
        try:
            print("Could you tell me your postcode? ")
            post_code = input().lower()
            response = requests.get(
                url="https://api.postcodes.io/postcodes/" + post_code + "/validate",
            )
            response = str(response.json())
            response_one = str(response.replace("'", '"'))
            response_one = str(response.replace("True", '"True"'))
            response_one = str(response_one.replace("'", '"'))
            data = json.loads(response_one)
            if data["result"] == "True":
                break
        except ValueError:
            print("Worng postcode! Please try again...")
    return(post_code)

post_code1 = checkPostcode()
def findLocation():
    """This function use a postcode and gives the location as an output, but do not print it - Mitko Donchev"""
    #https://api.getaddress.io/find/" + post_code + "?api-key=yKq60w4JvkuDFJUgGjtHjg11049
    post_code = post_code1
    try:
        response = requests.get(
            url="https://api.getaddress.io/find/" + post_code + "?api-key=hLpgUfHQU0eAculh2semoQ11095",
        )
        longlat = []
        response = str(response.json())
        response_one = str(response.replace("'", '"'))
        response_one = str(response_one.replace("None", '"Null"'))
        data = json.loads(response_one)
        longlat.append(round(data['latitude'], 3))
        longlat.append(round(data['longitude'], 3))
        return(longlat)
    except requests.exceptions.RequestException:
        print('HTTP Request failed') 

def cinemaSearch():
    """This function takes the location from the previous one as an input and prints
    the first five closest cinemas in a radius of 3,5 miles."""
    longlat = list(findLocation())
    count = 0
    limit = 5
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=" + str(longlat[0]) + "," + str(longlat[1]) + "&distance=10",
            params={
                "countries": "GB",
            },
            headers={
                "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
            },
        )
        response = str(response.json())
        response_one = str(response.replace("'", '"'))
        response_one = str(response_one.replace('"s ',"'s "))
        response_one = str(response_one.replace('"s, ',"'s, "))
        response_one = str(response_one.replace('"s.',"'s."))
        response_one = str(response_one.replace('k"s',"k's"))
        response_one = str(response_one.replace("\\x"," "))
        response_one = str(response_one.replace('"t ',"'t "))
        response_one = str(response_one.replace('"t, ',"'t, "))
        response_one1 = str(response_one.replace("None", '"Null"'))
        data = json.loads(response_one1)
        print(" ")
        print("Searching. Please wait... ")
        time.sleep(1.5)
        print("These are the closest cinemas to your location:")
        for item in data['cinemas']:
            print (str(count+1),".","Cinema name: ",item['name'])   
            print("-"*(len(item['name'])+23))
            time.sleep(0.8)
            count += 1
            if count == limit:
                break 
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
cinemaSearch()

def cinemaID():
    """This function takes the location from the first function as input and gives 
    all information about the closest cinemas as output but do not print it to the user - Mitko Donchev"""
    longlat = list(findLocation())
    count = 0
    limit = 5
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=" + str(longlat[0]) + "," + str(longlat[1]) + "&distance=10",
            params={
                "countries": "GB",
            },
            headers={
                "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
            },
        )
        response = str(response.json())
        response_one = str(response.replace("'", '"'))
        response_one = str(response_one.replace('"s ',"'s "))
        response_one = str(response_one.replace('"s, ',"'s, "))
        response_one = str(response_one.replace('"s.',"'s."))
        response_one = str(response_one.replace('k"s',"k's"))
        response_one = str(response_one.replace("\\x"," "))
        response_one = str(response_one.replace('"t ',"'t "))
        response_one = str(response_one.replace('"t, ',"'t, "))
        response_one1 = str(response_one.replace("None", '"Null"'))
        data = json.loads(response_one1)
        IDC = []
        count1 = 0
        for item in data['cinemas']:
            IDC.append(str(item['id']))
            IDC.append(str(item['telephone']))
            IDC.append(str(item['website']))
            IDC.append(str(item['name']))
            count1 += 1
            if count1 > 8:
                break  
        return (IDC)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
        

def showTime(IDC):
    """This function is using information from the previous function 
    as input and present to the user all the iformation for the selected cinema and the showtime."""
    cinemaIDlist = list(IDC)
    while True:
        try:
            user_cin = int(input("For which cinema do you want more information (pick a number)? "))
            print(" ")
            print("Loading...")
            time.sleep(1.5)
            print("-"*70)
            if user_cin == 1:   
                try:
                    response = requests.get(
                        url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[0],
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
                    response_one = str(response_one.replace('"t ',"'t "))
                    response_one1 = str(response_one.replace("None", '"Null"'))
                    data = json.loads(response_one1)
                    print("There is some more information about the " + str(cinemaIDlist[3])+ ":")
                    time.sleep(0.5)
                    print("-"*70)
                    print('Telepehone: ' + str(cinemaIDlist[1]))
                    print('Website: ' + str(cinemaIDlist[2]))
                    print("-"*70)
                    print("Showtime for this cinema:")
                    for item in data['movies']:
                        print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                        time.sleep(0.8)
                        countnew += 1
                        if countnew == limitnew:
                            break
                    print("-"*70)
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
                    response_one = str(response_one.replace('"t ',"'t "))
                    response_one1 = str(response_one.replace("None", '"Null"'))
                    data = json.loads(response_one1)
                    print("There is some more information about the " + str(cinemaIDlist[7])+ ":")
                    time.sleep(0.5)
                    print("-"*70)
                    print('Telepehone: ' + str(cinemaIDlist[5]))
                    print('Website: ' + str(cinemaIDlist[6]))
                    print("-"*70)
                    print("Showtime for this cinema:")
                    time.sleep(0.9)
                    for item in data['movies']:
                        print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                        time.sleep(0.8)
                        countnew += 1
                        if countnew == limitnew:
                            break
                    print("-"*70)
                except requests.exceptions.RequestException:
                    print('HTTP Request failed') 
            elif user_cin == 3:
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
                    response_one = str(response_one.replace('"t ',"'t "))            
                    response_one1 = str(response_one.replace("None", '"Null"'))
                    data = json.loads(response_one1)
                    print("There is some more information about the " + str(cinemaIDlist[11])+ ":")
                    time.sleep(0.5)
                    print("-"*70)
                    print('Telepehone: ' + str(cinemaIDlist[9]))
                    print('Website: ' + str(cinemaIDlist[10]))
                    print("-"*70)
                    print("Showtime for this cinema:")
                    time.sleep(0.9)
                    for item in data['movies']:
                        print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                        time.sleep(0.8)
                        countnew += 1
                        if countnew == limitnew:
                            break
                    print("-"*70)                
                except requests.exceptions.RequestException:
                    print('HTTP Request failed')       
            elif user_cin == 4:
                try:
                    response = requests.get(
                        url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[12],
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
                    response_one = str(response_one.replace('"t ',"'t "))
                    response_one1 = str(response_one.replace("None", '"Null"'))
                    data = json.loads(response_one1)
                    print("There is some more information about the " + str(cinemaIDlist[15])+ ":")
                    time.sleep(0.5)
                    print("-"*70)
                    print('Telepehone: ' + str(cinemaIDlist[13]))
                    print('Website: ' + str(cinemaIDlist[14]))
                    print("-"*70)
                    print("Showtime for this cinema:")
                    time.sleep(0.9)
                    for item in data['movies']:
                        print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                        time.sleep(0.8)
                        countnew += 1
                        if countnew == limitnew:
                            break
                    print("-"*70)
                except requests.exceptions.RequestException:
                    print('HTTP Request failed') 
            elif user_cin == 5:
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
                    response_one = str(response_one.replace('"t ',"'t "))
                    response_one1 = str(response_one.replace("None", '"Null"'))
                    data = json.loads(response_one1)
                    print("There is some more information about the " + str(cinemaIDlist[19])+ ":")
                    time.sleep(0.5)
                    print("-"*70)
                    print('Telepehone: ' + str(cinemaIDlist[17]))
                    print('Website: ' + str(cinemaIDlist[18]))
                    print("-"*70)
                    print("Showtime for this cinema:")
                    time.sleep(0.9)
                    for item in data['movies']:
                        print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail'])  
                        time.sleep(0.8)
                        countnew += 1
                        if countnew == limitnew:
                            break
                    print("-"*70)
                except requests.exceptions.RequestException:
                    print('HTTP Request failed') 
            print("Do you want to see information about another cinema? Y/N")
            mode = input().lower()
            if mode == "y" or mode == "yes" or mode == "yeah":
                continue
            else:
                print("Thank you! Have a nice day!")
                exit = input("Press enter!")
                break        
        except:
            print("Wrong cinema! Please try again by chosing the right number!") 
showTime(cinemaID())
