# -*- coding: latin-1 -*-
""" Module for Processing PDF Documents 
2018(c), Andrew Ferlitsch
"""
#chcp 65001


import os.path
import re
import threading
import time
import shutil
import glob
import sys
import json

from nltk.stem import *
import nltk
from nltk import pos_tag
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from vocabulary import Vocabulary, vocab
from pdf_res import PDFResource

# Ghostscript executable for Windows 64bit
GHOSTSCRIPT = "gswin64c"
TESSERACT   = "tesseract"
MAGICK      = "magick"

class Document(object):
    """ Base (super) Class for Classifying a Document """
    
    RESOLUTION = 300    # Resolution for OCR

    def __init__(self, document=None, dir="./", ehandler=None, config=None):
        """ Constructor for document object 
        document - - path to the document
        dir - directory where to store extracted pages and text
        """
        self._document = document   # document path
        self._name     = None       # Name of document (no path and no suffix)
        self._class    = None       # classification of the document
        self._pages    = []         # document pages
        self._dir      = dir        # directory where extracted pages and text are stored
        self._type     = None       # file type of the document
        self._size     = 0          # byte size of the document
        self._ehandler = ehandler   # event completion handler for async execution of splitting
        self._time     = 0          # elapse time to do collation
        self._scanned  = False      # flag indicating if scanned PDF, TIFF or image capture
        
        # value must be a string
        if dir is not None and isinstance(dir, str) == False:
            raise TypeError("String expected for page directory path")
                       
        # NLP configuration
        if config is not None:
            for key in config:
                if key == 'bare':
                    Page.BARE = True
                elif key.startswith('stem'):
                    vals = key.split('=')
                    if len(vals) == 2:
                        Page.STEM = vals[1]
                elif key.startswith('pos'):
                        Page.POS = True
                                     
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
                    # Create Page Object and read in the text for the page
                    page = Page(pdf_file, f.read(), n+1)
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
                    page = Page(tif_file, text, n+1)
                    # Store the tokenized text
                    json_file = dir + self._name + str(n+1) + '.json' 
                    page.store(json_file)
                    self.__iadd__(page) 
                    
            self._scanned = True 
            
        # Total time to do collation
        self._time = time.time() - start
        
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
        pageno = 1
        for file in files:
            page = Page(pageno=pageno)
            page.load(file)
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
    def classification(self):
        """ Getter for the document classification """
        return self._class
        
    @classification.setter
    def classification(self, classification):
        """ Setter for document classification """
        # value must be an integer
        if classification is not None and isinstance(classification, str) == False:
            raise TypeError("String expected for classification (label)")
        self._class = classification
        
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
        """ Return the elapse time to do collation """
        return self._time
        
    @property
    def scanned(self):
        """ Return whether document is a scanned (captured) image """
        return self._scanned
        
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
        return self._class

        
class Page(object):
    """ Base (super) class for Page object """
    
    BARE=False
    STEM='internal'
    POS=False
    
    def __init__(self, path=None, text=None, pageno=None):
        """ Constructor for page object 
        path - filepath to the page
        text - extracted text
        """
        self._path   = path     # Path to where PDF page is stored
        self._text   = text     # Raw text extracted from page
        self._pageno = pageno   # Page Number
        self._words  = None     # Tokenized List of words on page
        self._class  = None     # The page classification (label)
        self._size   = 0        # byte size of the page
        
        if path is not None:
            if isinstance(path, str) == False:
                raise TypeError("string expected for path parameter")
            if os.path.isfile(path) == False:
                raise FileNotFoundError("not a valid path for the page")
        if text is not None:
            if isinstance(text, str) == False:
                raise TypeError("string expected for text parameter")
            self._text = text.strip()
            self._size = len(text)
        
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
        return self._text
        
    @text.setter
    def text(self, text):
        """ Setter for page text """
        if text is not None:
            if isinstance(text, str) == False:
                raise TypeError("string expected for text parameter")
            text = text.strip()
            self._size = len(text)
        else:
            self._size = 0
        self._text = text
        
    @property
    def size(self):
        """ Getter for byte size of page """
        return self._size
        
    @property
    def classification(self):
        """ Getter for the document classification """
        return self._class
        
    @classification.setter
    def classification(self, classification):
        """ Setter for document classification """
        # value must be an integer
        if classification is not None and isinstance(classification, str) == False:
            raise TypeError("String expected for classification (label)")
        self._class = classification
        
    @property
    def words(self):
        """ Getter for page words (tokenized) """
        if self._text is None and self._words is None:
            return None
            
        # If text has not been tokenized yet, then tokenize it
        if self._words is None:
            self._words = Words(self._text, bare=self.BARE, stem=self.STEM, pos=self.POS)
        return self._words.words 
        
    @property
    def pageno(self):
        """ Getter for the page number """
        return self._pageno
        
    def store(self, file):
        """ Store the NLP tokenized string to storage """
        with open(file, 'w') as f:
            json.dump( self.words, f)
        
    def load(self, file):
        """ Load the NLP tokenized string from storage """
        with open(file, 'r') as f:
            self._words = Words()
            self._words._words = json.load(f)
        
    def __len__(self):
        """ Override the len() operator - get the number of tokenized words """
        if self._text is None:
            return 0
            
        # If text has not been tokenized yet, then tokenize it
        if self._words is None:
            self._words = Words(self._text, bare=self.BARE, stem=self.STEM, pos=self.POS)
        return len(self._words.words)
        
    def __str__(self):
        """ Override the str() operator - return the document classification """
        return self._class
        
    def __iadd__(self, text):
        """ Override the += operator - add text to the page """
        if text is None:
            return self
        if isinstance(text,str) == False:
            raise TypeError("String expected for text")
            self._text = text
        else:
            # Extend the text
            if self._text is None:
                self._text = text
            else:
                self._text += " " + text
            
            # Was already tokenized
            if self._words is not None:
                # Tokenize new text
                words = Words(text, bare=self.BARE, stem=self.STEM, pos=self.POS)
                # Add tokens to existing list
                self._words += words.words
        return self
        
        
