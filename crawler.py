#!/usr/bin/env python
#-*-encoding:UTF-8-*-

import re
try:
    import urlparse
    import Queue as queue
except ImportError:
    from urllib.parse import urlparse
    import queue

import requests
import gevent
from gevent.threadpool import ThreadPool
from bs4 import BeautifulSoup


class PluginManage(object):
    plugins = {}
    def __init__(self,**kw):
        self.kwargs = kw

    def __call__(self,f):
        self.plugins[f]=self.kwargs

    @classmethod
    def test(cls,f):
        def F(self,req):
            f(self,req)
            for k,v in cls.plugins.items():
                k(req).request(**v)
        return F


#@PluginManage()
class XssPlugin(object):
    payload = ["11'\"11","<2222>"]
    def __init__(self,req):
        self.req = req

    def request(self,**kwargs):
        for xss in self.payload:
            for k,v in self.req.query.items():
                self.req.query[k]=xss
                if xss in self.req.reload().text:
                   self.handler(self.req,xss)
                   return

    def handler(self,req,xss):
        print("XSS %s[payload]%s"%req.url,xss)

class Request(object):
    req = requests.Session()
    def __init__(self,url,data={},headers={},method='GET',version='HTTP/1.1'):
        self.url    = url
        self.data   = data
        self.headers= {
            "User-Agent":"Mozilla/5.0 (compatible; Baiduspider/2.0;)",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Connection":"keep-alive",
            "Referer":self.url,}
        self.headers.update(headers)
        self.method = method.strip()
        self.version= version.strip()
        parser      = urlparse.urlsplit(self.url)
        self.scheme = parser.scheme
        self.netloc = parser.netloc
        self.path   = parser.path
        self.query  = {}
        query       = parser.query
        if query:
           self.query = dict([q.split('=') for q in query.split('&') if '=' in q])
        if data and method=='GET':
            self.method = 'POST'

    def reload(self):
        self.url = "%s://%s%s"%(
            self.scheme,
            self.netloc,
            '%s?%s'%(self.path,
                '&'.join(['%s=%s'%(k,v) for k,v in self.query.items()]) \
                if self.query else self.path))
        return self.request()

    def request(self,timeout=10,proxy={}):
        req=getattr(self.req,self.method.lower())
        return req(self.url,data=self.data,headers=self.headers,timeout=timeout)

    def __eq__(self,req):
        return self.url==req.url and self.data==req.data

    def __str__(self):
        s=[]
        s.append("%s %s %s"%(
            self.method.upper(),
            '%s?%s'%(self.path,
                '&'.join(['%s=%s'%(k,v) for k,v in self.query.items()])) \
                if self.query else self.path,
            self.version))
        s.append('Host: %s'%(self.netloc))
        for k,v in self.headers.items():
            s.append("%s: %s"%(k,v))
        if self.data:
            s.append('\n\n')
            s.append("&".join(["%s=%s"%(k,v) for k,v in self.data.items()]))
        s.append('\n\n')
        return '\r\n'.join(s)

