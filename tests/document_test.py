"""
Copyright, 2018(c), Andrew Ferlitsch
"""
from splitter import Document, Page
from pdf_res import PDFResource
import unittest
import pytest
import os
import sys
import time

class MyTest(unittest.TestCase):
        
    def setup_class(self):
        self.isdone = False
        with open("test.txt", "w") as f:
            f.write("foo")
        with open("empty.txt", "w") as f:
            pass
        with open("toosmall.pdf", "w") as f:
            f.write("foo")
            
    def teardown_class(self):
        os.remove("test.txt")
        os.remove("empty.txt")
        os.remove("toosmall.pdf")
    
    def test_001(self):
        """ Document Constructor - no document argument """
        document = Document()
        self.assertEqual(document.document, None)
        
    def test_002(self):
        """ Document Constructor - document = None """
        document = Document(None)
        self.assertEqual(document.document, None)
        
    def test_003(self):
        """ Document Constructor - document = not a string """
        with pytest.raises(TypeError):
            document = Document(1)
        
    def test_004(self):
        """ Document Constructor - document = nonexistent document """
        with pytest.raises(FileNotFoundError):
            document = Document("files/nonexist.txt")
        
    def test_005(self):
        """ Document Constructor - document = valid text document """
        document = Document("test.txt")
        self.assertEqual(document.document, "test.txt")
        self.assertEqual(document.name, "test")
        self.assertEqual(len(document), 1)
        self.assertEqual(document.text, ["foo"])
        self.assertTrue(os.path.isfile("test1.txt"))
        self.assertTrue(os.path.isfile("test1.json"))
        os.remove("test1.txt")
        os.remove("test1.json")
        
    def test_006(self):
        """ Document Constructor - document = valid pdf document """
        document = Document("files/4page.pdf")
        self.assertEqual(document.document, "files/4page.pdf")
        self.assertEqual(document.name, "4page")
        self.assertEqual(len(document), 4)
        for i in range(1,5):
            self.assertTrue(os.path.isfile("4page" + str(i) + ".pdf"))
            self.assertTrue(os.path.isfile("4page" + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("4page" + str(i) + ".json"))
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_007(self):
        """ Document Constructor - document = valid pdf document with page directory specified """
        document = Document("files/4page.pdf", "./")
        self.assertEqual(document.document, "files/4page.pdf")
        self.assertEqual(document.name, "4page")
        self.assertEqual(len(document), 4)
        for i in range(1,5):
            self.assertTrue(os.path.isfile("4page"  + str(i) + ".pdf"))
            self.assertTrue(os.path.isfile("4page"  + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("4page"  + str(i) + ".json"))
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")  
            os.remove("4page" + str(i) + ".json")      
        
    def test_008(self):
        """ Document constructor - keyword argument: document """
        document = Document(document="test.txt")
        self.assertEqual(document.name, "test")
        self.assertEqual(len(document), 1)
        os.remove("test1.txt")
        os.remove("test1.json")
        
    def test_009(self):
        """ Document constructor - keyword argument: dir """
        document = Document(dir="./")
        self.assertEqual(document.dir, "./")

    def test_010(self):
        """ Document constructor - directory is not a string """
        with pytest.raises(TypeError):
            document = Document(dir=12)
        
    def test_011(self):
        """ Document constructor - store single page text file for raw text document """
        document = Document("test.txt", "./")
        self.assertEqual(document.name, "test")
        self.assertTrue(os.path.isfile("test1.txt"))
        os.remove("test1.txt")
        os.remove("test1.json")
        
    def test_012(self):
        """ Document constructor - non-ascii characters in document (UTF-8 encoding) """
        document = Document("files/7page.pdf", "./")
        self.assertEqual(document[0].text.strip()[0:7], "MEDICAL")
        for i in range(1,8):
            os.remove("7page" + str(i) + ".pdf")
            os.remove("7page" + str(i) + ".txt")
            os.remove("7page" + str(i) + ".json")
        
    def test_013(self):
        """ Document constructor - create page directory """
        document = Document("files/4page.pdf", "tests2")
        self.assertTrue(os.path.isdir("tests2"))
        for i in range(1,5):
            os.remove("tests2/4page" + str(i) + ".pdf")
            os.remove("tests2/4page" + str(i) + ".txt")
            os.remove("tests2/4page" + str(i) + ".json")
        os.removedirs("tests2")
        
    def test_014(self):
        """ Document constructor - cannot create page directory """
        with pytest.raises(FileNotFoundError):
            document = Document("files/4page.pdf", "tests3/foobar")
        
    def test_015(self):
        """ Document document setter - nonexistent file """
        document = Document()
        with pytest.raises(FileNotFoundError):
            document.document = "files/nonexist.txt"
        
    def test_016(self):
        """ Document document setter - valid text file """
        document = Document()
        document.document = "test.txt"
        self.assertEqual(document.name, "test")
        self.assertEqual(len(document), 1)
        self.assertEqual(document.text, ["foo"])
        os.remove("test1.txt")
        
    def test_017(self):
        """ Document document setter - valid PDF file """
        document = Document()
        document.document = "files/4page.pdf"
        self.assertEqual(document.document, "files/4page.pdf")
        self.assertEqual(document.name, "4page")
        self.assertEqual(len(document), 4)
        for i in range(1,5):
            self.assertTrue(os.path.isfile("4page" + str(i) + ".pdf"))
            self.assertTrue(os.path.isfile("4page" + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("4page" + str(i) + ".json"))
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_018(self):
        """ Document document setter - valid PDF file with page directory """
        document = Document()
        document.dir = "./"
        document.document = "files/4page.pdf"
        self.assertEqual(document.name, "4page")
        self.assertEqual(len(document), 4)
        for i in range(1,5):
            self.assertTrue(os.path.isfile("4page" + str(i) + ".pdf"))
            self.assertTrue(os.path.isfile("4page" + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("4page" + str(i) + ".json"))
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_019(self):
        """ Document document setter - not a string """
        document = Document()
        with pytest.raises(TypeError):
            document.document = 12
        
    def test_020(self):
        """ Document dir setter """
        document = Document()
        document.dir = "./"
        self.assertEqual(document.dir, "./")
            
    def test_021(self):
        """ Document dir setter - not a string """
        document = Document()
        with pytest.raises(TypeError):
            document.dir = 12
        
    def test_022(self):
        """ Document text getter - PDF file """
        document = Document("files/4page.pdf", "./")
        self.assertEqual(document.text[0].strip()[0:6], "TIER 1")
        self.assertEqual(document.text[1].strip()[0:15], "COVERED MEDICAL")
        self.assertEqual(document.text[2].strip()[0:14], "Emergency mean")
        self.assertEqual(document.text[3].strip()[0:15], "Maximum Benefit")
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_023(self):
        """ Document text setter """
        document = Document("files/4page.pdf", "./")
        document.text[0] = "goo"
        # TODO
        #self.assertEqual(document.text[0], "goo")
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_024(self):
        """ Document [] getter """
        document = Document("files/4page.pdf", "./")
        for i in range(1,5):
            self.assertEqual(document[i-1].path, "./4page" + str(i) + ".pdf")
        self.assertEqual(document[0].text.strip()[0:6], "TIER 1")
        self.assertEqual(document[1].text.strip()[0:15], "COVERED MEDICAL")
        self.assertEqual(document[2].text.strip()[0:14], "Emergency mean")
        self.assertEqual(document[3].text.strip()[0:15], "Maximum Benefit")
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_025(self):
        """ Document [] getter - index out of range """
        document = Document("files/4page.pdf", "./")
        self.assertEqual(document[4], None)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".json")
        
    def test_026(self):
        """ Document [] setter """
        document = Document("test.txt")
        page = Page(text='hello world')
        document[0] = page
        self.assertEqual(document[0].text, "hello world")
        os.remove("test1.txt")    
        
    def test_027(self):
        """ Document [] setter - not a Page """
        document = Document("test.txt")
        with pytest.raises(TypeError):
            document[0] = 12
        os.remove("test1.txt")  
        
    def test_028(self):
        """ Document [] setter - not an int index """
        document = Document("test.txt")
        page = Page(text='hello world')
        with pytest.raises(TypeError):
            document['abc'] = page
        os.remove("test1.txt")

    def test_029(self):
        """ Document classification getter (default) """
        document = Document(dir="./")
        self.assertEqual(document.label, None)
        
    def test_030(self):
        """ Document classification getter/setter """
        document = Document(dir="./")
        document.label = "foobar"
        self.assertEqual(document.label, "foobar")
        
    def test_031(self):
        """ Document classification setter - not a string """
        document = Document()
        with pytest.raises(TypeError):
            document.label = 12
        
    def test_032(self):
        """ Document overridden str() """
        document = Document()
        document.label = "foobar"
        self.assertEqual(str(document), "foobar")
        
    def test_033(self):
        """ Document overridden str() """
        document = Document("test.txt")
        document += Page()
        self.assertEqual(len(document), 2)  
        os.remove("test1.txt")       
        
    def test_034(self): 
        """ Document size getter - zero """
        document = Document()
        self.assertEqual(document.size, 0)          
        
    def test_035(self): 
        """ Document size getter - non-zero """
        document = Document("files/4page.pdf", "./")
        self.assertEqual(document.size, 32667)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt") 
            os.remove("4page" + str(i) + ".json") 

    def test_036(self): 
        """ Document type getter - None """
        document = Document()
        self.assertEqual(document.type, None)                 
        
    def test_037(self): 
        """ Document type getter - PDF """
        document = Document("files/4page.pdf", "./")
        self.assertEqual(document.type, "pdf")
        for i in range(1,5):
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".txt")   
            os.remove("4page" + str(i) + ".json")      
        
    def test_038(self): 
        """ Document - empty file """ 
        with pytest.raises(IOError): 
            document = Document("files/empty.txt")        
        
    def test_039(self): 
        """ Document - too small PDF""" 
        with pytest.raises(IOError): 
            document = Document("files/toosmall.pdf") 
        
    def test_040(self): 
        """ Document - color PDF with overlay """
        document = Document("files/5page.pdf", "./")
        self.assertEqual(len(document), 5)
        for i in range(1,6):
            self.assertTrue(os.path.isfile("5page"  + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("5page"  + str(i) + ".json"))
        for i in range(1,6):
            os.remove("5page" + str(i) + ".txt")
            os.remove("5page" + str(i) + ".pdf") 
            os.remove("5page" + str(i) + ".json") 
        
    def test_041(self): 
        """ Document - invoice PDF """
        document = Document("files/invoice.pdf", "./")
        self.assertEqual(len(document), 1)
        self.assertTrue(os.path.isfile("invoice1.txt"))
        self.assertTrue(os.path.isfile("invoice1.pdf"))
        self.assertTrue(os.path.isfile("invoice1.json"))
        os.remove("invoice1.txt")
        os.remove("invoice1.pdf")
        os.remove("invoice1.json")
		
    def test_042(self):
        """ Document - Adobe Example """
        document = Document("files/adobepdf.pdf", "./")
        self.assertEqual(len(document), 4)
        scanned, quality = document.scanned
        self.assertFalse(scanned)
        self.assertEquals(quality, 0)
        for i in range(1,5):
            self.assertTrue(os.path.isfile("adobepdf" + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("adobepdf" + str(i) + ".pdf"))
            self.assertTrue(os.path.isfile("adobepdf" + str(i) + ".json"))
        for i in range(1,5):
            os.remove("adobepdf" + str(i) + ".txt")
            os.remove("adobepdf" + str(i) + ".pdf") 
            os.remove("adobepdf" + str(i) + ".json") 

    ### SCANNED PDF ###
        
    def test_043(self): 
        """ Document - scanned PDF - single page, text file is empty """
        document = Document("files/scan.pdf", "./")
        self.assertEqual(len(document), 1)
        self.assertTrue(os.path.isfile("scan1.png"))
        scanned, quality = document.scanned
        self.assertTrue(scanned)
        self.assertTrue(quality > 0)
        l = len(document.pages[0])
        self.assertTrue(l >= 83 and l <= 100)
        os.remove("scan1.txt")
        os.remove("scan1.pdf")
        os.remove("scan1.png")
        os.remove("scan1.json")
        
    def test_044(self): 
        """ Document - scanned PDF - multi page, no text, but noise """
        document = Document("files/4scan.pdf", "./")
        self.assertEqual(len(document), 4)
        scanned, quality = document.scanned
        self.assertTrue(scanned)
        self.assertTrue(quality > 0)
        for i in range(1,5):
            self.assertTrue(os.path.isfile("4scan"  + str(i) + ".png"))
            self.assertTrue(os.path.isfile("4scan"  + str(i) + ".json"))
        for i in range(1,5):
            os.remove("4scan" + str(i) + ".txt")
            os.remove("4scan" + str(i) + ".pdf")
            os.remove("4scan" + str(i) + ".png")
            os.remove("4scan" + str(i) + ".json")
        
    def test_045(self): 
        """ Document - scanned PDF - single page, set resolution """
        Document.RESOLUTION = 100
        document = Document("files/scan.pdf", "./")
        self.assertEqual(len(document), 1)
        scanned, quality = document.scanned
        self.assertTrue(scanned)
        self.assertTrue(quality > 0)
        self.assertTrue(os.path.isfile("scan1.png"))
        l = len(document.pages[0])
        self.assertTrue(l >= 97 and l <= 110)
        os.remove("scan1.txt")
        os.remove("scan1.pdf")
        os.remove("scan1.png")
        os.remove("scan1.json")
        
    def test_046(self): 
        """ Document - scanned PDF - single page, with text back """
        Document.RESOLUTION = 200
        document = Document("files/scan_textback.pdf", "./")
        self.assertEqual(len(document), 1)
        scanned, quality = document.scanned
        self.assertFalse(scanned)
        self.assertEquals(quality, 0)
        self.assertTrue(os.path.isfile("scan_textback1.txt"))
        self.assertFalse(os.path.isfile("scan_textback1.png"))
        l = len(document.pages[0])
        os.remove("scan_textback1.txt")
        os.remove("scan_textback1.pdf")
        os.remove("scan_textback1.json")
        
    def test_047(self): 
        """ Document - scanned PDF - single page, non-text example """
        Document.RESOLUTION = 200
        document = Document("files/nontext.pdf", "./")
        self.assertEqual(len(document), 1)
        self.assertTrue(document.scanned)
        self.assertTrue(os.path.isfile("nontext1.txt"))
        self.assertTrue(os.path.isfile("nontext1.png"))
        l = len(document.pages[0])
        os.remove("nontext1.txt")
        os.remove("nontext1.pdf")
        os.remove("nontext1.png")
        os.remove("nontext1.json")
        
    def test_048(self): 
        """ Document - PNG text """
        Document.RESOLUTION = 200
        document = Document("files/text.png", "./")
        self.assertEqual(len(document), 1)
        self.assertTrue(os.path.isfile("text1.txt"))
        self.assertTrue(os.path.isfile("text1.png"))
        self.assertTrue(document.scanned)
        l = len(document.pages[0])
        self.assertTrue(l >= 25 and l <= 30)
        self.assertTrue(document[0].pageno, 1)
        os.remove("text1.txt")
        os.remove("text1.png")
        
    def test_049(self): 
        """ Document - JPG text """
        Document.RESOLUTION = 300
        document = Document("files/text.jpg", "./")
        self.assertEqual(len(document), 1)
        self.assertTrue(document.scanned)
        self.assertTrue(os.path.isfile("text1.txt"))
        self.assertTrue(os.path.isfile("text1.jpg"))
        self.assertTrue(os.path.isfile("text1.json"))
        l = len(document.pages[0])
        self.assertTrue(l >= 14 and l <= 30)
        os.remove("text1.txt")
        os.remove("text1.jpg")
        os.remove("text1.json")
        
    def test_050(self): 
        """ Document - TIF text """
        document = Document("files/6page.tif", "./")
        self.assertEqual(len(document), 6)
        for i in range(1,7):
            self.assertTrue(os.path.isfile("6page" + str(i) + ".tif"))
            self.assertTrue(os.path.isfile("6page" + str(i) + ".txt"))
            self.assertTrue(os.path.isfile("6page" + str(i) + ".json"))
        for i in range(1,7):
            os.remove("6page" + str(i) + ".txt")
            os.remove("6page" + str(i) + ".tif")
            os.remove("6page" + str(i) + ".json")
        
    ### ASYNC PROCESSING ###
        
    def test_051(self):
        """ async processing """
        document = Document("files/invoice.pdf", "./", self.done)
        time.sleep(6)
        self.assertTrue(self.isdone)
        os.remove("invoice1.pdf")
        os.remove("invoice1.txt")
        os.remove("invoice1.json")
        
    def test_052(self):
        """ document load from store """
        document = Document("files/4page.pdf", "./")
        document = Document()
        document.load("files/4page.pdf", "./")
        self.assertEquals(len(document), 4)
        self.assertTrue(document[0].words != None)
        self.assertTrue(document[0].text != None)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".json")

    def test_053(self):
        # page.path for .txt file
        document = Document("test.txt")
        self.assertTrue(os.path.isfile("test1.json"))
        self.assertEquals(document[0].path, "./test1.txt")
        os.remove("test1.txt")
        os.remove("test1.json")

    def test_054(self):
        """ bag of words / freqDist """
        document = Document("files/4page.pdf", "./")
        self.assertTrue(document.bagOfWords != None)
        self.assertTrue(document.freqDist != None)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".json")

    def test_055(self):
        """ config is not a list """
        with pytest.raises(TypeError):
            document = Document(config=12)

    def test_056(self):
        """ config entry is not a string """
        with pytest.raises(TypeError):
            document = Document(config=[12])

    def test_057(self):
        """ config is None """
        document = Document("files/4page.pdf", "./", config=None)
        self.assertTrue(document.bagOfWords != None)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".json")

    def test_058(self):
        """ config is empty """
        document = Document("files/4page.pdf", "./", config=[])
        self.assertTrue(document.bagOfWords != None)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".json")

    def test_059(self):
        """ config has multiple entries """
        document = Document("files/4page.pdf", "./", config=['bare', 'pos', 'roman'])
        self.assertTrue(document.bagOfWords != None)
        for i in range(1,5):
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".json")

    def test_060(self):
        """ config stem is invalid """
        with pytest.raises(AttributeError):
            document = Document(config=['stem'])

    def test_061(self):
        """ config stem is invalid """
        with pytest.raises(AttributeError):
            document = Document(config=['stem='])

    def test_062(self):
        """ config stem is invalid """
        with pytest.raises(AttributeError):
            document = Document(config=['stem=foo'])

    def test_063(self):
        """ config setting not valid """
        with pytest.raises(AttributeError):
            document = Document(config=['foo'])

    def test_064(self):
        """ config stem is valid """
        document = Document("files/4page.pdf", "./", config=['stem=gap'])
        document = Document("files/4page.pdf", "./", config=['stem=porter'])
        document = Document("files/4page.pdf", "./", config=['stem=snowball'])
        document = Document("files/4page.pdf", "./", config=['stem=lancaster'])
        document = Document("files/4page.pdf", "./", config=['stem=lemma'])
        for i in range(1,5):
            os.remove("4page" + str(i) + ".txt")
            os.remove("4page" + str(i) + ".pdf")
            os.remove("4page" + str(i) + ".json")

    def test_065(self):
        """ config segment txt """
        document = Document('files/segment_para.txt', './', config=['segment'])
        self.assertEquals(document[0].size, 91)
        self.assertEquals(document[0].text, 'This is a first paragraph\nand continues to next line.\n\nThen this is the second\nparagraph.')
        self.assertEquals(len(document[0].words), 2)
        os.remove('segment_para1.txt')
        os.remove('segment_para1.json')

    def test_066(self):
        """ config segment pdf """
        document = Document('files/invoice.pdf', './', config=['segment'])
        self.assertEquals(len(document[0].words), 15)
        os.remove('invoice1.pdf')
        os.remove('invoice1.txt')
        os.remove('invoice1.json')

    def test_067(self):
        """ config segment image """
        document = Document('files/text.png', './', config=['segment'])
        self.assertEquals(len(document[0].words), 7)
        os.remove('text1.png')
        os.remove('text1.txt')
        os.remove('text1.json')

    def test_068(self):
        """ config - spell checker - invalid """
        with pytest.raises(AttributeError):
            document = Document(config=['spell'])

    def test_069(self):
        """ config - spell checker - invalid """
        with pytest.raises(AttributeError):
            document = Document(config=['spell='])

    def test_070(self):
        """ config - spell checker - invalid """
        with pytest.raises(AttributeError):
            document = Document(config=['spell=foo'])            
            
    def test_071(self):
        """ config - spell checker - norvig """
        with open("spell.txt", "w") as f:
            f.write("mispell speling similiar")
        Document.WORDDICT = 'norvig'
        document = Document('spell.txt')
        page = document[0]
        os.remove('spell.txt')
        os.remove('spell1.txt')
        os.remove('spell1.json')
        
    def test_072(self): 
        """ Document - scanned PDF - scancheck with norvig """
        Document.WORDDICT = 'norvig'
        document = Document("files/scan.pdf", "./")
        self.assertEqual(len(document), 1)
        scanned, quality = document.scanned
        self.assertTrue(scanned)
        self.assertTrue(quality > 0)
        self.assertTrue(os.path.isfile("scan1.png"))
        os.remove("scan1.txt")
        os.remove("scan1.pdf")
        os.remove("scan1.png")
        os.remove("scan1.json")
        
    def test_073(self): 
        """ Document - scanned PDF - disable scan check """
        Document.SCANCHECK = 0
        document = Document("files/scan.pdf", "./")
        self.assertEqual(len(document), 1)
        scanned, quality = document.scanned
        self.assertTrue(scanned)
        self.assertEquals(quality, 1)
        self.assertTrue(os.path.isfile("scan1.png"))
        os.remove("scan1.txt")
        os.remove("scan1.pdf")
        os.remove("scan1.png")
        os.remove("scan1.json")
        
    def test_074(self):
        """ Document - lang type, page 1 """
        document = Document("files/lang-en.txt", "./")
        self.assertEquals(document.lang, 'en')
        document = Document("files/lang-sp.txt", "./")
        self.assertEquals(document.lang, 'sp')
        document = Document("files/lang-fr.txt", "./")
        self.assertEquals(document.lang, 'fr')
        for lang in ['en', 'sp', 'fr']:
            os.remove("lang-" + lang + "1.txt")
            os.remove("lang-" + lang + "1.json")
		
    def done(self, document):
        self.isdone = True
        
        
def towords(list):
    words = []
    for word in list:
        words.append(word['word'])
    return words