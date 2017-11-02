#!/usr/bin/python
''' client.py '''

import socket
import threading
import argparse
import os
import subprocess
from colorama import Fore, Style

def getArgs():
    ''' getArgs returns all program arguments '''
    parser = argparse.ArgumentParser(description='') # Add description
    parser.add_argument('-p', '--port', metavar='Port', type=int, default=1143, help='Server port')
    parser.add_argument('-a', '--address', metavar='Address', required=True, type=str, help='Server address')
    return parser.parse_args()

def clear():
    ''' clears bash terminal display '''
    if os.name in ('nt','dos'):
        subprocess.call("cls")
    elif os.name in ('linux','osx','posix'):
        subprocess.call("clear")
    else:
        print("\n"*120)

def drawHeader():
    ''' draws program ui header '''
    clear()
    print(Fore.GREEN + " _____ _           _    ______       _   \n" + Fore.BLUE + "/  __ \ |         | |   | ___ \     | |  \n" + Fore.MAGENTA + "| /  \/ |__   __ _| |_  | |_/ / ___ | |_ \n" + Fore.RED + "| |   | '_ \ / _` | __| | ___ \/ _ \| __|\n" + Fore.YELLOW + "| \__/\ | | | (_| | |_  | |_/ / (_) | |_ \n" + Fore.CYAN + " \____/_| |_|\__,_|\__| \____/ \___/ \__|\n\n" + Style.RESET_ALL + " "*17 + 'Welcome!' )


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
