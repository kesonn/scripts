import base64
import json
import time
import requests
i=1
while True:
    try:
        st = time.time()
        with open('AntiVC2.3.dll','r') as f:
            dll = base64.b64encode(f.read())*i
            data = json.dumps({
                "token":"02a65881687af2503857ce0130dc0b99",
                "uid":10320,
                "picname":"%00.jpg",
                "picinfo":"data:text/plain;base64,%s"%dll,
                "pictype":"post"})
            f.close()
        url = "http://www.ichboard.com/v1/upload"
        req = requests.post(url,data)
        print req.text#['content']['picurl']
        now = int(time.time()- st)
        print i,len(dll),now,
        i+=1
    except:
        pass
