# -*- coding: utf-8 -*-
"""

UDP SERVER SOCKET

@author: bighi
"""

import socket as sk
import sys, time, os

MESS_OK = 'Ok'
#MESS_CK = 'Check'

HOST = 'localhost'
PORT = 10000
ADDR = (HOST,PORT)

#Create server socket UDP and bind it to the port
try:
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    print('Server socket initialized: ')
    print ('starting up on %s port %s' % ADDR)
    sock.bind(ADDR)
except sk.error:
    print('Server socket failed')
    sys.exit()


def Server_List():
    where = 'List function'
    print(where)
    sock.sendto(where.encode('utf8'), address)
    lists = os.listdir(os.getcwd())
    sock.sendto(str(lists).encode('utf8'), address)
    check, client_address = sock.recvfrom(1024)
    if check.decode('utf8') == 'Ok':
        print('List sent correctly')
    else:
        print('List NOT sent correctly')


def Server_Get(file_name):
    print('Get function')
    #Check if file is present and count number of packets to send
    if os.path.isfile(file_name):    
        size = os.stat(file_name).st_size
        num_pack = int(size / 4096) + 1
        sock.sendto(str(num_pack).encode('utf8'), address)
        print('File size: %s bytes - %s packets' % (str(size),str(num_pack)) )
        
        File = open(file_name,'rb')
        while num_pack != 0:
            check, client_address = sock.recvfrom(1024)
            if check.decode('utf8') == 'Ok':
                read = File.read(4096)
                sock.sendto(read, address)
                num_pack = num_pack-1
            else:
                #resend packet lost
                sock.sendto(read, address)      
        File.close()
        last, client_address = sock.recvfrom(1024)
        if num_pack == 0:
            print('File %s sent correctly' % file_name)
        else:
            print('File %s NOT sent correctly' % file_name)
    else:
        #If file not exist sent -1
        sock.sendto(str(-1).encode('utf8'), address)
        print('Error, file not found')


def Server_Put(file_name):
    print('Put function')
    #Get number of packets to be received
    data, address = sock.recvfrom(1024)
    pack = data.decode('utf8')
    num_pack = int(pack)
    #Check if the client have the file
    if num_pack == -1:
        print('Error, file not found')
    else:
        File = open(file_name, 'wb')
        sock.sendto(MESS_OK.encode('utf8'), address)
        
        while num_pack != 0:
            try:
                data, address = sock.recvfrom(4096)
                File.write(data)
                num_pack = num_pack - 1
                sock.sendto(MESS_OK.encode('utf8'), address)
            except sock.TimeoutError:
                sock.sendto('Resend'.encode('utf8'), address)   
        
        File.close()
        print('File size: %s bytes - %s packets' % (str(os.stat(file_name).st_size),str(pack)) )
        if num_pack == 0:
            print('File %s received correctly' % file_name)
        else:
            print('File %s NOT received correctly' % file_name)


time.sleep(1)
while True:
    
    print('\n\r waiting client...')
    #waiting to receive name command from the client
    data, address = sock.recvfrom(4096)
    command = data.decode('utf8')
    cm = command.split()     #in case, second argument is the file name

    if cm[0] == 'list':
        Server_List()
        
    elif cm[0] == 'get':
        try:
           Server_Get(cm[1]) 
        except Exception as info:
            print(info)
        
    elif cm[0] == 'put':
        try:
            Server_Put(cm[1])
        except Exception as info:
            print(info)
        
    elif cm[0] == 'close':
        print('closing client socket')
        
    elif cm[0] == 'exit':
        print('closing server socket')
        break
    
    else:
        print('Error, command non found')
        
time.sleep(2)
sock.close()