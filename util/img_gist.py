import os
import sys
import Image

cur_path = os.path.abspath(os.path.dirname(__file__))

def gist(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((100, 100), Image.ANTIALIAS).convert('RGB')
    im.save('a.ppm')
    feats = os.popen(cur_path+'/compute_gist -nblocks 2 -orientationsPerScale 4,4,4 a.ppm').read().strip()
    return [float(v) for v in feats.split(' ')]

def test(): 
    path = '../static/upload/66ndiy4n5r.png'
    print 'gist len:', len(gist(path))

if __name__ == '__main__':
    test()
