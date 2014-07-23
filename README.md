Demo of Content Based Image Retrieval, implemented by Python and Tornado.

Image descriptors used in this project:

* perceptual hash, otsu hash
* gray/rgb/yuv/hsv histogram
* GIST
* HoG and LSH
* SIFT and LSH
* Dense SIFT

LSH is built by kmeans clustering.

Distance functions: 

* hamming distance (L0)
* norm0 distance (L0)
* abs distance (L1)
* eculidean distance (L2)

Simple re-ranking: blending and ensembling
