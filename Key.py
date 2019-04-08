n=97109519409189850199997869289849283920342893472938473845723894729348129381023910434923849384938439583945839485394859348593485934859348593485934859348593485934593457934752876317253617231
#f(2*n)=2*f(n)-1
#f(2*n+1)=2*f(n)+1
cc=n
A=1
array=[]
while True:
    if(cc%2==1):
        array.append(1)
    else:
        array.append(-1)
    cc=cc/2
    if cc==1:
        break
print array
arr=array[::-1]
for ar in arr:
    A=A*2+ar
s=A%987654321235
print s
import hashlib
md5=hashlib.md5()
md5.update(str(s))
s=md5.hexdigest()[8:24]
print(s)