#!/usr/bin/env python
#coding:UTF-8

import os
from PIL import  Image

def binary(f):
    img = Image.open(f)
    pixdata = img.load()
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
    return img
    
def cut(img):
    font = []    
    for i in range(5):
        x=0+i*19
        y=0
        font.append(img.crop((x,y,x+19,y+25)))

    return font
    
def compare(img, im):
    num = 0
    for x in range(19):
        for y in range(25):
            if img[x, y] != im[x, y]:
                num += 1
    return num
    
def recognize(img):
    tmp = 1000
    num = -1
    for i in range(10):
        im = Image.open('./font_res/%d.png' % i).convert('RGBA').load()
        if compare(img.convert('RGBA').load(), im) < tmp:
            tmp = compare(img.convert('RGBA').load(), im)
            num = i
    return num
    
if __name__ == '__main__':
    num = 0
    codedir="./data1/"
    for imgfile in os.listdir(codedir):
        if imgfile.endswith(".png"):
            fname = imgfile[0:-4]
            #print fname
            img=binary(codedir+imgfile)
            font = cut(img)
            str_tmp = ''
            for im in font:
                str_tmp += str(recognize(im))
            #print str_tmp
            a = int(str_tmp)*int(fname)
            num +=a
    print num