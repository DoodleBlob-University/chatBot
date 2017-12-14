### Mitko Donchev
import requests
import urllib.request
import json
import time


def fetchCinema(location):
    returnstring = ""
    """This function takes the location from the previous one as an input and prints
    the first five closest cinemas in a radius of 3,5 miles.- Mitko Donchev"""
    count = 0 #set count to 0
    limit = 5 #set a limit
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get( #retrive data from a website
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=" + str(location.get('latitude')) + "," + str(location.get('longitude')) + "&distance=10",
            headers={ #api key to get access to the data
                "X-API-Key": "VFMy2YO0yMDVtpkopLI6pDGtNrY9O0Ww",
            },
        )
        response = str(response.json())
        response_one = str(response.replace("'", '"'))
        response_one = str(response_one.replace('"s ',"'s "))  #make a lot of replaces to avoid any errors
        response_one = str(response_one.replace('"s, ',"'s, "))
        response_one = str(response_one.replace('"s.',"'s."))
        response_one = str(response_one.replace('k"s',"k's")) #make a lot of replaces to avoid any errors
        response_one = str(response_one.replace("\\x"," "))
        response_one = str(response_one.replace('"t ',"'t "))
        response_one = str(response_one.replace('"t, ',"'t, ")) #make a lot of replaces to avoid any errors
        response_one1 = str(response_one.replace("None", '"Null"'))
        data = json.loads(response_one1) #decode the data
        returnstring += "These are the closest cinemas to your location:\n"
        for item in data['cinemas']: #accessing a key in the dictionary
            returnstring += str((str(count+1)+"."+"Cinema name: "+item['name']) + "\n") #by using for loop it prints only the first five closest cinemas
            returnstring += str("-"*(len(item['name'])+23) + "\n")
            count += 1
            if count == limit:
                break #for loop stops when it reaches the limit
    except requests.exceptions.RequestException: #an exception if the data can't be retrived
        returnstring += 'HTTP Request failed\n'
    return returnstring


def searchCinema(location):
    """This function takes the location from the first function as input and gives
    all information about the closest cinemas as output but do not print it to the user - Mitko Donchev"""
    count = 0
    limit = 5
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=" + str(location.get('latitude')) + "," + str(location.get('longitude')) + "&distance=10",
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
        IDC = [] #creating a new empty list
        count1 = 0
        for item in data['cinemas']:
            IDC.append(str(item['id']))   #append information about every cinema in the list
            IDC.append(str(item['telephone'])) #append information about every cinema in the list
            IDC.append(str(item['website'])) #append information about every cinema in the list
            IDC.append(str(item['name'])) #append information about every cinema in the list
            count1 += 1
            if count1 > 8:
                break
        return (IDC) #return the IDC list as an output and use it in the last function
    except requests.exceptions.RequestException:
        return 'HTTP Request failed'


