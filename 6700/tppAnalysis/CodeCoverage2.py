'''
Created on Jul 1, 2016

@author: susanha
'''
import ConfigParser
import sys, os, re, unittest, coverage
from unittest import TextTestRunner
import TextTestResultWithSuccesses
import inspect
import modulefinder
from coverage.misc import CoverageException


class CodeCoverage(object):
    def __init__(self):
        '''
        Constructor
        '''
        

    def analyzeCodeCoverage(self, myDrive, myHome, mySemester, myAssignment):
        #myCoverageAnalysis = CodeCoverage()
        reportLocation = os.path.join(myDrive, myHome, mySemester)
        coverageResultsList = {}
        resultoutFile = open(reportLocation + os.sep + myAssignment + ".result", "w")
        for root, myDir, files in os.walk(myDrive + os.sep + myHome + os.sep + mySemester + os.sep + myAssignment + os.sep + "submissions"):
            if re.search("test", root):
                includePath = ""
                if not re.search("__MACOSX",root):
                    nameSplit = root.split(os.sep)
                    if nameSplit[len(nameSplit)-1] == "__pycache__":
                        nameSplit = nameSplit[:len(nameSplit)-1]
                    print nameSplit
                    for i in range(0,len(nameSplit)-1):
                        includePath = includePath + nameSplit[i] + os.sep
                    print includePath
                    cov = coverage.Coverage(config_file=False, source=includePath, branch=True )
                    #testpath = root
                    prodpath = includePath
                    #if not (re.search("test",self.root)):     
                    testpath = includePath+"test" 
                    if (re.search("prod",root)):
                        prodpath = includePath + "prod"
                        sys.path.insert(0,prodpath)
                    #cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
                    sys.path.insert(0,includePath)
                    sys.path.insert(0,testpath)
                    print sys.path
                    testfiles = os.listdir(testpath)                               
                    prodfiles = os.listdir(prodpath)
                    os.chdir(testpath)  
                    myTestLoader = unittest.TestLoader()
                    suite = myTestLoader.discover(testpath, pattern="*Test.py")
                    '''
                    test = re.compile(r"\b.py\b", re.IGNORECASE)          
                    testfiles = filter(test.search, testfiles)                     
                    prodfiles = filter(test.search, prodfiles)                     
                    filenameToModuleName = lambda f: os.path.splitext(f)[0]
                    moduleTestNames = map(filenameToModuleName, testfiles)   
                    moduleProdNames = map(filenameToModuleName, prodfiles)
                    '''
                    #try:      
                    #modules = map(__import__, moduleProdNames)
                    #except ImportError:
                    #    return -2   
                    #for mn in moduleTestNames:
                    cov.start()
                    '''
                    from importlib import import_module
                    for mpn in moduleProdNames:
                        import_module(mpn, 'Assignment')

                    
                    load = myTestLoader.loadTestsFromNames(moduleTestNames)  
                    print load.countTestCases()
                    '''
                    #cov.load()

                    #testResult = TextTestResultWithSuccesses()
                    testRunner = unittest.runner.TextTestRunner(verbosity=0)
                    result = testRunner.run(suite)
                    resultoutFile.write(includePath + "\n\r")
                    resultoutFile.write(str(result.testsRun) + "\n\r")
                    for failedTestCase, failure in result.failures:
                        resultoutFile.write(str(failedTestCase) + failure + "\n\r")
                    '''
                    f, s, excluded, missing, m = cov.analysis2('g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\prod\\Fix.py')
                    print "file name:  " + f, "\n\rline numbers of executable statements:  " + str(s).strip('[]'), "\n\rline numbers of excluded statements:  "+str(excluded).strip('[]'), "\n\rline numbers missing from execution:  "+str(missing).strip('[]'), "\n\rstring with missing line numbers:  "+m
                     
                    
                    for fn in moduleTestNames:
                        if fn != "__init__.py":
                            f, s, excluded, missing, m = cov.analysis2('g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\test\\' + fn + '.py')
                            print "file name:  " + f, "\n\rline numbers of executable statements:  " + str(s).strip('[]'), "\n\rline numbers of excluded statements:  "+str(excluded).strip('[]'), "\n\rline numbers missing from execution:  "+str(missing).strip('[]'), "\n\rstring with missing line numbers:  "+m
                    for fn in prodfiles:
                        if fn != "__init__.py":
                            f, s, excluded, missing, m = cov.analysis2('g:\\git\\6700Spring16\\CA05\\submissions\\danieljames_1246453_74826857_jhd0008\\softwareProcess\\SoftwareProcess\\Assignment\\prod\\' + fn)
                            print "file name:  " + f, "\n\rline numbers of executable statements:  " + str(s).strip('[]'), "\n\rline numbers of excluded statements:  "+str(excluded).strip('[]'), "\n\rline numbers missing from execution:  "+str(missing).strip('[]'), "\n\rstring with missing line numbers:  "+m
                    '''
                    cov.stop()
                    if result.wasSuccessful():
                        cov.save()
                        try:
                            cov.html_report(ignore_errors=True)
                
                            pctg = cov.report()
                            fileName = nameSplit[6]
                            studentName = fileName.split("_")
                            coverageResultsList[studentName[0]] = pctg
                            print pctg
                            #return pctg
                        except CoverageException:
                            #return -1
                            raw_input("Continue after Coverage Exception?")
                    else:
                        #return -1
                        raw_input("Continue after test failure?")
                    sys.path.remove(includePath)
                    if (re.search("prod",root)):
                        sys.path.remove(prodpath)
                    sys.path.remove(testpath)
                    print sys.path

        
        outFile = open(reportLocation + myAssignment + ".cvg", "w")
        outFile.write("Module Name\t\tCode Coverage percentage\n\r")
        for studentNm in coverageResultsList:
            outFile.write("\n\r" + studentNm + "\t\t" + format(coverageResultsList[studentNm], ".2f"))
                    
        outFile.close()
        resultoutFile.close()
        
    def createCoverageAnalysisReport(self):
        
        myDrive = "g:\\"
    #printToFile = raw_input("Print output to file?  ")
        mySemester = "6700Spring16\\"
        myAssignment = "CA02"
        includePath = ""
        #myCoverageAnalysis = CodeCoverage()
        reportLocation = os.path.join(myDrive,"git\\",mySemester)
        outFile = open(reportLocation + myAssignment + ".cvg", "w")
        outFile.write("Module Name\t\tCode Coverage percentage\n\r")
        for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myAssignment + "\\submissions"):
            if re.search("test", root):
                if not re.search("__MACOSX",root):
                    nameSplit = root.split("\\")
                    if nameSplit[len(nameSplit)-1] == "__pycache__":
                        nameSplit = nameSplit[:len(nameSplit)-1]
                    print nameSplit
                    for i in range(0,len(nameSplit)-1):
                        includePath = includePath + nameSplit[i] + "\\"
                    print includePath
                    myCCPct = myCoverageAnalysis.analyzeCodeCoverage(includePath, myAssignment)
                    fileName = nameSplit[6]
                    studentName = fileName.split("_")
                    outFile.write("\n\r" + studentName[0] + "\t\t" + format(myCCPct, ".2f"))
                    includePath = ""
        outFile.close()


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
    myCoverageAnalysis = CodeCoverage()

    myCoverageAnalysis.analyzeCodeCoverage(myDrive, myHome, mySemester, myAssignment)
    '''
    myCodeCoverage = CodeCoverage("g:\\git\\6700Spring16\\CA05\\submissions\\almohaimeedabdulaziz_3162651_74846339_asa0021CA05\\softwareProcess\\SoftwareProcess\\Assignment")
    myPct = myCodeCoverage.analyzeCodeCoverage()
    print myPct
    '''
