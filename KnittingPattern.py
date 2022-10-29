from abc import abstractclassmethod
from copy import deepcopy
from tabnanny import verbose
from unicodedata import ucd_3_2_0
from math import floor
import measurement as m
from collections import namedtuple
from PatternCalcs import PatternMeasure

class YarnWeight(Enum):
    """
    Enumerator for yarn weights
    """
    LACE=0
    SUPERFINE=1
    FINE=2
    LIGHT=3
    MEDIUM=4
    BULKY=5
    SUPERBULKY=6
    JUMBO=7

class KnitterType(Enum):
    """
    Enumerator for how closely a knitter matches usual guage
    """
    TIGHT=1
    AVERAGE=0
    LOOSE=-1

class NeedleConversion:
    """
    Convert needle sizes between mm, US, and UK-style sizes
    """
    Needle=namedtuple("Needle",["mm","us","uk"])
    def __init__(self):
        self._needles={1.25:Needle(us='0000',mm=1.25,uk=18),
        1.5:Needle(us='000',mm=1.5,uk=17),
        1.75:Needle(us='00',mm=1.75,uk=15),
        2.0: Needle(us=0,mm=2.0,uk=14),
        2.25: Needle(us=1,mm=2.25,uk=13),
        2.5: Needle(us=1.5,mm=2.5,uk=None),
        2.75: Needle(us=2,mm=2.75,uk=12),
        3.0: Needle(us=2.5,mm=3.0,uk=11),
        3.25: Needle(us=3,mm=3.25,uk=10), 
        3.5: Needle(us=4,mm=3.5,uk=None),
        3.75:Needle(us=5,mm=3.75,uk=9),
        4.0:Needle(us=6,mm=4.0,uk=8),
        4.5: Neeedle(us=7,mm=4.5,uk=8),
        5.0: Needle(us=8,mm=5.0,uk=7),
        5.5: Needle(us=9,mm=5.5,uk=5),
        6.0: Needle(us=10,mm=6.0,uk=4),
        6.5: Needle(us=10.5,mm=6.5,uk=3),
        7.0:Needle(us=None,mm=7.0,uk=2),
        7.5:Needle(us=None,mm=7.5,uk=1),
        8.0: Needle(us=11,mm=8.0,uk=0),
        9.0: Needle(us=13,mm=9.0,uk='00'),
        10.0: Needle(us=15,mm=10.0,uk='000'),
        13.0: Needle(us=17,mm=13.0,uk=None),
        15.0: Needle(us=19,mm=15.0,uk=None),
        19.0:Neelde(us=35,mm=19.0,uk=None),
        20.0:Needle(us=36,mm=2.0,uk=None),
        25.0:Needle(us=50,mm=25.0,uk=None)}

        self._us_to_mm={}
        self._uk_to_mm={}
        for k,v in self._needles.items():
            if v["us"] is not None:
                self._us_to_mm[v["us"]]=k
            if v["uk"] is not None:
                self._uk_to_mm[v['uk']]=k

    def convert_needle(self,in_size,in_units="us",out_units="uk"):
        if in_units=="us":
            mm=self._us_to_mm.get(in_size)
            if mm is None:
                raise ValueError(f"No US Needle of size {in_size}. Use in_units= if converting from mm or UK needle size.")
            if out_units=="uk":
                return self.mm_to_uk(mm)
            if out_units=="mm":
                return mm

    def mm_to_uk(self,mm):
        size=self._needles[mm]["uk"]
        if size is None:
            if mm>10.0:
                raise ValueError(f"There is no UK size needle larger than 10.0mm. Use US measurements.")
            else:
                self.get_closest_needle(mm,"uk")
        return size

    def mm_to_us(self,mm):
        size=self._needles[mm]["us"]
        if size is None:
            size=self.get_closest_needle(mm,"us")
        return size

    def get_closest_needle(self,mm,units):
        """
        When there's no needle of the required size in needed units, return the closest.
        """
        if units not in ("us","uk"):
            raise ValueError(f"We only have US or UK needle sizes available. Given: {units}")
        possible_mms=self._needles.keys()
        diff=abs(mm-possible_mms)
        test_size=self._needles[possible_mms[diff.index(0.0)]][units]
        if test_size is not None:
            return test_size
        m=min([mm for mm in diff if mm!=0])
        indicies=[i for x in enumerate(diff) if x==m]
        for i in indicies:
            size=self._needles[possible_mms[i]]
            if size is not None:
                return size
        else: 
            raise ValueError(f"No close needle of size {mm} mms in {units}.")

