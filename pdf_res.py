"""
Copyright 2018(c), Andrew Ferlitsch
"""
import os.path

class PDFResource(object):
    """ Parse the Resource Definition of a PDF File """
    PAGES   = 1
    
    def __init__(self, document, debug=False):
        self._debug = debug
        
        # Check that document exists
        if os.path.isfile(document) == False:
            raise FileNotFoundError(document)
            
        # open the PDF document for reading
        self._document = document
        with open(document, 'rb') as f:
            # Read the magic sequence
            self._magic = f.read(5)
            if self._magic != b'%PDF-':
                raise ValueError("%PDF not found")
            self._version = f.read(3)
            if self._debug: print("PDF Version", str(self._version.decode("utf-8")))
            
            self._text = self._image = False
            while True:
                try:
                    line = f.readline().decode()
                except:
                    continue
                if line.startswith("/Resources<</ProcSet[/PDF"):
                    resources = line[25:]
                    if self._debug: print("resources", resources)
                    if "/Text" in resources:
                        self._text = True
                    if "/ImageB" in resources or "/ImageC" in resources or "/ImageI" in resources:
                        self._image = True
                    break
    @property
    def version(self):
        """ Get the PDF version """
        return self._version

    @property
    def text(self):
        """ Get whether the page contains text """
        return self._text

    @property
    def image(self):
        """ Get whether the page contains an image """
        return self._image
        

import sys
if __name__ == "__main__":
    p = PDFResource(sys.argv[1])
    print("Text", p.text)
    print("Image", p.image)