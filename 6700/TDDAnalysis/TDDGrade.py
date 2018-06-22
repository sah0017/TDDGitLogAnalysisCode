"""
Created on April 2, 2018

@author: susanha

Used by:  CreateGitfileAnalysisReport
At a class level, contains the data and logic to calculate the TDD Grade.
Parameters:  None

Results:  holds the data used to assess the TDD grade from an assignment
and contains the algorithm for calculating TDD grade
"""
import ConfigParser
import collections
import AssignmentTotals

class TDDGradeRubric(object):
    rubric_dict = {}

    @classmethod
    def load_rubric(cls):
        my_config = ConfigParser.SafeConfigParser()
        my_config.read("TDDanalysis.cfg")

        rubric = collections.namedtuple("Rubric", 'basis deduction')
        for crit, rub_string in my_config.items("Grading Rubric"):
            rub_parts = rub_string.split(",")
            basis = int(rub_parts[0].strip("\"\'"))
            deductions = int(rub_parts[1].strip("\"\'"))
            cls.rubric_dict[crit] = rubric(basis = basis, deduction= deductions)
        #cls.keyIndexList = cls.assignmentNameDict.keys()
        #cls.keyIndexList.sort()

    def __init__(self):
        pass

    def calculateTDDGrade(self, avg_rl_length, avg_gl_length, tdd_commit_grades):
        avg_commit_grade = tdd_commit_grades
        if avg_rl_length > 0:
            rl_length_grade = self.calculate_tdd_grade(avg_rl_length, "consredlight")
        else:
            rl_length_grade = "N/A"
        if avg_gl_length > 0:
            gl_length_grade = self.calculate_tdd_grade(avg_gl_length, "consgreenlight")
        else:
            gl_length_grade = "N/A"
        return self.calc_assignment_grade(avg_commit_grade , rl_length_grade, gl_length_grade)


    def calculate_tdd_grade(self, total, reason):
        grade = 100
        basis = TDDGradeRubric.rubric_dict[reason].basis
        deductions = TDDGradeRubric.rubric_dict[reason].deduction
        if total < basis:
            total = basis
        if reason == "consgreenlight":
            total = total - basis
            grade = grade - (total * deductions)
        else:
            grade = grade - (((total / basis) - 1) * deductions)
        if grade < 0:
            grade = 0
        return grade

    def calc_assignment_grade(self, avg_com, rl_lgth, gl_lgth):
        divisor = 3
        if rl_lgth == "N/A":
            divisor -= 1
            rl_lgth = 0
        if gl_lgth == "N/A":
            divisor -= 1
            gl_lgth = 0
        return (avg_com + rl_lgth + gl_lgth) / divisor


if __name__ == "__main__":
    TDDGradeRubric.load_rubric()
