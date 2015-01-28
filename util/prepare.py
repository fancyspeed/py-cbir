import os
from img_hash import EXTS, phash, otsu_hash, otsu_hash2 
from img_histo import gray_histo, rgb_histo, yuv_histo, hsv_histo
from img_gist import gist
from img_hog import hog3, hog_histo, hog_lsh_list
from lsh import LSH_hog, LSH_sift
from img_sift import sift2, sift_lsh_list, sift_histo

def prepare(setname, func, p_out):
    p_out = '../conf/%s_%s.txt' % (setname, p_out)
    with open(p_out, 'w') as f_out:
        relative_path = '../static/dataset/%s' % setname
        for root, dirs, files in os.walk(relative_path):
            for f in files:
                postfix = f.split('.')[-1]
                if postfix not in EXTS: continue
                full_path = os.path.join(root, f)
                try:
                    F = func(full_path)
                    f_out.write('%s\t%s\n' % (full_path[2:], repr(F)))
                except Exception, e:
                    print repr(e)
                    print full_path

def prepare_local(setname, f_func, h_func, p_out):
    p_out = '../conf/%s_%s.txt' % (setname, p_out)
    with open(p_out, 'w') as f_out:
        relative_path = '../static/dataset/%s' % setname
        for root, dirs, files in os.walk(relative_path):
            for f in files:
                postfix = f.split('.')[-1]
                if postfix not in EXTS: continue
                full_path = os.path.join(root, f)
                try:
                    F = f_func(full_path)
                    for f in F:
                        f = list(f)
                        h = h_func(f)
                        f_out.write('%s\t%s\t%s\n' % (full_path[2:], repr(f), repr(h)))
                except Exception, e:
                    print repr(e)
                    print full_path

def prepare_all(setname):
    prepare(dataset, phash, 'phash')
    prepare(dataset, otsu_hash, 'otsu_hash')
    prepare(dataset, otsu_hash2, 'otsu_hash2')

    prepare(dataset, gray_histo, 'grayhisto')
    prepare(dataset, rgb_histo, 'rgbhisto')
    prepare(dataset, yuv_histo, 'yuvhisto')
    prepare(dataset, hsv_histo, 'hsvhisto')

    prepare(dataset, gist, 'gist')

    prepare_local(dataset, hog3, LSH_hog, 'hog_lsh')
    prepare_local(dataset, sift2, LSH_sift, 'sift_lsh')

if __name__ == '__main__':
    #dataset = 'simpcity'
    #dataset = 'infochimps'
    dataset = 'ferrari'
    #dataset = 'mixed'
    prepare_all(dataset)

