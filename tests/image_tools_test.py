from gapml.utils.img_tools import ImgUtils
import unittest
import pytest
import os

class MyTest(unittest.TestCase):

    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def test_001(self):
        
        with pytest.raises(TypeError):
            gap = ImgUtils(root_path=1)
