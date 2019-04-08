
from urllib import parse,request
from http import cookiejar
import random
import re
import json
import time
import os
import sys
import queue
import socket


__all__ = [
    'request',
    'getqrcode',
    'login',
    'webwxinit',
    'webwxgetcontact',
    'webwxbatchgetcontact',
    'webwxstatusnotify',
    'webwxsendmsg',
    'webwxlogout',
    'synccheck',
    'webwxsync',
]

def log(*s):print(s)
def RT():return int(time.time())
def CT():return int(time.time()*1000)
def DeviceID():return ''.join(['e',repr(random.random())[2:17]])
def MsgID():return ''.join([CT(),repr(random.random())[2:6]])

class Wechat(object):

    def _createRequest(self,**kwargs):
        data = {"BaseRequest":{
                    "Uin":self.logininfo['wxuin'],
                    "Sid":self.logininfo['wxsid'],
                    "Skey":self.logininfo['skey'],
                    "DeviceID":DeviceID(),}}
        data.update(**kwargs)
        return data

    def _baseResponse(self,res):
        try:
            result = json.loads(res)
            keys = result.keys()
            if 'BaseResponse' in keys:
                BaseResponse = result['BaseResponse']
                log(BaseResponse)
            return result
        except Exception as e:
            #logger.error(e)
            return res

    def _createMsg(self,ToUserName,Content,Type=1,**kv):
        data = {"Type":Type,
                "Content":Content,
                "FromUserName":self.User['UserName'],
                "ToUserName":ToUserName,
                "LocalID":MsgID(),
                "ClientMsgId":MsgID(),}
        data.update(**kv)
        return data

    def __init__(self,uid=0):
        self.uuid           = uid
        self.QRCODE         = "QRCODE.PNG"
        self.COOKIE         = "COOKIE%s"%self.uuid
        self.lang           = "zh_CN"
        self.appid          = "wx782c26e4c19acffb"
        self.host           = "https://wx.qq.com"
        self.cookieJar = cookiejar.MozillaCookieJar(self.COOKIE)
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookieJar))
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            #'Accept-Encoding':'gzip,deflate,sdch',    #不压缩
            "Connection":"keep-alive",
            "Referer":"https://wx.qq.com",
            "Origin":"https://wx.qq.com",
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110',}
        self.Queue          = queue.Queue(0)
        self.logininfo      = {}    #登录相关信息
        self.MemberList     = {}    #好友列表   {'Uin':{...}}
        self.ContactList    = {}    #群组列表   {'Uin':{...}}
        self.SyncKey        = {}    #同步列表   {'Count':n,'List':[{'Key':1,'Val':934},]}
        self.User           = {}    #自己的信息 {...}

    def request(self,url,data=None,timeout=0):
        #logger.info(url)
        #logger.warn(data)
        if timeout:
            socket.setdefaulttimeout(timeout)  #设置超时
        if data:
            data = parse.urlencode(data).encode('utf-8')
            rr = request.Request(url, data, headers=self.headers)
        else:
            rr = request.Request(url=url, headers=self.headers)
        fp=self.opener.open(rr)
        if fp:
            if fp.info().get('Content-Encoding') == 'gzip':  #先不压缩 测试完成通过后再加入解压缩代码
                log('gzip')
            else:
                res = fp.read()
                try:
                    res = res.decode('utf-8')
                except:
                    res = res
            self.cookieJar.save(self.COOKIE,ignore_discard=True,ignore_expires=True)
            self.logininfo.update(dict([(x.name,x.value) for x in self.cookieJar]))

        #logger.error(res)
        return self._baseResponse(res)

    def getqrcode(self):
        with open(self.QRCODE,'wb') as fq:
           fq.write(self.request(url="https://login.weixin.qq.com/qrcode/%s"%self.uuid))
           fq.close()
           log("二维码已下载,请扫码登录。")

    def login(self):
        if os.path.isfile(self.COOKIE):
            #存在cookie则载入
            self.cookieJar.load(self.COOKIE,ignore_discard=True,ignore_expires=True)
        url = "https://login.weixin.qq.com/jslogin?appid={}&redirect_uri={}&fun=new&lang={}" \
            .format(self.appid,parse.quote("%s/cgi-bin/mmwebwx-bin/webwxnewloginpage"%self.host),self.lang)
        res = self.request(url)
        code,self.uuid = re.compile("""window.QRLogin.code = (\d+); window.QRLogin.uuid = "(.*?)";""").findall(res)[0]
        log(code+self.uuid)
        url = "https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=1&r={}&lang={}" \
            .format(self.uuid,RT(),self.lang)
        self.request(url)
        self.getqrcode()
        url = "https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={}&tip=0&r={}&lang={}" \
            .format(self.uuid,RT(),self.lang)
        while True:
            res = self.request(url)
            code = int(re.compile("""window.code=(\d+);""").findall(res)[0])
            if code==200:
                redirect_uri = re.compile("""window.redirect_uri="(.*?)";""").findall(res)[0]
                if redirect_uri:
                    url = "%s&fun=new&version=v2&lang=zh_CN"%redirect_uri
                    res = self.request(url)
                    #'''
                    self.logininfo['skey'] = util.find(res,'<skey>','</skey>')
                    self.logininfo['wxsid'] = util.find(res,'<wxsid>','</wxsid>')
                    self.logininfo['wxuin'] = util.find(res,'<wxuin>','</wxuin>')
                    self.logininfo['pass_ticket'] = parse.quote(util.find(res,'<pass_ticket>','</pass_ticket>'))
                    #'''
                    self.logininfo.update(dict([(x.name,x.value) for x in self.cookieJar]))
                    return res
            elif code==201:
                log("扫描成功,请确认登录。")
            elif code==408:
                log("请用手机微信扫描二维码。")
            else:
                log(code,"Error")
                return
        '''
        self.webwxinit()
        self.webwxgetcontact()

        #开始心跳
        while True:
            self.synccheck()
        '''

    def webwxinit(self):
        """微信初始化 获取SyncKey"""
        self.headers.update({
            'Accept':'application/json, text/plain, */*',
            'Content-Type':'application/json;charset=UTF-8',})
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r={}&lang={}&pass_ticket={}" \
            .format(RT(),self.lang,self.logininfo['pass_ticket'])
        result = self.request(url,self._createRequest())
        return result
        if 'SyncKey' in result.keys():
            self.SyncKey = result['SyncKey']
        if 'User' in result.keys():
            self.User = result['User']
        if 'ContactList' in result.keys():
            for data in result['ContactList']:
                self.ContactList[data['Uin']] = data
        return result

    def webwxgetcontact(self):
        """获取好友列表"""
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?pass_ticket={}&r={}&skey={}" \
            .format(self.logininfo['pass_ticket'],RT(),self.logininfo['skey'])
        result = self.request(url)
        return result
        if 'MemberList' in result.keys():
            for data in result['MemberList']:
                self.MemberList[data['Uin']] = data

    def webwxbatchgetcontact(self,ContactList):
        """获取群列表成员"""
        """ContactList=[{"UserName":"@@22e0f7da92fbead96e37fa3e9f92abc7d8748af6b485ccf9ae8472f8b823a52e","ChatRoomId":"67567675"},]"""
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxbatchgetcontact?type=ex&r={}&pass_ticket={}" \
            .format(RT(),self.logininfo['pass_ticket'])
        result = self.request(url,self._createRequest(Count=len(ContactList),List=ContactList))
        if 'ContactList' in result.keys():
            return result['ContactList']

    def synccheck(self):
        """syncCheck轮询是否有消息更新 timeout: 35000"""
        url = "https://webpush.weixin.qq.com/cgi-bin/mmwebwx-bin/synccheck?r={}&skey={}&sid={}&uin={}&deviceid={}&synckey={}&pass_ticket={}" \
            .format(RT(),
                    self.logininfo['skey'],
                    self.logininfo['wxsid'],
                    self.logininfo['wxuin'],
                    DeviceID(),
                    '|'.join(['_'.join([d['Key'],d['Val']]) for d in self.SyncKey['List']]),
                    self.logininfo['pass_ticket'],)
        res = self.request(url,timeout=35) #超时35秒
        retcode,selector = re.compile("""window.synccheck={retcode:"(.*?)",selector:"(.*?)"}""").findall(res)[0]
        if retcode == '0':
            if selector != '0':
                self.webwxsync()
        else:
            log('登出')

    def webwxsync(self):
        """sync获取消息更新具体内容"""
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid={}&skey={}&pass_ticket={}" \
            .format(self.logininfo['wxsid'],self.logininfo['skey'],self.logininfo['pass_ticket'])
        result = self.request(url,self._createRequest(SyncKey=self.SyncKey,rr=RT()))
        keys = result.keys()
        if 'SKey' in keys:
            if result['SKey']:
                self.logininfo['skey'] = result['SKey']
        if 'SyncKey' in keys:
            self.SyncKey = result['SyncKey']
        if 'ModContactList' in keys:
            pass
        if 'DelContactList' in keys:
            pass
        if 'ModChatRoomMemberList' in keys:
            pass
        if 'AddMsgList' in keys:
            for data in result['AddMsgList']:
                self.Queue.put(data)

    def webwxstatusnotify(self,ToUserName=None,code=3):
        """通知客户端修改消息状态"""
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxstatusnotify?pass_ticket={}" \
            .format(self.logininfo['pass_ticket'])
        data = {'ClientMsgId':MsgID(),
                'Code':code,
                'FromUserName':self.User['UserName'],
                'ToUserName':ToUserName if ToUserName else self.User['UserName'],}  #通常只通知自己
        result = self.request(url,self._createRequest(**data))

    def webwxsendmsg(self,ToUserName,Content,Type=1,**kv):
        """发送消息"""
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?pass_ticket={}" \
            .format(self.logininfo['pass_ticket'])
        result = self.request(url,self._createRequest(Msg=self._createMsg(ToUserName,Content,Type,**kv)))
        return result

    def webwxlogout(self):
        """登出"""
        url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxlogout?redirect=1&type=0&skey={}" \
            .format(self.logininfo['skey'])
        data = {'sid':self.logininfo['wxsid'],
                'uin':self.logininfo['wxuin'],}
        result = self.request(url,data)
        return result


wx=Wechat()
wx.login()
print(wx.webwxinit())
while True:
    Q=input('#')
    wx.synccheck()





