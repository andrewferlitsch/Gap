"""
Image Data Processing
Copyright 2018(c), Andrew Ferlitsch
"""

import os
import threading
import time
import copy
import random
import requests
import imutils

# Import numpy for the high performance in-memory matrix/array storage and operations.
import numpy as np

# Import h5py for the HD5 filesystem high performance file storage of big data.
import h5py

# Performance Testing note:
#   cv2 loaded grayscale images 25% faster than PIL, and 10% faster for color images

# Import cv2 for Python image manipulation library. 
import cv2

# Import pillow for Python image manipulation for GIF
from PIL import Image as PILImage

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
            # Create Directory if it does not exist  
            if not os.path.isdir(dir):
               os.mkdir(dir)
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
            
        # File is at a remote (Internet) location
        if self._image.startswith("http"):
            pass
        # Check that image exists
        elif os.path.isfile(self._image) == False:
            raise FileNotFoundError(self._image)
        
        # Get the file name and file type of the image without the extension 
        basename = os.path.splitext(os.path.basename(self._image))
        self._name = basename[0]
        self._type = basename[1][1:].lower()
        
        if self._type not in [ 'png', 'jpg', 'bmp', 'tif', 'tiff', 'gif']:
            raise TypeError("Not an image file:", self._image)
        
        # Get the size of the image 
        if not self._image.startswith("http"):
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
            
        if self._image.startswith("http"):
            try:
                response = requests.get(self._image, timeout=10)
            except: return None
            
            # Read in the image data
            data = np.fromstring(response.content, np.uint8)
            self._size = len(data)
            if self._grayscale:
                image = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
            # Load RGB image (dropping any alpha channel)
            else:
                image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        else:
            # GIF files
            if self._image.endswith("gif"):
                image = PILImage.open(self._image)
                if self._grayscale:
                    image = image.convert('L')
                else:
                    image = image.convert('RGB')
                image = np.array(image)
            # Read in the image data
            elif self._grayscale:
                image = cv2.imread(self._image, cv2.IMREAD_GRAYSCALE)
            # Load RGB image (dropping any alpha channel)
            else:
                image = cv2.imread(self._image, cv2.IMREAD_COLOR)
            
        # if bad image, skip
        if np.any(image == None):
            return None
            
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
            imgset.attrs['type']  = self._type
            hf.create_dataset("raw", data=[self._raw])
            try:
                hf.create_dataset("thumb", data=[self._thumb])
            except: pass
            
    def rotate(self, degree):
        """ rotate the image """
        if not isinstance(degree, int):
            raise ValueError("Degree must be an integer")
            
        if degree <= -360 or degree >= 360:
            raise ValueError("Degree must be between -360 and 360")
            
        # rotate the image
        rotated = imutils.rotate_bound(self._imgdata, degree)
        
        # resize back to expected dimensions
        if degree not in [ 0, 90, 180, 270, -90, -180, -270 ]:
            # resize takes only height x width
            shape = (self._imgdata.shape[0], self._imgdata.shape[1])
            rotated = cv2.resize(rotated, shape, interpolation=cv2.INTER_AREA)
        return rotated
        
    def edge(self):
        """ """
        gray = cv2.GaussianBlur(self._imgdata, (3, 3), 0)
        edged = cv2.Canny(gray, 20, 100)
        return edged
            
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
            imgset = hf['images']
            self._imgdata =  hf['images'][0]
            self._label   =  hf['labels'][0]
            self._raw     =  hf['raw'][0]
            try:
                self._thumb =  hf['thumb'][0]
            except: pass  
            self._type  = imgset.attrs["type"]  
            self._size  = imgset.attrs["size"]
        self._shape = self._imgdata.shape  
      
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
    def label(self):
        """ Getter for image label (classification) """
        return self._label
        
    @label.setter
    def label(self, label):
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
        return str(self._label)
        
