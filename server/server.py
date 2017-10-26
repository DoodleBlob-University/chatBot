#!/usr/bin/python
''' server.py '''

import socket
import threading
import argparse

class server(object):
    def __init__(self, hostIP, hostPort):
        self.hostIP = hostIP
        self.hostPort = hostPort
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostIP, self.hostPort))

    def serverListen(self):
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

def main():
    ''' main '''
    # Add header and UI
    args = getArgs()
    if args.port:
        server('', args.port).serverListen()

if __name__ == '__main__':
    main()
