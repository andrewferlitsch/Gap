""" Syntax Module for Processing PDF Documents 
Copyright 2018(c), Andrew Ferlitsch
"""

version = '0.9.2'

import re
import json
import os

from nltk.stem import *
import nltk
from nltk import pos_tag
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from unidecode import unidecode

from .vocabulary import Vocabulary, vocab
from .address import Address

        
class Words(object):
    """ Base class for NLP tokenized words """

    DECIMAL		    = '.'	# Standard Unit for Decimal Point
    THOUSANDS 	    = ','	# Standard Unit for Thousandth Separator
    
    def __init__(self, text=None, bare=False, stem='gap', pos=False, roman = False, stopwords=False, punct=False, conjunction=False, article=False, demonstrative=False, preposition=False, question=False, pronoun=False, quantifier=False, date=False, number=False, ssn=False, telephone=False, name=False, address=False, sentiment=False, gender=False, age = False, dob=False, unit=False, standard=False, metric=False, spell=None ):
        """ Constructor 
        text - raw text as string to tokenize
        """
        self._text          = text          # raw text
        self._words         = None          # list of words
        self._punct         = punct         # keep/remove punctuation
        self._stemming      = stem          # on/off stemming
        self._pos           = pos           # on/off parts of speech
        self._roman         = roman         # on/off romanization 
        self._porter        = stopwords     # keep/remove stopwords
        self._bare          = bare          # on/off bare tokenizing
        self._standard      = standard      # convert metric to standard units
        self._metric        = metric        # convert standard to metric units
        self._spell         = None          # spell checking
        self._bow           = None          # bag of words
        self._freq          = None          # word count frequency
        self._tf            = None          # term frequency
        
        # More than just bare tokenizing
        if self._bare == False:
            self._spell = spell                     # do (not) spell checking
            
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
                self._age           = True          # keep age
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
                self._age           = age           # keep/remove age
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
            raise TypeError("Gender must be a boolean")
        if isinstance(age, bool) is False:
            raise TypeError("Age must be a boolean")
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
        if spell is not None:
            if spell not in ['en', 'fr', 'es', 'it', 'de']:
                raise ValueError("Wrong value for spell: en, es, fr, it or de")
            
        if text is not None:
            self._split()
            if self._bare == False:
                # preprocess the tokens
                self._preprocess()
                # word stemming
                if self._stemming == 'gap':
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
                    # decimal, thousandths, fraction symbol
                    if word[i] in ['.', ',', '/'] and i < length-1 and word[i+1].isdigit():
                        continue
                    # degree
                    if word[i] in ['°'] and i < length-1 and word[i+1] in [ 'f', 'F', 'c', 'C']:
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
                if word['word'].isupper() and not word['word'][0].isdigit() and not  word['word'][0] == '°':
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
                            
                # lowercase
                word['word'] = word['word'].lower()
                # romanize
                if self._roman:
                    word['word'] = unidecode(word['word'])
                _words.append(word)
                
        self._words = _words
                
    def _stem(self):
        """ Word stemming """

        length = len(self._words)
        for i in range(length):
            word = self._words[i]['word']
            l = len(word)

            # Don't stem words already categorized
            if self._words[i]['tag'] != Vocabulary.UNTAG:
                continue
                
            # Do spell checking
            if self._spell is not None:
                spell = Norvig( self._spell)
                replace = spell.correction(self._words[i]['word'])
                self._words[i]['word'] = replace
                
            # If in vocabulary, do not stem
            try:
                v = vocab[word]
                t = v['tag']
                if len(t) == 1:
                    if t[0] not in [ Vocabulary.QUANTIFIER, Vocabulary.UNIT, Vocabulary.MEASUREMENT ]:
                        l = v['lemma']
                        if l is not None:
                            self._words[i]['word'] = l[0]
                            self._words[i]['tag']  = t[0]
                continue
            except: pass
            
            # Don't stem short words
            if l < 4:
                continue
                        
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
                elif word.endswith("tring") or word.endswith("yzing") or word.endswith("ysing"):
                    self._words[i]['word'] = word[0:-3] + 'e'
                elif word.endswith("ding") or word.endswith("king") or word.endswith("zing") or word.endswith("ting"):
                    if self._words[i]['word'][-5] in ['a', 'e', 'i', 'o', 'u', 'y']:
                        self._words[i]['word'] = word[0:-3] + 'e'
                    else:
                        self._words[i]['word'] = word[0:-3]
                elif word.endswith("ving"):
                    self._words[i]['word'] = word[0:-3] + 'e'
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
                elif word.endswith("tred") or word.endswith("nced") or word.endswith("psed") or word.endswith("ysed") or word.endswith("yzed"):
                    self._words[i]['word'] = word[0:-1]
                elif word.endswith("mmed"):
                    self._words[i]['word'] = word[0:-3]
                elif word.endswith("ied"):
                    self._words[i]['word'] = word[0:-3] + 'y'
                elif word.endswith("zed") or word.endswith("ved"):
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
                elif word.endswith("ncer"):
                    self._words[i]['word'] = word[0:-1]
                elif word.endswith("ier"):
                    self._words[i]['word'] = word[0:-3] + 'y'
                elif word.endswith("der"):
                    self._words[i]['word'] = word[0:-1]
                elif word.endswith("er"):
                    self._words[i]['word'] = word[0:-2]
                    
            if l > 5:
                # Superlative endings
                if word.endswith("iest"):
                    self._words[i]['word'] = word[0:-4] + 'y'
                elif word.endswith("est"):
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
                elif word.endswith("able"):
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
        measurement = False
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
                w, n = self._isDate(self._words, i)
                if w is not None:
                    skip = n
                    if len(words) > 0 and words[-1]['word'] in ['birth', 'birthdate', 'birthday', 'DOB', 'dob']:
                        if self._dob is True:
                            words[-1] = {'word': w, 'tag': Vocabulary.DOB }
                    elif len(words) > 1 and words[-1]['word'] == 'date' and words[-2]['word'] == 'birth':
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
                w, n, tag = self._isTele(self._words, i)
                if w is not None:
                    skip = n
                    if self._telephone is True:
                        words.append( {'word': w, 'tag': tag } )
                    continue

                # Check if this word or sequence of words is a USA/CA Address
                n = self._isAddr(self._words, i)
                if n > 0:
                    skip = n
                    if self._address is True:
                        for _x in range(i, i+skip):
                            if self._words[_x]['tag'] in [ Vocabulary.STREET_NUM, Vocabulary.STREET_DIR, 
                                                           Vocabulary.STREET_NAME, Vocabulary.STREET_TYPE,
                                                           Vocabulary.POB, Vocabulary.SAC, 
                                                           Vocabulary.CITY, Vocabulary.STATE, Vocabulary.POSTAL,
                                                           Vocabulary.STATION]:
                                words.append( self._words[_x] )
                    skip -= 1
                    continue
                    
                # Check if this word is a gender reference
                w, n = self._isAge(self._words, i)
                if w is not None:
                    skip = n
                    if self._age is True:
                        words.append( {'word': w, 'tag': Vocabulary.AGE } )
                    continue
  
                # Check if this word is a number
                w, n = self._isNumber(self._words, i)
                if w is not None:
                    skip = n
                    if self._number is True or self._unit is True:
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
                        
                        if measurement:
                            if i + 1 < nwords:
                                if self._words[i+1]['word'] == "'":
                                    words.append( {'word': 'foot', 'tag': Vocabulary.UNIT } )
                                    i += 1
                                    continue
                                if self._words[i+1]['word'] == '"':
                                    words.append( {'word': 'inch', 'tag': Vocabulary.UNIT } )
                                    i += 1
                                    continue
                            measurement = False
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
                                if self._words[i-1]['word'] != 'and':
                                    words[-1]['tag'] = Vocabulary.POSITIVE
                            else:
                                words.append({'word': word, 'tag': Vocabulary.NEGATIVE})
                    elif tag[0] == Vocabulary.UNIT:
                        if self._unit == True:
                            if len(word) > 1:
                                words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.UNIT})
                            else:
                                words.append({ 'word': word, 'tag': Vocabulary.UNTAG})
                    elif tag[0] == Vocabulary.MEASUREMENT:
                        if self._unit == True:
                            if len(word) > 1:
                                words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.MEASUREMENT})
                                measurement = True
                            else:
                                words.append({ 'word': word, 'tag': Vocabulary.UNTAG})
                    elif tag[0] == Vocabulary.NUMBER:
                        if self._number == True or self._unit == True:
                            words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.NUMBER})
                    elif tag[0] == Vocabulary.PORTER:
                        if self._porter == True:
                            words.append({ 'word': word, 'tag': Vocabulary.PORTER})
                    elif tag[0] in [ Vocabulary.ADDRESS, Vocabulary.STREET_TYPE, Vocabulary.SAC ]:
                        # Not an Address
                        words.append({ 'word': word, 'tag': Vocabulary.UNTAG})
                    elif tag[0] == Vocabulary.UNTAG:
                        words.append({ 'word': vocab[word]['lemma'][0], 'tag': Vocabulary.UNTAG})
                    continue
                except:
                    words.append({ 'word': word, 'tag': tag[0] } )
            else:
                if self._punct != False:
                    words.append(self._words[i])
                    continue
                    
        self._words = words
            
    def _isNumber(self, words, index):
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
        
    def _isDate(self, words, index):
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
        
        tag = Vocabulary.TELEPHONE
        length = len(words)
        
        # Expect Phone, Home, Tele[phone], Cell, Mobile, Work, Fax, Office, Contact
        start = index
        if words[index]['word'] in ['phone', 'tel', 'tele', 'telephone', 'home', 'work', 'office', 'cell', 'mobile', 'fax', 'contact', 'support']:
            if words[index]['word'] == 'home':
                tag = Vocabulary.TELEPHONE_HOME
            elif words[index]['word'] in ['work', 'office']:
                tag = Vocabulary.TELEPHONE_WORK
            elif words[index]['word'] in ['cell', 'mobile']:
                tag = Vocabulary.TELEPHONE_CELL
            elif words[index]['word'] in ['fax']:
                tag = Vocabulary.TELEPHONE_FAX

            index += 1
            if index == length:
                return None, 0, 0
            if words[index]['word'] in ['number', 'no', 'num', ]:
                index += 1
                if index == length:
                    return None, 0, 0
            
            while words[index]['tag'] in [ Vocabulary.PUNCT, Vocabulary.SYMBOL]  or words[index]['word'] in ['is', 'of']:
                index += 1
                if index == length:
                    return None, 0, 0
            prefix = True
        else: 
            prefix = False
            
        tele = ""

        # NNNNNNNNNN
        if prefix == True and len(words[index]['word']) == 10 and words[index]['word'].isdigit():
            return words[index]['word'], index - start, tag

        # 1NNNNNNNNNN
        if prefix == True and len(words[index]['word']) == 11 and words[index]['word'].isdigit() and words[index]['word'][0] == '1':
            return words[index]['word'], index - start, tag
            
        if '.' in words[index]['word']:
            toks = words[index]['word'].split('.')
            if len(toks) == 3:
                for i in range(3):
                    if not toks[i].isdigit():
                        return None, 0, 0
                    tele += toks[i]
                return tele, index - start, tag
            if len(toks) == 4:
                tele = "1"
                if toks[0] != '1':
                    return None, 0, 0
                for i in range(1,4):
                    if not toks[i].isdigit():
                        return None, 0, 0
                    tele += toks[i]
                return tele, index - start, tag
            
        # International Prefix
        if len(words[index]['word']) == 1 and words[index]['word'] == '1':
            tele = "1"
            index += 1
            if index == length:
                return None, 0, 0
                
            if words[index]['word'] in ['-', '.']:
                index += 1
                if index == length:
                    return None, 0, 0
                    
        if words[index]['word'] == '(':
            index += 1
            if index == length:
                return None, 0, 0
            
        # NNN NNN[sp]NNNN or NNN-NNN-NNNN
        if len(words[index]['word']) == 3 and words[index]['word'].isdigit():
            tele += words[index]['word']
            index += 1
            if index == length:
                return None, 0, 0
                
            if words[index]['word'] in ['-', '.', ')']:
                index += 1
                if index == length:
                    return None, 0, 0
                
            # NNN[-]NNNNNNN
            if len(words[index]['word']) == 7:
                tele += words[index]['word']
                return tele, index - start, tag

            # NNN[-]NNN[-]NNNN
            if len(words[index]['word']) != 3:
                return None, 0, 0
            tele += words[index]['word']
            index += 1
            if index == length:
                return None, 0, 0
            
            if words[index]['word'] in ['-', '.']:
                index += 1
                if index == length:
                    return None, 0, 0
                    
            if len(words[index]['word']) != 4:
                return None, 0, 0
            tele += words[index]['word']
            
            return tele, index - start, tag
    
        return None, 0, 0
        
    def _isAddr(self, words, index):
        """ Check if sequence of words is a USA/CA Address """
        # Street-Number Street-Direction Street-Name Street-Type [, City, State, Postal]
        
        start = index
        addr = Address(words, index)
        if addr.is_addr():
            return addr.index - start
        else:
            return 0

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
        
    def _isAge(self, words, index):
        """ Check if sequence is age reference """
        start = index
        length = len(words)
        
        # [age[:]] number [yr/yrs] [old]
        if words[index]['word'] == 'age':
            index += 1
            if index == length:
                return None, 0
            if words[index]['word'] == ':':
                index += 1
                if index == length:
                    return None, 0
            age_key = True
        else:
            age_key = False
            
        if not words[index]['word'].isdigit():
            return None, 0
            
        age = words[index]['word']
        
        index += 1
        if index < length:
            if words[index]['word'] in [ 'yr', 'yrs', 'year', 'years' ]:
                age_key = True
                index += 1
                if index < length:
                    if words[index]['word'] == 'old':
                        index += 1
                        
        if age_key:
            return age, index - start - 1
            
        return None, 0
        
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
            
    @property
    def bagOfWords(self):
        """ Generate/return Bag of Words """
        if self._bow is None:
            self._bow = {}
            for word in self._words:
                if word['word'] in self._bow:
                    self._bow[word['word']] += 1
                else:
                    self._bow[word['word']] = 1
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
        if self._tf is None:
            nwords = len(self)
            self._tf = []
            for t in self.freqDist:
                self._tf.append( ( t[0], t[1] / nwords ) )
        return self._tf
                
            
                        
    def __len__(self):
        """ Override the len() operator - get the number of tokenized words """
        if self._words is None:
            return 0
        return len(self._words)
        
    def __iadd__(self, words):
        """ Override the += operator """
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
        
