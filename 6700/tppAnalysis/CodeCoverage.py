'''
Created on Jul 1, 2016

@author: susanha
'''
import sys, os, re, unittest, coverage
from unittest.runner import TextTestRunner
from coverage.misc import CoverageException
import time, traceback
from contextlib import contextmanager
from py._iniconfig import SectionWrapper
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
        
    
           

    def analyzeCodeCoverage(self, root, assignment):
        try:
            submissionPath = ""
            cov = coverage.Coverage(data_file=root+".cvg",include=root + os.sep + "*.py", branch=True )
            nameSplit = root.split(os.sep)
            fileName = nameSplit[5]
            submissionPath = os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep)
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("\n\rStudent submission and path:  " + root + "\n\r")
            studentName = fileName.split("_")
            testpath = os.path.join(root + os.sep + "test") 
            prodpath = os.path.join(root + os.sep + "prod")  
            sys.path.insert(0,root)
            sys.path.insert(0,prodpath)
            sys.path.insert(0,testpath)
            testfiles = os.listdir(testpath)                               
            prodfiles = os.listdir(prodpath)  
            os.chdir(testpath)  
            myTestLoader = unittest.TestLoader()  
            test = re.compile(r"\b.py\b", re.IGNORECASE)          
            testfiles = filter(test.search, testfiles)                     
            prodfiles = filter(test.search, prodfiles)                     
            filenameToModuleName = lambda f: os.path.splitext(f)[0]
            moduleTestNames = map(filenameToModuleName, testfiles)   
            #moduleProdNames = map(filenameToModuleName, prodfiles)   
            cov.start()
            '''
            from importlib import import_module
            '''
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("Test Names\n\r")
            for mtn in moduleTestNames:
                with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                    CCreportoutFile.write(mtn + "\r")
            
            
            load = myTestLoader.loadTestsFromNames(moduleTestNames)  
        except Exception as e:
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,file=CCreportoutFile)
            return -3, studentName[0]
        
        CCreport = TextTestRunner().run(load)
        with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
            CCreportoutFile.write("Number of tests run:  " + str(CCreport.testsRun) + "\n\r")
            if not CCreport.wasSuccessful():
                CCreportoutFile.write("Content of TestRunner failures\r")
                for failedTestCase, failure in CCreport.failures:
                    CCreportoutFile.write(str(failedTestCase) + failure + "\n\r")
        cov.stop()
        cov.save()
            
        if CCreport.wasSuccessful():
            try:
                #print root
                #cov.html_report(directory=root)
                with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as f, redirect_stdout(f):
                    pctg = cov.report()
                print pctg
                #raw_input("Continue (success)?")
                return pctg, studentName[0]
            except CoverageException:
                print "CoverageException testpath" + testpath 
                with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                    CCreportoutFile.write("CoverageException \n\r")
                #raw_input("Continue (CoverageException)?")
                return -1, studentName[0]
        else:
            print "Test cases not successful at " + testpath 
            with open(os.path.join(submissionPath + assignment + ".CCreport"), "a+") as CCreportoutFile:
                CCreportoutFile.write("Test cases not successful \n\r")
            
            #raw_input("Continue (CCreport not successful)?")
            return -2, studentName[0]
        

if __name__ == '__main__':
    totalArgs = len(sys.argv)
    args = str(sys.argv)
    
    print os.getcwd()
    myConfig = ConfigParser.ConfigParser() 
    myConfig.read("TDDanalysis.cfg")
    myDrive = myConfig.get("Location","Root")
    myHome = myConfig.get("Location","Home")
    mySemester = myConfig.get("Location","Semester")
    myAssignment = myConfig.get("Location","Assignment")
    
    myCodeCoverage = CodeCoverage()
    '''
    with open("g:\\git\\6700Spring16\\"+myCodeCoverage.assignment+"\\"+myCodeCoverage.assignment+".cvgrpt", "w") as outFile :
        outFile.write("Module Name\t\tCode Coverage percentage\n\r")
    with open("g:\\git\\6700Spring16\\"+myCodeCoverage.assignment+"\\"+myCodeCoverage.assignment+".CCreport", "w") as CCreportoutFile:
        CCreportoutFile.write("Run date/time:  " + time.strftime("%a, %d %b %Y %H:%M:%S")+"\n\r")
    '''
    if totalArgs > 1:
        dataFile = str(sys.argv[1])
        myCodeCoverage.assignment = str(sys.argv[2])
    else:
        #dataFile = "g:\\git\\6700Spring16\\CA03\\submissions\\yanyufei_late_3331231_73091650_yzy0050CA03\\SoftwareProcess\\SoftwareProcess\\Assignment\\"
        dataFile = "g:\\git\\6700Spring16\\CA05\\submissions\\bakerthomas_late_1313011_74933289_thb0008CA05\\Software_Process03\\Software_Process03\\Assignment\\"
        myCodeCoverage.assignment = myAssignment
    print ("Datafile location is : %s" % dataFile)
    
    myPct, sName = myCodeCoverage.analyzeCodeCoverage(dataFile,myCodeCoverage.assignment)
    print myPct, sName
    with open(os.path.join(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment+os.sep+myCodeCoverage.assignment+".cvgrpt"), "a+") as outFile:
        if myPct < 0:
            outFile.write("\n\r" + sName + "\t\t" + errorDict[myPct])
        else:
            outFile.write("\n\r" + sName + "\t\t" + format(myPct, ".2f"))
    

    