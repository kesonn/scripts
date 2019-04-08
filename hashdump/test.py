# -*- coding: utf-8 -*-
import mmd5
import sys
import six
import requests
import hashlib

def getmd5(MD5_Hash,length,text=None):
    s1=eval('0x'+MD5_Hash[:8].decode('hex')[::-1].encode('hex'))
    s2=eval('0x'+MD5_Hash[8:16].decode('hex')[::-1].encode('hex'))
    s3=eval('0x'+MD5_Hash[16:24].decode('hex')[::-1].encode('hex'))
    s4=eval('0x'+MD5_Hash[24:32].decode('hex')[::-1].encode('hex'))
    secret = "a"*length
    test=secret+'\x80'+'\x00'*((512-length*8-8-8*8)/8)+six.int2byte(length*8)+'\x00\x00\x00\x00\x00\x00\x00'+text
    s = mmd5.deal_rawInputMsg(test)
    r = mmd5.deal_rawInputMsg(secret)
    inp = s[len(r):]
    return mmd5.run_md5(s1,s2,s3,s4,inp)


MD5_Hash = '571580b26c65f306376d4f64e53cb5c7'
filename = 'guest'
signature = getmd5(MD5_Hash,15,filename)

print(signature)

