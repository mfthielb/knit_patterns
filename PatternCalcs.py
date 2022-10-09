from abc import abstractclassmethod

class PatternMeasure:
    """
    A base class for classes that can calculate some measurements from others.
    This allows us to abstract out the checks for whether we have the right measurements for a calculation.
    Class attributes
     _vital_measures: a set of strings that have labels for must-have measurements. If any of these are missing, the object does not have enough information to be created.
     _all_measures: a set of strings that is the complete set of measurements needed for the pattern section including vital measures and measures that can be calculated.
     _measure_values: a dictionary of measurements with strings as keys and integers as values. Measurements may be in rows, stritches, inches or centimeters.
    """
    def __init__(self,vital_measures,all_measures,measures_dict,*args,**kwargs):
        """
        Fill _measure_values dictionary and make sure we have all the measurements the user told us we needed.
        """
        self._vital_measures=set(vital_measures)
        self._all_measures=self._vital_measures.union(all_measures)
        self._measure_values={}
        for k,v in measures_dict.items():
            self.measure_values(k,v)
        #Raise an error if we are missing key metrics on initialization
        if self._vital_measures is not None and not self.have_what_i_need(self._vital_measures):
            raise ValueError(f"We needed: {self._vital_measures}.")

    def measure_values(self,key,value=None):
        """
        Setter and getter for _measurements dictionary values
        key (str): label of value you are setting
        value (int): value
        """
        if not isinstance(key,str):
            raise ValueError("Measure labels must be strings.")
        if value:
            self._measure_values[key]=value
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
        return all([k in values_i_have for k in values_i_need])

    def what_do_i_have(self):
        """
        Get a list of strings for measurements that are entered in _measure_vlaues
        """
        return self._measure_values.keys()
    
class IncOrDecPatternMeasure(PatternMeasure):
    """
    This class is a pattern measure for a constant increases/decrease over a set number of rows (increase_x_by_y)
    Attributes: 
    _measurements: dictionary
    _vital_measures: ["start_stitches"] (constant)
    _all_measures: ["start_stitches","end_stitches","increase_x_every_y","n_rows"]
    """
    def __init__(self,vital_measures,all_measures,measures_dict):
        """
        We must have 3 of the 4 
        """
        super().__init__(["start_stitches"],["increase_x_every_y","end_stitches","n_rows"],measures_dict)
        self.fill_in_missing_measures()

    def _calc_n_rows(self):
        """
        If we have min and max stitches and its straight-up increase/decrease, calc number of rows
        """
        #TODO: Make sure there's no remainer when we divide
        need_list=["start_stitches","end_stitches","increase_x_every_y"]
        if self.have_what_i_need(need_list):
            increase_rate=self.measure_values("increase_x_every_y")
            increase_per_row=increase_rate[0]/increase_rate[1]
            n_to_increase=self.measure_values("end_stitches")-self.measure_values("start_stitches")
            self.measure_values("n_rows",n_to_increase/increase_per_row)
            return None
        else:
            raise ValueError("Trying to calculate number of rows in increase but missing one of these: {0}".format(need_list))
        
    def _calc_end_stitches(self):
        """"
        If we have increases/decreases but not the number we need at the end, calculate end_stitches (number of stitches per row at end of section"
        """
        need_list=["increase_x_every_y","n_rows","start_stitches"]
        if self.have_what_i_need(need_list):
            #raise a value error and return
            raise ValueError("Trying to calculate number of stitches at the end but missing one of: {0}, We have: {1}".format(need_list,self.what_do_i_have()))
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
            raise ValueError("We need :{0}. We only have:{1}.".format(need_list,self.what_do_i_have()))
        x=(self.end_stitches()-self.start_stitches())/self.n_rows()
        self.increase_x_every_y((x,1))
            
    def start_stitches(self,v=None):
        """
        Convenience function to set and get start_stitches
        """
        return self.measure_values("start_stitches",v)
    
    def end_stitches(self,v=None):
        """
        Convenience function to set and get end_stitches
        """
        return self.measure_values("end_stitches",v)
    
    def increase_x_every_y(self,v=None):
        """
        Convenience function to set and get increase_x_every_y
        """
        return self.measure_values("increase_x_every_y",v)

    def n_rows(self,v=None):
        """
        Convenience function to set and get n_rows
        """
        return self.measure_values("n_rows",v)
        
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

    # def __str__(self):
    #     return "A pattern measure for a simple increase or decrease: {0} to {1} over {2} rows".format(self.start_stitches().self.end_stitches(),self.n_rows())

    # def __repr__(self):
    #     return "IncOrDecMeasure({start_stitches={0},end_stitches={1},n_rows={2}})".format(self.start_stitches(),self.end_stitches(),self.n_rows())

