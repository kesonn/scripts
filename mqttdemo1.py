#-*-coding:utf-8-*-


import json
with open('1.txt','r') as f:
    a=json.loads(f.read())
print(a)
with open('11.txt','w') as f:
    for i in a['data'].keys():
        print(i)
        f.write(i)
        f.write('\n')