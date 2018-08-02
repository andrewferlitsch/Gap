""" setup Gap-ML
Copyright, 2018(c), Andrew Ferlitsch
David Molina @virtualdvid
"""

from setuptools import setup, find_packages
from distutils.command.install import install
import os, sys
import requests

with open('README.md') as f:
  long_description = f.read()

install_requires=[
  'numpy',
  'h5py',
  'imutils',
  'unidecode',
  'nltk',
  'requests',
  'opencv-python']
		  
tests_require=[
  'pytest',
  'pytest-cov']

package_data ={'gapml': ['org-os/*', 'plan/*', 'specs/*', 'test/*', 'tools/*', 'train/*']}

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

def install_apps(app_name, app_path, url):
  app = url.split('/')[-1]
  if os.path.exists(app_path):
    print('{} already installed'.format(app_name))
  else:
    print('Download has started')
    if sys.platform.startswith('win64'):
      print('Please verify C:\\Program Files\\ is part of the path to install the app')
    else:
      print('Please verify C:\\Program Files (x86)\\ is part of the path to install the app')
    r = requests.get(url, allow_redirects=True)
    open(app, 'wb').write(r.content)
    os.system(os.path.join(os.getcwd(),app))
    os.remove(app)
    if app_path not in sys.path:
      sys.path.append(app_path)
    print('{} has been installed successful'.format(app_name))
  
def main():
  if sys.platform.startswith('win'):
    windows={'win64':{1:{'app_name':'Ghostscript',
                        'app_path':'C:\\Program Files\\gs\\gs9.23\\bin\\',
                        'url':'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs923/gs923w64.exe'},
                      2:{'app_name':'Imagemagick',
                        'app_path':'C:\\Program Files\\ImageMagick-7.0.8-Q8',
                        'url':'https://www.imagemagick.org/download/binaries/ImageMagick-7.0.8-8-Q8-x64-static.exe'},
                      3:{'app_name':'Tesseract',
                        'app_path':'C:\\Program Files\\Tesseract-OCR',
                        'url':'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.0.0-beta.1.20180608.exe'}
                     },
            'win32':{1:{'app_name':'Ghostscript',
                        'app_path':'C:\\Program Files (x86)\\gs\\gs9.23\\bin\\',
                        'url':'https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs923/gs923w32.exe'},
                    2:{'app_name':'Imagemagick',
                        'app_path':'C:\\Program Files (x86)\\ImageMagick-7.0.8-Q8',
                        'url':'https://www.imagemagick.org/download/binaries/ImageMagick-7.0.8-8-Q8-x86-static.exe'},
                    3:{'app_name':'Tesseract',
                        'app_path':'C:\\Program Files (x86)\\Tesseract-OCR',
                        'url':'https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v4.0.0-beta.1.20180608.exe'}
                    },
            'common':{1:{'app_name':'Ghostscript',
                        'url':'https://www.ghostscript.com/download/gsdnld.html'},
                      2:{'app_name':'Imagemagick',
                        'url':'https://www.imagemagick.org/script/download.php'},
                      3:{'app_name':'Tesseract',
                        'url':'https://github.com/UB-Mannheim/tesseract/wiki'}
                     }
            }

    OS=sys.platform
    for i in range(1,4):
        try:
            app_name = windows[OS][i]['app_name']
            app_path = windows[OS][i]['app_path']
            url = windows[OS][i]['url']
            install_apps(app_name, app_path, url)
        except:
            app_name = windows['common'][i]['app_name']
            url = windows['common'][i]['url']
            print('{} Download files on {}'.format(app_name, url))

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

class CustomInstall(install):
  def run(self):
    install.run(self)
    main()

setup(
  name='Gap-ML',
  version='0.9.1',
  description='NLP and CV Data Engineering Framework',
  author='Andrew Ferlitsch',
  author_email='aferlitsch@gmail.com',
  license='CC-BY-SA',
  url='https://github.com/andrewferlitsch/Gap',
  long_description=long_description,
  packages=find_packages(), #exclude=['tests', 'tests*']
  install_requires=install_requires,
  tests_require=tests_require,
  package_data=package_data,
  cmdclass={'install': CustomInstall},
  classifiers=classifiers
)