class PatternSection:
    """
    A class to write and store the directions for a section of a pattern. 
    Attributes: 
    _label (str) Label used when writing pattern directions
    _measurements (PatternMeasure): object that holds measurements for section
    _directions (list): Directions for the pattern section in proper order. 
    """

    def __init__(self,vital_measures,all_measures,measures_dict,*args,**kwargs):
        """
        Initialize PatternMeasure and set label for Pattern Section
        vital_measures (list of str): Measurements that must be input by the calling function
        all_measures (list of str): All the measurements needed for the section, including those that are calculated
        measures_dict (dict str:int): A dictionary holding input measurements
        """
        self._directions=[]
        if "label" in kwargs.keys():
            self.label(kwargs["label"])
        else:
            self.label("Generic Pattern Section")
        self.make_measure(vital_measures,all_measures,measures_dict)

    def label(self,text=None):
        "Set or get the label for this section"
        if text:
            self._label=str(text)
        return self._label

    @abstractclassmethod
    def how_to_end(self):
        """
        Sections may have a cast-on or an attach instruction instead of a start for the beginning, but they all need an ending. 
        """
        pass

    @abstractclassmethod
    def make_measure(self,vital_measures,all_measures,measures_dict):
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
    def __init__(self,measures_dict):
        super().__init__(None,None,measures_dict)
        self.label("Toe")
    
    #TODO: We know increase_x_every_y for a toe, so check the input dictionary
    #Add increase_x_every_y=(4,2) and make sure you're adding a multiple of 4
    def make_measure(self,vital_measures,all_measures,measures_dict):
        """
        This is a standard increase from start_stitches to end_stitches
        """
        self._measurements=IncOrDecPatternMeasure(None,None,measures_dict)

    def how_to_cast_on(self):
        """
        Instructions for starting. This is a toe-up sock, so the toe starts with cast-on instructions.
        n_start: Number of starting stitches.
        """
        n_start=self._measurements.start_stitches()
        half_of_n_start=n_start/2
        return f"Cast on {n_start} ({half_of_n_start} per needle) in preferred style (Figure 8, crocet, etc).\nKnit all stitches around."
    
    def how_to_end(self):
        """
        Instructions for the end with number of stitches you should have.
        n_end: Number of stitches you have at the end
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
    Directions for the instep of a toe-up sock
    """
    def __init__(self,measures_dict):
        super().__init__(None,None,measures_dict)
        self.label("Instep")

    def make_measure(self,vital_measures,all_measures,measures_dict):
        """
        Use an IncOrDecPatternMeasure with a 0 increase.
        """
        #TODO: Check the input measures_dict and make sure we have the right numbers
        self._measurements=IncOrDecPatternMeasure(None,None,measures_dict)

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
        super().__init__(None,None,measures_dict)
        self.label("Gusset")
        self.make_measure(None,None,measures_dict)

    def make_measure(self,vital_measures,all_measures,measures_dict):
        """
        A guesset is an increase, but you only increase on a single needle.
        vital_measures: not used
        all_measures: not used
        measures_dict: dictionary with start_stitches, end_stitches and either n_rows or increase_x_every_y
        """
        #TODO: Check Measures dictionary
        self._measurements=IncOrDecPatternMeasure(None,None,measures_dict)

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
    def __init__(self,measures_dict,*args,**kwargs):
        measures_for_initial=measures_dict
        if "increase_x_every_y" not in measures_dict.keys():
            new_measures=measures_dict.copy()
            new_measures["increase_x_every_y"]=(-1,1)
            super().__init__(["start_stitches","end_stitches","increase_x_every_y"],["start_stitches","end_stitches","increase_x_every_y","first_turn","second_turn"],new_measures)
        else:
            super().__init__(["start_stitches","end_stitches","increase_x_every_y"],["start_stitches","end_stitches","increase_x_every_y","first_turn","second_turn"],new_measures)
        self.label("Heel Turn")
        self.fill_in_missing_measures()

    def make_measure(self,vital_measures,all_measures,measures_dict):
        self._measurements=IncOrDecPatternMeasure(vital_measures,all_measures,measures_dict)

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
        super().__init__(None,None,measures_dict)
        self.label("Cuff")
    
    def make_measure(self,vital_measures,all_measures,measures_dict):
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
    pattern_list=[toe,instep,gusset,turn,cuff]
    # #Print directions to screen
    print("\n----Pattern Directions------")
    for s in pattern_list:
    #A PatternSection only writes its directions when prompted
        s.write_directions()
        print("\n"+s.label())
        s.print_directions()

if __name__=="__main__": main()