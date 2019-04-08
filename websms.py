import requests
import json

url = "http://www.ichboard.com"
a = "/v1/users/register/new"
b = "/v1/sms"
while True:
    phone = input('>')
    data = json.dumps({"name":"test","password":"aaaa","phone":phone,"email":"w@w.m"})
    res = json.load(requests.post(url+a,data).text)
    print(res)
    data = json.dumps({"key":res['content']['key'],"ts":int(res['content']['ts']),"phone":phone})
    res = requests.post(url+b,data).text
    print(res)