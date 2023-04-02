from abc import abstractclassmethod
from typing import NamedTuple
from src.conversions import *
"""
Basic classes for PatternMeasure's and PatternSections
"""
class PatternMeasure:
    """
    A base class for classes that can calculate some measurements from others.
    This allows us to abstract out the checks for whether we have the right measurements for a calculation.
    Class attributes
     _vital_measures: a set of strings that have labels for must-have measurements. If any of these are missing, the object does not have enough information to be created.
     _all_measures: a set of strings that is the complete set of measurements needed for the pattern section including vital measures and measures that can be calculated.
     _measure_values: a dictionary of measurements with strings as keys and integers as values. Measurements may be in rows, stritches, inches or centimeters.
    """
    def __init__(self,vital_measures,all_measures,measures_dict,*args,label="",**kwargs):
        """
        Fill _measure_values dictionary and make sure we have all the measurements the user told us we needed.
        """
        if all_measures is not None:
            self.all_measures(set(all_measures+vital_measures))
        else:
            self._all_measures=set()
        self._measure_values={}
        if measures_dict is not None:
            for k,v in measures_dict.items():
                self.measure_values(k,v)
        if vital_measures is not None:
            self.vital_measures(vital_measures)
            self.edit_measures(va=self.vital_measures())
        else:
            self.vital_measures(set())
        self.label(label)
        self.check_myself()

    def check_myself(self):
        if not self.have_what_i_need(self.vital_measures()):
            raise Warning("Measure initialized without all vital measures set. Missing: {0}".format(self.vital_measures()-self.what_do_i_have()))
        if self.vital_measures()==set() and self.what_do_i_have()==set():
            raise Warning("Empty pattern measure. No vital measures set and measure dictionary empty.")

    def label(self,v=None):
        """
        Get or Set measure label.
        """
        if v is not None:
            if not isinstance(v,str):
                raise TypeError("Label must be a str. Value entered was a {0}.".format(type(v)))
            else:
                self._label=v
        return self._label

    def edit_measures(self,va=set(),vrm=set()):
        """
        Add/remove a single string or an iterable that can be made into a set to/from _all_measures
        """
        if isinstance(va,str):
            self.all_measures(self.all_measures().add(va))
        else:
            for i in va:
                if not isinstance(i,str):
                    raise TypeError(f"Value {i} is not a string. Cannot be a measure name.")
                self.all_measures(self.all_measures().add(i))
        if isinstance(vrm,str):
            self.all_measures(self.all_measures().remove(vrm))
        else:
            for i in vrm:
                if not isinstance(i,str):
                    raise TypeError(f"Value {i} is not a string. Cannot be a measure name.")
                self.all_measures(self.all_measures().remove(i))
    
    def vital_measures(self,v=None):
        if v is not None:
            if isinstance(v,str):
                self._vital_measures=set([v])
            else:
                self._vital_measures=set(v)
            if not self.have_what_i_need(self.what_do_i_have()):
                raise Warning("Vital measures has been edited, but measures are missing. Need to add: {}".format(self.vital_measures()-self.what_do_i_have()))
        return self._vital_measures
    
    def all_measures(self,v=None):
        """
        Setter and getter for all_measures 
        """
        if v is not None:
            if isinstance(v,str):
                self._all_measures=set([v])
            else:
                self._all_measures=set(v)
        return self._all_measures

    def measure_values(self,key,value=None):
        """
        Setter and getter for _measurements dictionary values
        key (str): label of value you are setting
        value (int): value
        """
        if not isinstance(key,str):
            raise ValueError("Measure labels must be strings.")
        if value is not None:
            self._measure_values[key]=value
            self.edit_measures(va=key)
        if key in self._measure_values.keys():
            return self._measure_values.get(key)
        else:
            raise ValueError(f"Key {key} not in measure_values dictionary")

    def have_what_i_need(self,values_i_need,values_i_have=None):
        """
        Check measure dictionary for a set of values and return True if all are in the dictionary. 
        Return False otherwise
        """
        if values_i_have is None:
            values_i_have=self.what_do_i_have()
        elif values_i_need==set():
            return True
        if values_i_need is None:
            values_i_need=self.vital_measures()
        return all([k in values_i_have for k in values_i_need])

    def what_do_i_have(self):
        """
        Get a list of strings for measurements that are entered in _measure_values
        """
        return set(self._measure_values.keys())
    
