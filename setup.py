#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""C Extension for faster UUID generation using libuuid."""

__version_info__ = (0, 9, 0)
__version__ = ".".join(map(str, __version_info__))
__author__ = "Daniel Lundin"
__contact__ = "dln@eintr.org"
__homepage__ = "http://github.com/dln/python-libuuid/"
__docformat__ = "restructuredtext"

import codecs
import os
from glob import glob

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages, Extension
from distutils.command.sdist import sdist

extra_setup_args = {}
try:
    from Cython.Distutils import build_ext
    import Cython.Compiler.Version
    import Cython.Compiler.Main as cython_compiler
    print("building with Cython " + Cython.Compiler.Version.version)
    class Sdist(sdist):
        def __init__(self, *args, **kwargs):
            for src in glob('libuuid/*.pyx'):
                cython_compiler.compile(glob('libuuid/*.pyx'),
                                        cython_compiler.default_options)
            sdist.__init__(self, *args, **kwargs)
    extra_setup_args['cmdclass'] = {'build_ext': build_ext, 'sdist': Sdist}
    source_extension = ".pyx"
except ImportError:
    print("building without Cython")
    source_extension = ".c"


ext_modules = [
    Extension('libuuid._uuid',
              sources=['libuuid/_uuid' + source_extension],
              libraries=['uuid'])
    ]


long_description = '\n' + codecs.open('README.rst', "r", "utf-8").read()

setup(name = 'python-libuuid',
      version = __version__,
      description = __doc__,
      author = __author__,
      author_email = __contact__,
      license = 'BSD',
      url = __homepage__,
      packages = ['libuuid'],
      ext_modules = ext_modules,
      zip_safe=False,
      test_suite="nose.collector",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "Programming Language :: Cython",
                   "License :: OSI Approved :: BSD License",
                   "Intended Audience :: Developers",
                   "Topic :: Communications",
                   "Topic :: System :: Distributed Computing",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                  ],
      long_description=long_description,
    **extra_setup_args
)