class Images(object):
    """ Base (super) for classifying a group of images """
    def __init__(self, images=None, labels=None, dir='./', name=None, ehandler=None, config=None):
        self._images   = images     # collection of images to process
        self._dir      = dir        # storage directory for processed images
        self._labels   = labels     # labels corresponding to collection of images
        self._ehandler = ehandler   # asynchronous processing event handler
        self._data     = None       # list of image objects
        self._name     = name       # name of collection file
        self._config   = config     # configuration settings
        self._time     = time       # time to process the images
        self._split    = 0.8        # percentage of split between train / test
        self._seed     = 0          # seed for random shuffle of data
        self._train    = None       # indexes for training set
        self._test     = None       # indexes for test set
        self._trainsz  = 0          # size of training set
        self._testsz   = 0          # size of test set
        self._minisz   = 1          # mini batch size
        self._next     = 0          # next item in training set
        self._augment  = False      # image augmentation
        self._toggle   = True       # toggle for image augmentation
        
        if images is None:
            return
        
        if isinstance(images, list) is False:
            if isinstance(images, str) is False and not os.path.isdir(images):
                raise TypeError("List or Directory expected for image paths")
            # parameter is a directory, convert to list of images in the directory
            self._images = [images + '/' + image for image in os.listdir(images)]
        else:
            for ele in images:
                if not isinstance(ele, str):
                    raise TypeError("String expected for image paths")
        
        # if labels is a single value, then all the images share the same label
        if isinstance(labels, int):
            self._labels = [ labels for _ in range(len(self._images)) ]
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
        
        if name is not None:
            if isinstance(name, str) == False:
                raise TypeError("String expected for collection name")
  
        if config is not None and isinstance(config, list) == False:
            raise TypeError("List expected for config settings")
        
        if self._config is None:
            self._config = []
        # Tell downstream Image objects not to separately store the data
        self._config.append("nostore")
        
        # Process collection synchronously
        if ehandler is None:
            self._process()
        else:
            # Process collection asynchronously
            t = threading.Thread(target=self._async, args=())
            t.start()
 
    def _async(self):
        """ Asynchronous processing of the collection """
        self._process()
        # signal user defined event handler when processing is done
        self._ehandler(self)
            
            
    def _process(self):
        """ Process a collection of images """
       
        start = time.time()
 
        # Process each image
        self._data = []
        for ix in range(len(self._images)):
            # directory of files
            if os.path.isdir(self._images[ix]):
                for image in [ self._images[ix] + '/' + file for file in os.listdir(self._images[ix])]:
                    self._data.append( Image(image, dir=self._dir, label=self._labels[ix], config=self._config) )
            # single file
            else:
                image = Image(self._images[ix], dir=self._dir, label=self._labels[ix], config=self._config)
                self._data.append( image )
            
        # Store the images as a collection in an HD5 filesystem
        imgdata = []
        clsdata = []
        rawdata = []
        sizdata = []
        thmdata = []
        names   = []
        types   = []
        paths   = []
        for img in self._data:
            imgdata.append( img.data )
            clsdata.append( img.label )
            rawdata.append( img.raw )
            sizdata.append( img.size )
            #thmdata.append( img.thumb )
            names.append( bytes(img.name, 'utf-8') )
            types.append( bytes(img.type, 'utf-8') )
            paths.append( bytes(img.image, 'utf-8') )
            
        # if no collection name specified, use root of first test file.
        if self._name is None:
            self._name = "collection." + self._data[0].name
            
        # Write the images and labels to disk as HD5 file
        with h5py.File(self._dir + self._name + '.h5', 'w') as hf:
            # needed to store raw data of varying lengths
            #dt = h5py.special_dtype(vlen=np.dtype('uint8'))
            
            hf.create_dataset("images",  data=imgdata)
            hf.create_dataset("labels",  data=clsdata)
            hf.create_dataset("raw",     data=rawdata)
            #hf.create_dataset("thumb",   data=thmdata)
            hf.create_dataset("size",    data=sizdata)
            hf.attrs.create("names", names)
            hf.attrs.create("types", types)
            try:
                hf.attrs.create("paths", paths)
            except Exception as e: print(e)

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
    def label(self):
        """ Getter for image labels (classification) """
        return self._labels
        
    @label.setter
    def label(self, labels):
        """ Setter for image labels (classification) """
        self._labels = labels
        
    @property
    def images(self):
        """ Getter for the list of processed images """
        return self._data
        
    @property
    def name(self):
        """ Getter for the name of the collection """
        return self._name
        
    @property
    def time(self):
        """ Getter for the processing time """
        return self._time
        
    def load(self, name, dir=None):
        """ Load a Collection of Images """
        if name is None:
            raise ValueError("Name parameter cannot be None")
        if not isinstance(name, str):
            raise TypeError("String expected for collection name")
        self._name = name
        
        if dir is not None:
            self.dir = dir
            
        if self._dir is None:
            self._dir = "./"
        
        # Read the images and labels from disk as HD5 file
        with h5py.File(self._dir + self._name + '.h5', 'r') as hf:
            self._data = []
            length = len(hf["images"])
            for i in range(length):
                image = Image()
                image._imgdata = hf["images"][i]
                image._raw = hf["raw"][i]
                image._size = hf["size"][i]
                image._label = hf["labels"][i]
                #image._thumb = hf["thumb"][i]
                image._name  = hf.attrs["names"][i].decode()
                image._type  = hf.attrs["types"][i].decode()
                image._image = hf.attrs["paths"][i].decode()
                image._shape = image._imgdata.shape
                image._dir   = self._dir
                self._data.append( image )
            self._labels = hf["labels"][:]
        
    @property
    def split(self):
        """ Getter for return a split training set """
        
        # Training set not already split, so split it
        if self._train == None:
            self.split = (1 - self._split)
            
        # Construct the train and test lists
        X_train = []
        Y_train = []
        X_test  = []
        Y_test  = []
        for _ in range(0, self._trainsz):
            ix = self._train[_]
            X_train.append( self._data[ix]._imgdata )
            Y_train.append( self._data[ix]._label )
        for _ in range(0, self._testsz):
            ix = self._test[_]
            X_test.append( self._data[ix]._imgdata )
            Y_test.append( self._data[ix]._label )
        return X_train, X_test, Y_train, Y_test
        
    @split.setter
    def split(self, percent):
        """ Set the split for training/test and create a randomized index """
        
        if isinstance(percent, tuple):
            if len(percent) != 2:
                raise AttributeError("Split setter must be percent, seed")
            self._seed = percent[1]
            if not isinstance(self._seed, int):
                raise TypeError("Seed parameter must be an integer")
            percent = percent[0]
            
        if not isinstance(percent, float) and percent != 0:
            raise TypeError("Float expected for percent")
        if percent < 0 or percent >= 1:
            raise ValueError("Percent parameter must be between 0 and 1")
        self._split = (1 - percent)
        
        # create a randomized index to the images
        random.seed(self._seed)
        self._indices = random.sample([ index for index in range(len(self._data))], len(self._data))
        
        # split the indices into train and test
        split = int((1 - percent) * len(self._data))
        self._train   = self._indices[:split]
        self._test    = self._indices[split:]
        self._trainsz = len(self._train)
        self._testsz  = len(self._test)
        self._next    = 0
    
    @property
    def minibatch(self):
        """ Return a generator for the next mini batch """
        # Minibatch, return a generator
        for _ in range(self._next, min(self._next + self._minisz, self._trainsz)): 
            ix = self._train[_]
            self._next += 1 
            yield self._data[ix]._imgdata , self._data[ix]._label
            if self._augment:
                degree = random.randint(-90, 90)
                yield self._data[ix].rotate(degree), self._data[ix]._label
        
    @minibatch.setter
    def minibatch(self, batch_size):
        """ Generator for creating minibatches """
        if not isinstance(batch_size, int):
            raise TypeError("Integer expected for mini batch size")
        
        # training set was not pre-split, implicitly split it.
        if self._train == None:
            self.split = 0.8
            
        if batch_size < 2 or batch_size >= self._trainsz:
            raise ValueError("Mini batch size is out of range")
            
        self._minisz = batch_size
        
    @property
    def augment(self):
        """ Getter for image augmentation """
        return self._augment
        
    @augment.setter
    def augment(self, augment):
        """ Setter for image augmentation """
        self._augment = augment
        
    def __next__(self):
        """ Iterate through the training set (single image at a time) """

        # training set was not pre-split, implicitly split it.
        if self._train == None:
            self.split = (1 - self._split)

        # End of training set
        if self._next >= self._trainsz:
            # Reshuffle the training data for the next round
            random.shuffle(self._train)
            self._next = 0 
            return None, None
 
        ix = self._train[self._next]
        if self._augment:
            self._toggle = not self._toggle
            if not self._toggle:
                degree = random.randint(-90, 90)
                return self._data[ix].rotate(degree) , self._data[ix]._label
            
        self._next += 1
        return self._data[ix]._imgdata , self._data[ix]._label
                

    def __len__(self):
        """ Override the len() operator - return the number of images """
        if self._data is None:
            raise IndexError("Index out of range for Images")
        return len(self._data)
        
    def __getitem__(self, ix):
        """ Override the index operator - return the image at the corresponding index """
        if not isinstance(ix, int):
            raise TypeError("Index must be an integer")
        if ix > len(self):
            raise IndexError("Index out of range for Images")
        return self._data[ ix ]