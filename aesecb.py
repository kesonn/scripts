#coding=utf8
from Crypto.Cipher import AES
import base64

s1 ="cGhyYWNrICBjdGYgMjAxNg=="
s2 ="sSNnx1UKbYrA1+MOrdtDTA=="
sa = AES.new(base64.b64decode(s1), AES.MODE_ECB)
print(sa.decrypt(base64.b64decode(s2)))