class Crawler(object):
    def __init__(self,baseurl,threads=1,timeout=10,sleep=5):
        self.baseurl = baseurl
        self.threads = threads
        self.timeout = timeout
        self.sleep   = sleep
        self.pool    = ThreadPool(self.threads)
        self.Queue   = queue.Queue()
        self.block   = set()
        self.flag    = 0
        self.isstop  = False

    @PluginManage.test
    def addreq(self,req):
        print("GET %s"%req.url)
        print('\r')
        self.Queue.put(req)

    def urljoin(self,url):
        block = ('http://','https://','file://','javascript:','#','mailto:')
        if url:
           if url.startswith(self.baseurl):
              return url
           elif url.startswith('/') and not url.startswith('//'):
              return '%s%s'%(self.baseurl,url)
           elif not url.lower().strip().startswith(block):
              return '%s/%s'%(self.baseurl,url)

    def isback(self,req):
        if req not in self.block:
           self.block.add(req)
           self.addreq(req)

    def run(self,req):
        try:
            response = req.request()
        except requests.ConnectionError:
            gevent.sleep(self.sleep)
        content_type = response.headers.get('content-type')
        if "html" in content_type:
            self.htmlparse(response.text)
        elif "text" in content_type \
        or "json" in content_type \
        or "javascript" in content_type:
            self.textparse(response.text)
        else:
            pass

    def start(self):
        self.run(Request(self.baseurl))
        while True and self.flag<=60*5: #5分钟后还没有任务加进来就当爬完了
            try:
                req = self.Queue.get(block=False)
            except queue.Empty:
                gevent.sleep(1)
                print(self.flag)
                self.flag += 1
            else:
                self.pool.spawn(self.run,req)
        gevent.wait(timeout=self.timeout)
        self.isstop  = True

    def textparse(self,response):
        urls = []
        re_url = ("(http[s]?://(?:[-a-zA-Z0-9_]+\.)+[a-zA-Z]+(?::\d+)?(?:/[-a-zA-Z0-9_%./]+)*\??[-a-zA-Z0-9_&%=.]*)")
        urls += re.findall(re_url,response)
        for url in urls:
            url = self.urljoin(url)
            if url:
                req = Request(url)
                self.isback(req)

    def htmlparse(self,response):
        href_tags = {"a", "link", "area"}
        src_tags = {"form", "script", "img", "iframe", "frame", "embed", "source", "track"}
        param_names = {"movie", "href", "link", "src", "url", "uri"}
        for tag in BeautifulSoup(response,"html.parser").findAll():
            url = None
            data = {}
            name = tag.name.lower()
            if name in href_tags:
                url = tag.get("href", None)
            elif name in src_tags:
                url = tag.get("src", None)
            elif name == "param":
                name = tag.get("name", "").lower().strip()
                if name in param_names:
                    url = tag.get("value", None)
            elif name == "object":
                url = tag.get("data", None)
            elif name == "applet":
                url = tag.get("code", None)
            elif name == "meta":
                name = tag.get("name", "").lower().strip()
                if name == "http-equiv":
                    content = tag.get("content", "")
                    p = content.find(";")
                    if p >= 0:
                        url = content[ p + 1 : ]
            elif name == "base":
                url = tag.get("href", None)
            #for post fomm
            if name == "form":
                action = tag.get('action','')
                method = tag.get('method','GET').upper()
                data = {}
                #Process <input type="test" name="...
                for m in tag.findAll('input',{'name' : True,'type' : 'text'}):
                    value = m.get('value','')
                    data[m['name']] = value
                #Process <input type="password" name="...
                for m in tag.findAll('input',{'name' : True,'type' : 'password'}):
                    value = m.get('value','')
                    data[m['name']] = value
                #Process <input type="submit" name="...
                for m in tag.findAll('input',{'name' : True,'type' : 'submit'}):
                    value = m.get('value','')
                    data[m['name']] = value
                #Process <input type="hidden" name="...
                for m in tag.findAll('input',{'name' : True,'type' : 'hidden'}):
                    value = m.get('value','')
                    data[m['name']] = value
                #Process <input type="checkbox" name="...
                for m in tag.findAll('input',{'name' : True,'type' : 'checkbox'}):
                    value = m.get('value','')
                    data[m['name']] = value
                #Process <input type="radio" name="...
                listRadio = []
                for m in tag.findAll('input',{'name' : True,'type' : 'radio'}):
                    if not m['name'] in listRadio:
                        listRadio.append(m['name'])
                        value = m.get('value','')
                        data[m['name']] = value
                #Process <textarea name="...
                for m in tag.findAll('textarea',{'name' : True}):
                    data[m['name']] = m.contents[0]
                #Process <select name="...
                for m in tag.findAll('select',{'name' : True}):
                    if len(m.findAll('option',value=True))>0:
                        name = m['name']
                        data[name] = m.findAll('option',value=True)[0]['value']

            url = self.urljoin(url)
            if url:
                req = Request(url,data)
                self.isback(req)

x=Crawler('http://www.heungkong.com')
x.start()
x.run(Request('http://www.szweb.cn/'))
