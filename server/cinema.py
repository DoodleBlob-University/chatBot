import requests
import urllib.request
import json
import time

def cinemaSearch():
    """This function takes the location from the previous one as an input and prints
    the first five closest cinemas in a radius of 3,5 miles.- Mitko Donchev"""
    longlat = list(findLocation()) #using the output from the previous function and store it in a list
    count = 0
    limit = 5 #set a limit
    #https://api.internationalshowtimes.com/v4/cinemas/?location=52.5,13.37&distance=1000
    try:
        response = requests.get(
            url="https://api.internationalshowtimes.com/v4/cinemas/?location=" + str(longlat[0])  + "," + str(longlat[1]) + "&distance=10", #using the first and the second values in the list 
            params={ #setting parameters
                "countries": "GB",
            },
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
        print(" ")
        print("Searching. Please wait... ")
        time.sleep(1.5)  #make an ilusion that the program is thinking 
        print("These are the closest cinemas to your location:")
        for item in data['cinemas']: #accessing a key in the dictionary
            print (str(count+1),".","Cinema name: ",item['name']) #by using for loop it prints only the first five closest cinemas
            print("-"*(len(item['name'])+23))
            time.sleep(0.8)
            count += 1
            if count == limit:
                break #for loop stops when it reaches the limit
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
        print('HTTP Request failed')
        

def showTime(IDC):
    """This function is using information from the previous function 
    as input and present to the user all the iformation for the selected cinema and the showtime.- Mitko Donchev """
    cinemaIDlist = list(IDC) #use the output from the previous function and make it a list
    while True: #using while loop to give the user an option to get information about several cinemas 
        try: #checks if the input is valid or not by tring to execute the code block
            user_cin = int(input("For which cinema do you want more information (pick a number)? ")) #askoing user to choose a cinema
            print(" ")
            print("Loading...")
            time.sleep(1.5)
            print("-"*70)
            if user_cin == 1:   #according to user choice execute different code block using if statements
                try:
                    response = requests.get( #takes information about showtimes for the cinema chosen by the user
                        url="https://api.internationalshowtimes.com/v4/movies/?cinema_id=" + cinemaIDlist[0], #use information from cinemaIDlist to replace cinema id for each cinema
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
                    print("There is some more information about the " + str(cinemaIDlist[3])+ ":") #use information from cinemaIDlist to replace the information for each cinema
                    time.sleep(0.5)
                    print("-"*70)
                    print('Telepehone: ' + str(cinemaIDlist[1])) #use information from cinemaIDlist to replace the information for each cinema
                    print('Website: ' + str(cinemaIDlist[2]))
                    print("-"*70)
                    print("Showtime for this cinema:")
                    for item in data['movies']:
                        print (str(countnew+1),".","Title:","",item['title'],"\n"," ","Image:","",item['poster_image_thumbnail']) #print the showtime - first five more popular movies 
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
            print("Do you want to see information about another cinema? Y/N") #ask the user if he/she wants to see the showtime and the information another cinema 
            mode = input().lower()
            if mode == "y" or mode == "yes" or mode == "yeah":
                continue #if the answer is yes the while loop repeat again 
            else: #else the program ends by printing a message and waits the user to press enter
                print("Thank you! Have a nice day!")
                exit = input("Press enter!")
                break  #while loop stops.     
        except:  #if the input is wrong the while loop starts again untill the input is valid 
            print("Wrong cinema! Please try again by chosing the right number!") 
showTime(cinemaID())
