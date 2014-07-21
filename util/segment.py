#!/usr/bin/python
import os
import sys
import glob
import Image
import math
from img_hash import avg, update 

class MRFSegmenter(object):
    def __init__(self):
        pass

    def init(self, im):
        if not isinstance(im, Image.Image):
            im = Image.open(im)
        im = im.resize((100, 100), Image.ANTIALIAS)
        im.show()
        im2 = im.convert('L')
        avg = reduce(lambda x, y: x + y, im2.getdata()) / 10000.
        for x in range(100):
            for y in range(100):
                if im2.getpixel((x, y)) > avg:
                    im2.putpixel((x, y), 255)
                else:
                    im2.putpixel((x, y), 0)
        im2.show()

        
def test():
    path = '../static/dataset/simpcity/1.jpg'
    #seg = MRFSegmenter()
    #seg.init(path)

if __name__ == '__main__':
    test()
        
