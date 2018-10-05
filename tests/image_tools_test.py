from gapml.utils.img_tools import ImgUtils
import unittest
import pytest
import os
import shutil

class MyTest(unittest.TestCase):

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_001(self):
        """ ImgUtils Constructor - directory = not a string """
        with pytest.raises(TypeError):
            gap = ImgUtils(root_path=1)

    def test_002(self):
        """ transform dataset from tree 1 to tree 2 """
        gap = ImgUtils(root_path='files/imtest4')
        gap.transform(shufle=True, img_split=0.2)
        self.assertTrue(os.path.exists('files/imtest4_t2'))
        self.assertTrue(os.path.exists('files/imtest4_t2/errors'))
        self.assertTrue(os.path.exists('files/imtest4_t2/test'))
        self.assertTrue(os.path.exists('files/imtest4_t2/test/test'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_tr'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_tr/daisy'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_tr/dandelion'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_tr/roses'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_val'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_val/daisy'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_val/dandelion'))
        self.assertTrue(os.path.exists('files/imtest4_t2/train_val/roses'))

    def test_003(self):
        """ Setter - transform """
        gap = ImgUtils(root_path='files/imtest4_t2/train_tr')
        gap.transf = '2to1'
        self.assertEqual(gap.transf, '2to1')

    def test_004(self):
        """ transform dataset from tree 2 to tree 1  """
        gap = ImgUtils(root_path='files/imtest4_t2/train_tr')
        gap.transf = '2to1'
        gap.transform()
        self.assertTrue(os.path.exists('files/imtest4'))
        self.assertTrue(os.path.exists('files/imtest4/daisy'))
        self.assertTrue(os.path.exists('files/imtest4/dandelion'))
        self.assertTrue(os.path.exists('files/imtest4/roses'))

    def test_005(self):
        """ getting a sample from tree 1 to tree 1 """
        gap = ImgUtils(root_path='files/imtest4')
        gap.img_container(action='copy', spl=5)
        self.assertTrue(os.path.exists('files/imtest4_spl'))
        self.assertTrue(os.path.exists('files/imtest4_spl/daisy'))
        self.assertTrue(os.path.exists('files/imtest4_spl/dandelion'))
        self.assertTrue(os.path.exists('files/imtest4_spl/roses'))

    def test_006(self):
        """ getting a sample from tree 1 to tree 2 """
        gap = ImgUtils(root_path='files/imtest4', tree=2)
        gap.img_container(action='copy', spl=6, shufle=True, img_split=0.5)
        self.assertTrue(os.path.exists('files/imtest4_t2_spl'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/errors'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/test'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/test/test'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_tr'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_tr/daisy'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_tr/dandelion'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_tr/roses'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_val'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_val/daisy'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_val/dandelion'))
        self.assertTrue(os.path.exists('files/imtest4_t2_spl/train_val/roses'))

    def test_007(self):
        """ rename images with an id  - tree 1"""
        gap = ImgUtils(root_path='files/imtest4_spl')
        gap.img_rename()
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/3.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/4.jpg'))

    def test_008(self):
        """ rename images with label name_id  - tree 1 """
        gap = ImgUtils(root_path='files/imtest4_spl')
        gap.img_rename(text=True)
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/daisy_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/daisy_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/daisy_2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/roses_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/roses_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/roses_2.jpg'))

    def test_009(self):
        """ rename images with a specific word_id  - tree 1 """
        gap = ImgUtils(root_path='files/imtest4_spl')
        gap.img_rename(text='test')
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/test_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/test_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/test_2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/test_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/test_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/test_2.jpg'))

    def test_010(self):
        """ replace part of the image name with a specific woRD_id - tree 1 """
        gap = ImgUtils(root_path='files/imtest4_spl')
        gap.img_replace(old='st', new='sted', img_id=False)
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/tested_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/tested_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/daisy/tested_2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/tested_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/tested_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_spl/roses/tested_2.jpg'))
        shutil.rmtree('files/imtest4_spl')

    def test_011(self):
        """ rename images with an id  - tree 2 """
        gap = ImgUtils(root_path='files/imtest4_t2_spl/train_tr', tree=2)
        gap.img_rename()
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/daisy/0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/daisy/1.jpg'))

    def test_012(self):
        """ rename images with label name_id  - tree 2 """
        gap = ImgUtils(root_path='files/imtest4_t2_spl/train_tr', tree=2)
        gap.img_rename(text=True)
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/daisy_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/daisy_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/daisy_2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/roses/roses_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/roses/roses_1.jpg'))

    def test_013(self):
        """ rename images with a specific word_id  - tree 2 """
        gap = ImgUtils(root_path='files/imtest4_t2_spl/train_tr', tree=2)
        gap.img_rename(text='test')
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/daisy/test_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/daisy/test_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/roses/test_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/roses/test_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/roses/test_2.jpg'))

    def test_014(self):
        """ replace part of the image name with a specific woRD_id - tree 2 """
        gap = ImgUtils(root_path='files/imtest4_t2_spl/train_tr', tree=2)
        gap.img_replace(old='st', new='sted', img_id=False)
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/tested_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/tested_1.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_tr/daisy/tested_2.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/roses/tested_0.jpg'))
        self.assertTrue(os.path.isfile('files/imtest4_t2_spl/train_val/roses/tested_1.jpg'))
        shutil.rmtree('files/imtest4_t2_spl')
