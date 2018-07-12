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

# Performance Testing note:
#   cv2 loaded grayscale images 25% faster than PIL, and 10% faster for color images

# Import cv2 for Python image manipulation library. 
import cv2

class Image(object):
    """ Base (super) Class for Classifying an Image """
    
    _debug = False
    
    def __init__(self, image=None, label=0, dir='./', ehandler=None, config=None):
        """ """
        self._image     = image     # image path
        self._name      = None      # name of image (no path or suffix)
        self._size      = 0         # byte size of the image on disk
        self._type      = None      # image type of the image
        self._dir       = None      # image storage
        self._shape     = None      # shape of the image
        self._ehandler  = ehandler  # event handler for asynchronous processing 
        self._thumbnail = None      # thumbnail size
        self._label     = label     # image label
        self._grayscale = False     # convert to grayscale
        self._flatten   = False     # flatten the data (into 1D vector)
        self._resize    = None      # resize the image
        self._hd5       = True      # store processed image data to hd5 filesystem
        self._imgdata   = None      # processed image data in memory
        self._raw       = None      # unprocessed image data in memory
        self._thumb     = None      # thumb image data in memory
        self._time      = 0         # elapse time to do processing
        
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
        
        if config is not None:
            for setting in config:
                if isinstance(setting, str) == False:
                     raise TypeError("String expected for each config setting")
                if setting in ['gray', 'grayscale']:
                    self._grayscale = True
                elif setting in ['flat', 'flatten']:
                    self._flatten = True
                elif setting in ['nostore']:
                    self._hd5 = False
                elif setting.startswith('resize='):
                    toks = setting.split('=')
                    if len(toks) != 2:
                        raise AttributeError("Tuple(height, width) expected for resize")
                    vals = toks[1].split(',')
                    if len(vals) != 2:
                        raise AttributeError("Tuple(height, width) expected for resize")
                    if vals[0][0] == '(':
                        vals[0] = vals[0][1:]
                    if vals[1][-1] == ')':
                        vals[1] = vals[1][:-1]
                    if not vals[0].isdigit() or not vals[1].isdigit():
                        raise AttributeError("Resize values must be an integer")
                    self._resize = ( int(vals[1]), int(vals[0]) )
                elif setting.startswith('thumb='):
                    toks = setting.split('=')
                    if len(toks) != 2:
                        raise AttributeError("Tuple(height, width) expected for thumbnail")
                    vals = toks[1].split(',')
                    if len(vals) != 2:
                        raise AttributeError("Tuple(height, width) expected for thumbnail")
                    if vals[0][0] == '(':
                        vals[0] = vals[0][1:]
                    if vals[1][-1] == ')':
                        vals[1] = vals[1][:-1]
                    if not vals[0].isdigit() or not vals[1].isdigit():
                        raise AttributeError("Thumbnail values must be an integer")
                    self._thumbnail = ( int(vals[1]), int(vals[0]) )
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
            raise TypeError("Not an image file:", self._image)
        
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
        if self._grayscale:
            image = cv2.imread(self._image, cv2.IMREAD_GRAYSCALE)
        # Load RGB image (dropping any alpha channel)
        else:
            image = cv2.imread(self._image, cv2.IMREAD_COLOR)
            
        self._raw = image   

        # Store the thumbnail
        if self._hd5 and self._thumbnail:
            try:
                self._thumb = cv2.resize(image, self._thumbnail,interpolation=cv2.INTER_AREA)
            except Exception as e: print(e)
            
        if self._resize:
            image = cv2.resize(image, self._resize)
        
        # Get the shape of the array
        self._shape = image.shape
            
        # Normalize the image (convert pixel values from int range 0 .. 255 to float range 0 .. 1)
        image = image / 255
            
        # Flatten the image into a 1D vector
        if self._flatten:
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
            imgset = hf.create_dataset("images",  data=[self._imgdata])
            labset = hf.create_dataset("labels",  data=[self._label])
            imgset.attrs['shape'] = self._shape
            imgset.attrs['name']  = self._name
            imgset.attrs['type']  = self._type
            imgset.attrs['size']  = self._size
            hf.create_dataset("raw", data=[self._raw])
            try:
                hf.create_dataset("thumb", data=[self._thumb])
            except: pass
            
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
            self._imgdata =  hf['images'][0]
            self._label   =  hf['labels'][0]
            self._raw     =  hf['raw'][0]
            try:
                self._thumb =  hf['thumb'][0]
            except: pass
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
    def thumb(self):
        """ Getter for the thumbnail data """
        return self._thumb    

    @property
    def raw(self):
        """ Getter for the raw unprocessed data """
        return self._raw    
        
    def __str__(self):
        """ Override the str() operator - return the document classification """
        return str(self._class)
        
 
