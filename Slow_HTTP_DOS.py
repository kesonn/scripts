#coding=utf8

import socket   #for sockets
import sys  #for exit

host = 'www.google.com'
port = 80

remote_ip = socket.gethostbyname(host)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((remote_ip , port))

message = "GET / HTTP/1.1\r\n\r\n"

sock.sendall(message)

reply = sock.recv(4096)
sock.close()

