import unittest
import tppAnalysis.TDDGrade as TDDGrade


class MyTDDGradeTestCase(unittest.TestCase):
    def test_has_cons_RL_data(self):
        myTDDGrade = TDDGrade.TDDGrade()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