class Words(object):
    """ Base class for NLP tokenized words """

    DECIMAL		    = '.'	# Standard Unit for Decimal Point
    THOUSANDS 	    = ','	# Standard Unit for Thousandth Separator
    
    def __init__(self, text=None, bare=False, stem='internal', pos=False, stopwords=False, punct=False, conjunction=False, article=False, demonstrative=False, preposition=False, question=False, pronoun=False, quantifier=False, date=False, number=False, ssn=False, telephone=False, name=False, address=False, sentiment=False, gender=False, dob=False, unit=False, standard=False, metric=False ):
        """ Constructor 
        text - raw text as string to tokenize
        """
        self._text          = text          # raw text
        self._words         = None          # list of words
        self._punct         = punct         # keep/remove punctuation
        self._stemming      = stem          # on/off stemming
        self._pos           = pos           # on/off parts of speech
        self._porter        = stopwords     # keep/remove stopwords
        self._bare          = bare          # on/off bare tokenizing
        self._standard      = standard      # convert metric to standard units
        self._metric        = metric        # convert standard to metric units
        
        # More than just bare tokenizing
        if self._bare == False:
            # Keep Stopwords
            if stopwords is True:
                self._quantifier    = True          # keep words indicating a size
                self._preposition   = True          # keep prepositions
                self._article       = True          # keep articles
                self._conjunction   = True          # keep conjunctions
                self._demonstrative = True          # keep demonstratives
                self._question      = True          # keep question words
                self._pronoun       = True          # keep pronouns        
                self._sentiment     = True          # keep sentiment words
                self._number        = True          # keep numbers 
                self._date          = True          # keep date
                self._ssn           = True          # keep social security number
                self._telephone     = True          # keep telephone numbers
                self._address       = True          # keep street addresses
                self._name          = True          # keep proper names
                self._gender        = True          # keep gender words
                self._dob           = True          # keep date of birth words
                self._unit          = True          # keep unit of measurement
            # Remove Stopwords
            else:
                self._quantifier    = quantifier    # keep/remove words indicating a size
                self._preposition   = preposition   # keep/remove prepositions
                self._article       = article       # keep/remove articles
                self._conjunction   = conjunction   # keep/remove conjunctions
                self._demonstrative = demonstrative # keep/remove demonstratives
                self._question      = question      # keep/remove question words
                self._pronoun       = pronoun       # keep/remove pronouns
                self._sentiment     = sentiment     # keep/remove sentiment words
                self._number        = number        # keep/remove numbers
                self._date          = date          # keep/remove date
                self._ssn           = ssn           # keep/remove social security number
                self._telephone     = telephone     # keep/remove telephone numbers
                self._address       = address       # keep/remove street addresses
                self._name          = name          # keep/remove proper names
                self._gender        = gender        # keep/remove gender words
                self._dob           = dob           # keep/remove date of birth words
                self._unit          = unit          # keep/remove unit of measurement words
            
        if isinstance(stopwords, bool) is False:
            raise TypeError("Stopwords must be a boolean")
        if isinstance(bare, bool) is False:
            raise TypeError("Bare must be a boolean")
        if isinstance(quantifier, bool) is False:
            raise TypeError("Quantifier must be a boolean")
        if isinstance(preposition, bool) is False:
            raise TypeError("Preposition must be a boolean")
        if isinstance(conjunction, bool) is False:
            raise TypeError("Conjunction must be a boolean")
        if isinstance(article, bool) is False:
            raise TypeError("Article must be a boolean")
        if isinstance(demonstrative, bool) is False:
            raise TypeError("Demonstrative must be a boolean")
        if isinstance(question, bool) is False:
            raise TypeError("Question must be a boolean")
        if isinstance(pronoun, bool) is False:
            raise TypeError("Pronoun must be a boolean")
        if isinstance(number, bool) is False:
            raise TypeError("Number must be a boolean")
        if isinstance(date, bool) is False:
            raise TypeError("Date must be a boolean")
        if isinstance(ssn, bool) is False:
            raise TypeError("SSN must be a boolean")
        if isinstance(telephone, bool) is False:
            raise TypeError("Telephone must be a boolean")
        if isinstance(name, bool) is False:
            raise TypeError("Name must be a boolean")
        if isinstance(address, bool) is False:
            raise TypeError("Address must be a boolean")
        if isinstance(sentiment, bool) is False:
            raise TypeError("Sentiment must be a boolean")
        if isinstance(gender, bool) is False:
            raise TypeError("Gender must be a boolean")
        if isinstance(dob, bool) is False:
            raise TypeError("DOB must be a boolean")
        if isinstance(punct, bool) is False:
            raise TypeError("Punct must be a boolean")
        if isinstance(unit, bool) is False:
            raise TypeError("Unit must be a boolean")
        if isinstance(standard, bool) is False:
            raise TypeError("Standard must be a boolean")
        if isinstance(metric, bool) is False:
            raise TypeError("Metric must be a boolean")
        if text is not None:
            if isinstance(text, str) is False:
                raise TypeError("String expected for text")
            # tokenize the text
            self._split()
            if self._bare == False:
                # preprocess the tokens
                self._preprocess()
                # word stemming
                if self._stemming == 'internal':
                    self._stem()
                elif self._stemming == 'porter':
                    self._nltkStemmer('porter')
                elif self._stemming == 'snowball':
                    self._nltkStemmer('snowball')
                elif self._stemming == 'lancaster':
                    self._nltkStemmer('lancaster')
                elif self._stemming == 'lemma':
                    self._lemma()
                # remove stop words
                self._stopwords()
                # Do unit conversions
                self._conversion()
                # Do POS tagging
                if self._pos == True:
                    self._partsofspeech()
    
    @property
    def text(self):
        """ Getter for text """
        return self._text
    
    @property
    def words(self):
        """ Getter for words """
        return self._words
        
    def _split(self):
        """ Tokenize the Text
            1. Expand contractions.
            2. Replace newlines, carriage returns, tabs with space.
            3. Reduce multi-spaces into single space.
            4. Split text by whitespace (tokenize).
            5. Separate Punctuation.
        """
        
        self._words = []
        
        # (1) Expand contractions
        text = self._text.replace("'m ", " am ")
        text = text.replace("'d ", " would ")
        text = text.replace("'ll ", " will ")
        text = text.replace("'ve ", " have ")
        text = text.replace("'re ", " are ")
        text = text.replace("can't ", "can not ")
        text = text.replace("won't ", "will not ")
        text = text.replace("n't ", " not ")
        # Assume possesives are contractions of is
        text = text.replace("'s ", " is ")
        text = text.replace("s' ", "s ")
        
        # (2) Replace newlines, carriage returns, tabs, form feed with space.
        text = re.sub('[\r\n\t\f]', ' ', text)
        
        # (3) remove duplicate spaces
        text = re.sub(' +', ' ', text.strip())
        
        # Empty text
        if len(text) == 0:
            return        
        
        # (4) Split text by whitespace (tokenize).
        words = text.split(' ')
     
        # (5) Separate out punctuation
        for word in words:
            length = len(word)
                
            begin = 0
            for i in range(0,length):
                if not word[i].isdigit() and not word[i].isalpha():
                    # decimal, thousandths and fraction symbol
                    if word[i] in ['.', ',', '/'] and i < length-1 and word[i+1].isdigit():
                        continue
                    # sign symbol
                    if word[i] in ['-', '+'] and i < length-1 and (word[i+1].isdigit() or word[i+1] in ['.', ',']):
                        # first char or exponent
                        if begin == i or word[i-1] in ['e', 'E']:
                            continue
                        
                    if begin != i:
                        self._words.append( { 'word': word[begin:i], 'tag': Vocabulary.UNTAG } )
                    if word[i] in [ '.', '?', '!', ',', ':', ';', '(', ')', '[', ']', '"', '\'', '¿', '¡']:
                        self._words.append( { 'word': word[i], 'tag': Vocabulary.PUNCT } )
                    # non-printable ascii
                    elif (ord(word[i]) >= 0 and ord(word[i]) <= 7) or (ord(word[i]) >= 14 and ord(word[i]) <= 31):
                        pass
                    else:
                        self._words.append( { 'word': word[i], 'tag': Vocabulary.SYMBOL } )
                    begin = i + 1
            if begin < length:
                self._words.append( { 'word': word[begin:], 'tag': Vocabulary.UNTAG } )
        
        
    def _preprocess(self):
        """ Preprocess Token List.
                1.  Remove periods from Abbreviations
                2.  Identify Acronyms
                3.  Identify Proper Names (Capitalized).
                4.  Lowercase.
        """
        _words = []
        
        # Preprocess Token List.
        wasCaps = False
        nwords = len(self._words)
        for index in range(nwords):
            word = self._words[index]
            length = len(word['word'])

            # (1) Remove periods from abbreviations
            if word['word'] == '.':
                # Preceded by a single letter
                if len(_words) > 0 and len(_words[-1]['word']) == 1 and _words[-1]['word'].isalpha():
                    # Set previous word as Abbreviation
                    if _words[-1]['tag'] not in [Vocabulary.NAME, Vocabulary.TITLE]:
                        _words[-1]['tag'] = Vocabulary.ABBR
                    # Drop the punct!
                # Proceeded by an abbreviated name title
                elif self._punct == False and len(_words) > 0 and (_words[-1]['tag'] in [Vocabulary.NAME, Vocabulary.TITLE] or _words[-1]['tag'] == Vocabulary.DATE):
                    # Drop the punct!
                    pass
                else:
                    _words.append(word)
                    
            # Single character
            elif length == 1:
                # Lowercase the single letter
                if word['word'].isupper():
                    word['word'] = word['word'].lower()
                
                if word['word'].isalpha():
                    # Continuation of a Name
                    if len(_words) > 0 and _words[-1]['tag'] == Vocabulary.NAME:
                        word['tag'] = Vocabulary.NAME
                        
                # Keep single letter word
                _words.append(word)
                    
                wasCaps = False
                
            # Multiple Character 
            else:
                # All Uppercased (can't start with digit)
                if word['word'].isupper() and not word['word'][0].isdigit():
                    # (2) Identify Acronyms
                    # If the next word is uppercased, it is a title line, not an acronym
                    # If last word is uppercased, it is a title line, not an acronym
                    word['word'] = word['word'].lower()
                    if not (index+1 < nwords and self._words[index+1]['word'].isupper()) and (index+1 != nwords or wasCaps == False):
                        try:
                            v = vocab[word['word']]
                            if Vocabulary.NAME in v['tag']:
                                word['tag'] = Vocabulary.NAME
                            # Word is a title (e.g., CEO)
                            elif Vocabulary.TITLE in v['tag']:
                                word['tag'] = Vocabulary.TITLE
                                itag = v['tag'].index(Vocabulary.TITLE)
                                word['word'] = v['lemma'][itag]
                            else:
                                word['tag'] = Vocabulary.ACRONYM
                        except:
                            word['tag'] = Vocabulary.ACRONYM
                            
                    wasCaps = True
                    
                # First Letter is Capitalized
                elif word['word'][0].isupper():
                    # First Word 
                    if len(_words) == 0:
                        pass
                    # Follows abbreviated title
                    elif len(_words) > 1 and _words[-1]['word'] == '.' and _words[-2]['tag'] == Vocabulary.TITLE:
                        word['tag'] = Vocabulary.NAME
                    # Start of Sentence
                    elif _words[-1]['tag'] == Vocabulary.PUNCT and _words[-1]['word'] not in [',', ':']:
                        pass
                    elif word['word'] in ['Jan', 'January', 'Feb', 'February', 'Mar', 'March', 'Apr', 'April', 'May', 'Jun', 'June', 'Jul', 'July', 'Aug', 'August', 'Sep', 'Sept', 'September', 'Oct', 'October', 'Nov', 'November', 'Dec', 'December']:
                         word['tag'] = Vocabulary.DATE
                    # (3) Identify Proper Names
                    #   Word is capitalized and not proceeded by period (.), question (?) or exclamation (!)
                    #   or single/double quote
                    else:
                        word['tag'] = Vocabulary.NAME
                        # Proceeding Acronym is a really part of a name
                        if len(_words) > 0 and _words[-1]['tag'] == Vocabulary.ACRONYM:
                            _words[-1]['tag'] = Vocabulary.NAME
                        # Proceeding Word is a Title of a name (e.g., Mr)
                        else:
                            try:
                                v = vocab[_words[-1]['word']]
                                if Vocabulary.TITLE in v['tag']:
                                    _words[-1]['tag'] = Vocabulary.TITLE
                                    itag = v['tag'].index(Vocabulary.TITLE)
                                    _words[-1]['word'] = v['lemma'][itag]
                                    
                            except:
                                # Word is an ending title in a name
                                try:
                                    v = vocab[word['word'].lower()]
                                    if Vocabulary.TITLE in v['tag'] and Vocabulary.STREET_TYPE not in v['tag'] and Vocabulary.STATE not in v['tag']:
                                        word['tag'] = Vocabulary.TITLE
                                        itag = v['tag'].index(Vocabulary.TITLE)
                                        word['word'] = v['lemma'][itag]
                                except: pass
                    wasCaps = False
                    
                # First Letter is a Digit
                elif word['word'][0].isdigit():
                    cont = False
                    # Check if this is a number combined with a unit
                    for i in range(1, len(word['word'])):
                        # Separate the number from the proceeding text
                        if word['word'][i].isalpha():
                            token = word['word'][i:].lower()
                            # Check if the proceeding text is a Unit of Measurement
                            try:
                                v = vocab[token]
                                if Vocabulary.UNIT in v['tag']:
                                   itag = v['tag'].index(Vocabulary.UNIT)
                                   _words.append( { 'word':  word['word'][0:i], 'tag': Vocabulary.NUMBER } )
                                   _words.append( { 'word': v['lemma'][itag], 'tag': Vocabulary.UNIT } )
                                   cont = True
                            except: pass
                            break
                        elif not word['word'][i].isdigit() and word['word'][i] != Words.DECIMAL:
                            break
                    if cont == True:
                        continue
                            
                word['word'] = word['word'].lower()
                _words.append(word)
                
        self._words = _words
                
    def _stem(self):
        """ Word stemming """

        length = len(self._words)
        for i in range(length):
            word = self._words[i]['word']
            l = len(word)

            # Don't stem short words or words already categorized
            if l < 4 or self._words[i]['tag'] != Vocabulary.UNTAG:
                continue
            
            # If in vocabulary, do not stem
            try:
                v = vocab[word]
                t = v['tag']
                if len(t) == 1:
                    if t[0] != Vocabulary.QUANTIFIER and t[0] != Vocabulary.UNIT:
                        l = v['lemma']
                        if l is not None:
                            self._words[i]['word'] = l[0]
                continue
            except: pass
                        
            # purals
            if word.endswith("ies"):
                if l > 4:
                    self._words[i]['word'] = word[0:-3] + 'y'
                else:
                    self._words[i]['word'] = word[0:-1]
            elif word.endswith("ches") or word.endswith("ses") or word.endswith("xes") or word.endswith("zes"):
                self._words[i]['word'] = word[0:-2]
            #elif word.endswith("ves"):
                #self._words[i]['word'] = word[0:-3] + 'f'
            elif word.endswith("ss") or word.endswith("is") or word.endswith("us"):
                pass 
            elif word.endswith("s"):
                self._words[i]['word'] = word[0:-1]
              
            word = self._words[i]['word']  
            
            # If in vocabulary, do not stem
            try:
                v = vocab[word]
                t = v['tag']
                if len(t) == 1:
                    if t[0] != Vocabulary.QUANTIFIER and t[0] != Vocabulary.UNIT:
                        l = v['lemma']
                        if l is not None:
                            self._words[i]['word'] = l[0]
                continue
            except: pass
            
            l = len(word)

            # present participle endings
            if l > 5:
                if word.endswith("nning") or word.endswith("tting"):
                    self._words[i]['word'] = word[0:-4]
                elif word.endswith("ding") or word.endswith("king") or word.endswith("ving") or word.endswith("zing") or word.endswith("ting"):
                    if self._words[i]['word'][-5] in ['a', 'e', 'i', 'o', 'u', 'y']:
                        self._words[i]['word'] = word[0:-3] + 'e'
                    else:
                        self._words[i]['word'] = word[0:-3]
                elif word.endswith("ing"):
                    self._words[i]['word'] = word[0:-3]
              
            word = self._words[i]['word']  
            l = len(word) 
            
            # If in vocabulary, do not stem
            try:
                v = vocab[word]
                t = v['tag']
                if len(t) == 1:
                    if t[0] != Vocabulary.QUANTIFIER and t[0] != Vocabulary.UNIT:
                        l = v['lemma']
                        if l is not None:
                            self._words[i]['word'] = l[0]
                continue
            except: pass

            if l > 4:
                # Past Tense
                if word.endswith("dden") or word.endswith("tten") or word.endswith("nned"):
                    if word[-5] == 'i':
                        self._words[i]['word'] = word[0:-3] + 'e'
                    else:
                        self._words[i]['word'] = word[0:-3] 
                elif l > 6 and word.endswith("lled"):
                    self._words[i]['word'] = word[0:-3]
                elif word.endswith("mmed"):
                    self._words[i]['word'] = word[0:-3]
                elif word.endswith("ied"):
                    self._words[i]['word'] = word[0:-3] + 'y'
                elif word.endswith("zed"):
                    self._words[i]['word'] = word[0:-1]
                elif word.endswith("eed"):
                    continue
                elif word.endswith("ed"):
                    self._words[i]['word'] = word[0:-2]
                    
                # Verb to Noun and Comparative endings
                elif word.endswith("ther") or word.endswith("ever"):
                    continue
                elif word.endswith("mber"):
                    continue
                elif word.endswith("ier"):
                    self._words[i]['word'] = word[0:-3] + 'y'
                elif word.endswith("der"):
                    self._words[i]['word'] = word[0:-1]
                elif word.endswith("er"):
                    self._words[i]['word'] = word[0:-2]
                    
            if l > 5:
                # Superlative endings
                if word.endswith("est"):
                    self._words[i]['word'] = word[0:-3]
 
            word = self._words[i]['word']  
            l = len(word)
            if l > 5:
                # Adjective to Adverb endings
                if word.endswith("ily"):
                    self._words[i]['word'] = word[0:-3] + 'y'
                elif word.endswith("ly"):
                    self._words[i]['word'] = word[0:-2]
             
            # If in vocabulary, do not stem
            try:
                v = vocab[word]
                t = v['tag']
                if len(t) == 1:
                    if t[0] != Vocabulary.QUANTIFIER and t[0] != Vocabulary.UNIT:
                        l = v['lemma']
                        if l is not None:
                            self._words[i]['word'] = l[0]
                continue
            except: pass
            
            # Derivation
            if l > 5:
                if word.endswith("ise") or word.endswith("ize"):
                    self._words[i]['word'] = word[0:-3]
                elif word.endswith("ify"):
                    self._words[i]['word'] = word[0:-3] + 'y'
                elif word.endswith("fy"):
                    self._words[i]['word'] = word[0:-2]
                elif word.endswith("iful"):
                    self._words[i]['word'] = word[0:-4] + 'y'
                elif word.endswith("ful"):
                    self._words[i]['word'] = word[0:-3]
                elif word.endswith("iness"): 
                    self._words[i]['word'] = word[0:-5] + 'y'
                elif word.endswith("ness"):
                    self._words[i]['word'] = word[0:-4]    

    def _nltkStemmer(self, name):
        """ NLTK Stemmer """
        if name == 'porter':
            stemmer = PorterStemmer()
        elif name == 'snowball':
            stemmer = SnowballStemmer("english")
        elif name == "lancaster":
            stemmer = LancasterStemmer()
        else:
            return
        
        length = len(self._words)
        for i in range(length):
            word = self._words[i]['word']
            l = len(word)

            # Don't stem short words or words already categorized
            if l < 4 or self._words[i]['tag'] != Vocabulary.UNTAG:
                continue
            
            self._words[i]['word'] = stemmer.stem(self._words[i]['word'])    
            
    def _lemma(self):
        """ NLTK Lemmatizer """
        lemma = WordNetLemmatizer()

        length = len(self._words)
        for i in range(length):        
            self._words[i]['word'] = lemma.lemmatize(self._words[i]['word'])

    def _stopwords(self):
        """ Stop word removal """
        words = []
        nwords = len(self._words)
        skip = 0
        for i in range(nwords):
            # skip words
            if skip > 0:
                skip -= 1
                continue
              
            # Remove names
            if self._words[i]['tag'] in [Vocabulary.NAME, Vocabulary.TITLE] and self._name == False:
                continue
                
            word = self._words[i]['word']
                
            if self._words[i]['tag'] not in [Vocabulary.PUNCT, Vocabulary.SYMBOL]:
                # Check if this word or sequence of words is a date string
                w, n = self._isdate(self._words, i)
                if w is not None:
                    skip = n
                    if len(words) > 0 and words[-1]['word'] in ['birth', 'DOB', 'dob']:
                        if self._dob is True:
                            words[-1] = {'word': w, 'tag': Vocabulary.DOB }
                    elif self._date is True:
                        words.append( {'word': w, 'tag': Vocabulary.DATE } )
                    continue
                
                # Check if this word or sequence of words is a SSN number
                w, n = self._isSSN(self._words, i)
                if w is not None:
                    skip = n
                    if self._ssn is True:
                        words.append( {'word': w, 'tag': Vocabulary.SSN } )
                    continue
                
                # Check if this word or sequence of words is a Telephone number
                w, n = self._isTele(self._words, i)
                if w is not None:
                    skip = n
                    if self._telephone is True:
                        words.append( {'word': w, 'tag': Vocabulary.TELEPHONE } )
                    continue
                    
                    
                # Check if this word or sequence of words is a USA/CA Address
                n = self._isAddr(self._words, i)
                if n > 0:
                    skip = n
                    if self._address is True:
                        for _x in range(i, i+skip):
                            if self._words[_x]['tag'] in [ Vocabulary.STREET_NUM, Vocabulary.STREET_DIR, 
                                                           Vocabulary.STREET_NAME, Vocabulary.STREET_TYPE,
                                                           Vocabulary.POB, Vocabulary.STREET_ADDR2, 
                                                           Vocabulary.CITY, Vocabulary.STATE, Vocabulary.POSTAL,
                                                           Vocabulary.STATION]:
                                words.append( self._words[_x] )
                    continue
  
                # Check if this word is a number
                w, n = self._isnumber(self._words, i)
                if w is not None:
                    skip = n
                    if self._number is True:
                        try:
                            tag = vocab[word]['tag']
                            # If number proceeds a word that can double as a unit, set it as only a unit.
                            if Vocabulary.UNIT in tag and words != []:
                                if words[-1]['tag'] == Vocabulary.NUMBER:
                                    itag = tag.index(Vocabulary.UNIT)
                                    words.append({ 'word': vocab[word]['lemma'][itag], 'tag': Vocabulary.UNIT })
                                    continue
                        except: pass
                        # Remove Thousandth Unit
                        word = w.replace(self.THOUSANDS, '')
                        # Convert to using standard unit decimal
                        if self.DECIMAL == ',':
                            word = word.replace(',', '.')
                        words.append( {'word': word, 'tag': Vocabulary.NUMBER } )       
                    continue 
                    
  
                # Check if this word is a gender reference
                w, n, t = self._isGender(self._words, i)
                if w is not None:
                    skip = n
                    if self._gender is True:
                        words.append( {'word': w, 'tag': t } )
                    continue
                    
                if self._words[i]['tag'] in [ Vocabulary.ACRONYM, Vocabulary.NAME, Vocabulary.TITLE, Vocabulary.ABBR ]:
                    words.append(self._words[i])
                    continue

                tag = [Vocabulary.UNTAG]
                try:
                    tag = vocab[word]['tag']
                    
                    # If number proceeds a word that can double as a unit, set it as only a unit.
                    if Vocabulary.UNIT in tag and words != []:
                        if i + 2 < nwords:
                            # unit / hour
                            if self._words[i+1]['word'] == '/' and self._words[i+2]['word'] in ['h', 's']:
                                word += self._words[i+2]['word']
                                skip = 2
                        if words[-1]['tag'] == Vocabulary.NUMBER:
                            itag = tag.index(Vocabulary.UNIT)
                            words.append({ 'word': vocab[word]['lemma'][itag], 'tag': Vocabulary.UNIT })
                            continue
                        # compound unit of measurement (e.g., sq ft)
                        elif words[-1]['tag'] == Vocabulary.UNIT and words[-1]['word'] == 'square':
                            itag = tag.index(Vocabulary.UNIT)
                            words[-1]['word'] = 'square ' + vocab[word]['lemma'][itag]
                            continue
                        # Word is used as a non-unit abbreviation
                        elif Vocabulary.ABBR in tag:
                            itag = tag.index(Vocabulary.ABBR)
                            words.append({ 'word': vocab[word]['lemma'][itag], 'tag': Vocabulary.ABBR })
                            continue

                    if Vocabulary.QUANTIFIER in tag:
                        if self._quantifier == True:
                            if vocab[word]['lemma'] is not None:
                                words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.QUANTIFIER })
                            else:
                                words.append({ 'word': word, 'tag': Vocabulary.QUANTIFIER })
                    elif Vocabulary.CONJUNCTION in tag:
                        if self._conjunction == True:
                            words.append({ 'word': word, 'tag': Vocabulary.CONJUNCTION })
                    elif Vocabulary.ARTICLE in tag:
                        if self._article == True:
                            words.append({ 'word': word, 'tag': Vocabulary.ARTICLE })
                    elif Vocabulary.DEMONSTRATIVE in tag:
                        if self._demonstrative == True:
                            words.append({ 'word': word, 'tag': Vocabulary.DEMONSTRATIVE })
                    elif Vocabulary.PREPOSITION in tag:
                        if self._preposition == True:
                            words.append({ 'word': word, 'tag': Vocabulary.PREPOSITION })
                    elif Vocabulary.PRONOUN in tag:
                        if self._pronoun == True:
                            words.append({ 'word': word, 'tag': Vocabulary.PRONOUN })
                    elif Vocabulary.QUESTION in tag:
                        if self._question == True:
                            words.append({ 'word': word, 'tag': Vocabulary.QUESTION })
                    elif Vocabulary.NAME in tag:
                        if self._name == True:
                            words.append({ 'word': word, 'tag': Vocabulary.NAME })
                    elif Vocabulary.TITLE in tag:
                        if self._name == True:
                            if vocab[word]['lemma'] is not None:
                                itag = tag.index(Vocabulary.TITLE)
                                words.append({ 'word': vocab[word]['lemma'][itag], 'tag': Vocabulary.TITLE })
                            else:
                                words.append({ 'word': word, 'tag': Vocabulary.TITLE })
                    elif tag[0] in [ Vocabulary.MALE, Vocabulary.FEMALE, Vocabulary.TRANSGENDER]:
                        if self._gender == True:
                            words.append({ 'word': word, 'tag': tag[0]})
                    elif tag[0] == Vocabulary.POSITIVE:
                        if self._sentiment == True:
                            # check if previous word negates the sentiment
                            if len(words) == 0 or words[-1]['tag'] != Vocabulary.NEGATIVE:
                                words.append({'word': word, 'tag': Vocabulary.POSITIVE})
                    elif tag[0] == Vocabulary.NEGATIVE:
                        if self._sentiment == True:
                            # check if previous word negates the sentiment
                            if len(words) > 0 and words[-1]['tag'] == Vocabulary.NEGATIVE:
                                words[-1]['tag'] = Vocabulary.POSITIVE
                            else:
                                words.append({'word': word, 'tag': Vocabulary.NEGATIVE})
                    elif tag[0] == Vocabulary.UNIT:
                        if self._unit == True:
                            if len(word) > 1:
                                words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.UNIT})
                            else:
                                words.append({ 'word': word, 'tag': Vocabulary.UNTAG})
                    elif tag[0] == Vocabulary.NUMBER:
                        if self._number == True:
                            words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.NUMBER})
                    elif tag[0] == Vocabulary.PORTER:
                        if self._porter == True:
                            words.append({ 'word': word, 'tag': Vocabulary.PORTER})
                    elif tag[0] in [ Vocabulary.ADDRESS, Vocabulary.STREET_TYPE, Vocabulary.STREET_ADDR2 ]:
                        # Not an Address
                        words.append({ 'word': word, 'tag': Vocabulary.UNTAG})
                    elif tag[0] == Vocabulary.UNTAG:
                        words.append({ 'word': word, 'tag': Vocabulary.UNTAG})
                    continue
                except:
                    words.append({ 'word': word, 'tag': tag[0] } )
            else:
                if self._punct != False:
                    words.append(self._words[i])
                    continue
                    
        self._words = words
            
    def _isnumber(self, words, index):
        """ Check if word sequence is a number """
        word = words[index]['word']
        
        try:
            tag = vocab[word]['tag']
            if Vocabulary.NUMBER in tag:
                word = vocab[word]['lemma'][0]
        except: pass
        
        # Prefixes
        hex = False
        start = 0
        if word[0] == '+':
            word = word[1:]
        elif word[0] == '-':
            start = 1
        if start >= len(word):
            return None, 0
        
        if word[start] == self.DECIMAL:
            word = word[0:start] + '0' + word[start:]
            start += 2
        elif word.startswith("0x"):
            hex = True
            word = word[2:]

        digit = False   # last char was digit
        dpt   = False   # decimal point
        exp   = False   # exponent
        nom   = False   # nominarator in fraction
        end = len(word)
        for i in range(start, end):
            # digit
            if word[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]:
                digit = True
            elif hex and word[i] in ['a', 'b', 'c', 'd', 'e', 'f']:
                digit = True
            # decimal point
            elif digit and not dpt and word[i] == self.DECIMAL:
                digit = False
                dpt   = True
            # thousands separator
            elif digit and word[i] == self.THOUSANDS:
                digit = False
            # exponent
            elif digit and not exp and word[i] == 'e':
                exp = True
            # negative exponent
            elif exp and word[i] == '-':
                pass
            # fraction 
            elif digit and word[i] == '/':
                nom = i
            # ordered numbers
            elif digit:
                if word[i-1] == '1':
                    if word[i:] == 'st':
                        return word[0:i], 0
                elif word[i-1] == '2':
                    if word[i:] == 'nd':
                        return word[0:i], 0
                elif word[i-1] == '3':
                    if word[i:] == 'rd':
                        return word[0:i], 0
                else:
                    if word[i:] == 'th':
                        return word[0:i], 0
                return None, 0
            else:
                return None, 0
                
        # convert from hex to decimal
        if hex:
            try:
                word = str(int(word, 16))
            except: return None, 0
            
        # fraction
        if nom is not False:
            try:
                word = str(int(word[0:nom]) / int(word[nom+1:]))
            except: pass
            
        # next word is multiplier
        length = len(words)
        if index + 1 < length:
            try:
                tags = vocab[ words[index+1]['word'] ]['tag']
                # if MUNIT in tag and NUMBER in tag
                if Vocabulary.MUNIT in tags and Vocabulary.NUMBER in tags:
                    #   word = word * next word
                    if self.DECIMAL in word:
                        word = str(int(float(word) * int(vocab[ words[index+1]['word'] ]['lemma'][0])))
                    else:
                        word = str(int(word) * int(vocab[ words[index+1]['word'] ]['lemma'][0]))
                    return word, 1
            except: pass
            
        return word, 0
        
    def _isdate(self, words, index):
        """ Check if word sequence is a date """
        length = len(words)
        # Format month dd[,] yy[yy]
        if words[index]['word'] in ['jan', 'january', 'feb', 'february', 'mar', 'march', 'apr', 'april', 'may', 'jun', 'june', 'jul', 'july', 'aug', 'august', 'sep', 'september', 'oct', 'october', 'nov', 'november', 'dec', 'december' ]:
            if index+2 >= length:
                return None, 0
            
            day = words[index+1]['word']
            if not day.isdigit():
                return None, 0
            if int(day) < 10:
                day = '0' + day
             
            if words[index+2]['word'] == ',':
                if index+3 == length:
                    return None, 0
                year = words[index+3]['word']
                n = 3
            else:
                year = words[index+2]['word']
                n = 2
            if not year.isdigit():
                return None, 0
            if len(year) == 2:
                year = '20' + year
                
            months = { 'jan': '01', 'jan.': '01', 'january': '01',
                           'feb': '02', 'feb.': '02', 'february': '02',
                           'mar': '03', 'mar.': '03', 'march': '03',
                           'apr': '04', 'apr.': '04', 'april': '04',
                           'may': '05',
                           'jun': '06', 'jun.': '06', 'june': '06',
                           'jul': '07', 'jul.': '07', 'july': '07',
                           'aug': '08', 'aug.': '08', 'august': '08',
                           'sep': '09', 'sep.': '09', 'september': '09',
                           'oct': '10', 'oct.': '10', 'october': '10',
                           'nov': '11', 'nov.': '11', 'november': '11',
                           'dec': '12', 'dec.': '12', 'december': '12'
            }
            
            # return date in ISO 8601 format
            return  year + '-' + months[words[index]['word']] + '-' + day, n
        # Format: mm/dd/yy[yy] 
        elif '/' in words[index]['word']:
            terms = words[index]['word'].split('/')
            if len(terms) != 3:
                return None, 0
            month = terms[0]
            if not month.isdigit():
                return None, 0
            mm = int(month)
            day = terms[1]
            if not day.isdigit():
                return None, 0
            dd = int(day)
            year = terms[2]
            if not year.isdigit():
                return None, 0
            
            if mm < 1 or mm > 12:
                return None, 0 
            if dd < 1 or dd > 31:
                return None, 0 
            if len(year) == 2:
                yyyy = '20' + year
            elif len(year) == 4:
                yyyy = year
            else:
                return None, 0
                
            if mm < 10:
                mm = '0' + str(mm)
            else:
                mm = str(mm)
            if dd < 10:
                dd = '0' + str(dd)
            else:
                dd = str(dd)
            # return in ISO 8601 format
            return yyyy + '-' + mm + '-' + dd, 1
                
        # Format: mm-dd-yy[yy] or yyyy-mm-dd
        else:
            first = words[index]['word']
            if not first.isdigit():
                return None, 0
            
            index += 2
            if index >= length:
                return None, 0
            if words[index-1]['word'] != '-':
                    return None, 0
            
            second = words[index]['word']
            if not second.isdigit():
                return None, 0
             
            index += 2
            if index >= length:
                return None, 0
            if words[index-1]['word'] != '-':
                return None, 0
     
            third = words[index]['word']
            if not second.isdigit():
                return None, 0

            # ISO 8601
            if len(first) == 4:
                yyyy = first
                mm = int(second)
                if mm < 1 or mm > 12:
                    return None, 0 
                dd = int(third)
                if dd < 1 or dd > 31:
                    return None, 0 
            # US Format
            else:
                mm = int(first)
                if mm < 1 or mm > 12:
                    return None, 0 
                dd = int(second)
                if dd < 1 or dd > 31:
                    return None, 0 
                if len(third) == 2:
                    yyyy = '20' + third
                elif len(third) == 4:
                    yyyy = third
                else:
                    return None, 0
            if mm < 10:
                mm = '0' + str(mm)
            else:
                mm = str(mm)
            if dd < 10:
                dd = '0' + str(dd)
            else:
                dd = str(dd)
            # return in ISO 8601 format
            return yyyy + '-' + mm + '-' + dd, 5

    def _isSSN(self, words, index):
        """ Check if sequence of words is a SSN """
        length = len(words)
        # Expect SSN or Social Security [Number, Num, No,....] prefix
        start = index
        if words[index]['word'] == 'ssn':
            index += 1
        elif words[index]['word'] in ['social', 'soc']:
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '.':
                index += 1
                if index == length:
                    return None, 0
            if words[index]['word'] not in ['security', 'sec']:
                return None, 0
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '.':
                index += 1
                if index == length:
                    return None, 0
            if words[index]['word'] in ['number', 'num', 'no']:
                index += 1
                if words[index]['word'] == '.':
                    index += 1
                    if index == length:
                        return None, 0
        else:
            return None, 0
            
        if index == length:
            return None, 0
            
        while words[index]['tag'] in [ Vocabulary.PUNCT, Vocabulary.SYMBOL ] or words[index]['word'] in ['is', 'of']:
            index += 1
            if index == length:
                return None, 0

        # NNNNNNNNN
        if len(words[index]['word']) == 9 and words[index]['word'].isdigit():
            return words[index]['word'], index - start

        # NNN-NN-NNNN or NNN NN NNNN
        if len(words[index]['word']) == 3:
            ssn = words[index]['word']
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '-':
                index += 1
                if index == length:
                    return None, 0
                    
            if len(words[index]['word']) != 2:
                return None, 0
            ssn += words[index]['word']
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '-':
                index += 1
               
            if len(words[index]['word']) != 4:
                return None, 0
            ssn += words[index]['word']
            
            return ssn, index - start

        return None, 0

    def _isTele(self, words, index):
        """ Check if sequence of words is a USA/CA Telephone """
        length = len(words)
        # Expect Phone, Home, Tele[phone], Cell, Mobile, Work, Fax, Office, Contact
        start = index
        if words[index]['word'] in ['phone', 'tel', 'tele', 'telephone', 'home', 'work', 'office', 'cell', 'mobile', 'fax', 'contact']:
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] in ['number', 'no', 'num', ]:
                index += 1
                if index == length:
                    return None, 0
            
            while words[index]['tag'] in [ Vocabulary.PUNCT, Vocabulary.SYMBOL]  or words[index]['word'] in ['is', 'of']:
                index += 1
                if index == length:
                    return None, 0
            prefix = True
        else: 
            prefix = False
            #return None, 0

        # NNNNNNNNNN
        if prefix == True and len(words[index]['word']) == 10 and words[index]['word'].isdigit():
            return words[index]['word'], index - start
            
        # NNN NNN[sp]NNNN or NNN-NNN-NNNN
        if len(words[index]['word']) == 3 and words[index]['word'].isdigit():
            tele = words[index]['word']
            index += 1
            if index == length:
                return None, 0
                
            if words[index]['word'] in ['-', ')']:
                index += 1
                if index == length:
                    return None, 0
                
            # NNN[-]NNNNNNN
            if len(words[index]['word']) == 7:
                tele += words[index]['word']
                return tele, index - start

            # NNN[-]NNN[-]NNNN
            if len(words[index]['word']) != 3:
                return None, 0
            tele += words[index]['word']
            index += 1
            if index == length:
                return None, 0
            
            if words[index]['word'] == '-':
                index += 1
                if index == length:
                    return None, 0
                    
            if len(words[index]['word']) != 4:
                return None, 0
            tele += words[index]['word']
            
            return tele, index - start
    
        return None, 0
        
    def _isAddr(self, words, index):
        """ Check if sequence of words is a USA/CA Address """
        # Street-Number Street-Direction Street-Name Street-Type [, City, State, Postal]
        
        length = len(words)
        start = index
        
        # POB
        stn = None
        pob, n = self._pob(words, index)
        if pob is not None:
            index += n
            idx_pob = index - 1
            if index == length:
                return 0
            if words[index]['word'] == ',':
                index += 1
                if index == length:
                    return 0
            # Station (Canada)
            stn, n = self._stn(words, index)
            if stn is not None:
                index += n
                idx_stn = index - 1
                if index == length:
                    return 0
                if words[index]['word'] == ',':
                    index += 1
                    if index == length:
                        return 0
        
        # Street Number
        num, n = self._streetnum(words, index)
        if num is None:
            if pob:
                city, state, n, idx_state = self._citystate( words, index )
                words[idx_pob]['word'] = pob
                words[idx_pob]['tag'] = Vocabulary.POB
                if city is not None:
                    words[index]['word'] = city
                    words[index]['tag'] = Vocabulary.CITY
                if state is not None:
                    words[idx_state]['word'] = state
                    words[idx_state]['tag'] = Vocabulary.STATE
                return index + n - start
            else:
                return 0
        
        idx_num = index
        index += n
        if index == length:
           return 0
           
        # Street Direction
        dir, n = self._streetdir(words, index)
        if not dir:
            idx_dir = 0
        else:
            idx_dir = index
        
        index += n
        if index == length:
           return 0
           
        # Street Name / Street Type 
        idx_type = 0
        type = None
        comma    = False
        idx_name = index
        for i in range(4):
            if index + i == length:
                break
            if words[index+i]['word'] == ',':
                comma = True
                break
            try:
                word = vocab[words[index+i]['word']]
                if Vocabulary.STREET_TYPE in word['tag']:
                    index += i
                    idx_type = index
                    itag = word['tag'].index(Vocabulary.STREET_TYPE)
                    type = word['lemma'][itag]
                    if index + 1 < length and words[index+1]['word'] == '.':
                        index += 1
                    break
            except: 
                _dir, n = self._streetdir(words, index + i)
                if _dir != None:
                    index += i + n
                    idx_dir = index
                    dir = _dir
                    break
                
        if idx_type == 0 and idx_dir == 0:
            return 0
            
        index += 1
        # Direction Follows Street Name/Type
        if idx_dir == 0 and index != length:
            dir, n = self._streetdir(words, index)
            if dir != None:
                idx_dir = index
                index += n
            
        # Street Name
        try:
            word = vocab[words[idx_name]['word']]
            if word['lemma'] is not None:
                name = word['lemma'][0]
            else:
                name = words[idx_name]['word']
        except:
            if words[idx_name]['word'][-2:] in [ 'th', 'st', 'nd', 'rd' ]:
                name = words[idx_name]['word'][:-2]
            else:
                name = words[idx_name]['word']
                
        # Multiple Name for street name
        if idx_type - idx_name > 1:
            for i in range(idx_name+1, idx_type):
                name += " " + words[i]['word']
                
        if index < length:
            if words[index]['word'] == ',':
                index += 1

        # POB may follow address
        if index < length: 
            if pob is None:
                pob, n = self._pob(words, index)
                if pob is not None:
                    index += n
                    idx_pob = index - 1
                    if index < length and words[index]['word'] == ',':
                        index += 1
                    stn, n = self._stn(words, index)
                    index += n
                    idx_stn = index - 1
                    if index < length and words[index]['word'] == ',':
                        index += 1
       
        # Secondary Address may follow address
        idx_addr2 = 0
        addr2 = None
        if index < length:
            addr2, n = self._streetaddr2(words, index)
            if addr2:
                idx_addr2 = index
                index += n
                if index < length and words[index]['word'] == ',':
                    index += 1
                 
        # City / State
        idx_city = 0
        city = None
        state = None           
        if index < length: 
            city, state, n, idx_state = self._citystate( words, index )
            idx_city = index
            index += n
            
        # Postal Code
        idx_postal = 0
        postal = None
        if index < length: 
            if state and "CA-" in state:
                postal, n = self._postalcodeCA( words, index )
            else:
                postal, n = self._postalcode( words, index )
            idx_postal = index
            index += n
  
        words[idx_num ]['tag'] = Vocabulary.STREET_NUM
        words[idx_name]['tag'] = Vocabulary.STREET_NAME
        words[idx_name]['word'] = name
        words[idx_num ]['word'] = num
        if pob is not None:
            words[idx_pob]['word'] = pob
            words[idx_pob]['tag'] = Vocabulary.POB
        if stn is not None:
            words[idx_stn]['word'] = stn
            words[idx_stn]['tag'] = Vocabulary.STATION
        if dir is not None:
            words[idx_dir]['tag'] = Vocabulary.STREET_DIR
            words[idx_dir]['word'] = dir
        if type is not None:
            words[idx_type]['word'] = type
            words[idx_type]['tag'] = Vocabulary.STREET_TYPE
        if addr2 is not None:
            words[idx_addr2]['word'] = addr2
            words[idx_addr2]['tag'] = Vocabulary.STREET_ADDR2
        if city is not None:
            words[idx_city]['word'] = city
            words[idx_city]['tag'] = Vocabulary.CITY
        if state is not None:
            words[idx_state]['word'] = state
            words[idx_state]['tag'] = Vocabulary.STATE
        if postal is not None:
            words[idx_postal]['word'] = postal
            words[idx_postal]['tag'] = Vocabulary.POSTAL
        return index - start
        
    def _pob(self, words, index):
        """ Look for Post Office Box 
        PMB digits
        POB digits
        P.O.B digits
        P.O. Box digits
        P.O. digits
        """
        
        start = index
        length = len(words)
        
        if words[index]['word'] == 'pob' or words[index]['word'] == 'pmb':
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '.':
                return words[index+1]['word'], 3
            else:
                return words[index]['word'], 2
        elif words[index]['word'] == 'p':
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '.':
                index += 1
                if index == length:
                    return None, 0
            if words[index]['word'] not in ['o', 'm']:
                return None, 0
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '.':
                index += 1
                if index == length:
                    return None, 0
            if words[index]['word'] in ['b', 'box']:
                index += 1
                if index == length:
                    return None, 0
            elif not words[index]['word'].isdigit():
                return None,0
            if words[index]['word'] == '.':
                index += 1
                if index == length:
                    return None, 0
            return words[index]['word'], index - start + 1
        
        if words[index]['word'] == 'po':
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == 'box':
                index += 1
                if index == length:
                    return None, 0
            return words[index]['word'], index - start + 1
            
        return None, 0
        
    def _stn(self, words, index):
        """ Look for Station
        STN word
        Station word
        """
                
        start = index
        length = len(words)
        
        if index == length:
            return None, 0
        
        if words[index]['word'] == 'stn' or words[index]['word'] == 'station' or words[index]['word'] == 'rpo':
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == '.':
                return words[index+1]['word'], 3
            else:
                return words[index]['word'], 2
                
        return None, 0
              
    def _streetnum(self, words, index):
        """ Look for USA Street Number
        [(N|S|W|E)[-(N|S|W|E)digits]]digits[letter][-][digits]
        """
        
        start = index
        
        if len(words[index]['word']) == 1 and not words[index]['word'][0].isdigit():
            return None, 0
                    
        # [(N|S|W|E)]
        number = words[index]['word']
        if words[index]['word'][0] in ['n', 's', 'w', 'e']:
            word = words[index]['word'][1:]
        else:
            word = words[index]['word']
            
        # digits[letter]
        if not word[0].isdigit():
            return None, 0
            
        index += 1
        if index == len(words):
            return None, 0
            
        # [-][digits|letter]
        if words[index]['word'] == '-':
            index += 1
            if index == len(words):
                return None, 0
            
            # [(N|S|W|E)digits]
            if words[index]['word'][0] in ['n', 's', 'w', 'e'] and words[index]['word'][1:].isdigit():
                number += "-"
            #[letter]
            elif len(words[index]['word']) == 1 and words[index]['word'].isalpha():
                pass
            #[digits]
            elif not words[index]['word'].isdigit():
                index -= 2
            number += words[index]['word']
            index += 1
            if index == len(words):
                return None, 0

        return number, index - start
        
    def _streetdir(self, words, index):
        """ Look for direction """
        first = words[index]['word']
        if index + 1 < len(words):
            second = words[index+1]['word']
        else:
            second = None
        
        if first in ['northwest', 'northeast', 'southwest', 'southeast']:
            return first, 1
            
        elif first == 'nw':
            return "northwest", 1
        elif first == 'ne':
            return "northeast", 1
        elif first == 'sw':
            return "southwest", 1
        elif first == 'se':
            return "southeast", 1
            
        if first in ['n', 'north']:
            if second in ['w', 'west']:
                return "northwest", 2
            elif second in ['e', 'east']:
                return "northeast", 2
            else:
                return "north", 1
        elif first in ['s', 'south']:
            if second in ['w', 'west']:
                return "southwest", 2
            elif second in ['e', 'east']:
                return "southeast", 2
            else:
                return "south", 1
        elif first in ['e', 'east']:
            return "east", 1
        elif first in ['w', 'west']:
            return "west", 1
                
        return None,0
        
    def _streetaddr2(self, words, index):
        """ Check for 2nd (sub-component) of Street Address
        (Apt|Ste|Rm|Fl)word
        """
        start = index
        length = len(words)
        
        if words[index]['word'] == ',':
            index += 1
            if index == length:
                return None, 0  
                
        try:
            v = vocab[words[index]['word']]
            if Vocabulary.STREET_ADDR2 not in v['tag']:
                return None, 0  
            itag = v['tag'].index(Vocabulary.STREET_ADDR2)
            addr2 = v['lemma'][itag]
            
            index += 1
            if index == length:
                return None, 0
              
            # e.g., Apt #3
            if words[index]['word'] == '#':
                index += 1
                if index == length:
                    return None, 0
            
            addr2 += ' ' + words[index]['word']
            
            # e.g., Apt D-13
            if index + 1 < length and words[index+1]['word'] == '-':
                index += 2
                if index == length:
                    return None, 0
                addr2 += words[index]['word']
            
            return addr2, index - start + 1
            
        except:
            return None, 0
        
    def _citystate(self, words, index):
        """ Check if sequence is city, state """
        if words[index]['tag'] != Vocabulary.NAME:
            return None, None, 0, 0
            
        length = len(words)
        city = words[index]['word']
        start = index
            
        index += 1
        if index == length:
            return None, None, 0, 0
            
        if words[index]['word'] == ',':
            index += 1
            if index == length:
                return None, None, 0, 0
 
        elif words[index]['tag'] == Vocabulary.NAME: 
            # Hack
            if words[index]['word'] == 'medical doctor':
                return city, 'ISO3166-2:US-MD', index - start + 1, index
            try:
                state = self._state_dict[words[index]['word']]
                return city, state, index - start + 1, index
            except:
                city += ' ' + words[index]['word']
                index += 1
                if index == length:
                    return None, None, 0, 0
            
            if words[index]['word'] == ',':
                index += 1
                if index == length:
                    return None, None, 0, 0
           
        # D.C. special case
        if words[index]['word'] == 'd' and index + 1 < length and words[index+1]['word'] == 'c':
            return city, "ISO3166-2:US-DC", index - start + 1, index 
        # two word special case
        if words[index]['word'] == 'rhode' and index + 1 < length and words[index+1]['word'] == 'island':
            return city, "ISO3166-2:US-RI", index - start + 1, index
        if words[index]['word'] == 'virgin' and index + 1 < length and words[index+1]['word'] == 'islands':
            return city, "ISO3166-2:US-VI", index - start + 1, index
        if words[index]['word'] == 'puerto' and index + 1 < length and words[index+1]['word'] == 'rico':
            return city, "ISO3166-2:US-PR", index - start + 1, index
        if words[index]['word'] == 'american' and index + 1 < length and words[index+1]['word'] == 'samoa':
            return city, "ISO3166-2:US-AS", index - start + 1, index
        if words[index]['word'] == 'marshall' and index + 1 < length and words[index+1]['word'] == 'islands':
            return city, "ISO3166-2:US-FM", index - start + 1, index
        if words[index]['word'] == 'northern' and index + 1 < length and words[index+1]['word'] == 'marianas':
            return city, "ISO3166-2:US-FM", index - start + 1, index
        if words[index]['word'] == 'british' and index + 1 < length and words[index+1]['word'] == 'columbia':
            return city, "ISO3166-2:CA-BC", index - start + 1, index
        if words[index]['word'] == 'newfoundland' and index + 2 < length and words[index+1]['word'] == 'and':
            return city, "ISO3166-2:CA-NL", index - start + 2, index
        if words[index]['word'] == 'nova' and index + 1 < length and words[index+1]['word'] == 'scotia':
            return city, "ISO3166-2:CA-NS", index - start + 1, index
        if words[index]['word'] == 'prince' and index + 2 < length and words[index+1]['word'] == 'edward':
            return city, "ISO3166-2:CA-PE", index - start + 1, index
 
        # Hack
        if words[index]['word'] == 'medical doctor':
            return city, 'ISO3166-2:US-MD', index - start + 1, index
            
        if words[index]['tag'] not in [Vocabulary.NAME, Vocabulary.ACRONYM]:
            return None, None, 0, 0
                       
        # State Name Prefix
        if words[index]['word'] in [ 'new', 'north', 'south', 'west', 'northwest']:
            index += 1
            if index == length:
                return None, None, 0, 0
            word = words[index-1]['word'] + ' ' + words[index]['word']
        else:
            word = words[index]['word']
            
        try:
            state = self._state_dict[word]
            return city, state, index - start + 1, index
        except: 
            return None, None, 0, 0
        
    _state_dict = {
        'al'            : 'ISO3166-2:US-AL',
        'alabama'       : 'ISO3166-2:US-AL',
        'ak'            : 'ISO3166-2:US-AK',
        'alaska'        : 'ISO3166-2:US-AK',
        'az'            : 'ISO3166-2:US-AZ',
        'arizona'       : 'ISO3166-2:US-AZ',
        'ar'            : 'ISO3166-2:US-AR',
        'arkansas'      : 'ISO3166-2:US-AR',
        'ca'            : 'ISO3166-2:US-CA',
        'california'    : 'ISO3166-2:US-CA',
        'co'            : 'ISO3166-2:US-CO',
        'colorado'      : 'ISO3166-2:US-CO',
        'ct'            : 'ISO3166-2:US-CT',
        'connecticut'   : 'ISO3166-2:US-CT',
        'de'            : 'ISO3166-2:US-DE',
        'delaware'      : 'ISO3166-2:US-DE',
        'dc'            : 'ISO3166-2:US-DC',
        'fl'            : 'ISO3166-2:US-FL',
        'florida'       : 'ISO3166-2:US-FL',
        'ga'            : 'ISO3166-2:US-GA',
        'georgia'       : 'ISO3166-2:US-GA',
        'hi'            : 'ISO3166-2:US-HI',
        'hawaii'        : 'ISO3166-2:US-HI',
        'id'            : 'ISO3166-2:US-ID',
        'idaho'         : 'ISO3166-2:US-ID',
        'il'            : 'ISO3166-2:US-IL',
        'illinois'      : 'ISO3166-2:US-IL',
        'in'            : 'ISO3166-2:US-IN',
        'indiana'       : 'ISO3166-2:US-IN',
        'ia'            : 'ISO3166-2:US-IA',
        'iowa'          : 'ISO3166-2:US-IA',
        'ks'            : 'ISO3166-2:US-KS',
        'kansas'        : 'ISO3166-2:US-KS',
        'ky'            : 'ISO3166-2:US-KY',
        'kentucky'      : 'ISO3166-2:US-KY',
        'la'            : 'ISO3166-2:US-LA',
        'louisiana'     : 'ISO3166-2:US-LA',
        'me'            : 'ISO3166-2:US-ME',
        'maine'         : 'ISO3166-2:US-ME',
        'md'            : 'ISO3166-2:US-MD',
        'maryland'      : 'ISO3166-2:US-MD',
        'ma'            : 'ISO3166-2:US-MA',
        'massachusetts' : 'ISO3166-2:US-MA',
        'mi'            : 'ISO3166-2:US-MI',
        'michigan'      : 'ISO3166-2:US-MI',
        'mn'            : 'ISO3166-2:US-MN',
        'minnesota'     : 'ISO3166-2:US-MN',
        'ms'            : 'ISO3166-2:US-MS',
        'mississippi'   : 'ISO3166-2:US-MS',
        'mo'            : 'ISO3166-2:US-MO',
        'missouri'      : 'ISO3166-2:US-MO',
        'mt'            : 'ISO3166-2:US-MT',
        'montana'       : 'ISO3166-2:US-MT',
        'ne'            : 'ISO3166-2:US-NE',
        'nebraska'      : 'ISO3166-2:US-NE',
        'nv'            : 'ISO3166-2:US-NV',
        'nevada'        : 'ISO3166-2:US-NV',
        'nh'            : 'ISO3166-2:US-NH',
        'new hampshire' : 'ISO3166-2:US-NH',
        'nj'            : 'ISO3166-2:US-NJ',
        'new jersey'    : 'ISO3166-2:US-NJ',
        'nm'            : 'ISO3166-2:US-NM',
        'new mexico'    : 'ISO3166-2:US-NM',
        'ny'            : 'ISO3166-2:US-NY',
        'new york'      : 'ISO3166-2:US-NY',
        'nc'            : 'ISO3166-2:US-NC',
        'north carolina': 'ISO3166-2:US-NC',
        'nd'            : 'ISO3166-2:US-ND',
        'north dakota'  : 'ISO3166-2:US-ND',
        'oh'            : 'ISO3166-2:US-OH',
        'ohio'          : 'ISO3166-2:US-OH',
        'ok'            : 'ISO3166-2:US-OK',
        'oklahoma'      : 'ISO3166-2:US-OK',
        'or'            : 'ISO3166-2:US-OR',
        'oregon'        : 'ISO3166-2:US-OR',
        'pa'            : 'ISO3166-2:US-PA',
        'pennsylvania'  : 'ISO3166-2:US-PA',
        'ri'            : 'ISO3166-2:US-RI',
        'rhode island'  : 'ISO3166-2:US-RI',
        'sc'            : 'ISO3166-2:US-SC',
        'south carolina': 'ISO3166-2:US-SC',
        'sd'            : 'ISO3166-2:US-SD',
        'south dakota'  : 'ISO3166-2:US-SD',
        'tn'            : 'ISO3166-2:US-TN',
        'tennessee'     : 'ISO3166-2:US-TN',
        'tx'            : 'ISO3166-2:US-TX',
        'texas'         : 'ISO3166-2:US-TX',
        'ut'            : 'ISO3166-2:US-UT',
        'utah'          : 'ISO3166-2:US-UT',
        'vt'            : 'ISO3166-2:US-VT',
        'vermont'       : 'ISO3166-2:US-VT',
        'va'            : 'ISO3166-2:US-VA',
        'virginia'      : 'ISO3166-2:US-VA',
        'wa'            : 'ISO3166-2:US-WA',
        'washington'    : 'ISO3166-2:US-WA',
        'wv'            : 'ISO3166-2:US-WV',
        'west virginia' : 'ISO3166-2:US-WV',
        'wi'            : 'ISO3166-2:US-WI',
        'wisconsin'     : 'ISO3166-2:US-WI',
        'wy'            : 'ISO3166-2:US-WY',
        'wyoming'       : 'ISO3166-2:US-WY',
        'vi'            : 'ISO3166-2:US-VI',
        'pr'            : 'ISO3166-2:US-PR',
        'gu'            : 'ISO3166-2:US-GU',
        'guam'          : 'ISO3166-2:US-GU',
        'pw'            : 'ISO3166-2:US-PW',
        'palau'         : 'ISO3166-2:US-PW',
        'fm'            : 'ISO3166-2:US-FM',
        'micronesia'    : 'ISO3166-2:US-FM',
        'as'            : 'ISO3166-2:US-AS',
        'american samoa': 'ISO3166-2:US-AS',
        'mh'            : 'ISO3166-2:US-MH',
        'marshall islands': 'ISO3166-2:US-MH',
        'mp'            : 'ISO3166-2:US-MP',
        'northern marianas': 'ISO3166-2:US-MP',
        'ab'            : 'ISO3166-2:CA-AB',
        'alberta'       : 'ISO3166-2:CA-AB',
        'bc'            : 'ISO3166-2:CA-BC',
        'british columbia' : 'ISO3166-2:CA-BC',
        'mb'            : 'ISO3166-2:CA-MB',
        'manitoba'      : 'ISO3166-2:CA-MB',
        'nb'            : 'ISO3166-2:CA-NB',
        'new brunswick' : 'ISO3166-2:CA-NB',
        'nf'            : 'ISO3166-2:CA-NL',
        'nt'            : 'ISO3166-2:CA-NT',
        'northwest territories': 'ISO3166-2:CA-NT',
        'ns'            : 'ISO3166-2:CA-NS',
        'nova scotia'   : 'ISO3166-2:CA-NS',
        'nu'            : 'ISO3166-2:CA-NU*',
        'nunavat'       : 'ISO3166-2:CA-NU',
        'on'            : 'ISO3166-2:CA-ON',
        'ontario'       : 'ISO3166-2:CA-ON',
        'pe'            : 'ISO3166-2:CA-PE',
        'qc'            : 'ISO3166-2:CA-QC',
        'quebec'        : 'ISO3166-2:CA-QC',
        'québec'        : 'ISO3166-2:CA-QC',
        'sk'            : 'ISO3166-2:CA-SK',
        'saskatchewan'  : 'ISO3166-2:CA-SK',
        'yt'            : 'ISO3166-2:CA-YT',
        'yukon'         : 'ISO3166-2:CA-YT',
    }
    
    def _postalcode(self, words, index):
        """ Check if sequence is a USA postal code """

        length = len(words)
        if words[index]['word'] == ',':
            index += 1
            if index == length:
                return None, 0
                
        # US Postal Code
        if len(words[index]['word']) != 5 or not words[index]['word'].isdigit():
            return None, 0
        postal = words[index]['word']
        
        if index + 1 < length:
            if words[index+1]['word'] == '-':
                index += 2
                if index == length:
                    return None, 0
                if len(words[index]['word']) == 4 and words[index]['word'].isdigit():
                    postal += '-' + words[index]['word']
                    return postal, 3
                else:
                    return postal, 1
                    
        return postal, 1
    
    def _postalcodeCA(self, words, index):
        """ Check if sequence is a Canadian postal code """

        length = len(words)
        
        if words[index]['word'] == ',':
            index += 1
            if index == length:
                return None, 0
                
        if len(words[index]['word']) != 3:
            return None, 0
        postal = words[index]['word']
        index += 1
        if index == length:
            return None, 0
                
        if len(words[index]['word']) != 3:
            return None, 0
        postal += words[index]['word']
                    
        return postal, 2

    def _isGender(self, words, index):
        """ Check if sequence is Gender reference """
        length = len(words)
        
        # Expect Sex|Gender[:] M|F|T
        start = index
        if words[index]['word'] in ['sex', 'gender']:  
            index += 1
            if index == length:
                return None, 0, Vocabulary.UNTAG
            
            while words[index]['tag'] in [ Vocabulary.PUNCT, Vocabulary.SYMBOL]:
                index += 1
                if index == length:
                    return None, 0, Vocabulary.UNTAG
        else:         
            return None, 0, Vocabulary.UNTAG
            
        if words[index]['word'] in ['m', 'male']:
            words[index]['tag'] = Vocabulary.MALE
            return 'male', index - start, Vocabulary.MALE
        elif words[index]['word'] in ['f', 'female']:
            words[index]['tag'] = Vocabulary.FEMALE
            return 'female', index - start, Vocabulary.FEMALE
        elif words[index]['word'] in ['t', 'trans', 'tg', 'transgender']:
            words[index]['tag'] = Vocabulary.TRANSGENDER
            return 'transgender', index - start, Vocabulary.TRANSGENDER
            
        return None, 0, Vocabulary.UNTAG
        
    def _conversion(self):
        """ Do Unit Conversions """
        
        if not self._standard and not self._metric:
            return
            
        l = len(self._words)
        for i in range(1, l):
            tag = self._words[i]['tag']
            if tag == Vocabulary.UNIT and self._words[i-1]['tag'] == Vocabulary.NUMBER:
                unit = self._words[i]['word']
                numb = self._words[i-1]['word']
                if self._standard == True:
                    if unit == "millimeter":
                        self._words[i-1]['word'] = str(float(numb) * 0.0393701)
                        self._words[i]['word'] = "inch"
                    elif unit == "centimeter":
                        self._words[i-1]['word'] = str(float(numb) * 0.393701)
                        self._words[i]['word'] = "inch"
                    elif unit == "meter":
                        self._words[i-1]['word'] = str(float(numb) * 3.28084)
                        self._words[i]['word'] = "feet"
                    elif unit == "kilometer":
                        self._words[i-1]['word'] = str(float(numb) * 0.621371)
                        self._words[i]['word'] = "mile"
                    elif unit == "milliliter":
                        self._words[i-1]['word'] = str(float(numb) * 0.033814)
                        self._words[i]['word'] = "ounce"
                    elif unit == "liter":
                        self._words[i-1]['word'] = str(float(numb) * 0.264172)
                        self._words[i]['word'] = "gallon"
                    elif unit == "kiloliter":
                        self._words[i-1]['word'] = str(float(numb) * 264.172)
                        self._words[i]['word'] = "gallon"
                    elif unit == "milligram":
                        self._words[i-1]['word'] = str(float(numb) * 0.000035274)
                        self._words[i]['word'] = "ounce"
                    elif unit == "gram":
                        self._words[i-1]['word'] = str(float(numb) * 0.035274)
                        self._words[i]['word'] = "ounce"
                    elif unit == "kilogram":
                        self._words[i-1]['word'] = str(float(numb) * 2.20462)
                        self._words[i]['word'] = "pound"
                    elif unit == "square meter":
                        self._words[i-1]['word'] = str(float(numb) * 10.7639)
                        self._words[i]['word'] = "square foot"
                    elif unit == "kilometer per hour":
                        self._words[i-1]['word'] = str(float(numb) * 0.621371)
                        self._words[i]['word'] = "mile per hour"
                    elif unit == "hectera":
                        self._words[i-1]['word'] = str(float(numb) * 2.47105)
                        self._words[i]['word'] = "acre"
                    elif unit == "tonne":
                        self._words[i-1]['word'] = str(float(numb) * 1.10231)
                        self._words[i]['word'] = "ton"
                    elif unit == "cubic meter":
                        self._words[i-1]['word'] = str(float(numb) * 35.3147)
                        self._words[i]['word'] = "cubic foot"
                    elif unit == "square kilometer":
                        self._words[i-1]['word'] = str(float(numb) * 0.386102)
                        self._words[i]['word'] = "square mile"
                elif self._metric == True:
                    if unit == "inch":
                        self._words[i-1]['word'] = str(float(numb) * 2.54)
                        self._words[i]['word'] = "centimeter"
                    elif unit == "foot":
                        self._words[i-1]['word'] = str(float(numb) * 0.3048)
                        self._words[i]['word'] = "meter"
                    elif unit == "yard":
                        self._words[i-1]['word'] = str(float(numb) * 0.9144)
                        self._words[i]['word'] = "meter"
                    elif unit == "mile":
                        self._words[i-1]['word'] = str(float(numb) * 1.60934)
                        self._words[i]['word'] = "kilometer"
                    elif unit == "ounce":
                        self._words[i-1]['word'] = str(float(numb) * 0.0295735)
                        self._words[i]['word'] = "liter"
                    elif unit == "cup":
                        self._words[i-1]['word'] = str(float(numb) * 0.236588)
                        self._words[i]['word'] = "liter"
                    elif unit == "pint":
                        self._words[i-1]['word'] = str(float(numb) * 0.473176)
                        self._words[i]['word'] = "liter"
                    elif unit == "gallon":
                        self._words[i-1]['word'] = str(float(numb) * 3.78541)
                        self._words[i]['word'] = "liter"
                    elif unit == "pound":
                        self._words[i-1]['word'] = str(float(numb) * 0.453592)
                        self._words[i]['word'] = "kilogram"
                    elif unit == "ton":
                        self._words[i-1]['word'] = str(float(numb) * 0.907185)
                        self._words[i]['word'] = "tonne"
                    elif unit == "square foot":
                        self._words[i-1]['word'] = str(float(numb) * 0.092903)
                        self._words[i]['word'] = "square meter"
                    elif unit == "square mile":
                        self._words[i-1]['word'] = str(float(numb) * 2.58999)
                        self._words[i]['word'] = "square kilometer"
                    elif unit == "acre":
                        self._words[i-1]['word'] = str(float(numb) * 0.404686)
                        self._words[i]['word'] = "hectera"
                    elif unit == "mile per hour":
                        self._words[i-1]['word'] = str(float(numb) * 1.60934)
                        self._words[i]['word'] = "kilometer per hour"
                    elif unit == "knot":
                        self._words[i-1]['word'] = str(float(numb) * 1.852)
                        self._words[i]['word'] = "kilometer per hour"     
                        
    
    def _partsofspeech(self):
        """ Do Parts of Speech Tagging """
           
        l = len(self._words)
        for i in range(l):
            self._words[i]['pos'] = pos_tag( [ self._words[i]['word'] ])[0][1]
                        
    def __len__(self):
        """ Override the len() operator - get the number of tokenized words """
        if self._words is None:
            return 0
        return len(self._words)
        
    def __iadd__(self, words):
        """ Overide the += operator """
        if words is None:
            return self
        if isinstance(words, str):
            pass
        elif isinstance(words, list):  
            if self._words is None:
                self._words = words
            else:
                self._words += words
        else:
            raise TypeError("String or List expected for words")
        return self
        
class Address(object):
    """ US/CA Street/Postal Addresses """
    def __init__(self):
        self._pob = None
        self._stn = None
        self._num = None
        self._dir = None
        self._nam = None
        self._typ = None
        self._sec = None
        self._cty = None
        self._sta = None
        self._pst = None
        
    def parse(self, words, index):
        """ Parse an Address """
        self.words = words
        self.index = index
        self.pob()
        self.streetnum()
        self,streetdir()
        self.sreetname()
        self.sreettype()
        self.streetdir()
        self.pob()
        self.addr2()
        self.city()
        self.state()
        self.postal()
        pass
        
    def pob(self):
        """ """
        pass
       
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
        
