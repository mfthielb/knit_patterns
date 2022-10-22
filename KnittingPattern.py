from abc import abstractclassmethod
from copy import deepcopy
import measurement as m
from PatternCalcs import PatternMeasure

class Stitch(m.MeasureBase):
    """
    Stitches are a unit of measure. We can also convert to 
    """

class Row(m.MeasureBase):

class StitchesPerLength(m.BidirectionaMeasure):
    PRIMARY_DIMENSION=stitches

class BodyMeasure(PatternMeasure):
    def __init__(self,all_measures,measure_dict,units='in'):
        super().__init__(None,)

class KnittingPattern:
    """
    Abstract class for all Knitting Patterns. 
    Members
    finished_measure: A PatternMeasure in inches or centimeters for the finished product
    sections: An ordered list of PatternSections.
    Methods
    """

    def __init__(self):