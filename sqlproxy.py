#!/usr/bin/python
# -*- coding: UTF-8 -*-
import execjs
import binascii
import json
import logging
import os
import re
import sys
import socket
import time
import urllib
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.iostream

jst = open('test.js','r').read()
jse = execjs.compile(jst)

class ProxyHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        req = {
            "RequestId":"10000000001",
            "MethodName":"QueryDBGD",
            "GdType":"1",
            "LoginID":"sysscan",
            "TitleOrOrderNo":"11",
            "LinkName":self.get_argument('no','1'),
            "SubscribeStartTime":"",
            "SubscribeEndTime":"",
            "Page":"1",
            "PageSize":"10",
            "Extend":"",
            "Signature":"e026fdda203c200468fab10b6538c3138f1296c3",
            "ReqTimestamp":int(time.time()*1000)
        }
        client = tornado.httpclient.AsyncHTTPClient()
        req = tornado.httpclient.HTTPRequest(
            "http://120.198.246.21:9101/bssAppServ/getBssData.do",
            method = 'POST',
            body = urllib.urlencode({"ReqKey":jse.call('encode', json.dumps(req))})
        )
        response = yield tornado.gen.Task(client.fetch,req)
        if response.error:
            self.write("Error: %s" % response.error)
        else:
            self.write(jse.call('decode',json.loads(response.body)['rspData']))
            #self.write(response.body)
        self.finish()

def run_proxy(port):
    app = tornado.web.Application([
        (r'/sql', ProxyHandler),
    ])
    app.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()

if __name__ == '__main__':
    run_proxy(8080)
    print(jse.call('decode','69544D7D41605F17423DE9D9135D2267D5113702CEF298B65FF5274F8BA752BC6DD101867117579C6DD101867117579C8329D69479F06B2860AF31BD317BF64CD98027DD40C51057246D9C85DD80B7A4FB6E7D64B653566C546CC09A762896204689999E89845E8BE3AE1FA3EA88D1F138CA301767E3D6D5C588C3B125BA9194EA034DCD97E8C50E9CC492C573EFAEABAC5D1F3CA8C8331D1049A4FEC300A9E568B38390BE9A7086303FEE282685AACDF6261F463D89A7F642CA8B639E66FA881EB30C22CB06E366C6305FAF4A5F3BFA0F6AF81648BD32FE2973B47F0C6A8308BFD024D6F5E48CBEDA06420D81E8A4BDDF15524A098183CD5AB994FCCD81AA0FC8CD4C6ECB630B849345E77A201EC84923853C6B04ECD6E617B3A6BE89018F6BDA06420D81E8A4BD5AB994FCCD81AA0FC8CD4C6ECB630B849345E77A201EC8497DEF47C40F12D15C5431A6EE94668687B32E2D087D09D6EB19F026D27414AF31DA06420D81E8A4BD8329D69479F06B28CC31716A2590AD0446473C91080CB996C6305FAF4A5F3BFAC283BEED745DABB74F352D336E398D57C388AA23554011EB06AA5C33A09E8459B0A88E2FB863BDADEBC738AB00BB82DADA06420D81E8A4BDE461B4C148248A94D89A15FFBD9C117B11D28AD0A4AEEA9AB56C59A5A4EC3FD3EFB720601FF76A372CDA559538547089AD4679182F7C4C3FF6DD52BECB807D5B99C8445149EA8BC0BA0127C5120B42B05397DCC9D180F59E04DCEC9121DFCF85D82443FCCD54B35F3FC993F4330C2BE5D10F5F5908315EB8C0C77DF0A1616BCD862B476FD7A8A6AA2AB8F817B5639847'))
