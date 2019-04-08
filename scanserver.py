#coding=utf8

import sys,re,threading,requests

if len(sys.argv)<2:
    raise Exception(u'请输入要处理的文件路径')
else:
    path = sys.argv[1]

def getver(url):
    if not url.startswith(('http','HTTP')):
        url = 'http://'+url
    url = '/'.join(url.strip().split('/')[:3]) #取主机
    try:
        req = requests.get(url+'/TOPSEC404TEST.txt',timeout=60)
    except Exception as e:
        return url,'timeout'
    headers = req.headers
    text = req.text
    server = headers.get('Server') if 'Server' in headers else headers.get('X-Powered-By')
    if 'Tomcat' in text:
        server = re.findall("<h3>(.*?)</h3>",text)[0]
    if 'Hypertext' in text:
        server = 'Weblogic '+re.findall("<H4>(.*?)404 Not Found</H4>",text)[0]
    return url,server

with open(path,'r') as fr:
    with open('result.csv','w') as fw:
        fw.write('url,server,osver\n')
        for li in fr.readlines():
            if li:
                ver = getver(li)
                print(ver)
                fw.write('%s,%s\n'%ver)

