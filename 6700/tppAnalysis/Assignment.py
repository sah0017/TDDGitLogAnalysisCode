'''
Created on Apr 7, 2016

@author: susanha
'''
import time
import ConfigParser
import Transformations
import AssignmentTotals



class Assignment(object):
    '''
    classdocs
    '''
    '''
    Assignment3 = date(2017,3,20)
    Assignment4 = date(2017,3,27)

    assignmentNameDict = {Assignment3:"Assignment3", Assignment4:"Assignment4"}
    '''
    @classmethod
    def loadAssignments(self):
        myConfig = ConfigParser.SafeConfigParser() 
        myConfig.read("TDDanalysis.cfg")
        self.myFirstAssignment = myConfig.get("Assignments","BaseName") + myConfig.get("Assignments","FirstTDDAssignment")
        self.assignmentNameDict = {}
        for key, val in myConfig.items("Due Dates"):
            self.assignmentNameDict[key] = time.strptime(val,"%Y, %m, %d")
        #print self.assignmentNameDict
    
    @classmethod
    def getMyFirstAssignment(self):
        return self.myFirstAssignment   
    
    @classmethod
    def get_assignment_name_dict(self):
        return self.assignmentNameDict

    def __init__(self,assnName):
        '''
        Constructor
        '''
        self.assignmentName = assnName
        self.myCommits = []
        self.myCommitTotals = []
        self.consecutiveRedLights = 0
        self.consecutiveGreenLights = 0


    def incrementConsecutiveRedLights(self):
        self.consecutiveRedLights += 1

    def incrementConsecutiveGreenLights(self):
        self.consecutiveGreenLights += 1

    def getConsecutiveRedLights(self):
        return self.consecutiveRedLights

    def getConsecutiveGreenLights(self):
        return self.consecutiveGreenLights

    def addCommitToAssignment(self, commit):
        self.myCommits.append(commit)
        
    def addCommitTotalsToAssignment(self, commitTotals):
        self.myCommitTotals.append(commitTotals)
    


    def get_assignment_nbr(self):
        return self.__assignmentNbr


    def get_my_commits(self):
        return self.__myCommits


    def get_my_commit_totals(self):
        return self.__myCommitTotals


    def set_assignment_dict(self, value):
        self.__assignmentDict = value


    def set_assignment_nbr(self, value):
        self.__assignmentNbr = value


    def set_my_commits(self, value):
        self.__myCommits = value


    def set_my_commit_totals(self, value):
        self.__myCommitTotals = value


    def del_assignment_dict(self):
        del self.__assignmentDict


    def del_assignment_nbr(self):
        del self.__assignmentNbr


    def del_my_commits(self):
        del self.__myCommits


    def del_my_commit_totals(self):
        del self.__myCommitTotals
        
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
        nbrGreenLight = 0
        nbrRefactor = 0
        nbrUnknownCommit = 0
        nbrTransformations = 0
        nbrAntiTransformations = 0
        ratio = 0
        outFile.write("\r\n*********************************\r\nAssignment Name:" + str(self.assignmentName)+"\r\n*********************************")
        outFile.write("\r\nConsecutive Green Lights:  " + str(self.getConsecutiveGreenLights()) + "\tConsecutive Red Lights:  " + str(self.getConsecutiveRedLights()))
        nbrCommits = nbrCommits + len(self.myCommits)
        for myCommit in self.myCommits:
            outFile.write("\r\n------------------------------\r\n\tCommit Number:" + str(myCommit.commitNbr) + "\tCommit type: " + myCommit.commitType + "\tAdded lines:" + str(myCommit.addedLinesInCommit) + ".  Deleted lines:" + str(myCommit.deletedLinesInCommit) + ".\r\n\t  Added test lines:" + str(myCommit.addedTestLOC) + "  Deleted test lines:" + str(myCommit.deletedTestLOC) + ".\r\n\t  Test files:" + str(myCommit.nbrTestFiles) + ".  Production files:" + str(myCommit.nbrProdFiles) + ".  Number of Transformations:  " + str(myCommit.numberOfTransformations) + ". \n\r")
            if myCommit.get_commit_type()=="Red Light":
                nbrRedLight = nbrRedLight + 1
            elif myCommit.get_commit_type()=="Green Light":
                nbrGreenLight = nbrGreenLight + 1
            elif myCommit.get_commit_type()=="Refactor":
                nbrRefactor = nbrRefactor + 1
            else:
                nbrUnknownCommit = nbrUnknownCommit + 1
            addedLines = addedLines + myCommit.addedLinesInCommit
            addedTestLines = addedTestLines + myCommit.addedTestLOC
            deletedLines = deletedLines + myCommit.deletedLinesInCommit
            deletedTestLines = deletedTestLines + myCommit.deletedTestLOC
            myTrans = myCommit.get_transformations()
            outFile.write("\tTransformations:")
            for myTran in myTrans:
                outFile.write("\r\t" + myTransNames.getTransformationName(myTran))
                if myTran >= 0:
                    self.__transTotalsInAnalysis[myTran] = self.__transTotalsInAnalysis[myTran] + 1
                    transTotalsInAssignment[myTran] = transTotalsInAssignment[myTran] + 1
                    nbrTransformations = nbrTransformations + 1
                else:
                    self.__antitransTotalsInAnalysis[abs(myTran)] = self.__antitransTotalsInAnalysis[abs(myTran)] + 1
                    antitransTotalsInAssignment[abs(myTran)] = antitransTotalsInAssignment[abs(myTran)] + 1
                    nbrAntiTransformations = nbrAntiTransformations + 1
        
        overallDeletedLines = deletedLines + deletedTestLines
        outFile.write("\r\n============================================\r\nTotal test code lines added:" + str(addedTestLines))
        outFile.write("\r\nTotal production code lines added:" + str(addedLines))
        outFile.write("\r\nTotal test code lines deleted:" + str(deletedTestLines))
        outFile.write("\r\nTotal production code lines deleted:" + str(deletedLines))
        if addedLines > 0:
            ratio = addedTestLines / float(addedLines)
            outFile.write("\r\nRatio of test code to production code:" + format(ratio, '.2f') + ":1\r\n============================================")
        self.add_to_total_commits_in_analysis(nbrCommits)
        self.__totalTransformationsInAnalysis = self.__totalTransformationsInAnalysis + nbrTransformations
        self.__totalAntiTransformationsInAnalysis = self.__totalAntiTransformationsInAnalysis + nbrAntiTransformations
        self.__totalLinesOfCodeInAnalysis = self.__totalLinesOfCodeInAnalysis + addedLines
        myCommitStats = AssignmentTotals.AssignmentTotals()
        myCommitStats.nbrCommits = nbrCommits
        myCommitStats.RLCommit = nbrRedLight
        myCommitStats.GLCommit = nbrGreenLight
        myCommitStats.refCommit = nbrRefactor
        myCommitStats.otherCommit = nbrUnknownCommit
        myCommitStats.addedLinesInAssignment = addedLines
        myCommitStats.addedTestLOCInAssignment = addedTestLines
        myCommitStats.deletedLinesInAssignment = deletedLines
        myCommitStats.deletedTestLOCInAssignment = deletedTestLines
        myCommitStats.totalDelLines = overallDeletedLines
        myCommitStats.totalTransByTypeInAssignment = transTotalsInAssignment
        myCommitStats.totalAntiTransByTypeInAssignment = antitransTotalsInAssignment


    assignmentName = property(get_assignment_nbr, set_assignment_nbr, del_assignment_nbr, "assignmentName's docstring")
    myCommits = property(get_my_commits, set_my_commits, del_my_commits, "myCommits's docstring")
    myCommitTotals = property(get_my_commit_totals, set_my_commit_totals, del_my_commit_totals, "myCommitTotals's docstring")


if __name__ == "__main__":
    Assignment.loadAssignments()
    
