import sys
sys.path.append("..")
from PatternCalcs import IncOrDecPatternMeasure
import unittest

class TestIncOrDecMeasure(unittest.TestCase):
    def test_minimal_args(self):
        with self.assertRaises(ValueError):
            toe=IncOrDecPatternMeasure(None,None,{"start_stitches":24,"end_stitches":48})
        with self.assertRaises(ValueError):
            ##TODO: WHY ERROR WTF????
            toe=IncOrDecPatternMeasure(None,None,{"increase_x_every_y":(4,2),"end_stitches":48})
        toe=IncOrDecPatternMeasure(None,None,{"start_stitches":32,"increase_x_every_y":(4,2),"end_stitches":64})
        self.assertEqual(toe.vital_measures(),{"start_stitches"})
        self.assertEqual(toe.what_do_i_have(),{"start_stitches","end_stitches","n_rows","increase_x_every_y"})

if __name__=="__main__": 
    unittest.main()