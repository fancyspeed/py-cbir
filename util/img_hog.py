import os
import sys
import Image 
from hog import hog
from kmeans import kmeans, kmeans_classify, load_centers
from lsh import LSH_hog

cur_path = os.path.abspath(os.path.dirname(__file__))
center_path = os.path.join(cur_path, '../conf/hog_kmeans.txt')

centers = None

def hog2(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((100, 100), Image.ANTIALIAS).convert('RGB')
    im.save('a.jpg')
    F = hog('a.jpg')
    feat_list = []
    for fs in F:
        for f in fs:
            feat_list.append(list(f))
    return feat_list

def hog3(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((100, 100), Image.ANTIALIAS).convert('RGB')
    im.save('a.jpg')
    F = hog('a.jpg')
    feat_list = []
    for i, fs in enumerate(F):
        if i % 2 == 1: continue
        for j, f in enumerate(fs):
            if j % 2 == 1: continue
            feat_list.append(list(f))
    return feat_list

def hog_lsh_list(im):
    feat_list = hog3(im)
    F = []
    for feat in feat_list:
        lsh = LSH_hog(feat)
        F.append(lsh)
    return F

def hog_histo(im, p_centers=center_path):
    global centers
    if centers == None:
        centers = load_centers(p_centers)
    F = hog2(im)
    histo = {}
    for feat in F:
        c = kmeans_classify(centers, feat)
        histo[c] = histo.get(c, 0) + 1
    return [histo.get(c, 0) for c in range(len(centers))]


def test():
    full_path = '../../dataset/lena.png'
    feat = hog2(full_path)
    print len(feat), len(feat[0])
    feat = hog3(full_path)
    print len(feat), len(feat[0])
    histo = hog_histo(full_path)
    print histo 

if __name__ == '__main__':
    test()

