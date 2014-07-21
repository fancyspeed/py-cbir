Python Wrapper for the LEAR image descriptor implementation
===========================================================

:author: <olivier.grisel@ensta.org>

Library to compute GIST global image descriptors to be used to compare pictures
based on their content (to be used global scene recognition and categorization).

The GIST image descriptor theoritical definition can be found on A. Torralba's
page: http://people.csail.mit.edu/torralba/code/spatialenvelope/

The source code of the C implementation is included in the ``lear_gist``
subfolder. See http://lear.inrialpes.fr/software for the original project
information.

pyleargist is licensed under the GPL, the same license as the original C
project.


Install
-------

Install libfftw3 with development headers (http://www.fftw.org), python dev
headers, gcc, the Python Imaging Library (PIL) and numpy.

Build locally for testing::

  % python setup.py buid_ext -i
  % export PYTHONPATH=`pwd`/src

Build and install system wide::

  % python setup.py build
  % sudo python setup.py install


Usage
-----

Here is a sample session in  a python shell once the library is installed::

  >>> from PIL import Image
  >>> import leargist

  >>> im = Image.open('lear_gist/ar.ppm')
  >>> descriptors = leargist.color_gist(im)

  >>> descriptors.shape
  (960,)

  >>> descriptors.dtype
  dtype('float32')

  >>> descriptors[:4]
  array([ 0.05786307,  0.19255637,  0.09331483,  0.06622448], dtype=float32)


The GIST descriptors (fixed size, 960 by default) can then be used as an
euclidian space to cluster images based on their content.

This dimension can then be reduced to a 32 or 64 bits semantic hash by using
Locality Sensitive Hashing, Spectral Hashing or Stacked Denoising Autoencoders.

A sample implementation of picture semantic hashing with SDAs is showcased in
the libsgd library: http://code.oliviergrisel.name/libsgd

Changes
-------

- 1.1.0: 2010/03/25 - fix segmentation fault bug, thx to S. Campion

- 1.0.1: 2009/10/10 - added missing missing MANIFEST

- 1.0.0: 2009/10/10 - initial release

