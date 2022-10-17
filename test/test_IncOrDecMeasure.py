import sys
sys.path.append("..")
from PatternCalcs import IncOrDecPatternMeasure
import unittest

class TestIncOrDecMeasure(unittest.TestCase):
    def test_minimal_args(self):
        """
        Test __init__ warnings 
        """
        with self.assertRaises(ValueError):
            toe=IncOrDecPatternMeasure(None,None,{"start_stitches":24,"end_stitches":48})
        with self.assertRaises(Warning):
            toe=IncOrDecPatternMeasure(None,None,{"increase_x_every_y":(4,2),"end_stitches":48})

    def test_measures_set(self):
        toe=IncOrDecPatternMeasure(None,None,{"start_stitches":32,"increase_x_every_y":(4,2),"end_stitches":64})
        self.assertEqual(toe.vital_measures(),{"start_stitches"})
        self.assertEqual(toe.what_do_i_have(),{"start_stitches","end_stitches","n_rows","increase_x_every_y"})
    
    def test_calc_increase(self):
        toe=IncOrDecPatternMeasure(None,None,{"start_stitches":12,"end_stitches":32,"n_rows":10})
        self.assertEqual(toe.increase_x_every_y(),(2,1))

    def test_calc_decrease(self):
        toe=IncOrDecPatternMeasure(None,None,{"start_stitches":32,"end_stitches":12,"n_rows":10})
        self.assertEqual(toe.increase_x_every_y(),(-2,1))
    
    def test_calc_n_rows(self):
        toe=IncOrDecPatternMeasure(None,None,{"start_stitches":32,"end_stitches":12,"increase_x_every_y":(-2,1)})
        self.assertEqual(toe.n_rows(),10)

    def test_calc_n_rows(self):
        toe=IncOrDecPatternMeasure(None,None,{"start_stitches":12,"end_stitches":32,"increase_x_every_y":(2,1)})
        self.assertEqual(toe.n_rows(),10)        

if __name__=="__main__": 
    unittest.main()