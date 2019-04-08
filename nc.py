import socket
from threading import Thread

class Tunnel(Thread):
    def __init__(self,client,addr):
        Thread.__init__(self)
        self.client = client
        self.addr = addr

    def run(self):
        buff = self.client.recv(10240)
        req = buff.decode()
        self.doproxy(req)

    def doproxy(self,req):
        try:
            self.save(req)
            self.client.sendall('HTTP/1.1 200 OK\r\n\r\n'.encode())
        except Exception as e:
            print(e)
        finally:
            self.client.close()

    def save(self,req):
        with open(str(self.addr[0]),'a') as f:
            f.write(req)
        print(req)

class SockProxy(object):
    def __init__(self,host='0.0.0.0',port=53,listen=10):
        self.host = host
        self.port = port
        self.listen = listen
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host,self.port))

    def start(self):
        self.sock.listen(self.listen)
        print('Start Proxy Listen - %s:%s'%(self.host,self.port))
        while True:
            client,addr = self.sock.accept()
            Tunnel(client,addr).start()

c = SockProxy()
c.start()