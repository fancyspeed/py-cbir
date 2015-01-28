import os
import sys
import random
import string
import hashlib

import tornado.web
from tornado.escape import json_encode

import Image

cur_path = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(cur_path, '../util/')))
from img_hash import EXTS, phash, otsu_hash, otsu_hash2, hamming
from img_histo import gray_histo, rgb_histo, yuv_histo, hsv_histo, abs_dist
from img_gist import gist
from kmeans import eculidean_dist, norm0_dist
from img_hog import hog2, hog3, hog_lsh_list, hog_histo
from img_sift import sift2, sift_histo
from lsh import LSH_hog, LSH_sift
from rerank import blending, ensembling

upload_prefix = './static/upload/'
SETNAME = 'ferrari'

class LocalMatcher(object):
    def __init__(self, setname):
        self.hog_index = {}
        self.load('conf/%s_hog_lsh.txt' % setname, self.hog_index)
        self.sift_index = {}
        self.load('conf/%s_sift_lsh.txt' % setname, self.sift_index)

    def load(self, pin, obj):
        for line in open(pin):
            path, f_str, code = line.strip().split('\t')
            f = eval(f_str)
            code = eval(code)
            if code not in obj:
                obj[code] = {} 
            if path not in obj[code]:
                obj[code][path] = []
            obj[code][path].append(f)

    def match(self, img_dst, obj, f_func, h_func, d_func):
        F = f_func(img_dst)
        match_dict = {}
        for f in F:
            code = h_func(f)
            if code not in obj:
                continue
            for path in obj[code]:
                match_dict[path] = match_dict.get(path, 0) + 1.
        result_list = [(k, 1-v/len(F)) for k, v in match_dict.items()]
        sort_list = sorted(result_list, key=lambda d:d[1])
        return sort_list[:5]
        

    def match2(self, img_dst, obj, f_func, h_func, d_func):
        F = f_func(img_dst)
        match_dict = {}
        for f in F:
            code = h_func(f)
            if code not in obj:
                continue
            for path in obj[code]:
                if path not in match_dict:
                    match_dict[path] = []
                min_d = -1 
                for f0 in obj[code][path]:
                    d = d_func(f, f0)
                    if min_d < 0 or d < min_d:
                        min_d = d
                match_dict[path].append(min_d)
        result_list = []
        for path in match_dict:
            d_list = sorted(match_dict[path])[:3]
            weight = sum(d_list) * 3 / (len(d_list))**2
            result_list.append((path, weight))
        sort_list = sorted(result_list, key=lambda d:d[1])
        return [(k, repr(v)) for k, v in sort_list[:5]]

    def match3(self, img_dst, obj, f_func, h_func, d_func, thres=0.3):
        F = f_func(img_dst)
        match_dict = {}
        for f in F:
            code = h_func(f)
            if code not in obj:
                continue
            for path in obj[code]:
                min_d = -1 
                for f0 in obj[code][path]:
                    d = d_func(f, f0)
                    if min_d < 0 or d < min_d:
                        min_d = d
                if min_d < thres:
                    match_dict[path] = match_dict.get(path, 0) + 1 
        sort_list = sorted(match_dict.items(), key=lambda d:d[1], reverse=True)
        return [(k, repr(v)) for k, v in sort_list[:5]]

    def search(self, dst_thum, debug=False):
        hog_list = self.match(dst_thum, self.hog_index, hog3, LSH_hog, eculidean_dist)
        #hog_list2 = self.match2(dst_thum, self.hog_index, hog3, LSH_hog, eculidean_dist)
        sift_list = self.match(dst_thum, self.sift_index, sift2, LSH_sift, eculidean_dist)
        #sift_list2 = self.match2(dst_thum, self.sift_index, sift2, LSH_sift, eculidean_dist)
        local_list = blending([(hog_list, 0.8),
                               (sift_list, 1),
                               ], 5, 2)
        local_list2 = ensembling([(hog_list, 1),
                               (sift_list, 1),
                               ], 5, 2)
        if debug:
            return [
                ('hog lsh', hog_list),
                ('sift lsh', sift_list),
                ('similar images (local similarity)', local_list),
                ('local ensembing', local_list2),
                ]
        else:
            return [
                ('similar images (local similarity)', local_list),
                ]


