#coding=utf8

import base64
import struct
from random import seed
from random import randint
from hashlib import md5
import codecs

seed()
op = 0xffffffff
delta = 0x9e3779b9

import rsa

__all__ = ['getqqpass', 'getqqhash']

seed()
op = 0xffffffff
delta = 0x9e3779b9

#RSA 公钥
pubkey = "F20CE00BAE5361F8FA3AE9CEFA495362FF7DA1BA628F64A347F0A8C012BF0B254A30CD92ABFFE7A6EE0DC424CB6166F8819EFA5BCCB20EDFB4AD02E412CCF579B1CA711D55B8B0B3AEB60153D5E0693A2A86F3167D7847A0CB8B00004716A9095D9BADC977CBB804DBDCBA6029A9710869A453F27DFDDF83C016D928B3CBF4C7"
rsaPublickey = int(pubkey, 16)
key = rsa.PublicKey(rsaPublickey, 3)

def xor(a, b):
    a1,a2 = struct.unpack('>LL', a[0:8])
    b1,b2 = struct.unpack('>LL', b[0:8])
    r = struct.pack('>LL', ( a1 ^ b1) & op, ( a2 ^ b2) & op)
    return r

def code(v, k):
    n=16
    k = struct.unpack('>LLLL', k[0:16])
    y, z = struct.unpack('>LL', v[0:8])
    s = 0
    for i in range(n):
        s += delta
        y += (op &(z<<4))+ k[0] ^ z+ s ^ (op&(z>>5)) + k[1]
        y &= op
        z += (op &(y<<4))+ k[2] ^ y+ s ^ (op&(y>>5)) + k[3]
        z &= op
    r = struct.pack('>LL',y,z)
    return r

def encrypt(v, k):
    END_CHAR = b'\0'
    fills = b''
    filln = ((8-(len(v)+2))%8) + 2
    list = [b'"', b'\xd8', b'\xc3', b'A', b'~', b's', b'\xa6', b'\xc9']
    for i in list:
        fills = fills + i#chr(randint(0,0xff))
    v = (b'\xfe' #(chr((filln-2)|0xF8)
        + fills
        + v
        + END_CHAR *7)
    tr = to = o = END_CHAR * 8
    r = b''
    for i in range(0, len(v), 8):
        g = v[i:i+8]
        o = xor(g,tr)
        tr = xor(code(o,k),to)
        to = o
        r += tr
    return r

def getqqpass(q, p, v):
  q = int(q)
  p = p.encode()
  p = md5(p).digest()
  #TEA 的KEY
  m = md5(p + codecs.decode("%0.16X" % q, 'hex_codec')).digest()
  #RSA的加密结果
  n = rsa.encrypt(p, key)
  #RSA 结果的长度
  d = codecs.decode("%0.4X" % len(n), 'hex_codec')
  #RSA 加密结果
  d += n
  #salt
  d += codecs.decode("%0.16X" % q, 'hex_codec')
  #验证码长度
  d += codecs.decode("%0.4X" % len(v), 'hex_codec')
  #验证码
  d += v.upper().encode()
  #TEA 加密并Base64编码
  r = base64.b64encode(encrypt(d,m)).decode()
  #对特殊字符进行替换
  return r.replace('/', '-').replace('+', '*').replace('=', '_')

def getqqhash(x,K):
    N = [0,0,0,0]
    for T in range(len(K)):
        N[T % 4] = N[T % 4] ^ ord(K[T])
    U = ['EC','OK']
    V = [0,0,0,0]
    V[0] =  int(x) >> 24 & 255 ^ ord(U[0][0])
    V[1] =  int(x) >> 16 & 255 ^ ord(U[0][1])
    V[2] =  int(x) >> 8 & 255 ^ ord(U[1][0])
    V[3] =  int(x) & 255 ^ ord(U[1][1])
    U = [0,0,0,0,0,0,0,0]
    for T in range(8):
        U[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]
    N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    V = ""
    for T in range(len(U)):
        V += N[U[T] >> 4 & 15]
        V += N[U[T] & 15]
    return V


if __name__=='__main__':
    print(
        getqqpass('1149757929','111111','WUWV'),
        #zAlZmx9YUa9uH0hMOgOnGhr5FKZH4ENLPzAa3hNMJvrHixL2YnFW6kwMt6APl1*81BmtZjPV5f-B7FqNwAsUYMDzH89gg5hG-PVcu6dGhvN*aENOqH3K2OtN3CkV30BgtphUStvfXAF2hPyQH87HCe1QsdBBYfYyakzmkrsV5v6gVCvj*VEl4itZsDwoYpRrcgLvdzG7Tf5n1pHifceNSQ__
        getqqhash('1149757929','48e265b2412d99ff49611a4ab7de097700806e7c4dbbe32cfd446bdc2bda111b'),
        #5C0104C458A606A2

    )




