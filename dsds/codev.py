#coding=utf8
from PIL import Image
from pytesser import image_to_string
import requests
import time
PATH ="vcode.png"
r = requests.Session()
while True:
    c=r.get("http://www.hualixy.com/inc/checkcode.asp?r=%s"%time.time()).content
    #print(c)
    with open(PATH,'wb') as f:
     f.write(c)
     f.close()
    code = image_to_string(Image.open(PATH)).strip()
    print(code)



