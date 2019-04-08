#!/usr/bin python
#coding: utf-8
import os
from PIL import Image
j = 1
dir="./sdata/"
for f in os.listdir(dir):
    if f.endswith(".png"):
        img = Image.open(dir+f)
        #img.show()
        for i in range(5):
            x = 0 + i*19
            #x=0
            y = 0
            img.crop((x, y, x+19, y+25)).save("./font/%d.bmp" % j, 'bmp')
            print "j=",j
            j += 1
