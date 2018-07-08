from image import Image, Images
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
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        
    def test_010(self):
        """ image dir is None """
        image = Image("tests/0_100.jpg", dir=None)
        self.assertEqual(image.image, "tests/0_100.jpg")
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        
    def test_011(self):
        """ image dir is not-None - nonexist """
        image = Image("tests/0_100.jpg", dir='tmp')
        self.assertTrue(os.path.isfile("tmp/0_100.jpg"))
        self.assertTrue(os.path.isfile("tmp/0_100.h5"))
        os.remove("tmp/0_100.jpg")
        os.remove("tmp/0_100.h5")
        os.remove("tmp/0_100.thumbnail.jpg")
        
    def test_012(self):
        """ image dir is not-None - exist """
        image = Image("tests/0_100.jpg", dir='tmp')
        self.assertTrue(os.path.isfile("tmp/0_100.jpg"))
        self.assertTrue(os.path.isfile("tmp/0_100.h5"))
        os.remove("tmp/0_100.jpg")
        os.remove("tmp/0_100.h5")
        os.remove("tmp/0_100.thumbnail.jpg")
        os.rmdir("tmp")
        
    def test_013(self):
        """ label is None """
        with pytest.raises(TypeError):
            image = Image("tests/0_100.jpg", dir='tmp', label=None)
            
    def test_014(self):
        """ label is valid """
        image = Image("tests/0_100.jpg", dir='tmp', label=16)
        self.assertEqual(image.classification, 16)
        os.remove("tmp/0_100.jpg")
        os.remove("tmp/0_100.h5")
        os.remove("tmp/0_100.thumbnail.jpg")
        os.rmdir("tmp")
            
    def test_015(self):
        """ config is None """
        image = Image("tests/0_100.jpg", config=None)
        self.assertEqual(image.image, "tests/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
            
    def test_016(self):
        """ config is empty """
        image = Image("tests/0_100.jpg", config=[])
        self.assertEqual(image.image, "tests/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
            
    def test_017(self):
        """ config has non-string entry """
        with pytest.raises(TypeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=[1])
            
    def test_018(self):
        """ config has invalid setting """
        with pytest.raises(AttributeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=['foo'])
            
    def test_019(self):
        """ config has valid setting """
        image = Image("tests/0_100.jpg", config=['gray', 'grayscale'])
        image = Image("tests/0_100.jpg", config=['flat', 'flatten'])
        image = Image("tests/0_100.jpg", config=['normal', 'normalize'])
        image = Image("tests/0_100.jpg", config=['nostore'])
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
            
    def test_020(self):
        """ config resize has no value """
        with pytest.raises(AttributeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=['resize'])
        with pytest.raises(AttributeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=['resize='])
            
    def test_021(self):
        """ config resize is wrong format """
        with pytest.raises(AttributeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=['resize=1'])
        with pytest.raises(AttributeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=['resize=a,2'])
        with pytest.raises(AttributeError):
            image = Image("tests/0_100.jpg", dir='tmp', config=['resize=2,b'])
            
    def test_022(self):
        """ config - RGB to grayscale """
        image = Image("tests/0_100.jpg", config=['gray'])
        self.assertEqual(image.image, "tests/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        image = Image("tests/0_100.jpg", config=['grayscale'])
        self.assertEqual(image.image, "tests/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (100, 100))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
            
    def test_023(self):
        """ config - grayscale to RGB """
        image = Image("tests/0_100g.jpg")
        self.assertEqual(image.image, "tests/0_100g.jpg")
        self.assertEqual(image.name, "0_100g")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 4253)
        self.assertEqual(image.shape, (100, 100, 3))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100g.jpg"))
        self.assertTrue(os.path.isfile("0_100g.h5"))
        os.remove("0_100g.jpg")
        os.remove("0_100g.h5")
        os.remove("0_100g.thumbnail.jpg")   
        
    def test_024(self):
        """ config - resize """
        image = Image("tests/0_100.jpg", config=['resize=50,50'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (50, 50, 3))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        image = Image("tests/0_100.jpg", config=['resize=(200,200)'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (200, 200, 3))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")

    def test_025(self):
        """ config - flatten """
        image = Image("tests/0_100.jpg", config=['flat'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        image = Image("tests/0_100.jpg", config=['flatten'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")  
        
    def test_026(self):
        """ config - nostore """
        image = Image("tests/0_100.jpg", config=['flat', 'nostore'])
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.classification, 0)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertFalse(os.path.isfile("0_100.h5"))
        os.remove("0_100.jpg")
        
    def test_027(self):
        """ async processing """
        image = Image("tests/0_100.jpg", ehandler=self.done)
        time.sleep(3)
        self.assertTrue(self.isdone)
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        
    def test_028(self):
        """ png file """
        image = Image("tests/text.png")
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "png")
        os.remove("text.png")
        os.remove("text.h5")
        os.remove("text.thumbnail.png")
        
    def test_029(self):
        """ tif file """
        image = Image("tests/6page.tif", thumbnail=None)
        self.assertEqual(image.name, "6page")
        self.assertEqual(image.type, "tif")
        os.remove("6page.tif")
        os.remove("6page.h5")
        image = Image("tests/text.tiff", thumbnail=None)
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "tiff")
        os.remove("text.tiff")
        os.remove("text.h5")
        
    def test_030(self):
        """ bmp file """
        image = Image("tests/text.bmp")
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "bmp")
        os.remove("text.bmp")
        os.remove("text.h5")
        os.remove("text.thumbnail.bmp")
        
    def test_031(self):
        """ config - load """
        image = Image("tests/0_100.jpg", config=['flat'])
        self.assertTrue(os.path.isfile("0_100.h5"))
        image = None
        image = Image()
        image.load("tests/0_100.jpg")
        self.assertEqual(image.name, "0_100")
        self.assertEqual(image.type, "jpg")
        self.assertEqual(image.dir, "./")
        self.assertEqual(image.size, 3643)
        self.assertEqual(image.shape, (30000,))
        self.assertEqual(image.classification, 0)
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        
    def test_032(self):
        """ thumbnail """
        image = Image("tests/0_100.jpg", thumbnail=(32,32))
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertTrue(os.path.isfile("0_100.thumbnail.jpg"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        os.remove("0_100.thumbnail.jpg")
        
    def test_033(self):
        """ no thumbnail """
        image = Image("tests/0_100.jpg", thumbnail=None)
        self.assertTrue(os.path.isfile("0_100.h5"))
        self.assertFalse(os.path.isfile("0_100.thumbnail.jpg"))
        os.remove("0_100.jpg")
        os.remove("0_100.h5")
        
    def test_034(self):
        """ time """
        image = Image("tests/0_100.jpg", thumbnail=None)
        self.assertTrue(image.time > 0)
        os.remove("0_100.jpg")
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
            images = Images(["nonexist.jpg"], [0])
        
    def test_040(self):
        """ Images Constructor - labels not a string """
        with pytest.raises(TypeError):
            images = Images(["tests/0_100.jpg"], ['a'])
        
    def test_041(self):
        """ Images Constructor - labels not specified """
        with pytest.raises(TypeError):
            images = Images(["tests/0_100.jpg"])
        
    def test_042(self):
        """ Images Constructor - labels not match images """
        with pytest.raises(IndexError):
            images = Images(["tests/0_100.jpg"], [0, 1])
        
    def test_043(self):
        """ Images Constructor - labels is None """
        with pytest.raises(TypeError):
            images = Images(["tests/0_100.jpg"], labels=None)
        
    def test_044(self):
        """ Images Constructor - single file """
        images = Images(["tests/0_100.jpg"], labels=[2])
        self.assertEqual(len(images), 1)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.thumbnail.jpg"))
        self.assertTrue(os.path.isfile("batch.0_100.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("batch.0_100.h5")
        
    def test_045(self):
        """ Images Constructor - multi file """
        images = Images(["tests/0_100.jpg", "tests/1_100.jpg"], labels=[2, 2])
        self.assertEqual(len(images), 2)
        self.assertTrue(os.path.isfile("0_100.jpg"))
        self.assertTrue(os.path.isfile("0_100.thumbnail.jpg"))
        self.assertTrue(os.path.isfile("1_100.jpg"))
        self.assertTrue(os.path.isfile("1_100.thumbnail.jpg"))
        self.assertTrue(os.path.isfile("batch.0_100.h5"))
        self.assertTrue(images.images != None)
        self.assertEqual(len(images.images), 2)
        self.assertEqual(images.images[0].name, '0_100')
        self.assertEqual(images.images[1].name, '1_100')
        self.assertEqual(images[1].name, '1_100')
        self.assertEqual(images.name, 'batch.0_100')
        os.remove("0_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("1_100.jpg")
        os.remove("1_100.thumbnail.jpg")
        os.remove("batch.0_100.h5")
        
    def test_046(self):
        """ images properties dir, class """
        images = Images(["tests/0_100.jpg"], labels=[2], dir="tmp")
        self.assertTrue(images.dir, "tmp")
        self.assertTrue(images.classification, [2])
        os.remove("tmp/0_100.jpg")
        os.remove("tmp/0_100.thumbnail.jpg")
        os.remove("tmp/batch.0_100.h5")
        
    def test_047(self):
        """ images constructor - dir not a string """
        with pytest.raises(TypeError):
            images = Images(["tests/0_100.jpg"], labels=[0], dir=0)
        
    def test_048(self):
        """ images constructor - batch not a string """
        with pytest.raises(TypeError):
            images = Images(["tests/0_100.jpg"], labels=[0], batch=0)
        
    def test_049(self):
        """ images properties dir, class """
        images = Images(["tests/0_100.jpg"], labels=[2], batch="foobar")
        self.assertEqual(images.name, 'foobar')
        self.assertTrue(os.path.isfile("foobar.h5"))
        os.remove("0_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("foobar.h5")
            
    def test_050(self):
        """ images load - default batch name """
        images = Images(["tests/0_100.jpg", "tests/1_100.jpg"], labels=[1,2])
        images = Images()
        images.load("batch.0_100")
        self.assertEqual(images.name, 'batch.0_100')
        self.assertEqual(len(images), 2)
        os.remove("0_100.jpg")
        os.remove("1_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("1_100.thumbnail.jpg")
        os.remove("batch.0_100.h5")
            
    def test_051(self):
        """ images load - batch name """
        images = Images(["tests/0_100.jpg", "tests/1_100.jpg"], labels=[1,2], batch='foobar')
        images = Images()
        images.load("foobar")
        self.assertEqual(images.name, 'foobar')
        self.assertEqual(len(images), 2)
        os.remove("0_100.jpg")
        os.remove("1_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("1_100.thumbnail.jpg")
        os.remove("foobar.h5")
            
    def test_052(self):
        """ images async """
        self.isdone = False
        images = Images(["tests/0_100.jpg", "tests/1_100.jpg"], labels=[1,2], batch='foobar', ehandler=self.done) 
        time.sleep(3)
        self.assertTrue(self.isdone)
        self.assertEqual(images.name, 'foobar')
        self.assertEqual(len(images), 2)
        os.remove("0_100.jpg")
        os.remove("1_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("1_100.thumbnail.jpg")
        os.remove("foobar.h5")
        
    def test_053(self):
        """ Images - time """
        images = Images(["tests/0_100.jpg"], labels=[2])
        self.assertEqual(len(images), 1)
        self.assertTrue(images.time > 0)
        os.remove("0_100.jpg")
        os.remove("0_100.thumbnail.jpg")
        os.remove("batch.0_100.h5")

    def xxtest_031(self):
        """ gif file """,
        """  BUG: can't handle gifs """
        image = Image("tests/text.gif")
        self.assertEqual(image.name, "text")
        self.assertEqual(image.type, "gif")
        os.remove("text.gif")
        os.remove("text.h5")
        os.remove("text.thumbnail.gif")

		
    def done(self, image):
        self.isdone = True
        os.remove(image)
        
        