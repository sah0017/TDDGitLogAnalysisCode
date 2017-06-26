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

    def createProcessConformanceReport(self, reportRoot, analysisRoot, item):
        myGitFile = GitFile.GitFile()
        if os.path.isfile(os.path.join(analysisRoot, item)):
            fileName, ext = os.path.splitext(item)
            studentName = fileName.split("_")
            print 'Processing ' + studentName[0]
            if ext == ".json":
                currentGitFile = myGitFile.retrieveGitReportObject(analysisRoot + os.sep + fileName)
                if (currentGitFile != None):
                    self.outFile = open(reportRoot + os.sep + studentName[0] + "ProcessConformanceReport" + ".csv", "w")
                    self.outFile.write("Assignment Name, Total Commits, Invalid Red Light Commits, "
                                       "Invalid Green Light Commits, "
                                       "Nbr of Commits with Too Many Transactions, Nbr of Invalid Commits,"
                                       "Nbr TDD Cycles, Nbr Valid TDD Cycles")
                    self.collectProcessConformanceData(currentGitFile, self.outFile)
                    self.outFile.close()

    def collectProcessConformanceData(self, gitFile, outFile):
        assignmentsList = gitFile.getAssignments()
        for assignment in assignmentsList:
            commits = assignment.get_my_commits()
            tddCycles = assignment.get_my_tddcycles()
            invalidRL = 0
            invalidGL = 0
            for myCommit in commits:
                if myCommit.get_commit_validity() == "INVALID":
                    if myCommit.get_commit_type() == "Red Light":
                        invalidRL += 1
                    else:
                        invalidGL += 1
            self.invalidRedLights = invalidRL
            self.invalidGreenLights = invalidGL
            validCycles = 0
            for myTDDCycle in tddCycles:
                if myTDDCycle != None:
                    if myTDDCycle.is_cycle_valid():
                        validCycles += 1
            outFile.write("\r" + assignment.assignmentName + ", " +
                                str(len(commits)) + ", " +
                                str(self.invalidRedLights) + ", " +
                               str(self.invalidGreenLights) + ", " +
                               str(len(tddCycles)) + ", " +
                               str(validCycles))



if __name__ == '__main__':
    myReport = ProcessConformance()
    myReport.createProcessConformanceReport("/Users/shammond/Google Drive/6700Spring17",
                                            "/Users/shammond/Google Drive/6700Spring17/Assignment5",
                                            "anakinlauLog.json")

