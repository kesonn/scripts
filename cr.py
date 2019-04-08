#coding=utf8
from threading import Thread
import urlparse
import time

class recv(object):
    pass

class Handler(object):
    def __init__(self,Queue=None,backlist=[]):
        self.Queue = Queue
        self.scheme = ['http','https']
    def handler(self,url):
        self.url = urlparse.urlparse(url)
        if self.url.scheme in self.scheme:
            text = requests.get(url).text


class QueueThread(object):
    """队列模式的多线程，会一直等待队列中增加元素。
    任务完成后不会自动退出，直到手动调用STOP退出"""
    def __init__(self,Queue,func):
        self.Queue      = Queue
        self.func       = func(self.Queue)
        self.threads    = []
        self.FLAG       = True
        self.STAT       = False

    def run(self):
        while self.FLAG:
            if self.STAT:
                time.sleep(0.1)
                continue
            data = self.Queue.get()
            self.func.handler(data)

    def start(self,num_thread=10):
        for i in range(num_thread):
            self.threads.append(Thread(target = self.run))
        loops = range(len(self.threads))
        for j in loops:
            #self.threads[j].setDaemon(True)
            self.threads[j].start()
        for k in loops:
            self.threads[k].join()

    def stop(self):
        self.FLAG = False

    def pause(self):
        self.STAT = not self.STAT

    def clear(self):
        self.Queue.clear()

    def isdone(self):
        return True and self.Queue.qsize()