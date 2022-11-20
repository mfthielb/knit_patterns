from abc import abstractclassmethod
from measurement.measures import Distance
from containers import namedtuple
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
            self.all_measures(all_measures)
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
            return self._measure_values[key]
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

    def print_directions(self):
        """
        Basic print method to print all directions in _directions (a list)
        """
        for d in self._directions:
            print(d)

class ToeUpToeML(PatternSection):
    """
    A Toe section for a basic toe-up sock using magic loop
    """
    def __init__(self,measures_dict,label=""):
        super().__init__(measures_dict,label=label)
        if len(self.label())==0:
            self.label("Toe")
    
    #TODO: We know increase_x_every_y for a toe, so check the input dictionary
    #Add increase_x_every_y=(4,2) and make sure you're adding a multiple of 4
    def make_measure(self,measures_dict):
        """
        Toes are usually increase 4 every 2 rows. Use defaults if missiing some measures. start_stitches to end_stitches. 
        """
        start_stitches=measures_dict.get("start_stitches")
        if start_stitches is None:
            raise ValueError("Toe measures dict has only: {0}. Need start_stitches to calculate toe.".format(measures_dict.keys()))
        inc=measures_dict.get("increase_x_every_y")
        if inc is None:
            if (measures_dict["start_stitches"]-measures_dict["end_stitches"])%4==0:
                measures_dict["increase_x_every_y"]=(4,2)
        self._measurements=IncOrDecPatternMeasure(measures_dict)

    def how_to_cast_on(self):
        """
        Instructions for starting. This is a toe-up sock, so the toe starts with cast-on instructions.
        """
        n_start=self._measurements.start_stitches()
        if n_start%2:
            raise Warning("Starting stitches is an odd number. Adding 1 stitch.")
        half_of_n_start=int(round(n_start/2))
        return f"Cast on {n_start} ({half_of_n_start} per needle) in preferred style (Figure 8, crocet, etc).\nKnit all stitches around."
    
    def how_to_end(self):
        """
        Instructions for the end with number of stitches you should have.
        """
        n_end=self._measurements.end_stitches()
        per_needle=n_end/2
        return f"Repeat Row 1 and Row 2 until there are {n_end} stitches total on your two needles ({per_needle} on each needle).\n"

    def pattern_repeat(self):
        return f"Row 1: Needle 1: K1 M1R, K to last stitch, M1L K1.\n   Needle 2:K1 M1R, K to last stitch, M1L K1.\nRow 2: Knit all stitches around.\n"

    def write_directions(self):
        """
        Add lines to directions list.
        """
        self._directions.append(self.how_to_cast_on())
        self._directions.append(self.pattern_repeat())
        self._directions.append(self.how_to_end())
        self._directions.append("You will have knitted {0} rows.".format(self._measurements.n_rows()))
    
    def __str__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"Toe for magic loop toe-up {start} stitches inc to {end} stitches."
    
    def __repr__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"ToeUpToeML({{'start_stitches':{start},'end_stitches':{end},'increase_x_every_y':(4,2)}})."

class InstepML(PatternSection):
    """
    Directions for the instep of a sock. Toe up or cuff down, the directions are the same
    """
    def __init__(self,measures_dict):
        super().__init__(measures_dict)
        if len(self.label())==0:
            self.label("Instep")

    def make_measure(self,measures_dict):
        """
        Use an IncOrDecPatternMeasure with a 0 increase.
        """
        #TODO: Check the input measures_dict and make sure we have the right numbers
        self._measurements=IncOrDecPatternMeasure(measures_dict)

    def how_to_end(self):
        """
        Instep is just knitting around.
        """
        n_rows=self._measurements.n_rows()
        return f"Knit all stitches around for {n_rows} rows."
    
    def write_directions(self):
        """
        Gusset is just one line of directions.
        """
        self._directions.append(self.how_to_end())
    
    def __str__(self):
        start=self._measurements.start_stitches()
        rows=self._measurements.n_rows()
        return f"Generic instep for foot that is {start} stitches around and {rows} rows long."
    
    def __repr__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.n_rows()
        return f"InstepML({{'start_stitches':{start},'n_rows':{end},'increase_x_every_y':(0,1)}})."
    
