"""
Created on April 2, 2018

@author: susanha

Used by:  Assignment and Commit
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
            cls.rubric_dict[crit] = rubric(basis=basis, deduction=deductions)
        #cls.keyIndexList = cls.assignmentNameDict.keys()
        #cls.keyIndexList.sort()

    def __init__(self):
        pass

    def calculate_overall_tdd_grade(self, avg_rl_length, percent_rl, avg_gl_length, percent_gl, tdd_commit_grades):
        rla_basis = float(TDDGradeRubric.rubric_dict["redlightavg"].basis) / 100
        rla_grade = TDDGradeRubric.rubric_dict["redlightavg"].deduction
        gla_basis = float(TDDGradeRubric.rubric_dict["greenlightavg"].basis) / 100
        gla_grade = TDDGradeRubric.rubric_dict["greenlightavg"].deduction
        rlstdev_basis = float(TDDGradeRubric.rubric_dict["rlstdev"].basis) / 100
        rlstdev_grade = TDDGradeRubric.rubric_dict["rlstdev"].deduction
        glstdev_basis = float(TDDGradeRubric.rubric_dict["glstdev"].basis) / 100
        glstdev_grade = TDDGradeRubric.rubric_dict["glstdev"].deduction
        rl_length_grade = 100
        gl_length_grade = 100

        avg_commit_grade = tdd_commit_grades
        if percent_rl < rlstdev_basis:
            rl_length_grade = rlstdev_grade
        elif percent_rl < rla_basis:
            rl_length_grade = rla_grade
        elif avg_rl_length > 0:
            rl_length_grade = self.calculate_tdd_commit_grade(avg_rl_length, "consredlight")
        if percent_gl < glstdev_basis:
            gl_length_grade = glstdev_grade
        elif percent_gl < gla_basis:
            gl_length_grade = gla_grade
        elif avg_gl_length > 0:
            gl_length_grade = self.calculate_tdd_commit_grade(avg_gl_length, "consgreenlight")
        return self.calc_assignment_grade(avg_commit_grade , rl_length_grade, gl_length_grade)

    def calculate_tdd_commit_grade(self, total, reason):
        grade = 100
        basis = TDDGradeRubric.rubric_dict[reason].basis
        deductions = TDDGradeRubric.rubric_dict[reason].deduction
        if total < basis:
            total = basis
        if reason == "consgreenlight":
            total = total - basis
            grade = grade - (total * deductions)
        else:
            grade = grade - ((float(total / basis) - 1) * deductions)
        if grade < 0:
            grade = 0
        return round(grade)

    def calc_assignment_grade(self, avg_com, rl_lgth, gl_lgth):
        if avg_com == "N/A":
            return "N/A"
        divisor = 3
        return round((avg_com + rl_lgth + gl_lgth) / float(divisor))


if __name__ == "__main__":
    TDDGradeRubric.load_rubric()
