import sys
sys.path.append('..')
from KnittingConversions import *
import unittest

class TestGuessNeedle(unittest.TestCase):
    sg=StandardGuage()
    def test_tight_knitter(self):
        """
        Tight knitters (max knitter) should get the largest recommended needle
        """
        for w,n in self.sg._recommended_needle.items():
            self.assertEqual(self.sg._guess_needle_size(w,0.99),max(n),f"We don't get the largest needle for weight {w} and knitter=0.99")

    def test_loose_knitter(self):
        """
        Loose knitters (min knitter) should get the smallest recommended needle
        """
        for w,n in self.sg._recommended_needle.items():
            self.assertEqual(self.sg._guess_needle_size(w,0),min(n),f"We don't get the smallest needle for weight {w} and knitter=0.0")

    def test_mid_knitter(self):
        """
        Loose knitters (min knitter) should get the smallest recommended needle
        """
        for w,n in self.sg._recommended_needle.items():
            self.assertEqual(self.sg._guess_needle_size(w,0.5),n[floor(len(n)/2)],f"We don't get the smallest needle for weight {w} and knitter=0.0")

    def test_needle_range(self):
        """
        Every needle in the list should be 'reachable', i.e. there should be a knitter setting that will let us get that needle
        """
        for w,n in self.sg._recommended_needle.items():
            all_ns=[]
            for k in range(0,99):
                all_ns.append(self.sg._guess_needle_size(w,k/100))
            self.assertEqual(len(set(all_ns)),len(n),f"Not all needles are reachable for yarn weight {w}")

class TestGuessSPerUnit(unittest.TestCase):
    sg=StandardGuage()
    def test_mid_knitter_mid_needle(self):
        """
        Mid-sized needle for average knitter should give middle guage guess
        """
        for w,n in self.sg._recommended_needle.items():
            stitches=list(self.sg._stitches_per_4_inches.get(w))
            guess=self.sg._guess_s_per_4(w,n[floor(len(n)/2)],knitter=0.5)
            self.assertEqual(guess,stitches[floor(len(stitches)/2)])

    def tight_knitter_large_needle(self):
        """
        If a tight knitter has the largest needle, they should have average guage
        """
        for w,n in self.sg._recommended_needle.items():
            stitches=list(self.sg._stitches_per_4_inches.get(w))
            guess=self.sg._guess_s_per_4(w,max(n),knitter=0.99)
            self.assertEqual(guess,stitches[floor(len(stitches)/2)])
    
    def test_loose_knitter_large_needle(self):
        """
        If a loose knitter uses a large needle, they should have average guage
        """
        for w,n in self.sg._recommended_needle.items():
            stitches=list(self.sg._stitches_per_4_inches.get(w))
            guess=self.sg._guess_s_per_4(w,min(n),knitter=0)
            self.assertEqual(guess,stitches[floor(len(stitches)/2)])

if __name__=="__main__":unittest.main()