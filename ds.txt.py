import re

response="""
<link rel="stylesheet" href="/uimc/css/login.css" type="text/css" />
path : 'https://ihs2.cert.org.cn/uimc',
success_url  : './uimc/login/erweilinglogin.htm',
<link rel="stylesheet" href="/uimc/css/login.css" type="text/css" />
path : 'https://ihs2.cert.org.cn/uimc',
success_url  : "../uimc/login/erweilinglogin.htm",
<link rel="stylesheet" href='/uimc/css/login.css' type="text/css" />
path : "https://ihs2.cert.org.cn/uimc",
success_url  : "/uimc/login/erweilinglogin.htm",
"""

urls = []
urls += re.findall("['\./|'\.\./](\..*?)[']",response)      #'./url/dsf'
urls += re.findall("[\"\./|\"\.\./](\..*?)[\"]",response)   #"../url/asd"
urls += re.findall("['](/.*?)[']",response)                     #'/url/sdf'
urls += re.findall("[\"](/.*?)[\"]",response)                 #"/url/dsf"
urls += re.findall("['http](http.*?)[']",response)          #'http://sdfsd/sdf'
urls += re.findall("[\"http](http.*?)[\"]",response)        #"http://fdsdf/sdf"

print(
urls ,len(urls)
)
