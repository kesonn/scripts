import time
alist = []
aset = set()
s1 = time.time()

for i in range(10000000):
    alist.append(i)
s2 = time.time()

for j in range(10000000):
    aset.add(j)
s3 = time.time()

print(s2-s1)
print(s3-s2)

for k in range(10000):
    k in alist
s4 = time.time()

for l in range(10000):
    l in aset
s5 = time.time()

print(s4-s3)
print(s5-s4)