class ToeUpGuessetML(PatternSection):
    """
    A basic guesset section for a toe-up sock using magic loop
    Attributes: 
    _measurements: An IncOrDecPatternMeasure with a positive increase
    _directions: written directions
    """
    def __init__(self,measures_dict):
        super().__init__(measures_dict)
        if len(self.label())==0:
            self.label("Gusset")
        self.make_measure(measures_dict)

    def make_measure(self,measures_dict):
        """
        A guesset is an increase, but you only increase on a single needle.
        vital_measures: not used
        all_measures: not used
        measures_dict: dictionary with start_stitches, end_stitches and either n_rows or increase_x_every_y
        """
        #TODO: Check Measures dictionary
        self._measurements=IncOrDecPatternMeasure(measures_dict)

    def pattern_repeat(self):
        """
        Increase at either side of Needle 2 every other row.
        """
        return f"Row 1: Needle 1: Knit all stitches across. Needle 2: K1, M1R, Knit across to last stitche. M1L K1.\nRow 2: Knit all stitches around.\n"

    def how_to_end(self):
        """
        Calculate how many stitches are on each needle by end and return line of pattern.
        """
        end_stitches=self._measurements.end_stitches()
        start_stiches=self._measurements.start_stitches()
        n_per_needle_begin=start_stiches/2
        n_needle_2_end=end_stitches-n_per_needle_begin
        return f"Repeat Rows 1 and 2 until there are {n_per_needle_begin} stitches on Needle 1 and {n_needle_2_end} stitches on Needle 2."

    def write_directions(self):
        """
        Add all pattern lines to _directions.
        """
        self._directions.append(self.pattern_repeat())
        self._directions.append(self.how_to_end())
    
    def __str__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"Gusset for magic loop toe-up {start} stitches inc to {end} stitches."
    
    def __repr__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"ToeUpGussetML({{'start_stitches':{start},'end_stitches':{end},'increase_x_every_y':(1,1)}})."

class HeelTurnML(PatternSection):
    """
    Heel turn with magic loop.
    """
    def __init__(self,measures_dict,label="",*args,**kwargs):
        measures_for_initial=measures_dict
        if "increase_x_every_y" not in measures_dict.keys():
            new_measures=measures_dict.copy()
            new_measures["increase_x_every_y"]=(-1,1)
            super().__init__(new_measures)
        else:
            super().__init__(new_measures)
        if len(self.label())==0:
            self.label("Heel Turn")
        self.fill_in_missing_measures()

    def make_measure(self,measures_dict):
        self._measurements=IncOrDecPatternMeasure(measures_dict)

    def _calc_first_turn(self):
        if not self._measurements.have_what_i_need(["start_stitches"]):
            raise ValueError("start_stitches not in measures dictionary.")
        self._measurements.measure_values("first_turn",self._measurements.measure_values("start_stitches")-1)
    
    def _calc_second_turn(self):
        """
        Heels don't vary that much. The second turn is always 7
        """
        self._measurements.measure_values("second_turn",7)

    def fill_in_missing_measures(self):
        """
        A heel turn is an IncOrDecMeasure
        """
        values_i_have=self._measurements.what_do_i_have()
        if "first_turn" not in values_i_have:
            self._calc_first_turn()
        if "second_turn" not in values_i_have:
            self._calc_second_turn()
    
    def write_directions(self):
        self._directions.append("Knit across needle 1. Leave all top-of-foot stitches on the cable and work back and forth on the gusset stitches as follows:\n")
        row=1
        self._directions.append("Row {0}: Knit {1} ssk k1,turn.".format(row,self._measurements.measure_values("end_stitches")-1))
        start=self._measurements.measure_values("second_turn")
        for i in range(1,11):
            row=row+1
            if row%2==0:
                self._directions.append("Row {0}: S1, p{1}, p2tog, p1, turn.".format(row,start+i-1))
            else:
                self._directions.append("Row {0}: S1, k{1}, ssk, k1, turn.".format(row,start+i-1))

        self._directions.append("Continue until there are {0} stitches on the working needle.\n".format(self._measurements.end_stitches()))
        self._directions.append("Knit 1 row around.\n")
    
    def __str__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"Heel turn for magic loop toe-up {start} stitches inc to {end} stitches."
    
    def __repr__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"HeelTurnML({{'start_stitches':{start},'end_stitches':{end},'increase_x_every_y':(-1,1)}})."

