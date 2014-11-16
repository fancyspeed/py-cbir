Demo of Content Based Image Retrieval, implemented by Python and Tornado.

## Image descriptors

* perceptual hash, otsu hash
* gray/rgb/yuv/hsv histograms
* GIST
* HoG and LSH (built by kmeans clustering)
* SIFT and LSH (built by kmeans clustering)
* Dense SIFT

## Distance functions

* hamming distance (L0)
* norm0 distance (L0)
* abs distance (L1)
* eculidean distance (L2)

## Simple re-ranking

* blending: mix results
* ensembling: weighted sum

