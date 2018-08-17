""" Dataset Module for handling datasets
Copyright, 2018(c), Andrew Ferlitsch
"""

import numpy as np

from .vision import Images

class Dataset(object):
    """ Manage Dataset for Training a Model """
    def __init__(self):
        self._init()
        
    def _init(self):
        """ re-initialize variables """
        self.X_train = []   # Training input data (independent variables)
        self.Y_train = []   # Training Labels     (dependent variable)
        self.X_test  = []   # Test input data
        self.Y_test  = []   # Test Labels
        
class ImageDataset(Dataset):
    """ Manage Image Dataset for Training a Model """
    
    def __init__(self, collections):
        self._collections = collections
        self._split      = 0.2
        self._seed       = 0
        
    def split(self, percent, seed, nlabels=None):
        """ Split dataset into training and test data """
        self._init()
        
        self._split = percent
        self._seed  = seed
        
        # Split each collection in the dataset
        for images in self._collections:
            # Split the collection
            images.split = self._split, self._seed
            
            # Retrieve the split data
            x_train, x_test, y_train, y_test = images.split
            
            self.X_train.extend(x_train)
            self.X_test.extend(x_test)
            self.Y_train.extend(y_train)
            self.Y_test.extend(y_test)
            
        # Convert lists to numpy arrays
        self.X_train = np.asarray(self.X_train)
        self.Y_train = np.asarray(self.Y_train)
        self.X_test  = np.asarray(self.X_test)
        self.Y_test  = np.asarray(self.Y_test)
        
        # If the number of unique labels is not specified, assume each collection is a unique label
        if nlabels == None:
            nlabels = len(self._collections)
        
        # Convert label values to one hot encoding (dummy variable conversion
        self.Y_train = self.convert_labels_to_one_hot_encoding(self.Y_train, nlabels)
        self.Y_test  = self.convert_labels_to_one_hot_encoding(self.Y_test, nlabels)
        
        return self.X_train, self.X_test, self.Y_train, self.Y_test

        
    def convert_labels_to_one_hot_encoding(self, Y, C):
        """ This function will do the reshape and conversion """
        Y = np.eye(C)[Y.reshape(-1)]
        return Y