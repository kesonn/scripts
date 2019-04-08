import hashlib
import base64

s="jacky"
s=base64.b64encode(s)
s=s[:5].strip()
ss=hashlib.md5()
ss.update(s)
s=ss.hexdigest()
s=base64.b64encode(s[:8]+s[24:32])
ss=hashlib.md5()
ss.update(s)
s=ss.hexdigest()
s=s[8:16]
print(s)
