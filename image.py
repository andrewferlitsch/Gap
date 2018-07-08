-+6.,"""
Image Data Processing
Copyright 2018(c), Andrew Ferlitsch
"""

import os
import threading
import time
import copy

# Import numpy for the high performance in-memory matrix/array storage and operations.
import numpy as np

# Import h5py for the HD5 filesystem high performance file storage of big data.
import h5py

# Import PIL.Image for Python image manipulation library. 
import PIL
from PIL import Image

class Image(object):
    """ Base (super) Class for Classifying an Image """
    
    _debug = False
    
    def __init__(self, image=None, label=0, dir='./', ehandler=None, thumbnail=(32,32), config=None):
        """ """
        self._image     = image     # image path
        self._name      = None      # name of image (no path or suffix)
        self._size      = 0         # byte size of the image on disk
        self._type      = None      # image type of the image
        self._dir       = None      # image storage
        self._shape     = None      # shape of the image
        self._ehandler  = ehandler  # event handler for asynchronous processing 
        self._thumbnail = thumbnail # thumbnail size
        self._label     = label     # image label
        self._grayscale = False     # convert to grayscale
        self._normalize = False     # normalize the image
        self._flatten   = False     # flatten the image
        self._resize    = None      # resize the image
        self._hd5       = True      # store processed image data to hd5 filesystem
        self._imgdata   = None      # processed image data in memory
        self._time      = 0          # elapse time to do processing
        
        if self._debug: print(config)
        
        # value must be a string
        if image is not None and isinstance(image, str) == False:
            raise TypeError("String expected for image path")
        
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError("String expected for image storage path")
            if dir.endswith("/") == False:
                    dir += "/"  
            self._dir = dir
        elif dir == None:
            self._dir = "./"
        
        # value must be a string
        if label is None or isinstance(label, int) == False:
            raise TypeError("Integer expected for image label")
            
        if config is not None and isinstance(config, list) == False:
            raise TypeError("List expected for config settings")
            
        if thumbnail is not None:
            if isinstance(thumbnail, tuple) == False:
                raise TypeError("Tuple expected for thumbnail")
            if len(thumbnail) != 2 or not int(thumbnail[0]) or not int(thumbnail[1]):
                raise TypeError("Tuple(height, width) expected for thumbnail")
        
        if config is not None:
            for setting in config:
                if isinstance(setting, str) == False:
                     raise TypeError("String expected for each config setting")
                if setting in ['gray', 'grayscale']:
                    self._grayscale = True
                elif setting in ['normal', 'normalize']:
                    self._normalize = True
                elif setting in ['flat', 'flatten']:
                    self._flatten = True
                elif setting in ['nostore']:
                    self._hd5 = False
                elif setting.startswith('resize='):
                    toks = setting.split('=')
                    if len(toks) != 2:
                        raise AttributeError("Resize is wrong format")
                    vals = toks[1].split(',')
                    if len(vals) != 2:
                        raise AttributeError("Resize is wrong format")
                    if vals[0][0] == '(':
                        vals[0] = vals[0][1:]
                    if vals[1][-1] == ')':
                        vals[1] = vals[1][:-1]
                    if not vals[0].isdigit() or not vals[1].isdigit():
                        raise AttributeError("Resize values must be an integer")
                    self._resize = ( int(vals[1]), int(vals[0]) )
                else:
                    raise AttributeError("Setting is not recognized: " + setting)
        
        if self._image is not None:
            self._exist()
            # Process document synchronously
            if ehandler is None:
                self._collate(self._dir)
            # Process document asynchronously
            else:
                t = threading.Thread(target=self._async, args=(self._dir, ))
                t.start()   
                
    def _async(self, dir):
        """ Asynchronous processing of the document """
        self._collate(dir)
        # signal user defined event handler when processing is done
        self._ehandler(self)
                
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
        
        if self._type not in [ 'png', 'jpg', 'bmp', 'tif', 'tiff', 'gif']:
            raise TypeError("Not an image file")
        
        # Get the size of the image
        self._size = os.path.getsize(self._image)
        
        # Size sanity check
        if self._size == 0:
            raise IOError("The image is an empty file")
            
    def _collate(self, dir='./'):
        """ Process the image """   
        
        start = time.time()
        
        # If directory does not exist, create it
        if dir != "./" and os.path.isdir(dir) == False:
            os.mkdir(dir)
        
        # Read in the image data
        pixels = PIL.Image.open(self._image)
        
        # Store the image
        pixels.save(dir + "/" + self._name + "." + self._type )
        
        # Store the thumbnail
        if self._thumbnail:
            try:
                thumb = copy.deepcopy(pixels)
                thumb.thumbnail( self._thumbnail )
                thumb.save(dir + "/" + self._name + "." + "thumbnail" + "." + self._type )
            except: pass
            
        if self._resize:
            pixels = pixels.resize(self._resize, resample=PIL.Image.LANCZOS)
        
        # Convert to numpy array
        image = np.asarray(pixels)
        
        # Get the shape of the array
        self._shape = image.shape
        
        # Grayscale image
        if self._shape[2] == 1:
            # Extend to three channels, replicating the single channel
            if self._grayscale == False:
                pixels = pixels.convert('RGB')
                image = np.asarray(pixels)
        # RGB image
        elif self._shape[2] == 3:
            if self._grayscale == True:
                # convert to grayscale
                pixels = pixels.convert('L')
                image = np.asarray(pixels)
        # RGBA image (RGB + alpha channel)
        elif self._shape[2] == 4:
            if self._grayscale == False:
                # Remove Alpha Channel from Image
                pixels = pixels.convert('RGB')
                image = np.asarray(pixels)
            else:
                # convert to grayscale
                pixels = pixels.convert('L')
                image = np.asarray(pixels)
            
        # Normalize the image (convert pixel values from int range 0 .. 255 to float range 0 .. 1)
        if self._normalize == True:
            image = image / 255
            
        # Flatten the image into a 1D vector
        if self._flatten == True:
            image = image.flatten()
        
        # Get the shape of the array
        self._shape = image.shape
            
        self._imgdata = image
        
        if self._hd5:
            self._store() 
            
        # Total time to do collation
        self._time = time.time() - start
        
    def _store(self):
        """ Store the processed image data in a HD5 file """
        
        if self._debug: print("STORE")
            
        # Write the image to disk as HD5 file
        with h5py.File(self._dir + "/" + self._name + '.h5', 'w') as hf:
            hf.create_dataset("images",  data=[self._imgdata])
            hf.create_dataset("labels",  data=[self._label])
            
    def load(self, image, dir='./'):
        """ Load an image from storage """
        # value must be a string
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError("String expected for image storage path")
            if dir.endswith("/") == False:
                    dir += "/"  
            self._dir = dir
        self._dir = dir 
        
        # value must be a string
        if image is not None and isinstance(image, str) == False:
            raise TypeError("String expected for image path")
        self._image = image
        
        basename = os.path.splitext(os.path.basename(self._image))
        self._name = basename[0]
        self._type = basename[1][1:].lower()
            
        # Read the image from disk as HD5 file
        with h5py.File(self._dir + "/" + self._name + '.h5', 'r') as hf:
            X =  hf['images'][:]
            Y =  hf['labels'][:]
            
        self._imgdata = X[0]
        self._label   = Y[0]
        self._shape   = self._imgdata.shape       
        
        # Get the size of the image
        self._size = os.path.getsize(image)
       
    @property
    def image(self):
        """ Getter for the image name (path) """
        return self._image
        
    @image.setter
    def image(self, image):
        """ Setter for the image name (path) 
       image - path to the image
        """
        self._image = image 
        self._exist()
        self._collate(self._dir)

    @property
    def name(self):
        """ Getter for the image name (path) """
        return self._name

    @property
    def type(self):
        """ Getter for the image type (suffix) """
        return self._type

    @property
    def shape(self):
        """ Getter for the image shape (height, width [,planes]) """
        return self._shape
        
    @property 
    def data(self):
        """ Getter for the processed image data """
        return self._imgdata
        
    @property
    def dir(self):
        """ Getter for the image directory """
        return self._dir
        
    @dir.setter
    def dir(self, dir):
        """ Setter for image directory """
        # value must be a string
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError("String expected for image storage path")
            if dir.endswith("/") == False:
                    dir += "/"  
            self._dir = dir
        self._dir = dir 
        
    @property
    def classification(self):
        """ Getter for image label (classification) """
        return self._label
        
    @classification.setter
    def classification(self, label):
        """ Setter for image label (classification) """
        self._label = label
             
    @property
    def size(self):
        """ Return the byte size of the image """
        return self._size    
        
    @property
    def time(self):
        """ Return the elapse time to do collation """
        return self._time

    @property
    def thumbnail(self):
        """ Getter for the thumbnail path """
        return self._dir + "/" + self._name + "." + "thumbnail" + "." + self._type    
        
    def __str__(self):
        """ Override the str() operator - return the document classification """
        return str(self._class)
        
 
