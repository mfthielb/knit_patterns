from pattern import *

class ToeUpToeML(IncOrDecPatternSection):
    """
    A Toe section for a basic toe-up sock using magic loop
    """
    def __init__(self,measures_dict,label=""):
        super().__init__(measures_dict,label=label)
    
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
    
    def __repr__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"ToeUpToeML({{'start_stitches':{start},'end_stitches':{end},'increase_x_every_y':(4,2)}})."

class InstepML(IncOrDecPatternSection):
    """
    Directions for the instep of a sock. Toe up or cuff down, the directions are the same
    """
    def __init__(self,measures_dict,label=""):
        super().__init__(measures_dict,label=label)
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
    
class ToeUpGuessetML(IncOrDecPatternSection):
    """
    A basic guesset section for a toe-up sock using magic loop
    Attributes: 
    _measurements: An IncOrDecPatternMeasure with a positive increase
    _directions: written directions
    """
    def __init__(self,measures_dict,label=""):
        super().__init__(measures_dict,label=label)
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

class HeelTurnML(IncOrDecPatternSection):
    """
    Heel turn with magic loop.
    """
    def __init__(self,measures_dict,label="",*args,**kwargs):
        if "increase_x_every_y" not in measures_dict.keys():
            new_measures=measures_dict.copy()
            new_measures["increase_x_every_y"]=(-1,1)
            super().__init__(new_measures,label=label)
        else:
            super().__init__(measures_dict,label,label)
        if len(self.label())==0:
            self.label("Heel Turn")
        self.fill_in_missing_measures()

    def make_measure(self,measures_dict):
        self._measurements=IncOrDecPatternMeasure(measures_dict)

    def _calc_first_turn(self):
        if not self._measurements.have_what_i_need(["start_stitches"]):
            raise ValueError("start_stitches not in measures dictionary.")
        self._measurements.measure_values("first_turn",value=self.start_stitches()-1)
    
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
        start=self.start_stitches()
        end=self.end_stitches()
        return f"Heel turn for magic loop toe-up {start} stitches inc to {end} stitches."
    
    def __repr__(self):
        start=self._measurements.start_stitches()
        end=self._measurements.end_stitches()
        return f"HeelTurnML({{'start_stitches':{start},'end_stitches':{end},'increase_x_every_y':(-1,1)}})."

class BasicCuff(IncOrDecPatternSection):
    def __init__(self,measures_dict,label=""):
        super().__init__(measures_dict,label=label)
        if len(self.label())==0:
            self.label("Cuff")
    
    def make_measure(self,measures_dict):
        self._measurements=IncOrDecPatternMeasure(measures_dict)
    
    def write_directions(self):
        self._directions.append("Row 1: K1, P1 for all {0} around".format(self._measurements.measure_values("start_stitches")))
        self._directions.append("Repeat Row 1 for {0} rows.".format(self._measurements.measure_values("n_rows")))
        self._directions.append("Bind off LOOSELY (or you won't be able to get the sock onto your foot).")
    
    def __str__(self):
        return "Cuff {0} stitches for {1} rows".format(self.start_stitches(),self.n_rows())
    
    def __repr__(self):
        return "Cuff({'start_stitches':{0},'end_stitches':{0},n_rows: {1})".format(self.start_stitches(),self.n_rows())

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
        self.ease_adjusted=ease
        #TODO: Implement the ability to guess sock size based on shoe size and shoe size based on sock size
        self.calc_ease()
        if not self.have_what_i_need(['around_foot','toe_to_heel']):
            raise Warning("Foot measure initialized without all needed measurements. Need: {0}. Initialized with: {1}").format(self.what_do_i_have(),self.vital_measures())
    
    def calc_ease(self):
        if self.ease_adjusted:
            print("Measurements already ease adjusted: "+self.__str__())
            return
        self.measure_values("around_foot",value=(self.measure_values("around_foot")*0.9))
        self.measure_values("toe_to_heel",value=(self.measure_values("toe_to_heel")*0.9))
        self.ease_adjusted=True
    
    def __str__(self):
        return "Foot measurements {0} {2} around and {1} {2} long.".format(self.measure_values("around_foot"),self.measure_values("toe_to_heel"),self.units)

    def __repr__(self):
        return "FootMeasure(\{'around_foot'={0},'toe_to_heel'={1}\},units={2},ease={3})".format(self.measure_values("around_foot"),self.measure_values("toe_to_heel"),self.units,self.ease_adjusted)

class SockStitches(NamedTuple):
    """
    NamedTuple that holds vital stitch statistics for a sock pattern
    """
    s_around_foot:float 
    r_toe_to_heel:float
    r_per_inch:float
    @property
    def toe_start(self):
        return round(self.s_around_foot/2)
    @property
    def toe_rows(self):
        return round(self.s_around_foot/2)
    @property
    def instep_rows(self):
        return self.r_toe_to_heel-self.toe_rows-self.r_per_inch*2
    @property
    def gusset_increase(self):
        return self.s_around_foot/4

class SockPatternSections(NamedTuple):
    toe:float
    instep:float
    gusset: float
    heel:float
    leg:float
    cuff: float 

