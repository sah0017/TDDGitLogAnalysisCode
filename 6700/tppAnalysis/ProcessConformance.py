'''
Created on June 6, 2017

@author: susanha
'''

import GitFile
import Assignment
import Commit
import os

class ProcessConformance(object):
    '''
    The ProcessConformance object will collect the various pieces of data we will use to try and
    determine TDD and TPP process conformance.  Will result in data to be used in a radar chart.
    '''

    def init(self):
        self.invalidRedLights = 0
        self.invalidGreenLights = 0
        self.TDDCycleNbrCommitsTooManyTrans = 0
        self.NbrInvalidCommits = 0

    def createProcessConformanceReport(self, reportRoot, analysisRoot, item):
        myGitFile = GitFile.GitFile()
        if os.path.isfile(os.path.join(analysisRoot, item)):
            fileName, ext = os.path.splitext(item)
            studentName = fileName.split("_")
            print 'Processing ' + studentName[0]
            if ext == ".json":
                currentGitFile = myGitFile.retrieveGitReportObject(analysisRoot + os.sep + fileName)
                if (currentGitFile != None):
                    self.collectProcessConformanceData(currentGitFile)
                    self.outFile = open(reportRoot + os.sep + studentName[0] + "ProcessConformanceReport" + ".csv", "w")
                    self.collectProcessConformanceData(currentGitFile)
                    self.outFile.write("Invalid Red Light Commits\tInvalid Green Light Commits\t"
                                       "Nbr of Commits with Too Many Transactions\tNbr of Invalid Commits")
                    self.outFile.write(str(self.invalidRedLights)+str(self.invalidGreenLights) +
                                       str(self.TDDCycleNbrCommitsTooManyTrans) + str(self.NbrInvalidCommits))
                    self.outFile.close()

    def collectProcessConformanceData(self, gitFile):
        assignmentsList = gitFile.getAssignments()
        for assignment in assignmentsList:
            commits = assignment.get_my_commits()
            tddCycles = assignment.get_my_tddcycles()
            invalidRL = 0
            invalidGL = 0
            for myCommit in commits:
                if not myCommit.validCommit:
                    if myCommit.get_commit_type() == "Red Light":
                        invalidRL += 1
                    else:
                        invalidGL += 1
            self.invalidRedLights = invalidRL
            self.invalidGreenLights = invalidGL
            nbrCommitsWithTooManyTrans = 0
            nbrInvalidCommits = 0
            for myTDDCycle in tddCycles:
                nbrCommitsWithTooManyTrans += myTDDCycle.too_many_trans()
                nbrInvalidCommits += myTDDCycle.get_cycle_validity()
            self.TDDCycleNbrCommitsTooManyTrans = nbrCommitsWithTooManyTrans
            self.NbrInvalidCommits = nbrInvalidCommits



if __name__ == '__main__':
    myReport = ProcessConformance()
    myReport.createProcessConformanceReport("/Users/shammond/Google Drive/6700Spring17",
                                            "/Users/shammond/Google Drive/6700Spring17/Assignment5",
                                            "anakinlauLog.json")

