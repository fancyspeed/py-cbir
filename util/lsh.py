from numpy import array, floor

def idx_hog(p):
    p2 = [(c,v) for c, v in enumerate(p)]
    sort_list = sorted(p2, key=lambda d:d[1], reverse=True)
    p3 = ['%02d%02d' % (c, int(v*50)) for c, v in sort_list[:5] if v > 0.02]
    #p3 = ['%02d%02d' % (c, int(v*25)) for c, v in sort_list[:9] if v > 0.01]
    return ''.join(p3) 

def LSH_hog(h0):
    p_list = [h0[i*0:i*0+9] for i in range(4)]
    idx_list = [idx_hog(p) for p in p_list]
    return ''.join(idx_list)

def idx_sift(p):
    p2 = [(c,v) for c, v in enumerate(p)]
    sort_list = sorted(p2, key=lambda d:d[1], reverse=True)
    p3 = ['%02d%02d' % (c, int(v*0)) for c, v in sort_list[:4] if v > 0.02]
    return ''.join(p3)

def LSH_sift(h0):
    idx_list = idx_sift(h0)
    return ''.join(idx_list)

