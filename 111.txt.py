#coding=utf8
import requests
import re
url = "http://www.it404.com/project/10_it404.php"
headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'__cfduid=df07bdf384e7524b0351b698be24d1ac41491632767; cf_clearance=65a2224a4f6b188624531e64ad65a832e3e242b3-1491656428-1800',
    'Host':'www.it404.com',
    'Upgrade-Insecure-Requests':1,
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
req = requests.session()
state = []
enc=''
with open('aad.txt','a+') as f:
    for i in range(99):
        data={'bingo':enc,'submit':'1'}
        res = req.post(url,data,headers=headers).text
        f.write(res)
        enc = re.findall('\d{9}',res)[1]
        print(enc)
        state.append(int(enc))
    index = len(state)
    mod = (state[index-3]+state[index-31])%2147483647
    print(mod)
    data={'bingo':mod,'submit':'1'}
    res = req.post(url,data,headers=headers).text
    f.write(res)
    print(res)




