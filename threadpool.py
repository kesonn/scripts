from __future__ import print_function
import time
import gevent
from gevent.threadpool import ThreadPool
import requests

def get(url):
    print(requests.get(url).status_code)

pool = ThreadPool(40)
start = time.time()
for _ in range(40):
    print(_)
    pool.spawn(get, 'http://www.baidu.com/')
gevent.wait(timeout=3)
delay = time.time() - start
print('Running "time.sleep(1)" 4 times with 3 threads. Should take about 2 seconds: %.3fs' % delay)

pool = ThreadPool(40)
start = time.time()
for _ in range(40):
    print(_)
    pool.spawn(get, 'http://www.baidu.com/')
gevent.wait(timeout=3)
delay = time.time() - start
print('Running "time.sleep(1)" 4 times with 3 threads. Should take about 2 seconds: %.3fs' % delay)
