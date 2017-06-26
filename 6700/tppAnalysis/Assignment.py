'''
Created on Apr 7, 2016

@author: susanha
'''
import time
import ConfigParser
import Transformations
import AssignmentTotals
import Commit
import FileHandler
from time import strptime
import ConsecutiveCommitsOfSameType
import TDDCycle


class Assignment(object):
    '''
    classdocs
    '''
    ''' **********************  class variables and methods  **********************   '''
    assignmentNameDict = {}
    keyIndexList = []
    originalAssignment = None

    @classmethod
    def is_first_assignment(cls, commitDate):
        if commitDate <= cls.assignmentNameDict[cls.keyIndexList[0]]:
            return True
        else:
            return False

    '''
    This method uses the date on the commit to determine which assignment the commit goes with
    '''
    @classmethod
    def get_curr_assignmentName(cls, commitDate):
        for k in range(0, len(cls.keyIndexList)-1):
            if (cls.assignmentNameDict[cls.keyIndexList[k]] <= commitDate <= cls.assignmentNameDict[cls.keyIndexList[k+1]]):
                return cls.keyIndexList[k+1]


    @classmethod
    def loadAssignments(cls):
        myConfig = ConfigParser.SafeConfigParser() 
        myConfig.read("TDDanalysis.cfg")
        cls.originalAssignment = myConfig.get("Assignments","BaseName") + myConfig.get("Assignments","FirstTDDAssignment")

        for key, val in myConfig.items("Due Dates"):
            cls.assignmentNameDict[key] = time.strptime(val,"%Y, %m, %d")
        cls.keyIndexList = cls.assignmentNameDict.keys()
        cls.keyIndexList.sort()

    @classmethod
    def getMyFirstAssignment(cls):
        return cls.originalAssignment
    
    @classmethod
    def get_assignment_name_dict(cls):
        return cls.assignmentNameDict
    ''' **********************  end class variables and methods  **********************   '''

    def __init__(self,assnName):
        '''
        Constructor
        '''
        self.assignmentName = assnName
        self.myCommits = []
        self.myCommitTotals = []
        self.consecutiveCommitsOfSameTypeList = []
        self.consecutiveRedLights = 0
        self.consecutiveGreenLights = 0
        self.TDDPoints = 0.0
        self.TDDGrade = 0.0
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
                if newCommitType=="Red Light":
                    self.incrementConsecutiveRedLights()
                elif newCommitType=="Green Light":
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
        " a git file can contain multiple assignments.  This is looking for the current one for analysis."
        # line after commit contains the commit date.  Use this date to determine which assignment commit belongs in
        dateLine = line.split("-")
        commitDate = strptime(dateLine[0].strip(), '%a %b %d %X %Y')

        if Assignment.is_first_assignment(commitDate):
            currAssignmentName = Assignment.originalAssignment
        else:
            currAssignmentName = Assignment.get_curr_assignmentName(commitDate)
        return currAssignmentName


    def CalculateMyCommitStats(self, outFile):
        myTransNames = Transformations.Trans()
        transTotalsInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0,0]
        antitransTotalsInAssignment = [0,0,0,0,0,0,0,0,0,0,0,0]
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
        outFile.write("\r\nNumber of TDD Cycles:  " + str(len(self.TDDCycles)) +
                      "\tConsecutive Green Lights:  " + str(self.getConsecutiveGreenLights()) +
                      "\tConsecutive Red Lights:  " + str(self.getConsecutiveRedLights()) +
                      "\r\nConsecutive Commits of Same Type:  " + str(len(self.consecutiveCommitsOfSameTypeList)))
        for ConsCommits in self.consecutiveCommitsOfSameTypeList:
            outFile.write("\n\r\tCommit Type:  " + ConsCommits.consCommitType +
                          "\n\r\t\tFirst Commit:  " + str(ConsCommits.firstCommitNbr) +
                          "\tFirst Commit File List:  ")
            for f in ConsCommits.firstCommitFileList:
                outFile.write(f + "\t")
            outFile.write("\n\r\t\tSecond Commit:  " + str(ConsCommits.secondCommitNbr) +
                          "\tSecond Commit File List:  ")
            for f in ConsCommits.secondCommitFileList:
                outFile.write(f + "\t")
        nbrCommits = nbrCommits + len(self.myCommits)
        for myCommit in self.myCommits:
            ctype = myCommit.get_commit_type()
            commit_validity = myCommit.get_commit_validity()
            if ctype=="Red Light":
                nbrRedLight = nbrRedLight + 1
                if commit_validity == "INVALID":
                    nbrInvalidRL += 1

            elif ctype=="Green Light":
                nbrGreenLight = nbrGreenLight + 1
                if commit_validity == "INVALID":
                    nbrInvalidGL += 1
            elif ctype=="Refactor":
                nbrRefactor = nbrRefactor + 1
            else:
                nbrUnknownCommit = nbrUnknownCommit + 1
            outFile.write("\r\n------------------------------\r\n\tCommit Number:" + str(myCommit.commitNbr) +
                          "\tCommit type: " + myCommit.commitType + ". Validity value -- " + commit_validity +
                          "\n\r\tAdded lines:" +
                          str(myCommit.addedLinesInCommit) + ".  Deleted lines:" +
                          str(myCommit.deletedLinesInCommit) + ".\r\n\t  Added test lines:" +
                          str(myCommit.addedTestLOC) + "  Deleted test lines:" +
                          str(myCommit.deletedTestLOC) + ".\r\n\t  Test files:" + str(myCommit.nbrTestFiles) +
                          ".  Production files:" + str(myCommit.nbrProdFiles) + ".  Number of Transformations:  " +
                          str(myCommit.numberOfTransformations) + ". \n\r")

            addedLines = addedLines + myCommit.addedLinesInCommit
            addedTestLines = addedTestLines + myCommit.addedTestLOC
            deletedLines = deletedLines + myCommit.deletedLinesInCommit
            deletedTestLines = deletedTestLines + myCommit.deletedTestLOC
            self.assignTDDPoints(commit_type=ctype, commit_validity=commit_validity,
                                 commitLOC=addedLines+addedTestLines, nbrTrans=myCommit.numberOfTransformations)
            myFiles = myCommit.get_file_list()
            '''
            outFile.write("\n\r#################################################### " +
                              "Summary of file transformations in this Assignment ##########################\n\r")
            '''
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
            myCommitStats = AssignmentTotals.AssignmentTotals()
            myCommitStats.nbrCommits = nbrCommits
            myCommitStats.RLCommit = nbrRedLight
            myCommitStats.add_invalid_rl_commits(nbrInvalidRL)
            myCommitStats.GLCommit = nbrGreenLight
            myCommitStats.add_invalid_gl_commits(nbrInvalidGL)
            myCommitStats.refCommit = nbrRefactor
            myCommitStats.otherCommit = nbrUnknownCommit
            myCommitStats.addedLinesInAssignment = addedLines
            myCommitStats.addedTestLOCInAssignment = addedTestLines
            myCommitStats.deletedLinesInAssignment = deletedLines
            myCommitStats.deletedTestLOCInAssignment = deletedTestLines
            overallDeletedLines = deletedLines + deletedTestLines
            myCommitStats.totalDelLines = overallDeletedLines
            myCommitStats.totalTransByTypeInAssignment = transTotalsInAssignment
            myCommitStats.totalAntiTransByTypeInAssignment = antitransTotalsInAssignment

        self.TDDGrade = self.calculateTDDGrade() * 100.0
        outFile.write("\r\n============================================\r\nTotal test code lines added:" + str(addedTestLines))
        outFile.write("\r\nTotal production code lines added:" + str(addedLines))
        outFile.write("\r\nTotal test code lines deleted:" + str(deletedTestLines))
        outFile.write("\r\nTotal production code lines deleted:" + str(deletedLines))
        if addedLines > 0:
            ratio = addedTestLines / float(addedLines)
            outFile.write("\r\nRatio of test code to production code:" + format(ratio, '.2f') + ":1\r\n")
        outFile.write("TDD Grade:  " + format(self.TDDGrade, '.2f') +
                      "\r\n============================================\r\n\r\n")
        '''
        self.add_to_total_commits_in_analysis(nbrCommits)
        self.__totalTransformationsInAnalysis = self.__totalTransformationsInAnalysis + nbrTransformations
        self.__totalAntiTransformationsInAnalysis = self.__totalAntiTransformationsInAnalysis + nbrAntiTransformations
        self.__totalLinesOfCodeInAnalysis = self.__totalLinesOfCodeInAnalysis + addedLines
        '''
        return myCommitStats

    def assignTDDPoints(self, commit_type=None, commit_validity=None, nbrTrans=None, commitLOC=None):
        if commit_validity == "Valid":
            self.TDDPoints += 1.0
        elif commit_validity == "INVALID":
            self.TDDPoints -= 1.0
        if commit_type == "Other":
            self.TDDPoints -= .5
        if nbrTrans == 1:
            self.TDDPoints += .5
        if commitLOC < 20:
            self.TDDPoints += .5
        elif commitLOC > 100:
            self.TDDPoints -= .5


    def calculateTDDGrade(self):
        return (self.TDDPoints - self.consecutiveRedLights/2 - self.consecutiveGreenLights/2)/len(self.myCommits)

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
        for r in self.consecutiveCommitsOfSameTypeList:
            if r.consCommitType == commitType:
                reason = r.reasonForDuplicateTypes()
                reasonList[reason] += 1
        reasonString = str(reasonList[0]) + ", " + str(reasonList[1]) + ", " + \
                       str(reasonList[2]) + ", " + str(reasonList[3])
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
        validCycles = 0
        for myTDDCycle in self.TDDCycles:
            if myTDDCycle != None:
                if myTDDCycle.is_cycle_valid():
                    validCycles += 1
        return validCycles


    def set_my_commit_totals(self, value):
        self.myCommitTotals = value

if __name__ == "__main__":
    Assignment.loadAssignments()
