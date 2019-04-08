#coding=utf8
import requests
import time
import re
import threading

class Md5pj(object):
    _NOT_IN_RESULT = (
        u'很抱歉，您输入的密文没有记录',
        u'未查到,已加入本站后台解密',
        u'已查到,这是一条付费记录',
    )
    def __init__(self):
        self._session = requests.Session()
        self._result = {}
    def test(self,hash,fall=True):
        __=[threading.Thread(target=self._start,args=(f2,hash,fall,)) for f2 in [
            f1 for f1 in dir(self) if not f1.startswith(('test','_'))]]
        [_.start() for _ in __]
        [_.join() for _ in __]
        return self._result
    def _start(self,fun,hash,fall):
        try:
            res = self._h2m(getattr(self,fun)(hash))
            print(fun[:20].ljust(20),' ...... ',res)
            if res and not res.startswith(self._NOT_IN_RESULT):
               self._result[fun] = res
        except Exception as e:
            print(e)
    def _h2m(self,s):
        if s and type(s)==str:
           s = s.replace('&quot;','"').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>')
           s = s.replace('&nbsp;','[SPACE]')#空格
           return s
    def hashtoolkasdasdasdasdasdasdasdsdasdit_com(self,hash):
        url = "http://hashtoolkit.com/reverse-hash?hash={0}".format(hash)
        req = self._session.get(url,headers={"Referer":"http://hashtoolkit.com/"}).text
        res = re.findall(r"<span title=\"decrypted md5 hash\">(.*)</span>",req)
        if len(res):return res[0]
    def cracker_blackbap_org(self,hash):
        url = "http://cracker.blackbap.org/?do=search"
        data = {'isajax':'1','md5':hash}
        req = self._session.post(url,data=data,headers={"Referer":"http://cracker.blackbap.org/"}).text
        res = re.findall(r"<strong>(.*)</strong></p>",req)
        if len(res)>1:return res[1]
    def md5_syue_com(self,hash):
        url = "http://md5.syue.com/ShowMD5Info.asp?md5_str={0}&GetType=ShowInfo&no-cache={1}".format(hash,time.time())
        req = self._session.get(url,headers={"Referer":"http://md5.syue.com/"}).text
        res = re.findall(r"line-height:25px\">(.*)</span><br>",req)
        if len(res):return res[0].strip()
    def www_cmd5_com(self,hash):
        url = "http://www.cmd5.com/"
        req = self._session.get(url).text
        data = dict(re.findall("<input.*name=\"(.*?)\".*value=\"(.*?)\".*/>",req))
        data['ctl00$ContentPlaceHolder1$TextBoxInput'] = hash
        req = self._session.post(url=url,data=data,headers={'Referer':'http://www.cmd5.com/'}).text
        res = re.findall(r"id=\"ctl00_ContentPlaceHolder1_LabelAnswer\">(.*?)<",req)
        if len(res):return res[0]
    def www_somd5_com(self,hash):
        url ="http://www.somd5.com/somd5-md5-js.html"
        req = self._session.get(url).text
        key = re.findall(r"isajax=(.*)&\"",req)[0]
        data={'isajax':key,'md5':hash}
        url = "http://www.somd5.com/somd5-index-md5.html"
        req = self._session.post(url=url,data=data,headers={'Referer':'http://www.somd5.com/'}).text
        res = re.findall(r"<h1 style=\"display:inline;\">(.*)</h1>",req)
        if len(res):return res[0]
    def www_xmd5_com(self,hash):
        url = "http://www.xmd5.com/"
        req = self._session.get(url).text
        data = dict(re.findall("<input.*name=\"(.*?)\".*value=\"(.*?)\".*/>",req))
        data['hash'] = hash
        req = self._session.post(url=url,data=data,headers={'Referer':'http://www.xmd5.com/'}).text
        res = re.findall(r"id=\"ctl00_ContentPlaceHolder1_LabelAnswer\">(.*?)<",req)
        if len(res):return res[0]

if __name__=='__main__':
    import json
    pj=Md5pj()
    while True:
        v=pj.test(input('>'))
        print(json.dumps(v))
