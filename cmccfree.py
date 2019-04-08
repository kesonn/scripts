#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#codeby     道长且阻
#email      ydhcui@suliu.net/QQ664284092
#website    http://www.suliu.net
#
#20160314 create cmccfree object
#20160415 create chanreip function
#
##just for win

__doc__=u"""#直接运行，按提示输入所需的配置
#CTRL+Q 切换客户端
#CTRL+A 增加客户端
#CTRL+Z 断开当前客户端
"""

try:#py3
    from urllib import parse,request
    from http import cookiejar
except ImportError:#py2
    import urllib as parse
    import urllib2 as request
    import cookielib as cookiejar

import sys
import random
import time
import json
import threading
import socket
import platform

ISWIN = False
if platform.system() =="Windows":
    ISWIN = True

class Utils(object):
    lock = threading.Lock()
    def __init__(self):
        self.cookieJar = cookiejar.MozillaCookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookieJar))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            #'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',}
    def request(self,url,data=None):
        #self.outbox('RequestURL> %s'%url)
        self.headers.update({'referer':url})
        if data:
            data = parse.urlencode(data).encode('utf-8')
            rr = request.Request(url,data,headers = self.headers)
        else:
            rr = request.Request(url,headers = self.headers)
        for t in range(60):#断线重连 每次超时等待递增1分钟最多60次
            try:
                req = self.opener.open(rr)
                break
            except Exception as e:
                self.outbox(e)
                time.sleep(t*60)
        return req
    @classmethod
    def outbox(self,*ss):
        self.lock.acquire()
        sys.stdout.write(str(ss))
        sys.stdout.write('\n')
        sys.stdout.flush()
        self.lock.release()
    @classmethod
    def inbox(self,ss,df=None):
        """
        #ss --- 输入时显示的提示信息
        #df --- 默认值
        """
        self.lock.acquire()
        sys.stdout.write(ss+u'[%s]'%str(df))
        sys.stdout.flush()
        ret = sys.stdin.readline()[:-1]
        if ret:
            self.lock.release()
            return ret
        else:
            sys.stdout.write(str(df))
            sys.stdout.write('\n')
            sys.stdout.flush()
            self.lock.release()
            return df
    @classmethod
    def getlocalip(self):
        for i in range(8):
            ip = socket.gethostbyname_ex(socket.gethostname())[2][i]
            if ip.startswith("10."):
                return ip

class CmccFree(object):
    def __init__(self):
        self.info = {}
        self.request = Utils().request
    def parse(self,req):
        res = req.read()
        try:res = res.decode('utf-8')
        except:res = res
        try:
            res = json.loads(res)
            retcode,msg = res['resultCode'],res['resultDesc']
            Utils.outbox(retcode,msg)
            return retcode
        except Exception as e:
            Utils.outbox(e)
            return res
    def getinit(self):
        url = "http://%s/wlan-portal-web/portal?wlanacname=%s&wlanuserip=%s&wlanacssid=%s&spe=%s" \
            %(self.info['host'],
              self.info['wlanacname'],
              self.info['wlanuserip'],
              self.info['wlanacssid'],
              self.info['spe'])
        self.request(url)
    def sendsms(self):
        url = "http://%s/wlan-portal-web/service/portalAccountService.getAccount.rest?t=%s" \
            %(self.info['host'],random.random())
        data = {"paramMap.phone"        :self.info['USER'],
                "paramMap.wlanSsid"     :self.info['wlanacssid']}
        self.parse(self.request(url,data))
    def login(self):
        url = "http://%s/wlan-portal-web/service/portalAccountService.loginByPortal.rest?t=%s" \
            %(self.info['host'],random.random())
        data = {"paramMap.USER"         :self.info['USER'],
                "paramMap.PWD"          :self.info['PWD'],
                "paramMap.wlanacname"   :self.info['wlanacname'],
                "paramMap.wlanuserip"   :self.info['wlanuserip'],
                "paramMap.actiontype"   :'LOGIN',
                "paramMap.wlanacssid"   :self.info['wlanacssid'],
                "paramMap.forceflag"    :1,
                "paramMap.useragent"    :self.info['useragent'],
                "paramMap.spe"          :self.info['spe']}
        return self.parse(self.request(url,data))

def login(obj,AUTO_LOGIN=True,selfip=None):
    obj.info['host']       = "221.176.66.85:81"
    obj.info['wlanacname'] = "4143.0020.200.00"
    obj.info['wlanacssid'] = "CMCC-FREE"
    obj.info['spe']        = "ggmb"
    obj.info['useragent']  = "Mozilla&#47;5.0 &#40;Windows NT 6.1; WOW64; rv:34.0&#41; Gecko&#47;20100101 Firefox&#47;34.0"
    '''
    req = obj.request("http://www.baidu.com")
    if req.get('url'):
        res = obj.parse(obj.request(req.get('url')))
        regex = "<iframe id=\"loginIframe\" src=\"(.*?)\""
        url = re.findall(regex,res)
            if len(url):
                for value in url[0].split('?')[1].split('&'):
                    k,v = value.split('=')
                    obj.info[k] = v
    '''
    user = random.randint(13800000000,13800138000)
    localip = selfip if selfip else Utils.getlocalip()
    Utils.outbox(localip)
    if AUTO_LOGIN:
        obj.info['wlanuserip'] = selfip
        obj.getinit()
        obj.info['USER'] = user
        obj.sendsms()
        obj.info['PWD'] = '    '
    else:
        obj.info['wlanuserip'] = Utils.inbox(u'请输入你的IP地址',df=localip)
        obj.getinit()
        obj.info['USER'] = Utils.inbox(u"请输入手机号码",df=user)
        obj.sendsms()
        obj.info['PWD'] = Utils.inbox(u"请输入收到的短信验证码",df='    ')
    while True:
        if obj.login() not in ['0','122']:
            break
        time.sleep(50*60) #50分钟 * 60秒

def changeip(obj):
    import msvcrt   #just for win
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            #print(key)
            if key == b'\x11':  #ctrl+q
                userip = Utils.inbox(u'请输入你的IP地址', df = obj.info['wlanuserip'])
                if userip:
                    obj.info['wlanuserip'] = userip
                    obj.login()
            if key == b'\x01':  #ctrl+a
                main(False)
            if key == b'\x1a':  #ctrl+z
               Utils.outbox(u'退出。%s'%obj.info['wlanuserip'])
               sys.exit(0)

def main(AUTO_LOGIN=True):
    CF = CmccFree()
    threading.Thread(target=login,args=(CF,AUTO_LOGIN,)).start()
    if ISWIN:
        threading.Thread(target=changeip,args=(CF,)).start()

if __name__=='__main__':
    print(__doc__)
    main(0)


