class Segment(object):
    """ Segment text into Regions """
    
    HEADING   = 1
    PARAGRAPH = 2
    
    def __init__(self, text):
        """ """
        self._text = text
        self._segments = []
        self._segmentation()
        
    def _segmentation(self):
        """ Split text into paragraphs """
        para = ''
        
        lines = self._text.split('\n')
        for line in lines:
            s_line = line.strip()
            if s_line == '':
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = ''
            elif s_line.isupper():
                if para != '':
                    self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
                    para = '' 
                self._segments.append( { 'text': line, 'tag': self.HEADING } )
            else:
                para += line
                
        if para != '':
            self._segments.append( { 'text': para, 'tag': self.PARAGRAPH } )
            para = ''