class BasicCuff(PatternSection):
    def __init__(self,measures_dict):
        super().__init__(measures_dict,label="",)
        if len(self.label())==0:
            self.label("Cuff")
    
    def make_measure(self,measures_dict):
        self._measurements=PatternMeasure(["start_stitches","n_rows"],[],measures_dict)
    
    def write_directions(self):
        self._directions.append("Row 1: K1, P1 for all {0} around".format(self._measurements.measure_values("start_stitches")))
        self._directions.append("Repeat Row 1 for {0} rows.".format(self._measurements.measure_values("n_rows")))
        self._directions.append("Bind off LOOSELY (or you won't be able to get the sock onto your foot).")
    
    def __str__(self):
        return "Cuff {0} stitches for {1} rows".format(self._measurements.start_stitches(),self._measurements.n_rows())
    
    def __repr__(self):
        return "Cuff({'start_stitches':{0},'end_stitches':{0},n_rows: {1})".format(self._measurements.start_stitches(),self._measurements.n_rows())
    
    def __str__(self):
        start=self._measurements.measure_values("start_stitches")
        rows=self._measurements.measure_values("n_rows")
        return f"Generic cuff for sock that is {start} stitches around and {rows} long."
    
    def __repr__(self):
        start=self._measurements.measure_values("start_stitches")
        rows=self._measurements.measure_values("n_rows")
        return f"BasicCuff({{'start_stitches':{start},'n_rows':{rows},'increase_x_every_y':(0,1)}})."

class FootMeasure(PatternMeasure):
    """
    A measurement class to hold physical measurements for a foot.
    Members
    units: 'in' or 'cm' ('in' by default)
    ease_adjusted: Socks have 10% or 1-1.5 inches negative ease. bool for whether foot measurements have been ease adjusted. 
    """
    def __init__(self,measure_dict,units='in',ease=False):
        super().__init__(["around_foot","toe_to_heel"],None,measure_dict)
        if units in ['cm', 'in']:
            self.units=units
        else:
            #TODO; Implement the ability to guess inches or cm based on measurements
            raise Warning(f"Invalid units for foot measure, valid units are 'in' or 'cm'. Units given are {units}.")
        #TODO: Implement the ability to guess sock size based on shoe size and shoe size based on sock size
        self.calc_ease()
        if not self.have_what_i_need():
            raise Warning("Foot measure initialized without all needed measurements. Need: {0}. Initialized with: {1}").format(self.what_do_i_have(),self.what_do_i_need())
    
    def calc_ease(self):
        if self.ease_adjust:
            print("Measurements already ease adjusted: "+self.__str__())
            return
        self.measure_value("around_foot",self.measure_value("around_foot")*0.9)
        self.ease_adjusted=True
    
    def __str__(self):
        return "Measure for a foot that is {0} {2} around and {0} {2} long.".format(self.measure_values("around_foot"),self.measure_values("toe_to_heel"),self.units)

    def __repr__(self):
        return "FootMeasure(\{'around_foot'={0},'toe_to_heel'={1}\},units={2},ease={3})".format(self.measure_values("around_foot"),self.measure_values("toe_to_heel"),self.units,self.ease_adjusted)

