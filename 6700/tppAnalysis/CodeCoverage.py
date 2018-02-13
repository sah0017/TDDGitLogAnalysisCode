'''
Created on Jul 1, 2016

@author: susanha

This program is called from the CodeCovAnalysis batch (for Windows) or shell script (for Mac).  CodeCovAnalysis
loops through the list of submissions and passes in the student path and assignment.
analyzeCodeCoverage method loops through the student's submission, finds and loads test files, starts
the code coverage analyzer, runs the student's tests against the student's code, the stops the CC analyzer.
'''
import sys, os, re, unittest, coverage
from unittest.runner import TextTestRunner
from coverage.misc import CoverageException
import time, traceback
from contextlib import contextmanager
# from py._iniconfig import SectionWrapper
import ConfigParser

errorDict = {-1:"Coverage Exception",
             -2:"Run Error",
             -3:"Import Error/Didn't get to student's tests"}
SUBPATH = 0
PRODPATH = 1
TESTPATH = 2
FILENAME = 3
@contextmanager
def redirect_stdout(new_target):
    old_target, sys.stdout = sys.stdout, new_target
    try:
        yield new_target
    finally:
        sys.stdout = old_target

class CodeCoverage(object):
    def __init__(self):
        '''
        Constructor
        '''
         
        #myConfig = ConfigParser.ConfigParser() 
        #myConfig.read("analysis.cfg")
        #self.root = myConfig.get("Location","Root")
        self.assignment = ""
        self.dataFile = ""
        self.namePathDepth = 0
        self.CCReport = {}


    def retrieveCodeCoverageForSpecificStudentAndAssignment(self, studentName, assignmentName):

        ccpct = "N/A"
        aLC = assignmentName.lower()
        try:
            students = self.CCReport[aLC].split()
            try:
                index = students.index(studentName)
                ccpct = students[index+1]
                print ccpct
            except:
                ccpct = "CC Error"    # student not found
        except:
            pass    # assignment not in code coverage list
        return ccpct

    def loadCoverageReports(self, root, assignmentList):
        for assignment in assignmentList:
            aLC = assignment.lower()
            ccFileName = root + os.sep + assignment + os.sep + assignment + ".cvgrpt"
            try:
                ccFile = open(ccFileName,"r")
                self.CCReport[aLC] = ccFile.read()
                ccFile.close()
            except Exception as e:
                pass    # report not found

        return

    def findStudentTestFiles(self, root):
        paths = ["","","",""]
        paths[SUBPATH] = ""
        nameSplit = root.split(os.sep)
        fileName = nameSplit[self.namePathDepth]
        paths[SUBPATH] = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep)
        studentName = fileName.split("_")
        print studentName[0]
        prodpath = os.path.join(root + os.sep + "softwareprocess")
        if (os.path.exists(os.path.join(prodpath,"prod"))):  # there is a prod directory is under softwareprocess dir
            prodpath = os.path.join(prodpath + os.sep + "prod")
        testpath = os.path.join(root + os.sep + "test")
        paths[SUBPATH] = paths[SUBPATH]
        paths[PRODPATH] = prodpath
        paths[TESTPATH] = testpath
        paths[FILENAME] = fileName
        if (os.path.exists(testpath)):      # test directory is off of the student ID directory
            testfiles = os.listdir(testpath)
        else:
            testpath = os.path.join(root + os.sep + "softwareprocess" + os.sep + "test")  # test directory is under softwareprocess dir
            testfiles = os.listdir(testpath)
        return testfiles, paths, studentName[0]

    def analyzeCodeCoverage(self, root, assignment, htmlReport):
        print root
        paths = []
        testfiles, paths, stuName = self.findStudentTestFiles(root)
        try:
            cov = coverage.Coverage(source=[paths[PRODPATH]],include="*.py", omit=[paths[TESTPATH]], branch=True, cover_pylib=False )
            #cov = coverage.Coverage(source=[root])
            with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("\n\rStudent submission and path:  " + root + "\n\r")
            prodfiles = os.listdir(paths[PRODPATH])
            sys.path.insert(0,root)
            sys.path.insert(0,paths[PRODPATH])
            sys.path.insert(0,paths[TESTPATH])
            os.chdir(paths[PRODPATH])

            myTestLoader = unittest.TestLoader()
            test = re.compile(r"\b.py\b", re.IGNORECASE)      # test is a compiled regular expression to search for python files
            testfiles = filter(test.search, testfiles)        # this will filter out any files that aren't python files
            prodfiles = filter(test.search, prodfiles)
            filenameToModuleName = lambda f: os.path.splitext(f)[0]  # this removes the python extension from test files
            moduleTestNames = map(filenameToModuleName, testfiles)
            #moduleProdNames = map(filenameToModuleName, prodfiles)

            cov.start()

        except Exception as e:
            with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,file=CCreportoutFile)
            #return -3, studentName[0]

        with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
            CCreportoutFile.write("Test File Names\n\r")
        for t in testfiles:
            with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
                    CCreportoutFile.write(t + "\r")

        load = myTestLoader.loadTestsFromNames(moduleTestNames)
        CCreport = TextTestRunner().run(load)
        with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
            CCreportoutFile.write("Number of tests run:  " + str(CCreport.testsRun) + "\n\r")
            if not CCreport.wasSuccessful():
                CCreportoutFile.write("Content of TestRunner failures\r")
                for failedTestCase, failure in CCreport.failures:
                    CCreportoutFile.write(str(failedTestCase) + failure + "\n\r")
            else:
                CCreportoutFile.write("All tests completed successfully!\n\r")
            CCreportoutFile.write("********************************************************************************")

        cov.stop()
        cov.save()

        #if CCreport.wasSuccessful():
        try:
            #print root
            if htmlReport:
                myHDrive = myConfig.get("Location","Root")
                myHHome = myConfig.get("Location","Home")
                myHSemester = myConfig.get("Location","Semester")
                myHAssignment = myConfig.get("Location","Assignment")
                HPath = os.path.join(myHDrive + os.sep + myHHome + os.sep + myHSemester + os.sep + myHAssignment + os.sep + stuName)
                if not (os.path.exists(HPath)):
                    os.mkdir(HPath)
                pctg = cov.html_report(directory=HPath)
            with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+"):

                outfile = open(os.path.join(paths[SUBPATH] + assignment + paths[FILENAME] + ".cvg"), "a+")
                pctg = cov.report(file=outfile)
                outfile.close()

            pctg = cov.report(omit=[paths[TESTPATH]])
            #print pctg
            #raw_input("Continue (success)?")
            return pctg, stuName
        except CoverageException as ce:
            print "CoverageException testpath:  " + paths[TESTPATH] + "\t" + str(ce)
            with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("CoverageException " + str(ce) + "\n\r")
                CCreportoutFile.write("********************************************************************************")
            #raw_input("Continue (CoverageException)?")
            return -1, stuName

        else:
            print "Test cases not successful at " + paths[TESTPATH]
            with open(os.path.join(paths[SUBPATH] + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("Test cases not successful \n\r")
                CCreportoutFile.write("********************************************************************************")

            #raw_input("Continue (CCreport not successful)?")
            return -2, studentName[0]

    def runTATests(self, TAPath, prodPath, assignment):
        myTestLoader = unittest.TestLoader()
        sys.path.insert(0,prodPath)

        testSuite = myTestLoader.discover(TAPath,'*.py')
        with open(os.path.join(TAPath + assignment + ".TAreport"), "a+") as TAreportoutFile:
            try:
                TAreport = TextTestRunner().run(testSuite)
                TAreportoutFile.write("\n\rStudent submission path:  " + prodPath + "\n\r")
                TAreportoutFile.write("Number of tests run:  " + str(TAreport.testsRun) + "\n\r")
                if not TAreport.wasSuccessful():
                    TAreportoutFile.write("Content of TestRunner failures\r")
                    for failedTestCase, failure in TAreport.failures:
                        TAreportoutFile.write(str(failedTestCase) + failure + "\n\r")
                else:
                    TAreportoutFile.write("All tests completed successfully!\n\r")
            except Exception:
                TAreportoutFile.write("Import Error:  " + prodPath + "\n\r")

            TAreportoutFile.write("********************************************************************************\n\r")


if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)

    #print os.getcwd()
    myConfig = ConfigParser.ConfigParser()
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    TATestLocation = myConfig.get("TA Test Case Location", "Test Directory")

    myCodeCoverage = CodeCoverage()
    myCodeCoverage.namePathDepth = myConfig.getint("Location","Name Path Depth")

    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment+os.sep+myCodeCoverage.assignment+".cvgrpt"), "a+") as outFile :
        outFile.write("Module Name\t\tCode Coverage percentage\n\r")
    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myCodeCoverage.assignment+".CCreport"), "a+") as CCreportoutFile:
        CCreportoutFile.write("Run date/time:  " + time.strftime("%a, %d %b %Y %H:%M:%S")+"\n\r")

    if totalArgs > 1:
        dataFile = str(sys.argv[1])
        assignmentStr = str(sys.argv[2]).split(".")
        myCodeCoverage.assignment = assignmentStr[0]
        if str(sys.argv[3]) == "yes":
            htmlReport = True
        else:
            htmlReport = False 
    else:
        #dataFile = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
        dataFile = myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment + os.sep + "submissions" + os.sep + "xzw0059" +os.sep
        myCodeCoverage.assignment = myAssignment
        htmlReport = False
    '''
    myPct, sName = myCodeCoverage.analyzeCodeCoverage(dataFile,myCodeCoverage.assignment, htmlReport)
    print myPct, sName
    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment+os.sep+myCodeCoverage.assignment+".cvgrpt"), "a+") as outFile:
        if myPct < 0:
            outFile.write("\n\r" + sName + "\t\t" + errorDict[myPct])
        else:
            outFile.write("\n\r" + sName + "\t\t" + format(myPct, ".2f"))
    '''
    myCodeCoverage.runTATests(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + TATestLocation),
                              os.path.join(dataFile + os.sep + "softwareprocess"), myCodeCoverage.assignment)
