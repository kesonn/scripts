#coding=utf8
from itertools import imap
def fox(x):#求阶乘
    return reduce(long.__mul__, imap(long, xrange(1, x + 1)))

def primefactors(n):#求因数
    f = 2
    while f * f <= n:
        while not n % f:
            yield f
            n //= f
        f += 1
    if n>1:
        yield n

'''
x=52013!尾巴连续零的个数，
y=1!+2!+3!+4!+.......+52013!的末尾19位数（十进制数），
z=52013^52013的所有因数之和mod 9690(^表示幂运算)，
x+y+z的十六进制表达值（不含0x，小写)即为答案
'''
print sum(primefactors(600851475149867585764536753))
