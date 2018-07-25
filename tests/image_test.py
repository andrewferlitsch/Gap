"""
Copyright, 2018(c), Andrew Ferlitsch
"""
from vision import Image, Images
import unittest
import pytest
import os
import sys
import time

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
        image = Image("files/0_100.jpg")
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
        image = Image("files/0_100.jpg", dir=None)
        self.assertEqual(image.image, "files/0_100.jpg")
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("0_100.h5")
        
    def test_011(self):
        """ image dir is not-None - nonexist """
        image = Image("files/0_100.jpg", dir='tmp')
        self.assertTrue(os.path.isfile("tmp/0_100.h5"))
        self.assertTrue(len(image.raw) > 0 )
        self.assertEqual(image.thumb, None )
        os.remove("tmp/0_100.h5")
        
    def test_012(self):
        """ image dir is not-None - exist """
        image = Image("files/0_100.jpg", dir='tmp')
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
        image = Image("files/0_100.jpg", dir='tmp', label=16)
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
        self.assertTrue(len(image.raw) > 0 )
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
        self.assertTrue(len(image.raw) > 0 )
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
        
    ### Images
    
    def test_035(self):
        """ Images Constructor - no images argument """
        images = Images()
        self.assertEqual(images.images, None)
        
    def test_036(self):
        """ Images Constructor - images = None """
        images = Images(None)
        self.assertEqual(images.images, None)
        
    def test_037(self):
        """ Images Constructor - images = not a list """
        with pytest.raises(TypeError):
            images = Images(1, [0])
        
    def test_038(self):
        """ Images Constructor - images = entries not a string """
        with pytest.raises(TypeError):
            images = Images([0], [0])
        
    def test_039(self):
        """ Images Constructor - images = image not exist """
        with pytest.raises(FileNotFoundError):
            images = Images(["files/nonexist.jpg"], [0])
        
    def test_040(self):
        """ Images Constructor - labels not a string """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], ['a'])
        
    def test_041(self):
        """ Images Constructor - labels not specified """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"])
        
    def test_042(self):
        """ Images Constructor - labels not match images """
        with pytest.raises(IndexError):
            images = Images(["files/0_100.jpg"], [0, 1])
        
    def test_043(self):
        """ Images Constructor - labels is None """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], labels=None)
        
    def test_044(self):
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
        self.assertTrue(len(images[0].raw) > 0 )
        self.assertEqual(images[0].thumb, None )
        os.remove("collection.0_100.h5")
        
    def test_045(self):
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
        self.assertTrue(len(images[1].raw) > 0 )
        self.assertEqual(images[1].thumb, None)
        self.assertEqual(images.name, 'collection.0_100')
        os.remove("collection.0_100.h5")
        
    def test_046(self):
        """ images properties dir, class """
        images = Images(["files/0_100.jpg"], labels=[2], dir="tmp")
        self.assertTrue(images.dir, "tmp")
        self.assertTrue(images.label, [2])
        os.remove("tmp/collection.0_100.h5")
        os.rmdir("tmp")
        
    def test_047(self):
        """ images constructor - dir not a string """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], labels=[0], dir=0)
        
    def test_048(self):
        """ images constructor - collection not a string """
        with pytest.raises(TypeError):
            images = Images(["files/0_100.jpg"], labels=[0], collection=0)
        
    def test_049(self):
        """ images properties dir, class """
        images = Images(["files/0_100.jpg"], labels=[2], name="foobar")
        self.assertEqual(images.name, 'foobar')
        self.assertTrue(os.path.isfile("foobar.h5"))
        os.remove("foobar.h5")
        
    def test_050(self):
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
        self.assertTrue(len(images[1].raw) > 0 )
        self.assertEqual(images[1].thumb, None)
        self.assertEqual(images.name, 'collection.0_100')
        os.remove("collection.0_100.h5")
                
    def test_051(self):
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
            
    def test_052(self):
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
            
    def test_053(self):
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
        
    def test_054(self):
        """ Images - time """
        images = Images(["files/0_100.jpg"], labels=[2])
        self.assertEqual(len(images), 1)
        self.assertTrue(images.time > 0)
        os.remove("collection.0_100.h5")
        
    def test_055(self):
        """ Images - create dir"""
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg'], 2, name='foobar', dir='tmp2')
        self.assertTrue(os.path.isfile("tmp2/foobar.h5"))
        os.remove("tmp2/foobar.h5")
        os.rmdir('tmp2')
        
    def test_056(self):
        """ Images - split not an float """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(TypeError):
            images.split = 'a'
        os.remove('foobar.h5')
        
    def test_057(self):
        """ Images - split not a valid range """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(ValueError):
            images.split = 0.0
        with pytest.raises(ValueError):
            images.split = 1.0
        os.remove('foobar.h5')
        
    def test_058(self):
        """ Images - split by default """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        x1, x2, y1, y2 = images.split
        self.assertEquals(len(x1), 3)
        self.assertEquals(len(x2), 1)
        self.assertEquals(len(y1), 3)
        self.assertEquals(len(y2), 1)
        os.remove('collection.0_100.h5')
        
    def test_059(self):
        """ Images - split, set percent """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        images.split = 0.5
        self.assertEqual(len(images._train), 2)
        self.assertEqual(len(images._test), 2)
        os.remove('collection.0_100.h5')
        
    def test_060(self):
        """ Images - split, percent specified """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        images.split = 0.25
        x1, x2, y1, y2 = images.split
        self.assertEquals(len(x1), 1)
        self.assertEquals(len(x2), 3)
        self.assertEquals(len(y1), 1)
        self.assertEquals(len(y2), 3)
        os.remove('collection.0_100.h5')
        
    def test_061(self):
        """ Images - iterate through collection """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4])
        images.split = 0.75
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), None)
        os.remove('collection.0_100.h5')
            
    def test_062(self):
        """ Images - iterate 2nd pass """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg', 'files/3_100.jpg'], [1,2,3,4,5], name='foobar')
        images.split = 0.5
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), None)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(len(next(images)), 2)
        self.assertEqual(next(images), None)
        os.remove('foobar.h5')
        
    def test_063(self):
        """ Images - minibatch not an integer """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(TypeError):
            images.minibatch = 'a'
        os.remove('foobar.h5')
        
    def test_064(self):
        """ Images - minibatch invalid range """
        images = Images(['files/0_100.jpg', 'files/1_100.jpg', 'files/2_100.jpg', 'files/0_100g.jpg'], [1,2,3,4], name='foobar')
        with pytest.raises(ValueError):
            images.minibatch = 0
        with pytest.raises(ValueError):
            images.minibatch = 4
        os.remove('foobar.h5')
        
    def test_065(self):
        """ minibatch - fetch """
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
        
    def done(self, image):
        self.isdone = True
        os.remove(image)