from segment import Segment
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
        """ """
        with open("tests/segment_para.txt", "r") as f:
            text = f.read()
        segment = Segment(text)
        self.assertEquals(segment.segments, [{'tag': 2, 'text': 'This is a first paragraph\nand continues to next line.'}, {'tag': 2, 'text': 'Then this is the second\nparagraph.'}])
        pass