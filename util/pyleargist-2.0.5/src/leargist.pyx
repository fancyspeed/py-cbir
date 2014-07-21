from libc.stdlib cimport free

from cpython cimport PyObject, Py_INCREF
import cython 

cimport leargist
import numpy as np 
cimport numpy as np
np.import_array()

cdef extern from "stdlib.h" nogil:
    void *memmove(void *str1, void *str2, size_t n)
    
cdef extern from "standalone_image.h":
    ctypedef struct color_image_t:    
        int width
        int height
        float *c1		# R 
        float *c2		# G
        float *c3		# B  
    cdef color_image_t* color_image_new(int width, int height)
    cdef void color_image_delete(color_image_t *image)

cdef extern from "gist.h":
    cdef float* color_gist_scaletab(color_image_t* src, int nblocks, int n_scale, int* n_orientations)
    cdef void free_desc(float *d)

def color_gist(im, nblocks=4, orientations=(8, 8, 4)):
     """Compute the GIST descriptor of an RGB image"""
     scales = len(orientations)
     orientations = np.array(orientations, dtype=np.int32)

     # check minimum image size
     if im.size[0] < 8 or im.size[1] < 8:
          raise ValueError(
               "image size should at least be (8, 8), got %r" % (im.size,))
         
     # ensure the image is encoded in RGB
     im = im.convert(mode='RGB')
         
     # build the lear_gist color image C datastructure
     arr = np.fromstring(im.tostring(), np.uint8)
     arr.shape = list(im.size) + [3]
     arr = arr.transpose(2, 0, 1)
     arr = np.ascontiguousarray(arr, dtype=np.float32)

     width, height = im.size
     cdef leargist.color_image_t* _c_color_image_t = leargist.color_image_new(width, height)
      
      
     size = width * height * cython.sizeof(cython.float) 
     memmove(_c_color_image_t.c1, np.PyArray_DATA(arr[0]), size  )
     memmove(_c_color_image_t.c2, np.PyArray_DATA(arr[1]), size  )
     memmove(_c_color_image_t.c3, np.PyArray_DATA(arr[2]), size  )

     cdef int nb = nblocks
     cdef int s = scales
     cdef int* no = <int*>np.PyArray_DATA(orientations)
     array = leargist.color_gist_scaletab(_c_color_image_t, nb, s, no)
     leargist.color_image_delete(_c_color_image_t)
                   
     cdef np.npy_intp dim = <np.npy_intp> nblocks * nblocks * orientations.sum() * 3
     cdef np.ndarray g = np.PyArray_SimpleNewFromData(1, &dim, np.NPY_FLOAT,
                                                      <void *> array)
     r = g.copy()
     free(<void*>array)
     return r
