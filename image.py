"""
Image Data Processing
Copyright 2018(c), Andrew Ferlitsch
"""

# Import numpy for the high performance in-memory matrix/array storage and operations.
import numpy as np

# Import h5py for the HD5 filesystem high performance file storage of big data.
import h5py

# Import PIL.Image for Python image manipulation library. 
import PIL

import os

class Image(object):
    """ Base (super) Class for Classifying an Image """
    
    def __init__(self, image, dir='./', ehandler=None):
        """ """
        self._image     = image     # image path
        self._name      = None      # name of image (no path or suffix)
        self._size      = 0         # byte size of the image on disk
        self._type      = None      # image type of the image
        self._dir       = dir       # image storage
        self._ehandler  = ehandler  # event handler for asynchronous processing    
        
        # value must be a string
        if dir is not None and isinstance(dir, str) == False:
            raise TypeError("String expected for image storage path")
        
        if self._image is not None:
            self._exist()
            self._collate()
        
    def _exist(self):
        """ Check if document exists """
        if isinstance(self._image, str) == False:
            raise TypeError("String expected for image path")
    
        # Check that image exists
        if os.path.isfile(self._image) == False:
            raise FileNotFoundError(self._image)
        
        # Get the file name and file type of the image without the extension 
        basename = os.path.splitext(os.path.basename(self._image))
        self._name = basename[0]
        self._type = basename[1][1:].lower()
        
        if self._type not in [ 'png', 'jpg', 'bmp', 'tif']:
            raise TypeError("Not an image file")
        
        # Get the size of the image
        self._size = os.path.getsize(self._image)
        
        # Size sanity check
        if self._size == 0:
            raise IOError("The image is an empty file")
            
    def _collate(self):
        """ Process the image """
        pixels = PIL.Image.open(self._image)
        
            
        
        