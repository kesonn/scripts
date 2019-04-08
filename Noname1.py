#!/usr/bin/python
#coding:utf-8
#codeby     道长且阻
#email      ydhcui@suliu.net
#website    http://www.suliu.net
class a(object):
    def __init__(self,c,e):
        self.c = c
        self.e = e
        print(3333,c)
    def __eq__(self,q):
        print(22222,self.c,q.c,self.e,q.e )
        return self.c == q.c and self.e == q.e

b=set([a(1,1)])
n=a(2,1)
if n not in b:
   print(n)