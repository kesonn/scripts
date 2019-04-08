import asyncio
import time
import requests
import socket

def ddos(addr):
    TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPClient.connect(addr) #连接服务器
    TCPClient.send('0x00'.encode())

#@asyncio.coroutine
def main():
    tasks = []
    result = []
    for site in sites:
        #tasks.append(loop.run_in_executor(None, requests.head, site))
        tasks.append(loop.run_in_executor(None, ddos, (site,23151)))
    for task in tasks:
        #print(time.time())
        r = yield from task
        result.append(r)
    for s in result:
        print(r)


now =time.time()
lenth = 10
sites = ['127.0.0.1']*lenth
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print(time.time()-now)

class QAsyncThread(QThread):
    """
    使用异步方式,只支持py3.4以上
    还没写完，异步理论上来说会比多线程更快，
    但是实际测试中会因为并发太高而导致网站中断连接
    """
    signal = pyqtSignal(bool)
    def __init__(self):
        QThread.__init__(self)
        self.Queue   = []
        self.threads = 10
        self.timeout = 10
        self.event   = None
        self.FLAG    = True   #stop
        self.STAT    = False  #pause

    def stop(self):
        self.FLAG = False
        self.STAT = False

    def pause(self):
        self.STAT = not self.STAT

    def setup(self,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)

    def run(self):
        while self.FLAG:
            __ = []
            if self.STAT:
                self.sleep(1)
                continue
            for _ in range(self.threads):
                task = []
                result = []
                try:
                    data = next(self.Queue)
                except StopIteration:
                    self.FLAG = False
                    break
                tasks.append(loop.run_in_executor(None, self.__get_status, data))
                for task in tasks:
                    r = yield from task
                    result.append(r)
                for req in result:
                    self.signal.emit(req,data)

    def __get_status(self,url):
        pass