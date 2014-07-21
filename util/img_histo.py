#!/usr/bin/python
import Image
from hsv import convert2hsv

normalize = lambda x: [float(v)/sum(x) for v in x]
sample = lambda x: [sum(x[i:i+4]) for i in xrange(0, 255, 4)]

n_bin = 8
bin_size = 32

def gray_histo(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    #im = im.resize((200, 200), Image.ANTIALIAS).convert('L')
    im = im.convert('L')
    histo = im.histogram()
    return normalize(sample(histo))

def gothrough_img(im, binsize=64):
    w, h = im.size
    for x in range(w):
        for y in range(h):
            p = im.getpixel((x, y))
            r, g, b = p[0]/binsize, p[1]/binsize, p[2]/binsize
            s = 256 / binsize
            yield r * s**2 + g * s + b

def stat(v_list, v_len=64):
    histo = [0] * v_len
    for x in v_list:
        histo[x] += 1
    return histo

def rgb_histo(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    #im = im.resize((200, 200), Image.ANTIALIAS).convert('RGB')
    im = im.convert('RGB')
    v_list = gothrough_img(im, bin_size)
    return normalize(stat(v_list, n_bin**3))

def yuv_histo(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    #im = im.resize((200, 200), Image.ANTIALIAS).convert('YCbCr')
    im = im.convert('YCbCr')
    v_list = gothrough_img(im, bin_size)
    return normalize(stat(v_list, n_bin**3))

def hsv_histo(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    #im = im.resize((200, 200), Image.ANTIALIAS).convert('RGB')
    im = im.convert('RGB')
    im = convert2hsv(im)
    v_list = gothrough_img(im, bin_size)
    return normalize(stat(v_list, n_bin**3))

def abs_dist(h1, h2):
    h = sum([abs(h1[i]-h2[i]) for i in range(len(h1))]) 
    return h


def test():
    path = '../static/upload/66ndiy4n5r.png'
    path = '../static/dataset/simpcity/0.jpg'
    print gray_histo(path)
    print rgb_histo(path)
    print yuv_histo(path)
    print hsv_histo(path)

if __name__ == '__main__':
    test()
