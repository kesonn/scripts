#coding=utf8

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind(("127.0.0.1", 0))
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 0)
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

while True:
    pkt = s.recvfrom(65535)
    print(pkt)