class Guage(namedtuple('Guage',['s_per_unit','r_per_unit','units'])):
    __slots__=()
    def stitches(self,v):
        """
        Guage is often set as x stitches per y units. Check to see if we have a tuple or not.
        """
        if isinstance(self.s_per_unit,tuple):
            return self.s_per_unit[0]/self.s_per_unit[1]*v
        else:
            return self.s_per_unit*v
    def rows(self,v):
        """
        Guage is often set as x rows per y units. Check to see if we have a tuple or not.
        """
        if isinstance(self.r_per_unit,tuple):
            return self.r_per_unit[0]/self.r_per_unit[1]*v
        else:
            return self.r_per_unit*v

    def units_to_rows(self,v,units=None):
        if isinstance(self.s_per_unit,tuple):
            return self.r_per_unit[1]/self.r_per_unit[0]*v
        else:
            return v/self.r_per_unit

    def units_to_stitches(self,v):
        if isinstance(self.s_per_unit,tuple):
            return self.s_per_unit[1]/self.s_per_unit[0]*v
        else:
            return v/self.s_per_unit
    def __str__():
        return "Guage is: {0}, stitches per {2} and {1} rows per {2}.".format(self.s_per_unit,self.r_per_unit,self.units)
    def __repr__():
        return "Guage(s_per_unit={0},r_per_unit={1},units={2})".format(self.s_per_unit,self.r_per_unit,self.units)

class ToeUpSockPattern():
    """
    Basic toe up sock pattern class.
    Members
    guage: Guage object holding stitches/unit and rows/unit and units of pattern
    foot_measurements: FootMeasure object with foot measurements
    pattern_sections: list object of PatternSections
    Methods
    stitches_around_foot: number of stitches around the foot
    stitches_toe_to_heel: number of stitches from toe to heel
    heel_type
    """
    def __init__(self,foot_measure_dict,guage,**kwargs):
        self.guage=guage
        self.foot_measurements=FootMeasure(foot_measure_dict,units=guage.units,**kwargs)
        self.foot_measurements.calc_ease()
    
    def stitches_around_foot(self):
        """
        Number of stitches to go around foot. Always a multiple of 4, so round as needed.
        """
        return self.guage.stitches(self.foot_measurements.measure_values("around_foot"))
    def rows_toe_to_heel(self):
        return self.guage.rows(self.foot_measurements.measure_values("toe_to_heel"))

    def calculate_pattern(self):
        #sock pattern goes here
        toe=ToeUpToeML({"start_stitches":round(self.stitches_around_foot()/2), "end_stitches":self.stitches_around_foot()})
        
        #Gusset heels start 2 inches from back of foot.
        if self.guage.units=='in':
            heel_rows=self.guage.units_to_rows(2)
        else:
            heel_rows=self.guage.units_to_rows(2.54*2)

        instep_rows=self.rows_toe_to_heel()-toe.n_rows()-heel_rows
        instep=InstepML({"start_stitches":self.stitches_around_foot(),"end_stitches":self.stitches_around_foot(),"n_rows":instep_rows})
        gusset_increase=round(instep.measure_values("end_stitches")*0.25)
        gusset=ToeUpGuessetML({"start_stitches":instep.measure_values("end_stitches"),"end_stitches":instep.measure_values("end_stitches")+guesset_increase})
        heel_turn_start=gusset_increase+round(instep.measure_values("end_stitches")/2)
        heel_turn_end=round(self.stitches_around_foot()/2)
        heel_turn=HeelTurnML({"start_stitches":heel_turn_start,"end_stitches":(heel_turn_end)})
        cuff=BasicCuff({"start_stitches":self.stitches_around_foot()})
        return [toe,instep,gusset,heel_turn,cuff]

def main():
    print("Basic Sock Elements")
    #In the finished product, there would be a SockCalculator that takes in the 
    #measurements for the foot (in inches or cm) and calculates the stitches for each of these calls
    toe=ToeUpToeML({"start_stitches":32,"end_stitches":64,"increase_x_every_y":(4,2)})
    instep=InstepML({"start_stitches":64,"end_stitches":64,"n_rows":24})
    gusset=ToeUpGuessetML({"start_stitches":64,"end_stitches":88,"increase_x_every_y":(2,2)})
    turn=HeelTurnML({"start_stitches":56,"end_stitches":32})
    cuff=BasicCuff({"start_stitches":64,"n_rows":12})

    #Each object makes its calculations on create. 
    #pattern_list=sock(64, 88,x,y,z)#
    # #Print directions to screen
    pattern_list=[toe,instep,gusset,turn,cuff]
    print("\n----Pattern Directions------")
    for s in pattern_list:
    #A PatternSection only writes its directions when prompted
        s.write_directions()
        print("\n"+s.label())
        s.print_directions()
    
if __name__=="__main__": main()