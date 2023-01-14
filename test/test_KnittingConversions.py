import sys
sys.path.append('..')
from KnittingConversions import *
import unittest
from collections import Counter
from math import floor, ceil

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
        Middle knitters (knitter=0.5) should get the middle recommended needle
        """
        for w,n in self.sg._recommended_needle.items():
            self.assertEqual(self.sg._guess_needle_size(w,0.5),n[floor(len(n)/2)],f"We don't get the middle needle for weight {w} and knitter=0.5")

    def test_needle_range(self):
        """
        Every needle in the recommended list should be 'reachable', i.e. there should be a knitter setting that will let us get that needle
        """
        for w,n in self.sg._recommended_needle.items():
            all_ns=[]
            for k in range(0,99):
                all_ns.append(self.sg._guess_needle_size(w,k/100))
            self.assertEqual(len(set(all_ns)),len(n),f"Not all needles are reachable for yarn weight {w}")
            c=Counter(all_ns)
            n=sum(c.values())
            expected=n/len(c)
            ok_diff=ceil(expected*0.2)
            for k,v in c.items():
                self.assertLess(abs(v-expected),ok_diff,f"Needle {k} is off for weight {w}. Expected to get {expected} times but got {v} instead.")

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
        If a loose knitter uses the smallest needle, they should have average guage
        """
        for w,n in self.sg._recommended_needle.items():
            stitches=list(self.sg._stitches_per_4_inches.get(w))
            guess=self.sg._guess_s_per_4(w,min(n),knitter=0)
            self.assertEqual(guess,stitches[floor(len(stitches)/2)])

class TestNeedleConversion(unittest.TestCase):
    n_converter=NeedleConversion()
    def test_mm_to_us_uk(self):
        """
        Make sure 1:1 conversions work for US needles
        """
        for mm,needle in self.n_converter._needles.items():
            if needle.uk is not None:
                closest=self.n_converter.get_closest_needle(mm,"uk")
                self.assertEqual(needle.uk,closest,
                "Wrong answer for NeedleConversion.get_closest_needle. got {0}. Should have {1}. Needle is: {2}"
                .format(closest,needle.uk,needle))
                self.assertEqual(self.n_converter.mm_to_uk(mm),needle.uk,
                f"Wrong answer for needle conversion mm_to_uk. Got {self.n_converter.mm_to_uk(mm)}. Should have {needle.uk}. Needle is: {needle}")
            if needle.us is not None:
                closest=self.n_converter.get_closest_needle(mm,"us")
                self.assertEqual(needle.us,closest,
                "Wrong answer for NeedleConversion.get_closest_needle. got {0}. Should have {1}. Needle is: {2}"
                .format(closest,needle.us,needle))
                self.assertEqual(self.n_converter.mm_to_us(mm),needle.us,
                f"Wrong answer for needle conversion mm_to_us. Got {self.n_converter.mm_to_us(mm)}. Should have {needle.us}. Needle is: {needle}")
 
    def test_some_none(self):
        c=0
        for mm,needle in self.n_converter._needles.items():
            if needle.uk is None:
                c=c+1
        self.assertNotEqual(c,0,"There should be at least one needle with no UK equivalent")

    def test_closest_us_1point5(self):
        needle=self.n_converter._needles.get(2.5).us
        closest=self.n_converter.convert_needle(1.5,"us","uk")
        self.assertEqual(needle,closest,f"Wrong answer for NeedleConversion.convert_needle. Got {closest}. Should have {needle}")


if __name__=="__main__":unittest.main()