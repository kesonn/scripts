#!/usr/bin/env python3

import os
import sys

class XOR_CBC:
    BLOCK_SIZE = 16

    def __init__(self, key: bytes, iv: bytes):
        self.key = key
        self.iv = iv
        assert len(key) == len(iv) == self.__class__.BLOCK_SIZE

    def pad(self, msg: bytes):
        l = len(msg)
        padding_len = 16 - len(msg) % 16
        return msg + (chr(padding_len) * padding_len).encode()

    def xor(self, a, b):
        return bytes([x ^ b[i%len(b)] for i, x in enumerate(a)])

    def encrypt(self, msg: bytes):
        padded_msg = self.pad(msg)

        block_size = self.__class__.BLOCK_SIZE

        assert len(padded_msg) % block_size == 0
        count = len(padded_msg) // block_size

        c = []

        last = self.iv
        for i in range(count):
            xored_plain = self.xor(padded_msg[i*block_size:(i+1)*block_size], last)
            cipher_text = self.xor(xored_plain, self.key)
            last = cipher_text
            c.append(cipher_text)

        return b''.join(c)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: %s <plain_text>')
        sys.exit(0)

    key = os.urandom(16)
    iv = os.urandom(16)
    cipher = XOR_CBC(key, iv)

    with open(sys.argv[1], 'rb') as f:
        encrypted = cipher.encrypt(f.read())

    with open(sys.argv[1]+'.encrypted', 'wb') as f:
        f.write(encrypted)




#########################
#decode
"""
代码逻辑是对明文按16位分块加密，第一块与初始向量iv做异或，再与key做异或；后续明文块与前一个密文块做异或，再与key做异或。
在加密之前，为了保证明文长度可以被16整除，首先对明文做一个padding

 def pad(self, msg: bytes):
        l = len(msg)
        padding_len = 16 - len(msg) % 16
        return msg + (chr(padding_len) * padding_len).encode()
我们已知密文和原始明文的最后一部分，那么可以根据上述逻辑遍历出key：从末尾向前计算：
密文1 = 密文2^明文1^key
密文2 = 密文3^明文2^key
计算这两个key然后比较，如果两个key相同，就是正确的key。
算出来明文补了两位，key:
[127, 84, 183, 104, 20, 239, 255, 134, 158, 177, 142, 38, 36, 137, 8, 162]
然后根据前面的分析，从后往前计算明文，每一个明文块都是密文块异或后一个密文异或key：
"""

def xor(a, b):
    return bytearray([i^j for i,j in zip(a, b)])
k = [127, 84, 183, 104, 20, 239, 255, 134, 158, 177, 142, 38, 36, 137, 8, 162]
with open('enctypted.txt', 'rb') as f:
    c = bytearray(f.read())
res = bytearray()
for i in range(len(c), 0, -16):
    tmp = xor(c[i-16:i], c[i-32:i-16])
    res = xor(tmp, k) + res
print repr(res)