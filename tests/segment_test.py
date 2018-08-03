"""
Copyright, 2018(c), Andrew Ferlitsch
"""
from gapml.segment import Segment
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
        """ Segment constructor - text is not a string"""
        with pytest.raises(TypeError):
            segment = Segment(12)
        
    def test_002(self):
        """ Segment constructor - no params """
        with pytest.raises(TypeError):
            segment = Segment()
        
    def test_003(self):
        """ paragraph """
        with open("files/segment_para.txt", "r") as f:
            text = f.read()
        segment = Segment(text)
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'This is a first paragraph\nand continues to next line.'}, {'tag': 1002, 'text': 'Then this is the second\nparagraph.'}])

    def test_004(self):
        """ single paragraph """
        segment = Segment("first\nsecond")
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'first\nsecond'}])
    
    def test_005(self):
        """ single paragraph with training whitespace"""
        segment = Segment("first\nsecond\n\n")
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'first\nsecond'}])
        
    def test_006(self):
        """ headings """
        with open("files/segment_heading.txt", "r") as f:
            text = f.read()
        segment = Segment(text)
        self.assertEquals(segment.segments, [{'tag': 1001, 'text': 'TABLE OF CONTENTS'}, {'tag': 1001, 'text': '1. Section One'}, {'tag': 1001, 'text': '2. Section Two'}])
        
    def test_007(self):
        """ page nimbering - top of page """
        segment = Segment("Page 1\nfirst\nsecond\n\n")
        self.assertEquals(segment.segments, [{'tag': 1003, 'text': 'Page 1'}, {'tag': 1002, 'text': 'first\nsecond'}])     
        
    def test_008(self):
        """ page nimbering- bottom of page """
        segment = Segment("first\nsecond\n\nPage 1\n")
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'first\nsecond'}, {'tag': 1003, 'text': 'Page 1'}])    
        
    def test_009(self):
        """ page numbering- abbr """
        segment = Segment("first\nsecond\n\np 1\n")
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'first\nsecond'}, {'tag': 1003, 'text': 'p 1'}])
        segment = Segment("first\nsecond\n\np. 1\n")
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'first\nsecond'}, {'tag': 1003, 'text': 'p. 1'}])   
        
    def test_010(self):
        """ more page numbering """
        with open("files/segment_page.txt", "r") as f:
            text = f.read()
        segment = Segment(text)
        self.assertEquals(segment.segments, [{'tag': 1002, 'text': 'first para'}, {'tag': 1003, 'text': 'Page 1'}, {'tag': 1002, 'text': 'second para'}, {'tag': 1003, 'text': 'p. 2'}, {'tag': 1002, 'text': 'third para'}, {'tag': 1003, 'text': '3'}])   
        
    def test_011(self):
        """ page numbering - page - """
        segment = Segment("- 2 -\n")
        self.assertEquals(segment.segments, [{'tag': 1003, 'text': '- 2 -'}])
        
