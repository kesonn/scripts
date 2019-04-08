#coding=utf8

import os,sys
import re
from urllib import parse as urllib
import requests

class Basestore(object):
    def __init__(self):
        self.appurl     = ''
        self.appname    = ''
        self.appver     = ''
        self.appauthor  = ''
        self.appdesc    = ''
        self.appdate    = ''

    def request(self,url):
        headers ={
            'Referer':url,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept':'text/html,application/xhtml'
        }
        self.appurl = url
        text = ''
        try:text = requests.get(url,headers=headers).text
        except Exception as e:print(e))
        return text

    def writecsv(self,data,path='result.csv'):
        with open(path,'a') as f:
            for d in data:
                try:f.write(','.join(d))
                except Exception as e:print(e)
                f.write('\n')
            f.close()

    def test(self):
        for app in self.__dict__:
            try:print(app,getattr(self,app))
            except Exception as e:print(e)

    def start(self,keyword,num=10):
        for n in range(1,num):
            urls = self.search(urllib.quote(keyword),n)
            data = []
            for url in urls:
                print(url)
                self.parse(self.request(url))
                self.test()
                data.append([
                    self.__class__.__name__,
                    self.appname,
                    self.appver,
                    self.appauthor,
                    self.appdate,
                    self.appurl,
                    self.appdesc])
            self.writecsv(data)

class Appstore(Basestore):
    '''苹果应用市场'''
    def parse(self,data):
        self.appname    = ''.join(re.findall(u'<h1 itemprop="name">(.*?)</h1>',data))
        self.appver     = ''.join(re.findall(u'<span itemprop="softwareVersion">(.*?)</span>',data))
        self.appauthor  = ''.join(re.findall(u'<h2>开发者：(.*?)</h2>',data))
        self.appdesc    = ''.join([v.replace('\n','') for v in re.findall(u'<p itemprop="description">(.*?)</p>',data)])
        self.appdate    = ''.join(re.findall(u'<span itemprop="datePublished" content=".*?">(.*?)</span>',data))

class Mmstore(Basestore):
    '''移动MM应用市场'''
    def parse(self,data):
        self.appname    = ''.join(re.findall(u'<span title="(.*?)">',data))
        self.appver     = ''.join(re.findall('<li>版　　本：([\s\S]*?)</li>',data))
        self.appauthor  = ''.join(re.findall(u'title="(.*?)">.*?</a></li><li>',data))
        self.appdesc    = ''.join(re.findall(u'<div class="mj_yyjs font-f-yh">(.*?)</div>',data))
        self.appdate    = ''.join(re.findall('</li><li>更新时间：(.*?)</li><li>',data))
    def search(self,keyword,page=1):
       url = "http://mm.10086.cn/searchapp?st=2&q=%s&p=%s"%(keyword,page)
       return ['http://mm.10086.cn%s'%u for u in re.findall('class="info_name font-f-yh" href="(.*?)"',self.request(url))]

class Vmall(Basestore):
    '''华为应用市场'''
    def parse(self,data):
        self.appname    = ''.join(re.findall(u'<h3 class="app-title">(.*?)</h3>',data))
        self.appauthor  = ''.join([v.strip() for v in re.findall(u'<span>开发者：</span>([\s\S]*?)</li>',data)])
        self.appver     = ''.join([v.strip() for v in re.findall(u'<span>版本：</span>([\s\S]*?)</li>',data)])
        self.appdesc    = ''.join(re.findall(u'<input type="hidden" id="desc" value="(.*?)"/>',data))
        self.appdate    = ''.join([v.strip() for v in re.findall(u'<span>发布时间：</span>([\s\S]*?)</li>',data)])
    def search(self,keyword,page=1):
       url = "http://a.vmall.com/search/searchaction.action?keywords=%s&reqPageNum=%s"%(keyword,page)
       return re.findall('''<a href="javascript:window.location.href='(.*?)'">''',self.request(url))

class Mistore(Basestore):
    '''小米应用市场'''
    def parse(self,data):
        self.appname    = ''.join(re.findall(u'<div class="intro-titles"><p>.*?</p><h3>(.*?)</h3>',data))
        self.appver     = ''.join(re.findall(u'<li class="weight-font">版本号：</li><li>(.*?)</li>',data))
        self.appauthor  = ''.join(re.findall(u'<div class="intro-titles"><p>(.*?)</p><h3>.*?</h3>',data))
        self.appdesc    = ''.join([v.replace('\n','') for v in re.findall(u'<h3>应用介绍</h3><p class="pslide">(.*?)</p>',data)])
        self.appdate    = ''.join(re.findall(u'<li class="weight-font">更新时间：</li><li>(.*?)</li>',data))
    def search(self,keyword,page=1):
       url = "http://app.mi.com/searchAll?keywords=%s&typeall=phone&page=%s"%(keyword,page)
       return ['http://app.mi.com%s'%u for u in re.findall('</a><h5><a href="(.*?)">',self.request(url))]

#Mmstore().test("http://mm.10086.cn/android/info/300010128413.html")
#Appstore().test("https://itunes.apple.com/cn/app/王者荣耀/id989673964")
#Mistore().test("http://app.mi.com/details?id=com.zhinanmao.app")
#Vmall().start("中国移动")

def main(keyword):
    Vmall().start(keyword)
    #for M in Basestore.__subclasses__():
    #    M().start(keyword)

main('中国移动')
