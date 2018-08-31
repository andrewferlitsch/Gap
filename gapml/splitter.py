# -*- coding: utf-8 -*-
""" Splitter Module for Processing PDF Documents
Copyright, 2018(c), Andrew Ferlitsch
"""
#chcp 65001

version = '0.9.2'

import os.path
import re
import threading
import time
import shutil
import glob
import sys
import json
import shutil

from .segment import Segment
from .syntax import Words, Vocabulary, Norvig
from .pdf_res import PDFResource
from .lg.word2int_en import word2int_en
from .lg.word2int_fr import word2int_fr
from .lg.word2int_es import word2int_es
from .lg.word2int_it import word2int_it
from .lg.word2int_de import word2int_de

if shutil.which('gswin64c'):
    # Ghostscript executable for Windows.
    GHOSTSCRIPT = 'gswin64c'
elif shutil.which('gswin32c'):
    # Ghostscript executable for Windows.
    GHOSTSCRIPT = 'gswin32c'
elif shutil.which('gs'):
    # Ghostscript executable for Mac.
    GHOSTSCRIPT = 'gs'
else:
    # Linux
    GHOSTSCRIPT = 'gs'

TESSERACT   = "tesseract"
MAGICK      = "magick"

class Document(object):
    """ Base (super) Class for Classifying a Document """

    RESOLUTION = 300            # Resolution for OCR
    SCANCHECK  = 20             # Sample the first 20 words to determine scan quality
    WORDDICT   = 'norvig'       # Word Dictionary to look up words for scan check

    def __init__(self, document=None, dir="./", ehandler=None, config=None):
        """ Constructor for document object
        document - - path to the document
        dir - directory where to store extracted pages and text
        """
        self._document = document   # document path
        self._name     = None       # Name of document (no path and no suffix)
        self._label    = None       # classification of the document
        self._pages    = []         # document pages
        self._dir      = dir        # directory where extracted pages and text are stored
        self._type     = None       # file type of the document
        self._size     = 0          # byte size of the document
        self._ehandler = ehandler   # event completion handler for async execution of splitting
        self._time     = 0          # elapse time to do processing
        self._scanned  = False      # flag indicating if scanned PDF, TIFF or image capture
        self._quality  = 0          # quality (typically of scan) of the text extraction as a percentage estimate
        self._segment  = False      # Segment the text info regions
        self._bow      = None       # Bag of Words for the document
        self._freq     = None       # Frequency Distribution (word counts) for the document
        self._tf       = None       # Term Frequency (TF) for the document
        self._lang     = 'en'       # Document language

        # value must be a string
        if dir is not None and isinstance(dir, str) == False:
            raise TypeError("String expected for page directory path")

        if config is not None and isinstance(config, list) == False:
            raise TypeError("List expected for config settings")

        # NLP configuration
        if config is not None:
            for setting in config:
                if isinstance(setting, str) == False:
                     raise TypeError("String expected for each config setting")
                if setting == 'bare':
                    Page.BARE = True
                elif setting == 'pos':
                        Page.POS = True
                elif setting == 'roman':
                    Page.ROMAN = True
                elif setting == 'segment':
                    self._segment = True
                elif setting.startswith('stem'):
                    vals = setting.split('=')
                    if len(vals) == 2:
                        if vals[1] in ['gap', 'porter', 'snowball', 'lancaster', 'lemma']:
                            Page.STEM = vals[1]
                        else:
                            raise AttributeError("Setting stem set to an invalid value: " + vals[1])
                    else:
                        raise AttributeError("Setting stem not assigned to a value")
                elif setting.startswith('spell'):
                    vals = setting.split('=')
                    if len(vals) == 2:
                        if vals[1] in ['norvig']:
                            Page.SPELL = vals[1]
                        else:
                            raise AttributeError("Setting spell set to an invalid value: " + vals[1])
                    else:
                        raise AttributeError("Setting spell not assigned to a value")
                else:
                    raise AttributeError("Setting is not recognized: " + setting)

        # Verify that the document exists
        if self._document is not None:
            self._exist()
            # Process document synchronously
            if ehandler is None:
                self._collate(dir)
            # Process document asynchronously
            else:
                t = threading.Thread(target=self._async, args=(dir, ))
                t.start()

    def _async(self, dir):
        """ Asynchronous processing of the document """
        self._collate(dir)
        # signal user defined event handler when processing is done
        self._ehandler(self)

    def _exist(self):
        """ Check if document exists """
        # Document value must be a string
        if isinstance(self._document, str) == False:
            raise TypeError("String expected for document name")
        # Check that document exists
        if os.path.isfile(self._document) == False:
            raise FileNotFoundError(self._document)

        # Get the file name and file type of the document without the extension
        basename = os.path.splitext(os.path.basename(self._document))
        self._name = basename[0]
        self._type = basename[1][1:].lower()

        # Get the size of the document
        self._size = os.path.getsize(self._document)

        # Size sanity check
        if self._size == 0:
            raise IOError("The document is an empty file")
        if self._type == "pdf" and self._size < 100:
            raise IOError("The document is too small for a PDF document")

    def _collate(self, dir="./"):
        """ split document into pages and extract text
        dir - the directory where to store the split pages (defaults to current directory)
        """

        start = time.time()

        # If directory parameter does not end in a slash, add one
        if dir.endswith("/") == False:
                dir += "/"
        self._dir = dir

        # If directory does not exist, create it
        if dir != "./" and os.path.isdir(dir) == False:
            os.mkdir(dir)

        # A Text document is considered to have only one page
        if self._type == 'txt':
            text_file = dir + self._name + '1.txt'
            with open(self._document, 'r', encoding="utf-8") as f:
                text = f.read()
            with open(text_file, 'w', encoding="utf-8") as f:
                f.write(text)

            # Separate text into regions (headings, paragraphs, etc)
            if self._segment:
                segment = Segment(text)
                text = segment.segments
        
            page = Page(text_file, text, 1)
            self.__iadd__(page)
            # Store the tokenized text
            json_file = dir + self._name + '1.json'
            page.store(json_file)
        # Extract text from image files
        elif self._type == 'png' or self._type == 'jpg':
            img_file = dir + self._name + '1.' + self._type
            shutil.copy2( self._document, img_file)

            # Extract text from image
            text_file = dir + self._name + '1.txt'
            os.system(TESSERACT + ' ' + img_file + ' ' + dir + self._name + '1' + ' >nul 2>&1' )

            # Read text file
            with open(text_file, 'r', encoding="utf-8") as f:
                text = f.read()

            # Separate text into regions (headings, paragraphs, etc)
            if self._segment:
                segment = Segment(text)
                text = segment.segments
                
            page = Page(img_file, text, 1)
            self.__iadd__(page)
            # Store the tokenized text
            json_file = dir + self._name + '1.json'
            page.store(json_file)

            self._scanned = True
        # Split the PDF document into pages
        elif self._type == 'pdf':
            # Use ghostscript to get the number of pages
            os.system(GHOSTSCRIPT + ' -dBATCH -q -dNODISPLAY -c "("' + self.document + '") (r) file runpdfbegin pdfpagecount = quit" >tmp.tmp')

            with open("tmp.tmp", "r") as f:
                npages = int(f.read())
            os.remove("tmp.tmp")

            # Separate each PDF page and convert to text
            for n in range(npages):
                # Extract next page as a single page PDF
                pdf_file = dir + self._name + str(n+1) + '.pdf'
                os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile='  + pdf_file + ' -sPageList=' + str(n+1) + ' -sDEVICE=pdfwrite ' + self.document + ' >nul')

                # First Page
                if n == 0:
                    # Check if the resource definition indicates this is a scanned PDF
                    res = PDFResource(pdf_file)
                    if res.image == True and res.text == False:
                        self._scanned = True

                # Known to be a scanned PDF
                text_file = dir + self._name + str(n+1) + '.txt'
                if self._scanned == True:
                    # Extract scanned image
                    image_file = dir + self._name + str(n+1) + '.png'
                    os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile='  + image_file + ' -sPageList=1 -sDEVICE=pnggray -r' + str(self.RESOLUTION) + ' ' + dir + self._name + str(n+1) + '.pdf >nul')

                    # Extract text from scanned image
                    os.system(TESSERACT + ' ' + image_file + ' ' + dir + self._name + str(n+1) + ' >nul 2>&1' )
                else:
                    # Extract text from the PDF page
                    os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile='  + text_file + ' -sPageList=1 -sDEVICE=txtwrite ' + dir + self._name + str(n+1) + '.pdf >nul')

                # Add a page object to this document
                with open(text_file, 'r', encoding="utf-8") as f:
                    # read in the text for the page
                    text = f.read()

                    # Separate text into regions (headings, paragraphs, etc)
                    if self._segment:
                        segment = Segment(text)
                        text = segment.segments
                    
                    # Create Page Object and read in the text for the page
                    page = Page(pdf_file, text, n+1)

                    # Store the tokenized text
                    json_file = dir + self._name + str(n+1) + '.json'
                    page.store(json_file)
                    # Add the page to this document
                    self.__iadd__(page)

                    # First Page
                    if n == 0 and self._scanned == False:
                        # Empty page - could be a 'undetected' scanned PDF (no text)
                        # Garbage Page (not really a text PDF)
                        if self._pages[0].size == 0 or self._pages[0].text[0] == '\x01':
                            # Extract scanned image
                            image_file = dir + self._name + str(n+1) + '.png'
                            os.system(GHOSTSCRIPT + ' -dBATCH -dNOPAUSE -sOutputFile='  + image_file + ' -sPageList=1 -sDEVICE=pnggray -r' + str(self.RESOLUTION) + ' ' + dir + self._name + str(n+1) + '.pdf >nul')

                            # Extract text from scanned image
                            os.system(TESSERACT + ' ' + image_file + ' ' + dir + self._name + str(n+1) + ' >nul 2>&1' )

                            # Reread text file
                            with open(text_file, 'r', encoding="utf-8") as f:
                                self.pages[n] = Page(pdf_file, f.read(), n+1)
                                # Store the tokenized text
                                page.store(json_file)
                            # Assume all remaining pages are scanned images
                            self._scanned = True
                            
        # Split the TIF document into pages
        elif self._type == 'tif' or self._type == 'tiff':
            # Use image magic to split the TIFF file
            os.system(MAGICK + ' ' + self.document + ' ' + dir + self._name + '%d.tif')
            # Get the number of pages
            files = glob.glob(dir + self._name + '*.tif')
            npages = 0
            for file in files:
                if file.replace('\\', '/') != self._document:
                    npages += 1

            # image magic names pages 0 .. N-1. We rename tp 1 .. N
            for n in range(npages,0,-1):
                os.rename( dir + self._name + str(n-1) + '.tif' , dir + self._name + str(n) + '.tif' )

            for n in range(npages):
                # Extract text from TIF page
                tif_file  = dir + self._name + str(n+1) + '.tif'
                text_file = dir + self._name + str(n+1) + '.tif'
                os.system(TESSERACT + ' ' + tif_file + ' ' + dir + self._name + str(n+1) + ' >nul 2>&1' )

                # Read text file
                with open(text_file, 'r', encoding="utf-8", errors='ignore') as f:
                    # Create Page Object and read in the text for the page
                    text = f.read()

                    # Separate text into regions (headings, paragraphs, etc)
                    if self._segment:
                        segment = Segment(text)
                        text = segment.segments
                        
                    page = Page(tif_file, text, n+1)
                    # Store the tokenized text
                    json_file = dir + self._name + str(n+1) + '.json'
                    page.store(json_file)
                    self.__iadd__(page)

            self._scanned = True
                
        # Determine the document's language 
        if len(self.pages) == 1 or len(self.pages[0]) > len(self.pages[1]):
            self._langcheck(self.pages[0].words)
        else:
            self._langcheck(self.pages[1].words)
                            
        # If scanned document, determine the quality of the scan
        if self._scanned:
            if len(self.pages) == 1 or len(self.pages[0]) > len(self.pages[1]):
                self._scancheck(self.pages[0].words)
            else:
                self._scancheck(self.pages[1].words)

        # Total time to do processing
        self._time = time.time() - start
        
    def _langcheck(self, words):
        """ Use the speller checker to determine which language the document is in """
        english = 0
        spanish = 0
        french  = 0
        italian = 0
        german  = 0

        lg = {'en':{'dict':word2int_en,
                    'lang':english},
              'es':{'dict':word2int_es,
                    'lang':spanish},
              'fr':{'dict':word2int_fr,
                    'lang':french},
              'it':{'dict':word2int_it,
                    'lang':italian},
              'de':{'dict':word2int_de,
                    'lang':german}
             }

        for _ in range(20):
            try:
                if len(words[_]['word']) == 1:
                    continue
            # bad entry
            except:
                continue
                
            if words[_]['word'].isdigit():
                continue
            elif words[_]['tag'] == Vocabulary.ACRONYM:
                continue
                
            for item in lg:
                try:
                    id = lg[item]['dict'][words[_]['word']]
                    lg[item]['lang'] += 1
                except:
                    pass

            #verify after 12 iterations if exist a duplicate of words quantity
            if _ >= 11:
                lg_list_val = [lg[item]['lang'] for item in lg]
                if len(set(lg_list_val)) != len(lg_list_val):
                    continue
                else:
                    break

        for i in lg:
            #create a list with all the values in lg except i
            exc_lg = [lg[j]['lang'] for j in lg if i != j]
            #verify if value i is greater than the values in exc_lg
            verify = all(lg[i]['lang'] > item for item in exc_lg)
            #if True set the first two letters from dict key as lang
            if verify:
                self._lang = i
        
    def _scancheck(self, words):
        """ Use spell checker to determine the quality of the scan """
        correct = 0
        count   = 0
        for _ in range(0, min(len(words), self.SCANCHECK)):
            try:
                if len(words[_]['word']) == 1:
                    continue
            # bad entry
            except:
                count += 1
                continue
                
            if words[_]['word'].isdigit():
                continue
            elif words[_]['tag'] == Vocabulary.ACRONYM:
                continue
            count += 1
            if self.WORDDICT == 'norvig':
                norvig = Norvig(self._lang)
                if norvig.known(words[_]['word'].lower()):
                    correct += 1
          
        if count:
            self._quality = correct / count
        else:
            self._quality = 1

    def load(self, document, dir='./'):
        """ """
        self._document = document
        if dir.endswith("/") == False:
                dir += "/"
        self._dir = dir
        basename = os.path.splitext(os.path.basename(self._document))
        self._name = basename[0]
        self._type = basename[1][1:].lower()

        files = glob.glob(dir + self._name + '*.json')
        npages = len(files)
        pageno = 1
        for pageno in range(1, npages+1):
            page = Page(pageno=pageno)
            page.load(dir + self._name + str(pageno) + '.json')
            self.__iadd__(page)


    @property
    def document(self):
        """ Getter for the document name (path) """
        return self._document

    @document.setter
    def document(self, document):
        """ Setter for the document name (path)
        document - path to the document
        """
        self._document = document
        self._exist()
        self._collate(self._dir)

    @property
    def name(self):
        """ Getter for the document name (path) """
        return self._name

    @property
    def text(self):
        """ Getter for the raw text in the document """
        text = []
        for page in self._pages:
            text.append(page.text)
        return text

    @text.setter
    def text(self, text):
        """ Setter for the raw text in a document """
        self._text = text

    @property
    def dir(self):
        """ Getter for the page directory """
        return self._dir

    @dir.setter
    def dir(self, dir):
        """ Setter for page directory """
        # value must be a string
        if dir is not None and isinstance(dir, str) == False:
            raise TypeError("String expected for page directory path")
        self._dir = dir

    @property
    def label(self):
        """ Getter for the document classification """
        return self._label

    @label.setter
    def label(self, label):
        """ Setter for document classification """
        # value must be an integer
        if label is not None and isinstance(label, str) == False:
            raise TypeError("String expected for classification (label)")
        self._label = label

    @property
    def pages(self):
        """ Return the list of pages """
        return self._pages

    @property
    def size(self):
        """ Return the byte size of the document """
        return self._size

    @property
    def type(self):
        """ Return the file type of the document """
        return self._type

    @property
    def time(self):
        """ Return the elapse time to do processing """
        return self._time
        
    @property
    def lang(self):
        """ Return the document language """
        return self._lang

    @property
    def scanned(self):
        """ Return whether document is a scanned (captured) image """
        return self._scanned, self._quality

    @property
    def bagOfWords(self):
        """ Return  bag of words for the document """
        if self._bow is None:
            # Seed the dictionary with the first page's bag of words
            self._bow = self[0].bagOfWords
            # Incrementally merge in each of the remaining page's bag of words
            for i in range(1, len(self)):
                bag = self[i].bagOfWords
                for word, count in bag.items():
                    if word in self._bow:
                        self._bow[word] += count
                    else:
                        self._bow[word] = count
        return self._bow

    @property
    def freqDist(self):
        """ Generate / return frequency distribution """
        if self._freq is None:
            self._freq = sorted( self.bagOfWords.items(), key=lambda x: x[1], reverse=True)
        return self._freq

    @property
    def termFreq(self):
        """ Generate / return term frequencies """
        # REDO
        if self._tf is None:
            nwords = len(self)
            self._tf = []
            for t in self.freqDist:
                self._tf.append( ( t[0], t[1] / nwords ) )
        return self._tf

    def __len__(self):
        """ Override the len() operator - return the number of pages """
        return len(self._pages)

    def __getitem__(self, index):
        """ Override the [] operator - return a page """
        if index < len(self):
            return self._pages[index]
        else:
            return None

    def __setitem__(self, index, page):
        """ Override the [] operator - set a page """
        # value must be a Page object
        if page is not None and isinstance(page, Page) == False:
            raise TypeError("Page expected for [] set operation")
        self._pages[index] = page

    def __iadd__(self, page):
        """ Override the + operator - add a page """
        self._pages.append(page)
        return self

    def __str__(self):
        """ Override the str() operator - return the document classification """
        return self._label