class IncOrDecPatternMeasure(PatternMeasure):
    """
    This class is a pattern measure for a constant increases/decrease over a set number of rows (increase_x_by_y)
    Attributes: 
    _measure_values: dictionary
    _vital_measures: ["start_stitches"] (constant)
    _all_measures: ["start_stitches","end_stitches","increase_x_every_y","n_rows"]
    """
    def __init__(self,measures_dict):
        """
        We must have 3 of the 4 
        """
        super().__init__(["start_stitches"],["increase_x_every_y","end_stitches","n_rows"],measures_dict)
        self.fill_in_missing_measures()

    def _calc_n_rows(self):
        """
        If we have min and max stitches and it's straight-up increase/decrease, calc number of rows
        """
        #TODO: Make sure there's no remainer when we divide
        need_list=set(["start_stitches","end_stitches","increase_x_every_y"])
        if not self.have_what_i_need(need_list):
            raise ValueError("Trying to calculate number of rows in increase but missing: {0}".format(need_list-self.what_do_i_have()))
        increase_rate=self.measure_values("increase_x_every_y")
        increase_per_row=increase_rate[0]/increase_rate[1]
        n_to_increase=self.measure_values("end_stitches")-self.measure_values("start_stitches")
        self.measure_values("n_rows",n_to_increase/increase_per_row)
        
    def _calc_end_stitches(self):
        """"
        If we have increases/decreases but not the number we need at the end, calculate end_stitches (number of stitches per row at end of section"
        """
        need_list=["increase_x_every_y","n_rows","start_stitches"]
        if not self.have_what_i_need(need_list):
            #raise a value error and return
            raise ValueError("Trying to calculate number of stitches at the end but missing: {0}".format(need_list-self.what_do_i_have()))
        increase_rate=self.measure_values("increase_x_every_y")
        increase_per_row=increase_rate[0]/increase_rate[1]
        start=self.measure_values("start_stitches")
        n_rows=self.measure_values("n_rows")
        self.measure_values("end_stitches",start+increase_per_row*n_rows)

    def _calc_increase_rate(self):
        """
        If we only know how many start_stitches,end_stitches and n_rows, then calculate increase_x_every_y
        """
        need_list=["start_stitches","end_stitches","n_rows"]
        if not self.have_what_i_need(need_list):
            raise ValueError("Cannot calculate increase rate. Missing:{0}.".format(need_list-self.what_do_i_have()))
        x=(self.end_stitches()-self.start_stitches())/self.n_rows()
        self.increase_x_every_y((x,1))
            
    def start_stitches(self,v=None):
        """
        Convenience function to set and get start_stitches
        """
        if v is not None:
            self.measure_values("start_stitches",v)
        return self.measure_values("start_stitches")

    def end_stitches(self,v=None):
        """
        Convenience function to set and get end_stitches
        """
        if v is not None:
            self.measure_values("end_stitches",v)
        return self.measure_values("end_stitches")
    
    def increase_x_every_y(self,v=None):
        """
        Convenience function to set and get increase_x_every_y
        """
        if v is not None:
            self.measure_values("increase_x_every_y",v)
        return self.measure_values("increase_x_every_y")

    def n_rows(self,v=None):
        """
        Convenience function to set and get n_rows
        """
        if v is not None:
            self.measure_values("n_rows",v)
        return self.measure_values("n_rows")
        
    def fill_in_missing_measures(self):
        """
        Decide if the list is complete and if not, calculate what we're missing
        """
        values_i_have=self.what_do_i_have()
        if (sum(k in values_i_have for k in {"increase_x_every_y","end_stitches","n_rows"})<2):
            raise ValueError("Need two of these three: {0}\n I have: {1}".format(["increase_x_every_y","end_stitches","n_rows"],values_i_have))
        if "n_rows" not in values_i_have:
            self._calc_n_rows()
        if "end_stitches" not in values_i_have:
            self._calc_end_stitches()
        if "increase_x_every_y" not in values_i_have:
            self._calc_increase_rate()

class PatternSection:
    """
    A class to write and store the directions for a section of a pattern. 
    Attributes: 
    _label (str) Label used when writing pattern directions
    _measurements (PatternMeasure): object that holds measurements for section
    _directions (list): Directions for the pattern section in proper order. 
    """

    def __init__(self,measures_dict,*args,label="",**kwargs):
        """
        Initialize PatternMeasure and set label for Pattern Section
        measures_dict (dict str:int): A dictionary holding input measurements
        """
        self._directions=[]
        self._label=label
        self.make_measure(measures_dict)

    def label(self,text=None):
        "Set or get the label for this section"
        if text is not None:
            self._label=str(text)
        return self._label

    @abstractclassmethod
    def how_to_end(self):
        """
        Sections may have a cast-on or an attach instruction instead of a start for the beginning, but they all need an ending. 
        """
        pass

    @abstractclassmethod
    def make_measure(self,measures_dict):
        """
        A pattern section requires a measure object. This method creates that object.
        """
        pass

    @abstractclassmethod
    def write_directions(self):
        """
        How to fill the directions list
        """
        pass
    
    @abstractclassmethod
    def end_stitches(self):
        """
        Calculate how many stitches you have at the end and return.
        """
    def print_directions(self):
        """
        Basic print method to print all directions in _directions (a list)
        """
        for d in self._directions:
            print(d)

class IncOrDecPatternSection(PatternSection):
    """
    Generic class method of an increasing or decreasing PatternSection
    """
    def __init__(self,measures_dict,label=""):
        super().__init__(measures_dict,label=label)

    def start_stitches(self):
        return self._measurements.measure_values("start_stitches")

    def end_stitches(self):
        return self._measurements.measure_values("end_stitches")

    def n_rows(self):
        return self._measurements.measure_values("n_rows")    

    def __str__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        l=self.label()
        return f"{l} for magic loop toe-up {start} stitches inc to {end} stitches."