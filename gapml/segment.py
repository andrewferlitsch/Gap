""" Segment Module for Processing PDF Documents 
Copyright 2018(c), Andrew Ferlitsch
"""

version = '0.9.2'

class Segment(object):
    """ Segment text into Regions """
    
    HEADING     = 1001
    PARAGRAPH   = 1002
    PAGENO      = 1003
    COPYRIGHT   = 1004
    
    def __init__(self, text):
        """ constructor """  
        # value must be a string
        if text and not isinstance(text, str) :
            raise TypeError("String expected for text")
            
        self._text = text
        self._segments = []
            
        # Do Segmentation of the text
        if text:
            self._segmentation()
        
    def _segmentation(self):
        """ Split text into:
        Headings
        Paragraphs
        Table of Contents
        Page Numbering
        """
        para = ''
        
        # Split the text into lines
        lines = self._text.split('\n')
        # Process each line
        for line in lines:
            s_line = line.strip()
            # Blank Line: look for paragraph
            if s_line == '':
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = ''
            # All Upper: Heading
            elif s_line.isupper():
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = '' 
                self._segments.append( { 'text': line, 'tag': self.HEADING } )
            # Copyright
            elif s_line.lower().startswith("copyright"):
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = '' 
                self._segments.append( { 'text': line, 'tag': self.COPYRIGHT } )
            else:
                # Look for page number
                pageno = False
                toks = s_line.split(' ')
                ntoks = len(toks)
                
                # Number by itself on a line
                if ntoks == 1 and toks[0].isdigit():
                    pageno = True
                # page|p[.] number
                elif ntoks == 2:
                    if toks[0].lower() in [ 'page', 'p', 'p.'] and toks[1].isdigit():
                        pageno = True
                # - number -
                elif ntoks == 3:
                    if toks[0] == '-' and toks[1].isdigit() and toks[2] == '-':
                        pageno = True
                if not pageno:
                    # Look for heading
                    heading = True
                    for tok in toks:
                        if tok == '' or len(tok) == 0:
                            pass
                        elif tok[0].isdigit() or tok[0].isupper() or tok[0] == '.':
                            pass
                        else:
                            heading = False
                else:
                    heading = False
                    
                if heading:
                    if para != '':
                        self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                        para = '' 
                    self._segments.append( { 'text': line, 'tag': self.HEADING } )
                elif pageno:      
                    if para != '':
                        self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                        para = '' 
                    self._segments.append( { 'text': line, 'tag': self.PAGENO } )  
                else:
                    if para != '':
                        para += '\n' + line
                    else:
                        para = line
                
        if para != '':
            self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
            para = ''
            
    @property
    def segments(self):
        """ Getter for segments """
        return self._segments
        
    def __len__(self):
        """ return the number of segments """
        return len(self._segments)