Demo of Content Based Image Retrieval, implemented by Python and Tornado.

## Image descriptors

* perceptual hash
* Otsu's method
* gray/RGB/YUV/HSV histograms
* GIST
* HoG and LSH (built by Kmeans clustering)
* SIFT and LSH (built by Kmeans clustering)
* Dense SIFT

## Distance functions

* Hamming distance, or norm0 distance (L0)
* abs distance (L1)
* Eculidean distance (L2)

## Simple re-ranking

* blending: mix results
* ensembling: weighted sum

## Code structure

* util/:  feature descriptors, feature and LSH preparation
* app/:  http server, matching and retrieval
* templates/:  html templates
* static/:  datasets, js, css
* conf/:  log.conf, and for feature data
* logs/:  for log data
* settings.py:  http port, common setting 
* urls.py:  server url path

## Dependencies

* Tornado
* Image
* numpy, scipy

## Run (Linux or Mac)

* `cd util/pyleargist-2.0.5/lear_gist/ && make && cp compute_gist ../../ && cd -`
* `cd util && python prepare.py && cd -`
* `python main.py`
* access http://localhost:19999/cbir

## How to change dataset

* add a new image folder in static/dataset/
* in util/prepare.py, change dataset to the folder name, like `dataset = 'ferrari'` 
* run as previous section 

## Author

Any question, please contact:  Zuotao Liu(zuotaoliu@126.com)

