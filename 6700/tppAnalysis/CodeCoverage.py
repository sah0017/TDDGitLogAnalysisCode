'''
Created on Jul 1, 2016

@author: susanha
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
        
    
           

    def analyzeCodeCoverage(self, root, assignment, htmlReport):
        print root
        submissionPath = ""
        nameSplit = root.split(os.sep)
        fileName = nameSplit[self.namePathDepth]
        submissionPath = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep)
        studentName = fileName.split("_")
        print studentName[0]
        prodpath = os.path.join(root + os.sep + "softwareprocess")
        if (os.path.exists(os.path.join(prodpath,"prod"))):  # there is a prod directory is under softwareprocess dir
            prodpath = os.path.join(prodpath + os.sep + "prod")
        testpath = os.path.join(root + os.sep + "test")
        if (os.path.exists(testpath)):      # test directory is off of the student ID directory
            testfiles = os.listdir(testpath)
        else:
            testpath = os.path.join(root + os.sep + "softwareprocess" + os.sep + "test")  # test directory is under softwareprocess dir
            testfiles = os.listdir(testpath)
        try:
            cov = coverage.Coverage(source=[prodpath],include="*.py", omit=[testpath], branch=True, cover_pylib=False )
            #cov = coverage.Coverage(source=[root])
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("\n\rStudent submission and path:  " + root + "\n\r")
            prodfiles = os.listdir(prodpath)
            sys.path.insert(0,root)
            sys.path.insert(0,prodpath)
            sys.path.insert(0,testpath)
            os.chdir(prodpath)

            myTestLoader = unittest.TestLoader()
            test = re.compile(r"\b.py\b", re.IGNORECASE)      # test is a compiled regular expression to search for python files
            testfiles = filter(test.search, testfiles)        # this will filter out any files that aren't python files
            prodfiles = filter(test.search, prodfiles)
            filenameToModuleName = lambda f: os.path.splitext(f)[0]  # this removes the python extension from test files
            moduleTestNames = map(filenameToModuleName, testfiles)
            #moduleProdNames = map(filenameToModuleName, prodfiles)

            cov.start()

        except Exception as e:
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,file=CCreportoutFile)
            #return -3, studentName[0]

        with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
            CCreportoutFile.write("Test File Names\n\r")
        for t in testfiles:
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                    CCreportoutFile.write(t + "\r")

        load = myTestLoader.loadTestsFromNames(moduleTestNames)
        CCreport = TextTestRunner().run(load)
        with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
            CCreportoutFile.write("Number of tests run:  " + str(CCreport.testsRun) + "\n\r")
            if not CCreport.wasSuccessful():
                CCreportoutFile.write("Content of TestRunner failures\r")
                for failedTestCase, failure in CCreport.failures:
                    CCreportoutFile.write(str(failedTestCase) + failure + "\n\r")
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
                HPath = os.path.join(myHDrive + os.sep + myHHome + os.sep + myHSemester + os.sep + myHAssignment + os.sep + studentName[0])
                if not (os.path.exists(HPath)):
                    os.mkdir(HPath)
                pctg = cov.html_report(directory=HPath)
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+"):

                outfile = open(os.path.join(submissionPath + assignment + fileName + ".cvg"), "a+")
                pctg = cov.report(file=outfile)
                outfile.close()

            pctg = cov.report(omit=[testpath])
            #print pctg
            #raw_input("Continue (success)?")
            return pctg, studentName[0]
        except CoverageException as ce:
            print "CoverageException testpath:  " + testpath + "\t" + str(ce)
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("CoverageException " + str(ce) + "\n\r")
                CCreportoutFile.write("********************************************************************************")
            #raw_input("Continue (CoverageException)?")
            return -1, studentName[0]

        else:
            print "Test cases not successful at " + testpath
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("Test cases not successful \n\r")
                CCreportoutFile.write("********************************************************************************")

            #raw_input("Continue (CCreport not successful)?")
            return -2, studentName[0]

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

    myPct, sName = myCodeCoverage.analyzeCodeCoverage(dataFile,myCodeCoverage.assignment, htmlReport)
    print myPct, sName
    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment+os.sep+myCodeCoverage.assignment+".cvgrpt"), "a+") as outFile:
        if myPct < 0:
            outFile.write("\n\r" + sName + "\t\t" + errorDict[myPct])
        else:
            outFile.write("\n\r" + sName + "\t\t" + format(myPct, ".2f"))
    

