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

## Code structure

* util/: feature descriptors, feature and lsh preparation
* app/: http server, matching and retrieval
* templates/: html templates
* static/: datasets, js, css
* conf: log.conf, and for feature data
* logs: for log data
* settings.py: http port, common setting 
* urls.py: url path

## Dependency

* tornado
* Image
* numpy, scipy

## Run (Linux or Mac)

* `cd util/pyleargist-2.0.5/lear_gist/ && make && cp compute_gist ../../ && cd -`
* `cd util && python prepare.py && cd -`
* `python main.py`
* access http://localhost:19999/cbir
