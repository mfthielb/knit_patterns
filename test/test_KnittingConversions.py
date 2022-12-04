import sys
sys.path.append('..')
from KnittingConversions import *
import unittest

class TestTightSmall(unittest.TestCase):
    sg=StandardGuage()
    def test_guess_needle(self):
        """
        Tight knitters with small needles should always get the max guage
        """
        for w,n in self.sg._recmmended_needle.items():
            self.assertEqual(self.sg._guess_needle_size(w,1),min(n))


if __name__=="__main__":unittest.main()