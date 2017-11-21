#!/usr/bin/python
''' server.py '''

import socket
import threading
import argparse
import json
import datetime
import netifaces
import requests
from aes import AESEncryption
from weather import weather
from currency import currency

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
        byteSize = 4096
        while True:
            #try:
                receivedData = client.recv(byteSize)
                if receivedData and type(receivedData) == bytes:
                    aesObject = AESEncryption(self.key)
                    receivedStr = aesObject.decrypt(receivedData).replace('!',"").replace('?',"")
                    client.sendall(aesObject.encrypt(self.formResponse(receivedStr, self.key, clientAddress)))
                else:
                    print('** Client Disconnected {}'.format(clientAddress))#when client disconnects
                    client.close()
                    return False
            #except Exception as e:#any exception in server.py
            #    print("{} - Disconnecting {}\n".format(e, clientAddress))
            #    client.close()
            #    return False

    def formResponse(self, receivedStr, key, clientAddress):
        keysFound, extraData = self.searchJSON(receivedStr)
        # IF ONLY PYTHON HAD SWITCH STATEMENTS <- :) :)
        if 'curse' in keysFound:
            return "Please watch your language."

        elif 'currency' in keysFound:
            if extraData.get('currency') != "":
                currencyInfo = extraData.get('currency')
                currencyData = currency()
                answer = currencyData.convert(currencyInfo['cFrom'],currencyInfo['cTo'],currencyInfo['amount'])
                if answer != "":
                    return "{} {} in {} is {}".format(currencyInfo['amount'],currencyInfo['cFrom'].upper(),currencyInfo['cTo'].upper(), answer)
            return "Sorry, I can't convert that."

        elif 'weather' in keysFound:
            clientIpData = self.getIpData(clientAddress)
            weatherData = weather()
            return weatherData.weatherResponse(keysFound, clientIpData, extraData)

        elif 'cinema' in keysFound:
            return "You are talking about cinema"

        elif 'ipinfo' in keysFound:
            ipData = self.getIpData(clientAddress)
            return "Your IP is {}, provided by {}.".format(ipData['query'], ipData['isp'])

        elif 'celery' in keysFound:
            return self.celery()

        else:
            return "Sorry, I don't understand what you are talking about."

    def getServerIP(self):
        ''' returns servers internal and external ip address '''
        deviseName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return {'internal': netifaces.ifaddresses(deviseName)[netifaces.AF_INET][0]['addr'],'external': self.getIpData('')['query']}

    def searchJSON(self, recievedStr):
        ''' Gets JSON data from a webpage - the git repo '''
        jsonData = json.load(open('keywords.json', encoding='utf-8'))
        recievedList = recievedStr.split(" ")
        keysFound = []
        extraData = {}
        for key in jsonData:                        #for each key in jsonData
            for keyword in jsonData[key]:           #get each keyword from the key
                for word in recievedList:           #for each word in recievedList
                    if word.lower() == keyword:     #if said word is a keyword

                        if key == 'location' and 'location' not in keysFound:                           #if the key is 'location', and a location has not yet been found
                            try:                                                                        #try
                                extraData['location'] = recievedList[recievedList.index(word) + 1]      #to add the following word to extraData
                                keysFound.append(key)                                                   #and add the key to keysFound
                            except:                                                                     #otherwise
                                continue                                                                #continue

                        elif key == 'currency' and 'currency' not in keysFound:                     #if the key is 'currency', and a currency has not yet been found
                            keysFound.append(key)                                                   #add the key to keysFound
                            currencyData = currency()                                               #create an instance of the class 'currency'
                            extraData['currency'] = currencyData.inputStr(recievedStr)              #then return the currency conversion and add this to extraData

                        elif key == 'time' and 'time' not in keysFound:
                            keysFound.append(key)
                            extraData['time'] = keyword

                        else:
                            if key not in keysFound:
                                keysFound.append(key)
                        continue

        return keysFound, extraData

    def celery(self):
        '''Celery man easter egg'''
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
