#coding=utf8

import socket

def check(host,port,pwd='',timeout=10):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host,int(port)))
            s.send("INFO\r\n")
            recvdata = s.recv(1024)
            print(recvdata)
            if 'redis_version' in recvdata:
                return True
            elif "Authentication" in result:
                s.send("AUTH %s\r\n"%(pwd))
                result = s.recv(1024)
                if '+OK' in result:
                   return True
        except Exception as e:
            print(e)
            return False
        finally:
            s.close()

for ip in open('6379.txt').readlines():
    if check(ip.strip(),6379):
        r=open('rr.txt','a+')
        r.write(ip+'\n')
        r.close()
