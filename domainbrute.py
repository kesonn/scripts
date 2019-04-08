#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
import time
import dns.resolver
import gevent
from gevent.threadpool import ThreadPool


class GeventThread(object):
  """使用异步方式"""
  def __init__(self,threads=10):
    self.Queue   = []
    self.threads = threads
    self.timeout = 10
    self.__FLAG  = True   #stop
    self.__STAT  = False  #pause
  def recv(self,*args,**kw):
    self.handler(*args,**kw)
  def run(self):
    if self.Queue and self.handler:
      self.__FLAG  = True
      self.__STAT  = False
      pool = ThreadPool(self.threads)
      Queue = iter(self.Queue)
      while self.__FLAG:
        if self.__STAT:
          time.sleep(1)
          continue
        try:
          data = next(Queue)
          pool.spawn(self.recv, data)
        except StopIteration:
          self.__FLAG = False
          break
        gevent.wait(timeout=self.timeout)
  def stop(self):
    self.__FLAG = False
    self.__STAT = False
  def pause(self):
    self.__STAT = not self.__STAT
  def setup(self,**kwargs):
    for k,v in kwargs.items():
      setattr(self,k,v)

class DNSBrute(object):
    def __init__(self,target,namelist):
        self.target = target.strip()
        self.resolvers = dns.resolver.Resolver()


    def recv(self,subdomain):
        answers = self.resolvers.query(subdomain)
        if answers:
          for answer in answers:
            self.answers.append(answer.address)

    def run(self):
        for subdomain in self.Queue:
            print subdomain,
            ans = self.resolvers.query(subdomain.strip())
            for a in ans:
                print a


if __name__ == '__main__':
    namelist = open('subnames.txt').readlines()
    d = DNSBrute('qq.com',namelist)
    d.run()

