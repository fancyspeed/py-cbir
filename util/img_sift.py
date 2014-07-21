import os
import sys
import numpy as np
from scipy import misc
from dsift import DsiftExtractor, SingleSiftExtractor
from kmeans import kmeans, kmeans_classify, load_centers
from lsh import LSH_sift

#gridSpacing: the spacing for sampling dense descriptors
#patchSize: the size for each sift patch
#nrml_thres: low contrast normalization threshold
#sigma_edge: the standard deviation for the gaussian smoothing the standard deviation for the gaussian smoothing
#sift_thres: sift thresholding (0.2 works well based on Lowe's SIFT paper
extractor = DsiftExtractor(12, 24, 1, 0.8, 0.1)
extractor2 = SingleSiftExtractor(24, 1, 0.8, 0.2)

cur_path = os.path.abspath(os.path.dirname(__file__))
center_path = os.path.join(cur_path, '../conf/sift_kmeans.txt')

centers = None

def sift(im):
    if not isinstance(im, np.ndarray):
        im = misc.imread(im)
    F, P = extractor.process_image(im)
    return F

def sift2(im):
    if not isinstance(im, np.ndarray):
        im = misc.imread(im)
    F = extractor2.process_image(im)
    F2 = []
    for f in F:
        F2.append(list(f))
    return F2

def sift_lsh_list(im):
    feat_list = sift2(im)
    F = []
    for feat in feat_list:
        lsh = LSH_sift(feat)
        F.append(lsh)
    return F

def sift_histo(im, p_centers=center_path):
    global centers
    if centers == None:
        centers = load_centers(p_centers)
    F = sift2(im)
    histo = {}
    for feat in F:
        c = kmeans_classify(centers, feat)
        histo[c] = histo.get(c, 0) + 1
    return [histo.get(c, 0) for c in range(len(centers))]

def test():
    full_path = '../../dataset/lena.png'
    feat = sift(full_path)
    print len(feat), len(feat[0])
    feat = sift2(full_path)
    print len(feat), len(feat[0])
    histo = sift_histo(full_path)
    print histo

if __name__ == '__main__':
    test()
