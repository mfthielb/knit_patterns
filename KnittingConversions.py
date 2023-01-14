from abc import abstractclassmethod
from enum import IntEnum,Enum
from copy import deepcopy
from tabnanny import verbose
from unicodedata import ucd_3_2_0
from math import floor
from measurement.base import MeasureBase
from collections import namedtuple

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

Needle=namedtuple("Needle",["mm","us","uk"])

class NeedleConversion:
    """
    Convert needle sizes between mm, US, and UK-style sizes
    Members: 
    Needle: namedtuple of needles with all needle measurements
    _needles: A dictionary of needle conversions indexed by size in mm. Has US and UK sizes  
    _us_to_mm: Dictionary converting US needle sizes to size in mm
    _uk_to_mm: Dictionary converting UK needle sizes to size in mm
    """
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
        4.5: Needle(us=7,mm=4.5,uk=8),
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
        19.0: Needle(us=35,mm=19.0,uk=None),
        20.0:Needle(us=36,mm=2.0,uk=None),
        25.0:Needle(us=50,mm=25.0,uk=None)}

        self._us_to_mm={}
        self._uk_to_mm={}
        for k,v in self._needles.items():
            if v.us is not None:
                self._us_to_mm[v.us]=k
            if v.uk is not None:
                self._uk_to_mm[v.uk]=k

    def convert_needle(self,in_size,in_units="us",out_units="uk"):
        if in_units=="us":
            mm=self._us_to_mm.get(in_size)
        elif in_units=="uk":
            mm=self._uk_to_mm.get(in_size)
        elif in_units=="mm":
            mm=in_size
        if mm is None:
            raise ValueError(f"No Needle of size {in_size} in {in_units} units. Use in_units= if converting from mm or UK needle size.")
        if out_units=="uk":
            return self.mm_to_uk(mm)
        if out_units=="us":
            return self.mm_to_us(mm)
        if out_units=="mm":
            return mm

    def mm_to_uk(self,mm):
        size=self._needles[mm].uk
        if size is None:
            if mm>10.0:
                raise ValueError(f"There is no UK size needle larger than 10.0mm. Use US measurements.")
            else:
                self.get_closest_needle(mm,"uk")
        return size

    def mm_to_us(self,mm):
        size=self._needles[mm].us
        if size is None:
            size=self.get_closest_needle(mm,"us")
        return size

    def get_closest_needle(self,mm,units):
        """
        When there's no needle of the required size in needed units, return the closest.
        """
        if units not in ("us","uk"):
            raise ValueError(f"We only have US or UK needle sizes available. Given: {units}")
        size=self._needles.get(mm).__getattribute__(units)
        if size is not None:
            return size
        possible_mms=self._needles.keys()
        diff=[abs(mm-x) for x in possible_mms]
        smallest_diff=min([d for d in diff if d>0])
        i=diff.index(smallest_diff)
        size=self._needles[possible_mms[i]].__getattribute__(units)
        if size is not None:
            return size
        raise ValueError(f"No close needle of size {mm} mms in {units}.")
    
class Guage(namedtuple('Guage',['s_per_unit','r_per_unit','units'])):
    """
    An object to keep track of knitters guage and calculate stitches/rows for a given units input.
    """
    __slots__=()
    def stitches(self,v):
        """
        Guage is set as x stitches per y units.
        """
        return self.s_per_unit[0]/self.s_per_unit[1]*v

    def rows(self,v):
        """
        Guage is often set as x rows per y units.
        """
        return self.r_per_unit[0]/self.r_per_unit[1]*v
        
    def units_to_rows(self,v):
        """
        Given inches or cm, return number of rows
        """
        return self.r_per_unit[1]/self.r_per_unit[0]*v
        
    def units_to_stitches(self,v):
        """
        Given inches or cm, return number of stitches
        """
        return self.s_per_unit[1]/self.s_per_unit[0]*v

    def __str__(self):
        return "Guage is: {0}, stitches per {2} and {1} rows per {2}.".format(self.s_per_unit.__str__(),self.r_per_unit.__str__(),self.units)
    def __repr__(self):
        return "Guage(s_per_unit={0},r_per_unit={1},units={2})".format(self.s_per_unit.__repr__(),self.r_per_unit.__repr__(),self.units)

