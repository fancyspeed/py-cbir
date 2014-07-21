from lsh import *

def transform(p_in, lsh_func, p_out):
    fout = open(p_out, 'w')
    for line in open(p_in):
        path, s = line.strip().split('\t')
        h0 = eval(s)
        lsh = lsh_func(h0)
        if len(lsh) >= 8:
            fout.write('%s\t%s\n' % (path, lsh))
    fout.close()

if __name__ == '__main__':
    #transform('../conf/hog_feat.txt', LSH_hog, '../conf/hog_lsh.txt')
    transform('../conf/sift_feat.txt', LSH_sift, '../conf/sift_lsh.txt')
