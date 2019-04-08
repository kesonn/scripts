#!/usr/bin/python
#coding:utf-8
#codeby     道长且阻
#email      ydhcui@suliu.net
#website    http://www.suliu.net

import unittest
import random
import struct
import binascii

class TEA(object):
    ''' http://baike.baidu.com/view/6064828.htm
        http://blog.chinaunix.net/uid-324919-id-135731.html
        http://abcn.cneu.eu/crypto/tea/tea.c
    '''
    @staticmethod
    def xor(a, b):
        op = 0xffffffff
        a1,a2 = struct.unpack('>LL', a[0:8])
        b1,b2 = struct.unpack('>LL', b[0:8])
        return struct.pack('>LL', ( a1 ^ b1) & op, ( a2 ^ b2) & op)

    @staticmethod
    def code(v, k):
        n=16
        op = 0xffffffff
        delta = 0x9e3779b9
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

    @staticmethod
    def encrypt(v, key):
        END_CHAR = '\0'
        FILL_N_OR = 0xF8
        vl = len(v)
        filln = (8-(vl+2))%8 + 2
        fills = ''
        for i in range(filln):
            fills = fills + chr(random.randint(0, 255))
        v = ( chr((filln -2)|FILL_N_OR)
              + fills
              + v
              + END_CHAR * 7)
        tr = '\0'*8
        to = '\0'*8
        r = ''
        o = '\0' * 8
        for i in range(0, len(v), 8):
            o = TEA.xor(v[i:i+8], tr)
            tr = TEA.xor(TEA.code(o, key), to)
            to = o
            r += tr
        return r

    @staticmethod
    def decipher(v, k):
        n = 16
        op = 0xffffffff
        y, z = struct.unpack('>LL', v[0:8])
        a, b, c, d = struct.unpack('>LLLL', k[0:16])
        delta = 0x9E3779B9
        s = (delta << 4)&op
        for i in xrange(n):
            z -= ((y<<4)+c) ^ (y+s) ^ ((y>>5) + d)
            z &= op
            y -= ((z<<4)+a) ^ (z+s) ^ ((z>>5) + b)
            y &= op
            s -= delta
            s &= op
        return struct.pack('>LL', y, z)

    @staticmethod
    def decrypt(v, key):
        l = len(v)
        prePlain = TEA.decipher(v, key)
        pos = (ord(prePlain[0]) & 0x07) +2
        r = prePlain
        preCrypt = v[0:8]
        for i in xrange(8, l, 8):
            x = TEA.xor(TEA.decipher(TEA.xor(v[i:i+8], prePlain),key ), preCrypt)
            prePlain = TEA.xor(x, preCrypt)
            preCrypt = v[i:i+8]
            r += x
        if r[-7:] != '\0'*7:
            return None
        return r[pos+1:-7]

    @staticmethod
    def entea_hexstr(data, key):
        return TEA.encrypt(data.decode('hex'), key.decode('hex')).encode('hex')

    @staticmethod
    def detea_hexstr(data, key):
        return TEA.decrypt(data.decode('hex'), key.decode('hex')).encode('hex')


class TestCaseTEA(unittest.TestCase):
    def test_tea(self):
        hexstr = '12345678'
        key = '00000000000000000000000000000000'
        self.assertEqual(TEA.detea_hexstr(TEA.entea_hexstr(hexstr, key), key), hexstr)

if __name__ == '__main__':
    unittest.main()
