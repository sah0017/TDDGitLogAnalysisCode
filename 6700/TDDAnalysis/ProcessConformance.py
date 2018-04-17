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
import CodeCoverage

class ProcessConformance(object):
    '''
    The ProcessConformance object will collect the various pieces of data we will use to try and
    determine TDD and TPP process conformance.  Will result in data to be used in a radar chart.
    '''

    def __init__(self):
        Assignment.Assignment.loadAssignments()
        self.assignmentList = Assignment.Assignment.get_assignment_list()
        self.myCodeCov = CodeCoverage.CodeCoverage()
        self.myCodeCov.loadCoverageReports(reportRoot, self.assignmentList)  # load up available code coverage reports; they're small, text-based files
        self.invalidRedLights = 0
        self.invalidGreenLights = 0
        self.masterFile = open(reportRoot + os.sep + "Overall Process Conformance Report.csv", "w")
        self.masterFile.write("Student Name\n  Assignment Name, Total Commits, Red Light Validity Ratio, "
                       "Green Light Validity Ratio, "
                       "TPP Conformance Ratio, "
                       "Nbr TDD Cycles, Nbr Valid TDD Cycles, Nbr Ideal Cycles, Code Coverage")
        self.masterFile.close()


    def createProcessConformanceReport(self, reportRoot, analysisRoot, fileName, studentName):
        myGitFile = GitFile.GitFile()
        currentGitFile = myGitFile.retrieveGitReportObject(analysisRoot + os.sep + fileName)
        if (currentGitFile != None):
            self.outFile = open(reportRoot + os.sep + studentName + " Process Conformance Report" + ".csv", "w")
            self.outFile.write("Assignment Name, Total Commits, Red Light Validity Ratio, "
                               "Green Light Validity Ratio, "
                               "TPP Conformance Ratio, "
                               "Nbr TDD Cycles, Nbr Valid TDD Cycles, Nbr Ideal Cycles, Code Coverage")
            self.collectProcessConformanceData(currentGitFile, self.outFile, reportRoot, studentName)
            self.outFile.close()

    def collectProcessConformanceData(self, gitFile, outFile, reportRoot, studentName):
        assignmentsList = gitFile.getAssignments()
        with open(os.path.join(reportRoot + os.sep + "Overall Process Conformance Report.csv"), "a+") as masterFile:
            masterFile.write("\n\n" + studentName + "\n")
        for assignment in assignmentsList:
            try:
                commits = assignment.get_my_commits()
            except:
                commits = None
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
            if commits is not None:
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
            studentName = studentName.replace(" ","")
            ccPct = self.myCodeCov.retrieveCodeCoverageForSpecificStudentAndAssignment(studentName, assignment.assignmentName)
            if isinstance(ccPct, float):
                ccPct = format(ccPct, '.2f')

            with open(os.path.join(reportRoot + os.sep + "Overall Process Conformance Report.csv"), "a+") as masterFile:
                masterFile.write("\r" + assignment.assignmentName + ", " +
                                str(nbrOfCommits) + ", " +
                                format(invalidRLratio, '.2f') + ", " +
                                format(invalidGLratio, '.2f') + ", " +
                                format(TPPConformanceRatio, '.2f') + ", " +
                                str(nbrTDDCycles) + ", " +
                                str(validCycles) + ", " +
                                str(idealCycles) + ", " +
                                str(ccPct))

            outFile.write("\r" + assignment.assignmentName + ", " +
                                str(nbrOfCommits) + ", " +
                                format(invalidRLratio, '.2f') + ", " +
                                format(invalidGLratio, '.2f') + ", " +
                                format(TPPConformanceRatio, '.2f') + ", " +
                                str(nbrTDDCycles) + ", " +
                                str(validCycles) + ", " +
                                str(idealCycles) + ", " +
                                str(ccPct))

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

