"""
Created on Apr 7, 2016

@author: susanha
Used by:  GitFile
At a class level, contains the current assignments to be analyzed
Parameters:  when instantiated, receives an assignment name.  Keeps track of commit data per assignment.

Results:  analyzes a specific assignment within a git file and tracks data about it.  Contains a list
of commit objects within the assignment.
Uses:  Commit

"""
import time
import ConfigParser
import Transformations
import AssignmentTotals
import Commit
from time import strptime
import ConsecutiveCommitsOfSameType
import TDDCycle
import TDDGrade
from collections import OrderedDict


class Assignment(object):
    """
    classdocs
    """
    """ **********************  class variables and methods  **********************   """
    assignmentNameDict = {}
    recommendations_dict = {}
    ordered_assignment_name_dict = {}
    keyIndexList = []
    originalAssignment = None

    @classmethod
    def is_first_assignment(cls, commitDate):
        if commitDate <= cls.ordered_assignment_name_dict.items()[0]:
            return True
        else:
            return False

    """
    This method uses the date on the commit to determine which assignment the commit goes with
    """
    @classmethod
    def get_curr_assignmentName(cls, commit_date):
        for k in range(0, len(cls.ordered_assignment_name_dict)-1):
            if cls.ordered_assignment_name_dict.items()[k] <= commit_date <= cls.ordered_assignment_name_dict.items()[k + 1]:
                return cls.ordered_assignment_name_dict.items()[k+1]


    @classmethod
    def loadAssignments(cls):
        my_config = ConfigParser.SafeConfigParser()
        my_config.read("TDDanalysis.cfg")
        cls.originalAssignment = my_config.get("Assignments","BaseName") + my_config.get("Assignments","FirstAssignment")

        for key, val in my_config.items("Due Dates"):
            cls.assignmentNameDict[key] = val
        cls.ordered_assignment_name_dict = OrderedDict(sorted(cls.assignmentNameDict.items(), key=lambda x: time.mktime(time.strptime(x[1],"%Y, %m, %d"))))
        for key, val in my_config.items("Recommendations"):
            cls.recommendations_dict[key] = val

    @classmethod
    def getMyFirstAssignment(cls):
        return cls.originalAssignment
    
    @classmethod
    def get_assignment_name_dict(cls):
        return cls.ordered_assignment_name_dict

    @classmethod
    def get_assignment_list(cls):
        assignment_name_list = cls.ordered_assignment_name_dict.keys()
        return assignment_name_list
    """ **********************  end class variables and methods  **********************   """

    def __init__(self, assn_name):
        """
        Constructor
        """
        self.assignmentName = assn_name
        self.myCommits = []
        self.myCommitTotals = []
        self.consecutiveCommitsOfSameTypeList = []
        self.consecutiveRedLights = 0
        self.consecutiveGreenLights = 0
        self.tdd_commit_grades = []
        self.tdd_grade = 0
        self.TDDCycles = []

    def analyzeAssignment(self, file_io_object):
        __commits = 0
        prev_commit = None
        line = file_io_object.getCurrentLine()
        tdd_cycle_contains_green_light = True
        my_tdd_cycle = None

        # line = fileIOobject.readNextLine()          # commit date
        while line is not False:
            __assignmentName = self.findCurrentAssignment(line)  # advances to next line to check the commit date
            if self.assignmentName != __assignmentName:
                return __assignmentName                    # we've moved to a new assignment, done with this one

            __commits = __commits + 1
            my_new_commit = Commit.Commit(__commits, file_io_object)
            self.addCommitToAssignment(my_new_commit.analyzeCommit(file_io_object, line))
            new_commit_type = my_new_commit.get_commit_type()
            my_new_commit.set_commit_validity(new_commit_type)
            if prev_commit == new_commit_type:            # looking for consecutive Red or Green Lights
                if new_commit_type == "Red Light":
                    self.incrementConsecutiveRedLights()
                elif new_commit_type == "Green Light":
                    self.incrementConsecutiveGreenLights()

                my_cons_commit = ConsecutiveCommitsOfSameType.ConsecutiveCommitsOfSameType(new_commit_type,
                                                                                         __commits-1,__commits)
                file_list = self.myCommits[__commits-2].get_file_names_list()
                my_cons_commit.setFirstCommitList(file_list)
                file_list = self.myCommits[__commits-1].get_file_names_list()
                my_cons_commit.setSecondCommitList(file_list)
                self.consecutiveCommitsOfSameTypeList.append(my_cons_commit)
            elif new_commit_type == "Green Light":
                tdd_cycle_contains_green_light = True
            elif prev_commit is None and new_commit_type != "Red Light":
                my_tdd_cycle = self.addNewTDDCycle(False)
            else:
                if new_commit_type == "Red Light" and tdd_cycle_contains_green_light:
                    self.addTddCycleToAssignment(my_tdd_cycle)
                    my_tdd_cycle = self.addNewTDDCycle(True)
                    tdd_cycle_contains_green_light = False
            my_tdd_cycle = self.addCommitToTDDCycle(my_tdd_cycle, my_new_commit)
            prev_commit = new_commit_type
            line = file_io_object.readNextLine()
        self.addTddCycleToAssignment(my_tdd_cycle)
        return False

    def addNewTDDCycle(self, starts_with_rl):
        return TDDCycle.TDDCycle(starts_with_rl)

    def addCommitToTDDCycle(self, my_tdd_cycle, commit):
        if my_tdd_cycle is None:
            my_tdd_cycle = self.addNewTDDCycle(False)
        my_tdd_cycle.addCommit(commit)
        return my_tdd_cycle

    def addTddCycleToAssignment(self, tdd_cycle):
        self.TDDCycles.append(tdd_cycle)

    def findCurrentAssignment(self, line):
        """ a git file can contain multiple assignments.  This is looking for the current one for analysis.
         line after commit contains the commit date.  Use this date to determine which assignment commit belongs in
        """
        date_line = line.split("-")
        commit_date = strptime(date_line[0].strip(), '%a %b %d %X %Y')

        if Assignment.is_first_assignment(commit_date):
            curr_assignment_name = Assignment.originalAssignment
        else:
            curr_assignment_name = Assignment.get_curr_assignmentName(commit_date)
        return curr_assignment_name


    def CalculateMyCommitStats(self, out_file):
        """
        This method calculates the commit stats for an assignment and creates the individual report file (.gitout)
        :param out_file: the file handle for the report file
        :return: my_assignment_stats - the total of all the different statistics we're tracking
        """
        my_trans_names = Transformations.Trans()
        Commit.Commit.load_grade_criteria()
        grader = TDDGrade.TDDGradeRubric()
        #RecDict = self.loadRecommendations()
        trans_totals_in_assignment = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        antitrans_totals_in_assignment = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        assignment_commit_tdd_grades = []
        added_lines = 0
        added_test_lines = 0
        deleted_lines = 0
        deleted_test_lines = 0
        nbr_commits = 0
        nbr_red_light = 0
        nbr_invalid_r_l = 0
        nbr_green_light = 0
        nbr_invalid_g_l = 0
        nbr_refactor = 0
        nbr_unknown_commit = 0
        nbr_transformations = 0
        nbr_anti_transformations = 0
        ratio = 0
        out_file.write("\r\n*********************************\r\nAssignment Name:" + str(self.assignmentName) +
                      "\r\n*********************************")
        """
        if self.getConsecutiveRedLights() > 1:
            outFile.write("\r\n TDD Recommendation:  " + Assignment.recommendations_dict["consredlight"])
        if self.getConsecutiveGreenLights() > 1:
            outFile.write("\r\n TDD Recommendation:  " + Assignment.recommendations_dict["consgreenlight"])
        """
        gl_longest_consec, gl_avg_length = \
            self.longest_string_and_avg_of_consecutive_types(self.consecutiveCommitsOfSameTypeList, "Green Light")
        rl_longest_consec, rl_avg_length = \
            self.longest_string_and_avg_of_consecutive_types(self.consecutiveCommitsOfSameTypeList, "Red Light")
        out_file.write("\r\nNumber of TDD Cycles:  " + str(len(self.TDDCycles)))
        if gl_avg_length > 0 or gl_longest_consec > 0:
            out_file.write("\r\nLongest Streak of Consecutive Green Lights:  " + str(gl_longest_consec) +
                      "\tAverage Length of Consecutive Green Light Streaks:  " + str(gl_avg_length))
        if rl_avg_length > 0 or rl_longest_consec > 0:
            out_file.write("\r\nLongest Streak of Consecutive Red Lights:  " + str(rl_longest_consec) +
                      "\tAverage Length of Consecutive Red Light Streaks:  " + str(rl_avg_length))
                      #"\r\nConsecutive Commits of Same Type:  " + str(len(self.consecutiveCommitsOfSameTypeList)))
        """
        for ConsCommits in self.consecutiveCommitsOfSameTypeList:
            outFile.write("\r\tCommit Type:  " + ConsCommits.consCommitType +
                          "\r\t\tFirst Commit:  " + str(ConsCommits.firstCommitNbr) +
                          "\tFirst Commit File List:  ")
            for f in ConsCommits.firstCommitFileList:
                outFile.write(f + "\t")
            outFile.write("\r\t\tSecond Commit:  " + str(ConsCommits.secondCommitNbr) +
                          "\tSecond Commit File List:  ")
            for f in ConsCommits.secondCommitFileList:
                outFile.write(f + "\t")
        """
        nbr_commits = nbr_commits + len(self.myCommits)
        for my_commit in self.myCommits:
            my_files = my_commit.get_file_list()
            ctype = my_commit.get_commit_type()
            commit_validity = my_commit.get_commit_validity()
            if ctype == "Red Light":
                nbr_red_light = nbr_red_light + 1
                if commit_validity == "INVALID":
                    nbr_invalid_r_l += 1

            elif ctype == "Green Light":
                nbr_green_light = nbr_green_light + 1
                if commit_validity == "INVALID":
                    nbr_invalid_g_l += 1
                for my_file in my_files:      # 6/27/18 moved here to only count transformations for GL commits
                    my_trans = my_file.get_transformations()
                    out_file.write("\n\r\tTransformations to file:  " + my_file.getFileName() +
                                  "  (" + my_file.getFileType() + ")")
                    for my_tran in my_trans:
                        out_file.write("\r\t" + my_trans_names.getTransformationName(my_tran))

                        if my_tran >= 0:
                            #transTotalsInAnalysis[my_tran] = transTotalsInAnalysis[my_tran] + 1
                            trans_totals_in_assignment[my_tran] = trans_totals_in_assignment[my_tran] + 1
                            nbr_transformations = nbr_transformations + 1
                        else:
                            #self.__antitransTotalsInAnalysis[abs(my_tran)] = self.__antitransTotalsInAnalysis[abs(my_tran)] + 1
                            antitrans_totals_in_assignment[abs(my_tran)] = antitrans_totals_in_assignment[abs(my_tran)] + 1
                        nbr_anti_transformations = nbr_anti_transformations + 1
            elif ctype == "Refactor":
                nbr_refactor = nbr_refactor + 1
            else:
                nbr_unknown_commit = nbr_unknown_commit + 1
            out_file.write("\r\n------------------------------\r\n\tCommit Number:" + str(my_commit.commit_nbr) +
                          "\tCommit type: " + my_commit.commitType)  # + "    Validity value -- " + commit_validity)  SAH temporarily removed
            commit_tdd_grade = my_commit.calculate_tdd_grade()
            out_file.write("\t  Commit TDD Score:  " + str(commit_tdd_grade))
            if commit_validity == "INVALID":
                out_file.write("\r\nCommit Feedback")
                invalid_reason = my_commit.get_invalid_reason()
                for r in invalid_reason:
                    out_file.write("\r\n" + Assignment.recommendations_dict[r])
            self.tdd_commit_grades.append(commit_tdd_grade)
            out_file.write("\n\r\tAdded lines:" +
                           str(my_commit.added_lines_in_commit) + ".  Deleted lines:" +
                           str(my_commit.deleted_lines_in_commit) + ".\r\n\t  Added test lines:" +
                           str(my_commit.added_test_loc) + "  Deleted test lines:" +
                           str(my_commit.deleted_test_loc) + ".\r\n\t  Test files:" + str(my_commit.nbr_test_files) +
                          ".  Production files:" + str(my_commit.nbr_prod_files) + ".  Number of Transformations:  " +
                           str(my_commit.number_of_transformations) + ".\r\n")

            added_lines = added_lines + my_commit.added_lines_in_commit
            added_test_lines = added_test_lines + my_commit.added_test_loc
            deleted_lines = deleted_lines + my_commit.deleted_lines_in_commit
            deleted_test_lines = deleted_test_lines + my_commit.deleted_test_loc

            my_assignment_stats = AssignmentTotals.AssignmentTotals()
            my_assignment_stats.nbrCommits = nbr_commits
            my_assignment_stats.RLCommit = nbr_red_light
            my_assignment_stats.add_invalid_rl_commits(nbr_invalid_r_l)
            my_assignment_stats.GLCommit = nbr_green_light
            my_assignment_stats.add_invalid_gl_commits(nbr_invalid_g_l)
            my_assignment_stats.refCommit = nbr_refactor
            my_assignment_stats.otherCommit = nbr_unknown_commit
            my_assignment_stats.addedLinesInAssignment = added_lines
            my_assignment_stats.addedTestLOCInAssignment = added_test_lines
            my_assignment_stats.deletedLinesInAssignment = deleted_lines
            my_assignment_stats.deletedTestLOCInAssignment = deleted_test_lines
            overall_deleted_lines = deleted_lines + deleted_test_lines
            my_assignment_stats.totalDelLines = overall_deleted_lines
            my_assignment_stats.totalTransByTypeInAssignment = trans_totals_in_assignment
            my_assignment_stats.totalAntiTransByTypeInAssignment = antitrans_totals_in_assignment

        grade_total = 0
        nbr_of_grades = 0
        for grade in self.tdd_commit_grades:
            if grade != "N/A":
                grade_total = grade_total + grade
                nbr_of_grades += 1
        if nbr_of_grades == 0:
            tdd_commit_avg_grade = "N/A"
        else:
            tdd_commit_avg_grade = grade_total / nbr_of_grades
        self.tdd_grade = grader.calculateTDDGrade(rl_avg_length, gl_avg_length, tdd_commit_avg_grade)
        out_file.write("\r\n============================================\r\nTotal test code lines added:" + str(added_test_lines))
        out_file.write("\r\nTotal production code lines added:" + str(added_lines))
        out_file.write("\r\nTotal test code lines deleted:" + str(deleted_test_lines))
        out_file.write("\r\nTotal production code lines deleted:" + str(deleted_lines))
        if added_lines > 0:
            ratio = added_test_lines / float(added_lines)
            out_file.write("\r\nRatio of test code to production code:" + format(ratio, '.2f') + ":1")
        out_file.write("\r\nTDD Score:  " + str(self.tdd_grade))
        if self.tdd_grade == "N/A":
            out_file.write("\r\nNo Red or Green Light commits found ")
        else:
            out_file.write("\r\nGrade Components:  Average Red Light Length - " + str(rl_avg_length) +
                      ";  Average Green Light Length - " + str(gl_avg_length) +
                      ";  Average of TDD Commit Scores - " + str(tdd_commit_avg_grade))
        out_file.write("\r\n============================================\r\n\r\n")
        """
        self.add_to_total_commits_in_analysis(nbr_commits)
        self.__totalTransformationsInAnalysis = self.__totalTransformationsInAnalysis + nbr_transformations
        self.__totalAntiTransformationsInAnalysis = self.__totalAntiTransformationsInAnalysis + nbr_anti_transformations
        self.__totalLinesOfCodeInAnalysis = self.__totalLinesOfCodeInAnalysis + added_lines
        """
        return my_assignment_stats

    def longest_string_and_avg_of_consecutive_types(self, con_commits_list, cm_type):
        prev_cm_type = "None"
        consecutive_streaks = []
        streak_count = 0
        second_commit_nbr = 0
        for cons_commit in con_commits_list:
            curr_cm_type = cons_commit.get_commit_type()
            if cons_commit.get_first_commit_nbr() == second_commit_nbr and curr_cm_type == prev_cm_type:
                if curr_cm_type == cm_type:
                    streak_count += 1
            else:
                if streak_count > 0:
                    consecutive_streaks.append(streak_count)
                    streak_count = 0
            prev_cm_type = curr_cm_type
            second_commit_nbr = cons_commit.get_second_commit_nbr()
        if consecutive_streaks:
            tot_of_streaks = 0
            for i in consecutive_streaks:
                tot_of_streaks += i
            avg_streak_lgth = tot_of_streaks / len(consecutive_streaks)
            lrgst_cons_strk_lgth = max(consecutive_streaks)
        else:
            avg_streak_lgth = 0
            lrgst_cons_strk_lgth = 0
        return lrgst_cons_strk_lgth, avg_streak_lgth

    def incrementConsecutiveRedLights(self):
        self.consecutiveRedLights += 1

    def incrementConsecutiveGreenLights(self):
        self.consecutiveGreenLights += 1

    def getTDDCycleCount(self):
        return len(self.TDDCycles)

    def getConsecutiveRedLights(self):
        return self.consecutiveRedLights

    def getConsecutiveGreenLights(self):
        return self.consecutiveGreenLights

    def getReasonsForConsecutiveCommits(self, commit_type):
        reason_list = [0, 0, 0, 0]
        reason_string = ""
        for r in self.consecutiveCommitsOfSameTypeList:
            if r.consCommitType == commit_type:
                reason = r.reasonForDuplicateTypes()
                reason_list[reason] += 1
        for s in reason_list:
            reason_string = reason_string + ", " + str(s)
        return reason_string

    def addCommitToAssignment(self, commit):
        self.myCommits.append(commit)

    def addCommitTotalsToAssignment(self, commit_totals):
        self.myCommitTotals.append(commit_totals)

    def get_assignment_name(self):
        return self.assignmentName

    def get_my_commit_totals(self):
        return self.myCommitTotals

    def get_my_commits(self):
        return self.myCommits

    def get_my_tddcycles(self):
        return self.TDDCycles

    def get_nbr_valid_cycles(self):
        valid_cycles = 0
        for my_t_d_d_cycle in self.TDDCycles:
            if my_t_d_d_cycle is not None:
                if my_t_d_d_cycle.is_cycle_valid():
                    valid_cycles += 1
        return valid_cycles

    def set_my_commit_totals(self, value):
        self.myCommitTotals = value


if __name__ == "__main__":
    Assignment.loadAssignments()
