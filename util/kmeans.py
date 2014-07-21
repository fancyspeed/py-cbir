import os
import math
import random
import copy
import numpy as np
from numpy import array
from img_hash import EXTS

def norm0_dist(h1, h2):
    return len(h1) - sum(array(h1)==array(h2))    

def eculidean_dist(h1, h2):
    return math.sqrt(square_eculidean_dist(h1, h2))

def square_eculidean_dist(h1, h2):
    return sum((array(h1)-array(h2))**2)

def kmeans_classify(centers, h):
    min_c, min_d = -1, -1
    for c, center in enumerate(centers):
        d = square_eculidean_dist(h, center)
        if min_c == -1 or d < min_d:
            min_c, min_d = c, d
    return min_c

def save_centers(p_out, centers):
    with open(p_out, 'w') as fout:
        for center in centers:
            fout.write('%s\n' % (repr(center)))

def load_centers(p_center):
    centers = [] 
    for line in open(p_center):
        centers.append(eval(line.strip()))
    return centers

def kmeans(p_feat, p_out, nclass=100, max_iter=100, percent=0.02, theta=0.01):
    feat_list = [] 
    for line in open(p_feat):
        if random.random() <= percent:
            arr = line.strip().split('\t')
            path, feat = arr[0], eval(arr[1])
            feat_list.append(feat)
    print 'feat_list len', len(feat_list)
    print 'feat len', len(feat_list[0]) 

    theta2 = nclass * 100. / len(feat_list)
    print 'theta2', theta2

    centers = random.sample(feat_list, nclass)
    for niter in range(max_iter): 
        print 'iter %d...' % niter
        old_centers = copy.deepcopy(centers)
        print 'old_centers finished'
        class_feats = [[] for i in range(len(centers))]
        print 'class_feats initialized'
        for feat in feat_list:
            if random.random() < theta2: 
                min_c = kmeans_classify(centers, feat)
                class_feats[min_c].append(feat)
        print 'class_feats finished'

        centers = []
        for i, feats in enumerate(class_feats):
            if feats:
                centers.append(list(np.mean(feats, 0)))
            else:
                centers.append([0]*len(feat_list[0]))
        print 'centers finished, len:', len(centers)

        save_centers(p_out, centers)
        print 'saved centers...'

        diff = 0
        for c, center in enumerate(centers):
            diff += eculidean_dist(center, old_centers[c])
        print 'diff %s', diff
        if diff < theta:
            break

def test():
    a = [[1, 2], [5,6]]
    b = [1.3, 3]
    c = kmeans_classify(a, b)
    print a, b, c


if __name__ == '__main__':
    test()
        
