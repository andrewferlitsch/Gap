from image import Image
import unittest
import pytest
import os
import sys
import time

class MyTest(unittest.TestCase):
        
    def setup_class(self):
        pass
            
    def teardown_class(self):
        pass
    
    def test_001(self):
        """ Image Constructor - no image argument """
        image = Image()
        self.assertEqual(image.image, None)
        
    def test_002(self):
        """ Image Constructor - image = None """
        image = Image(None)
        self.assertEqual(image.image, None)
        
    def test_003(self):
        """ Image Constructor - image = not a string """
        with pytest.raises(TypeError):
            image = Image(1)
        
    def test_004(self):
        """ Image Constructor - image = nonexistent image """
        with pytest.raises(FileNotFoundError):
            image = Image("nonexist.txt")
        
    def test_005(self):
        """ Image Constructor - not an image """
        with pytest.raises(TypeError):
            image = Image("tests/4page.pdf")

    def test_006(self):
        """ Image constructor - directory is not a string """
        with pytest.raises(TypeError):
            image = Image(dir=12)

    def test_007(self):
        """ Image constructor - label is not an int """
        with pytest.raises(TypeError):
            image = Image(label='c')

    def test_008(self):
        """ Image constructor - config is not a list """
        with pytest.raises(TypeError):
            image = Image(label='c')

    def test_009(self):
        """ image properties """
        image = Image("tests/0_100.jpg")
        self.assertEqual(image.image, "tests/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        