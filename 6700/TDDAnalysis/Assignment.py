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


class Assignment(object):
    """
    classdocs
    """
    """ **********************  class variables and methods  **********************   """
    assignmentNameDict = {}
    recommendations_dict = {}
    keyIndexList = []
    originalAssignment = None

    @classmethod
    def is_first_assignment(cls, commitDate):
        if commitDate <= cls.assignmentNameDict[cls.keyIndexList[0]]:
            return True
        else:
            return False

    """
    This method uses the date on the commit to determine which assignment the commit goes with
    """
    @classmethod
    def get_curr_assignmentName(cls, commitDate):
        for k in range(0, len(cls.keyIndexList)-1):
            if (cls.assignmentNameDict[cls.keyIndexList[k]] <= commitDate <= cls.assignmentNameDict[cls.keyIndexList[k+1]]):
                return cls.keyIndexList[k+1]


    @classmethod
    def loadAssignments(cls):
        myConfig = ConfigParser.SafeConfigParser() 
        myConfig.read("TDDanalysis.cfg")
        cls.originalAssignment = myConfig.get("Assignments","BaseName") + myConfig.get("Assignments","FirstAssignment")

        for key, val in myConfig.items("Due Dates"):
            cls.assignmentNameDict[key] = time.strptime(val,"%Y, %m, %d")
        cls.keyIndexList = cls.assignmentNameDict.keys()
        cls.keyIndexList.sort()
        for key, val in myConfig.items("Recommendations"):
            cls.recommendations_dict[key] = val

    @classmethod
    def getMyFirstAssignment(cls):
        return cls.originalAssignment
    
    @classmethod
    def get_assignment_name_dict(cls):
        return cls.assignmentNameDict

    @classmethod
    def get_assignment_list(cls):
        assignment_name_list = cls.assignmentNameDict.keys()
        return assignment_name_list
    """ **********************  end class variables and methods  **********************   """

    def __init__(self,assnName):
        """
        Constructor
        """
        self.assignmentName = assnName
        self.myCommits = []
        self.myCommitTotals = []
        self.consecutiveCommitsOfSameTypeList = []
        self.consecutiveRedLights = 0
        self.consecutiveGreenLights = 0
        self.tdd_commit_grades = []
        self.tdd_grade = 0
        self.TDDCycles = []

    def analyzeAssignment(self, fileIOobject):
        __commits = 0
        prevCommit = None
        line = fileIOobject.getCurrentLine()
        tddCycleContainsGreenLight = True
        myTddCycle = None

        # line = fileIOobject.readNextLine()          # commit date
        while line != False:
            __assignmentName = self.findCurrentAssignment(line)  # advances to next line to check the commit date
            if self.assignmentName != __assignmentName:
                return  __assignmentName                    # we've moved to a new assignment, done with this one

            __commits = __commits + 1
            myNewCommit = Commit.Commit(__commits, fileIOobject)
            self.addCommitToAssignment(myNewCommit.analyzeCommit(fileIOobject, line))
            newCommitType = myNewCommit.get_commit_type()
            myNewCommit.set_commit_validity(newCommitType)
            if prevCommit == newCommitType:            # looking for consecutive Red or Green Lights
                if newCommitType == "Red Light":
                    self.incrementConsecutiveRedLights()
                elif newCommitType == "Green Light":
                    self.incrementConsecutiveGreenLights()

                myConsCommit = ConsecutiveCommitsOfSameType.ConsecutiveCommitsOfSameType(newCommitType,
                                                                                         __commits-1,__commits)
                fileList = self.myCommits[__commits-2].get_file_names_list()
                myConsCommit.setFirstCommitList(fileList)
                fileList = self.myCommits[__commits-1].get_file_names_list()
                myConsCommit.setSecondCommitList(fileList)
                self.consecutiveCommitsOfSameTypeList.append(myConsCommit)
            elif newCommitType == "Green Light":
                tddCycleContainsGreenLight = True
            elif prevCommit is None and newCommitType != "Red Light":
                myTddCycle = self.addNewTDDCycle(False)
            else:
                if newCommitType == "Red Light" and tddCycleContainsGreenLight:
                    self.addTddCycleToAssignment(myTddCycle)
                    myTddCycle = self.addNewTDDCycle(True)
                    tddCycleContainsGreenLight = False
            myTddCycle = self.addCommitToTDDCycle(myTddCycle, myNewCommit)
            prevCommit = newCommitType
            line = fileIOobject.readNextLine()
        self.addTddCycleToAssignment(myTddCycle)
        return False

    def addNewTDDCycle(self, startsWithRL):
        return TDDCycle.TDDCycle(startsWithRL)

    def addCommitToTDDCycle(self, myTddCycle, commit):
        if myTddCycle is None:
            myTddCycle = self.addNewTDDCycle(False)
        myTddCycle.addCommit(commit)
        return myTddCycle

    def addTddCycleToAssignment(self, tddCycle):
        self.TDDCycles.append(tddCycle)

    def findCurrentAssignment(self, line):
        """ a git file can contain multiple assignments.  This is looking for the current one for analysis."""
        # line after commit contains the commit date.  Use this date to determine which assignment commit belongs in
        dateLine = line.split("-")
        commitDate = strptime(dateLine[0].strip(), '%a %b %d %X %Y')

        if Assignment.is_first_assignment(commitDate):
            currAssignmentName = Assignment.originalAssignment
        else:
            currAssignmentName = Assignment.get_curr_assignmentName(commitDate)
        return currAssignmentName


    def CalculateMyCommitStats(self, outFile):
        """
        This method calculates the commit stats for an assignment and creates the individual report file (.gitout)
        :param outFile: the file handle for the report file
        :return: my_assignment_stats - the total of all the different statistics we're tracking
        """
        myTransNames = Transformations.Trans()
        Commit.Commit.load_grade_criteria()
        grader = TDDGrade.TDDGradeRubric()
        #RecDict = self.loadRecommendations()
        transTotalsInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        antitransTotalsInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0]
        assignment_commit_tdd_grades = []
        addedLines = 0
        addedTestLines = 0
        deletedLines = 0
        deletedTestLines = 0
        nbrCommits = 0
        nbrRedLight = 0
        nbrInvalidRL = 0
        nbrGreenLight = 0
        nbrInvalidGL = 0
        nbrRefactor = 0
        nbrUnknownCommit = 0
        nbrTransformations = 0
        nbrAntiTransformations = 0
        ratio = 0
        outFile.write("\r\n*********************************\r\nAssignment Name:" + str(self.assignmentName)+
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
        outFile.write("\r\nNumber of TDD Cycles:  " + str(len(self.TDDCycles)))
        if gl_avg_length > 0 or gl_longest_consec > 0:
            outFile.write("\r\nLongest Streak of Consecutive Green Lights:  " + str(gl_longest_consec) +
                      "\tAverage Length of Consecutive Green Light Streaks:  " + str(gl_avg_length))
        if rl_avg_length > 0 or rl_longest_consec > 0:
            outFile.write("\r\nLongest Streak of Consecutive Red Lights:  " + str(rl_longest_consec) +
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
        nbrCommits = nbrCommits + len(self.myCommits)
        for myCommit in self.myCommits:
            ctype = myCommit.get_commit_type()
            commit_validity = myCommit.get_commit_validity()
            if ctype == "Red Light":
                nbrRedLight = nbrRedLight + 1
                if commit_validity == "INVALID":
                    nbrInvalidRL += 1

            elif ctype == "Green Light":
                nbrGreenLight = nbrGreenLight + 1
                if commit_validity == "INVALID":
                    nbrInvalidGL += 1
            elif ctype == "Refactor":
                nbrRefactor = nbrRefactor + 1
            else:
                nbrUnknownCommit = nbrUnknownCommit + 1
            outFile.write("\r\n------------------------------\r\n\tCommit Number:" + str(myCommit.commit_nbr) +
                          "\tCommit type: " + myCommit.commitType)  # + "    Validity value -- " + commit_validity)  SAH temporarily removed
            commit_tdd_grade = myCommit.calculate_tdd_grade()
            outFile.write("\t  Commit TDD Score:  " + str(commit_tdd_grade))
            if commit_validity == "INVALID":
                outFile.write("\r\nCommit Feedback")
                invalid_reason = myCommit.get_invalid_reason()
                for r in invalid_reason:
                    outFile.write("\r\n"+Assignment.recommendations_dict[r])
            self.tdd_commit_grades.append(commit_tdd_grade)
            outFile.write("\n\r\tAdded lines:" +
                          str(myCommit.added_lines_in_commit) + ".  Deleted lines:" +
                          str(myCommit.deleted_lines_in_commit) + ".\r\n\t  Added test lines:" +
                          str(myCommit.added_test_loc) + "  Deleted test lines:" +
                          str(myCommit.deleted_test_loc) + ".\r\n\t  Test files:" + str(myCommit.nbr_test_files) +
                          ".  Production files:" + str(myCommit.nbr_prod_files) + ".  Number of Transformations:  " +
                          str(myCommit.number_of_transformations) + ".\r\n")

            addedLines = addedLines + myCommit.added_lines_in_commit
            addedTestLines = addedTestLines + myCommit.added_test_loc
            deletedLines = deletedLines + myCommit.deleted_lines_in_commit
            deletedTestLines = deletedTestLines + myCommit.deleted_test_loc
            myFiles = myCommit.get_file_list()

            for myFile in myFiles:
                myTrans = myFile.get_transformations()
                outFile.write("\n\r\tTransformations to file:  " + myFile.getFileName() +
                              "  (" + myFile.getFileType() + ")")
                for myTran in myTrans:
                    outFile.write("\r\t" + myTransNames.getTransformationName(myTran))

                    if myTran >= 0:
                        #transTotalsInAnalysis[myTran] = transTotalsInAnalysis[myTran] + 1
                        transTotalsInAssignment[myTran] = transTotalsInAssignment[myTran] + 1
                        nbrTransformations = nbrTransformations + 1
                    else:
                        #self.__antitransTotalsInAnalysis[abs(myTran)] = self.__antitransTotalsInAnalysis[abs(myTran)] + 1
                        antitransTotalsInAssignment[abs(myTran)] = antitransTotalsInAssignment[abs(myTran)] + 1
                        nbrAntiTransformations = nbrAntiTransformations + 1
            my_assignment_stats = AssignmentTotals.AssignmentTotals()
            my_assignment_stats.nbrCommits = nbrCommits
            my_assignment_stats.RLCommit = nbrRedLight
            my_assignment_stats.add_invalid_rl_commits(nbrInvalidRL)
            my_assignment_stats.GLCommit = nbrGreenLight
            my_assignment_stats.add_invalid_gl_commits(nbrInvalidGL)
            my_assignment_stats.refCommit = nbrRefactor
            my_assignment_stats.otherCommit = nbrUnknownCommit
            my_assignment_stats.addedLinesInAssignment = addedLines
            my_assignment_stats.addedTestLOCInAssignment = addedTestLines
            my_assignment_stats.deletedLinesInAssignment = deletedLines
            my_assignment_stats.deletedTestLOCInAssignment = deletedTestLines
            overallDeletedLines = deletedLines + deletedTestLines
            my_assignment_stats.totalDelLines = overallDeletedLines
            my_assignment_stats.totalTransByTypeInAssignment = transTotalsInAssignment
            my_assignment_stats.totalAntiTransByTypeInAssignment = antitransTotalsInAssignment

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
        outFile.write("\r\n============================================\r\nTotal test code lines added:" + str(addedTestLines))
        outFile.write("\r\nTotal production code lines added:" + str(addedLines))
        outFile.write("\r\nTotal test code lines deleted:" + str(deletedTestLines))
        outFile.write("\r\nTotal production code lines deleted:" + str(deletedLines))
        if addedLines > 0:
            ratio = addedTestLines / float(addedLines)
            outFile.write("\r\nRatio of test code to production code:" + format(ratio, '.2f') + ":1")
        outFile.write("\r\nTDD Score:  " + str(self.tdd_grade))
        if self.tdd_grade == "N/A":
            outFile.write("\r\nNo Red or Green Light commits found ")
        else:
            outFile.write("\r\nGrade Components:  Average Red Light Length - " + str(rl_avg_length) +
                      ";  Average Green Light Length - " + str(gl_avg_length) +
                      ";  Average of TDD Commit Scores - " + str(tdd_commit_avg_grade))
        outFile.write("\r\n============================================\r\n\r\n")
        """
        self.add_to_total_commits_in_analysis(nbrCommits)
        self.__totalTransformationsInAnalysis = self.__totalTransformationsInAnalysis + nbrTransformations
        self.__totalAntiTransformationsInAnalysis = self.__totalAntiTransformationsInAnalysis + nbrAntiTransformations
        self.__totalLinesOfCodeInAnalysis = self.__totalLinesOfCodeInAnalysis + addedLines
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

    def getReasonsForConsecutiveCommits(self, commitType):
        reasonList = [0,0,0,0]
        reasonString = ""
        for r in self.consecutiveCommitsOfSameTypeList:
            if r.consCommitType == commitType:
                reason = r.reasonForDuplicateTypes()
                reasonList[reason] += 1
        for s in reasonList:
            reasonString = reasonString + ", " + str(s)
        return reasonString

    def addCommitToAssignment(self, commit):
        self.myCommits.append(commit)

    def addCommitTotalsToAssignment(self, commitTotals):
        self.myCommitTotals.append(commitTotals)

    def get_my_commit_totals(self):
        return self.myCommitTotals

    def get_my_commits(self):
        return self.myCommits

    def get_my_tddcycles(self):
        return self.TDDCycles

    def get_nbr_valid_cycles(self):
        valid_cycles = 0
        for myTDDCycle in self.TDDCycles:
            if myTDDCycle != None:
                if myTDDCycle.is_cycle_valid():
                    valid_cycles += 1
        return valid_cycles


    def set_my_commit_totals(self, value):
        self.myCommitTotals = value
if __name__ == "__main__":
    Assignment.loadAssignments()
