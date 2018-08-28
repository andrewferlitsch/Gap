""" Address Module for Identifying/Reducing US/CA Street and Postal Addresses
Copyright, 2018(c), Andrew Ferlitsch
"""
from .vocabulary import Vocabulary, vocab

class Address(object):
    _debug = False
    
    """ US/CA Street/Postal Addresses """
    def __init__(self, words, index):
        """ Parse an Address """
        self._pob = None
        self._stn = None
        self._num = None
        self._dir = None
        self._nam = None
        self._typ = None
        self._sac = None
        self._cty = None
        self._sta = None
        self._pst = None
        self.idx_pob = 0
        self.idx_stn = 0
        self.idx_num = 0
        self.idx_dir = 0
        self.idx_nam = 0
        self.idx_typ = 0
        self.idx_sac = 0
        self.idx_cty = 0
        self.idx_sta = 0
        self.idx_pst = 0
        self.isaddr  = False
        
        self.words = words
        self.index = index
        self.length = len(self.words) 
        
        if self.pob():
            self.stn()
        self.streetnum()
        
        if self._pob is None and self._num is None:
            return 
        if self._num is not None:
            self.streetdir()
            self.streetname()
            self.streettype()
        
        if not self._pob and not self._typ:
            return
            
        if not self._dir:
            self.streetdir()
        if not self._pob:
            self.pob()
            
        self.sac()

        if self.citystate():
            self.postal()

        if self._pob is not None:
            words[self.idx_pob]['word'] = self._pob
            words[self.idx_pob]['tag']  = Vocabulary.POB
        if self._stn is not None:
            words[self.idx_stn]['word'] = self._stn
            words[self.idx_stn]['tag']  = Vocabulary.STATION
        if self._num is not None:
            words[self.idx_num]['word'] = self._num
            words[self.idx_num]['tag']  = Vocabulary.STREET_NUM
        if self._dir is not None:
            words[self.idx_dir]['word'] = self._dir
            words[self.idx_dir]['tag']  = Vocabulary.STREET_DIR
        if self._nam is not None:
            words[self.idx_nam]['word'] = self._nam
            words[self.idx_nam]['tag']  = Vocabulary.STREET_NAME
        if self._typ is not None:
            words[self.idx_typ]['word'] = self._typ
            words[self.idx_typ]['tag']  = Vocabulary.STREET_TYPE
        if self._sac is not None:
            words[self.idx_sac]['word'] = self._sac
            words[self.idx_sac]['tag']  = Vocabulary.SAC
        if self._cty is not None:
            words[self.idx_cty]['word'] = self._cty
            words[self.idx_cty]['tag']  = Vocabulary.CITY
        if self._sta is not None:
            words[self.idx_sta]['word'] = self._sta
            words[self.idx_sta]['tag']  = Vocabulary.STATE
        if self._pst is not None:
            words[self.idx_pst]['word'] = self._pst
            words[self.idx_pst]['tag']  = Vocabulary.POSTAL
        
    def pob(self):
        """ Parse a Post Office Box """
        if self.index >= self.length:
            return False
            
        self._pob, n = self.parse_pob()
        if self._pob is not None:
            self.idx_pob = self.index
            self.index += n
            self.isaddr = True
            if self.index < self.length and self.words[self.index]['word'] == ',':
                self.index += 1
            if self._debug: print("POB", self._pob, self.idx_pob)
            return True
        return False
            
    def parse_pob(self):
        """ Parse a Post Office Box 
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
        
    def stn(self):
        """ Parse a Postal Station """
        if self.index >= self.length:
            return False
            
        self._stn, n = self.parse_stn()
        if self._stn is not None:
            self.idx_stn = self.index
            self.index += n
            if self.index < self.length and self.words[self.index]['word'] == ',':
                self.index += 1
            if self._debug: print("STN", self._stn, self.idx_stn)
            return True
        return False
        
    def parse_stn(self):
        """ Parse a Postal Station
        (STN|RPO|Station) word
        """
        
        index  = self.index
        start  = self.index    
        
        if index == self.length:
            return None, 0
        
        if self.words[index]['word'] == 'stn' or self.words[index]['word'] == 'station' or self.words[index]['word'] == 'rpo':
            index += 1
            if index == self.length:
                return None, 0
            if self.words[index]['word'] == '.':
                return self.words[index+1]['word'], 3
            else:
                return self.words[index]['word'], 2
                
        return None, 0
        
    def streetnum(self):
        """ Parse a Street Number """
        if self.index >= self.length:
            return False
            
        self._num, n = self.parse_streetnum()
        if self._num is not None:
            self.idx_num = self.index
            self.index += n
            if self._debug: print("NUM", self._num, self.idx_num)
            return True
        return False
        
    def parse_streetnum(self):
        """ Parse a Street Number:
        [(N|S|W|E)[-(N|S|W|E)digits]]digits[letter][-][digits]
        """
        
        index  = self.index
        start  = self.index 
        
        if len(self.words[index]['word']) == 1 and not self.words[index]['word'][0].isdigit():
            return None, 0
                    
        # [(N|S|W|E)]
        number = self.words[index]['word']
        if self.words[index]['word'][0] in ['n', 's', 'w', 'e']:
            word = self.words[index]['word'][1:]
        else:
            word = self.words[index]['word']
            
        # digits[letter]
        if not word[0].isdigit():
            return None, 0
            
        index += 1
        if index == self.length:
            return None, 0
            
        # [-][digits|letter]
        if self.words[index]['word'] == '-':
            index += 1
            if index == self.length:
                return None, 0
            
            # [(N|S|W|E)digits]
            if self.words[index]['word'][0] in ['n', 's', 'w', 'e'] and self.words[index]['word'][1:].isdigit():
                number += "-"
            #[letter]
            elif len(self.words[index]['word']) == 1 and self.words[index]['word'].isalpha():
                pass
            #[digits]
            elif not self.words[index]['word'].isdigit():
                index -= 2
            number += self.words[index]['word']
            index += 1
            if index == self.length:
                return None, 0

        return number, index - start
        
    def streetdir(self):
        """ Parse a Street Direction """
        if self.index >= self.length:
            return False
            
        self._dir, n = self.parse_streetdir()
        if self._dir is not None:
            self.idx_dir = self.index
            self.index += n
            if self.index < self.length and self.words[self.index]['word'] == '.':
                self.index += 1
            if self.index < self.length and self.words[self.index]['word'] == ',':
                self.index += 1
            if self._debug: print("DIR", self._dir, self.idx_dir)
            return True
        return False

    def parse_streetdir(self):
        """ Parse a Street Direction 
        (n|s|w|e|nw|ne|sw|se)
        (north|south|west|east)
        (north[[sp]west|east]|south[[sp]west|east])
        """
        
        first = self.words[self.index]['word']
        if self.index + 1 < self.length:
            second = self.words[self.index+1]['word']
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
        
    def streetname(self):
        """ Parse a Street Name """
        if self.index >= self.length:
            return False
            
        self._nam, n = self.parse_streetname()
        if self._nam is not None:
            self.idx_nam = self.index
            self.index += n
            if self._debug: print("NAM", self._nam, self.idx_nam)
            return True
        return False
        
    def parse_streetname(self):
        """ Parse a Street Name """
        index = self.index
        
        name = ""
        for i in range(4):
            if index + i == self.length:
                break
            if self.words[index+i]['word'] == ',':
                break
            # Hack
            if self.words[index+i]['word'] == 'doctor':
                self.words[index+i]['word'] = 'drive'
                break
            try:
                word = sttype[self.words[index+i]['word']]
                break
            except:
                try:
                    word = vocab[self.words[index+i]['word']]
                    if Vocabulary.STREET_TYPE in word['tag']:
                        break
                    if name != '':
                        name += ' ' + word['lemma'][0]
                    else:
                        name = word['lemma'][0]
                except: 
                    if self.words[index+i]['word'][-2:] in [ 'th', 'st', 'nd', 'rd' ]:
                        name = self.words[index+i]['word'][:-2]
                    else:
                        self.index += i
                        _dir, _n = self.parse_streetdir()
                        self.index -= i
                        if _dir:
                            break
                        if name != '':
                            name += ' ' + self.words[index+i]['word']
                        else:
                            name = self.words[index+i]['word']
                    
        if i == 0 or i == 4:
            return None, 0
        else:
            return name, i
        
    def streettype(self):
        """ Parse a Street Type """
        if self.index >= self.length:
            return False
            
        self._typ, n = self.parse_streettype()
        if self._typ is not None:
            self.idx_typ = self.index
            self.index += n
            if self.index < self.length and self.words[self.index]['word'] == '.':
                self.index += 1
            if self.index < self.length and self.words[self.index]['word'] == ',':
                self.index += 1
            if self._debug: print("TYP", self._typ, self.idx_typ)
            self.isaddr = True
            return True
        return False

    def parse_streettype(self):
        """ Parse a Street Type """
        

        try:
            word = sttype[self.words[self.index]['word']]
            if Vocabulary.STREET_TYPE in word['tag']:
                itag = word['tag'].index(Vocabulary.STREET_TYPE)
                lemma = word['lemma'][itag]
                return lemma, 1
            return None, 0
        except: return None, 0
        
    def sac(self):
        """ Parse a Secondary Address Component (SAC) """
        if self.index >= self.length:
            return False
            
        self._sac, n = self.parse_sac()
        if self._sac is not None:
            self.idx_sac = self.index
            self.index += n
            if self.index < self.length and self.words[self.index]['word'] == ',':
                self.index += 1
            if self._debug: print("SAC", self._sac, self.idx_sac)
            return True
        return False
        
    def parse_sac(self):
        """ Check for Secondary Address Component
        (Apt|Ste|Rm|Fl|Dept)word
        """
        
        index  = self.index
        start  = self.index 
                
        try:
            v = sttype[self.words[index]['word']]
            if Vocabulary.SAC not in v['tag']:
                return None, 0  
            itag = v['tag'].index(Vocabulary.SAC)
            addr2 = v['lemma'][itag]
            
            index += 1
            if index == self.length:
                return None, 0
              
            # e.g., Apt #3
            if self.words[index]['word'] == '#':
                index += 1
                if index == self.length:
                    return None, 0
            
            addr2 += ' ' + self.words[index]['word']
            
            # e.g., Apt D-13
            if index + 1 < self.length and self.words[index+1]['word'] == '-':
                index += 2
                if index == self.length:
                    return None, 0
                addr2 += self.words[index]['word']
            
            return addr2, index - start + 1
            
        except:
            return None, 0
        
    def citystate(self):
        """ Parse a City and State """
        if self.index >= self.length:
            return False
            
        self._cty, self._sta, n, idx_sta = self.parse_citystate()
        if self._cty is not None:
            self.idx_cty = self.index
            self.idx_sta = idx_sta
            self.index += n
            if self.index < self.length and self.words[self.index]['word'] == ',':
                self.index += 1
            if self._debug: 
                print("CTY", self._cty, self.idx_cty) 
                print("STA", self._sta, self.idx_sta)
            self.isaddr = True
            return True
        return False
        
    def parse_citystate(self):
        """ Parse a City and State """
        
        index = self.index
        
        if self.words[index]['tag'] != Vocabulary.NAME:
            return None, None, 0, 0
            
        if self.words[index]['word'] == 'mt':
            city = "mountain"
        else:
            city = self.words[index]['word']
        start = index
            
        index += 1
        if index == self.length:
            return None, None, 0, 0
            
        if self.words[index]['word'] == ',':
            index += 1
            if index == self.length:
                return None, None, 0, 0
        elif self.words[index]['tag'] == Vocabulary.NAME: 
            # Hack
            state, n = self.state_hack(index)
            if n > 0:
                index += n
                return city, state, index - start + 1, index
                
            #if self.words[index]['word'] == 'medical doctor':
                #return city, "ISO3166-2:US-MD", index - start + 1, index
            try:
                state = self._state_dict[self.words[index]['word']]
                return city, state, index - start + 1, index
            except:
                city += ' ' + self.words[index]['word']
                index += 1
                if index == self.length:
                    return None, None, 0, 0
            
            if self.words[index]['word'] == ',':
                index += 1
                if index == self.length:
                    return None, None, 0, 0

        # Hack
        state, n = self.state_hack(index)
        if n > 0:
            index += n
            if index == self.length: index -= 1 # Hack
            return city, state, index - start + 1, index
                
        if self.words[index]['tag'] not in [Vocabulary.NAME, Vocabulary.ACRONYM]:
            return None, None, 0, 0
   
        try:
            state = self._state_dict[self.words[index]['word']]
            return city, state, index - start + 1, index
        except: 
            return None, None, 0, 0
            
    def state_hack(self, index):
        """ """
        if self.words[index]['word'] == 'medical doctor':
            return 'ISO3166-2:US-MD', 1
            
        if self.words[index]['word'] == 'd' and index + 1 < self.length and self.words[index+1]['word'] == 'c':
            return "ISO3166-2:US-DC", 1
            
        # two word special case
        if self.words[index]['word'] == 'rhode' and index + 1 < self.length and self.words[index+1]['word'] == 'island':
            return "ISO3166-2:US-RI", 1
        if self.words[index]['word'] == 'virgin' and index + 1 < self.length and self.words[index+1]['word'] == 'islands':
            return "ISO3166-2:US-VI", 1
        if self.words[index]['word'] == 'puerto' and index + 1 < self.length and self.words[index+1]['word'] == 'rico':
            return "ISO3166-2:US-PR", 1
        if self.words[index]['word'] == 'american' and index + 1 < self.length and self.words[index+1]['word'] == 'samoa':
            return "ISO3166-2:US-AS", 1
        if self.words[index]['word'] == 'marshall' and index + 1 < self.length and self.words[index+1]['word'] == 'islands':
            return "ISO3166-2:US-FM", 1
        if self.words[index]['word'] == 'northern' and index + 1 < self.length and self.words[index+1]['word'] == 'marianas':
            return "ISO3166-2:US-FM", 1
        if self.words[index]['word'] == 'british' and index + 1 < self.length and self.words[index+1]['word'] == 'columbia':
            return "ISO3166-2:CA-BC", 1
        if self.words[index]['word'] == 'newfoundland' and index + 2 < self.length and self.words[index+1]['word'] == 'and':
            return "ISO3166-2:CA-NL", 1
        if self.words[index]['word'] == 'nova' and index + 1 < self.length and self.words[index+1]['word'] == 'scotia':
            return "ISO3166-2:CA-NS", 1
        if self.words[index]['word'] == 'prince' and index + 2 < self.length and self.words[index+1]['word'] == 'edward':
            return "ISO3166-2:CA-PE", 1
        if self.words[index]['word'] in [ 'new', 'north', 'south', 'west', 'northwest']:
            index += 1
            if index == self.length:
                return None, None, 0, 0
            word = self.words[index-1]['word'] + ' ' + self.words[index]['word']
            try:
                return self._state_dict[word], 1
            except: pass
        return None, 0
        
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
        
    def postal(self):
        """ Parse a Postal Code """
        if self.index >= self.length:
            return False 
            
        if self._sta and "CA-" in self._sta:
            self._pst, n = self.parse_postalCA()
        else:
            self._pst, n = self.parse_postalUS()
            
        if self._pst is not None:
            self.idx_pst = self.index
            self.index += n
            if self._debug: print("PST", self._pst, self.idx_pst)
            return True
        return False
        
    def parse_postalUS(self):
        """ Parse a US Postal Code """
        
        index = self.index
                
        # US Postal Code
        if len(self.words[index]['word']) != 5 or not self.words[index]['word'].isdigit():
            return None, 0
        postal = self.words[index]['word']
        
        if index + 1 < self.length:
            if self.words[index+1]['word'] == '-':
                index += 2
                if index == self.length:
                    return None, 0
                if len(self.words[index]['word']) == 4 and self.words[index]['word'].isdigit():
                    postal += '-' + self.words[index]['word']
                    return postal, 3
                else:
                    return postal, 1
                    
        return postal, 1
        
    def parse_postalCA(self):
        """ Parse a Canadian Postal Code """
        
        index = self.index
                
        if len(self.words[index]['word']) != 3:
            return None, 0
        postal = self.words[index]['word']
        index += 1
        if index == self.length:
            return None, 0
                
        if len(self.words[index]['word']) != 3:
            return None, 0
        postal += self.words[index]['word']
                    
        return postal, 2
        
        
    def is_addr(self):
        if self.isaddr == False:
            return False
        return True
        
sttype = {
         'aly'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['alley']},
         'alley'        : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['alley']},
         'apt'          : { 'tag': [  Vocabulary.SAC ], 'lemma': ['apartment']},
         'apartment'    : { 'tag': [  Vocabulary.SAC ], 'lemma': ['apartment']},
         'av'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['avenue']},
         'ave'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['avenue']},
         'avenue'       : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['avenue']},
         'bvd'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['boulevard']},
         'blvd'         : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['boulevard']},
         'boulevard'    : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['boulevard']},
         'crt'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['court']},
         'ct'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['court']},
         'court'        : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['court']},
         'ctr'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['center']},
         'center'       : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['center']},
         'centre'       : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['center']},
         'dept'         : { 'tag': [  Vocabulary.SAC ], 'lemma': ['department']},
         'department'   : { 'tag': [  Vocabulary.SAC ], 'lemma': ['department']},
         'dr'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['drive']},
         'drive'        : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['drive']},
         'hwy'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['highway']},
         'highway'      : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['highway']},
         'jct'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['junction']},
         'junction'     : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['junction']},
         'ln'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['lane']},
         'lane'         : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['lane']},
         'pk'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['park']},
         'park'         : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['park']},
         'pky'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['parkway']},
         'pkwy'         : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['parkway']},
         'parkway'      : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['parkway']},
         'pl'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['place']},
         'place'        : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['place']},
         'po'           : { 'tag': [  Vocabulary.SAC ], 'lemma': ['post office']},
         'rd'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['road']},
         'road'         : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['road']},
         'rt'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['route']},
         'rte'          : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['route']},
         'route'        : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['route']},
         'st'           : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['street']},
         'street'       : { 'tag': [  Vocabulary.STREET_TYPE ], 'lemma': ['street']},
         'ste'          : { 'tag': [  Vocabulary.SAC ], 'lemma': ['suite']},
         'suite'        : { 'tag': [  Vocabulary.SAC ], 'lemma': ['suite']},
         'fl'           : { 'tag': [  Vocabulary.SAC ], 'lemma': ['floor']},
         'floor'        : { 'tag': [  Vocabulary.SAC ], 'lemma': ['floor']},
         'rm'           : { 'tag': [  Vocabulary.SAC ], 'lemma': ['room']},
         'room'         : { 'tag': [  Vocabulary.SAC ], 'lemma': ['room']},
         'bldg'         : { 'tag': [  Vocabulary.SAC ], 'lemma': ['building']},
         'building'     : { 'tag': [  Vocabulary.SAC ], 'lemma': ['building']},
         'unit'         : { 'tag': [  Vocabulary.SAC ], 'lemma': ['lane']},
}       