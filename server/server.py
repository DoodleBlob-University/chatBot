#!/usr/bin/python
''' server.py '''

import socket
import threading
import argparse

class server(object):
    ''' server is a class that handled network connections, pass host ip and host port for init'''
    def __init__(self, hostIP, hostPort):
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostIP, self.hostPort))
        print('** server started on {}:{}'.format(socket.gethostbyname(socket.gethostname()), self.hostPort))

    def serverListen(self):
        ''' serverListen listens to incoming connects from clients and opens a new thread for each connected client '''
        self.socket.listen(15)
        while True:
            try:
                client, clientAddress = self.socket.accept()
                client.settimeout(120)
                threading.Thread(target=self.receiveFromClient,args = (client, clientAddress)).start()
                print('** Client Connected {}'.format(clientAddress))
            except:
                raise Exception('Client connection error')
        
    def receiveFromClient(self, client, clientAddress):
        ''' receiveFromClient handles incoming data from clients '''
        byteSize = 1024
        while True:
            try:
                receivedData = client.recv(byteSize)
                if receivedData and type(receivedData) == bytes:
                    # receivedStr = receivedData.decode()
                    # send to language decoder
                    pass
                else:
                    print('** Client Disconeted {}'.format(clientAddress))
                    client.close()
                    return False
            except:
                client.close()
                return False

def getArgs():
    ''' getArgs returns all program arguments '''
    parser = argparse.ArgumentParser(description='') # Add description 
    parser.add_argument('-p', '--port', metavar='Port', type=int, help='Server port')
    return parser.parse_args()

def drawHeader():
    ''' draws program ui header '''
    print('*** Server Header ***\nWelcome\n\n')

def main():
    ''' main '''
    drawHeader()
    args = getArgs()
    if args.port != 1143:
        print('** no server port specified using defult')
    server('', int(args.port)).serverListen() # i have passed empty string for the host ip as it will be filled in later

if __name__ == '__main__':
    main()
