""" setup Gap-ML
Copyright, 2018(c), Andrew Ferlitsch
Autor: David Molina @virtualdvid
"""

from setuptools import setup, find_packages

#setup components
with open('README.md', 'r', encoding="utf-8") as f:
    long_description = f.read()

install_requires=[
    'beautifulsoup4==4.6.3',
    'numpy==1.14.5',
    'h5py==2.8.0',
    'imutils==0.5.1',
    'Unidecode==1.0.22',
    'nltk==3.3',
    'pandas==0.23.4',
    'requests==2.19.1',
    'opencv-python==3.4.3.18',
    'Pillow==5.2.0',
    'matplotlib==2.2.3']

tests_require=[
    'pytest',
    'pytest-cov']

package_data={'gapml':['tools/*', 'train/*']}

project_urls={"Documentation": "https://andrewferlitsch.github.io/Gap/",
              "Source Code": "https://github.com/andrewferlitsch/Gap"}

#https://pypi.org/pypi?%3Aaction=list_classifiers
classifiers=[
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: Apache Software License',
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
    name='gapml',
    version='0.9.3',
    description='NLP and CV Data Engineering Framework',
    author='Andrew Ferlitsch',
    author_email='aferlitsch@gmail.com',
    license='Apache 2.0',
    url='https://github.com/andrewferlitsch/Gap',
    project_urls=project_urls,
    long_description=long_description,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    tests_require=tests_require,
    package_data=package_data,
    classifiers=classifiers
)
