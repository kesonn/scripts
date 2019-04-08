#coding=utf8

import os,sys
import socket

if len(sys.argv)>=2:
    host = sys.argv[1]
    port = sys.argv[2]
else:
    port = 23

print('HOST: %s PORT: %s'%(host,port))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,int(port)))
while True:
    sock.send(input().encode())
    print(sock.recv(1024))

