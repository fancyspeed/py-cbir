from setuptools import setup
from setuptools.extension import Extension
#from Cython.Distutils import build_ext
import sys, os
import numpy as np 

version = file('VERSION.txt').read().strip()

setup(name='pyleargist',
      version=version,
      description="GIST Image descriptor for scene recognition",
      long_description=file('README.txt').read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords=('image-processing computer-vision scene-recognition'),
      author='Olivier Grisel',
      author_email='olivier.grisel@ensta.org',
      url='http://www.bitbucket.org/ogrisel/pyleargist/src/tip/',
      license='PSL',
      package_dir={'': 'src'},
      #cmdclass = {"build_ext": build_ext},
      ext_modules=[
          Extension(
              'leargist', [
                  'lear_gist/standalone_image.c',
                  'lear_gist/gist.c',
                  'src/leargist.pyx',
              ],
              libraries=['m', 'fftw3f'],
              include_dirs=[np.get_include(), 'lear_gist',],
              extra_compile_args=['-DUSE_GIST', '-DSTANDALONE_GIST'],
          ),
      ],
      )
