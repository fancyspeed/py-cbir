#!/usr/bin/python
import os
import sys
import glob
import math
import Image

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'

def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h


def phash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),
                  0)

avg = lambda x: sum([i*c for i, c in enumerate(x)]) / (sum(x) + 0.1)
update = lambda oldi, oldv, newi, newv: (oldi, oldv) if oldv > newv else (newi, newv) 

def otsu_hash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.convert('L')
    hist = im.histogram()
    tot_avg = avg(hist)
    max_i, max_score = 0, 0
    for i in range(len(hist)):
        num1, avg1 = sum(hist[:i]), avg(hist[:i])
        num2, avg2 = sum(hist[i:]), avg(hist[i:])
        score = num1 * (avg1 - tot_avg)**2 + num2 * (avg2 - tot_avg)**2
        max_i, max_score = update(max_i, max_score, i, score)
    im = im.resize((8, 8), Image.ANTIALIAS)
    return reduce(lambda x, (y, z): x | (z<<y), 
                  enumerate(map(lambda i: 0 if i < max_i else 1, im.getdata())),
                  0)

def otsu_hash2(im):
        if not isinstance(im, Image.Image):
            im = Image.open(im)
        im = im.convert('L')
        hist = im.histogram()
        tot_avg = avg(hist)
        max_i, max_score = 0, 0
        for i in range(len(hist)):
            num1, avg1 = sum(hist[:i]), avg(hist[:i])
            num2, avg2 = sum(hist[i:]), avg(hist[i:])
            score = num1 * (avg1 - tot_avg)**2 + num2 * (avg2 - tot_avg)**2
            max_i, max_score = update(max_i, max_score, i, score)
        im = im.resize((8, 8), Image.ANTIALIAS)
        x, y = 8, 8 
        up_score, down_score, n_up, n_down = 0, 0, 0, 0
        for i in range(x):
            for j in range(y):
                score = math.sqrt((i-x/2)**2 + (j-y/2)**2)
                if im.getpixel((i, j)) > max_i:
                    up_score += score
                    n_up += 1
                else:
                    down_score += score
                    n_down += 1
        if up_score/n_up <= down_score/n_down:
            return reduce(lambda x, (y, z): x | (z<<y), 
                          enumerate(map(lambda i: 0 if i < max_i else 1, im.getdata())), 0)
        else:
            return reduce(lambda x, (y, z): x | (z<<y), 
                          enumerate(map(lambda i: 0 if i >= max_i else 1, im.getdata())), 0)

def test():
    path = '../static/upload/66ndiy4n5r.png'
    print '%X' % otsu_hash(path)
    print otsu_hash2(path)
    
def demo(sys):
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print "Usage: %s image.jpg [dir]" % sys.argv[0]
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
        h = phash(im)

        os.chdir(wd)
        images = []
        for ext in EXTS:
            images.extend(glob.glob('*.%s' % ext))

        seq = []
        prog = int(len(images) > 50 and sys.stdout.isatty())
        for f in images:
            seq.append((f, hamming(phash(f), h)))
            if prog:
                perc = 100. * prog / len(images)
                x = int(2 * perc / 5)
                print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
                print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
                sys.stdout.flush()
                prog += 1

        if prog: print
        for f, ham in sorted(seq, key=lambda i: i[1]):
            print "%d\t%s" % (ham, f)

if __name__ == '__main__':
    test()
    demo(sys)
