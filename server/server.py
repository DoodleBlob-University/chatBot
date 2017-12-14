import socket
import threading
import argparse
import json
import datetime
import netifaces ### imported module netifaces <https://pypi.python.org/pypi/netifaces> - 09/11/17
import requests ### imported module requests <https://pypi.python.org/pypi/requests> - 09/11/17
from aes import AESEncryption
from weather import weather
from currency import currency

class server(object): ### Dominic Egginton
    ''' server is a class that handled network connections, pass host ip, host port and AES key for init'''
    def __init__(self, hostIP, hostPort, key): ### Dominic Egginton
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.key = key
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostIP, self.hostPort))
        print('** server started on\n** internal - {}:{}\n** external - {}:{}\n'.format(self.getServerIP()['internal'], self.hostPort,self.getServerIP()['external'] ,self.hostPort))

    def serverListen(self): ### Dominic Egginton
        ''' serverListen listens to incoming connects from clients and opens a new thread for each connected client '''
        self.socket.listen(15)
        while True:
            try:
                client, clientAddress = self.socket.accept()
                client.settimeout(300)
                threading.Thread(target=self.receiveFromClient,args = (client, clientAddress)).start() # Open new thread for each client. calling receiveFromClient and pass the client socket and client address
                print('** Client Connected {} - {}'.format(clientAddress, self.getIpData(clientAddress)['city']))
            except:
                raise Exception('Client connection error')

    def getIpData(self, clientAddress): ### Dominic Egginton
        ''' getIpData returns ip data from http://ip-api.com/ in json format. pass client address as string '''
        request = requests.get('http://ip-api.com/json/{}'.format(clientAddress))
        requestJson = request.json()
        if requestJson['status'] == 'success':
            return requestJson
        else:
            return self.getIpData('') # recursive call in case client ip is in private range, therefore needs to get server ip data

    def receiveFromClient(self, client, clientAddress): ### Dominic Egginton
        ''' receiveFromClient handles incoming data from clients and sends formatted responses back to client '''
        byteSize = 4096 # large bytesize as we need to send and receive large data between client and server
        while True:
            try:
                receivedData = client.recv(byteSize)
                if receivedData and type(receivedData) == bytes:
                    aesObject = AESEncryption(self.key)
                    receivedStr = aesObject.decrypt(receivedData).replace('!',"").replace('?',"")
                    client.sendall(aesObject.encrypt(self.formResponse(receivedStr, clientAddress, client)))
                else:
                    print('** Client Disconnected {}'.format(clientAddress))
                    client.close()
                    return False
            except Exception as e:
                print("{} - Disconnecting {}\n".format(e, clientAddress))
                client.close()
                return False

    def formResponse(self, receivedStr, clientAddress, client): ### Charlie Barry and Dominic Egginton
        keysFound, extraData = self.searchJSON(receivedStr)
        # IF ONLY PYTHON HAD SWITCH STATEMENTS <- :) :)
        if 'curse' in keysFound: ### Tom has done the curse code
            return "Please watch your language."

        elif 'currency' in keysFound:
            if extraData.get('currency'):
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

        elif 'cinema' in keysFound: ### Charlie Barry and Mitko Donchev
            ### I apologise for the laziness of this code, need to patch it up sometime :( - Charlie
            from cinema import searchCinema, showTime, fetchCinema #imports all the functions from cinema.py
            clientIpData = self.getIpData(clientAddress)
            location = {'latitude': clientIpData['lat'], 'longitude': clientIpData['lon']}#gets the location of the client from their ip address
            aesObject = AESEncryption(self.key)
            client.sendall(aesObject.encrypt(fetchCinema(location) + "Select a cinema for more information (type 'back' to go back)"))#sends message to client
            while True:
                cinemaData = client.recv(4096)#interepts message sent from client
                cinemaStr = aesObject.decrypt(cinemaData).replace('!',"").replace('?',"")#decrypts message into plaintext
                if cinemaStr.lower() != 'back':
                    IDC = searchCinema(location)
                    extracinemainfo = showTime(IDC,cinemaStr)
                    client.sendall(aesObject.encrypt(extracinemainfo))#gets extra info for cinema and sends it to client
                    if not(extracinemainfo == 'Wrong cinema! Please try again by chosing the right number!'):#if user inputted a legitimate answer
                        cinemaData = client.recv(4096)#recieve any string
                        break#returns to main server code
                elif cinemaStr.lower() == 'back':#if user says 'back' then returns to main server code
                    break
            return "Exitted Cinema Mode Successfully"#returns to main server code


        elif 'ipinfo' in keysFound:
            ipData = self.getIpData(clientAddress)
            return "Your IP is {}, provided by {}.".format(ipData['query'], ipData['isp'])

        elif 'celery' in keysFound:
            return "/w/https://youtu.be/MHWBEK8w_YY"

        else:
            return "Sorry, I don't understand what you are talking about."

    def getServerIP(self): ### Charlie Barry and Dominic Egginton
        ''' returns servers internal and external ip address as dictionary '''
        deviseName = netifaces.gateways()['default'][netifaces.AF_INET][1]
        return {'internal': netifaces.ifaddresses(deviseName)[netifaces.AF_INET][0]['addr'],'external': self.getIpData('')['query']}

    def searchJSON(self, recievedStr): ### Charlie Barry
        '''searches recievedStr for keywords which appear in keywords.json. returns a list of keysFound and a dictionary of additional data'''
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

                        elif key == 'time' and 'time' not in keysFound:                 #if the key is 'time', and a time has not yet been found
                            keysFound.append(key)                                       #add the key to keysFound
                            extraData['time'] = keyword                                 #adds time to extraData

                        else:
                            if key not in keysFound:            #if the key has not yet been found
                                keysFound.append(key)           #add key to keysFound
                        continue

        return keysFound, extraData


def getArgs(): ### Dominic Egginton
    ''' getArgs returns all program arguments '''
    parser = argparse.ArgumentParser(description='Server')
    parser.add_argument('-p', '--port', metavar='Port', default=1143, type=int, help='Server port')
    parser.add_argument('-k', '--key', metavar='Key', default='gbaei395y27ny9', type=str, help='Encryption Key')
    return parser.parse_args()

def main(): ### Dominic Egginton
    ''' main - init server '''
    args = getArgs()
    if args.port == 1143:
        print('** no server port specified using default - 1143')
    server('', args.port, args.key).serverListen() # i have passed empty string for the host ip as it will be filled in later

if __name__ == '__main__':
    main()