class GlobalMatcher(object):
    def __init__(self, setname):
        self.phash = {}
        self.load('conf/%s_phash.txt' % setname, self.phash)
        self.ohash = {}
        self.load('conf/%s_otsu_hash.txt' % setname, self.ohash)
        self.grayhisto = {}
        self.ohash2 = {}
        self.load('conf/%s_otsu_hash2.txt' % setname, self.ohash2)
        self.load('conf/%s_grayhisto.txt' % setname, self.grayhisto)
        self.rgbhisto = {}
        self.load('conf/%s_rgbhisto.txt' % setname, self.rgbhisto)
        self.yuvhisto = {}
        self.load('conf/%s_yuvhisto.txt' % setname, self.yuvhisto)
        self.hsvhisto = {}
        self.load('conf/%s_hsvhisto.txt' % setname, self.hsvhisto)
        self.gist = {}
        self.load('conf/%s_gist.txt' % setname, self.gist)

    def load(self, pin, obj):
        for line in open(pin):
            try:
                path, hcode = line.strip().split('\t')
                obj[path] = eval(hcode)
            except Exception, e:
                print repr(e)

    def match(self, img_dst, obj, f_func, d_func):
        code = f_func(img_dst)
        value_list = []
        for path in obj:
            d = d_func(obj[path], code)
            value_list.append((path, d))
        sort_list = sorted(value_list, key=lambda d:d[1])
        return sort_list[:5]

    def search(self, dst_thum, debug=False):
        phash_list = self.match(dst_thum, self.phash, phash, hamming)
        ohash_list = self.match(dst_thum, self.ohash, otsu_hash, hamming)
        ohash_list2 = self.match(dst_thum, self.ohash2, otsu_hash2, hamming)
        hash_list = blending([(phash_list, 1), 
                              (ohash_list, 1),
                              (ohash_list2, 1),
                              ], 1, 6)

        ghisto_list = self.match(dst_thum, self.grayhisto, gray_histo, abs_dist)
        rhisto_list = self.match(dst_thum, self.rgbhisto, rgb_histo, abs_dist)
        yhisto_list = self.match(dst_thum, self.yuvhisto, yuv_histo, abs_dist)
        hhisto_list = self.match(dst_thum, self.hsvhisto, hsv_histo, abs_dist)
        histo_list = blending([(ghisto_list, 4),
                               (rhisto_list, 1),
                               (yhisto_list, 1),
                               (hhisto_list, 1),
                               ], 5, 2)
        histo_list2 = ensembling([(ghisto_list, 3),
                               (rhisto_list, 1),
                               (yhisto_list, 1),
                               (hhisto_list, 1),
                               ], 5, 6)

        gist_list = self.match(dst_thum, self.gist, gist, eculidean_dist)
        texture_list = blending([(gist_list, 1),
                                 ], 5, 0.8)

        if debug:
            return [('duplicate images', hash_list), 
                ('gray', ghisto_list),
                ('rgb', rhisto_list),
                ('hsv', hhisto_list),
                ('yuv', yhisto_list),
                ('similar images (color histogram)', histo_list), 
                ('similar images (texture)', texture_list),
                ]
        else:
            return [('duplicate images', hash_list), 
                ('similar images (color histogram)', histo_list), 
                ('similar images (texture)', texture_list),
                ]


phash_alg = None
index_alg = None
def get_global_vars():
    global phash_alg
    global index_alg
    if phash_alg == None:
        phash_alg = GlobalMatcher(SETNAME)
        index_alg = LocalMatcher(SETNAME)
    return phash_alg, index_alg


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('template_cbir.html', err_msg="", imgpath="", lists=[])

    def post(self):
        err_msg = ''
        img_path = ''
        lists = []
        debug_flag = self.get_argument("debug", "")
        if debug_flag:
            debug = True
        else:
            debug = False

        if self.request.files:
            f = self.request.files['imgpath'][0]
            rawname = f['filename']
            extension = os.path.splitext(rawname)[1]
            if extension[1:] not in EXTS:
                err_msg = 'wrong file type'
                self.render('template_cbir.html', err_msg=err_msg, imgpath=img_path, lists=[])

            #dstname = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10))
            dstname = hashlib.md5(f['body']).hexdigest()
            dstname += extension
            dst_full = upload_prefix + dstname
            open(dst_full, 'w').write(f['body'])
            #img = Image.open(dst_full)
            #img.thumbnail((50, 50), resample=1)
            #dst_thum = upload_prefix + 'thum_' + dstname 
            #img.save(dst_thum)

            phash_alg, index_alg = get_global_vars()
            lists = []
            lists += phash_alg.search(dst_full, False)
            #lists += index_alg.search(dst_full, True)
        else:
            err_msg = 'No file is uploaded'
        self.render('template_cbir.html', err_msg=err_msg, imgpath=dst_full, lists=lists)

