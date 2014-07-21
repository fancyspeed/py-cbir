import os
import math
import random
import copy
from scipy import misc
from img_hash import EXTS
from img_hog import hog2, hog_histo 
from img_sift import sift2
from kmeans import kmeans, kmeans_classify, load_centers

class Prepare(object):
    def __init__(self):
        self.centers = []
    
    def prepare(self, set_name, func, p_out):
        f_out = open(p_out, 'w')
        relative_path = '../static/dataset/%s' % set_name
        idx = 0
        for f in os.listdir(relative_path):
            print 'processing %d...' % idx
            idx += 1
            full_path = relative_path + '/' + f
            postfix = f.split('.')[-1]
            if postfix in EXTS:
                try:
                    F = func(full_path)
                    for feat in F:
                        f_out.write('static/dataset/%s/%s\t%s\n' % (set_name, f, repr(list(feat))))
                except Exception, e:
                    print 'Exception:', repr(e)
                    print 'img path:', full_path
        f_out.close()


if __name__ == '__main__':
    prep = Prepare()
    dataset = 'infochimps'
    prep.prepare(dataset, hog2, '../conf/hog_feat2.txt')
    #kmeans('../conf/hog_feat.txt', '../conf/hog_kmeans.txt', nclass=100, max_iter=20, percent=0.5)

    #prep.prepare(dataset, sift2, '../conf/sift_feat.txt')
    #kmeans('../conf/sift_feat.txt', '../conf/sift_kmeans.txt', nclass=100, max_iter=20, percent=0.5)
        
