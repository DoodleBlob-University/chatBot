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
    print(args.port)

if __name__ == '__main__':
    main()