class SockPattern():
    """
    Implementation for measurements needed by any sock pattern.
    """
    def __init__(self,foot_measure_dict,guage,**kwargs):
        if not (isinstance(guage.s_per_unit,tuple) and isinstance(guage.r_per_unit,tuple) and isinstance(guage.units,str)):
            raise ValueError("Guage should be Guage((int,int),(int,int),units). Guage entered is {0}".format(guage.__repr__()))
        self.guage=guage
        self.foot_measurements=FootMeasure(foot_measure_dict,units=guage.units,**kwargs)
        foot_stitches=guage.stitches(self.foot_measurements.measure_values('around_foot'))
        total_foot_rows=guage.rows(self.foot_measurements.measure_values('toe_to_heel'))
        r_per_unit=round(guage.r_per_unit[0]/guage.r_per_unit[1])
        if not (guage.units=='in'):
            r_per_unit=round(r_per_unit*2.54) 
        self.stitches=SockStitches(foot_stitches,total_foot_rows,r_per_unit)
        self.calculate_pattern()
        self.check_myself()

    def start_stitches(self,which):
        """
        Start stitches for requested pattern section
        """
        return self.pattern_sections.__getattribute__(which).start_stitches()

    def end_stitches(self,which):
        """
        End stitches for requested pattern section
        """
        return self.pattern_sections.__getattribute__(which).end_stitches()
    
    def write_directions(self):
        """
        Populate directions for each pattern section
        """
        for s in self.pattern_sections:
            if s is not None:
                s.write_directions()

    def print_pattern(self):
        """
        Print pattern sections to screen
        """
        for s in self.pattern_sections:
            if s is not None:
                print(s.print_directions())

    @abstractclassmethod
    def check_myself(self):
        pass

    @abstractclassmethod
    def calculate_pattern(self):
        pass

class ToeUpSockPattern(SockPattern):
    """
    Basic toe up sock pattern class.
    Members
    guage: Guage object holding stitches/unit and rows/unit and units of pattern
    stitches:SockStitches object holding all the vital measurements
    foot_measurements: FootMeasure object with foot measurements
    pattern_sections: Sock pattern sections named tuple
    Methods:
    calculate_pattern(self): Measurements for pattern sections
    """
    def __init__(self,foot_measure_dict,guage,**kwargs):
        super().__init__(foot_measure_dict,guage,**kwargs)

    def calculate_pattern(self):
        """
        Create pattern sections for sock.
        """
        toe=ToeUpToeML({"start_stitches":self.stitches.toe_start, "end_stitches":self.stitches.s_around_foot,"increase_x_every_y":(4,2)})
        instep=InstepML({"start_stitches":self.stitches.s_around_foot,"end_stitches":self.stitches.s_around_foot,"n_rows":self.stitches.instep_rows})
        gusset=ToeUpGuessetML({"start_stitches":self.stitches.s_around_foot,"end_stitches":self.stitches.gusset_increase+self.stitches.s_around_foot,"increase_x_every_y":(2,2)})
        heel_turn=HeelTurnML({"start_stitches":self.stitches.toe_start+self.stitches.gusset_increase,"end_stitches":(self.stitches.toe_start)})
        cuff=BasicCuff({"start_stitches":self.stitches.s_around_foot,"end_stitches":self.stitches.s_around_foot,"n_rows":self.stitches.r_per_inch})
        self.pattern_sections=SockPatternSections(toe,instep,gusset,heel_turn,None,cuff)

    def check_myself(self):
        """
        Make sure the sections of the sock meet up.
        """
        toe_meets_instep=(self.end_stitches('toe')==self.start_stitches('instep'))
        instep_meets_gusset=(self.end_stitches('instep')==self.start_stitches('gusset'))
        heel_finish_correct=(self.end_stitches('heel')==round(self.stitches.s_around_foot/2)) 
        if toe_meets_instep and instep_meets_gusset and heel_finish_correct:
            print("Congratulations! Your sock has no holes")
            return
        errors=[]
        if not toe_meets_instep:
            errors.append("Toe and instep won't meet: Toe ends with {0} stitches. Instep begins with {1}".format(self.pattern_sections.toe.end_stitches(),self.pattern_sections.instep.start_stitches()))
        if not instep_meets_gusset:
            errors.append("Instep and Gueest won't meet: Instep ends with {0}. Gusset starts with: {1}.",self.pattern_sections.instep.end_stitches(),self.pattern_sections.gusset.start_stitches())
        if not heel_finish_correct:
            errors.append("Heel turn finishes with {0} stitches. It should have {1} stitches.".format(self.pattern_sections.heel.end_stitches(),self.stitches.s_around_foot))      
        raise ValueError("\n".join(errors))
    
    def __str__(self):
        return "Toe-up sock with gusset heel for: {0}.".format(self.foot_measurements)

def main():
    print("Basic Sock Elements")
    foot_measure_dict={'around_foot':(4*2)/0.9,'toe_to_heel':9.5}
    guage=Guage((32,4),(32,4),'in')
    print("Toe-up sock pattern for a {0} foot with a {1} Guage.".format(foot_measure_dict.__str__(),guage.__str__()))
    sock=ToeUpSockPattern(foot_measure_dict,guage)
    sock.calculate_pattern()
    print("\n----Pattern Directions------")
    print(sock)
    sock.write_directions()
    sock.print_pattern()
    
if __name__=="__main__": main()