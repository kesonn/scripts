#coding=utf8

import hashlib
import multiprocessing
import threading
import time


def log(s,fn='log'):
    with open(fn,'a+') as f:
        f.write(s)
        f.write('\n')
        f.flush()

def hash(s):
    m = hashlib.md5()
    m.update(s.encode())
    return  m.hexdigest()


def burp(r,n):
    time.sleep(n)
    r=iter(r)
    while True:
        #try:
            try:
                i=next(r)
            except:
                break
            s='0e%s'%i
            m=hash(s)
            #print(str(n)+'   '+s+'       hash:'+m)
            if m[:2]=='0e':
                log(s+'      '+m)
                if m[2:].isdigit():
                    log(s+'      '+m,'success')
                    return True
        #except Exception as e:
            #log(e,'err')
def burp1(r,i):
    print(iter(r),i)

def main(n):
    while True:
        for i in range(10):
            p=n+100000
            r=range(n,p)
            t=threading.Thread(target=burp,args=(r,i,))
            t.start()
            t.join()
            n=p

if __name__ == '__main__':
    main(42991780)
