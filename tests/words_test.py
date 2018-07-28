# -*- coding: utf-8 -*-
"""
Copyright, 2018(c), Andrew Ferlitsch
"""
from syntax import Words
import unittest
import pytest
import os
import sys

class MyTest(unittest.TestCase):
    def setup_class(self):
        pass
            
    def teardown_class(self):
        pass
        
    def test_001(self):
        """ Words constructor  = no parameters """
        words = Words()
        self.assertEqual(words.words, None)
        self.assertEqual(len(words), 0)

    def test_002(self):
        """ Words constructor  = text is not a string """
        with pytest.raises(TypeError):
            words = Words(12)
        
    def test_003(self):
        """ Words constructor  = number is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", number=12)
        
    def test_004(self):
        """ Words constructor  = quantifier is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", quantifier=12)
        
    def test_005(self):
        """ Words constructor  = preposition is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", preposition=12)
        
    def test_006(self):
        """ Words constructor  = conjunction is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", conjunction=12)
        
    def test_007(self):
        """ Words constructor  = date is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", date=12)
        
    def test_008(self):
        """ Words constructor  = article is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", article=12)
        
    def test_009(self):
        """ Words constructor  = demonstrative is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", demonstrative=12)
        
    def test_010(self):
        """ Words constructor  = question is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", question=12)
        
    def test_011(self):
        """ Words constructor  = pronoun is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", pronoun=12)
        
    def test_012(self):
        """ Words constructor  = ssn is not a bool """
        with pytest.raises(TypeError):
            words = Words("ssn", ssn=12)
        
    def test_013(self):
        """ Words constructor  = telephone is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", telephone=12)
        
    def test_014(self):
        """ Words constructor  = name is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", name=12)
        
    def test_015(self):
        """ Words constructor  = address is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", address=12)
        
    def test_016(self):
        """ Words constructor  = punct is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", punct=12)
            
    def test_017(self):
        """ Words constructor  = gender is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", gender=12)
		
    def test_018(self):
        """ Words constructor  = sentiment is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", sentiment=12)  
            
    def test_019(self):
        """ Words constructor  = stopwords is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", stopwords=12)   
        
    def test_020(self):
        """ Words constructor  = dob is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", dob=12)      
        
    def test_021(self):
        """ Words constructor  = bare is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", bare=12)      
        
    def test_022(self):
        """ Words text getter """
        words = Words("hello world, goodbye. Hello again.", bare=True)
        self.assertEqual(words.text, "hello world, goodbye. Hello again.")
        
    def test_023(self):
        """ Words words getter """
        words = Words("hello world, goodbye. Hello again.", bare=True)
        self.assertEqual(towords(words.words), ['hello', 'world', ',', 'goodbye', '.', 'Hello', 'again', '.'])
        
    def test_024(self):
        """ Words overridden len() operator """
        words = Words()
        self.assertEqual(len(words), 0)
        words = Words("hello world, goodbye. Hello again.", bare=True)
        self.assertEqual(len(words), 8)
        
    def test_025(self):
        """ Words overridden += operator - None """
        words = Words("hello world, goodbye", bare=True)
        words += None
        self.assertEqual(towords(words.words), ['hello', 'world', ',', 'goodbye'])
        self.assertEqual(len(words), 4)
        
    def test_026(self):
        """ Words overridden += operator - not a string or list """
        words = Words("hello world, goodbye", bare=True)
        with pytest.raises(TypeError):
            words += 12
        
    def test_027(self):
        """ Words bare processing - punctuation """
        words = Words("hello world", bare=True)
        self.assertEqual(words.words, [{'word': 'hello', 'tag': 0}, {'word': 'world', 'tag': 0}])
        words = Words("hello, world! : ; ?", bare=True)
        self.assertEqual(words.words, [{'word': 'hello', 'tag': 0}, {'word': ',', 'tag': 23}, {'word': 'world', 'tag': 0}, {'word': '!', 'tag': 23}, {'word': ':', 'tag': 23}, {'word': ';', 'tag': 23}, {'word': '?', 'tag': 23}])

    def test_028(self):
        """ Words bare processing - punctuation [] () """
        words = Words("[hello] (world)", bare=True)
        self.assertEqual(words.words, [{'word': '[', 'tag': 23}, {'word': 'hello', 'tag': 0}, {'word': ']', 'tag': 23}, {'word': '(', 'tag': 23}, {'word': 'world', 'tag': 0}, {'word': ')', 'tag': 23}])
        
    def test_029(self):
        """ Words bare processing - punctuation ' and " """
        words = Words("he said, 'hello'.", bare=True)
        self.assertEqual(words.words, [{'word': 'he', 'tag': 0}, {'word': 'said', 'tag': 0}, {'word': ',', 'tag': 23}, {'word': '\'', 'tag': 23}, {'word': 'hello', 'tag': 0}, {'word': '\'', 'tag': 23}, {'word': '.', 'tag': 23}])
        words = Words("he said, \"hello\".", bare=True)
        self.assertEqual(words.words, [{'word': 'he', 'tag': 0}, {'word': 'said', 'tag': 0}, {'word': ',', 'tag': 23}, {'word': '"', 'tag': 23}, {'word': 'hello', 'tag': 0}, {'word': '"', 'tag': 23}, {'word': '.', 'tag': 23}])
        
    def test_030(self):
        """ Words bare processing - symbols """
        words = Words("45*16", bare=True)
        self.assertEqual(words.words, [{'word': '45', 'tag': 0}, {'word': '*', 'tag': 24}, {'word': '16', 'tag': 0}])
                
    def test_031(self):
        """ Words bare processing - sign symbol """
        words = Words("2-1 2+1 -1 +2", bare=True)
        self.assertEqual(words.words, [{'word': '2', 'tag': 0}, {'word': '-', 'tag': 24}, {'word': '1', 'tag': 0}, {'word': '2', 'tag': 0}, {'word': '+', 'tag': 24}, {'word': '1', 'tag': 0}, {'word': '-1', 'tag': 0}, {'word': '+2', 'tag': 0}])
        words = Words("log(-10)", bare=True)
        self.assertEqual(words.words, [{'word': 'log', 'tag': 0}, {'word': '(', 'tag': 23}, {'word': '-10', 'tag': 0}, {'word': ')', 'tag': 23}])
        
    def test_032(self):
        """ Words contractions """
        words = Words("can't I'll must've ", bare=True)
        self.assertEqual(towords(words.words), ["can", "not", "I", "will", "must", "have" ])   
        words = Words("parent's parents' ", bare=True)
        self.assertEqual(towords(words.words), ["parent", "is", "parents" ]) 
       
    def test_033(self):
        """ Words _split() - replace newlines """
        words = Words("one\ntwo\n three\n", bare=True)
        self.assertEqual(towords(words.words), ['one', 'two', 'three'])
        
    def test_034(self):
        """ Words _split() - replace carriage return """
        words = Words("one\r\ntwo\r\n three\r\n", bare=True)
        self.assertEqual(towords(words.words), ['one', 'two', 'three'])
        
    def test_035(self):
        """ Words _split() - replace tabs """
        words = Words("one\ttwo\t three\t", bare=True)
        self.assertEqual(towords(words.words), ['one', 'two', 'three'])
        
    def test_036(self):
        """ Words _split() - remove leading/trailing whitespace """
        words = Words(" one two three ", bare=True)
        self.assertEqual(towords(words.words), ['one', 'two', 'three'])
        
    def test_037(self):
        """ Words _split() - remove duplicate whitespace """
        words = Words("one   two three", bare=True)
        self.assertEqual(towords(words.words), ['one', 'two', 'three'])    
        
    def test_038(self): 
        """ Words - remove non-printable ASCII chars"""
        words = Words('abc \0\1\2\3\4\5\6\7 def', bare=True)
        self.assertEqual(towords(words.words), ['abc', 'def'])   
        
    def test_039(self):  
        """ Words _preprocess """
        words = Words("hello, again.", stopwords=True, punct=True)
        self.assertEqual(towords(words.words), ['hello', ',', 'again', '.'])    
        
    def test_040(self):
        """ Words _preprocess() - empty string """
        words = Words("")
        self.assertEqual(words.words, [])
        words = Words()
        self.assertEqual(words.words, None)
        words = Words(None)
        self.assertEqual(words.words, None)
        
    def test_041(self):
        """ Words _preprocess() - Acronyms """
        words = Words("ABC Company MAGIC", name=True)
        self.assertEqual(towords(words.words), ['abc', 'company', 'magic'])
        words = Words("ABC Company", name=True)
        self.assertEqual(words.words, [{ 'word': 'abc', 'tag': 11 }, { 'word': 'company', 'tag': 11 }])
 
    def test_042(self):
        """ Words _preprocess() - lowercase uppercase title """
        words = Words("MEDICAL COVERAGE GUIDELINE ORIGINAL EFFECTIVE DATE")
        self.assertEqual(towords(words.words), ['medical', 'coverage', 'guideline', 'original', 'effective', 'date'])
        
    def test_043(self):
        """ Words _split() - lowercase - uppercased words """
        words = Words("ZOO KID")
        self.assertEqual(towords(words.words), ['zoo', 'kid'])   
        
    def test_044(self):
        """ Words _split() - lowercase - Capitalized words """
        words = Words("name James R Smith", name=True)
        self.assertEqual(words.words, [{ 'word': 'name', 'tag': 0 }, { 'word': 'james', 'tag': 11 }, { 'word': 'r', 'tag': 11 }, { 'word': 'smith', 'tag': 11 }]) 
        
    def test_045(self):
        """ Words _split() - lowercase - single uppercase word per line """
        words = Words("name James\nR\nSmith", name=True)
        self.assertEqual(words.words, [{ 'word': 'name', 'tag': 0 }, { 'word': 'james', 'tag': 11 }, { 'word': 'r', 'tag': 11 }, { 'word': 'smith', 'tag': 11 }])    
        
    def test_046(self):
        """ Words _split() - lowercase - Capitalized words """
        words = Words("name James R. Smith", name=True)
        self.assertEqual(words.words, [{ 'word': 'name', 'tag': 0 }, { 'word': 'james', 'tag': 11 }, { 'word': 'r', 'tag': 11 }, { 'word': 'smith', 'tag': 11 }]) 
        
    def test_047(self):
        """ Words _split() - lowercase - Capitalized words, punctuation """
        words = Words("Zoo, Ugly. Goat", punct=True, stopwords=True)
        self.assertEqual(words.words, [{ 'word': 'zoo', 'tag': 0 }, { 'word': ',', 'tag': 23 }, { 'word': 'ugly', 'tag': 11 }, { 'word': '.', 'tag': 23 }, { 'word': 'goat', 'tag': 0 }]) 
       
    def test_048(self):
        """ Words _split() - name title - Capitalized words """
        words = Words("name Dr James R Smith", stopwords=True)
        self.assertEqual(words.words, [{ 'word': 'name', 'tag': 0 }, { 'word': 'doctor', 'tag': 33 }, { 'word': 'james', 'tag': 11 }, { 'word': 'r', 'tag': 11 }, { 'word': 'smith', 'tag': 11 }]) 
            
    def test_049(self):
        """ Words _split() - name title with periods - Capitalized words """
        words = Words("name Dr. James R. Smith", stopwords=True)
        self.assertEqual(words.words, [{ 'word': 'name', 'tag': 0 }, { 'word': 'doctor', 'tag': 33 }, { 'word': 'james', 'tag': 11 }, { 'word': 'r', 'tag': 11 }, { 'word': 'smith', 'tag': 11 }]) 
             
    def test_050(self):
        """ Words _split() - no space after punctuation """
        words = Words("zoo.hot", punct=True)
        self.assertEqual(towords(words.words), ['zoo', '.', 'hot'])
        
    def test_051(self):
        """ Words _split() - math symbols """
        words = Words("1+2=3", punct=True, number=True)
        self.assertEqual(towords(words.words), ['1', '+', '2', '=', '3'])     
  
    def test_052(self):
        """ Words _stem reduce dden and tten """
        words = Words("ridden bitten gotten", stopwords=True)
        self.assertEqual(towords(words.words), [ 'ride', 'bite', 'get' ]) 
        
    def test_053(self):
        """ Words _stem reduce nning dding tting """
        words = Words("planning hope spitting")
        self.assertEqual(towords(words.words), [ 'plan', 'hope', 'spit' ]) 
        
    def test_054(self):
        """ Words _stem reduce ing """
        words = Words("bring ding cling riding flying boating boring thing flattening biking excluding giving", stopwords=True)
        self.assertEqual(towords(words.words), [ 'bring', 'ding', 'cling', 'ride', 'fly', 'boat', 'bore', 'thing', 'flat', 'bike', 'exclude', 'give']) 
        
    def test_055(self):
        """ Words _stem reduce ies, ied, ier """
        words = Words("flies flier cries cried tied costlier libraries")
        self.assertEqual(towords(words.words), [ 'fly', 'fly', 'cry', 'cry', 'tied', 'cost', 'library' ])  
        
    def test_056(self):
        """ Words _stem reduce ves """
        words = Words("leaves wolves")
        self.assertEqual(towords(words.words), [ 'leaf', 'wolf' ])  
        
    def test_057(self):
        """ Words _stem reduce des, nes, ces, ees """
        words = Words("tides rides bees enhances planes includes", stopwords=True)
        self.assertEqual(towords(words.words), [ 'tide', 'ride', 'bee', 'enhance', 'plane', 'include' ])  
        
    def test_058(self):
        """ Words _stem reduce der """
        words = Words("under rider", stopwords=True)
        self.assertEqual(towords(words.words), [ 'under', 'ride' ])    
        
    def test_059(self):
        """ Words _stem reduce es, ed mmed oes"""
        words = Words("classes, planted, walked tracked trimmed toes tomatoes potatoes roses")
        self.assertEqual(towords(words.words), [ 'class', 'plant', 'walk', 'track', 'trim', 'toe', 'tomato', 'potato', 'rose' ])      
        
    def test_060(self):
        """ Words _stem reduce nned """
        words = Words("tanned canned", stopwords=True)
        self.assertEqual(towords(words.words), [ 'tan', 'can' ])    
        
    def test_061(self):
        """ Words _stem reduce er """
        words = Words("under boxer fighter climber number", stopwords=True)
        self.assertEqual(towords(words.words), [ 'under', 'boxer', 'fight', 'climb', 'number' ])      
        
    def test_062(self):
        """ Words _stem reduce ers """    
        words = Words("boxers fighters climbers numbers", stopwords=True)
        self.assertEqual(towords(words.words), [ 'boxer', 'fight', 'climb', 'number' ])      
        
    def test_063(self):
        """ Words _stem reduce ly """       
        words = Words("costly particularly")
        self.assertEqual(towords(words.words), [ 'cost', 'particular' ])      
        
    def test_064(self):
        """ Words _stem reduce ss """         
        words = Words("class bass")  
        self.assertEqual(towords(words.words), [ 'class', 'bass' ])        
        
    def test_065(self): 
        """ Words _stem reduce s """           
        words = Words("cars books bikes trains")     
        self.assertEqual(towords(words.words), [ 'car', 'book', 'bike', 'train' ])        
        
    def test_066(self): 
        """ Words _stem Porter list """              
        words = Words("always another at consider during do does exclude for from further fully given give gives having here however if include including likes later member minus nothing never only order other orderings pending perhaps plus possibly rather really")     
        self.assertEqual(towords(words.words), [])          
        
    def test_067(self): 
        """ Words _stem remove est """
        words = Words("greatest least biggest smallest", stopwords=True)
        self.assertEqual(towords(words.words), ['great', 'least', 'big', 'small'])     
        
    def test_068(self): 
        """ Words _stem remove zing zed endings """
        words = Words("desensitized anesthetizing; paralyzing")
        self.assertEqual(towords(words.words), [ 'desensitize', 'anesthetize', 'paralyze'])      
        
    def test_069(self): 
        """ Words _stem more word endings """
        words = Words("endings suites features passes", stopwords=True)
        self.assertEqual(towords(words.words), ['end', 'suite', 'feature', 'pass']) 
           
    def test_070(self): 
        """ Words _stem misc word endings """
        words = Words("biggest largest greatest smallest latest taken hidden youngest", stopwords=True)
        self.assertEqual(towords(words.words), ['big', 'large', 'great', 'small', 'late', 'take', 'hide', 'young'])    
  
    def test_071(self):
        """ Words _stem reduce dden and tten """
        words = Words("ridden bitten gotten")
        self.assertEqual(towords(words.words), [ 'ride', 'bite' ]) 
        
    def test_072(self):
        """ Words _stem reduce nning dding tting """
        words = Words("planning hope spitting")
        self.assertEqual(towords(words.words), [ 'plan', 'hope', 'spit' ]) 
        
    def test_073(self):
        """ Words _stem reduce ing """
        words = Words("bring ding cling riding flying boating boring thing flattening biking excluding giving")
        self.assertEqual(towords(words.words), [ 'bring', 'ding', 'cling', 'ride', 'fly', 'boat', 'flat', 'bike']) 
        
    def test_074(self):
        """ Words _stem reduce ies, ied, ier """
        words = Words("flies flier cries cried tied costlier libraries")
        self.assertEqual(towords(words.words), [ 'fly', 'fly', 'cry', 'cry', 'tied', 'cost', 'library' ])  
        
    def test_075(self):
        """ Words _stem reduce ves """
        words = Words("leaves wolves")
        self.assertEqual(towords(words.words), [ 'leaf', 'wolf' ])  
        
    def test_076(self):
        """ Words _stem reduce des, nes, ces, ees """
        words = Words("tides rides bees enhances planes includes")
        self.assertEqual(towords(words.words), [ 'tide', 'ride', 'bee', 'enhance', 'plane' ])  
        
    def test_077(self):
        """ Words _stem reduce der """
        words = Words("under rider")
        self.assertEqual(towords(words.words), [ 'ride' ])    
        
    def test_078(self):
        """ Words _stem reduce es, ed mmed oes"""
        words = Words("classes, planted, walked tracked trimmed toes tomatoes potatoes roses", stopwords=True)
        self.assertEqual(towords(words.words), [ 'class', 'plant', 'walk', 'track', 'trim', 'toe', 'tomato', 'potato', 'rose' ])      
        
    def test_079(self):
        """ Words _stem reduce nned """
        words = Words("tanned canned")
        self.assertEqual(towords(words.words), [ 'tan' ])    
        
    def test_080(self):
        """ Words _stem reduce er """
        words = Words("under boxer fighter climber number")
        self.assertEqual(towords(words.words), [ 'boxer', 'fight', 'climb' ])      
        
    def test_081(self):
        """ Words _stem reduce ers """    
        words = Words("boxers fighters climbers numbers")
        self.assertEqual(towords(words.words), [ 'boxer', 'fight', 'climb' ])      
        
    def test_082(self):
        """ Words _stem reduce ly """       
        words = Words("costly particularly")
        self.assertEqual(towords(words.words), [ 'cost', 'particular' ])      
        
    def test_083(self):
        """ Words _stem reduce ss """         
        words = Words("class bass")  
        self.assertEqual(towords(words.words), [ 'class', 'bass' ])        
        
    def test_084(self): 
        """ Words _stem reduce s """           
        words = Words("cars books bikes trains")     
        self.assertEqual(towords(words.words), [ 'car', 'book', 'bike', 'train' ])        
        
    def test_085(self): 
        """ Words _stem Porter list """              
        words = Words("always another at consider during do does exclude for from further fully given give gives having here however if include including likes later member minus nothing never only order other orderings pending perhaps plus possibly rather really")     
        self.assertEqual(towords(words.words), [])          
        
    def test_086(self): 
        """ Words _stem remove est """
        words = Words("greatest least biggest smallest")
        self.assertEqual(towords(words.words), [])     
        
    def test_087(self): 
        """ Words _stem remove zing zed endings """
        words = Words("desensitized anesthetizing; paralyzing")
        self.assertEqual(towords(words.words), [ 'desensitize', 'anesthetize', 'paralyze'])      
        
    def test_088(self): 
        """ Words _stem more word endings """
        words = Words("endings suites features passes")
        self.assertEqual(towords(words.words), ['suite', 'feature', 'pass']) 
        
    def test_089(self):
        """ Words more on Acronyms """
        words = Words("The ABC", stopwords=True)
        self.assertEqual(words.words, [{'word': 'the', 'tag': 4}, {'word': 'abc', 'tag': 14}])
        words = Words("The MEDICAL PLAN", stopwords=True)
        self.assertEqual(words.words, [{'word': 'the', 'tag': 4}, {'word': 'medical', 'tag': 0}, {'word': 'plan', 'tag': 0}])
       
    def test_090(self):
        """ Words _stopwords remove quantifier words """
        words = Words("all any both big least less little more most much short small many few large tall tiny high low long non none often once some several")
        self.assertEqual(towords(words.words), [])
        
    def test_091(self):
        """ Words _stopwords remove quantifier words, quantifier = True """
        words = Words("all any both big least less little more most much short small many few large tall tiny high low long non none often once some several", quantifier=True)
        self.assertEqual(towords(words.words), ['1', 'any', 'both', 'big', 'least', 'less', 'little', 'more', 'most', 'much', 'short',
                                                'small', 'many', 'few', 'large', 'tall', 'tiny', 'high', 'low', 'long', 'non', '0',
                                                'often', '1', 'some', 'several'])      
    def test_092(self):
        """ Words _stopwords quantifier tag """
        words = Words("all any", quantifier=True)
        self.assertEqual(words.words, [{'word': '1', 'tag': 13}, {'word': 'any', 'tag': 13}])

 
    def test_093(self):
        """ Words _stopwords remove preposition words """
        words = Words("to from over under above into up down in out at near across after between besides bottom by inside near on outside to top within behind below beneath far here instead near of there through throughout underneath upon with")
        self.assertEqual(towords(words.words), [])
        
    def test_094(self):
        """ Words _stopwords remove preposition words - preposition = True """
        words = Words("to from over under above into up down in out at near across between besides bottom by inside near on outside to top within behind below beneath far here instead near of there through throughout underneath upon with", preposition=True)
        self.assertEqual(towords(words.words), ['to', 'from', 'over', 'under', 'above', 'into', 'up', 'down', 'in', 'out', 'at', 
                                                'near', 'across', 'between', 'besides', 'bottom', 'by', 'inside', 'near', 
                                                'on', 'outside', 'to', 'top', 'within', 'behind', 'below', 'beneath', 'far', 'here', 'instead',
                                                'near', 'of', 'there', 'through', 'throughout', 'underneath', 'upon', 'with'])
       
    def test_095(self): 
        """ Words _stopwords, conjunction = False """ 
        words = Words("after as although and also because before but consequently either for furthermore hence however if indeed likewise meanwhile neither nor or otherwise since so still therefore though thus unless until while yet whether wherever such than")
        self.assertEqual(words.words, [])
        
    def test_096(self): 
        """ Words _stopwords, conjunction = True """ 
        words = Words("as although and also because before but consequently either for furthermore hence however if indeed likewise meanwhile neither nor or otherwise  since so still  therefore though thus unless until while yet whether wherever such than", conjunction=True)
        self.assertEqual(towords(words.words), ['as', 'although', 'and', 'also', 'because', 'before', 'but', 'consequently', 
                                                'either', 'for', 'furthermore', 'hence', 'however', 'if', 'indeed', 'likewise', 
                                                'meanwhile', 'neither', 'nor', 'or', 'otherwise', 'since', 'so', 'still', 'therefore',
                                                'though', 'thus', 'unless', 'until', 'while', 'yet', 'whether', 'wherever', 'such', 'than'])
           
    def test_097(self): 
        """ Words _stopwords, conjunction tag """ 
        words = Words("also as", conjunction=True)
        self.assertEqual(words.words, [{'word': 'also', 'tag': 3}, {'word': 'as', 'tag': 3}])     
        
    def test_098(self): 
        """ Words _stopwords, article = False """ 
        words = Words("a an the")
        self.assertEqual(words.words, [])  
        
    def test_099(self): 
        """ Words _stopwords, article = True """ 
        words = Words("a an the", article=True)
        self.assertEqual(towords(words.words), ['a', 'an', 'the']) 
        
    def test_100(self): 
        """ Words _stopwords, article tag """ 
        words = Words("an the", article=True)
        self.assertEqual(words.words, [{'word': 'an', 'tag': 4}, {'word': 'the', 'tag': 4}])          
        
    def test_101(self): 
        """ Words _stopwords, demonstrative = False """ 
        words = Words("this that these those")
        self.assertEqual(words.words, [])  
        
    def test_102(self): 
        """ Words _stopwords, demonstrative = True """ 
        words = Words("this that these those", demonstrative=True)
        self.assertEqual(towords(words.words), ['this', 'that', 'these', 'those']) 
        
    def test_103(self): 
        """ Words _stopwords, demonstrative tag """ 
        words = Words("this that", demonstrative=True)
        self.assertEqual(words.words, [{'word': 'this', 'tag': 5}, {'word': 'that', 'tag': 5}])       
        
    def test_104(self): 
        """ Words _stopwords, pronoun = False """ 
        words = Words("anybody anyone anything each everybody everyone he him his her herself himself i it its itself me my myself nobody nothing our ourself oneself she somebody someone something self they them their thee themselves thine thou thyself us we whoever whomever whichever whom you your yourself ye")
        self.assertEqual(words.words, [])  
        
    def test_105(self): 
        """ Words _stopwords, pronoun = True """ 
        words = Words("anybody anyone anything each everybody everyone everything he him his her herself himself i it its itself me my myself nobody nothing our ourself oneself she somebody someone something self they them their thee themselves thine thou thyself us we whoever whomever whichever whom you your yourself ye", pronoun=True)
        self.assertEqual(towords(words.words), ['anybody', 'anyone', 'anything', 'each', 'everybody', 'everyone', 'everything', 'he', 'him', 'his', 'her', 'herself', 
                                                'himself', 'i', 'it', 'its', 'itself', 'me', 'my', 'myself', 'nobody', 'our', 'ourself', 'oneself', 'she', 
                                                'somebody', 'someone', 'something', 'self', 'they', 'them', 'their', 'thee', 'themselves', 'thine', 'thou', 'thyself',
                                                'us', 'we', 'whoever', 'whomever', 'whichever', 'whom', 'you', 'your', 'yourself', 'ye']) 
        
    def test_106(self): 
        """ Words _stopwords, pronoun tag """ 
        words = Words("anybody anyone", pronoun=True)
        self.assertEqual(words.words, [{'word': 'anybody', 'tag': 8}, {'word': 'anyone', 'tag': 8}])                
        
    def test_107(self): 
        """ Words _stopwords, question = False """ 
        words = Words("how why what which where who when")
        self.assertEqual(words.words, [])  
        
    def test_108(self): 
        """ Words _stopwords, question = True """ 
        words = Words("how why what which where who when", question=True)
        self.assertEqual(towords(words.words), ['how', 'why', 'what', 'which', 'where', 'who', 'when']) 
        
    def test_109(self): 
        """ Words _stopwords, question tag """ 
        words = Words("how why", question=True)
        self.assertEqual(words.words, [{'word': 'how', 'tag': 7}, {'word': 'why', 'tag': 7}])                   
       
    def test_110(self): 
        """ Words _stopwords, name = False """ 
        words = Words("mr mrs ms jr sr phd dr")
        self.assertEqual(words.words, [])  
        
    def test_111(self): 
        """ Words _stopwords, name = True """ 
        words = Words("mr mrs ms jr sr phd dr", name=True)
        self.assertEqual(towords(words.words), ['mr', 'mrs', 'ms', 'junior', 'senior', 'phd', 'doctor']) 
        
    def test_112(self): 
        """ Words _stopwords, name tag """ 
        words = Words("mr mrs", name=True)
        self.assertEqual(words.words, [{'word': 'mr', 'tag': 33}, {'word': 'mrs', 'tag': 33}])           
    
    def test_113(self): 
        """ Words - misc word endings """
        words = Words("biggest largest greatest smallest latest taken hidden youngest", quantifier=True)
        self.assertEqual(towords(words.words), ['big', 'large', 'small', 'late', 'hide']) 
 
    def test_114(self): 
        """ Words - remove Porter words """
        words = Words("here however if ilk including interest is it just keep kind knew know known later let like made make making may member might")
        self.assertEqual(towords(words.words), [])
		
    def test_115(self): 
        """ Words - remove Porter words """
        words = Words("mine minus much naught necessary need never new nothing notwithstand nothing now nowhere number off old only onto open opposite")
        self.assertEqual(towords(words.words), [])
			
    def test_116(self): 
        """ Words - remove Porter words """
        words = Words("order other otherwise ought own part past pending per perhaps plus point possible present problem put quite rather really regards regarding room round said same save say see saw seen seem")
        self.assertEqual(towords(words.words), [])	
		
    def test_117(self): 
        """ Words - remove Porter words """
        words = Words("shall should so side somewhere since somewhat state still sure take therefore thing think though thought thus till to today together too took toward turn twain turned unless unlike use various versus")
        self.assertEqual(towords(words.words), [])
		
    def test_118(self): 
        """ Words - remove Porter words """
        words = Words("very via want was way were went whatall whatever whatsoever whereas wherewith wherewithall whether whichever whichsoever while whoever while whoever whole whomsoever whosoever whose will with without work would worth whenever yet yon yonder young")
        self.assertEqual(towords(words.words), [])
		
    def test_119(self): 
        """ Words other name/title words """
        words = Words("VP CEO coo cio cto")
        self.assertEqual(words.words, []) 
        words = Words("vp CEO coo cio CTO", name=True)
        self.assertEqual(words.words, [{'word': 'vice president', 'tag': 33}, {'word': 'chief executive officier', 'tag': 33}, {'word': 'coo', 'tag': 33}, {'word': 'cio', 'tag': 33}, {'word': 'cto', 'tag': 33}]) 					
			
    def test_120(self): 
        """ Words other name/title words """
        words = Words("mayor councilman senator congressman governor president treasurer")
        self.assertEqual(words.words, []) 
        words = Words("mayor councilman senator congressman governor president treasurer", name=True)
        self.assertEqual(towords(words.words), ["mayor", "councilman", "senator", "congressman", "governor", "president", "treasurer"]) 
        words = Words("sergeant colonel lieutenant commander vice")
        self.assertEqual(words.words, []) 
        words = Words("sergeant colonel lieutenant commander vice", name=True)
        self.assertEqual(towords(words.words), ["sergeant", "colonel", "lieutenant", "commander", "vice"]) 

    def test_121(self): 
        """ Words gender() """ 
        words = Words("man men boy guy male dude gentleman gentlemen brother father uncle", gender=True)
        self.assertEqual(words.words, [{'word': 'man', 'tag': 15}, {'word': 'men', 'tag': 15}, {'word': 'boy', 'tag': 15}, {'word': 'guy', 'tag': 15}, {'word': 'male', 'tag': 15}, {'word': 'dude', 'tag': 15}, {'word': 'gentleman', 'tag': 15}, {'word': 'gentlemen', 'tag': 15}, {'word': 'brother', 'tag': 15}, {'word': 'father', 'tag': 15}, {'word': 'uncle', 'tag': 15}])     
        words = Words("woman women girl gal female lady mother sister aunt", gender=True)
        self.assertEqual(words.words, [{'word': 'woman', 'tag': 16}, {'word': 'women', 'tag': 16}, {'word': 'girl', 'tag': 16}, {'word': 'gal', 'tag': 16}, {'word': 'female', 'tag': 16}, {'word': 'lady', 'tag': 16}, {'word': 'mother', 'tag': 16}, {'word': 'sister', 'tag': 16}, {'word': 'aunt', 'tag': 16}])     

       
    def test_122(self): 
        """ Words _gender() bro/sis """ 
        words = Words("bro sis", gender=True)
        self.assertEqual(words.words, [{'word': 'brother', 'tag': 15}, {'word': 'sister', 'tag': 16}])    

    def test_123(self): 
        """ Words - gender = False """
        words = Words("man female", gender=False)
        self.assertEqual(towords(words.words), [])  
        
    def test_124(self): 
        """ Words - gender = True (default) """
        words = Words("man female", gender=True)
        self.assertEqual(towords(words.words), ['man', 'female'])  
        
    def test_125(self):
        """ Words constructor  = gender is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", gender=12)
             		
    def test_126(self): 
        """ Words other gender words """
        words = Words("dad daddy mom mommy sir auntie madam", gender=False)
        self.assertEqual(words.words, []) 
        words = Words("dad daddy mom mommy sir auntie madam", gender=True)
        self.assertEqual(towords(words.words), ["father", "father", "mother", "mother", "sir", "aunt", "madam"])
                    		
    def test_127(self): 
        """ Words other transgender words """
        words = Words("transgender tranny ladyboy shemale sissy crossdresser tg", gender=False)
        self.assertEqual(words.words, []) 
        words = Words("transgender tranny ladyboy shemale sissy crossdresser tg", gender=True)
        self.assertEqual(towords(words.words), ["transgender", "tranny", "ladyboy", "shemale", "sissy", "crossdresser", "tg"])
    		
    def test_128(self):
        """ Words constructor  = stopwords is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", stopwords=12)   
		
    def test_129(self):
        """ Words - stopwords is True """
        words = Words("can could get", stopwords=False)
        self.assertEqual(words.words, []) 
        words = Words("can could get", stopwords=True)
        self.assertEqual(towords(words.words), ["can", "can", "get"])   
		
    def test_130(self):
        """ Words contractions """
        words = Words("can't I'll must've ", stopwords=True)
        self.assertEqual(towords(words.words), ["can", "not", "i", "will", "must", "has" ])    
			
    def test_131(self):
        """ Words constructor  = sentiment is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", sentiment=12)   
			
    def test_132(self): 
        """ Words remove sentiment - positive """
        words = Words("yes good great fair recommend best wonderful excellent fantastic", sentiment=False)
        self.assertEqual(words.words, [])     
			
    def test_133(self): 
        """ Words keep sentiment - positive """
        words = Words("yes good great fair recommend best wonderful  excellent fantastic", sentiment=True)
        self.assertEqual(words.words, [{'word': 'yes', 'tag': 18}, {'word': 'good', 'tag': 18}, {'word': 'great', 'tag': 18}, {'word': 'fair', 'tag': 18}, {'word': 'recommend', 'tag': 18}, {'word': 'best', 'tag': 18}, {'word': 'wonderful', 'tag': 18}, {'word': 'excellent', 'tag': 18}, {'word': 'fantastic', 'tag': 18}])    
			
    def test_134(self): 
        """ Words remove sentiment - negative """
        words = Words("no not nothing lousy bad never", sentiment=False)
        self.assertEqual(words.words, []) 		
		
    def test_135(self): 
        """ Words keep sentiment - negative """
        words = Words("no", sentiment=True)
        self.assertEqual(words.words, [{'word': 'no', 'tag': 19}]) 
        words = Words("not", sentiment=True)
        self.assertEqual(words.words, [{'word': 'not', 'tag': 19}]) 
        words = Words("nothing", sentiment=True)
        self.assertEqual(words.words, [{'word': 'nothing', 'tag': 19}]) 
        words = Words("lousy", sentiment=True)
        self.assertEqual(words.words, [{'word': 'lousy', 'tag': 19}]) 
        words = Words("bad", sentiment=True)
        self.assertEqual(words.words, [{'word': 'bad', 'tag': 19}])
        words = Words("never", sentiment=True)
        self.assertEqual(words.words, [{'word': 'never', 'tag': 19}])

    def test_136(self): 
        """ Words keep sentiment - negate """
        words = Words("not good", sentiment=True)
        self.assertEqual(words.words, [{'word': 'not', 'tag': 19}]) 
        words = Words("not that bad", sentiment=True)
        self.assertEqual(words.words, [{'word': 'not', 'tag': 18}]) 
                		
    def test_137(self): 
        """ Words other sentiment words """
        words = Words("better superb disgust nice worse worst")
        self.assertEqual(words.words, []) 
        words = Words("better superb nice", sentiment=True)
        self.assertEqual(towords(words.words), ["better", "superb", "nice"])
        words = Words("disgust", sentiment=True)
        self.assertEqual(towords(words.words), ["disgust"])
        words = Words("worse", sentiment=True)
        self.assertEqual(towords(words.words), ["worse"])
        words = Words("worst", sentiment=True)
        self.assertEqual(towords(words.words), ["worse"])
               
    def test_138(self):
        """ Words more on sentiment """
        words = Words("it was always breaking", sentiment=True)
        self.assertEqual(words.words, [{'word': 'break', 'tag': 19}])
        words = Words("we loved it", sentiment=True)
        self.assertEqual(words.words, [{'word': 'love', 'tag': 18}])
        words = Words("would not recommend it", sentiment=True)
        self.assertEqual(words.words, [{'word': 'not', 'tag': 19}])
        words = Words("it was perfect", sentiment=True)
        self.assertEqual(words.words, [{'word': 'perfect', 'tag': 18}])
        words = Words("of poor quality", sentiment=True)
        self.assertEqual(words.words, [{'word': 'poor', 'tag': 19}, {'word': 'quality', 'tag': 0}])
        words = Words("just terrible", sentiment=True)
        self.assertEqual(words.words, [{'word': 'terrible', 'tag': 19}])
              
    def test_139(self):
        """ Words more on Acronyms """
        words = Words("The ABC")
        self.assertEqual(words.words, [{'word': 'abc', 'tag': 14}])
        words = Words("The MEDICAL PLAN")
        self.assertEqual(words.words, [{'word': 'medical', 'tag': 0}, {'word': 'plan', 'tag': 0}])
 
    def test_140(self): 
        """ Words other quantifier words """
        words = Words("empty full half")
        self.assertEqual(words.words, []) 
        words = Words("empty full half", quantifier=True)
        self.assertEqual(words.words, [{'word': '0', 'tag': 13}, {'word': '1', 'tag': 13}, {'word': '0.5', 'tag': 13}])
        words = Words("part partial whole")
        self.assertEqual(words.words, []) 
        words = Words("part partial whole", quantifier=True)
        self.assertEqual(words.words, [{'word': 'part', 'tag': 13}, {'word': 'partial', 'tag': 13}, {'word': '1', 'tag': 13}]) 					

    def test_141(self):
        """ Words numbers as words """
        words = Words("zero one two three four five six seven eight nine ten eleven twelve")
        self.assertEqual(towords(words.words), [])
        words = Words("zero one two three four five six seven eight nine ten eleven twelve", number=True)
        self.assertEqual(towords(words.words), ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        words = Words("zeros ones twos threes fours fives sixes sevens eights nines tens elevens twelves", number=True)
        self.assertEqual(towords(words.words), ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        words = Words("one", number=True)
        self.assertEqual(words.words, [{'word': '1', 'tag': 1}])
        
    def test_142(self):
        """ Words large numbers as words """
        words = Words("thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty")
        self.assertEqual(towords(words.words), [])
        words = Words("thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty", number=True)
        self.assertEqual(towords(words.words), ["13", "14", "15", "16", "17", "18", "19", "20", "30"])       
        words = Words("forty fifty sixty seventy eighty ninety hundred thousand million billion trillion infinity")
        self.assertEqual(towords(words.words), [])      
        words = Words("forty fifty sixty seventy eighty ninety one hundred thousand one million billion one trillion infinity", number=True)
        self.assertEqual(towords(words.words), ["40", "50", "60", "70", "80", "90", "100", "1000", "1000000", "1000000000", "1000000000000", "infinity"])

    def test_143(self):
        """ Words numbers as words with th """
        words = Words("tenth fifth hundredth twentieth")
        self.assertEqual(towords(words.words), [])
        words = Words("tenth fifth hundredth twentieth", number=True)
        self.assertEqual(towords(words.words), ["10", "5", "100", "20"]) 

    def test_144(self):
        """ Words quantifier quarter, half, whole """
        words = Words("quarter half whole empty all full", quantifier=True)
        self.assertEqual(towords(words.words), ["0.25", "0.5", "1", "0", "1", "1"])
       
    def test_145(self):
        """ Words _split() - remove punctuation """
        words = Words("period. comma, semi-colon; colon: exclamation! question?")
        self.assertEqual(towords(words.words), ['period', 'comma', 'semi', 'colon', 'colon', 'exclamation', 'question'])
    
    def test_146(self):
        """ Words _split() - remove symbols """
        words = Words("zoo @# $% ^&*() {} [] <> hot")
        self.assertEqual(towords(words.words), ['zoo', 'hot'])

    def test_147(self):
        """ Words _stopwords numbers 0 thru 9 """
        words = Words("0 1 2 3 4 5 6 7 8 9")
        self.assertEqual(towords(words.words), [])
        words = Words("0 1 2 3 4 5 6 7 8 9", number=True)
        self.assertEqual(towords(words.words), ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        
    def test_148(self):
        """ Words _stopwords numbers > 9 """
        words = Words("10 11 22 33 445")
        self.assertEqual(words.words, [])
        words = Words("10 11 22 33 445", number=True)
        self.assertEqual(towords(words.words), ['10', '11', '22', '33', '445'])
        words = Words("15", number=True)
        self.assertEqual(words.words, [{'word': '15', 'tag': 1}])
        
    def test_149(self):
        """ Words _stopwords numbers > 9, number = True """
        words = Words("10 11 22 33 445", number=True)
        self.assertEqual(towords(words.words), ['10', '11', '22', '33', '445'])
               
    def test_150(self):
        """ Words _stopwords remove non-decimal periods, number = True """
        words = Words("one, two.", number=True)
        self.assertEqual(towords(words.words), ['1', '2'])
                       
    def test_151(self): 
        """ Words _stopwords, integer number tag """             
        words = Words("0 1 23", number=True)        
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '0' }, { 'tag': 1, 'word': '1' }, { 'tag': 1, 'word': '23' } ])        
       
    def test_152(self): 
        """ Words _stopwords, unsigned integer number tag """                
        words = Words("1 23 16", number=True)           
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '1' }, { 'tag': 1, 'word': '23' }, { 'tag': 1, 'word': '16' } ])          
      
    def test_153(self):
        """ Words _stopwords keep negative numbers, number = True """
        words = Words("This is -3", number=True)
        self.assertEqual(towords(words.words), ['-3'])
        words = Words("1-3 -4", number=True)
        self.assertEqual(towords(words.words), ['1', '3', '-4'])
               
    def test_154(self): 
        """ Words _stopwords, signed integer number tag """              
        words = Words("-1 -23 +16", number=True)           
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '-1' }, { 'tag': 1, 'word': '-23' }, { 'tag': 1, 'word': '16' } ])         
       
    def test_155(self):
        """ Words _stopwords decimal and negative numbers, number = True """
        words = Words("1.2 .3 0.03", number=True)
        self.assertEqual(towords(words.words), ['1.2', '0.3', '0.03'])
        
    def test_156(self):
        """ Words _stopwords remove comma """
        words = Words("1,000 8,012.6")
        self.assertEqual(towords(words.words), [])
        
    def test_157(self):
        """ Words _stopwords thousands unit (default) """
        words = Words("1,000 8,012.6", number=True)
        self.assertEqual(towords(words.words), ['1000', '8012.6'])
        
    def test_158(self):
        """ Words _stopwords thousands unit (standard) """
        Words.THOUSANDS = ','
        words = Words("1,000 8,012.6", number=True)
        self.assertEqual(towords(words.words), ['1000', '8012.6'])
        
    def test_159(self):
        """ Words _stopwords thousands unit (eu) """
        Words.THOUSANDS = '.'
        Words.DECIMAL   = ','
        words = Words("1.000 8.012,6", number=True)
        self.assertEqual(towords(words.words), ['1000', '8012.6'])
        
    def test_160(self):
        """ Words _stopwords thousands unit (eu) """
        Words.THOUSANDS = '.'
        Words.DECIMAL   = ','
        words = Words("1.000 8.012,6", number=True)
        self.assertEqual(towords(words.words), ['1000', '8012.6'])
        
    def test_161(self):
        """ Words _stopwords exponents """
        Words.THOUSANDS = ','
        Words.DECIMAL   = '.'
        words = Words("2e9 2.3e-7")
        self.assertEqual(towords(words.words), [])
        words = Words("2e9 2.3e-7", number=True)
        self.assertEqual(towords(words.words), ['2e9', '2.3e-7'])
        
    def test_162(self):
        """ Words _stopwords exponents - number = True"""
        words = Words("2e9 2.3e-7", number=True)
        self.assertEqual(towords(words.words), ['2e9', '2.3e-7'])
 
    def test_163(self): 
        """ Words _stopwords, floating point number tag """              
        words = Words(".1, 0.1 23.6", number=True)           
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '0.1' }, { 'tag': 1, 'word': '0.1' }, { 'tag': 1, 'word': '23.6' } ])                          
           
    def test_164(self): 
        """ Words _stopwords, negative floating point number tag """              
        words = Words("-.1, -0.1 -23.6", number=True)           
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '-0.1' }, { 'tag': 1, 'word': '-0.1' }, { 'tag': 1, 'word': '-23.6' } ])                          
        
    def test_165(self): 
        """ Words _stopwords, exponent number tag """              
        words = Words("1e1 2.3e4 6e-4", number=True)           
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '1e1' }, { 'tag': 1, 'word': '2.3e4' }, { 'tag': 1, 'word': '6e-4' } ])                          
        
    def test_166(self): 
        """ Words _stopwords, hex number tag """              
        words = Words("0x00 0x02 0x10", number=True)             
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '0' }, { 'tag': 1, 'word': '2' }, { 'tag': 1, 'word': '16' } ])                          

    def test_167(self):
        """ Words  number and date are true """
        words = Words("0 1 1.2 .2 -6 -6.2 1,661 2e7 2e-6 2e.5 0x12 0xFF")
        self.assertEqual(towords(words.words), [])
        words = Words("0 1 1.2 .2 -6 -6.2 1,661 2e7 2e-6 2e.5 0x12 0xFF", date=True, number=True)
        self.assertEqual(towords(words.words), ["0", "1", "1.2", "0.2", "-6", "-6.2", "1661", "2e7", "2e-6", "2e.5", "18", "255"])
                
    def test_168(self):
        """ Words ordered numbers """
        words = Words("1st 2nd 3rd 4th")
        self.assertEqual(towords(words.words), [])
        words = Words("1st 2nd 3rd 4th", number=True)
        self.assertEqual(towords(words.words), ["1", "2", "3", "4"])
            
    def test_169(self): 
        """ Words _stopwords, hex number with caps """              
        words = Words("0X00 0XFF 0xff", number=True)             
        self.assertEqual(words.words, [ { 'tag': 1, 'word': '0' }, { 'tag': 1, 'word': '255' }, { 'tag': 1, 'word': '255' } ])                          
     
    def test_170(self): 
        """ Words _stopwords, single cap letters """              
        words = Words("A B C. D", article=True)   
        self.assertEqual(towords(words.words), ["a", "b", "c", "d"])
        
    def test_171(self):
        """ Words numbers - fractions """
        words = Words("one 1/4 zoo 1/2", number=True)
        self.assertEqual(towords(words.words), ["1", "0.25", "zoo", "0.5"])
         
    def test_172(self):
        """ Words _stopwords January day, year: date = False """
        words = Words("one January 6, 2016", date=False)
        self.assertEqual(towords(words.words), [] )  
    
    def test_173(self):
        """ Words _stopwords January day, year: date = True """
        words = Words("one January 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-06'] )    
    
    def test_174(self):
        """ Words _stopwords Jan. day, year: date = True """
        words = Words("one Jan. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-06'] )    
    
    def test_175(self):
        """ Words _stopwords Jan day, year: date = True """
        words = Words("one Jan 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-06'] )   
    
    def test_176(self):
        """ Words _stopwords February day, year: date = True """
        words = Words("one February 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-02-06'] )       
    
    def test_177(self):
        """ Words _stopwords February day, year: date = True """
        words = Words("March 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-03-04'] )   
        words = Words("April 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-04-04'] ) 
        words = Words("May 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-05-04'] )  
        words = Words("June 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-06-04'] )     
        words = Words("July 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-07-04'] )   
        words = Words("August 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-08-04'] )     
        words = Words("September 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-09-04'] )     
        words = Words("October 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-10-04'] )       
        words = Words("November 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-11-04'] )      
        words = Words("December 4 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-12-04'] ) 
    
    def test_178(self):
        """ Words _stopwords Feb. day, year: date = True """
        words = Words("one Feb. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-02-06'] )    
    
    def test_179(self):
        """ Words _stopwords Feb day, year: date = True """
        words = Words("one Feb 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-02-06'] )   
    
    def test_180(self):
        """ Words _stopwords March day, year: date = True """
        words = Words("one March 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-03-06'] )    
    
    def test_181(self):
        """ Words _stopwords Mar. day, year: date = True """
        words = Words("one Mar. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-03-06'] )    
    
    def test_182(self):
        """ Words _stopwords Mar day, year: date = True """
        words = Words("one Mar 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-03-06'] )  
    
    def test_183(self):
        """ Words _stopwords April day, year: date = True """
        words = Words("one April 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-04-06'] )    
    
    def test_184(self):
        """ Words _stopwords Apr. day, year: date = True """
        words = Words("one Apr. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-04-06'] )    
    
    def test_185(self):
        """ Words _stopwords Apr day, year: date = True """
        words = Words("one Apr 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-04-06'] )   
    
    def test_186(self):
        """ Words _stopwords May day, year: date = True """
        words = Words("one May 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-05-06'] )   
    
    def test_187(self):
        """ Words _stopwords June day, year: date = True """
        words = Words("one June 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-06-06'] )    
    
    def test_188(self):
        """ Words _stopwords Jun. day, year: date = True """
        words = Words("one Jun. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-06-06'] )    
    
    def test_189(self):
        """ Words _stopwords Jun day, year: date = True """
        words = Words("one Jun 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-06-06'] )     
    
    def test_190(self):
        """ Words _stopwords July day, year: date = True """
        words = Words("one July 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-07-06'] )    
    
    def test_191(self):
        """ Words _stopwords Jul. day, year: date = True """
        words = Words("one Jul. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-07-06'] )    
    
    def test_192(self):
        """ Words _stopwords Jul day, year: date = True """
        words = Words("one Jul 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-07-06'] )     
    
    def test_193(self):
        """ Words _stopwords August day, year: date = True """
        words = Words("one August 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-08-06'] )    
    
    def test_194(self):
        """ Words _stopwords Aug. day, year: date = True """
        words = Words("one Aug. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-08-06'] )    
    
    def test_195(self):
        """ Words _stopwords Aug day, year: date = True """
        words = Words("one Aug 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-08-06'] )     
        
    def test_196(self):
        """ Words _stopwords September day, year: date = True """
        words = Words("one September 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-09-06'] )    
    
    def test_197(self):
        """ Words _stopwords Sep. day, year: date = True """
        words = Words("one Sep. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-09-06'] )    
    
    def test_198(self):
        """ Words _stopwords Sep day, year: date = True """
        words = Words("one Sep 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-09-06'] )       
    
    def test_199(self):
        """ Words _stopwords October day, year: date = True """
        words = Words("one October 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['2016-10-06'] )    
    
    def test_200(self):
        """ Words _stopwords Oct. day, year: date = True """
        words = Words("zoo Oct. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-10-06'] )    
    
    def test_201(self):
        """ Words _stopwords Oct day, year: date = True """
        words = Words("zoo Oct 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-10-06'] )         
    
    def test_202(self):
        """ Words _stopwords November day, year: date = True """
        words = Words("zoo November 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-11-06'] )    
    
    def test_203(self):
        """ Words _stopwords Nov. day, year: date = True """
        words = Words("zoo Nov. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-11-06'] )    
    
    def test_204(self):
        """ Words _stopwords Nov day, year: date = True """
        words = Words("zoo Nov 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-11-06'] )        
    
    def test_205(self):
        """ Words _stopwords December day, year: date = True """
        words = Words("zoo December 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-12-06'] )    
    
    def test_206(self):
        """ Words _stopwords Dec. day, year: date = True """
        words = Words("zoo Dec. 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-12-06'] )    
    
    def test_207(self):
        """ Words _stopwords Dec day, year: date = True """
        words = Words("zoo Dec 6, 2016", date=True)
        self.assertEqual(towords(words.words), ['zoo', '2016-12-06'] )

    def test_208(self):
        """ Words _stopwords mm-dd-yyyy, date = False """
        words = Words("one 01-02-2016")
        self.assertEqual(towords(words.words), [] )     
        
    def test_209(self):
        """ Words _stopwords mm-dd-yyyy, date = True """
        words = Words("one 01-02-2016", date=True)
        self.assertEqual(towords(words.words), [ '2016-01-02'] )     
    
    def test_210(self):
        """ Words _stopwords m-d-yyyy, date = True """
        words = Words("one 1-2-2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-02'] )     
    
    def test_211(self):
        """ Words _stopwords mm-dd-yy, date = True """
        words = Words("one 01-02-16", date=True)
        self.assertEqual(towords(words.words), ['2016-01-02'] )       
    
    def test_212(self):
        """ Words _stopwords ISO, date = True """
        words = Words("one 2016-02-01", date=True)
        self.assertEqual(towords(words.words), ['2016-02-01'] )     
        words = Words("one 1997-02-06", date=True)
        self.assertEqual(towords(words.words), ['1997-02-06'] )     
 
    def test_213(self):
        """ Words _stopwords mm/dd/yyyy, date = False """
        words = Words("one 01/02/2016")
        self.assertEqual(towords(words.words), [] )    
    
    def test_214(self):
        """ Words _stopwords mm/dd/yyyy, date = True """
        words = Words("one 01/02/2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-02'] )   
 
    
    def test_215(self):
        """ Words _stopwords mm/dd/yyyy, date = False """
        words = Words("one 01/02/2016")
        self.assertEqual(towords(words.words), [] )    
    
    def test_216(self):
        """ Words _stopwords mm/dd/yyyy, date = True """
        words = Words("one 01/02/2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-02'] )    
    
    def test_217(self):
        """ Words _stopwords m/d/yyyy, date = True """
        words = Words("one 1/2/2016", date=True)
        self.assertEqual(towords(words.words), ['2016-01-02'] )     
    
    def test_218(self):
        """ Words _stopwords m/d/yy, date = True """
        words = Words("one 1/2/16", date=True)
        self.assertEqual(towords(words.words), ['2016-01-02'] ) 
    
    def test_219(self):
        """ Words _stopwords date mm-dd-yyyy not valid """
        words = Words("one 13-02-2016", date=True)
        self.assertEqual(towords(words.words), [] )
        words = Words("one 01-32-2016", date=True, number=True)
        self.assertEqual(towords(words.words), ['1', '01', '32', '2016'] )
        words = Words("2016-13-01", date=True)
        self.assertEqual(words.words, [] )
        words = Words("2016-02-00", date=True)
        self.assertEqual(words.words, [] )
        words = Words("13/02/2016", date=True)
        self.assertEqual(words.words, [] )
        words = Words("01/32/2016", date=True)
        self.assertEqual(words.words, [] )
    
    def test_220(self):
        """ Words _stopwords mm-, date = True """
        words = Words("one 01-", date=True)
        self.assertEqual(towords(words.words), [] )
    
    def test_221(self):
        """ Words _stopwords mm/, date = True """
        words = Words("one 01/", date=True)
        self.assertEqual(towords(words.words), [] )       
    
    def test_222(self):
        """ Words _stopwords mm-, date = True """
        words = Words("one 01-AB", date=True)
        self.assertEqual(towords(words.words), ['ab'] )
    
    def test_223(self):
        """ Words _stopwords mm/, date = True """
        words = Words("one 01/AB", date=True)
        self.assertEqual(towords(words.words), ['ab'] )    
    
    def test_224(self):
        """ Words _stopwords mm-dd, date = True """
        words = Words("one 01-06", date=True)
        self.assertEqual(towords(words.words), [] )     
    
    def test_225(self):
        """ Words _stopwords mm/dd, date = True """
        words = Words("one 01/06", date=True)
        self.assertEqual(towords(words.words), [] ) 
        
    def test_226(self): 
        """ Words _stopwords, numeric date, date tag """                
        words = Words("01/02/2018", date=True)
        self.assertEqual(words.words, [ { 'tag': 2, 'word': '2018-01-02' } ] )   

    def test_227(self):
        """ Words constructor  = dob is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", dob=12)   
        
    def test_228(self):
        """ Words date of birth = False """
        words = Words("DOB: 01/02/2016 and date of birth is 01/02/2016")
        self.assertEqual(towords(words.words), ["dob", "date", "birth"])
        words = Words("DOB: 01/02/2016 and date of birth is 01/02/2016", date=True)
        self.assertEqual(towords(words.words), ["dob", "date", "birth"])
        words = Words("DOB: 01/02/2016 and date of birth is 01/02/2016", dob=True)
        self.assertEqual(words.words, [{'word': '2016-01-02', 'tag': 20}, {'word': 'date', 'tag': 0}, {'word': '2016-01-02', 'tag': 20}])  
        
    def test_229(self):
        """ Words SSN : SSN"""
        words = Words("SSN: 511-81-1270")
        self.assertEqual(towords(words.words), [])
        words = Words("SSN: 511-81-1270", number=True)
        self.assertEqual(towords(words.words), [])
        words = Words("SSN: 511-81-1270", ssn=True)
        self.assertEqual(words.words, [{'word': '511811270', 'tag': 9}]) 
        words = Words("SSN: 511811270")
        self.assertEqual(towords(words.words), [])
        words = Words("SSN: 511811270", number=True)
        self.assertEqual(towords(words.words), [])
        words = Words("SSN: 511811270", ssn=True)
        self.assertEqual(words.words, [{'word': '511811270', 'tag': 9}]) 
        words = Words("SSN: 511 81 1270")
        self.assertEqual(towords(words.words), [])
        words = Words("SSN: 511 81 1270", number=True)
        self.assertEqual(towords(words.words), [])
        words = Words("SSN: 511 81 1270", ssn=True)
        self.assertEqual(words.words, [{'word': '511811270', 'tag': 9}]) 
        
    def test_230(self):
        """ Words SSN = Social Security Nuumber"""
        words = Words("Social Security Number 249 45 6789")
        self.assertEqual(towords(words.words), [])
        words = Words("Social Security Number 249 45 6789", number=True)
        self.assertEqual(towords(words.words), [])
        words = Words("Social Security Number 249 45 6789", ssn=True)
        self.assertEqual(words.words, [{'word': '249456789', 'tag': 9}])
        words = Words("Soc Sec No 249 45 6789")
        self.assertEqual(towords(words.words), [])
        words = Words("Soc Sec No 249 45 6789", number=True)
        self.assertEqual(towords(words.words), [])
        words = Words("Soc Sec No 249 45 6789", ssn=True)
        self.assertEqual(words.words, [{'word': '249456789', 'tag': 9}])
        words = Words("Soc. Sec. No. 249 45 6789")
        self.assertEqual(towords(words.words), [])
        words = Words("Soc. Sec. No. 249 45 6789", number=True)
        self.assertEqual(towords(words.words), [])
        words = Words("Soc. Sec. No. 249 45 6789", ssn=True)
        self.assertEqual(words.words, [{'word': '249456789', 'tag': 9}])
        
    def test_231(self):
        """ Words SSN = Social Security Nuumber #"""
        words = Words("SSN# 249 45 6789")
        self.assertEqual(towords(words.words), [])
        words = Words("SSN# 249 45 6789", ssn=True)
        self.assertEqual(words.words, [{'word': '249456789', 'tag': 9}]) 
        words = Words("Social Security Number # 249 45 6789")
        self.assertEqual(towords(words.words), []) 
        words = Words("Social Security Number # 249 45 6789", ssn=True)
        self.assertEqual(words.words, [{'word': '249456789', 'tag': 9}]) 
        words = Words("Social Security Number #: 249 45 6789")
        self.assertEqual(towords(words.words), []) 
        words = Words("Social Security Number #: 249 45 6789", ssn=True)
        self.assertEqual(words.words, [{'word': '249456789', 'tag': 9}])  

    def test_232(self):
        """ Words - Telephone NNNNNNNNNN """
        words = Words("Phone: 3601231234")
        self.assertEqual(towords(words.words), [])
        words = Words("Phone: 3601231234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 10}])
        words = Words("Work# 3601231234")
        self.assertEqual(towords(words.words), [])
        words = Words("Work# 3601231234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 40}])

    def test_233(self):
        """ Words - Telephone NNN[-]NNNNNNN """
        words = Words("Office #: 360 1231234")
        self.assertEqual(towords(words.words), [])
        words = Words("Phone: 360 1231234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 10}])
        words = Words("Office #: 360-1231234")
        self.assertEqual(towords(words.words), [])
        words = Words("Phone: 360-1231234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 10}])

    def test_234(self):
        """ Words - Telephone NNN[-]NNNN[-]NNNN """
        words = Words("Office #: 360-123-1234")
        self.assertEqual(towords(words.words), [])
        words = Words("Phone: 360-123-1234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 10}])
        words = Words("Phone: 360-123-1234", telephone=True, number=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 10}])
        words = Words("Mobile Number 360 123 1234")
        self.assertEqual(towords(words.words), [])
        words = Words("Mobile Number 360 123 1234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 41}])
        words = Words("Mobile Number 360 123 1234", telephone=True, number=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 41}])

    def test_235(self):
        """ Words - Telephone (NNN) NNN[-]NNNN """
        words = Words("Mobile Number (360) 123 1234")
        self.assertEqual(towords(words.words), [])
        words = Words("Mobile Number (360) 123 1234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 41}])
        words = Words("Mobile Number (360) 123-1234")
        self.assertEqual(towords(words.words), [])
        words = Words("Mobile Number (360) 123-1234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 41}])
        
    def test_236(self):
        """ Words - Single Letter abbreviations """
        words = Words("S. N.")
        self.assertEqual(words.words, [{'word': 's', 'tag': 22}, {'word': 'n', 'tag': 22}])
        words = Words("s. n.")
        self.assertEqual(words.words, [{'word': 's', 'tag': 22}, {'word': 'n', 'tag': 22}]) 
        
    def test_237(self):
        """ Words - Multi-Word abbreviations """
        words = Words("N.E.")
        self.assertEqual(words.words, [{'word': 'n', 'tag': 22}, {'word': 'e', 'tag': 22}])
        words = Words("n.e.")
        self.assertEqual(words.words, [{'word': 'n', 'tag': 22}, {'word': 'e', 'tag': 22}])   
        
    def test_238(self):
        """ Words - Multi-Letter abbreviations """
        words = Words("NE.")
        self.assertEqual(words.words, [{'word': 'ne', 'tag': 14}])
        words = Words("ne.")
        self.assertEqual(words.words, [{'word': 'ne', 'tag': 0}])
                
    def test_239(self):
        """ Words - Spanish punctuation """
        words = Words("¿¡", punct=True)
        self.assertEqual(words.words, [{'word': '¿', 'tag': 23}, {'word': '¡', 'tag': 23}])
                
    def test_240(self):
        """ Words - More quantifiers """
        words = Words("middle last", quantifier=True)
        self.assertEqual(words.words, [{'word': '0.5', 'tag': 13}, {'word': 'last', 'tag': 13}])  

    def test_241(self):
        """ Words constructor  = unit is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", unit=12)    
            
    def test_242(self):
        """ Words - US Standard Units """
        words = Words("ft ft. feet foot", unit=True)
        self.assertEqual(words.words, [{'word': 'foot', 'tag': 25}, {'word': 'foot', 'tag': 25}, {'word': 'foot', 'tag': 25}, {'word': 'foot', 'tag': 25}]) 
        words = Words("yd yd. yard yards yds", unit=True)
        self.assertEqual(words.words, [{'word': 'yard', 'tag': 25}, {'word': 'yard', 'tag': 25}, {'word': 'yard', 'tag': 25}, {'word': 'yard', 'tag': 25}, {'word': 'yard', 'tag': 25}])    
       
    def test_243(self):
        """ Words unit as number multiplier """
        words = Words("the price is six hundred", number=True)
        self.assertEqual(words.words, [{'word': 'price', 'tag': 0}, {'word': '600', 'tag': 1}])
        words = Words("the price is twenty thousand", number=True)
        self.assertEqual(words.words, [{'word': 'price', 'tag': 0}, {'word': '20000', 'tag': 1}])
        words = Words("the 2 million homes", number=True)
        self.assertEqual(words.words, [{'word': '2000000', 'tag': 1}, {'word': 'home', 'tag': 0}])
        words = Words("the 3.5 million homes", number=True)
        self.assertEqual(words.words, [{'word': '3500000', 'tag': 1}, {'word': 'home', 'tag': 0}])
        words = Words("the 20 billion rats", number=True)
        self.assertEqual(words.words, [{'word': '20000000000', 'tag': 1}, {'word': 'rat', 'tag': 0}])
       
    def test_244(self):
        """ Words units of measure """
        words = Words("10 in, 20 in.", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'inch', 'tag': 25}, {'word': '20', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("inch inches", stopwords=True)
        self.assertEqual(words.words, [{'word': 'inch', 'tag': 25}, {'word': 'inch', 'tag': 25}])
        words = Words("mile oz ounces", stopwords=True)
        self.assertEqual(words.words, [{'word': 'mile', 'tag': 25}, {'word': 'ounce', 'tag': 25}, {'word': 'ounce', 'tag': 25}])
        words = Words("pts pints pt", stopwords=True)
        self.assertEqual(words.words, [{'word': 'pint', 'tag': 25}, {'word': 'pint', 'tag': 25}, {'word': 'pint', 'tag': 25}])
        words = Words("qts quarts qt", stopwords=True)
        self.assertEqual(words.words, [{'word': 'quart', 'tag': 25}, {'word': 'quart', 'tag': 25}, {'word': 'quart', 'tag': 25}])
        words = Words("lbs pound lb", stopwords=True)
        self.assertEqual(words.words, [{'word': 'pound', 'tag': 25}, {'word': 'pound', 'tag': 25}, {'word': 'pound', 'tag': 25}])
        words = Words("ton tons", stopwords=True)
        self.assertEqual(words.words, [{'word': 'ton', 'tag': 25}, {'word': 'ton', 'tag': 25}])
     
    def test_245(self):
        """ Words units of measure """
        words = Words("sec secs", stopwords=True)
        self.assertEqual(words.words, [{'word': 'second', 'tag': 25}, {'word': 'second', 'tag': 25}])
        words = Words("min minutes", stopwords=True)
        self.assertEqual(words.words, [{'word': 'minute', 'tag': 25}, {'word': 'minute', 'tag': 25}])
        words = Words("hr hrs hours", stopwords=True)
        self.assertEqual(words.words, [{'word': 'hour', 'tag': 25}, {'word': 'hour', 'tag': 25}, {'word': 'hour', 'tag': 25}])
        words = Words("day days", stopwords=True)
        self.assertEqual(words.words, [{'word': 'day', 'tag': 25}, {'word': 'day', 'tag': 25}])
        words = Words("yr yrs years", stopwords=True)
        self.assertEqual(words.words, [{'word': 'year', 'tag': 25}, {'word': 'year', 'tag': 25}, {'word': 'year', 'tag': 25}])
             
    def test_246(self):
        """ Words more units of measure """
        words = Words("10 seconds", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'second', 'tag': 25}])
        words = Words("4 ins", stopwords=True)
        self.assertEqual(words.words, [{'word': '4', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        
    def test_247(self):   
        """ Words - metric units of measure """
        words = Words("mm millimeter cm centimeter", stopwords=True)
        self.assertEqual(words.words, [{'word': 'millimeter', 'tag': 25}, {'word': 'millimeter', 'tag': 25}, {'word': 'centimeter', 'tag': 25}, {'word': 'centimeter', 'tag': 25}])
        words = Words("km kilometer ml milliliter", stopwords=True)
        self.assertEqual(words.words, [{'word': 'kilometer', 'tag': 25}, {'word': 'kilometer', 'tag': 25}, {'word': 'milliliter', 'tag': 25}, {'word': 'milliliter', 'tag': 25}])
        words = Words("kg kilogram mg milligram", stopwords=True)
        self.assertEqual(words.words, [{'word': 'kilogram', 'tag': 25}, {'word': 'kilogram', 'tag': 25}, {'word': 'milligram', 'tag': 25}, {'word': 'milligram', 'tag': 25}])
        words = Words("kw kilowatt", stopwords=True)
        self.assertEqual(words.words, [{'word': 'kilowatt', 'tag': 25}, {'word': 'kilowatt', 'tag': 25}])
        words = Words("1 m meter", stopwords=True)
        self.assertEqual(words.words, [{'word': '1', 'tag': 1}, {'word': 'meter', 'tag': 25}, {'word': 'meter', 'tag': 25}])
        words = Words("2 g gram", stopwords=True)
        self.assertEqual(words.words, [{'word': '2', 'tag': 1}, {'word': 'gram', 'tag': 25}, {'word': 'gram', 'tag': 25}])
        words = Words("sqm ha hectera m2", stopwords=True)
        self.assertEqual(words.words, [{'word': 'square meter', 'tag': 25}, {'word': 'hectera', 'tag': 25}, {'word': 'hectera', 'tag': 25}, {'word': 'square meter', 'tag': 25}])
       
    def test_248(self):   
        """ Words - more US units of measure """
        words = Words("10 gals", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'gallon', 'tag': 25}])
        words = Words("mi sqft sf ft2", stopwords=True)
        self.assertEqual(words.words, [{'word': 'mile', 'tag': 25}, {'word': 'square foot', 'tag': 25}, {'word': 'square foot', 'tag': 25}, {'word': 'square foot', 'tag': 25}])
        words = Words("mins", stopwords=True)
        self.assertEqual(words.words, [{'word': 'minute', 'tag': 25}])
        words = Words("ac acres", stopwords=True)
        self.assertEqual(words.words, [{'word': 'acre', 'tag': 25}, {'word': 'acre', 'tag': 25}])
        words = Words("mph sqmi", stopwords=True)
        self.assertEqual(words.words, [{'word': 'mile per hour', 'tag': 25}, {'word': 'square mile', 'tag': 25}])
        words = Words("10 sq ft 20 sq mi", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'square foot', 'tag': 25}, {'word': '20', 'tag': 1}, {'word': 'square mile', 'tag': 25}])
        words = Words("10 kilos", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'kilogram', 'tag': 25}])
        
    def test_249(self):   
        """ Words - min(imum) vs min(ute) """
        words = Words("the min time", stopwords=True)
        self.assertEqual(words.words, [{'word': 'the', 'tag': 4}, {'word': 'minimum', 'tag': 22}, {'word': 'time', 'tag': 0}])
            
    def test_250(self):   
        """ Words - metre version of metric """
        words = Words("10 l liter litre", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'liter', 'tag': 25}, {'word': 'liter', 'tag': 25},{'word': 'liter', 'tag': 25}])
        words = Words("metre millimetre centimetre kilometre", stopwords=True)
        self.assertEqual(words.words, [{'word': 'meter', 'tag': 25}, {'word': 'millimeter', 'tag': 25}, {'word': 'centimeter', 'tag': 25}, {'word': 'kilometer', 'tag': 25}])
                   
    def test_251(self):  
        """ Words - single letters when not abbreviated units of measuments """
        words = Words("g l", stopwords=True)
        self.assertEqual(words.words, [{'word': 'g', 'tag': 0}, {'word': 'l', 'tag': 0}])
                  
    def test_252(self):  
        """ Words Constructor - standard / metric is not a bool """
        with pytest.raises(TypeError):
            words = Words("standard", unit=12)    
        with pytest.raises(TypeError):
            words = Words("metric", unit=12)      
            
    def test_253(self):  
        """ Words - Metric to Standard Conversion """
        words = Words("10 mm", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '0.39370099999999997', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("10 cm", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '3.9370100000000003', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("10 m", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '32.8084', 'tag': 1}, {'word': 'feet', 'tag': 25}])
        words = Words("10 km", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '6.21371', 'tag': 1}, {'word': 'mile', 'tag': 25}])
        words = Words("10 ml", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '0.33814', 'tag': 1}, {'word': 'ounce', 'tag': 25}])
        words = Words("10 l", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '2.6417200000000003', 'tag': 1}, {'word': 'gallon', 'tag': 25}])
        words = Words("10 mg", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '0.00035274000000000004', 'tag': 1}, {'word': 'ounce', 'tag': 25}])
        words = Words("10 g", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '0.35274', 'tag': 1}, {'word': 'ounce', 'tag': 25}])
        words = Words("10 kg", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '22.0462', 'tag': 1}, {'word': 'pound', 'tag': 25}])
        words = Words("10 sqm", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '107.639', 'tag': 1}, {'word': 'square foot', 'tag': 25}])
        words = Words("10 kmh", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '6.21371', 'tag': 1}, {'word': 'mile per hour', 'tag': 25}])
        words = Words("10 ha", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '24.7105', 'tag': 1}, {'word': 'acre', 'tag': 25}])

    def test_254(self):  
        """ Words - Standard to Metric Conversion """
        words = Words("10 in", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '25.4', 'tag': 1}, {'word': 'centimeter', 'tag': 25}])
        words = Words("10 feet", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '3.048', 'tag': 1}, {'word': 'meter', 'tag': 25}])
        words = Words("10 yards", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '9.144', 'tag': 1}, {'word': 'meter', 'tag': 25}])
        words = Words("10 mile", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '16.0934', 'tag': 1}, {'word': 'kilometer', 'tag': 25}])
        words = Words("10 oz", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '0.29573499999999997', 'tag': 1}, {'word': 'liter', 'tag': 25}])
        words = Words("10 pints", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '4.7317599999999995', 'tag': 1}, {'word': 'liter', 'tag': 25}])
        words = Words("10 gallons", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '37.8541', 'tag': 1}, {'word': 'liter', 'tag': 25}])
        words = Words("10 pounds", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '4.53592', 'tag': 1}, {'word': 'kilogram', 'tag': 25}])
        words = Words("10 tons", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '9.07185', 'tag': 1}, {'word': 'tonne', 'tag': 25}])
        words = Words("10 sqft", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '0.92903', 'tag': 1}, {'word': 'square meter', 'tag': 25}])
        words = Words("10 ac", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '4.04686', 'tag': 1}, {'word': 'hectera', 'tag': 25}])
        words = Words("10 mph", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '16.0934', 'tag': 1}, {'word': 'kilometer per hour', 'tag': 25}])
        
    def test_255(self):  
        """ Words - more measurements """
        words = Words("10 tonnes", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'tonne', 'tag': 25}])
        words = Words("10 tonnes", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '11.0231', 'tag': 1}, {'word': 'ton', 'tag': 25}])
        words = Words("10 cups", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'cup', 'tag': 25}])
        words = Words("10 cups", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '2.3658799999999998', 'tag': 1}, {'word': 'liter', 'tag': 25}])
        words = Words("tsp teaspoons", stopwords=True)
        self.assertEqual(words.words, [{'word': 'teaspoon', 'tag': 25}, {'word': 'teaspoon', 'tag': 25}])
        words = Words("kn knots", stopwords=True)
        self.assertEqual(words.words, [{'word': 'knot', 'tag': 25}, {'word': 'knot', 'tag': 25}])
        words = Words("10 kn", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '18.52', 'tag': 1}, {'word': 'kilometer per hour', 'tag': 25}])
             
    def test_256(self):  
        """ Words - address: num dir name """
        words = Words("12 East Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'east', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 West Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 North Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'north', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 South Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'south', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 E Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'east', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 W Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 N Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'north', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 S Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'south', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 e. Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'east', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        
    def test_257(self):  
        """ Words - more address: num dir name """
        words = Words("12 Northwest Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 Northeast Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 Southwest Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 Southeast Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 North west Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 North East Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 South West Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 South East Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 NW Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 NE Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 SW Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 SE Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 N.W. Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 N.E. Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'northeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 S.W. Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southwest', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 S.E. Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
               
    def test_258(self):  
        """ Words - more address: num dir name """
        words = Words("the 12 se Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("the 12 se Main Ave the", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 Main the", address=True)
        self.assertEqual(words.words, [])
        words = Words("the 12 se 1st Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': '1', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("the 12 se First Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': '1', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
                       
    def test_259(self):  
        """ Words - more address: num dir name type """
        words = Words("12 se Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 Main Ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 se Main Avenue", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 se Main Av", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 se Main Aly", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'alley', 'tag': 30}])
        words = Words("12 se Main Alley", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'alley', 'tag': 30}])
        words = Words("12 se Main Bvd", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'boulevard', 'tag': 30}])
        words = Words("12 se Main Blvd", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'boulevard', 'tag': 30}])
        words = Words("12 se Main Boulevard", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'boulevard', 'tag': 30}])
        words = Words("12 se Main Ct", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'court', 'tag': 30}])
        words = Words("12 se Main Crt", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'court', 'tag': 30}])
        words = Words("12 se Main Court", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'court', 'tag': 30}])
        words = Words("12 se Main Ctr", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'center', 'tag': 30}])
        words = Words("12 se Main Centre", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'center', 'tag': 30}])
        words = Words("12 se Main Center", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'center', 'tag': 30}])
        words = Words("12 se Main Drive", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'drive', 'tag': 30}])
        words = Words("12 se Main Dr", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'drive', 'tag': 30}])
                              
    def test_260(self):  
        """ Words - more address: multiple words for street name """
        words = Words("12 se foo goo ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'foo goo', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 se the goo ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'the goo', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 se foo the ave", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'southeast', 'tag': 28}, {'word': 'foo the', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
                                     
    def test_261(self):
        """ Words - more units of measurement """
        words = Words("10 km/h", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'kilometer per hour', 'tag': 25}])
        words = Words("10 kw/h", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'kilowatt per hour', 'tag': 25}])
        words = Words("10 m3", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'cubic meter', 'tag': 25}])
        words = Words("10 km2", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'square kilometer', 'tag': 25}])
        words = Words("10 mi2", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 1}, {'word': 'square mile', 'tag': 25}])
                                           
    def test_262(self):
        """ Words - more conversions """
        words = Words("10 km2", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '3.86102', 'tag': 1}, {'word': 'square mile', 'tag': 25}])
        words = Words("10 mi2", stopwords=True, metric=True)
        self.assertEqual(words.words, [{'word': '25.8999', 'tag': 1}, {'word': 'square kilometer', 'tag': 25}])
        words = Words("10 m3", stopwords=True, standard=True)
        self.assertEqual(words.words, [{'word': '353.14700000000005', 'tag': 1}, {'word': 'cubic foot', 'tag': 25}])
                                                 
    def test_263(self):
        """ Words - name preceded by a comma """
        words = Words(", James", name=True)
        self.assertEqual(words.words, [{'word': 'james', 'tag': 11}])
        words = Words(", James R. Johns", name=True)
        self.assertEqual(words.words, [{'word': 'james', 'tag': 11}, {'word': 'r', 'tag': 11}, {'word': 'johns', 'tag': 11}])
                                                 
    def test_264(self):
        """ Words - gender reference """
        words = Words("sex: M", gender=True)
        self.assertEqual(words.words, [{'word': 'male', 'tag': 15}])
        words = Words("sex: F", gender=True)
        self.assertEqual(words.words, [{'word': 'female', 'tag': 16}])
        words = Words("sex: T", gender=True)
        self.assertEqual(words.words, [{'word': 'transgender', 'tag': 17}])
        words = Words("sex: Male", gender=True)
        self.assertEqual(words.words, [{'word': 'male', 'tag': 15}])
        words = Words("sex: Female", gender=True)
        self.assertEqual(words.words, [{'word': 'female', 'tag': 16}])
        words = Words("sex: Transgender", gender=True)
        self.assertEqual(words.words, [{'word': 'transgender', 'tag': 17}])
        words = Words("gender: M", gender=True)
        self.assertEqual(words.words, [{'word': 'male', 'tag': 15}])
        words = Words("gender: F", gender=True)
        self.assertEqual(words.words, [{'word': 'female', 'tag': 16}])
        words = Words("gender: T", gender=True)
        self.assertEqual(words.words, [{'word': 'transgender', 'tag': 17}])
        words = Words("gender: Male", gender=True)
        self.assertEqual(words.words, [{'word': 'male', 'tag': 15}])
        words = Words("gender: Female", gender=True)
        self.assertEqual(words.words, [{'word': 'female', 'tag': 16}])
        words = Words("gender: Transgender", gender=True)
        self.assertEqual(words.words, [{'word': 'transgender', 'tag': 17}])
                                                        
    def test_265(self):
        """ Words - address - direction follows street """
        words = Words("12 Main Ave. E.", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'east', 'tag': 28} ])
        words = Words("12 Main Ave. E. the", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'east', 'tag': 28} ])
                                                               
    def test_266(self):
        """ Words - _stem() lemma """
        words = Words("transgenders", gender=True)
        self.assertEqual(words.words, [{'word': 'transgender', 'tag': 17}])    
        
    def test_267(self):
        """ Words - more titles """
        words = Words("Sgt Sam", name=True)
        self.assertEqual(words.words, [{'word': 'sergeant', 'tag': 33}, {'word': 'sam', 'tag': 11}])    
        words = Words("Cpl Sam", name=True)
        self.assertEqual(words.words, [{'word': 'corporal', 'tag': 33}, {'word': 'sam', 'tag': 11}])  
        words = Words("Corporal Sam", name=True)
        self.assertEqual(words.words, [{'word': 'corporal', 'tag': 33}, {'word': 'sam', 'tag': 11}]) 
        words = Words("the Sgt. Sam", name=True)
        self.assertEqual(words.words, [{'word': 'sergeant', 'tag': 33}, {'word': 'sam', 'tag': 11}]) 
        words = Words("the Dr. Sam", name=True)
        self.assertEqual(words.words, [{'word': 'doctor', 'tag': 33}, {'word': 'sam', 'tag': 11}])        
        words = Words(", Dr. James R. Johns", name=True)
        self.assertEqual(words.words, [{'word': 'doctor', 'tag': 33}, {'word': 'james', 'tag': 11}, {'word': 'r', 'tag': 11}, {'word': 'johns', 'tag': 11}])
        words = Words(", Prof. Smith", name=True)
        self.assertEqual(words.words, [{'word': 'professor', 'tag': 33}, {'word': 'smith', 'tag': 11}])
        words = Words(", Dr. James Johns, MD.", name=True)
        self.assertEqual(words.words, [{'word': 'doctor', 'tag': 33}, {'word': 'james', 'tag': 11}, {'word': 'johns', 'tag': 11}, {'word': 'medical doctor', 'tag': 33}])
        
    def test_268(self):
        """ Words - more contradictions """
        words = Words("they're won't ", stopwords=True)
        self.assertEqual(words.words, [{'word': 'they', 'tag': 8}, {'word': 'is', 'tag': 21}, {'word': 'will', 'tag': 21}, {'word': 'not', 'tag': 19}])
                
    def test_269(self):
        """ Words - Number and Unit of Measurement combined """
        words = Words("is 2cm long", number=True)
        self.assertEqual(words.words, [{'word': '2', 'tag': 1}, {'word': 'centimeter', 'tag': 25}])
        words = Words("is 2CM long", number=True)
        self.assertEqual(words.words, [{'word': '2', 'tag': 1}, {'word': 'centimeter', 'tag': 25}])
        words = Words("is 2.6CM long", number=True)
        self.assertEqual(words.words, [{'word': '2.6', 'tag': 1}, {'word': 'centimeter', 'tag': 25}])
                        
    def test_270(self):
        """ Words - more stem corrections """
        words = Words("boring", sentiment=True)
        self.assertEqual(words.words, [{'word': 'bore', 'tag': 19}])
        words = Words("bored", sentiment=True)
        self.assertEqual(words.words, [{'word': 'bore', 'tag': 19}])
        words = Words("promoted contributed", stopwords=True)
        self.assertEqual(towords(words.words), ["promote", "contribute"])
        words = Words("loved lover loves lovely", stopwords=True)
        self.assertEqual(towords(words.words), ["love", "love", "love", "love"])
        words = Words("lived lives liver", stopwords=True)
        self.assertEqual(towords(words.words), ["live", "live", "liver"])
        words = Words("tinest smallest", stopwords=True)
        self.assertEqual(towords(words.words), ["tiny", "small"])
        words = Words("gone", stopwords=True)
        self.assertEqual(towords(words.words), ["go"])
        words = Words("emptied fewer fullest", stopwords=True)
        self.assertEqual(towords(words.words), ["0", "few", "1"])
        words = Words("lowest lower lowering", stopwords=True)
        self.assertEqual(towords(words.words), ["low", "low", "low"])
                           
    def test_271(self):
        """ Words - more street numbers """
        words = Words("12A W Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12-A W Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("123-33 W Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': '12333', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("N1300 Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': 'n1300', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("S1300 Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': 's1300', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("W1300 Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': 'w1300', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("E1300 Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': 'e1300', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("N1100-E1300 Main Ave", stopwords=True)
        self.assertEqual(words.words, [{'word': 'n1100-e1300', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
                        
    def test_272(self):
        """ Words - address - city/state """
        words = Words("12A W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12A W Main Ave., Hoops AL", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AL', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Alabama", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AL', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, AK", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AK', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Alaska", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AK', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops AZ", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AZ', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Arizona", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AZ', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops AR", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AR', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Arkansas", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AR', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops CA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-CA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops California", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-CA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops CO", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-CO', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Colorado", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-CO', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops CT", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-CT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Connecticut", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-CT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops DE", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-DE', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Delaware", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-DE', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops DC", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-DC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, D.C.", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-DC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops FL", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-FL', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Florida", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-FL', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops GA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-GA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Georgia", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-GA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops HI", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-HI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Hawaii", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-HI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Id.", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ID', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Idaho", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ID', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops IL", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-IL', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Illinois", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-IL', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops IN", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-IN', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Indiana", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-IN', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops IA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-IA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Iowa", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-IA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops KS", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-KS', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Kansas", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-KS', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops KY", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-KY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Kentucky", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-KY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops LA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-LA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Louisiana", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-LA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops ME", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ME', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Maine", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ME', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, MD", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MD', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MD", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MD', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Maryland", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MD', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops ME", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ME', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Maine", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ME', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Massachusetts", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MI", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Michigan", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MN", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MN', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Minnesota", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MN', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MS", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MS', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Mississippi", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MS', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MO", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MO', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Missouri", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MO', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops MT", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Montana", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-MT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NE", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NE', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Nebraska", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NE', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NV", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NV', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Nevada", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NV', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NH", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NH', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, New Hampshire", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NH', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NJ", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NJ', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, New Jersey", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NJ', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NM", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NM', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, New Mexico", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NM', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NY", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, New York", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops NC", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, North Carolina", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops ND", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ND', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, North Dakota", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-ND', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops OH", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-OH', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Ohio", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-OH', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops OK", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-OK', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Oklahoma", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-OK', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops PA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Pennsylvania", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops RI", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-RI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Rhode Island", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-RI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops SC", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-SC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, South Carolina", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-SC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops SD", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-SD', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, South Dakota", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-SD', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops TN", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-TN', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Tennessee", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-TN', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops TX", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-TX', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Texas", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-TX', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops UT", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-UT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Utah", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-UT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops VT", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Vermont", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VT', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops VA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Virginia", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops WA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Washington", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops WV", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WV', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, West Virginia", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WV', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops WI", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Wisconsin", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops WY", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Wyoming", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops VI", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Virgin Islands", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops PR", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PR', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Puerto Rico", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PR', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops GU", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-GU', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Guam", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-GU', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops PW", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PW', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Palau", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PW', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops AS", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AS', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, American Samoa", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-AS', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops FM", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-FM', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Micronesia", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-FM', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, Wyoming", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-WY', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, VI", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-VI', 'tag': 32}])
        words = Words("12A W Main Ave., New York, NY", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'new york', 'tag': 31}, {'word': 'ISO3166-2:US-NY', 'tag': 32}])
                               
    def test_273(self):
        """ Words - Post Office Box """
        words = Words("POB 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("POB. 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("P.O.B. 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
                          
    def test_274(self):  
        """ Words - more address: street types """
        words = Words("12 Main Av", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("12 Main Hwy", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'highway', 'tag': 30}])
        words = Words("12 99W Highway", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'highway', 'tag': 30}])
        words = Words("12 Main Jct", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'junction', 'tag': 30}])
        words = Words("12 99W Junction", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'junction', 'tag': 30}])
        words = Words("12 Main Ln.", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'lane', 'tag': 30}])
        words = Words("12 99W Lane", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'lane', 'tag': 30}])
        words = Words("12 Main Pk", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'park', 'tag': 30}])
        words = Words("12 99W Park", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'park', 'tag': 30}])
        words = Words("12 Main Pky", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'parkway', 'tag': 30}])
        words = Words("12 99W Pkwy", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'parkway', 'tag': 30}])
        words = Words("12 Main Parkway", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'parkway', 'tag': 30}])
        words = Words("12 Main Pl", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'place', 'tag': 30}])
        words = Words("12 99W Place", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'place', 'tag': 30}])
        words = Words("12 Main Rd", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'road', 'tag': 30}])
        words = Words("12 99W Road", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'road', 'tag': 30}])
        words = Words("12 99W St", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'street', 'tag': 30}])
        words = Words("12 99W Street", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': '99w', 'tag': 29}, {'word': 'street', 'tag': 30}])
               
    def test_275(self):
        """ Words - multiple names for city """
        words = Words("12A W Main Ave., Lake Oswego, OR", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'lake oswego', 'tag': 31}, {'word': 'ISO3166-2:US-OR', 'tag': 32}])
        words = Words("12A W Main Ave., Lake Oswego OR", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'lake oswego', 'tag': 31}, {'word': 'ISO3166-2:US-OR', 'tag': 32}])
        words = Words("12A W Main Ave., Oregon City, OR", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'oregon city', 'tag': 31}, {'word': 'ISO3166-2:US-OR', 'tag': 32}])
        
    def test_276(self):
        """ Words - title suffixes """
        words = Words(", James Johns, Atty.", name=True)
        self.assertEqual(words.words, [{'word': 'james', 'tag': 11}, {'word': 'johns', 'tag': 11}, {'word': 'attorney', 'tag': 33}])
        words = Words(", James Johns, Attorney", name=True)
        self.assertEqual(words.words, [{'word': 'james', 'tag': 11}, {'word': 'johns', 'tag': 11}, {'word': 'attorney', 'tag': 33}])
        words = Words(", James Johns, Jr.", name=True)
        self.assertEqual(words.words, [{'word': 'james', 'tag': 11}, {'word': 'johns', 'tag': 11}, {'word': 'junior', 'tag': 33}])
        words = Words(", James Johns, Sr.", name=True)
        self.assertEqual(words.words, [{'word': 'james', 'tag': 11}, {'word': 'johns', 'tag': 11}, {'word': 'senior', 'tag': 33}])
                
    def test_277(self):
        """ Words - more Post Office Box """
        words = Words("P.O. Box 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("PO Box 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("PO 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("P.O. 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("P.O. 10, 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("P.O. 10, Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12 W Main Ave., POB 10", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': '10', 'tag': 35}, ])
        words = Words("12 W Main Ave. POB 10", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': '10', 'tag': 35}, ])
        words = Words("POB 123, Seattle, WA", address=True)
        self.assertEqual(words.words, [{'word': '123', 'tag': 35}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("POB 123 Seattle, WA", address=True)
        self.assertEqual(words.words, [{'word': '123', 'tag': 35}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12 W Main Ave. POB 10, Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': '10', 'tag': 35}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12 W Main Ave. POB 10 Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': '10', 'tag': 35}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
                       
    def test_278(self):
        """ Words - secondary address component """
        words = Words("12 W Main Ave., Apt. 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'apartment 3', 'tag': 36}])
        words = Words("12 W Main Ave. Apt. 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'apartment 3', 'tag': 36}])
        words = Words("12 W Main Ave., Apartment 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'apartment 3', 'tag': 36}])
        words = Words("12 W Main Ave., Ste. 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'suite 3', 'tag': 36}])   
        words = Words("12 W Main Ave., Suite 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'suite 3', 'tag': 36}])
        words = Words("12 W Main Ave., Fl. 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'floor 3', 'tag': 36}])   
        words = Words("12 W Main Ave., Floor 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'floor 3', 'tag': 36}])
        words = Words("12 W Main Ave., Rm. 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'room 3', 'tag': 36}])   
        words = Words("12 W Main Ave., Room 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'room 3', 'tag': 36}])
        words = Words("12 W Main Ave., Dept. 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}])   
        words = Words("12 W Main Ave., Dept 3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}])   
        words = Words("12 W Main Ave., Dept #3", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}])  
        words = Words("12 W Main Ave., Dept D-13", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department d13', 'tag': 36}])  
        words = Words("12 W Main Ave., Bldg D-13", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'building d13', 'tag': 36}])  
        words = Words("12 W Main Ave., Building D-13", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'building d13', 'tag': 36}])
        
    def test_279(self):
        """ Words - address words not in address """
        words = Words("suites lanes apartments rooms floors drives", stopwords=True)
        self.assertEqual(towords(words.words), ["suite", "lane", "apartment", "room", "floor", "drive"])
                              
    def test_280(self):
        """ Words - secondary address component, City/State """
        words = Words("12 W Main Ave., Dept 3, Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12 W Main Ave., Dept 3 Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
                                    
    def test_281(self):
        """ Words - Postal Code """
        words = Words("12 W Main Ave., Dept 3, Seattle, WA 98607", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}, {'word': '98607', 'tag': 34}])
        words = Words("12 W Main Ave., Dept 3, Seattle, WA, 98607", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}, {'word': '98607', 'tag': 34}])
        words = Words("12 W Main Ave., Dept 3, Seattle, WA 98607-1234", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'department 3', 'tag': 36}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}, {'word': '98607-1234', 'tag': 34}])
                                            
    def test_282(self):
        """ Words - ily word endings """
        words = Words("arbitrarily ordinarily culinarily")
        self.assertEqual(towords(words.words), ["arbitrary", "ordinary", "culinary"])
        words = Words("stepfamily")
        self.assertEqual(towords(words.words), ["stepfamily"])  
        
    def test_283(self):
        """ Words - gender - step """
        words = Words("stepbrother stepfather stepsister stepmother", gender=True)
        self.assertEqual(words.words, [{'word': 'stepbrother', 'tag': 15}, {'word': 'stepfather', 'tag': 15}, {'word': 'stepsister', 'tag': 16}, {'word': 'stepmother', 'tag': 16}])
        words = Words("stepdad stepmom", gender=True)
        self.assertEqual(words.words, [{'word': 'stepdad', 'tag': 15}, {'word': 'stepmom', 'tag': 16}])
        words = Words("husband wife", gender=True)
        self.assertEqual(words.words, [{'word': 'husband', 'tag': 15}, {'word': 'wife', 'tag': 16}])
                
    def test_284(self):
        """ Words - word endings lled """
        words = Words("annulled canceled called")
        self.assertEqual(towords(words.words), ["annul", "cancel", "call"]) 
        words = Words("appalled bankrolled chilled", stopwords=True)  
        self.assertEqual(towords(words.words), ["appall", "bankroll", "chill"])    
        
    def test_285(self):
        """ Words - more sentiment words """
        words = Words("horribly", sentiment=True)
        self.assertEqual(words.words, [{'word': 'horror', 'tag': 19}])
        words = Words("horrible", sentiment=True)
        self.assertEqual(words.words, [{'word': 'horror', 'tag': 19}])
        words = Words("horrifying", sentiment=True)
        self.assertEqual(words.words, [{'word': 'horror', 'tag': 19}])
        words = Words("appalled", sentiment=True)
        self.assertEqual(words.words, [{'word': 'appall', 'tag': 19}])
        words = Words("terribly", sentiment=True)
        self.assertEqual(words.words, [{'word': 'terrible', 'tag': 19}])  
        
    def test_286(self):
        """ Words - more endings """
        words = Words("taxes lives elves hides haves halves grasses braves", stopwords=True)
        self.assertEqual(towords(words.words), ["tax", "live", "elf", "hide", "has", "0.5", "grass", "brave"]) 
        words = Words("pies ponies loaves fishes wives", stopwords=True)
        self.assertEqual(towords(words.words), ["pie", "pony", "loaf", "fish", "wife"])
        words = Words("dwarves wharves", stopwords=True)
        self.assertEqual(towords(words.words), ["dwarf", "wharf"])
        words = Words("floating hiking biking hiding sinking", stopwords=True)
        self.assertEqual(towords(words.words), ["float", "hike", "bike", "hide", "sink"])
        words = Words("plotting committing", stopwords=True)
        self.assertEqual(towords(words.words), ["plot", "commit"])
        words = Words("raced racing races", stopwords=True)
        self.assertEqual(towords(words.words), ["race", "race", "race"])
        words = Words("dances danced dancing", stopwords=True)
        self.assertEqual(towords(words.words), ["dance", "dance", "dance"])    
        words = Words("combined deaths injuries", stopwords=True)
        self.assertEqual(towords(words.words), ["combine", "death", "injury"])        
        words = Words("crashed crashes", stopwords=True)
        self.assertEqual(towords(words.words), ["crash", "crash"])    
        
    def test_287(self):
        """ Words - more addresses """
        words = Words("12 E. Main st., Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'east', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'street', 'tag': 30}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
        words = Words("12 Main st. e., Seattle, WA", stopwords=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'main', 'tag': 29}, {'word': 'street', 'tag': 30}, {'word': 'east', 'tag': 28}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}])
                 
    def test_288(self):
        """ Words - more word endings """
        words = Words("received receives receiving")
        self.assertEqual(towords(words.words), ["receive", "receive", "receive"])      
        words = Words("serves served serving")
        self.assertEqual(towords(words.words), ["serve", "serve", "serve"])       
        words = Words("computer computers")
        self.assertEqual(towords(words.words), ["computer", "computer"])      
        words = Words("continued continuing")
        self.assertEqual(towords(words.words), ["continue", "continue"])    
        
    def test_289(self):
        """ Words - more names """
        words = Words(": Andy James", name=True)
        self.assertEqual(words.words, [{'word': 'andy', 'tag': 11}, {'word': 'james', 'tag': 11}])
           
    def test_290(self):
        """ Words - other telephone """
        words = Words("202-123-4567", stopwords=True)
        self.assertEqual(words.words, [{'word': '2021234567', 'tag': 10}])
        words = Words("202 123-4567", stopwords=True)
        self.assertEqual(words.words, [{'word': '2021234567', 'tag': 10}])
        words = Words("(202) 123-4567", stopwords=True)
        self.assertEqual(words.words, [{'word': '2021234567', 'tag': 10}])      
        
    def test_291(self):
        """ Words - Derivation endings """
        words = Words("ongoing advertise normalise alphabetise sexualized franchise industrialise baptise chastise fantasized sized", stopwords=True)
        self.assertEqual(towords(words.words), ["ongoing", "advertise", "normal", "alphabet", "sexual", "franchise", "industrial", "baptise", "chastise", "fantasy", "size"])
        words = Words("merchandise legalize legalizing legitimize authorize")
        self.assertEqual(towords(words.words), ["merchandise", "legal", "legal", "legitimate", "authorize"])
        words = Words("rarefy testify testified uglify happify gentrify categorify betterfy", stopwords=True)
        self.assertEqual(towords(words.words), ["rare", "testify", "testify", "ugly", "happy", "gentry", "category", "better"])
        words = Words("butterflies")
        self.assertEqual(towords(words.words), ["butterfly"])
        words = Words("handful powerful shitful artful beautiful colorful fanciful merciful")
        self.assertEqual(towords(words.words), ["hand", "power", "shit", "art", "beauty", "color", "fancy", "mercy"])
        words = Words("calmness darkness kindness messiness", stopwords=True)
        self.assertEqual(towords(words.words), ["calm", "dark", "kind", "messy"])
              
    def test_292(self):
        """ More stemming """
        words = Words("dinner transfer transferrer")
        self.assertEqual(towords(words.words), ["dine", "transfer", "transfer"])       
        
    def test_293(self):
        """ More NER gender """
        words = Words("grandfather grandpa papa grandmother grandma momma son daughter", stopwords=True)
        self.assertEqual(words.words, [{'word': 'grandfather', 'tag': 15}, {'word': 'grandfather', 'tag': 15}, {'word': 'father', 'tag': 15}, {'word': 'grandmother', 'tag': 16}, {'word': 'grandmother', 'tag': 16}, {'word': 'mother', 'tag': 16}, {'word': 'son', 'tag': 15}, {'word': 'daughter', 'tag': 16}])    
        words = Words("sis bro", stopwords=True)
        self.assertEqual(words.words, [{'word': 'sister', 'tag': 16}, {'word': 'brother', 'tag': 15}])
        
    def test_294(self):
        """ Porter Stemmer """
        words = Words("taxes lives elves hides haves halves grasses braves", stem='porter')
        self.assertEqual(towords(words.words), ["tax", "live", "elv", "hide", "halv", "grass", "brave"])      
        
    def test_295(self):
        """ Snowball Stemmer """
        words = Words("taxes lives elves hides haves halves grasses braves", stem='snowball')
        self.assertEqual(towords(words.words), ["tax", "live", "elv", "hide", "halv", "grass", "brave"])      
        
    def test_296(self):
        """ Lancaster Stemmer """
        words = Words("taxes lives elves hides haves halves grasses braves", stem='lancaster')
        self.assertEqual(towords(words.words), ["tax", "liv", "elv", "hid", "hav", "halv", "grass", "brav"])      
        
    def test_297(self):
        """ Lemma """
        words = Words("taxes lives elves hides haves halves grasses braves", stem='lemma')
        self.assertEqual(towords(words.words), ["tax", "life", "elf", "hide", "grass", "brave"])      
        
    def test_298(self):
        """ POS tags """
        words = Words("Jim Jones", pos=True, stopwords=True)
        self.assertEqual(words.words, [{'word': 'jim', 'tag':0, 'pos': 'NN'}, {'word': 'jones', 'tag':11, 'pos': 'NNS'}])     
        
    def test_299(self):
        """ Words - more key value separators """
        words = Words("SSN is 544-12-1222", ssn=True)
        self.assertEqual(towords(words.words), ["544121222"])
        words = Words("DOB is 01-02-2018", dob=True)
        self.assertEqual(towords(words.words), ["2018-01-02"])
        words = Words("Phone of (800) 123-1234", telephone=True)
        self.assertEqual(towords(words.words), ["8001231234"])   
        
    def test_300(self):
        """ Words - Address PMB """
        words = Words("PMB 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("PMB. 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("P.M.B. 10 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])

    def test_301(self):
        """ Words - Address Canada STN/RPO """
        words = Words("POB 10 STN A 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': 'a', 'tag': 37}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("POB 10 RPO A 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': 'a', 'tag': 37}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])
        words = Words("POB 10 Station A 12 W Main Ave.,", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': 'a', 'tag': 37}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}])

    def test_302(self):
        """ Words - Canada Provinces """
        words = Words("12 W Main Ave., Calgary, Alberta", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'calgary', 'tag': 31}, {'word': 'ISO3166-2:CA-AB', 'tag': 32}])
        words = Words("12 W Main Ave., Calgary, AB", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'calgary', 'tag': 31}, {'word': 'ISO3166-2:CA-AB', 'tag': 32}])
        words = Words("12 W Main Ave., Victoria Island, British Columbia", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'victoria island', 'tag': 31}, {'word': 'ISO3166-2:CA-BC', 'tag': 32}])
        words = Words("12 W Main Ave., Victoria Island, BC", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'victoria island', 'tag': 31}, {'word': 'ISO3166-2:CA-BC', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Manitoba", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-MB', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, MB", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-MB', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, New Brunswick", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NB', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, NB", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NB', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Newfoundland and Labrador", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NL', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, NF", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NL', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Northwest Territories", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NT', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, NT", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NT', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Nova Scotia", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NS', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, NS", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NS', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Northwest Territories", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NT', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, NT", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-NT', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Ontario", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-ON', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, ON", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-ON', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Prince Edward Island", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-PE', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, PE", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-PE', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Quebec", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-QC', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, QC", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-QC', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Québec", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-QC', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, SK", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-SK', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Saskatchewan", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-SK', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, YT", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-YT', 'tag': 32}])
        words = Words("12 W Main Ave., Hoops, Yukon", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:CA-YT', 'tag': 32}])

    def test_303(self):
        """ Words - Canada Postal Codes """
        words = Words("12 W Main Ave., Calgary, Alberta V8X 3X4", address=True)
        self.assertEqual(words.words, [{'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'calgary', 'tag': 31}, {'word': 'ISO3166-2:CA-AB', 'tag': 32}, {'word': 'v8x3x4', 'tag': 34}])

    def test_304(self):
        """ Words - USA international code in telephone number """
        words = Words("1-800-360-1234", telephone=True)
        self.assertEqual(words.words, [{'word': '18003601234', 'tag': 10}])
        words = Words("1 (800) 360-1234", telephone=True)
        self.assertEqual(words.words, [{'word': '18003601234', 'tag': 10}])
        words = Words("1 800 360 1234", telephone=True)
        self.assertEqual(words.words, [{'word': '18003601234', 'tag': 10}])
        words = Words("tele: 18003601234", telephone=True)
        self.assertEqual(words.words, [{'word': '18003601234', 'tag': 10}])
        words = Words("1.800.360.1234", telephone=True)
        self.assertEqual(words.words, [{'word': '18003601234', 'tag': 10}])
        words = Words("800.360.1234", telephone=True)
        self.assertEqual(words.words, [{'word': '8003601234', 'tag': 10}])
        
    def test_305(self):
        """ Words - Romanization """
        words = Words("Quebec", roman=True)
        self.assertEqual(words.words, [{'word': 'quebec', 'tag': 0}])
        words = Words("Québec", roman=False)
        self.assertEqual(words.words, [{'word': 'québec', 'tag': 0}])
        words = Words("Québec")
        self.assertEqual(words.words, [{'word': 'québec', 'tag': 0}])
        
    def test_306(self):
        """ Words - addresses that were broken """
        words = Words("PMB 10 12 W Main Ave. foo", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'foo', 'tag': 0}])
        words = Words("PMB 10 12 W Main Ave., Seattle, WA foo", stopwords=True)
        self.assertEqual(words.words, [{'word': '10', 'tag': 35}, {'word': '12', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'seattle', 'tag': 31}, {'word': 'ISO3166-2:US-WA', 'tag': 32}, {'word': 'foo', 'tag': 0}])
        words = Words("12A W Main Ave., Hoops D.C.", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-DC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops, D.C.", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-DC', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Rhode Island", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-RI', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops Puerto Rico", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-PR', 'tag': 32}])
        words = Words("12A W Main Ave., Hoops New Hampshire", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'hoops', 'tag': 31}, {'word': 'ISO3166-2:US-NH', 'tag': 32}])
        words = Words("12A W Main Ave., Mt. View CA", address=True)
        self.assertEqual(words.words, [{'word': '12a', 'tag': 27}, {'word': 'west', 'tag': 28}, {'word': 'main', 'tag': 29}, {'word': 'avenue', 'tag': 30}, {'word': 'mountain view', 'tag': 31}, {'word': 'ISO3166-2:US-CA', 'tag': 32}])
   
    def test_307(self):
        """ Words - more birthdates """     
        words = Words("birthdate: 01/02/2018", dob=True)     
        self.assertEqual(words.words, [{'word': '2018-01-02', 'tag': 20}])
        words = Words("birth date: 01/02/2018", dob=True)
        self.assertEqual(words.words, [{'word': 'birth', 'tag': 0}, {'word': '2018-01-02', 'tag': 20}])       
        words = Words("birthday: 01/02/2018", dob=True)     
        self.assertEqual(words.words, [{'word': '2018-01-02', 'tag': 20}])
        
    def test_308(self):
        """ Words - Units of Measurements """
        words = Words("Height: 71 inches", unit=True)
        self.assertEqual(words.words, [{'word': 'height', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Height: 71 in.", unit=True)
        self.assertEqual(words.words, [{'word': 'height', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Height: 71in", unit=True)
        self.assertEqual(words.words, [{'word': 'height', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Ht. 71in", unit=True)
        self.assertEqual(words.words, [{'word': 'height', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Ht.: 71in", unit=True)
        self.assertEqual(words.words, [{'word': 'height', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Weight: 71lbs", unit=True)
        self.assertEqual(words.words, [{'word': 'weight', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'pound', 'tag': 25}])
        words = Words("Wt: 71 lbs", unit=True)
        self.assertEqual(words.words, [{'word': 'weight', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'pound', 'tag': 25}])
        words = Words("Length: 71in", unit=True)
        self.assertEqual(words.words, [{'word': 'length', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("len: 71in", unit=True)
        self.assertEqual(words.words, [{'word': 'length', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Width: 71in", unit=True)
        self.assertEqual(words.words, [{'word': 'width', 'tag': 38}, {'word': '71', 'tag': 1}, {'word': 'inch', 'tag': 25}])
        words = Words("Volume: 2 liters", unit=True)
        self.assertEqual(words.words, [{'word': 'volume', 'tag': 38}, {'word': '2', 'tag': 1}, {'word': 'liter', 'tag': 25}])
        words = Words("Distance: 3.7mi", unit=True)
        self.assertEqual(words.words, [{'word': 'length', 'tag': 38}, {'word': '3.7', 'tag': 1}, {'word': 'mile', 'tag': 25}])
        words = Words("Speed: 10 mph", unit=True)
        self.assertEqual(words.words, [{'word': 'speed', 'tag': 38}, {'word': '10', 'tag': 1}, {'word': 'mile per hour', 'tag': 25}])
        words = Words("velocity: 10 mph", unit=True)
        self.assertEqual(words.words, [{'word': 'speed', 'tag': 38}, {'word': '10', 'tag': 1}, {'word': 'mile per hour', 'tag': 25}])
        words = Words("quantity: 10", unit=True)
        self.assertEqual(words.words, [{'word': 'quantity', 'tag': 38}, {'word': '10', 'tag': 1}])
        words = Words("depth: 20ft", unit=True)
        self.assertEqual(words.words, [{'word': 'depth', 'tag': 38}, {'word': '20', 'tag': 1}, {'word': 'foot', 'tag': 25}])
        words = Words("deep: 20ft", unit=True)
        self.assertEqual(words.words, [{'word': 'depth', 'tag': 38}, {'word': '20', 'tag': 1}, {'word': 'foot', 'tag': 25}])
        words = Words("size: 3 x 4", unit=True)
        self.assertEqual(words.words, [{'word': 'size', 'tag': 38}, {'word': '3', 'tag': 1}, {'word': 'x', 'tag': 0}, {'word': '4', 'tag': 1}])
        words = Words("ht: 5' 6\"", unit=True)
        self.assertEqual(words.words, [{'word': 'height', 'tag': 38}, {'word': '5', 'tag': 1}, {'word': 'foot', 'tag': 25}, {'word': '6', 'tag': 1}, {'word': 'inch', 'tag': 25}]) 
        
    def test_309(self):
        """ Words - more telephone """
        words = Words("Customer Support: (360) 123-1234", telephone=True)
        self.assertEqual(words.words, [{'word': 'customer', 'tag': 0}, {'word': '3601231234', 'tag': 10}]) 
        words = Words("Fax: (360) 123-1234", telephone=True)
        self.assertEqual(words.words, [{'word': '3601231234', 'tag': 42}])      
        
    def test_310(self):
        """ Words - not a measurement """
        words = Words("he said, 'I am 26'", stopwords = True)
        self.assertEqual(words.words, [{'word': 'he', 'tag': 8}, {'word': 'said', 'tag': 21}, {'word': 'i', 'tag': 8}, {'word': 'am', 'tag': 21}, {'word': '26', 'tag': 1}]) 
       
    def test_311(self):
        """ Words - fahrenheit / celsius """
        words = Words("26 °F", stopwords=True)
        self.assertEqual(words.words, [{'word': '26', 'tag': 1}, {'word': 'fahrenheit', 'tag': 25}])
        words = Words("26 °C", stopwords=True)
        self.assertEqual(words.words, [{'word': '26', 'tag': 1}, {'word': 'celsius', 'tag': 25}])
              
    def test_312(self):
        """ Words - min/max/ave measurements """
        words = Words("maximum: 36", stopwords=True)
        self.assertEqual(words.words, [{'word': 'maximum', 'tag': 38}, {'word': '36', 'tag': 1}])
        words = Words("max. 36", stopwords=True)
        self.assertEqual(words.words, [{'word': 'maximum', 'tag': 38}, {'word': '36', 'tag': 1}])
        words = Words("max 36", stopwords=True)
        self.assertEqual(words.words, [{'word': 'maximum', 'tag': 38}, {'word': '36', 'tag': 1}])
        words = Words("average: 36", stopwords=True)
        self.assertEqual(words.words, [{'word': 'average', 'tag': 38}, {'word': '36', 'tag': 1}])
        words = Words("ave. 36", stopwords=True)
        self.assertEqual(words.words, [{'word': 'average', 'tag': 38}, {'word': '36', 'tag': 1}])
        words = Words("ave 36", stopwords=True)
        self.assertEqual(words.words, [{'word': 'average', 'tag': 38}, {'word': '36', 'tag': 1}])   
        
    def test_313(self):
        """ Words constructor  = age is not a bool """
        with pytest.raises(TypeError):
            words = Words("one", age=12)
        
    def test_314(self):
        """ Words: Age """
        words = Words("age: 36", age=True)
        self.assertEqual(words.words, [{'word': '36', 'tag': 43}])   
        words = Words("36 yrs", age=True)
        self.assertEqual(words.words, [{'word': '36', 'tag': 43}])  
        words = Words("36 yr foo", age=True)
        self.assertEqual(words.words, [{'word': '36', 'tag': 43}, {'word': 'foo', 'tag': 0}])  
        words = Words("36 years old foo", age=True)
        self.assertEqual(words.words, [{'word': '36', 'tag': 43}, {'word': 'foo', 'tag': 0}])  
        
    def test_315(self):
        """ Words bag of words """
        words = Words("three two one three three two", number=True)
        self.assertEqual(words.bagOfWords, { '2': 2, '1': 1, '3': 3 }) 
        self.assertEqual(words.freqDist, [ ('3', 3), ('2', 2), ('1', 1) ])  
        
    def test_316(self):
        """ hwy / fwy """
        words = Words("hwy accidents fwy accidents")
        self.assertEqual(towords(words.words), ["highway", "accident", "freeway", "accident"])
        
    def test_317(self):
        """ more word endings """
        words = Words("permitted provider provided based shared sharing")
        self.assertEqual(towords(words.words), ["permit", "provide", "provide", "base", "share", "share"])
        words = Words("includes included including", stopwords=True)
        self.assertEqual(towords(words.words), ["include", "include", "include"])
        words = Words("treated treating treatment lazy", stopwords=True)
        self.assertEqual(towords(words.words), ["treat", "treat", "treat", "lazy"])
          
    def xtest_bugs(self):
        words = Words("vis-a-vis semi-colon twenty-three")
        words = Words("10 m/s", stopwords=True)
        words = Words("10 ft/s", stopwords=True)
        words = Words("min 36", stopwords=True)
        # dad -> father, mom -> 
           
def towords(list):
    words = []
    for word in list:
        words.append(word['word'])
    return words
