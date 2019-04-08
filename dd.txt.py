import requests ,re

session = requests.session()
with open("proxies.proxy","r") as f:
    for line in f.readlines():
        proxies = {'http': line.strip()}
        try:
            resp = session.get('http://1212.ip138.com/ic.asp',proxies=proxies,timeout=1)
            print(resp.text)
        except Exception as e:
            print(e)