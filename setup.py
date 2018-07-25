#!/usr/bin/env python

from setuptools import setup, find_packages
import os, sys

with open('README.md') as f:
  long_description = f.read()

install_requires=[
  'numpy',
  'h5py',
  'unidecode',
  'nltk',
  'opencv-python']
		  
tests_require=[
  'pytest',
  'pytest-cov']

data_files=[('gapml', ['org-os', 'plan', 'specs', 'tools', 'train'])]

#https://pypi.org/pypi?%3Aaction=list_classifiers
classifiers=[
  'Development Status :: 4 - Beta',
  'Intended Audience :: Healthcare Industry',
  'Topic :: Text Processing',
  'License :: CC-BY',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: MacOS',
  'Operating System :: POSIX :: Linux',
  'Programming Language :: Python :: 3',
  'Programming Language :: Python :: 3.0',
  'Programming Language :: Python :: 3.1',
  'Programming Language :: Python :: 3.2',
  'Programming Language :: Python :: 3.3',
  'Programming Language :: Python :: 3.4',
  'Programming Language :: Python :: 3.5',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7'
]

setup(
  name='Gap-ML',
  version='0.9',
  description='NLP and CV Data Engineering Framework',
  author='Andrew Ferlitsch',
  author_email='aferlitsch@gmail.com',
  license='CC-BY',
  url='https://github.com/andrewferlitsch/Gap',
  long_description=long_description,
  packages=find_packages(exclude=['tests', 'tests*']),
  install_requires=install_requires,
  tests_require=tests_require,
  #data_files=data_files,
  #classifiers=classifiers
)

if sys.platform.startswith('win'):
    pass
elif sys.platform.startswith('linux'):
    #install Ghostscript:
    os.system('sudo apt-get update && sudo apt-get install ghostscript')
    #install ImageMagick:
    os.system('sudo apt-get install imagemagick')
    #install Tesseract:
    os.system('sudo apt-get install tesseract-ocr && sudo apt-get install tesseract-ocr-eng')
elif sys.platform.startswith('darwin'):
    os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
    os.system('brew update')
    os.system('brew install ghostscript imagemagick tesseract')
