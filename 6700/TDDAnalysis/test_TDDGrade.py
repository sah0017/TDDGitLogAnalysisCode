
import unittest
import sys

from TDDGrade import TDDGradeRubric
import AssignmentTotals


class MyTDDGradeTestCase(unittest.TestCase):
    def setUp(self):
        TDDGradeRubric.load_rubric()

    def test_redlightwithprodcode(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(2, "redlightwithprodcode"), 90)

    def test_consredlight(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(2, "consredlight"), 95)

    def test_onetransformation(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(2, "onetransformation"), 95)

    def test_largecommit20(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(20, "largecommit"), 95)

    def test_largecommit30(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(30, "largecommit"), 90)

    def test_greenlightwithtestcode(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(2, "greenlightwithtestcode"), 90)

    def test_greenlightwithtestcode6(self):
        my_tdd_grade = TDDGradeRubric()
        self.assertEqual(my_tdd_grade.calculate_tdd_commit_grade(6, "greenlightwithtestcode"), 50)

    def test_overall_grade(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [100, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(1, 1, 100), 100)

    def test_overall_grade_high_rl_avg(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [100, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(2, 1, 100), 98)

    def test_overall_grade_high_gl_avg(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [100, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(1, 6, 100), 98)

    def test_overall_grade_low_grade_list(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [90, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(1, 4, 96), 98)

    def test_overall_no_rls(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [90, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(0, 4, 100), 100)

    def test_overall_no_gls(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [90, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(1, 0, 100), 100)

    def test_overall_no_gls_low_com_avg(self):
        my_tdd_grade = TDDGradeRubric()
        grade_list = [90, 100, 100]
        self.assertEqual(my_tdd_grade.calculate_overall_tdd_grade(1, 0, 90), 95)

    """
    current configuration values
    ConsRedLight:  "1, 5"
    ConsGreenLight:  "5, 5"
    RedLightWithProdCode:  "1, 10"
    GreenLightWithTestCode:  "1, 10"
    OneTransformation:  "1, 5"
    LargeCommits:  "10, 5"
            
    """


if __name__ == '__main__':
    unittest.main()

