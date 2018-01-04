'''
Created on June 6, 2017

@author: susanha
'''
import ConfigParser

import GitFile
import Assignment
import AssignmentTotals
import Commit
import os
import FormattedGitLog

class ProcessConformance(object):
    '''
    The ProcessConformance object will collect the various pieces of data we will use to try and
    determine TDD and TPP process conformance.  Will result in data to be used in a radar chart.
    '''

    def init(self):
        self.invalidRedLights = 0
        self.invalidGreenLights = 0

    def createProcessConformanceReport(self, reportRoot, analysisRoot, fileName, studentName):
        myGitFile = GitFile.GitFile()
        currentGitFile = myGitFile.retrieveGitReportObject(analysisRoot + os.sep + fileName)
        if (currentGitFile != None):
            self.outFile = open(reportRoot + os.sep + studentName + "ProcessConformanceReport" + ".csv", "w")
            self.outFile.write("Assignment Name, Total Commits, Red Light Validity Ratio, "
                               "Green Light Validity Ratio, "
                               "TPP Conformance Ratio, "
                               "Nbr TDD Cycles, Nbr Valid TDD Cycles, Nbr Ideal Cycles")
            self.collectProcessConformanceData(currentGitFile, self.outFile)
            self.outFile.close()

    def collectProcessConformanceData(self, gitFile, outFile):
        assignmentsList = gitFile.getAssignments()
        for assignment in assignmentsList:
            commits = assignment.get_my_commits()
            tddCycles = assignment.get_my_tddcycles()
            if tddCycles is None:
                nbrTDDCycles = 0
            else:
                nbrTDDCycles = len(tddCycles)
            idealCycles = 0
            commitStats = assignment.get_my_commit_totals()
            for cstats in commitStats:
                idealCycles += cstats.get_ideal_number_of_cycles()
            totalRL = 0
            invalidRL = 0
            invalidGL = 0
            totalGL = 0
            commitsWithTooManyTrans = 0
            for myCommit in commits:
                if myCommit.get_number_of_transformations() > 1:
                    commitsWithTooManyTrans += 1
                commitValidity = myCommit.get_commit_validity()
                commitType = myCommit.get_commit_type()
                if commitType == "Red Light":
                    totalRL += 1
                    if commitValidity == "INVALID":
                        invalidRL += 1
                elif commitType == "Green Light":
                    totalGL += 1
                    if commitValidity == "INVALID":
                        invalidGL += 1
            self.invalidRedLights = invalidRL
            self.invalidGreenLights = invalidGL
            validCycles = 0
            for myTDDCycle in tddCycles:
                if myTDDCycle != None:
                    if myTDDCycle.is_cycle_valid():
                        validCycles += 1
            nbrOfCommits = len(commits)
            if totalRL == 0:
                invalidRLratio = 0.0
            else:
                invalidRLratio = (totalRL-self.invalidRedLights)/float(totalRL)
            if totalGL == 0:
                invalidGLratio = 0.0
            else:
                invalidGLratio = (totalGL-self.invalidGreenLights)/float(totalGL)
            if nbrOfCommits == 0:
                TPPConformanceRatio = 0.0
            else:
                TPPConformanceRatio = (nbrOfCommits-commitsWithTooManyTrans)/float(nbrOfCommits)
            outFile.write("\r" + assignment.assignmentName + ", " +
                                str(nbrOfCommits) + ", " +
                                format(invalidRLratio, '.2f') + ", " +
                                format(invalidGLratio, '.2f') + ", " +
                                format(TPPConformanceRatio, '.2f') + ", " +
                                str(nbrTDDCycles) + ", " +
                                str(validCycles) + ", " +
                                str(idealCycles))



if __name__ == '__main__':
    myConfig = ConfigParser.ConfigParser()
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    printToFile = True
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    analysisRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment)
    reportRoot = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester)
    myReport = ProcessConformance()

    for gitDataFile in os.listdir(analysisRoot):
        if os.path.isfile(os.path.join(analysisRoot, gitDataFile)):
            fileName, ext = os.path.splitext(gitDataFile)
            if ext == ".json":
                studentName = fileName.split("_")
                print 'Processing ' + studentName[0]
                myReport.createProcessConformanceReport(reportRoot,
                                                        analysisRoot,
                                                        fileName, studentName[0])

