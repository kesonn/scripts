#!/usr/bin/python
#coding:utf-8

import socket

def sss(f):
    target = []
    for l in  f.split('\n'):
        ll = []
        for r in  l.strip():
            if r == '1':
                r=0
            if r == '0':
                r=1
            ll.append(r)
        target.append(ll)


    '''
    m = [[0,1,0,0,0,1,1,0,0,0,1,1,1,1,1],
         [1,0,0,0,1,1,0,1,1,1,0,0,1,1,1],
         [0,1,1,0,0,0,0,1,1,1,1,0,0,1,1],
         [1,1,0,1,1,1,1,0,1,1,0,1,1,0,0],
         [1,1,0,1,0,0,1,0,1,1,1,1,1,1,1],
         [0,0,1,1,0,1,1,1,0,1,0,0,1,0,1],
         [0,0,1,1,0,1,1,1,0,1,0,0,1,0,1],
         [0,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
         [0,0,1,1,0,1,1,0,1,1,1,1,1,0,1],
         [1,1,0,0,0,1,1,0,1,1,0,0,0,0,0],
         [0,0,1,1,1,1,1,0,0,0,1,1,1,1,0],
         [0,1,0,0,1,1,1,1,1,0,1,1,1,1,0]];
    '''

    m=target[1:-1]


    #算法思路：
    # 使用一个栈，在python可以用列表当做栈使用
    # 一开始，栈中只有入口单元 cell(0,0)；其中0,0是单元在迷宫矩阵中所处位置
    # 对栈中最上面的单元stack[-1], 寻找相邻的未在栈中出现的通道单元，简称新邻单元
    # 如果最上面单元即是出口单元，则打印出栈中内容即为迷宫的解答路径，跳出循环
    # 否则如果最上面的单元的8个方向还有未试探的，试探这个方向的新邻单元；有新邻单元就压入栈中
    # 否则，从栈中弹出该单元
    result = []
    class cell:
        def __init__(self,x,y):
            self.x,self.y=x,y
            if self.x>=0 and self.x<len(m) and self.y>=0 and self.y<len(m[-1]): self.value=m[self.x][self.y]
            else: self.value=1
            self.direction=0
        def newnextcell(self):
            ds=((0,1),(1,0),(0,-1),(-1,0))
            i,j = ds[self.direction]
            self.direction += 1
            return cell(self.x+i,self.y+j)

    stack=[cell(0,0)]

    while(stack):
        curcell=stack[-1]
        if (curcell.x,curcell.y)==(len(m)-1,len(m[-1])-1): aa=[(c.x,c.y) for c in stack]; return len(aa);break
        elif curcell.direction < 4:
            nn=curcell.newnextcell()
            if nn.value==0 and (nn.x,nn.y) not in [(c.x,c.y) for c in stack]: stack.append(nn)
        else: stack.pop()

HOST = "www.loudong.org"
PORT = 28880
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
TCPClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClient.connect(ADDR)


while True:
    recvdate = TCPClient.recv(BUFFERSIZE)
    if recvdate:
        print recvdate
        if '(y/n)' in recvdate:
            TCPClient.send('%s' % ('y'))
        if '#Maze' in recvdate:
            TCPClient.send('%s' % ('y'))
        #TCPClient.send('%s' % ('\n'))

TCPClient.close()

