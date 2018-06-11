#!/usr/bin/env python
from distutils.core import setup
#from distutils.extension import Extension
#from Cython.Distutils import build_ext

import sys

for cmd in ('egg_info', 'develop'):
    if cmd in sys.argv:
        from setuptools import setup

def get_version():
    with open("morpho_analyzer/version.py", "rt") as f:
        return f.readline().split("=")[1].strip(' "\n')

setup(
    name = 'morpho_analyzer',
    version = get_version(),
    author = 'Sevastyan Rakhimov',
    author_email = 'Rakhimov.SE@gmail.com',
    url = 'https://github.com/RakhimovSE/morpho_analyzer',

    description = 'Morphological analyzer (POS tagger + inflection engine) for Russian language.',
    long_description = open('README.rst').read(),

    packages = ['morpho_analyzer', 'morpho_analyzer.vendor', 'morpho_analyzer.opencorpora_dict'],
    scripts=['bin/m_analyzer'],
    requires=['dawg_python (>= 0.5)', 'morpho_analyzer_dicts (<2.0)'],

#    cmdclass = {'build_ext': build_ext},
#    ext_modules = [Extension("morpho_analyzer.analyzer", ["morpho_analyzer/analyzer.py"])],

    classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'Natural Language :: Russian',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing :: Linguistic',
    ],
)
