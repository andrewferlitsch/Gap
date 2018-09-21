""" Performance Testing for Vision Module 
Copyright 2018(c), Andrew Ferlitsch
"""
import unittest
import numpy as np
import h5py
import cv2
import os, time, sys
import PIL
from PIL import Image
import cv2

from gapml.vision import Image, Images
class MyTest(unittest.TestCase):
    files = []
    dir = []
    def setup_class(self):
        os.chdir("./tests")
    def teardown_class(self):
        os.chdir("..")

    def test_001(self):
#        global files, dir
        """ PIL Performance Tests """
        total = 0
        for _ in range(10):
            start = time.time()
            images = []
            for file in self.files:
                pixels = PIL.Image.open(dir + "/" + file)
                image  = np.asarray(pixels)
                image  = image / 255.0
                image  = image.flatten()
                images.append(image)
            with h5py.File('tmp.h5', 'w') as hf:
                hf.create_dataset("images",  data=images)
            batch_time = time.time() - start
            print("BATCH", batch_time)
            total += batch_time
            os.remove("tmp.h5")
        print("PIL AVE", total / 10 )

    def test_002(self):
        """ openCV Performance Tests """
        #        global files, dir
        total = 0
        for _ in range(10):
            start = time.time()
            images = []
            for file in self.files:
                pixels = cv2.imread(dir + "/" + file, 0)
                image  = np.asarray(pixels)
                image  = image / 255.0
                image  = image.flatten()
                images.append(image)
            with h5py.File('tmp.h5', 'w') as hf:
                hf.create_dataset("images",  data=images)
            batch_time = time.time() - start
            print("BATCH", batch_time)
            total += batch_time
            os.remove("tmp.h5")
        print("CV2 AVE", total / 10 )
        
            
    def test_003(self):
        """ Vision/Image Performance Tests """
#        global files, dir
        total = 0
        for _ in range(10):
            start = time.time()
            images = []
            labels = []
            for file in self.files:
                image = Image(dir + "/" + file, config=['flatten', 'grayscale', 'nostore'])
                images.append( image.data )
                labels.append( 1 )
            with h5py.File('tmp.h5', 'w') as hf:
                hf.create_dataset("images",  data=images)
                hf.create_dataset("labels",  data=labels)
            batch_time = time.time() - start
            print("BATCH", batch_time)
            total += batch_time
            os.remove("tmp.h5")
        print("VISION/IMAGE AVE", total / 10 )
        
    def test_004(self):
        """ Vision/Images Performance Tests """
        #        global files, dir
        images = []
        for file in self.files:
            images.append( dir + "/" + file )
        total = 0
        for _ in range(10):
            start = time.time()
            Images(images, 1, batch='foobar', dir='tmp', config=['grayscale', 'flatten'])
            batch_time = time.time() - start
            print("BATCH", batch_time)
            total += batch_time
            os.remove("tmp/foobar.h5")
        print("VISION/IMAGES AVE", total / 10 )
        
    if __name__ == "__main__":
        dir = sys.argv[1]
        #dir = '../Training/AITraining/Intermediate/Machine Learning/sign-lang/gestures/1'
        files = os.listdir(dir)
        if sys.argv[2] == '1':
            test_001(self)
        elif sys.argv[2] == '2':
            test_002(self)
        elif sys.argv[2] == '3':
            test_003(self)
        elif sys.argv[2] == '4':
            test_004(self)