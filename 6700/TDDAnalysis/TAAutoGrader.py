'''
Created on Jul 1, 2016

@author: susanha

This program is called from the AutoGrader batch (for Windows) or shell script (for Mac).  AutoGrader
loops through the list of submissions (created by GetDirectoryList) and passes in the student path and
correct assignment to analyze.
The runTaTests method loads the TA test files and runs the student's tests against the
TA Test code.
'''
import sys, os, re, unittest, coverage
from unittest.runner import TextTestRunner
import ConfigParser
import json
import ast


class TAAutoGrader(object):
    FAIL = "fail_report"
    ERROR = "error_report"

    def __init__(self):
        self.myConfig = ConfigParser.ConfigParser()
        self.myConfig.read("TDDanalysis.cfg")
        self.myDrive = self.myConfig.get("Location","Root")
        self.myHome = self.myConfig.get("Location","Home")
        self.mySemester = self.myConfig.get("Location","Semester")
        self.myAssignment = self.myConfig.get("Location","Assignment")
        self.myProdPath = self.myConfig.get("Location","ProdPath")
        self.TATestLocation = self.myConfig.get("TA Test Case Location", "Test Directory")
        self.TATestPath = self.myDrive + os.sep + self.myHome + os.sep + self.mySemester + os.sep + self.TATestLocation
        self.namePathDepth = self.myConfig.getint("Location","Name Path Depth")


    def collectReportStats(self, report):

        failureStats = self.retrieveTAReportObject(TAAutoGrader.FAIL)
        if failureStats == None:
            failureStats = {}
        errorStats = self.retrieveTAReportObject(TAAutoGrader.ERROR)
        if errorStats == None:
            errorStats = {}


        for failedTestCase, failure in report.failures:
            if failureStats.has_key(failedTestCase._testMethodName):
                failureStats[failedTestCase._testMethodName] += 1
            else:
                failureStats[failedTestCase._testMethodName] = 1
        for errorCase, error in report.errors:
            if errorStats.has_key(errorCase._testMethodName):
                errorStats[errorCase._testMethodName] += 1
            else:
                errorStats[errorCase._testMethodName] = 1

        self.storeTAReportObject(TAAutoGrader.FAIL, failureStats)
        self.storeTAReportObject(TAAutoGrader.ERROR, errorStats)


    def runTATests(self, TAPath, prodPath, assignment):
        sys.stdout = open(TAPath+os.sep+'ta_test.stdout.log', 'a+')

        sys.path.insert(0,prodPath)

        testSuite = unittest.TestLoader().discover(TAPath,'*.py')

        with open(os.path.join(TAPath + assignment + ".TAreport"), "a+") as TAreportoutFile:
            try:
                sys.stdout.write("/n******************************************************************************************\n")
                sys.stdout.write("***  Student submission path:  " + prodPath + "\n")
                sys.stdout.write("******************************************************************************************\n")
                TAreport = TextTestRunner(stream=sys.stdout, verbosity=2).run(testSuite)
                TAreportoutFile.write("\n\rStudent submission path:  " + prodPath + "\n\r")
                TAreportoutFile.write("Number of tests run:  " + str(TAreport.testsRun) + "\n\r")
                if TAreport.wasSuccessful():
                    TAreportoutFile.write("All tests completed successfully!\n\r")
                else:
                    TAreportoutFile.write("See log for Content of TestRunner failures\r")
                    self.collectReportStats(TAreport)
            except Exception:
                TAreportoutFile.write("Import Error:  " + prodPath + "\n\r")

            TAreportoutFile.write("********************************************************************************\n\r")

    def storeTAReportObject(self, fileName, stats):
        out_s = open(os.path.join(self.TATestPath + os.sep + fileName + '.json'), 'w')

        # Write to the stream
        try:
            json.dump(stats, out_s, sort_keys=True)
        except Exception as e:
            print e
        out_s.close()

    def retrieveTAReportObject(self,filename):
        try:
            in_s = open(os.path.join(self.TATestPath + os.sep + filename +'.json'), 'r')

            # Read from the stream
            JSonStringObject = in_s.read()
            TAReportObject = json.loads(JSonStringObject)

            '''
            try:
                TAReportObject = json.load(JSonStringObject)
            except Exception as e:
                TAReportObject = None
            '''
            in_s.close()
        except:
            TAReportObject = None

        return TAReportObject

    def runAutoGrader(self, totalArgs):
        if totalArgs > 1:
            dataFile = str(sys.argv[1])
            assignmentStr = str(sys.argv[2]).split(".")
            myAutoGrader.assignment = assignmentStr[0]
        else:
            #dataFile = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
            dataFile = self.myDrive + os.sep + self.myHome + os.sep + self.mySemester + os.sep + self.myAssignment + os.sep + "submissions" + os.sep + "SaurabhGupta"
            myAutoGrader.assignment = self.myAssignment

        myAutoGrader.runTATests(os.path.join(self.TATestPath),
                                  os.path.join(dataFile + os.sep + self.myProdPath), myAutoGrader.assignment)

if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)

    #print os.getcwd()

    myAutoGrader = TAAutoGrader()
    myAutoGrader.runAutoGrader(totalArgs)

