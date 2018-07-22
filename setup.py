#!/usr/bin/env python

from distutils.core import setup

setup(name='Gap-ML',
      version='0.9',
      description='NLP and CV Data Engineering Framework',
      author='Andrew Ferlitsch',
      author_email='aferlitsch@gmail.com',
      license='CC-BY',
      url='',
      packages=['./'],
       install_requires=[
          'numpy',
          'h5py',
          'unidecode',
          'nltk',
      ],
     )