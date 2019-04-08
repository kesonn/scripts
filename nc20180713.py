import socket
from threading import Thread
import logging  # 引入logging模块
import os.path
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fn = logging.FileHandler('logs.log', mode='w')
fn.setLevel(logging.DEBUG)
fn.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(fn)

class SsrfTunnel(Thread):
    def __init__(self,client,addr):
        Thread.__init__(self)
        self.client = client
        self.addr = addr

    def run(self):
        buff = self.client.recv(10240)
        req = buff
        self.doproxy(req)

    def doproxy(self,req):
        try:
            self.save(req)
            self.client.sendall('HTTP/1.1 200 OK\r\n\r\n\r\n\r\n\r\n\r\n'.encode())
        except Exception as e:
            logger.error(str(e))
        finally:
            self.client.close()

    def save(self,req):
        ip = str(self.addr[0])
        logger.info(ip)
        with open('./data/'+ip,'a') as f:
            f.write(req.decode())
        logger.info(str(req))

class SockProxy(object):
    def __init__(self,host='0.0.0.0',port=53,listen=10):
        self.host = host
        self.port = port
        self.listen = listen
        self.clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientsock.bind((self.host,self.port))

    def start(self):
        self.clientsock.listen(self.listen)
        print('Start Proxy Listen - %s:%s'%(self.host,self.port))
        while True:
            client,addr = self.clientsock.accept()
            SsrfTunnel(client,addr).start()

import sys
try:
    port = int(sys.argv[1])
except:
    port = 53
c = SockProxy('0.0.0.0',port)
c.start()
