"""
Copyright, 2018(c), Andrew Ferlitsch
"""
from gapml.vision import Image, Images
import unittest
import pytest
import os
import sys
import time
from shutil import copy
import cv2
import numpy as np

class MyTest(unittest.TestCase):
        
    def setup_class(self):
        self.isdone = False
            
    def teardown_class(self):
        pass
        
    ### Image
    
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
            image = Image("files/nonexist.txt")
        
    def test_005(self):
        """ Image Constructor - not an image """
        with pytest.raises(TypeError):
            image = Image("files/4page.pdf")

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
        image = Image("files/0_100.jpg", config=['raw'])
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")
        
    def test_010(self):
        """ image dir is None """
        image = Image("files/0_100.jpg", dir=None, config=['raw'])
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("0_100.h5")
        
    def test_011(self):
        """ image dir is not-None - nonexist """
        image = Image("files/0_100.jpg", dir='tmp', config=['raw'])
        self.assertTrue(os.path.isfile("tmp/0_100.h5"))
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("tmp/0_100.h5")
        
    def test_012(self):
        """ image dir is not-None - exist """
        image = Image("files/0_100.jpg", dir='tmp', config=['raw'])
        self.assertTrue(os.path.isfile("tmp/0_100.h5"))
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("tmp/0_100.h5")
        os.rmdir("tmp")
        
    def test_013(self):
        """ label is None """
        with pytest.raises(TypeError):
            image = Image("tests/files/0_100.jpg", dir='tmp', label=None)
            
    def test_014(self):
        """ label is valid """
        image = Image("files/0_100.jpg", dir='tmp', label=16, config=['raw'])
        self.assertEqual(image.label, 16)
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("tmp/0_100.h5")
        os.rmdir("tmp")
            
    def test_015(self):
        """ config is None """
        image = Image("files/0_100.jpg", config=None)
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertEquals(image.raw, None )
        self.assertEqual(image.thumb, None )
        os.remove("0_100.h5")
            
    def test_016(self):
        """ config is empty """
        image = Image("files/0_100.jpg", config=[])
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertEquals(image.raw, None)
        self.assertEqual(image.thumb, None )
        os.remove("0_100.h5")
            
    def test_017(self):
        """ config has non-string entry """
        with pytest.raises(TypeError):
            image = Image("files/0_100.jpg", dir='tmp', config=[1])
            
    def test_018(self):
        """ config has invalid setting """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['foo'])
            
    def test_019(self):
        """ config has valid setting """
        image = Image("files/0_100.jpg", config=['gray', 'grayscale'])
        image = Image("files/0_100.jpg", config=['nostore'])
        os.remove("0_100.h5")
            
    def test_020(self):
        """ config resize has no value """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['resize'])
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['resize='])
            
    def test_021(self):
        """ config resize is wrong format """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['resize=1'])
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['resize=a,2'])
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['resize=2,b'])
            
    def test_022(self):
        """ config - RGB to grayscale """
        image = Image("files/0_100.jpg", config=['gray'])
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")
        image = Image("files/0_100.jpg", config=['grayscale'])
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")
            
    def test_023(self):
        """ config - grayscale to RGB """
        image = Image("files/0_100g.jpg")
        self.assertEqual(image.image, "files/0_100g.jpg")
        self.assertEqual(image.name, "0_100g")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 4253)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100g.h5"))
        os.remove("0_100g.h5")  
        
    def test_024(self):
        """ config - resize """
        image = Image("files/0_100.jpg", config=['resize=50,50'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (50, 50, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")
        image = Image("files/0_100.jpg", config=['resize=(200,200)'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (200, 200, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")

    def test_025(self):
        """ config - flatten """
        image = Image("files/0_100.jpg", config=['flat'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")
        image = Image("files/0_100.jpg", config=['flatten'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.h5")  
        
    def test_026(self):
        """ config - nostore """
        image = Image("files/0_100.jpg", config=['flat', 'nostore'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.label, 0)
        self.assertFalse(os.path.isfile("0_100.h5"))
        
    def test_027(self):
        """ async processing """
        image = Image("files/0_100.jpg", ehandler=self.done)
        time.sleep(3)
        self.assertTrue(self.isdone)
        os.remove("0_100.h5")
        self._isdone = False
        
    def test_028(self):
        """ png file """
        image = Image("files/text.png")
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "png")
        os.remove("text.h5")
        
    def test_029(self):
        """ tif file """
        image = Image("files/6page.tif")
        self.assertEqual(image.name, "6page")
        self.assertEqual(image.type, "tif")
        os.remove("6page.h5")
        image = Image("files/text.tiff")
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "tiff")
        os.remove("text.h5")
        
    def test_030(self):
        """ bmp file """
        image = Image("files/text.bmp")
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "bmp")
        os.remove("text.h5")
        
    def test_031(self):
        """ config - load """
        image = Image("files/0_100.jpg", config=['flat'])
        self.assertTrue(os.path.isfile("0_100.h5"))
        image = None
        image = Image()
        image.load("files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.label, 0)
        os.remove("0_100.h5")
        
    def test_032(self):
        """ thumbnail """
        image = Image("files/0_100.jpg", config=['thumb=(32,32)'])
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertEqual(image.thumb.shape, (32, 32, 3))
        os.remove("0_100.h5")
        image = Image("files/0_100.jpg", config=['thumb=(16,16)'])
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertEqual(image.thumb.shape, (16,16,3))
        os.remove("0_100.h5")
        
    def test_033(self):
        """ thumbnail invalid """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['thumb=1'])
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['thumb=a,2'])
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", dir='tmp', config=['thumb=2,b'])
        
    def test_034(self):
        """ time """
        image = Image("files/0_100.jpg")
        self.assertTrue(image.time > 0)
        os.remove("0_100.h5")

    def test_035(self):
        """ elapsed """
        image = Image("files/0_100.jpg")
        self.assertIsInstance(image.elapsed, str)
        os.remove("0_100.h5")
        
    ### Images
    
    def test_036(self):
        """ Images Constructor - no images argument """
        images = Images()
        self.assertEqual(images.images, None)
        
    def test_037(self):
        """ Images Constructor - images = None """
        images = Images(None)
        self.assertEqual(images.images, None)
        
    def test_038(self):
        """ Images Constructor - images = not a list """
        with pytest.raises(TypeError):
            images = Images(1, [0])
        
    def test_039(self):
        """ Images Constructor - images = entries not a string """
        with pytest.raises(TypeError):
            images = Images([0], [0])
        
    def test_040(self):
        """ Images Constructor - images = image not exist """
        with pytest.raises(FileNotFoundError):
            images = Images(["files/nonexist.jpg"], [0])
        
    def test_041(self):
        """ Images Constructor - labels not a string """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], ['a'])
        
    def test_042(self):
        """ Images Constructor - labels not specified """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"])
        
    def test_043(self):
        """ Images Constructor - labels not match images """
        with pytest.raises(IndexError):
            images = Images(["files/0_100.jpg"], [0, 1])
        
    def test_044(self):
        """ Images Constructor - labels is None """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], labels=None)
        
    def test_045(self):
        """ Images Constructor - single file """
        images = Images(["files/0_100.jpg"], labels=[2])
        self.assertEqual(len(images), 1)
        self.assertTrue(os.path.isfile("collection.0_100.h5"))
        self.assertEqual(images[0].name, "0_100")
        self.assertEqual(images[0].type, "jpg")
        self.assertEqual(images[0].dir, "./")
        self.assertEqual(images[0].size, 3643)
        self.assertEqual(images[0].shape, (100, 100, 3))
        self.assertEqual(images[0].label, 2)
        self.assertEqual(images[0].raw, None )
        self.assertEqual(images[0].thumb, None )
        os.remove("collection.0_100.h5")
        
    def test_046(self):
        """ Images Constructor - multi file """
        images = Images(["files/0_100.jpg", "files/1_100.jpg"], labels=[2, 2])
        self.assertEqual(len(images), 2)
        self.assertTrue(os.path.isfile("collection.0_100.h5"))
        self.assertTrue(images.images != None)
        self.assertEqual(len(images.images), 2)
        self.assertEqual(images.images[0].name, '0_100')
        self.assertEqual(images.images[1].name, '1_100')
        self.assertEqual(images[1].name, '1_100')
        self.assertEqual(images[1].type, "jpg")
        self.assertEqual(images[1].dir, "./")
        self.assertEqual(images[1].size, 3574)
        self.assertEqual(images[1].shape, (100, 100, 3))
        self.assertEqual(images[1].label, 2)
        self.assertEqual(images[1].raw, None )
        self.assertEqual(images[1].thumb, None)
        self.assertEqual(images.name, 'collection.0_100')
        os.remove("collection.0_100.h5")
        
    def test_047(self):
        """ images properties dir, class """
        images = Images(["files/0_100.jpg"], labels=[2], dir="tmp")
        self.assertTrue(images.dir, "tmp")
        self.assertTrue(images.labels, [2])
        os.remove("tmp/collection.0_100.h5")
        os.rmdir("tmp")
        
    def test_048(self):
        """ images constructor - dir not a string """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], labels=[0], dir=0)
        
    def test_049(self):
        """ images constructor - collection not a string """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], labels=[0], collection=0)
        
    def test_050(self):
        """ images properties dir, class """
        images = Images(["files/0_100.jpg"], labels=[2], name="foobar")
        self.assertEqual(images.name, 'foobar')
        self.assertTrue(os.path.isfile("foobar.h5"))
        os.remove("foobar.h5")
        
    def test_051(self):
        """ Images Constructor - multi file """
        images = Images(["files/0_100.jpg", "files/1_100.jpg"], labels=2)
        self.assertEqual(len(images), 2)
        self.assertTrue(os.path.isfile("collection.0_100.h5"))
        self.assertTrue(images.images != None)
        self.assertEqual(len(images.images), 2)
        self.assertEqual(images.images[0].name, '0_100')
        self.assertEqual(images.images[1].name, '1_100')
        self.assertEqual(images[1].name, '1_100')
        self.assertEqual(images[1].type, "jpg")
        self.assertEqual(images[1].dir, "./")
        self.assertEqual(images[1].size, 3574)
        self.assertEqual(images[1].shape, (100, 100, 3))
        self.assertEqual(images[1].label, 2)
        self.assertEqual(images[1].raw, None)
        self.assertEqual(images[1].thumb, None)
        self.assertEqual(images.name, 'collection.0_100')
        os.remove("collection.0_100.h5")
                
    def test_052(self):
        """ images load - default collection name """
        images = Images(["files/0_100.jpg", "files/1_100.jpg"], labels=[1,2])
        self.assertEqual(images.name, 'collection.0_100')
        images = Images()
        images.load("collection.0_100")
        self.assertEqual(images.name, 'collection.0_100')
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].label, 1)
        self.assertEqual(images[1].label, 2)
        os.remove("collection.0_100.h5")
            
    def test_053(self):
        """ images load - collection name """
        images = Images(["files/0_100.jpg", "files/1_100.jpg"], labels=[1,2], name='foobar')
        self.assertEqual(images.name, 'foobar')
        images = Images()
        images.load("foobar")
        self.assertEqual(images.name, 'foobar')
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].label, 1)
        self.assertEqual(images[1].label, 2)
        os.remove("foobar.h5")
            
    def test_054(self):
        """ images async """
        self.isdone = False
        images = Images(["files/0_100.jpg", "files/1_100.jpg"], labels=[1,2], name='foobar', ehandler=self.done) 
        time.sleep(3)
        self.assertTrue(self.isdone)
        self.assertEqual(images.name, 'foobar')
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0].label, 1)
        self.assertEqual(images[1].label, 2)
        os.remove("foobar.h5")
        self.is_done = False
        
    def test_055(self):
        """ Images - time """
        images = Images(["files/0_100.jpg"], labels=[2])
        self.assertEqual(len(images), 1)
        self.assertTrue(images.time > 0)
        os.remove("collection.0_100.h5")
        
    def test_056(self):
        """ Images - create dir"""
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg'], 2, name='foobar', dir='tmp2')
        self.assertTrue(os.path.isfile("tmp2/foobar.h5"))
        os.remove("tmp2/foobar.h5")
        os.rmdir('tmp2')
        
    def test_057(self):
        """ Images - split not an float """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(TypeError):
            images.split = 'a'
        os.remove('foobar.h5')
        
    def test_058(self):
        """ Images - split not a valid range """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(ValueError):
            images.split = -0.1
        with pytest.raises(ValueError):
            images.split = 1.0
        os.remove('foobar.h5')
        
    def test_059(self):
        """ Images - split by default """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        x1, x2, y1, y2 = images.split
        self.assertEquals(len(x1), 3)
        self.assertEquals(len(x2), 1)
        self.assertEquals(len(y1), 3)
        self.assertEquals(len(y2), 1)
        os.remove('collection.0_100.h5')
        
    def test_060(self):
        """ Images - split, set percent """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        images.split = 0.5
        self.assertEqual(len(images._train), 2)
        self.assertEqual(len(images._test), 2)
        os.remove('collection.0_100.h5')
        
    def test_061(self):
        """ Images - split, percent specified """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        images.split = 0.25
        x1, x2, y1, y2 = images.split
        self.assertEquals(len(x1), 3)
        self.assertEquals(len(x2), 1)
        self.assertEquals(len(y1), 3)
        self.assertEquals(len(y2), 1)
        os.remove('collection.0_100.h5')
        
    def test_062(self):
        """ Images - iterate through collection """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        images.split = 0.25
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), (None, None))
        os.remove('collection.0_100.h5')
            
    def test_063(self):
        """ Images - iterate 2nd pass """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg', 'files/3_100.jpg'], [1,2,3,4,5], name='foobar')
        images.split = 0.5
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), (None, None))
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), (None, None))
        os.remove('foobar.h5')
        
    def test_064(self):
        """ Images - minibatch not an integer """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(TypeError):
            images.minibatch = 'a'
        os.remove('foobar.h5')
        
    def test_065(self):
        """ Images - minibatch invalid range """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(ValueError):
            images.minibatch = 0
        with pytest.raises(ValueError):
            images.minibatch = 4
        os.remove('foobar.h5')
        
    def test_066(self):
        """ Images - minibatch - fetch """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg', 'files/3_100.jpg', 'files/1_100.jpg'], [1,2,3,4,5,6], name='foobar')
        images.split = 0.5
        images.minibatch = 2
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 2)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 1)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 0)
        os.remove('foobar.h5')
        
    def test_067(self):
        """ Images - split - invalid tuple size """
        images = Images(['files/0_100.jpg'], [1], name='foobar')
        with pytest.raises(AttributeError):
            images.split = (0.9, 2, 3)
        os.remove('foobar.h5')
        
    def test_068(self):
        """ Images - split - tuple, percent not a float, seed not an int """
        images = Images(['files/0_100.jpg'], [1], name='foobar')
        with pytest.raises(TypeError):
            images.split = ('a', 2)
        with pytest.raises(TypeError):
            images.split = (0.8, 'a')
        os.remove('foobar.h5')
        
    def test_069(self):
        """ Image - split - tuple valid """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg'], [1, 2], name='foobar')
        images.split = 0.5, 2
        self.assertEqual(len(next(images)), 2)
        os.remove('foobar.h5')
        
    def test_070(self):
        """ Image - remote image """
        image = Image('https://cdn.cnn.com/cnnnext/dam/assets/180727161452-trump-speech-economy-072718-exlarge-tease.jpg', 2)
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.size, 38302)
        self.assertEqual(image.shape, (438, 780, 3))
        image = Image('https://cdn.cnn.com/cnnnext/dam/assets/180727161452-trump-speech-economy-072718-exlarge-tease.jpg', 2, config=['grayscale'])
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.size, 38302)
        self.assertEqual(image.shape, (438, 780))
        os.remove('180727161452-trump-speech-economy-072718-exlarge-tease.h5')
        
    def test_071(self):
        """ Image - nonexistent remote image """
        image = Image('https://cdn.cnn.com/cnnnext/dam/assets/18ch-economy-072718-exlarge-tease.jpg', 2)
        self.assertEqual(image.data, None)
        
    def test_072(self):
        """ Image - bad image """
        f = open("tmp.jpg", "w")
        f.write("foobar")
        f.close()
        image = Image('tmp.jpg', 2)
        self.assertEqual(image.data, None)
        os.remove('tmp.jpg')
        
    def test_073(self):
        """ Images - directory """
        os.mkdir("tmp1")
        copy('files/0_100.jpg', 'tmp1')
        copy('files/1_100.jpg', 'tmp1')
        os.mkdir("tmp2")
        copy('files/2_100.jpg', 'tmp2')
        copy('files/3_100.jpg', 'tmp2')
        images = Images( ['tmp1', 'tmp2'], [1,2], name='foobar', config=['grayscale'])
        self.assertEqual(len(images), 4)
        os.remove('foobar.h5')
        os.remove('tmp1/0_100.jpg')
        os.remove('tmp1/1_100.jpg')
        os.rmdir("tmp1")
        os.remove('tmp2/2_100.jpg')
        os.remove('tmp2/3_100.jpg')
        os.rmdir("tmp2")
        
    def test_074(self):
        """ Image - rotate - grayscale """
        image = Image("files/1_100.jpg", 1, config=['resize=(64,64)', 'grayscale'])
        rotated = image.rotate(90)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(180)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(270)
        self.assertTrue(rotated.shape, (64, 64))
        os.remove('1_100.h5')
        
    def test_075(self):
        """ Images - [] not an int """
        images = Images(["files/1_100.jpg"], 1)
        with pytest.raises(TypeError):
            image = images['abc']
        os.remove('collection.1_100.h5')
        
    def test_076(self):
        """ Images - len() returns 0 when no files loaded """
        images = Images()
        self.assertEquals(len(images), 0)
        
    def test_077(self):
        """ Image - load() attr type and size """
        image = Image("files/0_100.jpg", 1)
        image = Image()
        image.load('0_100.h5')
        self.assertEquals(image.type, 'jpg')
        self.assertEquals(image.size, 3643)
        os.remove('0_100.h5')
        
    def test_078(self):
        """ Images - directories as image arguments """
        images = Images(["files/imtest1", "files/imtest2"], [1,2], name="foobar")
        self.assertEquals(len(images), 4)
        self.assertEquals(images[0].name, "0_100")
        self.assertEquals(images[1].name, "0_100g")
        self.assertEquals(images[2].name, "1_100")
        self.assertEquals(images[3].name, "2_100")
        self.assertEquals(images[0].label, 1)
        self.assertEquals(images[1].label, 1)
        self.assertEquals(images[2].label, 2)
        self.assertEquals(images[3].label, 2)
        os.remove("foobar.h5")
        
    def test_079(self):
        """ Images - split = 0 """
        images = Images(["files/imtest1", "files/imtest2"], [1,2], name="foobar")
        images.split = 0.0
        self.assertEquals(len(images._train), 4)
        self.assertEquals(len(images._test), 0)
        images.split = 0
        self.assertEquals(len(images._train), 4)
        self.assertEquals(len(images._test), 0)
        os.remove("foobar.h5")
        
    def test_080(self):
        """ Image - gif file """
        image = Image("files/gray.gif", 1)
        self.assertEquals(image.shape, (415, 506, 3))
        image = Image("files/gray.gif", 1, config=['grayscale'])
        self.assertEquals(image.shape, (415, 506))
        image = Image("files/rgb.gif", 1)
        self.assertEquals(image.shape, (561, 748, 3))
        image = Image("files/rgb.gif", 1, config=['grayscale'])
        self.assertEquals(image.shape, (561, 748))
        os.remove("gray.h5")
        os.remove("rgb.h5")
        
    def test_081(self):
        """ Image - rotate - grayscale, non-90 degree """
        image = Image("files/1_100.jpg", 1, config=['resize=(64,64)', 'grayscale'])
        rotated = image.rotate(30)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(45)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(60)
        self.assertTrue(rotated.shape, (64, 64))
        os.remove('1_100.h5')
        
    def test_082(self):
        """ Image - rotate - rgb """
        image = Image("files/1_100.jpg", 1, config=['resize=(64,64)'])
        rotated = image.rotate(90)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(180)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(270)
        self.assertTrue(rotated.shape, (64, 64))
        os.remove('1_100.h5')
        
    def test_083(self):
        """ Image - rotate - rgb, non-90 degree """
        image = Image("files/1_100.jpg", 1, config=['resize=(64,64)'])
        rotated = image.rotate(30)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(45)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(60)
        self.assertTrue(rotated.shape, (64, 64))
        os.remove('1_100.h5')
        
    def test_084(self):
        """ Image - rotate - rgb,negative degree """
        image = Image("files/1_100.jpg", 1, config=['resize=(64,64)'])
        rotated = image.rotate(-30)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(-45)
        self.assertTrue(rotated.shape, (64, 64))
        rotated = image.rotate(-60)
        self.assertTrue(rotated.shape, (64, 64))
        os.remove('1_100.h5')
        
    def test_085(self):
        """ Image - rotate invalid """
        image = Image("files/1_100.jpg", 1, config=['resize=(64,64)'])
        with pytest.raises(ValueError):
            image.rotate(-360)
        with pytest.raises(ValueError):
            image.rotate(360)
        os.remove('1_100.h5')
        
    def test_086(self):
        """ Images - iterate through collection multiple times """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [0,1,2,3])
        images.split = 0.50
        ref = images._train[:]
        
        for i in range(0,4):
            data, label = next(images)
            self.assertTrue(label in ref)
            data, label = next(images)
            self.assertTrue(label in ref)
            data, label = next(images)
        os.remove('collection.0_100.h5')
        
    def test_087(self):
        """ Images - next() - augmentation """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [0,1,2,3])
        images.split = 0.50
        images.augment = True
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), (None, None))
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), (None, None))
        os.remove('collection.0_100.h5')
        
    def test_088(self):
        """ Images - minibatch - augmentation """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg', 'files/3_100.jpg', 'files/1_100.jpg'], [1,2,3,4,5,6], name='foobar')
        images.split = 0.5
        images.minibatch = 2
        images.augment = True
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 4)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 2)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 0)
        os.remove('foobar.h5')
        
    def test_089(self):
        """ Images - thumbnail """
        images = Images(["files/0_100.jpg"], 1, config=['thumb=16,16'], name='foobar')
        self.assertEquals(images[0].thumb.shape, (16, 16, 3))
        os.remove('foobar.h5')
        
    def test_090(self):
        """ Images - thumbnail - load """
        images = Images(["files/0_100.jpg"], 1, config=['thumb=16,16'], name='foobar')
        images = Images()
        images.load('foobar')
        self.assertEquals(images[0].thumb.shape, (16, 16, 3))
        os.remove('foobar.h5')
        
    def test_091(self):
        """ Image - raw pixel input """
        pixels = cv2.imread('files/1_100.jpg')
        image = Image(pixels, 1)
        self.assertEquals(image.name, 'untitled')
        self.assertEquals(image.type, 'raw')
        self.assertEquals(image.size, 30000)
        self.assertEquals(image.shape, (100, 100, 3))
        image = Image(pixels, 1, config=['gray'])
        self.assertEquals(image.name, 'untitled')
        self.assertEquals(image.type, 'raw')
        self.assertEquals(image.size, 30000)
        self.assertEquals(image.shape, (100, 100))
        os.remove('untitled.h5')
        
    def test_092(self):
        """ Image - raw pixel input - gray to color """
        pixels = cv2.imread('files/1_100.jpg', cv2.IMREAD_GRAYSCALE)
        image = Image(pixels, 1)
        self.assertEquals(image.name, 'untitled')
        self.assertEquals(image.type, 'raw')
        self.assertEquals(image.size, 10000)
        self.assertEquals(image.shape, (100, 100, 3))
        image = Image(pixels, 1, config=['gray'])
        self.assertEquals(image.name, 'untitled')
        self.assertEquals(image.type, 'raw')
        self.assertEquals(image.size, 10000)
        self.assertEquals(image.shape, (100, 100))
        os.remove('untitled.h5')
 
    def test_093(self):
        """ Image - ehandler not a function """
        with pytest.raises(TypeError):
            image = Image('files/1_100.jpg', 1, ehandler=2)
 
    def test_094(self):
        """ Image - ehandler not a function """
        with pytest.raises(TypeError):
            image = Image('files/1_100.jpg', 1, ehandler=(2,2))
 
    def test_095(self):
        """ Image - ehandler with arguments """
        image = Image('files/1_100.jpg', 1, ehandler=(self.done2, 6))
        time.sleep(3)
        self.assertTrue(self.isdone)
        self.assertTrue(self.args, 6)
        os.remove("1_100.h5")
        self._isdone = False
 
    def test_096(self):
        """ Images - ehandler not a function """
        with pytest.raises(TypeError):
            image = Images(['files/1_100.jpg'], 1, ehandler=2)
 
    def test_097(self):
        """ Images - ehandler not a function """
        with pytest.raises(TypeError):
            image = Images(['files/1_100.jpg'], 1, ehandler=(2,2))
 
    def test_098(self):
        """ Images - ehandler with arguments """
        images = Images(['files/1_100.jpg'], 1, ehandler=(self.done2, 6))
        time.sleep(3)
        self.assertTrue(self.isdone)
        self.assertTrue(self.args, 6)
        os.remove("collection.1_100.h5")
        self._isdone = False
 
    def test_099(self):
        """ Images - mixed size images """
        images = Images(['files/1_100.jpg', 'files/text.jpg'], [1,2], config=['resize=(100,100)', 'raw'])
        images = Images()
        images.load('collection.1_100')
        self.assertEquals(len(images), 2)
        self.assertEquals(images[0].raw.shape, (100, 100, 3))
        self.assertEquals(images[1].raw.shape, (297, 275, 3))
        os.remove("collection.1_100.h5")
 
    def test_100(self):
        """ Images - += Image """
        images = Images(['files/1_100.jpg'], 1)
        image = Image('files/2_100.jpg', 2, config=['nostore'])
        images += image
        self.assertEquals(len(images), 2)
        self.assertEquals(images[0].name, '1_100')
        self.assertEquals(images[1].name, '2_100')
        self.assertEquals(images[0].label, 1)
        self.assertEquals(images[1].label, 2)
        os.remove("collection.1_100.h5")
 
    def test_101(self):
        """ Images - += Images """
        images = Images(['files/1_100.jpg', 'files/2_100.jpg'], 1)
        images2 = Images(['files/0_100.jpg', 'files/3_100.jpg'], 2, config=['nostore'])
        images += images2
        self.assertEquals(len(images), 4)
        self.assertEquals(images[0].name, '1_100')
        self.assertEquals(images[1].name, '2_100')
        self.assertEquals(images[2].name, '0_100')
        self.assertEquals(images[3].name, '3_100')
        self.assertEquals(images[0].label, 1)
        self.assertEquals(images[1].label, 1)
        self.assertEquals(images[2].label, 2)
        self.assertEquals(images[3].label, 2)
        os.remove("collection.1_100.h5")
 
    def test_102(self):
        """ Images - += Images nostore, then store """
        images = Images(['files/1_100.jpg', 'files/2_100.jpg'], 1, config=['nostore'])
        images2 = Images(['files/0_100.jpg', 'files/3_100.jpg'], 2, config=['nostore'])
        images += images2
        self.assertEquals(len(images), 4)
        self.assertEquals(images[0].name, '1_100')
        self.assertEquals(images[1].name, '2_100')
        self.assertEquals(images[2].name, '0_100')
        self.assertEquals(images[3].name, '3_100')
        self.assertEquals(images[0].label, 1)
        self.assertEquals(images[1].label, 1)
        self.assertEquals(images[2].label, 2)
        self.assertEquals(images[3].label, 2)
        images.store()
        os.remove("collection.1_100.h5")
 
    def test_103(self):
        """ Images - nostore """
        images = Images(['files/1_100.jpg', 'files/2_100.jpg'], 1, config=['nostore'])
        self.assertFalse(os.path.isfile('collection.1_100.h5'))
        
    def test_104(self):
        """ Images - += Images """
        images = Images(['files/1_100.jpg', 'files/2_100.jpg'], 1)
        images2 = Images(['files/0_100.jpg', 'files/3_100.jpg'], 2)
        images += images2
        self.assertEquals(len(images), 4)
        self.assertEquals(images[0].name, '1_100')
        self.assertEquals(images[1].name, '2_100')
        self.assertEquals(images[2].name, '0_100')
        self.assertEquals(images[3].name, '3_100')
        self.assertEquals(images[0].label, 1)
        self.assertEquals(images[1].label, 1)
        self.assertEquals(images[2].label, 2)
        self.assertEquals(images[3].label, 2)
        images.store()
        os.remove("collection.1_100.h5")
        os.remove("collection.0_100.h5")
        
    def test_105(self):
        """ Images - augment - too few tuple """
        images = Images()
        with pytest.raises(TypeError):
            images.augment = (1)
        
    def test_106(self):
        """ Images - augment - tuple not an int """
        images = Images()
        with pytest.raises(TypeError):
            images.augment = ('a', 1)
        with pytest.raises(TypeError):
            images.augment = (1, 'a')
        with pytest.raises(TypeError):
            images.augment = 'a', 1
        with pytest.raises(TypeError):
            images.augment = 1, 'a'
        with pytest.raises(TypeError):
            images.augment = 1, 1, 'a'
        
    def test_107(self):
        """ Images - augment - valid tuple (min, max) """
        images = Images()
        images.augment = (-45, 45)
        self.assertEquals(images._rotate[0], -45)
        self.assertEquals(images._rotate[1], 45)
        images.augment = 20, 60
        self.assertEquals(images._rotate[0], 20)
        self.assertEquals(images._rotate[1], 60)
        
    def test_108(self):
        """ Images - augment - valid tuple (min, max, n) - next """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [0,1,2,3])
        images.split = 0.50
        images.augment = (-45, 45, 2)
        self.assertEquals(images._rotate[0], -45)
        self.assertEquals(images._rotate[1], 45)
        self.assertEquals(images._rotate[2], 2)
        self.assertEquals(images._rotate[3], 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), (None, None))
        os.remove("collection.0_100.h5")
        
    def test_109(self):
        """ Images - augment - valid tuple (min, max, n) - minibatch """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg', 'files/3_100.jpg', 'files/1_100.jpg'], [1,2,3,4,5,6], name='foobar')
        images.split = 0.5
        images.minibatch = 2
        images.augment = (-45, 45, 2)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 6)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 3)
        g = images.minibatch
        x = 0
        for _ in g: x += 1
        self.assertEquals(x, 0)
        os.remove('foobar.h5')
        
    def test_110(self):
        """ Images - transform / flatten """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore'])
        images.flatten = True
        self.assertEquals(images[0].data.shape, (30000,))
        self.assertEquals(images[1].data.shape, (30000,))
        
    def test_111(self):
        """ Images - transform / flatten - already flatten """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'flat'])
        images.flatten = True
        self.assertEquals(images[0].data.shape, (30000,))
        self.assertEquals(images[1].data.shape, (30000,))
        
    def test_112(self):
        """ Images - transform / flatten - resized"""
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'resize=(50,50)'])
        images.flatten = True
        self.assertEquals(images[0].data.shape, (7500,))
        self.assertEquals(images[1].data.shape, (7500,))
        
    def test_113(self):
        """ Images - transform / flatten - no images """
        images = Images()
        images.flatten = True
        
    def test_114(self):
        """ Images - transform / flatten - grayscale """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'gray'])
        images.flatten = True
        self.assertEquals(images[0].data.shape, (10000,))
        self.assertEquals(images[1].data.shape, (10000,))
        
    def test_115(self):
        """ Images - transform / flatten - not a boolean """
        images = Images()
        with pytest.raises(TypeError):
            images.flatten = 3
        
    def test_116(self):
        """ Images - transform / unflatten - already unflatten """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore'])
        images.flatten = False
        self.assertEquals(images[0].data.shape, (100, 100, 3))
        self.assertEquals(images[1].data.shape, (100, 100, 3))
        
    def test_117(self):
        """ Images - transform / unflatten - already unflatten / gray """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'gray'])
        images.flatten = False
        self.assertEquals(images[0].data.shape, (100, 100))
        self.assertEquals(images[1].data.shape, (100, 100))
        
    def test_118(self):
        """ Images - transform / unflatten - no images """
        images = Images()
        images.flatten = False
        
    def test_119(self):
        """ Images - transform / unflatten - same size """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'flat', 'raw'])
        images.flatten = False
        self.assertEquals(images[0].data.shape, (100, 100, 3))
        self.assertEquals(images[1].data.shape, (100, 100, 3))
        
    def test_120(self):
        """ Images - transform / unflatten - different size """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'flat', 'resize=(60,60)'])
        images.flatten = False
        self.assertEquals(images[0].data.shape, (60, 60, 3))
        self.assertEquals(images[1].data.shape, (60, 60, 3))
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'flat', 'resize=60,60'])
        images.flatten = False
        self.assertEquals(images[0].data.shape, (60, 60, 3))
        self.assertEquals(images[1].data.shape, (60, 60, 3))
        
    def test_121(self):
        """ Images - labels are one hot encoded in split """
        images =  Images(['files/0_100.jpg', 'files/1_100.jpg'], [1,2], config=['nostore', 'flat', 'resize=(60,60)'])
        images.split = 0.5
        X_train, X_test, Y_train, Y_test = images.split
        self.assertTrue(type(X_train), np.ndarray)
        self.assertTrue(type(X_test ), np.ndarray)
        self.assertTrue(type(Y_train), np.ndarray)
        self.assertTrue(type(Y_test ), np.ndarray)
        self.assertTrue(Y_train.shape, (2,3))
        self.assertTrue(Y_test.shape, (2,3))
        
    def test_122(self):
        """ Image / Images: time property when on processing """
        image = Image()
        images = Images()
        self.assertEquals(image.time, 0)
        self.assertEquals(images.time, 0)
        
    def test_123(self):
        """ Image / Images - time property is non-zero """
        image = Image('files/0_100.jpg', 1)
        self.assertTrue(image.time > 0)
        os.remove('0_100.h5')
        images = Images(['files/0_100.jpg'], 1)
        self.assertTrue(images.time > 0)
        os.remove('collection.0_100.h5')
        
    def test_124(self):
        """ Image - config setting is raw """
        image = Image("files/0_100.jpg", config=['raw'])
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.label, 0)
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("0_100.h5")
         
    def test_125(self):
        """ Images Constructor - single file """
        images = Images(["files/0_100.jpg"], labels=[2], config=['raw'])
        self.assertEqual(len(images), 1)
        self.assertTrue(os.path.isfile("collection.0_100.h5"))
        self.assertEqual(images[0].name, "0_100")
        self.assertEqual(images[0].type, "jpg")
        self.assertEqual(images[0].dir, "./")
        self.assertEqual(images[0].size, 3643)
        self.assertEqual(images[0].shape, (100, 100, 3))
        self.assertEqual(images[0].label, 2)
        self.assertTrue(len(images[0].raw) > 0 )
        self.assertEqual(images[0].thumb, None )
        os.remove("collection.0_100.h5")
         
    def test_126(self):
        """ Image Constructor - default float32 on normalize """
        image = Image("files/0_100.jpg", 2)
        self.assertEquals(type(image.data[0][0][0]), np.float32)
        os.remove("0_100.h5")
         
    def test_127(self):
        """ Image Constructor - set float on normalize """
        image = Image("files/0_100.jpg", 2, config=['float16'])
        self.assertEquals(type(image.data[0][0][0]), np.float16)
        image = Image("files/0_100.jpg", 2, config=['float32'])
        self.assertEquals(type(image.data[0][0][0]), np.float32)
        image = Image("files/0_100.jpg", 2, config=['float64'])
        self.assertEquals(type(image.data[0][0][0]), np.float64)
        os.remove("0_100.h5")
        
    def test_128(self):
        """ Image - config setting float invalid """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", 2, config=['float24'])
        
    def test_129(self):
        """ Images - config not a list """
        with pytest.raises(TypeError):
            image = Image("files/0_100.jpg", 2, config='float24')
        
    def test_130(self):
        """ Images - config setting resize is invalid """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", 2, config=['resize=(10,20)='])
        
    def test_131(self):
        """ Images - config setting thumb is invalid """
        with pytest.raises(AttributeError):
            image = Image("files/0_100.jpg", 2, config=['thumb=(10,20)='])
        
    def test_132(self):
        """ Images - invalid type for images """
        with pytest.raises(TypeError):
            images = Images(1,1)
            
    def test_133(self):
        """ Images - 1d numpy array is invalid """
        arr = np.array( [ 1, 2, 3 ] )
        with pytest.raises(TypeError):
            images = Images(arr,1)
            
    def test_134(self):
        """ Images - 1d numpy array is uint8 """
        arr = np.array( [ [255,2], [3,4], [5,6] ], dtype=np.uint8 )
        images = Images(arr,1)
        self.assertEquals(len(images), 3)     
        self.assertEquals(type(images[0].data[0]), np.float32)   
        self.assertEquals(images[0].data[0], 1.0) 
        self.assertEquals(images[0].name, 'untitled')
        self.assertEquals(images[0].image, 'untitled')
            
    def test_135(self):
        """ Images - 1d numpy array is uint16 """
        arr = np.array( [ [65535,2], [3,4], [5,6] ], dtype=np.uint16 )
        images = Images(arr,1)
        self.assertEquals(len(images), 3)     
        self.assertEquals(type(images[0].data[0]), np.float32)   
        self.assertEquals(images[0].data[0], 1.0) 
        self.assertEquals(images[0].name, 'untitled')
        self.assertEquals(images[0].image, 'untitled')
            
    def test_136(self):
        """ Images - 1d numpy array is float16 """
        arr = np.array( [ [1.0, 0.5], [0.25, 0.75], [0.2, 0.4] ], dtype=np.float16 )
        images = Images(arr,1)
        self.assertEquals(len(images), 3)     
        self.assertEquals(type(images[0].data[0]), np.float32)   
        self.assertEquals(images[0].data[0], 1.0) 
        self.assertEquals(images[0].name, 'untitled')
        self.assertEquals(images[0].image, 'untitled')
            
    def test_137(self):
        """ Images - 1d numpy array is float32 """
        arr = np.array( [ [1.0, 0.5], [0.25, 0.75], [0.2, 0.4] ], dtype=np.float32 )
        images = Images(arr,1)
        self.assertEquals(len(images), 3)     
        self.assertEquals(type(images[0].data[0]), np.float32)   
        self.assertEquals(images[0].data[0], 1.0) 
        self.assertEquals(images[0].name, 'untitled')
        self.assertEquals(images[0].image, 'untitled')
            
    def test_138(self):
        """ Images - 1d numpy array is float64 """
        arr = np.array( [ [1.0, 0.5], [0.25, 0.75], [0.2, 0.4] ], dtype=np.float64 )
        images = Images(arr,1)
        self.assertEquals(len(images), 3)     
        self.assertEquals(type(images[0].data[0]), np.float32)   
        self.assertEquals(images[0].data[0], 1.0) 
        self.assertEquals(images[0].name, 'untitled')
        self.assertEquals(images[0].image, 'untitled')
        
        
    def done(self, image):
        self.isdone = True
        os.remove(image)
        
    def done2(self, image, args):
        self.isdone = True
        self.args = args
