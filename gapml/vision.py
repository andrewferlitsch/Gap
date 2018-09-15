"""
Image Data Processing
Copyright 2018(c), Andrew Ferlitsch
"""

version = '0.9.4'

import os
import io
import threading
import time
import copy
import random
import requests
import imutils
import gc

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
        self._image     = image      # image path
        self._name      = None       # name of image (no path or suffix)
        self._size      = 0          # byte size of the image on disk
        self._ressize   = 0          # byte size of the image on memory after resize
        self._type      = None       # image type of the image
        self._dir       = None       # image storage
        self._shape     = None       # shape of the image
        self._ehandler  = ehandler   # event handler for asynchronous processing 
        self._thumbnail = None       # thumbnail size
        self._label     = label      # image label
        self._grayscale = False      # convert to grayscale
        self._flatten   = False      # flatten the data (into 1D vector)
        self._resize    = None       # resize the image
        self._hd5       = True       # store processed image data to hd5 filesystem
        self._noraw     = True       # config setting for storing raw data
        self._imgdata   = None       # processed image data in memory
        self._raw       = None       # unprocessed image data in memory
        self._rawshape  = None       # raw shape of the image
        self._thumb     = None       # thumb image data in memory
        self._time      = 0          # elapse time to do processing
        self._float     = np.float32 # data type after normalization
        
        if self._debug: print(config)
        
        # value must be a string
        if image is not None and not isinstance(image, str) and not isinstance(image, np.ndarray):
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
        
        # label must be an int or a list of floats (one-hot encoded)
        if isinstance(label, int):
            pass
        # one-hot encoded
        elif isinstance(label, list) or isinstance(label, np.ndarray):
            pass
        else:
            raise TypeError("Integer or 1D vector (one-hot encoded) expected for image label")
            
        if ehandler:
            if isinstance(ehandler, tuple):
                if not callable(ehandler[0]):
                    raise TypeError("Function expected for ehandler")
            elif not callable(ehandler):
                raise TypeError("Function expected for ehandler")
            
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
                elif setting in ['raw']:
                    self._noraw = False
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
                elif setting.startswith('float'):
                    if setting == 'float16':
                        self._float = np.float16
                    elif setting == 'float32':
                        self._float = np.float32
                    elif setting == 'float64':
                        self._float = np.float64
                    else:
                        raise AttributeError("Float values must be float16, float32 or float64")
                elif setting.startswith('nlabels='):
                    pass # ignore
                else:
                    raise AttributeError("Setting is not recognized: " + setting)
        
        if self._image is not None:
            self._exist()
            # Process image synchronously
            if ehandler is None:
                self._collate(self._dir)
            # Process image asynchronously
            else:
                # no parameters
                if not isinstance(self._async, tuple):
                    t = threading.Thread(target=self._async, args=(dir, ))
                else:
                    t = threading.Thread(target=self._async, args=(dir, ehandler[1:], ))
                t.start()   
                
    def _async(self, dir):
        """ Asynchronous processing of the image """
        try:
            self._collate(dir)
        except Exception as e:
            self._ehandler(e)
            
        # signal user defined event handler when processing is done
        if isinstance(self._ehandler, tuple):
            self._ehandler[0](self, self._ehandler[1:])
        else:
            self._ehandler(self)
                
    def _exist(self):
        """ Check if image exists """
        
        # Image data was directly inputted as an argument
        if isinstance(self._image, np.ndarray):
            self._name = 'untitled'
            self._type = 'raw'
            self._size = self._image.size
            return
            
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
        
        if self._type not in ['png', 'jpg', 'jpeg', 'j2k', 'bmp', 'tif', 'tiff', 'gif']:
            raise TypeError("Not an image file:", self._image)
        
        # Get the size of the image 
        if not self._image.startswith("http"):
            self._size = os.path.getsize(self._image)
        
            # Size sanity check
            if self._size == 0:
                raise IOError("The image is an empty file")

    def _sizeof(self):
        """ Returns the byte size of the processed image """
        size = 1
        for dim in self.shape:
            size *= dim
        if self._float == np.uint8:
            size * 1
        elif self._float == np.float16:
            size * 2
        elif self._float == np.float32:
            size * 4
        elif self._float == np.float64:
            size * 8
        return size / 8

    def _collate(self, dir='./'):
        """ Process the image """   
        
        start = time.time()
        
        # If directory does not exist, create it
        if dir != "./" and os.path.isdir(dir) == False:
            os.mkdir(dir)
    
        # Image data was directly inputted
        if isinstance(self._image, np.ndarray):
            if self._grayscale:
                if not len(self._image.shape) == 2:
                    image = cv2.cvtColor(self._image, cv2.COLOR_RGB2GRAY)
                else:
                    image = self._image
            elif len(self._image.shape) == 2:
                image = cv2.cvtColor(self._image, cv2.COLOR_GRAY2RGB)
            else:
                image = self._image
        # remote image
        elif self._image.startswith("http"):
            try:
                response = requests.get(self._image, timeout=10)
            except:
                raise TimeoutError('Unable to get remote image')
            
            # Read in the image data
            data = np.fromstring(response.content, np.uint8)
            self._size = len(data)
            if self._grayscale:
                image = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
            # Load RGB image (dropping any alpha channel)
            else:
                image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        else:
            # GIF / JP2000 files
            if self._image.endswith('gif') or self._image.endswith('j2k'):
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
            raise EOFError('Not an Image')
        
        # Get the raw shape of the array
        self._rawshape = image.shape

        if self._noraw == False:
            self._raw = image   

        # Create the thumbnail
        if self._thumbnail:
            try:
                self._thumb = cv2.resize(image, self._thumbnail,interpolation=cv2.INTER_AREA)
            except Exception as e: print(e)
        
        if self._resize:
            image = cv2.resize(image, self._resize)
            #get new image size
            self._ressize = self._sizeof(image)
        
        # Get the shape of the array
        self._shape = image.shape
            
        # Get the data type of the pixel data
        if len(image.shape) == 1:
            data_type = type(image[0])
        elif len(image.shape) == 2:
            data_type = type(image[0][0])
        else:
            data_type = type(image[0][0][0])
        
        # Normalize the image (convert pixel values from int range 0 .. 255 to float range 0 .. 1)
        if data_type == np.uint8:
            if self._float == np.float16:
                image = (image / 255.0).astype(np.float16)
            elif self._float == np.float64:
                image = (image / 255.0).astype(np.float64)
            else:
                image = (image / 255.0).astype(np.float32)
        elif data_type == np.uint16:
            if self._float == np.float16:
                image = (image / 65535.0 ).astype(np.float16)
            elif self._float == np.float64:
                image = (image / 65535.0 ).astype(np.float64)
            else:
                image = (image / 65535.0 ).astype(np.float32)
        # assume pixel data is normalized
        elif data_type == np.float16 or data_type is np.float32 or data_type is np.float64:
            if self._float == np.float16:
                image = image.astype(np.float16)
            elif self._float == np.float64:
                image = image.astype(np.float64)
            else:
                image = image.astype(np.float32)
            
        # Flatten the image into a 1D vector
        if self._flatten:
            image = image.flatten()
        
        # Get the shape of the array
        self._shape = image.shape
        
        self._imgdata = image
        
        if isinstance(self._image, np.ndarray):
            self._image = "untitled"
        
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
            imgset.attrs['rawshape'] = self._rawshape
            imgset.attrs['shape'] = self._shape
            imgset.attrs['name']  = self._name
            imgset.attrs['type']  = self._type
            imgset.attrs['size']  = self._size
            imgset.attrs['ressize']  = self._ressize
            imgset.attrs['type']  = self._type
            if not self._noraw:
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
            try:
                self._raw     =  hf['raw'][0]
            except: pass
            try:
                self._thumb =  hf['thumb'][0]
            except: pass
            self._type  = imgset.attrs["type"]  
            self._size  = imgset.attrs["size"]
            self._ressize  = imgset.attrs["ressize"]
            self._rawshape = imgset.attrs["rawshape"]
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
        """ Return the byte size of the original image """
        return self._size    
        
    @property
    def ressize(self):
        """ Return the byte size of the image after resize """
        return self._ressize

    @property
    def time(self):
        """ Return the elapse time to do collation """
        return self._time

    @property
    def elapsed(self):
        """ Returns elapsed time in hh:mm:ss format to do collation """
        return time.strftime("%H:%M:%S", time.gmtime(self._time))

    @property
    def thumb(self):
        """ Getter for the thumbnail data """
        return self._thumb    

    @property
    def raw(self):
        """ Getter for the raw unprocessed data """
        return self._raw

    @property
    def rawshape(self):
        """ Getter for the image raw shape (height, width [,planes]) """
        return self._rawshape
        
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
        self._nostore  = False      # do not store into HDF5 flag
        self._rotate   = [-90, 90, 1, 1] # rotation parameters for image augmentation
        self._resize   = None       # config setting for resize
        self._noraw    = True       # config setting for not storing raw data
        self._time     = 0          # processing time
        self._fail     = 0          # how many images that failed to process
        self._nlabels  = None       # number of labels in the collection
        self._errors   = None       # list of errors reporting
        
        if images is None:
            return
        
        if isinstance(images, list):
            for ele in images:
                if isinstance(ele, str) or isinstance(ele, np.ndarray):
                    pass
                else:
                    raise TypeError("String or Raw Pixel data expected for image paths")
        elif isinstance(images, str):
            if not os.path.isdir(images):
                raise TypeError("List or Directory expected for image paths")
            # parameter is a directory, convert to list of images in the directory
            self._images = [images + '/' + image for image in os.listdir(images)]
        elif isinstance(images, np.ndarray):
            if len(images.shape) < 2:
                raise TypeError("2D or greater numpy array expected for images")
        else:
            raise TypeError("List or Directory expected for image paths")
        
        
        # if labels is a single value, then all the images share the same label
        if isinstance(labels, int):
            self._labels = [ labels for _ in range(len(self._images)) ]
        elif isinstance(labels, list):
            for ele in labels:
                if not isinstance(ele, int):
                    raise TypeError("Integer expected for image labels")
            
            if len(images) != len(labels):
                raise IndexError("Number of images and labels do not match")
        elif isinstance(labels, np.ndarray):
            if len(labels.shape) == 1:
                if type(labels[0]) not in [ np.uint8, np.uint16, np.uint32, np.int8, np.int16, np.int32 ]:
                    raise TypeError("Integer values expected for labels") 
                self._labels = [ int(label) for label in labels ]
            elif len(labels.shape) == 2:
                if type(labels[0][0]) not in [ np.float16, np.float32, np.float64]:
                    raise TypeError("Floating point values expected for one-hot encoded labels") 
                self._labels = [ label for label in labels ]
            else:
                raise TypeError("1D or 2D numpy array expected for labels")
                
            if len(images) != len(labels):
                raise IndexError("Number of images and labels do not match")
        else:
            raise TypeError("List expected for image labels")
            
        if dir is not None:
            if isinstance(dir, str) == False:
                raise TypeError("String expected for image storage path")
            if dir.endswith("/") == False:
                    dir += "/"  
        self._dir = dir 
        
        if name is not None:
            if isinstance(name, str) == False:
                raise TypeError("String expected for collection name")
            
        if ehandler:
            if isinstance(ehandler, tuple):
                if not callable(ehandler[0]):
                    raise TypeError("Function expected for ehandler")
            elif not callable(ehandler):
                raise TypeError("Function expected for ehandler")
  
        if config is not None and isinstance(config, list) == False:
            raise TypeError("List expected for config settings")
        
        if self._config is None:
            self._config = []
        else:
            for setting in config:
                if setting == 'nostore':
                    self._nostore = True
                elif setting == 'raw':
                    self._noraw = False
                elif setting.startswith("resize="):
                    param = setting.split('=')[1]
                    toks  = param.split(',')
                    if toks[0][0] == '(':
                        toks[0] = toks[0][1:]
                        toks[1] = toks[1][:-1]
                    try:
                        self._resize = ( int(toks[0]), int(toks[1]), 3)
                    except:
                        raise AttributeError("Tuple(int,int) expected for resize")
                elif setting.startswith("nlabels="):
                    param = setting.split('=')[1]
                    try:
                        self._nlabels = int(param)
                    except:
                        raise AttributeError("Integer expected for nlabels")                
                    
        # Tell downstream Image objects not to separately store the data
        if self._nostore == False:
            self._config.append("nostore")
        if self._noraw == False:
            self._config.append('raw')
        
        # Process collection synchronously
        if ehandler is None:
            self._process()
        else:
            # no parameters
            if not isinstance(self._async, tuple):
                t = threading.Thread(target=self._async, args=())
            else:
                t = threading.Thread(target=self._async, args=(ehandler[1:], ))
            t.start()   
 
    def _async(self):
        """ Asynchronous processing of the collection """
        self._process()
        # signal user defined event handler when processing is done
        if isinstance(self._ehandler, tuple):
            self._ehandler[0](self, self._ehandler[1:])
        else:
            self._ehandler(self)
            
    def _process(self):
        """ Process a collection of images """
       
        start = time.time()
 
        # Process each image
        self._data = []
        self._errors = []
        for ix in range(len(self._images)):
            # directory of files
            if isinstance(self._images[ix], str) and os.path.isdir(self._images[ix]):
                for image in [ self._images[ix] + '/' + file for file in os.listdir(self._images[ix])]:
                    try:
                        self._data.append( Image(image, dir=self._dir, label=self._labels[ix], config=self._config) )
                    except Exception as e: 
                        self._data.append(None)
                        self._fail += 1
                        error = (image, e)
                        if e not in self._errors:
                            self._errors.append( error )
            # single file
            else:
                try:
                    self._data.append( Image(self._images[ix], dir=self._dir, label=self._labels[ix], config=self._config) )
                except Exception as e:
                    self._data.append(None)
                    self._fail += 1
                    error = (self._images[ix] , e)
                    if e not in self._errors:
                        self._errors.append( error )
        
        # Store machine learning ready data
        if self._nostore is False:
            self.store()
            
        self._time = time.time() - start

    def store(self):
        """ """
        # Store the images as a collection in an HD5 filesystem
        imgdata   = []
        clsdata   = []
        rawdata   = []
        sizdata   = []
        thmdata   = []
        rawshape  = []
        ressizedt = []
        names     = []
        types     = []
        paths     = []
        for img in self._data:
            # unprocessed image
            if not img:
                pass
            else:
                imgdata.append( img.data )
                clsdata.append( img.label )
                if img.raw is not None:
                    rawdata.append( img.raw )
                rawshape.append( img.rawshape )
                sizdata.append( img.size )
                ressizedt.append( img.ressize )
                if img.thumb is not None:
                    thmdata.append( img.thumb )
                names.append( bytes(img.name, 'utf-8') )
                types.append( bytes(img.type, 'utf-8') )
                paths.append( bytes(img.image, 'utf-8') )

        # if no collection name specified, use root of first test file.
        if self._name is None:
            if self._data[0] is not None:
                self._name = "collection." + self._data[0].name
            else:
                self._name = "collection.untitled"
            
        # Write the images and labels to disk as HD5 file
        with h5py.File(self._dir + self._name + '.h5', 'w') as hf:
            try:
                hf.create_dataset("images", data=imgdata)
            except:
                for i, img in enumerate(imgdata):
                    hf.create_dataset("imgdata" + str(i), data=img)
            hf.create_dataset("labels", data=clsdata)
            # use separate datasets to handle raw images of different size/shape
            for i, img in enumerate(rawdata):
                hf.create_dataset("raw" + str(i), data=img)
            hf.create_dataset("rawshape", data=rawshape)
            if len(thmdata) > 0:
                hf.create_dataset("thumb", data=thmdata)
            hf.create_dataset("size",  data=sizdata)
            hf.create_dataset("ressize",  data=ressizedt)
            hf.create_dataset("names", data=names)
            hf.create_dataset("types", data=types)
            hf.create_dataset("paths", data=paths)
            
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
    def labels(self):
        """ Getter for image labels (classification) """
        return self._labels
        
    @labels.setter
    def labels(self, labels):
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

    @property
    def elapsed(self):
        """ Elapsed time in hh:mm:ss format for the processing time """
        return time.strftime("%H:%M:%S", time.gmtime(self._time))
        
    @property
    def fail(self):
        """ Number of images that failed processing """
        return self._fail

    @property
    def errors(self):
        """ list errors reporting """
        return self._errors
        
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
            length = len(hf["names"])
            for i in range(length):
                image = Image()
                try:
                    image._imgdata = hf["images"][i]
                except:
                    image._imgdata = hf["imgdata" + str(i)][:]
                try:
                    image._raw = hf["raw" + str(i)][:]
                except: pass
                image._rawshape = hf["rawshape"][i]
                image._size     = hf["size"][i]
                image._ressize  = hf['ressize'][i]
                image._label    = hf["labels"][i]
                try:
                    image._thumb = hf["thumb"][i]
                except: pass
                image._name  = hf["names"][i].decode()
                image._type  = hf["types"][i].decode()
                image._image = hf["paths"][i].decode()
                image._shape = image._imgdata.shape
                image._dir   = self._dir
                self._data.append( image )
            self._labels = hf["labels"][:]
            
        gc.collect()
        
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
          
        # calculate the number of labels in the training set
        if self._nlabels == None:
            self._nlabels = np.max(Y_train) + 1
            
        if self._testsz > 0:    
            # labels already one-hot encoded
            if isinstance(Y_train[0], np.ndarray):
                return np.asarray(X_train), np.asarray(X_test), np.asarray(Y_train), np.asarray(Y_test)
            # one-hot encode the labels
            else:
                # Calculate the number of labels as a sequence starting from 0
                nlabels = np.max(Y_train) + 1
                return np.asarray(X_train), np.asarray(X_test), self._one_hot(np.asarray(Y_train), self._nlabels), self._one_hot(np.asarray(Y_test), self._nlabels)
        else:
            # Calculate the number of labels as a sequence starting from 0
            return np.asarray(X_train), None, self._one_hot(np.asarray(Y_train), self._nlabels), None
        
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
        
        # split the indexes into train and test
        split = int((1 - percent) * len(self._data))
        self._train   = self._indices[:split]
        self._test    = self._indices[split:]
        self._trainsz = len(self._train)
        self._testsz  = len(self._test)
        self._next    = 0
        
    def _one_hot(self, Y, C=0):
        """ Convert Vector to one-hot encoding """
        if C == 0:
            # Calculate the number of labels in Y
            C = len(np.max(Y)) + 1
        Y = np.eye(C)[Y.reshape(-1)]
        return Y
    
    @property
    def minibatch(self):
        """ Return a generator for the next mini batch """
        # Minibatch, return a generator
        for _ in range(self._next, min(self._next + self._minisz, self._trainsz)): 
            ix = self._train[_]
            self._next += 1 
            yield self._data[ix]._imgdata , self._data[ix]._label
            if self._augment:
                for _ in range(self._rotate[2]):
                    degree = random.randint(self._rotate[0], self._rotate[1])
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
        if not isinstance(augment, bool) and not isinstance(augment, tuple):
           raise TypeError("Bool or Tuple expected for augment parameter")
        if isinstance(augment, tuple):
            if len(augment) < 2:
                raise AttributeError("Augment parameter must have at least two values")
            if not isinstance(augment[0], int):
                raise TypeError("Integer expected for minimum rotation")
            if not isinstance(augment[1], int):
                raise TypeError("Integer expected for minimum rotation")
            self._rotate[0] = augment[0]
            self._rotate[1] = augment[1]
            if len(augment) > 2:
                if not isinstance(augment[2], int):
                    raise TypeError("Integer expected for number of augmentations")
                self._rotate[2] = augment[2]
                self._rotate[3] = augment[2]
            self._augment = True
        else:       
            self._augment = augment
            
    @property
    def flatten(self):
        """ dummy property """
        return None
            
    @flatten.setter
    def flatten(self, flatten):
        """ (Un)Flatten the Image Data """
        if not isinstance(flatten, bool):
            raise TypeError("Boolean expected for flatten")
        if len(self) == 0:
            return
        if flatten == True:
            # Already Flattened
            if len(self._data[0].shape) == 1:
                return
            for image in self._data:
                image._imgdata = image._imgdata.flatten()
        else:
            # Not Flattened
            if len(self._data[0].shape) != 1:
                return
            if self._resize != None:
                resize = tuple(self._resize)
            else:
                resize = self._data[0]._raw.shape
            for image in self._data:
                image._imgdata = image._imgdata.reshape( resize )
                
    @property
    def resize(self):
        """ dummy property """
        return None
        
    @resize.setter
    def resize(self, resize):
        """ Resize the Image Data """
        if not isinstance(resize, tuple):
            raise TypeError("Tuple expected for resize")
        
        if len(resize) != 2:
            raise AttributeError("Tuple for resize must be in form (height, width)")
            
        # there are no images
        if len(self) == 0:
            return
            
        # openCV uses width, height
        resize = ( resize[1], resize[0] )
        
        # Data is flatten, so let's unflatten it first
        if len(self._data[0].shape) == 1:
            self.flatten = False
        
        for image in self._data:
            image._imgdata = cv2.resize(image._imgdata, resize, interpolation=cv2.INTER_AREA)
            image._shape   = image._imgdata.shape
         
      
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
            if self._rotate[3] > 0:
                self._rotate[3] -= 1
                degree = random.randint(self._rotate[0], self._rotate[1])
                return self._data[ix].rotate(degree) , self._data[ix]._label
            else:
                self._rotate[3] = self._rotate[2]
            
        self._next += 1
        return self._data[ix]._imgdata , self._data[ix]._label
                

    def __len__(self):
        """ Override the len() operator - return the number of images """
        if self._data is None:
            return 0
        return len(self._data)
        
    def __getitem__(self, ix):
        """ Override the index operator - return the image at the corresponding index """
        if not isinstance(ix, int):
            raise TypeError("Index must be an integer")
        if ix > len(self):
            raise IndexError("Index out of range for Images")
        return self._data[ ix ]

    def __iadd__(self, image):
        """ Override the += operator - add an image to the collection """
        if image is None:
            return self
            
        # Add single image
        if isinstance(image, Image):  
            self._data.append( image )
        # Add a collection of images
        elif isinstance(image, Images):
            for img in image:
                self._data.append(img)
            self._time += image.time
        else:
            raise TypeError("Image(s) expected for image")

        if self._nostore == False:
            self.store()
        return self