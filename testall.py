#coding=utf8

import requests
from threading import Thread
import queue
import re

class QueueThread(object):
    def __init__(self,Queue,func):
        self.Queue      = Queue
        self.func       = func

    def run(self):
        while self.Queue.qsize():
            data = self.Queue.get()
            self.func(data)

    def start(self,num_thread=100):
        for i in range(num_thread):
            threads.append(Thread(target = self.run))
        loops = range(len(threads))
        for j in loops:
            #threads[j].setDaemon(True)
            threads[j].start()
        for k in loops:
            threads[k].join()

def log(u,t):
    print(u)
    with open('results.txt','a+') as f:
        f.write(u)
        f.write('\n')
        f.write(t.split('\n')[0])
        f.write('\n')
        f.close()

def get(u):
    try:
        ret = requests.get(u,verify=False)
        return ret.status_code , ret.text
    except Exception as e:
        print(e)
        return 0,''

def rep(h,u,cs=[],ts=''):
    url = h+u
    c,d = get(url)
    if cs and ts:
        if c in cs and ts in d:
            log(url,d)
    elif cs:
        if c in cs:
            log(url,d)
    elif ts:
        if ts in d:
            log(url,d)

def start(host):
    rep(host,'/WEB-INF/web.xml',ts='<web-app>')
    rep(host,'/Web.config',ts='<configuration>')
    rep(host,'/services',ts='(wsdl)')
    rep(host,'/service',ts='(wsdl)')
    rep(host,'/webservices',ts='(wsdl)')

    rep(host,'/manager/html',cs=[401,402])

    rep(host,'/console',cs=[200],ts='logic')
    rep(host,'/axis2',cs=[200],ts='axis2')
    rep(host,'/phpinfo.php',cs=[200],ts='php')
    rep(host,'/upload',cs=[200],ts='file')
    rep(host,'/images',cs=[200],ts='Index of')

    rep(host,'/dwr',cs=[200,301,302])
    rep(host,'/.svn',cs=[200,301,302])
    rep(host,'/.git',cs=[200,301,302])

if __name__=='__main__':
    Queue = queue.Queue(0)
    for host in open('zc.txt','r'):#.readlines():
        try:
            host = host.strip()
            if not host.startswith('http'):
                host = 'http://'+host
            host = '/'.join(host.strip().split('/')[:4])
            Queue.put(host)
        except:pass
    QT = QueueThread(Queue,start)
    QT.start()
