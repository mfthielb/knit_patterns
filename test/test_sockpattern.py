import sys
sys.path.append('..')
import unittest 
from PatternCalcs import *

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
    sock.calculate_pattern()

    def test_auto_ease_adjust(self):
        self.assertTrue(self.sock.foot_measurements.ease_adjusted)
    def test_around_foot_ease(self):
        self.assertAlmostEqual(self.sock.foot_measurements.measure_values("around_foot"),0.9*2*4.1)
    def test_toe_to_heel_ease(self):
        self.assertAlmostEqual(self.sock.foot_measurements.measure_values("toe_to_heel"),0.9*9.5)
    def test_toe_to_heel_rows(self):
        self.assertAlmostEqual(self.sock.stitches.r_toe_to_heel,9.5*30/4*0.9)
    def test_around_foot_stitches(self):
        self.assertAlmostEqual(self.sock.stitches.s_around_foot,4.1*2*30/4*0.9)

    def test_pattern_section_types(self):
        expected_types=[ToeUpToeML,InstepML,ToeUpGuessetML,HeelTurnML,BasicCuff]
        for p,e in zip(self.sock.pattern_sections,expected_types):
            self.assertIsInstance(p,e)
    def test_toe_meets_instep(self):
        self.assertEqual(self.sock.pattern_sections[0].end_stitches(),self.sock.pattern_sections[1].start_stitches())
    def test_instep_meets_gusset(self):
        self.assertEqual(self.sock.pattern_sections[1].end_stitches(),self.sock.pattern_sections[2].start_stitches())
    def test_gusset_end(self):
        self.assertAlmostEqual(self.sock.pattern_sections[2].end_stitches(),self.sock.stitches.s_around_foot*(1.25))
    def test_gusset_meets_heel(self):
        self.assertEqual(self.sock.pattern_sections[3].end_stitches(),self.sock.pattern_sections[4].start_stitches)
    def test_heel_start(self):
        self.assertEqual(round(self.sock.pattern_sections[3].start_stitches()),round(self.sock.stitches.s_around_foot/2+self.sock.stitches.s_around_foot/4))
    def test_heel_end(self):
        self.assertEqual(round(self.sock.pattern_sections[3].end_stitches()),round(self.sock.stitches.s_around_foot/2))
    def test_heel_meets_cuff(self):
        self.assertEqual(self.sock.pattern_sections[4].start_stitches(),self.sock.stitches.s_around_foot)
if __name__=="__main__": unittest.main()