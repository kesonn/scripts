#coding=utf8

import re
import requests


file_rds = open('rds.txt','w')
rdsre = re.compile('[a-zA-Z0-9-]+.mysql.rds.aliyuncs.com')
urlre = re.compile('<a href="(.*?)" title=".*">.*</a>')
codes = re.compile('<div class="code-list-item code-list-item-public ">(.*?)</div>')
keyword=input('>')
for page in range(1,100):
    url = "https://github.com/search?p={0}&q={1}&ref=searchresults&type=Code&utf8=%E2%9C%93".format(page,keyword)
    data = requests.get(url).text
    print(data)
    input('sdf')
    for value in re.findall(codes,data):
        code_url = ''.join(re.findall(urlre,value))
        for rds in re.findall(rdsre,value):
            print(rds)
            try:
                requests.get("http://%s:3306"%rds)
                #result.update({'key':keyword,'content':{'url':code_url,'rds':rds}})
                file_rds.write(code_url+'\n')
            except:
                pass



#https://raw.githubusercontent.com/Dalocklei/Taobao_API_Test/c0f9db782251d0fd5e3095ca6574496008465c11/Da/web/getTransferData.php~
#https://github.com/Dalocklei/Taobao_API_Test/blob/c0f9db782251d0fd5e3095ca6574496008465c11/Da/web/getTransferData.php~

