"""
Copyright, 2018(c), Andrew Ferlitsch
"""

from splitter import Page
from syntax import Words
from segment import Segment
import unittest
import pytest
import os
import sys

class MyTest(unittest.TestCase):
    def setup_class(self):
        with open("files/test.txt", "w") as f:
            f.write("foo")
            
    def teardown_class(self):
        os.remove("files/test.txt")

    def test_001(self):
        """ Page constructor - no parameters """
        page = Page()
        self.assertEqual(page.path,  None)
        self.assertEqual(page.text,  None)
        self.assertEqual(page.words, None)
        
    def test_002(self):
        """ Page constructor - path parameter """
        page = Page("files/test.txt")
        self.assertEqual(page.path,  "files/test.txt")
        self.assertEqual(page.text,  None)
        self.assertEqual(page.words, None)
        
    def test_003(self):
        """ Page constructor - path and text parameter """
        page = Page("files/test.txt", "foo")
        self.assertEqual(page.path,  "files/test.txt")
        self.assertEqual(page.text,  "foo")
        self.assertEqual(towords(page.words), [ "foo" ] )

    def test_004(self):
        """ Page constructor - path keyword parameter """
        page = Page(path="files/test.txt")
        self.assertEqual(page.path,  "files/test.txt")
        self.assertEqual(page.text,  None)
        self.assertEqual(page.words, None)

    def test_005(self):
        """ Page constructor - path keyword parameter """
        page = Page(text="foo")
        self.assertEqual(page.path,  None)
        self.assertEqual(page.text,  'foo')
        self.assertEqual(towords(page.words), ["foo"])

    def test_006(self):
        """ Page constructor - path is not a string """
        with pytest.raises(TypeError):
            page = Page(path=12)

    def test_007(self):
        """ Page constructor - text is not a string """
        with pytest.raises(TypeError):
            page = Page(text=12)

    def test_008(self):
        """ Page constructor - path is not a file """
        with pytest.raises(FileNotFoundError):
            page = Page(path='files/nonexist.txt')

    def test_009(self):
        """ Page path getter/setter """
        page = Page()
        self.assertEqual(page.path,  None)
        page.path = "files/test.txt"
        self.assertEqual(page.path,  'files/test.txt')

    def test_010(self):
        """ Page path setter - not a string """
        page = Page()
        with pytest.raises(TypeError):
            page.path = 12

    def test_011(self):
        """ Page path setter - not a valid file """
        page = Page()
        with pytest.raises(FileNotFoundError):
            page.path = 'files/nonexist.txt'

    def test_012(self):
        """ Page path setter - None """
        page = Page()
        page.path = None
        self.assertEqual(page.path,  None)

    def test_013(self):
        """ Page text getter/setter """
        page = Page()
        self.assertEqual(page.text,  None)
        page.text = "hello world"
        self.assertEqual(page.text,  'hello world')
        
    def test_014(self):
        """ Page text setter - not a string """
        page = Page()
        with pytest.raises(TypeError):
            page.text = 12
        
    def test_015(self):
        """ Page words getter - None """
        page = Page()
        self.assertEqual(page.words,  None)

    def test_016(self):
        """ Page classification getter (default) """
        page = Page()
        self.assertEqual(page.label, None)
        
    def test_017(self):
        """ Page classification getter/setter """
        page = Page()
        page.label = "foobar"
        self.assertEqual(page.label, "foobar")
        
    def test_018(self):
        """ Page classification setter - not an int """
        page = Page()
        with pytest.raises(TypeError):
            page.label = 10
        
    def test_019(self):
        """ Page overridden str() """
        page = Page()
        page.label = "foobar"
        self.assertEqual(str(page), "foobar")
        
    def test_020(self):
        """ Page overridden len() : length 0 """
        page = Page()
        self.assertEqual(len(page), 0)
        
    def test_021(self):
        """ Page overridden len() : length non-zero """
        page = Page()
        page.text = "hello world, goodbye"
        self.assertEqual(len(page), 3)
        
    def test_022(self):
        """ Page overridden += : text is None, self._text is None """
        page = Page()
        page += None
        self.assertEqual(page.text, None)
        
    def test_023(self):
        """ Page overridden += : text is None, self._text is non-None """
        page = Page(text="hello")
        page += None
        self.assertEqual(page.text, "hello")
        
    def test_024(self):
        """ Page overridden += : text is non-None, self._text is None """
        page = Page()
        page += "hello world"
        self.assertEqual(page.text, "hello world")
        
    def test_025(self):
        """ Page overridden += : text is non-None, self._text is non-None """
        page = Page(text="hello")
        page += "world"
        self.assertEqual(page.text, "hello world")
        
    def test_026(self):
        """ Page overridden += : words is non-None """
        page = Page(text="hello")
        self.assertEqual(len(page), 1)
        page += "world"
        self.assertEqual(page.text, "hello world")
        self.assertEqual(len(page), 2)
        
    def test_027(self):
        """ Page words getter  """
        page = Page(text="hello world")
        self.assertEqual(towords(page.words), ['hello', 'world'])
        
    def test_028(self):
        """ Page size getter - no page  """
        page = Page()
        self.assertEqual(page.size, 0)
        
    def test_029(self):
        """ Page size getter - no text  """
        page = Page(text="")
        self.assertEqual(page.size, 0)
        
    def test_030(self):
        """ Page size getter - text  """
        page = Page(text="hello world")
        self.assertEqual(page.size, 11)
        
    def test_031(self):
        """ Page number """
        page = Page("files/test.txt")
        self.assertEqual(page.pageno, None)
        page = Page("files/test.txt", pageno=2)
        self.assertEqual(page.pageno, 2)
        
    def test_032(self):
        """ Page store/load """
        page = Page(text="hello world, goodbye")
        page.store('files/tmp.txt')
        page._words = None
        page.load('files/tmp.txt')
        os.remove("files/tmp.txt")
        self.assertEqual(towords(page.words), ["hello", "world", "goodbye"])
        
    def test_033(self):
        """ Page store/load - unicode - latin """
        page = Page(text="hāllo world, goodbye")
        page.store('files/tmp.txt')
        page._words = None
        page.load('files/tmp.txt')
        self.assertEqual(towords(page.words), ["hāllo", "world", "goodbye"])
        os.remove("files/tmp.txt")
        Page.ROMAN = True
        page = Page(text="québec")
        page.store('files/tmp.txt')
        page._words = None
        page.load('files/tmp.txt')
        Page.ROMAN = False
        self.assertEqual(towords(page.words), ["quebec"])
        os.remove("files/tmp.txt")    
        
    def test_034(self):
        """ Page - Bag of Words """
        page = Page(text="zoo castle zoo bird zoo bird")
        self.assertEqual(page.bagOfWords, { 'zoo': 3, 'castle': 1, 'bird': 2 })    
        
    def test_035(self):
        """ Page - Word Counts """
        page = Page(text="zoo castle zoo bird zoo bird")
        self.assertEqual(page.freqDist, [( 'zoo', 3), ('bird', 2), ('castle', 1 )])   
        
    def test_036(self):
        """ Page - Term Frequency """
        page = Page(text="zoo castle zoo bird zoo bird zoo bird")
        self.assertEqual(page.termFreq, [( 'zoo', 0.5), ('bird', 0.375), ('castle', 0.125 )])   
        
    def test_037(self):
        """ segment option - empty list """
        page = Page(text=[])
        self.assertEqual(page.words, [])
        
    def test_038(self):
        """ segment option - element not a dictionary """
        with pytest.raises(TypeError):
            page = Page(text=[ 3 ])
        
    def test_039(self):
        """ segment option - paragraphs """
        segment = Segment('para 1\n\npara 2')
        page = Page(text=segment.segments)
        self.assertEqual(page.text, 'para 1\n\npara 2')
        self.assertEqual(page.size, 16)
        self.assertEqual(page.words, [{ 'tag': 1002, 'words': [{ 'tag': 0, 'word': 'para'}]}, { 'tag': 1002, 'words': [{ 'tag': 0, 'word': 'para'}]}])
        
    def test_040(self):
        """ segment option - path and segments """
        with open('files/segment_para.txt', 'r', encoding="utf-8") as f:
            segment = Segment(f.read())
        page = Page('files/segment_para.txt', segment.segments)
        
    def xtest_bugs(self):
        """ Page store/load - unicode - cryllic """
        page = Page(text="Й й")
        page.store('files/tmp.txt')
        page._words = None
        page.load('files/tmp.txt')
        os.remove("files/tmp.txt")
        self.assertEqual(towords(page.words), ["Й", "й"])
        
        
def towords(list):
    words = []
    for word in list:
        words.append(word['word'])
    return words