
class Bugs(dict):
    def getdiff(self):
        return (self['b'],self['c'])
    def __eq__(self,bug):
        return self.getdiff() == bug.getdiff()
    def __hash__(self):
        return hash(self.getdiff())

jj=[] #交集 a∩b
cj=[] #差集 b-a

#只比较b,c的值，求 a∩b 和 b-a
l1 = [{'a':1,'b':2,'c':3},{'a':2,'b':3,'c':4},{'a':3,'b':4,'c':5}]
l2 = [{'a':4,'b':2,'c':3},{'a':5,'b':4,'c':5},{'a':6,'b':4,'c':3}]

if l1 and l2:
    for j in l2:
        a = Bugs(j)
        for i in l1:
            b = Bugs(i)
            if a == b:
                jj.append(a)
            if a not in l1 and a not in cj:
                cj.append(a)
elif l2:
    cj = l2
#预期结果
#jj = [{'a':4,'b':2,'c':3},{'a':5,'b':4,'c':5}]
#cj = [{'a':6,'b':4,'c':3}]
print(jj)
print(cj)