class StandardGuage():
    """
    Class that knows standard guages for yarn weights and needle sizes.
    Has the ability to guess stockingette guage given yarn weight and either needle size or knitter type (0,1)
    """
    #stitches per 4 inches for various yarn weights
    _stitches_per_4_inches={0:range(33,40),1:range(27,32),
    2:range(23,26),3:range(21,24),4:range(16,20),5:range(12,15),
    6:range(7,11),7:range(1,6)}
    _recommended_needle={0:[1.5,1.75,2.00,2.25],
        1:[2.25,2.5,3.0,3.25],
        2:[3.0,3.25,3.5,3.75],
        3:[3.75,4.0,4.25,4.5],
        4:[4.5,5.0,5.5],
        5:[5.5,6.0,6.5,7.0,7.5],
        6:[8,9,10,11,12,13],
        7:[13,14,15,16,17,18,19,20,21,22,23,24,25]}

    def _guess_needle_size(self,yarn_weight,knitter=0.5):
        """
        Use US standard needle ranges to guess a recommended needle size given the yarn weight. Adjust if knitter knits tight/loose.
        """
        needle_range=self._recommended_needle.get(yarn_weight)
        if needle_range is None:
            raise ValueError(f"Yarn weight must be an integer between 0 and 7. Weight given is {yarn_weight}")
        needle_list=list(needle_range)
        needle_size=needle_list[floor(len(needle_list)*knitter)]
        return needle_size
        
    def _guess_s_per_4(self,yarn_weight,needle_size,knitter):
        """
        Use yarn_weight, needle_size and input knitter type to guess the number of stickingette stitches per 4 inches
        Arguments:
        yarn_weight: integer 0-7
        needle_size: Needle size (must be in mms), use NeedleConversion if you have a us or uk size
        """
        needle_list=list(self._recommended_needle.get(yarn_weight))
        stitch_list=list(self._stitches_per_4_inches.get(yarn_weight))
        if stitch_list is None or needle_list is None:
            raise ValueError("Yarn weight must be a number 0-7")
        #If needle size isn't given, guess based on whether the knitter 
        #recommended needle size is a range:"tight" (close to 1) knitters are recommended larger needles. 
        # "loose" knitters get smaller ones.
        if needle_size is None:
            needle_size=self._guess_needle_size(yarn_weight,knitter=knitter)
        elif needle_size not in needle_list:
            raise Warning(f"Needle size {needle_size}mm is not recommended for Yarn Weight {yarn_weight}. Please knit a guage swatch.")
        #Assume we're in the middle of the standard stitch range. 
        #Move up or down depending on which needle and knitter type we have
        needle_pos=needle_list.index(needle_size)/len(needle_list)
        s_pos=((knitter+(1-needle_pos))/2)
        if s_pos<=0:
            return min(stitch_list)
        elif s_pos>=1:
            return max(stitch_list)
        else:
             return stitch_list[floor(s_pos*len(stitch_list))]
    
    def guess_guage(self,yarn_weight,units='in',needle_size=None,knitter=0.5):
        s_per_4_inch=self._guess_s_per_4(yarn_weight,needle_size,knitter)
        if units=='in':
            return Guage((s_per_4_inch,4),(s_per_4_inch,4),units='in')
        elif units=='cm':
            return Guage((s_per_4_inch,4),(s_per_4_inch,4),units='cm')
        else:
            raise ValueError(f"Please measure in cm or in, units given was:{units}.") 
        
    def __str__(self):
        return "Class to recommend needle and guess guage given yarn weight."  
                  
def main():
    print("Demonstrations of Knitting Conversion Classes")
    print("Almost every knitting pattern needs a guage. If this is a garment (like a sweater or sock), you should knit a swatch.")
    g=Guage((33,4),(33,4),units='in')
    print("This is a standard lace weight guage with a US size 1 (2.25mm) needle:")
    print(g.__str__())
    print("We keep the decimal places and round where needed for the pattern instructions. This keeps measurements precise.")
    print("\n If you don't feel like knitting a swatch, we will use standard guagers if you tell us the yarn weight and needle size.")
    g2=StandardGuage()
    print(g2.guess_guage(0,knitter=0.5).__str__())

if __name__=="__main__":
    main()