class Images(object):
    """ Base (super) for classifying a group of images """
    def __init__(self, images=None, labels=None, dir='./', ehandler=None, config=None):
        self._images   = images
        self._dir      = dir
        self._labels   = labels
        self._ehandler = ehandler
        self._data     = None
        
        if images is None:
            return
        
        if isinstance(images, list) is False:
            raise TypeError("List expected for image paths")
        else:
            for ele in images:
                if not isinstance(ele, str):
                    raise TypeError("String expected for image paths")
        
        if isinstance(labels, list) is False:
            raise TypeError("List expected for image labels")
        else:
            for ele in labels:
                if not isinstance(ele, int):
                    raise TypeError("Integer expected for image labels")
            
        if len(images) != len(labels):
            raise IndexError("Number of images and labels do not match")
            
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError("String expected for image storage path")
            if dir.endswith("/") == False:
                    dir += "/"  
        self._dir = dir 
  
        if config is not None and isinstance(config, list) == False:
            raise TypeError("List expected for config settings")
        
        if config is None:
            config = []
        config.append("nostore")
            
        # Process each image
        self._data = []
        for ix in range(len(images)):
            self._data.append( Image(images[ix], dir=self._dir, label=labels[ix], config=config) )
            
        # Store the images as a batch in an HD5 filesystem
        imgdata = []
        clsdata = []
        for img in self._data:
            imgdata.append( img.data )
            clsdata.append( img.classification )
            
        # Write the images and labels to disk as HD5 file
        with h5py.File(self._dir + "batch." + self._data[0].name + '.h5', 'w') as hf:
            hf.create_dataset("images",  data=imgdata)
            hf.create_dataset("labels",  data=clsdata)
            
    @property
    def dir(self):
        """ Getter for the image directory """
        return self._dir
        
    @dir.setter
    def dir(self, dir):
        """ Setter for image directory """
        # value must be a string
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError("String expected for image storage path")
            if dir.endswith("/") == False:
                    dir += "/"  
            self._dir = dir
        self._dir = dir 
        
    @property
    def classification(self):
        """ Getter for image labels (classification) """
        return self._labels
        
    @classification.setter
    def classification(self, labels):
        """ Setter for image labels (classification) """
        self._labels = labels
        
    @property
    def images(self):
        """ Getter for the list of processed images """
        return self._data
        
    def load(self):
        """ TBD """
        pass
        
    def __len__(self):
        """ Override the len() operator - return the number of images """
        return len(self._data)
        
    def __getitem__(self, ix):
        """ Override the index operator - return the image at the corresponding index """
        if ix > len(self):
            raise IndexError("Index out of range for Images")
        return self._data[ ix ]
            
        