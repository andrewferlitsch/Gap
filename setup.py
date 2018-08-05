#!/usr/bin/env python

from setuptools import setup, find_packages
import os, sys, platform

with open('README.md') as f:
  long_description = f.read()

install_requires=[
  'numpy',
  'h5py',
  'imutils',
  'unidecode',
  'nltk',
  'requests',
  'opencv-python',
  'pyaspeller']
		  
tests_require=[
  'pytest',
  'pytest-cov']

package_data ={'gapml': ['./org-os/*', './plan/*', './specs/*', './tools/*', './train/*']}

#https://pypi.org/pypi?%3Aaction=list_classifiers
classifiers=[
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Healthcare Industry',
  'Topic :: Text Processing',
  'License :: CC-BY-SA',
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
  'Programming Language :: Python :: 3.7']

setup(
  name='Gap-ML',
  version='0.9',
  description='NLP and CV Data Engineering Framework',
  author='Andrew Ferlitsch',
  author_email='aferlitsch@gmail.com',
  license='CC-BY-SA',
  url='https://github.com/andrewferlitsch/Gap',
  long_description=long_description,
  packages=find_packages(exclude=['tests', 'tests*']),
  install_requires=install_requires,
  tests_require=tests_require,
  package_data=package_data,
  classifiers=classifiers
)

import requests

def answere_verify(app, app_path):
  if os.path.exists(app_path):
    print('{} already installed'.format(app))
    answere = 'installed'
  else:
    return 'y'
    answere_ok = False
    while answere_ok == False:
      answere = input('Would you like to download and install {}? (Y/n): '.format(app))
      answere = answere[0].lower()
      if answere == 'y' or answere == 'n':
        answere_ok = True
  return answere

def install_apps(url, app_path):
  print('Download has started')
  if sys.platform.startswith('win64'):
    print('Please verify C:\\Program Files\\ is part of the path to install the app')
  else:
    print('Please verify C:\\Program Files (x86)\\ is part of the path to install the app')
  app = url.split('/')[-1]
  r = requests.get(url, allow_redirects=True)
  open(app, 'wb').write(r.content)
  os.system(os.path.join(os.getcwd(),app))
  os.remove(app)
  if app_path not in sys.path:
    sys.path.insert(0, app_path)
  return print('{} has been installed successful'.format(app))

def main():
  if sys.platform.startswith('win'):
    if platform.machine().endswith('64'):
      app_path = 'C:\\Program Files\\gs\\gs9.23\\bin\\'
      answere = answere_verify('Ghostscript', app_path)
      if answere == 'y':
        url = 'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs923/gs923w64.exe'
        install_apps(url, app_path)
      elif answere == 'installed':
        pass
      else:
        print('Download files on https://www.ghostscript.com/download/gsdnld.html')

      app_path = 'C:\\Program Files\\ImageMagick-7.0.8-Q8'
      answere = answere_verify('Magick', app_path)
      if answere == 'y':
        url = 'https://www.imagemagick.org/download/binaries/ImageMagick-7.0.8-8-Q8-x64-static.exe'
        install_apps(url, app_path)
      elif answere == 'installed':
        pass
      else:
        print('Download files on https://www.imagemagick.org/script/download.php')

      app_path = 'C:\\Program Files\\Tesseract-OCR'
      answere = answere_verify('Tesseract', app_path)
      if answere == 'y':
        url = 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe'
        install_apps(url, app_path)
      elif answere == 'installed':
        pass
      else:
        print('Download files on https://github.com/UB-Mannheim/tesseract/wiki')

    else: #win32
      app_path = 'C:\\Program Files (x86)\\gs\\gs9.23\\bin\\'
      answere = answere_verify('Ghostscript', app_path)
      if answere == 'y':
        url = 'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs923/gs923w32.exe'
        install_apps(url, app_path)
      elif answere == 'installed':
        pass
      else:
        print('Download files on https://www.ghostscript.com/download/gsdnld.html')

      app_path = 'C:\\Program Files (x86)\\ImageMagick-7.0.8-Q8'
      answere = answere_verify('Magick', app_path)
      if answere == 'y':
        url = 'https://www.imagemagick.org/download/binaries/ImageMagick-7.0.8-8-Q8-x86-static.exe'
        install_apps(url, app_path)
      elif answere == 'installed':
        pass
      else:
        print('Download files on https://www.imagemagick.org/script/download.php')

      app_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
      answere = answere_verify('Tesseract', app_path)
      if answere == 'y':
        url = 'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.0.0-beta.1.20180608.exe'
        install_apps(url, app_path)
      elif answere == 'installed':
        pass
      else:
        print('Download files on https://github.com/UB-Mannheim/tesseract/wiki')

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

if __name__=='__main__':
  main()