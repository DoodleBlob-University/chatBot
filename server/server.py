#!/usr/bin/python
''' server.py '''

import socket
import threading
import argparse
import json
import netifaces
import requests

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
                client.settimeout(120)
                threading.Thread(target=self.receiveFromClient,args = (client, clientAddress)).start()
                print('** Client Connected {} - {}'.format(clientAddress, self.getIpData(clientAddress)['city']))
            except:
                raise Exception('Client connection error')

    def getIpData(self, clientAddress):
        '''gets ip information in json format from ip address'''
        request = requests.get('http://ip-api.com/json/{}'.format(clientAddress))
        requestJson = request.json()
        if requestJson['status'] == 'success':
            return requestJson
        else:
            return self.getIpData('') #gets the ip for the server as oppose to client - as they should be on the same network

    def receiveFromClient(self, client, clientAddress):
        ''' receiveFromClient handles incoming data from clients '''
        byteSize = 1024
        while True:
            try:
                receivedData = client.recv(byteSize)
                if receivedData and type(receivedData) == bytes:
                    receivedStr = receivedData.decode().replace('!',"").replace('?',"").replace('.',"")
                    client.sendall(self.formResponse(receivedStr, self.key))
                else:
                    print('** Client Disconnected {}'.format(clientAddress))
                    client.close()
                    return False
            except Exception as e:
                print("{} - Disconnecting {}\n".format(e, clientAddress))
                client.close()
                return False

    def formResponse(self, receivedStr, key):
        from aes import AESEncryption
        aesObject = AESEncryption(key)
        keyWord = str(self.searchJSON(receivedStr))
        if keyWord == "['weather']": 
            return aesObject.encrypt("You are talking about weather")
        elif keyWord == "['cinema']":
            return aesObject.encrypt("You are talking about cinema")
        elif keyWord == "['celery']":
            return aesObject.encrypt(self.celery())
        else: 
            return aesObject.encrypt("Sorry, I don't understand what you are talking about.")

    def getServerIP(self):
        ''' returns servers internal and external ip address '''
        deviseName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return {'internal': netifaces.ifaddresses(deviseName)[netifaces.AF_INET][0]['addr'],'external': self.getIpData('')['query']}

    def searchJSON(self, recievedStr):
        ''' Gets JSON data from a webpage - the git repo '''
        request = requests.get('https://github.coventry.ac.uk/raw/eggintod/chatBot/master/server/keywords.json?token=AAAH3f6uTRxnnISwgawNP_h741zJFpLbks5aBGZXwA%3D%3D')
        jsonData = request.json()
        recievedList = recievedStr.split(" ")
        found = []
        for key in jsonData:
            for keyword in jsonData[key]:
                for word in recievedList:
                    if word.lower() == keyword:
                        found.append(word)
                        return [key]

    def celery(self):
        from random import randint
        rand = randint(0, 3)
        celerystring = b""
        if rand == 0: celerystring = "Good morning Paul, what will your first sequence of the day be?"
        elif rand == 1: celerystring = "Load sequence Oyster"
        elif rand == 2: celerystring = "4d3d3 engaged"
        elif rand == 3: celerystring = "Generating nude Tayne"
        return celerystring

    def encrypt(self, rawData, key):
        aesObject = AES.new(key, AES.MODE_CBC, )
        encryptedData = aesObject.encrypt(rawData)

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
