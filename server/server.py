#!/usr/bin/python
''' server.py '''

import socket
import threading
import argparse
import json
import netifaces
import requests
from aes import AESEncryption
from weather import weather

class server(object):
    ''' server is a class that handled network connections, pass host ip and host port for init'''
    def __init__(self, hostIP, hostPort, key):
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.key = key
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostIP, self.hostPort))
        print('** server started on\n** internal - {}:{}\n** external - {}:{}\n'.format(self.getServerIP()['internal'], self.hostPort,self.getServerIP()['external'] ,self.hostPort))

    def serverListen(self):
        ''' serverListen listens to incoming connects from clients and opens a new thread for each connected client '''
        self.socket.listen(15)
        while True:
            try:
                client, clientAddress = self.socket.accept()
                client.settimeout(300)
                threading.Thread(target=self.receiveFromClient,args = (client, clientAddress)).start()
                print('** Client Connected {} - {}'.format(clientAddress, self.getIpData(clientAddress)['city']))
            except:
                raise Exception('Client connection error')

    def getIpData(self, clientAddress):
        '''gets ip information in json format from ip address'''
        request = requests.get('http://ip-api.com/json/{}'.format(clientAddress))#gets data about the clients ip
        requestJson = request.json()
        if requestJson['status'] == 'success':#if received succesfully
            return requestJson
        else:
            return self.getIpData('') #else gets the ip for the server when the client is on the same network

    def receiveFromClient(self, client, clientAddress):
        ''' receiveFromClient handles incoming data from clients '''
        byteSize = 1024
        while True:
            #try:
                receivedData = client.recv(byteSize)
                if receivedData and type(receivedData) == bytes:
                    aesObject = AESEncryption(self.key)
                    receivedStr = aesObject.decrypt(receivedData).replace('!',"").replace('?',"").replace('.',"")
                    client.sendall(self.formResponse(receivedStr, self.key, clientAddress))
                else:
                    print('** Client Disconnected {}'.format(clientAddress))#when client disconnects
                    client.close()
                    return False
            #except Exception as e:#any exception in server.py
            #    print("{} - Disconnecting {}\n".format(e, clientAddress))
            #    client.close()
            #    return False

    def formResponse(self, receivedStr, key, clientAddress):
        aesObject = AESEncryption(key)
        keysFound, wordLocation, time = self.searchJSON(receivedStr)
        # IF ONLY PYTHON HAD SWITCH STATEMENTS <- :) :)
        if 'curse' in keysFound:
            return aesObject.encrypt("Please watch your language, you absolute ****!")
        elif 'weather' in keysFound:
            clientIpData = self.getIpData(clientAddress)
            if 'location' not in keysFound:#if no location is specified
                clientIpData = self.getIpData(clientAddress)
                location = {'latitude': clientIpData['lat'], 'longitude': clientIpData['lon']}#puts location data from IP in dictionary
                weatherData = weather(None, location)#weatherData = weather class from weather.py
                return aesObject.encrypt('It is currently {} and the temperature is {}'.format(weatherData.currently['summary'],str(weatherData.currently['temperature'])))
            else:#when a location is given
                from geoCode import geoCode as location
                lat, lng = location.getLocationCoords(wordLocation, clientIpData['countryCode'])#gets longitude and latitude from google geocode
                location = {'latitude': lat, 'longitude': lng}#puts into dictionary
                weatherData = weather(None, location)#weatherData = weather class from weather.py
                return aesObject.encrypt('It is currently {} in {}, and the temperature is {}'.format(weatherData.currently['summary'],wordLocation.capitalize(),str(weatherData.currently['temperature'])))
        elif 'cinema' in keysFound:
            return aesObject.encrypt("You are talking about cinema")
        elif 'ipinfo' in keysFound:
            query = self.getIpData(clientAddress)['query']
            isp = self.getIpData(clientAddress)['isp']
            return aesObject.encrypt("Your IP is {}, provided by {}.".format(query, isp))
        elif 'celery' in keysFound:
            return aesObject.encrypt(self.celery())
        else:
            return aesObject.encrypt("Sorry, I don't understand what you are talking about.")

    def getServerIP(self):
        ''' returns servers internal and external ip address '''
        deviseName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return {'internal': netifaces.ifaddresses(deviseName)[netifaces.AF_INET][0]['addr'],'external': self.getIpData('')['query']}

    def searchJSON(self, recievedStr):
        ''' Gets JSON data from a webpage - the git repo '''
        jsonData = json.load(open('keywords.json', encoding='utf-8'))
        recievedList = recievedStr.split(" ")
        keysFound = []
        location = ''
        time = ''
        for key in jsonData:
            for keyword in jsonData[key]:
                for word in recievedList:
                    if word.lower() == keyword:
                        if key == 'location':
                            if 'location' not in keysFound: #if a location keyword has not been found...
                                try: #gets the next word after "in" or "at" which should be the location
                                    location = recievedList[recievedList.index(word) + 1]
                                    keysFound.append(key)#adds 'Location' to keysFound
                                except: #if the next word dosent exist and it goes out of bound of the array
                                    continue
                            else:#if a location keyword has already been found... - ignore all future location keywords
                                continue
                        if key == 'time':
                            time = word
                        else:#add key to keysFound
                            keysFound.append(key)
                        continue
        return keysFound, location, time

    def celery(self):
        from random import randint
        rand = randint(0, 3)
        celerystring = b""
        if rand == 0: celerystring = "Good morning Paul, what will your first sequence of the day be?"
        elif rand == 1: celerystring = "Load sequence Oyster"
        elif rand == 2: celerystring = "4d3d3 engaged"
        elif rand == 3: celerystring = "Generating nude Tayne"
        return celerystring

def getArgs():
    ''' getArgs returns all program arguments '''
    parser = argparse.ArgumentParser(description='') # Add description
    parser.add_argument('-p', '--port', metavar='Port', default=1143, type=int, help='Server port')
    parser.add_argument('-k', '--key', metavar='Key', default='gbaei395y27ny9', type=str, help='Encryption Key')
    return parser.parse_args()

def drawHeader():
    ''' draws program ui header '''
    print('*** Server Header ***\nWelcome\n\n')

def main():
    ''' main '''
    drawHeader()
    args = getArgs()
    if args.port != 1143:
        print('** no server port specified using default')
    server('', args.port, args.key).serverListen() # i have passed empty string for the host ip as it will be filled in later

if __name__ == '__main__':
    main()
