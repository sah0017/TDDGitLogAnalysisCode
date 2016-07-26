'''
Created on Jul 1, 2016

@author: susanha
'''
import sys, os, re, unittest, coverage
from unittest.runner import TextTestRunner
import inspect
import modulefinder
from coverage.misc import CoverageException

class CodeCoverage(object):
    def __init__(self):
        '''
        Constructor
        '''
        

    def analyzeCodeCoverage(self):
        myDrive = "g:\\"
    #printToFile = raw_input("Print output to file?  ")
        mySemester = "6700Spring16"
        myAssignment = "CA02"
        includePath = ""
        #myCoverageAnalysis = CodeCoverage()
        reportLocation = os.path.join(myDrive,"git\\",mySemester)
        coverageResultsList = {}
        resultoutFile = open(reportLocation + myAssignment + ".result", "w")
        for root, myDir, files in os.walk(myDrive + "git\\" + mySemester + "\\" + myAssignment + "\\submissions"):
            if re.search("test", root):
                includePath = ""
                if not re.search("__MACOSX",root):
                    nameSplit = root.split("\\")
                    if nameSplit[len(nameSplit)-1] == "__pycache__":
                        nameSplit = nameSplit[:len(nameSplit)-1]
                    print nameSplit
                    for i in range(0,len(nameSplit)-1):
                        includePath = includePath + nameSplit[i] + "\\"
                    print includePath
                    cov = coverage.Coverage(data_file="g:\\git\\6700Spring16\\CA02\\submissions\\CA02.cvg",include=root + "\\*.py", branch=True )
                    #testpath = root
                    #prodpath = root
                    #if not (re.search("test",self.root)):     
                    testpath = includePath+"test" 
                    #if not (re.search("prod",self.root)):  
                    prodpath = includePath + "prod"   
                    #cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
                    sys.path.insert(0,includePath)
                    sys.path.insert(0,prodpath)
                    sys.path.insert(0,testpath)
                    print sys.path
                    testfiles = os.listdir(testpath)                               
                    prodfiles = os.listdir(prodpath)                               
                    os.chdir(testpath)  
                    myTestLoader = unittest.TestLoader()  
                    test = re.compile(r"\b.py\b", re.IGNORECASE)          
                    testfiles = filter(test.search, testfiles)                     
                    prodfiles = filter(test.search, prodfiles)                     
                    filenameToModuleName = lambda f: os.path.splitext(f)[0]
                    moduleTestNames = map(filenameToModuleName, testfiles)   
                    moduleProdNames = map(filenameToModuleName, prodfiles)   
                    #try:      
                    modules = map(__import__, moduleProdNames)
                    #except ImportError:
                    #    return -2   
                    #for mn in moduleTestNames:
                    cov.start()
                    from importlib import import_module
                    for mpn in moduleProdNames:
                        import_module(mpn, 'Assignment')
                    
                    
                    load = myTestLoader.loadTestsFromNames(moduleTestNames)  
                    print load.countTestCases()
                    #cov.load()
                    result = TextTestRunner().run(load)
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
                            raw_input("Continue?")
                    else:
                        #return -1
                        raw_input("Continue?")
                    sys.path.remove(includePath)
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
    myCoverageAnalysis = CodeCoverage()

    myCoverageAnalysis.analyzeCodeCoverage()
    '''
    myCodeCoverage = CodeCoverage("g:\\git\\6700Spring16\\CA05\\submissions\\almohaimeedabdulaziz_3162651_74846339_asa0021CA05\\softwareProcess\\SoftwareProcess\\Assignment")
    myPct = myCodeCoverage.analyzeCodeCoverage()
    print myPct
    '''