class Page(object):
    """ Base (super) class for Page object """

    BARE    = False         # bare tokenization mode
    STEM    = 'gap'         # NLP stemmer to use
    POS     = False         # Annotation of Parts of Speech
    ROMAN   = False         # Romanize text to 
    SPELL   = None          # Speller

    def __init__(self, path=None, text=None, pageno=None):
        """ Constructor for page object
        path - filepath to the page
        text - extracted text
        """
        self._path   = path     # Path to where PDF page is stored
        self._text   = text     # Raw text extracted from page
        self._pageno = pageno   # Page Number
        self._words  = None     # Tokenized List of words on page
        self._label  = None     # The page classification (label)
        self._size   = 0        # byte size of the page

        if path is not None:
            if isinstance(path, str) == False:
                raise TypeError("String expected for path parameter")
            if os.path.isfile(path) == False:
                raise FileNotFoundError("Not a valid path for the page")
        if text is not None:
            if isinstance(text, list):
                self._size = 0
                for segment in text:
                    if isinstance(segment, dict) == False:
                        raise TypeError("Dictionary expected for text segment:", type(segment))
                    if segment['tag'] == Segment.PARAGRAPH:
                        self._size += 2 + len(segment['text'])
                    else:
                        self._size += 1 + len(segment['text'])
            elif isinstance(text, str):
                self._text = text.strip()
                self._size = len(text)
            else:
                raise TypeError("String expected for text parameter:" , type(text))

    @property
    def path(self):
        """ Getter for page path """
        return self._path

    @path.setter
    def path(self, path):
        """ Setter for page path """
        if path is not None:
            if isinstance(path, str) == False:
                raise TypeError("string expected for path parameter")
            if os.path.isfile(path) == False:
                raise FileNotFoundError("not a valid path for the page")
        self._path = path

    @property
    def text(self):
        """ Getter for page text content """
        if self._text is None:
            return None
        if isinstance(self._text, str):
            return self._text
            
        # Segmented Text
        text = ''
        for segment in self._text:
            if segment['tag'] == Segment.PARAGRAPH:
                text += '\n\n' + segment['text']
            else:
                text += '\n' + segment['text']
        return text.strip()

    @text.setter
    def text(self, text):
        """ Setter for page text """
        if text is not None:
            if isinstance(text, str) == False:
                raise TypeError("String expected for text parameter:", type(text))
            text = text.strip()
            self._size = len(text)
        else:
            self._size = 0
        self._text = text

    @property
    def size(self):
        """ Getter for byte size of page """
        if self._text is None:
            return 0
        return self._size

    @property
    def label(self):
        """ Getter for the document classification """
        return self._label

    @label.setter
    def label(self, label):
        """ Setter for document classification """
        # value must be an integer
        if label is not None and isinstance(label, str) == False:
            raise TypeError("String expected for classification (label)")
        self._label = label

    @property
    def words(self):
        """ Getter for page words (tokenized) """
        if self._text is None and self._words is None:
            return None

        # If text has not been tokenized yet, then tokenize it
        if self._words is None:
            if isinstance(self._text, str):
                self._words = Words(self._text, bare=self.BARE, stem=self.STEM, pos=self.POS, roman=self.ROMAN, spell=self.SPELL)
            else:
                words = []
                for segment in self._text:
                    words.append( { 'tag': segment['tag'], 'words': Words(segment['text'], bare=self.BARE, stem=self.STEM, pos=self.POS, roman=self.ROMAN, spell=self.SPELL).words } )
                self._words = Words()
                self._words._words = words
        return self._words.words

    @property
    def pageno(self):
        """ Getter for the page number """
        return self._pageno

    @property
    def bagOfWords(self):
        """ Getter for bag of words """
        # force a NLP processing if not already
        words = self.words
        if isinstance(self._text, str):
            return self._words.bagOfWords
        # Segmented Text
        else:
            if len(self._words._words) == 0:
                return None
            # TODO
            for segment in self._words._words:
                pass
            return None

    @property
    def freqDist(self):
        """ Getter for frequency distribution """
        # force a NLP processing if not already
        words = self.words
        return self._words.freqDist

    @property
    def termFreq(self):
        """ Getter for term frequency (TF) distribution """
        # force a NLP processing if not already
        words = self.words
        return self._words.termFreq

    def store(self, path):
        """ Store the NLP tokenized string to storage """
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        with open(path, 'w') as f:
            json.dump( self.words, f)

    def load(self, path):
        """ Load the NLP tokenized string from storage """
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        if os.path.isfile(path) == False:
                raise FileNotFoundError("Not a valid path")
        with open(path, 'r', encoding='utf-8') as f:
            self._words = Words()
            self._words._words = json.load(f)
        path = path.replace('.json', '.txt')
        with open(path, 'r', encoding='utf-8') as f:
            self._text = f.read()


    def __len__(self):
        """ Override the len() operator - get the number of tokenized words """
        if self._text is None:
            return 0

        # If text has not been tokenized yet, then tokenize it
        if self._words is None:
            self._words = Words(self._text, bare=self.BARE, stem=self.STEM, pos=self.POS, roman=self.ROMAN, spell=self.SPELL)
        return len(self._words.words)

    def __str__(self):
        """ Override the str() operator - return the document classification """
        return self._label

    def __iadd__(self, text):
        """ Override the += operator - add text to the page """
        if text is None:
            return self
        if isinstance(text,str) == False:
            raise TypeError("String expected for text")
        else:
            # Extend the text
            if self._text is None:
                self._text = text
            else:
                self._text += " " + text

            # Was already tokenized
            if self._words is not None:
                # Tokenize new text
                words = Words(text, bare=self.BARE, stem=self.STEM, pos=self.POS, roman=self.ROMAN, spell=self.SPELL)
                # Add tokens to existing list
                self._words += words.words
        return self


def towords(words):
    ret = []
    for word in words:
        print(word['word'])

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: document.py document [directory]")
    elif len(sys.argv) == 2:
        d = Document(sys.argv[1])
    else:
        d = Document(sys.argv[1], sys.argv[2])
        p = d[0]
        print(towords(p.words))