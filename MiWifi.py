#coding=utf8

import requests
import json
import time

def callback(data):
    print(data)
    data = data.split('callback(')[1].split(');')[0]
    return json.loads(data)

class MiWifi(object):
    def __init__(self):
        self.req = requests.Session()
        self.guesthost = "http://guest.miwifi.com:8999"
        self.apihost   = "http://api.miwifi.com"
        self.headers = {"Referer": "http://guest.miwifi.com:8999/wifishare.html"}

    def init(self):
        uri = self.guesthost + '/cgi-bin/luci/api/misns/sns_init?callback=callback'
        res = self.req.get(uri)
        data = callback(res.text)
        self.deviceid = data['deviceid']
        self.clientinfo = data['clientinfo']
        self.ssid = data['ssid']

    def prepare(self):
        url = self.guesthost + "/cgi-bin/luci/api/misns/prepare?callback=callback"
        res = self.req.get(url)
        return callback(res.text)

    def clickad(self):
        self.prepare()
        uri = self.apihost + '/wifirent/api/ad_apply_rent'
        data= {
            'callback':'callback',
            'router_id':self.deviceid,
            'client_info':self.clientinfo}
        res = self.req.post(uri,data,)
        return callback(res.text)

    def qrcode(self):
        url = self.apihost + "/wifirent/api/get_official_account?callback=callback&version=1&router_id=%s&client_info=%s"%(self.deviceid,self.clientinfo)
        res = self.req.get(url)
        return callback(res.text)
        #if res['code'] == 0:
        #    self.req.get(res['data']['url'])
        #assa({"code":0,"data":{"url":"http://api.goluodi.com/xiaomi/createurl?appid=wxbc99939cfc1fcf16&mac=e3:b0:bf:da:8e:65&extend=aWRlbnRpZnk9MTc3Jm1hYz1lMzpiMDpiZjpkYTo4ZTo2NSZ0YXNraWQ9NjQyNDkmcHQ9MyZ0b2tlbj0xNTMwMzM5ODQ1MTAwMTYzMDc=&ssid=WiFi&shopid=17067708&secretkey=e1a8d51e736c5ece93c95682d6f946cc"}})

    def loop(self):
        self.init()
        while True:
            try:
                res = self.clickad()
                res = self.qrcode()
                if res['code'] !='0':
                    self.init()
            except Exception as e:
                print(e)
            time.sleep(60)

MW = MiWifi()
MW.loop()