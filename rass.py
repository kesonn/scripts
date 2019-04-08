#coding=utf8
#用工具先分解N，求出p和q
e = 3
N = 0xBF53062CA45F25C5
p = 0xEED04DF1
q = 0xCD17D115
assert(p*q == N)
import gmpy
phi = (p-1)*(q-1)
d = gmpy.invert(e, phi)
enc = open('key.enc', 'r').read()
enc = int(enc.encode('hex'), 16)
print enc
m = pow(enc, d, N)
assert(pow(m, e, N) == enc)
print("%01024x" % m).decode('hex')