def showTime(IDC, userinput):
    """This function is using information from the previous function
    as input and present to the user all the iformation for the selected cinema and the showtime.- Mitko Donchev """
    returnstring = ""
    cinemaIDlist = list(IDC) #use the output from the previous function and put it into a list


    try: #checks if the input is valid or not by tring to execute the code block
        user_cin = int(userinput)
        if user_cin == 1:   #according to user choice execute different code block using if statements
            try:
                response = requests.get( #takes information about showtimes for the cinema chosen by the user
                    url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[0], #use information from cinemaIDlist to replace cinema id for each cinema
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
                returnstring += "There is some more information about the " + str(cinemaIDlist[3])+ ":" + "\n" #use information from cinemaIDlist to replace the information for each cinema
                returnstring += "-"*70 + "\n"
                returnstring += 'Telepehone: ' + str(cinemaIDlist[1]) + "\n" #use information from cinemaIDlist to replace the information for each cinema
                returnstring += 'Website: ' + str(cinemaIDlist[2]) + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += "Showtime for this cinema:\n"
                for item in data['movies']: #accessing a key in the dictionary
                    returnstring += str(str(countnew+1) +"." + "Title:" + "" + item['title'] + "\n" + " Image:" + item['poster_image_thumbnail'] + "\n") #print the showtime - first five more popular movies
                    countnew += 1
                    if countnew == limitnew:
                        break
                returnstring += "-"*70 + "\n"
            except requests.exceptions.RequestException:
                returnstring += 'HTTP Request failed\n'
        elif user_cin == 2:
            try:
                response = requests.get(
                    url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[4],
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
                returnstring += "There is some more information about the " + str(cinemaIDlist[7])+ ":" + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += 'Telepehone: ' + str(cinemaIDlist[5]) + "\n"
                returnstring += 'Website: ' + str(cinemaIDlist[6]) + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += "Showtime for this cinema:" + "\n"
                for item in data['movies']:
                    returnstring += str(str(countnew+1) +"." + "Title:" + "" + item['title'] + "\n" + " Image:" + item['poster_image_thumbnail'] + "\n") #print the showtime - first five more popular movies
                    countnew += 1
                    if countnew == limitnew:
                        break
                returnstring += "-"*70 + "\n"
            except requests.exceptions.RequestException:
                returnstring += 'HTTP Request failed' + "\n"
        elif user_cin == 3:
            try:
                response = requests.get(
                    url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[8],
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
                returnstring += "There is some more information about the " + str(cinemaIDlist[11])+ ":" + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += 'Telepehone: ' + str(cinemaIDlist[9]) + "\n"
                returnstring += 'Website: ' + str(cinemaIDlist[10]) + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += "Showtime for this cinema:" + "\n"
                for item in data['movies']:
                    returnstring += str(str(countnew+1) +"." + "Title:" + "" + item['title'] + "\n" + " Image:" + item['poster_image_thumbnail'] + "\n") #print the showtime - first five more popular movies
                    countnew += 1
                    if countnew == limitnew:
                        break
                returnstring += "-"*70 + "\n"
            except requests.exceptions.RequestException:
                returnstring += 'HTTP Request failed'+ "\n"
        elif user_cin == 4:
            try:
                response = requests.get(
                    url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[12],
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
                returnstring += "There is some more information about the " + str(cinemaIDlist[15])+ ":" + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += 'Telepehone: ' + str(cinemaIDlist[13]) + "\n"
                returnstring += 'Website: ' + str(cinemaIDlist[14]) + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += "Showtime for this cinema:" + "\n"
                for item in data['movies']:
                    returnstring += str(str(countnew+1) +"." + "Title:" + "" + item['title'] + "\n" + " Image:" + item['poster_image_thumbnail'] + "\n") #print the showtime - first five more popular movies
                    countnew += 1
                    if countnew == limitnew:
                        break
                returnstring += "-"*70 + "\n"
            except requests.exceptions.RequestException:
                returnstring += 'HTTP Request failed\n'
        elif user_cin == 5:
            try:
                response = requests.get(
                    url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[16],
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
                returnstring += "There is some more information about the " + str(cinemaIDlist[19])+ ":" + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += 'Telepehone: ' + str(cinemaIDlist[17]) + "\n"
                returnstring += 'Website: ' + str(cinemaIDlist[18]) + "\n"
                returnstring += "-"*70 + "\n"
                returnstring += "Showtime for this cinema:\n"
                for item in data['movies']:
                    returnstring += str(str(countnew+1) +"." + "Title:" + "" + item['title'] + "\n" + " Image:" + item['poster_image_thumbnail'] + "\n") #print the showtime - first five more popular movies
                    countnew += 1
                    if countnew == limitnew:
                        break
                returnstring += "-"*70 + "\n"
            except requests.exceptions.RequestException:
                returnstring += 'HTTP Request failed' + "\n"
        returnstring += "Input any string to exit cinema mode\n" #ask the user if he/she wants to see the showtime and the information another cinema
        return returnstring

    except:  #if the input is wrong the while loop starts again untill the input is valid
        return "Wrong cinema! Please try again by chosing the right number!"

#showTime(searchCinema({'latitude': 52.4167, 'longitude': -1.55}))