class Images(object):
    """ Base (super) for classifying a group of images """
    def __init__(self, images=None, labels=None, dir='./', batch=None, ehandler=None, config=None):
        self._images   = images     # batch of images to process
        self._dir      = dir        # storage directory for processed images
        self._labels   = labels     # labels corresponding to batch of images
        self._ehandler = ehandler   # asynchronous processing event handler
        self._data     = None       # list of image objects
        self._batch    = batch      # name of batch file
        self._config   = config     # configuration settings
        self._time     = time       # time to process the images
        
        if images is None:
            return
        
        if isinstance(images, list) is False:
            raise TypeError("List expected for image paths")
        else:
            for ele in images:
                if not isinstance(ele, str):
                    raise TypeError("String expected for image paths")
        
        # if labels is a single value, then all the images share the same label
        if isinstance(labels, int):
            self._labels = [ labels for _ in range(len(images)) ]
        elif not isinstance(labels, list):
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
        
        if batch is not None:
            if isinstance(batch, str) == False:
                raise TypeError("String expected for batch name")
  
        if config is not None and isinstance(config, list) == False:
            raise TypeError("List expected for config settings")
        
        if self._config is None:
            self._config = []
        self._config.append("nostore")
        
        # Process batch synchronously
        if ehandler is None:
            self._process()
        else:
            # Process batch asynchronously
            t = threading.Thread(target=self._async, args=())
            t.start()
 
    def _async(self):
        """ Asynchronous processing of the batch """
        self._process()
        # signal user defined event handler when processing is done
        self._ehandler(self)
            
            
    def _process(self):
        """ Process a batch of images """
       
        start = time.time()
        
        # Process each image
        self._data = []
        for ix in range(len(self._images)):
            self._data.append( Image(self._images[ix], dir=self._dir, label=self._labels[ix], config=self._config) )
            
        # Store the images as a batch in an HD5 filesystem
        imgdata = []
        clsdata = []
        rawdata = []
        for img in self._data:
            imgdata.append( img.data )
            clsdata.append( img.classification )
            rawdata.append( img.raw )
            
        # if no batch name specified, use root of first test file.
        if self._batch is None:
            self._batch = "batch." + self._data[0].name
            
        # Write the images and labels to disk as HD5 file
        with h5py.File(self._dir + self._batch + '.h5', 'w') as hf:
            hf.create_dataset("images",  data=imgdata)
            hf.create_dataset("labels",  data=clsdata)
            hf.create_dataset("raw",  data=rawdata)
            
        self._time = time.time() - start
            
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
        
    @property
    def name(self):
        """ Getter for the name of the batch """
        return self._batch
        
    @property
    def time(self):
        """ Getter for the processing time """
        return self._time
        
    def load(self, batch):
        """ Load a Batch file of Images """
        if batch is None:
            raise ValueError("Batch parameter cannot be None")
        if not isinstance(batch, str):
            raise TypeError("String expected for batch name")
        self._batch = batch
        
        if self._dir is None:
            self._dir = "./"
        
        # Read the images and labels from disk as HD5 file
        with h5py.File(self._dir + self._batch + '.h5', 'r') as hf:
            self._data = []
            length = len(hf["images"])
            for i in range(length):
                image = Image()
                image._imgdata = hf["images"][i]
                image.classification = hf["labels"][i]
                self._data.append( image )
            self._labels = hf["labels"][:]

    def __len__(self):
        """ Override the len() operator - return the number of images """
        return len(self._data)
        
    def __getitem__(self, ix):
        """ Override the index operator - return the image at the corresponding index """
        if ix > len(self):
            raise IndexError("Index out of range for Images")
        return self._data[ ix ]
            
        