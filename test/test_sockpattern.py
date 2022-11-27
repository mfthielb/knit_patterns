import sys
sys.path.append('..')
import unittest 
from PatternCalcs import *

class TestGuage(unittest.TestCase):
    guage_in=Guage((30,4),(30,4),units='in')
    guage_cm=Guage((30,4*2.54),(30,4*2.54),units='cm')
    def test_guage_stitches(self):
        self.assertEqual(self.guage_in.stitches(4),30)
    def test_guage_rows(self):
        self.assertEqual(self.guage_in.rows(4),30)
    def test_guage_cm_rows(self):
        self.assertEqual(self.guage_in.rows(4),self.guage_cm.rows(4*2.54))
    def test_guage_cm_stitches(self):
        self.assertEqual(self.guage_in.stitches(4),self.guage_cm.stitches(4*2.54))
    def test_units_to_rows(self):
        self.assertEqual(self.guage_in.units_to_rows(30),4)
    def test_units_to_stitches(self):
        self.assertEqual(self.guage_in.units_to_stitches(30),4)

class TestPatternCalculator(unittest.TestCase):
    foot_measure_dict={'around_foot':4.1*2,'toe_to_heel':9.5}
    guage=Guage((30,4),(30,4),'in')
    sock=ToeUpSockPattern(foot_measure_dict,guage)
    sock.calculate_pattern()

    def test_auto_ease_adjust(self):
        """
        Make sure foot measure is automatically ease adjusted by default
        """
        self.assertTrue(self.sock.foot_measurements.ease_adjusted)

    def test_around_foot_ease(self):
        """
        Test that ease-adjusted foot measurement is set
        """
        self.assertAlmostEqual(self.sock.foot_measurements.measure_values("around_foot"),0.9*2*4.1)
    
    def test_ease_already_adjusted(self):
        """
        Make sure ability to set ease=True on create is intact
        """
        s=ToeUpSockPattern(self.foot_measure_dict,self.guage,ease=True)
        self.assertTrue(s.foot_measurements.ease_adjusted)
        self.assertEqual(s.foot_measurements.measure_values("around_foot"),2*4.1)
        self.assertEqual(s.foot_measurements.measure_values("toe_to_heel"),9.5)

    def test_toe_to_heel_ease(self):
        """
        Test that ease-adjusted toe-to-heel measurement is set 
        """
        self.assertAlmostEqual(self.sock.foot_measurements.measure_values("toe_to_heel"),0.9*9.5)

    def test_toe_to_heel_rows(self):
        """
        Test calculations for number of rows from toe-to-heel
        """
        self.assertAlmostEqual(self.sock.stitches.r_toe_to_heel,9.5*30/4*0.9)

    def test_around_foot_stitches(self):
        """
        Test that stitches around foot are calculated correctly
        """
        self.assertAlmostEqual(self.sock.stitches.s_around_foot,4.1*2*30/4*0.9)

    def test_pattern_section_types(self):
        """
        Test whether pattern types are created correctly and in the correct order
        """
        expected_types=[ToeUpToeML,InstepML,ToeUpGuessetML,HeelTurnML,None,BasicCuff]
        for p,e in zip(self.sock.pattern_sections,expected_types):
            if e is not None:
                self.assertIsInstance(p,e)

    def test_toe_meets_instep(self):
        """
        End stitches for toe should match begin stitches for instep
        """
        self.assertEqual(self.sock.end_stitches('toe'),self.sock.start_stitches('instep'))

    def test_instep_meets_gusset(self):
        """
        Begin stitches for gusset should match end stitches for instep
        """
        self.assertEqual(self.sock.end_stitches('instep'),self.sock.start_stitches('gusset'))

    def test_gusset_end(self):
        """
        End stitches for gusset should be number of stitches around foot +25% 
        """
        self.assertAlmostEqual(self.sock.end_stitches('gusset'),self.sock.stitches.s_around_foot*(1.25))

    def test_heel_start(self):
        """
        Heel turn starting stitches is half the stitches around + the added stitches for the gusset
        """
        self.assertEqual(round(self.sock.start_stitches('heel')),round(self.sock.stitches.s_around_foot/2+self.sock.stitches.s_around_foot/4))

    def test_heel_end(self):
        """
        Heel turn ending stitches should be back to the number of stitches around the foot.
        """
        self.assertEqual(round(self.sock.end_stitches('heel')),round(self.sock.stitches.s_around_foot/2))

    def test_heel_meets_cuff(self):
        """
        Cuff begin should be around foot stitches
        """
        self.assertEqual(self.sock.start_stitches('cuff'),self.sock.stitches.s_around_foot)
if __name__=="__main__": unittest.main()