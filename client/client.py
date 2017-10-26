#!/usr/bin/python
''' client.py '''

import socket
import threading
import argparse

def getArgs():
    ''' getArgs returns all program arguments '''
    parser = argparse.ArgumentParser(description='') # Add description
    parser.add_argument('-p', '--port', metavar='Port', type=int, default=1143, help='Server port')
    parser.add_argument('-a', '--address', metavar='Address', required=True, type=str, help='Server address')
    return parser.parse_args()

def drawHeader():
    ''' draws program ui header '''
    print('*** Client Header ***\nWelcome\n\n')

def main():
    ''' main '''
    args = getArgs()
    drawHeader()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((args.address, args.port))
    while True:
        messageData = input('>> ')
        if messageData.lower() == 'exit':
            exit()
        elif messageData == '':
            continue
        else:
            messageData = messageData.encode()
            sock.sendall(messageData)
            receivedData = sock.recv(1024)
            print(receivedData.decode())

if __name__ == '__main__':
    main()
