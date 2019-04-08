import socket
import base64
import binascii
import hashlib
HOST = "104.224.169.128"
PORT = 18881
BUFFERSIZE = 1024
hash={}
for i in range(1000,9999):
    md5 = hashlib.md5()
    md5.update(str(i))
    hash.update({md5.hexdigest()[8:24]:str(i)})
def dede(s):
    s=binascii.a2b_hex(s[:-1])
    s=base64.b64decode(s)
    return hash[s]
def ddos():
    TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPClient.connect((HOST,PORT))
    while True:
        recvdate = TCPClient.recv(BUFFERSIZE)
        print(len(recvdate),recvdate)
        if not recvdate:
            break
        if "(y/n)" in recvdate:
            TCPClient.send('y'.encode())
            continue
        if len(recvdate)==49 and 'Welcome' not in recvdate:
            TCPClient.send(b"%s\n"%dede(recvdate).encode())
ddos()
