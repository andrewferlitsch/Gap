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
        self.index_pob = 0
        self.index_stn = 0
        
    def parse(self, words, index):
        """ Parse an Address """
        self.words = words
        self.index = index
        self.length = len(self.words) 
        
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
        self.pob, n = self.parse_pob()
        if self.pob is not None:
            self.index_pob = index
            index += n
            return True
        return False
            
    def parse_pob(self):
        """ Look for Post Office Box 
        PMB digits
        POB digits
        P.O.B digits
        P.O. Box digits
        P.O. digits
        """
        
        index  = self.index
        start  = self.index      
        
        if self.words[index]['word'] == 'pob' or self.words[index]['word'] == 'pmb':
            index += 1
            if index == self.length:
                return None, 0
            if self.words[index]['word'] == '.':
                return self.words[index+1]['word'], 3
            else:
                return self.words[index]['word'], 2
        elif self.words[index]['word'] == 'p':
            index += 1
            if index == self.length:
                return None, 0
            if self.words[index]['word'] == '.':
                index += 1
                if index == self.length:
                    return None, 0
            if self.words[index]['word'] not in ['o', 'm']:
                return None, 0
            index += 1
            if index == self.length:
                return None, 0
            if self.words[index]['word'] == '.':
                index += 1
                if index == self.length:
                    return None, 0
            if self.words[index]['word'] in ['b', 'box']:
                index += 1
                if index == self.length:
                    return None, 0
            elif not self.words[index]['word'].isdigit():
                return None,0
            if self.words[index]['word'] == '.':
                index += 1
                if index == self.length:
                    return None, 0
            return self.words[index]['word'], index - start + 1
        
        if self.words[index]['word'] == 'po':
            index += 1
            if index == self.length:
                return None, 0
            if self.words[index]['word'] == 'box':
                index += 1
                if index == self.length:
                    return None, 0
            return self.words[index]['word'], index - start + 1
            
        return None, 0