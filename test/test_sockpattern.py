import sys
sys.path.append('..')
import unittest 
from PatternCalcs import Guage, ToeUpSockPattern

class TestGuage(unittest.TestCase):
    def test_guage_init(self):
        guage_in=Guage((30,4),(30,4),units='in')
        guage_cm=Guage((30,4*2.54),(30,4*2.54),units='cm')
        self.assertEqual(guage_in.stitches(4),30)
        self.assertEqual(guage_in.rows(4),30)
        self.assertEqual(guage_in.rows(4),guage_cm.rows(4*2.54))
        self.assertEqual(guage_in.stitches(4),guage_cm.stitches(4*2.54))
        self.assertEqual(guage_in.units_to_rows(30),4)
        self.assertEqual(guage_in.units_to_stitches(30),4)

class TestPatternCalculator(unittest.TestCase):
    foot_measure_dict={'around_foot':4.1*2,'toe_to_heel':9.5}
    guage=Guage((30,4),(30,4),'in')
    sock=ToeUpSockPattern(foot_measure_dict,guage)

    def test_pattern_init(self):
        self.assertTrue(self.sock.foot_measurements.ease_adjusted)
        self.assertAlmostEqual(self.sock.foot_measurements.measure_values("around_foot"),0.9*2*4.1)
        self.assertAlmostEqual(self.sock.foot_measurements.measure_values("toe_to_heel"),0.9*9.5)
        self.assertAlmostEqual(self.sock.stitches.r_toe_to_heel,9.5*30/4*0.9)
        self.assertAlmostEqual(self.sock.stitches.s_around_foot,4.1*2*30/4*0.9)

if __name__=="__main__": unittest.main()