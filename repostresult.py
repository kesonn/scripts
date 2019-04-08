#coding=utf8

import os,re,codecs

def readfile(path):
    with codecs.open(path,'r') as f:
        return f.read()

def writefile(path,data):
    with codecs.open(path,'w') as f:
      f.write(','.join([
        '漏洞等级','主机IP','所在端口','漏洞名称','详细描述','解决办法','\n'
      ]))
      for host,vuls in data.items():
        for name,vul in vuls.items():
            d=','.join([
                  vul['m'],
                  host,
                  vul['p'],
                  name,
                  vul['i1'].strip(),
                  vul['i2'].strip(),
               ])
            f.write(rehtml(d).strip())
            f.write('\n')

def listfile(path='./'):
    f=[]
    for fn in os.listdir(path):
        if fn.endswith('.html'):
            f.append(fn)
    return f

def rehtml(html):
    dr = re.compile(r'<[^>]+>',re.S)
    html = dr.sub('',html)
    html = html.replace('\n','')
    html = html.replace(' ','')
    html = html.replace('&#34;','\'')
    html = html.replace('&#39;','"')
    html = html.replace('&lt;','<')
    html = html.replace('&gt;','>')
    return html

def recvfile(data):
    host = re.findall('<td>(.*?)</td>',data)[0]
    port = re.findall(r'''<div class="vul_summary" data-id=".*?" data-port="(.*?)">''',data)
    vuls = re.findall(r'''/><span class="level_danger_(.*?)" style="cursor:pointer">(.*?)</span>''',data)
    info1 = re.findall('''<th width="100">详细描述</th>[\s\S]*?<td>([\s\S]*?)</td>''',data)
    info2 = re.findall('''<th width="100">解决办法</th>[\s\S]*?<td>([\s\S]*?)</td>''',data)
    i=0
    data={}
    for md,name in vuls:
        data[name]={}
        data[name]['m'] = md
        data[name]['p'] = port[i]
        data[name]['i1'] = info1[i]
        data[name]['i2'] = info2[i]
        i+=1
    return host,data

def main():
    d={}
    for f in listfile():
        p = readfile(f)
        h,s = recvfile(p)
        d[h] = s
    writefile('resulr.csv',d)

main()