class Guage:
    """
    Keep track of stitches per inch/cm. Provides an interface where user can input guage naturally and system converts to needed units.  
    needle_size
    yarn_weight
    stitches_per_inch
    stitches_per_cm
    rows_per_inch
    rows_per_cm
    """
    def __init__(self,s,r,needle_size, yarn_weight,units='in',**kwargs):
        self._units=units
        self._needle_size=needle_size
        self._yarn_weight=yarn_weight
        if not isinstance(s,tuple) or not isinstance(r,tuple):
            print("Rows given as a {0}. Stitches given as a {1}".format(type(r),type(s)))
            raise TypeError(f"Stitches per {units}. Must be a tuple of the form (n_stitches,n_{units}.")
        if units=='in':
            self.stitches_per_inch=s[0]/s[1]
            self.stitches_per_cm=s[0]/(s[1]*2.54)
            self.rows_per_inch=r[0]/r[1]
            self.rows_per_cm=r[0]/(r[1]*2.54)
        elif units=='cm':
            self.stitches_per_cm=s[0]/s[1]
            self.stitches_per_inch=s[0]*2.54/s[1]            
            self.rows_per_cm=r[0]/r[1]
            self.rows_per_inch=r[0]*2.54/r[1]
        else:
            raise ValueError("Unknown units: {0}".format(units))
        
    def get(self,what,units=None):
        if units==None:
            units=self.units
        if units not in ('in','cm'):
            raise TypeError(f"Units must be 'cm' or 'in'. Units given: {units}")
        if what not in ('s','r'):
            raise TypeError(f"You asked for {what}. Can only tell you n-stitches ('s') or n_rows ('r').")
        if units=='in':
            if what=='s':
                return self.rows_per_inch
            elif what=='s':
                return self.stitches_per_inch
        elif units=='cm':
            if what=='s':
                return self.stitches_per_cm
            elif what=='r':
                return self.rows_per_cm

class StandardGuage(Guage):
    """
    Create an inherited class that has the ability to guess a guage based on needle size and yarn weight.
    """
    def __init__(self,yarn_weight,knitter=KnitterType.AVERAGE,**kwargs):
        #Standard n_stitches per 4 inches according to craft yarn council.org
        self._stitches_per_4_inches={0:range(33,40),1:range(27,32),
            2:range(23,26),3:range(21,24),4:range(16,20),5:range(12,15),
            6:range(7,11),7:range(1,6)}
        self._recommended_needle={0:range(1.5,2.25,by=0.25),
            1:range(2.25,3.25,by=0.25),
            2:range(3.25,3.75,by=0.25),
            3:range(3.75,4.5,by=0.25),
            4:range(4.5,5.5,by=0.5),
            5:range(5.5,8,by=0.5),
            6:range(8,13,by=1),
            7:range(13,25,by=1)}
        if 'needle_size' in kwargs.keys():
            needle=kwargs['needle_size']
        else:
            needle=self.guess_needle_size(yarn_weight,knitter)
        s=self.guess_guage(yarn_weight,needle)
        super().__init__((s,4),(s,4),needle,yarn_weight)

    def guess_needle_size(self,yarn_weight,knitter=KnitterType.AVERAGE):
        """
        Use US standard needle ranges to guess a recommended needle size given the yarn weight. Adjust if knitter knits tight/loose.
        """
        needle_range=self._recommended_needle.get(yarn_weight)
        if needle_range is None:
            raise ValueError(f"Yarn weight must be an integer between 0 and 7. Weight given is {yarn_weight}")
        needle_list=list(needle_range)
        if knitter==KnitterType.TIGHT:
            self._needle_size=needle_list[-1]
        elif knitter==KnitterType.LOOSE:
            needle=needle_list[0]
        else:
            needle=needle_list[len(needle_list)//2]
            print(f"Needle type guessed to be {needle} for yarn weight {yarn_weight}.")
        return needle
        
    def guess_guage(self,yarn_weight,needle_size,knitter=KnitterType.AVERAGE):
        """
        Use yarn_weight, needle_size and input knitter type to guess the number of stickingette stitches per 4 inches
        """
        needle_list=list(self._recommended_needle.get(yarn_weight))
        stitch_list=list(self._stitches_per_4_inches)
        if needle_size not in needle_list:
            raise ValueError(f"Needle size {needle_size} is not recommended for Yarn Weight {yarn_weight}. Please knit a guage swatch.")
        middle_n=len(needle_list)//2
        if len(needle_list)==1:
            n=0
        else:
            n=(needle_list.index(needle_size)-middle_n)/(len(needle_list)-1)
        #Assume we're in the middle of the standard stitch range. 
        #Move up or down depending on which needle and knitter type we have
        pos=0.5+knitter*0.25
        pos=pos+n
        if pos<=0:
            return min(stitch_list)
        elif pos>=1:
            return max(stitch_list)
        else:
            return stitch_list[floor(pos*(len(stitch_list)-1))]            

class KnittingDistance(m.MeasureBase):
    """
    A units-aware class that includes stitches per inch and rows per inch. 
    """
    STANDARD_UNIT='cm'
    UNITS={'cm':1.0,'in':2.54,'yd':91.44,'m':1000.0}
    ALIAS={'inch':'in','centimeters':'cm','yard':'yd','meter':'m','s':'stitch','r':'row'}

    def __init__(self,guage,*args,**kwargs):
        """
        Read in guage numbers that the user provides. Turn the numbers into something we can use to calculate.  
        """
        super.__init__(*args,**kwargs)
        if 'stitches_per_inch' in kwargs:
            self.UNITS['s']=2.54*kwargs['stitches_per_inch']
        elif 'stitches_per_cm' in kwargs:
            self.UNITS['s']=kwargs['stitches_per_cm']
        if 'rows_per_inch' in kwargs:
            self.UNITS['r']=2.54*kwargs['rows_per_inch']
        if 'rows_per_cm' in kwargs:
            self.UNITS['r']=kwargs['rows']
        
class PhysicalMeasure(PatternMeasure):
    """
    A class for the Physical Mea
    """
    def __init__(self,all_measures,measure_dict,units='in'):
        super().__init__()

class KnittingPattern:
    """
    Abstract class for all Knitting Patterns. 
    Members
    _finished_measure: A PhysicalMeasure in inches or centimeters for the finished product
    _sections: An ordered list of PatternSections.
    Methods
    """

    def __init__(self):