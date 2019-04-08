#!/usr/bin/env python
# encoding=utf-8
#codeby     道长且阻
#email      ydhcui@suliu.net/QQ664284092
#website    http://www.suliu.net


import ftplib
import telnetlib
import socket
import binascii
import hashlib
import struct
import re
import time
import threading

def check_mssql(host,port=1433,user='sa',pwd='',timeout=10):
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
       sock.connect((host,port))
       hh = binascii.b2a_hex(host)
       husername = binascii.b2a_hex(user)
       lusername = len(user)
       lpassword = len(pwd)
       ladd = len(host)+len(str(port))+1
       hladd = hex(ladd).replace('0x','')
       hpwd = binascii.b2a_hex(pwd)
       pp = binascii.b2a_hex(str(port))
       address = hh+'3a'+pp
       hhost = binascii.b2a_hex(host)
       data = ("02000200000000001234567890000000"
               "00000000000000000000000000000000"
               "000000000000ZZ544000000000000000"
               "00000000000000000000000000000000"
               "00000000000X33600000000000000000"
               "00000000000000000000000000000000"
               "000000000Y3739333400000000000000"
               "00000000000000000000000000000000"
               "000000040301060a0901000000000200"
               "0000000070796d7373716c0000000000"
               "00000000000000000000000000000000"
               "00000712345678900000000000000000"
               "00000000000000000000000000000000"
               "00ZZ3360000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "00000000000000000000000000000000"
               "000Y0402000044422d4c696272617279"
               "0a00000000000d1175735f656e676c69"
               "73680000000000000000000000000000"
               "0201004c000000000000000000000a00"
               "0000000000000000000000000069736f"
               "5f310000000000000000000000000000"
               "00000000000000000000000501353132"
               "000000030000000000000000")
       data1 = data.replace(data[16:16+len(address)],address)
       data2 = data1.replace(data1[78:78+len(husername)],husername)
       data3 = data2.replace(data2[140:140+len(hpwd)],hpwd)
       if lusername >= 16:
           data4 = data3.replace('0X',str(hex(lusername)).replace('0x',''))
       else:
           data4 = data3.replace('X',str(hex(lusername)).replace('0x',''))
       if lpassword >= 16:
           data5 = data4.replace('0Y',str(hex(lpassword)).replace('0x',''))
       else:
           data5 = data4.replace('Y',str(hex(lpassword)).replace('0x',''))
       hladd = hex(ladd).replace('0x', '')
       data6 = data5.replace('ZZ',str(hladd))
       data7 = binascii.a2b_hex(data6)
       sock.send(data7)
       packet = sock.recv(1024)
       if 'master' in packet:
           payload = "username:%s,password:%s" % (user,pwd)
           print(host,payload)
           return True
   except Exception as e:
       #print(e)
       return False
   finally:
       sock.close()
       print(host+'\n')


with open('1433.txt') as f:
    for host in f.readlines():
        threading.Thread(target=check_mssql,args=(host.strip(),1433,'sa','',)).start()