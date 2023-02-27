# -*- coding: utf-8 -*-
"""

UDP CLIENT SOCKET

@author: bighi
"""

import socket as sk
import sys, time, os

MESS_OK = 'Ok'

HOST = 'localhost'
PORT = 10000
server_address = (HOST,PORT)

#Create client socket UDP
try:
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    print('Client socket initialized')
    sock.setblocking(0)
    sock.settimeout(10)
except sk.error:
    print('Client socket failed')
    sys.exit()

server_address = (HOST, PORT)


def Client_List():
    data, server = sock.recvfrom(1024)
    if data.decode('utf8') == 'List function':
        try:
            file_list, server = sock.recvfrom(4096)
            sock.sendto(MESS_OK.encode('utf8'), server_address)
            print('\n%s' % file_list.decode('utf8'))
        except sock.TimeoutError:
            sock.sendto('Error'.encode('utf8'), server_address)
            print('List NOT sent correctly')
    else:
        sock.sendto('Error'.encode('utf8'), server_address)
        print('Error, not List')


def Client_Get():
    #Get number of packets to be received
    data, server = sock.recvfrom(1024)
    num_pack = int(data.decode('utf8'))
    #Check if the server have the file
    if num_pack == -1:
        print('\nError, file not found')
    else:
        File = open(cm[1].decode('utf8'), 'wb')
        sock.sendto(MESS_OK.encode('utf8'), server_address)
        
        while num_pack != 0:
            try:
                pack, server = sock.recvfrom(4096)
                File.write(pack)
                num_pack = num_pack-1
                sock.sendto(MESS_OK.encode('utf8'), server_address)
            except sock.TimeoutError:
                sock.sendto('Resend'.encode('utf8'), server_address)
        
        File.close()
        if num_pack == 0:
            print('\nFile %s received correctly' % cm[1].decode('utf8'))
        else:
            print('\nFile %s NOT received correctly' % cm[1].decode('utf8'))


def Client_Put():
    #Check if file is present and count number of packets to send
    if os.path.isfile(cm[1].decode('utf8')):
        size = os.stat(cm[1]).st_size
        num_pack = int(size / 4096) + 1
        sock.sendto(str(num_pack).encode('utf8'), server_address)
        
        File = open(cm[1].decode('utf8'), 'rb')
        while num_pack != 0:
            check, client_address = sock.recvfrom(1024)
            if check.decode('utf8') == 'Ok':
                read = File.read(4096)
                sock.sendto(read, server_address)
                num_pack = num_pack-1
            else:
                #resend packet lost
                sock.sendto(read, server_address)
        File.close()
        last, client_address = sock.recvfrom(1024)
        if num_pack == 0:
            print('\nFile %s sent correctly' % cm[1].decode('utf8'))
        else:
            print('File %s NOT sent correctly' % cm[1].decode('utf8'))
    else:
        #If file not exist sent -1
        sock.sendto(str(-1).encode('utf8'), server_address)
        print('\nError, file not found')


while True:
    
    time.sleep(1)
    message = input(
        '\nChoose an option\r\n1.[list] Files available on the server\r\n2.[get][file_name] Download a file from the server\r\n3.[put][file_name] Upload a file to the server\r\n4.[close] Close client socket\r\n5.[exit] Close client and server socket\r\n')
    command = message.encode('utf8')
    
    try:
        sock.sendto(command, server_address)
    except ConnectionResetError:
        print('\nPort %s not found' % server_address)
        sys.exit()
    
    cm = command.split()

    if cm[0].decode('utf8') == 'list': 
        try:
            Client_List()
        except Exception as info:
            print(info)

    elif cm[0].decode('utf8') == 'get':
        try:
            cm[1]
            Client_Get()
        except Exception as info:
            print(info)
            
    elif cm[0].decode('utf8') == 'put':
        try:
            cm[1]
            Client_Put()
        except Exception as info:
            print(info)
            
    elif cm[0].decode('utf8') == 'close':
        print('\nclosing client socket')
        break
    
    elif cm[0].decode('utf8') == 'exit':
        print('\nclosing client and server socket')
        break
    
    else:
        print('\nError, command non found')
    
time.sleep(2)
sock.close()