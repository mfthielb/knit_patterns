import sys
sys.path.append("..")
from src.pattern import PatternMeasure
import unittest

class TestPatternMeasure(unittest.TestCase):
    def test_minimal_arg(self):
        """
        Make sure pattern measure raises errors when not given vital measures or a dictionary 
        """
        with self.assertRaises(Warning):
            m=PatternMeasure(None,None,None)
            self.assertEqual(m.vital_measures(),set())
            self.assertEqual(m.all_measures(),set())
            self.assertEqual(m.what_do_i_have(),set())

    def test_measure_dict_only(self):
        m=PatternMeasure(None,None,{"start_stitches":1,"end_stitches":11})
        self.assertEqual(m.label(),"")
        self.assertEqual(m.vital_measures(),set())
        self.assertEqual(m.all_measures(),set(["start_stitches","end_stitches"]))
        self.assertEqual(m.vital_measures(),set())

    def test_init_with_all(self):
        with self.assertRaises(Warning):
            m=PatternMeasure(["n_rows"],None,{"start_stitches":1,"end_stitches":11})
            self.assertEqual(m.label(),"")
            self.assertEqual(m.all_measures(),set(["start_stitches","end_stitches","n_rows"]))
            m.measure_values("n_rows",6)
            self.assertTrue(m.have_what_i_need())

if __name__=="__main__": 
    unittest.main()