#!/usr/bin/python
#coding:utf-8
#codeby     道长且阻
#email      ydhcui@suliu.net
#website    http://www.suliu.net

import socket
import datetime

"""
定义基本的信息: 主机和端口要和服务器一致
"""
HOST = "114.55.22.127"  #服务其地址
PORT = 3306       #服务器端口
BUFFERSIZE = 1024
ADDR = (HOST, PORT)

"""
建立套接字,开始连接
"""
TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClient.connect(ADDR) #连接服务器

"""
开始进行数据的传输
"""
while True:
    senddate = raw_input("input:")
    if senddate:
        TCPClient.send('%s' % (senddate))  #发送数据
    recvdate = TCPClient.recv(BUFFERSIZE)  #接受数据
    print  recvdate

"""
传输完毕，关闭套接字
"""
print "client close"
TCPClient.close()