from .lg.word2int_en import word2int_en
from .lg.word2int_fr import word2int_fr
from .lg.word2int_es import word2int_es
from .lg.word2int_it import word2int_it
from .lg.word2int_de import word2int_de
        
class Norvig(object):
    """ 
    https://norvig.com/spell-correct.html
    
    Enhanced version of the Norvig spell checker. Enhancements designed by Andrew Ferlitsch and coded by David Molina.
    In the original Norvig spell checker, guess of what would be the next character replacement to try was in alphabetical order.
    In this enhancement, the next character is based on the QWERTY keyboard layout and the likelihood that the hand shifted one key.
    """
    
    def __init__(self, lang='en'):
        global word2int_en, word2int_fr, word2int_es, word2int_it, word2int_de
        if lang == 'en':
            self.word2int = word2int_en
        elif lang == 'es':
            self.word2int = word2int_es
        elif lang == 'fr':
            self.word2int = word2int_fr
        elif lang == 'it':
            self.word2int = word2int_it
        elif lang == 'de':
            self.word2int = word2int_de
                    
    def known(self, words): 
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.word2int)

    def edits1(self, word):
        "All edits that are one edit away from `word`."
        letters={'a': 'asqzbcdefghijklmnoprtuvwxy',
                 'b': 'bnvghacdefijklmopqrstuwxyz',
                 'c': 'cvxdfabeghijklmnopqrstuwyz',
                 'd': 'dfsexcabghijklmnopqrtuvwyz',
                 'e': 'erwsdabcfghijklmnopqtuvxyz',
                 'f': 'fgdrcvabehijklmnopqstuwxyz',
                 'g': 'ghftvbacdeijklmnopqrsuwxyz',
                 'h': 'hjgybnacdefiklmopqrstuvwxz',
                 'i': 'ioujkabcdefghlmnpqrstvwxyz',
                 'j': 'jkhunmabcdefgilopqrstvwxyz',
                 'k': 'kljimabcdefghnopqrstuvwxyz',
                 'l': 'lkoabcdefghijmnpqrstuvwxyz',
                 'm': 'mnjkabcdefghilopqrstuvwxyz',
                 'n': 'nmbhjacdefgiklopqrstuvwxyz',
                 'o': 'opiklabcdefghjmnqrstuvwxyz',
                 'p': 'polabcdefghijkmnqrstuvwxyz',
                 'q': 'qwabcdefghijklmnoprstuvxyz',
                 'r': 'rtedfabcghijklmnopqsuvwxyz',
                 's': 'sdawzxbcefghijklmnopqrtuvy',
                 't': 'tyrfgabcdehijklmnopqsuvwxz',
                 'u': 'uiyhjabcdefgklmnopqrstvwxz',
                 'v': 'vbcfgadehijklmnopqrstuwxyz',
                 'w': 'weqasbcdfghijklmnoprtuvxyz',
                 'x': 'xczsdabefghijklmnopqrtuvwy',
                 'y': 'yutghabcdefijklmnopqrsvwxz',
                 'z': 'zxasbcdefghijklmnopqrtuvwy'}
        splits     = [(word[:i], word[i:])    for i in range(1, len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters[R[0]]]
        inserts    = [L + c + R               for L, R in splits if R for c in letters[R[0]]]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self, word): 
        """All edits that are two edits away from `word`."""
        return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

    def candidates(self, word): 
        """Generate possible spelling corrections for word."""
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])
        
    def correction(self, word):
        k = self.candidates(word)
        return k.pop()
        
    def encode(self, word):
        global word2int
        k = self.candidates(word)
        word = k.pop()
        try:
            intval = self.word2int[word]
            return word, intval
        except:
            return '<OUT>', self.word2int['<OUT>']