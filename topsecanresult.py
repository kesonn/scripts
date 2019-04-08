#coding=utf8

import os,re

def readfile(path):
    with open(path,'r') as f:
        return f.read()

def writefile(path,data):
    with open(path,'a') as f:
        for d in data:
            f.write(d)
            f.write('\n')

def listfile(path='./'):
    f=[]
    for fn in os.listdir(path):
        if fn.endswith('html'):
            f.append(fn)
    return f

def recvfile(data):
    host = re.findall('<td>(.*?)</td>',data)[0]
    port = re.findall(r'''<div class="vul_summary" data-id=".*?" data-port="(.*?)">''',data)
    vuls = re.findall(r'''/><span class="level_danger_(.*?)" style="cursor:pointer">(.*?)</span>''',data)
    i=0
    data = []
    for md,name in vuls:
        data.append(','.join([host,port[i],md,name.decode('utf8').encode('utf8')]))
        i+=1
    return data

d=[]
for i in listfile():
    a=readfile(i)
    d += recvfile(a)
writefile('resulr.csv',d)
