class TestToeUpToe(unittest.TestCase):
    def test_start_end(self):
        toe=ToeUpGuessetML(None,None,{"start_stitches":32,"end_stitches":64})
        self.assertEqual(toe.vital_measures(),{"start_stitches"})
        self.assertEqual(toe.what_i_have(),{"start_stitches","end_stitches","increase_x_every_y","n_rows"})
        self.assertEqual(toe.start_stitches(),32)
        self.assertEqual(toe.end_stitches(),64)
        self.assertEqual(toe.increase_x_every_y(),4)

