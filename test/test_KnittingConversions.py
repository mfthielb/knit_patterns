import sys
sys.path.append('..')
from KnittingConversions import *
import unittest

class TestKnittingDistance(unittest.TestCase):
    def test_guage(self):
        g=Guage((33,4),(33,4),1,0)
        self.assertEqual(g.get('s'),33.0/4.0)
    def test_cm_to_inches(self):
         g=Guage((33,4),(33,4),2.25,0)
         d=KnittingDistance()
         self.assertEqual(d.cm,2.54*10)

if __name__=="__main__":
    unittest.main()